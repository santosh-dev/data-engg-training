from jinja2 import Template
ename = input("enter your name:")
tm = Template("Hello {{name}}") 
msg = tm.render(name=ename)
print(msg)