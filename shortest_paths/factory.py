from shortest_paths.algorithms import A_Star, DijkstraAlgo
from shortest_paths.interface import ShortestPathStrategy


class ShortestPathFactory():

    @staticmethod
    def build(name: str) -> ShortestPathStrategy:
        if name == "DijkstraAlgo":
            return DijkstraAlgo()
        elif name == "A_Star":
            return A_Star()
        else:
            raise ValueError(name)
