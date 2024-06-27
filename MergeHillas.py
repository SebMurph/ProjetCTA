#S. Murphy Octobre 2023
#Crée un fichier Hillas_marged.csv à partir des deux fichiers Hillas protons et gammas (en mélangeant les lignes)
#aléatoirement

import os
import random
import csv

# Function to check if a file exists
def file_exists(file_path):
    return os.path.exists(file_path)

# Path to the three CSV files
file1_path = "gamma_diffuse_hillas_param_modified.csv"  # Replace with the actual path to your first CSV file
file2_path = "protons_diffuse_hillas_param_modified.csv"  # Replace with the actual path to your second CSV file
#file3_path = "Hillas-Modif/protons_diffuse_hillas_param_easy_modified.csv"  # Replace with the actual path to your third CSV file

# Create a list of file paths for checking existence
input_files = [file1_path, file2_path]

# Check if the input files exist before proceeding
missing_files = [file for file in input_files if not file_exists(file)]

if missing_files:
    print("The following input files do not exist:")
    for file in missing_files:
        print(file)
    exit(1)

# Path to the new big CSV file
output_file_path = "Hillas-merge.csv"  # Replace with your desired output path

# Number of lines to randomly select from each file
num_lines_to_select = 6000

# Function to read the third line (header) of a CSV file
def read_third_line(input_file):
    with open(input_file, "r") as file:
        reader = csv.reader(file)
        header = None
        for _ in range(1):
            header = next(reader)  # Read and store the header (third line)
    return header

# Determine which file's third line to use as the header (e.g., file1_path)
specific_header_file = file1_path

# Get the specific header from the chosen file
specific_header = read_third_line(specific_header_file)

# Create or open the new big CSV file
with open(output_file_path, "w", newline="") as output_file:
    writer = csv.writer(output_file)

    # Write the specific header to the big CSV file
    writer.writerow(specific_header)

    # Loop through the three CSV files
    for input_file_path in [file1_path, file2_path]:
        lines = []
        with open(input_file_path, "r") as file:
            reader = csv.reader(file)
            for _ in range(1):  # Skip the first three lines (header)
                next(reader)
            for row in reader:
                lines.append(row)


        # Select the first num_lines_to_select lines
        selected_lines = lines[:num_lines_to_select]

        # Write the selected lines to the big CSV file
        writer.writerows(selected_lines)

# Read the CSV file into a list of lines
with open(output_file_path, "r") as file:
    lines = file.readlines()

# Split the lines into header and data
header = lines[0]
data_lines = lines[1:]

# Shuffle the data lines randomly
random.shuffle(data_lines)

# Write the shuffled lines back to the CSV file
with open(output_file_path, "w") as file:
    file.write(header)  # Write the header
    file.writelines(data_lines)

print("Lines in the CSV file have been shuffled.")

print("file:", output_file_path)
