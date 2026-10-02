"""Independent literal2520-point AP audit; imports no producer module.

Masks use physical bit positions, and every phase is independently generated
as a literal arithmetic progression. Marginal maxima traverse phases backward;
the producer groups required points by residues into compressed masks. Full
record hashes agree only after every original phase and every branch is checked.
All four stages and the affine audit are necessary for the exclusion theorem.
"""
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import json
import struct


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(c):
    p = [[8, 0], [9, 0], [10, 1], [14, 1], [12, 10]]
    labels = [d for d in range(8, 2521) if 2520 % d == 0
              and d not in (8, 9, 10, 12, 14)]
    require(c['schema'] == 1 and c['period'] == 2520 and c['prefix'] == p
            and c['parent'] == 4 and c['required'] == 1118,
            'Wrong literal required set/prefix')
    require(c['original_base_labels'] == labels and len(labels) == 36
            and sum(labels) == 9279 and 21 in labels and 16 not in labels,
            'Missing/relabelled original resource')
    require(c['fixed_order'] == [15, 18, 24, 36, 20]
            and c['canonical15'] == [0, 1, 2, 4, 6, 11]
            and c['canonical18'] == [0, 1, 2, 3, 4, 5, 6, 9, 12, 15]
            and c['normalization_group'] == 288
            and c['retained_frontier_limit'] == 300,
            'Wrong simultaneous orbit cover or operational domain')
    require(len(c['stages']) == 4, 'Missing stage')
    for j, s in enumerate(c['stages']):
        fixed = c['fixed_order'][:j + 2]
        keep = s['retained_phase_vectors']
        require(s['stage'] == j + 1 and s['fixed_originals'] == fixed
                and s['remaining_originals'] == [n for n in labels if n not in fixed],
                'Wrong actual remaining original inventory')
        require(type(s['retained_vectors']) is int and 0 <= s['retained_vectors'] <= 300
                and len(keep) == s['retained_vectors'], 'Wrong retained-frontier count/cap')
        tuples = [tuple(row) for row in keep]
        require(tuples == sorted(set(tuples)) and all(len(row) == len(fixed)
                and all(type(a) is int and 0 <= a < n for n, a in zip(fixed, row))
                for row in tuples), 'Malformed/duplicate original tuple')
        require(len(s['maximum_row']) == 38 and s['maximum_row'][-1] == s['total_upper_range'][1],
                'Malformed maximum witness')
        prior = 60 if j == 0 else c['stages'][j - 1]['retained_vectors']
        children = prior if j == 0 else prior * fixed[-1]
        require(s['parent_vectors'] == prior and s['records'] == children,
                'Skipped parent or skipped original phase')
    return p, labels


def run(stage, c):
    p, labels = validate(c)
    require(type(stage) is int and stage in (1, 2, 3, 4), 'Invalid requested stage')
    expected = c['stages'][stage - 1]
    fixed = [15, 18, 24, 36, 20][:stage + 1]
    remaining = [n for n in labels if n not in fixed]
    if stage == 1:
        parent = list(product([0, 1, 2, 4, 6, 11], [0, 1, 2, 3, 4, 5, 6, 9, 12, 15]))
    else:
        parent = [tuple(row) for row in c['stages'][stage - 2]['retained_phase_vectors']]
    # Prefix union by literal arithmetic progressions, independent of a
    # pointwise modular test or producer's compressed point indexing.
    unavailable = {x for n, a in p for x in range(a, 2520, n)}
    other_parents = set(range(2520)) - set(range(4, 2520, 8))
    required = sorted(other_parents - unavailable)
    require(len(required) == 1118, 'Literal AP required set differs')
    R = sum(1 << x for x in required)
    actions = {}
    raw_phase_actions = 0
    for n in reversed(labels):
        literal = []
        for a in range(n):
            literal.append(sum(1 << x for x in range(a, 2520, n)
                               if x not in unavailable and x % 8 != 4))
            raw_phase_actions += 1
        require(all(m & ~R == 0 for m in literal), 'Action outside literal required set')
        actions[n] = literal
    require(raw_phase_actions == 9279, 'Incomplete AP phase catalogue')
    digest = sha256()
    kept = []
    count = 0
    min_upper, max_upper = 65536, -1
    min_gain, max_gain = 65536, -1
    min_out, max_out = 65536, -1
    min_in, max_in = 65536, -1
    maxrow = None
    for prior in parent:
        extension = (None,) if stage == 1 else range(fixed[-1])
        for a in extension:
            tuple_phases = prior if a is None else (*prior, a)
            covered = 0
            for j in range(len(fixed) - 1, -1, -1):
                covered |= actions[fixed[j]][tuple_phases[j]]
            residual = R ^ covered
            gain = len(required) - residual.bit_count()
            caps = []
            for n in remaining:
                best = 0
                for phase in range(n - 1, -1, -1):
                    hit = (actions[n][phase] & residual).bit_count()
                    if hit > best:
                        best = hit
                caps.append(best)
            upper = gain + sum(caps)
            row = [*tuple_phases, gain, *caps, upper]
            require(len(row) == 38, 'Wrong complete canonical record')
            digest.update(struct.pack('<38H', *row))
            count += 1
            min_upper, max_upper = min(min_upper, upper), max(max_upper, upper)
            min_gain, max_gain = min(min_gain, gain), max(max_gain, gain)
            if maxrow is None or upper > maxrow[-1]:
                maxrow = row
            if upper < 1118:
                min_out, max_out = min(min_out, upper), max(max_out, upper)
            else:
                require(len(kept) < 300, 'Frontier cap: audit incomplete, no exclusion')
                kept.append(list(tuple_phases))
                min_in, max_in = min(min_in, upper), max(max_in, upper)
    actual = dict(stage=stage, fixed_originals=fixed, remaining_originals=remaining,
                  parent_vectors=len(parent), parent_vectors_sha256=sha256(json.dumps(
                      parent, separators=(',', ':')).encode()).hexdigest(), records=count,
                  required_points_sha256=sha256(struct.pack('<1118H', *required)).hexdigest(),
                  union_gain_range=[min_gain, max_gain], total_upper_range=[min_upper, max_upper],
                  excluded_upper_range=None if max_out < 0 else [min_out, max_out],
                  retained_upper_range=None if max_in < 0 else [min_in, max_in],
                  all_rows38H_sha256=digest.hexdigest(), maximum_row=maxrow,
                  retained_vectors=len(kept), retained_phase_vectors=kept)
    require(actual == expected, 'Complete independent AP stage record differs')
    return {k: v for k, v in actual.items() if k != 'retained_phase_vectors'} | {
        'independent_literal_AP_audit': True, 'all_raw_original_phase_actions': raw_phase_actions,
        'native_solver': False, 'external_review_claimed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=int, choices=(1, 2, 3, 4), required=True)
    parser.add_argument('--certificate', type=Path, default=Path(__file__).with_name('certificate.json'))
    args = parser.parse_args()
    print(json.dumps(run(args.stage, json.loads(args.certificate.read_text())), sort_keys=True))
