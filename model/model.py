import copy
import datetime
import time

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self._possibili_soluzioni = []
        self.N_ricorsioni = 0
        self.N_soluzioni = 0

    def worstCase(self, nerc, maxY, maxH):
        self.loadEvents(nerc)
        self.fine_ricorsione = False
        self.ricorsione([], maxY, maxH, set(self._listEvents))

        ottima = self.get_max()
        print(ottima[0])
        for i in ottima[1]:
            print(i)
        return ottima

    def ricorsione(self, parziale, maxY, maxH, eventi_rimanenti):
        self.N_ricorsioni += 1
        if self.fine_ricorsione:
            self.N_soluzioni += 1
            popolazione = 0
            for event in parziale:
                popolazione += event.customers_affected
            self._possibili_soluzioni.append((popolazione, copy.deepcopy(parziale)))
        #    print(parziale)
        else:
            contatore = 0
            lunghezza_rimanenti = len(eventi_rimanenti)
            for event in eventi_rimanenti:
                parziale.append(event)
                contatore += 1
                if contatore == lunghezza_rimanenti:
                    self.fine_ricorsione = True
                if self.filtro(parziale, maxY, maxH):
                    new_eventi_rimanenti = copy.deepcopy(eventi_rimanenti)
                    new_eventi_rimanenti.remove(event)
                    self.ricorsione(parziale, maxY, maxH, new_eventi_rimanenti)
                parziale.pop()

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    @property
    def listNerc(self):
        return self._listNerc

    def filtro(self, parziale, maxY, maxH):
        tot_durata = 0
        for event in parziale:
            event.set_durata()
            tot_durata += event._durata
        max_secondi = maxH * 3600
        if tot_durata > max_secondi:
            return False

        min_data = datetime.datetime(2015, 12, 25, 15, 42, 21)
        for event in parziale:
            if event.date_event_began < min_data:
                min_data = event.date_event_began
        max_data = datetime.datetime(min_data.year + maxY, min_data.month, min_data.day, min_data.hour, min_data.minute,
                                     min_data.second)
        if parziale[-1].date_event_finished > max_data:
            return False

        return True

    def get_max(self):
        ottima = max(self._possibili_soluzioni, key=(lambda x : x[0]))
        return ottima
