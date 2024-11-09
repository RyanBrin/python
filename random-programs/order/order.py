# Ryan Brinkman
# Order
# Page 101
# 3/24/23

# obtain information
burgers = int(input("Enter the number of burgers: "))
fries = int(input("Enter the number of fries: "))
sodas = int(input("Enter the number of sodas: "))

# calculate
burgers = burgers * 1.69
fries = fries * 1.09
sodas = sodas * 0.99
cost = burgers + fries + sodas
beforetax = cost
beforetax = str(beforetax)
tax = cost * 0.065
tax = tax
beforetax = float(beforetax)
tax = tax
finaltotal = beforetax + tax
finaltotal = finaltotal


# display results
print("Total before tax: " + "$"+ str(beforetax))
print("Tax: " + "$" + str(tax))
print("Final total: " + "$"+ str(finaltotal))
