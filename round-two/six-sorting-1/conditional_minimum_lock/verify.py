"""Standalone scalar/whole-cube/lattice checker; imports no producer or sibling.
Generic numeric primitives copied exactly with credit from actual9420 verify.py
(source d6a2bbdaabed14fdbcfd901256240a6f59c6c407), itself crediting9285/9127.
New abstract minimum-lock proof is ordinary; full-cube and monotone-lattice checks
verify its finite premises. Same author, no independent external verdict.
"""
import argparse
from copy import deepcopy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time
ROOT=Path(__file__).resolve().parent
METRICS={}
FIXTURE_SHA256='b2cadfceabddba477d9da1785a1462e823062628d092028227dfaccb51fec162'

def need(test, message):
    if not test:
        raise ValueError(message)


def count(name, amount=1):
    METRICS[name] = METRICS.get(name, 0) + amount


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(",", ":")).encode()).hexdigest()


def marked(value):
    return value < 0 or value > 1


def ports(row):
    return [sum(2 ** i for i, v in enumerate(row) if v < 0),
            sum(2 ** i for i, v in enumerate(row) if v > 1)]


def simulate(row, gates):
    values = list(row)
    for a, b in gates:
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values


def template(n, low, high):
    need(low >= 0 and high >= 0 and not low & high and (low | high) < 2 ** n,
         "invalid original marker masks")
    lows = [i for i in range(n) if low >> i & 1]
    highs = [i for i in range(n) if high >> i & 1]
    free = [i for i in range(n) if not (low | high) >> i & 1]
    row = [0] * n
    for rank, i in enumerate(lows):
        row[i] = rank - len(lows)
    for rank, i in enumerate(highs):
        row[i] = rank + 2
    return row, free


def family(n, gates, low, high, level):
    initial, free = template(n, low, high)
    touches = final = None
    active = 0
    for x in range(2 ** len(free)):
        row = list(initial)
        for j, i in enumerate(free):
            row[i] = x >> j & 1
        hit_mask = 0
        for t, (a, b) in enumerate(gates):
            hit = marked(row[a]) or marked(row[b])
            if hit:
                hit_mask |= 2 ** t
            if row[a] > row[b]:
                if not hit:
                    active |= 2 ** t
                row[a], row[b] = row[b], row[a]
        if touches is None:
            touches, final = hit_mask, ports(row)
        need(touches == hit_mask and final == ports(row), "free-dependent marker route")
        count(level + "_free_assignments")
        count(level + "_gate_evaluations", len(gates))
    redundant = (2 ** len(gates) - 1) & ~(touches | active)
    return [low, high, *final, touches.bit_count(), redundant.bit_count(), redundant]


def pruning(n, gates, record):
    low, high = record[:2]
    reference, free = template(n, low, high)
    carrier = [free.index(i) if i in free else None for i in range(n)]
    word, touches = [], 0
    for t, (a, b) in enumerate(gates):
        if marked(reference[a]) or marked(reference[b]):
            touches |= 2 ** t
            need(not record[6] >> t & 1, "marked gate also deleted as free identity")
            if reference[a] > reference[b]:
                reference[a], reference[b] = reference[b], reference[a]
                carrier[a], carrier[b] = carrier[b], carrier[a]
        elif not record[6] >> t & 1:
            word.append([carrier[a], carrier[b]])
    output_free = [i for i in range(n) if not marked(reference[i])]
    rename = {carrier[i]: j for j, i in enumerate(output_free)}
    need(sorted(rename) == list(range(len(free))), "nonbijective free-carrier routing")
    result = {"outer_record": record, "marked_touch_mask": touches,
              "input_free_wires": free, "output_free_wires": output_free,
              "input_to_output_wire": [rename[i] for i in range(len(free))],
              "retained_prefix": [[rename[a], rename[b]] for a, b in word]}
    need(touches.bit_count() == record[4] and record[6].bit_count() == record[5],
         "deletion count differs")
    need(len(word) + record[4] + record[5] == len(gates), "gates not partitioned")
    for x in range(2 ** len(free)):
        full = list(template(n, low, high)[0])
        small = [0] * len(free)
        for j, i in enumerate(free):
            full[i] = small[rename[j]] = x >> j & 1
        actual = simulate(full, gates)
        need([actual[i] for i in output_free] == simulate(small, result["retained_prefix"]),
             "conditional pruning function differs")
        count("pruning_function_assignments")
    return result


