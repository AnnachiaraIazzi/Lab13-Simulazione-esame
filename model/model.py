import copy

from database.DAO import DAO
import networkx as nx
from datetime import datetime
from geopy.distance import distance
class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._AllSig = DAO.getAllSightings()
        self._AllStates = DAO.getAllStates()
        self._idMap = {}
        for s in self._AllStates:
            self._idMap[s.id] = s
        self._bestPath = []
        self._lun = 0
        self._path_edge = []

    def getComponentiDD(self):
        shapes = []
        anni = []
        for s in self._AllSig:
            if s.shape not in shapes:
                shapes.append(s.shape)
            if s.datetime.year not in anni:
                anni.append(s.datetime.year)
        shapes.sort()
        anni.sort(reverse=True)
        return shapes, anni

    def buildGraph(self, shape, anno):
        self._grafo.add_nodes_from(self._AllStates)
        self._grafo.clear_edges()
        connessioni = DAO.getConnessioni(shape, anno, self._idMap)
        for c in connessioni:
            self._grafo.add_edge(c[0], c[1], weight=c[2])

    def getSommaAdiacenti(self):
        adiacenti = []
        for s in self._AllStates:
            peso = 0
            for v in self._grafo.edges(s, data=True):
                peso+= v[2]['weight']

            adiacenti.append((s, peso))
        return adiacenti

    def getNumeri(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getDistanzaGeoLista(self, parziale):
        peso = 0
        for e in parziale:
            peso += distance((e[0].Latitude, e[0].Longitude), (e[1].Latitude, e[1].Longitude)).km
        return peso

    def getPath(self):
        self._bestPath = []
        self._lun = 0

        for n in self._grafo.nodes():
            parziale = []
            parziale.append(n)
            self.ricorsione(parziale, [])

        return self._path_edge

    def ricorsione(self, parziale, archi_parziale):
        vicini = self._getVicini(parziale[-1], archi_parziale)

        if len(vicini)==0:
            peso = self.getDistanzaGeoLista(archi_parziale)
            if peso>self._lun:
                self._bestPath = copy.deepcopy(parziale)
                self._lun = peso
                self._path_edge = copy.deepcopy(archi_parziale)
        for n in vicini:
            archi_parziale.append(parziale[-1], n, self._grafo.get_edge_data(parziale[-1], n)['weight'])
            parziale.append(n)

            self.ricorsione(parziale, archi_parziale)
            parziale.pop()
            archi_parziale.pop()


    def _getVicini(self, nodo, archi_parziale):
        vicini = self._grafo.edges(nodo, data=True)
        result = []
        for v in vicini:
            if len(archi_parziale)!=0:
                if v[2]['weight'] > archi_parziale[-1][2]:
                    result.append(v[1])
            else:
                result.append(v[1])
        return result


