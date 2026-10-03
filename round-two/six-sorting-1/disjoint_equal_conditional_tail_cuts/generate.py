"""Exact packed original-domain witnesses for six disjoint HIGH routes.

Adapted from the credited owned conditional-maximum producer9916. No old
negative corpus, preparation catalogue, scalar checker or graph is read.
"""
from itertools import combinations
import hashlib
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def gate(values, a, b):
    left, right = values[a], values[b]
    if isinstance(left, tuple) or isinstance(right, tuple):
        order = lambda x: x[1] if isinstance(x, tuple) else 0
        if order(left) > order(right):
            values[a], values[b] = right, left
        return 1, 0
    identity = int(not left & ~right)
    values[a], values[b] = left & right, left | right
    return 0, identity


def main():
    start = time.monotonic()
    f = json.loads((ROOT/'fixture.json').read_text())
    need(f['ports'] == 13 and len(f['routes']) == 6 and f['barrier_port'] == 11
         and f['held_top_port'] == 12, 'Wrong ground fixture')
    columns = [sum(1 << x for x in range(2048) if x >> j & 1) for j in range(11)]
    records = []
    for route in f['routes']:
        need(time.monotonic()-start < 45, 'Operational guard: incomplete producer')
        branch = route['prior_HIGH_merges']
        high = route['original_HIGH_inputs']
        need(len(branch) == 2 and len(set(sum(branch, []))) == 4, 'Not two disjoint binary gates')
        roots = sorted(max(pair) for pair in branch)
        slack = next(p for p in f['ordinary_HIGH_unit_ports'] if p not in sum(branch, []))
        dead = sorted(set(range(2, 12)) - set(roots+[slack, 11]))
        word = f['B23'] + f['LOW_suffix'] + branch
        need(len(word) == 28 and all(0 <= a < b < 13 for a, b in word), 'Invalid literal seed')
        free = [p for p in range(13) if p not in high]
        values = [None] * 13
        for p, rank in zip(high, (2, 3)):
            values[p] = ('HIGH', rank)
        for p, col in zip(free, columns):
            values[p] = col
        touches = identities = 0
        for t, (a, b) in enumerate(word):
            D, R = gate(values, a, b)
            touches |= D << t
            identities |= R << t
        marks = [[p, v[1]] for p, v in enumerate(values) if isinstance(v, tuple)]
        need(marks[-1] == [12, 3] and marks[0][0] in roots and marks[0][1] == 2,
             'Actual original HIGH ranks differ')
        need(touches.bit_count() == 7 and identities == 0, 'Witness seed is not tight')
        rows = [[v[1] if isinstance(v, tuple) else v >> x & 1 for v in values]
                for x in range(2048)]
        need(all(row[slack] <= row[11] <= 1 for row in rows), 'Missing original root/barrier relation')
        conditional = [x for x, row in enumerate(rows) if row[11] == 0]
        patterns = sorted({sum(rows[x][p] << j for j, p in enumerate(dead)) for x in conditional})
        join = 0
        for pattern in patterns:
            join |= pattern
        need(join in patterns and join.bit_count() == 2 and join & 7 == 0,
             'Conditional maximum is not an attained weight-two input with three leading zeros')
        need(dead[:3] == [2, 3, 4], 'Fixed zero-head labels changed')
        envelope = []
        for ones in combinations(range(3, 6), 2):
            v = sum(1 << j for j in ones)
            zeros = [p for j, p in enumerate(dead) if not v >> j & 1]
            adaptive = next(p for p in dead[3:] if p in zeros)
            bindings = []
            for p in zeros:
                r = max(p, slack)
                head = sorted([p, slack])
                tail = [roots, [r, 11], [roots[-1], 11]]
                need(all(a < b for a, b in [head]+tail), 'Head/tail orientation changed')
                bindings.append({'head_port': p, 'actual_head': head, 'actual_head_root': r,
                                 'literal_balanced_tail': tail, 'identity_tail_index': 1,
                                 'additional_marked_tail_touches': 2})
            envelope.append({'output_mask': v, 'zero_head_ports': zeros,
                             'adaptive_extra_head': adaptive, 'bindings': bindings})
        envelope.sort(key=lambda x: x['output_mask'])
        records.append({'prior_HIGH_merges': branch, 'literal_seed_sha256': digest(word),
                        'live_pair_roots': roots, 'slack_root': slack, 'dead_preparation_ports': dead,
                        'original_HIGH_inputs': high, 'original_HIGH_mask': sum(1 << p for p in high),
                        'original_free_input_ports': free, 'actual_seed_marked_ports_and_ranks': marks,
                        'actual_original_seed_D': 7, 'actual_original_seed_R': 0,
                        'actual_original_seed_touch_mask': touches, 'actual_original_seed_identity_mask': identities,
                        'full2048_original_seed_rows_sha256': digest(rows),
                        'full_original_slack_le_barrier': True,
                        'complete_original_conditional_assignments': conditional,
                        'complete_conditional_dead_patterns': patterns,
                        'attained_conditional_maximum_mask': join,
                        'maximum_original_witness_assignment': next(x for x in conditional
                            if sum(rows[x][p] << j for j, p in enumerate(dead)) == join),
                        'maximum_weight': 2, 'fixed_head_ports': [2, 3, 4],
                        'conservative_output_envelope': envelope,
                        'minimum_excluded_head_count': 4,
                        'certified_total_lower_bound': 7+2+1+35})
    finite = {'literal_B23_LOW_sha256': digest(f['B23']+f['LOW_suffix']),
              'route_records': records, 'total_routes': 6,
              'fixed_head_tail_exclusions_per_preparation': 18,
              'minimum_head_tail_exclusions_per_preparation_across_routes': 24,
              'output_envelope_claimed_exactly_reachable': False,
              'arbitrary_preparation_length_allowed': True, 'suffix_depth_restricted': False,
              'other_balanced_tails_excluded': False, 'entire_six_routes_excluded': False,
              'global_size44_exclusion_claimed': False}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'PACKED_SIX_ROUTE_ORIGINAL_MAXIMUM_PROPOSAL_NEEDS_SEPARATE_SCALAR_REPLAY',
              'finite': finite, 'finite_sha256': digest(finite), 'seconds': time.monotonic()-start}
    (ROOT/'work').mkdir(exist_ok=True)
    (ROOT/'work/proposal.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'finite_sha256': result['finite_sha256'], 'total_routes': 6,
                      'seconds': result['seconds']}), flush=True)


if __name__ == '__main__':
    main()
