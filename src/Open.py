import json
import os


class SubjectSave(object):

    def __init__(self, key, priority, classJson):
        # -------#Limits get#-------#
        with open(os.getcwd() + "/json/Limits/LessonLimit.json") as limit_file:
            self.limitFile = json.load(limit_file)
        # -------#Limits get#-------#

        # -------#Teacher get#-------#
        with open(os.getcwd() + "/json/Teachers/Teachers.json") as teacher_file:
            self.teacher = json.load(teacher_file)
        self.teachers = []
        # -------#Teacher get#-------#

        self.id = key
        self.priority = priority
        self.grade1 = classJson["1"]["Hours"]
        self.grade2 = classJson["2"]["Hours"]
        self.grade3A = classJson["3"]["A"]["Hours"]
        self.grade3B = classJson["3"]["B"]["Hours"]
        self.grade4A = classJson["4"]["A"]["Hours"]
        self.grade4B = classJson["4"]["B"]["Hours"]

    def MaxGroup(self):
        for x in range(self.limitFile["subjectSpecific"].__len__()):
            if self.id == self.limitFile["subjectSpecific"][x]["ID"]:
                return self.limitFile["subjectSpecific"][x]["max"]
    def MinGroup(self):
        for x in range(self.limitFile["subjectSpecific"].__len__()):
            if self.id == self.limitFile["subjectSpecific"][x]["ID"]:
                return self.limitFile["subjectSpecific"][x]["min"]

    def AvailableCount(self): # Teacher Availability for certain subject during the week
        # (Shows how many teachers are available for a certain subject each day of the week)
        # function(subject of choice, ||provide load data)
        self.count = [0, 0, 0, 0, 0]
        for x in range(self.teacher["Teacher"].__len__()):
            if self.teacher["Teacher"][x]["subject"] == self.id:
                for z in range(self.teacher["Teacher"][x]["available"].__len__()):
                    self.count[self.teacher["Teacher"][x]["available"][z] - 1] += 1
        return self.count  # Returns teacher amount for the subject for the day

    def AvailableDay(self, day):  # Sees the list of free teachers for selected day
        # (Lesson availability data is not provided)
        # function(subject of choice, day of choice, ||provide load data)
        self.count = 0
        for x in range(self.teacher["Teacher"].__len__()):
            if self.teacher["Teacher"][x]["subject"] == self.id:
                for z in range(self.teacher["Teacher"][x]["available"].__len__()):
                    if self.teacher["Teacher"][x]["available"][z] == day:
                        self.teachers.append(self.teacher["Teacher"][x]["name"])
        return self.teachers  # Returns list of teachers

    def StudentCount(self, classN, type = 'C'): #Counts the amount of Students who chose the subject for the class group
                                                # function(subject of choice, class of choice[1,2,3,4], type["A", "B"] ||provide load data)
        self.type = ""
        if classN > 2:                                  #Type only needed for classN[3,4]
            self.type = type
            if self.type not in ["a", "b", "A", "B"]:   #Returns error -1 if type is not [A,B]
                print("Wrong type choice, returned -1 (StudentSubjectCount)")
                return -1
            self.type = self.type.upper()

        self.count = 0
        for x in range(self.student["Students"].__len__()):
            if self.student["Students"][x]["class"] == classN:
                for z in range(self.student["Students"][x]["subjects"].__len__()):
                    if self.student["Students"][x]["subjects"][z].upper() == self.id + self.type:
                        self.count += 1
        return self.count                                           #Returns the student count for the subject



class GetSubject(object):
    def __init__(self):
        #-------#Subject get#-------#
        with open(os.getcwd() + "/json/Subjects/Template.json") as subject_file:
            self.subject = json.load(subject_file)
        #-------#Subject get#-------#

    def Names(self):                                          #Returns all subject name list
        self.list = []
        for x in range(self.subject["Subject"].__len__()):
            self.list.append(self.subject["Subject"][x]["ID"])
        return self.list                                            #Returns list of subject ID's

    def All(self):
        subjectArray = []
        for x in range(self.subject["Subject"].__len__()):
            subjectArray.append(SubjectSave(self.subject["Subject"][x]["ID"], self.subject["Subject"][x]["Priority"], self.subject["Subject"][x]["Class"]))
        return subjectArray


class StudentSave(object):
    def __init__(self, name, subjects, classN, letter):
        self.name = name
        self.subjects = subjects
        self.classN = classN
        self.letter = letter



