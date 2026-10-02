"""Exact complete count-envelope checker, standard-library Python only."""
from argparse import ArgumentParser
from copy import deepcopy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORE = (10, 12, 15, 16, 18, 20)
PAIRS = ((24, 30), (36, 40), (45, 48), (60, 72), (80, 90),
         (120, 144), (180, 240), (360, 720))
GROUPS = (CORE,) + PAIRS
LABELS = tuple(m for m in range(8, 721) if 720 % m == 0 and m not in (8, 9))


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def bitset(values):
    return sum(1 << x for x in values)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def validate_shape(c):
    need(set(c) == {'schema', 'period', 'fixed', 'hole_targets', 'compulsory_size',
                    'even_target_size', 'groups', 'gain_tables', 'envelope', 'conclusion'}, 'certificate fields')
    need(c['schema'] == 1 and c['period'] == 720 and c['fixed'] == [[8, 5], [9, 6]] and
         c['hole_targets'] == [[18, 3], [4, 0]], 'certificate domain')
    need(c['compulsory_size'] == 370 and c['even_target_size'] == 160, 'certificate demands')
    need(c['groups'] == [list(g) for g in GROUPS] and
         sorted(m for g in c['groups'] for m in g) == list(LABELS), 'ORIGINAL disjoint partition')
    need(len(c['gain_tables']) == len(GROUPS) and
         c['conclusion'] == {'maximum_even_incidence_sum': 61, 'minimum_actual_even_holes': 99},
         'certificate scope/conclusion')
    for group, table in zip(GROUPS, c['gain_tables']):
        need(set(table) == {'moduli', 'raw_phase_tuples', 'distinct_phase_mask_tuples', 'gain_pairs'},
             'gain table fields')
        need(table['moduli'] == list(group) and
             all(type(x) is int and 0 <= x <= bound for p in table['gain_pairs']
                 for x, bound in zip(p, (370, 160))) and
             all(len(p) == 2 for p in table['gain_pairs']) and
             table['gain_pairs'] == [list(p) for p in sorted({tuple(p) for p in table['gain_pairs']})],
             'gain pair syntax/order')


def compute_tables():
    R = bitset(x for x in range(720) if x % 8 != 5 and x % 9 != 6 and x % 18 != 3)
    S = bitset(x for x in range(720) if x % 4 == 0 and x % 9 != 6)
    F = R & ~S
    need(R.bit_count() == 530 and S.bit_count() == 160 and F.bit_count() == 370,
         'literal fixed-class/target split')
    masks = {m: sorted({bitset(range(a, 720, m)) & R for a in range(m)}) for m in LABELS}
    tables = []
    for group in GROUPS:
        gains = set()
        visits = 0

        def visit(i, covered):
            nonlocal visits
            if i == len(group):
                visits += 1
                gains.add(((covered & F).bit_count(), (covered & S).bit_count()))
            else:
                for mask in masks[group[i]]:
                    visit(i + 1, covered | mask)

        visit(0, 0)
        raw, distinct = 1, 1
        for m in group:
            raw *= m
            distinct *= len(masks[m])
        need(visits == distinct, 'incomplete ORIGINAL phase-mask product')
        tables.append({'moduli': list(group), 'raw_phase_tuples': raw,
                       'distinct_phase_mask_tuples': distinct, 'gain_pairs': sorted(gains)})
    return json.loads(json.dumps(tables))


def compute_envelope(tables):
    # Exact DP on ALL gain pairs; at a fixed compulsory sum retain only
    # the largest even sum. That choice can only improve later even sums.
    dp, counts = {0: 0}, []
    for table in tables:
        new = {}
        for f, s in dp.items():
            for f1, s1 in table['gain_pairs']:
                new[f + f1] = max(new.get(f + f1, -1), s + s1)
        dp = new
        counts.append(len(dp))
    eligible = [(f, s) for f, s in sorted(dp.items()) if f >= 370]
    need(eligible, 'no compulsory-cover count profile')
    return {'state_counts': counts, 'final_best_even_by_compulsory_sum': [[f, s] for f, s in sorted(dp.items())],
            'maximum_even_sum_with_compulsory_at_least370': max(s for f, s in eligible)}


def check_certificate(c, tables, envelope):
    validate_shape(c)
    need(c['gain_tables'] == tables, 'complete ORIGINAL phase-gain table differs')
    need(c['envelope'] == envelope, 'full exact envelope differs')
    maximum = envelope['maximum_even_sum_with_compulsory_at_least370']
    need(maximum == 61 and 160 - maximum == 99, 'necessary actual-hole bound differs')


def damage_controls(c, tables, envelope):
    mutations = []
    q = deepcopy(c); q['fixed'][0][1] = 4; mutations.append(('fixed8phase', q))
    q = deepcopy(c); q['hole_targets'][0][1] = 0; mutations.append(('odd_target', q))
    q = deepcopy(c); q['groups'][0][0] = 12; mutations.append(('original_resource', q))
    q = deepcopy(c); q['compulsory_size'] = 369; mutations.append(('compulsory_demand', q))
    q = deepcopy(c); q['gain_tables'][0]['raw_phase_tuples'] -= 1; mutations.append(('incomplete_product', q))
    q = deepcopy(c); q['gain_tables'][0]['gain_pairs'].pop(); mutations.append(('omitted_gain_pair', q))
    q = deepcopy(c); q['gain_tables'][0]['gain_pairs'].append([370, 160]); mutations.append(('invented_gain_pair', q))
    q = deepcopy(c); q['envelope']['final_best_even_by_compulsory_sum'][-1][1] += 1; mutations.append(('changed_envelope_entry', q))
    q = deepcopy(c); q['conclusion']['minimum_actual_even_holes'] = 100; mutations.append(('stronger_claim', q))
    rejected = []
    for name, candidate in mutations:
        try:
            check_certificate(candidate, tables, envelope)
        except RuntimeError:
            rejected.append(name)
        else:
            raise RuntimeError('semantic damage escaped: ' + name)
    return rejected


def main():
    ap = ArgumentParser()
    ap.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    ap.add_argument('--output', type=Path)
    a = ap.parse_args()
    c = json.loads(a.certificate.read_text())
    validate_shape(c)
    tables = compute_tables()
    envelope = compute_envelope(tables)
    check_certificate(c, tables, envelope)
    result = {'original_moduli': list(LABELS), 'compulsory_points': 370, 'even_target_points': 160,
              'raw_phase_tuples_by_group': [t['raw_phase_tuples'] for t in tables],
              'distinct_phase_mask_tuples_by_group': [t['distinct_phase_mask_tuples'] for t in tables],
              'gain_pair_counts_by_group': [len(t['gain_pairs']) for t in tables],
              'complete_tables_sha256': hashlib.sha256(canonical(tables)).hexdigest(),
              'full_envelope_sha256': hashlib.sha256(canonical(envelope)).hexdigest(),
              'maximum_even_incidence_sum': 61, 'minimum_actual_even_holes': 99,
              'semantic_damages_rejected': damage_controls(c, tables, envelope),
              'first_stage_witness_asserted': False, 'unrestricted_15120_exclusion_asserted': False}
    need(result == json.loads((HERE / 'expected.json').read_text()), 'frozen counters differ')
    if a.output:
        a.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
