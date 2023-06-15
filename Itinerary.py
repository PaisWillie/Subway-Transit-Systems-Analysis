from typing import Optional
from GraphModels import EdgeWeightedDigraph
from shortest_paths.interface import ShortestPathStrategy


class Itinerary():

    startNodeId: int
    destinationNodeId: int
    _strategy: ShortestPathStrategy

    def __init__(self, strategy: ShortestPathStrategy, startNodeId: int, destinationNodeId: int) -> None:
        self._strategy = strategy
        self.startNodeId = startNodeId
        self.destinationNodeId = destinationNodeId

    @property
    def strategy(self) -> ShortestPathStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ShortestPathStrategy) -> None:
        self._strategy = strategy

    def returnPath(self, G: EdgeWeightedDigraph, mapping: dict[str, int], nodeData: Optional[dict[str, dict]] = None, *args, **kwargs) -> list[int]:
        startNodeId = mapping[str(self.startNodeId)]
        destinationNodeId = mapping[str(self.destinationNodeId)]
        data = self._strategy(
            G, startNodeId, destinationNodeId, nodeData, mapping)
        return {
            'shortestPath': [int(nodeData[x]['id']) for x in data['shortestPath']],
            'ops': data['ops']
        }
