"""Independent scalar original-cube and full64-row preparation-cover audit.

Imports no producer, profiler, packed primitive or probe. Every selected cut
is checked on its whole original free cube; graph closure uses row functions.
"""
from collections import deque
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

SOURCE = Path(__file__).resolve().parent
INPUT = None
DEAD = (2, 5, 6, 7, 9, 10)
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
    certificate = json.loads(INPUT.read_text())
    result = certificate['result']
    fixture = json.loads((SOURCE/'fixture.json').read_text())
    need(fixture['schema'] == 'native-HIGH3-one-LOW-six-fixture-v1' and fixture['n'] == 13 and fixture['size_budget'] == 44, 'fixture order or budget differs')
    need(fixture['imported_lower_bounds'] == {'11':35,'12':39}, 'fixture imported bounds differ')
    need(fixture['first_LOW_merge'] == [1,2] and fixture['dead_ports'] == list(DEAD) and fixture['held_ranks'] == [0,11,12], 'fixture support differs')
    expected_parent = [
        [0,11],[1,7],[2,4],[3,5],[8,9],[10,12],[0,2],[3,6],
        [4,12],[5,7],[8,10],[0,8],[1,3],[2,5],[4,9],[6,11],
        [7,12],[0,1],[2,10],[9,11],[11,12],[3,6],
        [6,7],[5,7],[9,10],[10,11],[7,11]]
    need(fixture['literal_parent_prefix'] == expected_parent, 'fixture parent prefix differs')
    need(digest(expected_parent) == fixture['parent_prefix_sha256'], 'fixture parent pin differs')
    prefix = expected_parent + [[1,2]]
    need(result['literal_prefix'] == prefix, 'literal prefix differs')
    need(digest(prefix) == result['prefix_sha256'], 'literal prefix differs')
    tight, ordinary, images = {}, {}, set()
    activity_records, reserved = [], []
    full = [bool_word(x,prefix) for x in range(8192)]
    original_assignments = 0
    all_records = []
    for count in (1,2):
        for ports in combinations(range(13), count):
            for selector in range(1 << count):
                low = sum(1 << q for j,q in enumerate(ports) if selector >> j & 1)
                high = sum(1 << q for j,q in enumerate(ports) if not selector >> j & 1)
                record, rows = domain(prefix, low, high)
                all_records.append(record)
                original_assignments += len(rows)
                need(record[4]+record[5] <= (5 if count == 1 else 9), 'original root exceeds budget')
                if count == 2 and (low == 0 or high == 0):
                    family = 'HIGH' if low == 0 else 'LOW'
                    mask = record[3] if low == 0 else record[2]
                    ordinary[family,mask] = max(ordinary.get((family,mask), -1), record[4])
                cost = record[4]+record[5]
                marked_mask = record[2]|record[3]
                reserve_port = None
                if cost == (4 if count == 1 else 8) and all(not (marked_mask >> q & 1) for q in DEAD):
                    reserve_port = next((q for q in range(13) if marked_mask >> q & 1 and
                                         any((y >> q & 1) != int(x.bit_count() >= 13-q) for x,y in enumerate(full))), None)
                if cost != (5 if count == 1 else 9) and reserve_port is None:
                    continue
                need(all(0 <= row[q] <= 1 for row in rows for q in DEAD), 'activity mark lies in dead ports')
                image = {sum(row[q] << j for j,q in enumerate(DEAD)) for row in rows}
                activity_records.append(record)
                images.add(sum(1 << x for x in image))
                if cost == (5 if count == 1 else 9):
                    tight[low,high] = (record,rows)
                if reserve_port is not None:
                    q = reserve_port
                    x = next(x for x,y in enumerate(full) if (y >> q & 1) != int(x.bit_count() >= 13-q))
                    reserved.append({'record':record,'physical_port':q,'full_Boolean_witness':x,
                                     'actual_bit':full[x] >> q & 1,'sorted_bit':int(x.bit_count() >= 13-q)})
    low_profile = sorted([[(mask^1).bit_length()-1,cost] for (family,mask),cost in ordinary.items() if family == 'LOW'])
    high_profile = sorted([[(mask^(1<<12)).bit_length()-1,cost] for (family,mask),cost in ordinary.items() if family == 'HIGH'])
    need(low_profile == [[1,8],[3,6],[4,6],[8,6]] and high_profile == [[11,9]], 'new ordinary inventories differ')
    need(digest(all_records) == result['all_original_records_sha256'], 'all actual original records differ')
    need([tight[key][0] for key in tight] == result['tight_records'], 'tight original records differ')
    need(activity_records == result['activity_records'], 'entire original activity records differ')
    need(reserved == result['repair_reserved_originals'], 'entire mandatory repair reservations differ')
    need(result['repair_reserved_original_domains'] == len(reserved), 'mandatory repair reservation count differs')
    full = [bool_word(x,prefix) for x in range(8192)]
    need(all((y >> q & 1) == int(x.bit_count() >= 13-q) for x,y in enumerate(full) for q in (0,11,12)), 'held full ranks differ')
    return {'prefix':prefix, 'target':{'prefix_sha256':digest(prefix)}, 'tight':tight,
            'activity':sorted(images), 'full':full, 'original_assignments':original_assignments, 'reserved_originals':len(reserved), 'repair_reservations':reserved, 'activity_records':activity_records}


