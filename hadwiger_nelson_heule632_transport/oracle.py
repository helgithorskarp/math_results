"""Exact four-colour list extension on a forest with at most one cycle.

lists[v] is an integer mask 0..15. Omitted keys denote deleted vertices;
zero denotes a retained vertex with an empty list. No solver is used.
"""


def require(ok, message):
    if not ok:
        raise ValueError(message)


def colours(mask):
    return [c for c in range(4) if mask & (1 << c)]


def forest(adjacency, lists):
    """Return a proper list-colouring or None; reject a retained cycle."""
    parent = {}
    order = []
    for root in sorted(lists):
        if root in parent:
            continue
        parent[root] = None
        stack = [root]
        while stack:
            v = stack.pop()
            order.append(v)
            for w in sorted(adjacency[v], reverse=True):
                if w not in lists or w == parent[v]:
                    continue
                require(w not in parent, 'residual graph must be a forest')
                parent[w] = v
                stack.append(w)
    possible = dict(lists)
    for v in reversed(order):
        p = parent[v]
        if p is not None:
            possible[p] &= sum(1 << c for c in colours(possible[p]) if possible[v] & ~(1 << c))
    if any(possible[v] == 0 for v in lists if parent[v] is None):
        return None
    answer = {}
    for v in order:
        available = possible[v]
        if parent[v] is not None:
            available &= ~(1 << answer[parent[v]])
        require(available != 0, 'subtree reconstruction')
        answer[v] = colours(available)[0]
    return answer


def extend(adjacency, lists, cycle=()):
    require(set(lists) <= set(adjacency), 'selected vertices')
    require(all(type(mask) is int and 0 <= mask <= 15 for mask in lists.values()), 'list masks')
    # Validate the forest structure even when an empty list is present.
    if cycle and all(v in lists for v in cycle):
        pivot = min(cycle)
        tail = {v: mask for v, mask in lists.items() if v != pivot}
        # A call with unrestricted lists verifies the promised deletion forest.
        forest(adjacency, {v: 15 for v in tail})
        for c in colours(lists[pivot]):
            restricted = {v: mask & ~(1 << c) if v in adjacency[pivot] else mask for v, mask in tail.items()}
            answer = forest(adjacency, restricted)
            if answer is not None:
                answer[pivot] = c
                return answer
        return None
    return forest(adjacency, lists)


def graph(vertices, edges):
    adjacency = {v: set() for v in vertices}
    require(len(adjacency) == len(vertices), 'unique graph labels')
    seen = set()
    for u, v in edges:
        require(u in adjacency and v in adjacency and u != v, 'edge domain')
        edge = tuple(sorted((u, v)))
        require(edge not in seen, 'duplicate edge')
        seen.add(edge)
        adjacency[u].add(v)
        adjacency[v].add(u)
    return adjacency


def check_answer(adjacency, lists, answer):
    require(answer is not None and set(answer) == set(lists), 'complete selected colouring')
    require(all(type(c) is int and 0 <= c < 4 and lists[v] & (1 << c) for v, c in answer.items()), 'list membership')
    for u in answer:
        for v in adjacency[u]:
            if v in answer:
                require(answer[u] != answer[v], 'list edge inequality')
