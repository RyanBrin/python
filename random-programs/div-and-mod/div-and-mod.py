# Ryan Brinkman
# Div And Mod
# Page 100
# 3/23/23

# obtain information
int1 = int(input("Enter an integer: "))
int2 = int(input("Enter a second integer: "))

# calculate
output1 = int(int1 / int2)
output2 = int(int1 % int2)
output3 = int(int2 / int1)
output4 = int(int2 % int1)

# display results
print("")
print(int1, "/", int2, "=", output1)
print(int1, "%", int2, "=", output2)
print("")
print(int2, "/", int1, "=", output3)
print(int2, "%", int1, "=", output4)
