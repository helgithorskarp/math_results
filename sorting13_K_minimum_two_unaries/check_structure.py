"""Independent scalar/port, language, activity and boundary audits.

Author: six-sorting-2, researcher. No native SAT package is imported.
The7436 scalar middle-port algorithm and complete43-word classifier are
reused with explicit dependency credit. Counts are exact integers.
"""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / 'sorting13_double_pure_obstruction'
sys.path.insert(0, str(HERE.parent / 'sorting13_pure_maximum_exclusions'))
PAIRS = tuple(itertools.combinations(range(10), 2))
from activity import encode
from boundary_ranks import encode as rank_encode

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def generic_language(words):
    # A node is its separately tracked zero routes and its allowed future
    # kernel words. Nongates loop; an actual passage must advance a word.
    initial = ((0, 1, 5), tuple(sorted(words)))
    states = [initial]
    labels = {initial: 0}
    transitions = {}
    for label, (positions, futures) in enumerate(states):
        for pair in PAIRS:
            if not any(p in pair for p in positions):
                destination = label
            else:
                remaining = tuple(sorted({word[1:] for word in futures if word and word[0] == pair}))
                if not remaining:
                    destination = None
                else:
                    routes = tuple(pair[0] if p == pair[1] else p for p in positions)
                    child = routes, remaining
                    if child not in labels:
                        labels[child] = len(states)
                        states.append(child)
                    destination = labels[child]
            transitions[label, pair] = destination
    assert len(states) == 7 and states[6] == ((0, 0, 0), ((),))
    return states, transitions


def minimum_word(word):
    routes = [0, 1, 5]
    events = []
    for a, b in word:
        if any(p in (a, b) for p in routes):
            events.append((a, b))
            routes = [a if p == b else p for p in routes]
    return tuple(events), tuple(routes)


def dfa_audit(fixture, scalar):
    assert scalar.check_minimum_cover(fixture['minimum_kernel_words']) == 175
    words = tuple(sorted(tuple(map(tuple, w)) for w in fixture['minimum_kernel_words'] if len(w) == 3))
    assert len(words) == 6
    states, transitions = generic_language(words)
    search = module('new_private_search', HERE / 'minimum.py')
    assert tuple(positions for positions, future in states) == search.POSITIONS
    for (label, pair), destination in transitions.items():
        assert search.destination(label, pair) == destination
    controls = []
    for word in words:
        control = []
        state = 0
        for event in word:
            nongates = [p for p in PAIRS if transitions[state, p] == state]
            assert nongates
            control += nongates[:2] + [event]
            state = transitions[state, event]
        control += [(2, 3)] * (18 - len(control))
        assert len(control) == 18 and minimum_word(control) == (word, (0, 0, 0))
        controls.append(control)
    for control in controls:
        label = 0
        for pair in control:
            label = transitions[label, pair]
            assert label is not None
        assert label == 6
        changed = [(0, 1)] + control[1:]
        label = 0
        for pair in changed:
            label = transitions[label, pair]
            if label is None:
                break
        assert label is None
    # In particular stationary passages count as events:5,6 moves none
    # of the three routes but must consume the one unary passage.
    assert transitions[0, (5, 6)] == 4 and states[0][0] == states[4][0]
    assert transitions[4, (5, 6)] is None
    encoded = dict(states=[dict(routes=list(p), futures=[list(w) for w in future]) for p, future in states],
                   transitions=[[s, list(p), d] for (s, p), d in sorted(transitions.items())],
                   kernel_words=[list(word) for word in words])
    (HERE / 'scratch' / 'dfa-audit.json').write_text(json.dumps(encoded, indent=2) + '\n')
    return dict(independently_classified_cover_states=175, covered_unary_words=6,
                generic_quotient_states=7, audited_pair_transitions=len(transitions),
                interleaved_positive_words=len(controls), negative_early_root_words=len(controls),
                stationary_unary_event_audited=True,
                dfa_sha256=hashlib.sha256((HERE / 'scratch' / 'dfa-audit.json').read_bytes()).hexdigest())


class Clauses:
    def __init__(self):
        self.variables = 0
        self.rows = []

    def var(self):
        self.variables += 1
        return self.variables

    def add(self, *literals):
        assert all(type(x) is int and x != 0 for x in literals)
        self.rows.append(literals)


def comparator(mask, pair):
    a, b = pair
    values = [(mask >> i) & 1 for i in range(10)]
    values[a], values[b] = min(values[a], values[b]), max(values[a], values[b])
    return sum(value << i for i, value in enumerate(values))


