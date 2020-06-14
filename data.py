import pickle

TOKEN = ""                                          #BotToken

with open("token.p",'wb') as fh:
    pickle.dump(TOKEN,fh)

from models import *
limit = LimitCamp()

cat = limit.add_category(None)
vperms = {
    "verified" : {
        "read_messages": False,
        "send_messages": False,
        "send_tts_messages": False,
    },
    "@everyone" : {
        "read_messages": True,
        "send_messages": True,
        "send_tts_messages": True,
        "mention_everyone": True,
    },
}
cperms = dict.fromkeys(("Lecturer","Mentor","CoHost"),{
        "read_messages": True,
        "send_messages": True,
        "send_tts_messages": True,
        "mention_everyone": True,
    })
fperms = {
    "Student" : {
        "read_messages": True,
        "send_messages": True,
        "send_tts_messages": True,
        "embed_links": True,
        "attach_files": True,
        "read_message_history": True,
        "mention_everyone": True,
        "external_emojis": True,
        "add_reactions": True,
    }
}
cat.add_channels([
    ("text","admin",{},"Console for Admin Commands"),
    ("text","verify",vperms,"Verify Here: Use the command \"!verify <user id/roll no>\""),
    ("text","claim",cperms,"Claim Roles Here: Use the command \"!claim <user id>\""),
    ("text","feedback",fperms,"Feedback Channel")
])

perms = dict.fromkeys(("Lecturer","Mentor","CoHost"),{
        "read_messages": True,
        "send_messages": True,
        "send_tts_messages": True,
        "embed_links": True,
        "attach_files": True,
        "read_message_history": True,
        "mention_everyone": True,
        "external_emojis": True,
        "add_reactions": True,
        "connect": True,
        "speak": True,
        "stream": True,
        "use_voice_activation": True,
    })
cat = limit.add_category("Team Talk",perms)
cat.add_channels([
    ("text","text-chat",{},"Text Chat for LIMIT Team"),
    ("voice","Voice & Video Chat"),
])

perms_cat = dict.fromkeys(("Lecturer","Mentor","CoHost"),{
        "read_messages": True,
        "read_message_history": True,
    })
perms = {
    "Student Cat {category}" : {
        "read_messages": True,
        "read_message_history": True,
    }
}
cat1 = limit.add_category("Notifications",perms_cat)
cat2 = limit.add_category("Extras",perms_cat)
cat3 = limit.add_category("Lectures/Recordings",perms_cat)
perms_modA = {}
perms_modB = {}
for key in perms.keys():
    perms_modA[key.format(category="A")] = perms[key]
    perms_modB[key.format(category="B")] = perms[key]
cat1.add_channels([
    ("text","category-a",perms_modA,"Notifications for Category A will appear here"),
    ("text","category-b",perms_modB,"Notifications for Category B will appear here"),
])
cat2.add_channels([
    ("text","category-a",perms_modA,"Required Documents for Category A"),
    ("text","category-b",perms_modB,"Required Documents for Category B"),
])
cat3.add_channels([
    ("text","category-a",perms_modA,"All Lecture Videos/Recordings of Category A will appear here after the Camp is over for the Day"),
    ("text","category-b",perms_modB,"All Lecture Videos/Recordings of Category B will appear here after the Camp is over for the Day"),
])

#Students
limit.add_students([
    ("20A00000","A","Some StudentA"),               #Student Details
    ("20B00000","B","Some StudentB"),
])
perms = {
    "Student{type}" : {
        "read_messages": True,
        "send_messages": True,
        "send_tts_messages": True,
        "embed_links": True,
        "attach_files": True,
        "read_message_history": True,
        "mention_everyone": True,
        "external_emojis": True,
        "add_reactions": True,
        "connect": True,
        "speak": True,
        "stream": True,
        "use_voice_activation": True,
        "priority_speaker": True,
    },
}
perms_cat = dict.fromkeys(("Lecturer","Mentor","CoHost"),{
    "read_messages": True,
    "send_messages": True,
    "send_tts_messages": True,
    "embed_links": True,
    "attach_files": True,
    "read_message_history": True,
    "mention_everyone": True,
    "external_emojis": True,
    "add_reactions": True,
    "connect": True,
    "speak": True,
    "stream": True,
    "use_voice_activation": True,
    "priority_speaker": True,
    })
