import datetime

from models.Database import Database

class ExportToFile:

    def __init__(self, model):
        self.model = model
        self.db = Database()
        self.data = self.db.for_export()
        self.dst = self.db.db_name.replace('.db', '.txt')

    def export(self):
        try:
            with open(self.dst, 'w', encoding='utf-8') as f:
                f.write(f'name;steps;quess;cheater;game_length;game_time \n')
                for row in self.data:
                    name = row[1]
                    steps = row[2]
                    quess = row[3]
                    cheater = row[4]
                    game_length = self.model.format_time(row[5])
                    game_time = datetime.datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')
                    new_game_time = game_time.strftime('%d.%m.%Y %H:%M:%S')
                    f.write(f'{name};{steps};{quess};{cheater};{game_length};{new_game_time} \n')
            print(f'Edetabel eksporditi faili: {self.dst}')

        except Exception as e:
            print(f'Edetabeli eksportimisel tekkis tõrge: {e}')

