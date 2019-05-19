import math

def Pythagorean_Theorem(a,b,c):
    if a == None:
        a = math.sqrt(c**2 - b**2)
        result = ("Square root of " + str(c) + " squared - " + str(b) + " squared equals " + str(a))
    elif b == None:
        b = math.sqrt(c**2 - a**2)
        result = ("Square root of " + str(c) + " squared - " + str(a) + " squared equals " + str(b))
    elif c == None:
        c = math.sqrt(a**2 + b**2)
        result = ("Square root of " + str(a) + " squared + " + str(b) + " squared equals " + str(c))
    else:
        return("Incorrect number of parameters passed into the function")

    return (result)

print(Pythagorean_Theorem(2,4,None))
print(Pythagorean_Theorem(16,None,45))
print(Pythagorean_Theorem(None,7,8))
