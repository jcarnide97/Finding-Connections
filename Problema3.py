from collections import defaultdict
from itertools import combinations
INF = 99999


class Network:
    def __init__(self, vertices):
        self.v = vertices  # número de vertices
        self.graph = defaultdict(list)  # dicionario para a rede
        self.times = 0  # quantas vezes visitou
        self.graph_servers = []  # rede apenas com servidores (para kruskal)

    def add_ligacao(self, v1, v2):
        self.graph[v1].append(v2)
        self.graph[v2].append(v1)

    def pontos_articulacao(self, v, visitado, ap, parent, low, dfs):
        child = 0
        visitado[v] = True
        dfs[v] = self.times
        low[v] = self.times
        self.times += 1
        for w in self.graph[v]:
            if not visitado[w]:
                parent[w] = v
                child += 1
                self.pontos_articulacao(w, visitado, ap, parent, low, dfs)
                low[v] = min(low[v], low[w])
                if parent[v] == -1 and child > 1:
                    ap[v] = True
                if parent[v] != -1 and low[w] >= dfs[v]:
                    ap[v] = True
            elif w != parent[v]:
                low[v] = min(low[v], dfs[w])

    def n_servers(self):  # retorna uma lista de todos os servidores encontrados
        visitado = [False] * self.v
        low = [float("Inf")] * self.v
        dfs = [float("Inf")] * self.v
        parent = [-1] * self.v
        ap = [False] * self.v
        for i in range(self.v):
            if not visitado[i]:
                self.pontos_articulacao(i, visitado, ap, parent, low, dfs)
        lista_server = []
        for index, value in enumerate(ap):
            if value:
                lista_server.append(index)
        return lista_server

    def floyd_warshall(self, matrix, v):
        dist = list(map(lambda i: list(map(lambda j: j, i)), matrix))
        for i in range(v):
            dist[i][i] = 0
        for k in range(v):
            for i in range(v):
                for j in range(v):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        return dist

    def comp_cabo(self, servers, matrix):
        cabo = 0
        comb_servers = []
        add = []
        for subset in combinations(servers, 2):
            comb_servers.append(list(subset))
        for i in range(len(comb_servers)):
            if matrix[comb_servers[i][0]][comb_servers[i][1]] == INF:
                cabo += 0
            elif comb_servers[i] not in add:
                add.append(comb_servers[i])
                cabo += matrix[comb_servers[i][0]][comb_servers[i][1]]
                self.graph_servers.append([comb_servers[i][0], comb_servers[i][1], matrix[comb_servers[i][0]][comb_servers[i][1]]])
        return cabo

    def find_set(self, parent, i):
        if parent[i] == i:
            return i
        return self.find_set(parent, parent[i])

    def union(self, parent, rank, x, y):
        x_root = self.find_set(parent, x)
        y_root = self.find_set(parent, y)
        if rank[x_root] < rank[y_root]:
            parent[x_root] = y_root
        elif rank[x_root] > rank[y_root]:
            parent[y_root] = x_root
        else:
            parent[y_root] = x_root
            rank[x_root] += 1

    def kruskal(self):
        i = 0
        e = 0
        self.graph_servers = sorted(self.graph_servers, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.v):
            parent.append(node)
            rank.append(0)
        short_d = 0
        while e < self.v - 1 and i < len(self.graph_servers):
            u, v, w = self.graph_servers[i]
            i = i + 1
            x = self.find_set(parent, u)
            y = self.find_set(parent, v)
            if x != y:
                e = e + 1
                short_d += w
                self.union(parent, rank, x, y)
        return short_d


if __name__ == '__main__':
    while True:
        try:
            net = int(input())
            network = Network(net)
            matriz_ad = [[INF for col in range(net)] for row in range(net)]  # matriz de adjacencia
            aux_list = []
            while True:
                dados = input()
                dados = dados.split(' ', 2)
                lig1 = int(dados[0])
                if lig1 == 0:
                    break
                else:
                    lig2 = int(dados[1])
                    comp = int(dados[2])
                    aux_list.append([lig1 - 1, lig2 - 1, comp])
                    network.add_ligacao(lig1-1, lig2-1)
            servers = network.n_servers()
            if not servers:
                print('no server')
                continue
            else:
                if len(servers) == 1:
                    print(len(servers), "0 0")
                    continue
                else:
                    for i in range(len(aux_list)):
                        matriz_ad[aux_list[i][0]][aux_list[i][1]] = aux_list[i][2]
                        matriz_ad[aux_list[i][1]][aux_list[i][0]] = aux_list[i][2]
                    pesos = network.floyd_warshall(matriz_ad, net)
                    cabo_network = network.comp_cabo(servers, pesos)
                    arvo_network = network.kruskal()
                    print(len(servers), cabo_network, arvo_network)
        except EOFError:
            break
