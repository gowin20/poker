import poker_info as info
import random



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
        self.type = str(val)
        self.name = str(val) + " of " + self.suit

        #set the art
        self.art = info.card_art[suit][value-1]

#Each card has a suit and a value associated with it. Cards will eventually have images associated with them as well.
# functions containing the logic for poker hand rankings


#takes in a player's holding and the current board, and returns a list of seven cards - these are the cards which determine the hand a player holds
def play_cards(holding,board):
    cards = []

    for card in holding:
        cards.append(card)
    for card in board:
        cards.append(card)

    return cards


#sorts a list of cards from highest to lowest according to their value
def sort_cards(cards): 
    
    #janky workaround for the Ace
    for card in cards:
        if card.value == 1:
            card.value = 14
    
    #classic insertion sort. Taken from geeksforgeeks because i've written this too many times
    # Traverse through 1 to len(cards) 
    for i in range(1, len(cards)): 
  
        key = cards[i] 
  
        # Move elements of cards[0..i-1], that are 
        # greater than key, to one position ahead 
        # of their current position 
        j = i-1
        while j >= 0 and key.value > cards[j].value : 
                cards[j + 1] = cards[j] 
                j -= 1
        cards[j + 1] = key
    
    #janky ace workaround
    for card in cards:
        if card.value == 14:
            card.value = 1


#returns "num" high cards from a provided list of seven cards
#optionally specify a number/multiple numbers to EXCLUDE - this prevents things like trips or pairs from being included
def high_cards(cards,num,excludes=False):

    #happens when this function is called before the river
    if num > len(cards):
        return []

    highest_cards = []

    #sort the cards
    sort_cards(cards)

    #find the highest cards
    i = 0
    while len(highest_cards) < num:
        #ignore the excludes
        if excludes and cards[i] in excludes:
            i += 1
            continue
        else:
            highest_cards.append(cards[i])
            i += 1

    return highest_cards


### Function which calculates a numerical value for poker hands. 
### Takes IN a list containing 7 total cards, inc. the board + the 2 players
### returns a list containing two pieces of information: the hand value and THE ACTUAL HAND THAT PLAYS


#also returns the 5 CARD HAND THAT PLAYS, IN ORDER OF IMPORTANCE

#Flush: the 5 highest cards of that suit on the board
#Straight: the 5 cards of the straight, from HIGHEST TO LOWEST

#straight flush: the 5 cards of the straight once again, from HIGHEST TO LOWEST
#same for Royal Flush ^

#pair: the 2 cards of the pair, then the next 3 highest cards

#2 pair: the 2 cards in the higher pair, then the 2 cards in the lower pair, then the highest card not in either pair

#trips: the 3 cards in the trips, then the highest 2 cards not in trips
#quads: the 4 cards in the quads, then the highest 1 card not in the quads

#full house: the value of both the trips, and the pair ("trips full of pair")

#if they have the same pair, or the same BOTH pairs, then they go to high cards for comparison. This can be accomplished via the "hand_comparison" function, and doesn't need to be built in to here




def hand_info(cards):
    hand_ranking = 1

    #format the dictionary information it returns
    hand_info = {"rank":1,"info":[]}

    #dictionary that keeps track of how many of each number card there are
    card_nums = {}
    
    #dictionary that keeps track of how many of each suit there are
    card_suits = {}

    for card in cards:
        #add cards to the suits
        if card.suit in card_suits:
            card_suits[card.suit] += 1
        else:
            card_suits[card.suit] = 1
        
        #add cards to the numbers count
        if card.value in card_nums:
            card_nums[card.value] += 1
        else:
            card_nums[card.value] = 1
    
    #print(card_nums,card_suits)