def activity_table():
    w = Clauses()
    pairs = tuple(itertools.combinations(range(10), 2))
    choices = [[w.var() for _ in pairs]]
    inputs = [w.var() for _ in range(10)]
    flags = encode(w, choices, pairs, {0: [inputs]}, [0], 1, require_every=False)
    flag = flags[0][0]
    simplified = []
    for selector in choices[0]:
        rows = []
        for row in w.rows:
            if any(abs(v) <= 45 and ((v > 0) == (abs(v) == selector)) for v in row):
                continue
            rows.append(tuple(v for v in row if abs(v) > 45))
        simplified.append(rows)
    cases = active = rejected_flips = 0
    for mask in range(1024):
        truth = [False] * (w.variables + 1)
        for i, v in enumerate(inputs):
            truth[v] = bool(mask >> i & 1)
        for j, pair in enumerate(pairs):
            expected = comparator(mask, pair) != mask
            active += expected
            truth[flag] = expected
            clauses = simplified[j]
            assert all(any(truth[abs(v)] == (v > 0) for v in row) for row in clauses)
            truth[flag] = not expected
            assert not all(any(truth[abs(v)] == (v > 0) for v in row) for row in clauses)
            cases += 1
            rejected_flips += 1
    assert cases == 46080 and active == 11520 and rejected_flips == cases
    return dict(all_boolean_row_comparator_cases=cases, swapping_cases=active,
                wrong_activity_flag_controls=rejected_flips)


def commute_table():
    # Disjoint gates commute independently on all1024 Boolean rows.
    # Packed columns make the complete truth table compact and exact.
    columns = tuple(sum(((mask >> i) & 1) << mask for mask in range(1024))
                    for i in range(10))
    def apply(values, pair):
        result = list(values)
        a, b = pair
        result[a], result[b] = values[a] & values[b], values[a] | values[b]
        return tuple(result)
    cases = 0
    pairs = tuple(itertools.combinations(range(10), 2))
    for p, q in itertools.combinations(pairs, 2):
        if set(p).isdisjoint(q):
            assert apply(apply(columns, p), q) == apply(apply(columns, q), p)
            cases += 1
    assert cases == 630
    f = json.loads((HERE / 'scratch' / 'dfa-audit.json').read_text())
    transition = {(s, tuple(pair)): d for s, pair, d in f['transitions']}
    # The language is unchanged when adjacent disjoint gates are swapped.
    # Verify every pair transition in every one of the seven DFA states.
    route_cases = 0
    for s in range(7):
        for p, q in itertools.combinations(pairs, 2):
            if not set(p).isdisjoint(q):
                continue
            left = transition[s, p]
            left = None if left is None else transition[left, q]
            right = transition[s, q]
            right = None if right is None else transition[right, p]
            assert left == right, (s, p, q, left, right)
            route_cases += 1
    return dict(disjoint_pair_cases=cases, scalar_boolean_truth_cases=cases * 1024,
                complete_DFA_commutation_cases=route_cases)


def rank_table():
    cases = count_cases = conditional_controls = 0
    for weight in range(11):
        w = Clauses()
        cuts = [[w.var() for _ in range(9)]]
        row = [w.var() for _ in range(10)]
        rank_encode(w, cuts, {(1 << weight) - 1: [row]}, 10, 0)
        by_boundary = {k: [] for k in range(9)}
        for clause in w.rows:
            assert len(clause) == 2 and clause[0] < 0
            k = cuts[0].index(-clause[0])
            assert abs(clause[1]) in row
            by_boundary[k].append(clause)
        for mask in range(1024):
            if mask.bit_count() != weight:
                continue
            truth = [False] * (w.variables + 1)
            for i, variable in enumerate(row):
                truth[variable] = bool(mask >> i & 1)
            target = ((1 << weight) - 1) << (10 - weight)
            for k in range(9):
                prefix = (1 << (k + 1)) - 1
                expected = (mask & prefix).bit_count() == (target & prefix).bit_count()
                truth[cuts[0][k]] = True
                actual = all(any(truth[abs(v)] == (v > 0) for v in clause)
                             for clause in by_boundary[k])
                assert actual == expected
                truth[cuts[0][k]] = False
                assert all(any(truth[abs(v)] == (v > 0) for v in clause)
                           for clause in by_boundary[k])
                cases += 1
                count_cases += expected
                conditional_controls += 1
    assert cases == conditional_controls == 9216 and count_cases == 2035
    return dict(row_boundary_cases=cases, equal_final_count_cases=count_cases,
                inactive_cut_controls=conditional_controls)


