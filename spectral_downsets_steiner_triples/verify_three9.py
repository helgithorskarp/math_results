"""Capped maximal-rank H for every union of three block-disjoint STS(9).

CPython 3.11+, standard library only. Regenerates all inputs and full point
automorphisms; decodes nine fixed rational orbit lists, with two independent
PSD algorithms. No optimizer, floating arithmetic, or external census.
Author: six-downset-2, researcher. Written bridges: THREE_STS9_PROOF.md.
"""
import argparse
import copy
import json
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path

from certificates import affine_sts9, check_sts, downset, steiner_certificate
from maxrank_certificates import mix_certificates
from verify import check_definition, exact_psd_rank, matrix_hash, rejects
from verify_two9 import (affine_group, all_sts9, complete_cohort, moved,
                         polynomial_psd, relabelling_orbit)


def compose(p, q):
    return tuple(p[q[i]] for i in range(9))


def inverse(p):
    result = [0]*9
    for i, j in enumerate(p):
        result[j] = i
    return tuple(result)


def image(system, p):
    return tuple(sorted(moved(a, p) for a in system))


def union_structure(union, systems, transport, affine):
    """Full Aut(U) and canonical point-isomorphism key, without assuming
    that the supplied decomposition is unique or exhausts its subsystems.
    """
    U = set(union)
    contained = sorted(system for system in systems if set(system) <= U)
    decompositions = []
    for i, a in enumerate(contained):
        for b in contained[i+1:]:
            if set(a) & set(b):
                continue
            c = tuple(sorted(U-set(a)-set(b)))
            if c in contained and b < c:
                decompositions.append((a, b, c))
    assert decompositions
    autos = set()
    canonical = None
    for system in contained:
        q = transport[system]
        for g in affine:
            p = compose(q, g)
            if image(union, p) == union:
                autos.add(p)
        normalized = image(union, inverse(q))
        for g in affine:
            candidate = image(normalized, g)
            if canonical is None or candidate < canonical:
                canonical = candidate
    assert tuple(range(9)) in autos and all(inverse(p) in autos for p in autos)
    return {'canonical': canonical, 'group': sorted(autos),
            'contained': contained, 'decompositions': decompositions}


