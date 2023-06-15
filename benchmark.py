import pyperf
import random

from GraphParser import GraphParser
from shortest_paths.factory import ShortestPathFactory
from GraphModels import EdgeWeightedDigraph
from ConnectedIslands import ConnectedIslands


def do_shortest_path_bench(runner, algorithms: list[str], G: EdgeWeightedDigraph, nodeData: dict[int, dict]):
    startNodeId = random.choice(list(G.getNodeIds()))
    destinationNodeId = random.choice(list(G.getNodeIds()))

    for algorithm in algorithms:
        shortestPathStrategy = ShortestPathFactory.build(algorithm)
        runner.bench_func(algorithm, shortestPathStrategy.returnPath,
                          G, startNodeId, destinationNodeId, nodeData)


def benchmark_connected_islands(graph: EdgeWeightedDigraph):
    ConnectedIslands(graph)


def do_connected_islands_bench(runner, algorithms: list[str], G: EdgeWeightedDigraph):
    runner.bench_func("ConnectedIslands", benchmark_connected_islands, G)


def main():
    random.seed(1659644754)
    algorithms = ["DijkstraAlgo", "A_Star"]
    parser = GraphParser()
    graph = parser.parseGraph(
        "./_dataset/london.stations.csv", "./_dataset/london.connections.csv")
    nodeData = graph.getNodeData()
    
    runner = pyperf.Runner()

    do_shortest_path_bench(runner, algorithms, graph, nodeData)
    do_connected_islands_bench(runner, algorithms, graph)


if __name__ == "__main__":
    main()
