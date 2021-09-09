#constants and logic
import poker_info as info
#import poker_logic as logic

#all major classes
#from poker_round import Round
#from poker_players import Player
from poker_game import Game
from poker_logic import Card

"""
MASTER TODO

Fix the "bet" function
add in "size comparison" information - start a new file for "poker_logic"
fix the other todos
work towards a better UI
bugs bugs bugsk
"""



#TODO: Code special exception for "Ace" allowing it to be high or low. Currently represented as just 1
    #add a 14:ace entry?
    #write code to automatically wrap around once it hits 13


####################
#
#    MAIN PROGRAM
#
####################

#Start by creating a deck of cards


#The deck contains 13 cards of each suit, for a total of 52 cards.
for suit in info.suits:
    for val in range(1,14):
        info.deck.append(Card(suit,val))

#CREATE A GAME. We specify how many players to have, and how many human players we want as well.

### TODO: For discord migration, add this stuff to a separate file with includes. The file then executes when the command arg "-poker n" is executed, where n is the number of players.
# Could still support computer players, but later.

#TODO: Add a "play again?" feature which creates a new GAME with different player counts. Not necessary for a simple program, but good if I ever want to have it on my website.
# Additionally, I can use pygame to make graphics.
print("Welcome to Poker! This is a program which simulates the classic game Texas Hold-em.")

#when creating game, catch errors
valid = False
while not valid:
    num_p = input("How many players would you like the game to have?\n")
    if num_p.isdigit():
        num_p = int(num_p)
        if num_p > 0 and num_p <= 10:
            valid = True
        else:
            print("Sorry, please enter a number between 1 and 10!")
            continue
    else:
        print("Sorry, please enter a number between 1 and 10!")
        continue

    num_h = input("How many human players will there be? (Default 1) \n")
    if num_h.isdigit():
        num_h = int(num_h)
        if num_h < 0 or num_h > num_p:
            num_h = 1
    else:
        num_h = 1


#start the game
game = Game(num_p,num_h)

#print out the players in game
print("Here are the players in the game: ")
for player in game.players:
    print(player.name)
print("\n\n")

#Main game loop. Generate Rounds
playing = True
num_Rounds = 0
while playing:
    #Round loop
    num_Rounds += 1
    print("Round "+str(num_Rounds)+": ")

    #main function
    game.play_Round()

    #Exit condition
    if input("Type STOP if you want to quit, or press ENTER to start a new round").upper() == "STOP":
        playing = False
    
    #reset player's holdings at the end of each Round
    for player in game.players:
        player.clear_holding()


#Create a list of players, based off of player input


#create a game object with all the information we just put together
