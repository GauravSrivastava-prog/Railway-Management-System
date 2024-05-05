import csv
import random
import os
from datetime import datetime, timedelta
from tabulate import tabulate
import pandas as pd

class show_available_trains:
    def available_trains(self):
        print("---------------------------------------------")
        print("\tList Of Trains Running Right Now !")
        print("---------------------------------------------")
        with open("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                print("->",row['Train_Name'])

class book_ticket:
    src = ""
    des = ""
    dod = ""
    cls = ""
    quo = ""
    dep_time = ""
    arr_time = ""
    trnum = ""
    trname = ""
    user_name = ""
    user_age = ""
    user_num = ""
    user_gender = ""
    user_nationality = ""
    pnr = ''.join(random.choices('0123456789', k=12))
    seat_number = ""
    birth_type = ""
    user_email = ""
    waiting = 0
    available = 0
    route = []
    
    def route_calculate(self):
        df = pd.read_csv("/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/Trains.csv")
        train_schedule = df[df['Train_Name'] == self.trname]
        stations = train_schedule['Stations'].iloc[0].split(", ")
        from_index = stations.index(self.src)
        to_index = stations.index(self.des)
        self.route = stations[from_index:to_index+1]    
        
    def register(self):
        print("---------------------------------------------")
        self.user_name = input("Name :\t")
        self.user_age = input("Age :\t")
        self.user_gender = input("Gender :\t")
        self.user_nationality = input("Nationality :\t")
        self.user_num = input("Number :\t")
        self.user_email = input("Email :\t")
        path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/User-Data/" + self.pnr + ".csv"
        headers = ['From','To','Train_Name','Route','Train_Number','Name','PNR','Seat_Number','Birth_Type','Quota','Class','Date_Of_Departure','Age','Gender','Nationality','Number','Email']
        data = {'From':self.src,'To':self.des,'Train_Name':self.trname,'Train_Route':self.route,'Train_Number':self.trnum,'Name':self.user_name,'PNR':self.pnr,'Seat_Number':self.seat_number,'Birth_Type':self.birth_type,'Quota':self.quo,'Class':self.cls,'Date_Of_Departure':self.dod,'Age':self.user_age,'Gender':self.user_gender,'Nationality':self.user_nationality,'Number':self.user_num,'Email':self.user_email}
        with open(path, 'a', newline='') as file:
            writer = csv.writer(file)
            for key, value in data.items():
                writer.writerow([key, value])

    def available_seat_calculator(self):
        path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/" + self.trnum + ".csv"
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.cls == row['Class'] and self.quo == row['Quota'] and row['Booking_Status'] == "True" and row['Current_Station'] in self.route:
                    self.available += 1

    def waiting_list_calculator(self, wquo):
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
        for row in train_data:
            station_list = row['Stations'].split(', ')
            if src_lower in [station.lower() for station in station_list] and des_lower in [station.lower() for station in station_list]:
                if not found_train:
                    print("Available Train ->")
                    print(row['Train_Name'])
                    self.trname = row['Train_Name']
                    self.route_calculate()
                    self.trnum = row['Train_No.']
                    found_train = True

        if not found_train:
            print("Train Not Found !")
            exit(0)

        self.trname = input("Choose Train : ")
        for row in train_data:
            if row['Train_Name'].lower() == self.trname.lower():
                self.trnum = row['Train_No.']
                return True

    
    def check_seat(self):
        path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/" + self.trnum + ".csv"
        available_seats = False

        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.cls == row['Class'] and row['Quota'] == self.quo and row['Current_Station'] in self.route:
                    if row['Booking_Status'] == "True": 
                        print("---------------------------------------------")
                        print("Checking for " + self.quo + " Seats...")
                        no_of_seats = self.available_seat_calculator()
                        print("Available Seats:\t", no_of_seats)
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
                print("Exiting...")
                exit(0)

if __name__ == "__main__":
    quota_list = ['GN', 'LD', 'HP', 'DF', 'YU','TQ']
    class_list = ['1A', '2A', '3A', 'SL']
    while True:
        print("\t\t Welcome to RailWise\n\tThe Smart Railway Management System...")
        print("---------------------------------------------")
        print("1 ->\t Book Ticket")
        print("2 ->\t Cancel Ticket")
        print("3 ->\t Your Ticket Status")
        print("4 ->\t Show Available Trains")
        print("5 ->\t Exit")
        print("---------------------------------------------")
        
        choice = input("Enter Choice User : ")

        if choice == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
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

            else:
                print("Wrong Train Input !")

        if choice == '3':
            os.system('cls' if os.name == 'nt' else 'clear')

        if choice == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("---------------------------------------------")
            show_available_trains().available_trains()
            print("---------------------------------------------")
        
        if choice == '5':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("---------------------------------------------")
            print("\tThank You for Visiting RailWise !")
            print("---------------------------------------------")
            exit(0)
