import csv
import random
import os
from datetime import datetime, timedelta
import pandas as pd
import xlsxwriter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import tkinter as tk
from tkinter import messagebox
from tabulate import tabulate


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

        file_path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/User-Data/" + self.pnr + ".xlsx"
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
        df = pd.read_csv("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv")
        train_schedule = df[df['Train_Name'] == self.trname]
        stations = train_schedule['Stations'].iloc[0].split(", ")
        from_index = stations.index(self.src)
        to_index = stations.index(self.des)
        time = train_schedule['Time'].iloc[0].split(", ")
        self.times = time[from_index:to_index + 1]

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

        amount = distance_fare * quota_fare * class_fare
        self.fare = '₹ ' + str(amount) + " Only"

    def route_calculate(self):
        df = pd.read_csv("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv")
        train_schedule = df[df['Train_Name'] == self.trname]
        stations = train_schedule['Stations'].iloc[0].split(", ")
        from_index = stations.index(self.src)
        to_index = stations.index(self.des)
        self.route = stations[from_index:to_index + 1]

    def register(self):
        self.fare_calculate()
        self.time_calculate()
        self.user_name = input("Name :\t")
        self.user_age = input("Age :\t")
        self.user_gender = input("Gender :\t")
        self.user_nationality = input("Nationality :\t")
        self.user_num = input("Number :\t")
        self.user_email = input("Email :\t")
        path_excel = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/User-Data/" + self.pnr + ".xlsx"
        headers = ['From', 'To', 'Train_Name', 'Train_Number', 'Name', 'PNR', 'Seat_Number', 'Birth_Type', 'Quota',
                   'Class', 'Date_Of_Departure', 'Age', 'Gender', 'Nationality', 'Number', 'Email', 'Waiting_List',
                   'Price']
        data = {'From': [self.src], 'To': [self.des], 'Train_Name': [self.trname], 'Train_Number': [self.trnum],
                'Name': [self.user_name], 'PNR': [self.pnr], 'Seat_Number': [self.seat_number],
                'Birth_Type': [self.birth_type], 'Quota': [self.quo], 'Class': [self.cls],
                'Date_Of_Departure': [self.dod], 'Age': [self.user_age], 'Gender': [self.user_gender],
                'Nationality': [self.user_nationality], 'Number': [self.user_num], 'Email': [self.user_email],
                'Waiting_List': [self.waiting], 'Price': [self.fare]}
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

    def available_seat_calculator(self):
        self.available = 0  # Reset available seats counter
        path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/" + self.trnum + ".csv"
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.cls == row['Class'] and self.quo == row['Quota'] and row['Booking_Status'] == "True" and row[
                    'Current_Station'] in self.route:
                    self.available += 1

    def waiting_list_calculator(self, wquo):
        self.waiting = 0  # Reset waiting list counter
        path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/" + self.trnum + ".csv"
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.cls == row['Class'] and self.quo == row['Quota'] and row['Booking_Status'] == "False" and row[
                    'Current_Station'] in self.route:
                    self.waiting += 1
        return self.waiting

    def check_train(self):
        train_data = []
        with open("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                train_data.append(row)

        src_lower = self.src.lower()
        des_lower = self.des.lower()

        found_train = False
        for row in train_data:
            station_list = row['Stations'].split(', ')
            if src_lower in [station.lower() for station in station_list] and des_lower in [
                station.lower() for station in station_list]:
                if not found_train:
                    print("Available Train ->")
                    print(row['Train_Name'])
                    self.trname = row['Train_Name']
                    self.route_calculate()
                    self.trnum = row['Train_No.']
                    found_train = True

        if not found_train:
            print("Train Not Found !")
            os.system('cls' if os.name == 'nt' else 'clear')
            return

        self.trname = input("Choose Train : ")
        for row in train_data:
            if row['Train_Name'].lower() == self.trname.lower():
                self.trnum = row['Train_No.']
                return True

    def check_seat(self):
        path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/" + self.trnum + ".csv"
        available_seats = False
        self.available_seat_calculator()  # Calculate available seats once

        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.cls == row['Class'] and row['Quota'] == self.quo and row['Current_Station'] in self.route:
                    if row['Booking_Status'] == "True":
                        messagebox.showinfo("Seat Availability",
                                            "Checking for " + self.quo + " Seats...\nAvailable Seats: " + str(
                                                self.available))
                        self.seat_number = random.choice(row['Seat_No.'])
                        self.birth_type = row['Birth_Type']
                        available_seats = True
                    elif row['Booking_Status'] == "False" and not available_seats and row['Current_Station'] in self.route:
                        available_seats = False

        if not available_seats:
            messagebox.showinfo("Seat Availability",
                                "Checking for " + self.quo + " Seats...\nWaiting List: " + str(
                                    self.waiting_list_calculator(self.quo)))
            askk = messagebox.askyesno("Booking Confirmation", "Do you wanna continue with your bookings ?")
            if askk:
                self.register()
            else:
                messagebox.showinfo("RailWise", "Thank You For Visiting RailWise !")

        if available_seats:
            askk = messagebox.askyesno("Booking Confirmation", "Do you wanna continue with your bookings ?")
            if askk:
                with open(path, 'r+') as file:
                    data = list(csv.DictReader(file))
                    for row in data:
                        if self.cls == row['Class'] and row['Quota'] == self.quo and self.seat_number == row[
                            'Seat_No.']:
                            row['Booking_Status'] = 'False'
                    file.seek(0)
                    writer = csv.DictWriter(file, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
                self.register()
            else:
                messagebox.showinfo("RailWise", "Thank You for Visiting RailWise !")

class RailWiseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RailWise")
        self.root.geometry("400x300")

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.label = tk.Label(self.frame, text="Welcome to RailWise", font=("Helvetica", 16))
        self.label.pack()

        self.book_button = tk.Button(self.frame, text="Book Ticket", command=self.book_ticket)
        self.book_button.pack(pady=10)

        self.status_button = tk.Button(self.frame, text="Check Ticket Status", command=self.check_status)
        self.status_button.pack(pady=10)

        self.train_button = tk.Button(self.frame, text="Show Available Trains", command=self.show_trains)
        self.train_button.pack(pady=10)

        self.exit_button = tk.Button(self.frame, text="Exit", command=root.quit)
        self.exit_button.pack(pady=10)

    def book_ticket(self):
        book_ticket_window = tk.Toplevel(self.root)
        book_ticket_window.title("Book Ticket")
        book_ticket_window.geometry("500x400")

        self.book_ticket_frame = tk.Frame(book_ticket_window)
        self.book_ticket_frame.pack(pady=20)

        self.source_label = tk.Label(self.book_ticket_frame, text="Source:")
        self.source_label.grid(row=0, column=0)
        self.source_entry = tk.Entry(self.book_ticket_frame)
        self.source_entry.grid(row=0, column=1)

        self.dest_label = tk.Label(self.book_ticket_frame, text="Destination:")
        self.dest_label.grid(row=1, column=0)
        self.dest_entry = tk.Entry(self.book_ticket_frame)
        self.dest_entry.grid(row=1, column=1)

        self.date_label = tk.Label(self.book_ticket_frame, text="Date of Departure (YYYY-MM-DD):")
        self.date_label.grid(row=2, column=0)
        self.date_entry = tk.Entry(self.book_ticket_frame)
        self.date_entry.grid(row=2, column=1)

        self.book_button = tk.Button(self.book_ticket_frame, text="Book", command=self.book)
        self.book_button.grid(row=3, columnspan=2, pady=10)

    def book(self):
        bookT = BookTicket()
        bookT.src = self.source_entry.get()
        bookT.des = self.dest_entry.get()
        bookT.dod = self.date_entry.get()
        if (bookT.check_train() == True):
            quota_list = ['GN', 'LD', 'HP', 'DF', 'YU', 'TQ']
            class_list = ['1A', '2A', '3A', 'SL']
            messagebox.showinfo("Enter Details",
                                "Enter the Details as Code...\nQuota Codes:\nGeneral (GN)\nTatkal (TQ)\nLadies (LD)\nPhysically Handicapped (HP)\nDefence (DF)\nYuva (YU)")
            bookT.quo = messagebox.askquestion("Quota", "Quota :")
            if datetime.strptime(bookT.dod, '%Y-%m-%d').date() != (datetime.now().date() + timedelta(days=1)) and \
                    bookT.quo == 'TQ':
                messagebox.showinfo("Tatkal Error", "Tatkal quota is only available for booking for tomorrow's date.")
                return
            if bookT.quo not in quota_list:
                messagebox.showinfo("Invalid Quota", "Entered Quota does not exist !")
                return
            messagebox.showinfo("Enter Class",
                                "Class Codes:\n1st AC (1A)\n2nd AC (2A)\n3rd AC (3A)\nSleeper (SL)")
            bookT.cls = messagebox.askquestion("Class", "Class :")
            if bookT.cls not in class_list:
                messagebox.showinfo("Invalid Class", "Entered Class does not exist !")
                return
            bookT.check_seat()

    def check_status(self):
        ticket_status_window = tk.Toplevel(self.root)
        ticket_status_window.title("Ticket Status")
        ticket_status_window.geometry("400x300")

        self.status_frame = tk.Frame(ticket_status_window)
        self.status_frame.pack(pady=20)

        self.pnr_label = tk.Label(self.status_frame, text="Enter PNR Number:")
        self.pnr_label.grid(row=0, column=0)
        self.pnr_entry = tk.Entry(self.status_frame)
        self.pnr_entry.grid(row=0, column=1)

        self.check_button = tk.Button(self.status_frame, text="Check Status", command=self.check)
        self.check_button.grid(row=1, columnspan=2, pady=10)

    def check(self):
        path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/User-Data/"
        file = self.pnr_entry.get() + ".xlsx"
        if file in os.listdir(path):
            df = pd.read_excel(path + file, engine='openpyxl')
            print(tabulate(df, headers='keys', tablefmt='pretty'))
        else:
            messagebox.showinfo("Invalid PNR", "Entered PNR does not exist !")

    def show_trains(self):
        show_trains_window = tk.Toplevel(self.root)
        show_trains_window.title("Available Trains")
        show_trains_window.geometry("400x300")

        self.show_trains_frame = tk.Frame(show_trains_window)
        self.show_trains_frame.pack(pady=20)

        self.trains_label = tk.Label(self.show_trains_frame, text="Available Trains:")
        self.trains_label.grid(row=0, column=0)

        self.trains_text = tk.Text(self.show_trains_frame, height=10, width=50)
        self.trains_text.grid(row=1, column=0)

        with open("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.trains_text.insert(tk.END, f"{row['Train_Name']} - {row['Train_No.']}\n")


if __name__ == "__main__":
    root = tk.Tk()
    railwise = RailWiseGUI(root)
    root.mainloop()

