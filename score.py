def update_scores(players, caller_index, assaf_happened):
    caller = players[caller_index]
    opponent = players[1 - caller_index]

    caller_value = caller.hand_value()
    opponent_value = opponent.hand_value()

    if assaf_happened:
        # Assaf penalty: Caller gets 20 + their hand value, opponent gains win streak
        caller.score += 20 + caller_value
        caller.wins_in_a_row = 0
        opponent.wins_in_a_row += 1
    else:
        # Yaniv success: Opponent gains points, caller gains win streak
        opponent.score += opponent_value
        caller.wins_in_a_row += 1

    # Exact 50 rule: score resets to 0
    for player in players:
        if player.score == 50:
            player.score = 0

    # Exact 100 rule: score becomes 51
    for player in players:
        if player.score == 100:
            player.score = 51

    # 3 wins in a row: subtract 5 points, then reset streak
    for player in players:
        if player.wins_in_a_row == 3:
            player.score = max(0, player.score - 5)
            player.wins_in_a_row = 0



