class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0
        self.wins_in_a_row = 0 

    def draw_card(self, cards):
        # This function adds cards to the player's hand after drawing
        self.hand.extend(cards)

    def remove_cards(self, cards):
        # This function removes cards from the player's hand when placed
        for c in cards:
            self.hand.remove(c)

    def hand_value(self):
        # This function calculates the total value of the player's hand
        return sum(card.value() for card in self.hand)

    def reset_hand(self):
        # The hand has to reset between rounds
        self.hand = []

    def __repr__(self):
        # This function returns a string representation of the player's hand just for simplicity, may remove later
        return f"{self.name}'s hand: {', '.join(map(str, self.hand))}"

