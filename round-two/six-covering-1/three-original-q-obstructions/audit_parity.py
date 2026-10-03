"""Exact local arithmetic for an ordinary parity/singleton Q obstruction.

Python3.10+ stdlib; no previous code, native builder, solver or input corpus.
The ordinary proof, not full-allocation enumeration, supplies the exclusion.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from math import gcd
import json
from pathlib import Path


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def bitmap(points):
    return sum(1 << t for t in points)


def add_record(digest, row):
    digest.update(json.dumps(row, separators=(',', ':')).encode()+b'\n')


def main():
    F = tuple(t for t in range(180) if t % 9 != 3)
    originals = tuple(d for d in range(2, 721) if 720 % d == 0 and d not in (2, 4))
    need(len(F) == 160 and len(originals) == 27, 'original universe')
    moduli = sorted({d//gcd(d, 4) for d in originals})
    projected = {e: tuple(bitmap(t for t in F if t % e == r) for r in range(e)) for e in moduli}
    lifts = {s: {t: next(y for y in range(4*t+3, 5040, 720) if y % 7 == s+2) for t in F}
             for s in range(5)}
    physical, active, inactive, maps = {}, 0, 0, 0
    # Entire original residue pools, including every erased-copy or inactive
    # residue. Compare literal period5040 APs with projected supports.
    for d in originals:
        e = d//gcd(d, 4)
        phase_by_b = {(4*r+3) % d: r for r in range(e)}
        need(len(phase_by_b) == e, 'projected phase injection')
        for residue in range(7*d):
            maps += 1
            owner = residue % 7-2
            if owner not in lifts:
                observed, expected = 0, 0
            else:
                observed = bitmap(t for t in F if (lifts[owner][t]-residue) % (7*d) == 0)
                r = phase_by_b.get(residue % d)
                expected = 0 if r is None else projected[e][r]
                if r is not None:
                    key = (d, owner, r)
                    need(key not in physical, 'duplicate original active phase')
                    physical[key] = observed
            need(observed == expected, 'literal original physical phase differs')
            active += bool(observed)
            inactive += not bool(observed)
    need((maps, active, inactive) == (16877, 3225, 13652), 'complete original phase census')
    need(len(physical) == 3495, 'complete gate-compatible original phase census')
    raw_Q = high_Q = 0
    shapes = {}
    for r3, parity, z in product(range(3), range(2), range(180)):
        raw_Q += 1
        union = projected[3][r3] | projected[2][parity] | projected[180][z]
        need(union.bit_count() <= 111, 'Q exceeds111')
        if union.bit_count() == 111:
            high_Q += 1
            need(r3 in (1, 2) and z in F and z % 3 != r3 and z % 2 != parity,
                 'Q111 footprint shape differs')
            shape = tuple(t for t in F if union >> t & 1)
            key = (r3, parity, z)
            need(key not in shapes, 'duplicate Q111 shape')
            shapes[key] = shape
    need((raw_Q, high_Q, len(shapes)) == (1080, 200, 200), 'complete Q phase census')
    credits = {3:60, 4:40, 5:23, 6:30, 9:20, 10:16, 12:15,
               15:12, 18:10, 20:8, 30:6, 36:5, 45:4, 60:3, 90:2}
    expected_counts = {3:2, 4:1, 5:3, 6:1, 9:3, 10:1, 12:1,
                       15:3, 18:1, 20:1, 30:1, 36:1, 45:3, 60:1, 90:1}
    capacity_digest, column_digest, fine_digest = sha256(), sha256(), sha256()
    capacity_values = force_values = full_column_tuples = closed_column_tuples = 0
    feasible_column_tuples = fine_first_options = fine_second_options = 0
    prefix_profiles = 0
    column_costs, fine_final_costs = Counter(), Counter()

    def extend(covered, owner, support, credit):
        if owner < 0:
            return covered, credit
        gain = (support & ~covered[owner]).bit_count()
        result = list(covered)
        result[owner] |= support
        return tuple(result), credit-gain

    for key, target in sorted(shapes.items()):
        colour, parity, z = key
        T = bitmap(target)
        full = projected[3][colour] & T
        for d3 in (3, 6, 12):
            free = [d for d in originals if d not in (d3, 8, 720)]
            count = Counter(d//gcd(d, 4) for d in free)
            need(dict(count) == expected_counts and len(free) == 24, 'typed original resource inventory')
            total = 0
            for d in free:
                e = d//gcd(d, 4)
                histogram = [0]*e
                for t in target:
                    histogram[t % e] += 1
                literal = [(physical[(d, 0, r)] & T).bit_count() for r in range(e)]
                need(literal == histogram and max(literal) == credits[e], 'entire typed original phase capacity differs')
                capacity_values += e
                total += max(literal)
                add_record(capacity_digest, (key, d3, d, literal))
            need(total == 432 and total+20-4*len(target) == 8, 'resource budget8 differs')
        for r in range(3):
            n = (projected[3][r] & T).bit_count()
            need(n == 60 if r == colour else n <= 31, 'forced full-colour phase')
            force_values += 1
        need(full.bit_count() == 60, 'full-colour population')
        for r4 in range(4):
            m4 = projected[4][r4] & T
            if r4 % 2 != parity:
                need(m4.bit_count() <= 16, 'wrong-parity projected4 population')
            else:
                need(m4.bit_count() == 40 and (m4 & full).bit_count() == 15,
                     'forced projected4 owner population')
            force_values += 1
        columns = [projected[5][r] & T for r in range(5)]
        need(sorted(m.bit_count() for m in columns) == [22,22,22,22,23], 'five-column populations')
        options = [(-1, -1, 0)]+[(s, r, columns[r]) for s in range(4) for r in range(5)]
        need(len(options) == 21, 'column phase/owner/omission options')
        for r4 in (parity, parity+2):
            initial = (full, full, projected[4][r4] & T, 0)
            leaves, closed = [], [0]

            def visit(depth, covered, cost, choices):
                if cost > 8:
                    closed[0] += 21**(3-depth)
                    return
                if depth == 3:
                    need(all(owner == 3 for owner, phase in choices)
                         and len({phase for owner, phase in choices}) == 3,
                         'a feasible column triple escapes forced fourth owner')
                    need(cost in (2,3), 'three distinct column cost')
                    leaves.append((choices, cost))
                    add_record(column_digest, (key, r4, choices, cost))
                    return
                for owner, phase, support in options:
                    updated, extra = extend(covered, owner, support, 23)
                    visit(depth+1, updated, cost+extra, choices+((owner, phase),))

            visit(0, initial, 0, ())
            need(len(leaves) == 60 and closed[0]+len(leaves) == 21**3,
                 'complete local three-column option coverage')
            full_column_tuples += 21**3
            closed_column_tuples += closed[0]
            feasible_column_tuples += len(leaves)
            for choices, cost in leaves:
                column_costs[cost] += 1
            rows = [projected[9][r] & T for r in range(9)]
            fine_options = [(-1, -1, 0)]+[(s, r, rows[r]) for s in range(4) for r in range(9)]
            need(len(fine_options) == 37, 'fine-row phase/owner/omission options')
            # Three-column orders give the same whole state. Every unordered
            # three-column subset is separately checked; no covering symmetry.
            for used in combinations(range(5), 3):
                prefix_profiles += 1
                covered = list(initial)
                covered[3] = columns[used[0]] | columns[used[1]] | columns[used[2]]
                cost = 69-covered[3].bit_count()
                need(cost in (2,3), 'column-set cost')
                first_survivors = 0
                for owner, phase, support in fine_options:
                    fine_first_options += 1
                    after, loss = extend(tuple(covered), owner, support, 20)
                    first_cost = cost+loss
                    add_record(fine_digest, (key,r4,used,1,owner,phase,first_cost))
                    if first_cost > 8:
                        continue
                    first_survivors += 1
                    need(owner == 2 and phase % 3 == colour and loss == 5,
                         'first fine row escapes forced modulo4 owner')
                    for second_owner, second_phase, second_support in fine_options:
                        fine_second_options += 1
                        unused, extra = extend(after, second_owner, second_support, 20)
                        final_cost = first_cost+extra
                        need(final_cost > 8 and extra >= 5, 'second fine row escapes budget obstruction')
                        fine_final_costs[final_cost] += 1
                        add_record(fine_digest, (key,r4,used,2,owner,phase,second_owner,second_phase,final_cost))
                need(first_survivors == 3, 'complete first fine-row survivors')
    result = {'agent':'six-covering-1','role':'researcher','status':'PARITY_SINGLETON_Q_UPPER110_LITERAL_FACTS_VERIFIED',
              'original_phase_owner_maps':maps,'active_maps':active,'inactive_maps':inactive,
              'gate_compatible_original_phase_owner_maps':len(physical),
              'raw_Q_tuples_per_type':raw_Q,'Q111_tuples_per_type':high_Q,
              'original_Q_types':3,'unmarked_Q_placements':4,'target_shapes':len(shapes),
              'free_original_phase_capacity_values':capacity_values,'forced_coarse_phase_values':force_values,
              'local_column_owner_phase_omission_tuples':full_column_tuples,
              'closed_local_column_tuples':closed_column_tuples,'feasible_local_column_tuples':feasible_column_tuples,
              'column_prefix_profiles':prefix_profiles,'fine_first_options':fine_first_options,
              'fine_second_options':fine_second_options,'column_cost_histogram':dict(sorted(column_costs.items())),
              'fine_final_cost_histogram':dict(sorted(fine_final_costs.items())),
              'capacity_rows_sha256':capacity_digest.hexdigest(),'column_rows_sha256':column_digest.hexdigest(),
              'fine_rows_sha256':fine_digest.hexdigest(),'free_original_credit':432,'supplemental_row_credit':20,
              'loss_overlap_budget':8,'ordinary_common_support_upper':110,
              'entire_Q_inventory_required':True,'all_allocations_enumerated':False,
              'ordinary_unformalized_proof_required':True,'omissions_and_inactive_phases_allowed':True,
              'independent_external_review':False,'global_L_min_8_bounds_changed':False,'full_cover_found':False,
              'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
