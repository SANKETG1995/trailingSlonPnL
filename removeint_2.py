def remove_lines_starting_with_integer(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Check if the first character of the line is an integer
            if not line.lstrip()[0].isdigit():
                outfile.write(line)

if __name__ == "__main__":
    input_file = "file4.txt"  # Replace with the path to your input file
    output_file = "file5.txt"  # Replace with the desired output file path
    remove_lines_starting_with_integer(input_file, output_file)

