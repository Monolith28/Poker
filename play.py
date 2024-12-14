from cards import Player, Hand, Deck, Table, print_cards, Card, get_hand_strength
import copy
import time

#TODO:, implement structured betting and folding
#one round of betting
def place_bets(table):
    loop_breaker = 0
    while True:
        once_around(table)
        loop_breaker += 1
        if check_calls(table):
            break
        if loop_breaker > 99:
            break
    

#check if anyone needs to call        
def check_calls(table):
    no_more_bets = True
    for player in table.players:
        if table.curr_bet - player.curr_pbet != 0 and player.folded == False:
            no_more_bets = False
    return no_more_bets


#go around the table once
def once_around(table):
    if len(table.players) == 1:
        return
    for player in table.players[:]:
        if player.folded == True:
            continue
        starting_pot = table.pot
        player_action = player.player_action()
        pot_change = table.pot - starting_pot
        print(f"{player.name}: {player_action[0]} ${player_action[1]}, ${pot_change} in - ${table.pot: .1f} in the pot")
        



def check_early_win(table):
    if len(table.players) == 1:
        table.round_winners = [table.players[-1]]
        reset_bets(table)
        return True
    else:
        reset_bets(table)
        return False
        
    


def get_winner(table: Table):
    get_hand_strength(table)
    players = table.players    
    winners = players[:]
    for i in range(4):
        highest = max([player.hand.hand_strength[i] for player in winners])
        temp_winners = []
        for player in winners:
            if player.hand.hand_strength[i] == highest:
                temp_winners.append(player)
        winners = temp_winners

    return [player for player in winners]


def print_active_players(table):
    active_players = ", ".join([player.name for player in table.players])
    print(f"{active_players} are in the round.")



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
    initialise_round(table)
    deal_players(table)
    check_early_win(table)
    if len(table.round_winners) > 0:
        pay_out(table.round_winners)
        return
    
    play_flop(table)
    check_early_win(table)
    if len(table.round_winners) > 0:
        pay_out(table.round_winners)
        return

    play_turn(table)
    check_early_win(table)
    if len(table.round_winners) > 0:
        pay_out(table.round_winners)
        return

    play_river(table)
    pay_out(table.round_winners)
    
    

def initialise_round(table):
    table.street = 0
    #re-add all folded players to the round
    table.players += table.folded_players
    #clear the list of folded players
    table.folded_players = []

    for player in table.players:
        print(f"{player.name}: ${player.chips}")

    
    #prompt = input("Deal player cards (Enter)")
def deal_players(table):
    for player in table.players:
        table.deck.deal_player(player,2)

    for player in table.players:
        print(player.name)
        print_cards(player.hole_cards)
    
    table.street = 1

    place_bets(table)

    #prompt = input("Deal Flop cards (Enter)")

def play_flop(table):
    
    table.deck.deal_community(table,3)
    print("Flop Cards:")
    print_active_players(table)
    print_cards(table.community_cards)

    table.street = 2

    place_bets(table)


    #prompt = input("Deal Turn Card (Enter)")
def play_turn(table):
    
    table.deck.deal_community(table,1)
    print("Turn:")
    print_active_players(table)
    print_cards(table.community_cards)

    table.street = 3

    place_bets(table)
    #prompt = input("Deal River Card (Enter)")

def play_river(table):
    
    table.deck.deal_community(table,1)
    print("River:")
    print_active_players(table)
    print_cards(table.community_cards)

    table.street = 4

    #print_all_hands(table)
    print()
    table.round_winners = get_winner(table)
    reset_table(table)
    
    
    

def pay_out(round_winners):
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

#reset bets after a round of betting
def reset_bets(table):
    table.curr_bet = 0
    for player in table.players:
        player.curr_pbet = 0
        player.curr_dbet = 0
    
    for player in table.folded_players:
        player.curr_pbet = 0
        player.curr_dbet = 0

def reset_table(table):
    #return cards to the deck
    table.deck.cards += table.community_cards
    table.community_cards = []
    
    for player in table.players:
        table.deck.cards += player.hole_cards
        player.hole_cards = []
        

players = [Player("Ellie", 100), Player("Jakub",100), Player("Drake",100), Player("Diddy", 100)]
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