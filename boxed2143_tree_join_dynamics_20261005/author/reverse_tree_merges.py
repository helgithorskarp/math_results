#!/usr/bin/env python3
"""Reverse maximum insertion via the two boundary spines; author mechanism."""
from __future__ import annotations

from functools import lru_cache

from tree_dynamics import size


def boundary_merges(left, right, admissible_only=True):
    """Yield(parent_shape, descending_priority_word); no LL after the first R."""
    def build(l, r, seen_r, last_l):
        if l == () and r == ():
            yield (), ""
            return
        if l != () and (not admissible_only or not (seen_r and last_l)):
            for remainder, suffix in build(l[1], r, seen_r, True):
                yield (l[0], remainder), "L" + suffix
        if r != ():
            for remainder, suffix in build(l, r[0], True, False):
                yield (remainder, r[1]), "R" + suffix

    yield from build(left, right, False, False)


def word_legal(word):
    seen_r = False
    previous = None
    for letter in word:
        if letter not in ("L", "R"):
            raise ValueError("merge words contain only L,R")
        if letter == "L" and previous == "L" and seen_r:
            return False
        seen_r = seen_r or letter == "R"
        previous = letter
    return True


def perfect_tree(height):
    if type(height) is not int or height < 0:
        raise ValueError("height must be a nonnegative integer")
    if height == 0:
        return ()
    child = perfect_tree(height - 1)
    return child, child


class StateCapExceeded(RuntimeError):
    pass


class ReverseWeights:
    def __init__(self, cap=200000):
        self.cap = cap
        self.states = set()
        self.transitions = 0
        self.weight = lru_cache(maxsize=None)(self._weight)

    def _weight(self, tree):
        self.states.add(tree)
        if len(self.states) > self.cap:
            raise StateCapExceeded("reverse-state budget exceeded; no count certified")
        if tree == ():
            return 1
        total = 0
        for parent, _word in boundary_merges(tree[0], tree[1]):
            self.transitions += 1
            total += self.weight(parent)
        return total
