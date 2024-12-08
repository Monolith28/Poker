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
        self.update_all_hands()
    
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
    
    def table_values(self):
        #Average of flush rank val is used
        #bestpair = sort_high_card(get_of_a_kind(self.table_cards)[2])
        #secondbestpair = sort_high_card(get_of_a_kind(self.table_cards).remove(bestpair)[2])
        fours, threes, pairs = get_of_a_kind(self.table_cards)
        self.hand_value["Straight Flush"] =  get_straight_flush(self.table_cards)
        self.hand_value["Four of a Kind"] = fours[-1] if len(fours) > 0 else [[]]
        self.hand_value["Flush"] = get_flush(self.table_cards)
        self.hand_value["Straight"] = get_straight(self.table_cards)
        self.hand_value["Three of a Kind"] = threes[-1] if len(threes) > 0 else [[]]
        self.hand_value["Two Pair"] = pairs[-2:] if len(pairs) > 1 else [[]]
        self.hand_value["One Pair"] = [pairs[-1]] if len(pairs) > 0 else [[]]
        self.hand_value["High Card"] = [self.table_cards[-1]]

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
    def __init__(self, name: str):
        self.name = name
        self.hole_cards = []
        self.chips = 0
        self.table = None
        self.hand = None

#after a card is dealt from the deck class, it updates all players hands at the table
    def update_hand(self):
        self.hand = Hand(self.table.community_cards, self.hole_cards)
        self.hand.table_values
    
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


#needs to be fixed (TODO)
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

    return flush

def get_straight_flush(table_cards: list):
    straight_flushes = []
    flushes = get_flush(table_cards)
    for flush in flushes:
        temp_sflush = get_straight(flush)
        for sflush in temp_sflush:
            if len(sflush) > 4:
                straight_flushes.append(sflush)
    return straight_flushes


def get_highest(hand_list: list, card_num: int):

    #finds the best hand from a list of all hands fo the same type
    #if hand_list length is 1, just return the only hand
    if len(hand_list) == 0:
        return None
    if len(hand_list) == 1:
        return hand_list[0]
    #slice it so we dont edit the original
    best_hands = [sorted(hand)[-card_num:] for hand in hand_list]
    for i in range(card_num-1,-1,-1):
        pos_max = max([hand[i].rank_val for hand in best_hands])
        for hand in best_hands:
            if hand[i].rank_val < pos_max:
                best_hands.remove(hand)
    return best_hands
        


    
thathand = Hand([],[])
print(thathand)

    
        
        

        

"""
class Play:
    def __init_(self):
        pass
    
    def deal(self, player: int):


#test for flush
comcards = [Card("2","Spades"), Card("3","Spades"), Card("4","Spades"), Card("5","Spades"), Card("6","Spades")]
pcards = [Card("7","Spades"),Card("9","Spades")]

best_hand = Hand(comcards, pcards)
print_cards(best_hand.flush())

test_cards = [[Card(str(i),'Spades') for i in range(2,7)], [Card(str(i),'Hearts') for i in range(3,8)]]
#test_cards = [[Card('2','Spades'), Card('6','Spades')], [Card('7', 'Spades'), Card('2', 'Spades'), Card('6','Spades')]]
mydeck = Deck()
kuba = Player('Kuba')
mytable = Table()

mydeck.deal_community(mytable, 10)
mydeck.deal_player(kuba, 10)

#myhand = Hand(test_cards, [])
myhand = Hand(mytable.community_cards, kuba.hole_cards)
myhand.table_values()


for hand_type in myhand.hand_value:
    print(f"{hand_type}:")
    print('-')
    print_cards(myhand.hand_value[hand_type])
    print('-')

#print_cards(test_cards)
print_cards(get_highest(test_cards,1))

#test_cards = [Card(str(i), "Spades") for i in range(7,2,-1)] + [Card(str(i), "Hearts") for i in range(3,11)] + [Card("3", "Spades") for i in range(2,6)]

myflush = get_straight_flush(kuba.hole_cards + mytable.community_cards)
print_cards(myflush)
#print_cards(sort_high_card(myflush))
#print('hmm')







#test for dubs

myhand = Hand(cards, pcards)


flush = myhand.straight()[0]
straighthand = Hand(straight,[])
print(straighthand.flush())
"""