import datetime
from random import randint
from time import strftime, gmtime

from models.Database import Database
from models.ExportToFile import ExportToFile
from models.Stopwatch import Stopwatch


class Model:
    """Defineerime klassi muutujad"""
    pc_nr = randint(1,100) #Juhuslik number
    steps = 0 #Sammude arv
    game_over = False #Mäng ei ole läbi
    cheater = False #Mängija ei ole petja
    stopwatch = Stopwatch() #Loome stopperi objekti

    def __init__(self):
        """Konstruktor"""
        self.reset_game()

    def reset_game(self):
        """Teeb uue mängu"""
        self.pc_nr = randint(1,100)
        self.steps = 0
        self.game_over = False
        self.cheater = False
        self.stopwatch.reset() #Nullib stopperi
        # self.stopwatch.start() #Käivitab stopperi

    def ask(self):
        """Küsib numbrit ja kontrollib"""
        user_nr = int(input("Sisesta number: ")) #Küsib numbrit
        self.steps += 1 #Sammude arv kasvab

        if user_nr == 1000: #tagauks
            self.cheater = True #Oled petja
            self.game_over = True #Mäng läbi
            self.stopwatch.stop() #Peata aeg
            print(f'Leidsid mu nõrga koha. Õige number on {self.pc_nr}.')
        elif user_nr > self.pc_nr: #Kui pakutakse väiksem
            print('Väiksem')
        elif user_nr < self.pc_nr: #Kui pakutakse suurem
            print('Suurem')
        elif user_nr == self.pc_nr: #Kui number on sama
            self.game_over = True #Mäng läbi
            self.stopwatch.stop() #Aeg kinni
            print(f'Leidsid õige numbri {self.steps} sammuga.')

    def lets_play(self):
        """Mängime mängu avalik meetod"""
        self.stopwatch.start()
        while not self.game_over:
            self.ask()
        #Näita mängu aega
        print(f'Mäng kestis {self.stopwatch.format_time()}.')
        self.what_next() #Mis on järgmiseks Nime küsimine ja kirje lisamine
        self.show_menu() #Näita mängu menüüd

    def what_next(self):
        """Küsime nime ja lisame info andmebaasi"""
        name =  self.ask_name()
        db = Database() #Loome andmebaasi objekti
        db.add_record(name, self.steps, self.pc_nr, self.cheater, self.stopwatch.seconds)

    @staticmethod
    def ask_name():
        """Küsib nime ja tagastab korrektse nime"""
        name = input('Kuidas on mängija nimi: ')
        if not name.strip():
            name = 'Teadmata'
        return name.strip().title()

    def show_menu(self):
        """Näita mängu menüüd"""
        print('1 - Mängima')
        print('2 - Edetabel')
        print('3 - Välju programmist')
        user_input = int(input('Sisesta number [1, 2 või 3]: '))
        if 1 <= user_input <= 3:
            if user_input == 1:
                self.reset_game()
                self.lets_play()
            elif user_input == 2:
                #self.show_leaderboard()
                self.show_no_cheater()
                self.show_menu()
            elif user_input == 3:
                print('Bye, Bye!!!')
                exit() #Igasugune skripti töö lõpp
        else:
            self.show_menu()

    @staticmethod
    def format_time(seconds):
        """Aja muutmine inimlikuks"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        #return "%02d:%02d:%02d" % (hours, minutes, seconds) #Tagastab aja
        return f'{hours:02}:{minutes:02}:{seconds:02}' #Teine variant

    def show_leaderboard(self):
        """Näita edetabelit"""
        db = Database()
        data = db.no_cheater()
        print('{:<19}{:<10}{:<10}'.format('Nimi', 'Number', 'Sammud',) + 'Mängu aeg') #prindib edetabeli päise
        if data:
            for record in data:
                name = record[0][:15] #Näitame asukohta ja teeme et max 15
                quess = record[1]
                steps = record[2]
                #length = record[3]
                #hrs = strftime('%H:%M:%S', gmtime(length)) #Teeb nii, et kaks 00 tunni omas
                #hrs = datetime.timedelta(seconds=length) #Muudab sekundid t.m.s
                print('{:<19}{:<10}{:<9}'.format(name, quess, steps,), self.format_time(record[3])) #Tühikutega mängimine muudab
                #print(self.format_time(record[3]))
                #print(record[1]) #Näitab ainult nimesid

    def show_no_cheater(self):
        """Edetabel ausatele mängijatele"""
        db = Database()
        data = db.no_cheater()
        if data:
            #Vormindus funktsiooni veerule
            formatter = {
                'Mängu aeg': self.format_time,
            }
            print() #Tühirida enne tabelit
            #self.print_table(data, formatters)
            self.show_leaderboard()
            print() #Tühirida peale tabelit

            etf = ExportToFile(self)
            etf.export()