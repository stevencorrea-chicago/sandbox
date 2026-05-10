import json

def return_num(num, order='ascending'):
    if isinstance(num, int):
        num = str(num)

    # if (num[0] == num[1] and num[0] == num[2]) or \
    #     (num[1] == num[2] and num[1] == num[3]) :
    #     print(f"Cannot use {num}")
    #     return None
    # else:
    if order.lower() == 'ascending':
        return_value = list(num) 
        return_value.sort()
    elif order.lower() == 'descending':
        return_value = list(num) 
        return_value.sort(reverse=True)
    
    
    return int(''.join(return_value))


def find_kaprekars_num(num):
    global counter
    kaprekars_const = 6174
    low = return_num(num)

    if low:
        high = return_num(num, 'descending')
        if high - low == 6174:
            return (counter, kaprekars_const)
        else:
            counter += 1
            return find_kaprekars_num(str(high-low))
    else:
        return (counter, None)

# numbers = ['1114', '8743', '9012', '0388']
numbers = [f"{i:04d}" for i in range(0, 10000)
           if len(set(f"{i:04d}")) > 1]
numbers.sort()

output_to_file = []
counter_occurences = {}
for num in numbers:
    counter = 1  
    count, kaprekars_constant = find_kaprekars_num(num)
    if kaprekars_constant:
        output_to_file.append((f"{count},{kaprekars_constant}\n"))
        counter_occurences[count] = counter_occurences.get(count, 0) + 1

with open('kaprekars_constant_output.txt', 'w') as f:
    f.writelines(output_to_file)

print(json.dumps(counter_occurences, indent=2))
