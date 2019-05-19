"""
print("This will execute first")

for _ in range(3):
    print("This line will execute three times")
    print("This line will also execute three times")
    
print("Now we are outside of the for loop")

import turtle
wn = turtle.Screen()

elan = turtle.Turtle()

distance = 50
angle = 90
for _ in range(16):
    elan.forward(distance)
    elan.right(angle)
    distance = distance + 10
    angle = angle - 3
"""
print("-"*20)

L = [0.34, '6', 'SI106', 'Python', -2]
L2 = L[1:-1]

for item in L2:
    print(item)

print("-"*20)

s = "python rocks"
print(s[3:8])

print("-"*20)

new_lst = ["computer", "luxurious", "basket", "crime", 0, 2.49, "institution", "slice", "sun", ["water", "air", "fire", "earth"], "games", 2.7, "code", "java", ["birthday", "celebration", 1817, "party", "cake", 5], "rain", "thunderstorm", "top down"]
sub_lst = new_lst[9:13]
print(sub_lst)

print("-"*20)

sports = ['cricket', 'football', 'volleyball', 'baseball', 'softball', 'track and field', 'curling', 'ping pong', 'hockey']
last = sports[-3:]
print(last)

print("-"*20)

by = "You are"
az = "doing a great "
io = "job"
qy = "keep it up!"

message = by + " " +az + io + " " + qy

print(message)

print("-"*20)

nums = [4, 2, 8, 23.4, 8, 9, 545, 9, 1, 234.001, 5, 49, 8, 9 , 34, 52, 1, -2, 9.1, 4]
print (nums)
nums = [4, 2, 8, 23.4, 8, 9, 545, 9, 1, 234.001, 5, 49, 8, 9 , 34, 52, 1, -2, 9.1, 4]
nums = nums[0:4] + nums[5:]
print (nums)

print("-"*20)

lst = ["hi", "goodbye", "python", "106", "506", 91, ['all', 'Paul', 'Jackie', "UMSI", 1, "Stephen", 4.5], 109, "chair", "pizza", "wolverine", 2017, 3.92, 1817, "account", "readings", "papers", 12, "facebook", "twitter", 193.2, "snapchat", "leaders and the best", "social", "1986", 9, 29, "holiday", ["women", "olympics", "gold", "rio", 21, "2016", "men"], "26trombones"]
num_lst = len(lst)

print("-"*20)

z = ['abracadabra', 4,'steve','nuetron', 6, 'proton', 4, 'electron', 4, 'electron', 'atoms']
count = 0
for item in range(len(z)):
    if isinstance(z[item],int):
        pass
    else:
        print(z[item].count('a'))

if 'steve' in z:
    print ("He's been found")
else:
    print ("Not here")

print("-"*20)

sports = ['cricket', 'football', 'volleyball', 'baseball', 'softball', 'track and field', 'curling', 'ping pong', 'hockey']
last = sports[-3:]
print(sports)
print(last)

print("-" * 20)

lst = ["swimming", 2, "water bottle", 44, "lollipop", "shine", "marsh", "winter", "donkey", "rain", ["Rio", "Beijing", "London"], [1,2,3], "gold", "bronze", "silver", "mathematician", "scientist", "actor", "actress", "win", "cell phone", "leg", "running", "horse", "socket", "plug", ["Phelps", "le Clos", "Lochte"], "drink", 22, "happyfeet", "penguins"]
output = lst[5:13]
print(output)
print("Length of output: ", len(output))

print("-"*20)

number = list(range(0,53))
print(number)
print("Length of number: ", len(number))

print("-"*20)

s = "python"
for idx in range(len(s)):
    print("idx: ", idx)
    print("idx % 2: ", idx % 2)
    print(s[idx % 2])

print("-"*20)

for i in range(3):
    for j in range(2):
        print(i, j)

print("-"*20)

str_list = ["hello", "", "goodbye", "wonderful", "I love Python"]

# Write your code here.
for item in str_list:
    print(len(item))

print("-"*20)

numbers = list(range(41))
print (numbers)

print("-"*20)

addition_str = "2+5+10+20"
lst = addition_str.split('+')
print (lst)
sum_val = 0
for item in lst:
    sum_val += int(item)
print ("Value of the sum: ", sum_val)


print("-"*20)

item = ["M", "I", "S", "S", "O", "U", "R", "I"]
for val in item:
    val = val + "!"
    print(val)


print("-"*20)

percent_rain = [94.3, 45, 100, 78, 16, 5.3, 79, 86]
resps = []

for each_percent in percent_rain:
    if each_percent > 90:
        resps.append("Bring an umbrella.")
    elif each_percent > 80:
        resps.append("Good for the flowers?")
    elif each_percent > 50:
        resps.append("Watch out for clouds!")
    else:
        resps.append("Nice day!")

    print (resps) 

print("-"*20)

