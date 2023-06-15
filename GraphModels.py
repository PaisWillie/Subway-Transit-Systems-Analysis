class Node:

    _id: int

    _data: dict

    def __init__(self, id: int, data=None):
        self._id = id
        self._data = data

    def getId(self):
        return self._id

    def isEquals(self, node):
        return self.getId() == node.getId()

    def getData(self) -> dict:
        return self._data

    def getDataValue(self, key):
        return self._data[key]


class DirectedEdge:
    _v: str
    _w: str
    _line: int
    _data: dict
    _weight: float

    def __init__(self, fromNodeId: int, toNodeId: int, weight: int, **kwargs: dict):
        self._data = kwargs
        self._w = toNodeId
        self._v = fromNodeId
        self._weight = float(weight)
        self._line = kwargs.get("line") if "line" in kwargs else None

    def weight(self) -> float:
        return self._weight

    def fromNodeId(self) -> int:
        return self._v

    def toNodeId(self) -> int:
        return self._w

    def otherNodeId(self, node: int) -> int:
        if node == self._v:
            return self._w
        elif node == self._w:
            return self._v
        else:
            raise ValueError("Inconsistent edge")

    def getLine(self) -> int:
        return self._line

    def isLineChange(self, new_line: int) -> bool:
        if self._line == new_line:
            return False
        return True

    def __repr__(self):
        return f"{self._v} -> {self._w} (w: {self._weight}, l: {self._line})"


class EdgeWeightedDigraph:
    _V: int
    _E: int
    _adj: list[DirectedEdge]
    _nodes: list[Node]
    _mapping : dict

    def __init__(self, V: int):
        self._V = V
        self._E = 0
        self._adj = {}
        self._nodes = []

    def add_edge(self, e: DirectedEdge) -> None:
        if e.fromNodeId() not in self._adj:
            self._adj[e.fromNodeId()] = []
        self._adj[e.fromNodeId()].append(e)
        self._E += 1
        return

    def adj_matrix(self) -> list[list[float]]:
        result = [[float("inf")] * self._V for _ in range(self._V)]
        for nodeId in self._adj:
            for edge in self._adj[nodeId]:
                result[int(nodeId)][int(edge.toNodeId())] = edge.weight()
        return result

    def addMapping(self, mapping):
        self._mapping = mapping

    def getMapping(self):
        return self._mapping
        
    def addNodes(self, nodes: list[Node]):
        self._nodes = nodes

    def getNodeIds(self) -> set[str]:
        return set([node.getId() for node in self._nodes])

    def getNodes(self) -> list[Node]:
        return self._nodes

    def getNodeNum(self) -> int:
        return self._V

    def getEdgeNum(self) -> int:
        return self._E

    def getNodeData(self) -> dict[str, dict]:
        result = {}
        for node in self._nodes:
            result[node.getId()] = node.getData()
        return result

    def adj(self, v: str) -> list[DirectedEdge]:
        return self._adj[v]

    def getAdj(self) -> dict[int: list[DirectedEdge]]:
        return self._adj

    def V(self) -> int:
        return self._V

    def E(self) -> int:
        return self._E

    def __str__(self):
        return f"V: {self._V}, E: {self._E}, Adj: {self._adj}"

    def print_adj(self):
        import pprint
        pprint.pprint(self._adj)

    def __repr__(self):
        return f"V: {self._V}, E: {self._E}, Adj: {self._adj}"