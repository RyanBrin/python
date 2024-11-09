# Ryan Brinkman
# Object Height
# Page 99
# 3/5/23

# obtain information & calculate
time = float(input("Enter a time less than 4.5 seconds: "));
if time > 4.5: print("4.5ERROR: Time is greater than 4.5 seconds!");
height = 100 - 4.9 * time * time

#display
print("The height of the object is: ", height)