def literal_gates(gates, n):
    need(all(isinstance(g, list) and len(g) == 2 and
             all(type(p) is int for p in g) and 0 <= g[0] < g[1] < n for g in gates),
         "nonstandard literal comparator")


def cube(n, gates, low, locked, level):
    record = family(n, gates, low, 0, level)
    pruned = pruning(n, gates, record)
    initial, free = template(n, low, 0)
    output = pruned['output_free_wires']
    columns = [0]*len(output)
    is_minimum = True
    markers = None
    for x in range(2**len(free)):
        row = list(initial)
        for j, i in enumerate(free):
            row[i] = x >> j & 1
        actual = simulate(row, gates)
        sorted_marks = [v for v in actual if v < 0]
        if markers is None:
            markers = sorted_marks
        need(markers == sorted_marks, "marker ranks depend on free assignment")
        need(locked in output, "claimed minimum port is marked")
        is_minimum &= actual[locked] == min(actual[i] for i in output)
        for j, i in enumerate(output):
            columns[j] |= actual[i] << x
        count(level + "_minimum_assignments")
    return {'original_LOW_mask': low, 'pruning': pruned,
            'free_assignments': 2**len(free),
            'final_free_columns_sha256': digest([hex(c) for c in columns]),
            'physical_locked_port': locked,
            'locked_column_is_full_free_minimum': bool(is_minimum),
            'sorted_marker_values': markers}


def scalar_example(gates, assignment, low=0):
    row, free = template(13, low, 0)
    need(type(assignment) is int and 0 <= assignment < 2**len(free), "invalid original assignment")
    for j, i in enumerate(free):
        row[i] = assignment >> j & 1
    return {'assignment': assignment, 'original_LOW_mask': low,
            'input': row, 'output': simulate(row, gates), 'sorted_target': sorted(row)}


def antichain(terms):
    unique = set(terms)
    return sorted(a for a in unique if not any(b != a and b & a == b for b in unique))


def lattice(gates):
    # Boolean min is AND, max is OR. A term is a conjunction of variables.
    # Deleting supersets is the distributive-lattice absorption identity.
    wires = [[1 << i] for i in range(11)]
    snapshots = {'channels': 11}
    for t, (a, b) in enumerate(gates, 1):
        need(0 <= a < 11 and 0 <= b < 11 and a != b, "invalid oriented free comparator")
        x, y = wires[a], wires[b]
        wires[a] = antichain(i | j for i in x for j in y)
        wires[b] = antichain(x+y)
        if t == 9:
            snapshots['gate9_wire0_DNF'] = wires[0]
        if t == 14:
            snapshots['gate14_wire1_DNF'] = wires[1]
    snapshots['final_wire0_DNF'] = wires[0]
    need(wires[0] == [2047], "free prefix output zero is not the eleven-variable minimum")
    count('lattice_gates', len(gates))
    return snapshots


def require_minimum_on_original_cube(gates, low, locked):
    initial, free = template(13, low, 0)
    for x in range(2**len(free)):
        row = list(initial)
        for j, i in enumerate(free):
            row[i] = x >> j & 1
        actual = simulate(row, gates)
        need(actual[locked] == min(v for v in actual if not marked(v)),
             "original cube does not force the claimed free minimum")


def sorting_control(n, gates, level):
    literal_gates(gates, n)
    for x in range(2**n):
        row = [x >> i & 1 for i in range(n)]
        need(simulate(row, gates) == sorted(row), "positive network fails a Boolean input")
        count(level + '_inputs')
        count(level + '_gate_evaluations', len(gates))
    return {'channels': n, 'comparators': len(gates), 'Boolean_inputs': 2**n,
            'network_sha256': digest(gates)}


