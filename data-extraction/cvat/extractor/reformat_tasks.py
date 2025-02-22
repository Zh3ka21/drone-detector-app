import re

def extract_numbers(input_file, output_file):
    # Regular expression to find numbers, ignoring any surrounding characters
    number_pattern = r'[^\d]*(\d+)[^\d]*'
    
    # Open the input file and read all lines
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # List to hold the extracted numbers
    numbers = []

    # Iterate over each line in the input file
    for line in lines:
        # Find all numbers (ignoring occluding characters)
        found_numbers = re.findall(number_pattern, line)
        numbers.extend(found_numbers)

    # Write the numbers to the output file, two per line
    with open(output_file, 'w') as outfile:
        for i in range(0, len(numbers), 2):
            # Write two numbers per line, checking to avoid index out of range
            outfile.write(f"{numbers[i]} {numbers[i + 1] if i + 1 < len(numbers) else ''}\n")

def extract_numbers_for(input_file, output_file):
    # Regular expression to find numbers, ignoring any surrounding characters
    number_pattern = r'[^\d]*(\d+)[^\d]*'
    
    # Open the input file and read all lines
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # List to hold the extracted numbers
    numbers = []

    # Iterate over each line in the input file
    for line in lines:
        # Find all numbers (ignoring occluding characters)
        found_numbers = re.findall(number_pattern, line)
        numbers.extend(found_numbers)

    # Write the numbers to the output file, four per line
    with open(output_file, 'w') as outfile:
        for i in range(0, len(numbers), 4):
            # Write four numbers per line, checking to avoid index out of range
            outfile.write(f"{numbers[i]} {numbers[i + 1] if i + 1 < len(numbers) else ''} "
                          f"{numbers[i + 2] if i + 2 < len(numbers) else ''} "
                          f"{numbers[i + 3] if i + 3 < len(numbers) else ''}\n")

# Read the numbers from the two input files and find the difference
def subtract_files(file1, file2, output_file):
    # Read the numbers from the first file
    with open(file1, 'r') as f1:
        numbers_1 = set(map(int, f1.read().split()))
    
    # Read the numbers from the second file
    with open(file2, 'r') as f2:
        numbers_2 = set(map(int, f2.read().split()))
    
    # Find the numbers that are in file1 but not in file2
    result = numbers_1 - numbers_2
    
    # Write the result to the output file
    with open(output_file, 'w') as output:
        output.write("\n".join(map(str, sorted(result))))
    
    print(f"Output written to {output_file}")
    return output_file