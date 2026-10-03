"""Source-only separate scalar checker of each complete negative-certificate slice.

No producer/profiler imports. Pinned PUBLIC9836 scalar numeric-domain
operations are reused; its Context, old prefix and negative records are
not used. Complete new domain records/functions/cuts/masses are checked.
"""
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
DEAD = (4, 5, 6, 7, 9, 10)
PREFIX_HASH = '89c4715b824b7cf4cee8a5698a612f336abdf20497ed48c5132dca514486afd4'
FIXTURE_MATH_HASH = '724990406c196b603d8701b490c1c2c7c6d57b1c3142359551d03c6651de330b'
SCALAR_SOURCE = ROOT / 'numeric.py'
SCALAR_SHA = '83c79d716581cdc8f947a21d9120a001624d8179fab8935817e28326f10bb041'
FLOORS = {9: 25, 11: 35, 12: 39}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def get_scalar():
    need(hashlib.sha256(SCALAR_SOURCE.read_bytes()).hexdigest() == SCALAR_SHA,
         'whole numeric source pin differs')
    spec = importlib.util.spec_from_file_location('credited_scalar_domains', SCALAR_SOURCE)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def fixed_functions():
    value = json.loads((ROOT / 'generated/cover.json').read_text())['mathematical']
    need(digest(value) == FIXTURE_MATH_HASH, 'entire freshly reconstructed actual-Q cover differs')
    return {'quotient': value['whole_prefix_function_classes'], 'unchecked_quotient_ids': list(range(113)),
            'entire_reachable_input_patterns': value['entire_reachable_input_patterns']}


def interface(c):
    need(c['schema'] == 'HIGH3_LOW34_ZERO_SINGLETON_TWO_BINARY_EXCLUSION_V1'
         and c['size_budget'] == 44 and c['dead_ports'] == list(DEAD), 'candidate schema/support differs')
    need(len(c['literal_prefix']) == 28 and digest(c['literal_prefix']) == PREFIX_HASH,
         'literal new prefix differs')
    fixture = fixed_functions()
    a, b = c.get('function_range', [0, 113])
    need(type(a) is int and type(b) is int and 0 <= a < b <= 113, 'invalid exact candidate range')
    expected_ids = fixture['unchecked_quotient_ids'][a:b]
    fs = c['functions']
    need([f['state_id'] for f in fs] == expected_ids, 'entire selected function-ID coverage differs')
    m = get_scalar()
    for f in fs:
        expected = fixture['quotient'][f['state_id']]
        need(f['shortest_word'] == expected['representative_word'], 'literal chosen representative differs')
        local = [[DEAD.index(a), DEAD.index(b)] for a, b in f['shortest_word']]
        table = [m.bool_word(x, local) for x in range(64)]
        columns = [sum(((y >> j) & 1) << x for x, y in enumerate(table)) for j in range(6)]
        need(columns == f['full64_function'], 'whole six-output function binding differs')
        need([h['partner'] for h in f['heads']] == list(DEAD), 'six-head coverage differs')
        for h in f['heads']:
            refs = h['negative']
            need(type(refs) is int or isinstance(refs, list) and len(refs) == 3,
                 'three distinct full tail functions required')
            for ref in [refs] if type(refs) is int else refs:
                need(type(ref) is int and 0 <= ref < len(c['witnesses']), 'invalid negative binding')


