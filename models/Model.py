from random import randint

from models.Database import Database
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
        self.stopwatch.start() #Käivitab stopperi

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

    def ask_name(self):
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
                self.show_leaderboard()
                self.show_menu()
            elif user_input == 3:
                print('Bye, Bye!!!')
                exit() #Igasugune skripti töö lõpp
        else:
            self.show_menu()

    def show_leaderboard(self):
        """Näita edetabelit"""
        db = Database()
        data = db.read_records()
        if data:
            for record in data:
                print(record) #Näitab terve listi
                #print(record[1]) #Näitab ainult nimesid