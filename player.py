class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0
        self.wins_in_a_row = 0  # Track win streaks

    def draw_card(self, cards):
        self.hand.extend(cards)

    def remove_cards(self, cards):
        for c in cards:
            self.hand.remove(c)

    def hand_value(self):
        return sum(card.value() for card in self.hand)

    def reset_hand(self):
        self.hand = []

    def __repr__(self):
        return f"{self.name}'s hand: {', '.join(map(str, self.hand))}"

