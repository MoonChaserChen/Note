import json

j = json.loads('{"id": 12, "name": "akira", "school": {"id": 123, "name": "华强北大学"}}')
school_name = j["school"]["name"]
s = json.dumps(j, ensure_ascii=False)


class School:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Person:
    def __init__(self, id, name, school):
        self.id = id
        self.name = name
        self.school = school


_school = School(123, "华强北大学")
_person = Person(12, "akira", _school)
s = json.dumps(_person, default=lambda o: o.__dict__, ensure_ascii=False, indent=4)
p = Person(**json.loads(s))
