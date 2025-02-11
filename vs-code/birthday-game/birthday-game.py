# Ryan Brinkman
# Birthday Game
# Page 92-93
# 3/5/23

# obtain info
print("Using paper and pencil, perform the following calculations:")
print("")
print("1. Determine your birth month (January = 1, February = 2 and so on).")
print("2. Multiply that number by 5.")
print("3. Add 6 to that number.")
print("4. Multiply the number by 4.")
print("5. Add 9 to the number.")
print("6. Multiply that number by 5.")
print("7. Add the birth day to the number (10 if on the 10th and so on).")
print("")
playerNum = int(input("Enter your number: "))

# calculate
playerNum = playerNum - 165
birthMonth = int(playerNum / 100)
birthDay = playerNum % 100

# display results
print("Your birthday is ", birthMonth, "/", birthDay)