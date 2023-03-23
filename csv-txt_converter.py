import pandas as pd
import os

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('radioNZ_articles.csv')

# Loop through each row of the DataFrame
for index, row in df.iterrows():
    # Extract the relevant data from the row
    date = row['date']
    heading = row['heading']
    body = row['body']

    # Create the file name
    file_name = f'rnz_{date}.txt'

    # Write the data to the file
    directory_path = "/Users/duncanoregan/Desktop/UCdatascience/DIGI405/Assignments/corpus_building/RNZ_2"

    # open .txt file
    with open(os.path.join(directory_path, f'{file_name}.txt'), 'w') as f:
        f.write(heading + '\n' + body)