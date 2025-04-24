import random
from card import Card

class Deck:
    SUITS = ['H', 'D', 'C', 'S']
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, include_jokers: bool = False):
        self.include_jokers = include_jokers
        self._build()

    def _build(self):
        self.cards = [Card(rank, suit) for suit in self.SUITS for rank in self.RANKS]
        if self.include_jokers:
            self.cards += [Card(None, None, is_joker=True) for _ in range(2)]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, n: int = 1):
        if n > len(self.cards):
            raise ValueError("Not enough cards to draw")
        drawn, self.cards = self.cards[:n], self.cards[n:]
        return drawn

    def reset(self):
        self._build()

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return f"<Deck of {len(self.cards)} cards>"
