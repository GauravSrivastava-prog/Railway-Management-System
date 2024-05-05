import csv
import random

quota_values = ['GN', 'TQ', 'LD', 'HP', 'PH', 'DF', 'YU']
birth_type_values = ['Lower', 'Upper', 'Side']
booking_status = [True,False]
path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/12002.csv"
counter = 0


with open(path, mode='a', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["Class", "Quota", "Seat_No.", "Birth_Type","Booking_Status"])
    # Write random values
    for i in range(1,5):
        for j in range(1,25):
            if (counter == 0):
                rows = ["1A",random.choice(quota_values),j,random.choice(birth_type_values),random.choice(booking_status)]
                writer.writerow(rows)
                
            elif (counter == 1):
                rows = ["2A",random.choice(quota_values),j,random.choice(birth_type_values),random.choice(booking_status)]
                writer.writerow(rows)
            
            elif (counter == 2):
                rows = ["3A",random.choice(quota_values),j,random.choice(birth_type_values),random.choice(booking_status)]
                writer.writerow(rows)
            
            else:
                rows = ["SL",random.choice(quota_values),j,random.choice(birth_type_values),random.choice(booking_status)]
                writer.writerow(rows)
        counter = counter + 1
            

