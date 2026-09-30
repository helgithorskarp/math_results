#!/usr/bin/env python3
"""Independent endpoint review and a three-cut combinatorial proof.

No submitted implementation, SAT solver or cardinality package is imported.
The small public input files are hash-pinned; all comparator images and
pruning witnesses are independently decoded as integer flags.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path

from semantic_core import canon, require, semantic_audit


INPUT_HASHES = {
    'fixture.json': 'ab8ef78a8a914f7f9b951253ddf80964abeee7fc1175df04382846f3b00cc02e',
    'certificate.json': 'c4c9120b24f1b50e9fd3fe8867c4f1f5538e5c0e1047052b31f42f0ad6935ff1',
    'Z19-core.cnf': '81b7275e3f48e05fe803906f59c3b4164df6e4c240cc95f225ea27248f51c988',
    'Z19-proof.rup': '50a961f6b38fd6490cbcdff63b5ebadfa8595be8a47f4e77fb485cbcff40b333',
}


def trajectory(word, mask):
    high_touches = low_touches = 0
    for a, b in word:
        require(0 <= a < b, 'Nonstandard comparator')
        lower, upper = (mask >> a) & 1, (mask >> b) & 1
        high_touches += bool(lower or upper)
        low_touches += not (lower and upper)
        if lower and not upper:
            mask ^= (1 << a) | (1 << b)
    return mask, high_touches, low_touches


def sorted_mask(n, weight):
    return ((1 << weight) - 1) << (n - weight)


def image_check(fixture, certificate):
    p24 = fixture['prefix21'] + fixture['tournament']
    p25 = p24 + [[0, 10]]
    require(len(p24) == 24 and len(p25) == 25, 'Prefix lengths')
    require(p25 == certificate['prefix25'], 'Prefix25 input differs')
    y, z = set(), set()
    for x in range(1 << 13):
        yy = trajectory(p24, x)[0]
        zz = trajectory(p25, x)[0]
        final = sorted_mask(13, x.bit_count())
        require((yy >> 11) == (zz >> 11) == (final >> 11), 'Largest two outputs not fixed')
        y.add(yy & 2047)
        z.add(zz & 2047)
        require(trajectory(fixture['incumbent45'], x)[0] == final, 'Incumbent fails')
        require(trajectory(p24 + fixture['known21'], x)[0] == final, 'Y2 upper control fails')
        require(trajectory(p25 + fixture['known21'], x)[0] == final, 'Z upper control fails')
    require(sorted(y) == certificate['Y2_states'] and len(y) == 145, 'Y2 image')
    require(sorted(z) == certificate['Z_states'] and len(z) == 144, 'Z image')
    require([x for x in y if x & 1 and not (x >> 10 & 1)] == [65], 'Endpoint exception')
    require(trajectory([[0, 10]], 65)[0] == 1088 and 1088 in y and z == y - {65},
            'Endpoint quotient')
    require(all((x >> 1 & 1) <= (x >> 10 & 1) for x in z), 'Ordered rectangle')
    require(all(x == 2047 or any(not (x >> i & 1) for i in (0, 1, 5)) for x in z),
            'Minimum-candidate cover')
    require(all(sorted_mask(11, weight) in z for weight in range(12)), 'Sorted chain')

    # Only three original threshold inputs are required by the new proof.
    witnesses = {}
    for original, expected, deleted in [(46, 1536, 17), (38, 512, 12), (652, 68, 13)]:
        out, high, low = trajectory(p25, original)
        require(out & 2047 == expected and high == deleted, 'Three-cut prefix witness')
        require(out >> 11 == 3, 'Both discarded outputs must be high')
        witnesses[str(original)] = {'residual_state': expected, 'high_prefix_deletions': high,
                                   'fixed_maxima': original.bit_count()}
    require(witnesses['46']['fixed_maxima'] == 4, 'Nine free inputs')
    require({512, 68, 1536}.issubset(z), 'Cut proof rows absent')
    require(trajectory([[2, 9], [6, 10], [9, 10]], 512)[0] == sorted_mask(11, 1),
            'Abstract cut sharpness1')
    require(trajectory([[2, 9], [6, 10], [9, 10]], 68)[0] == sorted_mask(11, 2),
            'Abstract cut sharpness2')
    require(any(trajectory([[2, 9], [6, 10], [9, 10]], x)[0] != sorted_mask(11, x.bit_count())
                for x in z), 'Do not mislabel two-row sharpness as a Z sorter')

    minimum = [[0, 5], [0, 1]]
    w = set()
    for x in z:
        out = trajectory(minimum, x)[0]
        require((out & 1) == (x == 2047), 'Peeling loses minimum')
        w.add(out >> 1)
    require(sorted(w) == certificate['W_states'] and len(w) == 128, 'W projection')
    require(all(sorted_mask(10, weight) in w for weight in range(11)), 'W sorted chain')
    require(len(certificate['W_known19']) == 19, 'W control size')
    require(all(trajectory(certificate['W_known19'], x)[0] == sorted_mask(10, x.bit_count())
                for x in w), 'W upper control')
    # Closed-form enumeration of the conditional three-leaf kernel grammar.
    kernels = [((0, 5), (0, 1))]
    for partner in (2, 3, 4, 6, 7, 8, 9):
        first = (min(5, partner), max(5, partner))
        kernels.append((first, (0, min(5, partner)), (0, 1)))
    require(sorted(kernels) == sorted(tuple(map(tuple, word))
                                    for word in certificate['minimum_kernels']), 'Eight kernels')
    cut_bound = 3
    lower_z = 25 - len(p25) + witnesses['46']['high_prefix_deletions'] + cut_bound
    require(lower_z == 20, 'Pruning lower bound arithmetic')
    return p25, z, {'original_inputs': 8192, 'Y2_states': 145, 'Z_states': 144, 'W_states': 128,
                    'Z_W_upper_controls': [21, 19], 'three_cut_witnesses': witnesses,
                    'abstract_two_row_cut_bound': cut_bound, 'Z_lower_bound': lower_z,
                    'W_lower_bound': lower_z - len(minimum), 'conditional_minimum_kernel_words': 8}


def witness_check(p25, certificate):
    lower = [0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35, 39, 44]
    count = 0
    for record in certificate['single_threshold_bounds']:
        state = record['state']
        hi = trajectory(p25, record['high_witness'])
        lo = trajectory(p25, record['low_witness'])
        require(hi[0] & 2047 == lo[0] & 2047 == state, 'Threshold attainer image')
        require(hi[1] == record['high_deleted'] and lo[2] == record['low_deleted'],
                'Threshold deletion count')
        require(record['high_cap'] == 44 - lower[11 - state.bit_count()] - hi[1], 'High cap')
        require(record['low_cap'] == 44 - lower[state.bit_count() + 2] - lo[2], 'Low cap')
        count += 2
    labels = [0 if i == 10 else 2 if i in (2, 3, 5) else 1 for i in range(13)]
    code = sum(v*3**i for i, v in enumerate(labels))
    require(code == 738391 == certificate['central_mixed_bound']['witness_base3'], 'Mixed labels')
    deleted = 0
    for a, b in p25:
        deleted += labels[a] != 1 or labels[b] != 1
        if labels[a] > labels[b]:
            labels[a], labels[b] = labels[b], labels[a]
    require(deleted == 17, 'Mixed prefix deletion')
    high = sum((v == 2) << i for i, v in enumerate(labels[:11]))
    nonlow = sum((v != 0) << i for i, v in enumerate(labels[:11]))
    require((high, nonlow) == (1024, 2045), 'Mixed projection')
    return {'threshold_attainers': count, 'mixed_prefix_deletions': deleted,
            'mixed_masks': [high, nonlow], 'mixed_union_cap_at_size44': 2}


def read_clauses(path, header=False):
    lines = path.read_text().splitlines()
    if header:
        fields = lines.pop(0).split()
        require(fields[:2] == ['p', 'cnf'], 'DIMACS header')
        variables, count = map(int, fields[2:])
    else:
        variables, count = 40894, len(lines)
    clauses = []
    for line in lines:
        values = list(map(int, line.split()))
        require(values and values[-1] == 0, 'Clause terminator')
        require(all(0 < abs(v) <= variables for v in values[:-1]), 'Literal range')
        clauses.append(canon(values[:-1]))
    require(len(clauses) == count, 'Clause count')
    return clauses


def conflict_by_scan(formula, assumptions):
    # Deliberately different from the author's occurrence-index counter.
    # Repeated whole-clause scans implement ordinary unit propagation.
    assignment = {}
    for literal in assumptions:
        v, value = abs(literal), literal > 0
        if v in assignment and assignment[v] != value:
            return True
        assignment[v] = value
    while True:
        changed = False
        for clause in formula:
            if any(abs(lit) in assignment and assignment[abs(lit)] == (lit > 0)
                   for lit in clause):
                continue
            free = [lit for lit in clause if abs(lit) not in assignment]
            if not free:
                return True
            if len(free) == 1:
                lit = free[0]
                assignment[abs(lit)] = lit > 0
                changed = True
        if not changed:
            return False


def rup_audit(core, proof):
    formula = list(core)
    require(len(core) == 777 and len(proof) == 119 and proof[-1] == (), 'Certificate dimensions')
    for step, clause in enumerate(proof):
        require(conflict_by_scan(formula, [-lit for lit in clause]), 'Non-RUP step ' + str(step + 1))
        formula.append(clause)
    return {'RUP_additions': len(proof), 'final_empty_clause': True,
            'distinct_core_variables': len({abs(lit) for clause in core for lit in clause})}


def rejected(action):
    try:
        action()
    except ValueError:
        return True
    raise ValueError('A deliberately invalid control was accepted')


def cut_sharpness_controls():
    checks = 0
    for n in range(4, 13):
        for i, j in combinations(range(n - 2), 2):
            word = [(i, n - 2), (j, n - 1), (n - 2, n - 1)]
            for x in [1 << (n - 2), (1 << i) | (1 << j)]:
                require(trajectory(word, x)[0] == sorted_mask(n, x.bit_count()), 'Cut construction')
                checks += 1
    return checks


def derive(target):
    for name, expected in INPUT_HASHES.items():
        require(hashlib.sha256((target/name).read_bytes()).hexdigest() == expected, 'Input hash ' + name)
    fixture = json.loads((target/'fixture.json').read_text())
    certificate = json.loads((target/'certificate.json').read_text())
    p25, states, result = image_check(fixture, certificate)
    result.update(witness_check(p25, certificate))
    core, proof = read_clauses(target/'Z19-core.cnf', True), read_clauses(target/'Z19-proof.rup')
    result['semantic_core'] = semantic_audit(certificate, core)
    result['RUP'] = rup_audit(core, proof)
    # Complete small truth-assignment soundness controls for the scan checker.
    possible = [canon([lit for lit in (a, b) if lit])
                for a in (-1, 0, 1) for b in (-2, 0, 2)]
    tested = 0
    for bits in range(1 << len(possible)):
        formula = [clause for i, clause in enumerate(possible) if bits >> i & 1]
        for candidate in possible:
            answer = conflict_by_scan(formula, [-lit for lit in candidate])
            satisfiable = any(all(any((bool(mask >> (abs(lit) - 1) & 1)) == (lit > 0)
                                      for lit in clause) for clause in formula + [(-lit,) for lit in candidate])
                              for mask in range(4))
            require(not answer or not satisfiable, 'Unsound unit propagation')
            tested += 1
    result['unit_propagation_truth_controls'] = tested
    # A false empty proof, a foreign semantic clause and a changed deletion
    # count all fail. They do not assert SAT after deleting arbitrary clauses.
    controls = [rejected(lambda: require(conflict_by_scan(core, []), 'Premature empty clause')),
                rejected(lambda: semantic_audit(certificate, core + [(40894,)])),
                rejected(lambda: require(trajectory(p25, 46)[1] == 16, 'Wrong cut budget'))]
    require(all(controls), 'Negative controls')
    result['rejected_controls'] = len(controls)
    result['abstract_cut_sharpness_controls'] = cut_sharpness_controls()
    result['input_hashes'] = INPUT_HASHES
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target-dir', type=Path,
                        default=Path(__file__).resolve().parent.parent/'thirteen_endpoint_frontier')
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    result = derive(args.target_dir)
    if args.expected:
        require(result == json.loads(args.expected.read_text()), 'Independent expected output differs')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
