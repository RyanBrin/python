# Ryan Brinkman
# Sleep
# Page 101
# 3/23/23

# math formula needs to be tweaked to get right answers

# declare variables
days = 0

# obtain information
print("Enter your birthdate:")
birthyear = int(input("Year: "))
birthmonth = int(input("Month: "))
birthday = int(input("Day: "))
print("Enter today's date: ")
currentyear = int(input("Year: "))
currentmonth = int(input("Month: "))
currentday = int(input("Day: "))

# calculate
# years
years = currentyear - birthyear
days = days + (years * 365)
 
# months
months = birthmonth - currentmonth
days = days + (months * 30)

# days
days = days + (birthday - currentday)

# hours
hours = days * 8

# display results
print("You have been alive for", days, "days.")
print("You have slept for",  hours, "hours.")