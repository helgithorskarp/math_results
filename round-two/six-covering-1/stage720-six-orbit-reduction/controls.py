"""Semantic damage controls for the proof certificate, no solver."""
import copy
import json
from pathlib import Path
from check import check

c = json.loads(Path(__file__).with_name('certificate.json').read_text())
damaged = []
def case(name, edit):
    d = copy.deepcopy(c)
    edit(d)
    damaged.append((name, d))

case('wrong fixed class', lambda d: d['fixed'].update({'8': 4}))
case('missing original label', lambda d: d['original_labels'].pop())
case('anchor not earlier resource', lambda d: d['forced_anchor_pairs'].__setitem__(0, [9, 16]))
case('incorrect claimed strict upper', lambda d: d['envelope_cases'][0].__setitem__('even_upper', 198))
case('negative point weight', lambda d: next(r for r in d['excluded_shapes'] if r['reason'] == 'scalar_budget')['weights'].__setitem__(0, -1))
case('duplicate resource in partition', lambda d: d['resource_partitions'][0].__setitem__(0, [12]))
case('missing target case', lambda d: d['excluded_shapes'].pop())
case('invalid affine transfer', lambda d: next(r for r in d['excluded_shapes'] if r['reason'] == 'count_envelope').__setitem__('affine_map', [1, 1]))
rejected = []
for name, d in damaged:
    try:
        check(d)
    except RuntimeError:
        rejected.append(name)
    else:
        raise RuntimeError('damaged certificate accepted: ' + name)
print(json.dumps({'status': 'DAMAGE_CONTROLS_REJECTED', 'controls': rejected, 'count': len(rejected)}))