class GetStudent(object):
    def __init__(self, subject = -1, classN = -1):
        self.students = []
        #-------#Students get#-------#
        with open(os.getcwd() + "/json/Students/Students.json") as student_file:
            self.student = json.load(student_file)
        #-------#Students get#-------#

    def All(self): #Gets all the students
        self.tempName = ""
        self.tempSubject = []
        for x in range(self.student["Students"].__len__()):
            self.tempSubject = []
            self.tempName = self.student["Students"][x]["name"]
            for z in range(self.student["Students"][x]["subjects"].__len__()):
                self.tempSubject.append(self.student["Students"][x]["subjects"][z])
            self.students.append(StudentSave(self.tempName, self.tempSubject, self.student["Students"][x]["class"], self.student["Students"][x]["letter"]))
        return self.students

    def AllClass(self, classN):
        list = []
        for student in self.All():
            if student.classN == classN:
                list.append(student)
        return list


class TeacherSave(object):
    def __init__(self, name, subject, available):
        self.name = name
        self.subject = subject
        self.available = available


class TeacherGet(object):

    def __init__(self):
        self.teacherArray = []
        #-------#Teacher get#-------#
        with open(os.getcwd() + "/json/Teachers/Teachers.json") as teacher_file:
            self.teacher = json.load(teacher_file)
        #-------#Teacher get#-------#

    def All(self):
        for x in range(self.teacher["Teacher"].__len__()):
            self.teacherArray.append(TeacherSave(self.teacher["Teacher"][x]["name"],
                                                 self.teacher["Teacher"][x]["subject"],
                                                 self.teacher["Teacher"][x]["available"]))
        return self.teacherArray

class LimitGet():

    def __init__(self):
        #-------#Limits get#-------#
        with open(os.getcwd() + "/json/Limits/LessonLimit.json") as limit_file:
            self.limitFile = json.load(limit_file)
        #-------#Limits get#-------#

    def MaxHours(self):
        return self.limitFile["max"]

    def MinHours(self):
        return self.limitFile["min"]

    def MaxLessons(self):
        return self.limitFile["weekly"]


class SaveSPS(object):

    def __init__(self, subject, classN, level=None):
        # -------#Limits get#-------#
        with open(os.getcwd() + "/json/Limits/LessonLimit.json") as limit_file:
            self.limitFile = json.load(limit_file)
        # -------#Limits get#-------#
        self.id = subject["ID"]
        self.grade = classN
        self.level = level
        self.list = subject[str(self.grade)]
        if self.level is not None:
            self.list = self.list[self.level]
        self.size = self.Size()
        self.groups = self.GroupRange()

    def Size(self):
        return self.list.__len__()

    def MaxGroup(self):
        for x in range(self.limitFile["subjectSpecific"].__len__()):
            if self.id == self.limitFile["subjectSpecific"][x]["ID"]:
                return self.limitFile["subjectSpecific"][x]["max"]
        return 30

    def MinGroup(self):
        for x in range(self.limitFile["subjectSpecific"].__len__()):
            if self.id == self.limitFile["subjectSpecific"][x]["ID"]:
                return self.limitFile["subjectSpecific"][x]["min"]
        return 15

    def GroupRange(self):
        groupMin = int(self.size / self.MaxGroup())
        groupMax = int(self.size / self.MinGroup())
        return [groupMin, groupMax]


class SPSGet(object):

    def __init__(self, classN):
        with open(os.getcwd() + "/json/StudentsPerSubject/StudentsPerSubject.json") as per_file:
            self.sps = json.load(per_file)
        self.classN = classN

    def All(self):
        SPSArray = []
        for subject in self.sps["Per"]:
            if self.classN <= 2:
                SPSArray.append(SaveSPS(subject, self.classN))
            else:
                SPSArray.append(SaveSPS(subject, self.classN, "A"))
                SPSArray.append(SaveSPS(subject, self.classN, "B"))
        return SPSArray




#print(GetSubject().SubjectName())
#print(GetSubject().SubjectPriority("GEF"))
#print(GetSubject().SubjectHours("LT", 3, "a"))
#print(GetStudent().Students()[0].name)
#print(GetStudent().Students()[0].subjects)
#print(GetStudent().Students()[0].classN)
#print(LimitGet().MaxHours())
#print(LimitGet().MinHours())
#print(LimitGet().MaxLessons())
#print(GetSubject().AllSubjects()[0].MaxGroup())