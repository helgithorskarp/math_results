"""Capped maximal-rank H for every union of four block-disjoint STS(9).

CPython 3.11+, standard library, assertions enabled. Regenerates complete
input coverage and full point groups; fixed rational tables are untrusted.
Author: six-downset-2, researcher. Bridges: FOUR_STS9_PROOF.md.
"""
import argparse
import copy
import itertools
import json
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path

from certificates import affine_sts9, check_sts, downset, steiner_certificate
from maxrank_certificates import mix_certificates
from verify import check_definition, exact_psd_rank, matrix_hash, rejects
from verify_three9 import (buffered_upper, complete_three_cohort, compose,
                           gram_rank, image, inverse, supported_representatives,
                           upper)
from verify_two9 import polynomial_psd


def union_structure_four(union, systems, transport, affine):
    """Full groups/keys include every contained STS and alternative cover."""
    U = set(union)
    assert len(U) == 48
    contained = sorted(t for t in systems if set(t) <= U)
    decompositions = []
    for i, a in enumerate(contained):
        for j in range(i+1, len(contained)):
            b = contained[j]
            if set(a) & set(b):
                continue
            for c in contained[j+1:]:
                if set(c) & (set(a)|set(b)):
                    continue
                d = tuple(sorted(U-set(a)-set(b)-set(c)))
                if d in contained and c < d:
                    decompositions.append((a,b,c,d))
    assert decompositions
    autos = set()
    canonical = None
    for t in contained:
        q = transport[t]
        for g in affine:
            p = compose(q,g)
            if image(union,p) == union:
                autos.add(p)
        normalized = image(union,inverse(q))
        for g in affine:
            candidate = image(normalized,g)
            if canonical is None or candidate < canonical:
                canonical = candidate
    assert tuple(range(9)) in autos and all(inverse(p) in autos for p in autos)
    return {'canonical':canonical, 'group':sorted(autos),
            'contained':contained, 'decompositions':decompositions}


