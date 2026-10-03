"""Independent representation: literal2520 APs and all four10080 lifts.

No producer import. Compare every raw original-phase pair and every field.
Same-author algorithmic check, not independent peer review or formal proof.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from math import lcm
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def ap(period, modulus, phase):
    result = 0
    for x in range(phase, period, modulus):
        result |= 1 << x
    return result


def digest(data):
    return sha256(json.dumps(data, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def build_reference():
    ds = sorted({3**a * 5**b * 7**c for a in range(3) for b in range(2) for c in range(2)})
    unused = ds[1:]
    prefix = [[8,0],[9,0],[10,1],[14,0],[12,10],[16,2],[28,4],[32,6]]
    base_prefix = [x for x in prefix if 2520 % x[0] == 0]
    residual = ((1 << 2520) - 1)
    for m, a in base_prefix:
        residual &= ~ap(2520, m, a)
    parent_masks = {r: residual & ap(2520, 8, r) for r in range(8)}
    require([parent_masks[r].bit_count() for r in range(8)] == [0,224,150,224,200,224,150,224],
            'The literal six-BASE physical shadows changed')
    odd_ap = {d: [ap(2520, d, a) for a in range(d)] for d in ds}
    capacities = {}
    for d in ds:
        left = [(parent_masks[2] & points).bit_count() for points in odd_ap[d]]
        right = [(parent_masks[6] & points).bit_count() for points in odd_ap[d]]
        require(left == right, 'Mandatory-parent physical phase populations differ')
        capacities[d] = max(left)
    sums = {str(n): [[*xs, sum(capacities[d] for d in xs)]
                     for xs in combinations(unused, n)] for n in range(1,5)}
    intersections = {str(n): [[*xs, lcm(*xs), capacities[lcm(*xs)]]
                              for xs in combinations(unused, n)] for n in (2,3)}
    pair_sums = [[*xs, sum(capacities[lcm(*ys)] for ys in combinations(xs,2))]
                 for xs in combinations(unused,3)]
    triple_sums = [[*xs, sum(capacities[lcm(*ys)] for ys in combinations(xs,3))]
                   for xs in combinations(unused,4)]

    # Real literal original phases generate every local inactive/active pattern.
    # Scan phase candidates to solve CRT, rather than using the producer's masks.
    physical_patterns = {}
    for parent in (2,6):
        x = parent
        points = [x + 2520*k for k in range(4)]
        for kind, binary_states, two in (('H', (0,5,10),16), ('Q',(0,1,2,4,8),32)):
            for position, d in enumerate((3,5,7,9)):
                for state in binary_states:
                    if state:
                        touched = next(k for k in range(4) if state & (1 << k))
                        binary = points[touched] % two
                        odd = x % d
                    else:
                        binary = x % two
                        odd = (x+1) % d
                    phase = next(a for a in range(two*d) if a % two == binary and a % d == odd)
                    members = {k for k,y in enumerate(points) if y % (two*d) == phase}
                    require(sum(1 << k for k in members) == state, 'Literal original phase does not realize its local pattern')
                    physical_patterns[parent,kind,position,state] = members

    controls = []
    for parent, numbers in ((2,range(1,4)),(6,range(2,5))):
        mandatory = {k for k in range(4) if (parent + 2520*k) % (16 if parent == 2 else 32) == parent}
        for n in numbers:
            for nh in range(n+1):
                for hs in product((0,5,10), repeat=nh):
                    for qs in product((0,1,2,4,8), repeat=n-nh):
                        extra = set()
                        for i,s in enumerate(hs):
                            extra |= physical_patterns[parent,'H',i,s]
                        for i,s in enumerate(qs):
                            extra |= physical_patterns[parent,'Q',i,s]
                        covered = mandatory | extra == set(range(4))
                        nonempty_h = any(hs)
                        active_q = sum(s > 0 for s in qs)
                        if parent == 2:
                            if n == 1:
                                valid = nh == 1 and nonempty_h
                            elif n == 2:
                                valid = nonempty_h if nh else active_q == 2
                            elif nh >= 2:
                                valid = nonempty_h
                            else:
                                valid = nonempty_h or active_q >= 2
                        elif nh == n:
                            valid = extra == set(range(4))
                        elif n == 2:
                            valid = nh == 1 and nonempty_h and active_q == 1
                        elif n == 3:
                            valid = nonempty_h if nh else active_q == 3
                        elif nh >= 2:
                            valid = nonempty_h
                        else:
                            valid = nonempty_h or active_q >= 3
                        require(not covered or valid, 'A literal four-lift incidence contradicts its footprint bound')
                        controls.append([parent,n,nh,list(hs),list(qs),covered,bool(valid),sum(1 << k for k in extra)])

    phase_rows = []
    raw_blocks = []
    # Actual10080 original APs are built once. Their union is tested at ALL four
    # lifts of each literal BASE residue, without an odd-CRT compatibility test.
    whole_tail_aps = {(r,d): [ap(10080,16*d,a) for a in range(r,16*d,8)]
                      for r in (1,3,4,5,7) for d in unused}
    for r in (1,3,4,5,7):
        holes = parent_masks[r]
        for g,h in combinations(unused,2):
            q = lcm(g,h)
            populations = [(holes & points).bit_count() for points in odd_ap[q]]
            phase_rows.append([r,g,h,q,populations])
            counts = []
            for first in whole_tail_aps[r,g]:
                for second in whole_tail_aps[r,h]:
                    union = first | second
                    all_lifts = union & (union >> 2520) & (union >> 5040) & (union >> 7560)
                    counts.append((all_lifts & holes).bit_count())
            raw_blocks.append([r,g,h,counts])
    third_max = {str(r): max(max(row[4]) for row in phase_rows if row[0] == r)
                 for r in (1,3,4,5,7)}

    # Reconstruct every upper bound from the independently computed physical
    # capacity rows. No imported numeric seven-tail table is trusted here.
    S = {n:max(row[-1] for row in sums[str(n)]) for n in range(1,5)}
    I = {n:max(row[-1] for row in intersections[str(n)]) for n in (2,3)}
    Q3 = max(row[-1] for row in pair_sums)
    Q4 = 4*I[3]  # Conservative union of four triple intersections.
    cases = [
        ['2+5','H','HHHQ',S[4]], ['2+5','H','HHQQ',S[3]],
        ['2+5','H','HQQQ',S[2]+I[3]], ['2+5','H','QQQQ',S[1]+Q4],
        ['3+4','HH','HHQ',S[4]], ['3+4','HH','HQQ',S[3]],
        ['3+4','HH','QQQ',S[2]+I[3]], ['3+4','HQ','HHQ',S[3]],
        ['3+4','HQ','HQQ',S[2]], ['3+4','HQ','QQQ',S[1]+I[3]],
        ['3+4','QQ','HHQ',I[2]+S[2]], ['3+4','QQ','HQQ',I[2]+S[1]],
        ['3+4','QQ','QQQ',I[2]+I[3]],
        ['4+3','HHH','HQ',S[4]], ['4+3','HHQ','HQ',S[3]],
        ['4+3','HQQ','HQ',S[2]+I[2]], ['4+3','QQQ','HQ',Q3+S[1]],
    ]
    for r in (1,3,4,5,7):
        cases.append(['2+3+2','H','HQ',r,S[2]+third_max[str(r)]])
    return {'agent':'six-covering-2','role':'researcher','literal_prefix':prefix,
            'essential_originals_explicit':[16,32],'original_moduli_divide':10080,
            'unused_odd_cofactors':unused,'capacity_rows':[[d,capacities[d]] for d in ds],
            'globally_distinct_extra16_rows':sums,'quarter_intersection_rows':intersections,
            'three_quarter_pair_sum_rows':pair_sums,'four_quarter_triple_sum_rows':triple_sums,
            'complete_inactive_binary_controls':controls,
            'third_parent_all_odd_phase_rows':phase_rows,
            'third_parent_all_raw_original_phase_blocks':raw_blocks,
            'third_parent_maxima':third_max,'raw_original_phase_pairs':sum(len(row[3]) for row in raw_blocks),
            'complete_seven_tail_capacity_cases':cases,'maximum_seven_tail_BASE_holes':max(row[-1] for row in cases),
            'capacity_175_is_claimed_sharp':False,'ordinary_bridges_formalized':False,
            'independent_reviewer':False,'global_bound_changed':False}


def audit(candidate):
    reference = build_reference()
    require(candidate == reference, 'Entire record differs from the literal physical reference')
    require(reference['maximum_seven_tail_BASE_holes'] == 175,
            'Literal seven-tail upper bound is not175')
    require(reference['raw_original_phase_pairs'] == 2698300, 'Raw original phase domain incomplete')
    require(len(reference['complete_inactive_binary_controls']) == 2091, 'Binary type domain incomplete')

    # This full independently reconstructed reference is cached only AFTER its
    # literal mathematical audit. Every damaged candidate is still compared
    # against the ENTIRE reference, including all2,698,300 raw pair entries.
    damages = []
    def probe(name, change, restore):
        change()
        try:
            require(candidate != reference, 'Semantic damage was accepted: '+name)
            damages.append(name)
        finally:
            restore()
    old = candidate['literal_prefix'][3][1]
    probe('wrong14-prefix', lambda:candidate['literal_prefix'][3].__setitem__(1,1),
          lambda:candidate['literal_prefix'][3].__setitem__(1,old))
    old = candidate['essential_originals_explicit'][:]
    probe('dropped32-essentiality', lambda:candidate.__setitem__('essential_originals_explicit',[16]),
          lambda:candidate.__setitem__('essential_originals_explicit',old))
    row = candidate['capacity_rows'][-1];old = row[-1]
    probe('wrong315-capacity',lambda:row.__setitem__(-1,old+1),lambda:row.__setitem__(-1,old))
    row = candidate['complete_inactive_binary_controls'][0];old = row[5]
    probe('inactive-pattern-marked-covered',lambda:row.__setitem__(5,not old),lambda:row.__setitem__(5,old))
    row = candidate['third_parent_all_odd_phase_rows'][-1][-1];old = row[-1]
    probe('last-physical-odd-phase',lambda:row.__setitem__(-1,old+1),lambda:row.__setitem__(-1,old))
    row = candidate['third_parent_all_raw_original_phase_blocks'][-1][-1];old = row[-1]
    probe('last-literal-original-pair',lambda:row.__setitem__(-1,old+1),lambda:row.__setitem__(-1,old))
    row = candidate['third_parent_all_raw_original_phase_blocks'][0][-1];old = row[-1]
    probe('omitted-raw-original-pair',lambda:row.pop(),lambda:row.append(old))
    row = candidate['complete_seven_tail_capacity_cases'][0];old = row[-1]
    probe('false174-capacity-row',lambda:row.__setitem__(-1,174),lambda:row.__setitem__(-1,old))
    old = candidate['global_bound_changed']
    probe('unproved-global-bound',lambda:candidate.__setitem__('global_bound_changed',True),
          lambda:candidate.__setitem__('global_bound_changed',old))
    require(candidate == reference, 'Valid entire record not restored after semantic controls')
    return {'agent':'six-covering-2','role':'researcher','every_full_mathematical_field_compared':True,
            'whole_record_sha256':digest(reference),'raw_original_phase_pairs':2698300,
            'complete_binary_controls':2091,'complete_third_parent_odd_phase_entries':sum(len(row[4]) for row in reference['third_parent_all_odd_phase_rows']),
            'third_parent_maxima':reference['third_parent_maxima'],'seven_tail_capacity':175,
            'semantic_damages_rejected':damages,'valid_record_accepted_again':True,
            'independent_reviewer':False,'global_bound_changed':False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('record',type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(json.loads(args.record.read_text())),sort_keys=True))
