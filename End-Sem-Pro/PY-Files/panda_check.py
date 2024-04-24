import csv

# Open the CSV file in read mode
with open("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv", "r") as file:
    reader = csv.DictReader(file)
    
    # Count the number of rows in the CSV file
    row_count = sum(1 for row in reader)
    print("Total number of rows:", row_count)

    # Reset the file pointer back to the beginning of the file
    file.seek(0)

    # Iterate over the CSV file again to check the presence of 'Chennai' station in each row
    for row in reader:
        station_list = row['Stations'].split(', ')
        # Flag variable to track whether the train name has been printed
        train_printed = False
        for station in station_list:
            if station.strip() == 'Chennai':
                # Check if the train name has not been printed yet
                if not train_printed:
                    print(row['Train_Name'])
                    # Set the flag to True to indicate that the train name has been printed
                    train_printed = True
                # Break the loop once 'Chennai' station is found
                break
