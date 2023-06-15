from typing import Tuple, Dict
import pytest

from GraphParser import GraphParser
from Itinerary import Itinerary
from shortest_paths.factory import ShortestPathFactory


@pytest.fixture
def one_step() -> Dict[str, int]:
    return {
        "start": 1,
        "end": 73,
        "solution": [1, 73]
    }


@pytest.fixture
def two_step() -> Dict[str, int]:
    return {
        "start": 3,
        "end": 167,
        "solution": [3, 156, 167]
    }


@pytest.fixture
def same_step() -> Dict[str, int]:
    return {
        "start": 1,
        "end": 1,
        "solution": [1]
    }


@pytest.fixture
def long_step() -> Dict[str, int]:
    return {
        "start": 1,
        "end": 10,
        "solution": [1, 265, 110, 17, 74, 99, 236, 229, 273, 107, 192, 277, 89, 145, 123, 95, 10]
    }


@pytest.fixture
def all_cases(one_step, two_step, long_step, same_step):
    return [one_step, two_step, long_step, same_step]


def is_valid_path(path: list[int], solution: list[int]) -> bool:
    for i in range(len(path)):
        if path[i] != solution[i]:
            return False
    return True


@pytest.mark.parametrize("algorithm_name", ["DijkstraAlgo", "A_Star"])
def test_shortest_path(algorithm_name: str, all_cases):

    parser = GraphParser()
    graph = parser.parseGraph(
        "./_dataset/london.stations.csv", "./_dataset/london.connections.csv")

    algo = ShortestPathFactory.build(algorithm_name)

    mapping = graph.getMapping()
    nodeData = graph.getNodeData()

    for case in all_cases:
        itinerary = Itinerary(algo, case["start"], case["end"])
        result = itinerary.returnPath(graph, mapping, nodeData)
        assert is_valid_path(result, case["solution"])
