#names_scores = [("Jack",[67,89,91]),("Emily",[72,95,42]),("Taylor",[83,92,86])]
#for name, scores in names_scores:
#    print("The scores {nm} got were: {s1},{s2},{s3}.".format(nm=name,s1=scores[0],s2=scores[1],s3=scores[2]))

    # this works
names = ["Jack","Jill","Mary"]
#for n in names:
#    print("'{}!' she yelled. '{}! {}, {}!'".format(n,n,n,"say hello"))

# but this also works!
# What was confusing at first for me was figuring out what 1 is for.  The section (n,"say hello") is parametized
# as input values for the curly braces in the string, so n comes from the for statement and 1 is "say hello"
names = ["Jack","Steve","Mary"]
for n in names:
    print("'{0}!' she yelled. '{0}! {0}, {1}!'".format(n,"say hello"))


names = ["Alexey", "Catalina", "Mitsuki", "Pablo"]
print("'{first}!' she yelled. 'Come here, {first}! {f_one}, {f_two}, and {f_three} are here!'".format(first = names[1], f_one = names[0], f_two = names[2], f_three = names[3]))

names = ["Alexey", "Catalina", "Mitsuki", "Pablo"]
print("'{}!' she yelled. 'Come here, {}! {}, {}, and {} are here!'".format(names[1], names[1],names[0], names[2], names[3]))
