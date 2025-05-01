from deck import Deck
from player import Player
from score import update_scores
from game import get_computer_move, is_valid_set, is_valid_straight
from ascii_card import ascii_version_of_card
import time

# This function prints the player's hand and its total value
def print_hand(player): 
    print(f"\n{player.name}'s hand:")
    ascii_lines = ascii_version_of_card(*player.hand, return_string=False)
    labels = [f"    [{i}]    " for i in range(len(player.hand))]  # Indexes from 0 like the good old days
    print(''.join(labels))
    print('\n'.join(ascii_lines))
    print(f"Total hand value: {player.hand_value()}")

# This turns the input string into a list of integers 
def parse_indexes(index_str):
    try:
        return [int(i.strip()) for i in index_str.split()]
    except ValueError:
        return []

# Just an edge case if the user messes up or tries to cheat
def is_valid_play(cards):
    return is_valid_set(cards) or is_valid_straight(cards)

def main():
    # Give the player a name and stuff so it can be cutesy
    user_name = input("Enter your name: ").strip() or "You"
    user = Player(user_name)
    computer = Player("Computer")
    players = [user, computer]

    # The main while loop for the game, it keeps going until one player surpasses 100
    while all(p.score < 100 for p in players):
        deck = Deck(include_jokers=True)
        deck.shuffle()
        discard_pile = []

        for p in players:
            p.reset_hand()
            p.draw_card(deck.draw(5))

        # Draw a card from the deck to start the discard pile, I wanted to have the option to take from discard immediately but couldn't figure it out so this was easier
        discard_pile.extend(deck.draw(1))
        turn = 0
        prev_discard_group = []

        while True:
            # Keep track of whose turn it is
            current = players[turn % 2]
            opponent = players[(turn + 1) % 2]
            last_discard_group = prev_discard_group[:]

            print(f"\n--- {current.name}'s Turn ---")
            print("Top of discard pile:")
            print(ascii_version_of_card(discard_pile[-1]))

            if current == user:
                print_hand(user)  # show your majestic hand with numbered choices

                user_value = user.hand_value()
                # Yaniv and Assaf call logic!
                if user_value <= 7:
                    call = input("Call Yaniv? (y/n): ").strip().lower()
                    if call == 'y':
                        print(f"\n{user.name} called Yaniv with {user_value}!")
                        print("Computer's hand:")
                        print(ascii_version_of_card(*computer.hand))
                        print(f"Value: {computer.hand_value()}")
                        assaf = computer.hand_value() <= user_value
                        if assaf:
                            print("\n!!! ASSAF! You lose this round. !!!")
                        else:
                            print("\n>>> YANIV SUCCESSFUL! You win the round! <<<")
                        update_scores(players, 0, assaf)
                        time.sleep(2)
                        break

                while True:
                    # Ask user which cards they want to throw away (gently)
                    move_input = input("Enter card index(es) to discard (space-separated): ").strip()
                    indexes = parse_indexes(move_input)
                    if all(0 <= i < len(user.hand) for i in indexes):
                        move = [user.hand[i] for i in indexes]
                        if is_valid_play(move):
                            break
                        elif len(indexes) == 1:
                            # Allow single-card discard even if not part of a set/straight
                            break
                        else:
                            print("Invalid set/straight. Try again.")
                    else:
                        print("Invalid indexes. Try again.")

                # Remove the selected cards from the user's hand
                pending_discard = move[:]
                user.remove_cards(pending_discard)

                # Drawing logic happens before modifying discard pile so that user takes opponent's last card not their own
                if len(last_discard_group) == 1:
                    draw_input = input("Draw from (d)eck or (p)ile? ").strip().lower()
                    if draw_input == 'p':
                        user.draw_card([last_discard_group[-1]])
                        discard_pile.remove(last_discard_group[-1])
                    else:
                        user.draw_card(deck.draw())
                elif last_discard_group:
                    print("Top and Bottom of Discard:")
                    print("[Top]          [Bottom]")
                    print(ascii_version_of_card(last_discard_group[-1], last_discard_group[0]))
                    draw_input = input("Draw from (d)eck, (t)op, or (b)ottom? ").strip().lower()
                    if draw_input == 't':
                        card = last_discard_group[-1]
                        discard_pile.remove(card)
                        user.draw_card([card])
                    elif draw_input == 'b':
                        card = last_discard_group[0]
                        discard_pile.remove(card)
                        user.draw_card([card])
                    else:
                        user.draw_card(deck.draw())
                else:
                    user.draw_card(deck.draw())

                discard_pile.extend(pending_discard)
                prev_discard_group = pending_discard[:]

            else:
                move = get_computer_move(computer.hand)
                pending_discard = move[:]
                computer.remove_cards(pending_discard)

                # Computer draws from the best available option (it’s clever like that)
                top = last_discard_group[-1] if last_discard_group else None
                bottom = last_discard_group[0] if last_discard_group else None
                deck_card = deck.draw()[0] if len(deck) > 0 else None
                options = [c for c in [top, bottom, deck_card] if c]
                best = min(options, key=lambda c: c.value())
                if best in discard_pile:
                    discard_pile.remove(best)
                computer.draw_card([best])

                discard_pile.extend(pending_discard)
                prev_discard_group = pending_discard[:]

                computer_value = computer.hand_value()
                if computer_value <= 7:
                    print(f"\nComputer called Yaniv with {computer_value}!")
                    print_hand(user)
                    assaf = user.hand_value() <= computer_value
                    if assaf:
                        print("\n!!! ASSAF! You win this round. !!!")
                    else:
                        print("\n>>> YANIV SUCCESSFUL. You lose this round. <<<")
                    update_scores(players, 1, assaf)
                    time.sleep(2)
                    break

            turn += 1

        print("\n--- Scoreboard ---")
        for p in players:
            print(f"{p.name}: {p.score} pts | Win streak: {p.wins_in_a_row}")

    winner = min(players, key=lambda p: p.score)
    print(f"\n Game over! {winner.name} wins with {winner.score} points!")

if __name__ == "__main__":
    main()