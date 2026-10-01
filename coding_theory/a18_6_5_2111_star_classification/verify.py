#!/usr/bin/env python3
"""Literal eight-fixture checks and comparison of a complete reproduction."""
import argparse
from fractions import Fraction
from itertools import combinations
import hashlib
import json
from math import factorial, prod

import carrier as c
from paths import BASE, WORK


def literal_fixture(words):
    if len(words) != 20 or len(set(words)) != 20 or any(type(w) is not int or not 0 <= w < 131072 or w.bit_count() != 4 for w in words):
        raise RuntimeError('invalid literal twenty-quadruple fixture')
    blocks = [set(z for z in range(17) if w >> z & 1) for w in words]
    covered = set()
    for block in blocks:
        for pair in combinations(sorted(block), 2):
            if pair in covered:
                raise RuntimeError('literal fixture covers a pair twice')
            covered.add(pair)
    if len(covered) != 120 or [sum(z in block for block in blocks) for z in range(17)] != [3, 4, 4, 4] + [5] * 13:
        raise RuntimeError('literal fixture pair count or replication differs')
    return set(combinations(range(17), 2)) - covered


def check(certificate_only=False):
    expected = json.loads((BASE / 'expected.json').read_text())
    count = 0
    for family in expected['packing_families']:
        for orbit in family['orbits']:
            literal_fixture(orbit['representative'])
            count += 1
    if count != 8 or count != expected['packing_isomorphism_classes']:
        raise RuntimeError('eight-representative fixture count differs')
    for origin in expected['source_provenance']:
        if hashlib.sha256((BASE / origin['filename']).read_bytes()).hexdigest() != origin['sha256']:
            raise RuntimeError('unchanged native source provenance differs')
    if certificate_only:
        result = dict(status='EIGHT POSITIVE FIXTURES VERIFIED; enumeration completeness not checked',
                      agent='six-code-3', role='researcher', fixtures=count)
        print(json.dumps(result))
        return result
    run = json.loads((WORK / 'proof_run.json').read_text())
    if not run['status'].startswith('COMPLETE') or len(run['fibers']) != 75:
        raise RuntimeError('INCOMPLETE reproduction cannot establish classification')
    leaves = json.loads((WORK / 'leave_carrier.json').read_text())
    hubs = json.loads((WORK / 'hub_carrier.json').read_text())
    actual = json.loads((WORK / 'packing_classes.json').read_text())
    if actual['status'] != 'COMPLETE PACKING ISOMORPHISM CLASSIFICATION':
        raise RuntimeError('INCOMPLETE orbit classification')
    if c.digest(leaves) != expected['leave_carrier_sha256'] or c.digest({key: value for key, value in hubs.items() if key not in ('seconds', 'maxrss_kib')}) != expected['hub_carrier_sha256']:
        raise RuntimeError('full independently checked carrier hashes differ')
    families = [{key: value for key, value in family.items() if key not in ('seconds', 'status')} for family in actual['cases']]
    if families != expected['packing_families']:
        raise RuntimeError('all packing orbit records differ entry by entry')
    covered_keys = {(q['index'], q['prefix_index']) for q in run['fibers']}
    desired_keys = {(q['index'], q['prefix_index']) for q in expected['fibers']}
    if len(covered_keys) != 75 or covered_keys != desired_keys:
        raise RuntimeError('native fiber coverage repeated or incomplete')
    for spec in expected['fibers']:
        index, prefix = spec['index'], spec['prefix_index']
        stem = f'hub_{index}_{prefix}' if spec['mode'] == 'hub-only' else 'twice_5_0'
        primary = json.loads((WORK / (stem + '_fullcover.jsonl')).read_text())
        separate = json.loads((WORK / (stem + '_dlx.jsonl')).read_text())
        if primary['index'] != 0 or separate['index'] != 0 or primary['covers'] != separate['covers']:
            raise RuntimeError('native output streams differ entry by entry')
        if len(primary['covers']) != spec['covers'] or c.digest(primary['covers']) != spec['covers_sha256']:
            raise RuntimeError('native complete cover fingerprint differs')
    by_leave = {}
    for family in actual['cases']:
        index, prefix = family['index'], family['prefix_index']
        multiplier = hubs['cases'][index]['orbits'][prefix]['orbit_size']
        by_leave[index] = by_leave.get(index, 0) + family['cover_count'] * multiplier
        leave = set(map(tuple, leaves['cases'][index]['leave']))
        for orbit in family['orbits']:
            if literal_fixture(orbit['representative']) != leave:
                raise RuntimeError('literal representative leave differs')
    if {str(key): value for key, value in by_leave.items()} != expected['canonical_leave_covers']:
        raise RuntimeError('labeled hub multiplicity reconstruction differs')
    fixed_labels = 0
    for index, cover_count in by_leave.items():
        leaf = leaves['cases'][index]
        denominator = prod(factorial(len(cohort)) for cohort in leaf['cohorts']) * factorial(leaf['m']) * 2 ** leaf['m']
        if factorial(13) % denominator:
            raise RuntimeError('nonintegral low-leave attachment multiplicity')
        fixed_labels += factorial(13) // denominator * leaf['orbit_size'] * cover_count
    independent = sum(Fraction(6 * factorial(13), orbit['packing_automorphism_order'])
                      for family in families for orbit in family['orbits'])
    if independent.denominator != 1 or fixed_labels != independent or fixed_labels != expected['fixed_profile_labeled_packings']:
        raise RuntimeError('two independent labeled packing counts differ')
    if sum(q['primary_nodes'] for q in run['fibers']) != expected['primary_nodes'] or sum(q['sparse_nodes'] for q in run['fibers']) != expected['sparse_nodes']:
        raise RuntimeError('total exact-cover nodes differ')
    result = dict(agent='six-code-3', role='researcher', status='COMPLETE',
                  packing_isomorphism_classes=8, complete_cover_fibers=75,
                  first_hub_normal_form_covers=actual['first_hub_normal_form_covers'],
                  fixed_profile_labeled_packings=fixed_labels,
                  primary_nodes=expected['primary_nodes'], sparse_nodes=expected['sparse_nodes'])
    if result['first_hub_normal_form_covers'] != 45504:
        raise RuntimeError('normalized cover multiplicity differs')
    (WORK / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate-only', action='store_true')
    check(parser.parse_args().certificate_only)
