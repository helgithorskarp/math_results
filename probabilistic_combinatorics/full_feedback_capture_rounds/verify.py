#!/usr/bin/env python3
"""Exact finite checks for PROOF.md; no asymptotic inference from this census."""
from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from math import comb
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


def schedule_beliefs(adj, resp, probes):
    states = {frozenset(range(len(adj)))}
    for i, w in enumerate(probes):
        remaining = {u for state in states for u in partitions(resp[w], state)
                     if len(u) > 1}
        if not remaining:
            return True
        if i + 1 < len(probes):
            states = {closed(adj, u) for u in remaining}
    return False


def schedule_histories(adj, resp, probes):
    """Literal legal robber walks, grouped by their entire observation history."""
    paths = [(x,) for x in range(len(adj))]
    for i, w in enumerate(probes):
        groups = {}
        for path in paths:
            history = tuple(resp[probes[j]][path[j]] for j in range(i + 1))
            groups.setdefault(history, []).append(path)
        paths = [path for group in groups.values()
                 if len({p[-1] for p in group}) > 1 for path in group]
        if not paths:
            return True
        if i + 1 < len(probes):
            paths = [path + (x,) for path in paths
                     for x in adj[path[-1]] | {path[-1]}]
    return False


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


def bad_walk(adj, resp, probes):
    bad = [{x for u in partitions(resp[w], range(len(adj))) if len(u) > 1
            for x in u} for w in probes]
    paths = {x: (x,) for x in bad[0]}
    for layer in bad[1:]:
        nxt = {}
        for x, path in paths.items():
            for y in (adj[x] | {x}) & layer:
                nxt[y] = path + (y,)
        paths = nxt
    return next(iter(paths.values()), None)


def check_lower_certificate(adj, probes, paths):
    require(len(paths) == 2 and len(probes) > 0, "two nonempty walks required")
    n = len(adj)
    require(all(type(w) is int and 0 <= w < n for w in probes), "invalid probe")
    require(all(len(path) == len(probes) for path in paths), "walk length mismatch")
    require(all(type(x) is int and 0 <= x < n for path in paths for x in path),
            "invalid walk vertex")
    require(set(paths[0]).isdisjoint(paths[1]), "walks are not vertex-disjoint")
    d = distances(adj)
    require(d is not None, "connected graph required")
    resp = responses(adj, d)
    for path in paths:
        require(all(a == b or b in adj[a] for a, b in zip(path, path[1:])),
                "illegal robber move")
        require(all(resp[w][x] == adj[w] for w, x in zip(probes, path)),
                "response is not the full neighborhood")
    return True


def certificate_fixture(sequence):
    """Explicit buffer graph; repeated and mutually adjacent probes are allowed."""
    k, r = max(sequence) + 1, len(sequence)
    hub = 2 * k
    paths = tuple(tuple(2 * k + 1 + s * r + i for i in range(r)) for s in (0, 1))
    edges = set(combinations(range(k), 2))
    edges.update((i, k + i) for i in range(k))
    edges.update((k + i, hub) for i in range(k))
    for path in paths:
        for i, x in enumerate(path):
            edges.add((hub, x))
            edges.update((k + j, x) for j in range(k) if j != sequence[i])
        edges.update(zip(path, path[1:]))
    return graph(2 * k + 1 + 2 * r, sorted(edges)), paths


def set_partitions(n):
    if n == 0:
        yield ()
        return
    def extend(prefix, maximum):
        if len(prefix) == n:
            yield tuple(prefix)
        else:
            for label in range(maximum + 2):
                yield from extend(prefix + [label], max(maximum, label))
    yield from extend([0], 0)


