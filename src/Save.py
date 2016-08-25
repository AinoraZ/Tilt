import json
import copy
import os

class SubjectSave (object):

    def __init__(self):
        with open(os.getcwd() + "/json/Subjects/Template.json") as subject_file:
            self.subject = json.load(subject_file)
        with open(os.getcwd() + "/json/Subjects/Template.json") as subject_file2:
            self.subjectCopy = json.load(subject_file2)

    def SubjectAdd(self, ID, Priority, First, Two, ThreeA, ThreeB, FourA, FourB):

        for x in range(self.subject["Subject"].__len__()):
            if self.subject["Subject"][x]["ID"] == ID:
                print("Error, maybe class already exists? (ERROR: Subject add)")
                return -1

        self.template = self.subject["Subject"][0]
        self.templateCopy = self.subjectCopy["Subject"][0]
        self.template["ID"] = ID
        self.template["Priority"] = Priority
        self.template["Class"]["1"]["Hours"] = First
        self.template["Class"]["2"]["Hours"] = Two
        self.template["Class"]["3"]["A"]["Hours"] = ThreeA
        self.template["Class"]["3"]["B"]["Hours"] = ThreeB
        self.template["Class"]["4"]["A"]["Hours"] = FourA
        self.template["Class"]["4"]["B"]["Hours"] = FourB
        self.subjectCopy["Subject"].append(self.template)
        self.subjectCopy["Subject"][0] = self.templateCopy

        with open(os.getcwd() + "/json/Subjects/Template.json", 'w') as json_data:
            json_data.write(
                json.dumps(self.subjectCopy, sort_keys = True, indent = 2, separators = (',', ': '))
            )

        return 0

    def SubjectRemove(self, subject):
        self.found = False

        for x in range(self.subject["Subject"].__len__()):
            if self.subject["Subject"][x]["ID"] == subject:
                del self.subject["Subject"][x]
                self.found = True
                break
        if self.found == False:
            print("No such element, perhaps it doesn't exists? (ERROR SubjectRemove)")
            return -1

        with open(os.getcwd() + "/json/Subjects/Template.json", 'w') as json_data:
            json_data.write(
                json.dumps(self.subject,sort_keys = True, indent = 2, separators = (',', ': '))
            )

    def HourChange(self, subject, ID = "", Priority = "", First = -1, Two = -1, ThreeA = -1, ThreeB = -1, FourA = -1, FourB = -1):
        self.exists = False
        for x in range(self.subject["Subject"].__len__()):
            if self.subject["Subject"][x]["ID"] == subject:
                self.exists = True
                self.template = self.subject["Subject"][x]
                if ID != "":
                    self.template["ID"] = ID
                if Priority != "":
                    self.template["Priority"] = Priority
                if First != -1:
                    self.template["Class"]["1"]["Hours"] = First
                if Two != -1:
                    self.template["Class"]["2"]["Hours"] = Two
                if ThreeA != -1:
                    self.template["Class"]["3"]["A"]["Hours"] = ThreeA
                if ThreeB != -1:
                    self.template["Class"]["3"]["B"]["Hours"] = ThreeB
                if FourA != -1:
                    self.template["Class"]["4"]["A"]["Hours"] = FourA
                if FourB != -1:
                    self.template["Class"]["4"]["B"]["Hours"] = FourB

                self.subjectCopy["Subject"][x] = self.template
                break

        if self.exists == False:
            print("Error, maybe given subject doesn't exist? (ERROR: HourChange)")
            return -1

        with open(os.getcwd() + "/json/Subjects/Template.json", 'w') as json_data:
            json_data.write(
                json.dumps(self.subjectCopy, sort_keys = True, indent = 2, separators = (',', ': '))
            )

#SubjectSave().SubjectAdd("LOL", "LOL", 4, 6, 10, 20, 40, 80)
#SubjectSave().SubjectRemove("LOL")
#SubjectSave().HourChange("LT")

class StudentSave(object):

    def __init__(self):
        with open(os.getcwd() + "/json/Students/Students.json") as student_file:
            self.student = json.load(student_file)
        pass

    def StudentAdd(self, classN, name, subjectList):
        self.template = copy.copy(self.student["Students"][0])

        for x in range(self.student["Students"].__len__()):
            if self.student["Students"][x]["name"] == name:
                print("Warning, Student with same name exists (WARNING: StudentAdd)")
                break

        self.template["class"] = classN
        self.template["name"] = name
        self.template["subjects"] = subjectList

        self.student["Students"].append(self.template)
        with open(os.getcwd() + "/json/Students/Students.json", 'w') as json_data:
            json_data.write(
                json.dumps(self.student, sort_keys = True, indent = 2, separators = (',', ': '))
            )

    def StudentRemove(self, number):
        del self.student["Students"][number]

        with open(os.getcwd() + "/json/Students/Students.json", 'w') as json_data:
            json_data.write(
                json.dumps(self.student, sort_keys = True, indent = 2, separators = (',', ': '))
            )



class TeacherSave(object):
    pass

class LessonLimitSave(object):
    pass

#StudentSave().StudentAdd(3, "Ainoras Zukauskas", ["LTa", "MATa", "ISTa", "PROGa", "MUZb", "CHEa", "ENa", "FIZa", "KUN"])
#StudentSave().StudentRemove(7)