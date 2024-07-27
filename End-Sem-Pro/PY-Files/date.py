# Tatkaal Allocation Logic.

from datetime import datetime, timedelta

# Take the random date from the user
today = datetime.now().date()
tomorrow = today + timedelta(days=1)
date = input("Enter Date :\t")
entered_date = datetime.strptime(date, '%Y-%m-%d').date()
if (entered_date == tomorrow):
    print("True")
else:
    print("False")
