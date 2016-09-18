import json
import os
import numpy as np


class SubjectSave(object):

    def __init__(self, key, type, classJson, ):
        self.id = key
        self.hours = classJson
        self.type = type


class GetSubject(object):
    def __init__(self):
        # -------#Subject get#------- #
        with open(os.getcwd() + "/json/Subjects/Template.json") as subject_file:
            self.subject = json.load(subject_file)
        # -------#Subject get#------- #

    def Names(self):  # Returns all subject name list
        self.list = []
        for x in range(self.subject["Subject"].__len__()):
            self.list.append(self.subject["Subject"][x]["ID"])
        return self.list  # Returns list of subject ID's

    def All(self):
        subjectArray = []
        for x in range(self.subject["Subject"].__len__()):
            subjectArray.append(SubjectSave(self.subject["Subject"][x]["ID"],
                                            self.subject["Subject"][x]["Type"],
                                            self.subject["Subject"][x]["Class"]))
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
        # -------#Students get#------- #
        with open(os.getcwd() + "/json/Students/Students.json") as student_file:
            self.student = json.load(student_file)
        # -------#Students get#------- #

    def All(self):  # Gets all the students
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
        # -------#Teacher get#------- #
        with open(os.getcwd() + "/json/Teachers/Teachers.json") as teacher_file:
            self.teacher = json.load(teacher_file)
        # -------#Teacher get#------- #

    def All(self):
        for x in range(self.teacher["Teacher"].__len__()):
            self.teacherArray.append(TeacherSave(self.teacher["Teacher"][x]["name"],
                                                 self.teacher["Teacher"][x]["subject"],
                                                 self.teacher["Teacher"][x]["available"]))
        return self.teacherArray


class LimitGet():

    def __init__(self):
        # -------#Limits get#------- #
        with open(os.getcwd() + "/json/Limits/LessonLimit.json") as limit_file:
            self.limitFile = json.load(limit_file)
        # -------#Limits get#------- #

    def MaxHours(self):
        return self.limitFile["max"]

    def MinHours(self):
        return self.limitFile["min"]

    def MaxLessons(self):
        return self.limitFile["weekly"]


class SaveSPS(object):  # Refactored

    def __init__(self, subject, classN, level=None):
        # -------#Limits get#------- #
        with open(os.getcwd() + "/json/Limits/LessonLimit.json") as limit_file:
            self.limitFile = json.load(limit_file)
        # -------#Limits get#------- #

        # -------#Teacher get#------- #
        with open(os.getcwd() + "/json/Teachers/Teachers.json") as teacher_file:
            self.teacher = json.load(teacher_file)
        self.teachers = []
        # -------#Teacher get#------- #
        self.id = subject["ID"]                     # ID of subject. Ex: "LT", "MAT", ...
        self.grade = classN                         # The grade of this subject [1, 2, 3, 4]
        self.level = level                          # The level of this subject: None if [1, 2]   [A, B] if [3, 4]
        self.list = subject[str(self.grade)]        # List of all students who have chosen this subject
        if self.level is not None:                  # Checks if json needs additional level
            self.list = self.list[self.level]
        self.size = self.size()                     # Amount of students enrolled in subject
        self.groups = self.groups()                 # List of groups and their sizes (numerical values)
        self.available_list = self.available_count()# Returns list of available teachers for subject for each day
        self.hours = self.get_hours()               # Returns the amount of hours/week for this subject, grade and level

    def get_hours(self):
        subjects = GetSubject().All()
        for subject in subjects:
            if self.id == subject.id:
                ret = subject.hours[str(self.grade)]
                if self.level is not None:
                    ret = ret[self.level]
                return ret["Hours"]

    def size(self):
        return self.list.__len__()

    def max_group(self):
        for x in range(self.limitFile["subjectSpecific"].__len__()):
            if self.id == self.limitFile["subjectSpecific"][x]["ID"]:
                return self.limitFile["subjectSpecific"][x]["max"]
        return 30

    def min_group(self):
        for x in range(self.limitFile["subjectSpecific"].__len__()):
            if self.id == self.limitFile["subjectSpecific"][x]["ID"]:
                return self.limitFile["subjectSpecific"][x]["min"]
        return 15

    def groups(self):  # Creates array of class sizes [28, 27, 27, ...] [min
        studentSize = self.size
        devider = self.max_group()
        classAmount = studentSize / devider
        # DEBUG: print(studentSize, "/", devider, " = ", classAmount)
        if not classAmount.is_integer() or classAmount == 0:
            classAmount += 1
        classAmount = int(classAmount)
        filler = int(studentSize / classAmount)
        if classAmount > 1:
            classArray = np.full(classAmount, filler, dtype=int)
            difference = studentSize - filler * classAmount
            i = 0
            while difference != 0:
                classArray[i] += 1
                i += 1
                if i == classAmount:
                    i = 0
                difference -= 1
        else:
            classArray = [studentSize]
        return list(classArray)

    def available_count(self):  # Teacher Availability for certain subject during the week
         # (Shows how many teachers are available for a certain subject each day of the week)
        self.count = [0, 0, 0, 0, 0]
        for x in range(self.teacher["Teacher"].__len__()):
            if self.teacher["Teacher"][x]["subject"] == self.id:
                for z in range(self.teacher["Teacher"][x]["available"].__len__()):
                    self.count[self.teacher["Teacher"][x]["available"][z] - 1] += 1
        return self.count  # Returns teacher amount for the subject for the day

    def available_day(self, day):  # Sees the list of free teachers for selected day
        # (Lesson availability data is not provided)
        # function(subject of choice, day of choice, ||provide load data)
        self.count = 0
        for x in range(self.teacher["Teacher"].__len__()):
            if self.teacher["Teacher"][x]["subject"] == self.id:
                for z in range(self.teacher["Teacher"][x]["available"].__len__()):
                    if self.teacher["Teacher"][x]["available"][z] == day:
                        self.teachers.append(self.teacher["Teacher"][x]["name"])
        return self.teachers  # Returns list of teachers


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