"""Full five-input function closure before a zero-prior-LOW singleton.

Active edges respect each original tight cube. A general free-cut obstruction
may terminate a function. Closure completion, not a word cutoff, is essential.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import resource
import sys
import time

import hashlib
ROOT = Path(__file__).resolve().parent
import profile as s
SIZE = {11: 35, 12: 39}

def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()

def originals():
    for count in (1, 2):
        for ports in combinations(range(13), count):
            for selector in range(1 << count):
                low = sum(1 << q for j, q in enumerate(ports) if selector >> j & 1)
                high = sum(1 << q for j, q in enumerate(ports) if not selector >> j & 1)
                yield low, high

def profile(prefix, low, high):
    columns = iter(s.truth_columns(13 - (low | high).bit_count()))
    values = [s.LOW if low >> q & 1 else s.HIGH if high >> q & 1 else next(columns)
              for q in range(13)]
    d = r = mask = 0
    for t, (a, b) in enumerate(prefix):
        hit, redundant = s.transition(values, a, b)
        d += hit
        r += redundant
        if redundant:
            mask |= 1 << t
    return [low, high, *s.marked_ports(values), d, r, mask], values

def one_row_witness(record, values, full, ranks):
    k = 13 - (record[0] | record[1]).bit_count()
    if record[4] + record[5] != 44 - SIZE[k]:
        return None
    free = [q for q in range(13) if not isinstance(values[q], str)]
    for q in free:
        difference = full[q] ^ ranks[q]
        if not difference:
            continue
        if not all(not (values[t] & ~values[q]) if t < q else not (values[q] & ~values[t])
                   for t in free if t != q):
            continue
        x = (difference & -difference).bit_length() - 1
        return {'kind': 'TIGHT_FREE_CUT', 'record': record, 'imported_size': SIZE[k],
                'physical_port': q, 'full_Boolean_witness': x,
                'actual_bit': full[q] >> x & 1, 'sorted_bit': ranks[q] >> x & 1}
DEAD = [5, 6, 7, 9, 10]


def partition(values, k):
    total = (1 << (1 << k)) - 1
    parts = []
    for pattern in range(32):
        part = total
        for j, q in enumerate(DEAD):
            if isinstance(values[q], str):
                raise ValueError('tight mark in assumed dead preparation ports')
            part &= values[q] if pattern >> j & 1 else total ^ values[q]
        parts.append(part)
    if sum(part.bit_count() for part in parts) != 1 << k:
        raise ValueError('original cube partition is not complete')
    return parts


def apply_function(values, parts, function):
    result = list(values)
    for q, column in zip(DEAD, function):
        bits = column
        composed = 0
        while bits:
            flag = bits & -bits
            composed |= parts[flag.bit_length() - 1]
            bits -= flag
        result[q] = composed
    return result


def run(target):
    fixture = json.loads((ROOT / 'fixture.json').read_text())
    prefix = fixture['literal_prefix']
    if digest(prefix) != target['prefix_sha256']:
        raise ValueError('literal prefix provenance differs')
    original_rows = []
    for low, high in originals():
        marked = (low | high).bit_count()
        if marked == 3:
            continue
        record, values = profile(prefix, low, high)
        k = 13 - marked
        if record[4] + record[5] == 44 - SIZE[k]:
            parts = partition(values, k)
            image = sum(1 << i for i, part in enumerate(parts) if part)
            original_rows.append((record, values, parts, image))
    constraints = sorted({r[3] for r in original_rows})
    full = list(s.truth_columns(13))
    for a, b in prefix:
        full[a], full[b] = full[a] & full[b], full[a] | full[b]
    full_parts = partition(full, 13)
    ranks = {q: sum(1 << x for x in range(8192) if x.bit_count() >= 13 - q) for q in range(13)}
    identity = tuple(s.truth_columns(5))
    states = [identity]
    parents = [None]
    words = [[]]
    seen = {identity: 0}
    transitions = []
    blocked = []
    cursor = 0
    while cursor < len(states):
        if len(states) > 20000:
            raise RuntimeError('operational state cap reached; closure not complete')
        function = states[cursor]
        following_full = apply_function(full, full_parts, function)
        obstruction = None
        for record, values, parts, image in original_rows:
            after = apply_function(values, parts, function)
            obstruction = one_row_witness(record, after, following_full, ranks)
            if obstruction is not None:
                break
        if obstruction is not None:
            blocked.append({'state_id': cursor, 'witness': obstruction})
            cursor += 1
            continue
        for a, b in combinations(range(5), 2):
            inversions = function[a] & ~function[b]
            if any(not (inversions & image) for image in constraints):
                continue
            neighbor = list(function)
            neighbor[a], neighbor[b] = function[a] & function[b], function[a] | function[b]
            neighbor = tuple(neighbor)
            if neighbor not in seen:
                seen[neighbor] = len(states)
                states.append(neighbor)
                parents.append(cursor)
                words.append(words[cursor] + [[DEAD[a], DEAD[b]]])
            transitions.append([cursor, [DEAD[a], DEAD[b]], seen[neighbor]])
        cursor += 1
    return {'side': target['side'], 'genealogy': target['genealogy'], 'root_id': target['id'],
            'prefix_sha256': digest(prefix), 'dead_ports': DEAD,
            'tight_original_domains': len(original_rows), 'distinct_activity_images': len(constraints),
            'activity_image_masks': constraints,
            'function_states': len(states), 'admissible_edges': len(transitions),
            'blocked_functions': len(blocked), 'unblocked_functions': len(states) - len(blocked),
            'maximum_shortest_representative': max(map(len, words)),
            'closure_cursor': cursor, 'complete_closure': cursor == len(states),
            'states': [{'id': i, 'full32_function': list(state), 'shortest_word': words[i]}
                       for i, state in enumerate(states)], 'transitions': transitions,
            'blocked': blocked,
            'scope': 'Necessary preparation cover only; no singleton/tail or full-target exclusion.'}


def main():
    start = time.monotonic()
    fixture = json.loads((ROOT / 'fixture.json').read_text())
    if hashlib.sha256((ROOT / 'profile.py').read_bytes()).hexdigest() != fixture['packed_profile_sha256']:
        raise ValueError('upstream packed profile pin differs')
    result = run(fixture['target_metadata'])
    certificate = {'schema': 'native-HIGH3-zero-LOW-preparation-cover-v1',
                   'agent': 'six-sorting-2', 'role': 'researcher', 'n': 13, 'size_budget': 44,
                   'fixture_sha256': hashlib.sha256((ROOT / 'fixture.json').read_bytes()).hexdigest(),
                   'result': result}
    raw = json.dumps(certificate, separators=(',', ':')) + '\n'
    (ROOT / 'certificate.json').write_text(raw)
    print(json.dumps({'agent': 'six-sorting-2', 'role': 'researcher',
                      'status': 'COMPLETE_ZERO_PRIOR_LOW_PREPARATION_FUNCTION_COVER',
                      'function_states': result['function_states'], 'blocked': result['blocked_functions'],
                      'retained': result['unblocked_functions'], 'edges': result['admissible_edges'],
                      'maximum_shortest': result['maximum_shortest_representative'],
                      'certificate_sha256': hashlib.sha256(raw.encode()).hexdigest(),
                      'certificate_bytes': len(raw.encode()), 'seconds': time.monotonic() - start,
                      'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))

if __name__ == '__main__':
    main()
