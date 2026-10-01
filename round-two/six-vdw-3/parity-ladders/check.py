#!/usr/bin/env python3
"""Definition-level checks; imports neither the model generator nor a solver."""

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path


def demand(condition, message):
    if not condition:
        raise ValueError(message)


def cyclic_obstruction(bits):
    """Check every cyclic start and nonzero step, by bit intersections.

    Reversal pairs d with n-d. Bit j records coordinate j. Right cyclic
    rotation by jd aligns the AP's j-th term with its start coordinate.
    """
    n = len(bits)
    demand(n > 0 and all(bit in (0, 1) for bit in bits), 'malformed word')
    all_bits = (1 << n) - 1
    colors = [sum(bit << i for i, bit in enumerate(bits))]
    colors.append(colors[0] ^ all_bits)
    for d in range(1, n // 2 + 1):
        masks = colors.copy()
        for j in range(1, 7):
            shift = (j * d) % n
            for b in range(2):
                rotated = colors[b] if shift == 0 else (
                    (colors[b] >> shift)
                    | ((colors[b] << (n - shift)) & all_bits))
                masks[b] &= rotated
        for b, mask in enumerate(masks):
            if mask:
                a = (mask & -mask).bit_length() - 1
                return a, d, 1 - b
    return None


def interval_obstruction(bits):
    """Independent nonwrapping interval bit-intersection checker."""
    n = len(bits)
    demand(n > 0 and all(bit in (0, 1) for bit in bits), 'malformed word')
    red = sum(bit << i for i, bit in enumerate(bits))
    blue = red ^ ((1 << n) - 1)
    count = 0
    for d in range(1, (n - 1) // 6 + 1):
        count += n - 6 * d
        for color, word in enumerate((blue, red)):
            starts = word
            for j in range(1, 7):
                starts &= word >> (j * d)
            if starts:
                a = (starts & -starts).bit_length() - 1
                return (a + 1, d, color), count
    return None, count


def product(u):
    q = len(u)
    # Literal column 000111, with y=0 at the least significant bit.
    return [u[t % q] ^ ((56 >> (t % 6)) & 1) for t in range(6 * q)]


def ladder_obstruction(u):
    q = len(u)
    # Full directed field domain, different from generator representatives.
    for a in range(q):
        for r in range(1, q):
            parities = [u[(a + j*r) % q] ^ u[(a + (j+3)*r) % q]
                        for j in range(4)]
            if parities == [parities[0]] * 4:
                return a, r
    return None


def local_equivalence():
    patterns = {tuple((56 >> ((b + j*s) % 6)) & 1 for j in range(7))
                for b in range(6) for s in range(6)}
    demand(len(patterns) == 16, 'local pattern count')
    for bits in itertools.product(range(2), repeat=7):
        differences = [bits[j] ^ bits[j + 3] for j in range(4)]
        forbidden = differences == [differences[0]] * 4
        demand(forbidden == (bits in patterns), 'local equivalence')
    for s in range(1, 6):
        for b in range(6):
            colors = {(56 >> ((b + j*s) % 6)) & 1 for j in range(7)}
            demand(colors == {0, 1}, 'r=0 cyclic step')
    return {'seven_bit_assignments': 128, 'distinct_patterns': 16,
            'zero_field_step_cases': 30}


def parse_dimacs(text):
    lines = text.splitlines()
    demand(bool(lines), 'missing model')
    header = lines[0].split()
    demand(len(header) == 4 and header[:2] == ['p', 'cnf'], 'bad header')
    variables, count = map(int, header[2:])
    demand(variables > 0 and count >= 0, 'bad model size')
    rows = []
    for line in lines[1:]:
        tokens = [int(token) for token in line.split()]
        demand(bool(tokens) and tokens[-1] == 0, 'bad clause terminator')
        row = tuple(tokens[:-1])
        demand(bool(row), 'unexpected empty clause')
        demand(all(1 <= abs(v) <= variables for v in row), 'literal range')
        demand(len(set(row)) == len(row), 'duplicate literal')
        demand(all(-v not in row for v in row), 'tautology')
        demand(tuple(sorted(row, key=abs)) == row, 'literal ordering')
        rows.append(row)
    demand(len(rows) == count and len(set(rows)) == count, 'clause coverage')
    demand(rows == sorted(rows), 'clause ordering')
    return variables, set(rows)


def audit_model(text, q):
    variables, actual = parse_dimacs(text)
    demand(variables == q * (q - 1) // 2, 'edge-variable count')

    def label(x, y):
        demand(x != y, 'loop edge')
        x, y = min(x, y), max(x, y)
        return x * (2*q-x-1) // 2 + y-x

    expected = set()
    # Direct Boolean equivalence z=(a XOR b), not generator truth tables.
    for x in range(1, q):
        for y in range(x + 1, q):
            a, b, z = x, y, label(x, y)
            expected.update(((a, b, -z), (a, -b, z),
                             (-a, b, z), (-a, -b, -z)))
    gates = len(expected)
    ladders = set()
    # Include both r and -r, then deduplicate entire clauses.
    for r in range(1, q):
        for a in range(q):
            edges = tuple(sorted(label((a+j*r) % q, (a+(j+3)*r) % q)
                                 for j in range(4)))
            demand(len(set(edges)) == 4, 'repeated ladder edge')
            ladders.add(edges)
            expected.add(edges)
            expected.add(tuple(-v for v in edges))
    demand(actual == expected, 'entry-level model mismatch')
    return {'q': q, 'variables': variables, 'clauses': len(actual),
            'xor_cnf_clauses': gates, 'distinct_ladders': len(ladders),
            'sha256': hashlib.sha256(text.encode('ascii')).hexdigest()}


def direct_cyclic_check(bits):
    for a in range(len(bits)):
        for d in range(1, len(bits)):
            colors = [bits[(a + j*d) % len(bits)] for j in range(7)]
            if colors == [colors[0]] * 7:
                return a, d
    return None


def exhaustive_small():
    counts = []
    for q in (7, 11, 13, 17):
        survivors = 0
        comparisons = 0
        for tail in itertools.product(range(2), repeat=q - 1):
            u = [0, *tail]
            # Compare each individual word, rather than aggregate counts.
            cyclic = cyclic_obstruction(product(u))
            ladder = ladder_obstruction(u)
            demand((cyclic is None) == (ladder is None), 'word equivalence')
            survivors += int(cyclic is None)
            comparisons += 1
        counts.append({'q': q, 'normalized_words': comparisons,
                       'survivors': survivors})
    return counts


def derivative_cut_fixture(q):
    demand(q >= 23 and q % 4 == 3 and math.gcd(q, 6) == 1,
           'wrong extremal domain')
    minority = [int(x % 4 == 0) for x in range(q)]
    # Exactly the extremal run pattern, including its shortened final gap.
    for flip in range(2):
        v = [b ^ flip for b in minority]
        for j in range(4):
            demand(sum(v[4*j+3*l] for l in range(4)) % 2 == 1,
                   'telescoping obstruction')
    return minority


def integrate_difference(v, h):
    q = len(v)
    demand(math.gcd(q, h) == 1, 'nongenerating integration step')
    u = [None] * q
    u[0] = 0
    x = 0
    for _ in range(q):
        y = (x + h) % q
        bit = u[x] ^ v[x]
        if u[y] is not None:
            demand(u[y] == bit, 'inconsistent cyclic derivative')
        else:
            u[y] = bit
        x = y
    demand(all(bit is not None for bit in u), 'incomplete integration')
    return u


def extremal_controls():
    # Both derivative color orientations are checked; only even-weight
    # derivatives integrate, and a complement word has the same derivative.
    cases = [q for q in range(23, 200, 4) if math.gcd(q, 6) == 1]
    for q in cases:
        derivative_cut_fixture(q)
    v = derivative_cut_fixture(103)
    u = integrate_difference(v, 3)
    demand(sum(v) == 26, '103 extremal derivative weight')
    colors = product(u)
    progression = (231, 305)
    actual = [colors[(progression[0] - 1 + j*progression[1]) % 618]
              for j in range(7)]
    demand(actual == [0] * 7, 'actual product obstruction')
    demand(progression[0] + 6*progression[1] <= 3704, 'interval bridge')
    return {'checked_q_values': cases, 'extremal_q': 103,
            'derivative_ones': 26, 'orientation_ones': sum(u),
            'integer_ap_start': progression[0],
            'integer_ap_step': progression[1], 'integer_ap_color': 0}


def incumbent():
    p = 617
    squares = {x*x % p for x in range(1, p)}
    # The established seed, reconstructed without importing a fixture.
    bits = [0 if x % p == 0 or x % p in squares else 1 for x in range(3703)]
    bits[-1] = 1
    obstruction, coverage = interval_obstruction(bits)
    demand(obstruction is None and coverage == 1140833, 'incumbent check')
    text = ''.join(map(str, bits)) + '\n'
    # Two direct checker controls detect known monochromatic APs.
    demand(interval_obstruction([0] * 7)[0] == (1, 1, 0), 'interval control')
    demand(cyclic_obstruction([1] * 13) is not None, 'cyclic control')
    # A full term-by-term algorithm checks the small positive boundary case.
    q7 = product([0] + [1] * 6)
    demand(direct_cyclic_check(q7) is None, 'q7 direct positive control')
    demand(cyclic_obstruction(q7) is None, 'q7 bit control')
    return {'length': len(bits), 'integer_aps': coverage,
            'sha256_with_newline': hashlib.sha256(text.encode('ascii')).hexdigest()}


def check_fixture(path):
    data = json.loads(path.read_text())
    demand(set(data) == {'q', 'orientation'}, 'bad fixture fields')
    q, text = data['q'], data['orientation']
    demand(isinstance(q, int) and isinstance(text, str), 'bad fixture types')
    demand(len(text) == q and set(text) <= {'0', '1'}, 'bad fixture word')
    u = [int(c) for c in text]
    bits = product(u)
    demand(direct_cyclic_check(bits) is None, 'fixture is cyclically invalid')
    demand(cyclic_obstruction(bits) is None and ladder_obstruction(u) is None,
           'fixture checker disagreement')
    distances = [sum(u[x] ^ u[(x+h) % q] for x in range(q))
                 for h in range(1, q)]
    return {'q': q, 'orientation_ones': sum(u), 'cyclic_pairs': len(bits)*(len(bits)-1),
            'minimum_distance': min(distances), 'maximum_distance': max(distances)}


def run(model_path, fixture_path):
    model_text = model_path.read_text(encoding='ascii')
    result = {
        'status': 'VERIFIED_PARITY_LADDER_REDUCTION_AND_DERIVATIVE_CUTS',
        'local': local_equivalence(),
        'model103': audit_model(model_text, 103),
        'small_word_equivalence': exhaustive_small(),
        'extremal_run_controls': extremal_controls(),
        'q23_fixture': check_fixture(fixture_path),
        'incumbent': incumbent(),
        'excluded_biased103_orientations': 2*sum(math.comb(103, j) for j in range(17)),
        'm17_minimum_floor_shifts': 68,
    }
    controls = 0
    original = model_text.splitlines()
    malformed = [
        '\n'.join(original[1:]) + '\n',
        '\n'.join(original[:-1]) + '\n',
        model_text.replace('p cnf 5253 ', 'p cnf 5252 ', 1),
        model_text + original[1] + '\n',
        'p cnf 5253 1\n1 -1 0\n',
        'p cnf 5253 1\n1 0\n',
    ]
    for bad in malformed:
        try:
            audit_model(bad, 103)
        except (ValueError, IndexError):
            controls += 1
        else:
            raise ValueError('invalid model accepted')
    result['rejected_model_corruptions'] = controls
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, required=True)
    parser.add_argument('--fixture', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.model, args.fixture), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
