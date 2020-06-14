from models import *
import discord, asyncio, pickle
from discord.ext.commands import Bot
from datetime import datetime,timedelta
from sys import version

def time_now():
    return str(datetime.utcnow()+timedelta(hours=5.5))[:-7]
def get_token():
    with open("token.p",'rb') as fh:
        return pickle.load(fh)
    return None
def load_data():
    global limit
    limit = None
    with open("data.p",'rb') as fh:
        limit = pickle.load(fh)
    limit.last_time = time_now()
def dump_data():
    with open("data.p",'wb') as fh:
        pickle.dump(limit,fh)

def admin(unadmined):
    async def admined(ctx,*args,**kwargs):
        if str(ctx.channel) != "admin" or grole(ctx,"LIMIT Admin") not in ctx.author.roles:
            return
        await unadmined(ctx,*args,**kwargs)
    return admined
def grole(ctx,role):
    guild = ctx.guild
    if isinstance(role,str):
        return discord.utils.get(guild.roles, name=role)
    roles = []
    for r in role:
        roles.append(discord.utils.get(guild.roles, name=r))
    return roles
def gperms(ctx,perms):
    p = {}
    for role in perms.keys():
        p[grole(ctx,role)] = discord.PermissionOverwrite(**perms[role])
    return p

client = Bot('!')
client.last_time = time_now()

@client.command(name="verify")
async def verify(ctx,*args):
    if str(ctx.channel) != "verify":
        return
    if grole(ctx,"verified") in ctx.author.roles:
        return
    if not args:
        await ctx.send("Please Enter your user id/roll no in correct format: \"!verify <user id/roll no>\"")
        return
    persons = limit.get_persons(args)
    roles = []
    for person in persons:
        if person:
            roles.extend(grole(ctx,limit.get_roles(person)))
        else:
            await ctx.send("Invalid user id/roll no!")
            return
    nick = persons[0].name
    names = []
    for person in persons:
        if not person.name in names:
            names.append(person.name)
        if hasattr(person,'sname'):
            nick = person.sname
            break
    if len(names)!=1:
        await ctx.send("Invalid user id/roll no!")
        return
    await ctx.author.edit(nick=nick)
    for role in roles:
        await ctx.author.add_roles(role)
    await ctx.send(f"You have been Verified {ctx.author.mention}!")
    await asyncio.sleep(1)
    await ctx.author.add_roles(grole(ctx,"verified"))
@client.command(name="claim")
async def claim(ctx,*args):
    if str(ctx.channel) != "claim":
        return
    if not args:
        await ctx.send("Please Enter your user id in correct format: \"!claim <user id>\"")
        return
    persons = limit.get_persons(args)
    roles = []
    for person in persons:
        if person:
            roles.extend(grole(ctx,limit.get_roles(person)))
        else:
            await ctx.send("Invalid user id!")
            return
    names = []
    for person in persons:
        if not person.name in names:
            names.append(person.name)
    if len(names)!=1:
        await ctx.send("Invalid user id!")
        return
    for role in roles:
        await ctx.author.add_roles(role)
    await ctx.send(f"Claimed Roles have been added {ctx.author.mention}!")
@client.command(name="activate")
@admin
async def activate(ctx,*args):
    if not args or len(args)<2:
        await ctx.send("Please Enter correctly: \"!activate <user id of lecturer> <categories>\"")
        return
    lid = args[0]
    lecturer = limit.get_lecturer(lid)
    if not lecturer:
        await ctx.send("Invalid user id!")
        return
    cat = None
    for cat in limit.categories:
        if cat.name and cat.name.endswith(lecturer.name):
            break
    cat.activate(args[1:3])
    dump_data()
    await ctx.send(f"Lecturer {lid} has been activated! Please update channels! (!update channels)")
@client.command(name="deactivate")
@admin
async def deactivate(ctx,*args):
    lecturers = []
    if args:
        for lid in args:
            lecturer = limit.get_lecturer(lid)
            if not lecturer:
                await ctx.send(f"{lid} is an invalid user id!")
                continue
            lecturers.append(lecturer)
    else:
        lecturers = limit.lecturers
    if len(lecturers)==0:
        return
    vlids = []
    for lecturer in lecturers:
        cat = None
        vlids.append(lecturer.lecturer_id)
        for cat in limit.categories:
            if cat.name and cat.name.endswith(lecturer.name):
                break
        cat.deactivate()
    dump_data()
    await ctx.send(f"Lecturer {', '.join(vlids)} has been deactivated! Please update channels! (!update channels)")
