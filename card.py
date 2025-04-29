class Card:
    def __init__(self, rank, suit=None, is_joker=False):
        self.rank = rank
        self.suit = suit
        self.is_joker = is_joker

    def value(self):
        if self.is_joker:
            # The joker is a wild card, so it can be used to replace anything, so it is zero points
            return 0
        if self.rank in ['J', 'Q', 'K']:
            # Jack, Queen, King are worth 10 points
            return 10
        if self.rank == 'A':
            return 1
        return int(self.rank)

    def __str__(self):
        return "Joker" if self.is_joker else f"{self.rank}{self.suit}"

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return self.value() < other.value()
