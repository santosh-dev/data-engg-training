def make_upper(function):
    def upper():
        f= function()
        print("this is the origin value:{f}")
        return f.upper()
    return upper

@make_upper
def helloworld():
    return "welcome"

print(helloworld())