def validate_header(c, f):
    prefix = f['B23'] + f['LOW_suffix']
    literal_gates(c['prefix'], 13)
    need(c['schema'] == 'thirteen-conditional-minimum-lock-certificate-v1', "schema differs")
    need(c['agent'] == 'six-sorting-1' and c['role'] == 'researcher', "author role differs")
    need(c['fixture_sha256'] == FIXTURE_SHA256, "fixture pin differs")
    need(c['prefix'] == prefix and c['prefix_sha256'] == digest(prefix) and len(prefix) == 26,
         "literal partner-1 prefix differs")
    need(c['total_budget'] == 44 and c['imported_S11_lower_bound'] == 35 and
         c['minimum_sorting_completion_size_lower_bound'] == 45, "lower bound or budget differs")
    need(c['scope'] == 'Standard comparator completions of this literal partner-1 P26, arbitrary suffix order/depth.',
         "completion scope differs")
    base = c['original_minimum_cube']
    need(base['physical_locked_port'] == 2 and base['original_LOW_mask'] == 40 and
         base['pruning']['outer_record'] == [40, 0, 3, 0, 9, 0, 0], "tight original restriction differs")
    need(base['free_assignments'] == 2048 and base['sorted_marker_values'] == [-2, -1] and
         base['locked_column_is_full_free_minimum'] is True, "minimum cube premise differs")
    need(base['pruning']['output_free_wires'] == list(range(2, 13)) and
         len(base['pruning']['retained_prefix']) == 17, "free carrier frame differs")
    need(c['free_lattice_identity']['final_wire0_DNF'] == [2047], "lattice minimum premise differs")
    witness = c['full_original_Boolean_witness']
    need(witness == scalar_example(prefix, 235), "wrong full original witness")
    need(witness['output'][2] != witness['sorted_target'][2], "full original witness is correct at locked port")
    controls = c['all_incident_gate_controls']
    gates = [[i, 2] if i < 2 else [2, i] for i in range(13) if i != 2]
    need([r['gate'] for r in controls] == gates, "incident gate control missing or duplicated")
    for i, r in enumerate(controls):
        expected = [40, 0, 3, 0, 10, 0, 0] if i < 2 else [40, 0, 3, 0, 9, 1, 2**26]
        need(r['outer_record'] == expected and r['size_lower_bound'] == 45,
             "incident marked-or-identity count differs")


def check(c, f):
    validate_header(c, f)
    prefix = f['B23'] + f['LOW_suffix']
    base = cube(13, prefix, 40, 2, 'original_minimum_cube')
    need(c['original_minimum_cube'] == base, "replayed original minimum cube differs")
    need(base['locked_column_is_full_free_minimum'], "whole original cube is not minimum")
    need(c['free_lattice_identity'] == lattice(base['pruning']['retained_prefix']), "lattice derivation differs")
    negative = cube(13, prefix, 5, 2, 'same_configuration_negative_cube')
    need(c['same_configuration_negative_cube'] == negative, "negative control cube differs")
    need(base['pruning']['outer_record'][2:] == negative['pruning']['outer_record'][2:] and
         not negative['locked_column_is_full_free_minimum'], "same-configuration control is not negative")
    example = scalar_example(prefix, 571, 5)
    need(c['same_configuration_negative_witness'] == example and
         example['output'][2] != min(example['output'][2:]), "original negative witness differs")
    for r in c['all_incident_gate_controls']:
        actual = family(13, prefix + [r['gate']], 40, 0, 'incident_controls')
        need(r['outer_record'] == actual, "incident whole-cube control differs")
    need(c['positive11'] == sorting_control(11, f['positive11'], 'positive11'), "positive eleven sorter differs")
    tail = [[b-1, b] for a in range(3, 12) for b in range(a, 2, -1)]
    need(c['positive_prefix_completion'] == sorting_control(13, prefix + tail, 'positive_prefix_completion'),
         "positive 71-gate completion differs")


