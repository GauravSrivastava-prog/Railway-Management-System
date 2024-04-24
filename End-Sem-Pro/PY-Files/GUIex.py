import tkinter as tk
import csv
import random
import os
from datetime import datetime, timedelta
from tabulate import tabulate
import pandas as pd
import xlsxwriter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

class RailWiseApp:
    def __init__(self, master):
        self.master = master
        master.title("Welcome to RailWise")

        self.label = tk.Label(master, text="Welcome to RailWise", font=("Arial", 16))
        self.label.pack(pady=20)

        self.book_button = tk.Button(master, text="Book Ticket", command=self.book_ticket_window)
        self.book_button.pack()

        self.status_button = tk.Button(master, text="Check Ticket Status", command=self.check_status)
        self.status_button.pack()

        self.show_trains_button = tk.Button(master, text="Show Available Trains", command=self.show_trains)
        self.show_trains_button.pack()

        self.exit_button = tk.Button(master, text="Exit", command=master.quit)
        self.exit_button.pack()

    def book_ticket_window(self):
        self.book_window = tk.Toplevel(self.master)
        self.book_window.title("Book Ticket")

        self.src_label = tk.Label(self.book_window, text="Source:")
        self.src_label.grid(row=0, column=0)
        self.src_entry = tk.Entry(self.book_window)
        self.src_entry.grid(row=0, column=1)

        self.des_label = tk.Label(self.book_window, text="Destination:")
        self.des_label.grid(row=1, column=0)
        self.des_entry = tk.Entry(self.book_window)
        self.des_entry.grid(row=1, column=1)

        self.date_label = tk.Label(self.book_window, text="Date of Departure (YYYY-MM-DD):")
        self.date_label.grid(row=2, column=0)
        self.date_entry = tk.Entry(self.book_window)
        self.date_entry.grid(row=2, column=1)

        self.submit_button = tk.Button(self.book_window, text="Submit", command=self.book_ticket)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    def book_ticket(self):
        src = self.src_entry.get()
        des = self.des_entry.get()
        dod = self.date_entry.get()

        bookT = BookTicket(src, des, dod)
        bookT.check_train()
        bookT.quo = self.select_quota_window()
        bookT.cls = self.select_class_window()
        bookT.check_seat()

    def select_quota_window(self):
        self.quota_window = tk.Toplevel(self.book_window)
        self.quota_window.title("Select Quota")

        quota_list = ['GN', 'LD', 'HP', 'DF', 'YU','TQ']

        self.quota_label = tk.Label(self.quota_window, text="Select Quota:")
        self.quota_label.grid(row=0, column=0)
        self.quota_var = tk.StringVar()
        self.quota_var.set(quota_list[0])  # Default value
        self.quota_dropdown = tk.OptionMenu(self.quota_window, self.quota_var, *quota_list)
        self.quota_dropdown.grid(row=0, column=1)

        self.submit_button = tk.Button(self.quota_window, text="Submit", command=self.quota_window.destroy)
        self.submit_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.quota_window.wait_window()  # Wait for the window to be closed
        return self.quota_var.get()

    def select_class_window(self):
        self.class_window = tk.Toplevel(self.book_window)
        self.class_window.title("Select Class")

        class_list = ['1A', '2A', '3A', 'SL']

        self.class_label = tk.Label(self.class_window, text="Select Class:")
        self.class_label.grid(row=0, column=0)
        self.class_var = tk.StringVar()
        self.class_var.set(class_list[0])  # Default value
        self.class_dropdown = tk.OptionMenu(self.class_window, self.class_var, *class_list)
        self.class_dropdown.grid(row=0, column=1)

        self.submit_button = tk.Button(self.class_window, text="Submit", command=self.class_window.destroy)
        self.submit_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.class_window.wait_window()  # Wait for the window to be closed
        return self.class_var.get()

    def check_status(self):
        # Functionality to be added later
        pass

    def show_trains(self):
        # Functionality to be added later
        pass

