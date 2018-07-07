class season:
    def __init__(self):
        self.teams = {}

    def add_game(self, name, distance, rest):
        rec = game_record(name, distance, rest)
        if(not (name in self.teams.keys())):
            self.teams[name] = team()
        self.teams[name].add_game(rec)

    def get_last_three(self, name):
        if(not (name in self.teams.keys())):
            return []
        else:
            return self.teams[name].get_last_three()

    def remove_team(self, name):
        self.teams.pop(name, None)

class team:
    def __init__(self):
        self.name = ''
        self.games = []

    def set_name(self, name):
        self.name = name

    def get_last_three(self):
        if(len(self.games) < 3):
            return self.games
        else:
            return self.games[-3:]

    def add_game(self, game):
        self.games.append(game)

class game_record:
    def __init__(self):
        self.name = ''
        self.distance = ''
        self.rest = ''

    def __init__(self, name, distance, rest):
        self.name = name
        self.rest = rest
        self.distance = distance