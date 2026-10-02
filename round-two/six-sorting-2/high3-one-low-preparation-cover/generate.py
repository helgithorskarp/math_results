"""Complete six-input preparation cover; no depth or word-length cutoff.

six-sorting-2, researcher. Ancestor packed profile is byte-pinned. Each
activity subset comes from a whole original tight cube at the NEW prefix.
An operational cap returns an explicitly incomplete resumable record.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import sys
import time

PARENT = Path(__file__).resolve().parent
PROFILE_SHA = 'dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719'
if hashlib.sha256((PARENT / 'profile.py').read_bytes()).hexdigest() != PROFILE_SHA:
    raise ValueError('ancestral packed profile pin differs')
sys.path.insert(0, str(PARENT.resolve()))
import profile as s
SIZE = {11: 35, 12: 39}


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def originals():
    for count in (1, 2):
        for ports in combinations(range(13), count):
            for selector in range(1 << count):
                low = sum(1 << q for j, q in enumerate(ports) if selector >> j & 1)
                high = sum(1 << q for j, q in enumerate(ports) if not selector >> j & 1)
                yield low, high


def original_profile(prefix, low, high):
    k = 13 - (low | high).bit_count()
    columns = iter(s.truth_columns(k))
    values = [s.LOW if low >> q & 1 else s.HIGH if high >> q & 1 else next(columns)
              for q in range(13)]
    d = r = mask = 0
    for t, (a, b) in enumerate(prefix):
        hit, redundant = s.transition(values, a, b)
        d += hit
        r += redundant
        mask |= redundant << t
    return [low, high, *s.marked_ports(values), d, r, mask], values


def partition(values, k, dead):
    total = (1 << (1 << k)) - 1
    parts = []
    for pattern in range(1 << len(dead)):
        part = total
        for j, q in enumerate(dead):
            if isinstance(values[q], str):
                raise ValueError('tight mark lies in a preparation port')
            part &= values[q] if pattern >> j & 1 else total ^ values[q]
        parts.append(part)
    if sum(p.bit_count() for p in parts) != 1 << k:
        raise ValueError('original cube partition incomplete')
    return parts


def compose(values, parts, function, dead):
    following = list(values)
    for q, column in zip(dead, function):
        result = 0
        while column:
            flag = column & -column
            result |= parts[flag.bit_length() - 1]
            column -= flag
        following[q] = result
    return following


def cut_witness(record, values, full, ranks):
    k = 13 - (record[0] | record[1]).bit_count()
    if record[4] + record[5] != 44 - SIZE[k]:
        return None
    free = [q for q in range(13) if not isinstance(values[q], str)]
    for q in free:
        difference = full[q] ^ ranks[q]
        if not difference:
            continue
        if any((values[t] & ~values[q]) if t < q else (values[q] & ~values[t])
               for t in free if t != q):
            continue
        x = (difference & -difference).bit_length() - 1
        k = 13 - (record[0] | record[1]).bit_count()
        return {'kind': 'TIGHT_FREE_CUT', 'record': record, 'imported_size': SIZE[k],
                'physical_port': q, 'full_Boolean_witness': x,
                'actual_bit': full[q] >> x & 1, 'sorted_bit': ranks[q] >> x & 1}
    return None


def run(first, seconds_cap=30.0, state_cap=20000, reserve=False):
    started = time.monotonic()
    fixture = json.loads((PARENT / 'fixture.json').read_text())
    prefix = fixture['literal_parent_prefix'] + [list(first)]
    if fixture['first_LOW_merge'] != [1,2] or list(first) != [1,2]:
        raise ValueError('only the literal first LOW merge (1,2) is certified')
    low_data = s.analyze_family(13, prefix, 2, 0)
    high_data = s.analyze_family(13, prefix, 0, 2)
    live = sorted({q for row in low_data['envelope'] for q in range(1, 13)
                   if row[0] >> q & 1})
    dead = tuple(q for q in range(1, 11) if q not in live)
    if len(dead) != 6 or low_data['summary']['ordinary_mass'] != 448 or high_data['summary']['ordinary_mass'] != 512:
        raise ValueError('new one-prior inventory differs')
    full = list(s.truth_columns(13))
    for a, b in prefix:
        full[a], full[b] = full[a] & full[b], full[a] | full[b]
    full_parts = partition(full, 13, dead)
    ranks = [sum(1 << x for x in range(8192) if x.bit_count() >= 13 - q) for q in range(13)]
    rows = []
    reserve_rows = []
    all_records = []
    for low, high in originals():
        record, values = original_profile(prefix, low, high)
        all_records.append(record)
        k = 13 - (low | high).bit_count()
        if record[4] + record[5] > 44 - SIZE[k]:
            raise ValueError('new literal root already directly negative')
        reserved_port = None
        if reserve and record[4] + record[5] == 43 - SIZE[k]:
            marked_mask = record[2] | record[3]
            if not any(marked_mask >> q & 1 for q in dead):
                reserved_port = next((q for q in range(13) if marked_mask >> q & 1 and full[q] != ranks[q]), None)
        if record[4] + record[5] == 44 - SIZE[k] or reserved_port is not None:
            parts = partition(values, k, dead)
            image = sum(1 << x for x, p in enumerate(parts) if p)
            rows.append((record, values, parts, image))
            if reserved_port is not None:
                difference = full[reserved_port] ^ ranks[reserved_port]
                x = (difference & -difference).bit_length() - 1
                reserve_rows.append({'record': record, 'physical_port': reserved_port,
                                     'full_Boolean_witness': x,
                                     'actual_bit': full[reserved_port] >> x & 1,
                                     'sorted_bit': ranks[reserved_port] >> x & 1})
    activity = sorted({r[3] for r in rows})
    states = [tuple(s.truth_columns(6))]
    words = [[]]
    seen = {states[0]: 0}
    edges, blocked = [], []
    cursor = 0
    status = 'COMPLETE'
    while cursor < len(states):
        if len(states) > state_cap or time.monotonic() - started > seconds_cap:
            status = 'INCOMPLETE_OPERATIONAL_STATE_CAP' if len(states) > state_cap else 'INCOMPLETE_OPERATIONAL_TIME_CAP'
            break
        function = states[cursor]
        after_full = compose(full, full_parts, function, dead)
        obstruction = None
        for record, values, parts, _ in rows:
            after = compose(values, parts, function, dead)
            obstruction = cut_witness(record, after, after_full, ranks)
            if obstruction is not None:
                break
        if obstruction is not None:
            blocked.append({'state_id': cursor, 'witness': obstruction})
        else:
            for a, b in combinations(range(6), 2):
                swaps = function[a] & ~function[b]
                if any(not (swaps & image) for image in activity):
                    continue
                after = list(function)
                after[a], after[b] = function[a] & function[b], function[a] | function[b]
                after = tuple(after)
                if after not in seen:
                    seen[after] = len(states)
                    states.append(after)
                    words.append(words[cursor] + [[dead[a], dead[b]]])
                edges.append([cursor, [dead[a], dead[b]], seen[after]])
        cursor += 1
    result = {'first_LOW_merge': list(first), 'literal_prefix': prefix, 'prefix_sha256': digest(prefix),
              'dead_ports': list(dead), 'low_envelope': low_data['envelope'], 'high_envelope': high_data['envelope'],
              'tight_records': [r[0] for r in rows if r[0][4]+r[0][5] == 44-SIZE[13-(r[0][0]|r[0][1]).bit_count()]],
              'activity_records': [r[0] for r in rows], 'repair_reserved_originals': reserve_rows,
              'all_original_records_sha256': digest(all_records),
              'activity_image_masks': activity, 'tight_original_domains': len(rows)-len(reserve_rows),
              'repair_reserved_original_domains': len(reserve_rows),
              'distinct_activity_images': len(activity), 'function_states': len(states),
              'admissible_edges': len(edges), 'blocked_functions': len(blocked),
              'unblocked_functions': cursor - len(blocked), 'unprocessed_functions': len(states) - cursor,
              'maximum_shortest_representative': max(map(len, words)),
              'representative_length_histogram': dict(sorted(Counter(map(len, words)).items())),
              'closure_cursor': cursor, 'complete_closure': cursor == len(states), 'status': status,
              'states': [{'id': i, 'full64_function': list(f), 'shortest_word': words[i]} for i, f in enumerate(states)],
              'transitions': edges, 'blocked': blocked,
              'guard': {'seconds': seconds_cap, 'states': state_cap},
              'seconds': time.monotonic() - started, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Necessary SIX-input preparation cover only; no head/tail or whole-target exclusion.'}
    return {'schema': 'native-HIGH3-one-LOW-six-preparation-v1',
            'agent': 'six-sorting-2', 'role': 'researcher', 'n': 13, 'size_budget': 44,
            'ancestral_profile_sha256': PROFILE_SHA,
            'fixture_sha256': hashlib.sha256((PARENT/'fixture.json').read_bytes()).hexdigest(), 'result': result}


def compact(certificate):
    r = certificate['result']
    witnesses, index, bindings = [], {}, []
    for b in r['blocked']:
        key = json.dumps(b['witness'], separators=(',', ':'), sort_keys=True)
        if key not in index:
            index[key] = len(witnesses)
            witnesses.append(b['witness'])
        bindings.append([b['state_id'], index[key]])
    lengths = [len(s['shortest_word']) for s in r['states']]
    if not all(lengths[b] == lengths[a]+1 for a,g,b in r['transitions']):
        raise ValueError('actual-word grading is not established')
    blocked = {b['state_id'] for b in r['blocked']}
    return {'schema':'native-HIGH3-one-LOW-six-cover-compact-v1',
            'agent':'six-sorting-2','role':'researcher','n':13,'size_budget':44,
            'fixture_sha256':certificate['fixture_sha256'],
            'prefix_sha256':r['prefix_sha256'],'dead_ports':r['dead_ports'],
            'all_original_records_sha256':r['all_original_records_sha256'],
            'tight_original_domains':r['tight_original_domains'],
            'repair_reserved_original_domains':r['repair_reserved_original_domains'],
            'activity_image_masks':r['activity_image_masks'],
            'repair_reservations':r['repair_reserved_originals'],
            'full_function_columns_sha256':digest([s['full64_function'] for s in r['states']]),
            'full_function_words_sha256':digest([s['shortest_word'] for s in r['states']]),
            'entire_admissible_transitions_sha256':digest(r['transitions']),
            'function_states':r['function_states'],'admissible_edges':r['admissible_edges'],
            'blocked_functions':r['blocked_functions'],'retained_functions':r['unblocked_functions'],
            'maximum_shortest':max(lengths),
            'maximum_actual_retained_word':max(d for i,d in enumerate(lengths) if i not in blocked),
            'entire_edge_grading_raises_shortest_by_one':True,
            'full_graph_length_histogram':{str(k):v for k,v in sorted(Counter(lengths).items())},
            'retained_length_histogram':{str(k):v for k,v in sorted(Counter(d for i,d in enumerate(lengths) if i not in blocked).items())},
            'complete_closure':r['complete_closure'],
            'exit_bindings':bindings,'exit_witnesses':witnesses}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, help='Local scratch full-cover JSON, deliberately omitted from Git')
    parser.add_argument('--compact-output', help='Optional local compact reproduction, never overwrites checked source by default')
    args = parser.parse_args()
    started = time.monotonic()
    certificate = run((1,2), reserve=True)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(certificate,separators=(',',':'))+'\n')
    r = certificate['result']
    if not r['complete_closure']:
        raise SystemExit('OPERATIONAL_LIMIT_INCOMPLETE_CLOSURE: no mathematical exclusion')
    summary = compact(certificate)
    expected = json.loads((PARENT/'certificate.json').read_text())
    if summary != expected:
        raise ValueError('entire compact certificate reproduction differs')
    raw = (json.dumps(summary,separators=(',',':'))+'\n').encode()
    if args.compact_output:
        Path(args.compact_output).write_bytes(raw)
    print(json.dumps({'agent':'six-sorting-2','role':'researcher',
                     'status':'COMPLETE_SIX_INPUT_REPAIR_RESERVED_PREPARATION_COVER',
                     'compact_certificate_sha256':hashlib.sha256(raw).hexdigest(),
                     'function_states':r['function_states'],'exits':r['blocked_functions'],
                     'retained':r['unblocked_functions'],'edges':r['admissible_edges'],
                     'maximum_actual_retained_word':summary['maximum_actual_retained_word'],
                     'seconds':time.monotonic()-started,
                     'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__ == '__main__':
    main()
