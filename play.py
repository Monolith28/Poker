from cards import Player, Hand, Deck, Table, print_cards, Card

def print_all_hands(table):
    players = table.players

    player_names = [player.name for player in players]
    best_hand_names = [player.hand.best_hand[0] for player in players]
    best_hand_cards = [player.hand.best_hand[1] for player in players]

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
    print(f"{best_hand_names[0]:<20}{best_hand_names[1]:<20}{best_hand_names[2]:<20}")
    for i in range(card_rows):
        print(f"{data[i][0]:<20}{data[i][1]:<20}{data[i][2]:<20}")
        


players = [Player("Imogen"), Player("Kuba"), Player("Peter")]
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
