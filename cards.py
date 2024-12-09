import random
import statistics

def print_cards(cardlist: list):
    if cardlist == []:
        print('-')
        return
    if not isinstance(cardlist, list):
        print(cardlist)
        return
    if isinstance(cardlist[0],list):
        for sublist in cardlist:
            print('-')
            if len(sublist) > 0: 
                for card in sublist:
                    print(card)
            else:
                print("[]")
        print('-')
    else:
        print('-')
        for card in cardlist:
            print(card)
        print("-")
        

class Card:

    rank_val = {
    "2" : 2,
    "3" : 3,
    "4" : 4,
    "5" : 5,
    "6" : 6,
    "7" : 7,
    "8" : 8,
    "9" : 9,
    "10" : 10,
    "Jack" : 11,
    "Queen" : 12,
    "King" : 13,
    "Ace" : 14
}

    suits = ["Spades", "Hearts", "Diamonds","Clubs"]

    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.rank_val = Card.rank_val[self.rank]
        self.suit = suit

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, rank: str):
        if rank in Card.rank_val:
            self._rank = rank
        else:
            raise ValueError("Invalid Rank")

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, suit: str):
        if suit in Card.suits:
            self._suit = suit
        else:
            raise ValueError("Invalid suit")
    
    def __lt__(self, another):
        return self.rank_val < another.rank_val

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = self.new_deck()
        self.table = None

    def new_deck(self):
        card_list = []
        for rank in Card.rank_val:
            for suit in Card.suits:
                card_list.append(Card(rank,suit))
        return card_list
    
    def draw_card(self):
        return self.cards.pop(random.randint(0,len(self.cards)-1))

    def deal_player(self, player, qty: int):
        for i in range(qty):
            player.hole_cards.append(self.draw_card())
        
        player.update_hand()
    
    def deal_community(self, table, qty: int):
        for i in range(qty):
            table.community_cards.append(self.draw_card())
        self.update_all_hands()
    
    #nifty little function to update everyones hands, is called after a card is dealt to a player or the table
    def update_all_hands(self):
        for player in self.table.players:
            player.update_hand()


    def __str__(self):
        print_str = ""
        for card in self.cards:
            print_str += f"{card}\n"
        return print_str



class Hand:
    def __init__(self, community_cards: list, hole_cards: list):
        self.table_cards = sorted(community_cards + hole_cards)
        self.hand_value = {}
        self.best_hand = None
        self.kickers = None
        self.hand_strength = None

    name = ["Straight Flush", "Four of a Kind", "Full House" , "Flush", "Straight", "Three of a Kind", "Two Pair", "One Pair",  "High Card" ]
    
    def table_values(self):
        #Average of flush rank val is used
        #bestpair = sort_high_card(get_of_a_kind(self.table_cards)[2])
        #secondbestpair = sort_high_card(get_of_a_kind(self.table_cards).remove(bestpair)[2])
        
        straight_flushes = get_straight_flush(self.table_cards)
        straight_flush = [sorted(straight_flushes, key = lambda x : max(x))][-1] if straight_flushes[0] else [[]]
        self.hand_value["Straight Flush"] =  straight_flush

        fours, threes, pairs = get_of_a_kind(self.table_cards)
        self.hand_value["Four of a Kind"] = [fours[-1]] if len(fours) > 0 else [[]]
        self.hand_value["Three of a Kind"] = [threes[-1]] if len(threes) > 0 else [[]]
        self.hand_value["Two Pair"] = pairs[-2:] if len(pairs) > 1 else [[]]
        self.hand_value["One Pair"] = [pairs[-1]] if len(pairs) > 0 else [[]]
        self.hand_value["Full House"] = [pairs[-1], threes[-1]] if len(pairs)>0 and len(threes) > 0 else [[]]

        
        flushes = [flush[-5:] for flush in get_flush(self.table_cards)] if len(get_flush(self.table_cards)) > 0 else [[]]
        self.hand_value["Flush"] = [sorted(flushes, key = lambda x: max(x))][-1] if flushes[0] else [[]]

        straights = [straight[-5:] for straight in get_straight(self.table_cards)] if len(get_straight(self.table_cards)) > 0 else [[]]
        self.hand_value["Straight"] = [sorted(straights, key = lambda x: max(x))][-1] if straights[0] else [[]]
        
        self.hand_value["High Card"] = [self.table_cards[-1]]



    def get_best_hand(self):
        for type in self.name:
            if self.hand_value[type][-1]:
                if type == 'Two Pair' or type == 'Full House':
                    return type, self.hand_value[type][-2:]
                return type, self.hand_value[type][-1]
    
    def get_kickers(self):
        clean_hand = []
        bhand = self.best_hand[1]
        if isinstance(bhand, Card):
            clean_hand = [bhand]

        elif all(isinstance(thing,list) for thing in bhand):
            clean_hand = bhand[0] + bhand[1]
        else:
            clean_hand = [card for card in bhand]

        n_high = 5 - len(clean_hand)

        kickers = sorted([card for card in self.table_cards if card not in clean_hand])[-1:]
        
        return kickers


        


    def mean_val(self, myhand: list):
        if len(myhand) > 0 and myhand is not None:
            valsum = sum([item.rank_val for item in myhand])
            return valsum/len(myhand)
        else:
            return 0

    def __str__(self):
        bigstring = ""
        for htype in self.hand_value:
            bigstring += f"\n{htype}:\n" + "\n".join([str(card) for card in self.hand_value])
        return bigstring
    
