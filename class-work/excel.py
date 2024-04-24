import pandas as pd


data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 22], 'City': ['New York', 'London', 'Paris']}
df = pd.DataFrame(data)

writer = pd.ExcelWriter('/Users/gauravsrivastava1212/python-programming/class-work/NewExcel.xlsx', engine='xlsxwriter')  
df.to_excel(writer, sheet_name='Sheet1', index=False)  
writer._save()
df.to_csv('/Users/gauravsrivastava1212/python-programming/class-work/NewExcel.csv', index=False)  
