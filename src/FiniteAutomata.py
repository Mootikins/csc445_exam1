from __future__ import annotations
from typing import Union, Tuple, Any, Set
import graphviz
import pygraphviz
import networkx as nx
from networkx.classes import DiGraph

Transition = dict[str, dict[str, set[str]]]


def attrs_to_lists(G: DiGraph, attr: str = "label", delim: str = ",") -> DiGraph:
    for (start, end, data) in G.edges(data=True):
        if type(data.get(attr)) is str:
            G[start][end][attr] = data.get(attr).split(delim)
    return G


class FiniteAutomata:
    Q: set[str] = set()
    sigma: set[str] = set()
    delta: Transition = {}
    initial: str = "qi"
    F: set[str] = set()

    def __init__(self, G: DiGraph = None):
        if G:
            attrs_to_lists(G)
            for node in sorted(G.nodes()):
                self.Q.add(node)

            for (start, end, labels) in G.edges.data("label", []):
                if not self.delta.get(start):
                    self.delta[start] = {}
                if not self.delta.get(end):
                    self.delta[end] = {}
                if start == "qi":
                    self.delta[start]["λ"] = set([end])
                for label in labels:
                    self.sigma.add(label)
                    if not self.delta[start].get(label):
                        self.delta[start][label] = set()
                    self.delta[start][label].add(end)

            self.update_finals()

    def update_finals(self):
        for node in self.Q:
            self_looping = 0
            for alpha in self.delta[node]:
                if node in self.delta[node][alpha]:
                    print(node, "is self looping via", alpha)
                    self_looping += 1
            if self_looping == len(self.sigma):
                print(node, "should be final")
                self.F.add(node)

    def output(self, filename: str = None):
        G = DiGraph()
        for label in self.Q:
            G.add_node(label)

        for start in self.delta.keys():
            for alpha in self.delta[start]:
                for end in self.delta[start][alpha]:
                    G.add_edge(start, end)
                    if not G.edges[start, end].get("label"):
                        G.edges[start, end]["label"] = set()
                    G.edges[start, end]["label"].add(alpha)

        for (start, end, label) in G.edges.data("label"):
            if type(label) is set:
                G[start][end]["label"] = ",".join(list(label))
            if start == "qi":
                G[start][end]["label"] = ""
                G[start][end]["shape"] = "point"

        nx.drawing.nx_agraph.write_dot(G, filename)

        gv = pygraphviz.AGraph(
            filename, directed=True, strict=False, rankdir="LR", size="8,5"
        )
        gv.node_attr["shape"] = "circle"
        initial = gv.get_node(self.initial)
        initial.attr["shape"] = "point"

        for node in self.F:
            final = gv.get_node(node)
            final.attr["shape"] = "doublecircle"

        gv.write(filename)
        gv.draw(filename.split(".")[0] + ".pdf", prog="dot")

    def to_dfa(self):
        pass

    def mark(self):
        pass

    def reduce(self):
        pass

    def __str__(self):
        return f"States: {self.Q}\nAlphabet: {self.sigma}\nTransition: {self.delta}\nFinal State: {self.F}"