def complete_three_cohort(first):
    pairs, two_summary = complete_cohort(first)
    systems = all_sts9()
    transport = relabelling_orbit(first)
    affine = affine_group()
    assert set(transport) == systems and len(systems) == 840
    assert all(sorted(p) == list(range(9)) and image(first, p) == system
               for system, p in transport.items())
    assert all(image(first, g) == first for g in affine)
    assert len(affine)*len(systems) == 362880
    representatives = []
    pair_summary = []
    for second, pair_size, p in pairs:
        fixed = [g for g in affine if image(second, g) == second]
        assert len(fixed)*pair_size == len(affine)
        forbidden = set(first)|set(second)
        thirds = {t for t in systems if not set(t) & forbidden}
        remaining = set(thirds)
        orbit_sizes = []
        while remaining:
            third = min(remaining)
            images = {image(third, g) for g in fixed}
            assert images <= remaining
            stabilizer = sum(image(third, g) == third for g in fixed)
            assert len(images)*stabilizer == len(fixed)
            remaining -= images
            orbit_sizes.append(len(images))
            representatives.append((first, second, third))
        pair_summary.append({'pair_orbit_size': pair_size,
                             'pair_stabilizer_order': len(fixed),
                             'third_systems': len(thirds),
                             'third_orbit_sizes': orbit_sizes})
    assert [(r['third_systems'], len(r['third_orbit_sizes'])) for r in pair_summary] == [(41,17),(34,10)]
    assert len(representatives) == 27
    classes = {}
    for layers in representatives:
        union = tuple(sorted(set().union(*map(set, layers))))
        assert len(union) == 36
        structure = union_structure(union, systems, transport, affine)
        key = structure['canonical']
        classes.setdefault(key, []).append((layers, structure))
    assert len(classes) == 9
    class_summary = []
    for key, entries in sorted(classes.items()):
        structure = entries[0][1]
        group_order = len(structure['group'])
        assert all(len(e[1]['group']) == group_order and
                   len(e[1]['contained']) == len(structure['contained']) and
                   len(e[1]['decompositions']) == len(structure['decompositions'])
                   for e in entries)
        class_summary.append({'ordered_representatives': len(entries),
                              'full_automorphism_order': group_order,
                              'contained_STSs': len(structure['contained']),
                              'unordered_decompositions': len(structure['decompositions'])})
    assert all(r['unordered_decompositions'] == 1 for r in class_summary)

    # Independent entry-level coverage: unquotiented enumeration of every union
    # admitting a decomposition with the fixed first STS, against normalization
    # images of the nine types. Extra contained STSs need not participate in a
    # complete decomposition, so use the independently found exact covers here.
    disjoint = [t for t in systems if not set(t) & set(first)]
    direct = set()
    for second in disjoint:
        forbidden = set(first)|set(second)
        for third in disjoint:
            if second < third and not set(third) & forbidden:
                direct.add(tuple(sorted(forbidden|set(third))))
    covered = set()
    for entries in classes.values():
        layers, structure = entries[0]
        union = tuple(sorted(set().union(*map(set, layers))))
        participating = {s for dec in structure['decompositions'] for s in dec}
        for system in participating:
            normalized = image(union, inverse(transport[system]))
            covered.update(image(normalized, g) for g in affine)
    assert direct == covered and len(direct) == 3768
    return classes, systems, transport, affine, {
        **two_summary, 'ordered_triple_orbits': 27, 'pair_cases': pair_summary,
        'union_isomorphism_classes': class_summary,
        'fixed_first_union_count': len(direct),
        'fixed_first_union_sha256': sha256(json.dumps(sorted(direct), separators=(',',':')).encode()).hexdigest(),
        'labelled_union_count': sum(362880//r['full_automorphism_order'] for r in class_summary)}


def supported_representatives(D, group):
    reps = set()
    for i, a in enumerate(D):
        for b in D[i:]:
            if not a & b:
                reps.add(min(tuple(sorted((moved(a,p),moved(b,p)))) for p in group))
    return sorted(reps)


def decode_case(case, systems, transport, affine):
    layers = [tuple(layer) for layer in case['layers']]
    assert len(layers) == 3
    for layer in layers:
        check_sts(9, layer)
    assert layers[0] == tuple(affine_sts9())
    union = tuple(sorted(set().union(*map(set, layers))))
    assert len(union) == 36
    D = downset(9, layers)
    assert len(D) == 82
    structure = union_structure(union, systems, transport, affine)
    group = structure['group']
    assert len(group) == case['full_automorphism_order']
    reps = supported_representatives(D, group)
    den = case['denominator']
    assert isinstance(den, int) and den > 0
    nums = case['orbit_numerators']
    assert len(nums) == len(reps) and all(isinstance(x, int) for x in nums)
    table = {ab: F(value, den) for ab, value in zip(reps, nums)}
    Q = [[F(21 if i == j and i else 0) for j in range(82)] for i in range(82)]
    used = set()
    for i, a in enumerate(D):
        for j in range(i, 82):
            b = D[j]
            if a & b:
                continue
            rep = min(tuple(sorted((moved(a,p),moved(b,p)))) for p in group)
            assert rep in table
            used.add(rep)
            Q[i][j] = Q[j][i] = table[rep]
    assert used == set(table)
    return D, Q, layers, structure


def upper(Q):
    n = len(Q)
    return [[F(n if i == j else 0)-Q[i][j] for j in range(n)] for i in range(n)]


def buffered_upper(Q, delta):
    n = len(Q)
    return [[F(n if i == j else 0)-Q[i][j]-delta*int(i == j)+delta/n
             for j in range(n)] for i in range(n)]


def gram_rank(vectors):
    return exact_psd_rank([[sum(x*y for x,y in zip(a,b)) for b in vectors] for a in vectors])


def run():
    data = json.loads(Path(__file__).with_name('three9_certificates.json').read_text())
    assert (data['N'],data['s']) == (82,21)
    first = tuple(affine_sts9())
    classes, systems, transport, affine, coverage = complete_three_cohort(first)
    actual_keys = []
    decoded = []
    for case in data['cases']:
        D,Q,layers,structure = decode_case(case, systems, transport, affine)
        actual_keys.append(structure['canonical'])
        decoded.append((D,Q,layers,structure,case))
    assert len(set(actual_keys)) == len(actual_keys) == 9
    assert set(actual_keys) == set(classes)
    result = {'arithmetic': 'fractions.Fraction and arbitrary-precision integers',
              'coverage': coverage, 'matrices': []}
    for ci, (D,Q,layers,structure,case) in enumerate(decoded):
        qrank = check_definition(D,21,Q)
        assert qrank == 72 and all(x == 1 for x in Q[0])
        urank = exact_psd_rank(upper(Q))
        brank = exact_psd_rank(buffered_upper(Q,F(1,2)))
        assert urank == brank == 81
        lp = polynomial_psd(Q); up = polynomial_psd(upper(Q))
        assert (lp['rank'],up['rank']) == (qrank,urank)
        stars = [[F(bool(a >> i & 1))-F(21,82) for a in D] for i in range(9)]
        w = [F(j == 0)-F(1,82) for j in range(82)]
        assert gram_rank(stars) == 9 and gram_rank(stars+[w]) == 10
        ordinary = steiner_certificate(9,layers)
        Do,so,Qo = ordinary
        assert D == Do and so == 21
        assert check_definition(D,21,Qo) == 41
        assert Qo[0][0] == 811 and sum(Qo[i][i] for i in range(82)) == 2512
        assert sum(Qo[1][j]*w[j] for j in range(82)) == -108
        # Qo*w at a singleton is Qo[singleton,empty]-1=-107-1=-108.
        _,_,repaired,params = mix_certificates((D,21,Q),ordinary)
        assert params == {'epsilon':'1/10048','ordinary_trace':'2512'}
        rrank = check_definition(D,21,repaired)
        rurank = exact_psd_rank(upper(repaired))
        rbrank = exact_psd_rank(buffered_upper(repaired,F(1,4)))
        assert (rrank,rurank,rbrank) == (73,81,81)
        assert matrix_hash(Q) == case['centered_matrix_sha256']
        record = {'case':ci, 'full_automorphism_order':len(structure['group']),
                  'supported_pair_orbits':len(case['orbit_numerators']),
                  'centered_rank_Q':qrank, 'rank_upper':urank,
                  'half_buffer_rank':brank, 'centered_matrix_sha256':matrix_hash(Q),
                  'lower_polynomial':lp, 'upper_polynomial':up,
                  'maximal_rank_Q':rrank, 'repaired_upper_rank':rurank,
                  'quarter_buffer_rank':rbrank,
                  'repaired_matrix_sha256':matrix_hash(repaired), **params}
        result['matrices'].append(record)
        print('certified case',ci,'Aut',record['full_automorphism_order'],
              'ranks',qrank,rrank,urank,flush=True)
    D,Q,layers,structure,case = decoded[0]
    bad = copy.deepcopy(Q); bad[0][1] += 1
    rejects(lambda: check_definition(D,21,bad,psd=False))
    malformed = copy.deepcopy(case); malformed['layers'][2].pop()
    rejects(lambda: decode_case(malformed,systems,transport,affine))
    rejects(lambda: exact_psd_rank(upper(steiner_certificate(9,layers)[2])))
    rejects(lambda: polynomial_psd(upper(steiner_certificate(9,layers)[2])))
    result['rejection_controls'] = 4
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--write-expected',action='store_true')
    args = parser.parse_args()
    assert not (args.check and args.write_expected)
    result = run()
    expected = Path(__file__).with_name('three9_expected.json')
    if args.check:
        assert result == json.loads(expected.read_text()),'expected-output mismatch'
    if args.write_expected:
        expected.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
