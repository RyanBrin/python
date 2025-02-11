# nim
# Ryan Brinkman
# 11/16/2023

# imports
import random
import re

# variables
rocks = random.randint(15, 30)
minusRocks = 0
p1 = ""
p2 = ""
player = p1
negativeRocks = 0


# main
def checkRocks():
  if rocks > 0:
    game()
  elif rocks == 0:
    if player == p1:
      print("")
      print(p2 + " was stuck with the last rock!")
      print(p1 + " has won the game!")
      print("")
    elif player == p2:
      print("")
      print(p1 + " was stuck with the last rock!")
      print(p2 + " has won the game!")
      print("")


def changePlayer():
  global player
  player = p2 if player == p1 else p1


def chooseName1():
  p1 = input("Player 1 - Enter your name: ")
  print("")
  player = p1
  print("player: ", player, "p1: ", p1)
  checkName1(player)


def chooseName2():
  p2 = input("Player 2 - Enter your name: ")
  print("")
  player = p2
  print("player: ", player, "p2: ", p2)
  checkName2(player)


def checkName1(player):
  regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
  if (regex.search(player) == None):
    chooseName2()
  else:
    print("")
    print("ERROR: Your name may only contain letters, and numbers")
    chooseName1()


def checkName2(player):
  regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
  if (regex.search(player) == None):
    game()
  else:
    print("")
    print("ERROR: Your name may only contain letters, and numbers")
    chooseName2()


def game():
  global rocks
  global minusRocks
  if rocks > 0:
    print("")
    if player == p1:
      minusRocks = input(p1 + " - There are " + str(rocks) + " rocks, how many would you like to remove? ")
    elif player == p2:
      minusRocks = input(p2 + " - There are " + str(rocks) + " rocks, how many would you like to remove? ")
    print("")
    if minusRocks == "1" or minusRocks == "2" or minusRocks == "3":
      negativeRocks = int(rocks) - int(minusRocks)
      if negativeRocks < 0:
        print("")
        print("ERROR: You can't remove more rocks than there are!")
        print("")
        game()
      rocks = rocks - int(minusRocks)
      changePlayer()
      checkRocks()
    else:
      print("")
      print("ERROR: Please enter a value from 1 to 3")
      print("")
      game()
  elif rocks <= 0:
    None


if __name__ == '__main__':
  chooseName1()
  game()