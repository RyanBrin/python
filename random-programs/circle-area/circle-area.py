# Ryan Brinkman
# Cicle Area
# Page 87
# 3/5/23

import time

# obtain information
print("**************************")
print("*                        *")
print("* Circle Area Calculator *")
print("*                        *")
print("**************************")
print("")
radius = int(input("* Please enter a radius: "))
print("")

# calculate
print("* Calculating... ")
pi = 3.14
area = (radius * radius) * pi

# display
time.sleep(3)
print("")
print("* Area of circle: ", area)
print("")