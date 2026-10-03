"""Separate scalar replay of a bounded disjoint singleton/balanced-tail interface.

Enumerates every legal cost-equal event order, groups full16-row functions,
replays original-cube identities/cuts and each complete global157-state target.
Does not import the packed producer. Passing is not a completion exclusion.
"""
from collections import Counter
from bindings import selected_offsets
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT
INPUT = ROOT / 'work'
OUT = ROOT / 'work'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def operations_allow():
    from controls import operations_allow as authorize
    authorize()


def gate(value, a, b):
    if value >> a & 1 and not (value >> b & 1):
        return value ^ (1 << a) ^ (1 << b)
    return value


def full_table(word, ports):
    indices = {p: i for i, p in enumerate(ports)}
    table = []
    for original in range(1 << len(ports)):
        value = original
        for a, b in word:
            value = gate(value, indices[a], indices[b])
        table.append(value)
    return tuple(table)


def tail_cover(classes):
    words = []
    controls = 0
    def visit(state, word):
        nonlocal controls
        if len(state) == 1:
            need(state == ((11, 9),) and len(word) == 3, 'Saturated tail root/cost differs')
            words.append(word)
            return
        for i, j in combinations(range(len(state)), 2):
            controls += 1
            a, da = state[i]
            b, db = state[j]
            if da != db:
                continue
            after = tuple(sorted([r for k, r in enumerate(state) if k not in (i, j)] + [(b, da+1)]))
            visit(after, word+[[a, b]])
    ports = sorted(p for p, cost in classes)
    visit(tuple(sorted(classes)), [])
    groups = {}
    for word in words:
        key = full_table(word, ports)
        groups.setdefault(key, []).append(word)
    need(len(words) == 6 and controls == 30 and len(groups) == 3 and
         sorted(map(len, groups.values())) == [2, 2, 2], 'Complete6-order/3-function tail cover differs')
    return groups, controls