def row_function(columns):
    need(len(columns) == 6 and all(type(c) is int and 0 <= c < (1 << 64) for c in columns), 'invalid function column')
    return tuple(sum((columns[j] >> x & 1) << j for j in range(6)) for x in range(64))


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
    need(certificate['schema'] == 'native-HIGH3-one-LOW-six-preparation-v1' and certificate['n'] == 13 and certificate['size_budget'] == 44, 'certificate schema or budget differs')
    need(result['first_LOW_merge'] == [1,2], 'wrong first LOW merge')
    need(result['prefix_sha256'] == context['target']['prefix_sha256'], 'wrong prefix pin')
    need(result['dead_ports'] == list(DEAD), 'wrong dead ports')
    need(certificate['fixture_sha256'] == hashlib.sha256((SOURCE/'fixture.json').read_bytes()).hexdigest(), 'full cover fixture binding differs')
    need(result['repair_reserved_originals'] == context['repair_reservations'] and result['activity_records'] == context['activity_records'], 'original repair/activity rows differ')
    need(result['repair_reserved_original_domains'] == context['reserved_originals'], 'original repair row count differs')
    need(result['tight_original_domains'] == len(context['tight']), 'tight original domain count differs')
    need(result['activity_image_masks'] == context['activity'], 'original activity images differ')
    entries = result['states']
    need([s['id'] for s in entries] == list(range(len(entries))), 'missing or duplicate function state')
    tables = [row_function(s['full64_function']) for s in entries]
    need(len(set(tables)) == len(tables), 'duplicate full function')
    pairs = list(combinations(range(6), 2))
    for s, table in zip(entries, tables):
        word = s['shortest_word']
        need(all(a in DEAD and b in DEAD and a < b for a, b in word), 'invalid representative gate')
        local = [(DEAD.index(a), DEAD.index(b)) for a, b in word]
        need(tuple(bool_word(x, local) for x in range(64)) == table, 'representative whole function differs')
    blocked = set()
    for b in result['blocked']:
        i = b['state_id']
        need(type(i) is int and 0 <= i < len(tables) and i not in blocked, 'duplicate or invalid blocked function')
        blocked.add(i)
    blocked_tables = {tables[i] for i in blocked}
    identity = tuple(range(64))
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
    need(all(distances[after] == distances[before]+1 for before,gate,after in transitions), 'edge grading differs')
    for b in result['blocked']:
        i = b['state_id']
        check_cut(b,tables[i],entries[i]['shortest_word'],context)
    retained_actual_max = max(distances[table] for table in tables if table not in blocked_tables)
    return {'function_states': len(tables), 'admissible_edges': len(transitions), 'blocked': len(blocked),
            'retained': len(tables) - len(blocked), 'maximum_shortest': max(distances.values()),
            'mandatory_repair_originals':context['reserved_originals'],
            'maximum_actual_retained_word': retained_actual_max, 'entire_edge_grading_verified': True,
            'original_profile_assignments': context['original_assignments'],
            'selected_cut_assignments': sum(len(context['tight'][tuple(b['witness']['record'][:2])][1])
                                             for b in result['blocked']),
            'full_original_Boolean_assignments': 8192,
            'complete_representative_function_assignments': 64 * len(tables)}



def compact_binding(certificate):
    r = certificate['result']
    catalog, mapping, bindings = [], {}, []
    for entry in r['blocked']:
        w = entry['witness']
        key = json.dumps(w,sort_keys=True,separators=(',',':'))
        if key not in mapping:
            mapping[key] = len(catalog)
            catalog.append(w)
        bindings.append([entry['state_id'],mapping[key]])
    lengths = [len(s['shortest_word']) for s in r['states']]
    blocked = {b['state_id'] for b in r['blocked']}
    from collections import Counter
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
            'exit_bindings':bindings,'exit_witnesses':catalog}


def check_compact(certificate, expected):
    need(compact_binding(certificate) == expected, 'compact mathematical binding differs')


def positive_controls():
    fixture = json.loads((SOURCE/'fixture.json').read_text())
    word = fixture['positive_six_sorter']
    need(len(word) == 12 and all(0 <= a < b < 6 for a,b in word), 'invalid positive six sorter')
    need(all(bool_word(x,word) == ((1 << x.bit_count())-1) << (6-x.bit_count()) for x in range(64)), 'positive six sorter fails')
    return {'six_sorter_gates':12,'six_sorter_Boolean_inputs':64}


def main():
    global INPUT
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',required=True)
    args = parser.parse_args()
    INPUT = Path(args.input)
    started = time.monotonic()
    certificate = json.loads(INPUT.read_text())
    expected = json.loads((SOURCE/'certificate.json').read_text())
    check_compact(certificate,expected)
    context = make_context()
    metrics = verify(certificate,context)
    controls = positive_controls()
    print(json.dumps({'agent':'six-sorting-2','role':'researcher',
                      'status':'WHOLE_ORIGINAL_CUBES_FULL64_FUNCTIONS_ALL_EDGES_EXITS_AND_ACTUAL_LENGTH_VERIFIED',
                      'metrics':metrics,'positive_controls':controls,
                      'compact_certificate_sha256':hashlib.sha256((SOURCE/'certificate.json').read_bytes()).hexdigest(),
                      'seconds':time.monotonic()-started,
                      'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'trust':'Separate same-author scalar numeric algorithm; unformalized bridges and independent-person review pending.'},sort_keys=True))


if __name__ == '__main__':
    main()
