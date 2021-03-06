from __future__ import annotations

import copy
from typing import Union
import yaml

import networkx as nx
import pygraphviz
from networkx.classes import DiGraph

State = tuple[str, ...]
Transition = dict[State, dict[str, set[State]]]


def attrs_to_lists(G: DiGraph, attr: str = "label", delim: str = ",") -> DiGraph:
    for (start, end, data) in G.edges(data=True):
        if type(data.get(attr)) is str:
            G[start][end][attr] = data.get(attr).split(delim)
    return G


class FiniteAutomata:
    def __init__(self, G: DiGraph = None, initial: State = tuple(["qi"])):
        self.Q: set[State] = set()
        self.sigma: set[str] = set()
        self.delta: Transition = {}
        self.initial: State = initial
        self.F: set[State] = set()

        if G:
            attrs_to_lists(G)
            for node in sorted(G.nodes()):
                self.Q.add(tuple([node]))
                self.delta[tuple([node])] = {}

            for (_, _, labels) in G.edges.data("label", []):
                for node in self.Q:
                    for label in labels:
                        self.delta[node][label] = set()

            for (start, end, labels) in G.edges.data("label", []):
                if start == "qi":
                    self.delta[tuple([start])]["λ"].add(tuple([end]))
                for label in labels:
                    self.sigma.add(label)
                    self.delta[tuple([start])][label].add(tuple([end]))

            self.update_finals()

    def __str__(self):
        return f"States: {self.Q}\nAlphabet: {self.sigma}\nTransition: {self.delta}\nFinal State: {self.F}\nInitial State: {self.initial}"

    def update_finals(self):
        for node in self.Q:
            self_looping = 0
            for alpha in self.delta[node]:
                if node in self.delta[node][alpha]:
                    self_looping += 1
            if self_looping == len(self.sigma):
                self.F.add(node)

    def output(self, filename: str = None):
        G = DiGraph()
        self.update_finals()
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
        gv.draw("".join(filename.split(".")[:-1]) + ".pdf", prog="dot")

    def delta_star(self, state: State, alpha: str) -> set[State] | None:
        pass

    def to_dfa(self):
        pass

    def mark(self):
        pass

    def reduce(self):
        pass
