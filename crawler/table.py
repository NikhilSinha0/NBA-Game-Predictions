import os

class game_table:
    home = ''
    away = ''

    month = ''
    day = ''
    year = ''

    home_scores = {}
    away_scores = {}

    add_to_home = False
    remove_MP = True

    def add_name(self, name):
        if(self.away):
            self.home = name.split('(')[0].strip()
        else:
            self.away = name.split('(')[0].strip()

    def add_to_home_scores(self, row):
        if(self.home_scores.get(row[0])):
            if(row[1]=='Did Not Play'):
                return
            if(self.remove_MP):
                self.home_scores.get(row[0]).extend(row[2:])    
            else:
                self.home_scores.get(row[0]).extend(row[1:])
        else:
            self.home_scores[row[0]] = row[1:]

    def add_to_away_scores(self, row):
        if(self.away_scores.get(row[0])):
            if(row[1]=='Did Not Play'):
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
        result = ''
        result += 'Away: ' + self.away + '\n'
        for name, stats in self.away_scores.items():
            result += name + ',' + ','.join(stats)
            result += '\n'
        result += 'Home: ' + self.home + '\n'
        for name, stats in self.home_scores.items():
            result += name + ',' + ','.join(stats)
            result += '\n'
        path = './game_scores'
        fname = self.away.split(' ')[1]+'At'+self.home.split(' ')[1]+str(self.month)+str(self.day)+str(self.year)
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(os.path.join(path, fname+".txt"),"w+")
        f.write(result)
        f.close
        print('Created file ' + fname)

    def set_date(self, date):
        date = date.split('/')
        self.month = date[0]
        self.day = date[1]
        self.year = date[2]

