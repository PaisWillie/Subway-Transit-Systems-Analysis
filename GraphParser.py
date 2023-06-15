# from GraphModels import Graph, Node, Edge 
import csv
from GraphModels import Node, DirectedEdge, EdgeWeightedDigraph
from Patrol import getPatrolPath
from Itinerary import Itinerary
from shortest_paths.algorithms import A_Star, DijkstraAlgo
import random

class GraphParser:
    
    def __init__(self):
        pass

    def parseNode(self, csvPath : str) -> tuple[dict[str, int], list[Node]]:
        nodes = []
        with open(csvPath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            read_header = False
            counter = 0
            headers = []
            station_node_mapping : dict[str, int] = {}
            for row in reader:
                if not read_header:
                    headers = row
                    read_header = True
                    continue

                result = {}
                for i in range(len(headers)):
                    result[headers[i]] = row[i]
                nodes.append(Node(id = counter, data = result))
                station_node_mapping[result['id']] = counter
                counter += 1
        return station_node_mapping, nodes

    def parseEdges(self, csvPath: str, mapping: dict[str, int]) -> None:
        edges = []
        with open(csvPath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            headersList = next(reader)
            headers = {}
            for index, header in enumerate(headersList):
                headers[header] = index
            for row in reader:
                # fromNodeId, toNodeId, line, weight = row
                line       = row[headers['line']]
                weight     = row[headers['time']]
                toNodeId   = mapping[row[headers['station2']]]
                fromNodeId = mapping[row[headers['station1']]]
                edges.append(DirectedEdge(fromNodeId=fromNodeId, toNodeId=toNodeId, weight=weight, line=line))
                edges.append(DirectedEdge(fromNodeId=toNodeId, toNodeId=fromNodeId, weight=weight, line=line))
        return edges

    def parseGraph(self, nodeCSVPath: str, edgeCSVPath: str) -> EdgeWeightedDigraph:

        mapping, nodes = self.parseNode(nodeCSVPath)
        stationData = {}
        for node in nodes:
            stationData[node.getId()] = node._data
        
        graph = EdgeWeightedDigraph(len(nodes))

        edges = self.parseEdges(edgeCSVPath, mapping)
        graph.addNodes(nodes)
        for edge in edges:
            graph.add_edge(edge)
        graph.addMapping(mapping)
        return graph


if __name__ == "__main__":
    parser = GraphParser()
    graph = parser.parseGraph("./_dataset/london.stations.csv", "./_dataset/london.connections.csv")
    
    matrix  = graph.adj_matrix()
    mapping = graph.getMapping()

    stations = random.sample([graph.getNodeData()[x]['id'] for x in graph.getNodeIds()], 10)
    print(stations)
    result = getPatrolPath(graph, stations)
    print(result)
