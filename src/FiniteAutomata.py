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

            self.Q.remove(("qi",))
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

    def delta_star(self, state: State, alpha: str) -> set[str]:
        new_st: set[str] = set()
        if self.delta.get(state) and self.delta[state].get(alpha):
            for inner_st in self.delta[state][alpha]:
                if type(inner_st) is str:
                    new_st.add(inner_st)
                else:
                    for tup_st in inner_st:
                        new_st.add(tup_st)
                if self.delta[inner_st].get("λ"):
                    for lambda_st in self.delta[inner_st]["λ"]:
                        new_st = new_st.union(self.delta_star(lambda_st, alpha))
        if self.delta.get(state) and self.delta[state].get("λ"):
            for inner_st in self.delta[state]["λ"]:
                new_st = new_st.union(self.delta_star(inner_st, alpha))

        return new_st

    # I am aware it's not perfect but I have literally zero clue what is wrong
    def to_dfa(self):
        new = FiniteAutomata()
        new.Q.add(list(self.delta[self.initial]["λ"])[0])
        new.sigma = self.sigma
        new.sigma.remove("λ")

        added = True
        while added:
            added = False
            for state in new.Q.copy():
                if not new.delta.get(state):
                    new.delta[state] = {}
                for alpha in new.sigma:
                    if not new.delta[state].get(alpha):
                        new_st: State = tuple(self.delta_star(state, alpha))
                        new.delta[state][alpha] = set([new_st])
                        new.Q.add(new_st)
                        added = True

        new.delta[self.initial] = {}
        new.delta[self.initial]["λ"] = self.delta[self.initial]["λ"]
        self.delta = new.delta
        self.update_finals()

    def mark(self):
        for state in self.delta.keys():
            for trans in self.delta[state].keys():
                pass

    def reduce(self):
        pass
