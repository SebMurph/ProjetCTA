#S. Murphy modified: Octobre 2023
#Ce programme lit un fichier Hillas original, enlève certaines colonnes et ajoute deux colonnes:
# une coloone particle tag et une colonne avec le path de chaque fichier évenement
#Il faut spécifier trois repertoires:
#le repertoire où se trouve le fichier Hillas original qui se nomme par exemple:#gamma_diffuse_hillas_param.csv
#le repertoire où l'on va copier le fichier Hillas modifié: ce nom va être par exemple gamma_diffuse_hillas_param_modified.csv
#le repertoire où sont stockés les fichiers evenements (variable folder)


import re,csv,os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from datetime import datetime

#Pour enlever le # du header du fichier original
def remove_hash_from_header(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
        # Read the input CSV file
        lines = input_file.readlines()

        # Modify the header line (the first line) to remove '#' at the beginning
        header = lines[0].lstrip('#')

        # Write the modified header to the output file
        output_file.write(header)

        # Write the rest of the lines as-is
        output_file.writelines(lines[1:])
# Call the function to remove '#' from the header


folder="gamma_diffuse_tel2"
output_tag=None
particle=0 # 0= gamma 1=protons 2=protons-easy

# folder="protons_diffuse_tel2"
# output_tag=None
# particle=1 # 0= gamma 1=protons 2=protons-easy

#folder="gamma_diffuse_tel2"
#output_tag=None
#particle=0 # 0= gamma 1=protons 2=protons-easy


repo_to_copy="/Users/sebastienmurphy/Library/CloudStorage/Dropbox/Informatique-DF/Projet-3e-info/CTA/Tel2"
base_folder="/Users/sebastienmurphy/Library/CloudStorage/Dropbox/Informatique-DF/Projet-3e-info/CTA/"
hillas_folder=os.path.join(base_folder,folder)
if  not  os.path.exists(hillas_folder):
    print(hillas_folder," does not exist")
    exit(0)

hillas_files = [filename for filename in os.listdir(hillas_folder) if "hillas_param.csv" in filename]
if len(hillas_files)>1:
    print("WARNING more than one hillas file: ",hillas_files)
    exit(0)

hillas_file = hillas_files[0]
print("Selected hillas_file:", hillas_file)


filename = os.path.join(hillas_folder, hillas_file)
print("OPENING:",filename)
if  not  os.path.exists(filename):
    print(filename," does not exist")
    exit(0)


#remove_hash_from_header(filename, filename)

# Metadata
metadata = {
    "repository": hillas_folder,
    "execution_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

particle_tag=re.split(r'_', hillas_file)[0]
# Check if the last letter of particle is 's' and remove it if it is
if particle_tag.endswith('s'):
    particle_tag = particle_tag[:-1]


# Load the existing data
print("opening:", filename)
data = np.loadtxt(filename, delimiter=' ', skiprows=0, dtype=str)

# Add a new column with the character string protons" as the last column
new_column = np.array([particle] * data.shape[0], dtype=str).reshape(-1, 1)
data_with_column = np.hstack((data, new_column))

# Extract the event IDs from the first column
event_ids = data[:, 0]

# Create an array of event_filenames based on event IDs
event_filenames = [f"{folder}/Event_{particle_tag}_diffuse_{event_id}.csv" for event_id in event_ids]

# Add a new column with event_filenames to data
data_with_column = np.column_stack((data_with_column, event_filenames))


# Define the columns to remove (e.g., columns 3, 5, and 6, 0-based index)
columns_to_remove = [5, 7, 11,12,14,15,16]
# Remove the specified columns
data_with_column = np.delete(data_with_column, columns_to_remove, axis=1)
print("header:",data[0])
# Create a header with "particle_type" separated by commas
header = ",".join(data[0]) + ",particle_type"

# Get the original header
original_header = header.split(',')

print(original_header)
modified_header = [original_header[i] for i in range(len(original_header)) if i not in columns_to_remove]
print(modified_header)
#Create a new CSV file with a comma separator and the header


# Retrieve the desired string (assuming it's always at a specific position)
#if(output_tag):
#    new_filename = os.path.splitext(filename)[0]+"_"+output_tag +"_modified.csv"
#else :
#new_filename = os.path.splitext(filename)[0]+"_modified.csv"

file_name = os.path.basename(filename)  # Get the base file name
file_name_without_extension, file_extension = os.path.splitext(file_name)  # Split the name and extension
new_filename = file_name_without_extension+"_modified.csv"

print("--:",new_filename)
new_filename = os.path.join(repo_to_copy, new_filename)

with open(new_filename, 'w', newline='') as f:
    csv_writer = csv.writer(f)

    # Write metadata as comments in the first line of the header
    #csv_writer.writerow([f"# Repository: {metadata['repository']}"])
    #csv_writer.writerow([f"# Execution Date: {metadata['execution_date']}"])

    # Split the header into a list and write it
    csv_writer.writerow(modified_header)

    # Write the data
    csv_writer.writerows(data_with_column[1:])

print("New CSV file created:", new_filename)