def template_audit():
    count = Counter()
    for r in range(1, 5):
        for flags in product((False, True), repeat=r):
            h = sum(flags)
            for labels in set_partitions(r + h):
                edges = {tuple(sorted((labels[i], labels[i + 1])))
                         for i in range(r - 1) if labels[i] != labels[i + 1]}
                anchors = Counter()
                next_y = r
                invalid = False
                for i, flag in enumerate(flags):
                    if flag:
                        a, b = labels[i], labels[next_y]
                        next_y += 1
                        if a == b:
                            invalid = True
                            break
                        edges.add(tuple(sorted((a, b))))
                        anchors[a] += 1
                if invalid:
                    count['witness_loops_rejected'] += 1
                    continue
                v, e = max(labels) + 1, len(edges)
                require(e >= v - 1, "template lost connectedness")
                require(2 * v - h - e <= r + 1, "template exponent inequality")
                count['connected_templates'] += 1
                if any(k >= 3 for k in anchors.values()):
                    count['triple_anchors_excluded'] += 1
                if 2 * v - h - e == r + 1:
                    count['sharp_templates'] += 1
    return dict(sorted(count.items()))


def probability_audit():
    p, q = Fraction(1, 3), Fraction(2, 3)
    layers = 0
    for a in range(1, 4):
        for b in range(1, 5):
            distribution = [Fraction(0) for _ in range(b + 1)]
            for mask in range(1 << (a * b)):
                successes = sum(any(mask >> (x * a + y) & 1 for y in range(a))
                                for x in range(b))
                ones = mask.bit_count()
                distribution[successes] += p ** ones * q ** (a * b - ones)
            beta = 1 - q ** a
            expected = [comb(b, s) * beta ** s * (1 - beta) ** (b - s)
                        for s in range(b + 1)]
            require(distribution == expected, "layer binomial identity")
            layers += 1
    missing = 0
    for d, m in ((1, 1), (1, 3), (2, 2), (2, 3), (3, 2)):
        # w is not encoded: its fixed neighbors are 0,...,d-1.
        candidates = list(range(d, d + m))
        edges = [(a, x) for a in range(d) for x in candidates]
        edges += list(combinations(candidates, 2))
        expected = Fraction(0)
        for mask in range(1 << len(edges)):
            adj = graph(d + m, [edge for j, edge in enumerate(edges) if mask >> j & 1])
            defects = sum(not (adj[z] & set(range(d))) and not any(
                y in adj[b] and y in adj[z] for y in candidates if y != z)
                for z in candidates for b in range(d))
            ones = mask.bit_count()
            expected += defects * p ** ones * q ** (len(edges) - ones)
        require(expected == m * d * q ** d * (1 - p * p) ** (m - 1),
                "zero-code missing-direction expectation")
        missing += 1
    return {'exact_layer_distributions': layers, 'exact_missing_direction_means': missing}


