def print_combined_first_and_last_digits(file_path):
    total_sum = 0
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()  # Remove any leading/trailing whitespace
                digits = [char for char in line if char.isdigit()]
                if digits:
                    combined_number = int(digits[0] + digits[-1])
                    total_sum += combined_number
                    print(f"Line: {line}")
                    print(f"First digit: {digits[0]}, Last digit: {digits[-1]}")
                    print(f"Combined number: {combined_number}")
                    print(f"All digits: {', '.join(digits)}\n")
                else:
                    print(f"Line: {line}")
                    print("No digits found in the line\n")
        print(f"Total sum of combined numbers: {total_sum}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")

# Specify the path to your text file
file_path = 'input.txt'

# Call the function
print_combined_first_and_last_digits(file_path)
