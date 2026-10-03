"""Definition-level local audit for the entire {d3,8,d5} Q obstruction.

Run each --column 0,...,4 separately. The ordinary proof permits all K subsets
of the whole Q footprint; no enumeration of those subsets is asserted.
Python3.10+ stdlib, no previous source, solver, native builder or input corpus.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
from math import gcd
from pathlib import Path
import json


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def mask(points):
    return sum(1 << t for t in points)


def record(digest, row):
    digest.update(json.dumps(row, separators=(',', ':')).encode()+b'\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--column', type=int, required=True)
    args = parser.parse_args()
    need(args.column in range(5), 'column must be0,...,4')
    F = tuple(t for t in range(180) if t % 9 != 3)
    ds = tuple(d for d in range(2,721) if 720 % d == 0 and d not in (2,4))
    es = sorted({d//gcd(d,4) for d in ds})
    supports = {e: tuple(mask(t for t in F if t % e == r) for r in range(e)) for e in es}
    raw = {d:max(m.bit_count() for m in supports[d//gcd(d,4)]) for d in ds}
    need(len(ds)==27 and len(F)==160 and sum(raw.values())==600, 'complete raw original resource pool')
    physical = {}
    maps = active = empty = 0
    representatives = {s: {t:next(y for y in range(4*t+3,5040,720) if y%7==s+2) for t in F}
                       for s in range(5)}
    for d in ds:
        e = d//gcd(d,4)
        inverse_phase = {(4*r+3)%d:r for r in range(e)}
        need(len(inverse_phase)==e, 'original gate injection')
        for a in range(7*d):
            maps += 1
            s = a%7-2
            observed = 0 if s not in representatives else mask(t for t in F if (representatives[s][t]-a)%(7*d)==0)
            r = inverse_phase.get(a%d)
            expected = 0 if s not in representatives or r is None else supports[e][r]
            need(observed==expected, 'literal original AP differs from projected support')
            if s in representatives and r is not None:
                key = (d,s,r)
                need(key not in physical, 'duplicate original physical phase')
                physical[key] = observed
            active += bool(observed)
            empty += not bool(observed)
    need((maps,active,empty,len(physical))==(16877,3225,13652,3495), 'complete original physical census')
    facts_digest, column_digest, fine_digest, slot_digest = sha256(),sha256(),sha256(),sha256()
    Q_tuples = positive_Q = zero_Q = original_inventory_checks = capacity_values = 0
    column_tuples = closed_column_tuples = fine_nominal_tuples = closed_fine_tuples = 0
    column_prefixes = fine_visits = fine_survivors = slot_visits = slot_survivors = 0
    equality_owner_types = Counter()

    def add(covered, owner, support, credit):
        if owner < 0:
            return covered, credit
        gain = (support & ~covered[owner]).bit_count()
        updated = list(covered)
        updated[owner] |= support
        return tuple(updated), credit-gain

    for colour,parity in product(range(3),range(2)):
        key = (colour,parity,args.column)
        Q_tuples += 1
        T = supports[3][colour] | supports[2][parity] | supports[5][args.column]
        for d3,d5 in product((3,6,12),(5,10,20)):
            free = tuple(d for d in ds if d not in (d3,8,d5))
            need(len(free)==24 and sum(raw[d] for d in free)==428, 'typed free original raw credit')
            need(Counter(d//gcd(d,4) for d in free)[3]==2
                 and Counter(d//gcd(d,4) for d in free)[5]==2, 'typed coarse/column multiplicities')
            original_inventory_checks += 1
            for d in free:
                e = d//gcd(d,4)
                histogram = [0]*e
                for t in F:
                    if T >> t & 1:
                        histogram[t%e] += 1
                literal = [(physical[(d,0,r)]&T).bit_count() for r in range(e)]
                need(literal==histogram, 'typed entire physical phase vector')
                capacity_values += e
                record(facts_digest, (key,d3,d5,d,literal))
        if colour == 0:
            zero_Q += 1
            need(T.bit_count()==112 and max((s&T).bit_count() for s in supports[3])==40,
                 'zero-colour Q exclusion data')
            record(facts_digest, (key,'zero-colour',112,40,2*(60-40)))
            continue
        positive_Q += 1
        full = supports[3][colour]
        column = supports[5][args.column]
        need(T.bit_count()==120 and (full&T)==full and (column&T)==column, 'positive Q footprint')
        need((supports[3][3-colour]&T).bit_count()==36 and (supports[3][0]&T).bit_count()==24,
             'other colour capacities')
        need([m.bit_count() for m in supports[5]]==[32]*5, 'raw original column credits')
        need(sorted((m&T).bit_count() for m in supports[5])==[22,22,22,22,32], 'Q column phase capacities')
        for r,m in enumerate(supports[4]):
            need((m&T).bit_count()==(40 if r%2==parity else 20), 'projected4 Q phase capacity')
            need((m&full).bit_count()==15 and (m&column).bit_count()==8,
                 'projected4 full-colour/whole-column intersection')
        for r,m in enumerate(supports[9]):
            need((m&T).bit_count()==(20 if r%3==colour else (0 if r==3 else 12)), 'fine-row Q phase capacity')
        base = (full,full,0,0)
        options4 = [(-1,-1,0)]+[(s,r,m&T) for s in range(4) for r,m in enumerate(supports[4])]
        options5 = [(-1,-1,0)]+[(s,r,m&T) for s in range(4) for r,m in enumerate(supports[5])]
        options9 = [(-1,-1,0)]+[(s,r,m&T) for s in range(4) for r,m in enumerate(supports[9])]
        options15 = [(-1,-1,0)]+[(s,r,m&T) for s in range(4) for r,m in enumerate(supports[15])]
        need(tuple(map(len,(options4,options5,options9,options15)))==(17,21,37,61), 'complete local option domains')
        for owner4,phase4,support4 in options4:
            after4,cost4 = add(base,owner4,support4,40)
            # The complete local column pair is small enough to inspect literally.
            for first5,second5 in product(options5,repeat=2):
                column_tuples += 1
                after5,extra5 = add(after4,first5[0],first5[2],32)
                covered,cost_second = add(after5,second5[0],second5[2],32)
                cost = cost4+extra5+cost_second
                record(column_digest,(key,owner4,phase4,first5[:2],second5[:2],cost))
                if cost > 20:
                    closed_column_tuples += 1
                    continue
                column_prefixes += 1
                fine_nominal_tuples += 37**3
                initial_count = fine_survivors
                initial_closed = closed_fine_tuples

                def visit_fine(depth,state,spent,choices):
                    nonlocal fine_visits,closed_fine_tuples,fine_survivors,slot_visits,slot_survivors
                    fine_visits += 1
                    record(fine_digest,(key,owner4,phase4,first5[:2],second5[:2],choices,spent))
                    if spent > 20:
                        closed_fine_tuples += 37**(3-depth)
                        return
                    if depth != 3:
                        for s,r,m in options9:
                            updated,extra = add(state,s,m,20)
                            visit_fine(depth+1,updated,spent+extra,choices+((s,r),))
                        return
                    fine_survivors += 1
                    need(spent==20 and owner4 in (2,3) and phase4%2==parity,
                         'budget20 equality escaped correct-parity third owner')
                    ownerD = 5-owner4
                    need(all(s==ownerD and r%3==colour for s,r in choices)
                         and len({r for s,r in choices})==3, 'equality escaped three distinct full-colour fine rows')
                    need(first5[1]==args.column and second5[1]==args.column
                         and first5[0]!=second5[0]
                         and owner4 in (first5[0],second5[0]), 'equality escaped repeated whole Q column')
                    other = second5[0] if first5[0]==owner4 else first5[0]
                    equality_owner_types['D' if other==ownerD else ('A' if other==0 else 'B')] += 1
                    expected_slots = {(s,(3-colour)+3*((args.column-(3-colour))*2%5))
                                      for s in range(4) if s not in (first5[0],second5[0])}
                    actual_slots = {(s,r) for s,r,m in options15 if s>=0 and (m&~state[s]).bit_count()==12}
                    need(actual_slots==expected_slots and len(actual_slots)==2,
                         'projected15 zero-cost slot identity differs')
                    before_slots = slot_survivors

                    def visit_slots(depth,slot_state,slot_cost,slot_choices):
                        nonlocal slot_visits,slot_survivors
                        slot_visits += 1
                        record(slot_digest,(key,owner4,phase4,first5[:2],second5[:2],choices,slot_choices,slot_cost))
                        if slot_cost > 20:
                            return
                        if depth==3:
                            slot_survivors += 1
                            return
                        for s,r,m in options15:
                            updated,extra = add(slot_state,s,m,12)
                            visit_slots(depth+1,updated,slot_cost+extra,slot_choices+((s,r),))

                    visit_slots(0,state,spent,())
                    need(slot_survivors==before_slots, 'three projected15 originals fit the zero budget')

                visit_fine(0,covered,cost,())
                need(fine_survivors-initial_count+closed_fine_tuples-initial_closed==37**3,
                     'incomplete local fine triple accounting')
    need((Q_tuples,positive_Q,zero_Q)==(6,4,2), 'complete fixed-column Q phase partition')
    need(column_tuples==4*17*21**2 and fine_survivors==576 and slot_survivors==0,
         'complete fixed-column equality/profile census')
    need(dict(equality_owner_types)=={'A':192,'B':192,'D':192}, 'all equality owner types')
    result={'agent':'six-covering-1','role':'researcher','column_partition':args.column,
            'status':'COLUMN_Q_UPPER106_LITERAL_LOCAL_FACTS_VERIFIED',
            'original_phase_owner_maps':maps,'nonempty_original_maps':active,'empty_original_maps':empty,
            'gate_compatible_original_maps':len(physical),'Q_phase_tuples':Q_tuples,
            'positive_Q_footprints':positive_Q,'zero_colour_Q_footprints':zero_Q,
            'original_inventory_checks':original_inventory_checks,'original_Q_types':9,
            'typed_original_phase_capacity_values':capacity_values,
            'local_projected4_column_pair_tuples':column_tuples,'closed_column_pair_tuples':closed_column_tuples,
            'fine_prefix_profiles':column_prefixes,'fine_nominal_triples':fine_nominal_tuples,
            'closed_fine_triples':closed_fine_tuples,'fine_prefix_visits':fine_visits,
            'fine_equality_survivors':fine_survivors,'equality_column_other_owner_counts':dict(sorted(equality_owner_types.items())),
            'projected15_prefix_visits':slot_visits,'projected15_full_survivors':slot_survivors,
            'physical_capacity_rows_sha256':facts_digest.hexdigest(),'column_rows_sha256':column_digest.hexdigest(),
            'fine_prefix_rows_sha256':fine_digest.hexdigest(),'projected15_prefix_rows_sha256':slot_digest.hexdigest(),
            'raw_original_credit':600,'free_original_credit':428,'supplemental_row_credit':20,
            'budget_at_common107':20,'ordinary_common_support_upper':106,
            'all_K_subsets_enumerated':False,'all_allocations_enumerated':False,
            'ordinary_unformalized_proof_required':True,'entire_unmarked_Q_inventory_required':True,
            'independent_external_review':False,'global_L_min_8_bounds_changed':False,'full_cover_found':False,
            'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