def run():
    count = Counter()
    rounds_histogram = Counter()
    digest = sha256()
    # Full labelled census through five vertices; disconnected graphs are counted
    # but excluded from connected-game claims. No isomorphism library is used.
    for n in range(1, 6):
        edges = list(combinations(range(n), 2))
        for mask in range(1 << len(edges)):
            count['graphs'] += 1
            adj = graph(n, [e for j, e in enumerate(edges) if mask >> j & 1])
            d = distances(adj)
            if d is None:
                continue
            count['connected_graphs'] += 1
            resp = responses(adj, d)
            require(resp == first_step_responses(adj), "independent responses disagree")
            count['response_entries'] += n * n
            time = adaptive_rounds(adj, resp)
            rounds_histogram[str(time)] += 1
            digest.update(json.dumps([n, mask, time], separators=(',', ':')).encode() + b'\n')
            for w in range(n):
                D = adj[w]
                targets = set(range(n)) - D - {w}
                codes = {x: D & adj[x] for x in targets}
                small = {x for x in targets if len(codes[x]) <= 1}
                anchors = set().union(*(codes[x] for x in targets if len(codes[x]) == 1))
                nonzero = [codes[x] for x in targets if len(codes[x]) >= 2]
                zero_responses = [resp[w][x] for x in targets if not codes[x]]
                # Exact deterministic sufficient conditions used by Lemma 1.
                hypotheses = (len(nonzero) == len(set(nonzero)) and
                              all(len(z) > 1 and len(z) > max(
                                  [len(c) for c in codes.values()] + [0])
                                  for z in zero_responses))
                if hypotheses:
                    ambiguous = {x for group in partitions(resp[w], range(n))
                                 if len(group) > 1 for x in group}
                    require(ambiguous <= small | anchors, "ambiguity cover failed")
                    count['ambiguity_cover_instances'] += 1
            # Two representations of all fixed-schedule information histories.
            for probes in product(range(n), repeat=2):
                exact = schedule_histories(adj, resp, probes)
                require(exact == schedule_beliefs(adj, resp, probes), "history mismatch")
                bw = bad_walk(adj, resp, probes)
                if bw is None:
                    require(exact, "empty bad-walk certificate failed")
                    count['empty_bad_walk_certificates'] += 1
                elif exact:
                    count['bad_walk_not_a_lower_bound'] += 1
                count['fixed_schedules'] += 1
    # Three-round histories and adaptive controls on hand-checkable graphs.
    fixtures = [graph(4, [(0, 1), (1, 2), (2, 3)]),
                graph(5, [(i, (i + 1) % 5) for i in range(5)]),
                graph(4, [(0, 1), (1, 2), (2, 3), (0, 3)]),
                graph(4, list(combinations(range(4), 2)))]
    require([adaptive_rounds(a, responses(a, distances(a))) for a in fixtures]
            == [2, None, 1, 1], "path/cycle/complete adaptive controls")
    for adj in fixtures:
        resp = responses(adj, distances(adj))
        for probes in product(range(len(adj)), repeat=3):
            require(schedule_histories(adj, resp, probes)
                    == schedule_beliefs(adj, resp, probes), "three-round history mismatch")
            count['three_round_schedules'] += 1
    adj = fixtures[0]
    resp = responses(adj, distances(adj))
    require(schedule_beliefs(adj, resp, (1, 2)) and bad_walk(adj, resp, (1, 2)) is not None,
            "P4 must separate bad walks from actual failure")
    certificates = []
    for probes in ((0,), (0, 0), (0, 1), (0, 1, 2), (0, 1, 0), (0, 0, 0), (0, 1, 2, 1)):
        adj, paths = certificate_fixture(probes)
        require(check_lower_certificate(adj, probes, paths), "lower certificate")
        require(not schedule_beliefs(adj, responses(adj, distances(adj)), probes),
                "two walks did not force ambiguous histories")
        certificates.append({'probes': probes, 'paths': paths, 'order': len(adj)})
    count['lower_walk_certificates'] = len(certificates)
    # Invalid-input and invalid-certificate checks survive python -O.
    adj, paths = certificate_fixture((0, 1, 0))
    rejections = [lambda: graph(0, []), lambda: graph(2, [(0, 0)]),
                  lambda: graph(2, [(0, 1), (1, 0)]), lambda: graph(2, [(0, 2)]),
                  lambda: check_lower_certificate(adj, (0, 1, 0), (paths[0], paths[0])),
                  lambda: check_lower_certificate(adj, (0, 1), paths),
                  lambda: check_lower_certificate(adj, (0, 1, 0), ((0, 0, 0), paths[1])),
                  lambda: check_lower_certificate(adj, (0, 1, 0),
                      ((paths[0][0], paths[1][1], paths[0][2]),
                       (paths[1][0], paths[0][1], paths[1][2]))),
                  lambda: check_lower_certificate(adj, (0, 99, 0), paths)]
    for action in rejections:
        try:
            action()
        except ValueError:
            count['malformed_inputs_rejected'] += 1
        else:
            raise ValueError("invalid input accepted")
    count['adaptive_control_graphs'] = len(fixtures)
    return {'status': 'VERIFIED', 'scope': 'finite exact corroboration; asymptotic proof is PROOF.md',
            'census': dict(sorted(count.items())),
            'adaptive_rounds_histogram': dict(sorted(rounds_histogram.items())),
            'graph_records_sha256': digest.hexdigest(),
            'templates': template_audit(), 'probabilities': probability_audit(),
            'lower_certificate_fixtures': certificates}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
