"""Literal facts for an ordinary ENTIRE four-original Q obstruction.

Python3.10+ standard library. No solver, builder, old census, or external data.
The loss-budget proof is in proof.md; this is not full allocation enumeration.
"""
from hashlib import sha256
from itertools import combinations, product
from math import gcd
from pathlib import Path
import json


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def run():
    F = tuple(t for t in range(180) if t % 9 != 3)
    original = tuple(d for d in range(3, 721) if 720 % d == 0 and d != 4)
    need(len(F) == 160 and len(original) == 27, 'literal inventory')
    lifts = {s: {t: next(y for y in range(4*t+3, 5040, 720) if y % 7 == s+2) for t in F}
             for s in range(5)}
    ap, raw, active, inactive = {}, 0, 0, 0
    for d in original:
        e = d//gcd(d, 4)
        gate = {(4*r+3) % d: r for r in range(e)}
        for s in range(5):
            for b in range(d):
                residue = b+d*(((s+2-b)*pow(d, -1, 7)) % 7)
                mask = sum(1 << t for t in F if lifts[s][t] % (7*d) == residue)
                raw += 1
                if b not in gate:
                    need(mask == 0, 'inactive original residue acquired support')
                    inactive += 1
                else:
                    r = gate[b]
                    need(mask == sum(1 << t for t in F if t % e == r), 'literal/projected original AP mismatch')
                    ap[d, s, r] = mask
                    active += 1
    need((raw, active, inactive) == (12055, 3495, 8560), 'all original physical maps')
    coarse_shapes = {}
    raw_Q = large_Q = 0
    for r3, r9, r6 in product(range(3), range(9), range(6)):
        coarse = ap[3, 1, r3] | ap[9, 1, r9] | ap[24, 1, r6]
        n = coarse.bit_count()
        need(n <= 110, 'coarse Q upper110')
        if n == 110:
            a, u, p = r3, r9, r6 % 2
            need(a in (1, 2) and u in (0, 6) and r6 % 3 == 3-a, 'large Q normal form')
            coarse_shapes[a, u, p] = coarse
        for z in range(180):
            Q = coarse | ap[720, 1, z]
            raw_Q += 1
            need(Q.bit_count() <= 111, 'entire Q upper111')
            if Q.bit_count() == 111:
                large_Q += 1
                need(n == 110 and z in F and not (coarse >> z) & 1, 'entire Q111 form')
    need(raw_Q == 29160 and large_Q == 400 and len(coarse_shapes) == 8, 'complete large Q census')
    targets = [(a, u, p, z, coarse | (1 << z))
               for (a, u, p), coarse in sorted(coarse_shapes.items())
               for z in F if not (coarse >> z) & 1]
    need(len(targets) == 400, 'all target footprints')
    for d3, d9 in product((3, 6, 12), (9, 18, 36)):
        for r in range(3):
            need(ap[d3, 1, r] == ap[3, 1, r], 'original d3 alias map')
        for r in range(9):
            need(ap[d9, 1, r] == ap[9, 1, r], 'original d9 alias map')

    counts = {'target_shapes': len(targets), 'opposite_shapes': 0, 'same_shapes': 0,
              'original_Q_types': 9, 'free_original_phase_capacities': 0,
              'one_two_column_e4_options': 0, 'three_column_e4_options': 0,
              'budget_feasible_main_profiles': 0, 'locally_closed_main_profiles': 0,
              'e15_marginal_options': 0, 'e10_after_good_slots_options': 0}
    branch_counts = {key: 0 for key in ('p_AB_opposite', 'p_AB_same', 'wrong_C_opposite',
                                       'wrong_C_same', 'p_D_same')}
    caps_hash, facts_hash = sha256(), sha256()

    def record(h, row):
        h.update((json.dumps(row, separators=(',', ':'))+'\n').encode())

    for a, u, p, z, T in targets:
        opposite = z % 2 != p
        counts['opposite_shapes' if opposite else 'same_shapes'] += 1
        budget = 20 if opposite else 24
        capacities = {}
        for d in original:
            capacities[d] = max((ap[d, 0, r] & T).bit_count() for r in range(d//gcd(d, 4)))
        for d3, d9 in product((3, 6, 12), (9, 18, 36)):
            free = [d for d in original if d not in (d3, d9, 24, 720)]
            total = sum(capacities[d] for d in free)+20
            need(total == 444+budget, 'complete free ORIGINAL resource credit')
            need(sum(d//gcd(d, 4) for d in free) == 501, 'free phase count retains aliases')
            for d in free:
                for r in range(d//gcd(d, 4)):
                    record(caps_hash, [a, u, p, z, d3, d9, d, r, (ap[d, 0, r] & T).bit_count()])
                    counts['free_original_phase_capacities'] += 1
        colour = ap[3, 0, a] & T
        parity = ap[8, 0, p] & T
        need(colour.bit_count() == 60 and parity.bit_count() == (70 if opposite else 71), 'forced core capacities')
        need(max((ap[3, 0, r] & T).bit_count() for r in range(3) if r != a) < 60-budget,
             'nonmaximal e3 phase cannot fit budget')
        need(capacities[8]-(ap[8, 0, 1-p] & T).bit_count() > budget,
             'wrong parity-e2 phase cannot fit budget')
        need((colour & parity).bit_count() == 30 and 30 > budget, 'e2/e3 owners must differ')
        columns = [ap[5, 0, r] & T for r in range(5)]
        need(sorted(m.bit_count() for m in columns) == [22, 22, 22, 22, 23], 'five columns')
        for col in columns:
            need(23-(col & ~colour).bit_count() >= 12, 'e5 on colour owner costs12')
            need(23-(col & ~parity).bit_count() >= 14, 'e5 on parity owner costs14')
        for j in (1, 2):
            for selected in combinations(range(5), j):
                D = 0
                for col in selected:
                    D |= columns[col]
                base = [colour, colour, parity, D]
                for s, r in product(range(4), range(4)):
                    gain = (ap[16, 0, r] & T & ~base[s]).bit_count()
                    need(capacities[16]-gain >= 7*j, 'e4 after one/two D columns')
                    counts['one_two_column_e4_options'] += 1
        for selected in combinations(range(5), 3):
            D = columns[selected[0]] | columns[selected[1]] | columns[selected[2]]
            base = [colour, colour, parity, D]
            base_cost = 69-D.bit_count()
            need(base_cost in (2, 3), 'three distinct e5 columns cost2/3')
            for s, r in product(range(4), range(4)):
                counts['three_column_e4_options'] += 1
                copies = base.copy(); copies[s] |= ap[16, 0, r] & T
                main_cost = base_cost+capacities[16]-(ap[16, 0, r] & T & ~base[s]).bit_count()
                record(facts_hash, [a, u, p, z, list(selected), s, r, main_cost])
                if main_cost > budget:
                    counts['locally_closed_main_profiles'] += 1
                    continue
                counts['budget_feasible_main_profiles'] += 1
                same_p = r % 2 == p
                if same_p and s in (0, 1):
                    branch = 'p_AB'; floor = 17
                elif not same_p and s == 2:
                    branch = 'wrong_C'; floor = 16 if opposite else 18
                elif same_p and s == 3:
                    branch = 'p_D'; floor = 23
                else:
                    raise RuntimeError('unhandled e4 budget-feasible placement')
                need(main_cost >= floor, 'main branch loss floor')
                key = branch+('_opposite' if opposite else '_same')
                need(key in branch_counts, 'opposite p_D should already be closed')
                branch_counts[key] += 1
                options = {(v, h): (ap[15, 0, h] & T & ~copies[v]).bit_count()
                           for v, h in product(range(4), range(15))}
                counts['e15_marginal_options'] += len(options)
                if branch == 'p_D':
                    need(min(12-gain for gain in options.values()) >= 3
                         and main_cost+3 > budget, 'p_D closes with first e15')
                    continue
                good = [pick for pick, gain in options.items() if gain == 12]
                need(len(good) == 2 and {v for v, h in good} == {3}, 'exact two full-colour D slots')
                b = 7 if opposite else 6
                need(max(gain for pick, gain in options.items() if pick not in good) <= b,
                     'all other e15 marginal gains')
                good_masks = [ap[15, 0, h] & T for v, h in good]
                need(not (good_masks[0] & good_masks[1]) and all(m.bit_count() == 12 for m in good_masks),
                     'good slots are distinct disjoint full-colour columns')
                e15_cost = 12-b
                if opposite:
                    need(main_cost+e15_cost > budget, 'opposite closes with three e15')
                    continue
                need(b == 6 and budget-main_cost <= 7 and 12+2*b < 36-(budget-main_cost),
                     'small same-parity budget forces both distinct good slots')
                copies[3] |= good_masks[0] | good_masks[1]
                e10_floor = min(capacities[40]-(ap[40, 0, h] & T & ~copies[v]).bit_count()
                                for v, h in product(range(4), range(10)))
                counts['e10_after_good_slots_options'] += 40
                need(e10_floor >= 6 and main_cost+e15_cost+e10_floor > budget,
                     'same-parity closes with e10 after forced good slots')
    need(counts['opposite_shapes'] == 320 and counts['same_shapes'] == 80, 'parity target split')
    need(counts['free_original_phase_capacities'] == 1803600
         and counts['one_two_column_e4_options'] == 96000
         and counts['three_column_e4_options'] == 64000, 'complete literal fact domains')
    need(counts['budget_feasible_main_profiles']+counts['locally_closed_main_profiles'] == 64000,
         'complete e4 branch partition')
    return {'agent': 'six-covering-1', 'role': 'researcher',
            'status': 'ENTIRE_Q_ORDINARY_UPPER110_LITERAL_FACTS_VERIFIED',
            'original_phase_owner_maps': raw, 'active_maps': active, 'inactive_maps': inactive,
            'raw_Q_tuples': raw_Q, 'Q111_tuples': large_Q, **counts, 'branch_counts': branch_counts,
            'capacity_rows_sha256': caps_hash.hexdigest(), 'main_profiles_sha256': facts_hash.hexdigest(),
            'ordinary_common_support_upper': 110, 'one_supplemental_row_credit': 20,
            'free_incidence_credits': [464, 468], 'loss_overlap_budgets': [20, 24],
            'entire_original_Q_inventory_required': True, 'binary_owner_condition_required': False,
            'omissions_and_inactive_phases_allowed': True, 'all_allocations_enumerated': False,
            'ordinary_unformalized_proof_required': True, 'independent_external_review': False,
            'global_L_min_8_bounds_changed': False, 'full_cover_found': False,
            'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True))
