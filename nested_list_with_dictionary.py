nested2 = [{'a': 1, 'b': 3}, {'a': 5, 'c': 90, 5: 50}, {'b': 3, 'c': "yes"}]

#write code to print the value associated with key 'c' in the second dictionary (90)
print(nested2[1]['c'])

#write code to print the value associated with key 'b' in the third dictionary
print(nested2[2]['b'])

#add a fourth dictionary add the end of the list; print something to check your work.
nested2.append({'python':10,'rocks':20})
print(nested2[3]['python'])

#change the value associated with 'c' in the third dictionary from "yes" to "no"; print something to check your work
nested2[2]['c'] = "no"
print(nested2[2]['c'])


d = {'key1': {'a': 5, 'c': 90, 5: 50}, 'key2':{'b': 3, 'c': "yes"}}
#d[5] = {1: 2, 3: 4}
#d[{1:2, 3:4}] = 5
#d['key1']['d'] = d['key2']
d[key2] = 3
