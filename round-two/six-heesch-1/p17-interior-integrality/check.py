"""Solver-free P17 interior-integrality certificate reader."""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
from compact import compile_subset, audit_subset
from contact import Tile, require, check_patch, halo
from local import compile_cnf, dimacs
from audit import audit_pool
from rup import RupChecker
from reader import strict_rectangles

HERE = Path(__file__).resolve().parent


def reject(call):
    try:
        call()
    except ValueError:
        return 1
    raise ValueError('negative control was accepted')


def read_support_proof(cnf, nv, trace):
    checker = RupChecker(cnf, nv)
    count = 0
    for line in trace.splitlines():
        nums = list(map(int, line.split()))
        require(nums and nums[-1] == 0 and 0 not in nums[:-1], 'bad proof terminator')
        clause = nums[:-1]
        require(checker.rup(clause)[0], 'non-RUP support step')
        checker.add(clause)
        count += 1
    return {c[0] for c in checker.clauses if len(c) == 1}, count


def main():
    data = json.loads((HERE/'input.json').read_text())
    cert = json.loads((HERE/'certificate.json').read_text())
    deps = json.loads((HERE/'dependencies.json').read_text())
    sibling = HERE.parent/'finite-contact-types'
    for name, digest in deps.items():
        require(hashlib.sha256((sibling/name).read_bytes()).hexdigest() == digest,
                'dependency byte pin changed: '+name)
    tile = Tile(data['cells'])
    require(len(tile.frames[tile.root[0]]) == 1, 'P17 root stabilizer changed')
    require(tile.m == 17 and data['primary_zero_based_index'] == 43 and
            data['primary_reported_grid_Hc'] == data['primary_reported_grid_Hh'] == 3,
            'wrong primary seed provenance')
    pool, cnf, nv = compile_cnf(tile, [tile.root], 2)
    audit_pool(tile, [tile.root], 2, pool)
    require(hashlib.sha256(dimacs(cnf, nv)).hexdigest() == cert['first_formula_sha256'],
            'first formula hash mismatch')
    lookup = {pose: i for i, (pose, pixels) in enumerate(pool, 1)}
    floating = {i for p, i in lookup.items() if p[1] % 1 or p[2] % 1}
    F = set(map(tuple, cert['floating_support']))
    witnessed = set()
    for raw in cert['first_witnesses']:
        poses = [(o, Q(x), Q(y)) for o, x, y in raw]
        require(all(p in lookup for p in poses[1:]), 'witness candidate missing')
        check_patch(tile, [tile.root], poses, scale=2)
        require(strict_rectangles(tile, [tile.root], poses), 'witness missing exact collar')
        witnessed.update((o, int(2*x), int(2*y)) for o, x, y in poses[1:]
                         if x % 1 or y % 1)
    require(witnessed == F, 'floating support witnesses incomplete')
    proof = (HERE/'floating-support.rup').read_text()
    require(hashlib.sha256(proof.encode()).hexdigest() == cert['support_proof_sha256'],
            'support trace hash mismatch')
    units, steps = read_support_proof(cnf, nv, proof)
    require(steps == cert['support_proof_steps'], 'support count mismatch')
    excluded = set()
    for i in floating:
        p = pool[i-1][0]
        ty = p[0], int(2*p[1]), int(2*p[2])
        if ty not in F:
            require(-i in units, 'unsupported floating type has no proved exclusion')
            excluded.add(ty)
    require(len(F)+len(excluded) == len(floating), 'floating classification incomplete')
    E0 = {(p[0], int(2*p[1]), int(2*p[2])) for p, pixels in pool}
    for ty in E0:
        require(tile.relative_type(tile.pose(ty), tile.root) in E0, 'nonreciprocal E0')
        for frame in range(len(tile.frames[tile.root[0]])):
            require(tile.relative_type(tile.root, tile.pose(ty), frame) in E0,
                    'E0 not stabilizer closed')
    reciprocal = {ty for ty in F if tile.relative_type(tile.pose(ty), tile.root) in F}
    exceptional = tuple(data['exceptional_floating_type'])
    require(reciprocal == {exceptional}, 'floating reciprocal census changed')
    require(tile.relative_type(tile.pose(exceptional), tile.root) == exceptional,
            'exceptional type not self-reciprocal')
    fixed = [tile.root, tile.pose(exceptional)]
    check_patch(tile, fixed, fixed)
    target = set(map(tuple, data['quarter_grid_core_target']))
    old = set().union(*(tile.pixels(p, 4) for p in fixed))
    require(target <= halo(old) and len(target) == 3, 'target not a required halo subset')
    p, c, n = compile_subset(tile, fixed, 4, target)
    audit_subset(tile, fixed, 4, target, p)
    info = cert['exceptional_pair']
    require((len(p), len(c), n) == (info['pool'], info['clauses'], info['nv']),
            'exceptional core size mismatch')
    require(hashlib.sha256(dimacs(c, n)).hexdigest() == info['cnf_sha256'],
            'exceptional core hash mismatch')
    proof = (HERE/'exceptional-pair.rup').read_text()
    require(hashlib.sha256(proof.encode()).hexdigest() == info['proof_sha256'],
            'exceptional proof hash mismatch')
    pair_steps = RupChecker(c, n).verify(proof)['additions']
    # For every fractional contact, at least one directed first support fails,
    # or its literal canonical pair is exactly the certified exceptional core.
    for ty in F | excluded:
        inverse = tile.relative_type(tile.pose(ty), tile.root)
        require(ty in excluded or inverse in excluded or ty == exceptional,
                'floating type not covered by a pair exclusion')
    rejected = reject(lambda: RupChecker([[1]], 1).verify('0\n'))
    rejected += reject(lambda: audit_subset(tile, fixed, 4, target, p[:-1]))
    rejected += reject(lambda: audit_subset(tile, fixed, 4, target, p+[p[0]]))
    rejected += reject(lambda: check_patch(tile, [tile.root], [tile.root, tile.root], scale=2))
    result = {'agent': 'six-heesch-1', 'role': 'researcher', 'seed_cells': 17,
              'primary_grid_Hc': 3, 'primary_grid_Hh': 3,
              'E0_types': len(E0), 'floating_types': len(floating),
              'floating_first_support': len(F), 'floating_support_exclusions': len(excluded),
              'reciprocal_floating_first_support': len(reciprocal),
              'support_RUP_steps': steps, 'pair_core_target_pixels': len(target),
              'pair_core_candidates': len(p), 'pair_core_clauses': len(c),
              'pair_core_RUP_steps': pair_steps, 'rejected_controls': rejected,
              'claim': 'Every contact between two surrounded copies is integral; all prefixes through H-1 are integer in an H-corona packing.',
              'Hh_reduction': 'All-motion Hh existence is equivalent to an integral disc inner core and a half-grid final relaxed surround.',
              'scope': 'No fourth or fifth corona construction or new exact Heesch value.'}
    expected = HERE/'expected.json'
    if expected.exists():
        require(result == json.loads(expected.read_text()), 'expected result mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