### TOP DOWN

    flush = False
    straight = False
    
    #check for flush
    for suit in card_suits:
        if card_suits[suit] >= 5:
            flush = True
            flush_suit = suit

            #find ALL the cards in the flush - this is the TOP 5 CARDS OF THAT SUIT
            for card in cards:
                if card.suit == flush_suit:
                    #if there's already 5 cards in the flush, make sure that they're the correct cards. It always has to be the FIVE HIGHEST
                    if len(hand_info["info"]) > 5:
                        for flush_card in hand_info["info"]:
                            if card.value > flush_card.value:
                                hand_info["info"].remove(flush_card)
                                hand_info["info"].append(card)
                    else:
                        hand_info["info"].append(card)
    

    #check for straight
    length = 1
    #check for a straight that starts with each card
    for card in cards:    
        this_card = card

        #jacks or higher cannot be the first card in a straight
        if this_card.value >= 11:
            continue

        #check for straights which BEGIN with this_card
        other_cards = list(cards)  
        while other_cards:

            #print("Checking against other cards...")
            other_card = other_cards.pop(0)

            #aces can be high or low - they are encoded as "1" by default, but need to also work as the next card after a King
            #however, they can't be combined together, as they DO NOT wrap around
            if this_card.value == 13 and other_card.value == 1:
                #we know that if this is true, this is a complete straight: 10,11,12,13,14
                #the only way for this card's value to be 13 is if length is already 4
                straight = True
                hand_info["info"] = [other_card]
                break
            
            #if the other card is one higher, we increment length
            if other_card.value == (this_card.value + 1):
                this_card = other_card
                length += 1
                #straights must have length of 5
                if length >= 5:
                    #if we already found a straight
                    if straight:
                        #only store the highest value straight, if multiple are on the board
                        if hand_info["info"][0].value < this_card.value:
                            #store the top card of the straight for reference
                            hand_info["info"] = [this_card]
                    else:
                        #store the top card of the straight for reference
                        hand_info["info"] = [this_card]
                    straight = True
                    break

        length = 1

    #straight flush / royal flush checking
    if straight and flush:
        hand_ranking = 9
        #if the top card of the straight flush is an Ace, it's a royal flush!
        if hand_info["info"].value == 1:
            hand_ranking = 10
    elif flush:
        hand_ranking = 6
    elif straight:
        hand_ranking = 5


    quads = False
    trips = False
    pair1 = False
    pair2 = False
    #check for pairs, check for trips, check for quads
    for card_num in card_nums:
        #quads
        if card_nums[card_num] == 4:
            quads = []
            #only need the value of the card there are four of
            for card in cards:
                if card.value == card_num:
                    quads.append(card)
            break
           
        
        #contains 3 of a kind
        elif card_nums[card_num] == 3:
            trips = []
            for card in cards:
                if card.value == card_num:
                    trips.append(card)
            
        #contains one pair
        elif card_nums[card_num] == 2 and not pair1:
            pair1 = []
            for card in cards:
                if card.value == card_num:
                    pair1.append(card)
        #contains a second pair
        elif card_nums[card_num] == 2:
            pair2 = []
            for card in cards:
                if card.value == card_num:
                    pair2.append(card)

    #quads
    if quads:
        hand_ranking = 8
        last_card = high_cards(cards,1,quads)
        hand_info["info"] = quads + last_card

    #full house
    if trips and pair1:
        hand_ranking = 7

        #add the trips and then the pair to the hand info
        if pair2 and pair2[0].value > pair1[0].value:
            hand_info["info"] = trips + pair2
        else:
            hand_info["info"] = trips + pair1

    #make sure that higher-ranking hands like Straights and Flushes don't accidentally get tagged as a worse hand
    elif hand_ranking >= 5:
        pass
    #3 of a kind
    elif trips:
        hand_ranking = 4

        #find the 2 other cards not present in the trips
        last_cards = high_cards(cards,2,trips)

        #add the trips + 2 cards to the hand info
        hand_info["info"] = trips + last_cards
    
    #2 pair
    elif pair1 and pair2:
        hand_ranking = 3
        #sort the 2 pair + 1 largest card and put them in order
        if pair2[0].value > pair1[0].value:
            hand_info["info"] = pair2 + pair1
        else:
            hand_info["info"] = pair1 + pair2
        #TODO add the fifth card, which is the largest card NOT present in either pair
        
        last_card = high_cards(cards,1,hand_info["info"])[0]
        hand_info["info"].append(last_card)

    #1 pair
    elif pair1:
        hand_ranking = 2
        #add 3 largest cards NOT present in the pair
        largest_three = high_cards(cards,3,pair1)
        
        hand_info["info"] = pair1 + largest_three

    #if nothing else, high card
    else:
        hand_ranking = 1
        #sort the 5 largest cards and put them in order
        hand_info["info"] = high_cards(cards,5)
    
    hand_info["rank"] = hand_ranking
    return hand_info

