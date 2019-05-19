lst = [1,2,3,4,5,6,7,8,9,10]

for num in lst:
    lf = lambda num : num**2
    print(lf(num))

def together(num, string, optional = ""):
    value =  optional.join((str(num), string))
    print (value)

together(2, 'how are you', '!')


def greeting(name, greeting="Hello ", excl="!"):
    return greeting + name + excl

print(greeting("Bob"))
print(greeting(""))
print(greeting("Bob", excl="!!!"))
