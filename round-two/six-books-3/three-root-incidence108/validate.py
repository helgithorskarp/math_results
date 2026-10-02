"""Literal signed graph controls, not a census of valid hosts.

Reconstruct degree-correct 22-point graphs. Independently compare actual
red/complement intersections with the ordinary mixed-walk identities.
"""
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def high_graph(types):
    rows = [set() for _ in types]
    left = [10-t.bit_count() for t in types]
    while any(left):
        order = sorted(range(18), key=lambda x: (-left[x], x))
        x = order[0]
        degree = left[x]
        other = [y for y in order[1:] if left[y] > 0][:degree]
        require(len(other) == degree, 'Non-graphical prescribed high control degrees')
        left[x] = 0
        for y in other:
            require(y not in rows[x], 'Repeated control edge')
            rows[x].add(y)
            rows[y].add(x)
            left[y] -= 1
    return rows


def switched(rows):
    new = [set(row) for row in rows]
    edges = [(x, y) for x in range(18) for y in sorted(rows[x]) if x < y]
    for (a, b), (c, d) in itertools.combinations(edges, 2):
        if len({a, b, c, d}) != 4 or c in rows[a] or d in rows[b]:
            continue
        for x, y in [(a, b), (c, d)]:
            new[x].remove(y)
            new[y].remove(x)
        for x, y in [(a, c), (b, d)]:
            new[x].add(y)
            new[y].add(x)
        return new
    raise ValueError('No nontrivial degree-preserving control switch')


def q1_types():
    # Every singleton allocation and every triple omission, one complete
    # pair-margin solution apiece. These are deliberately invalid controls.
    for single in itertools.product(range(4), repeat=4):
        if sum(single) != 3:
            continue
        for omit in range(4):
            triple = 15 ^ (1 << omit)
            target = [9-(1 if i < 2 else 0)-single[i]-(triple >> i & 1)
                      for i in range(4)]
            solution = None
            for ab in range(10):
                for ac in range(10):
                    ad = target[0]-ab-ac
                    bc2 = target[1]-ab+target[2]-ac-target[3]+ad
                    if bc2 % 2:
                        continue
                    bc = bc2//2
                    bd = target[1]-ab-bc
                    cd = target[2]-ac-bc
                    pair = (ab, ac, ad, bc, bd, cd)
                    if min(pair) >= 0:
                        solution = pair
                        break
                if solution is not None:
                    break
            require(solution is not None, 'Missing signed-control incidence margins')
            result = []
            for i, n in enumerate(single):
                result.extend([1 << i]*n)
            result.append(triple)
            for mask, n in zip((3, 5, 9, 6, 10, 12), solution):
                result.extend([mask]*n)
            require(len(result) == 18, 'Wrong q1 control cardinality')
            yield sorted(result)


def assemble(types, high, q):
    rows = [set() for _ in range(22)]
    if q == 1:
        rows[0].add(1)
        rows[1].add(0)
    for x, mask in enumerate(types):
        for i in range(4):
            if mask >> i & 1:
                rows[i].add(x+4)
                rows[x+4].add(i)
        rows[x+4].update(y+4 for y in high[x])
    require([len(row) for row in rows] == [9]*4+[10]*18,
            'Signed control is not degree-correct')
    require(all(x not in rows[x] and (x in rows[y]) == (y in rows[x])
                for x in range(22) for y in range(22)), 'Not a simple control graph')
    return rows


