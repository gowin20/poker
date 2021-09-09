import poker_info as info
import random

### TODO: Get it all in the same place


#All players are part of this generic class. The "isHuman" variable will indicate whether the player is controlled by a human or not.
class Player:
    def __init__(self,number,bal):
        self.holding = []
        self.balance = int(bal)

        self.number = number

        ##TODO: Add in custom names
        self.name = "Player " + str(number)

        self.fsa_state = "opening"

        self.holding_name = ""

        self.amount_bet = 0


    ####
    ## ACTION FUNCTIONS
    ####

    #prompts the human player for an action, and returns that action as a string
    def human_action(self,round):
        
        #input variable: current_bet, keeps track of how much the player has to call

        #if they've folded, or don't have an action, just return nothing
        if self.fsa_state == "folded" or self.fsa_state == "finished":
            return
        response = ""
        while True:         #response not in info.player_fsa["actions"]:
            #different action prompts are available based off of teh player's current state
            if self.fsa_state == "opening":
                response = input("What is your action? You can Bet or Check.\n").lower()
            elif self.fsa_state == "response":
                response = input("What is your action? You can Call, Raise, or Fold.\n").lower()
            
            if len(response) < 3:
                print("Invalid Action! Please input a valid action.")
                continue

            #code for bets
            if response[0:3] == "bet" and self.fsa_state == "opening":

                components = response.split(" ")
                #error catching
                if len(components) == 2:
                    amount = int(components[1])
                else:
                    print("Invalid bet! To bet, please use the format \"bet <amount>\"")
                    continue
                #error catching
                if amount > self.balance:
                    print("Bet too large! Please bet an amount between 1 and " + str(self.balance) + " chips.")
                    continue

                #place the bet
                round.pot += amount
                round.current_bet = amount
                round.leading_player = self
                self.balance -= amount
                self.amount_bet += amount
                response = "bet"

            #check and fold don't need their own "if "

            #RAISING
            elif response[0:4] == "raise" and self.fsa_state == "response":
                components = response.split(" ")
                #error catching
                if len(components) == 2:
                    amount = int(components[1])
                else:
                    print("Invalid raise! To raise the current bet to a specified amount, please use the format \"raise <amount>\"")
                #error catching
                if amount > self.balance:
                    print("Bet too large! Please bet an amount between 1 and " + str(self.balance) + " chips.")
                    continue
                elif amount < (round.current_bet*2):
                    print("Raise too small! Please raise to at least twice the current bet")

                #do the raise
                new_chips = amount - round.current_bet
                round.pot += new_chips
                round.leading_player = self
                self.balance -= (amount - amount_bet)
                self.amount_bet = amount
                response = "raise"

            #CALL
            elif response == "call" and self.fsa_state == "response":
                if self.balance < round.current_bet:
                    print("You do not have enough chips to call! Going all in and making a side pot (NOT FUNCTIONAL YET)")
                    round.pot += self.balance
                    self.amount_bet = self.balance
                    self.balance = 0
                else:
                    round.pot += round.current_bet
                    self.amount_bet += round.current_bet
                    self.balance -= round.current_bet

            if response not in info.player_fsa[self.fsa_state]:
                print("Invalid Action! Please input a valid action.")
                continue

            break
        
        #after selecting an action, cycle player state and return the response
        if response == "fold":
            self.fsa_state = "folded"
        else:
            self.fsa_state = "finished"
        return response
    
    #returns a random valid action
    def bot_action(self,round):

        #if the bot has no action, it simply exits immediately
        if self.fsa_state == "finished" or self.fsa_state == "folded":
            return "I should have folded by now!!!"
        
        if self.fsa_state == "opening":
            possible_actions = ["check","bet"]
        elif self.fsa_state == "response":
            possible_actions = ["raise","fold","call"]
            if self.balance < (round.current_bet*2):
                possible_actions.remove("raise")
        else:
            #only happens when player is in an invalid state
            return "something went wrong!"
        
        weights = []
        for action in possible_actions:
            weights.append(info.action_weights[action])

        action = random.choices(population=possible_actions,weights=weights,k=1)[0]

        #update bot state, then return action
        if action == "fold":
            self.fsa_state = "folded"
            return action

        if action == "bet":
            if round.pot > 0:
                amount = random.randint(int(round.pot/4),round.pot)
            else:
                amount = random.randint(1,(self.balance/10))
            
            #place the bet
            round.pot += amount
            round.current_bet = amount
            round.leading_player = self
            self.balance -= amount
            self.amount_bet += amount

        elif action == "raise":


            amount = random.randint(round.current_bet*2,self.balance)
            #do the raise
            new_chips = amount - round.current_bet
            round.pot += new_chips
            round.leading_player = self
            self.balance -= (amount - self.amount_bet)
            self.amount_bet = amount

        elif action == "call":
            #going all in
            if self.balance < round.current_bet:
                round.pot += self.balance
                self.amount_bet = self.balance
                self.balance = 0
            #normal calling
            else:
                round.pot += round.current_bet
                self.amount_bet += round.current_bet
                self.balance -= round.current_bet

        elif action == "fold":
            self.fsa_state = "folded"
        else:
            self.fsa_state = "finished"

        self.fsa_state = "finished"
        return action

    #functions for bots to make decisions


    #clears a player's hand and reset for the next round
    def clear_holding(self):
        self.holding = []
        self.holding_name = ""
        self.fsa_state = "opening"