nums = [9, 3, 8, 11, 5, 29, 2]
best_num = nums[0]
for n in nums:
    if n > best_num:
        best_num = n
        
print(best_num)


print("-"*20)

s = "We are learning!"
x = 0
for i in s:
    if i in ['a', 'b', 'c', 'd', 'e']:
        x += 1
print(x)


print("-"*20)

list= [5, 2, 1, 4, 9, 10]
min_value = 0
for item in list:
   if item < min_value:
       min_value = item
print(min_value)

print("-"*20)

sentence = "students flock to the arb for a variety of outdoor activities such as jogging and picnicking"

# Write your code here.
same_letter_count = 0
words_of_sentence = sentence.split(" ")

for sentence in words_of_sentence:
    if sentence[0] == sentence[-1]:
        same_letter_count += 1

print (same_letter_count)        

print("-"*20)

classes = ["MATH 150", "PSYCH 111", "PSYCH 313", "PSYCH 412", "MATH 300", "MATH 404", "MATH 206", "ENG 100", "ENG 103", "ENG 201", "PSYCH 508", "ENG 220", "ENG 125", "ENG 124"]
upper = []
lower = []


for cls in classes:
    cls_lst = cls.split(" ")
    if cls_lst[0] == "ENG":
        if int(cls_lst[1]) > 199:
            upper.append(cls)
        else:
            lower.append(cls)

    if cls_lst[0] == "PSYCH":
        if int(cls_lst[1]) > 399:
            upper.append(cls)
        else:
            lower.append(cls)
      
    if cls_lst[0] == "MATH":
        if int(cls_lst[1]) > 299:
            upper.append(cls)
        else:
            lower.append(cls)

print("upper: ",upper)
print("lower: ",lower)

print("-"*20)

myList = [76, 92.3, 'hello', True, 4, 76]

# Your code here
myList.append("apple")
myList.append(76)
myList.insert(2, "cat")
myList.insert(0, 99)
myList.index("hello")
myList.count(76)
myList.index(76)
myList.pop(myList.index(True))

print(myList)

print("-"*20)

import string
chars = ['h', '1', 'C', 'i', '9', 'True', '3.1', '8', 'F', '4', 'j']
nums = string.digits
is_num = []

for indx, char in enumerate(chars):
    if char in nums:
        myTuple = ((chars[indx],True))
    else:
        myTuple = ((chars[indx],False))

    is_num.append(myTuple)

print (is_num)


print("-"*20)

a = ["holiday", "celebrate!"]
quiet = a
quiet.append("company")
print(a)

print("-"*20)

sent = "Holidays can be a fun time when you have good company!"
phrase = sent
phrase = phrase + " Holidays can also be fun on your own!"
print(id(phrase))
print(id(sent))

print("-"*20)

sent = "The mall has excellent sales right now."
wrds = sent.split()
wrds[1] = 'store'
new_sent = " ".join(wrds)
print(new_sent)

print("-"*20)

stopwords = ['to', 'a', 'for', 'by', 'an', 'am', 'the', 'so', 'it', 'and', "The"]
org = "The organization for health, safety, and education"
org_lst = org.split(' ')
acro = ""
for word in org_lst:
    if word in stopwords:
        pass
    else:
        acro = acro + word[0].upper()
print (acro)

print("-"*20)

stopwords = ['to', 'a', 'for', 'by', 'an', 'am', 'the', 'so', 'it', 'and', 'The']
sent = "The water earth and air are vital"
sent_lst = sent.split(' ')
acro = ""
length = len(sent_lst)

for word in sent_lst:
    if word in stopwords:
        pass
    else:
        if word == sent_lst[-1]:
            acro = acro + word[:2].upper()
        else:
            acro = acro + word[:2].upper() + ". "
print (acro)

print("-"*20)

sentence = ' hello  apple'
print(sentence.replace(" ", ""))
print(sentence)


print("-"*20)


origlist = [45,32,88]
print("Initialized origlist with values", origlist)

aliaslist = origlist
print("aliaslist = ", aliaslist)
print("origlist = ", origlist)

print("Adding 'cat' to origlist")
origlist += ["cat"]

print("aliaslist now = ", aliaslist)
print("origlist now = ", origlist)

print("Adding 'cow' to origlist")
origlist = origlist + ["cow"]

print("aliaslist now = ", aliaslist)
print("origlist now = ", origlist)



print("-"*20)

winners = ['Alice Munro', 'Alvin E. Roth', 'Kazuo Ishiguro', 'Malala Yousafzai', 'Rainer Weiss', 'Youyou Tu']
z_winners = winners[::-1]
y_winners = sorted(winners)

print("z_winners", z_winners)
print("y_winners", y_winners)

print("-"*20)

inventory = ["shoes, 12, 29.99", "shirts, 20, 9.99", "sweatpants, 25, 15.00", "scarves, 13, 7.75"]

