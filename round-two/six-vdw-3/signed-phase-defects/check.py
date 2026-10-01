#!/usr/bin/env python3
"""Independent exact local, incidence, normalization and complete CNF audit.

Imports neither the generator nor a solver. Local phases use literal six-bit
columns; cut labels use a closed index formula. All checks survive Python -O.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path


# In increasing y order: f(y), f(y-1), f(y+1).
COLUMNS = {0: (0, 0, 0, 1, 1, 1),
           1: (1, 0, 0, 0, 1, 1),
           -1: (0, 0, 1, 1, 1, 0)}
F = {w for w in range(128)
     if len({((w >> j) ^ (w >> (j+3))) & 1 for j in range(4)}) == 1}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_patterns(theta):
    return {sum(COLUMNS[t][(b+j*s) % 6] << j for j, t in enumerate(theta))
            for b in range(6) for s in range(6)}


def punctures(patterns, k):
    grouped = defaultdict(set)
    for w in patterns:
        grouped[w & ~(1 << k)].add((w >> k) & 1)
    return {w for w, values in grouped.items() if len(values) == 2}


def local_audit():
    require(len(F) == 16, 'Three-place code size')
    require(local_patterns([0]*7) == F, 'Literal columns/code disagreement')
    missing = Counter()
    no_conflict = 0
    witness_checks = 0
    for theta in itertools.product((-1, 0, 1), repeat=7):
        patterns = local_patterns(theta)
        require({w ^ 127 for w in patterns} == patterns, 'Complement closure')
        missing[len(F - patterns)] += 1
        conflict = any(theta[j] and theta[k] and
                       ((theta[j] == theta[k]) != ((k-j) % 3 == 0))
                       for j in range(7) for k in range(j+1, 7))
        if conflict:
            continue
        no_conflict += 1
        require(F <= patterns, 'No-conflicting-pair dominance')
        for w in F:
            p = ((w >> 0) ^ (w >> 3)) & 1
            realizations = []
            for b in range(6):
                for s in range(p, 6, 2):
                    original = [COLUMNS[0][(b+j*s) % 6] for j in range(7)]
                    shifted = [COLUMNS[t][(b+j*s) % 6] for j, t in enumerate(theta)]
                    if sum(v << j for j, v in enumerate(original)) == w and original == shifted:
                        realizations.append((b, s))
            require(realizations, 'Written proof stable realization')
            witness_checks += 1
    require(no_conflict == 129, 'No-conflict vector count')
    # Validate the boundary/reflection argument for every nontrivial slope.
    boundary_checks = 0
    for s in (1, 2, 4, 5):
        for b in range(6):
            values = [(b+j*s) % 6 for j in range(3)]
            plus = [j for j, y in enumerate(values) if y in (0, 3)]
            minus = [j for j, y in enumerate(values) if y in (2, 5)]
            require(len(plus) == len(minus) == 1 and plus != minus, 'Distinct boundary classes')
            reflected = [(2-y) % 6 for y in values]
            require([COLUMNS[0][y] for y in values] ==
                    [COLUMNS[0][y] for y in reflected], 'Color reflection')
            require([j for j, y in enumerate(reflected) if y in (0, 3)] == minus,
                    'Reflection swaps boundary classes')
            boundary_checks += 1
    single = {}
    for k in range(7):
        theta = [int(j == k) for j in range(7)]
        patterns = local_patterns(theta)
        require(patterns == local_patterns([-t for t in theta]), 'Exception-sign equivalence')
        ps = punctures(patterns, k)
        require(len(patterns) == 28 and F <= patterns and len(ps) == 12,
                'One-exception local counts')
        for w in range(128):
            parities = {((w >> j) ^ (w >> (j+3))) & 1 for j in range(4)}
            valid = len(parities) == 2 and (w & ~(1 << k)) not in ps
            require(valid == (w not in patterns), 'Cut-and-puncture truth table')
        single[k] = (patterns, ps)
    pair_table = Counter()
    for j, k in itertools.combinations(range(7), 2):
        for sign in (-1, 1):
            theta = [0]*7
            theta[j], theta[k] = 1, sign
            lost = len(F - local_patterns(theta))
            same_class = (k-j) % 3 == 0
            expected = (0 if same_class else 4) if sign == 1 else (8 if same_class else 0)
            require(lost == expected, 'Sharp local pair carrier classification')
            pair_table[('same' if sign == 1 else 'opposite', same_class, lost)] += 1
    return single, {
        'ternary_vectors': 2187, 'nonconflicting_vectors': no_conflict,
        'missing_F_histogram': dict(sorted(missing.items())),
        'stable_realizations_checked': witness_checks,
        'boundary_reflections_checked': boundary_checks,
        'one_exception_truth_assignments': 7*128,
        'pair_table': [{'signs': s, 'same_index_class': c, 'missing_F_words': m,
                       'position_pairs': count}
                      for (s, c, m), count in sorted(pair_table.items())],
    }


def edge_label(q, x, y):
    if x > y:
        x, y = y, x
    require(x < y, 'Cut loop')
    return x*(2*q-x-1)//2 + y-x


def read_model(path):
    rows = path.read_text(encoding='ascii').splitlines()
    header = rows[0].split()
    require(len(header) == 4 and header[:2] == ['p', 'cnf'], 'Model header')
    n, m = map(int, header[2:])
    require(len(rows) == m+1, 'Model coverage')
    clauses = set()
    for line in rows[1:]:
        tokens = list(map(int, line.split()))
        require(tokens and tokens[-1] == 0 and 0 not in tokens[:-1], 'Model terminator')
        row = tuple(tokens[:-1])
        require(all(1 <= abs(v) <= n for v in row), 'Model literal range')
        require(len(set(row)) == len(row) and not any(-v in row for v in row),
                'Duplicate or tautological literals')
        require(row == tuple(sorted(row, key=abs)), 'Model row ordering')
        require(row not in clauses, 'Duplicate model clause')
        clauses.add(row)
    return n, clauses


def model_audit(path, single, q=103):
    n, actual = read_model(path)
    require(n == q*(q-1)//2, 'Cut variable coverage')
    expected = set()
    for x in range(1, q):
        for y in range(x+1, q):
            z = edge_label(q, x, y)
            expected.update(((x, y, -z), (x, -y, z), (-x, y, z), (-x, -y, -z)))
    gates = len(expected)
    ladders, exceptions, supports = set(), set(), set()
    point_degrees = Counter()
    pair_degrees = Counter()
    # Both orientations, unlike the generator's half-step loop.
    for r in range(1, q):
        for a in range(q):
            points = tuple((a+j*r) % q for j in range(7))
            vertices = tuple(sorted(points))
            supports.add(vertices)
            ladder = tuple(sorted(edge_label(q, points[j], points[j+3]) for j in range(4)))
            ladders.add(ladder)
            expected.add(ladder)
            expected.add(tuple(-v for v in ladder))
            if 0 in points:
                exceptions.add(vertices)
                k = points.index(0)
                for w in single[k][1]:
                    clause = tuple(sorted(((-x if (w >> j) & 1 else x)
                                           for j, x in enumerate(points) if x), key=abs))
                    expected.add(clause)
    require(len(supports) == len(ladders) == q*(q-1)//2, 'Support/reversal uniqueness')
    for vertices in supports:
        point_degrees.update(vertices)
        pair_degrees.update(itertools.combinations(vertices, 2))
    require(set(point_degrees.values()) == {7*(q-1)//2}, 'Point incidence')
    require(len(pair_degrees) == q*(q-1)//2 and set(pair_degrees.values()) == {21},
            'Complete pair incidence')
    require(actual == expected, 'Entire model clause set differs')
    require(len(exceptions) == 7*(q-1)//2, 'Exceptional support incidence')
    # The 21 position-pair constructions through the fixed field pair (0,1).
    through_pair = {}
    for j, k in itertools.combinations(range(7), 2):
        r = pow(k-j, -1, q)
        a = (-j*r) % q
        vertices = tuple(sorted((a+l*r) % q for l in range(7)))
        require(vertices in supports and vertices not in through_pair, 'Pair-index support cover')
        through_pair[vertices] = (k-j) % 3 == 0
    require(Counter(through_pair.values()) == {False: 16, True: 5}, '16/5 pair classes')
    return {'q': q, 'variables': n, 'clauses': len(actual),
            'xor_clauses': gates, 'ladders': len(ladders),
            'puncture_clauses': len(actual)-gates-2*len(ladders),
            'exceptional_supports': len(exceptions),
            'field_pairs_with_21_supports': len(pair_degrees),
            'model_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def cyclic_count(colors):
    n = len(colors)
    mask = (1 << n)-1
    ones = sum(v << i for i, v in enumerate(colors))
    total = 0
    for d in range(1, n):
        for colored in (ones, mask ^ ones):
            intersection = colored
            for j in range(1, 7):
                shift = j*d % n
                rotated = colored if shift == 0 else (
                    (colored >> shift) | ((colored << (n-shift)) & mask))
                intersection &= rotated
            total += intersection.bit_count()
    return total


def finite_controls():
    results = []
    witness_checks = positive_checks = 0
    positive_fixture = None
    for q in (7, 13):
        patterns = []
        for r in range(1, q):
            for a in range(q):
                points = [(a+j*r) % q for j in range(7)]
                patterns.append((a, r, points, local_patterns([int(x == 0) for x in points])))
        valid_counts = [0, 0]
        for encoded in range(1 << (q-1)):
            word = encoded << 1  # all and only complement-normalized orientations
            for exception in (0, 1):
                theta = [exception] + [0]*(q-1)
                colors = [((word >> (t % q)) & 1) ^ COLUMNS[theta[t % q]][t % 6]
                          for t in range(6*q)]
                obstruction = None
                for a, r, points, G in patterns:
                    restriction = sum(((word >> x) & 1) << j for j, x in enumerate(points))
                    if restriction in (G if exception else F):
                        obstruction = (a, r, points)
                        break
                if obstruction is None:
                    require(cyclic_count(colors) == 0, 'Positive control has actual cyclic obstruction')
                    positive_checks += 1
                    valid_counts[exception] += 1
                    if q == 7 and exception and positive_fixture is None:
                        positive_fixture = ''.join(str((word >> x) & 1) for x in range(q))
                else:
                    a, r, points = obstruction
                    actual = None
                    for b in range(6):
                        for s in range(6):
                            values = [((word >> x) & 1) ^ COLUMNS[theta[x]][(b+j*s) % 6]
                                      for j, x in enumerate(points)]
                            if len(set(values)) == 1:
                                actual = (b, s, values[0])
                                break
                        if actual:
                            break
                    require(actual is not None, 'Failed local test lacks actual CRT obstruction')
                    b, s, color = actual
                    start = a + q*((b-a)*pow(q, -1, 6) % 6)
                    step = r + q*((s-r)*pow(q, -1, 6) % 6)
                    require(step and all(colors[(start+j*step) % (6*q)] == color for j in range(7)),
                            'Decoded obstruction has wrong colors or zero step')
                    witness_checks += 1
        require(valid_counts == ([21, 8] if q == 7 else [52, 0]), 'Finite orientation coverage changed')
        results.append({'q': q, 'normalized_orientations': 1 << (q-1),
                        'valid_separable': valid_counts[0], 'valid_one_exception': valid_counts[1]})
    return {'complete_enumerations': results, 'actual_negative_witnesses': witness_checks,
            'actual_positive_cyclic_checks': positive_checks,
            'positive_q7_one_exception': positive_fixture,
            'q7_period': 42, 'q7_fixture_is_not_a_length3704_witness': True}


def normalization_audit(q=103):
    truth_checks = 0
    for tau in range(3):
        for u in (0, 1):
            theta = -1 if tau == 2 else tau
            v = u ^ int(tau == 2)
            for y in range(6):
                original = u ^ COLUMNS[0][(y-tau) % 6]
                require(original == v ^ COLUMNS[theta][y], 'Nearest-phase orientation carry')
                truth_checks += 1
    translated_truth = 0
    for baseline in range(3):
        for tau in range(3):
            for u in (0, 1):
                phi = (tau+3*u-baseline) % 6
                theta = -1 if phi % 3 == 2 else phi % 3
                v = phi//3 ^ int(phi % 3 == 2)
                for y in range(6):
                    require(COLUMNS[0][(y+baseline-tau-3*u) % 6] ==
                            v ^ COLUMNS[theta][y], 'Baseline translation carry')
                    translated_truth += 1
    skeletons = set()
    for baseline in range(3):
        for position in range(q):
            for changed in range(3):
                if changed == baseline:
                    continue
                tau = [baseline]*q
                tau[position] = changed
                skeletons.add(tuple(tau))
                shifted = [(tau[(x+position) % q]-baseline) % 3 for x in range(q)]
                require(shifted[0] in (1, 2) and shifted[1:] == [0]*(q-1), 'One-exception skeleton cover')
    require(len(skeletons) == 6*q, 'Raw one-exception skeleton count')
    # All CRT points for field translations and the sign-changing y reflection.
    crt_checks = 0
    multiplier = 1 + q*((-2)*pow(q, -1, 6) % 6)
    require(math.gcd(multiplier, 6*q) == 1, 'CRT reflection multiplier is not a unit')
    for position in range(q):
        offset = position + q*((2-position)*pow(q, -1, 6) % 6)
        for t in range(6*q):
            transformed = (t+position) % q + q*((2-t-(t+position) % q)*pow(q, -1, 6) % 6)
            require(transformed % q == (t+position) % q and transformed % 6 == (2-t) % 6,
                    'CRT translation/reflection coordinates')
            require(transformed == (multiplier*t+offset) % (6*q), 'CRT map is not affine')
            require(COLUMNS[0][(2-(t % 6)) % 6] == COLUMNS[0][t % 6], 'Reflection preserves f')
            crt_checks += 1
    return {'one_exception_skeletons': len(skeletons),
            'nearest_phase_truth_entries': truth_checks, 'CRT_coordinate_entries': crt_checks,
            'baseline_translation_truth_entries': translated_truth,
            'normalized_orientations_per_skeleton': str(1 << (q-1))}


def corruption_controls(path, single):
    original = path.read_text()
    rows = original.splitlines()
    altered = rows.copy()
    altered[-1] = altered[-1].replace(' 0', ' 1 0')
    cases = ['\n'.join(rows[:-1])+'\n', '\n'.join(altered)+'\n',
             original.replace('p cnf 5253', 'p cnf 5252', 1)]
    target = path.with_name('corrupted-model.cnf')
    for text in cases:
        target.write_text(text)
        try:
            model_audit(target, single)
        except (ValueError, IndexError):
            pass
        else:
            raise ValueError('Corrupted model accepted')
    target.unlink()
    return len(cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    single, local = local_audit()
    result = {'status': 'EXACT_SIGNED_DEFECT_MODEL_VERIFIED', 'local': local,
              'model': model_audit(args.model, single), 'normalization': normalization_audit(),
              'finite_controls': finite_controls()}
    if args.controls:
        result['model_corruptions_rejected'] = corruption_controls(args.model, single)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
