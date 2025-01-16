"""
Stopperi klass
"""
import threading
import time


class Stopwatch:
    def __init__(self): #Stopperi konstruktor
        self.seconds = 0 #Aeg sekundites
        self.running = False   # Kas aeg töötab
        self.thread = None #Eraldi threadis, et jookseks taustaks

    def start(self): #Käivita stopper
        if not self.running: #Kui aeg ei jookse
            self.running = True #Aeg käima
            self.thread = threading.Thread(target=self._run) #Lisatud threadi
            self.thread.start() #Käivita thread

    def _run(self): #Aeg jookseb threadis
        while self.running:
            time.sleep(1) #Oota üks sekund
            self.seconds += 1 #Suurenda sekundit ühe võtta

    def stop(self): #Peata stopper
        self.running = False

    def reset(self):
        """Aja reset"""
        self.stop() #Aeg peatada
        self.seconds = 0 #Aeg nullida

    def format_time(self):
        """Aja muutmine inimlikuks"""
        hours = self.seconds // 3600
        minutes = (self.seconds % 3600) // 60
        seconds = self.seconds % 60
        return "%02d:%02d:%02d" % (hours, minutes, seconds) #Tagastab aja
        #return f'{hours:02}:{minutes:02}:{seconds:02}' #Teine variant