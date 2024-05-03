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
        self.N_ricorsioni_vecchie = 0
        self.N_soluzioni_vecchie = 0
        self._possibili_soluzioni_vecchie = []

    def worstCase(self, nerc, maxY, maxH):
        self.loadEvents(nerc)
        min_data = datetime.datetime(2015, 12, 25, 15, 42, 21)
        self.ricorsione([], maxY, maxH, 0, 0, min_data)

        ottima = self.get_max()
        print(ottima[0], ottima[1])
        for i in ottima[2]:
            print(i)
        """    
        print("*/*/*/*/")
        self.ricorsione_filtro_vecchio([], maxY, maxH, 0)
        ottima_vecchia = self.get_max_vecchia()
        print(ottima_vecchia[0], ottima_vecchia[1])
        for i in ottima_vecchia[2]:
            print(i)
        """
        return ottima

    def ricorsione(self, parziale, maxY, maxH, pos, durata_tot, min_data):
        self.N_ricorsioni += 1
        if pos == len(self._listEvents):
            self.N_soluzioni += 1
            popolazione = 0
            ore = 0
            for event in parziale:
                popolazione += event.customers_affected
                ore += event._durata
            self._possibili_soluzioni.append((popolazione, ore, copy.deepcopy(parziale)))
        #    print(parziale)
        else:
            for event in self._listEvents[pos: ]:
                pos += 1
                parziale.append(event)
                res_filtro = self.filtro(parziale, maxY, maxH, durata_tot, min_data)
                if res_filtro[0] == True:
                    durata_tot1 = res_filtro[1]
                    min_data1 = res_filtro[2]
                    self.ricorsione(parziale, maxY, maxH, pos, durata_tot1, min_data1)

                parziale.pop()

    def ricorsione_filtro_vecchio(self, parziale, maxY, maxH, pos):
        self.N_ricorsioni += 1
        if pos == len(self._listEvents):
            self.N_soluzioni += 1
            popolazione = 0
            ore = 0
            for event in parziale:
                popolazione += event.customers_affected
                ore += event._durata
            self._possibili_soluzioni_vecchie.append((popolazione, ore, copy.deepcopy(parziale)))
        #    print(parziale)
        else:
            for event in self._listEvents[pos: ]:
                pos += 1
                parziale.append(event)
                res_filtro = self.filtro_vecchio(parziale, maxY, maxH)
                if res_filtro:
                    self.ricorsione_filtro_vecchio(parziale, maxY, maxH, pos)

                parziale.pop()

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    @property
    def listNerc(self):
        return self._listNerc

    def filtro(self, parziale, maxY, maxH, durata_tot, min_data):
        parziale[-1].set_durata()
        durata_tot += parziale[-1]._durata
        if durata_tot > maxH:
            return False, durata_tot, min_data
        if parziale[-1].date_event_began < min_data:
            min_data = parziale[-1].date_event_began
        max_data = datetime.datetime(min_data.year + maxY, min_data.month, min_data.day, min_data.hour, min_data.minute,
                                     min_data.second)
        if parziale[-1].date_event_finished > max_data:
            return False, durata_tot, min_data

        return True, durata_tot, min_data

    def filtro_vecchio(self, parziale, maxY, maxH):
        durata_tot = 0
        for event in parziale:
            event.set_durata()
            durata_tot += event._durata
        if durata_tot > maxH:
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

    def get_max_vecchia(self):
        ottima = max(self._possibili_soluzioni_vecchie, key=(lambda x : x[0]))
        return ottima