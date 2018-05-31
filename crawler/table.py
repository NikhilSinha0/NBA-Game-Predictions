import os

class game_table:
    def __init__(self):
        self.home = ''
        self.away = ''

        self.home_last_game = ''
        self.home_last_game_location = ''
        self.away_last_game = ''
        self.away_last_game_location = ''

        self.date = ''

        self.home_scores = {}
        self.away_scores = {}

        self.add_to_home = False
        self.remove_MP = True

    def add_name(self, name):
        if(self.away):
            self.home = name.split('(')[0].strip()
        else:
            self.away = name.split('(')[0].strip()

    def add_last_game_info(self, prevs):
        for prev_game in prevs:
            if(self.away==prev_game[0]):
                self.away_last_game_location = prev_game[1]
                self.away_last_game = "/".join([prev_game[2][:4], prev_game[2][4:6], prev_game[2][6:]])
            else:
                self.home_last_game_location = prev_game[1]
                self.home_last_game = "/".join([prev_game[2][4:6], prev_game[2][6:], prev_game[2][:4]])

    def add_to_home_scores(self, row):
        if(self.home_scores.get(row[0])):
            if(len(row)==2):
                return
            if(self.remove_MP):
                self.home_scores.get(row[0]).extend(row[2:])    
            else:
                self.home_scores.get(row[0]).extend(row[1:])
        else:
            self.home_scores[row[0]] = row[1:]

    def add_to_away_scores(self, row):
        if(self.away_scores.get(row[0])):
            if(len(row)==2):
                return
            if(self.remove_MP):
                self.away_scores.get(row[0]).extend(row[2:])    
            else:
                self.away_scores.get(row[0]).extend(row[1:])
        else:
            self.away_scores[row[0]] = row[1:]

    def add_data_row(self, row):
        if(self.add_to_home):
            self.add_to_home_scores(row)
        else:
            self.add_to_away_scores(row)

    def add_row(self, row):
        if(not row[0]):
            self.remove_MP = not self.remove_MP
            if(self.away_scores and 'Basic' in row[1]):
                self.add_to_home = True
        elif(row[0]=='Starters'):
            row[0]='Name'
            self.add_data_row(row)
        elif(row[0]=='Reserves'):
            pass
        else:
            self.add_data_row(row)

    def print_table(self):
        print('Away: ' + self.away)
        print(self.away_scores)
        print('Home: ' + self.home)
        print(self.home_scores)

    def table_to_csv(self):
        result = 'Date: '+self.date+'\n'
        result += 'Away: ' + self.away + '\n'
        result += 'Last Game Date: '+self.away_last_game+'\n'
        result += 'Last Game Location: '+self.away_last_game_location+'\n'
        for name, stats in self.away_scores.items():
            result += name + ',' + ','.join(stats)
            result += '\n'
        result += 'Home: ' + self.home + '\n'
        result += 'Last Game Date: '+self.home_last_game+'\n'
        result += 'Last Game Location: '+self.home_last_game_location+'\n'
        for name, stats in self.home_scores.items():
            result += name + ',' + ','.join(stats)
            result += '\n'
        path = './game_csvs'
        fname = self.away.split(' ')[-1]+'At'+self.home.split(' ')[-1]+("".join(self.date.split("/")))
        if not os.path.exists(path):
            os.makedirs(path)
            print('Created path ' + path)
        f = open(os.path.join(path, fname+".csv"),"w+")
        f.write(result)
        f.close()
        print('Created file ' + fname+".csv")

    def table_to_json(self):
        result = "{\n"
        result += '\"Date\": \"'+self.date+'\",\n'
        result += '\"Away\": {\n'
        result += '\"Name\": \"' + self.away + '\",\n'
        result += '\"Last Game\": {\n'
        result += '\"Date: \": \"' + self.away_last_game + '\",\n'
        result += '\"Location: \": \"' + self.away_last_game_location + '\"\n'
        result += '},\n'
        result += '\"Players\": [\n'
        items = []
        for key in self.away_scores.keys():
            val = self.away_scores.get(key)[:]
            val.insert(0, key)
            items.append(val)
        header = items[0]
        players = items[1:-1]
        totals = items[-1]
        for i in range(len(players)):
            result += (',\n' if i!=0 else '')
            result += '{'
            for j in range(len(players[i])):
                result += ('\",\"' if j!=0 else '\"') + header[j] + '\": \"' + players[i][j]
            result += "\"}"
        result += '\n],\n'
        for i in range(len(totals)):
            if(i==0):
                result += '\"' + totals[0] +'\": {'
            else:
                result += ('\",\"' if i!=1 else '\"') + header[i] + '\": \"' + totals[i]
        result += "\"}\n"
        result += "},\n"
        result += '\"Home\": {\n'
        result += '\"Name\": \"' + self.home + '\",\n'
        result += '\"Last Game\": {\n'
        result += '\"Date: \": \"' + self.home_last_game + '\",\n'
        result += '\"Location: \": \"' + self.home_last_game_location + '\"\n'
        result += '},\n'
        result += '\"Players\": [\n'
        items = []
        for key in self.home_scores.keys():
            val = self.home_scores.get(key)[:]
            val.insert(0, key)
            items.append(val)
        header = items[0]
        players = items[1:-1]
        totals = items[-1]
        for i in range(len(players)):
            result += (',\n' if i!=0 else '')
            result += '{'
            for j in range(len(players[i])):
                result += ('\",\"' if j!=0 else '\"') + header[j] + '\": \"' + players[i][j]
            result += "\"}"
        result += '\n],\n'
        for i in range(len(totals)):
            if(i==0):
                result += '\"' + totals[0] +'\": {'
            else:
                result += ('\",\"' if i!=1 else '\"') + header[i] + '\": \"' + totals[i]
        result += "\"}\n"
        result += "}\n"
        result += "}"
        path = './game_jsons'
        fname = self.away.split(' ')[-1]+'At'+self.home.split(' ')[-1]+("".join(self.date.split("/")))
        if not os.path.exists(path):
            os.makedirs(path)
            print('Created path ' + path)
        f = open(os.path.join(path, fname+".json"),"w+")
        f.write(result)
        f.close()
        print('Created file ' + fname+".json")

    def set_date(self, date):
        self.date = date

