values = [1,2,3,4,5] #Values separated by Commas are called list... They are mutable...ie, they can be changed or modified without creating a new refercence.
values[0] = 9
print(values)
print(type(values)) # type = list
print(len(values))
list1 = [True,False,True] #behaves as a simple list...
print(list1)
print(type(list1))
print(len(list1))

# ------------------------- #

list2 = ["hello","python","world"]
print(list2[:3]) # Goes from 0 to 3
print(list2[::-1]) # Reverses the list
print(list2[1:3]) # Goes from 1 to 2
list2[1:3] = ["Java","C++"] # Replaces the 1 and 2 element with Java and C++
print(list2)

print(len(list2))
# -------------------------- #

list3 = ["Apple","Cherry","Banana","Kiwi",3,1.79]
print(list3)
del list3[3] # Deletes 3rd Index element in the list.
print(list3)
list3.remove(1.79) # Deletes the element 1.79 as soon as it is encountered.

print(list3)
# -------------------------- #

list4 = [1,2,3,4]
list5 = [9,7]
list6 = [100,500]
list4.append(list5) # appends elements of list5 at the end of list 4 as a single element...
print(list4)
list5.insert(2,list6) # inserts elements of list 6 into list 5 at a speciic index position as a single element...
print(list5)
list6.extend(list4) # inserts elements of list 4 into list 6 as individual elements...
print(list6) 
