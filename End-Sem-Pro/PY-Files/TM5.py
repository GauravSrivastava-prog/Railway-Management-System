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


class ticket_status:
    pnr = ""
    def check_status(self):
        self.pnr = input("User Enter Your PNR Number : ")
        path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/User-Data/"+self.pnr+".xlsx"
        if os.path.exists(path):
            print("User Your Ticket Has Been Confirmed !")
            print("Here is your ticket ->")
            df = pd.read_excel(path)
            print(df)
        else:
            print("Ticket Can't be found !")


class show_available_trains:
    def available_trains(self):
        print("---------------------------------------------")
        print("\tList Of Trains Running Right Now !")
        print("---------------------------------------------")
        with open("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                print("->", row['Train_Name'])

class book_ticket:
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
        print("---------------------------------------------")
        self.fare_calculate()
        self.time_calculate()
        self.user_name = input("Name :\t")
        self.user_age = input("Age :\t")
        self.user_gender = input("Gender :\t")
        self.user_nationality = input("Nationality :\t")
        self.user_num = input("Number :\t")
        self.user_email = input("Email :\t")
        path_excel = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/User-Data/" + self.pnr + ".xlsx"
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

    def available_seat_calculator(self):
        self.available = 0  # Reset available seats counter
        path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/" + self.trnum + ".csv"
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.cls == row['Class'] and self.quo == row['Quota'] and row['Booking_Status'] == "True" and row['Current_Station'] in self.route:
                    self.available = self.available + 1

    def waiting_list_calculator(self, wquo):
        self.waiting = 0  # Reset waiting list counter
        path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/" + self.trnum + ".csv"
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.cls == row['Class'] and self.quo == row['Quota'] and row['Booking_Status'] == "False" and row['Current_Station'] in self.route:
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
        print("Available Train ->")
        for row in train_data:
            station_list = row['Stations'].split(', ')
            if src_lower in [station.lower() for station in station_list] and des_lower in [station.lower() for station in station_list]:
                    print(row['Train_Name'])
                    self.trname = row['Train_Name']
                    self.route_calculate()
                    self.trnum = row['Train_No.']
                    found_train = True

        if not found_train:
            print("Train Not Found !")
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
            print("---------------------------------------------")
            print("Checking for " + self.quo + " Seats...")
            print("Available Seats:")
            print(self.available)
            for row in reader:
                if self.cls == row['Class'] and row['Quota'] == self.quo and row['Current_Station'] in self.route:
                    if row['Booking_Status'] == "True": 
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

            askk = input("Do you wanna continue with your bookings ? (y/n):\t")
            if (askk == 'y' or askk == 'Y'):
                self.register()
            else:
                print("---------------------------------------------")
                print("\tThank You For Visiting RailWise !")
                print("---------------------------------------------")
        print("---------------------------------------------")

        if available_seats:

            askk = input("Do you wanna continue with your bookings ? (y/n):\t")
            if (askk == 'y' or askk == 'Y'):

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

                print("---------------------------------------------")
                print("\tThank You for Visiting RailWise !")
                print("---------------------------------------------")
                exit(0)


if __name__ == "__main__":
    quota_list = ['GN', 'LD', 'HP', 'DF', 'YU','TQ']
    class_list = ['1A', '2A', '3A', 'SL']
    while True:
        print("\t\t Welcome to RailWise\n\tThe Smart Railway Management System...")
        print("---------------------------------------------")
        print("1 ->\t Book Ticket")
        print("2 ->\t Your Ticket Status")
        print("3 ->\t Show Available Trains")
        print("4 ->\t Exit")
        print("---------------------------------------------")

        choice = input("Enter Choice User : ")

        if choice == '1':

            bookT = book_ticket()
            bookT.src = input("Enter Source :\t")
            bookT.des = input("Enter Destination :\t")
            bookT.dod = input("Enter Date of Departure (YYYY-MM-DD): ")
            if (bookT.check_train() == True):
                print("Enter the Details as Code...")
                print("---------------------------------------------")
                print("Quota Codes:")
                if datetime.strptime(bookT.dod, '%Y-%m-%d').date() == (datetime.now().date() + timedelta(days=1)):
                    print(tabulate([['General', 'GN'], ['Tatkal', 'TQ'], ['Ladies', 'LD'], ['Physically Handicapped', 'HP'], ['Defence', 'DF'], ['Yuva', 'YU']], headers=['Quota', 'Code']))
                else:
                    print(tabulate([['General', 'GN'], ['Ladies', 'LD'], ['Physically Handicapped', 'HP'], ['Defence', 'DF'], ['Yuva', 'YU']], headers=['Quota', 'Code']))
                print("---------------------------------------------")
                while True:
                    bookT.quo = input("Quota : ")
                    if datetime.strptime(bookT.dod, '%Y-%m-%d').date() != (datetime.now().date() + timedelta(days=1)) and bookT.quo == 'TQ':
                        print("Tatkal quota is only available for booking for tomorrow's date.")
                        print("Choose from the available list ...")
                        continue
                    if bookT.quo not in quota_list:
                        print("Entered Quota does not exist !")
                        print("Choose from the available list ...")
                        continue
                    else:
                        break
                print("---------------------------------------------")
                print("Class Codes:")
                print(tabulate([['1st AC', '1A'], ['2nd AC', '2A'], ['3rd AC', '3A'], ['Sleeper', 'SL']], headers=['Class', 'Code']))
                print("---------------------------------------------")
                while True:
                    bookT.cls = input("Class : ")
                    if bookT.cls not in class_list:
                        print("Entered Class does not exist !")
                        print("Choose from the available list ...")
                        continue
                    else:
                        break
                print("---------------------------------------------")
                bookT.check_seat()  


        if choice == '2':

            ticket_status().check_status()

        if choice == '3':

            print("---------------------------------------------")
            show_available_trains().available_trains()
            print("---------------------------------------------")

        if choice == '4':

            print("---------------------------------------------")
            print("\tThank You for Visiting RailWise !")
            print("---------------------------------------------")
            exit(0)
