import argparse
import graphviz
import networkx as nx
from networkx.classes.graph import Graph
from src import FiniteAutomata


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s action input_file [options]",
        description="Convert an NFA to a DFA, minimize a DFA, or both in"
        " sequence. Writes the output .dot file to 'out.dot' and a PDF rendering"
        " to 'out.pdf'",
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
        help="Output filename for intermediate .dot file and the PDF. Defaults to 'out.dot' and 'out.pdf'",
        default="out.dot",
    )
    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()

    G = nx.DiGraph(nx.drawing.nx_agraph.read_dot(args.input_file))
    fa = FiniteAutomata(G)

    if args.action in ["convert", "both"]:
        fa.to_dfa()

    if args.action in ["minimize", "both"]:
        fa.reduce()

    fa.output(args.output_file)


if __name__ == "__main__":
    main()
