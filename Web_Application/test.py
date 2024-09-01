import sys

def add_half(input_value):
    try:
        number = float(input_value)
        result = number + 0.5
        return result
    except ValueError:
        return "Invalid input. Please enter a numeric value."


if len(sys.argv) > 1:
    input_value = sys.argv[1]
    output_value = add_half(input_value)
    print(output_value)
else:
    print("Please provide an input value.")
