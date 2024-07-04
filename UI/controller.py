import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []
        self._shape = None
        self._anno = None

    def fillDD(self):
        shapes, anni = self._model.getComponentiDD()
        for s in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        for a in anni:
            self._view.ddyear.options.append(ft.dropdown.Option(a))
        self._view.update_page()

    def handle_graph(self, e):
        self._shape = self._view.ddshape.value
        self._anno = self._view.ddyear.value

        if self._shape is None or self._anno is None:
            warnings.warn_explicit(message="Errore nella selezione di uno degli elementi",
                                   category=TypeError,
                                   filename="controller.py",
                                   lineno=25)
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text('Errore nella selezione della forma "shape" o dell anno "year" '))
            self._view.update_page()
            return
        self._model.buildGraph(self._shape, self._anno)
        adiacenti = self._model.getSommaAdiacenti()
        n, e = self._model.getNumeri()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f'Il grafo è stato correttamente creato'))
        self._view.txt_result.controls.append(
            ft.Text(f'Il grafo ha {n} stati collegati tra loro da {e} archi'))
        for a in adiacenti:
            self._view.txt_result.controls.append(ft.Text(f'Nodo {a[0]}, somma pesi su archi: {a[1]}'))
        self._view.update_page()


    def handle_path(self, e):
        path = self._model.getPath()