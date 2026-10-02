"""Independent scalar check of HIGH3 zero-prior-LOW head/tail certificates.

No producer/profiler imports. Complete numeric original cubes retain distinct
extreme ranks. Full five-output functions and all equal-merge orders are
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
PARENT = ROOT / 'upstream'
DEAD = (5, 6, 7, 9, 10)
LOW = (3, 4, 8)
FLOORS = {9: 25, 11: 35, 12: 39}
PARENT_HASH = 'bdfdc23f34cffe622f623d00f4b005d57de1388c307a9662ab93b351c1d37257'
PREFIX_HASH = 'c944a462b99885ae5193a62a811b3cec9af026a4da2cf148eb2512eb5ba7703a'


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
    need(len(word) <= 6, 'retained shortest bound exceeds six')
    local = [[DEAD.index(a), DEAD.index(b)] for a, b in word]
    actual = [sum(((bool_word(x, local) >> j) & 1) << x for x in range(32)) for j in range(5)]
    need(actual == s['full32_function'], 'retained full function differs')
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
    # Derive by complete equal-cost event enumeration, then choose the
    # lexicographically least literal word for every whole five-row function.
    root = min(selected, partner)
    initial = {1: 7, 2: 7, root: 7}
    initial.update({q: 6 for q in LOW if q != selected})
    support = sorted(initial)
    orders = list(all_equal_tails(initial))
    need(len(orders) == 9 and all(len(w) == 4 for w in orders), 'equal-tail event enumeration differs')
    tables = {}
    for w in orders:
        local = [[support.index(a), support.index(b)] for a, b in w]
        table = tuple(bool_word(x, local) for x in range(32))
        need(all(table[x] & 1 == int(x == 31) for x in range(32)), 'tail fails whole five-input minimum')
        tables.setdefault(table, []).append(w)
    need(len(tables) == 3 and sorted(map(len, tables.values())) == [3, 3, 3], 'tail whole-function quotient differs')
    # Public tail numbering is determined by the three matchings AFTER
    # the unique six-six merge. Select their literal representatives,
    # then check that the complete independent enumeration has exactly
    # their full row functions. No order cutoff or tail sample is used.
    units = sorted(q for q in LOW if q != selected)
    live = sorted([1, 2, root, units[0]])
    a, b, c, d = live
    reps = [[units, list(x), list(y), sorted([min(x), min(y)])]
            for x, y in [((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))]]
    rep_tables = {tuple(bool_word(x, [[support.index(a), support.index(b)] for a, b in w]) for x in range(32)) for w in reps}
    need(rep_tables == set(tables), 'canonical tails omit a whole function')
    return reps


class Context:
    def __init__(self, parent_root=PARENT):
        raw = (parent_root / 'certificate.json').read_bytes()
        need(hashlib.sha256(raw).hexdigest() == PARENT_HASH, 'parent certificate pin differs')
        data = json.loads(raw)['result']
        fixture = json.loads((parent_root / 'fixture.json').read_text())
        self.prefix = fixture['literal_prefix']
        valid_word(self.prefix)
        need(len(self.prefix) == 27 and digest(self.prefix) == PREFIX_HASH, 'literal prefix pin differs')
        need(hashlib.sha256((parent_root / 'fixture.json').read_bytes()).hexdigest() ==
             '6a30d6752e5ccaeeea57f3193346249cad1ca6c5f937d81d54f4bbb219cafdca', 'parent fixture whole-byte pin differs')
        blocked = {b['state_id'] for b in data['blocked']}
        self.states = [s for s in data['states'] if s['id'] not in blocked]
        need(len(self.states) == 181, 'parent retained cover differs')
        self.words = {}
        for s in self.states:
            self.words[s['id']] = check_state(s)
        self.full_parent = [bool_word(x, self.prefix) for x in range(8192)]
        need(sorted({(y >> 1) & 1023 for y in self.full_parent}) == fixture['parent_core_states'], 'whole parent image differs')
        need(all((y >> q & 1) == int(x.bit_count() >= 13 - q) for x, y in enumerate(self.full_parent) for q in (0, 11, 12)), 'whole parent held rank differs')
        need(all(min(y >> q & 1 for q in (1, 2, 3, 4, 8)) == int(x.bit_count() >= 12)
                 for x, y in enumerate(self.full_parent)), 'live LOW ports omit second minimum')
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
            self.prepared[origin] = follow(self.base[origin], self.words[state], 27)
            self.assignments['preparation'] += len(self.prepared[origin][1])
        selected, partner = LOW[head // 5], DEAD[head % 5]
        key = (head, origin)
        if key not in self.headed:
            self.headed[key] = follow(self.prepared[origin], [sorted([selected, partner])], 27 + len(self.words[state]))
            self.assignments['head'] += len(self.headed[key][1])
        if tail is None:
            return self.headed[key]
        key = (head, tail, origin)
        if key not in self.tailed:
            self.tailed[key] = follow(self.headed[(head, origin)], self.tails[selected, partner][tail], 28 + len(self.words[state]))
            self.assignments['tail'] += len(self.tailed[key][1])
        return self.tailed[key]

    def extension(self, state, head, tail):
        selected, partner = LOW[head // 5], DEAD[head % 5]
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
    need(certificate['schema'] == 'HIGH3-zero-prior-LOW-exclusion-v1' and certificate['size_budget'] == 44, 'schema/budget differs')
    need(certificate['parent_certificate_sha256'] == PARENT_HASH, 'parent binding differs')
    entries = certificate['state_heads']
    need([s for s, h in entries] == [s['id'] for s in context.states], 'retained state cover differs')
    used = set()
    head_negatives = tail_negatives = 0
    for state, heads in entries:
        need(isinstance(heads, list) and len(heads) == 15, 'head cover differs')
        for refs in heads:
            ids = [refs] if type(refs) is int else refs
            need(isinstance(ids, list) and (type(refs) is int or len(ids) == 3), 'tail cover differs')
            need(all(type(i) is int and 0 <= i < len(certificate['witnesses']) for i in ids), 'invalid witness reference')
            used.update(ids)
            head_negatives += type(refs) is int
            tail_negatives += 0 if type(refs) is int else 3
    need(used == set(range(len(certificate['witnesses']))), 'unused or missing witness')
    return {'retained_functions': len(entries), 'heads': len(entries) * 15,
            'head_negatives': head_negatives, 'tail_negatives': tail_negatives,
            'negative_units': head_negatives + tail_negatives,
            'catalog_witnesses': len(used), 'all_tail_orders_per_head': 9, 'whole_tail_functions_per_head': 3}


def run(certificate, context, offset=0, count=None):
    summary = validate_interface(certificate, context)
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
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--functions', type=int)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    raw = args.certificate.read_bytes()
    result = run(json.loads(raw), Context(), args.offset, args.functions)
    data = {'agent': 'six-sorting-2', 'role': 'researcher', 'status': 'COMPLETE_SELECTED_INDEPENDENT_SCALAR_CHECK',
            'certificate_sha256': hashlib.sha256(raw).hexdigest(), 'mathematical_result': result,
            'seconds': time.monotonic() - started, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.output:
        args.output.write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(data), flush=True)


if __name__ == '__main__':
    main()