def complete_four_cohort(first):
    parents,systems,transport,affine,three_summary = complete_three_cohort(first)
    representatives = []
    parent_summary = []
    for entries in (parents[k] for k in sorted(parents)):
        layers,structure = entries[0]
        group = structure['group']
        forbidden = set().union(*map(set,layers))
        candidates = {t for t in systems if not set(t)&forbidden}
        remaining = set(candidates)
        orbit_sizes = []
        while remaining:
            fourth = min(remaining)
            images = {image(fourth,g) for g in group}
            assert images <= remaining
            stabilizer = sum(image(fourth,g) == fourth for g in group)
            assert len(images)*stabilizer == len(group)
            remaining -= images
            orbit_sizes.append(len(images))
            representatives.append(tuple(layers)+(fourth,))
        parent_summary.append({'parent_full_automorphism_order':len(group),
                               'disjoint_fourth_systems':len(candidates),
                               'fourth_orbit_sizes':orbit_sizes})
    assert [r['disjoint_fourth_systems'] for r in parent_summary] == [7,6,8,6,10,8,11,10,8]
    assert [len(r['fourth_orbit_sizes']) for r in parent_summary] == [5,3,4,3,5,2,5,3,2]
    assert len(representatives) == 32
    classes = {}
    for layers in representatives:
        union = tuple(sorted(set().union(*map(set,layers))))
        structure = union_structure_four(union,systems,transport,affine)
        assert tuple(sorted(layers)) in structure['decompositions']
        classes.setdefault(structure['canonical'],[]).append((layers,structure))
    assert len(classes) == 12
    class_summary = []
    for key,entries in sorted(classes.items()):
        structure = entries[0][1]
        order = len(structure['group'])
        assert all(len(e[1]['group']) == order and
                   len(e[1]['contained']) == len(structure['contained']) and
                   len(e[1]['decompositions']) == len(structure['decompositions'])
                   for e in entries)
        class_summary.append({'extension_representatives':len(entries),
                              'full_automorphism_order':order,
                              'contained_STSs':len(structure['contained']),
                              'unordered_decompositions':len(structure['decompositions'])})

    # Independent entry-level unquotiented coverage. Bit boards are an exact
    # encoding of subsets of the 84 possible triples, not hashes of unions.
    triples = sorted(sum(1<<i for i in c) for c in itertools.combinations(range(9),3))
    bit = {a:1<<i for i,a in enumerate(triples)}
    def board(t):
        return sum(bit[a] for a in t)
    fixed = board(first)
    disjoint = sorted(board(t) for t in systems if not set(t)&set(first))
    direct = set()
    direct_decompositions = 0
    for i,a in enumerate(disjoint):
        for j in range(i+1,len(disjoint)):
            b = disjoint[j]
            if a&b:
                continue
            for c in disjoint[j+1:]:
                if not c&(a|b):
                    direct.add(fixed|a|b|c)
                    direct_decompositions += 1
    covered = set()
    for entries in classes.values():
        layers,structure = entries[0]
        union = tuple(sorted(set().union(*map(set,layers))))
        participating = {t for dec in structure['decompositions'] for t in dec}
        for t in participating:
            normalized = image(union,inverse(transport[t]))
            covered.update(board(image(normalized,g)) for g in affine)
    assert direct == covered and len(direct) == 10048
    labelled = sum(362880//r['full_automorphism_order'] for r in class_summary)
    weighted = sum((362880//r['full_automorphism_order'])*r['unordered_decompositions']
                   for r in class_summary)
    assert labelled == 2068080 and weighted*4 == 840*direct_decompositions
    return classes,systems,transport,affine, {
        'three_system_baseline':three_summary, 'extension_pair_orbits':32,
        'parent_cases':parent_summary, 'union_isomorphism_classes':class_summary,
        'fixed_first_union_count':len(direct),
        'fixed_first_union_sha256':sha256(json.dumps(sorted(direct),separators=(',',':')).encode()).hexdigest(),
        'fixed_first_decomposition_count':direct_decompositions,
        'labelled_union_count':labelled, 'labelled_decomposition_count':weighted}


def decode_case(case,systems,transport,affine):
    layers = [tuple(t) for t in case['layers']]
    assert len(layers) == 4 and layers[0] == tuple(affine_sts9())
    for t in layers:
        check_sts(9,t)
    union = tuple(sorted(set().union(*map(set,layers))))
    assert len(union) == 48
    D = downset(9,layers)
    assert len(D) == 94
    structure = union_structure_four(union,systems,transport,affine)
    assert tuple(sorted(layers)) in structure['decompositions']
    group = structure['group']
    assert len(group) == case['full_automorphism_order']
    reps = supported_representatives(D,group)
    den = case['denominator']
    assert isinstance(den,int) and den > 0
    nums = case['orbit_numerators']
    assert len(nums) == len(reps) and all(isinstance(x,int) for x in nums)
    table = {ab:F(value,den) for ab,value in zip(reps,nums)}
    Q = [[F(25 if i == j and i else 0) for j in range(94)] for i in range(94)]
    filled = {}
    # Expand whole orbits with a checked permutation action. Each seed fills
    # every entry in its orbit; consistency checks reject collisions.
    from verify_two9 import moved
    index = {a:i for i,a in enumerate(D)}
    for (a,b),value in table.items():
        for p in group:
            i,j = index[moved(a,p)],index[moved(b,p)]
            key = tuple(sorted((i,j)))
            assert key not in filled or filled[key] == (a,b), 'overlapping seed orbits'
            filled[key] = (a,b)
            Q[i][j] = Q[j][i] = value
    assert set(filled) == {(i,j) for i,a in enumerate(D)
                           for j in range(i,94) if not a&D[j]}, 'incomplete orbit coverage'
    assert matrix_hash(Q) == case['centered_matrix_sha256']
    return D,Q,layers,structure


def run():
    data = json.loads(Path(__file__).with_name('four9_certificates.json').read_text())
    assert (data['N'],data['s']) == (94,25)
    classes,systems,transport,affine,coverage = complete_four_cohort(tuple(affine_sts9()))
    decoded = []
    keys = []
    for case in data['cases']:
        D,Q,layers,structure = decode_case(case,systems,transport,affine)
        decoded.append((D,Q,layers,structure,case))
        keys.append(structure['canonical'])
    assert len(keys) == len(set(keys)) == 12 and set(keys) == set(classes)
    result = {'arithmetic':'fractions.Fraction and arbitrary-precision integers',
              'coverage':coverage, 'matrices':[]}
    for ci,(D,Q,layers,structure,case) in enumerate(decoded):
        qrank = check_definition(D,25,Q)
        assert qrank == 84 and all(x == 1 for x in Q[0])
        urank = exact_psd_rank(upper(Q))
        brank = exact_psd_rank(buffered_upper(Q,F(1,2)))
        assert urank == brank == 93
        lp = polynomial_psd(Q)
        up = polynomial_psd(upper(Q))
        assert (lp['rank'],up['rank']) == (qrank,urank)
        stars = [[F(bool(a>>i&1))-F(25,94) for a in D] for i in range(9)]
        w = [F(j == 0)-F(1,94) for j in range(94)]
        assert gram_rank(stars) == 9 and gram_rank(stars+[w]) == 10
        Do,so,Qo = steiner_certificate(9,layers)
        assert D == Do and so == 25 and check_definition(D,25,Qo) == 45
        assert Qo[0][0] == 1027 and sum(Qo[i][i] for i in range(94)) == 3352
        assert sum(Qo[1][j]*w[j] for j in range(94)) == -132
        _,_,repaired,params = mix_certificates((D,25,Q),(Do,so,Qo))
        assert params == {'epsilon':'1/13408','ordinary_trace':'3352'}
        rrank = check_definition(D,25,repaired)
        rurank = exact_psd_rank(upper(repaired))
        rbrank = exact_psd_rank(buffered_upper(repaired,F(1,4)))
        assert (rrank,rurank,rbrank) == (85,93,93)
        record = {'case':ci, 'full_automorphism_order':len(structure['group']),
                  'supported_pair_orbits':len(case['orbit_numerators']),
                  'centered_rank_Q':qrank, 'rank_upper':urank,
                  'half_buffer_rank':brank, 'centered_matrix_sha256':matrix_hash(Q),
                  'lower_polynomial':lp, 'upper_polynomial':up,
                  'maximal_rank_Q':rrank, 'repaired_upper_rank':rurank,
                  'quarter_buffer_rank':rbrank,
                  'repaired_matrix_sha256':matrix_hash(repaired), **params}
        result['matrices'].append(record)
        print('certified case',ci,'Aut',len(structure['group']),
              'ranks',qrank,rrank,urank,flush=True)
    D,Q,layers,structure,case = decoded[0]
    bad = copy.deepcopy(Q)
    bad[0][1] += 1
    rejects(lambda:check_definition(D,25,bad,psd=False))
    malformed = copy.deepcopy(case)
    malformed['layers'][3].pop()
    rejects(lambda:decode_case(malformed,systems,transport,affine))
    rejects(lambda:exact_psd_rank(upper(steiner_certificate(9,layers)[2])))
    rejects(lambda:polynomial_psd(upper(steiner_certificate(9,layers)[2])))
    result['rejection_controls'] = 4
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--write-expected',action='store_true')
    args = parser.parse_args()
    assert not (args.check and args.write_expected)
    result = run()
    expected = Path(__file__).with_name('four9_expected.json')
    if args.check:
        assert result == json.loads(expected.read_text()),'expected-output mismatch'
    if args.write_expected:
        expected.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
