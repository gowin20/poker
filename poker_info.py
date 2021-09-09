#Hardcoded information about how cards in poker work
deck = []

#Default balance
balance = 1000

"""
possible_straights


A2345
23456
34567
45678
56789
678910
78910J
8910JQ
910JQK
10JQKA
"""

#relative numerical values for each hand
hand_values = {
    1:"High Card",
    2:"Pair",
    3:"Two Pair",
    4:"Three of a Kind",
    5:"Straight",
    6:"Flush",
    7:"Full House",
    8:"Four of a Kind",
    9:"Straight Flush",
    10:"Royal Flush"
}

suits = ["Hearts","Diamonds","Clubs","Spades"]

face_cards = {11:"Jack",12:"Queen",13:"King",1:"Ace"}



#copies of this list will be created with the valid actions for each turn

#valid board states in the game of poker. each number is the associated number of cards
states_cards = {"Pre-Flop":0,"Flop":3,"Turn":1,"River":1}
states = ["Pre-Flop","Flop","Turn","River"]


#dictionary for bot players. Each action has a relative weight (adding to 100), which determines the likelihood of the bot picking that action
action_weights = {"check":50,"bet":50,"raise":20,"call":50,"fold":30}

#transitions: tuple object in form (state,action,state)
player_fsa = {
    "states":["opening","response","finished","folded"],
    #valid actions in the game of poker
    "actions":["bet","check","raise","call","all in","fold","reset"],
    "initial":["opening","response"],
    "final":["finished","folded"],
    #the valid actions for each state
    "opening":["bet","check","all in"],
    "response":["raise","call","fold","all in"]
}

card_art = {
    "Hearts":[
        """ _____      
|A_ _ |     
|( v )|     
| \\ / |     
|  .  |     
|____V|     
""",""" _____      
|2    |     
|  v  |     
|     |     
|  v  |     
|____Z|     
""",""" _____      
|3    |     
| v v |     
|     |     
|  v  |     
|____E|     
""",""" _____      
|4    |     
| v v |     
|     |     
| v v |     
|____h|     
""",""" _____      
|5    |     
| v v |     
|  v  |     
| v v |     
|____S|     
""",""" _____      
|6    |     
| v v |     
| v v |     
| v v |     
|____9|     
""",""" _____      
|7    |     
| v v |     
|v v v|     
| v v |     
|____L|     
""",""" _____      
|8    |     
|v v v|     
| v v |     
|v v v|     
|____8|     
""",""" _____      
|9    |     
|v v v|     
|v v v|     
|v v v|     
|____6|     
""",""" _____      
|10 v |     
|v v v|     
|v v v|     
|v v v|     
|___0I|     
""",""" _____      
|J  ww|     
|   {)|     
|(v)  |     
| v   |     
|____[|     
""",""" _____      
|Q  ww|     
|   {(|     
|(v)  |     
| v   |     
|____O|     
""",""" _____      
|K  WW|     
|   {)|     
|(v)  |     
| v   |     
|____>|     
"""],
    "Diamonds":[""" _____      
|A ^  |     
| / \\ |     
| \\ / |     
|  .  |     
|____V|     
""",""" _____      
|2    |     
|  o  |     
|     |     
|  o  |     
|____Z|     
""",""" _____      
|3    |     
| o o |     
|     |     
|  o  |     
|____E|     
""",""" _____      
|4    |     
| o o |     
|     |     
| o o |     
|____h|     
""",""" _____      
|5    |     
| o o |     
|  o  |     
| o o |     
|____S|     
""",""" _____      
|6    |     
| o o |     
| o o |     
| o o |     
|____9|     
""",""" _____      
|7    |     
| o o |     
|o o o|     
| o o |     
|____L|     
""",""" _____      
|8    |     
|o o o|     
| o o |     
|o o o|     
|____8|     
""",""" _____      
|9    |     
|o o o|     
|o o o|     
|o o o|     
|____6|     
""",""" _____      
|10 o |     
|o o o|     
|o o o|     
|o o o|     
|___0I|     
""",""" _____      
|J  ww|     
|   {)|     
| /\\  |     
| \\/  |     
|____[|     
""",""" _____      
|Q  ww|     
|   {(|     
| /\\  |     
| \\/  |     
|____O|     
""",""" _____      
|K  WW|     
|   {)|     
| /\\  |     
| \\/  |     
|____>|     
"""
    ],
    "Clubs":[
""" _____      
|A _  |     
| ( ) |     
|(_'_)|     
|  |  |     
|____V|     
""",""" _____      
|2    |     
|  &  |     
|     |     
|  &  |     
|____Z|     
""",""" _____      
|3    |     
| & & |     
|     |     
|  &  |     
|____E|     
""",""" _____      
|4    |     
| & & |     
|     |     
| & & |     
|____h|     
""",""" _____      
|5    |     
| & & |     
|  &  |     
| & & |     
|____S|     
""",""" _____      
|6    |     
| & & |     
| & & |     
| & & |     
|____9|     
""",""" _____      
|7    |     
| & & |     
|& & &|     
| & & |     
|____L|     
""",""" _____      
|8    |     
|& & &|     
| & & |     
|& & &|     
|____8|     
""",""" _____      
|9    |     
|& & &|     
|& & &|     
|& & &|     
|____6|     
""",""" _____      
|10 & |     
|& & &|     
|& & &|     
|& & &|     
|___0I|     
""",""" _____      
|J  ww|     
| o {)|     
|o.o  |     
| |   |     
|____[|     
""",""" _____      
|Q  ww|     
| o {(|     
|o.o  |     
| |   |     
|____O|     
""",""" _____      
|K  WW|     
| o {)|     
|o.o  |     
| |   |     
|____>|     
"""
    ],
    "Spades":[
""" _____      
|A .  |     
| /.\\ |     
|(_._)|     
|  |  |     
|____V|     
""",""" _____      
|2    |     
|  ^  |     
|     |     
|  ^  |     
|____Z|     
""",""" _____      
|3    |     
| ^ ^ |     
|     |     
|  ^  |     
|____E|     
""",""" _____      
|4    |     
| ^ ^ |     
|     |     
| ^ ^ |     
|____h|     
""",""" _____      
|5    |     
| ^ ^ |     
|  ^  |     
| ^ ^ |     
|____S|     
""",""" _____      
|6    |     
| ^ ^ |     
| ^ ^ |     
| ^ ^ |     
|____9|     
""",""" _____      
|7    |     
| ^ ^ |     
|^ ^ ^|     
| ^ ^ |     
|____L|     
""",""" _____      
|8    |     
|^ ^ ^|     
| ^ ^ |     
|^ ^ ^|     
|____8|     
""",""" _____      
|9    |     
|^ ^ ^|     
|^ ^ ^|     
|^ ^ ^|     
|____6|     
""",""" _____      
|10 ^ |     
|^ ^ ^|     
|^ ^ ^|     
|^ ^ ^|     
|___0I|     
""",""" _____      
|J  ww|     
| ^ {)|     
|(.)  |     
| |   |     
|____[|     
""",""" _____      
|Q  ww|     
| ^ {(|     
|(.)  |     
| |   |     
|____O|     
""",""" _____      
|K  WW|     
| ^ {)|     
|(.)  |     
| |   |     
|____>|     
"""
    ]

}