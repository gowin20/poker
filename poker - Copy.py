import random
import time
import os
import poker_info as info
#import poker_logic as logic

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


#Default balance
balance = 1000
deck = []


"""
for suit in info.card_art:
    for card in info.card_art[suit]:
        print(card)
"""
####################
#
#    HELPER FUNCTIONS
#
####################

#combines two ASCII art strings into a single string. Dependent on the fact that each card is the same height
#returns one string with everything

def combine_Card_Strings(string1,string2,spaces):

    #split on newlines to get a list of each line
    lines_1 = string1.split('\n')
    lines_2 = string2.split('\n')
    #use for loop parsing to join each line together in a list

    output_lines = []
    for i in range(len(lines_1)):
        output_lines.append(lines_1[i] + lines_2[i])

    if spaces:
        output = "\n     "
    else:
        output = "\n"

    output = output.join(output_lines)
    #combinie the list into a string, with the end of each element being a newline

    if spaces:
        output = "     " + output

    return output


#print(combine_Card_Strings(info.card_art["Hearts"][0],info.card_art["Hearts"][1]))

####################
#
#    SMALL CLASSES
#
####################

#Each card has a suit and a value associated with it. Cards will eventually have images associated with them as well.
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

        #name used for printing

        if self.value in info.face_cards:
            val = info.face_cards[self.value]
        else:
            val = self.value
        
        self.name = str(val) + " of " + self.suit

        #set the art
        self.art = info.card_art[suit][value-1]

#All players are part of this generic class. The "isHuman" variable will indicate whether the player is controlled by a human or not.
class Player:
    def __init__(self,number,bal):
        self.holding = []
        self.balance = bal

        self.number = number

        ##TODO: Add in custom names
        self.name = "Player " + str(number)


        self.fsa_state = "opening"


    ####
    ## ACTION FUNCTIONS
    ####

    #prompts the human player for an action, and returns that action as a string
    def human_action(self):
        
        #input variable: current_bet, keeps track of how much the player has to call

        #if they've folded, or don't have an action, just return nothing
        if self.fsa_state == "folded" or self.fsa_state == "finished":
            return
        response = ""
        while response not in info.player_fsa["actions"]:
            #different action prompts are available based off of teh player's current state
            if self.fsa_state == "opening":
                response = input("What is your action? You can Bet or Check.\n")
            elif self.fsa_state == "response":
                response = input("What is your action? You can Call or Raise.\n")
            
            if response not in info.player_fsa["actions"]:
                print("Invalid Action! Please input a valid action.")
        #after selecting an action, cycle player state and return the response
        if response == "fold":
            self.fsa_state = "folded"
        else:
            self.fsa_state = "finished"
        return response
    
    #returns a random valid action
    def bot_action(self):

        #if the bot has no action, it simply exits immediately
        if self.fsa_state == "finished" or self.fsa_state == "folded":
            return
        
        if self.fsa_state == "opening":
            action = random.choices(population=info.opening_actions,weights=info.opening_weights,k=1)[0]
        elif self.fsa_state == "response":
            action = random.choices(population=info.response_actions,weights=info.response_weights,k=1)[0]
        else:
            #only happens when player is in an invalid state
            return False

        #update bot state, then return action
        if action == "fold":
            self.fsa_state = "folded"
        else:
            self.fsa_state = "finished"
        return action



    def bet(self,size,players):

        if self.balance >= size:
            self.balance -= size
        else:
            return -1

        for player in players:
            if player == self:
                continue
            player.fsa_state = "response"
        
    
        return size



    #returns "Player Info:" a string containing the player's name, followed by their pot on a new line

    #print out the player's current Hand
    def print_holding(self):

        print(self.name + "'s Hand: ")
        
        #print out the 2 hole cards
        hand = combine_Card_Strings(self.holding[0].art,self.holding[1].art,True)
        print(hand)

        for card in self.holding:
            print(card.name,end="\t")
        print("")

    def clear_holding(self):
        self.holding = []

    #functions for bots to make decisions



####################
#
#    Round CLASS
#
####################
states = {"Pre-Flop":0,"Flop":3,"Turn":1,"River":1}
# Round class containing all the information necessary for the current Round.
class Round:
    def __init__(self,order):

        #list containing board cards
        self.board = []
        self.current_state = ""
        self.pot = 0
        #copy the deck to deal cards from
        self.current_deck = list(deck)

        #turn order of the players
        self.order = list(order)

    def deal_Hand(self,player):
        for i in range(2):
            #Pick a random card from the deck and add it to the player's hand
            this_card = random.choice(self.current_deck)
            player.holding.append(this_card)

            #remove it from the deck
            self.current_deck.remove(this_card)
        return i
    
    #deals a hand to each player currently playing the game
    def deal_Hands(self):        
        #Deal player's hands
        for player in self.order:
            self.deal_Hand(player)


    #deals the cards for the current round (flop, turn, or river). Deals 0 cards on the pre-flop
    def deal_Round(self):
        #this repeats a number of times according to the current state of the board
        for i in range(states[self.current_state]):
            #pick a random card from the deck and put it on the board
            this_card = random.choice(self.current_deck)            
            self.board.append(this_card)

            #remove it from the deck
            self.current_deck.remove(this_card)
        return True

    #resets all the players in the game to the opening state
    def all_opening(self):
        for player in self.order:
            player.fsa_state = "opening"
        return True


    def actions(self):
        #cycle through each player and prompt for action


        #depending on what the action is, do something

        #while loop
        return True


    #prints the turn order

    #prints out the current board. Combines together each individual card string to do so.
    def print_board(self):

        print("\n\nBoard:")
        board_art = self.board[0].art

        #print out ASCII art of the board cards
        for i in range(1,len(self.board)):
            art2 = self.board[i].art
            if i == 1:
                board_art = combine_Card_Strings(board_art,art2,True)
            else:
                board_art = combine_Card_Strings(board_art,art2,False)

        print(board_art)

        #print out the card names on a new line
        for card in self.board:
            print(card.name,end="\t")
        print("\n")



