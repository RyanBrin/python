# Ryan Brinkman
# Mod Num Guess
# 2/13/2024
# https://github.com/ryanbrin/

# imports
import random
import os

# variables
num = random.randint(1, 50)
hints = "Your hints: "
tick1 = 0
tick2 = 0
tick3 = 0
tick4 = 0
tick5 = 0
tick6 = 0
tick7 = 0
tick8 = 0
tick9 = 0
game_over = False

# main
os.system('cls')
while game_over == False:
    print("Enter h1 - h9 for hints and use them to figure out the number (uses mod division)\n")
    print(hints + "\n")
    guess = str(input("Enter h1 - h9 or enter your number guess: "))
    if guess == "h1" or guess == "h2" or guess == "h3"  or guess == "h4"  or guess == "h5"  or guess == "h6"  or guess == "h7"  or guess == "h8"  or guess == "h9":
        if guess == "h1":
            if tick1 != 1:
                tick1 = 1
                hints = hints + ("([1] x % 1 = " + str(num % 1) + ") ")
                os.system('cls')
            else:
                os.system('cls')
                print("\n" + "Hint already used!\n")
        if guess == "h2":
            if tick2 != 1:
                tick2 = 1
                hints = hints + ("([2] x % 2 = " + str(num % 2) + ") ")
                os.system('cls')
            else:
                os.system('cls')
                print("\n" + "Hint already used!\n")
        if guess == "h3":
            if tick3 != 1:
                tick3 = 1
                hints = hints + ("([3] x % 3 = " + str(num % 3) + ") ")
                os.system('cls')
            else:
                os.system('cls')
                print("\n" + "Hint already used!\n")
        if guess == "h4":
            if tick4 != 1:
                tick4 = 1
                hints = hints + ("([4] x % 4 = " + str(num % 4) + ") ")
                os.system('cls')
            else:
                os.system('cls')
                print("\n" + "Hint already used!\n")
        if guess == "h5":
            if tick5 != 1:
                tick5 = 1
                hints = hints + ("([5] x % 5 = " + str(num % 5) + ") ")
                os.system('cls')
            else:
                os.system('cls')
                print("\n" + "Hint already used!\n")
        if guess == "h6":
            if tick6 != 1:
                tick6 = 1
                hints = hints + ("([6] x % 6 = " + str(num % 6) + ") ")
                os.system('cls')
            else:
                os.system('cls')
                print("\n" + "Hint already used!\n")
        if guess == "h7":
            if tick7 != 1:
                tick7 = 1
                hints = hints + ("([7] x % 7 = " + str(num % 7) + ") ")
                os.system('cls')
            else:
                os.system('cls')
                print("\n" + "Hint already used!\n")
        if guess == "h8":
            if tick8 != 1:
                tick8 = 1
                hints = hints + ("([8] x % 8 = " + str(num % 8) + ") ")
                os.system('cls')
            else:
                os.system('cls')
                print("\n" + "Hint already used!\n")
        if guess == "h9":
            if tick9 != 1:
                tick9 = 1
                hints = hints + ("([9] x % 9 = " + str(num % 9) + ") ")
                os.system('cls')
            else:
                os.system('cls')
                print("\n" + "Hint already used!\n")
    else:
        if guess == num:
            os.system('cls')
            print("\n" + "You won\n")
            print("The number was " + str(num) + "\n")
            game_over = True
        else:
            os.system('cls')
            print("\n" + "You lost\n")
            print("The number was " + str(num) + "\n")
            game_over = True