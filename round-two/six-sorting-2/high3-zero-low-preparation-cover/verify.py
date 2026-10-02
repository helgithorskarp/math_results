"""Independent scalar original-cube and full32-row preparation-cover audit.

Imports no producer, profiler, packed primitive or probe. Every selected cut
is checked on its whole original free cube; graph closure uses row functions.
"""
from collections import deque
import copy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

SOURCE = Path(__file__).resolve().parent
DEAD = (5, 6, 7, 9, 10)
DEAD_MASK = sum(1 << q for q in DEAD)


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def bool_word(x, word):
    for a, b in word:
        if x >> a & 1 and not x >> b & 1:
            x ^= (1 << a) | (1 << b)
    return x


def domain(prefix, low, high):
    lows = [q for q in range(13) if low >> q & 1]
    highs = [q for q in range(13) if high >> q & 1]
    free = [q for q in range(13) if not (low | high) >> q & 1]
    base = [0] * 13
    for j, q in enumerate(lows):
        base[q] = j - len(lows)
    for j, q in enumerate(highs):
        base[q] = 2 + j
    rows = []
    hits = None
    output_tags = None
    inversions = 0
    for x in range(1 << len(free)):
        values = list(base)
        for j, q in enumerate(free):
            values[q] = x >> j & 1
        touched = 0
        for t, (a, b) in enumerate(prefix):
            u, v = values[a], values[b]
            marked = u < 0 or u > 1 or v < 0 or v > 1
            if marked:
                touched |= 1 << t
            elif u > v:
                inversions |= 1 << t
            if u > v:
                values[a], values[b] = v, u
        tags = (sum(1 << q for q, v in enumerate(values) if v < 0),
                sum(1 << q for q, v in enumerate(values) if v > 1))
        if hits is None:
            hits, output_tags = touched, tags
        need(touched == hits and tags == output_tags, 'original-domain marked routes depend on free assignment')
        rows.append(values)
    identities = ((1 << len(prefix)) - 1) & ~(hits | inversions)
    return [low, high, *output_tags, hits.bit_count(), identities.bit_count(), identities], rows


def make_context():
    fixture = json.loads((SOURCE / 'fixture.json').read_text())
    target = fixture['target_metadata']
    prefix = fixture['literal_prefix']
    need(fixture['n'] == 13 and fixture['size_budget'] == 44 and fixture['imported_lower_bounds'] == {'11': 35, '12': 39}, 'fixture size or imported bounds differ')
    need(digest(prefix) == target['prefix_sha256'], 'literal prefix differs')
    tight = {}
    ordinary = {}
    images = set()
    original_assignments = 0
    for r in (1, 2):
        for low_count in range(r + 1):
            for lows in combinations(range(13), low_count):
                rest = [q for q in range(13) if q not in lows]
                for highs in combinations(rest, r - low_count):
                    low, high = sum(1 << q for q in lows), sum(1 << q for q in highs)
                    record, rows = domain(prefix, low, high)
                    original_assignments += len(rows)
                    if r == 2 and (low == 0 or high == 0):
                        family = 'HIGH' if low == 0 else 'LOW'
                        mask = record[3] if low == 0 else record[2]
                        ordinary[family, mask] = max(ordinary.get((family, mask), -1), record[4])
                    if record[4] + record[5] != (5 if r == 1 else 9):
                        continue
                    need(all(0 <= row[q] <= 1 for row in rows for q in DEAD), 'tight mark lies in dead ports')
                    image = {sum(row[q] << j for j, q in enumerate(DEAD)) for row in rows}
                    tight[low, high] = (record, rows)
                    images.add(sum(1 << x for x in image))
    low_profile = sorted([[((mask ^ 1).bit_length() - 1), cost] for (family, mask), cost in ordinary.items() if family == 'LOW'])
    high_profile = sorted([[((mask ^ (1 << 12)).bit_length() - 1), cost] for (family, mask), cost in ordinary.items() if family == 'HIGH'])
    need(low_profile == fixture['ordinary_LOW_secondary_profile'] and high_profile == fixture['ordinary_HIGH_secondary_profile'], 'ordinary inventories differ')
    need(all(bool_word(x, fixture['positive_five_sorter']) == ((1 << x.bit_count()) - 1) << (5 - x.bit_count()) for x in range(32)), 'positive five sorter fails')
    full = [bool_word(x, prefix) for x in range(8192)]
    core_image = sorted({(y >> 1) & 1023 for y in full})
    need(core_image == fixture['parent_core_states'], 'complete parent core image differs')
    need(all((y >> q & 1) == int(x.bit_count() >= 13 - q)
             for x, y in enumerate(full) for q in (0, 11, 12)), 'held full ranks differ')
    return {'prefix': prefix, 'target': target, 'tight': tight, 'activity': sorted(images),
            'full': full, 'original_assignments': original_assignments}


