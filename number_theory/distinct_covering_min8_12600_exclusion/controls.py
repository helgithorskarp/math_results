"""Small complete controls for the new standalone 12600 checker.

These check branch equivalence by full coordinate permutations, every entry
of joint tables by actual unions, and rejection of malformed proof inputs.
They supplement rather than replace the two full exact replays.
"""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import random
import check
import audit


def run(certificate):
    rng = random.Random(20260930012600)
    symmetry_phases = 0
    coordinate_witnesses = 0
    for L in (12, 24, 60, 120, 840):
        moduli = [m for m in range(2, L + 1) if L % m == 0]
        for count in range(8):
            placed = rng.sample(moduli, min(count % 5, len(moduli)))
            A = tuple((m, rng.randrange(m)) for m in placed)
            for m in (q for q in moduli if q not in placed and q <= 30):
                representatives = {}
                for a in range(m):
                    key = check.normalize(A + ((m, a),))
                    b = representatives.setdefault(key, a)
                    for p, e in audit.factor(L):
                        P = p ** e
                        q = p ** audit.valuation(m, p)
                        fixed = tuple((p ** audit.valuation(n, p), c % (p ** audit.valuation(n, p)))
                                      for n, c in A)
                        audit.coordinate_transport(p, P, q, a % q, b % q, fixed)
                        coordinate_witnesses += 1
                    symmetry_phases += 1
    pair_cases = pair_phases = 0
    for L in (12, 24, 60):
        moduli = [m for m in range(2, L + 1) if L % m == 0]
        for sample in range(3):
            W = [rng.randrange(5) for x in range(L)]
            for i, m in enumerate(moduli):
                for n in moduli[i + 1:]:
                    digest, largest = sha256(), 0
                    for a in range(m):
                        X = set(range(a, L, m))
                        for b in range(n):
                            value = sum(W[x] for x in X | set(range(b, L, n)))
                            largest = max(largest, value)
                            digest.update((str(value) + ',').encode('ascii'))
                    if check.pair_capacity(W, m, n) != (largest, digest.hexdigest()):
                        raise ValueError('Joint capacity entry mismatch')
                    pair_cases += 1
                    pair_phases += m * n
    # Definition-level positive cover: no scalar strict cut can reject it.
    witness = [(2, 0), (3, 0), (4, 1), (6, 1), (12, 11)]
    if not all(any(x % m == a for m, a in witness) for x in range(12)):
        raise ValueError('Bad positive covering fixture')
    for depth in range(len(witness) + 1):
        A = witness[:depth]
        U = [int(all(x % m != a for m, a in A)) for x in range(12)]
        C = sum(max(check.population(U, m)) for m, a in witness[depth:])
        if sum(U) > C:
            raise ValueError('Actual covering was falsely rejected')
    rejections = 0
    for mutation in ('wrong-L', 'wrong-root', 'open-root', 'missing-child', 'false-root-cut'):
        broken = deepcopy(certificate)
        if mutation == 'wrong-L':
            broken['L'] = 12608
        elif mutation == 'wrong-root':
            broken['root_anchors'] = [[8, 1]]
        elif mutation == 'open-root':
            broken['nodes'][0] = [3]
        elif mutation == 'missing-child':
            broken['nodes'][0][2] = []
        else:
            # A fabricated uniform obstruction must not be accepted.
            broken['nodes'][0] = [0, 1, 0]
        try:
            check.prove(broken)
        except (ValueError, IndexError, TypeError):
            rejections += 1
        else:
            raise ValueError('Malformed global certificate accepted')
    for failure in ('covered-support', 'repeated-resource'):
        broken = {'schema': 2, 'L': 12600, 'minimum': 8, 'root_anchors': [[8, 0]],
                  'vectors': [[[1, 1, 1, 1, 1]]], 'nodes': [[1, 0, 1, 0, []]]}
        if failure == 'repeated-resource':
            broken['vectors'] = [[[2, 2, 2, 2, 1]]]
            broken['nodes'][0][4] = [[9, 10], [10, 12]]
        try:
            check.prove(broken)
        except ValueError:
            rejections += 1
        else:
            raise ValueError('Invalid support or resource partition accepted')
    for boxes in ([[0, 1, 1, 1]], [[1, 1, 1, 0]], [[1, 1, 1, 1], [1, 1, 1, 1]]):
        try:
            check.decode(60, boxes)
        except ValueError:
            rejections += 1
        else:
            raise ValueError('Invalid weight boxes accepted')
    return {'status': 'COMPLETE SMALL CONTROLS', 'symmetry_phases': symmetry_phases,
            'coordinate_transport_checks': coordinate_witnesses, 'joint_cases': pair_cases,
            'joint_phase_tuples': pair_phases, 'positive_cover_prefixes': len(witness) + 1,
            'malformed_rejections': rejections}


if __name__ == '__main__':
    certificate = json.loads(Path(__file__).with_name('certificate.json').read_text())
    actual=run(certificate)
    expected=json.loads(Path(__file__).with_name('controls_expected.json').read_text())
    if actual!=expected:raise ValueError('Control manifest mismatch')
    print(json.dumps(actual, indent=2))
