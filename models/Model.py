from random import randint

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
