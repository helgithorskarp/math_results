"""Reject invalid mathematical inputs at the AP, screen and integer-cut bridges."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path

import verify
import verify_fractional


def run(root):
    base = root / 'base'
    dual = json.loads((root / 'certificates/cover2-phase184-far55.json').read_text())
    fractional = json.loads((root / 'certificates/fractional-phase184-far55.json').read_text())
    rejected = {}

    def reject(name, data, checker, message):
        try:
            checker(data, base)
        except ValueError as exc:
            if message not in str(exc):
                raise RuntimeError((name, str(exc), message)) from exc
            rejected[name] = str(exc)
        else:
            raise RuntimeError('Invalid input accepted: ' + name)

    bad = deepcopy(dual); bad['color0_APs'][0][0] = 1668
    bad['color0_APs'][0][1] = 100
    reject('AP_contains_free_pole', bad, verify.check, 'Required nonpole original color')
    bad = deepcopy(dual); bad['color0_APs'][0][1] = 0
    reject('zero_difference', bad, verify.check, 'Actual AP integers')
    bad = deepcopy(dual); bad['color0_APs'].append(bad['color0_APs'][0])
    reject('duplicate_AP_weight', bad, verify.check, 'Positive unique AP weight')
    bad = deepcopy(dual); bad['class_cap'] = True
    reject('boolean_budget', bad, verify.check, 'Integer fields')
    bad = deepcopy(dual); bad['base_certificate_sha256'] = '0' * 64
    reject('wrong_parent_bytes', bad, verify.check, 'Base bytes')
    bad = deepcopy(dual); bad['color0_APs'][0][2] += 10**12
    reject('point_capacity_overload', bad, verify.check, 'Exact final point capacity')
    bad = deepcopy(dual); bad['color0_cover2'][0][0][2] = bad['color0_cover2'][0][0][0]
    reject('repeated_AP_in_triple', bad, verify.check, 'Unique three-AP cut')

    spec = importlib.util.spec_from_file_location('base_control', base / 'verify.py')
    v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
    parent = json.loads((base / 'certificates/phase-184.json').read_text())
    _, loads = v.check(parent, [196], return_loads=True)
    u, D = parent['mu_numerator'], parent['denominator']
    lo, hi = parent['inner']; slack = 196*u + 55*D - sum(e[2] for e in parent['color0_APs'])
    colors = []
    eligible = set()
    for x in range(3704):
        r = (x - 1852 + (184 if x < 1852 else 434)) % 617
        c = -1 if not r else v.q[r] ^ int(x >= 1852)
        colors.append(c)
        if c == 0 and u + D*int(not lo <= x < hi) - loads[x] <= slack:
            eligible.add(x)

    # Three distinct actual monochromatic APs through one eligible point.
    by_point = {}
    triple = None
    for a, d, _ in dual['color0_APs']:
        for j in range(7):
            x = a + j*d
            if x in eligible:
                by_point.setdefault(x, []).append([a, d])
                if len(by_point[x]) == 3:
                    triple = by_point[x]; break
        if triple is not None: break
    if triple is None: raise RuntimeError('Missing common-intersection control')
    bad = deepcopy(dual); bad['color0_cover2'][0][0] = triple
    reject('nonempty_common_intersection', bad, verify.check, 'common intersection must be empty')
    bad = deepcopy(dual); bad['color0_cover2'] = []
    reject('remove_all_integer_cuts', bad, verify.check, 'No strict exact budget contradiction')
    bad = deepcopy(dual); bad['far_cap'] = 56
    reject('unsupported_far56_exclusion', bad, verify.check, 'Exact final point capacity')
    bad = deepcopy(dual); bad['class_cap'] = 197
    reject('unsupported_class197_exclusion', bad, verify.check, 'Exact final point capacity')

    bad = deepcopy(fractional)
    for entry in bad['position_weights']: entry[1] = bad['denominator']
    reject('fractional_point_relabelled_binary', bad, verify_fractional.check, 'Exact weighted class sum196')
    bad = deepcopy(fractional); bad['position_weights'][0][0] = True
    reject('boolean_point', bad, verify_fractional.check, 'Point entry integers')
    bad = deepcopy(fractional); old_x = bad['position_weights'][0][0]
    forbidden = next(x for x in range(3704) if colors[x] == 0 and x not in eligible
                     and int(not lo <= x < hi) == int(not lo <= old_x < hi))
    bad['position_weights'][0][0] = forbidden
    reject('forbidden_point_with_both_budgets_preserved', bad, verify_fractional.check,
           'Eligible unique rational point')

    # Preserve both exact budgets while making one genuinely tight AP uncovered.
    nums = dict(fractional['position_weights']); Q = fractional['denominator']
    transfer = None
    for d in range(1, 618):
        for a in range(max(0, 1852 - 6*d), min(1852, 3704 - 6*d)):
            points = [a + j*d for j in range(7)]
            if any(colors[x] != 0 for x in points): continue
            if sum(nums.get(x, 0) for x in points) != Q + 1: continue
            for x in points:
                if nums.get(x, 0) <= 2: continue
                kind = int(not lo <= x < hi)
                recipient = next((y for y in sorted(eligible - set(points))
                                  if int(not lo <= y < hi) == kind and nums.get(y, 0) <= Q-2), None)
                if recipient is not None:
                    transfer = (x, recipient); break
            if transfer: break
        if transfer: break
    if transfer is None: raise RuntimeError('Missing coverage-preserving-budget control')
    x, y = transfer; nums[x] -= 2; nums[y] = nums.get(y, 0) + 2
    bad = deepcopy(fractional); bad['position_weights'] = sorted([x, n] for x, n in nums.items() if n)
    reject('uncovered_AP_with_both_budgets_preserved', bad, verify_fractional.check,
           'Uncovered original monochromatic AP')
    return {'rejected_controls': len(rejected), 'rejections': rejected}


if __name__ == '__main__':
    print(json.dumps(run(Path(__file__).resolve().parent), sort_keys=True))
