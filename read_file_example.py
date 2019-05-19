openedFile = open("travel_plans2.txt",'r')

num_lines = 0

for lines in openedFile:
    num_lines += 1
    
print (num_lines)
openedFile.close()