class Context:
    def __init__(self, c):
        self.m = get_scalar()
        self.prefix = c['literal_prefix']
        self.states = {f['state_id']: f for f in c['functions']}
        self.base = {}
        self.prepared = {}
        self.headed = {}
        self.tailed = {}
        self.full_prepared = {}
        self.full_headed = {}
        self.full_tailed = {}
        self.assignments = Counter()
        self.parent_boolean = [self.m.bool_word(x, self.prefix) for x in range(8192)]
        self.state = None
        self.tail_words, self.tail_tables = {}, {}
        structural = []
        for partner in DEAD:
            root = min(8, partner)
            costs = {1: 7, 2: 7, 3: 7, root: 7}
            support = sorted(costs)
            orders = list(self.m.all_equal_tails(costs))
            need(len(orders) == 6 and all(len(w) == 3 for w in orders),
                 'complete legal equal-tail recursion differs')
            groups = {}
            for w in orders:
                local = [[support.index(a), support.index(b)] for a, b in w]
                table = tuple(self.m.bool_word(x, local) for x in range(16))
                need(all(table[x] & 1 == int(x == 15) for x in range(16)), 'tail whole minimum differs')
                groups.setdefault(table, []).append(w)
            need(len(groups) == 3 and all(len(ws) == 2 for ws in groups.values()),
                 'complete full tail function partition differs')
            self.tail_words[partner] = [ws[0] for ws in groups.values()]
            self.tail_tables[partner] = [list(table) for table in groups]
            structural.append([partner, orders, [list(table) for table in groups], [2, 2, 2]])
        fixture = fixed_functions()
        function_record = []
        for f in c['functions']:
            word = f['shortest_word']
            need(all(g[0] in DEAD and g[1] in DEAD and g[0] < g[1] for g in word), 'non-preparation comparator')
            local = [[DEAD.index(a), DEAD.index(b)] for a, b in word]
            table = [self.m.bool_word(x, local) for x in range(64)]
            columns = [sum(((y >> j) & 1) << x for x, y in enumerate(table)) for j in range(6)]
            need(columns == f['full64_function'] and 2 <= len(word) <= 3,
                 'whole64 function or candidate length differs')
            full = [self.m.bool_word(x, word) for x in self.parent_boolean]
            expected = fixture['quotient'][f['state_id']]
            need(digest(full) == expected['entire_8192_FULL13_function_sha256'], 'entire thirteen-output function differs')
            actual = {}
            for x, y in zip(self.parent_boolean, full):
                start = sum(((x >> port) & 1) << j for j, port in enumerate(DEAD))
                end = sum(((y >> port) & 1) << j for j, port in enumerate(DEAD))
                need(start not in actual or actual[start] == end, 'prefix-function key is not deterministic')
                actual[start] = end
            need(sorted(actual) == fixture['entire_reachable_input_patterns'] and [actual[x] for x in sorted(actual)] == expected['actual_reachable_ordered_outputs'], 'ordered true-Q reachable function differs')
            self.full_prepared[f['state_id']] = full
            function_record.append([f['state_id'], word, table])
        self.structural = {'all_tail_orders_and_full_functions': structural,
                           'all_selected_preparation_row_functions': function_record,
                           'candidate_length_and_actual_Q_function_bindings_checked': True}

    def state_start(self, state):
        if self.state != state:
            self.prepared.clear()
            self.headed.clear()
            self.tailed.clear()
            self.state = state

    def original(self, state, partner, tail, lo, hi):
        self.state_start(state)
        key = (lo, hi)
        if key not in self.base:
            self.base[key] = self.m.follow(self.m.fresh_domain(lo, hi), self.prefix, 0)
            self.assignments['base'] += len(self.base[key][1])
        word = self.states[state]['shortest_word']
        if key not in self.prepared:
            self.prepared[key] = self.m.follow(self.base[key], word, 28)
            self.assignments['preparation'] += len(self.prepared[key][1])
        headed_key = (partner, key)
        if headed_key not in self.headed:
            self.headed[headed_key] = self.m.follow(self.prepared[key], [sorted([8, partner])], 28 + len(word))
            self.assignments['head'] += len(self.headed[headed_key][1])
        if tail is None:
            return self.headed[headed_key]
        tailed_key = (partner, tail, key)
        if tailed_key not in self.tailed:
            self.tailed[tailed_key] = self.m.follow(self.headed[headed_key], self.tail_words[partner][tail], 29 + len(word))
            self.assignments['tail'] += len(self.tailed[tailed_key][1])
        return self.tailed[tailed_key]

    def full(self, state, partner, tail):
        if state not in self.full_prepared:
            word = self.states[state]['shortest_word']
            self.full_prepared[state] = [self.m.bool_word(x, word) for x in self.parent_boolean]
        key = (state, partner)
        if key not in self.full_headed:
            self.full_headed[key] = [self.m.bool_word(x, [sorted([8, partner])]) for x in self.full_prepared[state]]
        if tail is None:
            return self.full_headed[key]
        key3 = (state, partner, tail)
        if key3 not in self.full_tailed:
            self.full_tailed[key3] = [self.m.bool_word(x, self.tail_words[partner][tail]) for x in self.full_headed[key]]
        return self.full_tailed[key3]


