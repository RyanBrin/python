# Ryan Brinkman
# Change
# Page 100
# 3/19/23

# obtain information
cents = int(input("Enter the change in cents: "))

# calculate
quarters = int(cents / 25)
cents = cents - (quarters * 25)
dimes = int(cents / 10)
cents = cents - (dimes * 10)
nickles = int(cents / 5)
cents = cents - (nickles * 5)
pennies = int(cents / 1)
cents = cents - (pennies * 1)

# display results
print("") 
print("The minimum number of coins is:")
print("     Quarters:", quarters)
print("     Dimes:", dimes)
print("     Nickles:", nickles)
print("     Pennies:", pennies)
