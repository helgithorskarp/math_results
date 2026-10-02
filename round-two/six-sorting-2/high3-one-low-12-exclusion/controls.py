"""Positive sorter and intended-damage controls for the independent checker."""
import copy
import json
from pathlib import Path
import tempfile
import time
import resource

import verify as v


def reject(operation, expected):
    try:
        operation()
    except ValueError as error:
        v.need(expected in str(error), 'damage rejected for an unintended reason: ' + str(error))
        return expected
    raise ValueError('damaged input accepted: ' + expected)


def controls(certificate, context):
    damaged = []

    def interface_damage(edit, why):
        altered = copy.deepcopy(certificate)
        edit(altered)
        damaged.append(reject(lambda: v.validate_interface(altered, context), why))

    interface_damage(lambda c: c.update(parent_certificate_sha256='0' * 64), 'parent binding differs')
    interface_damage(lambda c: c['state_heads'].pop(), 'retained state cover differs')
    interface_damage(lambda c: c['state_heads'][0][1].pop(), 'head cover differs')
    first_tail = next((i, j) for i, (s, hs) in enumerate(certificate['state_heads']) for j, refs in enumerate(hs) if isinstance(refs, list))
    interface_damage(lambda c: c['state_heads'][first_tail[0]][1][first_tail[1]].pop(), 'tail cover differs')
    interface_damage(lambda c: c.update(size_budget=45), 'schema/budget differs')
    altered_state = copy.deepcopy(context.states[0])
    altered_state['shortest_word'] = [[5, 6]]
    damaged.append(reject(lambda: v.check_state(altered_state), 'retained full function differs'))
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        raw = (v.PARENT / 'certificate.json').read_bytes()
        (root / 'certificate.json').write_bytes(raw + b' ')
        damaged.append(reject(lambda: v.Context(root, full_graph=v.FULL_GRAPH), 'parent certificate pin differs'))
        (root / 'certificate.json').write_bytes(raw)
        fixture = json.loads((v.PARENT / 'fixture.json').read_text())
        fixture['literal_parent_prefix'][0] = [0, 10]
        (root / 'fixture.json').write_text(json.dumps(fixture))
        damaged.append(reject(lambda: v.Context(root, full_graph=v.FULL_GRAPH), 'literal prefix pin differs'))

    chosen = {}
    for state, heads in certificate['state_heads']:
        for head, refs in enumerate(heads):
            for tail, ref in ((None, refs),) if type(refs) is int else enumerate(refs):
                w = certificate['witnesses'][ref]
                chosen.setdefault(w['kind'], (state, head, tail, w))
    v.need({'DIRECT_COST', 'TIGHT_FREE_CUT', 'TIGHT_MARKED_PORT_LOCK'} <= set(chosen), 'control kind missing')

    def witness_damage(kind, edit, why):
        state, head, tail, original = chosen[kind]
        altered = copy.deepcopy(original)
        edit(altered)
        damaged.append(reject(lambda: v.check_witness(altered, state, head, tail, context), why))

    for kind in chosen:
        state, head, tail, w = chosen[kind]
        v.check_witness(w, state, head, tail, context)
    witness_damage('DIRECT_COST', lambda w: w.update(imported_size=w['imported_size'] + 1), 'imported lower bound differs')
    witness_damage('DIRECT_COST', lambda w: w['record'].__setitem__(4, w['record'][4] + 1), 'complete original D/R/tag/identity record differs')
    witness_damage('DIRECT_COST', lambda w: w['record'].__setitem__(5, w['record'][5] + 1), 'complete original D/R/tag/identity record differs')
    witness_damage('DIRECT_COST', lambda w: w['record'].__setitem__(6, w['record'][6] ^ 1), 'complete original D/R/tag/identity record differs')
    witness_damage('TIGHT_FREE_CUT', lambda w: w.update(physical_port=(w['record'][2] | w['record'][3]).bit_length() - 1), 'cut port is marked')
    witness_damage('TIGHT_MARKED_PORT_LOCK', lambda w: w.update(physical_port=next(q for q in range(13) if not (w['record'][2] | w['record'][3]) >> q & 1)), 'lock port is not marked')
    witness_damage('TIGHT_FREE_CUT', lambda w: w.update(full_Boolean_witness=0), 'full wrong-rank witness differs')
    witness_damage('TIGHT_MARKED_PORT_LOCK', lambda w: w.update(full_Boolean_witness=0), 'full wrong-rank witness differs')
    if 'SEMANTIC_WEIGHTED_MASS' in chosen:
        witness_damage('SEMANTIC_WEIGHTED_MASS', lambda w: w['distinct_tag_witness_records'].append(copy.deepcopy(w['distinct_tag_witness_records'][0])), 'duplicate semantic output configuration')
        witness_damage('SEMANTIC_WEIGHTED_MASS', lambda w: w.update(original_counts=[4, 0] if w['original_counts'] != [4, 0] else [0, 4]), 'mixed original semantic family')
        witness_damage('SEMANTIC_WEIGHTED_MASS', lambda w: w.update(mass=w['mass'] - 1), 'semantic mass not a negative bound')
    interface_damage(lambda c: c['state_heads'][0][1].__setitem__(0, len(c['witnesses'])), 'invalid witness reference')
    interface_damage(lambda c: c['witnesses'].append(copy.deepcopy(c['witnesses'][0])), 'unused or missing witness')
    interface_damage(lambda c: c['state_heads'][1].__setitem__(0, c['state_heads'][0][0]), 'retained state cover differs')
    damaged.append(reject(lambda: v.run(certificate, context, offset=-1, count=1), 'invalid selected offset'))
    damaged.append(reject(lambda: v.run(certificate, context, offset=0, count=0), 'invalid complete selected count'))
    witness_damage('DIRECT_COST', lambda w: w['record'].__setitem__(2, w['record'][2] ^ 1), 'complete original D/R/tag/identity record differs')
    witness_damage('TIGHT_MARKED_PORT_LOCK', lambda w: w.update(actual_bit=1-w['actual_bit']), 'full wrong-rank witness differs')
    witness_damage('TIGHT_FREE_CUT', lambda w: w.update(sorted_bit=1-w['sorted_bit']), 'full wrong-rank witness differs')

    # Actual size-45 construction, independently evaluated on EVERY input.
    # Selected original domains are separately replayed with distinct ranks;
    # no negative prefix criterion may reject this genuine size-45 sorter.
    fixture = json.loads((v.ROOT / 'fixture.json').read_text())
    sorter = fixture['positive_thirteen_sorter']
    v.valid_word(sorter)
    v.need(len(sorter) == 45, 'positive thirteen sorter size differs')
    v.need(all(v.bool_word(x, sorter) == ((1 << x.bit_count()) - 1) << (13 - x.bit_count()) for x in range(8192)), 'positive thirteen sorter fails')
    origins = set()
    for w in certificate['witnesses']:
        for r in w.get('distinct_tag_witness_records', [w.get('record')]):
            origins.add(tuple(r[:2]))
    groups = {}
    assignments = 0
    for lo, hi in sorted(origins):
        record, rows = v.follow(v.fresh_domain(lo, hi), sorter, 0)
        assignments += len(rows)
        l, h = lo.bit_count(), hi.bit_count()
        v.need(record[2] == (1 << l) - 1 and record[3] == ((1 << h) - 1) << (13 - h), 'positive sorter marked outputs differ')
        v.need(all(row == sorted(row) for row in rows), 'positive original numeric sorter fails')
        cost = record[4] + record[5]
        floor = v.FLOORS[13 - l - h]
        v.need(cost + floor <= 45, 'false positive direct bound rejects known sorter')
        family = (l, h)
        groups[family] = max(groups.get(family, -1), cost)
    v.need(all((1 << c) <= (1 << (45 - v.FLOORS[13 - sum(f)])) for f, c in groups.items()), 'false positive semantic bound rejects known sorter')
    six = json.loads((v.PARENT / 'fixture.json').read_text())['positive_six_sorter']
    v.need(len(six) == 12 and all(v.bool_word(x, six) == ((1 << x.bit_count()) - 1) << (6 - x.bit_count()) for x in range(64)), 'positive six sorter fails')
    return {'status': 'POSITIVE_AND_INTENDED_DAMAGE_CONTROLS_PASS', 'damages': damaged,
            'damage_count': len(damaged), 'positive_certificate_kinds': len(chosen),
            'positive_thirteen_Boolean_inputs': 8192, 'positive_six_Boolean_inputs': 64,
            'positive_original_domains': len(origins), 'positive_original_numeric_assignments': assignments}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--full-graph', type=Path, default=v.FULL_GRAPH)
    args = parser.parse_args()
    v.FULL_GRAPH = args.full_graph
    started = time.monotonic()
    result = controls(json.loads((v.ROOT / 'certificate.json').read_text()), v.Context(full_graph=v.FULL_GRAPH))
    print(json.dumps({'agent': 'six-sorting-2', 'role': 'researcher', 'mathematical_result': result,
                      'seconds': time.monotonic() - started, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
