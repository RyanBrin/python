# NOTES

name = "Ryan Brinkman"

first_name = name[0:4] # or :4
last_name = name[5:] # or 5:13
funky_name = name[0:13:2] # or ::2 or :end:2
reversed_name = name[0:13:-1] # or ::-1 

print(first_name)
print(last_name)
print(funky_name)

website1 = "https://google.com/"
website2 = "https://paloaltonetworks.com/"

slice = slice(8,-5)

print(website1[slice])
print(website2[slice])

num = 2
if not(num == 1):
    print("num does not equal 1")

name = ""

while not(len(name)) == 0:
    name = input("Please enter your name: ")

print("Hello " + name)

for i in range(10,100 + 1, 2):
    print(i)

import time

for seconds in range(10, 0, -1):
    print(seconds)
    time.sleep(1)
print("Happy New Year!")

rows = int(input("How many rows? "))
columns = int(input("How many columns? "))
symbol = input("Enter a symbol to use: ")

for i in range(rows):
    for j in range(columns):
        print(symbol, end = "")
    print()

# WHILE LOOPS
# break - terminate
# continue - skip
# pass - do nothing

# LISTS
# append - append("value")
# remove - remove(index, "value")
# pop - remove last item in list
# insert - insert(index, "value")
# sort - alphabetically sort list
# clear - clear list

# TUPLES
# tuple - ordered and unchangeable list (uses '()' notation)
human = ("Ryan", 16, "male")

# DATA SETS

new_set = {}
list1 = {}
list2 = {}

# data set - unordered and unindexed list with no dupe values (uses '{}' notation)
utensils = {"fork", "spoon", "knife"}
# add - adds item
# remove - removes item
# clear - clears item
# update - adds two data sets 
list.update(list2)
# join - adds and creates new set 
new_set = list1.union(list2)
# difference - gets what one list has that another does not 
list1.difference(list2)
# intersection - gets what both lists have in common 
list1.intersection(list2)

# DICTIONARY
# dictionary - changable, unordered collection of value pairs that use '{}' notation and are fast due to hashing
people = {"Ryan":16,
         "Kaden":15, 
         "Alonso":16}
print(people["Ryan"]) # returns 16
print(people.get["Kash"]) # returns None instead of error like the one above if item isn't found
print(people.keys())
print(people.values())
print(people.items())

for key, value in people.items(): # returns entire dictionary
   print(key, value)

people.update({"Kash":15})
people.update({"Ryan":21}) # to give new value

people.pop("Ryan")
people.clear()

# FUNCTIONS
# return - sends values back to the caller

def multiply(num1, num2):
    return num1 * num2

x = multiply(6,8)

print(x)

# KEYWORD ARGS
# ENDED COURSE OFF AT KEYWORD ARGS AT 2:05:15