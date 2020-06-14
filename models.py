class Person:
    def __init__(self,id,name,roles=[]):
        self.id = id
        self.name = name
        self.roles = roles
class Student(Person):
    def __init__(self,rollno,cat,name,sname=None):
        Person.__init__(self,rollno,name,["Student",f"Student Cat {cat}"])
        self.rollno = rollno
        self.category = cat
        self.sname = sname if sname else name.split()[0]
        self.mentor = None
    def __str__(self):
        return str(self.rollno)
    def assign_mentor(self,mentor):
        self.mentor = mentor
        self.roles.append(f"{mentor.mentor_id} - Student")
class Mentor(Person):
    def __init__(self,mid,name,students=[]):
        Person.__init__(self,mid,name,["Mentor",f"{mid}"])
        self.mentor_id = mid
        self.students = students
        if students:
            for student in students:
                student.assign_mentor(self)
    def __str__(self):
        return str(self.mentor_id)
    def add_student(self,student):
        self.students.append(student)
        student.assign_mentor(self)
    def add_students(self,students):
        self.students.extend(students)
        for student in students:
            student.assign_mentor(self)
class Lecturer(Person):
    def __init__(self,lid,name):
        Person.__init__(self,lid,name,["Lecturer",f"{lid}"])
        self.lecturer_id = lid
        self.cohost = None
    def __str__(self):
        return str(self.lecturer_id)
    def assign_cohost(self,cohost):
        self.cohost = cohost
class CoHost(Person):
    def __init__(self,hid,name,lect):
        Person.__init__(self,hid,name,["CoHost",f"{hid}"])
        self.cohost_id = hid
        self.lecturer = lect
        lect.assign_cohost(self)
    def __str__(self):
        return str(self.lecturer_id)
class Role:
    def __init__(self,name,colour=None,hoist=False,ment=True,perm={}):
        self.name = name
        self.colour = colour
        self.hoist = hoist
        self.mentionable = ment
        self.permission = perm
    def __str__(self):
        return str(self.name)
class Category:
    def __init__(self,name,perms={}):
        self.name = name
        self.permissions = perms
        self.text_channels = []
        self.voice_channels = []
    def __str__(self):
        return str(self.name)
    def add_text_channel(self,name,perms={},topic=None):
        self.text_channels.append(TextChannel(self,name,perms,topic))
    def add_voice_channel(self,name,perms={}):
        self.voice_channels.append(VoiceChannel(self,name,perms))
    def add_channel(self,type,name,perms={},topic=None):
        if type == "text":
            self.add_text_channel(name,perms,topic)
        else:
            self.add_voice_channel(name,perms)
    def add_channels(self,lt):
        for l in lt:
            self.add_channel(*l)
def mod_perms(perms,cats):
    perms_mod = {}
    for key in perms.keys():
        if "{category}" in key:
            for cat in cats:
                perms_mod[key.format(category=cat)] = perms[key]
        else:
            perms_mod[key] = perms[key]
    return perms_mod
class LCategory(Category):
    def __init__(self,name,perms1={},perms2={}):
        self.perms = mod_perms(perms1,"AB")
        Category.__init__(self,name,self.perms)
        self.perms_alt = perms2
    def activate(self,cats=[]):
        self.permissions = mod_perms(self.perms_alt,cats)
    def deactivate(self):
        self.permissions = self.perms
class Channel:
    def __init__(self,category,type,name,perms={}):
        self.category = category
        self.type = type
        self.name = name
        self.permissions = perms
    def __str__(self):
        return str(self.name)
class TextChannel(Channel):
    def __init__(self,category,name,perms={},topic=None):
        Channel.__init__(self,category,"text",name,perms)
        self.topic = topic
class VoiceChannel(Channel):
    def __init__(self,category,name,perms={}):
        Channel.__init__(self,category,"voice",name,perms)
class LimitCamp:
    def __init__(self):
        self.students = []
        self.mentors = []
        self.lecturers = []
        self.cohosts = []
        self.roles = []
        self.categories = []
    def add_student(self,rollno,cat,name,sname=None):
        self.students.append(Student(rollno,cat,name,sname))
    def add_students(self,lt):
        for l in lt:
            self.add_student(*l)
    def add_mentor(self,mid,name,students=[]):
        tmp,students = students,[]
        for student in tmp:
            if isinstance(student,str):
                student = self.get_student(student)
            if student:
                students.append(student)
        self.mentors.append(Mentor(mid,name,students))
    def add_mentors(self,lt):
        for l in lt:
            self.add_mentor(*l)
    def add_lecturer(self,lid,name):
        self.lecturers.append(Lecturer(lid,name))
    def add_lecturers(self,lt):
        for l in lt:
            self.add_lecturer(*l)
    def add_cohost(self,hid,name,lecturer):
        if isinstance(lecturer,str):
            lecturer = self.get_lecturer(lecturer)
        self.cohosts.append(CoHost(hid,name,lecturer))
    def add_cohosts(self,lt):
        for l in lt:
            self.add_cohost(*l)
    def get_mentor(self,mid):
        for mentor in self.mentors:
            if mentor.mentor_id == mid:
                return mentor
        return None
    def get_student(self,rollno):
        for student in self.students:
            if student.rollno == rollno:
                return student
        return None
    def get_lecturer(self,lid):
        for lecturer in self.lecturers:
            if lecturer.lecturer_id == lid:
                return lecturer
        return None
    def get_cohost(self,hid):
        for cohost in self.cohosts:
            if cohost.cohost_id == hid:
                return cohost
        return None
    def get_person(self,id):
        person = self.get_mentor(id)
        if person:
            return person
        person = self.get_student(id)
        if person:
            return person
        person = self.get_lecturer(id)
        if person:
            return person
        person = self.get_cohost(id)
        return person
    def get_persons(self,ids):
        return list(map(lambda x: self.get_person(x),ids))
    def get_roles(self,obj):
        return obj.roles
    def add_role(self,name,colour=None,hoist=False,ment=True,perm={}):
        self.roles.append(Role(name,colour,hoist,ment,perm))
    def add_roles(self,lt):
        for l in lt:
            self.add_role(*l)
    def add_category(self,name,perms={}):
        self.categories.append(Category(name,perms))
        return self.categories[-1]
    def add_lcategory(self,name,perms1={},perms2={}):
        self.categories.append(LCategory(name,perms1,perms2))
        return self.categories[-1]
