class Transfer:
    def __init__(self, season, player, age, pos, joined, left, mv, fee):
        self.season = season
        self.player = player
        self.player_age = age
        self.player_pos = pos
        self.club_joined = joined
        self.club_left = left
        self.mv = mv
        self.transfer_fee = fee

    def __str__(self):
        return (self.season + '#' + self.player + '#' + self.player_age + '#' + self.player_pos + '#' + self.club_joined
                + '#' + self.club_left + '#' + self.mv + '#' + self.transfer_fee)
