import argparse
import graphviz
import networkx as nx
from networkx.classes.graph import Graph
from src import FiniteAutomata


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s action input_file [options]",
        description="Convert an NFA to a DFA, minimize a DFA, or both in"
        " sequence. Writes the output .dot file to 'grid.dot' and a PDF rendering"
        " to 'grid.dot.pdf'",
    )
    parser.add_argument(
        "action",
        help="convert an NFA to DFA, minimize a DFA, or both",
        choices=("convert", "minimize", "both"),
    )
    parser.add_argument("input_file", help="Input filename in graphviz .gv format")
    parser.add_argument(
        "-o",
        "--output_file",
        help="Output filename for intermediate .dot file and the PDF. Defaults to 'grid.dot' and 'grid.dot.pdf'",
        default="grid.dot",
    )
    return parser


def attrs_to_lists(G: Graph, attr: str = "label", delim: str = ",") -> Graph:
    for (start, end, data) in G.edges(data=True):
        if type(data.get(attr)) is str:
            G[start][end][attr] = data.get(attr).split(delim)
    return G


def output_graph(G: Graph, output: str):
    for (start, end, data) in G.edges(data=True):
        if data.get("label") is not None and type(data.get("label")) is list:
            G[start][end]["label"] = ",".join(data.get("label"))

    nx.drawing.nx_agraph.write_dot(G, output)
    graphviz.render("dot", "pdf", output)


def main():
    parser = make_parser()
    args = parser.parse_args()

    G = nx.DiGraph(nx.drawing.nx_agraph.read_dot(args.input_file))
    G = attrs_to_lists(G)
    fa = FiniteAutomata(G)

    if args.action in ["convert", "both"]:
        fa = fa.to_nfa()

    if args.action in ["minimize", "both"]:
        fa = fa.reduce()

    G = fa.to_graph()
    output_graph(G, args.output_file)


if __name__ == "__main__":
    main()
