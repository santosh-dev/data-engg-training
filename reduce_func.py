from functools import reduce

def add(x:int,y:int):
    return x+y

numbers = [1,2,3,4,5]

sumofno = reduce(add,numbers,5)#reduce function func,sequenceof no, intializer(optional)

sumofno_without3rd = reduce(add,numbers)#reduce function without intializer

print(sumofno,sumofno_without3rd)