cat1 = limit.add_category("Sides",perms_cat)
cat2 = limit.add_category("Students Discussion")
cat3 = limit.add_category("Off Topic")
for cat in ['A','B','']:
    perms_mod = {}
    type = f" Cat {cat}" if cat!='' else ""
    for key in perms.keys():
        perms_mod[key.format(type=type)] = perms[key]
    name1 = f"category-{cat.lower()}" if cat!='' else "common"
    name2 = f"Category {cat}" if cat!='' else "Common"
    top1 = f"Chat for Sides of Category {cat}" if cat!='' else "Chat for Sides of All Students"
    top2 = f"Chat for Students of Category {cat}" if cat!='' else "Chat for All Students"
    cat1.add_channels([
        ("text",name1,perms_mod,top1),
    ])
    cat2.add_channels([
        ("text",name1,perms_mod,top2),
        ("voice",name2,perms_mod),
    ])
    cat3.add_channels([
        ("text",name1,perms_mod,"Off Topic "+top2),
    ])

#Lecturers
limit.add_lecturers([
    ("L00","Some Lecturer"),                        #Lecturer Details
])
limit.add_cohosts([
    ("H00","Some CoHost","L00"),                    #CoHost Details
])
colour = 0xf1c40f
limit.add_role("Lecturer",colour,True)
perms = {
    "{lecturer.lecturer_id}" : {
        "read_messages": True,
        "send_messages": True,
        "send_tts_messages": True,
        "manage_messages": True,
        "embed_links": True,
        "attach_files": True,
        "read_message_history": True,
        "mention_everyone": True,
        "external_emojis": True,
        "add_reactions": True,
        "connect": True,
        "speak": True,
        "stream": True,
        "mute_members": True,
        "deafen_members": True,
        "move_members": True,
        "use_voice_activation": True,
        "priority_speaker": True,
    },
    "{lecturer.cohost.cohost_id}" : {
        "read_messages": True,
        "send_messages": True,
        "send_tts_messages": True,
        "manage_messages": True,
        "embed_links": True,
        "attach_files": True,
        "read_message_history": True,
        "mention_everyone": True,
        "external_emojis": True,
        "add_reactions": True,
        "connect": True,
        "speak": True,
        "stream": True,
        "mute_members": True,
        "deafen_members": True,
        "move_members": True,
        "use_voice_activation": True,
        "priority_speaker": True,
    },
    "{student}" : {
        "read_messages": True,
        "send_messages": True,
        "send_tts_messages": True,
        "manage_messages": False,
        "embed_links": True,
        "attach_files": True,
        "read_message_history": True,
        "mention_everyone": True,
        "external_emojis": True,
        "add_reactions": True,
        "connect": True,
        "speak": True,
        "stream": True,
        "mute_members": False,
        "deafen_members": False,
        "move_members": False,
        "use_voice_activation": True,
        "priority_speaker": True,
    },
}
for lecturer in limit.lecturers:
    student = "Student Cat {category}"
    perms_mod1 = {}
    perms_mod2 = {}
    for key in perms.keys():
        try:
            perms_mod1[key.format(lecturer=lecturer,student=student)] = {}
            perms_mod2[key.format(lecturer=lecturer,student=student)] = perms[key]
        except:
            pass
    cat = limit.add_lcategory(f"Lecturer {lecturer.name}",perms_mod1,perms_mod2)
    cat.add_channels([
        ("text","lecturer-chat",{},"Chat for Lecture Purpose"),
        ("voice","Live Discussion"),
    ])
    limit.add_role(f"{lecturer.lecturer_id}",colour)

