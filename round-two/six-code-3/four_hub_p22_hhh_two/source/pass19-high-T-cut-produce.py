"""Exact certificates for all eight necessary T3/T4 populations.

No whole P22 census, HH quota or HHH ownership mask is assumed. Support
partitions start with D and N; all typed assignments are then derived.
Ordinary mathematical bridges are explicit in the accompanying proof.
"""
import hashlib
import itertools
import json
from pathlib import Path
import time

S = Path('round-two/six-code-3/scratch')
CANON = lambda value: json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def need(condition, message):
    if not condition:
        raise ValueError(message)


def support_ok(B, C, J, N, minimum_C=5):
    return all((not b or n >= 2) and (not c or n >= minimum_C) and (not j or n >= 4)
               for b, c, j, n in zip(B, C, J, N))


def main():
    started = time.monotonic()
    data = json.loads((S / 'pass19-high-T-producer.json').read_text())
    inv = data['inventory']
    need(len(inv['branches']) == 30 and sum(len(b['templates']) for b in inv['branches']) == 283,
         'fresh complete thirty-branch census required')
    types = inv['types']
    meanings = {
        1: (0, 1, 1, 0, True, [4, 0, 0, 0, 0]),
        2: (0, 1, 1, 1, False, [4, 0, 0, 0, 0]),
        6: (0, 2, 2, 2, False, [3, 0, 0, 0, 0]),
        16: (1, 0, 0, 0, False, [3, 1, 0, 0, 0]),
        17: (1, 1, 1, 0, True, [2, 1, 0, 0, 0]),
        18: (1, 1, 2, 0, True, [3, 0, 0, 0, 0]),
        19: (1, 1, 1, 1, False, [2, 1, 0, 0, 0]),
        20: (1, 1, 2, 1, False, [3, 0, 0, 0, 0]),
    }
    for tid, expected in meanings.items():
        need(tuple(types[tid][k] for k in ('e', 'k', 'hub_weight', 'q', 'eligible', 'ss_hist')) == expected,
             'literal row semantics changed')
    survivors = [dict(branch=[b[k] for k in ('Q', 'T', 'X', 'tau')], population=t['population'])
                 for b in inv['branches'] for t in b['templates'] if not t['failures']]
    expected_populations = {
        (3, ((16, 2), (18, 11), (20, 1))),
        (3, ((17, 3), (18, 10), (19, 1))),
        (3, ((17, 4), (18, 9), (20, 1))),
        (3, ((1, 3), (2, 1), (18, 6), (20, 4))),
        (3, ((2, 4), (18, 9), (20, 1))),
        (3, ((2, 4), (6, 1), (18, 9))),
        (4, ((16, 2), (18, 12))),
        (4, ((17, 4), (18, 10))),
    }
    need({(r['branch'][1], tuple(tuple(p) for p in r['population'])) for r in survivors} == expected_populations
         and len(survivors) == 8, 'all eight ordered necessary populations must be covered')
    targets = [(h,) + lights for h in range(5, 14) for lights in itertools.product(range(1, 10), repeat=3)
               if h + sum(lights) == 24]
    need(len(targets) == 489, 'all necessary labelled D targets')
    records = []
    steps = 0
    for rec in survivors:
        pop = rec['population']
        units = [(types[t], c) for t, c in pop if types[t]['e'] == 0]
        unit_count = sum(c for row, c in units)
        unit_demand = sum(c * row['g1_S'] for row, c in units)
        ineligible_units = sum(c for row, c in units if not row['eligible'])
        internal_upper = min(unit_demand, ineligible_units * (ineligible_units - 1))
        external_upper = sum(c * min(unit_count, row['g1_S']) for t, c in pop
                             if (row := types[t])['e'] > 0 and not row['eligible'])
        if unit_demand > internal_upper + external_upper:
            records.append(dict(**rec, kind='UNIT_CAPACITY', unit_count=unit_count,
                                unit_demand=unit_demand, internal_incidence_upper=internal_upper,
                                external_incidence_upper=external_upper))
            continue
        if units and external_upper == 0 and unit_demand % 2:
            records.append(dict(**rec, kind='CLOSED_UNIT_PARITY', unit_count=unit_count,
                                closed_unit_degree_sum=unit_demand, external_incidence_upper=0))
            continue
        if all(types[t]['h'] == 4 and types[t]['k'] == 1 for t, c in pop):
            roots = [t for t, c in pop if types[t]['hub_weight'] == 1 and types[t]['q'] == 1]
            if roots:
                # Each such root has one deficit-one HIGH hub, leave degree4,
                # and one HIGH-SAT leave neighbor. Thus at most3 LOW-SAT hub friends.
                L_upper = 3
                ball_lower = 14 - L_upper
                ball_upper = 1 + 3 * 3
                need(ball_lower > ball_upper, 'strict generalized radius contradiction')
                records.append(dict(**rec, kind='GENERALIZED_RADIUS', root_type=roots[0],
                                    graph_regular_degree=3, hub_friend_upper=L_upper,
                                    two_step_ball_lower=ball_lower, two_step_ball_upper=ball_upper))
                continue
        counts = dict(pop)
        need(set(counts) <= {16, 17, 18, 20}, 'uncovered population has no exact support bridge')
        A, Btotal, Ctotal, Jtotal = (counts.get(t, 0) for t in (16, 17, 18, 20))
        need(A + Btotal + Ctotal + Jtotal == 14 and Btotal + 2*Ctotal + 2*Jtotal == 24,
             'support type cardinality and weight')
        need(Jtotal in (0, 1), 'single special center scope')
        Jchoices = [(0, 0, 0, 0)] if not Jtotal else [tuple(int(a == j) for a in range(4)) for j in range(4)]
        rows = []
        weak = []
        for D in targets:
            before = 0
            passing = []
            ranges = [range((d + 1)//2, d + 1) for d in D[:3]]
            for first in itertools.product(*ranges):
                N = first + (14 - A - sum(first),)
                steps += 1
                need(steps <= 500000 and time.monotonic() - started < 20,
                     'INCOMPLETE unchanged500000/20s support guard')
                B = tuple(2*n - d for n, d in zip(N, D))
                V = tuple(d - n for n, d in zip(N, D))
                if min(B + V) < 0 or sum(B) != Btotal or sum(V) != Ctotal + Jtotal:
                    continue
                for J in Jchoices:
                    C = tuple(v - j for v, j in zip(V, J))
                    if min(C) < 0:
                        continue
                    before += 1
                    witness = dict(B4=list(B), C4=list(C), J4=list(J), N4=list(N), D4=list(D))
                    if support_ok(B, C, J, N):
                        passing.append(witness)
                    if support_ok(B, C, J, N, minimum_C=4):
                        weak.append(witness)
            need(not passing, 'specified support population remains feasible')
            rows.append(dict(D4=list(D), pre_support_typed_allocations=before, passing_support=passing))
        weak.sort(key=lambda r: (r['D4'], r['N4'], r['J4']))
        records.append(dict(**rec, kind='DISJOINT_SUPPORT', neutral_rows=A, B_rows=Btotal,
                            C_rows=Ctotal, J_rows=Jtotal, degree_targets=len(targets), target_rows=rows,
                            pre_support_typed_allocations=sum(r['pre_support_typed_allocations'] for r in rows),
                            passing_support_allocations=0, weakened_C_threshold=4,
                            weakened_threshold_witnesses=weak))
    need(len(records) == len(survivors), 'every surviving vector has a certificate')
    mixed = next(r for r in records if r['kind'] == 'DISJOINT_SUPPORT' and r['J_rows'] == 1 and r['B_rows'] == 4)
    need(len(mixed['weakened_threshold_witnesses']) == 60, 'nonempty strict support-threshold sensitivity control')
    need(1 + 3*3 >= 14 - 4, 'weakened hub-friend radius boundary must pass')
    result = dict(agent='six-code-3', role='researcher', status='AUTHOR_COMPLETE_T3_T4_EXCLUSION_CERTIFICATES',
                  scalar_branches=30, raw_vectors=283, necessary_populations=survivors, records=records,
                  labelled_D_targets=len(targets), support_partition_steps=steps,
                  controls=dict(mixed_support_weakened_C4=60, weakened_radius_L4_boundary=1),
                  ordinary_bridges_formalized=False, external_review=False, unrestricted_code_bound=None,
                  support_guard_states=500000, support_guard_seconds=20)
    out = S / 'pass19-high-T-cut-producer.json'
    need(not out.exists(), 'fresh certificate output required')
    out.write_bytes(CANON(result) + b'\n')
    print(json.dumps(dict(status=result['status'], populations=len(records), support_steps=steps,
                         records_sha256=hashlib.sha256(CANON(records)).hexdigest(),
                         cuts=[dict(branch=r['branch'], population=r['population'], kind=r['kind'],
                                    pre_support=r.get('pre_support_typed_allocations')) for r in records],
                         elapsed_seconds=time.monotonic() - started)), flush=True)


if __name__ == '__main__':
    main()
