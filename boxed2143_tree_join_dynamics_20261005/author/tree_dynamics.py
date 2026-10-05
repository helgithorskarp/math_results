#!/usr/bin/env python3
"""Exact maximum-Cartesian-tree state; empty tree (), node (left,right)."""

from __future__ import annotations

from functools import lru_cache

from kernel import Blocker, validate_permutation


Tree = tuple


@lru_cache(maxsize=None)
def size(tree: Tree) -> int:
    return 0 if tree == () else 1 + size(tree[0]) + size(tree[1])


def cartesian_shape(values) -> Tree:
    p = validate_permutation(values)

    def build(entries: tuple[int, ...]) -> Tree:
        if not entries:
            return ()
        root = entries.index(max(entries))
        return build(entries[:root]), build(entries[root + 1:])

    return build(p)


def shape_blockers(tree: Tree) -> tuple[Blocker, ...]:
    """Right-child roots with an ancestor on their right are eligible."""
    answer: list[Blocker] = []

    def visit(node, offset, parent, direction, upper_right):
        if node == ():
            return
        left, right = node
        root = offset + size(left)
        if direction == "right" and upper_right is not None:
            answer.append(Blocker(parent, root, upper_right))
        visit(left, offset, root, "left", root)
        visit(right, root + 1, root, "right", upper_right)

    visit(tree, 0, None, None, None)
    return tuple(sorted(answer, key=lambda b: b.minimum))


def shape_legal_gaps(tree: Tree) -> tuple[int, ...]:
    n = size(tree)
    difference = [0] * (n + 2)
    for b in shape_blockers(tree):
        difference[b.first_gap] += 1
        difference[b.last_gap + 1] -= 1
    active = 0
    answer = []
    for gap in range(n + 1):
        active += difference[gap]
        if active == 0:
            answer.append(gap)
    return tuple(answer)


def split(tree: Tree, gap: int) -> tuple[Tree, Tree]:
    if type(gap) is not int or not 0 <= gap <= size(tree):
        raise ValueError("gap must be an integer between 0 and tree size")
    if tree == ():
        return (), ()
    left, right = tree
    k = size(left)
    if gap <= k:
        prefix, remainder = split(left, gap)
        return prefix, (remainder, right)
    remainder, suffix = split(right, gap - k - 1)
    return (left, remainder), suffix


def insert_maximum_shape(tree: Tree, gap: int) -> Tree:
    return split(tree, gap)


def tree_word(tree: Tree) -> str:
    if tree == ():
        return "."
    return "(" + tree_word(tree[0]) + tree_word(tree[1]) + ")"


def clear_caches() -> None:
    size.cache_clear()
