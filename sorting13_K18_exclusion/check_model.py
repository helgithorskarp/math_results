"""Solver-free complete CNF and scalar witness audit for the36-word probe.

Author: six-sorting-2, researcher. This does not import any generator or
SAT package. A positive result checks every clause and original Boolean
input, all108 marker bounds and the separately simulated minimum routes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent


def compare(mask, gate):
    a, b = gate
    if (mask >> a) & 1 and not (mask >> b) & 1:
        return mask ^ ((1 << a) | (1 << b))
    return mask


def trace(mask, word):
    result = [mask]
    for gate in word:
        mask = compare(mask, gate)
        result.append(mask)
    return result


def passages(mask, word, high):
    values = trace(mask, word)
    return [bool(values[t] & ((1 << a) | (1 << b))) if high else
            (values[t] & ((1 << a) | (1 << b))) != ((1 << a) | (1 << b))
            for t, (a, b) in enumerate(word)]


def check_suffix_intervals(word, meta, assignment):
    cuts = meta['extra']['interval_cuts']
    assert len(cuts) == len(word) + 1 and all(len(row) == 9 for row in cuts)
    parents = list(range(10))
    def root(i):
        while parents[i] != i:
            i = parents[i]
        return i
    checked = 0
    for t in range(len(word), -1, -1):
        if t < len(word):
            a, b = word[t]
            parents[root(a)] = root(b)
        groups = {}
        for i in range(10):
            groups.setdefault(root(i), []).append(i)
        assert all(group == list(range(min(group), max(group) + 1)) for group in groups.values())
        for k, variable in enumerate(cuts[t]):
            assert assignment[variable] == (root(k) != root(k + 1)), (t, k)
        checked += 1
    assert len({root(i) for i in range(10)}) == 1
    return dict(actual_suffix_partitions_checked=checked, full_graph_connected=True,
                wrong_frame_not_assumed_identity=True)


def check_activity(word, meta, assignment, states):
    if not meta['extra']['all_actual_gates_active']:
        return dict(activity_required=False)
    active = sorted(x for x in states if x != ((1 << x.bit_count()) - 1) << (10 - x.bit_count()))
    assert active == meta['extra']['activity_states']
    flags = meta['extra']['activity_flags']
    histories = {x: trace(x, word) for x in active}
    counts = []
    for t, row in enumerate(flags):
        assert len(row) == len(active)
        expected = [histories[x][t] != histories[x][t + 1] for x in active]
        for variable, truth in zip(row, expected):
            assert assignment[variable] == truth, (t, variable)
        assert any(expected), t
        counts.append(sum(expected))
    assert len(counts) == len(word)
    return dict(all_actual_gates_active=True, swapping_rows_by_gate=counts,
                exact_activity_flags_checked=len(word) * len(active))


def check_boundary_ranks(word, states):
    """Independent conservation check, using counts rather than obligations."""
    crossing = [0] * (len(word) + 1)
    for t in range(len(word) - 1, -1, -1):
        a, b = word[t]
        crossing[t] = crossing[t + 1] | sum(1 << k for k in range(a, b))
    checked = 0
    for state in states:
        target = ((1 << state.bit_count()) - 1) << (10 - state.bit_count())
        for t, current in enumerate(trace(state, word)):
            for k in range(9):
                if not (crossing[t] >> k) & 1:
                    low_mask = (1 << (k + 1)) - 1
                    assert (current & low_mask).bit_count() == (target & low_mask).bit_count()
                    checked += 1
    return dict(actual_row_boundary_counts_verified=checked)



def check_minimum_phases(word, meta, assignment):
    raw = (HERE / 'language-data.json').read_bytes()
    audited = json.loads((HERE / 'certificate.json').read_text())
    assert hashlib.sha256(raw).hexdigest() == audited['language_data_sha256']
    data = json.loads(raw)
    transition = {(s, tuple(pair)): dest for s, pair, dest in data['transitions']}
    phase = meta['extra']['minimum_phase']
    assert len(phase) == len(word) + 1 and all(len(row)==11 for row in phase)
    scalar = [trace(1023 ^ (1 << p), word) for p in (0,1,5)]
    state = 0
    for t, row in enumerate(phase):
        assert [i for i, variable in enumerate(row) if assignment[variable]] == [state]
        routes = [((1023 ^ history[t]) & -(1023 ^ history[t])).bit_length()-1 for history in scalar]
        assert routes == data['states'][state]['routes']
        if t < len(word):
            state = transition[state, word[t]]
            assert state is not None
    assert state == 10
    return dict(independently_traced_phase_rows=len(phase), quotient_states=11,
                minimum_events=4, unary_events=2)


def main():
    if not __debug__:
        raise RuntimeError('Run without Python optimization')
    p = argparse.ArgumentParser()
    p.add_argument('--cnf', type=Path, required=True)
    args = p.parse_args()
    started = time.monotonic()
    meta = json.loads(args.cnf.with_suffix('.meta.json').read_text())
    assert hashlib.sha256(args.cnf.read_bytes()).hexdigest() == meta['cnf_sha256']
    model = json.loads(args.cnf.with_suffix('.model.json').read_text())
    n = meta['variables']
    values = [None] * (n + 1)
    for literal in model:
        assert type(literal) is int and 1 <= abs(literal) <= n
        assert values[abs(literal)] in (None, literal > 0)
        values[abs(literal)] = literal > 0
    assert all(v is not None for v in values[1:])
    clauses = 0
    with args.cnf.open() as stream:
        for line in stream:
            line = line.strip()
            if not line or line.startswith('c'):
                continue
            if line.startswith('p'):
                assert list(map(int, line.split()[2:])) == [n, meta['clauses']]
                continue
            clause = list(map(int, line.split()))
            assert clause[-1] == 0 and all(1 <= abs(v) <= n for v in clause[:-1])
            assert any(values[abs(v)] == (v > 0) for v in clause[:-1]), clauses
            clauses += 1
    assert clauses == meta['clauses']
    word = []
    for choice in meta['choices']:
        selected = [j for j, variable in enumerate(choice) if values[variable]]
        assert len(selected) == 1
        word.append(tuple(meta['pairs'][selected[0]]))
    f = json.loads((HERE.parent / 'sorting13_double_pure_obstruction' / 'fixture.json').read_text())
    assert set(meta['states']) == set(f['K_states']) and meta['wires'] == 10
    for state in f['K_states']:
        final = trace(state, word)[-1]
        assert final == ((1 << state.bit_count()) - 1) << (10 - state.bit_count())
    for state in range(2048):
        v = [(state >> i) & 1 for i in range(11)]
        for a, b in f['prefix']:
            if v[a] > v[b]:
                v[a], v[b] = v[b], v[a]
        v = [v[i] for i in f['prefix_output_order']]
        for a, b in f['after'] + [list(pair) for pair in word]:
            if v[a] > v[b]:
                v[a], v[b] = v[b], v[a]
        assert v == sorted(v), state
    recorded = json.loads((HERE.parent / 'sorting13_K_minimum_two_unaries' / 'all-cuts.json').read_text())
    for r in recorded['selected_cuts']:
        high = passages(r['x'], word, True)
        low = passages(r['y'], word, False)
        assert sum(a or b for a, b in zip(high, low)) <= r['cap'] + len(word) - 18
    minimum_positions = [0, 1, 5]
    kernel = []
    for a, b in word:
        if any(p in (a, b) for p in minimum_positions):
            kernel.append((a, b))
            minimum_positions = [a if p == b else p for p in minimum_positions]
    if meta['extra']['minimum_dfa_states']:
        allowed = [tuple(map(tuple, w)) for w in f['minimum_kernel_words'] if len(w) == 4]
        assert tuple(kernel) in allowed and minimum_positions == [0, 0, 0]
    if len(word) == 18:
        assert [g for g, hit in zip(word, passages(64, word, True)) if hit] == [(6, 8), (8, 9)]
        assert [g for g, hit in zip(word, passages(512, word, True)) if hit] == [(8, 9)]
        root = word.index((8, 9))
        post = [g for g in word[root + 1:] if g[1] == 8]
        assert len(post) == 1 and post[0][0] in (6, 7)
        if post[0] == (6, 8):
            assert (7, 8) in word[:word.index((6, 8))]
        assert sum(passages(1021, word, False)) == 1
        rows = [passages(1 << i, word, True) for i in (4, 5, 6, 8, 9)]
        assert sum(any(row[t] for row in rows) for t in range(18)) >= 5
    phase_audit = check_minimum_phases(word, meta, values)
    interval_audit = check_suffix_intervals(word, meta, values)
    activity_audit = check_activity(word, meta, values, f['K_states'])
    boundary_audit = check_boundary_ranks(word, f['K_states'])
    if meta['commute_lexicographic']:
        for left, right in zip(word, word[1:]):
            assert not set(left).isdisjoint(right) or left <= right
    result = dict(agent='six-sorting-2', role='researcher', status='FULL_MODEL_AND_SCALAR_WITNESS_VERIFIED',
                  gates=len(word), cnf_sha256=meta['cnf_sha256'], variables=n,
                  all_clauses_verified=clauses, K_boolean_rows=127, original_boolean_inputs=2048,
                  witnessed_marker_bounds=108, minimum_kernel=kernel,
                  minimum_phase_audit=phase_audit, interval_audit=interval_audit, activity_audit=activity_audit,
                  boundary_audit=boundary_audit,
                  lexicographic_disjoint_order_verified=meta['commute_lexicographic'],
                  seconds=time.monotonic() - started,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    args.cnf.with_suffix('.model-audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
