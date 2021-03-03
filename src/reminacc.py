import graphviz
import networkx as nx

gv = graphviz.Source.from_file("dfa214.gv")
G = nx.DiGraph(nx.drawing.nx_agraph.read_dot("dfa214.gv"))

print(gv.source)

for i in sorted(G.nodes()):
    if i != "qi":
        print("qi -> " + i)
        print(nx.has_path(G, "qi", i))
        if nx.has_path(G, "qi", i) == False:
            G.remove_node(i)

nx.drawing.nx_agraph.write_dot(G, "grid.dot")

gv = graphviz.Source.from_file("grid.dot")
print(gv.source)
gv.view()
