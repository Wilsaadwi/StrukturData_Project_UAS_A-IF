import networkx as nx

def calculate_centrality(graph):

    G = nx.DiGraph()

    for source in graph:
        for target, weight in graph[source].items():
            G.add_edge(
                source,
                target,
                weight=weight
            )

    return nx.degree_centrality(G)