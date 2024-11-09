# Ryan Brinkman
# Rock Paper Scissors
# Page None
# 3/21/23

# imports
import random
import time
from colorama import Fore

# declare variables
r = "Rock"
p = "Paper"
s = "Scissors"
h = "Hard mode"
n = "Normal mode"
mode = ""
player = ""
computer = 0

#  title & mode selection & player selection
print(Fore.CYAN + "██████╗░██████╗░░██████╗")
print(Fore.CYAN + "██╔══██╗██╔══██╗██╔════╝")
print(Fore.LIGHTCYAN_EX + "██████╔╝██████╔╝╚█████╗░")
print(Fore.LIGHTCYAN_EX + "██╔══██╗██╔═══╝░░╚═══██╗")
print(Fore.LIGHTBLUE_EX + "██║░░██║██║░░░░░██████╔╝")
print(Fore.LIGHTBLUE_EX + "╚═╝░░╚═╝╚═╝░░░░░╚═════╝░")
print("")
print(Fore.RESET + "Made By: " + Fore.LIGHTCYAN_EX + "Ryan Brinkman")
print("")
print("")
print("")
mode = input(Fore.RESET + "Choose either Normal mode (n), or Hard mode (h): ")

#functions
# normal mode function
def normalmode():
  time.sleep(2)
  print("")
  print(Fore.RESET + "Computer is choosing...")
  print("")
  time.sleep(2)
  computer = random.randint(1, 3)
  if computer == 1:
    print(Fore.BLUE + "[🪨 ] Computer chose Rock!")
  elif computer == 2:
    print(Fore.BLUE + "[📄] Computer chose Paper!")
  elif computer == 3:
    print(Fore.BLUE + "[✂️ ] Computer chose Scissors!")
  print("")
  time.sleep(2)
  if player == "r" and computer == 1:
    print(Fore.BLACK + "[🟰 ] The game has been tied!")
  elif player == "r" and computer == 2:
    print(Fore.RED + "[💀] Computer has won the game!")
  elif player == "r" and computer == 3:
    print(Fore.LIGHTYELLOW_EX + "[👑] Player has won the game!")
  elif player == "p" and computer == 1:
    print(Fore.LIGHTYELLOW_EX + "[👑] Player has won the game!")
  elif player == "p" and computer == 2:
    print(Fore.BLACK + "[🟰 ] The game has been tied!")
  elif player == "p" and computer == 3:
    print(Fore.RED + "[💀] Computer has won the game!")
  elif player == "s" and computer == 1:
    print(Fore.RED + "[💀] Computer has won the game!")
  elif player == "s" and computer == 2:
    print(Fore.LIGHTYELLOW_EX + "[👑] Player has won the game!")
  elif player == "s" and computer == 3:
    print(Fore.BLACK + "[🟰 ] The game has been tied!")

# hard mode function
def hardmode():
  time.sleep(2)
  print("")
  print(Fore.RESET +"Computer is choosing...")
  print("")
  time.sleep(2)
  if player == "r":
    print(Fore.BLUE + "[📄] Computer chose Paper!")
    time.sleep(2)
    print("")
    print(Fore.RED + "[💀] Computer has won the game!")
  if player == "p":
    print(Fore.BLUE + "[✂️ ] Computer chose Scissors!")
    time.sleep(2)
    print("")
    print(Fore.RED + "[💀] Computer has won the game!")
  if player == "s":
    print(Fore.BLUE + "[🪨 ] Computer chose Rock!")
    time.sleep(2)
    print("")
    print(Fore.RED + "[💀] Computer has won the game!")

# base code for normal and hard mode
# normal mode base code
if mode == "n":
  print("")
  print(Fore.GREEN + "[👶] Continuing with Normal mode! [👶]")
  print("")
  player = input(Fore.RESET + "Choose either rock (r), paper (p), or scissors (s): ")
  if player == "r" or "p" or "s":
    print("")
    if player == "r":
      print(Fore.BLUE + "[🪨 ] You chose Rock!")
      normalmode()
    if player == "p":
      print(Fore.BLUE + "[📄] You chose Paper!")
      normalmode()
    if player == "s":
      print(Fore.BLUE + "[✂️ ] You chose Scissors!")
      normalmode()

# hard mode base code
if mode == "h":
  print("")
  print(Fore.RED + "[💀] Continuing with Hard mode! [💀]")
  print("")
  player = input(Fore.RESET + "Choose either rock (r), paper (p), or scissors (s): ")
  if player == "r" or "p" or "s":
    print("")
  if player == "r":
    print(Fore.BLUE + "[🪨 ] You chose Rock!")
    hardmode()
  elif player == "p":
    print(Fore.BLUE + "[📄] You chose Paper!")
    hardmode()
  elif player == "s":
    print(Fore.BLUE + "[✂️ ] You chose Scissors!")
    hardmode()