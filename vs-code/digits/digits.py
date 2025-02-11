# Ryan Brinkman
# Digits
# Page 100
# 3/19/23

# imports
import time

# declare variables
billions = 0
hundredmillions = 0
tenmillions = 0
millions = 0
hundredthousands = 0
tenthousands = 0
thousands = 0
hundreds = 0
tens = 0
ones = 0

# obtain information
number = int(input("Enter a number from -9,999,999,999 to 9,999,999,999: "))
print("")

# calculate
if number >= -9999999999 and number <= 99999999999: 
    print("SUCCESS: Number is within the valid range! Your number is:", number)
    billions = int(number / 1000000000)
    number = number - (billions * 1000000000)
    hundredmillions = int(number / 100000000)
    number = number - (hundredmillions * 100000000)
    tenmillions = int(number / 10000000)
    number = number - (tenmillions * 10000000)
    millions = int(number / 1000000)
    number = number - (millions * 1000000)
    hundredthousands = int(number / 100000)
    number = number - (hundredthousands * 100000)
    tenthousands = int(number / 10000)
    number = number - (tenthousands * 10000)
    thousands = int(number / 1000)
    number = number - (thousands * 1000)
    hundreds = int(number / 100)
    number = number - (hundreds * 100)
    tens = int(number / 10)
    number = number - (tens * 10)
    ones = int(number / 1)
    number = number - (ones * 1)
    
# calculating animation
    print("")
    print("Now Calculating Digits...")
    print("")
    print("Calculating...   0% [--------------------]")
    time.sleep(0.5)
    print("Calculating...   5% [|-------------------]")
    time.sleep(0.5)
    print("Calculating...  10% [||------------------]")
    time.sleep(0.5)
    print("Calculating...  15% [|||-----------------]")
    time.sleep(0.5)
    print("Calculating...  20% [||||----------------]")
    time.sleep(0.5)
    print("Calculating...  25% [|||||---------------]")
    time.sleep(0.5)
    print("Calculating...  30% [||||||--------------]")
    time.sleep(0.5)
    print("Calculating...  35% [|||||||-------------]")
    time.sleep(0.5)
    print("Calculating...  40% [||||||||------------]")
    time.sleep(0.5)
    print("Calculating...  45% [|||||||||-----------]")
    time.sleep(0.5)
    print("Calculating...  50% [||||||||||----------]")
    time.sleep(0.5)
    print("Calculating...  55% [|||||||||||---------]")
    time.sleep(0.5)
    print("Calculating...  60% [||||||||||||--------]")
    time.sleep(0.5)
    print("Calculating...  65% [|||||||||||||-------]")
    time.sleep(0.5)
    print("Calculating...  70% [||||||||||||||------]")
    time.sleep(0.5)
    print("Calculating...  75% [|||||||||||||||-----]")
    time.sleep(0.5)
    print("Calculating...  80% [||||||||||||||||----]")
    time.sleep(0.5)
    print("Calculating...  85% [|||||||||||||||||---]")
    time.sleep(0.5)
    print("Calculating...  90% [||||||||||||||||||--]")
    time.sleep(0.5)
    print("Calculating...  95% [|||||||||||||||||||-]")
    time.sleep(0.5)
    print("Calculating... 100% [||||||||||||||||||||]")
    time.sleep(0.75)
    print("")
    print("Calculations Completed! ")
    time.sleep(1)

# display results
    print("")
    print("Now Displaying Digits...")
    time.sleep(2.5)
    print("")
    print("-----------------------------")
    print("| Placement            | =# |")
    print("|---------------------------|")
    if billions >= 0: 
        print("| Billions:            | ", billions, "|")
    else: print("| Billions:            |", billions, "|")
    if hundredmillions >= 0: 
        print("| Hundred-millions:    | ", hundredmillions, "|")
    else: print("| Hundred-millions:    |", hundredmillions, "|")
    if tenmillions >= 0:
        print("| Ten-millions:        | ", tenmillions, "|")
    else: print("| Ten-millions:        |", tenmillions, "|")
    if millions >= 0: 
        print("| Millions:            | ", millions, "|")
    else: print("| Millions:            |", millions, "|")
    if hundredthousands >= 0:
        print("| Hundred-thousands:   | ", hundredthousands, "|")
    else: print("| Hundred-thousands:   |", hundredthousands, "|")
    if tenthousands >= 0:
        print("| Ten-thousands:       | ", tenthousands, "|")
    else: print("| Ten-thousands:       |", tenthousands, "|")
    if thousands >= 0:
        print("| Thousands:           | ", thousands, "|")
    else: print("| Thousands:           |", thousands, "|")
    if hundreds >= 0:
        print("| Hundreds:            | ", hundreds, "|")
    else: print("| Hundreds:            |", hundreds, "|")
    if tens >= 0:
        print("| Tens:                | ", tens, "|")
    else: print("| Tens:                |", tens, "|")
    if ones >= 0:
        print("| Ones:                | ", ones, "|")
    else: print("| Ones:                |", ones, "|")
    print("-----------------------------")
elif number > 9999999999: 
    print("ERROR: Number is not within valid range! (-9,999,999,999 -> 9,999,999,999)")
elif number < -9999999999: 
    print("ERROR: Number is not within valid range! (-9,999,999,999 -> 9,999,999,999)")