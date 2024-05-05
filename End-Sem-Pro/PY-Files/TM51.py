import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import csv
import os
import random
import pandas as pd
from tabulate import tabulate
import xlsxwriter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

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
        messagebox.showinfo("Ticket Confirmation", "Your ticket has been mailed successfully.\nThank you for using RailWise!")

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
            class_fare = int(class_rate[self.cls])
        quota_rate = {'GN': 1.0, 'LD': 1.0, 'HP': 1.0, 'DF': 1.0, 'YU': 1.1, 'TQ': 1.4}
        if self.quo in quota_rate:
            quota_fare = int(quota_rate[self.quo])

        amount = distance_fare*quota_fare*class_fare
        self.fare = '₹ '+str(amount)+" Only"

    def route_calculate(self):
        df = pd.read_csv("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv")
        train_schedule = df[df['Train_Name'] == self.trname]
        stations = train_schedule['Stations'].iloc[0].split(", ")
        from_index = stations.index(self.src)
        to_index = stations.index(self.des)
        self.route = stations[from_index:to_index+1]

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


class RailWiseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RailWise")
        self.root.geometry("400x300")

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.label = tk.Label(self.frame, text="Welcome to RailWise\nThe Smart Railway Management System...")
        self.label.grid(row=0, column=0, pady=10)

        self.book_button = tk.Button(self.frame, text="Book Ticket", command=self.book_ticket)
        self.book_button.grid(row=1, column=0, pady=10)

        self.status_button = tk.Button(self.frame, text="Your Ticket Status", command=self.check_status)
        self.status_button.grid(row=2, column=0, pady=10)

        self.trains_button = tk.Button(self.frame, text="Show Available Trains", command=self.show_trains)
        self.trains_button.grid(row=3, column=0, pady=10)

        self.exit_button = tk.Button(self.frame, text="Exit", command=root.destroy)
        self.exit_button.grid(row=4, column=0, pady=10)

    def check_status(self):
        status_window = tk.Toplevel(self.root)
        status_window.title("Ticket Status")
        status_window.geometry("400x300")

        self.status_frame = tk.Frame(status_window)
        self.status_frame.pack(pady=20)

        self.pnr_label = tk.Label(self.status_frame, text="Enter PNR:")
        self.pnr_label.grid(row=0, column=0)

        self.pnr_entry = tk.Entry(self.status_frame)
        self.pnr_entry.grid(row=0, column=1)

        self.check_button = tk.Button(self.status_frame, text="Check", command=self.check)
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

    def book_ticket(self):
        book_ticket_window = tk.Toplevel(self.root)
        book_ticket_window.title("Book Ticket")
        book_ticket_window.geometry("400x300")

        self.book_frame = tk.Frame(book_ticket_window)
        self.book_frame.pack(pady=20)

        self.src_label = tk.Label(self.book_frame, text="Enter Source:")
        self.src_label.grid(row=0, column=0)
        self.src_entry = tk.Entry(self.book_frame)
        self.src_entry.grid(row=0, column=1)

        self.des_label = tk.Label(self.book_frame, text="Enter Destination:")
        self.des_label.grid(row=1, column=0)
        self.des_entry = tk.Entry(self.book_frame)
        self.des_entry.grid(row=1, column=1)

        self.dod_label = tk.Label(self.book_frame, text="Enter Date of Departure (YYYY-MM-DD):")
        self.dod_label.grid(row=2, column=0)
        self.dod_entry = tk.Entry(self.book_frame)
        self.dod_entry.grid(row=2, column=1)

        self.next_button = tk.Button(self.book_frame, text="Next", command=self.select_train)
        self.next_button.grid(row=3, columnspan=2, pady=10)

    def select_train(self):
        self.src = self.src_entry.get()
        self.des = self.des_entry.get()
        self.dod = self.dod_entry.get()

        # Assuming you have a list of available trains in a file, you can show them in a new window similarly to "show_trains" function

        # Once the user selects a train, you can proceed to the next step of selecting quota and class
        self.select_quota_class()

    def select_quota_class(self):
        select_quota_class_window = tk.Toplevel(self.root)
        select_quota_class_window.title("Select Quota and Class")
        select_quota_class_window.geometry("400x300")

        self.quota_class_frame = tk.Frame(select_quota_class_window)
        self.quota_class_frame.pack(pady=20)

        self.quota_label = tk.Label(self.quota_class_frame, text="Select Quota:")
        self.quota_label.grid(row=0, column=0)
        self.quota_entry = tk.Entry(self.quota_class_frame)
        self.quota_entry.grid(row=0, column=1)

        self.class_label = tk.Label(self.quota_class_frame, text="Select Class:")
        self.class_label.grid(row=1, column=0)
        self.class_entry = tk.Entry(self.quota_class_frame)
        self.class_entry.grid(row=1, column=1)

        self.continue_button = tk.Button(self.quota_class_frame, text="Continue", command=self.popup)
        self.continue_button.grid(row=2, columnspan=2, pady=10)

    def popup(self):
        response = messagebox.askyesno("Continue Booking", "Do you want to continue with your booking?")
        if response:
            self.register()

    def register(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Register")
        register_window.geometry("400x300")

        self.register_frame = tk.Frame(register_window)
        self.register_frame.pack(pady=20)

        self.name_label = tk.Label(self.register_frame, text="Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.register_frame)
        self.name_entry.grid(row=0, column=1)

        self.age_label = tk.Label(self.register_frame, text="Age:")
        self.age_label.grid(row=1, column=0)
        self.age_entry = tk.Entry(self.register_frame)
        self.age_entry.grid(row=1, column=1)

        self.gender_label = tk.Label(self.register_frame, text="Gender:")
        self.gender_label.grid(row=2, column=0)
        self.gender_entry = tk.Entry(self.register_frame)
        self.gender_entry.grid(row=2, column=1)

        self.nationality_label = tk.Label(self.register_frame, text="Nationality:")
        self.nationality_label.grid(row=3, column=0)
        self.nationality_entry = tk.Entry(self.register_frame)
        self.nationality_entry.grid(row=3, column=1)

        self.number_label = tk.Label(self.register_frame, text="Number:")
        self.number_label.grid(row=4, column=0)
        self.number_entry = tk.Entry(self.register_frame)
        self.number_entry.grid(row=4, column=1)

        self.email_label = tk.Label(self.register_frame, text="Email:")
        self.email_label.grid(row=5, column=0)
        self.email_entry = tk.Entry(self.register_frame)
        self.email_entry.grid(row=5, column=1)

        self.submit_button = tk.Button(self.register_frame, text="Submit", command=self.submit)
        self.submit_button.grid(row=6, columnspan=2, pady=10)

    def submit(self):
        self.user_name = self.name_entry.get()
        self.user_age = self.age_entry.get()
        self.user_gender = self.gender_entry.get()
        self.user_nationality = self.nationality_entry.get()
        self.user_num = self.number_entry.get()
        self.user_email = self.email_entry.get()

        ticket = BookTicket()
        ticket.src = self.src
        ticket.des = self.des
        ticket.dod = self.dod
        ticket.cls = self.class_entry.get()
        ticket.quo = self.quota_entry.get()
        ticket.check_seat()

        # After booking, show a message that ticket has been mailed
        self.mail_popup()


    def mail_popup(self):
        messagebox.showinfo("Ticket Mailed", "Your ticket has been mailed successfully.")
        # After closing the popup, go back to the home page
        self.root.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    app = RailWiseGUI(root)
    root.mainloop()