def main():
    operations_allow()
    start = time.monotonic()
    deadline = start + 45
    branch, first, last = map(int, sys.argv[1:4])
    need(0 <= first < last and last-first <= 128, 'Require a bounded retained interval')
    p = json.loads((INPUT / f'branch{branch:02}.json').read_text())
    screen = json.loads((INPUT / f'cuts{branch:02}.json').read_text())
    front = json.loads((OUT / f'fronts{branch:02}-{first:05}-{last:05}.json').read_text())
    offsets, previous, universal, universal_ref = selected_offsets(first, last)
    ids = [screen['retained_function_ids'][i] for i in offsets]
    need(ids == front['retained_function_ids'] and offsets == front['processed_reserve_open_offsets'] and
         previous['finite_sha256'] == front['reserve_certificate_finite_sha256'], 'Original-open interval differs')
    need(digest(front['survivors']) == front['survivors_sha256'] and
         digest(front['rejections']) == front['rejections_sha256'], 'Front arrays differ')
    cache_record = json.loads((PUBLIC / 'work/two-prior-independent-original-cubes.json').read_text())
    cache = cache_record['scalar_cache']
    need(digest(cache) == cache_record['scalar_cache_sha256'] ==
         '105a51aade5e8409ba8c7487946c2fab80f819518d4e3758d2de503d6e90ae01', 'Independent base interface differs')
    states = [core for core, original, correct in cache['full_core_witnesses']]
    indices = {core: i for i, core in enumerate(states)}
    full_domains = dict(cache['original_LOW_domains'])
    domains = {lo: {indices[value & 1023] for value in values} for lo, values in full_domains.items()}
    need(len(states) == 157 and len(domains) == 39, 'Whole original image interface incomplete')
    live = {5: 6, 6: 6, 7: 6, 9: 6, 10: 6, 11: 7}
    initial = list(states)
    for a, b in p['HIGH_word']:
        need(a < b and live[a] == live[b], 'Nonstandard or unequal HIGH seed')
        del live[a]
        live[b] += 1
        initial = [gate(value, a-2, b-2) for value in initial]
    need(sorted(live.values()) == [6, 7, 7, 7], 'This is not a disjoint-pair route')
    dead = sorted(port for port in range(2, 12) if port not in live)
    need(dead == p['dead_preparation_ports'] == universal['dead_preparation_ports'] and
         cache['prefix'] + p['HIGH_word'] == universal['B23'] + universal['LOW_suffix'] + universal['prior_HIGH_merges'],
         'Full six-variable physical map or published universal literal differs')

    # Fresh independent reconstruction of the complete original HIGH(0,6)
    # cube used by10060. Numeric ranks2 and3 remain distinct throughout.
    original_high_seed = set()
    touched = active = 0
    seed_word = cache['prefix'] + p['HIGH_word']
    free_ports = [q for q in range(13) if q not in (0, 6)]
    for assignment in range(2048):
        row = [0]*13
        row[0], row[6] = 2, 3
        for j, port in enumerate(free_ports):
            row[port] = assignment >> j & 1
        actual_touched = 0
        for t, (a, b) in enumerate(seed_word):
            marked = row[a] > 1 or row[b] > 1
            actual_touched |= int(marked) << t
            if not marked and row[a] > row[b]:
                active |= 1 << t
            if row[a] > row[b]:
                row[a], row[b] = row[b], row[a]
        if assignment == 0:
            touched = actual_touched
        need(actual_touched == touched and touched.bit_count() == 7 and row[12] == 3 and
             [q for q in range(13) if row[q] == 2][0] in (6, 10),
             'Whole original HIGH cube seed cost or true marker ranks differ')
        original_high_seed.add(tuple(row))
    need(touched | active == (1 << 28)-1, 'Fresh original HIGH seed R is not zero')
    need(sorted({sum(row[port] << j for j, port in enumerate(dead))
                 for row in original_high_seed if row[11] == 0}) == [0,8,32,40],
         'Complete conditional original HIGH pattern set differs')

    def verify_public_original_cube(truth, single, tail):
        # Full truth replacement is legitimate on this original cube because
        # all six physical preparation ports hold unmarked Boolean values.
        for source in original_high_seed:
            row = list(source)
            pattern = sum(row[port] << j for j, port in enumerate(dead))
            output = truth[pattern]
            for j, port in enumerate(dead):
                row[port] = output >> j & 1
            hits = 0
            for t, (a, b) in enumerate([single]+tail):
                marked = row[a] > 1 or row[b] > 1
                hits += int(marked)
                if t == 2:
                    need(not marked and row[a] <= row[b],
                         'Reported middle tail gate is not a whole original unmarked identity')
                if row[a] > row[b]:
                    row[a], row[b] = row[b], row[a]
            need(hits == 2 and row[11:] == [2,3],
                 'Actual original cube does not reach D9 at physical11/12')
        # D=7+2, R>=1 and arbitrary-depth S11>=35 give45.
        need(7+2+1+35 == 45, 'Original pruning cost arithmetic differs')

    def inactive(values, event):
        a, b = event
        active = {i for i, value in enumerate(values) if (value >> (a-2) & 1) > (value >> (b-2) & 1)}
        return next((lo for lo, domain in domains.items() if not active & domain), None)

    def verify_reject(record, values, event, literal):
        lo = record['original_LOW_mask']
        need(lo in domains, 'Unknown original LOW cube')
        if record['kind'] == 'WHOLE_ORIGINAL_LOW_IDENTITY':
            a, b = event
            need(all((values[i] >> (a-2) & 1) <= (values[i] >> (b-2) & 1) for i in domains[lo]),
                 'Whole-cube identity proposal is false')
            return
        need(record['kind'] == 'TIGHT_ORIGINAL_LOW_FREE_PIVOT_CUT', 'Unknown rejection kind')
        port = record['pivot_port']
        need(2 <= port <= 11, 'Wrong free pivot label')
        conditional = set(full_domains[lo])
        for a, b in literal[len(cache['prefix']):]:
            need(any((value >> (a-2) & 1) > (value >> (b-2) & 1) for value in conditional),
                 'Cut prefix has an earlier unreported original identity')
            conditional = {gate(value, a-2, b-2) for value in conditional}
        pivot = port-2
        need(all(all((value >> q & 1) <= (value >> pivot & 1) for q in range(pivot)) and
                 all((value >> pivot & 1) <= (value >> q & 1) for q in range(pivot+1, 11))
                 for value in conditional), 'Original-space free-pivot inequalities fail')
        original = record['full_original_boolean_witness']
        row = original
        for a, b in literal:
            row = gate(row, a, b)
        need((row >> port & 1) != int(original.bit_count() >= 13-port), 'Reported wrong-rank witness is correct')

    heads, tails, surviving = {}, {}, {}
    for record in front['rejections']:
        key = (record['function_id'], tuple(record['singleton']))
        destination = heads if record['stage'] == 'HEAD' else tails
        if record['stage'] != 'HEAD':
            key += (record['tail_id'],)
        need(key not in destination, 'Repeated rejection')
        destination[key] = record
    for record in front['survivors']:
        key = (record['function_id'], tuple(record['singleton']), record['tail_id'])
        need(key not in surviving and key not in tails, 'Repeated or contradicting target')
        surviving[key] = record
    counts, metrics, budgets = Counter(), Counter(), Counter()
    covered_heads, covered_tails = set(), set()
    image_hashes, sizes, covers = [], [], set()
    for fid in ids:
        need(time.monotonic() < deadline, 'Incomplete45s scalar replay: no exclusion')
        operations_allow()
        f = p['functions'][fid]
        prep = f['shortest_word']
        need(all(a < b and a in dead and b in dead for a, b in prep), 'Nonstandard preparation word')
        truth = full_table(prep, dead)
        actual_output40 = truth[40]
        need(actual_output40.bit_count() == 2 and actual_output40 & 7 == 0,
             'Actual full64-row preparation conditional weight or leading zeros differs')
        full_columns = [sum((row >> j & 1) << i for i, row in enumerate(truth)) for j in range(6)]
        need(full_columns == f['full_six_variable_columns'], 'Full64-row preparation word differs')
        values = initial
        for a, b in prep:
            need(inactive(values, (a, b)) is None, 'Preparation representative inactive on an original cube')
            values = [gate(value, a-2, b-2) for value in values]
        counts['eligible_preparation_functions'] += 1
        high = next(port for port, cost in live.items() if cost == 6)
        for free in dead:
            single = sorted((high, free))
            hkey = (fid, tuple(single))
            counts['candidate_singleton_heads'] += 1
            literal_head = cache['prefix'] + p['HIGH_word'] + prep + [single]
            if hkey in heads:
                record = heads[hkey]
                verify_reject(record, values, single, literal_head)
                counts['head_' + record['kind']] += 1
                covered_heads.add(hkey)
                continue
            need(inactive(values, single) is None, 'Missing whole-cube head identity')
            head = [gate(value, single[0]-2, single[1]-2) for value in values]
            after = dict(live)
            del after[high]
            after[max(single)] = 7
            need(sorted(after.values()) == [7]*4 and sum(1 << cost for cost in after.values()) == 512,
                 'Whole HIGH cost/mass control differs')
            groups, controls = tail_cover(sorted(after.items()))
            covered_functions = set()
            metrics['legal_tail_orders'] += 6
            metrics['tail_event_controls'] += controls
            metrics['full_tail_function_rows'] += 3*16
            covers.add(digest(sorted(groups)))
            counts['active_uncut_singleton_heads'] += 1
            covered_heads.add(hkey)
            for tail_id in range(3):
                key = hkey + (tail_id,)
                need(key in tails or key in surviving, 'One necessary tail function is silently missing')
                record = tails[key] if key in tails else surviving[key]
                tail = record['HIGH_tail']
                table = full_table(tail, sorted(after))
                need(table in groups and table not in covered_functions and
                     tail == min(groups[table]), 'Tail is not a distinct full-function canonical representative')
                covered_functions.add(table)
                counts['candidate_complete_tail_functions'] += 1
                if key in tails and record['kind'] == 'PUBLIC_CONDITIONAL_MAXIMUM_OBSTRUCTION':
                    need(single == sorted((free, 7)) and
                         not (actual_output40 >> dead.index(free) & 1) and
                         tail == [[6,10],[max(7, free),11],[10,11]] and
                         record['zero_head_port'] == free and record['F40'] == actual_output40 and
                         record['moved_live_root'] == max(7, free) and
                         record['public_universal_graph_ref'] == universal_ref == front['public_universal_graph_ref'],
                         'Public10060 cut does not match actual full preparation, zero head or moved root')
                    verify_public_original_cube(truth, single, tail)
                    counts['tail_PUBLIC_CONDITIONAL_MAXIMUM_OBSTRUCTION'] += 1
                    covered_tails.add(key)
                    continue
                current = head
                for t, event in enumerate(tail):
                    if key in tails and record['tail_event_index'] == t:
                        verify_reject(record, current, event, literal_head + tail[:t+1])
                        counts['tail_' + record['kind']] += 1
                        break
                    need(inactive(current, event) is None, 'Unreported whole-cube tail identity')
                    current = [gate(value, event[0]-2, event[1]-2) for value in current]
                covered_tails.add(key)
                if key in tails:
                    continue
                need(all((value >> 9 & 1) == int(states[i].bit_count() >= 1) for i, value in enumerate(current)),
                     'Global157-state second-largest statistic differs')
                image = sorted({value & 511 for value in current})
                need(image == record['nine_core_states'] and digest(image) == record['nine_core_sha256'],
                     'Whole physical nine-core image differs')
                literal = literal_head + tail
                need(literal == record['prefix'] and digest(literal) == record['prefix_sha256'] and
                     len(literal) == record['prefix_length'] == 32+len(prep) and
                     record['remaining_gate_budget'] == 44-len(literal), 'Literal prefix/budget differs')
                need(record['global_port2_correct'] == all((value & 1) == int(states[i].bit_count() >= 10)
                                                          for i, value in enumerate(current)), 'Third-statistic flag differs')
                counts['surviving_complete_fronts'] += 1
                metrics['complete_scalar_core_inputs'] += 157
                image_hashes.append(record['nine_core_sha256'])
                sizes.append(len(image))
                budgets[record['remaining_gate_budget']] += 1
            need(covered_functions == set(groups), 'Full tail function cover incomplete')
    need(covered_heads.issuperset(heads) and covered_tails == set(tails) | set(surviving) and
         dict(counts) == front['census'], 'Candidate interval/census replay differs')
    finite = {'branch_index': branch, 'retained_interval': [first, last], 'retained_function_ids': ids,
              'processed_reserve_open_offsets': offsets, 'public_universal_graph_ref': universal_ref,
              'census': dict(counts), 'metrics': dict(metrics), 'producer_front_sha256': front['finite_sha256'],
              'complete_image_hashes_sha256': digest(image_hashes), 'tail_function_cover_hashes': sorted(covers),
              'front_image_size_range': [min(sizes, default=0), max(sizes, default=0)],
              'remaining_gate_budgets': dict(sorted(budgets.items()))}
    record = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'COMPLETE_BOUNDED_DISJOINT_PREPARATION_HEAD_TAIL_ORIGINAL_CUBE_IMAGE_REPLAY',
              'finite': finite, 'finite_sha256': digest(finite), 'seconds': time.monotonic()-start,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Exact recorded retained interval only; separate same-author check, no external review/branch exclusion.'}
    suffix = '-O' if not __debug__ else ''
    path = OUT / f'check{branch:02}-{first:05}-{last:05}{suffix}.json'
    path.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(record, sort_keys=True))


if __name__ == '__main__':
    main()