for item in inventory:
    split_item = item.split(",")
    store_item_desc = split_item[0]
    store_item_qnty = split_item[1]
    store_item_price = split_item[2]
    print("The store has{} {}, each for{} USD.".format(store_item_qnty,store_item_desc,store_item_price)) 

print("-"*20)

#import bisect 
#def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
#    i = bisect(breakpoints, score)
#    return grades[i]
#
#[grade(score) for score in [33, 99, 77, 70, 89, 90, 100]]

print("-"*20)

sent = "The mall has excellent sales right now."
wrds = sent.split()
wrds[1] = 'store'
new_sent = " ".join(wrds)
print(new_sent)

print("-"*20)

pirate_trans = {"sir":"matey",
"hotel":"fleabag inn",
"student":"swabbie",
"boy":"matey",
"madam":"proud beauty",
"professor":"foul blaggart",
"restaurant":"galley",
"your":"yer",
"excuse":"arr",
"students":"swabbies",
"are":"be",
"lawyer":"foul blaggart",
"the":"th’",
"restroom":"head",
"my":"me",
"hello":"avast",
"is":"be",
"man":"matey"}
user_input = "hello sir where is the hotel restaurant"
#user_input = input("Enter a sentence to be translated into Pirate: ")

translation = ""

english_to_pirate = user_input.split()

for english_word in english_to_pirate:
    if english_word in pirate_trans:
        translation = translation + pirate_trans[english_word] + " "
    else:
        translation = translation + english_word + " "

print(translation)

print("-"*20)

s = "python"
for idx in range(len(s)):
   print(s[idx % 2])

print("-"*20)

names_scores = [("Jack",[67,89,91]),("Emily",[72,95,42]),("Taylor",[83,92,86])]
for name, scores in names_scores:
    print("The scores {nm} got were: {s1},{s2},{s3}.".format(nm=name,s1=scores[0],s2=scores[1],s3=scores[2]))

    # this works
names = ["Jack","Jill","Mary"]
for n in names:
    print("'{}!' she yelled. '{}! {}, {}!'".format(n,n,n,"say hello"))

# but this also works!
names = ["Jack","Steve","Mary"]
for n in names:
    print("'{0}!' she yelled. '{0}! {0}, {1}!'".format(n,"say hello"))

print("-"*20)

x = 3
y = 5
z = 2
if x < y and x < z:
    print("a")
elif y < x and y < z:
    print("b")
else:
    print("c")
    
print("-"*20)

letters = "alwnfiwaksuezlaeiajsdl"
sorted_letters = sorted(letters)
print(sorted_letters)

print("-"*20)


animals = ['elephant', 'cat', 'moose', 'antelope', 'elk', 'rabbit', 'zebra', 'yak', 'salamander', 'deer', 'otter', 'minx', 'giraffe', 'goat', 'cow', 'tiger', 'bear']
animals_sorted = sorted(animals)
print(animals_sorted)

print("-"*20)

medals = {'Japan':41, 'Russia':56, 'South Korea':21, 'United States':121, 'Germany':42, 'China':70}

alphabetical = sorted(medals)
print(alphabetical)

print("-"*20)

medals = {'Japan':41, 'Russia':56, 'South Korea':21, 'United States':121, 'Germany':42, 'China':70}
medals_sorted = sorted(medals,reverse=True,key=lambda medal:medals[medal])
top_three = medals_sorted[:3]
print(top_three)

print("-"*20)

groceries = {'apples': 5, 'pasta': 3, 'carrots': 12, 'orange juice': 2, 'bananas': 8, 'popcorn': 1, 'salsa': 3, 'cereal': 4, 'coffee': 5, 'granola bars': 15, 'onions': 7, 'rice': 1, 'peanut butter': 2, 'spinach': 9}
most_needed = sorted(groceries,reverse=True,key=lambda grocery_item:groceries[grocery_item])
print(most_needed)
print("-"*20)

def last_four(x):
    x_str = str(x)
    lf = x_str[-4:]
    return(int(lf))


ids = [17573005, 17572342, 17579000, 17570002, 17572345, 17579329]
sorted_ids = sorted(ids, key=last_four)
print(sorted_ids)

print("-"*20)


ids = [17573005, 17572342, 17579000, 17570002, 17572345, 17579329]
sorted_ids = sorted(ids, key=lambda id:str(id)[-4:])
print(sorted_ids)

ex_lst = ['hi', 'how are you', 'bye', 'apple', 'zebra', 'dance']
lambda_sort = sorted(ex_lst,key=lambda x:x[1])
print(lambda_sort)

print("-" * 10)

def strip_punctuation(string):
    punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']
    for punctuation in punctuation_chars:
        if punctuation in string:
            string = string.replace(punctuation,"")
    return string

print(strip_punctuation('steven.correa@gmail.com'))