### Function which compares two hands to determine a winner - takes in two players' holdings and a 5-card board
def compare_hands(p1,p2,board):
    pass

    #if two people have the same numerical hand value (e.g. both have a pair), then the value of the highest cards determines the winner
    p1_cards = play_cards(p1.holding,board)
    p1_info = hand_info(p1_cards)

    p2_cards = play_cards(p2.holding,board)
    p2_info = hand_info(p2_cards)


    if p1_info["rank"] > p2_info["rank"]:
        return p1
    elif p2_info["rank"] > p1_info["rank"]:
        return p2
    else:
        ranking = p1_info["rank"]
        ##same hand type, pick based off of the higher card
        """
        
        TIE BREAKING PARTS

        if rank == 1:
            return 1
        elif rank == 2:

        elif rank == 3:
        elif rank == 4:
        elif rank == 5:
            
        elif rank == 6:
        elif rank == 7:
        elif rank == 8:
        elif rank == 9:
        elif rank == 10:
            return "tie"
        return 1
        """

### Function which takes in a "round" object and outputs the winner of that round. compares all the players still in the game
def determine_winner(round):

    candidates = round.order
    print(round.order)
    if len(candidates) < 1:
        return -1

    if len(candidates) == 1:
        winner = candidates[0]


    winner = candidates.pop(0)    
    while candidates:
        p2 = candidates.pop(0)
        winner = compare_hands(winner,p2,round.board)

    return winner

#returns a STRING containing the name of the hand, depending on the properties passed to it.
### Examples:
# 6-high straight
# pair of kings
# Full House, Threes full of Sixes
# Quad Fours
# Three of a Kind, Nines
# Pair of Kings
# Two Pair, Kings and Jacks
# Royal Flush
# Straight Flush
# King High
def hand_names(hand_info):
    #hand_info is a dictionary formatted as such:
    # {rank:num, info:[]}

    rank = hand_info["rank"]

    if rank == 1:
        return hand_info["info"][0].type + " High"
    elif rank == 2:
        return "Pair of " + hand_info["info"][0].type + "s"
    elif rank == 3:
        return "Two Pair, " + hand_info["info"][0].type + "s" + " and " + hand_info["info"][2].type + "s"
    elif rank == 4:
        return "Three of a Kind, " + hand_info["info"][0].type + "s"
    elif rank == 5:
        return hand_info["info"][0].type + "-High Straight"
    elif rank == 6:
        return hand_info["info"][0].type + "-High Flush"
    elif rank == 7:
        return "Full House, " + hand_info["info"][0].type + "s full of " + hand_info["info"][3].type + "s"
    elif rank == 8:
        return "Four of a kind, " + hand_info["info"][0].type + "s"
    elif rank == 9:
        return hand_info["info"][0].type + " high STRAIGHT FLUSH!!!"
    elif rank == 10:
        return "ROYAL FLUSH BAYBEEEEEEEEEEE"
    else:
        return -1

"""
cards = []
for i in range(7):
    suit = random.choice(info.suits) #info.suits[0]
    value = random.randint(1,13)
    cards.append(Card(suit,value))
#print(cards)


#for card in cards:
#    print(str(card.value) + " of " + card.suit)

analysis = hand_info(cards)

print("Hand Analysis:")

print(hand_names(analysis))

#for card in analysis["info"]:
#    print(card.name)
"""