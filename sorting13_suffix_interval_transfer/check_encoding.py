"""Independent graph components versus the complete ten-wire clause table.

Author: six-sorting-2, researcher. Reads the actual generated clauses, but
uses a separate disjoint-set graph algorithm to determine transitions.
No SAT package, numerical approximation or full-state dump is required.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

from interval_blocks import encode

HERE = Path(__file__).resolve().parent
N = 10
PAIRS = tuple(itertools.combinations(range(N), 2))


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


def components(cuts, pair):
    parents = list(range(N))
    def root(i):
        while parents[i] != i:
            i = parents[i]
        return i
    def join(i, j):
        parents[root(i)] = root(j)
    for k in range(N - 1):
        if not (cuts >> k) & 1:
            join(k, k + 1)
    join(*pair)
    groups = {}
    for i in range(N):
        groups.setdefault(root(i), []).append(i)
    intervals = all(group == list(range(min(group), max(group) + 1)) for group in groups.values())
    present = sum((root(k) != root(k + 1)) << k for k in range(N - 1))
    return intervals, present


def frozen_control(fixture):
    word = list(map(tuple, fixture['K_control20']))
    w = Clauses()
    choices = [[w.var() for _ in PAIRS] for _ in word]
    cuts = encode(w, choices, PAIRS, len(word), N)
    parents = list(range(N))
    def root(i):
        while parents[i] != i:
            i = parents[i]
        return i
    mask_rows = [None] * (len(word) + 1)
    mask_rows[-1] = (1 << (N - 1)) - 1
    for t in range(len(word) - 1, -1, -1):
        a, b = word[t]
        parents[root(a)] = root(b)
        groups = {}
        for i in range(N):
            groups.setdefault(root(i), []).append(i)
        assert all(group == list(range(min(group), max(group) + 1)) for group in groups.values())
        mask_rows[t] = sum((root(k) != root(k + 1)) << k for k in range(N - 1))
    truth = [False] * (w.variables + 1)
    for t, pair in enumerate(word):
        truth[choices[t][PAIRS.index(pair)]] = True
    for t, row in enumerate(cuts):
        for k, variable in enumerate(row):
            truth[variable] = bool(mask_rows[t] >> k & 1)
    assert all(any(truth[abs(v)] == (v > 0) for v in clause) for clause in w.rows)
    for variable in cuts[-1]:
        truth[variable] = False
        assert not all(any(truth[abs(v)] == (v > 0) for v in clause) for clause in w.rows)
        truth[variable] = True
    return dict(positive_K20_clause_checks=len(w.rows), positive_K20_suffix_partitions=21,
                wrong_empty_suffix_bit_controls=N - 1)


def audit():
    if not __debug__:
        raise RuntimeError('Run without Python optimization')
    started = time.monotonic()
    w = Clauses()
    choices = [[w.var() for _ in PAIRS]]
    cuts = encode(w, choices, PAIRS, 1, N, terminal_empty=False)
    # Freeze the selector separately for each of its45 possible choices.
    # This is plain clause simplification under an exhaustive one-hot
    # assignment, not a second implementation of the cut recurrence.
    simplified = []
    for selector in choices[0]:
        selected_rows = []
        for row in w.rows:
            if any(abs(v) <= len(PAIRS) and ((v > 0) == (abs(v) == selector)) for v in row):
                continue
            selected_rows.append(tuple(v for v in row if abs(v) > len(PAIRS)))
        simplified.append(selected_rows)
    valid = invalid = negative_flips = 0
    table = []
    future_variables = set(cuts[1])
    for future in range(1 << (N - 1)):
        for j, pair in enumerate(PAIRS):
            allowed, present = components(future, pair)
            truth = [False] * (w.variables + 1)
            for k in range(N - 1):
                truth[cuts[0][k]] = bool(present >> k & 1)
                truth[cuts[1][k]] = bool(future >> k & 1)
            rows = simplified[j]
            def satisfies():
                return all(any(truth[abs(v)] == (v > 0) for v in row) for row in rows)
            assert satisfies() == allowed
            if allowed:
                valid += 1
                for variable in cuts[0]:
                    truth[variable] = not truth[variable]
                    assert not satisfies()
                    truth[variable] = not truth[variable]
                    negative_flips += 1
            else:
                # A violated guard uses only future cuts. No alternative
                # assignment to the earlier cuts can satisfy this edge.
                assert any(all(abs(v) in future_variables for v in row) and
                           not any(truth[abs(v)] == (v > 0) for v in row) for row in rows)
                invalid += 1
            table.append([future, list(pair), present if allowed else None])
    assert valid + invalid == 23040
    assert components(511, (0, 2))[0] is False
    assert components(510, (0, 2)) == (True, 508)
    assert components(508, (0, 2)) == (True, 508)
    full = Clauses()
    all_choices = [[full.var() for _ in PAIRS] for _ in range(18)]
    before = full.variables
    encode(full, all_choices, PAIRS, 18, N)
    fixture = json.loads((HERE / 'fixture.json').read_text())
    result = dict(agent='six-sorting-2', role='researcher',
                  status='ALL_TEN_WIRE_INTERVAL_CNF_TRANSITIONS_INDEPENDENTLY_VERIFIED',
                  wires=N, partitions=512, comparators=45, transition_rows=23040,
                  accepted_transitions=valid, impossible_interval_merges=invalid,
                  wrong_successor_bit_controls=negative_flips,
                  same_block_comparators_allowed=True, skipped_block_comparators_rejected=True,
                  extra_variables_for_K18=full.variables - before,
                  extra_clauses_for_K18=len(full.rows),
                  truth_table_sha256=hashlib.sha256(json.dumps(table, separators=(',', ':')).encode()).hexdigest(),
                  **frozen_control(fixture),
                  seconds=time.monotonic() - started,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    result = audit()
    certificate = json.loads((HERE / 'certificate.json').read_text())
    assert hashlib.sha256((HERE / 'fixture.json').read_bytes()).hexdigest() == certificate['fixture_sha256']
    assert hashlib.sha256((HERE / 'interval_blocks.py').read_bytes()).hexdigest() == certificate['encoder_sha256']
    for key, expected in certificate['encoding_controls'].items():
        assert result[key] == expected, key
    if args.out:
        args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
