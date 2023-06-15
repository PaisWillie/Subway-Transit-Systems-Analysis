from GraphModels import EdgeWeightedDigraph, Node

# Apply DFS from every station, if adjacent station is not a different zone, then it is connected
# If it is a different zone, then it is not connected


class ConnectedIslands:
    _marked: list[bool]
    _ids: list[int]
    _nodes: list[Node]
    _count: int
    _graph: EdgeWeightedDigraph

    def __init__(self, graph: EdgeWeightedDigraph):
        self._graph = graph
        self._marked = [False for _ in range(graph.V())]
        self._ids = [0 for _ in range(graph.V())]
        self._nodes = graph.getNodes()

        self._count = 0

        for v in graph.getNodeIds():
            if not self._marked[v]:
                self._dfs(v)
                self._count += 1

    def _getZone(self, nodeId: int) -> float:
        return float(self._nodes[nodeId].getDataValue("zone"))

    def _isSameZone(self, v: int, w: int) -> bool:
        # If zone int is within 0.5 of each other, then it is the same zone
        return abs(self._getZone(v) - self._getZone(w)) < 0.5

    def _dfs(self, v: int):
        self._marked[v] = True
        self._ids[v] = self._count

        for edge in self._graph.adj(v):
            w = edge.otherNodeId(v)
            # If the other node is not in the same zone, then it is not connected
            if not self._marked[w] and self._isSameZone(v, w):
                self._dfs(w)

    def count(self) -> int:
        return self._count

    def connected(self, v: int, w: int) -> bool:
        return self._marked[v] and self._marked[w]

    def get_connected_islands(self, stationId: int) -> list[int]:
        return [i for i, x in enumerate(self._ids) if x == self._ids[stationId]]

    def __str__(self):

        s = f"{self._count} connected components\n"

        for i in range(self._count):
            s += f"{i}: "
            for v in range(self._graph.V()):
                if self._ids[v] == i:
                    s += f"{v} "
            s += "\n"
        return s
