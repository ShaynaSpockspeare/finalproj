# ascii_card.py

def ascii_version_of_card(*cards, return_string=True):
    suits_name = ['S', 'D', 'H', 'C', 'X']
    suits_symbols = ['♠', '♦', '♥', '♣', 'X']  # 'X' used for Joker

    lines = [[] for _ in range(9)]

    for card in cards:
        rank = card.rank
        suit_letter = card.suit.upper() if card.suit else 'X'

        if rank is None:
            r = 'J'          # show Joker rank as 'J'
            suit = 'X'       # plain, fixed-width Joker symbol
            space = ' '
        else:
            if rank == '10':
                r = '10'
                space = ''
            else:
                r = rank[0]
                space = ' '
            suit = suits_symbols[suits_name.index(suit_letter)]

        lines[0].append('┌─────────┐')
        lines[1].append(f'│{r}{space}       │')
        lines[2].append('│         │')
        lines[3].append('│         │')
        lines[4].append(f'│    {suit}    │')
        lines[5].append('│         │')
        lines[6].append('│         │')
        lines[7].append(f'│       {space}{r}│')
        lines[8].append('└─────────┘')

    result = [''.join(line) for line in lines]
    return '\n'.join(result) if return_string else result