@client.command(name="update")
@admin
async def update(ctx, arg=None):
    guild = ctx.guild
    if arg in ("roles","all",None):
        roles = limit.roles
        for i in range(len(roles)):
            rl = roles[i]
            role = grole(ctx,rl.name)
            if role:
                await role.edit(colour=discord.Colour(rl.colour), hoist=rl.hoist, mentionable=rl.mentionable, permissions=discord.Permissions(**rl.permission))
            else:
                role = await guild.create_role(name=rl.name, colour=discord.Colour(rl.colour), hoist=rl.hoist, mentionable=rl.mentionable, permissions=discord.Permissions(**rl.permission))
        roles = limit.roles[::-1]
        for i in range(len(roles)):
            rl = roles[i]
            role = grole(ctx,rl.name)
            await role.edit(position=i+1)
        await ctx.send("Updated Roles!")
    if arg in ("channels","all",None):
        for cat in limit.categories:
            if cat.name:
                category = discord.utils.get(guild.categories, name=cat.name)
                perms = gperms(ctx,cat.permissions)
                if category:
                    for role in perms:
                        await category.set_permissions(role, overwrite=perms[role])
                else:
                    category = await guild.create_category(cat.name, overwrites=perms)
                for chan in cat.text_channels:
                    channel = discord.utils.get(category.text_channels, name=chan.name)
                    # for channel in category.text_channels:
                    #     if str(channel) == chan.name:
                    #         break
                    perms = gperms(ctx,chan.permissions)
                    if channel:
                        await channel.edit(topic=chan.topic)
                        await channel.edit(sync_permissions=True)
                        for role in perms:
                            await channel.set_permissions(role, overwrite=perms[role])
                    else:
                        channel = await category.create_text_channel(chan.name, overwrites=perms, topic=chan.topic)
                for chan in cat.voice_channels:
                    channel = discord.utils.get(category.voice_channels, name=chan.name)
                    # for channel in category.voice_channels:
                    #     if str(channel) == chan.name:
                    #         break
                    perms = gperms(ctx,chan.permissions)
                    if channel:
                        await channel.edit(sync_permissions=True)
                        for role in perms:
                            await channel.set_permissions(role, overwrite=perms[role])
                    else:
                        channel = await category.create_voice_channel(chan.name, overwrites=perms)
            else:
                for chan in cat.text_channels:
                    channel = discord.utils.get(guild.text_channels, name=chan.name, category=None)
                    perms = gperms(ctx,chan.permissions)
                    if channel:
                        await channel.edit(topic=chan.topic)
                        await channel.edit(sync_permissions=True)
                        for role in perms:
                            await channel.set_permissions(role, overwrite=perms[role])
                    else:
                        channel = await guild.create_text_channel(chan.name, overwrites=perms, topic=chan.topic)
                for chan in cat.voice_channels:
                    channel = discord.utils.get(guild.voice_channels, name=chan.name, category=None)
                    perms = gperms(ctx,chan.permissions)
                    if channel:
                        await channel.edit(sync_permissions=True)
                        for role in perms:
                            await channel.set_permissions(role, overwrite=perms[role])
                    else:
                        channel = await guild.create_voice_channel(chan.name, overwrites=perms)
        await ctx.send("Updated Channels!")
@client.command(name="delete")
@admin
async def delete(ctx, arg=None):
    guild = ctx.guild
    if arg in ("roles","all",None):
        for role in guild.roles[1:-2]:
            await role.delete()
        await ctx.send("Deleted Roles!")
    if arg in ("channels","all",None):
        for channel in guild.text_channels:
            if channel == ctx.channel:
                continue
            await channel.delete()
        for channel in guild.voice_channels:
            await channel.delete()
        for category in guild.categories:
            await category.delete()
        await ctx.send("Deleted Channels!")
@client.command(name="load")
@admin
async def load(ctx):
    load_data()
    await ctx.send("Data Refreshed!")
@client.command(name="upload")
@admin
async def upload(ctx):
    await ctx.message.attachments[0].save("./data.p")
    await ctx.send("Uploaded!")
@client.command(name="download")
@admin
async def download(ctx):
    with open("data.p","rb") as fh:
        await ctx.send(file=discord.File(fh,"data.p"))
@client.command(name="ltime")
@admin
async def ltime(ctx):
    await ctx.send(f"Jarvis : {client.last_time}\nData : {limit.last_time}")
@client.command(name="specs")
@admin
async def specs(ctx):
    await ctx.send("Python : {0}\nDicord.py : {1.major}.{1.minor}.{1.micro} {1.releaselevel}".format(version,discord.version_info))
