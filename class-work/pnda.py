import pandas as pd

data = {'A': [20], 'B': [10], 'C': [30], 'D': [40], 'E': [50]}
df1 = pd.DataFrame(data)
writer1 = pd.ExcelWriter('/Users/gauravsrivastava1212/python-programming/class-work/OldData.xlsx', engine='xlsxwriter')  
df1.to_excel(writer1, sheet_name='Sheet1', index=False)  
writer1._save()


modified_data = {key: [value[0] + 2] for key, value in data.items()}  

df2 = pd.DataFrame(modified_data, index=[0])
writer2 = pd.ExcelWriter('/Users/gauravsrivastava1212/python-programming/class-work/NewData.xlsx', engine='xlsxwriter')  
df2.to_excel(writer2, sheet_name='Sheet1', index=False)  
writer2._save()



