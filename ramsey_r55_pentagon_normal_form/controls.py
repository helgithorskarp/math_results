#!/usr/bin/env python3
"""Exhaustive encoding controls and physical transport/candidate checks."""
import copy
import itertools as it
import json
import random
import tempfile
from collections import Counter
from pathlib import Path
import check_cnf
import decode
import encode
import normalize
import polynomial
import verify
import verify_graph

HERE = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise ValueError(message)


def adjacency(n, edges):
    a = [0] * n
    for i, j in edges:
        a[i] |= 1 << j; a[j] |= 1 << i
    return a


def brute_good(n, edges):
    for s in it.combinations(range(n), 5):
        colors = {int(e in edges) for e in it.combinations(s, 2)}
        if len(colors) == 1:
            return False
    return True


def controls():
    regular_counts = Counter()
    pairs5 = list(it.combinations(range(5), 2))
    for code in range(1024):
        edges = {e for k, e in enumerate(pairs5) if code >> k & 1}
        degrees = [sum(v in e for e in edges) for v in range(5)]
        if len(set(degrees)) == 1:
            require(degrees[0] in (0, 2, 4), "regular-five parity")
            regular_counts[str(degrees[0])] += 1
    require(dict(regular_counts) == {"0": 1, "2": 12, "4": 1}, "regular-five types")

    all_assignments = 0
    semantic_cases = []
    mutations_rejected = 0
    with tempfile.TemporaryDirectory() as temp:
        cnf = Path(temp) / "control.cnf"
        for n, cycles, joined in ((6, 0, False), (7, 1, False), (8, 1, True)):
            enc = encode.encode(cnf, n, cycles, joined)
            audit = check_cnf.check(cnf, n, cycles, joined)
            require({k: v for k, v in enc.items() if k != "status"} ==
                    {k: v for k, v in audit.items() if k not in ("status", "physical_five_color_cases")},
                    "small full audit")
            poly = polynomial.count(n, cycles, joined)
            require(poly["total"] == enc["clauses"], "polynomial count")
            clauses = [list(map(int, line.split()))[:-1] for line in cnf.read_text().splitlines()[1:]]
            masks = [(sum(1 << (x - 1) for x in c if x > 0),
                      sum(1 << (-x - 1) for x in c if x < 0)) for c in clauses]
            fixed, index, nv = check_cnf.layout(n, cycles, joined)
            good = 0
            for code in range(1 << nv):
                edges = {e for e in it.combinations(range(n), 2)
                         if (fixed[e[0]][e[1]] if fixed[e[0]][e[1]] is not None
                             else (code >> (index[e[0]][e[1]] - 1)) & 1)}
                sat = all((code & positive) or (~code & negative) for positive, negative in masks)
                direct = brute_good(n, edges)
                require(bool(sat) == direct, "Boolean/physical mismatch")
                good += direct
            all_assignments += 1 << nv
            semantic_cases.append({"n": n, "cycles": cycles, "joined": joined,
                                   "assignments": 1 << nv, "good": good})
        encode.encode(cnf, 8, 1, True)
        original = cnf.read_text().splitlines()
        damaged = []
        x = original.copy(); x.pop(); damaged.append(x)
        x = original.copy(); row = x[1].split(); row[0] = str(-int(row[0])); x[1] = ' '.join(row); damaged.append(x)
        x = original.copy(); row = x[1].split(); row[0] = '8'; x[1] = ' '.join(row); damaged.append(x)
        x = original.copy(); x.append(x[-1]); damaged.append(x)
        x = original.copy(); x[0] = x[0].replace('cnf 7 ', 'cnf 6 '); damaged.append(x)
        x = original.copy(); x[0] = 'p cnf 7 0'; damaged.append(x)
        x = original.copy(); x[-1] = x[-1][:-1] + '1'; damaged.append(x)
        for rows in damaged:
            cnf.write_text('\n'.join(rows) + '\n')
            try:
                check_cnf.check(cnf, 8, 1, True)
            except ValueError:
                mutations_rejected += 1
            else:
                raise ValueError("accepted corrupt formula")

    outcomes = Counter()
    rng = random.Random(431827)
    # A known good 42 graph, a known seven-defect43 graph, complements,
    # independent relabelings and unrestricted random43 colorings.
    for name in ("control42", "control43"):
        n, edges = verify.read_graph(HERE / (name + '.edges'))
        count_report = verify_graph.verify_graph(n, edges)
        require(count_report == json.loads((HERE / (name + '_counts.json')).read_text()),
                "fixture physical score")
        for iteration in range(24):
            order = list(range(n)); rng.shuffle(order)
            mapped = {tuple(sorted((order[i], order[j]))) for i, j in edges}
            if iteration % 2:
                mapped = set(it.combinations(range(n), 2)) - mapped
            cert = normalize.normalize(adjacency(n, mapped))
            report = verify.verify(n, mapped, cert)
            outcomes[report['status']] += 1
    for _ in range(32):
        edges = {e for e in it.combinations(range(43), 2) if rng.randrange(2)}
        cert = normalize.normalize(adjacency(43, edges))
        report = verify.verify(43, edges, cert)
        outcomes[report['status']] += 1
    for color in (0, 1):
        edges = set(it.combinations(range(43), 2)) if color else set()
        cert = normalize.normalize(adjacency(43, edges))
        require(cert['kind'] == 'monochromatic_five' and cert['color'] == color,
                "homogeneous graph outcome")
        verify.verify(43, edges, cert)
        outcomes['VERIFIED_PHYSICAL_FIVE'] += 1
    # Force the regular-five tail to find a blue five-set after a valid
    # two-pentagon ten-common-neighbor graph at the first anchor pair.
    edges = {(0, 1)} | {(i, j) for i in (0, 1) for j in range(2, 12)}
    for offset in (2, 7):
        edges |= {tuple(sorted((offset + i, offset + (i + 1) % 5))) for i in range(5)}
    cert = normalize.normalize(adjacency(43, edges))
    require(cert['kind'] == 'monochromatic_five' and cert['color'] == 0, "tail outcome")
    verify.verify(43, edges, cert)
    outcomes['VERIFIED_PHYSICAL_FIVE'] += 1

    n, edges = verify.read_graph(HERE / 'control43.edges')
    cert = json.loads((HERE / 'control43_certificate.json').read_text())
    corrupt = []
    x = copy.deepcopy(cert); x['order'][0] = x['order'][1]; corrupt.append(x)
    x = copy.deepcopy(cert); x['order'].pop(); corrupt.append(x)
    x = copy.deepcopy(cert); x['flip'] ^= 1; corrupt.append(x)
    x = copy.deepcopy(cert); x['order'][3], x['order'][4] = x['order'][4], x['order'][3]; corrupt.append(x)
    x = copy.deepcopy(cert); x['n'] = 42; corrupt.append(x)
    x = copy.deepcopy(cert); x['flip'] = False; corrupt.append(x)
    proof_mutations = 0
    for x in corrupt:
        try:
            verify.verify(n, edges, x)
        except ValueError:
            proof_mutations += 1
        else:
            raise ValueError('accepted corrupt frame')
    # Every free coordinate affects exactly its intended physical pair.
    fixed, index, nv = check_cnf.layout()
    required_red = {(i, j) for i, j in it.combinations(range(43), 2) if fixed[i][j] == 1}
    require(set(decode.decode('0' * nv)) == required_red, 'zero decoding')
    for i, j in it.combinations(range(43), 2):
        if index[i][j]:
            bits = ['0'] * nv; bits[index[i][j] - 1] = '1'
            require(set(decode.decode(''.join(bits))) == required_red | {(i, j)}, 'basis decoding')

    normal = polynomial.count()
    baseline = polynomial.count(cycles=1)
    expected = json.loads((HERE / 'expected_cnf.json').read_text())
    require(normal['total'] == expected['clauses'], 'full polynomial')
    require(sum(normal['red'].values()) == expected['red_clauses'] and
            sum(normal['blue'].values()) == expected['blue_clauses'], 'color polynomial')
    combined = Counter(normal['red']); combined.update(normal['blue'])
    require(dict(combined) == expected['length_histogram'], 'length polynomial')
    return {"status": "PENTAGON_FRAME_CONTROLS_PASS", "regular_five_graphs": dict(regular_counts),
            "physical_truth_assignments": all_assignments, "semantic_cases": semantic_cases,
            "formula_mutations_rejected": mutations_rejected,
            "frame_mutations_rejected": proof_mutations,
            "normalizer_outcomes": dict(outcomes), "decoder_basis_cases": nv + 1,
            "normal_form_polynomial": normal, "single_J_polynomial": baseline,
            "physical_variables_removed_beyond_J": 40,
            "clauses_removed_beyond_J": baseline['total'] - normal['total']}


if __name__ == '__main__':
    print(json.dumps(controls(), sort_keys=True))
