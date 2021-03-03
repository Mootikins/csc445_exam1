import graphviz
import networkx as nx

gv = graphviz.Source.from_file("nfa29.gv")
G = nx.DiGraph(nx.drawing.nx_agraph.read_dot("nfa29.gv"))

print(gv.source)
gv.view()

edge_labels = nx.get_edge_attributes(G, "label")
print(edge_labels)
