"""NEW post-binding exact semantic controls; no old positive driver/factor."""
from reader_binding import check_current
check_current()
import check_refined as c
from copy import deepcopy
from fractions import Fraction as F
import importlib
import json
from pathlib import Path
import resource
import sys
import tempfile
import time


def run(parent):
    started = time.monotonic()
    parent = Path(parent).resolve()
    c.bind_parent(parent)
    sys.path.insert(0, str(parent))
    encoding = importlib.import_module('encoding')
    base = encoding.comparison()
    members, masks, types = c.original_sets()
    edges = [(i, j) for i in range(2, 303) for j in range(i + 1, 303)
             if not masks[i] & masks[j]]
    rejects = []

    def reject(name, reason, test):
        try:
            test()
        except ValueError as error:
            c.require(str(error) == reason, 'designated semantic gate only: ' + name)
            rejects.append(dict(name=name, exception='ValueError', reason=str(error)))
        else:
            raise ValueError('invalid certificate accepted: ' + name)

    original = json.loads((parent / 'BOUNDARY-CANDIDATE.json').read_bytes())
    scope_reason = 'whole exact credited table scope; historical status is not proof'
    distinct_reason = 'each distinct original free table coordinate'
    delta_reason = 'every table value versus explicitly fixed comparison'
    with tempfile.TemporaryDirectory(prefix='q19-refined-semantic-', dir=Path.cwd()) as temporary:
        work = Path(temporary)

        def table_case(name, reason, change):
            data = deepcopy(original)
            change(data)
            (work / 'candidate.json').write_text(json.dumps(data))
            reject(name, reason, lambda: c.decode(work, 'candidate.json', c.U, base))

        for field, value in [('tau', '1/8'), ('agent', 'unknown'),
                             ('role', 'reviewer'), ('exact_input_sha256', '0' * 64)]:
            table_case('table-' + field, scope_reason,
                       lambda data, field=field, value=value: data.__setitem__(field, value))
        table_case('table-missing-coordinate',
                   'entire 143-coordinate credited table, no omission',
                   lambda data: data['free_pair_values'].pop())
        table_case('table-duplicate-coordinate', distinct_reason,
                   lambda data: data['free_pair_values'].append(deepcopy(data['free_pair_values'][0])))
        unequal = next(i for i, item in enumerate(original['free_pair_values'])
                       if item['types'][0] != item['types'][1])
        table_case('table-unsorted-coordinate', distinct_reason,
                   lambda data: data['free_pair_values'][unequal]['types'].reverse())
        table_case('table-unsupported-coordinate', distinct_reason,
                   lambda data: data['free_pair_values'][0].__setitem__('types', [[7, 2, 0], [7, 2, 0]]))
        table_case('table-false-value', delta_reason,
                   lambda data: data['free_pair_values'][0].__setitem__('value',
                       str(F(data['free_pair_values'][0]['value']) + 1)))
        table_case('table-false-delta', delta_reason,
                   lambda data: data['free_pair_values'][0].__setitem__('delta',
                       str(F(data['free_pair_values'][0]['delta']) + 1)))
        table_case('table-floating-value',
                   'exact rational strings required for complete table coefficients',
                   lambda data: data['free_pair_values'][0].__setitem__('value', 0.125))

    V = {c.pair(c.YY, c.XY): F(-1), c.pair(c.BY, c.XY): F(-1),
         c.pair(c.CY, c.XY): F(-1), c.pair(c.BCY, c.XY): F(-1),
         c.pair(c.YY, c.YY): F(9, 14), c.pair(c.YY, c.BY): F(9, 4),
         c.pair(c.YY, c.CY): F(9, 4), c.pair(c.YY, c.BCY): F(9, 4),
         c.pair(c.XY, c.XY): F(7, 8)}

    def direction_case(name, reason, change):
        damaged = V.copy()
        change(damaged)
        reject(name, reason, lambda: c.perturbation(members, masks, types, edges,
            base, encoding.scalar_rows, candidate=damaged))

    degree_reason = 'every original vertex degree and actual loop direction cancel exactly'
    direction_case('direction-missing-orbit', 'nine actual perturbation orbits',
                   lambda d: d.pop(c.pair(c.YY, c.XY)))

    def star_damage(d):
        d.pop(c.pair(c.YY, c.XY))
        d[c.pair((1, 0, 1), c.Y)] = F(-1)

    direction_case('direction-star-edge',
                   'perturbation is supported on original nonstar proper edges', star_damage)
    direction_case('direction-floating-coefficient', 'complete exact rational direction coefficients',
                   lambda d: d.__setitem__(c.pair(c.YY, c.XY), -1.0))
    direction_case('direction-double-norm',
                   'new full original row-absolute norm and entry-change bounds',
                   lambda d: d.update({key: 2 * value for key, value in d.items()}))
    direction_case('direction-reverse-KG', degree_reason,
                   lambda d: d.__setitem__(c.pair(c.YY, c.XY), F(1)))
    direction_case('direction-reverse-WW', degree_reason,
                   lambda d: d.__setitem__(c.pair(c.XY, c.XY), F(-7, 8)))
    direction_case('direction-false-compensation', degree_reason,
                   lambda d: d.__setitem__(c.pair(c.YY, c.BY), F(9, 4) + F(1, 100)))

    damaged_masks = masks.copy()
    damaged_masks[2] |= 1
    reject('geometry-original-mask', 'each original independent unordered free edge',
           lambda: c.geometry(members, damaged_masks, types, base, encoding.scalar_rows))
    damaged_types = types.copy()
    damaged_types[next(i for i, t in enumerate(types) if t == c.XY)] = c.X
    reject('geometry-missing-W-floor', 'all original bad and XY floor vertices',
           lambda: c.geometry(members, masks, damaged_types, base, encoding.scalar_rows))
    damaged_base = base.copy()
    damaged_base.pop(c.pair(c.Y, c.Y))
    reject('geometry-missing-free-type', 'all 143 invariant coordinates occur in literal free edges',
           lambda: c.geometry(members, masks, types, damaged_base, encoding.scalar_rows))
    reject('rank-singular-minor', 'new exact surviving six-floor minor is nonsingular',
           lambda: c.invert([[F(0)] * 6 for _ in range(6)]))
    c.require(len(rejects) == 22 and len({r['name'] for r in rejects}) == 22,
              'all22 distinct actual designated semantic rejects')
    return dict(agent='six-downset-2', role='researcher', semantic_rejection_count=22,
                actual_semantic_rejections=rejects,
                source_hash_crash_timeout_or_wrong_gate_not_counted=True,
                no_parent_positive_checker_factor_EXPECTED_math_replay=True,
                all_rejections_post_complete_source_binding=True,
                runtime=dict(observed_seconds=time.monotonic() - started,
                    peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', type=Path,
                        default=Path(__file__).resolve().parent.parent / 'q19-sharp-ceiling')
    print(json.dumps(run(parser.parse_args().parent), sort_keys=True, indent=2))
