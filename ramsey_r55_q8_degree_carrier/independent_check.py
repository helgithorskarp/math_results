#!/usr/bin/env python3
"""Audit literal C++ domains and replay marginals by Kronecker substitution.

Imports no producer module. Polynomial products are packed into integers,
not formed by the producer's dictionary convolutions.
"""
import argparse
import hashlib
import itertools as it
import json
import math
from fractions import Fraction
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pair_product(polynomials, offset):
    # Degree in each variable is at most 39. Base64 prevents variable mixing;
    # digit width exceeds the entire product mass, preventing coefficient carry.
    total = math.prod(sum(p) for p in polynomials)
    width = total.bit_length()+1
    product = 1
    for coefficients in polynomials:
        packed = sum(count << (width*(a+64*b))
                     for a in range(5) for b in range(5)
                     if (count := coefficients[5*a+b]))
        product *= packed
    digit = (1 << width)-1
    recovered = sum((product >> (width*(a+64*b))) & digit
                    for a in range(40) for b in range(40))
    require(recovered == total, "Kronecker mass lost")
    accepted = sum((product >> (width*(a+64*b))) & digit
                   for a in range(max(0,18-offset),25-offset)
                   for b in range(max(0,18-offset),25-offset))
    return accepted, total


def verify(package, native):
    expected = json.loads((package/'EXPECTED.json').read_text())
    pins = json.loads((package/'DOMAIN_PINS.json').read_text())
    records = json.loads(native.read_text())
    require(len(records) == 6, "wrong domain count")
    domains = {}
    for record in records:
        key = f'{record["left"]}{record["right"]}{record["root"]}'
        require(key not in domains and key in pins, "duplicate/unknown domain")
        flags = record['allowed_flags']
        require(len(flags) == 65536 and set(flags) <= {'0','1'}, "invalid flags")
        bitmap = int(flags[::-1], 2).to_bytes(8192,'big')
        require(hashlib.sha256(bitmap).hexdigest() == pins[key]['bitmap_sha256'],
                "literal domain differs from reviewed carrier")
        require(record['total'] == flags.count('1') == pins[key]['count'], "domain size")
        # Audit the native degree projection against its own literal allowed words.
        hist = [[0]*25 for _ in range(12)]
        for word, bit in enumerate(flags):
            if bit == '0':
                continue
            row = [sum((word >> (4*u+v)) & 1 for v in range(4)) for u in range(4)]
            col = [sum((word >> (4*u+v)) & 1 for u in range(4)) for v in range(4)]
            for side, values in enumerate((row,col)):
                for k,(u,v) in enumerate(it.combinations(range(4),2)):
                    hist[6*side+k][5*values[u]+values[v]] += 1
        require(hist == record['hist'], "native marginal projection differs")
        domains[key] = record
    require(sorted(row['r'] for row in expected['classes']) == [5,6,7,8], "macro classes")
    total_carrier = 0
    total_bound = Fraction(0)
    marginals = 0
    report = []
    for row in expected['classes']:
        r = row['r']
        require([b['block'] for b in row['blocks']] == list(range(8)), "block coverage")
        incidence = [set() for _ in range(19)]
        carrier = 1
        for i,j in it.combinations(range(8),2):
            key = f'{int(i<r)}{int(j<r)}{int(i==0)}'
            carrier *= domains[key]['total']
            incidence[i].add(('matrix',i,j)); incidence[j].add(('matrix',i,j))
        for i in range(8):
            for v in range(11):
                incidence[i].add(('star',i,v)); incidence[8+v].add(('star',i,v))
                carrier *= 15
        coordinates = set().union(*incidence)
        require(len(coordinates) == 116 and
                all(sum(c in event for event in incidence)==2 for c in coordinates),
                "twofold product-coordinate cover failed")
        require(carrier == row['per_task_carrier'], "carrier mismatch")
        square = Fraction(1)
        for block_info in row['blocks']:
            block = block_info['block']
            require([c['selected'] for c in block_info['choices']] ==
                    [list(p) for p in it.combinations(range(4),2)], "pair coverage")
            probabilities = []
            for pair_no, choice in enumerate(block_info['choices']):
                polynomials = []
                for other in range(8):
                    if other == block:
                        continue
                    i,j = sorted((block,other))
                    record = domains[f'{int(i<r)}{int(j<r)}{int(i==0)}']
                    polynomials.append(record['hist'][pair_no+6*int(block==j)])
                u,v = choice['selected']
                star = [0]*25
                for word in range(16):
                    if word == (15 if block<r else 0):
                        continue
                    star[5*((word>>u)&1)+((word>>v)&1)] += 1
                polynomials.extend([star]*11)
                count,size = pair_product(polynomials,3 if block<r else 0)
                require((count,size)==(choice['accepted'],choice['total']), "degree marginal mismatch")
                probabilities.append(Fraction(count,size)); marginals += 1
            chosen = block_info['best']
            require(chosen in block_info['choices'] and
                    Fraction(chosen['accepted'],chosen['total']) == min(probabilities), "best marginal")
            square *= min(probabilities)
        # Core marginal: one-variable integer encoding, independent of producer DP.
        width = (15**8).bit_length()+1
        packed = 1
        for i in range(8):
            packed *= sum(1 << (width*word.bit_count()) for word in range(16)
                          if word != (15 if i<r else 0))
        digit = (1<<width)-1
        counts = [sum((packed >> (width*k)) & digit
                      for k in range(max(0,18-d), min(32,24-d)+1)) for d in range(11)]
        require(counts==row['core']['accepted_by_fixed_degree'] and
                max(counts)==row['core']['maximum'] and row['core']['total']==15**8, "core marginal")
        square *= Fraction(max(counts),15**8)**11
        require(square == Fraction(**row['probability_squared_upper']), "product inequality data")
        upper = Fraction(**row['probability_upper'])
        require(upper >= 0 and upper*upper >= square, "unsafe square-root rounding")
        require(256*square <= 1 and row['each_task_factor16'], "per-task gate failure")
        total_carrier += 546356*carrier
        total_bound += 546356*carrier*upper
        report.append({'r':r,'retained_upper':{'numerator':upper.numerator,'denominator':upper.denominator},
                       'selected_pairs':[b['best']['selected'] for b in row['blocks']]})
    require(expected['q']==8 and expected['core_count']==546356 and expected['tasks']==2185424,
            "branch definition mismatch")
    require(total_carrier==expected['carrier'] and
            total_bound==Fraction(**expected['retained_upper_rational']), "aggregate mismatch")
    require(16*total_bound <= total_carrier and expected['parent_factor16'] and
            expected['parent_source']=='h3873', "parent bound failed")
    # The parent product measure is not the sorted carrier's uniform measure.
    # Transfer only the distinct-root part and charge all repeated-root outputs.
    ordered = expected['ordered_transfer']
    require(ordered['source']=='h3887' and [x['r'] for x in ordered['classes']]==[5,6,7,8],
            "wrong current carrier")
    sorted_carrier = 0; sorted_bound = Fraction(0)
    for parent_row, row in zip(expected['classes'],ordered['classes']):
        r=row['r']; a,b=r-1,8-r
        # Compute multiset and distinct counts by multiplying short recurrences,
        # independently of the producer's binomial calls.
        multi = unique = 1
        for alphabet, count in ((1998,a),(1931,b)):
            m=u=1
            for k in range(1,count+1):
                m=m*(alphabet+k-1)//k
                u=u*(alphabet-k+1)//k
            multi*=m; unique*=u
        sequences=1998**a*1931**b; orders=math.prod(range(1,a+1))*math.prod(range(1,b+1))
        require((multi,unique,sequences,orders)==(row['root_multisets'],row['distinct_root_multisets'],
                row['root_sequences'],row['label_orders']), "root repetition count")
        rest = 15**88
        for i,j in it.combinations(range(1,8),2):
            rest *= domains[f'{int(i<r)}{int(j<r)}0']['total']
        size=multi*rest
        require(row['remaining_coordinate_count']==rest and row['sorted_per_task_carrier']==size,
                "sorted carrier size")
        pairs=[b['best']['selected'] for b in parent_row['blocks']]
        require(all(pairs[i]==pairs[1] for i in range(1,r)) and
                all(pairs[i]==pairs[r] for i in range(r,8)), "event not invariant under block order")
        p=Fraction(**parent_row['probability_upper'])
        upper=(Fraction(parent_row['per_task_carrier'],orders)*p+(multi-unique)*rest)/size
        require(upper==Fraction(**row['sorted_fraction_bound']), "unsafe order transfer")
        require(16*upper<=1 and row['current_task_factor16'], "current per-task gate failed")
        sorted_carrier+=546356*size; sorted_bound+=546356*size*upper
    require(sorted_carrier==ordered['sorted_q8_carrier'] and
            sorted_bound==Fraction(**ordered['sorted_retained_upper']), "sorted aggregate")
    require(16*sorted_bound<=sorted_carrier and ordered['declared_gate_factor16'],
            "declared current-carrier gate failed")
    pins=json.loads((package/'CARRIER_PINS.json').read_text())
    require([r['q'] for r in pins['q8_classes']]==[8]*4, 'pinned branch')
    for row,pin in zip(ordered['classes'],pins['q8_classes']):
        require(row['r']==pin['r'] and row['sorted_per_task_carrier']==pin['per_task'] and
                pin['core_stop']==546356 and pin['core_start']==0, 'h3887 registry differs')
    summary=json.loads((package/'SUMMARY.json').read_text())
    require(int(summary['exact_q8_carrier'])==sorted_carrier and
            int(summary['retained_integer_upper'])==(sorted_bound.numerator+sorted_bound.denominator-1)//sorted_bound.denominator,
            'summary integer count')
    require(sorted_bound/sorted_carrier < Fraction(**summary['fraction_upper']) and
            18*sorted_bound < sorted_carrier and sorted_bound < 2**748, 'summary simplified bound')
    require(expected['new_q10_decisions']==expected['new_q7r5_decisions']==0, "scope count")
    return {'status':'INDEPENDENT_Q8_DEGREE_CARRIER_ACCEPT','domains':6,
            'literal_word_cases':6*65536,'bivariate_marginals':marginals,
            'events_per_task':19,'coordinates_per_task':116,'reads_per_coordinate':2,
            'parent_q8_factor16':True,'current_h3887_q8_factor16':True,'classes':report}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('package',type=Path)
    parser.add_argument('native',type=Path);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args(); result=verify(args.package,args.native)
    args.out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