def check_witness(w, state, partner, tail, ctx):
    kind = w['kind']
    need(kind in ('DIRECT_COST', 'TIGHT_FREE_CUT', 'TIGHT_MARKED_PORT_LOCK', 'SEMANTIC_WEIGHTED_MASS'),
         'unrecognized sufficient obstruction')
    records = w['distinct_tag_witness_records'] if kind == 'SEMANTIC_WEIGHTED_MASS' else [w['record']]
    need(isinstance(records, list) and len(records) > 0, 'empty actual original record list')
    actuals, row_hashes = [], []
    for expected in records:
        need(isinstance(expected, list) and len(expected) == 7 and all(type(n) is int for n in expected),
             'invalid original record')
        lo, hi = expected[:2]
        k = 13 - (lo | hi).bit_count()
        need(k in FLOORS and w['imported_size'] == FLOORS[k], 'published lower bound differs')
        actual, rows = ctx.original(state, partner, tail, lo, hi)
        need(actual == expected, 'actual whole original D/R/tag/identity history differs')
        actuals.append(actual)
        row_hashes.append(digest(rows))
        if kind == 'DIRECT_COST':
            need(actual[4] + actual[5] + FLOORS[k] > 44, 'direct cost is insufficient')
        elif kind in ('TIGHT_FREE_CUT', 'TIGHT_MARKED_PORT_LOCK'):
            need(actual[4] + actual[5] + FLOORS[k] == 44, 'lock/cut is not exactly tight')
            q, x = w['physical_port'], w['full_Boolean_witness']
            need(type(q) is int and 0 <= q < 13 and type(x) is int and 0 <= x < 8192,
                 'invalid wrong-rank witness')
            bit = ctx.full(state, partner, tail)[x] >> q & 1
            sorted_bit = int(x.bit_count() >= 13 - q)
            need(bit == w['actual_bit'] and sorted_bit == w['sorted_bit'] and bit != sorted_bit,
                 'whole13 wrong-rank witness differs')
            if kind == 'TIGHT_MARKED_PORT_LOCK':
                need(all(v[q] < 0 or v[q] > 1 for v in rows), 'locked port is not marked on whole cube')
            else:
                for v in rows:
                    need(v[q] in (0, 1), 'cut port is marked')
                    need(all(v[t] <= v[q] if t < q else v[q] <= v[t]
                             for t in range(13) if t != q and v[t] in (0, 1)),
                         'original whole-cube cut fails')
    if kind == 'SEMANTIC_WEIGHTED_MASS':
        family = tuple(w['original_counts'])
        need(len(family) == 2 and all((r[0].bit_count(), r[1].bit_count()) == family for r in actuals),
             'mass combines different original families')
        tags = [(r[2], r[3]) for r in actuals]
        need(len(set(tags)) == len(tags), 'mass counts a tag class twice')
        mass = sum(1 << (r[4] + r[5]) for r in actuals)
        ceiling = 1 << (44 - w['imported_size'])
        need(mass == w['mass'] and ceiling == w['ceiling'] and mass > ceiling,
             'weighted original mass is insufficient')
    return [state, partner, tail, kind, actuals, row_hashes]


