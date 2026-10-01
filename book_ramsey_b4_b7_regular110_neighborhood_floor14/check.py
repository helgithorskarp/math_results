"""Generator-free binary-row/single-edge audit, author six-books-3, researcher.

census.py copies our previous independently implemented local-core checker.
Default verification imports neither generate.py nor core.py.
"""
from itertools import combinations
from math import gcd
from pathlib import Path
import argparse
import hashlib
import json
import census as c

HERE = Path(__file__).resolve().parent


def selected_pairs(mask, stars):
    s = c.formula(mask, stars)
    candidates = []
    for word in range(1 << 10):
        if word.bit_count() != 5:
            continue
        row = tuple(i for i in range(10) if word >> i & 1)
        if all(s[i][j] > 0 for i, j in combinations(row, 2)):
            candidates.append(row)
    candidates.sort()
    for position, left in enumerate(candidates):
        for right in candidates[position:]:
            x = [int(i in left) for i in range(10)]
            y = [int(i in right) for i in range(10)]
            base = [[s[i][j] - x[i] * x[j] - y[i] * y[j] for j in range(10)] for i in range(10)]
            if any(value < 0 for row in base for value in row):
                continue
            degrees = [sum(row) - 4 * row[i] for i, row in enumerate(base)]
            c.need(min(degrees) >= 0 and sum(degrees) == 18, 'invalid independently derived slack degree')
            yield list(left), list(right), base, degrees


def integer_form(vector):
    positions = [i for i in range(10) if vector[i] != 0]
    return [(i, i, vector[i] * vector[i]) for i in positions] + [
        (i, j, 2 * vector[i] * vector[j]) for i, j in combinations(positions, 2)]


def is_negative(matrix, form):
    answer = 0
    for i, j, coefficient in form:
        answer += coefficient * matrix[i][j]
    return answer < 0


def validate_certificate(cert, profiles):
    c.need(cert.get('dimension') == 10, 'wrong certificate dimension')
    vectors, declared = cert.get('vectors'), cert.get('profiles')
    c.need(isinstance(vectors, list) and isinstance(declared, list), 'malformed certificate')
    c.need(len(declared) == len(profiles), 'wrong profile certificate count')
    for v in vectors:
        c.need(isinstance(v, list) and len(v) == 10 and all(type(x) is int for x in v), 'invalid integer vector')
        c.need(any(v) and gcd(*v) == 1 and next(x for x in v if x) > 0, 'nonprimitive or zero vector')
    c.need(len(vectors) == len({tuple(v) for v in vectors}), 'duplicate global integer vector')
    for i, rec in enumerate(declared):
        c.need(rec.get('index') == i and isinstance(rec.get('vector_indices'), list), 'malformed profile pool')
        ids = rec['vector_indices']
        c.need(all(type(k) is int and 0 <= k < len(vectors) for k in ids), 'out-of-range witness index')
        c.need(len(ids) == len(set(ids)) == profiles[i]['profile_vectors'], 'profile pool count mismatch')


def residual(base, degrees, edges):
    used = [0] * 10
    r = [row[:] for row in base]
    for i, j, weight in edges:
        c.need(type(weight) is int and 0 <= i < j < 10 and 0 < weight <= base[i][j], 'invalid literal slack edge')
        used[i] += weight
        used[j] += weight
        r[i][j] -= weight
        r[j][i] -= weight
    c.need(used == degrees, 'literal slack degrees disagree')
    c.need(all(sum(row) == 4 * row[i] for i, row in enumerate(r)), 'literal residual row sums disagree')
    c.need(min(value for row in r for value in row) >= 0, 'negative literal residual entry')
    return r