#Mentors
limit.add_mentors([
    ("M00","Some Mentor",("20A00000","20B00000")),  #Mentor Details
])
m_roles = []
m_st_roles = []
perms = {
    "{mentor.mentor_id}" : {
        "read_messages": True,
        "send_messages": True,
        "send_tts_messages": True,
        "manage_messages": True,
        "embed_links": True,
        "attach_files": True,
        "read_message_history": True,
        "mention_everyone": True,
        "external_emojis": True,
        "add_reactions": True,
        "connect": True,
        "speak": True,
        "stream": True,
        "mute_members": True,
        "deafen_members": True,
        "move_members": True,
        "use_voice_activation": True,
        "priority_speaker": True,
    },
    "{mentor.mentor_id} - Student" : {
        "read_messages": True,
        "send_messages": True,
        "send_tts_messages": True,
        "manage_messages": False,
        "embed_links": True,
        "attach_files": True,
        "read_message_history": True,
        "mention_everyone": True,
        "external_emojis": True,
        "add_reactions": True,
        "connect": True,
        "speak": True,
        "stream": True,
        "mute_members": False,
        "deafen_members": False,
        "move_members": False,
        "use_voice_activation": True,
        "priority_speaker": True,
    },
}
for mentor in limit.mentors:
    perms_mod = {}
    for key in perms.keys():
        perms_mod[key.format(mentor=mentor)] = perms[key]
    cat = limit.add_category(f"Mentor {mentor.name.split()[0]}",perms_mod)
    cat.add_channels([
        ("text","mentor-chat",{},"Chat for Mentoring Purpose"),
        ("voice","Live Discussion"),
    ])
    m_roles.append(f"{mentor.mentor_id}")
    m_st_roles.append(f"{mentor.mentor_id} - Student")
colour = 0x3498db
limit.add_role("Mentor",colour,True)
limit.add_roles([(t,colour) for t in m_roles])

colour = 0xc27c0e
limit.add_role("CoHost",colour,True)
for cohost in limit.cohosts:
    limit.add_role(f"{cohost.cohost_id}",colour)

colour = 0x1abc9c
limit.add_roles([
    ("Student",colour),
    ("Student Cat A",colour,True),
    ("Student Cat B",colour,True),
])
colour = 0x206694
limit.add_roles([(t,colour) for t in m_st_roles])

colour = 0x607d8b
limit.add_role("verified",colour,True,False)

cat = limit.add_category("Technical Assistance")
perms_lect = {
    "Lecturer" : {
        "read_messages": True,
        "send_messages": True,
        "send_tts_messages": True,
        "embed_links": True,
        "attach_files": True,
        "read_message_history": True,
        "mention_everyone": True,
        "external_emojis": True,
        "add_reactions": True,
    },
    "CoHost" : {
        "read_messages": True,
        "send_messages": True,
        "send_tts_messages": True,
        "embed_links": True,
        "attach_files": True,
        "read_message_history": True,
        "mention_everyone": True,
        "external_emojis": True,
        "add_reactions": True,
    }
}
perms_ment = {
    "Mentor" : {
        "read_messages": True,
        "send_messages": True,
        "send_tts_messages": True,
        "embed_links": True,
        "attach_files": True,
        "read_message_history": True,
        "mention_everyone": True,
        "external_emojis": True,
        "add_reactions": True,
    }
}
perms_std = {
    "Student" : {
        "read_messages": True,
        "send_messages": True,
        "send_tts_messages": True,
        "embed_links": True,
        "attach_files": True,
        "read_message_history": True,
        "mention_everyone": True,
        "external_emojis": True,
        "add_reactions": True,
    }
}
cat.add_channels([
    ("text","lecturers-cohosts",perms_lect,"Technical Assistance for Lectures & CoHosts"),
    ("text","mentors",perms_ment,"Technical Assistance for Mentors"),
    ("text","students",perms_std,"Technical Assistance for Students"),
])
perms_lect = {
    "Lecturer" : {
        "view_channel": True,
        "connect": True,
        "speak": True,
        "stream": True,
        "use_voice_activation": True,
    },
    "CoHost" : {
        "view_channel": True,
        "connect": True,
        "speak": True,
        "stream": True,
        "use_voice_activation": True,
    }
}
perms_ment = {
    "Mentor" : {
        "view_channel": True,
        "connect": True,
        "speak": True,
        "stream": True,
        "use_voice_activation": True,
    }
}
perms_std = {
    "Student" : {
        "view_channel": True,
        "connect": True,
        "speak": True,
        "stream": True,
        "use_voice_activation": True,
    }
}
cat.add_channels([
    ("voice","Lecturers & CoHosts",perms_lect),
    ("voice","Mentors",perms_ment),
    ("voice","Students",perms_std),
])

with open("data.p",'wb') as fh:
    pickle.dump(limit,fh)
