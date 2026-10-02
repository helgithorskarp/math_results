"""Packed truth-column producer for the original-domain minimum-lock premises.
No runtime sibling imports. Carrier deletion follows the credited generic
producer in actual9420; this packet has no nested bound or suffix enumeration.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
FIXTURE_SHA256 = 'b2cadfceabddba477d9da1785a1462e823062628d092028227dfaccb51fec162'


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def columns(n):
    return [sum(1 << x for x in range(1 << n) if x >> i & 1) for i in range(n)]


def packed(gates, original_low=0):
    free = [i for i in range(13) if not original_low >> i & 1]
    lows = [i for i in range(13) if original_low >> i & 1]
    initial = columns(len(free))
    values = [lows.index(i)-len(lows) if i in lows else initial[free.index(i)]
              for i in range(13)]
    carrier = [None if i in lows else free.index(i) for i in range(13)]
    retained = []
    touch = identity = 0
    for t, (a, b) in enumerate(gates):
        need(0 <= a < b < 13, 'nonstandard literal prefix')
        x, y = values[a], values[b]
        if x < 0 or y < 0:
            touch |= 1 << t
            if x > y:
                values[a], values[b] = y, x
                carrier[a], carrier[b] = carrier[b], carrier[a]
        else:
            if x & ~y:
                retained.append([carrier[a], carrier[b]])
            else:
                identity |= 1 << t
            values[a], values[b] = x & y, x | y
    output = [i for i, v in enumerate(values) if v >= 0]
    rename = {carrier[i]: j for j, i in enumerate(output)}
    record = [original_low, 0, sum(1 << i for i, v in enumerate(values) if v < 0),
              0, touch.bit_count(), identity.bit_count(), identity]
    return values, {'outer_record': record, 'marked_touch_mask': touch,
                    'input_free_wires': free, 'output_free_wires': output,
                    'input_to_output_wire': [rename[j] for j in range(len(free))],
                    'retained_prefix': [[rename[a], rename[b]] for a, b in retained]}


def cube(gates, low, locked):
    values, pruned = packed(gates, low)
    output = pruned['output_free_wires']
    minimum = (1 << ((1 << len(output))-1))
    return {'original_LOW_mask': low, 'pruning': pruned,
            'free_assignments': 1 << len(output),
            'final_free_columns_sha256': digest([hex(values[i]) for i in output]),
            'physical_locked_port': locked,
            'locked_column_is_full_free_minimum': values[locked] == minimum,
            'sorted_marker_values': [values[i] for i in range(13) if values[i] < 0]}


def example(gates, assignment, low=0):
    values, pruned = packed(gates, low)
    lows = [i for i in range(13) if low >> i & 1]
    free = pruned['input_free_wires']
    inp = [lows.index(i)-len(lows) if i in lows else assignment >> free.index(i) & 1
           for i in range(13)]
    out = [v if v < 0 else v >> assignment & 1 for v in values]
    return {'assignment': assignment, 'original_LOW_mask': low,
            'input': inp, 'output': out, 'sorted_target': sorted(inp)}


def insertion_tail():
    return [[b-1, b] for a in range(3, 12) for b in range(a, 2, -1)]


def sorting_control(n, gates):
    values = columns(n)
    for a, b in gates:
        need(0 <= a < b < n, 'nonstandard positive control')
        values[a], values[b] = values[a] & values[b], values[a] | values[b]
    target = [sum(1 << x for x in range(1 << n) if i >= n-x.bit_count()) for i in range(n)]
    need(values == target, 'positive network does not sort every Boolean input')
    return {'channels': n, 'comparators': len(gates), 'Boolean_inputs': 1 << n,
            'network_sha256': digest(gates)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'certificate.json')
    args = parser.parse_args()
    start = time.monotonic()
    raw = (ROOT / 'fixture.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == FIXTURE_SHA256, 'fixed fixture differs')
    f = json.loads(raw)
    prefix = f['B23'] + f['LOW_suffix']
    locked = f['physical_locked_port']
    base = cube(prefix, f['original_LOW_mask'], locked)
    control = cube(prefix, f['same_configuration_control_LOW_mask'], locked)
    need(base['locked_column_is_full_free_minimum'] and not control['locked_column_is_full_free_minimum'],
         'original-domain minimum distinction failed')
    incidents = []
    for q in range(13):
        if q == locked:
            continue
        gate = sorted([q, locked])
        item = cube(prefix + [gate], f['original_LOW_mask'], locked)
        incidents.append({'gate': gate, 'outer_record': item['pruning']['outer_record'],
                          'size_lower_bound': sum(item['pruning']['outer_record'][4:6]) + 35})
    counter = example(prefix, f['original_Boolean_counterexample_integer'])
    need(counter['output'][locked] != counter['sorted_target'][locked], 'full-cube witness is correct at locked port')
    same = example(prefix, f['same_configuration_control_assignment'], f['same_configuration_control_LOW_mask'])
    need(same['output'][locked] != min(same['output'][2:]), 'negative original-cube witness is minimum')
    packet = {'schema': 'thirteen-conditional-minimum-lock-certificate-v1',
              'agent': 'six-sorting-1', 'role': 'researcher', 'fixture_sha256': FIXTURE_SHA256,
              'scope': 'Standard comparator completions of this literal partner-1 P26, arbitrary suffix order/depth.',
              'prefix': prefix, 'prefix_sha256': digest(prefix), 'total_budget': 44,
              'imported_S11_lower_bound': 35, 'minimum_sorting_completion_size_lower_bound': 45,
              'original_minimum_cube': base, 'same_configuration_negative_cube': control,
              'same_configuration_negative_witness': same, 'full_original_Boolean_witness': counter,
              'free_lattice_identity': {'channels': 11, 'gate9_wire0_DNF': [1997],
                                        'gate14_wire1_DNF': [51, 562], 'final_wire0_DNF': [2047]},
              'all_incident_gate_controls': incidents,
              'positive11': sorting_control(11, f['positive11']),
              'positive_prefix_completion': sorting_control(13, prefix + insertion_tail())}
    args.output.write_text(json.dumps(packet, separators=(',', ':'))+'\n')
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher',
                      'status': 'CONDITIONAL_MINIMUM_LOCK_CERTIFICATE_REGENERATED',
                      'certificate_bytes': args.output.stat().st_size,
                      'certificate_sha256': hashlib.sha256(args.output.read_bytes()).hexdigest(),
                      'seconds': time.monotonic()-start,
                      'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))


if __name__ == '__main__':
    main()
