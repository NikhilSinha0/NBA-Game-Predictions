class teams:
    def __init__(self):
        self.teams = {}

    def add_game(self, name, distance, rest):
        rec = game_record(name, distance, rest)
        if(not (name in self.teams.keys())):
            self.teams[name] = team()
        self.teams[name].add_game(rec)

    def get_last_seven(self, name):
        if(not (name in self.teams.keys())):
            return None
        else:
            return self.teams[name].get_last_seven()

class team:
    def __init__(self):
        self.name = ''
        self.games = []

    def set_name(self, name):
        self.name = name

    def get_last_seven(self):
        if(len(self.games) < 7):
            return self.games
        else:
            return self.games[-7:]

    def add_game(self, game):
        games.append(game)

class game_record:
    def __init__(self):
        self.name = ''
        self.distance = ''
        self.rest = ''

    def __init__(self, name, distance, rest):
        self.name = name
        self.rest = rest
        self.distance = distance