def update_scores(players, caller_index, assaf_happened):
    caller = players[caller_index]
    opponent = players[1 - caller_index]

    caller_value = caller.hand_value()
    opponent_value = opponent.hand_value()

    if assaf_happened:
        # Assaf penalty: the caller gets 20 points pls whatever is in hand, and opponent gets a win streak
        caller.score += 20
        caller.wins_in_a_row = 0
        opponent.wins_in_a_row += 1
    else:
        # No Assaf: Add hand value to opponent's score and increment caller's win streak
        opponent.score += opponent_value
        caller.wins_in_a_row += 1
        opponent.wins_in_a_row = 0

    # If a player loses, reset their win streak
    if caller_value > opponent_value:
        opponent.wins_in_a_row = 0  # Reset opponent's win streak

    if opponent_value > caller_value:
        caller.wins_in_a_row = 0  # Reset caller's win streak

    # Adjust for exact 50 rule
    for player in players:
        if player.score == 50:
            player.score = 0

    # Adjust for exact 100 rule
    for player in players:
        if player.score == 100:
            player.score = 51

    # 3 wins in a row subtracts 15 points from total score
    for player in players:
        if player.wins_in_a_row == 3:
            player.score = max(0, player.score - 15)
            player.wins_in_a_row = 0