def connectedness(f):
    witnesses = {}
    for subset in range(1, 1023):
        for row in f['K_states']:
            target = ((1 << row.bit_count()) - 1) << (10 - row.bit_count())
            if (row & subset).bit_count() != (target & subset).bit_count():
                witnesses[str(subset)] = [row, target]
                break
        else:
            raise AssertionError(('Proper weight-conserving component', subset))
    sha = hashlib.sha256(json.dumps(witnesses, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()
    assert sha == 'c085193973b0770b958b3c7a9cc6799c41baf95d21a2f1549e909c2cab9eb854'
    return dict(proper_nonempty_subsets_rejected=len(witnesses), table_sha256=sha)


def target_and_controls(f, scalar, records):
    image = set()
    for state in range(2048):
        values = [(state >> i) & 1 for i in range(11)]
        after = scalar.run_prefix(values, f, f['after'])
        assert after[10] == max(values)
        image.add(scalar.mask(after[:10]))
    assert image == set(f['K_states']) and len(image) == 127
    control = json.loads((HERE / 'positive_word.json').read_text())
    assert len(control) == 21 and minimum_word(control)[0] in {
        tuple(map(tuple, word)) for word in f['minimum_kernel_words'] if len(word) == 3}
    for state in range(2048):
        values = [(state >> i) & 1 for i in range(11)]
        values = scalar.run_prefix(values, f, f['after'])
        assert scalar.scalar(values, control) == sorted(values)
    crossings = [0] * (len(control) + 1)
    partitions = [None] * (len(control) + 1)
    parents = list(range(10))
    def root(i):
        while parents[i] != i:
            i = parents[i]
        return i
    for t in range(len(control), -1, -1):
        if t < len(control):
            a, b = control[t]
            parents[root(a)] = root(b)
            crossings[t] = crossings[t + 1] | sum(1 << k for k in range(a, b))
        groups = {}
        for i in range(10):
            groups.setdefault(root(i), []).append(i)
        assert all(group == list(range(min(group), max(group) + 1)) for group in groups.values())
        partitions[t] = [root(k) != root(k + 1) for k in range(9)]
        assert partitions[t] == [not (crossings[t] >> k) & 1 for k in range(9)]
    assert len({root(i) for i in range(10)}) == 1
    histories = {}
    activity_counts = [0] * len(control)
    boundary_counts = 0
    for state in f['K_states']:
        values = [(state >> i) & 1 for i in range(10)]
        masks = [state]
        for t, pair in enumerate(control):
            new = scalar.scalar(values, [pair])
            activity_counts[t] += values != new
            values = new
            masks.append(scalar.mask(values))
        assert values == sorted(values)
        histories[state] = masks
        target = masks[-1]
        for t, current in enumerate(masks):
            for k, cut in enumerate(partitions[t]):
                if cut:
                    low = (1 << (k + 1)) - 1
                    assert (current & low).bit_count() == (target & low).bit_count()
                    boundary_counts += 1
    assert all(activity_counts)
    for left, right in zip(control, control[1:]):
        assert not set(left).isdisjoint(right) or tuple(left) <= tuple(right)
    for r in records:
        passages = 0
        for t, (a, b) in enumerate(control):
            high, low = histories[r['x']][t], histories[r['y']][t]
            ports = (1 << a) | (1 << b)
            passages += bool(high & ports) or low & ports != ports
        assert passages <= r['cap'] + 3
    return dict(K_rows=127, original_target_inputs=2048, original_control_inputs=2048,
                positive_control_gates=21, actual_suffix_partitions=len(partitions),
                swapping_rows_by_gate=activity_counts, row_boundary_counts=boundary_counts,
                shifted_marker_bounds=len(records), positive_control_is_not_K18=True)


def check():
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    (HERE / 'scratch').mkdir(exist_ok=True)
    f = json.loads((PRIOR / 'fixture.json').read_text())
    scalar = module('published_scalar7436', PRIOR / 'check.py')
    raw = (HERE / 'all-cuts.json').read_bytes()
    cuts = json.loads(raw)
    assert cuts['fixture_sha256'] == hashlib.sha256((PRIOR / 'fixture.json').read_bytes()).hexdigest()
    assert len(cuts['selected_cuts']) == 108 and len(cuts['additional_cuts']) == 75
    selected = {(r['x'], r['y'], r['cap']) for r in cuts['selected_cuts']}
    prior = json.loads((HERE / 'pruning.json').read_text())
    old = prior['critical_single_bounds'] + prior['selected_mixed_bounds']
    assert len(old) == 33 and all((r['x'], r['y'], r['cap']) in selected for r in old)
    assert {(r['x'], r['y'], r['cap']) for r in old + cuts['additional_cuts']} == selected
    f['lower_sizes'] = {str(i): size for i, size in enumerate(cuts['lower_sizes'])}
    assignments = scalar.check_witnesses(f, f['after'], cuts['selected_cuts'], 0, 10)
    assert assignments == 21144
    dfa = dfa_audit(f, scalar)
    result = dict(agent='six-sorting-2', role='researcher',
                  status='STRUCTURE_LANGUAGE_AND_INPUT_CERTIFICATES_VERIFIED',
                  marker_witnesses=108, additional_witnesses=75,
                  scalar_middle_port_assignments=assignments, dfa=dfa,
                  activity=activity_table(), commute=commute_table(),
                  boundary_ranks=rank_table(), connectedness=connectedness(f),
                  target_and_positive_control=target_and_controls(f, scalar, cuts['selected_cuts']))
    return result


if __name__ == '__main__':
    print(json.dumps(check()), flush=True)
