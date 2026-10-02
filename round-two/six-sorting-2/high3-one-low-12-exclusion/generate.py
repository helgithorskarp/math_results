"""Regenerate every selected negative record from original packed truth cubes.

This is a certificate producer, not the independent scalar checker. Recipes
name ORIGINAL inputs, not representative current marker configurations.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

SOURCE = Path(__file__).resolve().parent
PARENT = SOURCE.parent / 'high3-one-low-preparation-cover'
DEAD = (2, 5, 6, 7, 9, 10)
LOW = (3, 4, 8)
SIZE = {9: 25, 11: 35, 12: 39}
PARENT_HASH = 'a9dbfd3ce5419b6ad1053f0650943d76724c8acfb83c734ccc930cadc129ee36'
FIXTURE_HASH = 'c3302c9645233621ae78f06fedcd3ec013a4a1592acb2b28780c22e7569089a7'
PROFILE_HASH = 'dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719'


def need(ok, why):
    if not ok:
        raise ValueError(why)


def pinned(path, expected):
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == expected, 'whole source/input pin differs: ' + path.name)
    return raw


def tails(selected, partner):
    units = sorted(q for q in LOW if q != selected)
    second = sorted([min(selected,partner), units[0]])
    return [[units, second, [1,min(second)]]]


def produce(full_graph):
    # All external copied byte inputs are checked before the profiler import.
    compact = json.loads(pinned(PARENT / 'certificate.json', PARENT_HASH))
    parent = json.loads(full_graph.read_text())['result']
    need(hashlib.sha256(json.dumps([s['full64_function'] for s in parent['states']],separators=(',',':')).encode()).hexdigest() == compact['full_function_columns_sha256'], 'parent full function binding differs')
    need(hashlib.sha256(json.dumps([s['shortest_word'] for s in parent['states']],separators=(',',':')).encode()).hexdigest() == compact['full_function_words_sha256'], 'parent full word binding differs')
    fixture = json.loads(pinned(PARENT / 'fixture.json', FIXTURE_HASH))
    pinned(PARENT / 'profile.py', PROFILE_HASH)
    spec = importlib.util.spec_from_file_location('packed_original_profile', PARENT / 'profile.py')
    s = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(s)
    recipes = json.loads((SOURCE / 'recipes.json').read_text())
    need(recipes['schema'] == 'HIGH3-one-prior-LOW-12-recipes-v1', 'recipe schema differs')
    blocked = {i for i,ref in compact['exit_bindings']}
    need(blocked == {b['state_id'] for b in parent['blocked']} and len(blocked) == 1206, 'parent exit partition differs')
    states = {f['id']: f for f in parent['states'] if f['id'] not in blocked}
    need([i for i, heads in recipes['state_heads']] == list(states), 'recipe retained function cover differs')
    need(len(states) == 1129, 'retained function count differs')
    prefix = fixture['literal_parent_prefix'] + [fixture['first_LOW_merge']]
    need(parent['literal_prefix'] == prefix, 'literal prepared parent differs')

    def original(lo, hi):
        free = iter(s.truth_columns(13 - (lo | hi).bit_count()))
        values = [s.LOW if lo >> q & 1 else s.HIGH if hi >> q & 1 else next(free) for q in range(13)]
        return follow(([lo, hi, lo, hi, 0, 0, 0], values), prefix, 0)

    def follow(domain, word, start):
        old, old_values = domain
        values = list(old_values)
        d, r, identities = old[4:]
        for t, (a, b) in enumerate(word, start):
            hit, redundant = s.transition(values, a, b)
            d += hit
            r += redundant
            if redundant:
                identities |= 1 << t
        return [old[0], old[1], *s.marked_ports(values), d, r, identities], values

    def full_follow(columns, word):
        values = list(columns)
        for a, b in word:
            values[a], values[b] = values[a] & values[b], values[a] | values[b]
        return values

    whole = full_follow(s.truth_columns(13), prefix)
    base = {}
    catalog = [None] * len(recipes['witness_recipes'])
    checked = 0
    for state_id, heads in recipes['state_heads']:
        need(len(heads) == 18, 'recipe head cover differs')
        word = states[state_id]['shortest_word']
        prepared = {}
        following = full_follow(whole, word)
        for head_id, refs in enumerate(heads):
            selected, partner = LOW[head_id // 6], DEAD[head_id % 6]
            gate = sorted([selected, partner])
            for tail_id, ref in ((None, refs),) if type(refs) is int else enumerate(refs):
                if type(refs) is not int:
                    need(len(refs) == 1, 'recipe tail cover differs')
                recipe = recipes['witness_recipes'][ref]
                extension = [gate] + ([] if tail_id is None else tails(selected, partner)[tail_id])
                origins = recipe['origins'] if recipe['kind'] == 'SEMANTIC_WEIGHTED_MASS' else [recipe['origin']]
                records = []
                for lo, hi in origins:
                    origin = (lo, hi)
                    if origin not in base:
                        base[origin] = original(lo, hi)
                    if origin not in prepared:
                        prepared[origin] = follow(base[origin], word, 28)
                    record, values = follow(prepared[origin], extension, 28 + len(word))
                    records.append(record)
                floor = SIZE[13 - sum(origins[0][j].bit_count() for j in (0, 1))]
                if recipe['kind'] == 'SEMANTIC_WEIGHTED_MASS':
                    witness = {'kind': recipe['kind'], 'original_counts': recipe['original_counts'],
                               'imported_size': floor, 'mass': sum(1 << (r[4] + r[5]) for r in records),
                               'ceiling': 1 << (44 - floor), 'distinct_tag_witness_records': records}
                else:
                    witness = {'kind': recipe['kind'], 'record': records[0], 'imported_size': floor}
                    if recipe['kind'] != 'DIRECT_COST':
                        q, x = recipe['physical_port'], recipe['full_Boolean_witness']
                        columns = full_follow(following, extension)
                        witness.update(physical_port=q, full_Boolean_witness=x,
                                       actual_bit=columns[q] >> x & 1, sorted_bit=int(x.bit_count() >= 13 - q))
                if catalog[ref] is None:
                    catalog[ref] = witness
                else:
                    need(catalog[ref] == witness, 'a shared recipe produced different actual original records')
                checked += 1
    need(all(w is not None for w in catalog) and checked == 20322, 'recipe witnesses incomplete')
    return {'schema': 'HIGH3-one-prior-LOW-12-exclusion-v1', 'agent': 'six-sorting-2', 'role': 'researcher',
            'size_budget': 44, 'parent_certificate_sha256': PARENT_HASH,
            'state_heads': recipes['state_heads'], 'witnesses': catalog}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--full-graph', type=Path, default=SOURCE / 'generated/preparation.json')
    parser.add_argument('--output', type=Path, default=SOURCE / 'generated/certificate.json')
    args = parser.parse_args()
    started = time.monotonic()
    data = produce(args.full_graph)
    raw = (json.dumps(data, separators=(',', ':')) + '\n').encode()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(raw)
    print(json.dumps({'agent': 'six-sorting-2', 'role': 'researcher', 'status': 'ALL_SELECTED_ORIGINAL_RECORDS_REGENERATED',
                      'certificate_sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
                      'seconds': time.monotonic() - started, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
