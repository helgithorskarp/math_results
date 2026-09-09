#!/usr/bin/env python3
"""Produce the exact dependency-clique obstruction; no target search."""
import argparse
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path


def allowed(matrix):
    rows = [(matrix >> (4*i)) & 15 for i in range(4)]
    for subset in range(1, 16):
        intersection = 15
        for i in range(4):
            if subset >> i & 1:
                intersection &= rows[i]
        if intersection.bit_count() >= 5-subset.bit_count():
            return False
    return True


def rectangle(a, b):
    return sum(1 << (4*i+j) for i in range(a) for j in range(b))


def produce(out):
    out.mkdir(parents=True, exist_ok=False)
    domain = [m for m in range(65536) if allowed(m)]
    domain_bytes = b''.join(m.to_bytes(2,'little') for m in domain)
    (out/'domain.bin').write_bytes(domain_bytes)
    d = len(domain)
    counts = {(a,b): sum(m & rectangle(a,b) == rectangle(a,b) for m in domain)
              for a,b in product(range(1,4), repeat=2) if a+b <= 4}
    rows = []
    events = []
    for sizes in product(range(1,4), repeat=3):
        if sum(sizes) != 5:
            continue
        a,b,c = sizes
        probability = Fraction(counts[a,b]*counts[a,c]*counts[b,c], d**3)
        multiplicity = comb(4,a)*comb(4,b)*comb(4,c)
        rows.append(dict(sizes=list(sizes), per_triple_count=multiplicity,
                         probability=str(probability)))
        for third in (3,4):
            blocks = (range(4,8), range(8,12), range(4*third,4*third+4))
            for choices in product(*(combinations(block, size)
                                     for block,size in zip(blocks,sizes))):
                vertices = tuple(v for group in choices for v in group)
                events.append((vertices, probability))
    events.sort()
    lines = [','.join(map(str, v))+'\t'+str(p)+'\n' for v,p in events]
    stream = ''.join(lines).encode()
    (out/'events.tsv').write_bytes(stream)
    total = sum((p for _,p in events), Fraction())
    minimum = min(p for _,p in events)
    weight_test = 2*len(events)*minimum
    result = dict(
        status=('FAILED_ASYMMETRIC_LLL_WEIGHTS_ON_SAME_EVENT_CLIQUE'
                if weight_test > 1 else 'UNRESOLVED_LLL_CERTIFICATE_PREREQUISITE'),
        matrix_encoding='bit 4*i+j joins vertex i of the first K4 to vertex j of the second',
        matrices_examined=65536, allowed_matrices=d,
        domain_sha256=hashlib.sha256(domain_bytes).hexdigest(),
        rectangle_counts={f'{a},{b}':v for (a,b),v in counts.items()},
        event_types=rows, event_count=len(events),
        events_sha256=hashlib.sha256(stream).hexdigest(),
        clique_probability_sum=str(total), clique_sum_minus_one=str(total-1),
        initial_sum_greater_than_one_test_fired=total>1,
        minimum_event_probability=str(minimum),
        twice_clique_size_times_minimum=str(weight_test),
        direct_weight_contradiction=weight_test>1,
        shared_matrix_blocks=[1,2], third_blocks=[3,4],
        physical_vertices=list(range(4,20)), q8_r_values=[5,6,7,8],
        affected_certificate_instances=2185424,
        new_original_task_exclusions=0, new_good43=0, resampling_steps=0,
        target_solver_calls=0, core_catalog_records_read=0)
    (out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    return result


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    print(json.dumps(produce(args.output),indent=2,sort_keys=True))
