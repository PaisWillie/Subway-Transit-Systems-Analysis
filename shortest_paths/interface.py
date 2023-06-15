from abc import ABC, abstractmethod
from typing import TypedDict

from GraphModels import EdgeWeightedDigraph

class ShortestPathResult(TypedDict):

    shortestPath: list[str]
    ops: int


class ShortestPathStrategy(ABC):

    _count: int

    def __call__(self, graph: EdgeWeightedDigraph, startNodeId: int, destinationNodeId: int, mapping, *args, **kwargs) -> ShortestPathResult:

        self._count = 0

        result: ShortestPathResult = {
            "shortestPath": self.returnPath(graph, startNodeId, destinationNodeId, mapping),
            "ops": self._count
        }
        return result

    def _incr(self) -> None:

        self._count += 1

    @abstractmethod
    def returnPath(self, G: EdgeWeightedDigraph, startNodeId: int, destinationNodeId: int, mapping):
        pass