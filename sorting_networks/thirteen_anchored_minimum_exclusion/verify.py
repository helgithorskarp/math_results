"""Independent scalar/inverse-fiber audit; imports no generator functions.

six-sorting-1, researcher. Exact distinct-rank and Boolean executions. The
minimum-once exclusion is explicitly imported rather than rerun.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def run(values, gates, marked_values=()):
    values = list(values)
    deletions = 0
    for low, high in gates:
        deletions += values[low] in marked_values or values[high] in marked_values
        values[low], values[high] = sorted((values[low], values[high]))
    return values, deletions


def marker_row(n, positions):
    positions = tuple(sorted(positions))
    marks = set(positions)
    row = [None] * n
    for value, port in enumerate(positions):
        row[port] = value
    for value, port in enumerate((p for p in range(n) if p not in marks), len(positions)):
        row[port] = value
    return row


def encode_positions(positions):
    return sum(2 ** p for p in positions)


def local_facts():
    transitions = []
    anchors = []
    doubles = 0
    for n in (10, 11, 13):
        pairs = sorted(itertools.combinations(range(n), 2), key=encode_positions)
        for low, high in itertools.combinations(range(n), 2):
            table = {}
            inverse = {}
            for pair in pairs:
                after, deleted = run(marker_row(n, pair), [(low, high)], (0, 1))
                output = tuple(p for p, v in enumerate(after) if v < 2)
                assert len(output) == 2
                table[pair] = output, deleted
                inverse.setdefault(output, []).append((pair, deleted))
                transitions.append([n, encode_positions(pair), low, high, encode_positions(output), deleted])
            for before in inverse.values():
                assert len(before) in (1, 2)
                if len(before) == 2:
                    doubles += 1
                    assert {deleted for pair, deleted in before} == {1}
            for p in range(n):
                after, deleted = run(marker_row(n, [p]), [(low, high)], (0,))
                newp = after.index(0)
                subset = [pair for pair in pairs if p in pair]
                images = [table[pair][0] for pair in subset]
                assert all(newp in dest for dest in images)
                if deleted:
                    # An inverse-fiber check proves injectivity on the anchored domain.
                    assert all(sum(p in pre for pre, add in inverse[dest]) == 1 for dest in images)
                    assert all(table[pair][1] == 1 for pair in subset)
                else:
                    assert newp == p
                    assert all((p in pair) == (p in table[pair][0]) for pair in pairs)
                anchors.append([n, p, low, high, newp, int(deleted),
                                [[encode_positions(pair), encode_positions(table[pair][0]), table[pair][1]]
                                 for pair in subset]])
    return {'orders': [10, 11, 13], 'marker_transitions': len(transitions),
            'two_preimage_fibers': doubles, 'port_gate_facts': len(anchors),
            'transition_sha256': digest(transitions), 'anchor_sha256': digest(anchors)}


def reproduce(fixture):
    cases = []
    suffix = fixture['bridge'] + fixture['known19_control']
    assert len(suffix) == 21 and len(fixture['known19_control']) == 19
    for rec in fixture['cases']:
        prefix = fixture['prefix21'] + rec['tournament']
        assert len(prefix) == 24
        yrows = set()
        rrows = set()
        for row in itertools.product((0, 1), repeat=13):
            y, unused = run(row, prefix)
            assert y[11:] == sorted(row)[-2:]
            yrows.add(tuple(y[:11]))
            r, unused = run(y, fixture['bridge'])
            assert r[10:] == sorted(row)[-3:]
            rrows.add(tuple(r[:10]))
            assert run(y, suffix)[0] == sorted(row)
            assert run(r, fixture['known19_control'])[0] == sorted(row)
        yimage = sorted(encode_positions(p for p, v in enumerate(row) if v) for row in yrows)
        rimage = sorted(encode_positions(p for p, v in enumerate(row) if v) for row in rrows)
        assert yimage == rec['Y_states'] and rimage == fixture['R_states']
        strongest = {}
        for pair in itertools.combinations(range(13), 2):
            values = marker_row(13, pair)
            y, deleted = run(values, prefix, (0, 1))
            output = tuple(p for p, v in enumerate(y) if v < 2)
            assert all(p < 11 for p in output)
            strongest[output] = max(strongest.get(output, 0), deleted)
            r, more_deleted = run(y, fixture['bridge'], (0, 1))
            assert more_deleted == 0
            assert tuple(p for p, v in enumerate(r) if v < 2) == output
        profile = sorted([encode_positions(pair), d] for pair, d in strongest.items())
        assert profile == fixture['two_minimum_profile']
        row = marker_row(13, [fixture['anchor_original_input']])
        y, deleted = run(row, prefix, (0,))
        anchor_port = y.index(0)
        assert anchor_port == fixture['anchor_port'] == 1
        # Boolean membership, needed to apply the imported Y sorting theorem.
        single = tuple(int(p != anchor_port) for p in range(11))
        assert single in yrows
        mass = sum(2 ** d for pair, d in strongest.items() if anchor_port in pair)
        weight = sum(2 ** d for d in strongest.values())
        cap = 2 ** (fixture['full_budget'] - fixture['S11'])
        lower = 2 ** fixture['imported_minimum_passages'] * mass
        assert (mass, weight, lower, cap) == (160, 208, 640, 512) and lower > cap
        cases.append({'case': rec['case'], 'Y_states': len(yrows), 'R_states': len(rrows),
                      'Y_image_sha256': digest(yimage), 'R_image_sha256': digest(rimage),
                      'profile': profile, 'initial_weight': weight, 'initial_anchor_mass': mass,
                      'one_zero_original_input': fixture['anchor_original_input'],
                      'one_zero_Y_port': anchor_port, 'one_zero_prefix_deletions': deleted,
                      'required_suffix_passages': fixture['imported_minimum_passages'],
                      'anchored_lower_bound': lower, 'weight_ceiling': cap,
                      'original_inputs_checked': 8192, 'Y21_and_R19_controls': True})
    return {'cases': cases, 'local_controls': local_facts(),
            'conclusion': {'Y1_minimum': 21, 'Y2_minimum': 21, 'R137_minimum': 19,
                           'P21_minimum_suffix': 24,
                           'global_S13_interval': [44, 45]},
            'imported_minimum_once_exclusion': fixture['imports']['minimum_once']['graph_ref'],
            'imported_prefix_reduction': fixture['imports']['Y_provenance']['graph_ref'],
            'independence_scope': 'new local transport facts and fixture/control checks; prior exclusion and P21 reduction imported'}


def main():
    if sys.flags.optimize:
        raise RuntimeError('Run without -O: exact assertions are required.')
    result = reproduce(json.loads((HERE / 'fixture.json').read_text()))
    expected = json.loads((HERE / 'certificate.json').read_text())['expected']
    assert result == expected
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher', 'status': 'all_new_checks_passed',
                      'algorithm': 'scalar_rank_inverse_fibers', 'certificate_sha256': hashlib.sha256((HERE / 'certificate.json').read_bytes()).hexdigest(),
                      'checked': result}, indent=2))


if __name__ == '__main__':
    main()