def audit(rows, q, totals):
    blue = [set(range(22))-rows[x]-{x} for x in range(22)]
    invalid = False
    for u, v in itertools.combinations(range(22), 2):
        red = len(rows[u] & rows[v])
        actual_blue = len(blue[u] & blue[v])
        edge = int(v in rows[u])
        require(actual_blue == 20-len(rows[u])-len(rows[v])+red+2*edge,
                'Wrong literal endpoint identity')
        totals['endpoint_pairs'] += 1
        totals['red_endpoint_term_controls'] += edge
        invalid |= red > 3 if edge else actual_blue > 6
    require(invalid, 'Control satisfies full caps: inspect potential construction')
    totals['graphs_with_page_cap_violations'] += 1
    m = [[int(x+4 in rows[i]) for x in range(18)] for i in range(4)]
    low_adj = [[int(j in rows[i]) for j in range(4)] for i in range(4)]
    types = [sum(1 << i for i in range(4) if m[i][x]) for x in range(18)]
    require(all(types), 'Control unexpectedly has a full root')
    require(sum(t.bit_count() == 1 for t in types) ==
            2*q+sum(t.bit_count() == 3 for t in types)+
            2*sum(t.bit_count() == 4 for t in types), 'Wrong ordinary occurrence count')
    s = [[5-2*m[i][x]-len(rows[i] & rows[x+4]) for x in range(18)] for i in range(4)]
    for i in range(4):
        a = len(rows[i] & set(range(4)))
        singleton = sum(m[i][x] for x, t in enumerate(types) if t.bit_count() == 1)
        triple = sum(m[i][x] for x, t in enumerate(types) if t.bit_count() == 3)
        quad = sum(m[i][x] for x, t in enumerate(types) if t.bit_count() == 4)
        predicted = a+sum(len(rows[j] & set(range(4))) for j in rows[i] if j < 4)
        predicted += -singleton+triple+2*quad
        require(sum(s[i]) == predicted, 'Wrong signed local mixed row sum')
        if a == 0:
            neighborhood_edges = sum(len(rows[x] & rows[i]) for x in rows[i])//2
            alpha = sum(s[i][x] for x in range(18) if m[i][x])
            require(alpha == 27-2*neighborhood_edges and alpha % 2 == 1,
                    'Wrong signed isolated-low parity')
            totals['isolated_parity_rows'] += 1
        for x in range(18):
            mq = sum(m[i][y]*int(x+4 in rows[y+4]) for y in range(18))
            alm = sum(low_adj[i][j]*m[j][x] for j in range(4))
            require(mq == 5-2*m[i][x]-alm-s[i][x], 'Wrong actual MQ identity')
            totals['mixed_walk_entries'] += 1
            totals['negative_slack_entries'] += int(s[i][x] < 0)
            totals['positive_slack_entries'] += int(s[i][x] > 0)
    k = [[sum(m[i][x]*m[j][x] for x in range(18)) for j in range(4)] for i in range(4)]
    if q == 1:
        for j in (2, 3):
            require(k[1][j]+sum(s[0][x]*m[j][x] for x in range(18)) ==
                    5+sum(s[j][x]*m[0][x] for x in range(18)), 'Wrong A,j symmetry transport')
            require(k[0][j]+sum(s[1][x]*m[j][x] for x in range(18)) ==
                    5+sum(s[j][x]*m[1][x] for x in range(18)), 'Wrong B,j symmetry transport')
            totals['q1_signed_transports'] += 2
    else:
        for i, j in itertools.combinations(range(4), 2):
            require(sum(s[i][x]*m[j][x] for x in range(18)) ==
                    sum(s[j][x]*m[i][x] for x in range(18)), 'Wrong q0 signed transport')
            totals['q0_signed_transports'] += 1


def baseline():
    raw = (ROOT/'primary21.txt').read_bytes()
    require(hashlib.sha256(raw).hexdigest() ==
            '3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55',
            'Primary raw bytes differ')
    matrix, _ = json.JSONDecoder().raw_decode(raw.decode())
    require(len(matrix) == 21 and all(len(row) == 21 for row in matrix), 'Wrong primary order')
    red = [{j for j in range(21) if j != i and matrix[i][j] == 0} for i in range(21)]
    blue = [set(range(21))-red[i]-{i} for i in range(21)]
    counts, maxima = [0, 0], [0, 0]
    for i, j in itertools.combinations(range(21), 2):
        require(matrix[i][j] == matrix[j][i] and matrix[i][j] in (0, 1), 'Wrong primary matrix')
        color = matrix[i][j]
        rows = blue if color else red
        pages = len(rows[i] & rows[j])
        require(pages <= (6 if color else 3), 'Primary literal colored page cap fails')
        counts[color] += 1
        maxima[color] = max(maxima[color], pages)
    return dict(order=21, checked_pairs=210, red_edges=counts[0], blue_edges=counts[1],
                red_pages=maxima[0], blue_pages=maxima[1], primary_prior_art=True,
                raw_sha256=hashlib.sha256(raw).hexdigest())


def main():
    census = json.loads((ROOT/'incidence.json').read_text())
    totals = {k: 0 for k in ('graphs', 'endpoint_pairs', 'red_endpoint_term_controls',
                            'isolated_parity_rows', 'mixed_walk_entries',
                            'negative_slack_entries', 'positive_slack_entries',
                            'q1_signed_transports', 'q0_signed_transports',
                            'graphs_with_page_cap_violations')}
    transcript = []
    inputs = [(1, t) for t in q1_types()]
    inputs.extend((0, [m for m, n in enumerate(c, 1) for _ in range(n)])
                  for sector in census['sectors'] for c in sector['canonical'])
    for q, types in inputs:
        high = high_graph(types)
        for hh in (high, switched(high)):
            rows = assemble(types, hh, q)
            audit(rows, q, totals)
            transcript.append([sum(1 << y for y in r) for r in rows])
            totals['graphs'] += 1
    require(totals['negative_slack_entries'] > 0 and totals['positive_slack_entries'] > 0,
            'Signed controls do not exercise both signs')
    require(totals['q1_signed_transports'] > 0 and totals['q0_signed_transports'] > 0,
            'Missing matrix-transport controls')
    whole = (json.dumps(transcript, separators=(',', ':'))+'\n').encode()
    result = dict(scope='Finite deliberately invalid signed controls; validates identities, never host nonexistence',
                  controls=totals, control_graphs_sha256=hashlib.sha256(whole).hexdigest(),
                  primary=baseline())
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
