import Open
import json
import copy
import os
from progress.bar import Bar
import numpy as np
os.chdir('..')


class SPS(object):
    def __init__(self):
        self.per = 0
        self.perCopy = 0
        self.Load()
        self.subjectList = Open.GetSubject().Names()

    def Load(self):
        with open(os.getcwd() + "/json/StudentsPerSubject/StudentsPerSubject.json") as per_file:
            self.per = json.load(per_file)
        with open(os.getcwd() + "/json/StudentsPerSubject/StudentsPerSubject.json") as per_file2:
            self.perCopy = json.load(per_file2)

    def Reset(self):  # Resets to default backup json
        with open(os.getcwd() + "/json/StudentsPerSubject/StudentsPerSubjectBackup.json") as perBackup:
            self.perBackup = json.load(perBackup)

        with open(os.getcwd() + "/json/StudentsPerSubject/StudentsPerSubject.json", 'w') as json_data:
            json_data.write(
                json.dumps(self.perBackup, sort_keys = True, indent = 4, separators = (',', ': '))
            )

    def Template(self):  # Creates templates for every subject in /Subjects/Template.json
        self.template = copy.copy(self.per["Per"][0])
        for x in range(self.subjectList.__len__()):
            if x < self.perCopy["Per"].__len__():
                self.perCopy["Per"][x]["ID"] = self.subjectList[x]
            else:
                self.template["ID"] = self.subjectList[x]
                self.perCopy["Per"].append(copy.copy(self.template))

        with open(os.getcwd() + "/json/StudentsPerSubject/StudentsPerSubject.json", 'w') as json_data:
            json_data.write(
                json.dumps(self.perCopy, sort_keys = True, indent = 4, separators = (',', ': '))
            )
        self.Load()
        self.Create()

    def Create(self):  # Goes through every Student, and places their names in appropriate subjects
        # Ex: LT has ["Ainoras Zukauskas", "Domantas Mauruca", ...]
        students = Open.GetStudent().All()
        bar = Bar('Creating SPS Json', max=students.__len__())
        for x in range(students.__len__()):
            for z in range(students[x].subjects.__len__()):
                for i in range(self.per["Per"].__len__()):
                    if self.per["Per"][i]["ID"] == students[x].subjects[z]:
                        if students[x].classN == 1:
                            self.per["Per"][i]["1"].append(students[x].name)
                        elif students[x].classN == 2:
                            self.per["Per"][i]["2"].append(students[x].name)
                    elif self.per["Per"][i]["ID"] + "a" == students[x].subjects[z]:
                        if students[x].classN == 3:
                            self.per["Per"][i]["3"]["A"].append(students[x].name)
                        elif students[x].classN == 4:
                            self.per["Per"][i]["4"]["A"].append(students[x].name)
                    elif self.per["Per"][i]["ID"] + "b" == students[x].subjects[z]:
                        if students[x].classN == 3:
                            self.per["Per"][i]["3"]["B"].append(students[x].name)
                        elif students[x].classN == 4:
                            self.per["Per"][i]["4"]["B"].append(students[x].name)
            bar.next()
        with open(os.getcwd() + "/json/StudentsPerSubject/StudentsPerSubject.json", 'w') as json_data:
            json_data.write(
                json.dumps(self.per, sort_keys = True, indent = 2, separators = (',', ': '))
            )
        bar.finish()


class RandClass(object):
    def __init__(self):
        self.Save()
        self.groups = []

    def Size(self, classN):    # Creates array of class sizes [28, 27, 27, ...] [min
        studentSize = Open.GetStudent().AllClass(classN).__len__()
        devider = 30
        classAmount = studentSize / devider
        if not classAmount.is_integer():
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

    def Reset(self):
        with open(os.getcwd() + "/json/Groups/Groups.json") as groups:
            groups = json.load(groups)
            for x in range(1, 5):
                groups["Class"][str(x)] = []
            with open(os.getcwd() + "/json/Groups/Groups.json", 'w') as json_data:
                json_data.write(
                    json.dumps(groups, sort_keys = True, indent = 2, separators = (',', ': '))
                )

    def Save(self):    # Saves computer generated classes to Groups.json
        # Open GroupsBackup.Json
        with open(os.getcwd() + "/json/Groups/GroupsBackup.json") as groups:
            self.groups = json.load(groups)
        # Reset Classes in Group.json
        self.Reset()
        # Places classes
        for x in range(1, 5):
            classes = self.Size(x)  # Creates an array containing class sizes
            until = 97 + len(classes)
            alphabet = list(map(chr, range(97, until)))  # Creates alphabetical list for classes [a, b, c, ...]
            template = copy.copy(self.groups["Class"][str(x)][0])  # Copies in a template from GroupsBackup.json
            self.groups["Class"][str(x)] = []
            getStudent = 0
            students = Open.GetStudent().All()
            for i, alpha in enumerate(alphabet):    # Works with the classes and places students in the templates
                template["ID"] = alpha.upper()
                for student in range(0, classes[i]):
                    template["students"].append(students[getStudent].name)
                    getStudent += 1
                self.groups["Class"][str(x)].append(template)
        # Saving
        with open(os.getcwd() + "/json/Groups/Groups.json", 'w') as json_data:
            json_data.write(
                json.dumps(self.groups, sort_keys = True, indent = 2, separators = (',', ': '))
            )


class PrematureGen(object):

    def __init__(self):
        pass

    def calculate(self):
        pass


print("Starting")
SPS().Reset()
print("ResetDone")
SPS().Template()
print("Templating Done")
subjects = Open.SPSGet(3).All()
print(subjects[2].groups)
print(subjects[0].hours)
RandClass()


