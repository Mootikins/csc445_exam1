import argparse
from typing import Any
import graphviz
import networkx as nx
from networkx.classes.digraph import DiGraph
from networkx.classes.graph import Graph


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s action file",
        description="Convert an NFA to a DFA, minimize a DFA, or both in"
        " sequence. Writes the output .dot file to 'grid.dot' and a PDF rendering"
        " to 'grid.dot.pdf'",
    )
    parser.add_argument(
        "action",
        help="convert an NFA to DFA, minimize a DFA, or both",
        choices=("convert", "minimize", "both"),
    )
    parser.add_argument("file")
    return parser


def attrs_to_lists(G: Graph, attr: str = "label", delim: str = ","):
    for (start, end, data) in G.edges(data=True):
        if data.get(attr) is not None:
            G[start][end][attr] = data.get(attr).split(delim)


def remove_inaccessible(G: Graph, initial: Any = "qi"):
    for node in sorted(G.nodes()):
        if node != initial:
            if not nx.has_path(G, initial, node):
                G.remove_node(node)


def output_graph(G: Graph):
    for (start, end, data) in G.edges(data=True):
        if data.get("label") is not None and type(data.get("label")) is list:
            G[start][end]["label"] = ",".join(data.get("label"))

    nx.drawing.nx_agraph.write_dot(G, "grid.dot")
    gv = graphviz.Source.from_file("grid.dot")
    graphviz.render("dot", "pdf", "grid.dot")


def convert(G: Graph):
    pass


def minimize(G: Graph):
    pass


def main():
    parser = make_parser()
    args = parser.parse_args()

    G = nx.DiGraph(nx.drawing.nx_agraph.read_dot(args.file))

    if args.action in ["convert", "both"]:
        convert(G)

    if args.action in ["minimize", "both"]:
        minimize(G)

    output_graph(G)


if __name__ == "__main__":
    main()
