"""Semantic damages for complete cover proposals and actual AP conflicts."""
import copy
import json
from pathlib import Path
from check_cover import check
from check_minimum_masks import audit, check_unit


def need(ok, message):
    if not ok:
        raise ValueError(message)


here = Path(__file__).resolve().parent
h = json.loads((here / 'hypergraph72.json').read_text())
p = json.loads((here / 'cover9.json').read_text())
negative = json.loads((here / 'cover8.json').read_text())
r = json.loads((here / 'minimum-mask-proposal.json').read_text())
rejections = []

def rejects(name, base, mutation, checker):
    candidate = copy.deepcopy(base)
    mutation(candidate)
    try:
        checker(candidate)
    except ValueError as error:
        rejections.append({'name': name, 'reason': str(error)})
    else:
        raise ValueError('semantic damage accepted: ' + name)


# Cover completeness/normalization and direct-positive controls.
for name, change in [
    ('partial-negative', lambda x: x.update(complete=False)),
    ('wrong-negative-count', lambda x: x.update(tested_count=x['tested_count'] - 1)),
    ('wrong-negative-domain', lambda x: x.update(candidate_domain_size=x['candidate_domain_size'] + 1)),
    ('wrong-negative-status', lambda x: x.update(status='UNKNOWN')),
    ('wrong-fixed-vertex', lambda x: x.update(fixed_vertex=2)),
    ('wrong-whole-edge-hash', lambda x: x.update(edge_sha256='0' * 64)),
]:
    rejects(name, negative, change, lambda x: check(h, x))
rejects('noncover-positive', p, lambda x: x.update(first_cover=list(range(1, 10))), lambda x: check(h, x))


def first(x):
    return x['entries'][0]


def wrong_fixed_colors(x):
    e = first(x)
    free = e['actual_free_fields']
    squares = {r * r % 31 for r in range(1, 31)}
    for d in range(1, 620):
        positions = [(3 + j * d) % 620 for j in range(7)]
        fields = [n % 31 for n in positions]
        if 0 in fields or sum(r in free for r in fields) != 1:
            continue
        colors = [int((n % 31 + 1) % 31 not in squares)
                  ^ int(bool(72 & (1 << (n % 20 % 10)))) ^ int(n % 20 >= 10)
                  for n in positions[1:]]
        if len(set(colors)) == 2:
            e['unit_conflict']['opposite_actual_ap_demands'][0]['ap'] = [3, d]
            return
    raise ValueError('no genuinely mixed six-fixed-point damage found')


for name, change in [
    ('missing-minimum-mask', lambda x: x['entries'].pop()),
    ('duplicate-minimum-mask', lambda x: x['entries'].__setitem__(1, copy.deepcopy(x['entries'][0]))),
    ('wrong-whole-mask-count', lambda x: x.update(covers=x['covers'] - 1)),
    ('wrong-phase-word', lambda x: x.update(mask=73)),
    ('dropped-reference-zero', lambda x: first(x)['actual_free_fields'].remove(30)),
    ('silently-free-physical-pole', lambda x: first(x)['actual_free_fields'].append(0)),
    ('missing-physical-conflict', lambda x: first(x).update(unit_conflict=None)),
    ('same-demand-bits', lambda x: first(x)['unit_conflict']['opposite_actual_ap_demands'][1].update(required_lower=0)),
    ('wrong-conflict-field', lambda x: first(x)['unit_conflict'].update(field=7)),
    ('wrong-antipodal-cell', lambda x: first(x)['unit_conflict'].update(lower_phase_cell=4)),
    ('zero-cyclic-step', lambda x: first(x)['unit_conflict']['opposite_actual_ap_demands'][0].update(ap=[3, 0])),
    ('physical-pole-in-AP', lambda x: first(x)['unit_conflict']['opposite_actual_ap_demands'][0].update(ap=[0, 1])),
    ('extra-physical-free-point', lambda x: first(x)['unit_conflict']['opposite_actual_ap_demands'][0].update(ap=[3, 2])),
    ('wrong-six-fixed-colors', wrong_fixed_colors),
]:
    rejects(name, r, change, lambda x: audit(h, p, x))
positive = check(h, p)
e = r['entries'][0]
c = e['unit_conflict']
literal = [check_unit(e['actual_free_fields'], c['field'], c['lower_phase_cell'], d)
           for d in c['opposite_actual_ap_demands']]
print(json.dumps({'author': 'six-vdw-1', 'role': 'researcher',
                  'status': 'COMPLETE_MINIMUM_MASK_SEMANTIC_CONTROLS',
                  'positive_minimum_cover': positive['witness'],
                  'positive_actual_opposite_APs': literal,
                  'damages_rejected': len(rejections), 'rejections': rejections}, sort_keys=True))
