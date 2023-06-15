from GraphModels import EdgeWeightedDigraph
from itertools import permutations
from GraphModels import DirectedEdge, EdgeWeightedDigraph
import heapq

def getPatrolPath(G: EdgeWeightedDigraph, stations: list[int]) -> list[int]:
    def returnDistTo(G: EdgeWeightedDigraph, startNodeId: int, destinationNodeId: int) -> list[float]:
        _edgeTo: list[DirectedEdge] = [None for _ in range(G.V())]
        _distTo: list[float] = [float("inf") for _ in range(G.V())]
        _lineChangesTo: list[int] = [0 for _ in range(G.V())]
        _pq: list[DirectedEdge] = []
        
        def relax(e: DirectedEdge):
            v = e.fromNodeId()
            w = e.toNodeId()

            # If the line changes, add 1 to the line changes
            newLineChangesTo: int = _lineChangesTo[v] + 1 if _edgeTo[w] and _edgeTo[w].isLineChange(e.getLine()) else _lineChangesTo[v]
            if _distTo[w] == _distTo[v] + e.weight():
                if _lineChangesTo[w] > newLineChangesTo:
                    _lineChangesTo[w] = newLineChangesTo
                    _edgeTo[w] = e
            if _distTo[w] > _distTo[v] + e.weight():
                _distTo[w] = _distTo[v] + e.weight()
                _edgeTo[w] = e
                _lineChangesTo[w] = newLineChangesTo
                heapq.heappush(_pq, (_distTo[w], w))

        for node_id in G.getNodeIds():
            _distTo[node_id] = float("inf")
            _edgeTo[node_id] = None
        _distTo[startNodeId] = 0.0

        heapq.heappush(_pq, (0.0, startNodeId))

        while _pq:
            _, v = heapq.heappop(_pq)
            for e in G.adj(v):
                relax(e)

        path = []
        while destinationNodeId is not None:
            path.append(destinationNodeId)
            if not _edgeTo[destinationNodeId]:
                break
            destinationNodeId = _edgeTo[destinationNodeId].fromNodeId()
                    
        return path[::-1], _distTo
    stations = [G.getMapping()[str(i)] for i in stations]

    distTo : dict[list[float]] = {}
    for node in stations:
        distTo[node] = returnDistTo(G, node, -1)[1]

    s : int = stations[0]
    min_cost = float("inf")
    shortest_tour : list[int] = []

    next_permutation = permutations(stations)
    for possible_path in next_permutation:
        current_pathweight = 0
        current_path : list[int] = []
        currentNode = s
        for node in possible_path:
            if distTo[currentNode][node] != float("inf"):
                current_pathweight += distTo[currentNode][node]
                current_path.append(node)
                currentNode = node
            else:
                current_path = []
        if min_cost > current_pathweight and set(stations).issubset(set(current_path)):
            min_cost = min(min_cost, current_pathweight)
            shortest_tour = current_path
    return [int(G.getNodeData()[i]['id']) for i in shortest_tour]