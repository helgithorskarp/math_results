#!/usr/bin/env python3
"""Exact capped H for every nonempty point-transitive seven-point triple cohort.

Standard library only. The group/Cauchy, PSD, equality and product bridges
are stated in POINT_TRANSITIVE_SEVEN_PROOF.md. No numeric search is imported.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations
from math import lcm
from pathlib import Path
import argparse
import copy
import hashlib
import json

from kernel_trade import check_definition, digest, lift
from nine_point_exceptions import bareiss_psd
from verify import characteristic_polynomial


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def mask(points):
    return sum(1 << i for i in points)


def move(a, p):
    return mask(p[i] for i in range(7) if a >> i & 1)


def relabel(word, powers):
    result = 0
    while word:
        bit = word & -word
        result += powers[bit.bit_length()-1]
        word ^= bit
    return result


def cycle_orbits(triples, cycle):
    remaining, orbits = set(triples), []
    while remaining:
        seed = min(remaining)
        orbit, current = [], seed
        for _ in range(7):
            orbit.append(current)
            current = move(current, cycle)
        require(current == seed and len(set(orbit)) == 7, 'invalid seven-cycle orbit')
        require(set(orbit) <= remaining, 'cycle orbits overlap')
        remaining -= set(orbit)
        orbits.append(tuple(sorted(orbit)))
    require(len(orbits) == 5, 'wrong number of triple orbits')
    return sorted(orbits)


def union_words(orbits, position):
    words = [sum(1 << position[a] for a in orbit) for orbit in orbits]
    return {sum(words[i] for i in range(5) if pattern >> i & 1) for pattern in range(1,32)}


def all_cycle_subgroups(triples, position):
    """Independent labelled domain: all order-seven cyclic subgroups of S7."""
    groups, labelled = set(), set()
    for tail in permutations(range(1,7)):
        order = (0,)+tail
        p = [0]*7
        for i in range(7):
            p[order[i]] = order[(i+1) % 7]
        power, subgroup = tuple(range(7)), []
        for _ in range(6):
            power = tuple(p[j] for j in power)
            subgroup.append(power)
        key = tuple(sorted(subgroup))
        if key in groups:
            continue
        groups.add(key)
        labelled |= union_words(cycle_orbits(triples,p),position)
    require(len(groups) == 120, 'order-seven subgroup coverage differs')
    return labelled


def census():
    triples = sorted(mask(t) for t in combinations(range(7),3))
    position = {a:i for i,a in enumerate(triples)}
    shift = tuple((i+1) % 7 for i in range(7))
    orbits = cycle_orbits(triples,shift)
    gap_orbits = set()
    for a in range(1,6):
        for b in range(1,7-a):
            seed = mask((0,a,a+b))
            gap_orbits.add(tuple(sorted(move(seed,tuple((i+t) % 7 for i in range(7)))
                                        for t in range(7))))
    require(set(orbits) == gap_orbits, 'cyclic-gap enumeration disagrees')
    candidates = union_words(orbits,position)
    require(len(candidates) == 31, 'wrong number of fixed-cycle unions')
    pdata = [(p,tuple(1 << position[move(a,p)] for a in triples))
             for p in permutations(range(7))]
    cases, labelled = {}, set()
    for word in sorted(candidates):
        orbit = {relabel(word,powers) for _,powers in pdata}
        canonical = min(orbit)
        if canonical in cases:
            continue
        require(not labelled & orbit, 'canonical classes intersect')
        labelled |= orbit
        selected = [a for i,a in enumerate(triples) if canonical >> i & 1]
        group = [p for p,powers in pdata if relabel(canonical,powers) == canonical]
        require(len(group)*len(orbit) == 5040, 'orbit-stabilizer identity fails')
        require(all({p[i] for p in group} == set(range(7)) for i in range(7)),
                'full group is not point transitive')
        degrees = [sum(bool(a >> i & 1) for a in selected) for i in range(7)]
        require(len(set(degrees)) == 1 and 7*degrees[0] == 3*len(selected), 'not regular')
        cases[canonical] = {'canonical_word':canonical,'triple_masks':selected,
                            'N':29+len(selected),'s':7+degrees[0],
                            'triple_degree':degrees[0],
                            'automorphism_order':len(group),'labelled_orbit_size':len(orbit),
                            'point_group':group}
    independent = all_cycle_subgroups(triples,position)
    require(labelled == independent, 'independent labelled censuses disagree')
    require(len(cases) == 11 and len(labelled) == 3181, 'unexpected quantified coverage')
    counts = Counter(len(row['triple_masks']) for row in cases.values())
    require(counts == {7:2,14:3,21:3,28:2,35:1}, 'class profile differs')
    summary = {'fixed_cycle_unions':31,'full_permutation_classes':11,
               'labelled_collections':len(labelled),'order_seven_subgroups':120,
               'two_labelled_enumerations_agree':True,'gap_orbits_agree':True,
               'class_counts_by_triples':{str(k):v for k,v in sorted(counts.items())},
               'labelled_word_list_sha256':hashlib.sha256(json.dumps(sorted(labelled),separators=(',',':')).encode()).hexdigest()}
    return [cases[key] for key in sorted(cases)],summary


def decode(case, certificate):
    require(certificate['canonical_word'] == case['canonical_word'], 'wrong certificate class')
    require(certificate['triple_masks'] == case['triple_masks'], 'wrong literal triple domain')
    require(certificate['N'] == case['N'] and certificate['s'] == case['s'], 'wrong parameters')
    nonempty = sorted([1 << i for i in range(7)] +
                      [mask(p) for p in combinations(range(7),2)] + case['triple_masks'])
    allowed = {(a,b) for a,b in combinations(nonempty,2) if not a & b}
    entries, sizes = {}, []
    reps,values = certificate['orbit_representatives'],certificate['orbit_values']
    require(len(reps) == len(values), 'orbit table lengths differ')
    for pair,value in zip(reps,values):
        require(len(pair) == 2 and tuple(pair) in allowed, 'bad support representative')
        a,b = pair
        orbit = {tuple(sorted((move(a,p),move(b,p)))) for p in case['point_group']}
        require(orbit <= allowed and not set(entries) & orbit, 'orbit overlap or wrong support')
        entries.update({pair:F(value) for pair in orbit})
        sizes.append(len(orbit))
    require(set(entries) == allowed, 'incomplete disjoint-pair table')
    c = [[F(case['s']-1) if a==b else F(-1) if a & b else
          entries[tuple(sorted((a,b)))] for b in nonempty] for a in nonempty]
    return [0]+nonempty,c,sizes


def polynomial_psd(matrix, expected_rank=None):
    n = len(matrix)
    require(all(len(row) == n for row in matrix), 'nonsquare polynomial PSD input')
    require(all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n)),
            'asymmetric polynomial PSD input')
    denominator = lcm(*(F(x).denominator for row in matrix for x in row))
    integers = [[int(F(x)*denominator) for x in row] for row in matrix]
    coefficients = characteristic_polynomial(integers)
    require(all((-1)**j*x >= 0 for j,x in enumerate(coefficients)), 'negative-root sign certificate fails')
    rank = max(j for j,x in enumerate(coefficients) if x)
    if expected_rank is not None:
        require(rank == expected_rank, 'characteristic rank differs')
    polynomial_hash = hashlib.sha256(json.dumps(coefficients,separators=(',',':')).encode()).hexdigest()
    return rank,polynomial_hash,denominator


def audit(case, certificate):
    members,c,sizes = decode(case,certificate)
    n,s = case['N'],case['s']
    L = lift(c)
    active,stars,_ = check_definition(members,s,L)
    require(active == stars == list(range(7)), 'wrong largest-star set')
    u = [[F(n*int(i==j)-1)-c[i][j] for j in range(n-1)] for i in range(n-1)]
    require(bareiss_psd(c) == n-8 and bareiss_psd(u) == n-1, 'integer Schur ranks differ')
    _,c_poly,c_den = polynomial_psd(c,n-8)
    _,u_poly,u_den = polynomial_psd(u,n-1)
    m = [[F(L[i][j]-s*int(i==j),n-s) for j in range(n)] for i in range(n)]
    require(all(sum(row)==1 for row in m) and all(m[i][j]==0
            for i,a in enumerate(members) for j,b in enumerate(members) if a & b),
            'decoded M does not satisfy H linear equations')
    return {'canonical_word':case['canonical_word'],'N':n,'s':s,'triples':len(case['triple_masks']),
            'triple_degree':case['triple_degree'],'full_automorphism_order':case['automorphism_order'],
            'labelled_orbit_size':case['labelled_orbit_size'],'support_orbits':len(sizes),
            'disjoint_nonempty_pairs':sum(sizes),'core_rank':n-8,'full_L_rank':n-7,
            'upper_core_rank':n-1,'lower_endpoint_multiplicity':7,'unit_eigenvalue_simple':True,
            'maximum_family_count_by_written_kernel_proof':7,'C_denominator':c_den,
            'U_denominator':u_den,'M_denominator':lcm(*(x.denominator for row in m for x in row)),
            'C_sha256':digest(c),'L_sha256':digest(L),'M_sha256':digest(m),
            'C_charpoly_sha256':c_poly,'U_charpoly_sha256':u_poly,
            'L_empty_diagonal':str(L[0][0]),'M_empty_diagonal':str(m[0][0]),
            'minimum_offdiagonal_M_entry':str(min(m[i][j] for i in range(n) for j in range(i+1,n)))}


def controls(cases, certificates):
    rejections = 0
    for checker in (bareiss_psd,lambda matrix:polynomial_psd(matrix)[0]):
        for bad in ([[-1]],[[0,1],[1,0]],[[1,2],[0,1]]):
            try:
                checker(bad)
            except (ValueError,AssertionError):
                rejections += 1
            else:
                raise ValueError('invalid matrix accepted by control')
        require(checker([[2,0],[0,0]])==1 and checker([[2,1],[1,2]])==2,
                'PSD positive/singular control fails')
    for duplicate in (False,True):
        damaged = copy.deepcopy(certificates[0])
        if duplicate:
            damaged['orbit_representatives'].append(damaged['orbit_representatives'][0])
            damaged['orbit_values'].append(damaged['orbit_values'][0])
        else:
            damaged['orbit_values'][0] = str(F(damaged['orbit_values'][0])+1)
        try:
            audit(cases[0],damaged)
        except (ValueError,AssertionError):
            rejections += 1
        else:
            raise ValueError('damaged certificate accepted')
    return {'indefinite_or_asymmetric_rejections':6,'damaged_orbit_rejections':2,
            'positive_and_singular_rank_controls':4,'total_rejections':rejections}


def small_block_partitions(remaining):
    """Every partition of the remaining points into blocks of size at most three."""
    if not remaining:
        yield ()
        return
    first = remaining & -remaining
    others = [1 << i for i in range(7) if remaining >> i & 1 and (1 << i) != first]
    for count in range(min(2,len(others))+1):
        for selected in combinations(others,count):
            block = first + sum(selected)
            for suffix in small_block_partitions(remaining ^ block):
                yield (block,)+suffix


def fractional_uniform_seven():
    """Exact primal/dual certificates for the previously known value 91/4."""
    nonempty = [a for a in range(1,128) if a.bit_count() <= 3]
    dual = {a:F(a.bit_count()-1,4) for a in nonempty}
    cover = {a:F(0) for a in nonempty}
    value,counts,maximum = F(0),Counter(),F(0)
    partitions = list(small_block_partitions(127))
    require(len(set(partitions)) == len(partitions), 'duplicate partition')
    for blocks in partitions:
        require(sum(blocks) == 127 and all(not a & b for a,b in combinations(blocks,2)),
                'wrong partition support')
        weight = sum(dual[a] for a in blocks)
        require(weight <= 1, 'infeasible fractional dual')
        maximum = max(maximum,weight)
        sizes = tuple(sorted(a.bit_count() for a in blocks))
        coefficient = F(1,10) if sizes == (2,2,3) else F(7,40) if sizes == (1,3,3) else F(0)
        if coefficient:
            counts[sizes] += 1
            value += coefficient
            for a in blocks:
                cover[a] += coefficient
    require(counts == {(2,2,3):105,(1,3,3):70}, 'wrong fractional cover types')
    require(all(x >= 1 for x in cover.values()), 'infeasible fractional primal')
    require(value == sum(dual.values()) == F(91,4), 'fractional primal/dual values differ')
    return {'known_base_value':'91/4','base_N':64,'base_star':22,
            'small_block_partitions':len(partitions),'positive_cover_cliques':175,
            'cover_types':{'2+2+3':{'count':105,'weight':'1/10'},
                           '1+3+3':{'count':70,'weight':'7/40'}},
            'dual_by_size':{'1':'0','2':'1/4','3':'1/2'},
            'cover_by_size':{str(k):sorted({str(cover[a]) for a in nonempty if a.bit_count()==k})
                             for k in (1,2,3)},'maximum_partition_dual':str(maximum),
            'mixed_product_lower_bound_per_vertex':'91/256',
            'cohort_largest_star_density_bound':'11/32','mixed_product_gap_ratio_at_least':'91/88'}


def run(path):
    raw = path.read_bytes()
    fixture = json.loads(raw)
    cases,summary = census()
    certificates = fixture['cases']
    require([c['canonical_word'] for c in certificates] == [c['canonical_word'] for c in cases],
            'fixture is not the complete canonical cohort')
    rows = [audit(case,certificate) for case,certificate in zip(cases,certificates)]
    require(max(F(row['s'],row['N']) for row in rows) == F(11,32),
            'wrong cohort density for product separation')
    fano = next(case for case in cases if case['canonical_word'] == 1241792641)
    require(all(sum((a & pair) == pair for a in fano['triple_masks']) == 1
                for pair in (mask(p) for p in combinations(range(7),2))),
            'claimed Fano baseline is not an STS')
    return {'agent':'six-downset-3','role':'researcher',
            'scope':'Every nonempty point-transitive seven-point triple downset with full two-skeleton; written kernel/product bridges are not formalized.',
            'certificate_sha256':hashlib.sha256(raw).hexdigest(),'coverage':summary,
            'cases':rows,'controls':controls(cases,certificates),
            'known_uniform_fractional_baseline':fractional_uniform_seven()}


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,default=Path(__file__).with_name('POINT_TRANSITIVE_SEVEN_CERTIFICATES.json'))
    parser.add_argument('--check',type=Path)
    args = parser.parse_args()
    result = run(args.certificate)
    if args.check:
        require(result == json.loads(args.check.read_text()), 'expected result differs')
        print('exact eleven-class seven-point cohort, PSD ranks and controls match')
    else:
        print(json.dumps(result,indent=2,sort_keys=True))
