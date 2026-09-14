"""Author-side cross-checks; separate complete search, not independent review."""
from copy import deepcopy
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json
import verify as V

HERE = Path(__file__).resolve().parent


def colour_search(n, edges, pins):
    """Exhaustive finite domain search, without endpoint elimination."""
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    initial = [15] * n
    for v, c in pins:
        initial[v] &= 1 << c

    def visit(domains):
        if 0 in domains:
            return None
        queue = [v for v, d in enumerate(domains) if d & (d - 1) == 0]
        done = set()
        while queue:
            v = queue.pop()
            if v in done:
                continue
            done.add(v)
            for u in sorted(adj[v]):
                d = domains[u] & ~domains[v]
                if d != domains[u]:
                    if not d:
                        return None
                    domains[u] = d
                    if d & (d - 1) == 0:
                        queue.append(u)
        free = [v for v, d in enumerate(domains) if d & (d - 1)]
        if not free:
            return ''.join(str(d.bit_length() - 1) for d in domains)
        v = min(free, key=lambda i: (domains[i].bit_count(), -len(adj[i]), i))
        for c in range(4):
            if domains[v] & (1 << c):
                child = domains.copy()
                child[v] = 1 << c
                word = visit(child)
                if word is not None:
                    return word
        return None

    return visit(initial)


def mask_norm(point_difference):
    """Different prime-mask multiplication for a rational radical norm."""
    masks = (0, 1, 2, 4, 3, 5, 6, 7)
    out = [F(0)] * 8
    for axis in point_difference:
        for i, x in enumerate(axis):
            for j, y in enumerate(axis):
                factor = 1
                for k, p in enumerate((3, 5, 7)):
                    if masks[i] & masks[j] & (1 << k):
                        factor *= p
                out[masks.index(masks[i] ^ masks[j])] += x * y * factor
    return tuple(out)


def main():
    cert = json.loads((HERE / 'certificate.json').read_text())
    expected = json.loads((HERE / 'expected.json').read_text())
    for bits in (48, 80, 128):
        V.need(V.verify(cert, bits) == expected, 'precision replay')
    points, roots, _, edges, _ = V.physical_graph()
    exact = [p['exact'] for p in points if p['exact'] is not None]
    for a, b in combinations(exact, 2):
        delta = V.sub(a, b)
        V.need(mask_norm(delta) == V.norm(delta), 'independent field norm')

    # Test interval branches using rational endpoints, including zero crossing,
    # exact roots, near-square inputs, and invalid reciprocal/root domains.
    interval_cases = 0
    for lo, hi in ((-2, -1), (-2, 0), (-2, 3), (0, 0), (0, 2), (1, 3)):
        a = (F(lo), F(hi))
        for x in (a[0], (a[0] + a[1]) / 2, a[1]):
            b = V.sq(a)
            V.need(b[0] <= x * x <= b[1], 'square branch containment')
            interval_cases += 1
        for blo, bhi in ((-3, -1), (-1, 2), (0, 0), (2, 3)):
            b = (F(blo), F(bhi))
            c = V.im(a, b)
            for x, y in product((a[0], sum(a) / 2, a[1]),
                                (b[0], sum(b) / 2, b[1])):
                V.need(c[0] <= x * y <= c[1], 'product branch containment')
                interval_cases += 1
    for x in (F(0), F(1), F(2), F(4), F(4) - F(1, 1 << 90), F(4) + F(1, 1 << 90)):
        lo, hi = V.sqrt_bounds((x, x), 48)
        V.need(lo * lo <= x <= hi * hi, 'root boundary')
        interval_cases += 1

    def normal(word):
        renaming = {}
        return ''.join(str(renaming.setdefault(c, len(renaming))) for c in word)

    domain = sorted({normal(w) for w in product(range(4), repeat=8)})
    V.need(domain == V.canonical_patterns(8), 'complete colour-permutation quotient')
    positive, negative = 0, 0
    for pattern in domain:
        word = colour_search(len(points), edges, [(v, int(c)) for v, c in zip(V.T, pattern)])
        feasible = bool(V.endpoint_relation(pattern[:4]).intersection(
            (b, a) for a, b in V.endpoint_relation(pattern[4:])))
        V.need((word is not None) == feasible, 'complete independent terminal search')
        if word is None:
            negative += 1
        else:
            V.need(all(word[a] != word[b] for a, b in edges), 'decoded edge inequality')
            V.need(all(word[v] == c for v, c in zip(V.T, pattern)), 'decoded pins')
            positive += 1

    mutations = []
    bad = deepcopy(cert); bad['edges'].pop(); mutations.append(bad)
    bad = deepcopy(cert); bad['edges'].append([16, 17]); mutations.append(bad)
    bad = deepcopy(cert); bad['root_map'][0][3] = 16; mutations.append(bad)
    bad = deepcopy(cert); bad['root_map'][0][2] *= -1; mutations.append(bad)
    bad = deepcopy(cert); bad['root_map'].pop(); mutations.append(bad)
    bad = deepcopy(cert); bad['three_colour_word'] = '0' * 44; mutations.append(bad)
    bad = deepcopy(cert); bad['three_colour_word'] = cert['three_colour_word'][:-1]; mutations.append(bad)
    bad = deepcopy(cert); bad['schema'] = True; mutations.append(bad)
    for bad in mutations:
        try:
            V.verify(bad)
        except ValueError:
            continue
        raise ValueError('corruption was accepted')
    result = {'status': 'CONTROLS_PASS', 'precision_replays': [48, 80, 128],
              'independent_field_norms': len(exact) * (len(exact) - 1) // 2,
              'interval_checks': interval_cases, 'labelled_terminal_assignments': 4 ** 8,
              'complete_search_patterns': len(domain), 'positive_words_checked': positive,
              'exhausted_negative_patterns': negative, 'rejected_corruptions': len(mutations)}
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
