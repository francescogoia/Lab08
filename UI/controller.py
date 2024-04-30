import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()
        self._nerc = None

    def handleWorstCase(self, e):
        self.get_nerc()
        try:
            anni_X = int(self._view._txtYears.value)
            ore_Y = float(self._view._txtHours.value)
            #print(self._nerc, anni_X, ore_Y)
            ottime = self._model.worstCase(self._nerc, anni_X, ore_Y)
        except ValueError:
            self._view.create_alert("Inserire dei numeri")



    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v

    def get_nerc(self):
        self._nerc = self._idMap[self._view._ddNerc.value]