def damaged_controls(c, f):
    rejected = []

    def reject(name, action):
        try:
            action()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('damaged premise accepted: '+name)

    changes = [
        ('reversed_standard_orientation', lambda d: d['prefix'].__setitem__(0, [11, 0])),
        ('wrong_literal_gate', lambda d: d['prefix'].__setitem__(-1, [1, 4])),
        ('wrong_tight_D', lambda d: d['original_minimum_cube']['pruning']['outer_record'].__setitem__(4, 8)),
        ('false_free_identity', lambda d: d['original_minimum_cube']['pruning']['outer_record'].__setitem__(5, 1)),
        ('wrong_locked_port', lambda d: d['original_minimum_cube'].__setitem__('physical_locked_port', 3)),
        ('raised_budget', lambda d: d.__setitem__('total_budget', 45)),
        ('oriented_completion_scope', lambda d: d.__setitem__('scope', 'Arbitrary oriented completions.')),
        ('incomplete_original_cube', lambda d: d['original_minimum_cube'].__setitem__('free_assignments', 2047)),
        ('missing_minimum_literal', lambda d: d['free_lattice_identity'].__setitem__('final_wire0_DNF', [2046])),
        ('missing_incident_case', lambda d: d['all_incident_gate_controls'].pop()),
        ('correct_full_witness', lambda d: d.__setitem__('full_original_Boolean_witness', scalar_example(d['prefix'], 0))),
    ]
    for name, change in changes:
        damaged = deepcopy(c)
        change(damaged)
        reject(name, lambda: validate_header(damaged, f))
    damaged = deepcopy(c)
    damaged['original_minimum_cube']['pruning']['input_to_output_wire'][0] = 1
    reject('nonbijective_carrier', lambda: need(damaged['original_minimum_cube']['pruning'] ==
           pruning(13, f['B23']+f['LOW_suffix'], [40, 0, 3, 0, 9, 0, 0]), 'carrier frame differs'))
    damaged = deepcopy(c)
    damaged['original_minimum_cube']['final_free_columns_sha256'] = '0'*64
    reject('wrong_conditional_function', lambda: need(damaged['original_minimum_cube'] ==
           cube(13, f['B23']+f['LOW_suffix'], 40, 2, 'damaged_cube'), 'cube function differs'))
    # This test changes the original restriction and recomputes its valid route/counts.
    # It fails the SEMANTIC minimum predicate, rather than a fixed-mask/header pin.
    reject('repaired_same_configuration_original_domain',
           lambda: require_minimum_on_original_cube(f['B23']+f['LOW_suffix'], 5, 2))
    need(len(rejected) == 14, 'damage census differs')
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, default=ROOT / 'certificate.json')
    args = parser.parse_args()
    start = time.monotonic()
    raw = (ROOT / 'fixture.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == FIXTURE_SHA256, 'fixed fixture differs')
    f = json.loads(raw)
    raw_cert = args.certificate.read_bytes()
    c = json.loads(raw_cert)
    check(c, f)
    proof_metrics = dict(METRICS)
    METRICS.clear()
    rejected = damaged_controls(c, f)
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher',
                      'status': 'CONDITIONAL_MINIMUM_LOCK_PREMISES_VERIFIED',
                      'certificate_sha256': hashlib.sha256(raw_cert).hexdigest(),
                      'prefix_sha256': c['prefix_sha256'], 'marked_deletions': 9,
                      'prefix_free_identities': 0, 'locked_physical_port': 2,
                      'free_lattice_final_DNF': [2047], 'original_free_cube_assignments': 2048,
                      'imported_S11_lower_bound': 35, 'total_target': 44,
                      'sorting_completion_size_lower_bound': 45,
                      'incident_gate_controls': 12, 'damages_rejected': len(rejected),
                      'damage_names': rejected, 'positive_completion_size': 71,
                      'proof_metrics': proof_metrics, 'control_metrics': dict(METRICS),
                      'same_author_algorithmic_independence': True,
                      'external_person_review_claimed': False,
                      'scope': c['scope'], 'seconds': time.monotonic()-start,
                      'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))


if __name__ == '__main__':
    main()
