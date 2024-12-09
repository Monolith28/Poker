from cards import Player, Hand, Deck, Table, print_cards, Card
import copy

#TODO: Put cards back in deck after round, implement betting, implement auto detection of winning hand
#implement kicker card and pot splitting.

def get_winner(table):
    players = self.players
    power_level = []

    for player in players[1:]:
        hname = Hand.name.index(player.best_hand[0])
        if hname == "High Card":
            


            
                
    
    


        
def higher_than(this_hand, another_hand):
    



    
    
    





    



def print_all_hands(table):
    players = table.players

    player_names = [player.name for player in players]
    best_hand_names = [player.hand.best_hand[0] for player in players]
    best_hand_cards = [copy.deepcopy(player.hand.best_hand[1]) for player in players]

    clean_hands = []
    #just make any full houses or 2pair into a list of cards
    for hand in best_hand_cards:
        if isinstance(hand, Card):
            clean_hands.append([hand])

        elif all(isinstance(item,list) for item in hand):
            clean_hands.append(hand[0] + hand[1])
        else:
            clean_hands.append(hand)
    
    row_count = max([len(hand) for hand in clean_hands])
    for hand in clean_hands:
        while len(hand) < row_count:
            hand.append(" ")
    
    #get strings for the kickers
    print('Checkpoint')
    kickers = [player.hand.kickers[::-1] for player in table.players]

    n_kick_rows = max([len(sequence) for sequence in kickers])

    #pad the shorter kicker hands out with whitespace
    for sequence in kickers:
        while len(sequence) < n_kick_rows:
            sequence.append(" ")
    


    kick_rows = []
    for i in range(n_kick_rows):
        new_row = [str(sequence[i]) for sequence in kickers]
        kick_rows.append(new_row)



    

    card_rows = max([len(hand) for hand in clean_hands])

    #pad the shorter hands out with whitespace
    for hand in clean_hands:
        while len(hand) < card_rows:
            hand.append(" ")

    data = []
    for i in range(card_rows):
        new_row = [str(hand[i]) for hand in clean_hands]
        data.append(new_row)

    print(f"{player_names[0]:<20}{player_names[1]:<20}{player_names[2]:<20}")
    print(f"{'-'*16:<20}{'-'*16:<20}{'-'*16:<20}")
    print(f"{best_hand_names[0]:<20}{best_hand_names[1]:<20}{best_hand_names[2]:<20}")
    print(f"{'-'*16:<20}{'-'*16:<20}{'-'*16:<20}")
    for i in range(card_rows):
        print(f"{data[i][0]:<20}{data[i][1]:<20}{data[i][2]:<20}")
    print(f"{'-'*16:<20}{'-'*16:<20}{'-'*16:<20}")

    for i in range(n_kick_rows):
        print(f"{kick_rows[i][0]:<20}{kick_rows[i][1]:<20}{kick_rows[i][2]:<20}")

        


players = [Player("Tom"), Player("Harry"), Player("John")]
deck = Deck()

table = Table()
table.add_deck(deck)


for player in players:
    table.add_player(player)

prompt = input("Deal player cards (Enter)")

for player in table.players:
    table.deck.deal_player(player,2)

for player in table.players:
    print(player.name)
    print_cards(player.hole_cards)

prompt = input("Deal Flop cards (Enter)")


table.deck.deal_community(table,3)
print("Flop Cards:")
print_cards(table.community_cards)

prompt = input("Deal Turn Card (Enter)")

table.deck.deal_community(table,1)
print("Turn:")
print_cards(table.community_cards)

prompt = input("Deal River Card (Enter)")
table.deck.deal_community(table,1)
print("River:")
print_cards(table.community_cards)

print_all_hands(table)
