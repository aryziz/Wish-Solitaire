from time import sleep
from os import getcwd, system
from os.path import isfile
from string import ascii_uppercase
from random import shuffle
import pickle
import webbrowser

# Python ver 3.9


pile_of_cards = []


SPADES = "\u2660"
DIAMONDS = "\u2666"
CLUBS = "\u2663"
HEARTS = "\u2665"

letters = ascii_uppercase[0:9]

suits = [SPADES, DIAMONDS, CLUBS, HEARTS]


def make_pile():
    converter = {7: "A", 11: "J", 12: "Q", 13: "K"}
    for i in range(7, 14):
        if i in converter.keys():
            for suit in suits:
                pile_of_cards.append(f"{suit}{converter[i]}")
        else:
            for suit in suits:
                pile_of_cards.append(f"{suit}{i}")


def hand_out(distribute):

    shuffle(distribute)
    distribute = [distribute[card : card + 4] for card in range(0, len(distribute), 4)]
    return distribute


def remove_pair(card_1, card_2, card):

    global letters

    converter = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
    try:
        if (
            card_1 != card_2
            and card_1 in letters
            and card_2 in letters
            and deck[converter[card_1]][0][1] == deck[converter[card_2]][0][1]
        ):
            deck[converter[card_2]].pop(0)
            deck[converter[card_1]].pop(0)
        else:
            print("Not valid. Try again.")
            sleep(2)
    except IndexError:
        print("You have chosen an empty deck, please try again.")
        start(card)


def loss(card):
    checker = []

    for i in card:
        try:
            checker.append(i[0][1])
        except IndexError:
            continue

    rem_dup = set(checker)
    if len(checker) == len(rem_dup):
        return True


def win(card):
    player_won = True
    for i in card:
        if i:
            player_won = False
            break
        else:
            continue
    return player_won


def save(card):
    user_input = input("Are you sure you want to save? (y/n): ").lower()
    if user_input == "y":
        file_name = "wish-solitaire"
        pickle.dump(card, open(file_name + ".p", "wb"))
        print("Executed. The files name: wish-solitaire.p")
        sleep(2)
    elif user_input == "n":
        print("OK. The file will not be saved.")
        start(card)
    else:
        print("Oops! Something went wrong, try again.")
        sleep(2)

    main()


def start(card):
    while True:
        if win(card):
            print("Congrats, you won!")
            input("<Enter> main menu")
            break
        elif loss(card):
            game_layout(card)
            print("\nYou lost.")
            input("<Enter> main menu")
            break
        else:
            try:
                game_layout(card)
            except Exception:
                print("Oops! Something went wrong, try again.")
                break
            print("\n<S> to save the game")
            print("<Q> to enter the main menu")
            user = input("> ").upper().replace(" ", "")
            if user == "S":
                save(card)
            elif user == "Q":
                main()
            else:
                if len(user) == 2:
                    card_1 = user[0]
                    card_2 = user[1]
                    remove_pair(card_1, card_2, card)
                else:
                    start(card)


def game_layout(card):
    system("cls")
    for index, item in enumerate(card):
        if len(item) > 0:
            print("{:>2}".format(letters[index]), end="\t")
        else:
            print(f"{letters[index]}", end="\t")

    print("\n")
    for item in card:
        if len(item) > 0:
            print("{:>2}".format(f"{item[0]}"), end="\t")
        else:
            print(" ", end="\t")

    print("\n")
    for item in card:
        if len(item) > 0:
            print("{:>2}".format(f"{len(item[0:])}"), end="\t")
        else:
            print("X", end="\t")


def load():
    global deck
    if isfile("wish-solitaire.p"):
        deck = pickle.load(open("wish-solitaire.p", "rb"))
        start(deck)
    else:
        print("No saved file here: ", "\n", getcwd())
        sleep(2)


def game_rules():
    system("cls")
    while True:
        print(
            f"""
                {'-'*50}
                Wish Solitaire
                {'-'*50}
                
                ** Layout **
                Six piles of cards next to each other categorized by letters
                
                ** How to Play **
                Select the stacks that has the same card value
                To select piles, select two piles by entering the letter which belongs to the pile
                ** Goal **
                Discard all 32 cards
            """
        )
        user_input = input("Press Q to exit\n> ").strip()
        if user_input.upper() == "Q":
            break


def main():

    global deck

    menu = """
    ---------------
    1 - New Game
    2 - Load
    3 - Game rules
    9 - Exit
    ---------------
    """

    print(menu)
    user_input = input("> ")
    if user_input == "1":
        deck = hand_out(pile_of_cards)
        start(deck)
    elif user_input == "2":
        load()
    elif user_input == "3":
        game_rules()
    elif user_input == "9":
        for i in range(0, 4):
            b = "Terminating" + "." * i
            print(b, end="\r")
            sleep(1)

        exit()
    else:
        print("Invalid action. Try again")

    main()


if __name__ == "__main__":
    make_pile()
    main()
