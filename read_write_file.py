in_file = open("input.txt","r")
in_file2 = open("input2.txt","r")
out_file = open("output.txt","w")
out_file2 = open("output2.txt","w")

for value in in_file:
    result = int(value) * int(value) * int(value)
    out_file.write(str(result) + '\n')
    #file_obj.write('\n')
    
in_file.close()
out_file.close()

num = 1
while True:
    num = in_file2.read(1)
    print("Reading from input2.txt - value read from file is: ", num)
    if not num:
        print("Enf of file")
        break
    elif num == '\n':
        print("Input encountered a newline")
    else:
        result = int(num)** 5
        out_file2.write(str(result) + '\n')

in_file2.close()
out_file2.close()
"""
Example of alternate way to read files to not have to worry about explicity
closing the file

with <create some object that understands context> as <some name>:
    do some stuff with the object


with open('mydata.txt','r') as md:
    for line in md:
        print(line)

or

fname = 'mydata.txt'
with open(fname,'w') as md:
    for num in range(10):
        md.write(str(num))
        md.write('\n')


Here’s a foolproof recipe for processing the contents of a text file. If you’ve fully digested the previous sections, you’ll understand that there are other options as well. Some of those options are preferable for some situations, and some are preferred by python programmers for efficiency reasons. In this course, though, you can always succeed by following this recipe.

#1. Open the file using with and open.

#2. Use .readlines() to get a list of the lines of text in the file.

#3. Use a for loop to iterate through the strings in the list, each being one line from the file. On each iteration, process that line of text

#4. When you are done extracting data from the file, continue writing your code outside of the indentation. Using with will automatically close the file once the program exits the with block.

fname = "yourfile.txt"
with open(fname, 'r') as fileref:         # step 1
    lines = fileref.readlines()           # step 2
    for lin in lines:                     # step 3
        #some code that references the variable lin
#some other code not relying on fileref   # step 4
However, this will not be good to use when you are working with large data. Imagine working with a datafile that has 1000 rows of data. It would take a long time to read in all the data and then if you had to iterate over it, even more time would be necessary. This would be a case where programmers prefer another option for efficiency reasons.

This option involves iterating over the file itself while still iterating over each line in the file:

fname = "yourfile.txt"
with open(fname, 'r') as fileref:         # step 1
    for lin in fileref:                   # step 2
        ## some code that reference the variable lin
#some other code not relying on fileref   # step 3
"""