####################
#
#    GAME CLASS
#
####################


#GAME class contains everything necessary! Includes a record of all previous Rounds as well.
#TODO: Once I migrate to discord, I will make the number of players dynamic. Instead of entering a hardcoded number, the game size will gradually increase. 
#      As long as it's >= 2, you can start the game.
class Game:
    Rounds = []
    def __init__(self,num_players,num_humans):
        self.num_players = num_players
        self.players = []
        self.humans = []

        #Sets up the game by creating the players, and prompting input for the human players
        remaining_people = num_humans
        for i in range(1,num_players+1):
            #Each player has a unique number
            this_player = Player(i,1000)
            
            #add the necessary number of people to the game
            if remaining_people > 0:
                remaining_people -= 1

                #sets the human player's starting balance
                this_player.balance = input("How much money should " + this_player.name + " start with? ")

                #they're a human!
                self.humans.append(this_player)
            else:
                #Bots are marked as such
                this_player.name += " (Bot)"
            
            self.players.append(this_player)
    
    def print_players_info(self,round):
        #print out the turn order at the top
        print("Turn Order:")

        #print out the names first
        names = round[0].name
        for player in round[1:]:
            names = "{0:<15}{1:>15}".format(names,player.name)
        print(names)

        #next, print out the money
        money = round[0].balance
        for player in round[1:]:
            money = "{0:<15}{1:>15}".format(money,player.balance)
        print(money,"\n")

    def update_screen(self,round):

        #clears the screen first
        os.system('cls' if os.name == 'nt' else 'clear')
        #prints everything. hand at the bottom of the screen, with the board directly above it.

        #print the players' info first
        self.print_players_info(round)

        #print out the current board
        state = self.current_Round.current_state
        if state != "Pre-Flop":
           
            self.current_Round.print_board()
        
        #print out the current pot
        print("\n\t\t\t Pot: 0 \n\n")


        #print out the human players' current hands.
        ## TODO: Combine multiple player hands so they reside on the same line? perhaps
        ### Don't really worry about graphics for multiple players rn though
        for player in self.players:
            if player in self.humans: 
                player.print_holding()

    
        return True


    #Main function which plays a Round


    def play_Round(self):

        #Each hand is a unique round object
        self.current_Round = Round(self.players)

        print("players: ",self.current_Round.order)
        self.current_Round.deal_Hands()

        #main loop to play the game. Cycles through each board state
        for state in info.states:
            
            #get the next state
            self.current_Round.current_state = state

            #Deal cards to the board, with the number set according to the current state
            self.current_Round.deal_Round()


            #cycle through every person in the round
            #temporary list for this turn
            this_turn = list(self.current_Round.order)
    
            #this_turn[-1] = dealer
            #this_turn[0] = SB
            #this_turn[1] = BB

            #the pre-flop has a special case, where a bet is made already
            #if state == "Pre-Flop"
            #starts on this_turn[2]

            #updates the screen with current cards and all.
            self.update_screen(this_turn)
            finished = []
            input("Betting for the " + state + " will now begin, following the order above. Press ENTER to Continue.\n")
            while this_turn:
                
                this_player = this_turn.pop(0)
                print("\n" + this_player.name + " will now take an action.")
                time.sleep(1)
                #take an action
                if this_player in self.humans:
                    player_action = this_player.human_action()
                else:
                    player_action = this_player.bot_action()
                    print(this_player.name + " " + player_action + "s.")
                    time.sleep(1)
                
                #fold players that fold
                if player_action == "fold":
                    self.current_Round.order.remove(this_player)

                #let people be "finished" once performing a certain action
                if player_action == "check":
                    finished.append(this_player)
                elif player_action == "call":
                    finished.append(this_player)
                
                elif player_action == "bet" or player_action == "raise":
                    #decrease their funds according to how much
                    
                    #you're not done yet, guys!
                    this_turn = this_turn + finished
                    finished = []
                    finished.append(this_player)
                    #set player state
                    for player in this_turn:
                        if player == this_player:
                            continue
                        player.fsa_state = "response"
                    


                if this_turn:
                    self.update_screen(this_turn)
                #print(finished)

            if state != "River":
                next = info.states[info.states.index(state)+1]
                input("\nPress ENTER to continue to the " + next + ".")
            else:
                input("\nPress ENTER to continue.")

            self.current_Round.all_opening()
            #if the action is bet or raise, set all other players' states to response

            #prompt each for action


            #update screen with action

            #if that action causes a reset, reset each player to the response state. Additionally, add players which have already gone to the end of the turn order list
        #cycle the player turn order, so that the next round has a different order
        dealer = self.players.pop(0)
        self.players.append(dealer)

        return True


            


####################
#
#    MAIN PROGRAM
#
####################

#Start by creating a deck of cards
deck = []

#The deck contains 13 cards of each suit, for a total of 52 cards.
for suit in info.suits:
    for val in range(1,14):
        deck.append(Card(suit,val))

"""
#print out the deck
for card in deck:
    #print(card)
    print(card.name)

print(len(deck))
"""


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


game = Game(num_p,num_h)
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
    game.play_Round()

    #Exit condition
    if input("Type STOP if you want to quit, or press ENTER to continue").upper() == "STOP":
        playing = False
    
    #reset player's holdings at the end of each Round
    for player in game.players:
        player.clear_holding()


#Create a list of players, based off of player input


#create a game object with all the information we just put together
