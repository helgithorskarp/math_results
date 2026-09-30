"""Independent36-word scalar/future cover versus actual11-state clauses.

Author: six-sorting-2, researcher. No native solver is imported.
"""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import resource
import time

import language

HERE = Path(__file__).resolve().parent
PUBLIC = HERE.parent
PAIRS = tuple(itertools.combinations(range(10), 2))


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def classified_language(f, scalar):
    assert scalar.check_minimum_cover(f['minimum_kernel_words']) == 175
    words = tuple(sorted(tuple(map(tuple, w)) for w in f['minimum_kernel_words'] if len(w) == 4))
    assert len(words) == 36
    states = [((0, 1, 5), words)]
    labels = {states[0]: 0}
    rows = {}
    for s, (positions, futures) in enumerate(states):
        for pair in PAIRS:
            if not any(p in pair for p in positions):
                target = s
            else:
                tails = tuple(sorted({word[1:] for word in futures if word and word[0] == pair}))
                if not tails:
                    target = None
                else:
                    after = tuple(pair[0] if p == pair[1] else p for p in positions)
                    child = after, tails
                    if child not in labels:
                        labels[child] = len(states)
                        states.append(child)
                    target = labels[child]
            rows[s, pair] = target
    assert len(states) == 11 and states[10] == ((0, 0, 0), ((),))
    assert tuple(pos for pos, future in states) == language.POSITIONS
    assert len(rows) == 495
    for (s, pair), target in rows.items():
        assert language.destination(s, pair) == target
    return words, states, rows


class Clauses:
    def __init__(self):
        self.variables = 0
        self.rows = []
        self.counters = []
    def var(self):
        self.variables += 1
        return self.variables
    def add(self, *literals):
        self.rows.append(tuple(literals))
    def exactly_one(self, variables):
        before = self.variables
        encoder = module('actual_sequential_writer', PUBLIC / 'sorting13_pure_maximum_exclusions' / 'sequential_sat.py')
        encoder.Writer.exactly_one(self, variables)
        self.counters.append((tuple(variables), tuple(range(before+1,self.variables+1))))


def actual_clauses(rows):
    w = Clauses()
    choices = [[w.var() for _ in PAIRS]]
    phases = language.encode(w, choices, PAIRS, 1)
    assert (phases[0][0],) in w.rows and (phases[1][10],) in w.rows
    local = [row for row in w.rows if row not in ((phases[0][0],), (phases[1][10],))]
    checks = accepted = 0
    for (s, pair), target in rows.items():
        choice = choices[0][PAIRS.index(pair)]
        for candidate in range(11):
            positive = {choice, phases[0][s], phases[1][candidate]}
            for variables, auxiliaries in w.counters:
                assert len(variables)==11 and len(auxiliaries)==10
                seen = False
                for variable, auxiliary in zip(variables, auxiliaries):
                    seen |= variable in positive
                    if seen:
                        positive.add(auxiliary)
            satisfiable = all(any((v > 0) == (abs(v) in positive) for v in row) for row in local)
            assert satisfiable == (candidate == target), (s, pair, candidate, target)
            checks += 1
            accepted += satisfiable
    assert checks == 5445
    return dict(actual_transition_assignments=checks, allowed_transitions=accepted,
                wrong_successor_controls=checks-accepted, initial_and_final_units_verified=True,
                actual_width11_sequential_counter_clauses_included=True)


def scalar_word(word, scalar):
    rows = [[int(i != p) for i in range(10)] for p in (0, 1, 5)]
    events = []
    unary = binary = 0
    for pair in word:
        occupied = {row.index(0) for row in rows}
        groups = occupied & set(pair)
        if groups:
            events.append(tuple(pair))
            unary += len(groups) == 1
            binary += len(groups) == 2
        rows = [scalar.scalar(row, [pair]) for row in rows]
    return tuple(events), tuple(row.index(0) for row in rows), unary, binary


