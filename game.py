def is_valid_set(cards):
    #Checks if a group of cards forms a valid set (same rank, minimum 3 cards)
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
    if card.rank == 'A': return 1
    if card.rank == 'J': return 11
    if card.rank == 'Q': return 12
    if card.rank == 'K': return 13
    return int(card.rank)


def get_computer_move(hand):
   # Returns the best possible move for the computer; it falls back to discarding the lowest-value card if there is no possible combo.
    from itertools import combinations

    best_move = None
    best_value = float('inf')

    # Try all combinations of 1 to all cards in hand
    for n in range(1, len(hand)+1):
        for combo in combinations(hand, n):
            # If the combo is a valid set or straight, calculate remaining hand value
            if is_valid_set(combo) or is_valid_straight(combo):
                remaining = [card for card in hand if card not in combo]
                val = sum(c.value() for c in remaining)
                if val < best_value:
                    best_move = combo
                    best_value = val

    # Return best combo found, or the lowest-value card if nothing else is good
    return list(best_move) if best_move else [min(hand, key=lambda c: c.value())]
