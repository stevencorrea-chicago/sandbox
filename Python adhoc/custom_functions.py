def custom_range(start, end):
    return range(start, end+1)

def add_nums(*args):
    sum = 0
    exception_list = []
    for value in args:
        if isinstance(value, int) or isinstance(value, float):
            sum += value
        else:
            exception_list.append(f"Value '{value}' is not numeric.")
    return (sum, exception_list)