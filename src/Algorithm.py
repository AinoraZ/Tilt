import Open
import json
import copy
import os
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

        for x in range(Open.GetStudent().All().__len__()):
            for z in range(Open.GetStudent().All()[x].subjects.__len__()):
                for i in range(self.per["Per"].__len__()):
                    if self.per["Per"][i]["ID"] == Open.GetStudent().All()[x].subjects[z]:
                        if Open.GetStudent().All()[x].classN == 1:
                            self.per["Per"][i]["1"].append(Open.GetStudent().All()[x].name)
                        elif Open.GetStudent().All()[x].classN == 2:
                            self.per["Per"][i]["2"].append(Open.GetStudent().All()[x].name)
                    elif self.per["Per"][i]["ID"] + "a" == Open.GetStudent().All()[x].subjects[z]:
                        if Open.GetStudent().All()[x].classN == 3:
                            self.per["Per"][i]["3"]["A"].append(Open.GetStudent().All()[x].name)
                        elif Open.GetStudent().All()[x].classN == 4:
                            self.per["Per"][i]["4"]["A"].append(Open.GetStudent().All()[x].name)
                    elif self.per["Per"][i]["ID"] + "b" == Open.GetStudent().All()[x].subjects[z]:
                        if Open.GetStudent().All()[x].classN == 3:
                            self.per["Per"][i]["3"]["B"].append(Open.GetStudent().All()[x].name)
                        elif Open.GetStudent().All()[x].classN == 4:
                            self.per["Per"][i]["4"]["B"].append(Open.GetStudent().All()[x].name)
        with open(os.getcwd() + "/json/StudentsPerSubject/StudentsPerSubject.json", 'w') as json_data:
            json_data.write(
                json.dumps(self.per, sort_keys = True, indent = 4, separators = (',', ': '))
            )

    def GroupNumbers(self):
        pass


GroupSize().PerReset()
GroupSize().SPSTemplate()

