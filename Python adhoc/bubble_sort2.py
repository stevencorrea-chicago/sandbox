import random
import time

random_numbers = [ random.randint(1, 1000) for _ in range(1, 5000) ]


print(f"Unsorted list: {random_numbers[0:5]} ... {random_numbers[-5:-1]}")

start_time = time.time()
random_numbers.sort()
end_time = time.time()
print(f"Sorted list: {random_numbers[0:5]} ... {random_numbers[-5:-1]}")
print(f"Time taken: {end_time - start_time} seconds")