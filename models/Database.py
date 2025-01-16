import sqlite3


class Database:
    db_name = 'game_leaderboard_v2.db' #Andmebaasi nimi
    table = 'ranking' #Vajalik tabeli nimi

    def __init__(self):
        """Konstruktor"""
        self.conn = None #Ühendus
        self.cursor = None #Muutuja objekt cursor. vajalik.
        self.connect() #Loo ühendus

    def connect(self):
        """Loob ühenduse andmebaasiga"""
        try:
            if self.conn:
                self.conn.close() #Kui ühendus, siis sulgeks
                print('Varasem ühendus suleti.')
            self.conn = sqlite3.connect(self.db_name) #Loome ühenduse
            self.cursor = self.conn.cursor()
            print(f'Uus ühendus andmebaasiga {self.db_name} loodud.')
        except sqlite3.Error as error: #Toob välja vea, kui ühendust ei saa luua
            print(f'Tõrge andmebaasi ühenduse loomisel: {error}')
            self.conn = None
            self.cursor = None

    def close_connection(self):
        """Sulgeb andmebaasi ühenduse"""
        try:
            if self.conn:
                self.conn.close()
                print(f'Ühendus andmebaasiga {self.db_name} suletud.')
        except sqlite3.Error as error:
            print(f'Tõrge ühenduse sulgemisel: {error}')
