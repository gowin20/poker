from poker_players import Player
from poker_round import Round

import poker_info as info

from poker_logic import play_cards
from poker_logic import hand_info
from poker_logic import determine_winner
from poker_logic import hand_names

import os
import time



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
                this_player.balance = int(input("How much money should " + this_player.name + " start with? "))

                #they're a human!
                self.humans.append(this_player)
            else:
                #Bots are marked as such
                this_player.name += " (Bot)"
            
            self.players.append(this_player)
    

    ### PRINTS the state of all players in the current round. prints their balance, and in the proper turn order
    def print_players_info(self,turn_order):
        #print out the turn order at the top
        print("Turn Order:")

        #print out the names first
        names = turn_order[0].name
        for player in turn_order[1:]:
            names = "{0:<15}{1:>15}".format(names,player.name)
        print(names)

        #next, print out the money
        money = turn_order[0].balance
        for player in turn_order[1:]:
            money = "{0:<15}{1:>15}".format(money,player.balance)
        print(money,"\n")

    
    #ends the round properly, by determining the winner then assigning chips accordingly
    def round_end(self):
        
        #DETERMINE THE WINNER
        winner = determine_winner(self.current_Round)

        if isinstance(winner,list):
            print("It's a tie!")
        else:
            their_cards = play_cards(winner.holding,self.current_Round.board)
            their_info = hand_info(their_cards)
            
            print(winner.name + " wins " + str(self.current_Round.pot) + " chips with " + hand_names(their_info))

            winner.balance += self.current_Round.pot

        input("\nPress ENTER to continue.")

    
    def update_screen(self,turn_order):

        #clears the screen first
        os.system('cls' if os.name == 'nt' else 'clear')
        #prints everything. hand at the bottom of the screen, with the board directly above it.

        #print the players in the round first
        self.print_players_info(turn_order)

        #print out the current board
        state = self.current_Round.current_state
        
        if state != "Pre-Flop":
           
            print("\n\nBoard:")
            board_art = self.current_Round.board[0].art

            #print out ASCII art of the board cards
            for i in range(1,len(self.current_Round.board)):
                art2 = self.current_Round.board[i].art
                if i == 1:
                    board_art = combine_Card_Strings(board_art,art2,True)
                else:
                    board_art = combine_Card_Strings(board_art,art2,False)

            print(board_art)

            #print out the card names on a new line
            for card in self.current_Round.board:
                print(card.name,end="\t")
            print("\n")
        
        #print out the current pot
        print("\n\t\t\t Pot: "+ str(self.current_Round.pot))
        print("\t\t Current Bet: " + str(self.current_Round.current_bet) + "\n\n")
        #print out the human players' current hands.
        ## TODO: Combine multiple player hands so they reside on the same line? perhaps
        ### Don't really worry about graphics for multiple players rn though
        for player in self.players:
            if player in self.humans: 
                print(player.name + "'s Hand: ")
        
                #print out the 2 hole cards
                hand = combine_Card_Strings(player.holding[0].art,player.holding[1].art,True)
                print(hand)

                for card in player.holding:
                    print(card.name,end="\t")

                #print out the current hand ranking
                their_cards = play_cards(player.holding,self.current_Round.board)
                their_ranking = info.hand_values[hand_info(their_cards)["rank"]]
                print("\n Hand Rank: " + their_ranking)
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
                    player_action = this_player.human_action(self.current_Round)
                else:
                    player_action = this_player.bot_action(self.current_Round)
                    print(this_player.name + " " + player_action + "s.")
                    time.sleep(1)
                
                #TURN ORDER LOGIC
                #fold players that fold
                if player_action == "fold":
                    self.current_Round.order.remove(this_player)

                #let people be "finished" once performing a certain action
                if player_action == "check":
                    finished.append(this_player)
                elif player_action == "call":
                    finished.append(this_player)
                
                elif player_action == "bet" or player_action == "raise" or player_action == "all in":
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
            
            #the round ends when all but one person folds
            if len(self.current_Round.order) == 1:
                self.round_end()
            if state != "River":
                next = info.states[info.states.index(state)+1]
                input("\nPress ENTER to continue to the " + next + ".")
            else:
                #the round ends after the river
                self.round_end()


            # let the players know they're takin another action
            self.current_Round.all_opening()

            #if the action is bet or raise, set all other players' states to response

            #prompt each for action


            #update screen with action

            #if that action causes a reset, reset each player to the response state. Additionally, add players which have already gone to the end of the turn order list
        #cycle the player turn order, so that the next round has a different order
        dealer = self.players.pop(0)
        self.players.append(dealer)

        return True