def row_function(columns):
    need(len(columns) == 5 and all(type(c) is int and 0 <= c < (1 << 32) for c in columns), 'invalid function column')
    return tuple(sum((columns[j] >> x & 1) << j for j in range(5)) for x in range(32))


def check_cut(entry, state, word, context):
    witness = entry['witness']
    need(witness['kind'] == 'TIGHT_FREE_CUT', 'wrong obstruction kind')
    record = witness['record']
    key = tuple(record[:2])
    need(key in context['tight'], 'selected original is not tight')
    actual, rows = context['tight'][key]
    need(record == actual, 'selected original record differs')
    need(witness['imported_size'] == (39 if (key[0] | key[1]).bit_count() == 1 else 35), 'wrong imported size')
    q = witness['physical_port']
    need(0 <= q < 13 and not (record[2] | record[3]) >> q & 1, 'selected cut port is marked')
    free = [t for t in range(13) if not (record[2] | record[3]) >> t & 1]
    for row in rows:
        pattern = sum(row[t] << j for j, t in enumerate(DEAD))
        result = list(row)
        for j, t in enumerate(DEAD):
            result[t] = state[pattern] >> j & 1
        need(all(result[t] <= result[q] if t < q else result[q] <= result[t]
                 for t in free if t != q), 'whole original cut inequality fails')
    x = witness['full_Boolean_witness']
    need(type(x) is int and 0 <= x < 8192, 'invalid full Boolean witness')
    y = bool_word(context['full'][x], word)
    actual_bit, sorted_bit = y >> q & 1, int(x.bit_count() >= 13 - q)
    need(actual_bit != sorted_bit and actual_bit == witness['actual_bit'] and sorted_bit == witness['sorted_bit'],
         'full wrong-rank witness differs')


def verify(certificate, context):
    result = certificate['result']
    need(certificate['schema'] == 'native-HIGH3-zero-LOW-preparation-cover-v1' and certificate['n'] == 13 and certificate['size_budget'] == 44, 'certificate schema or budget differs')
    need(certificate['fixture_sha256'] == hashlib.sha256((SOURCE / 'fixture.json').read_bytes()).hexdigest(), 'certificate fixture differs')
    need(result['side'] == 'HIGH' and result['genealogy'] == 3 and result['root_id'] == 12, 'wrong target')
    need(result['prefix_sha256'] == context['target']['prefix_sha256'], 'wrong prefix pin')
    need(result['dead_ports'] == list(DEAD), 'wrong dead ports')
    need(result['tight_original_domains'] == len(context['tight']), 'tight original domain count differs')
    need(result['activity_image_masks'] == context['activity'], 'original activity images differ')
    entries = result['states']
    need([s['id'] for s in entries] == list(range(len(entries))), 'missing or duplicate function state')
    tables = [row_function(s['full32_function']) for s in entries]
    need(len(set(tables)) == len(tables), 'duplicate full function')
    pairs = list(combinations(range(5), 2))
    for s, table in zip(entries, tables):
        word = s['shortest_word']
        need(all(a in DEAD and b in DEAD and a < b for a, b in word), 'invalid representative gate')
        local = [(DEAD.index(a), DEAD.index(b)) for a, b in word]
        need(tuple(bool_word(x, local) for x in range(32)) == table, 'representative whole function differs')
    blocked = set()
    for b in result['blocked']:
        i = b['state_id']
        need(type(i) is int and 0 <= i < len(tables) and i not in blocked, 'duplicate or invalid blocked function')
        check_cut(b, tables[i], entries[i]['shortest_word'], context)
        blocked.add(i)
    blocked_tables = {tables[i] for i in blocked}
    identity = tuple(range(32))
    distances = {identity: 0}
    todo = deque([identity])
    transitions = set()
    while todo:
        table = todo.popleft()
        if table in blocked_tables:
            continue
        for a, b in pairs:
            swap_inputs = sum(1 << x for x, y in enumerate(table) if y >> a & 1 and not y >> b & 1)
            if any(not (swap_inputs & image) for image in context['activity']):
                continue
            after = tuple(y ^ ((1 << a) | (1 << b)) if y >> a & 1 and not y >> b & 1 else y for y in table)
            transitions.add((table, (DEAD[a], DEAD[b]), after))
            if after not in distances:
                distances[after] = distances[table] + 1
                todo.append(after)
    need(set(distances) == set(tables), 'whole function closure differs')
    stored_edges = set()
    for a, gate, b in result['transitions']:
        need(type(a) is int and type(b) is int and 0 <= a < len(tables) and 0 <= b < len(tables), 'invalid transition state')
        stored_edges.add((tables[a], tuple(gate), tables[b]))
    need(len(stored_edges) == len(result['transitions']) and stored_edges == transitions, 'entire admissible edge set differs')
    need(all(distances[table] == len(entry['shortest_word']) for table, entry in zip(tables, entries)),
         'representative shortest length differs')
    need(result['complete_closure'] is True and result['closure_cursor'] == len(tables), 'incomplete closure')
    need(result['function_states'] == len(tables) and result['admissible_edges'] == len(transitions), 'closure counts differ')
    need(result['blocked_functions'] == len(blocked) and result['unblocked_functions'] == len(tables) - len(blocked),
         'blocked counts differ')
    need(result['maximum_shortest_representative'] == max(distances.values()), 'maximum representative differs')
    return {'function_states': len(tables), 'admissible_edges': len(transitions), 'blocked': len(blocked),
            'retained': len(tables) - len(blocked), 'maximum_shortest': max(distances.values()),
            'original_profile_assignments': context['original_assignments'],
            'selected_cut_assignments': sum(len(context['tight'][tuple(b['witness']['record'][:2])][1])
                                             for b in result['blocked']),
            'full_original_Boolean_assignments': 8192,
            'complete_representative_function_assignments': 32 * len(tables)}


