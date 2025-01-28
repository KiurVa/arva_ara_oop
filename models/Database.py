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

    def read_records(self):
        """Andmebaasi info lugemiseks"""
        if self.cursor:
            try:
                sql = f'SELECT * FROM {self.table};'
                self.cursor.execute(sql) #Päringu käivitamiseks
                data = self.cursor.fetchall() #Kõik kirjed muutujasse data
                return data #Meetod tagastab meile kogu info
            except sqlite3.Error as error:
                print(f'Kirjete lugemisel ilmnes tõrge: {error}')
                return [] #Tagastab tühja listi
            finally:
                self.close_connection()
        else:
            print('Ühendus andmebaasiga puudub. Palun loo ühendus andmebaasiga.')

    def add_record(self, name, steps, pc_nr, cheater, seconds):
        """Lisab mängija andmetabelisse"""
        if self.cursor:
            try:
                sql = f'INSERT INTO {self.table} (name, steps, quess, cheater, game_length) VALUES (?, ?, ?, ?, ?);'
                self.cursor.execute(sql, (name, steps, pc_nr, cheater, seconds)) #Üritab lisada andmeid. Aga ei tea kas õnnestub
                self.conn.commit() #See lisab realselt tabelisse(save)
                print('Mängija on lisatud tabelisse.')
            except sqlite3.Error as error:
                print(f'Mängija lisamisel tekkis tõrge: {error}')
            finally:
                self.close_connection() #See tuleb ühenduse. Alati
        else:
            print('Ühendus puudub! Palun loo ühendus andmebaasiga.')

    def no_cheater(self):
        if self.cursor:
            try:
                sql = (f'SELECT name, quess, steps, game_length FROM {self.table} WHERE cheater=?'
                       f'ORDER BY steps, game_length, name DESC LIMIT 10;')
                self.cursor.execute(sql, (0,)) #Päringu käivitamiseks
                data = self.cursor.fetchall() #Kõik kirjed muutujasse data
                return data #Meetod tagastab meile kogu info
            except sqlite3.Error as error:
                print(f'Kirjete lugemisel ilmnes tõrge: {error}')
                return [] #Tagastab tühja listi
            finally:
                self.close_connection()
        else:
            print('Ühendus andmebaasiga puudub. Palun loo ühendus andmebaasiga.')

    def for_export(self):
        if self.cursor:
            try:
                sql = (f'SELECT * FROM {self.table} ORDER BY steps, game_length, name;')
                self.cursor.execute(sql) #Päringu käivitamiseks
                data_e = self.cursor.fetchall() #Kõik kirjed muutujasse data
                if not data_e:
                    print(f'Tabelis pole andmeid!')
                    return []
                return data_e #Meetod tagastab meile kogu info
            except sqlite3.Error as error:
                print(f'Kirjete lugemisel ilmnes tõrge: {error}')
                return [] #Tagastab tühja listi
            finally:
                self.close_connection()
        else:
            print('Ühendus andmebaasiga puudub. Palun loo ühendus andmebaasiga.')

