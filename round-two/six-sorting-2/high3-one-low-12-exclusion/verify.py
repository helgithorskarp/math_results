"""Independent scalar check of HIGH3 one-prior-LOW (1,2) head/tail certificates.

No producer/profiler imports. Complete numeric original cubes retain distinct
extreme ranks. Full six-output functions and all equal-merge orders are
checked as row functions. Caches only reuse already identical literal fronts.
"""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'high3-one-low-preparation-cover'
FULL_GRAPH = ROOT / 'generated/preparation.json'
DEAD = (2, 5, 6, 7, 9, 10)
LOW = (3, 4, 8)
FLOORS = {9: 25, 11: 35, 12: 39}
PARENT_HASH = 'a9dbfd3ce5419b6ad1053f0650943d76724c8acfb83c734ccc930cadc129ee36'
PREFIX_HASH = 'b1f9baeb79b1617e326aa8433c3c80988e1cf2e30292c90c07fe1650fb447e00'


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def bool_word(x, word):
    for a, b in word:
        if x >> a & 1 and not x >> b & 1:
            x ^= (1 << a) | (1 << b)
    return x


def valid_word(word, support=range(13)):
    need(isinstance(word, list) and all(isinstance(g, list) and len(g) == 2 and
         all(type(q) is int and q in support for q in g) and g[0] < g[1] for g in word), 'nonstandard gate')


def check_state(s):
    word = s['shortest_word']
    valid_word(word, DEAD)
    need(len(word) <= 8, 'retained shortest bound exceeds eight')
    local = [[DEAD.index(a), DEAD.index(b)] for a, b in word]
    actual = [sum(((bool_word(x, local) >> j) & 1) << x for x in range(64)) for j in range(6)]
    need(actual == s['full64_function'], 'retained full function differs')
    return word


def fresh_domain(lo, hi):
    need(type(lo) is int and type(hi) is int and 0 <= lo < 8192 and 0 <= hi < 8192 and not lo & hi, 'invalid original masks')
    lows = [q for q in range(13) if lo >> q & 1]
    highs = [q for q in range(13) if hi >> q & 1]
    free = [q for q in range(13) if not (lo | hi) >> q & 1]
    base = [0] * 13
    for j, q in enumerate(lows):
        base[q] = j - len(lows)
    for j, q in enumerate(highs):
        base[q] = j + 2
    rows = []
    for x in range(1 << len(free)):
        v = list(base)
        for j, q in enumerate(free):
            v[q] = x >> j & 1
        rows.append(v)
    return [lo, hi, lo, hi, 0, 0, 0], rows


def follow(domain, word, start):
    old, rows = domain
    result = []
    touch_mask = None
    tags = None
    active_mask = 0
    for old_row in rows:
        v = list(old_row)
        touches = 0
        for t, (a, b) in enumerate(word):
            u, w = v[a], v[b]
            if u < 0 or u > 1 or w < 0 or w > 1:
                touches |= 1 << t
            elif u > w:
                active_mask |= 1 << t
            if u > w:
                v[a], v[b] = w, u
        current = (sum(1 << q for q, w in enumerate(v) if w < 0),
                   sum(1 << q for q, w in enumerate(v) if w > 1))
        if touch_mask is None:
            touch_mask, tags = touches, current
        need(touches == touch_mask and current == tags, 'marked route varies over original cube')
        result.append(v)
    identities = ((1 << len(word)) - 1) & ~(touch_mask | active_mask)
    return [old[0], old[1], *tags, old[4] + touch_mask.bit_count(),
            old[5] + identities.bit_count(), old[6] | (identities << start)], result


def all_equal_tails(costs, word=()):
    if len(costs) == 1:
        yield [list(g) for g in word]
        return
    for a, b in combinations(sorted(costs), 2):
        if costs[a] != costs[b]:
            continue
        after = dict(costs)
        after[a] += 1
        del after[b]
        yield from all_equal_tails(after, word + ((a, b),))


def canonical_tails(selected, partner):
    # Complete recursion on labelled live costs, with no word/depth bound.
    root = min(selected, partner)
    initial = {1: 8, root: 7}
    initial.update({q: 6 for q in LOW if q != selected})
    support = sorted(initial)
    orders = list(all_equal_tails(initial))
    need(len(orders) == 1 and len(orders[0]) == 3,
         'unique equal-tail event enumeration differs')
    w = orders[0]
    local = [[support.index(a), support.index(b)] for a, b in w]
    table = tuple(bool_word(x, local) for x in range(16))
    need(all(table[x] & 1 == int(x == 15) for x in range(16)),
         'tail fails whole four-input minimum')
    return [w]


