import random
import statistics

def print_cards(cardlist: list):
    for sublist in cardlist:
        if len(sublist) > 0: 
            for card in sublist:
                print(str(card))
        else:
            print("[]")

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
    
    def deal_community(self, table, qty: int):
        for i in range(qty):
            table.community_cards.append(self.draw_card())

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
        self.hand_value["Straight Flush"] =  None
        self.hand_value["Four of a Kind"] = self.four_of_a_kind(self.table_cards)
        self.hand_value["Flush"] = (self.flush(), self.mean_val(self.flush))
        self.hand_value["Straight"] = None
        self.hand_value["Three of a Kind"] = None
        self.hand_value["Two Pair"] = None
        self.hand_value["One Pair"] = None
        self.hand_value["High Card"] = None




    def mean_val(self, myhand: list):
        if len(myhand) > 0 and myhand is not None:
            valsum = sum([item.rank_val for item in myhand])
            return valsum/len(myhand)
        else:
            return 0

    def __str__(self):
        return "\n".join([str(card) for card in table_cards])

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hole_cards = []
        self.chips = 0
    
    def __str__(self):
        print_cards = ""
        for mycard in self.hole_cards:
            print_cards += f"{mycard}\n"
        return f"{self.name}:\n{print_cards}"

class Table:
    def __init__(self):
        self.community_cards = []
        self.pot = 0
    
    def __str__(self):
        print_str = ""
        for item in self.community_cards:
            print_str += f"{item}\n"
        return f"Table:\n${self.pot} in the Pot\n{print_str}"
    

def flush(self, table_cards_orig: list):
        table_cards = table_cards_orig[:] #take a slice of the original so we don't edit it
        conseq = [table_cards.pop(0)]
        #Makes a list of lists of consecutive cards
        for item in table_cards:
            if item.rank_val == conseq[-1].rank_val + 1:
                conseq.append(item)
                table_cards.remove(item)
            else:
                conseq.append(self.flush(table_cards))
        #Returns a list only if the sequence has 5 or more cards.
        return [sequence for sequence in conseq if len(sequence) >= 5]

def of_a_kind(cards: list):
    card_freq = {}
    for card in cards:
        if card.rank in card_freq:
            card_freq[card.rank] += 1
        else:
            card_freq[card.rank] = 1

    for rank in card_freq:
        pairs = [card for card in cards if card_freq[card.rank] == 2]
        threes = [card for card in cards if card_freq[card.rank] == 3]
        fours = [card for card in cards if card_freq[card.rank] == 4]
    
    return fours, threes, pairs

def four_of_a_kind(table_cards: list):
    freq_dic = self.of_a_kind()
    return [card for card in table_cards if card.rank == rank]

#returns all the cards of the same suit. The highest straight is taken in the dictionary
def straight(self, table_cards: list):
    suit_dic = {}
    for card in table_cards:
        if card.suit not in suit_dic:
            suit_dic[card.suit] = 1
        else:
            suit_dic[card.suit] += 1

    straight = []
    for suit in Card.suits:
        if suit in suit_dic and suit_dic[suit] >= 5:
            straight = [card for card in table_cards if card.suit == suit]      
        
    if len(straight) >= 5:
        return straight
    else:
        return None


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
"""
#test_cards = [Card(str(i),'Spades') for i in range(2,7)] +  [Card("7", 'Hearts')]

test_cards = [Card("2", "Spades") for i in range(2,4)] + [Card("10", "Spades") for i in range(2,5)] + [Card("3", "Spades") for i in range(2,6)]

print_cards(of_a_kind(test_cards))





#test for dubs
"""
myhand = Hand(cards, pcards)


flush = myhand.straight()[0]
straighthand = Hand(straight,[])
print(straighthand.flush())
"""