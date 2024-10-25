from jinja2 import Template

class Person:
    def __init__(self,name,age):
        self.age = age
        self.name = name
    def getAge(self):
        return self.age
    def getName(self):
        return self.name

person = Person('Peter',34)
person_dict = {'name':'David','age':35}
tm = Template("my name is {{ per.getName()}} and my age is {{per.getAge()}}")
tm2 = Template("my name is {{ per.name}} and my age is {{per.age}}")
msg = tm.render(per=person)
msg2 = tm2.render(per=person_dict)
print(msg)
print(msg2)