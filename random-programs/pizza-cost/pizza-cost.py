# Ryan Brinkman
# Pizza Cost
# Page 99
# 3/5/23

# obtain info
diameter = int(input("Enter the diameter of the pizza in inches: "))

# calculate
cost = 0.05 * diameter * diameter
cost = cost + 1.75
cost = str(cost)

# display
print("The cost of making the pizza is: $" + cost)