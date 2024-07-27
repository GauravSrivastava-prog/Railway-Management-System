# Test Check on sample data for TM5.py
# Do not run !

import pandas as pd
from tabulate import tabulate

class TrainBooking:
    def __init__(self):
        pass

    def find_available_seats(self, train_number, travel_class, quota, current_station):
        # Read the CSV file for the train
        csv_path = f'/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/{train_number}.csv'
        seats_df = pd.read_csv(csv_path)
        
        # Debug print: show the head of the DataFrame
        print("Initial DataFrame:")
        print(seats_df.head())
        
        # Filter based on criteria
        available_seats = seats_df[
            (seats_df['Current_Station'] == current_station) &
            (seats_df['Class'] == travel_class) &
            (seats_df['Quota'] == quota) &
            (seats_df['Booking_Status'] == True)  # Booking_Status == True means the seat is available
        ]
        
        # Debug print: show the filtered DataFrame
        print("Filtered DataFrame based on criteria:")
        print(available_seats)
        
        return available_seats

    def booking(self):
        source_station = input("Source Station: ")
        destination_station = input("Destination Station: ")
        departure_date = input("Date of Departure: ")
        travel_class = input("Class (e.g., 1A, 2A, 3A, SL): ")
        quota = input("Quota (e.g., GN, LD, HP, DF, YU, TQ): ")

        # Simulate available trains data
        available_trains = pd.DataFrame({
            'Train_Name': ['Train1', 'Train2', 'Lucknow Express'],
            'Train_Number': [12345, 67890, 12503]
        })
        
        print("Available Trains:")
        print(tabulate(available_trains, headers='keys', tablefmt='psql'))
        
        train_name = input("Enter Train Name from the above list: ")
        train_number = int(input("Enter Train Number from the above list: "))
        
        print("---------------------------------------------")
        print("        Checking for Availability of Seats!")
        print("---------------------------------------------")
        
        available_seats = self.find_available_seats(train_number, travel_class, quota, source_station)
        
        if available_seats.empty:
            print("Available seats in your class are -> 0")
            print("Sorry, No Tickets Available!")
        else:
            print(f"Available seats in {train_name} in {travel_class} class from {source_station} are ->")
            print(available_seats)
            
            seat_no = int(input("Enter the Seat Number you want to book: "))
            
            if seat_no in available_seats['Seat_No.'].values:
                # Update the booking status of the selected seat
                csv_path = f'/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/{train_number}.csv'
                seats_df = pd.read_csv(csv_path)
                seats_df.loc[(seats_df['Class'] == travel_class) &
                             (seats_df['Quota'] == quota) &
                             (seats_df['Seat_No.'] == seat_no), 'Booking_Status'] = False  # Set to False to indicate the seat is now booked
                
                # Save the updated DataFrame back to the CSV file
                seats_df.to_csv(csv_path, index=False)
                
                print(f"Seat {seat_no} has been successfully booked!")
            else:
                print("Invalid seat number or seat is not available.")

def main():
    obj = TrainBooking()
    obj.booking()

if __name__ == "__main__":
    main()
