from deck import Deck
from player import Player
from score import update_scores
from game import get_computer_move, is_valid_set, is_valid_straight

def print_hand(player):
    print(f"\n{player.name}'s hand:")
    for i, card in enumerate(player.hand):
        print(f"  {i}: {card}")
    print(f"Total hand value: {player.hand_value()}")

def parse_indexes(index_str):
    try:
        return [int(i.strip()) for i in index_str.split()]
    except ValueError:
        return []

def is_valid_play(cards):
    return is_valid_set(cards) or is_valid_straight(cards)

def main():
    user_name = input("Enter your name: ").strip() or "You"
    user = Player(user_name)
    computer = Player("Computer")
    players = [user, computer]

    while all(p.score < 100 for p in players):
        deck = Deck(include_jokers=True)
        deck.shuffle()
        discard_pile = []

        for p in players:
            p.reset_hand()
            p.draw_card(deck.draw(5))

        discard_pile.extend(deck.draw(1))
        turn = 0
        prev_discard_group = []  # track last discarded cards from previous turn

        while True:
            current = players[turn % 2]
            opponent = players[(turn + 1) % 2]
            last_discard_group = prev_discard_group

            print(f"\n--- {current.name}'s Turn ---")
            print(f"Top of discard pile: {discard_pile[-1]}")
            
            if current == user:
                print_hand(user)

                if user.hand_value() <= 7:
                    choice = input("Call Yaniv? (y/n): ").strip().lower()
                    if choice == 'y':
                        print(f"\n{user.name} called Yaniv with value {user.hand_value()}!")
                        print(f"Computer's hand: {', '.join(str(c) for c in computer.hand)} ({computer.hand_value()})")
                        assaf = computer.hand_value() <= user.hand_value()
                        if assaf:
                            print("Assaf! You lose this round.")
                        else:
                            print("Yaniv successful!")
                        update_scores(players, 0, assaf)
                        break

                while True:
                    move_input = input("Enter card indexes to discard (space-separated), or press Enter to discard highest: ").strip()
                    if not move_input:
                        move = [max(user.hand, key=lambda c: c.value())]
                        break
                    indexes = parse_indexes(move_input)
                    if all(0 <= i < len(user.hand) for i in indexes):
                        move = [user.hand[i] for i in indexes]
                        if is_valid_play(move):
                            break
                        else:
                            print("Invalid set/straight. Try again.")
                    else:
                        print("Invalid indexes. Try again.")

                user.remove_cards(move)
                discard_pile.extend(move)
                prev_discard_group = move[:]

                # Drawing logic with safety check
                if len(last_discard_group) == 1:
                    draw_input = input("Draw from (d)eck or (p)ile? ").strip().lower()
                    if draw_input == 'p':
                        user.draw_card([discard_pile.pop()])
                    else:
                        user.draw_card(deck.draw())
                elif last_discard_group:
                    print(f"Top of discard: {last_discard_group[-1]}, Bottom: {last_discard_group[0]}")
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

            else:
                move = get_computer_move(computer.hand)
                computer.remove_cards(move)
                discard_pile.extend(move)
                prev_discard_group = move[:]

                if computer.hand_value() <= 7:
                    print(f"\nComputer called Yaniv with value {computer.hand_value()}!")
                    print_hand(user)
                    assaf = user.hand_value() <= computer.hand_value()
                    if assaf:
                        print("Assaf! You win this round.")
                    else:
                        print("Yaniv successful. You lose.")
                    update_scores(players, 1, assaf)
                    break

                top = last_discard_group[-1]
                bottom = last_discard_group[0]
                draw_options = [top, bottom, deck.cards[0]]
                best = min(draw_options, key=lambda c: c.value())
                if best in discard_pile:
                    discard_pile.remove(best)
                else:
                    deck.draw()
                computer.draw_card([best])

            turn += 1

        print("\n--- Scoreboard ---")
        for p in players:
            print(f"{p.name}: {p.score} pts | Win streak: {p.wins_in_a_row}")

    winner = min(players, key=lambda p: p.score)
    print(f"\n Game over! {winner.name} wins with {winner.score} points! ")

if __name__ == "__main__":
    main()
