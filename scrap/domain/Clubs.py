import csv


class Club:
    def __init__(self, club_name, league, league_acro, country, season):
        self.club_name = club_name
        self.league = league
        self.league_acro = league_acro
        self.country = country
        self.season = season

    def __str__(self):
        return self.club_name + '#' + self.league + '#' + self.league_acro + '#' + self.country + '#' + self.season

    @classmethod
    def persist_club_data(cls, clubs, file):
        with open('../data/' + str(file), 'a') as csv_table:
            writer = csv.writer(csv_table)
            for club in clubs:
                formatted_club = club.__str__().split('#')
                writer.writerow(formatted_club)
