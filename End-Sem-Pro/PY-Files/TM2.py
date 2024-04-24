import csv
import random
from tabulate import tabulate
import os
from datetime import date, timedelta

def check_seat(cls,quo,dod,trnum):
    today_date = date.today()
    tomorrow_date = today_date + timedelta(days=1)
    print("---------------------------------------------")
    path = "../CSV-Files/" + trnum + ".csv"
    with open(path,'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (cls == row['Class'] and quo == row['Quota']):
                    random_bool = random.choice([True, False])
                    if (random_bool == True and tomorrow_date != dod):
                        print("\tTrains Available !")
                        print("Train Name :\t",row['Train_Name'])
                        print("Train Number :\t",row['Train_No.'])
                        #print("Seats Available :\t",random.randint(1,97))
                    #elif (random_bool == True and tomorrow_date == dod):

def check_train():
    print("Please Enter Details :")
    src = input("From : ")
    des = input("To : ")
    print("\tWarning ! , Mention Date in DD-MM-YYYY format...")
    dod = input("Date Of Departure : ")
    print("---------------------------------------------")
    with open("../CSV-Files/Trains.csv","r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (src.lower() == row['Source'].lower() and des.lower() == row['Destination'].lower()):
                trnum = row['Train_Number']
                print()
                print("Enter the Details as Code...")
                print("---------------------------------------------")
                print(tabulate([['All Classes','A'],['General','GN'],['Tatkal','TQ'],['Ladies','LD'],['Physically Handicapped','HP'],['Defence','DF'],['Yuva','YU']], headers=['Quota','Code']))
                print("---------------------------------------------")
                quo = input("Quota : ")
                print("---------------------------------------------")
                print(tabulate([['1st AC','1A'],['2nd AC','2A'],['3rd AC','3A'],['Sleeper','SL']], headers=['Class','Code']))
                print("---------------------------------------------")
                cls = input("Class : ")
                print("---------------------------------------------")
                check_seat(cls,quo,dod,trnum)


if (__name__ == "__main__"):
    while(True):
        print()
        print("\t\t Welcome to RailWise\tThe Smart Railway Management System...")
        print("---------------------------------------------")
        print("1 ->\t Book Ticket")
        print("2 ->\t Cancel Ticket")
        print("3 ->\t Register Yourself")
        print("4 ->\t Train Status")
        print("5 ->\t Show Available Trains")
        print("6 ->\t Exit")
        print("---------------------------------------------")

        choice = input("Enter Choice User : ")

        if (choice == '1'):
            os.system('cls' if os.name == 'nt' else 'clear')
            check_train() 

        