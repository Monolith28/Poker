from cards import Player, Hand, Deck, Table, print_cards, Card
import copy
import time

#TODO:, implement structured betting and folding

def place_bets(table):
    for player in table.players:
        player.bet()
    print(f"${table.pot: .1f} in the pot")

def get_winner(table: Table):
    players = table.players
    power_level = []

    for player in players:
        best_hand = player.hand.best_hand
        hname = best_hand[0]
        htype = Hand.name.index(best_hand[0])
        if hname == "High Card":
            hrank = [best_hand[1].rank_val, 0]
        elif hname == "Two Pair" or hname == "Full House":
            hrank = [best_hand[1][1][-1].rank_val, best_hand[1][0][-1].rank_val ]
        else:
            hrank = [best_hand[1][-1].rank_val , 0]

        kickval = player.hand.kickers[-1].rank_val

        player.hand.hand_strength = (len(Hand.name) - htype, hrank[0], hrank[1], kickval)

    winners = players[:]
    for i in range(4):
        highest = max([player.hand.hand_strength[i] for player in winners])
        temp_winners = []
        for player in winners:
            if player.hand.hand_strength[i] == highest:
                temp_winners.append(player)
        winners = temp_winners

    return [player for player in winners]





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

    #reverse direction to print highest first     

    rev_clean_hands = []
    for hand in clean_hands:
        rev_clean_hands.append(hand[::-1])

    row_count = max([len(hand) for hand in rev_clean_hands])

    for hand in rev_clean_hands:
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

    data = []
    for i in range(card_rows):
        new_row = [str(hand[i]) for hand in rev_clean_hands]
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

        

def play_round(table: Table):
    for player in table.players:
        print(f"{player.name}: ${player.chips}")

    #prompt = input("Deal player cards (Enter)")

    for player in table.players:
        table.deck.deal_player(player,2)

    for player in table.players:
        print(player.name)
        print_cards(player.hole_cards)

    place_bets(table)
    #prompt = input("Deal Flop cards (Enter)")


    table.deck.deal_community(table,3)
    print("Flop Cards:")
    print_cards(table.community_cards)
    place_bets(table)

    #prompt = input("Deal Turn Card (Enter)")

    table.deck.deal_community(table,1)
    print("Turn:")
    print_cards(table.community_cards)

    place_bets(table)
    #prompt = input("Deal River Card (Enter)")
    table.deck.deal_community(table,1)
    print("River:")
    print_cards(table.community_cards)

    print_all_hands(table)
    print()
    round_winners = get_winner(table)

    reward = table.pot/len(round_winners)
    table.pot = 0

    if len(round_winners) > 1:
        winners = ", ".join([player.name for player in round_winners])
        print(f"{winners} split the pot for ${reward} each.")
        for player in round_winners:
            player.chips += reward

    else:
        print(f"{round_winners[0].name} wins ${reward}")
        round_winners[0].chips += reward
    
    #return cards to the deck
    table.deck.cards += table.community_cards
    table.community_cards = []
    for player in table.players:
        table.deck.cards += player.hole_cards
        player.hole_cards = []

players = [Player("Ellie", 100), Player("Jakub",100), Player("Drake2",100)]
deck = Deck()
table = Table()

table.add_deck(deck)

for player in players:
    table.add_player(player)
n_rounds = int(input("How many rounds?"))

start_time = time.time()
for i in range(n_rounds):
    play_round(table)

end_time = time.time()
for player in table.players:
    print(f"{player.name}: ${player.chips}")

print(f"{end_time - start_time} seconds per {n_rounds} rounds")