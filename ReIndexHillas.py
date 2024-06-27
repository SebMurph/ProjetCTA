#S. Murphy Octobre 2023
#Prog à executer après MergeHillas.py
#ne fait que réindexer la première colone pour avoir des events_id qui se suivent à partir de 1.
#Output Hillas-Reindex.csv

import csv

# Path to the input CSV file
input_csv_path = "Hillas-merged.csv"  # Replace with the actual path to your CSV file

# Path to the output CSV file
output_csv_path = "Hillas-Reindex.csv"  # Replace with your desired output path

# Initialize a counter for event_id
event_id_counter = 1

# Lists to store modified data and header
modified_data = []
header = []

# Read the input CSV file and make modifications
with open(input_csv_path, "r") as input_csv:
    reader = csv.reader(input_csv, delimiter=',')

    # Read the header
    header = next(reader)
    header[0] = "event_id"
#    header.insert(1, "ol_event_id")
    #header.insert(1, "event_id")

    # Append the modified header to the data
    modified_data.append(header)

    # Iterate through the rows and make modifications
    for row in reader:
        # Remove the last column (assuming it's not needed)
        #modified_row = row[:-1]

        # Insert new columns with ol_event_id and event_id
        #modified_row.insert(1, str(event_id_counter))
        row[0]=str(event_id_counter)
    #    modified_row.insert(2, str(event_id_counter))
        event_id_counter += 1

        # Append the modified row to the data
        modified_data.append(row)

# Write the modified data to the output CSV file
with open(output_csv_path, "w", newline='') as output_csv:
    writer = csv.writer(output_csv, delimiter=',')

    # Write the modified data
    writer.writerows(modified_data)

print("CSV file has been modified and saved to:", output_csv_path)
