import heapq
import math
from typing import Optional
from GraphModels import DirectedEdge, EdgeWeightedDigraph
from shortest_paths.interface import ShortestPathStrategy


class DijkstraAlgo(ShortestPathStrategy):
    def returnPath(self, G: EdgeWeightedDigraph, startNodeId: int, destinationNodeId: int, nodeData: Optional[dict[int, dict]] = None, *args, **kwargs) -> list[int]:
        _edgeTo: list[DirectedEdge] = [None for _ in range(G.V())]
        _distTo: list[float] = [float("inf") for _ in range(G.V())]
        _lineChangesTo: list[int] = [0 for _ in range(G.V())]
        _pq: list[DirectedEdge] = []

        def relax(e: DirectedEdge):

            self._incr()

            v = e.fromNodeId()
            w = e.toNodeId()

            # If the line changes, add 1 to the line changes
            newLineChangesTo: int = _lineChangesTo[v] + 1 if _edgeTo[w] and _edgeTo[w].isLineChange(
                e.getLine()) else _lineChangesTo[v]
            if _distTo[w] == _distTo[v] + e.weight():
                if _lineChangesTo[w] > newLineChangesTo:
                    _lineChangesTo[w] = newLineChangesTo
                    _edgeTo[w] = e
            if _distTo[w] > _distTo[v] + e.weight():
                _distTo[w] = _distTo[v] + e.weight()
                _edgeTo[w] = e
                _lineChangesTo[w] = newLineChangesTo
                heapq.heappush(_pq, (_distTo[w], w))

        # from pprint import pprint
        # pprint(mapping)

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

        return path[::-1]


class A_Star(ShortestPathStrategy):
    def returnPath(self, G: EdgeWeightedDigraph, startNodeId: int, destinationNodeId: int, nodeData: Optional[dict[int, dict]] = None, *args, **kwargs) -> list[int]:

        cameFrom: dict[int, int] = {}
        gScore: dict[str, float] = {}
        fScore: dict[str, float] = {}
        openNodes: list[tuple[int, str]] = []
        visited: set[int] = set()

        destinationNodeData: dict = nodeData[destinationNodeId]

        def h(currentNodeId: int) -> int:
            currentNodeData = nodeData[currentNodeId]
            return round(math.sqrt(
                (float(currentNodeData['latitude']) - float(destinationNodeData['latitude'])) ** 2 +
                (float(currentNodeData['longitude']) -
                 float(destinationNodeData['longitude'])) ** 2
            ) * 10000
            )

        def backTrack(cameFrom: dict, current: int) -> list[int]:
            path = []
            while current in cameFrom.keys():
                current = cameFrom[current]
                path.append(current)
            return [int(x) for x in path]

        heapq.heappush(openNodes, (h(startNodeId), startNodeId))

        # Init every scores to infinites
        for nodeId in G.getNodeIds():
            gScore[nodeId] = float("inf")
            fScore[nodeId] = float("inf")
        gScore[startNodeId] = 0

        # while the openNodes is not empty
        while len(openNodes) != 0:
            _, currentNodeId = heapq.heappop(openNodes)
            # if the current Node is the destination Node, return the path from current to the start
            if int(currentNodeId) == destinationNodeId:
                tempList: list[int] = backTrack(cameFrom, currentNodeId)
                tempList = tempList[::-1]
                tempList.append(destinationNodeId)
                return tempList

            visited.add(currentNodeId)

            # For every neighboring edges
            for edge in G.adj(int(currentNodeId)):
                neighborId = edge.toNodeId()

                # G_score of neighbor = g_score of current node + weight of the path between current and neighbors
                temp_gScore = gScore[int(currentNodeId)] + edge.weight()
                # If the g_score of neighbor is less then the previous g_score caluclated
                if temp_gScore < gScore[neighborId]:
                    # set neighbor cameFrom nearest Path to current
                    cameFrom[neighborId] = int(currentNodeId)
                    # reset g_score of neighbor to calculated g_score
                    gScore[neighborId] = temp_gScore
                    # reset f_score of neighbor to calculated g_score
                    fScore[neighborId] = temp_gScore + h(neighborId)

                    if neighborId not in visited:
                        self._incr()
                        neighborTuple = (fScore[neighborId], neighborId)
                        heapq.heappush(openNodes, neighborTuple)

        return []