def damages(certificate, context):
    rejected = []
    mutations = []
    def change(label, callback, reason):
        damaged = copy.deepcopy(certificate)
        callback(damaged['result'])
        mutations.append((label, damaged, reason))
    change('prefix pin', lambda r: r.update(prefix_sha256='0' * 64), 'wrong prefix pin')
    change('activity image', lambda r: r['activity_image_masks'].__setitem__(0, r['activity_image_masks'][0] ^ 1),
           'original activity images differ')
    change('whole function', lambda r: r['states'][1]['full32_function'].__setitem__(0, r['states'][1]['full32_function'][0] ^ 1),
           'representative whole function differs')
    change('missing state', lambda r: r['states'].pop(1), 'missing or duplicate function state')
    change('extra leading identity in representative', lambda r: r['states'][1]['shortest_word'].append(r['states'][1]['shortest_word'][-1]),
           'representative shortest length differs')
    change('original deletion count', lambda r: r['blocked'][0]['witness']['record'].__setitem__(4, 8),
           'selected original record differs')
    change('marked cut port', lambda r: r['blocked'][0]['witness'].update(physical_port=12), 'selected cut port is marked')
    change('full rank witness', lambda r: r['blocked'][0]['witness'].update(full_Boolean_witness=0), 'full wrong-rank witness differs')
    change('missing admissible edge', lambda r: r['transitions'].pop(), 'entire admissible edge set differs')
    change('incomplete closure', lambda r: r.update(complete_closure=False), 'incomplete closure')
    for label, damaged, reason in mutations:
        try:
            verify(damaged, context)
        except ValueError as error:
            need(str(error) == reason, 'damage rejected for unintended reason: ' + label + ': ' + str(error))
            rejected.append(label)
        else:
            raise ValueError('damage unexpectedly accepted: ' + label)
    return rejected


def main():
    start = time.monotonic()
    certificate = json.loads((SOURCE / 'certificate.json').read_text())
    context = make_context()
    metrics = verify(certificate, context)
    rejected = damages(certificate, context)
    output = {'agent': 'six-sorting-2', 'role': 'researcher',
              'status': 'WHOLE_ORIGINAL_CUBES_AND_FULL_FUNCTION_CLOSURE_VERIFIED', 'metrics': metrics,
              'damages_rejected_for_intended_reasons': rejected, 'seconds': time.monotonic() - start,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'trust': 'Separate same-author numeric algorithm; unformalized bridges, external review pending.'}
    print(json.dumps(output, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
