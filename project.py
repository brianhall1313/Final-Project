import sys
import csv
import deck
import player
import re

COMPUTER_LIMIT = 16
SAVE_FILE_PATH = "profiles.csv"


def main():
    intro()
    while True:
        selection = menu()
        play_game(selection)


def intro():
    print("Let's Play Blackjack!")


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
            print("I'm sorry but your selection was invalid, please enter the number of your selection")


def play_game(num):
    match num:
        case 1:
            play_blackjack()
        case 2:
            display_profiles()
        case 3:
            print("Thank you for playing!")
            sys.exit(0)


def display_profiles():
    data = get_load_data()
    for name, balance in data.items():
        print(name, balance)


def get_bet(limit):
    while True:
        try:
            return get_menu_selection("How much would you like to bet?", limit)
        except ValueError:
            print("I'm sorry but your selection was invalid")


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
        print("""What do you want to do?
1: hit
2: stay""")
        try:
            return get_menu_selection()
        except ValueError:
            print("I'm sorry but your selection was invalid, please enter the number of your selection")


def play_blackjack():
    data = init_player()
    player_one = player.Player(data[0], data[1])
    while True:
        current_deck = deck.Deck()
        current_deck.shuffle()
        bet = get_bet(player_one.balance)
        player_one.bet(bet)
        player_hand = [current_deck.deal_card(), current_deck.deal_card()]
        dealer_hand = [current_deck.deal_card(), current_deck.deal_card()]
        print("dealer:")
        print_hand(dealer_hand, True)
        print("Player:")
        print_hand(player_hand)
        playing = True
        while playing:
            choice = get_hand_choice()
            if choice == 1:
                print("hit!")
                player_hand.append(current_deck.deal_card())
                if evaluate_hand(player_hand) > 21:
                    print("bust!")
                    playing = False
            elif choice == 2:
                print("stay")
                playing = False
            print_hand(player_hand)
        print("dealer's Turn!")
        ai_turn = True
        while ai_turn:
            p = evaluate_hand(player_hand)
            c = evaluate_hand(dealer_hand)
            if c < p <= 21 and c <= COMPUTER_LIMIT:
                print("dealer Hits")
                dealer_hand.append(current_deck.deal_card())
                if evaluate_hand(dealer_hand) > 21:
                    print("dealer busts")
                    ai_turn = False
            else:
                print("dealer stays")
                ai_turn = False
            print_hand(dealer_hand)
        print("dealer done")
        winner = compare_hands(player_hand, dealer_hand)
        if winner:
            player_one.payout(bet*2)
        else:
            if player_one.balance <= 0:
                print("You are out of money, Have 100 points")
                player_one.payout(100)
        again = play_again(player_one.balance)
        if again == 2:
            print("Saving Profile")
            save_game(player_one)
            return
        else:
            print("Then lets play another hand!")


def play_again(balance):
    while True:
        print(f"Current Balance: {balance}")
        print("""Would you like to play again?
            1: Yes
            2: No""")
        try:
            return get_menu_selection()
        except ValueError:
            print("I'm sorry but your selection was invalid")


def save_game(player_to_save):
    data = get_load_data()
    data[player_to_save.name] = player_to_save.balance
    save_data(data)


def save_data(data):

    with open(SAVE_FILE_PATH, "a") as file:
        writer = csv.writer(file)
        for key in data.keys():
            writer.writerow([key, data[key]])


def compare_hands(player_hand, dealer_hand):
    p = evaluate_hand(player_hand)
    c = evaluate_hand(dealer_hand)
    if p > 21:
        print("Player Busted! Dealer Wins!")
        return False
    elif c > 21:
        print("Dealer Busted! Player Wins!")
        return True
    elif p > c:
        print("player Wins!")
        return True
    elif p <= c:
        print("Dealer Wins!")
        return False
    else:
        print("Tie! Dealer Wins!")
        return False


def init_player():
    load_data = get_load_data()
    if load_data:
        selection = load_selection()
    else:
        print("no save data, creating new profile")
        selection = 2
    if selection == 1:
        return check_load()
    elif selection == 2:
        name = get_name("Please Enter a Name: ")
        return [name, 100]


def check_load():
    player_name = get_name("Please enter the name of the profile you would like to load")
    data = get_load_data()
    if player_name in data.keys():
        return [player_name, data[player_name]]
    else:
        print("no profile found creating new one")
        return [player_name, 100]


def get_name(message):
    while True:
        try:
            return name_entry(message)
        except ValueError:
            print("I'm sorry but your selection was invalid (1-15 chars alpha-numeric + ~!@#$%^&*'.,/_-")


def name_entry(message):
    name = input(message).strip()
    if re.search(r"^[\w ~!@#$%^&*'.,/_-]{1,15}$", name):
        return name
    else:
        raise ValueError


def load_selection():
    while True:
        print("""would you like to load a profile or start a new profile?
1:Load Profile
2:New""")
        try:
            return get_menu_selection()
        except ValueError:
            print("I'm sorry but your selection was invalid, please enter the number of your selection")


def get_load_data():
    load = {}
    try:
        with open(SAVE_FILE_PATH, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                load[f"{row[0]}"] = int(row[1])
    except FileNotFoundError:
        pass
    return load


if __name__ == "__main__":
    main()
