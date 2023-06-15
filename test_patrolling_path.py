from typing import Tuple, Dict
import pytest
from ConnectedIslands import ConnectedIslands

from GraphParser import GraphParser
from shortest_paths.factory import ShortestPathFactory


parser = GraphParser()
graph = parser.parseGraph("./_dataset/london.stations.csv", "./_dataset/london.connections.csv")

matrix  = graph.adj_matrix()
mapping = graph.getMapping()

@pytest.fixture
def case1() -> Dict[str, int]:
    #['264', '52', '280', '88', '24', '66', '225', '144', '98', '53']
    return [264, 144, 280, 53, 52, 225, 24, 66, 98, 88]

@pytest.fixture
def case2() -> Dict[str, int]:
    # ['240', '219', '119', '21', '2', '221', '5', '92', '181', '300']
    return [240, 219, 21, 2, 92, 119, 300, 5, 181, 221]

@pytest.fixture
def case3() -> Dict[str, int]:
    # ['243', '87', '71', '230', '82', '202', '69', '249', '92', '138']
    return [243, 202, 71, 249, 82, 138, 87, 92, 230, 69]

@pytest.fixture
def all_cases(case1, case2, case3):
    return [case1, case2, case3]
