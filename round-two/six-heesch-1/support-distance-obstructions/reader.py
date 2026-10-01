"""Solver-free checker for exact support-distance obstruction thresholds."""
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path

from cover import ball, check_poses, compile_cover, dimacs, sweep
from rup import RupChecker

HERE = Path(__file__).resolve().parent


def independent_ball(cells, q):
    """Rectangle enumeration and direct D4 widths, without a convex hull."""
    @lru_cache(None)
    def norm(dx, dy):
        widths = []
        for swap in (False, True):
            for sx in (-1, 1):
                for sy in (-1, 1):
                    values = [dx * sx * (y if swap else x) +
                              dy * sy * (x if swap else y) for x, y in cells]
                    widths.append(max(values) - min(values) + abs(dx) + abs(dy))
        return max(widths)
    r = q // (max(max(x, y) for x, y in cells) + 1)
    result = []
    for x in range(min(a for a, b in cells) - r,
                   max(a for a, b in cells) + r + 1):
        for y in range(min(b for a, b in cells) - r,
                       max(b for a, b in cells) + r + 1):
            if min(norm(x - a, y - b) for a, b in cells) <= q:
                result.append((x, y))
    return sorted(result)


def independent_placements(cells, target):
    """D4 via successive rotations; full translation rectangles."""
    orientations = set()
    for reflect in (False, True):
        current = [(x, -y if reflect else y) for x, y in cells]
        for unused in range(4):
            xmin, ymin = min(x for x, y in current), min(y for x, y in current)
            orientations.add(tuple(sorted((x - xmin, y - ymin) for x, y in current)))
            current = [(-y, x) for x, y in current]
    demanded = set(target) - set(cells)
    found = set()
    for orientation in orientations:
        for dx in range(min(x for x, y in demanded) - max(x for x, y in orientation),
                        max(x for x, y in demanded) + 1):
            for dy in range(min(y for x, y in demanded) - max(y for x, y in orientation),
                            max(y for x, y in demanded) + 1):
                physical = tuple(sorted((x + dx, y + dy) for x, y in orientation))
                if set(cells).isdisjoint(physical) and not demanded.isdisjoint(physical):
                    found.add(physical)
    return sorted(found)


def rejects(function):
    try:
        function()
    except ValueError:
        return
    raise ValueError('malformed control was accepted')


def controls():
    rejects(lambda: RupChecker([[1, 2]], 2).verify('0\n'))
    rejects(lambda: RupChecker([[1, 2]], 2).verify('-1 0\n0\n'))
    rejects(lambda: RupChecker([[1]], 1).verify('1 0\n'))
    rejects(lambda: RupChecker([[1]], 1).verify('2 0\n0\n'))
    rejects(lambda: RupChecker([[1]], 1).verify('1\n0\n'))
    rejects(lambda: RupChecker([[1]], 1).verify('1 0 0\n0\n'))
    sweep.require(RupChecker([[1], [-1]], 1).verify('d 1 0\n0\n') ==
                  dict(additions=1, ignored_deletions=1), 'deletion control failed')
    return dict(rejected_rup_controls=6, deletion_control=1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    records = json.loads((HERE / 'cases.json').read_text())
    prior = json.loads((HERE.parent / 'linear-corona-bound/input.json').read_text())
    family, unused = sweep.growth_family(sweep.read_cells(prior['cells']), 3)
    family_hash = hashlib.sha256((json.dumps(family, separators=(',', ':')) + '\n').encode()).hexdigest()
    sweep.require(family_hash == sweep.FAMILY_SHA256, 'prior family hash mismatch')
    result = dict(agent='six-heesch-1', role='researcher',
                  scope='exact rooted grid-cover distance; transferred Hh upper only',
                  family_sha256=family_hash, cases=[], controls=controls())
    for record in records:
        cells = sweep.read_cells(record['cells'])
        sweep.require(cells == tuple(map(tuple, record['cells'])) == family[record['index']],
                      'root or family index mismatch')
        body = sweep.difference_body(cells)
        sweep.require(body == tuple(map(tuple, record['body'])), 'difference body mismatch')
        q = record['q']
        sweep.require(type(q) is int and q > 0 and record['lower_q'] == q - 1,
                      'thresholds must be consecutive positive integers')
        lower, upper = ball(cells, body, q - 1), ball(cells, body, q)
        sweep.require(lower == independent_ball(cells, q - 1) and
                      upper == independent_ball(cells, q), 'complete ball audit failed')
        poses = record['lower_poses']
        check_poses(cells, lower, poses)
        rejects(lambda: check_poses(cells, lower, poses[1:]))
        rejects(lambda: check_poses(cells, lower, poses + [poses[0]]))
        target = tuple(map(tuple, record['obstruction']))
        sweep.require(len(target) == len(set(target)) and
                      set(target) <= set(upper) and set(cells).isdisjoint(target),
                      'invalid negative target')
        rho = sweep.target_rho(cells, target, body)
        sweep.require(rho == q == record['obstruction_rho'], 'obstruction rho mismatch')
        candidates, cnf, nv = compile_cover(cells, target)
        sweep.require(candidates == independent_placements(cells, target),
                      'complete placement audit failed')
        raw = dimacs(cnf, nv)
        sweep.require(hashlib.sha256(raw).hexdigest() == record['cnf_sha256'], 'CNF hash mismatch')
        trace_raw = (HERE / f"case-{record['index']}.rup").read_bytes()
        sweep.require(hashlib.sha256(trace_raw).hexdigest() == record['proof_sha256'],
                      'proof hash mismatch')
        proof = RupChecker(cnf, nv).verify(trace_raw.decode('ascii'))
        height_upper = sweep.upper_from_rho(cells, body, q)
        facts = dict(index=record['index'], optimal_obstruction_rho=q,
                     optimal_transferred_upper=height_upper,
                     lower_ball_cells=len(lower), upper_ball_cells=len(upper),
                     lower_copy_count=1 + len(poses), negative_target_cells=len(target),
                     placements=len(candidates), variables=nv, clauses=len(cnf),
                     proof_additions=proof['additions'], proof_bytes=len(trace_raw),
                     cnf_sha256=record['cnf_sha256'], proof_sha256=record['proof_sha256'])
        for field, actual in [('body_twice_area', sweep.twice_area(body)),
                              ('diagonal_support', sweep.support(body, (1, 1))),
                              ('upper', height_upper), ('lower_ball_cells', len(lower)),
                              ('upper_ball_cells', len(upper)), ('placements', len(candidates)),
                              ('variables', nv), ('clauses', len(cnf)),
                              ('proof_bytes', len(trace_raw)),
                              ('proof_lines', proof['additions'])]:
            sweep.require(record[field] == actual, f'{field} mismatch')
        result['cases'].append(facts)
    if args.expected:
        sweep.require(result == json.loads(args.expected.read_text()), 'expected output mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
