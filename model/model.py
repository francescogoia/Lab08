import copy
import datetime

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self._possibili_soluzioni = []



    def worstCase(self, nerc, maxY, maxH):
        self.loadEvents(nerc)
        self.ricorsione([], maxY, maxH, set(self._listEvents))

        ottime = self.get_max()
        return ottime
    def ricorsione(self, parziale, maxY, maxH, eventi_rimanenti):
        # TO FILL

        if len(eventi_rimanenti) == 0:
            self._possibili_soluzioni.append(copy.deepcopy(parziale))
            print(parziale)
        else:
            for event in eventi_rimanenti:
                if self.filtro(parziale, event, maxY, maxH):
                    parziale.append(event)
                    new_eventi_rimanenti = copy.deepcopy(eventi_rimanenti)
                    new_eventi_rimanenti.remove(event)
                    self.ricorsione(parziale, maxY, maxH, new_eventi_rimanenti)
                    parziale.pop()
                else:
                    pass
        pass

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc

    def filtro(self, parziale, evento, maxY, maxH):
        tot_durata = evento._durata
        for event in parziale:
            tot_durata += event._durata
        max_secondi = maxH * 3600
        if tot_durata > max_secondi:
            return False

        min_data = datetime.datetime(2015, 12, 25, 15, 42, 21)
        for event in parziale:
            if event.date_event_began < min_data:
                min_data = event.date_event_began
        max_data = datetime.datetime(min_data.year+maxY, min_data.month, min_data.day, min_data.hour, min_data.minute, min_data.second)
        if evento.date_event_finished > max_data:
            return False

        return True

    def get_max(self):
        tot_popolazione = 0
        best_soluzioni = []
        for sol in self._possibili_soluzioni:
            tot_popolazione += sol.customers_affected
        for sol in self._possibili_soluzioni:
            if sol.customers_affected >= tot_popolazione:
                best_soluzioni.append(sol)
        return best_soluzioni
