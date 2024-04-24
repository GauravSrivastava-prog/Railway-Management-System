import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv")

# Create a new column "Stations" by concatenating station names
df['Stations'] = df[['Source', 'Station1', 'Station2', 'Station3', 'Destination']].apply(lambda x: ', '.join(x), axis=1)

# Drop the individual station columns
df.drop(['Source', 'Station1', 'Station2', 'Station3', 'Destination'], axis=1, inplace=True)

# Write the modified DataFrame back to a new CSV file
df.to_csv("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv", index=False)


print("CSV file generated successfully.")
