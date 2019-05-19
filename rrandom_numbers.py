import random

lst = []

for i in range(250):
    diceThrow = random.randrange(1,250)
    if diceThrow in lst:
        pass
    else:
        lst.append(diceThrow)

print(sorted(lst))

print("\nLength of lst is", len(lst))
