def print_separator(text):
    total_length = 80
    length_of_asterisks = (total_length - len(text) - 2) // 2
    print("*" * length_of_asterisks + f" {text.upper()} " + "*" * length_of_asterisks)