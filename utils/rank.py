RANKS = {
    "bronze": 0,
    "silver": 1200,
    "gold": 2800,
    "platinium": 4800,
    "diamond": 7200,
    "master": 10000
}


def get_rank(player_elo: int):
    current_rank = None
    next_rank = None

    for rank_name, rank_elo in RANKS.items():
        if player_elo > rank_elo:
            if next_rank is not None:
                continue
            else:
                current_rank = rank_name
        else:
            next_rank = rank_name
    if current_rank is None:
        return "No rank", 0
    elif next_rank is None:
        return current_rank, 0
    else:
        division_elo_step = (RANKS[next_rank] - RANKS[current_rank]) / 4
        player_rank_progression = player_elo - RANKS[current_rank]

        return current_rank, 4 - int(player_rank_progression/division_elo_step)
