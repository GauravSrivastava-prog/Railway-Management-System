# Dictionary is a derived data type. It's data type is dictionary itself.

# Syntax : this-dict = {"brand" : "ford" , "model" : "Mustang" , "year" : 1996}

# Normal Dictionary Defination :
car = {"Brand" : "Ford" , "Name" : "Mustang" , "Year" : "1996" , "Year" : "1997"} # We overwrite the 'key' = year here from 1996 to 1997...

# Constructor Dictionary Defination :
car2 = dict(Brand = "Nissan" , Name = "Supra - GTR" , Year = "2003") # But we can not overwrite the year here, it will throw an error...
                                                                    # Because we can not pass two same parameters inside a constructor...
print("First Dictionary : ")
print(car)
print("Second Dictionary : ")
print(car2)
print(car["Name"]) #Prints the value if the 'key' = name
print("Length of car dictionary is : ",len(car))

# Methods inside Dictionary (Pre-built Functions) :
# clear() -> Value at a particular key gets removed...
car.clear() # Completely clears the dictionary...
print(car) # It is a non-parameterised function, we can not clear a particular key in dictionary, it completley wipes out...
# copy() -> Copies the values of one dictionary to another...
dic1  = {"Name" : "Gaurav", 20 : [1,2,3] , 30 : "c"}
dic2 = dic1.copy()
print("New Copy : ",dic2)
dic2["Name"] = "Sahil"
dic2[20][0] = "a"
dic2[30] = 1
print(dic2)
# get() -> It's a secured method to access value from dictionary, why secured ? because if the key is not present then it won't throw any error, it will just print "None"
print(car2.get('Name'))
print(car.get("Engine")) # When we pass a key in "get" which is not present in the dictionary then it returns "None"
# Keys()
k = car2.keys()
print(k)
# fromKeys() 
x = {"Key1","Key2","Key3"} # This is a set , not a dictionary...
value = 0
dic3 = dict.fromkeys(x,value)
print(dic3)
# update()
# Values()
car2["Brand"] = "Maruti"
car2["Name"] = "Breeza"
k2 = car2.values()
print(k2) # prints only values...
# pop()
