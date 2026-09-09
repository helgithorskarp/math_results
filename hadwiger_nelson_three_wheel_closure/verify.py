#!/usr/bin/env python3
"""Complete chromatic cover, standard library only; no CAS or SAT imports."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse
import hashlib
import json
import arithmetic as A
import inputs
from norm_check import NormBlock

HERE = Path(__file__).resolve().parent


def projection_check(f, g, row, rfactors):
    E = A.resultant_y(f, g)
    product = (1,)
    seen = set()
    for entry in row:
        k, m = entry['r'], entry['multiplicity']
        A.need(type(k) is int and 0 <= k < len(rfactors) and k not in seen, 'unique projection factor index')
        A.need(type(m) is int and 1 <= m <= 8, 'projection multiplicity')
        seen.add(k)
        for _ in range(m):
            product = A.mul(product, rfactors[k])
    A.need(tuple(product) == E, 'exact Sylvester resultant factorization')
    return len(E)-1


def run(path, progress=False):
    cert = json.loads(path.read_text())
    A.need(cert.get('version') == 1, 'certificate version')
    src, coefficients, pairs, allowed, base, inventory = inputs.load()
    rows = []
    for row in cert['systems']:
        expanded = []
        for z in row:
            A.need(type(z) is list and len(z) == 3, 'projection row encoding')
            k, m, a = z
            A.need(type(a) is int and 0 <= a < len(cert['actions']), 'action index')
            expanded.append({'r': k, 'multiplicity': m, 'action': cert['actions'][a]})
        rows.append(expanded)
    rfactors = [tuple(r) for r in cert['rfactors']]
    A.need(len(rows) == len(pairs) == 800, 'all representative systems present')
    A.need(rfactors == sorted(set(rfactors)), 'canonical distinct projection factors')
    for r in rfactors:
        A.need(len(r) >= 2 and all(type(c) is int for c in r) and A.primitive(r) == r, 'primitive projection factor')
    words = cert['words']
    A.need(len(set(words)) == len(words), 'distinct colour witnesses')
    badwords = [inputs.bad_factors(w, allowed, base, inventory) for w in words]
    cache = {}; stats = Counter(); dims = Counter(); witnesses = hashlib.sha256()
    prime_counts = Counter(); unit_checks = 0; dimension_sum = 0; max_dimension = 0

    def certify(r, h, action):
        nonlocal unit_checks
        key = (r, h)
        tag = json.dumps(action, sort_keys=True, separators=(',', ':'))
        if key in cache:
            A.need(cache[key] == tag, 'consistent action for repeated quotient block')
            return
        A.need(h and h[-1] == (1,), 'monic finite y relation')
        A.need(isinstance(action, dict) and len(action) in (1, 2), 'proof action')
        if 'empty' in action:
            A.need(action == {'empty': True} and h == ((1,),), 'empty fibre identity')
            kind = 'empty'
        elif 'no_real_x' in action:
            A.need(action == {'no_real_x': True} and len(r) == 3 and r[1]*r[1]-4*r[0]*r[2] < 0, 'negative x discriminant')
            kind = 'no_real_x'
        elif 'no_real_y' in action:
            A.need(action == {'no_real_y': True} and len(h) == 3 and all(len(c) <= 1 for c in h), 'constant quadratic y relation')
            b = h[1][0] if h[1] else 0; c = h[0][0] if h[0] else 0
            A.need(b*b-4*c < 0, 'negative y discriminant')
            kind = 'no_real_y'
        elif 'split' in action:
            A.need(set(action) == {'split'} and len(action['split']) >= 2, 'nontrivial finite split')
            Q = A.Quotient(r); product = ((F(1),),); children = []
            for child in action['split']:
                z = A.decode_h(child['h'])
                A.need(1 < len(z) < len(h) and z[-1] == (1,), 'strict monic child degree')
                A.need(all(Q.red(c) == c for c in z), 'reduced split coefficients')
                product = Q.y_mul(product, z)
                children.append((z, child['action']))
            A.need(product == h, 'exact quotient factorization identity')
            for z, subaction in children:
                certify(r, z, subaction)
            kind = 'split'
        elif 'colour' in action:
            A.need(set(action) == {'colour', 'primes'}, 'colour action fields')
            wi, primes = action['colour'], action['primes']
            A.need(type(wi) is int and 0 <= wi < len(words), 'colour word index')
            A.need(type(primes) is list and 1 <= len(primes) <= 3 and len(primes) == len(set(primes)), 'finite prime witnesses')
            Q = A.Quotient(r)
            blocks = [(p, NormBlock(Q.r, h, p)) for p in primes]
            keyhash = hashlib.sha256(json.dumps([r, A.encode_h(h)], separators=(',', ':')).encode()).hexdigest()
            for f in sorted(badwords[wi]):
                good = next((p for p, block in blocks if block.unit(coefficients[f])), None)
                A.need(good is not None, f'unexcluded monochromatic factor {f}')
                witnesses.update(f'{keyhash},{f},{good}\n'.encode())
                prime_counts[str(good)] += 1; unit_checks += 1
            kind = 'colour'
        else:
            raise ValueError('unproved or residual action')
        cache[key] = tag
        stats[kind] += 1

    resultant_degrees = Counter(); branch_count = 0; gcd_fingerprints = hashlib.sha256()
    for index, ((a, b), row) in enumerate(zip(pairs, rows)):
        degree = projection_check(coefficients[a], coefficients[b], row, rfactors)
        resultant_degrees[str(degree)] += 1
        for entry in row:
            r = rfactors[entry['r']]
            Q = A.Quotient(r)
            h = Q.y_gcd(coefficients[a], coefficients[b])
            # Euclidean remainders certify h is in (f,g) modulo r. No
            # assertion of irreducibility or CAS ideal-membership is used.
            A.need(h[-1] == (1,) and all(Q.red(c) == c for c in h), 'reduced monic Euclidean relation')
            dim = (len(r)-1)*(len(h)-1)
            dims[str(dim)] += 1; dimension_sum += dim; max_dimension = max(max_dimension, dim)
            gcd_fingerprints.update(json.dumps([index, entry['r'], A.encode_h(h)], separators=(',', ':')).encode()+b'\n')
            certify(r, h, entry['action'])
            branch_count += 1
        if progress and (index % 100 == 0 or index == 799):
            import sys
            print(f'verified {index+1}/800 systems', file=sys.stderr, flush=True)
    return {
        'status': 'EVERY_THREE_WHEEL_SUM_IS_FOUR_COLOURABLE',
        'architecture': 'W+uW+vW, |u|=|v|=1, strict physical unit graph',
        'maximum_physical_order': 343, 'record_improvement': False,
        'systems_covered': 800, 'projection_factors': len(rfactors),
        'resultant_degree_histogram': dict(sorted(resultant_degrees.items())),
        'projection_branches_with_multiplicity_removed': branch_count,
        'quotient_dimension_histogram': dict(sorted(dims.items())),
        'sum_quotient_dimensions_over_systems': dimension_sum,
        'maximum_quotient_dimension': max_dimension, 'unique_quotient_blocks': len(cache),
        'block_action_counts': dict(sorted(stats.items())), 'colour_words': len(words),
        'modular_unit_certificates_checked': unit_checks,
        'unit_witness_prime_histogram': dict(sorted(prime_counts.items())),
        'unit_witness_stream_sha256': witnesses.hexdigest(),
        'euclidean_relation_stream_sha256': gcd_fingerprints.hexdigest(),
        'remaining_injective_physical_classes': 0,
        'noninjective_branch_dependency': 'h4073', 'symmetry_coverage_dependency': 'h4071',
        'source_distance_factorization_dependency': 'h4065',
        'proof_replay_solver_calls': 0, 'proof_replay_CAS_calls': 0,
        'root_isolation_performed': False, 'formalized': False,
        'external_reviewer_acceptance_claimed': False,
        'certificate_bytes': path.stat().st_size,
        'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE/'certificate.json')
    parser.add_argument('--check-expected', action='store_true')
    parser.add_argument('--progress', action='store_true')
    args = parser.parse_args(); result = run(args.certificate, args.progress)
    if args.check_expected:
        A.need(result == json.loads((HERE/'EXPECTED.json').read_text()), 'expected result')
    print(json.dumps(result, indent=2, sort_keys=True))
