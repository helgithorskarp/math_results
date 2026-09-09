#!/usr/bin/env python3
"""Standard-library verifier using the independent reviewer edge inventory."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import exact as X

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'hadwiger_nelson_radix_four_active_closure_review1/independent_check.py'
SPEC = importlib.util.spec_from_file_location('reviewer_inventory', SOURCE)
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)


def direct_inventory():
    rows, factors, circle, monomials, row_ids = V.reconstruct_inventory()
    special = [None]*len(factors)
    special[circle] = (-1,0,1)
    for row,c in row_ids.items():
        a = [d[0] for d in row]
        b = [d[1] for d in row]
        q = X.add(X.add(X.mul(a,a),X.mul(a,b)),X.mul(b,b))
        q = X.add(q,[1],-1)
        X.need(q[-1] == 1, 'direct real-axis norm is monic')
        special[c] = tuple(q)
        y_zero = [0]*(1+max(i for i,j,t in factors[c]))
        for i,j,t in factors[c]:
            if j == 0:
                y_zero[i] += t
        X.need(X.trim(y_zero) == q, 'direct Eisenstein norm equals real-axis specialization')
    groups = {c:[] for c in range(len(factors))}
    base = []
    for u,v in combinations(range(243),2):
        owner = V.edge_owner(u,v,monomials,row_ids,circle)
        (base if owner == 'base' else groups[owner]).append((u,v))
    X.need(len(base) == 243 and sum(map(len,groups.values())) == 29160, 'all actual label pairs')
    return factors,circle,special,groups,base


def check_products(cert, unique):
    blocks = cert['blocks']
    X.need(blocks == sorted(blocks) and len({tuple(q) for q in blocks}) == len(blocks), 'distinct sorted blocks')
    for q in blocks:
        X.need(2 <= len(q) <= 9 and q[-1] == 1 and all(type(x) is int for x in q), 'nonconstant monic integer block')
    X.need(len(cert['factorizations']) == len(unique), 'one factorization per real norm polynomial')
    event_blocks = []
    for f,terms in zip(unique,cert['factorizations']):
        X.need(terms == sorted(terms) and len({i for i,e in terms}) == len(terms), 'canonical factor multiplicities')
        result = [1]
        for i,e in terms:
            X.need(type(i) is int and 0 <= i < len(blocks) and type(e) is int and 1 <= e <= 8, 'factor index and multiplicity')
            for _ in range(e):
                result = X.mul(result,blocks[i])
        X.need(tuple(result) == f, 'exact integer factorization product')
        event_blocks.append({i for i,e in terms})
    X.need(set().union(*event_blocks) == set(range(len(blocks))), 'every supplied block occurs')
    return event_blocks


def modular_audit(blocks):
    X.need(all(X.is_prime(p) for p in X.PRIMES), 'all proof moduli are prime')
    histogram, trace = Counter(), hashlib.sha256()
    for i,j in combinations(range(len(blocks)),2):
        for prime in X.PRIMES:
            if X.gcd_is_one(blocks[i],blocks[j],prime):
                histogram[prime] += 1
                trace.update(f'{i},{j},{prime}\n'.encode())
                break
        else:
            raise ValueError('no modular coprimality certificate')
    squarefree = []
    for q in blocks:
        squarefree.append(next(p for p in X.PRIMES if X.gcd_is_one(q,X.derivative(q),p)))
    return {'pair_checks':sum(histogram.values()), 'prime_histogram':{str(p):n for p,n in sorted(histogram.items())},
            'pair_trace_sha256':trace.hexdigest(), 'squarefree_primes_sha256':X.digest(squarefree)}


def check_rotation():
    digits = V.DIGITS
    power = (1,0)
    shifts = []
    maps = []
    for j in range(5):
        shifted = [V.e_mul(power,d) for d in digits]
        possible = []
        for shift in shifted:
            translated = [(a-shift[0],b-shift[1]) for a,b in shifted]
            if set(translated) == set(digits):
                possible.append((shift,[digits.index(t) for t in translated]))
        X.need(len(possible) == 1, 'digit triangle translates under omega^2 rotation')
        shift,permutation = possible[0]
        shifts.append(shift)
        maps.append(permutation)
        power = V.e_mul(power,(-1,1))
    X.need(shifts == [(0,0),(-1,0),(0,-1),(0,0),(-1,0)], 'exact A5 parameter-rotation translation')
    X.need(len({tuple(maps[j][a[j]] for j in range(5)) for a in V.LABELS}) == 243, 'rotation digit bijection')
    return shifts


def run(certificate_path):
    cert = json.loads(Path(certificate_path).read_text())
    X.need(cert['schema'] == 'hn-radix-reflection-axis-v1','certificate schema')
    factors,circle,special,groups,base = direct_inventory()
    unique = sorted(set(special))
    X.need(X.digest(factors) == cert['curve_inventory_sha256'], 'original curve IDs')
    X.need(X.digest(unique) == cert['real_norm_inventory_sha256'], 'specialization inventory')
    fact_blocks = check_products(cert,unique)
    by_poly = dict(zip(unique,fact_blocks))
    event_lists = [[c for c,f in enumerate(special) if i in by_poly[f]] for i in range(len(cert['blocks']))]
    words = [[sum(a*b for a,b in zip(w,label)) % 3 for label in V.LABELS] for w in X.WEIGHTS]
    colours, roots = cert['colour_assignments'], cert['real_root_counts']
    X.need(len(colours) == len(roots) == len(cert['blocks']), 'block annotation lengths')
    for i,q in enumerate(cert['blocks']):
        if len(q) <= 5:
            X.need(colours[i] is None and roots[i] is None, 'accepted low-degree branch is imported')
            continue
        k = colours[i]
        X.need(type(k) is int and 0 <= k < len(words), 'valid colouring index')
        word = words[k]
        X.need(all(word[u] != word[v] for u,v in base), 'universal triangles are proper')
        for c in event_lists[i]:
            X.need(all(word[u] != word[v] for u,v in groups[c]), 'every edge in active factor graph is proper')
        X.need(roots[i] == X.root_count(q), 'independent Sturm real-root count')
    audit = modular_audit(cert['blocks'])
    check_rotation()
    high = [i for i,g in enumerate(cert['blocks']) if len(g)>5]
    higher = [i for i in high if len(event_lists[i])>=5 and roots[i]]
    result = {
        'active_curves':len(factors), 'unique_real_axis_norm_polynomials':len(unique),
        'monic_blocks':len(cert['blocks']), 'block_degree_histogram':{str(d):n for d,n in sorted(Counter(len(g)-1 for g in cert['blocks']).items())},
        'low_degree_blocks_closed_by_h4119':len(cert['blocks'])-len(high), 'higher_degree_blocks':len(high),
        'higher_block_colour_histogram':{str(k):n for k,n in sorted(Counter(colours[i] for i in high).items())},
        'higher_blocks_with_real_roots':sum(bool(roots[i]) for i in high),
        'higher_block_real_roots':sum(roots[i] for i in high),
        'higher_block_incidence_histogram':{str(k):n for k,n in sorted(Counter(len(event_lists[i]) for i in high).items())},
        'higher_incidence_real_blocks':[{'block_id':i,'polynomial':cert['blocks'][i],'curves':event_lists[i],
                                       'real_roots':roots[i],'colour_index':colours[i]} for i in higher],
        'coprimality':audit, 'all_reflection_axis_members_chromatic_number':3,
        'eight_active_gate_closed':False, 'record_improvement':False,
    }
    X.need(result == cert['result'], 'all expected counts and certificate hashes')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args=parser.parse_args()
    print(json.dumps(run(args.certificate),indent=2,sort_keys=True))
