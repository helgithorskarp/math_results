"""Packed exact original cube for the universal conditional-maximum cut.

Only compact fixture data are read. Generated data stay in work/. Marked
values are distinct ranks2/3; all eleven unmarked inputs are Boolean.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
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
    f = json.loads((ROOT/'fixture.json').read_text())
    n = f['ports']
    need(n == 13 and f['original_HIGH_inputs'] == [1, 2], 'Wrong original family')
    word = f['B23']+f['LOW_suffix']+f['prior_HIGH_merges']
    need(len(word) == 28 and all(0 <= a < b < n for a, b in word), 'Wrong standard seed word')
    free = [p for p in range(n) if p not in f['original_HIGH_inputs']]
    columns = [sum(1 << x for x in range(2048) if x >> j & 1) for j in range(11)]
    values = [None]*n
    for p, rank in zip(f['original_HIGH_inputs'], [2, 3]):
        values[p] = ('MARK', rank)
    for p, column in zip(free, columns):
        values[p] = column
    D = R = touches = identities = 0
    for t, (a, b) in enumerate(word):
        d, r = gate(values, a, b)
        D += d
        R += r
        touches |= d << t
        identities |= r << t
    rows = [[value[1] if isinstance(value, tuple) else value >> x & 1 for value in values]
            for x in range(2048)]
    dead = f['dead_preparation_ports']
    conditional = [x for x, row in enumerate(rows) if row[f['barrier_port']] == 0]
    patterns = sorted({sum(rows[x][p] << j for j, p in enumerate(dead)) for x in conditional})
    maxima = [x for x in patterns if not any(x != y and x & ~y == 0 for y in patterns)]
    need(maxima == [24] and maxima[0].bit_count() == 2, 'Greatest conditional pattern differs')
    choices = []
    for value in range(64):
        if value.bit_count() != 2:
            continue
        zeros = [p for p in f['candidate_head_ports'] if not value >> dead.index(p) & 1]
        need(zeros, 'Missing zero output among three candidates')
        choices.append([value, zeros, zeros[0]])
    finite = {
        'literal_seed_sha256': digest(word), 'actual_original_HIGH_mask': 6,
        'actual_free_input_ports': free, 'actual_seed_marked_ports': [p for p, v in enumerate(values) if isinstance(v, tuple)],
        'actual_seed_original_D': D, 'actual_seed_original_R': R,
        'actual_seed_touch_mask': touches, 'actual_seed_identity_mask': identities,
        'full2048_original_seed_rows_sha256': digest(rows),
        'full_original_seed_root9_le_root11': all(row[9] <= row[11] for row in rows),
        'full_original_conditional_assignments': conditional,
        'complete_conditional_dead_patterns': patterns,
        'conditional_coordinatewise_greatest_pattern': maxima[0],
        'greatest_pattern_original_witness_assignment': next(x for x in conditional
            if sum(rows[x][p] << j for j, p in enumerate(dead)) == maxima[0]),
        'greatest_pattern_weight': 2,
        'complete_weight2_output_zero_choices': choices,
        'future_literal_tail_marked_touches': 2,
        'forced_additional_whole_original_identities': 1,
        'certified_total_lower_bound': D+R+2+1+35,
        'arbitrary_preparation_word_lengths_allowed': True,
        'global_size44_exclusion_claimed': False,
    }
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'EXACT_SEED_AND_UNIVERSAL_ZERO_CHOICE_PROPOSAL_NEEDS_SCALAR_REPLAY',
              'finite': finite, 'finite_sha256': digest(finite)}
    (ROOT/'work').mkdir(exist_ok=True)
    (ROOT/'work/proposal.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
