from cards import Player, Hand, Deck, Table, print_cards

players = [Player("Player1"), Player("Player2"), Player("Player3")]
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


table.deck.deal_community(table,10)
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

for player in table.players:
    print(player.name)
    print_cards(player.hand.hand_value)

