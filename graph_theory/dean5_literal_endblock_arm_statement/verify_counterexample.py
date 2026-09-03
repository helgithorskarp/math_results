#!/usr/bin/env python3
"""Check the bridge counterexample to Lemma 7.2 of the Dean k=5 v1.0.1 claim."""

from collections import deque


def reachable(adjacency, start, deleted_vertex=None, deleted_edge=None):
    seen = set()
    if start == deleted_vertex:
        return seen
    queue = deque([start])
    seen.add(start)
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacency.get(vertex, set()):
            if neighbor == deleted_vertex:
                continue
            if deleted_edge is not None and frozenset((vertex, neighbor)) == deleted_edge:
                continue
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return seen


def main():
    # Y is the path u-z-t.  The ambient edge p-u supplies the prefix required
    # by the lemma but is not an edge of Y or B.
    y = {
        "u": {"z"},
        "z": {"u", "t"},
        "t": {"z"},
    }
    b = {
        "u": {"z"},
        "z": {"u"},
    }
    ambient = {**y, "p": {"u"}}
    ambient["u"] = set(ambient["u"]) | {"p"}

    assert reachable(y, "u") == set(y), "Y must be connected"
    assert reachable(y, "u", deleted_vertex="z") == {"u"}, "z must cut Y"
    assert reachable(y, "u", deleted_edge=frozenset(("u", "z"))) == {"u"}
    assert "p" not in y and "u" in ambient["p"], "p-u must be an ambient prefix edge"

    roots = {"u", "z"}
    nonroots = set(b) - roots
    assert not nonroots, "the degree premise in part (a) must be vacuous"

    rooted_reach = reachable(b, "u", deleted_edge=frozenset(("u", "z")))
    rooted_path_count = int("z" in rooted_reach)
    assert rooted_path_count == 0
    print("PASS: part (a) has 0 rooted paths although its premise is vacuous")


if __name__ == "__main__":
    main()
