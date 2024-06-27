#S. Murphy Octobre 2023
#Prog à executer après ReindexHillas.py
#Genère le fichier final élève d'Hillas
#Ce prog:
# -lit la dernière colonne et copie les fichiers evenements sélectionner en les réindexant pour que l'event_id correponde
#bien à celui du fichier Hillas
#-Supprime la dernière colonne avec les paths des fichier evenements originaux
#Output Hillas-J2.y

import csv
import os
import shutil

def file_exists(file_path):
    return os.path.exists(file_path)

# Path to the CSV file
csv_file_path = "Hillas-Reindex.csv"  # Replace with the actual path to your CSV file

# Output directory for copying files
output_directory = "Code-eleve/Data-Tel2/Raw-protons-gammas"  # Replace with the desired output directory

original_raw_data_path="/Users/sebastienmurphy/Library/CloudStorage/Dropbox/Informatique-DF/Projet-3e-info/CTA"
# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Lists to store data from the CSV file
data = []

# Read the CSV file and extract the last column
with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header=next(csv_reader)  # Skip the first line (header)
    for row in csv_reader:
        data.append(row)
        first_column_value = row[0]  # Extract the value from the first column
        last_column_value = row[-1]  # Extract the last column value
        file_to_copy=os.path.join(original_raw_data_path, last_column_value)
        #print(last_column_value)
        # Check if the last column value is a valid file path
        if os.path.isfile(file_to_copy):
            # Get the file extension
            file_extension = os.path.splitext(last_column_value)[1]
            # Construct the new file name with the index from the first column
            new_file_name = f"Event_{first_column_value}{file_extension}"
            # Copy the file to the output directory with the new name
            new_file_dir=os.path.join(original_raw_data_path,output_directory, new_file_name)
            #if not file_exists(new_file_dir):
        #        print(new_file_dir, " does not exist")
            shutil.copy(file_to_copy, new_file_dir)
            print(file_to_copy," copied to:",new_file_dir)
        else:
            print(f"File not found: {file_to_copy}")

# Copy the CSV file to the output directory
#csv_file_without_last_column=os.path.join(output_directory, os.path.basename(csv_file_path))

# Create a copy of the CSV file without the last column
#csv_file_without_last_column_path = os.path.join(output_directory, os.path.basename(csv_file_path))
csv_file_without_last_column_path = "Hillas-para-J2.csv"
#header = data[1]
print(header)
data_without_last_column = [row[:-1] for row in data[0:]]
with open(csv_file_without_last_column_path, mode='w', newline='') as csv_file_without_last_column:
    csv_writer = csv.writer(csv_file_without_last_column)
    csv_writer.writerow(header)
    csv_writer.writerows(data_without_last_column)

print("final Hillas file:",csv_file_without_last_column_path)
