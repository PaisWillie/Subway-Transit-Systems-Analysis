from GraphModels import EdgeWeightedDigraph


class GraphMetricExtractor():
    _graph : EdgeWeightedDigraph

    def __init__(self, graph:EdgeWeightedDigraph) -> None:
        self._graph = graph

    def replaceGraph(self, graph:EdgeWeightedDigraph) -> None:
        self._graph = graph

    def getNodeNum(self) -> int:
        return self._graph.getNodeNum()

    def getEdgeNum(self) -> int:
        return self._graph.getEdgeNum()

    def getNodeAverageDegree(self) -> float:
        return self._graph.getEdgeNum() / self._graph.getNodeNum()
    
    def getNodeDegreeDistribution(self) -> dict[int, int]:
        result : dict[int, int] = {}
        adj = self._graph.getAdj()
        for node in adj:
            degree = len(adj[node])
            if degree in result:
                result[degree] += 1
            else:
                result[degree] = 1
        maxDegree = max(result.keys())
        for i in range(0, maxDegree +1):
            if i not in result:
                result[i] = 0
        return result