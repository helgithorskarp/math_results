"""Definition-level scalar seed enumeration and generic comparator controls.

No producer/profile imports, cache or external data. Each of2048 original
assignments is replayed numerically, with distinct HIGH marks2/3. Complete
records, conditional patterns, all15 weight-two choices, and the illustrative
empty-preparation32-gate word are compared entry by entry.
"""
from itertools import combinations
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def step(row, a, b):
    result = list(row)
    if result[a] > result[b]:
        result[a], result[b] = result[b], result[a]
    return result


def main():
    f = json.loads((ROOT/'fixture.json').read_text())
    proposal_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT/'work/proposal.json'
    p = json.loads(proposal_path.read_text())
    need(digest(p['finite']) == p['finite_sha256'], 'Changed finite transport binding')
    n = f['ports']
    need(n == 13 and f['original_HIGH_inputs'] == [1, 2] and
         f['dead_preparation_ports'] == [2, 3, 4, 5, 7, 8] and
         f['candidate_head_ports'] == [5, 7, 8] and f['head_root'] == 9 and
         f['barrier_port'] == 11 and f['canonical_tail'] == [[6, 10], [9, 11], [10, 11]] and
         f['imported_S11_lower_bound'] == 35 and f['total_comparator_ceiling'] == 44,
         'Wrong literal theorem fixture or imported bound')
    word = f['B23']+f['LOW_suffix']+f['prior_HIGH_merges']
    need(len(word) == 28 and all(0 <= a < b < n for a, b in word), 'Wrong actual standard seed')
    free = [p for p in range(n) if p not in (1, 2)]
    rows, marked_masks, active_masks = [], [], []
    for x in range(2048):
        row = [0]*n
        row[1], row[2] = 2, 3
        for j, port in enumerate(free):
            row[port] = x >> j & 1
        touches = active = 0
        for t, (a, b) in enumerate(word):
            hit = row[a] > 1 or row[b] > 1
            touches |= int(hit) << t
            active |= int(not hit and row[a] > row[b]) << t
            row = step(row, a, b)
        need([q for q, value in enumerate(row) if value > 1] == [10, 12] and
             row[10] == 2 and row[12] == 3, 'Actual original HIGH ranks/tags differ at seed')
        rows.append(row)
        marked_masks.append(touches)
        active_masks.append(active)
    need(len(set(marked_masks)) == 1, 'Free-dependent marked deletion route')
    touches = marked_masks[0]
    active = 0
    for mask in active_masks:
        active |= mask
    identities = ((1 << 28)-1) & ~(touches | active)
    D, R = touches.bit_count(), identities.bit_count()
    dead = f['dead_preparation_ports']
    conditional = [x for x, row in enumerate(rows) if row[11] == 0]
    patterns = sorted({sum(rows[x][port] << j for j, port in enumerate(dead)) for x in conditional})
    need(patterns == [0, 8, 16, 24], 'Actual complete conditional dead-domain differs')
    greatest = 0
    for value in patterns:
        greatest |= value
    need(greatest in patterns and all(value & ~greatest == 0 for value in patterns) and
         greatest.bit_count() == 2, 'Conditional domain has no attained weight-two greatest input')
    need(all(row[9] <= row[11] <= 1 for row in rows), 'Actual unmarked root/barrier order differs')
    choices = []
    for ones in combinations(range(6), 2):
        value = sum(1 << i for i in ones)
        zeros = [port for port in [5, 7, 8] if not value >> dead.index(port) & 1]
        need(zeros, 'Weight-two output does not leave a zero among the three candidate heads')
        choices.append([value, zeros, zeros[0]])
    choices.sort()
    claimed = p['finite']
    need(claimed['actual_seed_original_D'] == D and claimed['actual_seed_original_R'] == R,
         'Claimed original seed deletion/identity counts differ from full scalar replay')
    need(claimed['full_original_conditional_assignments'] == conditional,
         'Claimed conditional assignments omit or substitute an actual original input')
    need(claimed['conditional_coordinatewise_greatest_pattern'] == greatest and
         claimed['greatest_pattern_weight'] == 2,
         'Claimed greatest conditional input differs from the actual attained weight-two maximum')
    for value, zeros, selected in claimed['complete_weight2_output_zero_choices']:
        need(value.bit_count() == 2 and selected in f['candidate_head_ports'] and
             selected in zeros and not value >> dead.index(selected) & 1,
             'Claimed selected head is not a zero coordinate of the weight-two output')
    expected = {
        'literal_seed_sha256': digest(word), 'actual_original_HIGH_mask': 6,
        'actual_free_input_ports': free, 'actual_seed_marked_ports': [10, 12],
        'actual_seed_original_D': D, 'actual_seed_original_R': R,
        'actual_seed_touch_mask': touches, 'actual_seed_identity_mask': identities,
        'full2048_original_seed_rows_sha256': digest(rows),
        'full_original_seed_root9_le_root11': all(row[9] <= row[11] for row in rows),
        'full_original_conditional_assignments': conditional,
        'complete_conditional_dead_patterns': patterns,
        'conditional_coordinatewise_greatest_pattern': greatest,
        'greatest_pattern_original_witness_assignment': next(x for x in conditional
            if sum(rows[x][port] << j for j, port in enumerate(dead)) == greatest),
        'greatest_pattern_weight': 2,
        'complete_weight2_output_zero_choices': choices,
        'future_literal_tail_marked_touches': 2,
        'forced_additional_whole_original_identities': 1,
        'certified_total_lower_bound': D+R+2+1+35,
        'arbitrary_preparation_word_lengths_allowed': True,
        'global_size44_exclusion_claimed': False,
    }
    need(expected == p['finite'] and D == 7 and R == 0 and expected['certified_total_lower_bound'] == 45,
         'Complete actual scalar seed/choice/cost record differs')
    # Basic local properties imply monotonicity and weight conservation for
    # words of ANY length. Finite checks corroborate the elementary argument.
    conservation = monotonicity = 0
    for a, b in combinations(range(6), 2):
        outputs = []
        for x in range(64):
            row = [(x >> i) & 1 for i in range(6)]
            result = step(row, a, b)
            need(sum(result) == x.bit_count(), 'Boolean comparator fails weight conservation')
            outputs.append(sum(value << i for i, value in enumerate(result)))
            conservation += 1
        for x in range(64):
            for y in range(64):
                if x & ~y:
                    continue
                need(not outputs[x] & ~outputs[y], 'Boolean comparator fails coordinatewise monotonicity')
                monotonicity += 1
    gate_control = []
    for z in (0, 1):
        for r in (0, 1):
            for s in (0, 1):
                if r > s or (s == 0 and z != 0):
                    continue
                after = max(z, r)
                need(after <= s, 'Conditional-zero head does not force the barrier identity')
                gate_control.append([z, r, s, after])
    # Actual F=empty supplies an illustrative32-gate instance, not a proof
    # by bounded sampling of all possible preparation words.
    sample = word+[[8, 9]]+f['canonical_tail']
    sample_touches, sample_active = [], 0
    sample_rows = []
    for x in range(2048):
        row = [0]*13
        row[1], row[2] = 2, 3
        for j, port in enumerate(free):
            row[port] = x >> j & 1
        hits = 0
        for t, (a, b) in enumerate(sample):
            marked = row[a] > 1 or row[b] > 1
            hits |= int(marked) << t
            sample_active |= int(not marked and row[a] > row[b]) << t
            row = step(row, a, b)
        sample_touches.append(hits)
        sample_rows.append(row)
    need(len(set(sample_touches)) == 1, 'Illustrative word has free-dependent mark route')
    redundant = ((1 << 32)-1) & ~(sample_touches[0] | sample_active)
    need(sample_touches[0].bit_count() == 9 and redundant >> 30 & 1 and
         not sample_touches[0] >> 30 & 1 and
         all([q for q, v in enumerate(row) if v > 1] == [11, 12] for row in sample_rows),
         'Actual illustrative word lacks the stated unmarked identity/deletion count')
    need((56).bit_count() == 3 and all(56 >> dead.index(port) & 1 for port in [5, 7, 8]),
         'Missing genuine weight-three boundary countercontrol')
    finite = {'producer_finite_sha256': p['finite_sha256'], 'whole_producer_finite_matched': True,
              'actual_original_seed_assignments': 2048, 'actual_original_seed_gates': 2048*28,
              'all15_weight2_zero_choices_checked': True,
              'local_comparator_conservation_controls': conservation,
              'local_comparator_coordinatewise_monotonicity_controls': monotonicity,
              'complete_conditional_zero_head_truth_table': gate_control,
              'illustrative_empty_preparation_word_sha256': digest(sample),
              'illustrative_original_assignments': 2048, 'illustrative_original_gates': 2048*32,
              'illustrative_original_marked_touches': 9,
              'illustrative_original_identity_mask': redundant,
              'illustrative_full_final_original_rows_sha256': digest(sample_rows),
              'weight3_no_zero_choice_countercontrol': [56, [5, 7, 8]],
              'arbitrary_F_bridge': 'Every comparator preserves weight and is monotone; every finite word does so by induction.',
              'external_person_review_claimed': False, 'formalized': False}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'UNIVERSAL_CONDITIONAL_MAXIMUM_SEED_AND_GENERIC_BRIDGE_CONTROLS_SCALAR_VERIFIED',
              'finite': finite, 'finite_sha256': digest(finite)}
    if len(sys.argv) <= 1:
        suffix = '-O' if not __debug__ else ''
        (ROOT/('work/checked'+suffix+'.json')).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
