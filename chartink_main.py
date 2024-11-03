import subprocess


# Run the other script
process=subprocess.run(["python", "/home/kali/Desktop/Kite_Zerodha-main/codebase/chartink.py"], capture_output=True)

output=process.stdout.decode("utf-8")

# Write the output to a file
output_file_path = "file.txt"
with open(output_file_path, "w") as file:
    file.write(output)

# Run the other script
process=subprocess.run(["python", "/home/kali/Desktop/Kite_Zerodha-main/codebase/sorter.py"], capture_output=True)

output=process.stdout.decode("utf-8")

# Write the output to a file
output_file_path = "file.txt"
with open(output_file_path, "w") as file:
    file.write(output)

subprocess.run(["python", "/home/kali/Desktop/Kite_Zerodha-main/codebase/removeint.py"])

subprocess.run(["python", "/home/kali/Desktop/Kite_Zerodha-main/codebase/descending_duplicates.py"])

#########################################################################################################3

# Run the other script
process=subprocess.run(["python", "/home/kali/Desktop/Kite_Zerodha-main/codebase/chartink_short.py"], capture_output=True)

output=process.stdout.decode("utf-8")

# Write the output to a file
output_file_path = "file3.txt"
with open(output_file_path, "w") as file:
    file.write(output)

# Run the other script
process=subprocess.run(["python", "/home/kali/Desktop/Kite_Zerodha-main/codebase/sorter.py"], capture_output=True)

output=process.stdout.decode("utf-8")

# Write the output to a file
output_file_path = "file4.txt"
with open(output_file_path, "w") as file:
    file.write(output)

subprocess.run(["python", "/home/kali/Desktop/Kite_Zerodha-main/codebase/removeint_2.py"])

subprocess.run(["python", "/home/kali/Desktop/Kite_Zerodha-main/codebase/descending_duplicates_2.py"])
