"""Exact controls for the ordinary C4/red-C exclusion, not proof premises.

Actual author six-books-1, role researcher. CPython 3.11, standard library.
All generated records are optional scratch output; no host enumeration.
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path

A, C = range(4), range(4, 6)
PAIRS = list(it.combinations(range(6), 2))
AC = list(it.product(A, C))
CYCLE = {(0, 1), (1, 2), (2, 3), (0, 3)}
OPPOSITE = {(0, 2), (1, 3)}
D = [8] * 4 + [10] * 2


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def root(mask):
    edges = CYCLE | {(4, 5)} | {p for j, p in enumerate(AC) if mask >> j & 1}
    red = [[int(tuple(sorted((i, j))) in edges) if i != j else 0
            for j in range(6)] for i in range(6)]
    f = [2 * (sum(red[i][:4]) - sum(red[i][4:]) + (-1 if i < 4 else 1))
         for i in range(6)]
    s = [D[i] - sum(red[i]) for i in range(6)]
    r = mask.bit_count()
    ell = [sum(red[i][c] for i in A) for c in C]
    L = sum(v * (v - 1) // 2 for v in ell)
    return red, f, s, r, L


def coefficients(red, s, weights):
    W = [[0] * 6 for _ in range(6)]
    for (i, j), w in zip(PAIRS, weights):
        W[i][j] = W[j][i] = w
    G = [[s[i] if i == j else D[i] + D[j] - 14
          + (17 - D[i] - D[j]) * red[i][j]
          - sum(red[i][u] * red[u][j] for u in range(6)) - W[i][j]
          for j in range(6)] for i in range(6)]
    return W, G


def aggregates(mask, W, G):
    _, _, _, r, L = root(mask)
    a = sum(W[i][j] for i, j in it.combinations(A, 2))
    b = W[4][5]
    Y = sum(W[i][c] for i in A for c in C)
    H2 = sum(G[i][j] for i in A for j in A)
    K2 = sum(G[i][j] for i in C for j in C)
    HK = sum(G[i][c] for i in A for c in C)
    require((H2, K2, HK) == (48 - r - 2 * L - 2 * a,
                            24 - r - 2 * b, 32 - 4 * r - Y),
            'double-counted block coefficients')
    S, T = H2 + K2 - 2 * HK, HK - K2
    require(S == 8 + 6 * r - 2 * L - 2 * a - 2 * b + 2 * Y,
            'square-sum coefficient')
    require(T == 8 - 3 * r - Y + 2 * b, 'weighted-C coefficient')
    return {'a': a, 'b': b, 'Y': Y, 'r': r, 'L': L,
            'H2': H2, 'K2': K2, 'HK': HK, 'S': S, 'T': T}


def complete_B(degrees):
    """Deterministic Havel--Hakimi realization; raises if nongraphical."""
    remaining = list(degrees)
    P = [[0] * 16 for _ in range(16)]
    while any(remaining):
        order = sorted(range(16), key=lambda i: (-remaining[i], i))
        v, degree = order[0], remaining[order[0]]
        require(0 <= degree < 16, 'control residual degree range')
        neighbors = order[1:degree + 1]
        require(len(neighbors) == degree and all(remaining[u] > 0 for u in neighbors),
                'control residual sequence is not graphical')
        remaining[v] = 0
        for u in neighbors:
            require(not P[v][u], 'control duplicate edge')
            P[v][u] = P[u][v] = 1
            remaining[u] -= 1
    require([sum(row) for row in P] == degrees, 'control B degrees')
    return P


def signed_control(mask, number):
    red, f, s, _, _ = root(mask)
    M = [[int((v - (3 * j + number)) % 16 < s[j]) for j in range(6)]
         for v in range(16)]
    P = complete_B([9 - sum(row) for row in M])
    R = [[0] * 22 for _ in range(22)]
    for i in range(6):
        R[i][:6] = red[i]
    for v in range(16):
        for j in range(6):
            R[6 + v][j] = R[j][6 + v] = M[v][j]
        R[6 + v][6:] = P[v]
    degrees = D + [9] * 16
    require([sum(row) for row in R] == degrees, 'signed control histogram')
    F = [[0 if i == j else degrees[i] + degrees[j] - 14
          + (17 - degrees[i] - degrees[j]) * R[i][j]
          - sum(R[i][u] * R[u][j] for u in range(22))
          for j in range(22)] for i in range(22)]
    for i in range(22):
        h, k = sum(R[i][:4]), sum(R[i][4:6])
        wanted = 2 * (h - k - 1) if i < 4 else 2 * (h - k + 1) if i < 6 else 1 + 2 * (h - k)
        require(sum(F[i]) == wanted, 'signed incident identity')
    require(sum(sum(F[i]) for i in range(6)) == 8, 'signed root budget')
    require(sum(sum(row[:4]) - sum(row[4:]) for row in M) == 6,
            'signed surplus total')
    W = [F[i][j] for i, j in PAIRS]
    _, G = coefficients(red, s, W)
    literal = [[sum(row[i] * row[j] for row in M) for j in range(6)] for i in range(6)]
    require(G == literal, 'signed Gram entries')
    agg = aggregates(mask, [row[:6] for row in F[:6]], G)
    # Signed controls validate identities only. No nonnegative-defect or h<=2
    # condition is imposed on them, so they are not Ramsey constructions.
    return {'ac_mask': mask, 'red_rows': [''.join(map(str, row)) for row in R],
            'F': F, 'G': G, 'aggregates': agg, 'root_f': f}


def build():
    incident, roots, states = [], [], []
    for mask in range(256):
        red, f, s, r, L = root(mask)
        if min(f) < 0:
            continue
        incident.append(mask)
        if any(sum(red[c][i] * red[c][j] for c in C) for i, j in OPPOSITE):
            continue
        require(all(sum(red[c][:4]) <= 2 for c in C), 'C support bound')
        require(2 * L <= r and sum(f) == 8, 'root aggregate bounds')
        roots.append(mask)
        caps = [0 if (i, j) in OPPOSITE else min(f[i], f[j], 3 if red[i][j] else 6)
                for i, j in PAIRS]
        for values in it.product(*(range(cap + 1) for cap in caps)):
            W, G = coefficients(red, s, values)
            if any(sum(W[i]) > f[i] for i in range(6)):
                continue
            agg = aggregates(mask, W, G)
            require(2 * agg['a'] + agg['Y'] <= 8 - 2 * r, 'A budget')
            if r >= 1:
                require(5 * r + 2 * agg['Y'] > 4 + 2 * L,
                        'positive attachment contradiction')
            else:
                require(agg['b'] == agg['Y'] == 0 and agg['T'] == 8,
                        'zero attachment coefficient')
            if agg['S'] >= 6:
                require(agg['S'] + agg['T'] > 12, 'weighted-C contradiction')
            states.append({'ac_mask': mask, 'W': list(values), 'G': G,
                           'aggregates': agg,
                           'nonnegative_Gram': all(0 <= G[i][j] <= min(s[i], s[j]) for i, j in PAIRS)})
    words = []
    for bits in it.product((0, 1), repeat=6):
        h, k = sum(bits[:4]), sum(bits[4:])
        delta = h - k
        if h <= 2 and delta >= 0:
            require(delta * k <= 2 * delta - delta * delta, 'word inequality')
            words.append({'bits': list(bits), 'h': h, 'k': k, 'delta': delta,
                          'gap': 2 * delta - delta * delta - delta * k})
    signed = [signed_control(mask, n) for n, mask in enumerate(roots)]
    records = {'fixed_cycle': sorted(CYCLE), 'incident_roots': incident,
               'structural_roots': roots, 'states': states, 'words': words,
               'signed_controls': signed}
    adequate = [s for s in states if s['aggregates']['S'] >= 6]
    summary = {'agent': 'six-books-1', 'role': 'researcher',
               'scope': 'ordinary C4/red-C exclusion; exact validation only, no host census',
               'fixed_cycle_incident_roots': len(incident),
               'all_labeled_incident_roots': 3 * len(incident),
               'fixed_cycle_structural_roots': len(roots),
               'all_labeled_structural_roots': 3 * len(roots),
               'capacity_states': len(states),
               'nonnegative_Gram_states': sum(s['nonnegative_Gram'] for s in states),
               'states_with_square_sum_at_least_six': len(adequate),
               'minimum_weighted_C_gap': min(s['aggregates']['S'] + s['aggregates']['T'] - 12 for s in adequate),
               'word_inequalities': len(words),
               'words_also_avoiding_opposite_pairs': sum(not any(w['bits'][i] and w['bits'][j] for i, j in OPPOSITE) for w in words),
               'signed_controls': len(signed), 'literal_signed_F_entries': 484 * len(signed),
               'signed_Gram_entries': 36 * len(signed),
               'signed_incident_rows': 22 * len(signed),
               'records_sha256': hashlib.sha256(canonical(records)).hexdigest()}
    require((len(incident), len(roots), len(words)) == (81, 49, 37), 'coverage controls')
    return records, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records', type=Path)
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    records, summary = build()
    expected = Path(__file__).with_name('degree98_root_eight_cycle_expected.json')
    if args.write_expected:
        expected.write_text(json.dumps(summary, indent=2) + '\n')
    else:
        require(summary == json.loads(expected.read_text()), 'expected summary differs')
    if args.records:
        args.records.write_bytes(canonical(records) + b'\n')
    print(json.dumps(summary, sort_keys=True))


if __name__ == '__main__':
    main()