#Initialises a player
class Player:
    def __init__(self, name: str, chips: float):
        self.name = name
        self.hole_cards = []
        self.chips = chips
        self.table = None
        self.hand = None

#after a card is dealt from the deck class, it updates all players hands at the table
    def update_hand(self):
        self.hand = Hand(self.table.community_cards, self.hole_cards)
        self.hand.table_values()
        self.hand.best_hand = self.hand.get_best_hand()
        self.hand.kickers = self.hand.get_kickers()
        
    def bet(self):
        hardcoded = True
        while True:
            if hardcoded == True:
                amount = 1
            else:
                amount = int(input(f"{self.name} raises by amount (0 to check):"))

            if self.chips < amount:
                print('Insufficient funds')
                continue
            else:
                self.chips -= amount
                self.table.pot += amount
                break
        

        
    def __str__(self):
        print_cards = ""
        for mycard in self.hole_cards:
            print_cards += f"{mycard}\n"
        return f"{self.name}:\n{print_cards}"

#initialises an empty playing table
class Table:
    def __init__(self):
        self.deck = None
        self.players = []
        self.community_cards = []
        self.pot = 0
    
    def add_deck(self, deck):
        self.deck = deck
        deck.table = self

    def add_player(self, player):
        self.players.append(player)
        player.table = self
    
    def __str__(self):
        print_str = ""
        for item in self.community_cards:
            print_str += f"{item}\n"
        return f"Table:\n${self.pot} in the Pot\n{print_str}"
    

def get_straight(table_cards: list):
        table_cards = sorted(table_cards)
        straight = [[table_cards[0]]]
        #Makes a list of lists of consecutive cards
        for i in range(1,len(table_cards)):
            #skip any double ups
            if table_cards[i].rank_val == straight[-1][-1].rank_val:
                continue

            if table_cards[i].rank_val == straight[-1][-1].rank_val + 1:
                straight[-1].append(table_cards[i])

        #Returns a list only if the sequence has 5 or more cards.
        return [sequence for sequence in straight if len(sequence) >= 5]



def get_of_a_kind(cards: list):
    card_freq = {}
    for card in cards:
        if card.rank in card_freq:
            card_freq[card.rank] += 1
        else:
            card_freq[card.rank] = 1
        pairs = []
        threes = []
        fours = []
    for key, value in card_freq.items():
        if value == 2:
            pairs.append([card for card in cards if card.rank == key])
        elif value == 3:
            threes.append([card for card in cards if card.rank == key])
        elif value == 4:
            fours.append([card for card in cards if card.rank == key])
        else:
            continue
    
    return fours, threes, pairs



#returns all the cards of the same suit. The highest straight is taken in the dictionary
def get_flush(table_cards: list):
    suit_dic = {}
    for card in table_cards:
        if card.suit not in suit_dic:
            suit_dic[card.suit] = 1
        else:
            suit_dic[card.suit] += 1

    flush = []
    for suit in Card.suits:
        if suit in suit_dic and suit_dic[suit] >= 5:
            flush.append([card for card in table_cards if card.suit == suit])      
        
    for sequence in flush:
        if len(sequence) < 5:
            flush.remove(sequence)

    if len(flush) == 0:
        return [[]]
    
    return flush

def get_straight_flush(table_cards: list):
    straight_flushes = []
    flushes = get_flush(table_cards)
    #return empty nested list if no flushes
    if flushes == [[]]:
        return flushes 
    
    for flush in flushes:
        temp_sflush = get_straight(flush)
        for sflush in temp_sflush:
            if len(sflush) > 4:
                straight_flushes.append(sflush)
                
    if len(straight_flushes) == 0:
        return [[]]
    
    return [st_flush[-5:] for st_flush in straight_flushes]