def controls(words, rows, scalar):
    positives = negatives = 0
    for word in words:
        interleaved = []
        state = 0
        for event in word:
            nongates = [pair for pair in PAIRS if rows[state, pair] == state]
            interleaved += nongates[:2] + [event]
            state = rows[state, event]
        interleaved += [(2, 3)] * (18 - len(interleaved))
        assert len(interleaved) == 18
        assert scalar_word(interleaved, scalar) == (word, (0, 0, 0), 2, 2)
        state = 0
        for pair in interleaved:
            state = rows[state, pair]
            assert state is not None
        assert state == 10
        positives += 1
        changed = [(0, 1)] + interleaved[1:]
        state = 0
        for pair in changed:
            state = rows[state, pair]
            if state is None:
                break
        assert state is None
        negatives += 1
    stationary = ((5, 6), (5, 6), (0, 5), (0, 1))
    assert stationary in words and rows[0, (5, 6)] == 4 and rows[4, (5, 6)] == 8
    assert scalar_word(stationary, scalar) == (stationary, (0, 0, 0), 2, 2)
    assert rows[8, (5, 6)] is None
    return dict(interleaved_positive_words=positives, premature_root_negative_words=negatives,
                repeated_stationary_unaries_counted=True, third_unary_rejected=True)


def commutation(rows):
    checked = 0
    for s in range(11):
        for p, q in itertools.combinations(PAIRS, 2):
            if not set(p).isdisjoint(q):
                continue
            left = rows[s, p]
            left = None if left is None else rows[left, q]
            right = rows[s, q]
            right = None if right is None else rows[right, p]
            assert left == right
            checked += 1
    assert checked == 6930
    return checked


def positive_control(f, scalar, words):
    word = list(map(tuple, json.loads((HERE / 'positive_word.json').read_text())))
    # Independent local disjoint ordering, then scalar all-input replay.
    while True:
        for i in range(len(word)-1):
            if word[i] > word[i+1] and set(word[i]).isdisjoint(word[i+1]):
                word[i:i+2] = [word[i+1], word[i]]
                break
        else:
            break
    events, positions, unary, binary = scalar_word(word, scalar)
    assert events in words and (positions, unary, binary) == ((0,0,0),2,2)
    for state in range(2048):
        values = [(state >> i) & 1 for i in range(11)]
        after = scalar.run_prefix(values, f, f['after'])
        assert scalar.scalar(after, word) == sorted(values)
    histories = [[(x>>i)&1 for i in range(10)] for x in f['K_states']]
    counts = []
    for pair in word:
        after = [scalar.scalar(row,[pair]) for row in histories]
        counts.append(sum(a!=b for a,b in zip(histories,after)))
        histories = after
    assert all(counts) and all(row==sorted(row) for row in histories)
    return dict(gates=len(word),K_rows=127,original_boolean_inputs=2048,
                minimum_word=events,unary_events=unary,binary_events=binary,
                actual_swapping_rows=counts,canonical_control=word)


def check():
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    start = time.monotonic()
    f = json.loads((PUBLIC / 'sorting13_double_pure_obstruction' / 'fixture.json').read_text())
    scalar = module('independent7436_scalar', PUBLIC / 'sorting13_double_pure_obstruction' / 'check.py')
    image = set()
    for mask in range(2048):
        values = [(mask >> i) & 1 for i in range(11)]
        after = scalar.run_prefix(values, f, f['after'])
        assert after[10] == max(values)
        image.add(scalar.mask(after[:10]))
        assert scalar.scalar(after, f['K_control20']) == sorted(values)
    assert image == set(f['K_states']) and len(image) == 127
    words, states, rows = classified_language(f, scalar)
    table = dict(states=[dict(routes=pos,futures=future) for pos,future in states],
                 transitions=[[s,list(pair),dest] for (s,pair),dest in rows.items()],words=words)
    data = json.dumps(table,indent=2)+'\n'
    assert (HERE / 'language-data.json').read_text() == data
    result = dict(agent='six-sorting-2',role='researcher',status='COMPLETE36_WORD_LANGUAGE_AND_ACTUAL_CLAUSES_VERIFIED',
                  scalar_complete_cover_states=175,K_image_inputs=2048,K20_control_inputs=2048,words=36,quotient_states=11,pair_transitions=495,
                  actual_clauses=actual_clauses(rows),controls=controls(words,rows,scalar),
                  commutation_cases=commutation(rows),positive_control=positive_control(f,scalar,words),
                  language_data_sha256=hashlib.sha256(data.encode()).hexdigest(),
                  seconds=time.monotonic()-start,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return result


if __name__ == '__main__':
    (HERE / 'scratch').mkdir(exist_ok=True)
    result = check()
    (HERE / 'scratch' / 'language-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
