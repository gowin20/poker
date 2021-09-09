import poker_info as info
import random
####################
#
#    Round CLASS
#
####################

# Round class containing all the information necessary for the current Round.
class Round:
    def __init__(self,order):

        #list containing board cards
        self.board = []
        self.current_state = ""
        self.pot = 0


        self.current_bet = 0
        self.leading_player = ""

        #copy the deck to deal cards from
        self.current_deck = list(info.deck)

        #turn order of the players
        self.order = list(order)

        self.all_opening()

    def deal_Hand(self,player):
        for i in range(2):
            #Pick a random card from the deck and add it to the player's hand
            this_card = random.choice(self.current_deck)
            player.holding.append(this_card)

            #remove it from the deck
            self.current_deck.remove(this_card)
        return i
    
    #the player places a bet of a given amount
    def place_bet(self,player,amount):
        pass

    #deals a hand to each player currently playing the game
    def deal_Hands(self):        
        #Deal player's hands
        for player in self.order:
            self.deal_Hand(player)


    #deals the cards for the current round (flop, turn, or river). Deals 0 cards on the pre-flop
    def deal_Round(self):
        #this repeats a number of times according to the current state of the board
        for i in range(info.states_cards[self.current_state]):
            #pick a random card from the deck and put it on the board
            this_card = random.choice(self.current_deck)            
            self.board.append(this_card)

            #remove it from the deck
            self.current_deck.remove(this_card)
        return True

    #resets all the players in the game to the opening state
    def all_opening(self):
        for player in self.order:
            if player.fsa_state == "folded":
                continue
            player.fsa_state = "opening"
            player.amount_bet = 0
        self.current_bet = 0
        return True