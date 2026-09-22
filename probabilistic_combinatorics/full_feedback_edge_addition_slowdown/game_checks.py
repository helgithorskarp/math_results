"""Exact game semantics. Basic graph routines adapted from the prior campaign checker.

The new policy replay enumerates literal legal robber moves independently of
its closed-neighborhood policy construction. No asymptotic inference is made.
"""
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def graph(n, edges):
    require(type(n) is int and n > 0, "positive integer order required")
    adj = [set() for _ in range(n)]
    for a, b in edges:
        require(type(a) is int and type(b) is int, "integer vertex required")
        require(0 <= a < n and 0 <= b < n and a != b, "invalid edge")
        require(b not in adj[a], "duplicate edge")
        adj[a].add(b)
        adj[b].add(a)
    return tuple(frozenset(a) for a in adj)


def distances(adj):
    n = len(adj)
    answer = []
    for root in range(n):
        d = [-1] * n
        d[root] = 0
        todo = deque([root])
        while todo:
            a = todo.popleft()
            for b in adj[a]:
                if d[b] == -1:
                    d[b] = d[a] + 1
                    todo.append(b)
        if -1 in d:
            return None
        answer.append(d)
    return answer


def responses(adj, dist):
    return tuple(tuple(frozenset({w}) if x == w else
                       frozenset(b for b in adj[w]
                                 if dist[b][x] + 1 == dist[w][x])
                       for x in range(len(adj))) for w in range(len(adj)))


def first_step_responses(adj):
    """Independent breadth-first propagation of first-step labels."""
    rows = []
    for w in range(len(adj)):
        layers = {w}
        visited = {w}
        codes = [set() for _ in adj]
        codes[w] = {w}
        for b in adj[w]:
            codes[b].add(b)
        while layers:
            nxt = set().union(*(adj[a] for a in layers)) - visited
            if w not in layers:
                for x in nxt:
                    codes[x] = set().union(*(codes[a] for a in layers
                                            if x in adj[a]))
            visited |= nxt
            layers = nxt
        rows.append(tuple(frozenset(c) for c in codes))
    return tuple(rows)


def closed(adj, vertices):
    return frozenset(vertices).union(*(adj[x] for x in vertices))


def partitions(row, vertices):
    groups = {}
    for x in vertices:
        groups.setdefault(row[x], set()).add(x)
    return tuple(frozenset(g) for g in groups.values())


def adaptive_rounds(adj, resp):
    """Exact information-set fixed point; None means one cop never wins."""
    n = len(adj)
    sets = [frozenset(x for x in range(n) if mask >> x & 1)
            for mask in range(1 << n)]
    wins = {s for s in sets if len(s) <= 1}
    all_vertices = sets[-1]
    if all_vertices in wins:
        return 0
    for rounds in range(1, 1 << n):
        new = {s for s in sets if s not in wins and any(
            all(len(u) <= 1 or closed(adj, u) in wins
                for u in partitions(resp[w], s)) for w in range(n))}
        if all_vertices in new:
            return rounds
        if not new:
            return None
        wins |= new
    raise ValueError("finite fixed point did not stabilize")


def make_policy(adj, resp, first, alternatives):
    policy = {}
    for group in partitions(resp[first], range(len(adj))):
        response = resp[first][min(group)]
        if len(group) == 1:
            policy[response] = None
            continue
        territory = closed(adj, group)
        for second in alternatives:
            if len({resp[second][x] for x in territory}) == len(territory):
                policy[response] = second
                break
        else:
            return None
    return policy


def replay_policy(adj, resp, first, policy):
    require(policy is not None, 'missing policy')
    histories = {}
    for initial in range(len(adj)):
        answer = resp[first][initial]
        require(answer in policy, 'first response omitted')
        second = policy[answer]
        if second is None:
            require(sum(x == answer for x in resp[first]) == 1, 'premature capture')
            continue
        require(type(second) is int and 0 <= second < len(adj), 'invalid second probe')
        for current in adj[initial] | {initial}:
            history = (answer, resp[second][current])
            histories.setdefault(history, set()).add(current)
    require(all(len(s) == 1 for s in histories.values()), 'policy leaves two current positions')
    return len(histories)


def run():
    counts, histogram, digest = Counter(), Counter(), sha256()
    for n in range(1, 6):
        possible = list(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            counts['graphs'] += 1
            adj = graph(n, [e for i, e in enumerate(possible) if mask >> i & 1])
            dist = distances(adj)
            if dist is None:
                continue
            counts['connected_graphs'] += 1
            resp = responses(adj, dist)
            require(resp == first_step_responses(adj), 'response algorithms disagree')
            counts['response_entries'] += n * n
            time = adaptive_rounds(adj, resp)
            histogram[str(time)] += 1
            successes = []
            for first in range(n):
                policy = make_policy(adj, resp, first, range(n))
                if policy is not None:
                    counts['full_menu_policies'] += 1
                    counts['full_menu_histories'] += replay_policy(adj, resp, first, policy)
                    successes.append(first)
                for menu in combinations([x for x in range(n) if x != first], 2):
                    counts['two_alternative_menus'] += 1
                    policy = make_policy(adj, resp, first, menu)
                    if policy is not None:
                        counts['successful_two_alternative_menus'] += 1
                        counts['two_alternative_histories'] += replay_policy(adj, resp, first, policy)
            require(bool(successes) == (time is not None and time <= 2),
                    'two-round policies disagree with adaptive fixed point')
            digest.update(json.dumps([n, mask, time, successes], separators=(',', ':')).encode() + b'\n')
    # A known elementary nonmonotonicity example; not a novelty claim.
    path = graph(5, [(0, 1), (1, 2), (2, 3), (3, 4)])
    cycle = graph(5, [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)])
    controls = [adaptive_rounds(a, responses(a, distances(a))) for a in (path, cycle)]
    require(controls == [2, None], 'known path-to-cycle control')
    resp = responses(path, distances(path))
    correct = make_policy(path, resp, 2, range(5))
    require(correct is not None, 'path middle probe has no two-round policy')
    wrong_capture = {a: None for a in correct}
    wrong_probe = dict(correct)
    wrong_probe[next(a for a, v in wrong_probe.items() if v is not None)] = 99
    actions = [lambda: replay_policy(path, resp, 2, wrong_capture),
               lambda: replay_policy(path, resp, 2, wrong_probe),
               lambda: replay_policy(path, resp, 2, {}),
               lambda: replay_policy(path, resp, 2, None),
               lambda: graph(0, []), lambda: graph(2, [(0, 0)]),
               lambda: graph(2, [(0, 1), (1, 0)])]
    for action in actions:
        try:
            action()
        except ValueError:
            counts['rejections'] += 1
        else:
            raise ValueError('corrupted policy or malformed graph accepted')
    return {'counts': dict(sorted(counts.items())),
            'adaptive_rounds_histogram': dict(sorted(histogram.items())),
            'records_sha256': digest.hexdigest(), 'known_path_cycle_times': controls}
