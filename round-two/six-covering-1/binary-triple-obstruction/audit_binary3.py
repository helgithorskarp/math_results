"""Exact counting facts for the ordinary binary-triple obstruction.

Standard library only; no search engine, producer table or local state import.
This checks the finite arithmetic facts, not all allocations. The proof is in
PROOF.md. Author separation is not independent external review.
"""
from hashlib import sha256
from itertools import product
from math import gcd
from pathlib import Path
import json


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def main():
    F = [t for t in range(180) if t % 9 != 3]
    original = [d for d in range(2, 721) if 720 % d == 0 and d not in (2, 4)]
    Q = {3, 9, 24, 720}
    B3 = {8, 16, 48}
    remaining20 = sorted(set(original)-Q-B3)
    remaining19 = sorted(set(remaining20)-{144})
    alternate19 = sorted(set(remaining20)-{72})
    need((len(original), len(remaining20), len(remaining19), len(alternate19)) == (27, 20, 19, 19), 'original labels merged or lost')
    lifts = {s: {t: next(y for y in range(4*t+3, 5040, 720) if y % 7 == s+2) for t in F}
             for s in range(5)}
    ap = {}
    raw = active = inactive = 0
    for d, s in product(original, range(5)):
        e = d//gcd(d, 4)
        productive = {(4*r+3) % d: r for r in range(e)}
        for b in range(d):
            residue = b+d*(((s+2-b)*pow(d, -1, 7)) % 7)
            mask = sum(1 << t for t in F if lifts[s][t] % (7*d) == residue)
            raw += 1
            if b not in productive:
                need(mask == 0, 'inactive physical phase gained support')
                inactive += 1
            else:
                r = productive[b]
                need(mask == sum(1 << t for t in F if t % e == r), 'literal original phase transport')
                ap[d, s, r] = mask
                active += 1
    need((raw, active, inactive) == (12055, 3495, 8560), 'physical map census')
    targets = []
    large_Q = raw_Q = 0
    for a, u, r6, z in product(range(3), range(9), range(6), range(180)):
        coarse = ap[3, 1, a] | ap[9, 1, u] | ap[24, 1, r6]
        target = coarse | ap[720, 1, z]
        raw_Q += 1
        need(coarse.bit_count() == 110 or coarse.bit_count() <= 100, 'coarse Q gap')
        if target.bit_count() >= 109:
            need(coarse.bit_count() == 110, 'marked108 large-Q bridge')
            large_Q += 1
        if target.bit_count() == 111:
            need(a in (1, 2) and u in (0, 6) and r6 % 3 == 3-a, 'forced Q111 shape')
            targets.append((a, u, r6 % 2, z, target))
    targets.sort(key=lambda row: row[:4])
    need(raw_Q == 29160 and large_Q == 1440 and len(targets) == 400, 'complete Q classification')
    for dl, d9 in product((3, 6, 12), (9, 18, 36)):
        pool = set(original)-{dl, d9, 24, 720}-B3
        need(len(pool) == 20 and sorted(d//gcd(d, 4) for d in pool)
             == sorted(d//gcd(d, 4) for d in remaining20), 'nine original Q types')
    capacities = triples = forced_triples = bad_triples = G_intersections = 0
    same = opposite = 0
    largest_bad = 0
    trace = sha256()
    cases = []
    for a, u, p, z, T in targets:
        same_parity = z % 2 == p
        same += same_parity
        opposite += not same_parity
        values = {d: [(T & ap[d, 4, r]).bit_count() for r in range(d//gcd(d, 4))]
                  for d in remaining20}
        weights = {d: max(v) for d, v in values.items()}
        capacities += sum(map(len, values.values()))
        cap20 = sum(weights.values())
        need(cap20 == (326 if same_parity else 324), 'remaining20 total')
        need(sum(weights[d] for d in remaining19) == (321 if same_parity else 319), 'original binary4 pool')
        need(sum(weights[d] for d in alternate19)+20 == (336 if same_parity else 334), 'binary3 plus original72 pool')
        virtual = [sum(1 << t for t in F if (4*t+3) % 18 == q)
                   for q in (1, 3, 5, 7, 9, 11, 13, 17)]
        need(max((T & v).bit_count() for v in virtual) == 20, 'one full supplemental row')
        slack = cap20+20-333
        need(slack == (13 if same_parity else 11), 'extra-owner capacity budget')
        five_factor = sorted((weights[d], d) for d in remaining20 if (d//gcd(d, 4)) % 5 == 0)
        need(sum(w for w, d in five_factor[:5]) == 17 > slack, 'five distinct column-bearing originals')
        need({d for d in remaining20 if (d//gcd(d, 4)) % 5 != 0 and weights[d] <= slack} == {72, 144}, 'all affordable non-five resources')
        colour = sum(1 << t for t in F if t % 3 == a)
        need(colour.bit_count() == 60, 'full colour60')
        for r in range(3):
            n = (T & ap[6, 4, r]).bit_count()
            need(n == 60 if r == a else n <= 31, 'ternary forced-colour loss')
        for r in range(5):
            mask = T & ap[5, 4, r]
            need(mask.bit_count() == (23 if r == z % 5 else 22)
                 and (mask & colour).bit_count() == 12, 'column loss and colour overlap')
        for r in range(15):
            n = (T & ap[15, 4, r]).bit_count()
            need(n == 12 if r % 3 == a else n <= (6 if same_parity else 7), 'three finer-colour resources')
        if same_parity:
            maxima10 = [r for r, n in enumerate(values[40]) if n == 15]
            maxima20 = [r for r, n in enumerate(values[80]) if n == 8]
            need(maxima10 == [z % 10] and maxima20 == [z % 20], 'same-parity terminal maxima')
            C10, C20 = T & ap[40, 4, maxima10[0]], T & ap[80, 4, maxima20[0]]
            need((C10 & C20).bit_count() == 8 and (C10 & colour).bit_count() == 6
                 and (C20 & colour).bit_count() == 3, 'unavoidable terminal overlaps')
        for r2, r4, r12 in product(range(2), range(4), range(12)):
            base = T & (ap[8, 4, r2] | ap[16, 4, r4] | ap[48, 4, r12])
            forced = r2 == p and r4 % 2 != p and r12 % 4 == (r4+2) % 4 and r12 % 3 == a
            triples += 1
            if not forced:
                bad_triples += 1
                largest_bad = max(largest_bad, base.bit_count())
                need(base.bit_count() <= 97 < 111-slack, 'noncanonical binary3 phases could satisfy capacity demand')
                continue
            forced_triples += 1
            G = sum(1 << t for t in F if t % 9 == u and t % 4 == (r4+2) % 4)
            need(G.bit_count() == 5 and not (G & base) and G & T == G, 'uncovered complete five-point row')
            for w, d in five_factor:
                for r in range(d//gcd(d, 4)):
                    need((G & ap[d, 4, r]).bit_count() <= 1, 'five-bearing original hits two row points')
                    G_intersections += 1
        trace.update(json.dumps([a, u, p, z, [[d, values[d]] for d in remaining20]], separators=(',', ':')).encode())
        cases.append([a, u, p, z, cap20, slack, sum(w for w, d in five_factor[:5])])
    need((opposite, same) == (320, 80) and triples == 38400 and forced_triples == 800
         and bad_triples == 37600 and capacities == 193200, 'complete new finite counts')
    result = {'agent': 'six-covering-1', 'role': 'researcher',
              'status': 'BINARY3_ORDINARY_PROOF_LITERAL_FACTS_VERIFIED',
              'ordinary_upper_core3_unmarked': 110, 'ordinary_upper_core3_marked': 108,
              'ordinary_upper_binary4_unmarked': 110, 'ordinary_upper_binary4_marked': 107,
              'extra_originals_allowed_on_binary_owner': True, 'omissions_and_inactive_phases_allowed': True,
              'necessary_productive_core3_owners_at_common111': 2,
              'original_Q_types': 9, 'ordered_Q_binary_owner_placements': 16,
              'all_raw_Q_tuples': raw_Q, 'large_Q_tuples_at_least109': large_Q,
              'target_shapes': len(targets), 'opposite_targets': opposite, 'same_targets': same,
              'original_phase_owner_maps': raw, 'active_maps': active, 'inactive_maps': inactive,
              'remaining20_phase_capacity_values': capacities, 'binary3_phase_triples': triples,
              'forced_binary3_triples': forced_triples, 'bad_binary3_triples': bad_triples,
              'maximum_bad_binary3_support': largest_bad, 'five_point_row_original_phase_intersections': G_intersections,
              'least_five_five_bearing_resource_capacity': 17, 'extra_capacity_budgets': [11, 13],
              'capacity_rows_sha256': trace.hexdigest(),
              'case_summary_sha256': sha256(json.dumps(cases, separators=(',', ':')).encode()).hexdigest(),
              'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'exclusion_uses_ordinary_capacity_and_overlap_proof': True,
              'all_allocations_enumerated': False, 'independent_external_review': False,
              'global_L_min_8_bounds_changed': False, 'full_cover_found': False}
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