class BookTicket:
    def __init__(self, src, des, dod):
        self.src = src
        self.des = des
        self.dod = dod
        self.quo = ""
        self.cls = ""
        self.trnum = ""
        self.trname = ""
        self.pnr = ''.join(random.choices('0123456789', k=12))
        self.seat_number = ""
        self.birth_type = ""
        self.user_email = ""
        self.waiting = 0
        self.available = 0
        self.route = []
        self.fare = ""
        self.times = []
    def check_train(self):
        train_data = []
        with open("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                train_data.append(row)
    
        src_lower = self.src.lower()
        des_lower = self.des.lower()
    
        found_train = None
        for row in train_data:
            station_list = row['Stations'].split(', ')
            if src_lower in [station.lower() for station in station_list] and des_lower in [station.lower() for station in station_list]:
                found_train = row['Train_Name']
                self.trname = row['Train_Name']
                self.route_calculate()
                self.trnum = row['Train_No.']
                break
            
        return found_train

    def check_seat(self):
        path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files"+self.trnum + ".csv"
        available_seats = False
        self.available_seat_calculator()  # Calculate available seats once

        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.cls == row['Class'] and row['Quota'] == self.quo and row['Current_Station'] in self.route:
                    if row['Booking_Status'] == "True": 
                        print("---------------------------------------------")
                        print("Checking for " + self.quo + " Seats...")
                        print("Available Seats:\t", self.available)  # Print available seats
                        self.seat_number = random.choice(row['Seat_No.'])
                        self.birth_type = row['Birth_Type']
                        available_seats = True 
                    elif row['Booking_Status'] == "False" and not available_seats and row['Current_Station'] in self.route:
                        available_seats = False

        if not available_seats:
            print("---------------------------------------------")
            print("Checking for " + self.quo + " Seats...")
            waiting_list = self.waiting_list_calculator(self.quo)
            print("Waiting List:\t", waiting_list)
            os.system('cls' if os.name == 'nt' else 'clear')
            askk = input("Do you wanna continue with your bookings ? (y/n):\t")
            if (askk == 'y' or askk == 'Y'):
                self.register()
            else:
                print("---------------------------------------------")
                print("\tThank You For Visiting RailWise !")
                print("---------------------------------------------")
        print("---------------------------------------------")

        if available_seats:
            os.system('cls' if os.name == 'nt' else 'clear')
            askk = input("Do you wanna continue with your bookings ? (y/n):\t")
            if (askk == 'y' or askk == 'Y'):
                os.system('cls' if os.name == 'nt' else 'clear')
                with open(path, 'r+') as file:
                    data = list(csv.DictReader(file))
                    for row in data:
                        if self.cls == row['Class'] and row['Quota'] == self.quo and self.seat_number == row['Seat_No.']:
                            row['Booking_Status'] = 'False'
                    file.seek(0)
                    writer = csv.DictWriter(file, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
                self.register()
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("---------------------------------------------")
                print("\tThank You for Visiting RailWise !")
                print("---------------------------------------------")
                exit(0)

    def available_seat_calculator(self):
        self.available = 0  # Reset available seats counter
        path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/"+self.trnum + ".csv"
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.cls == row['Class'] and self.quo == row['Quota'] and row['Booking_Status'] == "True" and row['Current_Station'] in self.route:
                    self.available += 1

    def waiting_list_calculator(self, wquo):
        self.waiting = 0  # Reset waiting list counter
        path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/"+self.trnum + ".csv"
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.cls == row['Class'] and self.quo == row['Quota'] and row['Booking_Status'] == "False" and row['Current_Station'] in self.route:
                    self.waiting += 1
        return self.waiting

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
        self.user_name = input("Name :\t")
        self.user_age = input("Age :\t")
        self.user_gender = input("Gender :\t")
        self.user_nationality = input("Nationality :\t")
        self.user_num = input("Number :\t")
        self.user_email = input("Email :\t")
        path_excel = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/User-Data/"+self.pnr + ".xlsx"
        headers = ['From','To','Train_Name','Train_Number','Name','PNR','Seat_Number','Birth_Type','Quota','Class','Date_Of_Departure','Age','Gender','Nationality','Number','Email', 'Waiting_List', 'Price']
        data = {'From':[self.src],'To':[self.des],'Train_Name':[self.trname],'Train_Number':[self.trnum],'Name':[self.user_name],'PNR':[self.pnr],'Seat_Number':[self.seat_number],'Birth_Type':[self.birth_type],'Quota':[self.quo],'Class':[self.cls],'Date_Of_Departure':[self.dod],'Age':[self.user_age],'Gender':[self.user_gender],'Nationality':[self.user_nationality],'Number':[self.user_num],'Email':[self.user_email], 'Waiting_List':[self.waiting], 'Price':[self.fare]}
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

    def mail(self):
        sender_email = "railwise1@gmail.com"
        receiver_email = self.user_email
        subject = "Your Ticket Has Been Confirmed !"
        body = "Thank You for Using Rail Wise, Here is your confirmed ticket attatched below ->"

        file_path = self.pnr + ".xlsx"
        file_name = self.pnr + ".xlsx"

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
        os.system('cls' if os.name == 'nt' else 'clear')
        print("---------------------------------------------")            
        print("\tYour Ticket has been mailed Successfully...")
        print("\t\tThank you for Using RailWise !")
        print("---------------------------------------------")
        print()

    def time_calculate(self):
        df = pd.read_csv("Trains.csv")
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
            class_fare = int(class_rate[self.cls])
        quota_rate = {'GN': 1.0, 'LD': 1.0, 'HP': 1.0, 'DF': 1.0, 'YU': 1.1, 'TQ': 1.4}
        if self.quo in quota_rate:
            quota_fare = int(quota_rate[self.quo])
        
        amount = distance_fare*quota_fare*class_fare
        self.fare = '₹ '+str(amount)+" Only"

root = tk.Tk()
app = RailWiseApp(root)
root.mainloop()
