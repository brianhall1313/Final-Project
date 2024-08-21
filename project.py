import sys
import csv
import deck
import player
import re
import time

COMPUTER_LIMIT = 16
SAVE_FILE_PATH = "profiles.csv"
debug = True


def main():
    send_message("Let's Play Blackjack!")
    while True:
        selection = menu()
        play_game(selection)


def send_message(message):
    if not debug:
        print(message)


def get_menu_selection(message="Please input your selection: ", menu_limit=2):
    num = int(input(message))
    if 0 < num <= menu_limit:
        return num
    else:
        raise ValueError


def menu():
    while True:
        print("""What do you want to do?
            1: Play Blackjack
            2: View Profiles
            3: quit""")
        try:
            return get_menu_selection(menu_limit=3)
        except ValueError:
            send_message("I'm sorry but your selection was invalid, please enter the number of your selection")


def play_game(num):
    match num:
        case 1:
            play_blackjack()
        case 2:
            display_profiles()
        case 3:
            send_message("Thank you for playing!")
            sys.exit(0)


def display_profiles():
    data = get_load_data()
    if len(data) > 0:
        for name, balance in data.items():
            print(name, balance)
    else:
        send_message("No Saved Profiles")


def get_bet(limit):
    send_message(f"Current Balance: {limit}")
    while True:
        try:
            return get_menu_selection("How much would you like to bet?", limit)
        except ValueError:
            send_message("I'm sorry but your selection was invalid")


def print_hand(hand, dealer=False):
    total = evaluate_hand(hand, dealer)
    first = True
    for card in hand:
        if dealer and first:
            print("|", "X", "|", end=' ')
            first = False
        else:
            print("|", card, "|", end=' ')
    print("")
    print("Card Total:", total)


def evaluate_hand(hand, dealer=False):
    total = 0
    ace_total = 0
    first = True
    for card in hand:
        if first and dealer:
            first = False
        else:
            total += card.value
            if card.value == 1:
                ace_total += 11
            else:
                ace_total += card.value
    if total < ace_total <= 21:
        return ace_total
    else:
        return total


def get_hand_choice():
    while True:
        send_message("""What do you want to do?
1: hit
2: stay""")
        try:
            return get_menu_selection()
        except ValueError:
            send_message("I'm sorry but your selection was invalid, please enter the number of your selection")


def player_turn(player_one, dealer, current_deck):
    send_message("Player's Turn")
    while True:
        choice = get_hand_choice()
        if choice == 1:
            send_message("hit!")
            player_one.dealt(current_deck.deal_card())
            if evaluate_hand(player_one.hand) > 21:
                send_message("bust!")
                return
        elif choice == 2:
            send_message("stay")
            return
        print_hands(player_one, dealer)


def ai_turn(player_one, dealer, current_deck):
    send_message("Dealer's Turn!")
    while True:
        p = evaluate_hand(player_one.hand)
        c = evaluate_hand(dealer.hand)
        if c < p <= 21 and c <= COMPUTER_LIMIT:
            send_message("Dealer Hits")
            dealer.dealt(current_deck.deal_card())
            if evaluate_hand(dealer.hand) > 21:
                send_message("Dealer busts")
                return
        else:
            send_message("Dealer stays")
            return

        print_hands(player_one, dealer)
        time.sleep(1)


def print_hands(player_one, dealer, final = False):
    send_message("Dealer:")
    print_hand(dealer.hand, not final)
    send_message("Player:")
    print_hand(player_one.hand)


def play_blackjack():
    data = init_player()
    player_one = player.Player(data[0], data[1])
    dealer = player.Player("Dealer", 0)
    while True:
        current_deck = deck.Deck()
        current_deck.shuffle()
        bet = get_bet(player_one.balance)
        player_one.bet(bet)
        player_one.dealt(current_deck.deal_card())
        player_one.dealt(current_deck.deal_card())
        dealer.dealt(current_deck.deal_card())
        dealer.dealt(current_deck.deal_card())
        print_hands(player_one, dealer)
        player_turn(player_one, dealer, current_deck)
        time.sleep(1)
        ai_turn(player_one, dealer , current_deck)
        print_hands(player_one, dealer, True)
        winner = compare_hands(player_one.hand, dealer.hand)
        if winner:
            player_one.payout(bet*2)
        else:
            if player_one.balance <= 0:
                send_message("You are out of money, Have 100 points")
                player_one.payout(100)
        player_one.clear_hand()
        dealer.clear_hand()
        again = play_again(player_one.balance)
        if again == 2:
            send_message("Saving Profile")
            save_game(player_one)
            return
        else:
            send_message("Then lets play another hand!")


def play_again(balance):
    while True:
        send_message(f"Current Balance: {balance}")
        send_message("""Would you like to play again?
            1: Yes
            2: No""")
        try:
            return get_menu_selection()
        except ValueError:
            send_message("I'm sorry but your selection was invalid")


def save_game(player_to_save):
    data = get_load_data()
    data[player_to_save.name] = player_to_save.balance
    save_data(data)


def save_data(data,path=SAVE_FILE_PATH):

    with open(path, "w") as file:
        writer = csv.writer(file)
        for key in data.keys():
            writer.writerow([key, data[key]])


def compare_hands(player_hand, dealer_hand):
    p = evaluate_hand(player_hand)
    c = evaluate_hand(dealer_hand)
    if p > 21:
        send_message("Player Busted! Dealer Wins!")
        return False
    elif c > 21:
        send_message("Dealer Busted! Player Wins!")
        return True
    elif p > c:
        send_message("Player Wins!")
        return True
    elif p <= c:
        send_message("Dealer Wins!")
        return False
    else:
        send_message("Tie! Dealer Wins!")
        return False


def init_player():
    load_data = get_load_data()
    if load_data:
        selection = load_selection()
    else:
        send_message("no save data, creating new profile")
        selection = 2
    if selection == 1:
        return check_load()
    elif selection == 2:
        name = get_name("Please Enter a Name: ")
        return [name, 100]


def print_load_names(data):
    if data == {}:
        print("No Saved Profiles")
    else:
        print("Profiles: ")
        for key in data.keys():
            print(key)



def check_load():
    data = get_load_data()
    print_load_names(data)
    player_name = get_name("Please enter the name of the profile you would like to load")
    if player_name in data.keys():
        return [player_name, data[player_name]]
    else:
        send_message("no profile found creating new one")
        return [player_name, 100]


def get_name(message):
    while True:
        try:
            return name_entry(message)
        except ValueError:
            send_message("I'm sorry but your selection was invalid (1-15 chars alpha-numeric + ~!@#$%^&*'.,()/_-)")


def name_entry(message):
    name = input(message).strip()
    if re.search(r"^[\w ~!@#$%^&*'.,()/_-]{1,15}$", name):
        return name
    else:
        raise ValueError


def load_selection():
    while True:
        send_message("""would you like to load a profile or start a new profile?
1:Load Profile
2:New""")
        try:
            return get_menu_selection()
        except ValueError:
            send_message("I'm sorry but your selection was invalid, please enter the number of your selection")


def get_load_data(path=SAVE_FILE_PATH):
    load = {}
    try:
        with open(path, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 1:
                    load[f"{row[0]}"] = int(row[1])
    except FileNotFoundError:
        pass
    return load


if __name__ == "__main__":
    debug = False
    main()
