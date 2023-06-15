from typing import Tuple, Dict
import pytest
from ConnectedIslands import ConnectedIslands

from GraphParser import GraphParser
from shortest_paths.factory import ShortestPathFactory


@pytest.fixture
def one_station_island() -> Dict[str, int]:
    return [6]


@pytest.fixture
def two_station_island() -> Dict[str, int]:
    return [284, 7]




@pytest.fixture
def lots_station_island() -> Dict[str, int]:
    return [1, 2, 5, 9, 11, 12, 16, 22, 25, 26, 37, 40, 41, 49, 67, 68, 71, 72, 73, 75, 82, 85, 87, 89, 103, 107, 114, 126, 127, 129, 130, 132,
            136, 137, 140, 141, 142, 145, 146, 163, 166, 167, 171, 172, 181, 185, 194, 200, 205, 217, 219, 224, 227, 230, 240, 244, 246, 251, 291]


@pytest.fixture
def all_cases(one_station_island, two_station_island, some_station_island, lots_station_island):
    return [one_station_island, two_station_island, some_station_island, lots_station_island]


def is_connected(station_ids: list[int], solution: list[int]) -> bool:
    # Checks if items in both list are same, regardless of order
    return sorted(station_ids) == sorted(solution)


def test_connected_islands(all_cases):

    parser = GraphParser()
    graph = parser.parseGraph(
        "./_dataset/london.stations.csv", "./_dataset/london.connections.csv")

    connected_islands = ConnectedIslands(graph)

    for case in all_cases:
        station_ids = connected_islands.get_connected_islands(case[0])
        assert is_connected(station_ids, case)
