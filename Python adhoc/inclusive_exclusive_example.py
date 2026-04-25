from custom_functions import custom_range
from custom_functions import add_nums

# for number in custom_range(1,10):
#     print(number, end=" ")

value_list = [1,2,3,4,5,6,7,8,9]
sum, exception_list = add_nums(*value_list)

if sum:
    print(f"Sum: {sum}")

if exception_list:
    print(exception_list)