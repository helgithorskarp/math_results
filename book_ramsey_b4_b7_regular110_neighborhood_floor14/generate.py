"""Exact two-five-row exclusion generator. Actual author six-books-3, researcher.

core.py reuses our explicit local census, weighted-star enumeration and
exact congruence routine. No solver, float, or external graph catalogue.
"""
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import argparse
import hashlib
import json
import core

HERE = Path(__file__).resolve().parent


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def certificate_bytes(vectors, profiles):
    return ('{\n"dimension":10,\n"vectors":[\n' +
            ',\n'.join(json.dumps(v, separators=(',', ':')) for v in vectors) +
            '\n],\n"profiles":[\n' +
            ',\n'.join(json.dumps(p, separators=(',', ':')) for p in profiles) + '\n]\n}\n').encode()


def sparse_form(vector):
    nz = [i for i, x in enumerate(vector) if x]
    return [(i, i, vector[i] ** 2) for i in nz] + [
        (i, j, 2 * vector[i] * vector[j]) for i, j in combinations(nz, 2)]


def negative(matrix, form):
    return sum(matrix[i][j] * coefficient for i, j, coefficient in form) < 0


def row_pairs(mask, stars):
    s = core.local_matrix(mask, stars)
    rows = [list(x) for x in combinations(range(10), 5)
            if all(s[i][j] > 0 for i, j in combinations(x, 2))]
    for left, right in combinations_with_replacement(rows, 2):
        a, b = set(left), set(right)
        base = [[s[i][j] - int(i in a and j in a) - int(i in b and j in b)
                 for j in range(10)] for i in range(10)]
        if min(x for r in base for x in r) >= 0:
            yield left, right, base


def degrees(mask, left, right):
    a, b = set(left), set(right)
    lam = [3 - len(x) for x in core.rows(mask)]
    return ([2 - int(i in a) - int(i in b) for i in range(4)] +
            [2 + lam[i] - int(4 + i in a) - int(4 + i in b) for i in range(6)])


def matrix(base, edges):
    r = [x[:] for x in base]
    for i, j, w in edges:
        r[i][j] -= w
        r[j][i] -= w
    core.need(all(sum(row) == 4 * row[i] for i, row in enumerate(r)), 'residual row-sum bridge failed')
    core.need(min(x for row in r for x in row) >= 0, 'negative residual incidence entry')
    return r


def state_bytes(index, left, right, edges, r):
    return (json.dumps([index, left, right, edges, r], separators=(',', ':')) + '\n').encode()


def run(progress=None):
    domain, catalog = core.core_census()
    records, vector_profiles, vectors = [], [], []
    vector_id = {}
    whole_hash, all_pairs_hash = hashlib.sha256(), hashlib.sha256()
    total_states = total_pairs = 0
    for rec in catalog:
        for profile in rec['profiles']:
            index = len(records)
            mask, stars = rec['F_mask'], profile['stars']
            local_vectors, forms, pool = [], [], []
            preferred = None
            pairs_hash, matrices_hash = hashlib.sha256(), hashlib.sha256()
            states_count = pair_count = 0
            for left, right, base in row_pairs(mask, stars):
                tag = (json.dumps([mask, stars, left, right], separators=(',', ':')) + '\n').encode()
                all_pairs_hash.update(tag)
                pairs_hash.update(tag)
                d = degrees(mask, left, right)
                core.need(min(d) >= 0 and sum(d) == 18, 'invalid two-five slack degrees')
                core.need(d == [sum(row) - 4 * row[i] for i, row in enumerate(base)], 'incident degree bridge failed')
                states = sorted(core.weighted_stars(d, base))
                core.need(len(states) == len(set(states)), 'duplicate weighted slack state')
                for edges in states:
                    r = matrix(base, edges)
                    found = preferred if preferred is not None and negative(r, forms[preferred]) else None
                    if found is None:
                        found = next((i for i, form in enumerate(forms) if negative(r, form)), None)
                    if found is None:
                        vector = core.negative_vector(r)
                        core.need(core.quadratic(r, vector) < 0, 'invalid new negative witness')
                        local_vectors.append(vector)
                        forms.append(sparse_form(vector))
                        found = len(forms) - 1
                    preferred = found
                    data = state_bytes(index, left, right, edges, r)
                    matrices_hash.update(data)
                    whole_hash.update(data)
                    states_count += 1
                pair_count += 1
            for vector in local_vectors:
                key = tuple(vector)
                if key not in vector_id:
                    vector_id[key] = len(vectors)
                    vectors.append(vector)
                pool.append(vector_id[key])
            vector_profiles.append({'index': index, 'vector_indices': pool})
            records.append({'index': index, 'F_mask': mask, 'stars': stars,
                            'row_pairs': pair_count, 'row_pairs_sha256': pairs_hash.hexdigest(),
                            'states': states_count, 'state_matrix_sha256': matrices_hash.hexdigest(),
                            'profile_vectors': len(pool)})
            total_pairs += pair_count
            total_states += states_count
            print(json.dumps({'profile': index + 1, 'states': total_states,
                              'row_pairs': total_pairs, 'vectors': len(vectors)}), flush=True)
            if progress:
                Path(progress).write_bytes(encoded({'agent': 'six-books-3', 'role': 'researcher',
                    'complete': False, 'completed_profiles': len(records), 'records': records,
                    'vectors': vectors, 'vector_profiles': vector_profiles, 'states': total_states,
                    'status': 'Saved author prefix; not an exclusion until the full checker passes.'}))
    cert = certificate_bytes(vectors, vector_profiles)
    result = {'agent': 'six-books-3', 'role': 'researcher', 'complete': True,
              'scope': 'Conditional ten-regular local2^4,3^6 theorem: every two-five-row residual Gram is indefinite.',
              'eligible_labeled_F': len(domain), 'F_orbits': len(catalog), 'catalog': catalog,
              'F_domain_sha256': hashlib.sha256(''.join(str(x) + '\n' for x in sorted(domain)).encode()).hexdigest(),
              'normalized_profiles': len(records),
              'labeled_local_cores': sum(r['orbit_size'] * sum(p['ordered_low_multiplicity'] for p in r['profiles']) for r in catalog),
              'profiles': records, 'row_pairs': total_pairs, 'row_pairs_sha256': all_pairs_hash.hexdigest(),
              'states': total_states, 'negative_forms': total_states, 'survivors': 0,
              'state_matrix_sha256': whole_hash.hexdigest(), 'unique_vectors': len(vectors),
              'profile_vector_references': sum(len(p['vector_indices']) for p in vector_profiles),
              'max_absolute_vector_entry': max(abs(x) for v in vectors for x in v),
              'negative_vectors_sha256': hashlib.sha256(cert).hexdigest()}
    return result, cert


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-certificates', action='store_true')
    parser.add_argument('--progress', help='private progress JSON outside the publication directory')
    args = parser.parse_args()
    result, cert = run(args.progress)
    data = encoded(result)
    if args.write_certificates:
        (HERE / 'expected.json').write_bytes(data)
        (HERE / 'negative_vectors.json').write_bytes(cert)
    else:
        core.need((HERE / 'expected.json').read_bytes() == data, 'expected summary differs')
        core.need((HERE / 'negative_vectors.json').read_bytes() == cert, 'integer certificate differs')
    print(json.dumps({k: v for k, v in result.items() if k not in ('catalog', 'profiles')}, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
