def check_seat(self):
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        entered_date = datetime.strptime(self.dod, '%Y-%m-%d').date() # Not Working !
        print("---------------------------------------------")
        path = "/Users/gauravsrivastava1212/python-programming/End-Sem-Pro/CSV-Files/" + self.trnum + ".csv"
        available_seats = False  # Flag to track if any seat with the requested quota is available
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.cls == row['Class'] and row['Quota'] == self.quo:
                    if row['Booking_Status'] == "True":
                        print("---------------------------------------------")
                        print("Your Ticket has been Successfully Generated !")
                        print(tabulate([['From :',self.src],['To :',self.des],['Train Name :',self.trname],['Train Number :',self.trnum],['Class :',self.cls],['Quota :',self.quo],['Date Of Departure :',self.dod],['Seat Number :',random.choice(row['Seat_No.'])],['Birth Type :',row['Birth_Type']]]))
                        print()
                        print("Thank You For Visiting Us !")
                        print()
                        print("Redirecting You To Home Page...")
                        print()
                        available_seats = True
                    elif row['Booking_Status'] == "False" and not available_seats:
                        available_seats = False

        if not available_seats:
            print("---------------------------------------------")
            print("Checking for " + self.quo + " Seats...")
            waiting_list = self.waiting_list_calculator(self.quo)
            print("Waiting List:\t", waiting_list)
        print("---------------------------------------------")

            
