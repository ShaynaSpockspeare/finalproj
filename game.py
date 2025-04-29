def is_valid_set(cards):
    # Checks if a group of cards forms a valid set (same rank, minimum 2 cards,jacks queens kings and 10s count separately despite having same value)
    if len(cards) < 2:
        return False
    non_jokers = [card for card in cards if not card.is_joker]
    if not non_jokers:
        return False
    base_rank = non_jokers[0].rank
    return all(c.rank == base_rank for c in non_jokers)


def is_valid_straight(cards):
    #Checks if a group of cards forms a valid straight (same suit, consecutive values).
    if len(cards) < 3:
        return False

    # Separate jokers and non-jokers
    non_jokers = [c for c in cards if not c.is_joker]
    jokers = [c for c in cards if c.is_joker]

    if not non_jokers:
        return False

    # All non-jokers must be of the same suit
    suit = non_jokers[0].suit
    if any(c.suit != suit for c in non_jokers):
        return False

    # Get sorted list of values
    values = sorted([card_value_for_straight(c) for c in non_jokers])
    needed_jokers = 0

    # Count how many jokers are needed to fill gaps
    for i in range(len(values) - 1):
        gap = values[i + 1] - values[i]
        if gap == 1:
            continue
        elif gap > 1:
            needed_jokers += gap - 1
        else:
            return False  # Duplicate values or invalid sequence

    return needed_jokers <= len(jokers)


def card_value_for_straight(card):
    # For straights since the values are the same but the order must be the same as in a standard deck
    if card.rank == 'A': return 1
    if card.rank == 'J': return 11
    if card.rank == 'Q': return 12
    if card.rank == 'K': return 13
    return int(card.rank)


from itertools import combinations

def get_computer_move(hand):
    # This function determines the best move for the computer (either dropping the highest value card or forming a set/straight)
    best_move = None
    best_score = float('inf')

    for n in range(1, len(hand)+1):
        for combo in combinations(hand, n):
            if is_valid_set(combo) or is_valid_straight(combo):
                remaining = [c for c in hand if c not in combo]
                remaining_value = sum(c.value() for c in remaining)
                cards_discarded = len(combo)
                jokers_used = sum(1 for c in combo if c.is_joker)

                score = (
                    remaining_value
                    - 3 * cards_discarded   
                    + 5 * jokers_used      
                )

                if score < best_score:
                    best_score = score
                    best_move = combo

    if best_move:
        return list(best_move)
    else:
        # If no valid set or straight is found, the computer should drop the highest value card. Lambda is used to get the value of the card
        return [max(hand, key=lambda c: c.value())]
