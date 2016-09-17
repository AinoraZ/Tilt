import Open
import json
import copy
import os
from progress.bar import Bar
import numpy as np
os.chdir('..')

class Algorithm(object):

    def __init__(self):
        pass

    def Calculate(self):
        pass

class GroupSize(object):
    def __init__(self):
        self.per = 0
        self.perCopy = 0
        self.LoadFile()
        self.subjectList = Open.GetSubject().Names()

    def LoadFile(self):
        with open(os.getcwd() + "/json/StudentsPerSubject/StudentsPerSubject.json") as per_file:
            self.per = json.load(per_file)
        with open(os.getcwd() + "/json/StudentsPerSubject/StudentsPerSubject.json") as per_file2:
            self.perCopy = json.load(per_file2)

    def PerReset(self): #Resets to default backup json
        with open(os.getcwd() + "/json/StudentsPerSubject/StudentsPerSubjectBackup.json") as perBackup:
            self.perBackup = json.load(perBackup)

        with open(os.getcwd() + "/json/StudentsPerSubject/StudentsPerSubject.json", 'w') as json_data:
            json_data.write(
                json.dumps(self.perBackup, sort_keys = True, indent = 4, separators = (',', ': '))
            )

    def SPSTemplate(self): #Creates templates for every subject in /Subjects/Template.json
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
        self.LoadFile()
        self.SPSCreate()

    def SPSCreate(self): #Goes through every Student, and places their names in appropriate subjects
                                         #Ex: LT has ["Ainoras Zukauskas", "Domantas Mauruca", ...]
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

    def RandomizeClass(self):
        studentSize = Open.GetStudent().AllClass(3).__len__()
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

    def SaveRandClass(self):
        with open(os.getcwd() + "/json/Groups/Groups.json") as groups:
            self.groups = json.load(groups)
        classes = self.RandomizeClass()
        until = 97 + len(self.classes)
        alphabet = list(map(chr, range(97, until)))
        for i, alpha in enumerate(alphabet):
            print(alpha, i)

        with open(os.getcwd() + "/json/Groups/Groups.json", 'w') as json_data:
            json_data.write(
                json.dumps(self.per, sort_keys = True, indent = 2, separators = (',', ': '))
            )



print("Starting")
GroupSize().PerReset()
print("ResetDone")
GroupSize().SPSTemplate()
print("Templating Done")
print(Open.SPSGet(3).All()[0].groups)
GroupSize().SaveRandClass()