@client.command(name="lecture")
@admin
async def lecture(ctx,*args):
    if not args or len(args)<6:
        return
    cats = []
    p = 0
    while args[p] in "AB":
        cats.append(args[p])
        p+= 1
    if len(cats)<1:
        return
    mtid = args[p]
    pasw = args[p+1]
    url = args[p+2]
    timing = ' '.join(args[p+3:])
    guild = ctx.guild
    embed = discord.Embed(title="Live Lecture", description="Live Lecture has been Scheduled", color=0x00ff00)
    embed.add_field(name="Meeting ID", value=mtid, inline=True)
    embed.add_field(name="Meeting Password", value=pasw, inline=True)
    embed.add_field(name="Timing", value=timing, inline=True)
    embed.add_field(name="Meeting Link", value=url, inline=True)
    embed.set_image(url=ctx.message.attachments[0].url)
    for cat in cats:
        cat = cat.lower()
        channel = discord.utils.get(guild.text_channels, name=f"category-{cat}")
        await channel.send(embed=embed)
    await ctx.send("Notified!")
@client.command(name="qna")
@admin
async def qna(ctx,*args):
    if not args or len(args)<6:
        return
    cats = []
    p = 0
    while args[p] in "AB":
        cats.append(args[p])
        p+= 1
    if len(cats)<1:
        return
    mtid = args[p]
    pasw = args[p+1]
    url = args[p+2]
    timing = ' '.join(args[p+3:])
    guild = ctx.guild
    embed = discord.Embed(title="QnA Session", description="QnA Session has been Scheduled", color=0x00ff00)
    embed.add_field(name="Meeting ID", value=mtid, inline=True)
    embed.add_field(name="Meeting Password", value=pasw, inline=True)
    embed.add_field(name="Timing", value=timing, inline=True)
    embed.add_field(name="Meeting Link", value=url, inline=True)
    embed.set_image(url=ctx.message.attachments[0].url)
    for cat in cats:
        cat = cat.lower()
        channel = discord.utils.get(guild.text_channels, name=f"category-{cat}")
        await channel.send(embed=embed)
    await ctx.send("Notified!")
@client.command(name="recorded")
@admin
async def recorded(ctx,*args):
    if not args or len(args)<3:
        return
    cats = []
    p = 0
    while args[p] in "AB":
        cats.append(args[p])
        p+= 1
    if len(cats)<1:
        return
    url = args[p]
    timing = ' '.join(args[p+1:])
    guild = ctx.guild
    embed = discord.Embed(title="Lecture Video", description="New Lecture Video is available on YouTube", color=0x00ff00)
    embed.add_field(name="Timing", value=timing, inline=False)
    embed.add_field(name="Video Link", value=url, inline=False)
    embed.set_image(url=ctx.message.attachments[0].url)
    for cat in cats:
        cat = cat.lower()
        category = discord.utils.get(guild.categories, name="Notifications")
        channel = discord.utils.get(category.text_channels, name=f"category-{cat}")
        await channel.send(embed=embed)
    await ctx.send("Notified!")
@client.command(name="video")
@admin
async def video(ctx,*args):
    if not args or len(args)<4:
        return
    cats = []
    p = 0
    while args[p] in "AB":
        cats.append(args[p])
        p+= 1
    if len(cats)<1:
        return
    url = args[p]
    day = args[p+1]
    date = ' '.join(args[p+2:])
    guild = ctx.guild
    embed = discord.Embed(title="Lecture Video", description="Lecture Video has been uploaded", color=0x00ff00)
    embed.add_field(name="Day", value=f"Day {day}", inline=True)
    embed.add_field(name="Date", value=date, inline=True)
    embed.add_field(name="Video Link", value=url, inline=False)
    embed.set_image(url=ctx.message.attachments[0].url)
    for cat in cats:
        cat = cat.lower()
        category = discord.utils.get(guild.categories, name="Lectures/Recordings")

        channel = discord.utils.get(category.text_channels, name=f"category-{cat}")
        await channel.send(embed=embed)
    await ctx.send("Notified!")
@client.command(name="mail")
@admin
async def mail(ctx,*args):
    if not args:
        return
    lt = []
    if 'A' in args or 'a' in args:
        lt.extend([                         #Email ID of Category A Students
        'email1@gmail.com',
        'email2@gmail.com',
        ])
    if 'B' in args or 'b' in args:
        lt.extend([                         #Email ID of Category B Students
        'email3@gmail.com',
        'email4@gmail.com',
        ])
    if 'Team' in args or 'team' in args or 'Team' in args:
        lt.extend([                         #Email ID of LIMIT Team Members
        'arghyadip.chak16@gmail.com',
        'email5@gmail.com',
        ])send('\n'.join(lt))
@client.event
async def on_message(message):
    # try:
    await client.process_commands(message)
    # except:
    #     pass
@client.event
async def on_ready():
    guild = client.guilds[0]
    channel = discord.utils.get(guild.text_channels, name="admin")
    if channel:
        await channel.send("Hey I'm back Online and maybe now I'm a better version of myself!")
    print("Ready!")

TOKEN = get_token()
limit = None
load_data()

client.run(TOKEN)
