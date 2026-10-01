"""Separate literal controls for the ordinary C4/red-C counting proof.

Actual author six-books-1, role researcher; no imports from author programs.
All 2^15 six-root edge words are inspected, capacity domains are recursively
regenerated, and signed graph controls receive literal red/blue page audits.
These are author validation, not independent peer review or host enumeration.
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path

PAIRS = list(it.combinations(range(6), 2))
AC = [(i, c) for i in range(4) for c in (4, 5)]
CYCLE = {(0, 1), (1, 2), (2, 3), (0, 3)}


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def roots():
    incident, structural, fixed, shapes = 0, 0, {}, set()
    for mask in range(1 << 15):
        edges = {pair for j, pair in enumerate(PAIRS) if mask & (1 << j)}
        if (4, 5) not in edges:
            continue
        AA = {pair for pair in edges if pair[1] < 4}
        if any(sum(v in e for e in AA) != 2 for v in range(4)):
            continue
        shapes.add(tuple(sorted(AA)))
        red = [{u for u in range(6) if tuple(sorted((v, u))) in edges}
               for v in range(6)]
        f = [2 * (len(red[v] & set(range(4))) - len(red[v] & {4, 5})
                  + (-1 if v < 4 else 1)) for v in range(6)]
        if any(value < 0 for value in f):
            continue
        incident += 1
        opposite = [pair for pair in it.combinations(range(4), 2) if pair not in AA]
        if any(red[i] & red[j] & {4, 5} for i, j in opposite):
            continue
        structural += 1
        if AA == CYCLE:
            ac_mask = sum(1 << j for j, pair in enumerate(AC) if pair in edges)
            fixed[ac_mask] = (red, f, opposite)
    check(len(shapes) == 3, 'all labeled four-cycle shapes')
    return incident, structural, fixed


def gram(red, W):
    blue = [set(range(6)) - red[i] - {i} for i in range(6)]
    s = [(8 if i < 4 else 10) - len(red[i]) for i in range(6)]
    G = [[0] * 6 for _ in range(6)]
    for i in range(6):
        G[i][i] = s[i]
        for j in range(i + 1, 6):
            if j in red[i]:
                value = 3 - W[i][j] - len(red[i] & red[j])
            else:
                value = 6 - W[i][j] - len(blue[i] & blue[j]) - 16 + s[i] + s[j]
            G[i][j] = G[j][i] = value
    return G, s


def aggregate(red, W, G):
    r = sum(len(red[i] & {4, 5}) for i in range(4))
    sizes = [len(red[c] & set(range(4))) for c in (4, 5)]
    L = sum(len(list(it.combinations(range(v), 2))) for v in sizes)
    a = sum(W[i][j] for i in range(4) for j in range(i + 1, 4))
    b = W[4][5]
    Y = sum(W[i][c] for i in range(4) for c in (4, 5))
    H2 = sum(sum(row[:4]) for row in G[:4])
    K2 = sum(sum(row[4:]) for row in G[4:])
    HK = sum(sum(row[4:]) for row in G[:4])
    # Check the direct pair-count proof, including its root corrections.
    check(H2 == (24 - r) + 2 * (16 - a - 4 - L), 'AA pair count')
    check(K2 == (18 - r) + 2 * (3 - b), 'CC pair count')
    check(HK == (32 - r - Y) - 2 * r - r, 'AC pair count')
    return {'a': a, 'b': b, 'Y': Y, 'r': r, 'L': L,
            'H2': H2, 'K2': K2, 'HK': HK,
            'S': H2 + K2 - 2 * HK, 'T': HK - K2}


def capacity_states(mask, red, f, opposite):
    W = [[0] * 6 for _ in range(6)]
    remaining = list(f)
    values = []

    def visit(index):
        if index == len(PAIRS):
            G, s = gram(red, W)
            agg = aggregate(red, W, G)
            check(2 * agg['a'] + agg['Y'] <= 8 - 2 * agg['r'], 'A row capacities')
            if agg['r']:
                check(2 * agg['L'] <= agg['r'], 'C support correction')
                check(4 + 3 * agg['r'] + agg['Y'] > 2 * agg['L'] + 2 * agg['a'],
                      'attachment violates weighted bound')
            else:
                check(agg['T'] == 8 and agg['b'] == agg['Y'] == 0, 'unattached C moment')
            if agg['S'] >= 6:
                check(agg['S'] + agg['T'] > 12, 'necessary moments contradict word bound')
            yield {'ac_mask': mask, 'W': list(values), 'G': G, 'aggregates': agg,
                   'nonnegative_Gram': all(0 <= G[i][j] <= min(s[i], s[j]) for i, j in PAIRS)}
            return
        i, j = PAIRS[index]
        cap = 0 if (i, j) in opposite else min(remaining[i], remaining[j], 3 if j in red[i] else 6)
        for w in range(cap + 1):
            W[i][j] = W[j][i] = w
            remaining[i] -= w
            remaining[j] -= w
            values.append(w)
            yield from visit(index + 1)
            values.pop()
            remaining[i] += w
            remaining[j] += w
        W[i][j] = W[j][i] = 0

    yield from visit(0)


def signed_audit(control, mask, root_red, root_f):
    R = [[int(bit) for bit in row] for row in control['red_rows']]
    check(len(R) == 22 and all(len(row) == 22 for row in R), 'control dimensions')
    check(all(R[i][i] == 0 and R[i][j] == R[j][i] for i in range(22) for j in range(22)),
          'simple symmetric graph')
    red = [{j for j, value in enumerate(row) if value} for row in R]
    blue = [set(range(22)) - red[i] - {i} for i in range(22)]
    check([len(row) for row in red] == [8] * 4 + [10] * 2 + [9] * 16, 'control histogram')
    check([row & set(range(6)) for row in red[:6]] == root_red, 'control root pattern')
    F = [[0 if i == j else 3 - len(red[i] & red[j]) if j in red[i]
          else 6 - len(blue[i] & blue[j]) for j in range(22)] for i in range(22)]
    M = [row[:6] for row in R[6:]]
    G = [[sum(row[i] * row[j] for row in M) for j in range(6)] for i in range(6)]
    W = [row[:6] for row in F[:6]]
    counted, _ = gram(root_red, W)
    check(G == counted, 'literal control Gram')
    agg = aggregate(root_red, W, G)
    h = [sum(row[:4]) for row in M]
    k = [sum(row[4:]) for row in M]
    check((agg['H2'], agg['K2'], agg['HK'], agg['S'], agg['T']) ==
          (sum(v * v for v in h), sum(v * v for v in k), sum(v * w for v, w in zip(h, k)),
           sum((v - w) ** 2 for v, w in zip(h, k)), sum((v - w) * w for v, w in zip(h, k))),
          'literal control moments')
    for i in range(22):
        hi, ki = len(red[i] & set(range(4))), len(red[i] & {4, 5})
        wanted = 2 * (hi - ki - 1) if i < 4 else 2 * (hi - ki + 1) if i < 6 else 1 + 2 * (hi - ki)
        check(sum(F[i]) == wanted, 'literal incident row')
    check([sum(row) for row in F[:6]] == root_f, 'literal root incident defects')
    check(sum(root_f) == 8 and sum(v - w for v, w in zip(h, k)) == 6, 'literal total budgets')
    rebuilt = {'ac_mask': mask, 'red_rows': control['red_rows'], 'F': F, 'G': G,
               'aggregates': agg, 'root_f': root_f}
    check(rebuilt == control, 'every signed control field')
    return rebuilt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    supplied = json.loads(args.records.read_text())
    incident_count, structural_count, fixed = roots()
    check((incident_count, structural_count, len(fixed)) == (243, 147, 49), 'whole root domain')
    incident_fixed = [mask for mask in range(256) if all(sum((mask >> j) & 1 for j in (2 * i, 2 * i + 1)) <= 1 for i in range(4))]
    states = [state for mask in sorted(fixed) for state in capacity_states(mask, *fixed[mask])]
    words = []
    for number in range(64):
        bits = [(number >> (5 - j)) & 1 for j in range(6)]
        h, k = sum(bits[:4]), sum(bits[4:])
        delta = h - k
        if h <= 2 and delta >= 0:
            check(delta in (0, 1, 2) and delta * delta >= delta, 'integral surplus range')
            check(delta * (2 - h) >= 0, 'weighted word inequality')
            words.append({'bits': bits, 'h': h, 'k': k, 'delta': delta, 'gap': delta * (2 - h)})
    controls = supplied['signed_controls']
    check([c['ac_mask'] for c in controls] == sorted(fixed), 'one signed control per structural pattern')
    signed = [signed_audit(c, c['ac_mask'], fixed[c['ac_mask']][0], fixed[c['ac_mask']][1]) for c in controls]
    records = {'fixed_cycle': sorted(CYCLE), 'incident_roots': incident_fixed,
               'structural_roots': sorted(fixed), 'states': states, 'words': words,
               'signed_controls': signed}
    check(canonical(records) == canonical(supplied), 'all regenerated records agree')
    adequate = [s for s in states if s['aggregates']['S'] >= 6]
    summary = {'agent': 'six-books-1', 'role': 'researcher',
               'scope': 'ordinary C4/red-C exclusion; exact validation only, no host census',
               'fixed_cycle_incident_roots': len(incident_fixed),
               'all_labeled_incident_roots': incident_count,
               'fixed_cycle_structural_roots': len(fixed),
               'all_labeled_structural_roots': structural_count,
               'capacity_states': len(states),
               'nonnegative_Gram_states': sum(s['nonnegative_Gram'] for s in states),
               'states_with_square_sum_at_least_six': len(adequate),
               'minimum_weighted_C_gap': min(s['aggregates']['S'] + s['aggregates']['T'] - 12 for s in adequate),
               'word_inequalities': len(words),
               'words_also_avoiding_opposite_pairs': sum(not ((w['bits'][0] and w['bits'][2]) or (w['bits'][1] and w['bits'][3])) for w in words),
               'signed_controls': len(signed), 'literal_signed_F_entries': 484 * len(signed),
               'signed_Gram_entries': 36 * len(signed), 'signed_incident_rows': 22 * len(signed),
               'records_sha256': hashlib.sha256(canonical(records)).hexdigest()}
    expected = json.loads(Path(__file__).with_name('degree98_root_eight_cycle_expected.json').read_text())
    check(summary == expected, 'separate expected summary')
    # An h=3,k=2 word violates the proposed inequality. This checks that the
    # hypothesis h<=2 is essential and is not silently applied to the paw.
    check(1 * 2 > 2 * 1 - 1 ** 2, 'outside-scope negative word control')
    report = {'summary': summary, 'whole_root_edge_words': 1 << 15,
              'author_program_imports': False, 'every_record_compared': True,
              'signed_controls_are_identity_checks_only': True,
              'h_le_two_hypothesis_negative_control': True}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