def run(compare=False, progress=None):
    expected = json.loads((HERE / 'expected.json').read_text())
    cert_bytes = (HERE / 'negative_vectors.json').read_bytes()
    c.need(hashlib.sha256(cert_bytes).hexdigest() == expected['negative_vectors_sha256'], 'certificate byte hash mismatch')
    cert = json.loads(cert_bytes)
    profiles = expected['profiles']
    validate_certificate(cert, profiles)
    observed, stats = c.census(expected)
    keys = [(p['F_mask'], tuple(tuple(s) for s in p['stars'])) for p in profiles]
    c.need(len(keys) == len(set(keys)) and set(keys) == set(observed), 'new profile domain differs from the complete local census')
    c.need([p['index'] for p in profiles] == list(range(len(profiles))), 'wrong profile index order')
    forms = [integer_form(v) for v in cert['vectors']]
    stats.update({'agent': 'six-books-3', 'role': 'researcher', 'completed_profiles': 0,
                  'row_pairs': 0, 'states': 0, 'negative_forms': 0,
                  'residual_entries_compared': 0, 'generator_comparison': compare})
    print(json.dumps(stats, sort_keys=True), flush=True)
    if compare:
        import generate
    whole_hash, pair_hash = hashlib.sha256(), hashlib.sha256()
    for profile, rec in zip(profiles, cert['profiles']):
        index, mask, stars = profile['index'], profile['F_mask'], profile['stars']
        pairs = list(selected_pairs(mask, stars))
        c.need(len(pairs) == profile['row_pairs'], 'five-row-pair census mismatch')
        if compare:
            genpairs = list(generate.row_pairs(mask, stars))
            c.need([(a, b) for a, b, base, d in pairs] == [(a, b) for a, b, base in genpairs],
                   'complete five-row-pair sets differ')
        pairs_digest, matrices_digest = hashlib.sha256(), hashlib.sha256()
        pool = rec['vector_indices']
        preferred = None
        count = 0
        for position, (left, right, base, degrees) in enumerate(pairs):
            data = (json.dumps([mask, stars, left, right], separators=(',', ':')) + '\n').encode()
            pair_hash.update(data)
            pairs_digest.update(data)
            states = sorted(c.single_edge_weights(degrees, base))
            c.need(len(states) == len(set(states)), 'duplicate independent weighted state')
            if compare:
                genbase = genpairs[position][2]
                gendeg = generate.degrees(mask, left, right)
                c.need(base == genbase and degrees == gendeg, 'base/incident-degree entries differ')
                genstates = sorted(generate.core.weighted_stars(gendeg, genbase))
                c.need(states == genstates, 'complete slack-state sets differ')
            for edges in states:
                r = residual(base, degrees, edges)
                found = preferred if preferred is not None and is_negative(r, forms[preferred]) else None
                if found is None:
                    found = next((k for k in pool if is_negative(r, forms[k])), None)
                c.need(found is not None, 'residual matrix lacks a strict negative-form certificate')
                preferred = found
                if compare:
                    c.need(r == generate.matrix(genbase, edges), 'complete residual matrix entries differ')
                    stats['residual_entries_compared'] += 100
                data = (json.dumps([index, left, right, edges, r], separators=(',', ':')) + '\n').encode()
                matrices_digest.update(data)
                whole_hash.update(data)
                count += 1
            stats['row_pairs'] += 1
        c.need(count == profile['states'], 'profile state count mismatch')
        c.need(pairs_digest.hexdigest() == profile['row_pairs_sha256'], 'profile selected-pair hash mismatch')
        c.need(matrices_digest.hexdigest() == profile['state_matrix_sha256'], 'profile full-matrix hash mismatch')
        stats['states'] += count
        stats['negative_forms'] += count
        stats['completed_profiles'] += 1
        print(json.dumps(stats, sort_keys=True), flush=True)
        if progress:
            Path(progress).write_text(json.dumps(dict(stats, complete=False), indent=2) + '\n')
    c.need(stats['row_pairs'] == expected['row_pairs'] and stats['states'] == expected['states'], 'complete-domain totals disagree')
    c.need(whole_hash.hexdigest() == expected['state_matrix_sha256'], 'complete matrix stream differs')
    c.need(pair_hash.hexdigest() == expected['row_pairs_sha256'], 'complete selected-pair stream differs')
    c.need(len(cert['vectors']) == expected['unique_vectors'] and max(abs(x) for v in cert['vectors'] for x in v) ==
           expected['max_absolute_vector_entry'], 'certificate statistics disagree')
    stats.update({'complete': True, 'survivors': 0, 'baseline': c.baseline(),
                  'state_matrix_sha256': whole_hash.hexdigest(), 'unique_vectors': len(cert['vectors'])})
    if progress:
        Path(progress).write_text(json.dumps(stats, indent=2) + '\n')
    return stats


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--compare-generator', action='store_true')
    parser.add_argument('--progress', help='private checkpoint path outside the publication directory')
    args = parser.parse_args()
    print(json.dumps(run(args.compare_generator, args.progress), sort_keys=True), flush=True)