class Context:
    def __init__(self, parent_root=PARENT, full_graph=FULL_GRAPH):
        raw = (parent_root / 'certificate.json').read_bytes()
        need(hashlib.sha256(raw).hexdigest() == PARENT_HASH, 'parent certificate pin differs')
        compact = json.loads(raw)
        fixture = json.loads((parent_root / 'fixture.json').read_text())
        graph = json.loads(full_graph.read_text())['result']
        self.prefix = fixture['literal_parent_prefix'] + [fixture['first_LOW_merge']]
        valid_word(self.prefix)
        need(len(self.prefix) == 28 and digest(self.prefix) == PREFIX_HASH,
             'literal prefix pin differs')
        need(graph['literal_prefix'] == self.prefix and graph['dead_ports'] == list(DEAD),
             'whole function graph prefix/support differs')
        all_states = graph['states']
        need([s['id'] for s in all_states] == list(range(2335)),
             'complete function indexing differs')
        need(digest([s['full64_function'] for s in all_states]) == compact['full_function_columns_sha256'],
             'all full-function columns binding differs')
        need(digest([s['shortest_word'] for s in all_states]) == compact['full_function_words_sha256'],
             'all representative words binding differs')
        need(digest(graph['transitions']) == compact['entire_admissible_transitions_sha256'],
             'entire edge binding differs')
        blocked = {s for s, witness in compact['exit_bindings']}
        need(blocked == {b['state_id'] for b in graph['blocked']}
             and len(blocked) == 1206 and graph['complete_closure'] is True,
             'published complete exit partition differs')
        self.states = [s for s in all_states if s['id'] not in blocked]
        need(len(self.states) == 1129, 'parent retained cover differs')
        self.words = {}
        for s in self.states:
            self.words[s['id']] = check_state(s)
        self.full_parent = [bool_word(x, self.prefix) for x in range(8192)]
        need(all((y >> q & 1) == int(x.bit_count() >= 13 - q)
                 for x, y in enumerate(self.full_parent) for q in (0, 11, 12)),
             'whole parent held rank differs')
        need(all(min(y >> q & 1 for q in (1, 3, 4, 8)) == int(x.bit_count() >= 12)
                 for x, y in enumerate(self.full_parent)),
             'live LOW ports omit second minimum')
        self.tails = {(s, d): canonical_tails(s, d) for s in LOW for d in DEAD}
        self.base = {}
        self.prepared = {}
        self.headed = {}
        self.tailed = {}
        self.state = None
        self.assignments = Counter()
        self.kinds = Counter()

    def state_start(self, state):
        if self.state != state:
            self.prepared.clear()
            self.headed.clear()
            self.tailed.clear()
            self.state = state

    def domain(self, state, head, tail, lo, hi):
        self.state_start(state)
        origin = (lo, hi)
        if origin not in self.base:
            self.base[origin] = follow(fresh_domain(lo, hi), self.prefix, 0)
            self.assignments['base'] += len(self.base[origin][1])
        if origin not in self.prepared:
            self.prepared[origin] = follow(self.base[origin], self.words[state], 28)
            self.assignments['preparation'] += len(self.prepared[origin][1])
        selected, partner = LOW[head // 6], DEAD[head % 6]
        key = (head, origin)
        if key not in self.headed:
            self.headed[key] = follow(self.prepared[origin], [sorted([selected, partner])], 28 + len(self.words[state]))
            self.assignments['head'] += len(self.headed[key][1])
        if tail is None:
            return self.headed[key]
        key = (head, tail, origin)
        if key not in self.tailed:
            self.tailed[key] = follow(self.headed[(head, origin)], self.tails[selected, partner][tail], 29 + len(self.words[state]))
            self.assignments['tail'] += len(self.tailed[key][1])
        return self.tailed[key]

    def extension(self, state, head, tail):
        selected, partner = LOW[head // 6], DEAD[head % 6]
        return self.words[state] + [sorted([selected, partner])] + ([] if tail is None else self.tails[selected, partner][tail])


def check_witness(witness, state, head, tail, context):
    kind = witness['kind']
    need(kind in ('DIRECT_COST', 'TIGHT_FREE_CUT', 'TIGHT_MARKED_PORT_LOCK', 'SEMANTIC_WEIGHTED_MASS'), 'invalid obstruction kind')
    records = witness['distinct_tag_witness_records'] if kind == 'SEMANTIC_WEIGHTED_MASS' else [witness['record']]
    need(isinstance(records, list) and len(records) > 0, 'empty original records')
    selected = []
    for record in records:
        need(isinstance(record, list) and len(record) == 7 and all(type(v) is int for v in record), 'invalid original record')
        lo, hi = record[:2]
        k = 13 - (lo | hi).bit_count()
        need(k in FLOORS and witness['imported_size'] == FLOORS[k], 'imported lower bound differs')
        actual, rows = context.domain(state, head, tail, lo, hi)
        need(actual == record, 'complete original D/R/tag/identity record differs')
        selected.append((actual, rows))
    if kind == 'DIRECT_COST':
        need(records[0][4] + records[0][5] + witness['imported_size'] > 44, 'direct original cost is not negative')
    elif kind == 'SEMANTIC_WEIGHTED_MASS':
        family = witness['original_counts']
        need(isinstance(family, list) and len(family) == 2 and all(type(v) is int and v >= 0 for v in family), 'invalid semantic family')
        need(all([r[0].bit_count(), r[1].bit_count()] == family for r in records), 'mixed original semantic family')
        tags = [(r[2], r[3]) for r in records]
        need(len(set(tags)) == len(tags), 'duplicate semantic output configuration')
        mass = sum(1 << (r[4] + r[5]) for r in records)
        ceiling = 1 << (44 - witness['imported_size'])
        need(witness['mass'] == mass and witness['ceiling'] == ceiling and mass > ceiling, 'semantic mass not a negative bound')
    else:
        record, rows = selected[0]
        need(record[4] + record[5] + witness['imported_size'] == 44, 'cut/lock original not tight')
        q = witness['physical_port']
        need(type(q) is int and 0 <= q < 13, 'invalid obstruction port')
        marked = record[2] | record[3]
        if kind == 'TIGHT_MARKED_PORT_LOCK':
            need(marked >> q & 1, 'lock port is not marked')
        else:
            need(not (marked >> q & 1), 'cut port is marked')
            free = [t for t in range(13) if not marked >> t & 1]
            need(all(all(v[t] <= v[q] if t < q else v[q] <= v[t] for t in free if t != q) for v in rows), 'whole original free cut fails')
        x = witness['full_Boolean_witness']
        need(type(x) is int and 0 <= x < 8192, 'invalid full witness')
        y = bool_word(context.full_parent[x], context.extension(state, head, tail))
        actual, target = y >> q & 1, int(x.bit_count() >= 13 - q)
        need(actual != target and actual == witness['actual_bit'] and target == witness['sorted_bit'], 'full wrong-rank witness differs')
    context.kinds[kind] += 1


def validate_interface(certificate, context):
    need(certificate['schema'] == 'HIGH3-one-prior-LOW-12-exclusion-v1' and certificate['size_budget'] == 44, 'schema/budget differs')
    need(certificate['parent_certificate_sha256'] == PARENT_HASH, 'parent binding differs')
    entries = certificate['state_heads']
    need([s for s, h in entries] == [s['id'] for s in context.states], 'retained state cover differs')
    used = set()
    head_negatives = tail_negatives = 0
    for state, heads in entries:
        need(isinstance(heads, list) and len(heads) == 18, 'head cover differs')
        for refs in heads:
            ids = [refs] if type(refs) is int else refs
            need(isinstance(ids, list) and (type(refs) is int or len(ids) == 1), 'tail cover differs')
            need(all(type(i) is int and 0 <= i < len(certificate['witnesses']) for i in ids), 'invalid witness reference')
            used.update(ids)
            head_negatives += type(refs) is int
            tail_negatives += 0 if type(refs) is int else 1
    need(used == set(range(len(certificate['witnesses']))), 'unused or missing witness')
    return {'retained_functions': len(entries), 'heads': len(entries) * 18,
            'head_negatives': head_negatives, 'tail_negatives': tail_negatives,
            'negative_units': head_negatives + tail_negatives,
            'catalog_witnesses': len(used), 'all_tail_orders_per_head': 1, 'whole_tail_functions_per_head': 1}


def run(certificate, context, offset=0, count=None):
    summary = validate_interface(certificate, context)
    need(type(offset) is int and 0 <= offset < len(certificate['state_heads']), 'invalid selected offset')
    need(count is None or type(count) is int and 1 <= count <= len(certificate['state_heads'])-offset, 'invalid complete selected count')
    entries = certificate['state_heads'][offset:] if count is None else certificate['state_heads'][offset:offset + count]
    checked = []
    for state, heads in entries:
        for head, refs in enumerate(heads):
            if type(refs) is int:
                check_witness(certificate['witnesses'][refs], state, head, None, context)
                checked.append([state, head, -1, refs])
            else:
                for tail, ref in enumerate(refs):
                    check_witness(certificate['witnesses'][ref], state, head, tail, context)
                    checked.append([state, head, tail, ref])
    return {**summary, 'completed_function_ids': [s for s, h in entries], 'checked_units': len(checked),
            'checked_bindings_sha256': digest(checked), 'kind_counts': dict(context.kinds),
            'original_cube_assignments': dict(context.assignments), 'selected_original_domains': len(context.base)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=ROOT / 'certificate.json')
    parser.add_argument('--full-graph', type=Path, default=FULL_GRAPH)
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--functions', type=int)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    raw = args.certificate.read_bytes()
    result = run(json.loads(raw), Context(full_graph=args.full_graph), args.offset, args.functions)
    data = {'agent': 'six-sorting-2', 'role': 'researcher', 'status': 'COMPLETE_SELECTED_INDEPENDENT_SCALAR_CHECK',
            'certificate_sha256': hashlib.sha256(raw).hexdigest(), 'mathematical_result': result,
            'seconds': time.monotonic() - started, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.output:
        args.output.write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(data), flush=True)


if __name__ == '__main__':
    main()