def damage_controls(c, ctx):
    tests = []

    def bad_interface(name, change):
        d = copy.deepcopy(c)
        change(d)
        try:
            interface(d)
        except (ValueError, KeyError, TypeError, IndexError):
            tests.append(name)
            return
        raise ValueError('intended interface damage accepted: ' + name)

    bad_interface('different_literal_prior_pair', lambda d: d['literal_prefix'][-1].__setitem__(0, 1))
    bad_interface('missing_full_preparation_function', lambda d: d['functions'].pop())
    bad_interface('damaged_full64_function', lambda d: d['functions'][0]['full64_function'].__setitem__(0, 0))
    bad_interface('missing_singleton_head', lambda d: d['functions'][0]['heads'].pop())
    bad_interface('missing_distinct_full_tail', lambda d: next(h for f in d['functions'] for h in f['heads'] if isinstance(h['negative'], list))['negative'].pop())
    bindings = [(f['state_id'], h['partner'], None, refs) if type(refs := h['negative']) is int
                else (f['state_id'], h['partner'], t, ref)
                for f in c['functions'] for h in f['heads']
                for t, ref in ([(None, h['negative'])] if type(h['negative']) is int else enumerate(h['negative']))]

    def bad_witness(name, kind, change):
        state, partner, tail, ref = next(b for b in bindings if c['witnesses'][b[3]]['kind'] == kind)
        w = copy.deepcopy(c['witnesses'][ref])
        change(w)
        try:
            check_witness(w, state, partner, tail, ctx)
        except (ValueError, KeyError, TypeError, IndexError):
            tests.append(name)
            return
        raise ValueError('intended witness damage accepted: ' + name)

    bad_witness('wrong_deletion_count', 'DIRECT_COST', lambda w: w['record'].__setitem__(4, w['record'][4] + 1))
    bad_witness('wrong_identity_count', 'DIRECT_COST', lambda w: w['record'].__setitem__(5, w['record'][5] + 1))
    bad_witness('wrong_identity_positions', 'DIRECT_COST', lambda w: w['record'].__setitem__(6, w['record'][6] ^ 1))
    bad_witness('wrong_current_marker', 'DIRECT_COST', lambda w: w['record'].__setitem__(2, w['record'][2] ^ 1))
    bad_witness('wrong_imported_floor', 'DIRECT_COST', lambda w: w.__setitem__('imported_size', w['imported_size'] + 1))
    bad_witness('wrong_full_Boolean_bit', 'TIGHT_FREE_CUT', lambda w: w.__setitem__('actual_bit', 1 - w['actual_bit']))
    bad_witness('invalid_marked_lock_port', 'TIGHT_MARKED_PORT_LOCK', lambda w: w.__setitem__('physical_port', 13))
    bad_witness('duplicated_mass_tag', 'SEMANTIC_WEIGHTED_MASS', lambda w: w['distinct_tag_witness_records'].append(w['distinct_tag_witness_records'][0]))
    bad_witness('wrong_mass', 'SEMANTIC_WEIGHTED_MASS', lambda w: w.__setitem__('mass', w['mass'] + 1))
    return tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=ROOT / 'certificate.json')
    parser.add_argument('--offset', type=int, required=True)
    parser.add_argument('--cases', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    whole_raw = args.certificate.read_bytes()
    whole = json.loads(whole_raw)
    interface(whole)
    a, b = args.offset, args.offset + args.cases
    need(type(a) is int and args.cases > 0 and 0 <= a < b <= 113, 'invalid complete proof slice')
    c = copy.deepcopy(whole)
    c['functions'] = c['functions'][a:b]
    used_refs = sorted({ref for f in c['functions'] for h in f['heads']
                        for ref in ([h['negative']] if type(h['negative']) is int else h['negative'])})
    translation = {old: new for new, old in enumerate(used_refs)}
    c['witnesses'] = [c['witnesses'][i] for i in used_refs]
    for f in c['functions']:
        for h in f['heads']:
            ref = h['negative']
            h['negative'] = translation[ref] if type(ref) is int else [translation[i] for i in ref]
    c['function_range'] = [a, b]
    interface(c)
    raw = (json.dumps(c, separators=(',', ':')) + '\n').encode()
    ctx = Context(c)
    bindings, kinds, used, held_inputs = [], Counter(), set(), 0
    for f in c['functions']:
        state = f['state_id']
        for h in f['heads']:
            partner = h['partner']
            for tail in range(3):
                full = ctx.full(state, partner, tail)
                need(all((y >> q & 1) == int(x.bit_count() >= 13 - q)
                         for x, y in enumerate(full) for q in (0, 1, 11, 12)),
                     'actual whole held-rank tail function differs')
                held_inputs += 8192
            refs = h['negative']
            for tail, ref in ([(None, refs)] if type(refs) is int else enumerate(refs)):
                w = c['witnesses'][ref]
                bindings.append(check_witness(w, state, partner, tail, ctx))
                kinds[w['kind']] += 1
                used.add(ref)
    need(len(bindings) == sum(1 if type(h['negative']) is int else 3 for f in c['functions'] for h in f['heads']) and used == set(range(len(c['witnesses']))),
         'all actual binding/catalogue coverage differs')
    tests = damage_controls(c, ctx)
    positive = json.loads((SCALAR_SOURCE.parent / 'fixture.json').read_text())['positive_thirteen_sorter']
    need(len(positive) == 45 and all(ctx.m.bool_word(x, positive) == sum(1 << q for q in range(13) if x.bit_count() >= 13 - q)
                                  for x in range(8192)), 'genuine45 sorter fails full Boolean positive control')
    positive_numeric = 0
    for lo, hi in ctx.base:
        final, rows = ctx.m.follow(ctx.m.fresh_domain(lo, hi), positive, 0)
        need(all(v == sorted(v) for v in rows), 'genuine45 sorter fails actual original domain')
        positive_numeric += len(rows)
    mathematical = {'certificate_sha256': hashlib.sha256(raw).hexdigest(),
                    'entire_public_certificate_sha256': hashlib.sha256(whole_raw).hexdigest(), 'function_range': [a, b],
                    'functions': len(c['functions']), 'actual_negative_bindings': len(bindings),
                    'full_tail_alternatives': 18 * len(c['functions']), 'kind_counts': dict(kinds),
                    'all_actual_negative_binding_records_and_rows': bindings,
                    'structural': ctx.structural, 'selected_original_domains': len(ctx.base),
                    'numeric_assignment_counts': dict(ctx.assignments),
                    'held_rank_full_Boolean_inputs': held_inputs,
                    'intended_rejections': tests, 'positive45_full_Boolean_inputs': 8192,
                    'positive45_numeric_original_assignments': positive_numeric}
    result = {'agent': 'six-sorting-2', 'role': 'researcher',
              'status': 'COMPLETE_SOURCE_ONLY_SCALAR_NEGATIVE_SLICE_CHECK',
              'mathematical': mathematical, 'entire_mathematical_record_sha256': digest(mathematical),
              'seconds': time.monotonic() - started,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Source-only selected two-binary slice checked. Full LOW34 and global44 gap remain open; independent-person review and formalization pending.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, separators=(',', ':')) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'mathematical'}))
    print(json.dumps({k: v for k, v in mathematical.items() if k not in ('all_actual_negative_binding_records_and_rows', 'structural')}))


if __name__ == '__main__':
    main()
