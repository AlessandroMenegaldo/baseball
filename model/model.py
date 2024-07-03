import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allTeams = []
        self._grafo = nx.Graph()

    def buildGraph(self, year):
        self._grafo.clear()
        if len(self._allTeams) == 0:
            print("Lista squadre vuota.")
            return

        self._grafo.add_nodes_from(self._allTeams)

        #grafo completo: aggiungo tutti i possibili archi
        myedges = list(itertools.combinations(self._allTeams, 2))

        self._grafo.add_edges_from(myedges)

        #stessa cosa di ittertools.combinations
        # for t1 in self._grafo.nodes:
        #     for t2 in self._grafo.nodes:
        #         if t1 != t2:
        #             self._grafo.add_edge(t1, t2)

        # aggiungere i pesi qui!

        salariesOfTeams = DAO.getSalaryOfTeams(year, self._idMapTeams)
        for e in self._grafo.edges:
            self._grafo[e[0]][e[1]]["weight"] = salariesOfTeams[e[0]] + salariesOfTeams[e[1]]

        # for t1 in self._grafo.nodes:
        #     for t2 in self._grafo.nodes:
        #         if t1 != t2:
        #             self._grafo.add_edge(t1, t2)


    def getWeightsOfPath(self, path):
        listTuples = [(path[0], 0)]
        for i in range(0, len(path) - 1):
            listTuples.append((path[i + 1], self._grafo[path[i]][path[i + 1]]["weight"]))

        return listTuples


    def getSortedNeighbors(self, v0):
        vicini = self._grafo.neighbors(v0)
        viciniTuples = []
        for v in vicini:
            viciniTuples.append((v, self._grafo[v0][v]["weight"]))

        viciniTuples.sort(key=lambda x: x[1], reverse=True)
        return viciniTuples


    def getYears(self):
        return DAO.getAllYears()


    def getTeamsOfYear(self, year):
        self._allTeams = DAO.getTeamsOfYear(year)
        self._idMapTeams = {t.ID: t for t in self._allTeams}

        # for t in self._allTeams:
        #     self._idMapTeams[t.ID] = t
        return self._allTeams


    def printGraphDetails(self):
        print(f"Grafo creato con {len(self._grafo.nodes)} nodi e {len(self._grafo.edges)} archi.")


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)