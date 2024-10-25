def power2(val:int)->int:
    return val*val

def square(val:int)->int:
    return val*2

numbers = [1,2,3,4,5]

power_numbers = list(map(power2,numbers))

square_numbers = list(map(lambda x: x**2,numbers))

print(power_numbers,square_numbers)