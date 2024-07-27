# This is the file you run !

import csv
import random
import os
from datetime import datetime, timedelta
from tabulate import tabulate
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import xlsxwriter

class TicketStatus:
    def __init__(self):
        self.pnr = ""

    def check_status(self):
        self.pnr = input("User Enter Your PNR Number: ")
        path = f"/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/User-Data/{self.pnr}.xlsx"
        if os.path.exists(path):
            print("User, your ticket has been confirmed!")
            print("Here is your ticket ->")
            df = pd.read_excel(path)
            print(df)
        else:
            print("Ticket can't be found!")

class ShowAvailableTrains:
    def available_trains(self):
        print("---------------------------------------------")
        print("\tList of Trains Running Right Now!")
        print("---------------------------------------------")
        with open("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                print("->", row['Train_Name'])

class BookTicket:
    def __init__(self):
        self.src = ""
        self.des = ""
        self.dod = ""
        self.cls = ""
        self.quo = ""
        self.trnum = ""
        self.trname = ""
        self.user_name = ""
        self.user_age = ""
        self.user_num = ""
        self.user_gender = ""
        self.user_nationality = ""
        self.pnr = ''.join(random.choices('0123456789', k=12))
        self.seat_number = ""
        self.birth_type = ""
        self.user_email = ""
        self.waiting = 0
        self.available = 0
        self.route = []
        self.fare = ""
        self.times = []

    def mail(self):
        sender_email = "railwise1@gmail.com"
        receiver_email = self.user_email
        subject = "Your Ticket Has Been Confirmed !"
        body = "Thank You for Using Rail Wise, Here is your confirmed ticket attatched below ->"


        file_path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/User-Data/"+self.pnr+".xlsx"
        file_name = self.pnr+".xlsx"


        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))


        with open(file_path, "rb") as attachment:

            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())


        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {file_name}",
        )

        message.attach(part)
        text = message.as_string()

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("railwise1@gmail.com", "dplzsobgvefapudv")
            server.sendmail(sender_email, receiver_email, text)

        print("---------------------------------------------")            
        print("\tYour Ticket has been mailed Successfully...")
        print("\t\tThank you for Using RailWise !")
        print("---------------------------------------------")
        print()

    def time_calculate(self):
        df = pd.read_csv("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv")
        train_schedule = df[df['Train_Name'] == self.trname]
        stations = train_schedule['Stations'].iloc[0].split(", ")
        from_index = stations.index(self.src)
        to_index = stations.index(self.des)
        time = train_schedule['Time'].iloc[0].split(", ")
        self.times = time[from_index:to_index+1]

    def fare_calculate(self):
        df = pd.read_csv("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv")
        train_schedule = df[df['Train_Name'] == self.trname]
        stations = train_schedule['Stations'].iloc[0].split(", ")
        from_index = stations.index(self.src)
        to_index = stations.index(self.des)
        distance = train_schedule['Distance'].iloc[0].split(", ")
        distance_travelled = int(distance[to_index]) - int(distance[from_index])
        distance_fare = distance_travelled * 10 
        class_rate = {'1A': 4, '2A': 1.5, '3A': 1.0, 'SL': 0.5}
        if self.cls in class_rate:
            class_fare = class_rate[self.cls]
        quota_rate = {'GN': 1.0, 'LD': 1.0, 'HP': 1.0, 'DF': 1.0, 'YU': 1.1, 'TQ': 1.4}
        if self.quo in quota_rate:
            quota_fare = quota_rate[self.quo]

        amount = abs(distance_fare * quota_fare * class_fare)
        self.fare = f'₹ {amount} Only'

    def route_calculate(self):
        df = pd.read_csv("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv")
        train_schedule = df[df['Train_Name'] == self.trname]
        stations = train_schedule['Stations'].iloc[0].split(", ")
        from_index = stations.index(self.src)
        to_index = stations.index(self.des)
        self.route = stations[from_index:to_index+1]

    def register(self):
        print("---------------------------------------------")
        self.fare_calculate()
        self.time_calculate()
        self.user_name = input("Name: ")
        self.user_age = input("Age: ")
        self.user_gender = input("Gender: ")
        self.user_nationality = input("Nationality: ")
        self.user_num = input("Number: ")
        self.user_email = input("Email: ")
        path_excel = f"/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/User-Data/{self.pnr}.xlsx"
        headers = ['From', 'To', 'Train_Name', 'Train_Number', 'Name', 'PNR', 'Seat_Number', 'Birth_Type', 'Quota', 'Class', 'Date_Of_Departure', 'Age', 'Gender', 'Nationality', 'Number', 'Email', 'Waiting_List', 'Price']
        data = {
            'From': [self.src], 'To': [self.des], 'Train_Name': [self.trname], 'Train_Number': [self.trnum],
            'Name': [self.user_name], 'PNR': [self.pnr], 'Seat_Number': [self.seat_number], 'Birth_Type': [self.birth_type],
            'Quota': [self.quo], 'Class': [self.cls], 'Date_Of_Departure': [self.dod], 'Age': [self.user_age],
            'Gender': [self.user_gender], 'Nationality': [self.user_nationality], 'Number': [self.user_num],
            'Email': [self.user_email], 'Waiting_List': [self.waiting], 'Price': [self.fare]
        }
        df = pd.DataFrame(data)
        route_timings_df = pd.DataFrame({'Route': self.route, 'Timings': self.times})
        df_transpose = df.T
        writer = pd.ExcelWriter(path_excel, engine='xlsxwriter')
        df_transpose.to_excel(writer, sheet_name='Sheet1', index=True, header=False)
        route_timings_df.to_excel(writer, sheet_name='Sheet1', startcol=df_transpose.shape[1] + 2, index=False)
        worksheet = writer.sheets['Sheet1']
        for i, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).map(len).max(), len(col))
            worksheet.set_column(i, i, max_length + 4)
        for i, col in enumerate(route_timings_df.columns):
            max_length = max(route_timings_df[col].astype(str).map(len).max(), len(col))
            worksheet.set_column(i, i, max_length + 4)

        writer._save()

        self.mail()

    def find_available_seats(self, train_number, travel_class, quota, current_station):
        csv_path = f'/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/{train_number}.csv'
        
        try:
            seats_df = pd.read_csv(csv_path)
        except FileNotFoundError:
            print(f"Error: File {csv_path} not found.")
            return pd.DataFrame()

        # Ensure we are looking for available seats
        available_seats = seats_df[
            (seats_df['Current_Station'] == current_station) &
            (seats_df['Class'] == travel_class) &
            (seats_df['Quota'] == quota) &
            (seats_df['Booking_Status'] == True)  # Booking_Status True indicates the seat is available
        ]

        return available_seats

    def available_seat_calculator(self):
        self.available = 0  # Reset available seats counter
        csv_path = f'/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/{self.trnum}.csv'
        try:
            seats_df = pd.read_csv(csv_path)
            # Count available seats directly
            self.available = len(seats_df[
                (seats_df['Class'] == self.cls) &
                (seats_df['Quota'] == self.quo) &
                (seats_df['Booking_Status'] == True)
            ])
        except FileNotFoundError:
            print(f"Error: File {csv_path} not found.")

    def display_available_seats(self):
        print("---------------------------------------------")
        print("\tChecking for Availability of Seats!")
        print("---------------------------------------------")
        available_seats = self.find_available_seats(self.trnum, self.cls, self.quo, self.src)
        
        if available_seats.empty:
            print("Available seats in your class are -> 0")
        else:
            print(f"Available Seats in {self.trname} in {self.cls} class from {self.src} are ->")
            print(available_seats[['Seat_No.', 'Birth_Type']])
        
    def booking(self):
        print("---------------------------------------------")
        self.src = input("Source Station: ")
        self.des = input("Destination Station: ")
        self.dod = input("Date of Departure: ")
        self.cls = input("Class (e.g., 1A, 2A, 3A, SL): ")
        self.quo = input("Quota (e.g., GN, LD, HP, DF, YU, TQ): ")

        # Display available trains based on source and destination
        df = pd.read_csv("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv")
        available_trains = df[(df['Stations'].str.contains(self.src)) & (df['Stations'].str.contains(self.des))]

        if available_trains.empty:
            print("No trains available for the selected route.")
            return

        print("\nAvailable Trains:")
        print(tabulate(available_trains[['Train_Name', 'Train_No.']], headers='keys', tablefmt='psql'))

        # Get train details from user
        self.trname = input("Enter Train Name from the above list: ")
        self.trnum = input("Enter Train Number from the above list: ")

        self.route_calculate()
        self.display_available_seats()
        self.available_seat_calculator()
        print("Available seats in your class are ->", self.available)
        if self.available > 0:
            seat_no = input("Enter the Seat Number you want to book: ")
            # Update the booking status of the selected seat
            csv_path = f'/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/{self.trnum}.csv'
            seats_df = pd.read_csv(csv_path)
            if int(seat_no) in seats_df['Seat_No.'].values:
                seats_df.loc[(seats_df['Class'] == self.cls) &
                             (seats_df['Quota'] == self.quo) &
                             (seats_df['Seat_No.'] == int(seat_no)), 'Booking_Status'] = False  # Set to False to indicate the seat is now booked
                seats_df.to_csv(csv_path, index=False)
                print(f"Seat {seat_no} has been successfully booked!")
                self.seat_number = seat_no
                self.register()
            else:
                print("Invalid seat number or seat is not available.")
        else:
            print("Sorry, No Tickets Available!")

def main():
    while True:
        print("---------------------------------------------")
        print("                Rail Wise!")
        print("---------------------------------------------")
        print("1. Book Tickets!")
        print("2. Check PNR Status!")
        print("3. Show All Available Trains!")
        print("4. Exit!")
        print("---------------------------------------------")
        choice = input("Enter your choice: ")

        if choice == '1':
            ticket = BookTicket()
            ticket.booking()
        elif choice == '2':
            status = TicketStatus()
            status.check_status()
        elif choice == '3':
            trains = ShowAvailableTrains()
            trains.available_trains()
        elif choice == '4':
            print("Thank you for using Rail Wise! Have a great day!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
