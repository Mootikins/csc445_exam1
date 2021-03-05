from __future__ import annotations
from typing import Union, Tuple, Any
import networkx as nx
from networkx.classes import Graph

Transition = dict[str, dict[str, list[Union[str, Tuple[str, ...]]]]]


def remove_inaccessible(G: Graph, initial: Any = "qi"):
    for node in sorted(G.nodes()):
        if node != initial:
            if not nx.has_path(G, initial, node):
                G.remove_node(node)
    return G


class FiniteAutomata:
    Q: list[str] = []
    sigma: list[str] = []
    delta: Transition = {}

    def __init__(self, G: Graph = None):
        if not G:
            return self

    def to_nfa(self) -> FiniteAutomata:
        prime = FiniteAutomata()
        return prime

    def mark(self):
        pass

    def reduce():
        pass
