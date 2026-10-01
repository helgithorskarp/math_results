"""Standard-library exact reader; controls check the phase/contact bridge."""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
from contact import Tile, compress, sigma, require, check_patch
from local import compile_cnf, dimacs
from audit import audit_pool
from rup import RupChecker


def strict_rectangles(tile, fixed, poses):
    """Independent variable-width face arrangement, not uniform pixels."""
    old_rects = [a for p in fixed for a in tile.anchors(p)]
    rectangles = [a for p in poses for a in tile.anchors(p)]
    axes = []
    for axis in (0, 1):
        values = {a[axis]+e for a in rectangles for e in (0, 1)}
        values.update((min(values)-1, max(values)+1))
        axes.append(sorted(values))
    xs, ys = axes
    occupied, old = set(), set()
    for i, (x, u) in enumerate(zip(xs, xs[1:])):
        for j, (y, v) in enumerate(zip(ys, ys[1:])):
            c, d = (x+u)/2, (y+v)/2
            if any(a < c < a+1 and b < d < b+1 for a, b in rectangles):
                occupied.add((i, j))
            if any(a < c < a+1 and b < d < b+1 for a, b in old_rects):
                old.add((i, j))
    return all((i+di, j+dj) in occupied for i, j in old
               for di in (-1, 0, 1) for dj in (-1, 0, 1))


def reject(call):
    try:
        call()
    except ValueError:
        return 1
    raise ValueError('negative control accepted')


def inventory(cells):
    tile = Tile(cells)
    universe = tile.universe()
    require(universe == tile.universe_rectangles(), 'contact enumeration disagreement')
    require(all(x % 2 == 0 or y % 2 == 0 for o, x, y in universe),
            'contact with two floating relative phases')
    for t in universe:
        B = tile.pose(t)
        require(tile.relative_type(B, tile.root) in universe, 'nonreciprocal universe')
        for frame in range(len(tile.frames[tile.root[0]])):
            require(tile.relative_type(tile.root, B, frame) in universe,
                    'universe not stabilizer closed')
    return {
        'cells': tile.m, 'orientations': len(tile.orientations),
        'half_grid_contact_types': len(universe),
        'floating_contact_types': sum(x % 2 or y % 2 for o, x, y in universe),
        'root_copy_budget': (tile.w+2*tile.L)*(tile.h+2*tile.L)//tile.m,
        'largest_pair_copy_budget': max(tile.pair_budget(tile.pose(t)) for t in universe),
        'contact_sha256': hashlib.sha256(json.dumps(sorted(universe),
                                  separators=(',', ':')).encode()).hexdigest()
    }


def phase_fixture():
    tile = Tile([(0, 0), (1, 0)])
    o = tile.root[0]
    fixed = [tile.root, (o, Q(2), Q(1, 2))]
    # Four horizontal domino columns, with genuinely distinct real phases.
    candidates = [(o, Q(x), Q(k)+f) for x, f in
                  [(-2, Q(1, 7)), (0, Q(0)), (2, Q(1, 2)), (4, Q(5, 7))]
                  for k in (-1, 0, 1)]
    poses = fixed + [p for p in candidates if p not in fixed and
                    any(tile.relation(p, A) == 'contact' for A in fixed)]
    domain = {(o, 0, 2), (o, 0, -2)} | {
        (o, x, y) for x in (-4, 4) for y in (-1, 1)}
    for t in domain:
        B = tile.pose(t)
        require(tile.relative_type(B, tile.root) in domain, 'fixture nonreciprocal')
        for frame in range(len(tile.frames[o])):
            require(tile.relative_type(tile.root, B, frame) in domain,
                    'fixture lacks stabilizer closure')
    old = check_patch(tile, fixed, poses, domain, 14)
    require(strict_rectangles(tile, fixed, poses), 'original exact containment failed')
    budget = tile.pair_budget(fixed[1])
    D, output = compress(poses, budget)
    new = check_patch(tile, fixed, output, domain, D)
    require(old == new and strict_rectangles(tile, fixed, output),
            'compression changed contacts or containment')
    # The elementary half-grid collapse need not preserve a restricted domain.
    collapsed = [(i, sigma(x), sigma(y)) for i, x, y in poses]
    rejected = reject(lambda: check_patch(tile, fixed, collapsed, domain))
    rejected += reject(lambda: compress(poses, len(poses)-1))
    rejected += reject(lambda: check_patch(tile, fixed, poses+[poses[2]], domain))
    rejected += reject(lambda: check_patch(tile, fixed, fixed, domain, 2))
    rejected += reject(lambda: compress([tile.root, (o, Q(2), Q(1, 3))], 2))
    # An independent scalar characterization: preserve the entire integer-threshold
    # sign vector, not only the particular contacts in the positive fixture.
    for axis in (1, 2):
        for i, A in enumerate(poses):
            for j, B in enumerate(poses):
                for k in range(-8, 9):
                    a = A[axis]-B[axis]-k
                    b = output[i][axis]-output[j][axis]-k
                    require((a > 0)-(a < 0) == (b > 0)-(b < 0),
                            'integer-threshold sign changed')
    return {'copies': len(poses), 'fixed_copies': 2, 'allowed_contact_types': len(domain),
            'copy_budget': budget, 'mesh_denominator': D,
            'contacts_preserved': len(old), 'rejected_controls': rejected,
            'claim': 'given witness is preserved; no negative half-grid existence claim'}


def calibration(here, cells):
    data = json.loads((here/'calibration.json').read_text())
    tile = Tile(cells)
    pool, cnf, nv = compile_cnf(tile, [tile.root], 2)
    audit_pool(tile, [tile.root], 2, pool)
    require(hashlib.sha256(dimacs(cnf, nv)).hexdigest() == data['root_cnf_sha256'],
            'first-support CNF changed')
    F = set(map(tuple, data['F']))
    lookup = {pose: i for i, (pose, pixels) in enumerate(pool, 1)}
    witnessed = set()
    for raw in data['first_witnesses']:
        poses = [(o, Q(x), Q(y)) for o, x, y in raw]
        check_patch(tile, [tile.root], poses, scale=2)
        require(strict_rectangles(tile, [tile.root], poses), 'first witness misses collar')
        witnessed.update((p[0], int(2*p[1]), int(2*p[2])) for p in poses[1:])
    require(witnessed == F, 'first-support positive witnesses incomplete')
    proof = (here/'support.rup').read_text()
    require(hashlib.sha256(proof.encode()).hexdigest() == data['support_proof_sha256'],
            'first-support proof changed')
    checker = RupChecker(cnf, nv)
    steps = 0
    for line in proof.splitlines():
        nums = list(map(int, line.split()))
        require(bool(nums) and nums[-1] == 0 and 0 not in nums[:-1], 'invalid RUP terminator')
        clause = nums[:-1]
        require(checker.rup(clause)[0], 'invalid conditional RUP step')
        checker.add(clause)
        steps += 1
    units = {c[0] for c in checker.clauses if len(c) == 1}
    require(all(-i in units for p, i in lookup.items()
                if (p[0], int(2*p[1]), int(2*p[2])) not in F), 'missing exclusion proof')
    require(steps == data['support_proof_steps'], 'proof step count changed')
    require(all(x % 2 == y % 2 == 0 for o, x, y in F), 'first support has floating types')
    reciprocal = {t for t in F if tile.relative_type(tile.pose(t), tile.root) in F}
    require(set(tuple(r['type']) for r in data['pairs']) == reciprocal and
            len(data['pairs']) == len(reciprocal), 'pair tests incomplete')
    E1 = set()
    pair_steps = 0
    for record in data['pairs']:
        ty = tuple(record['type'])
        fixed = [tile.root, tile.pose(ty)]
        p, c, n = compile_cnf(tile, fixed, 4)
        audit_pool(tile, fixed, 4, p)
        require(hashlib.sha256(dimacs(c, n)).hexdigest() == record['cnf_sha256'],
                'pair CNF changed')
        if record['sat']:
            poses = [(o, Q(x), Q(y)) for o, x, y in record['poses']]
            check_patch(tile, fixed, poses, scale=4)
            require(strict_rectangles(tile, fixed, poses), 'pair witness misses collar')
            E1.add(ty)
        else:
            proof = (here/record['proof']).read_text()
            require(hashlib.sha256(proof.encode()).hexdigest() == record['proof_sha256'],
                    'pair proof changed')
            pair_steps += RupChecker(c, n).verify(proof)['additions']
    require(all(x % 2 == y % 2 == 0 for o, x, y in E1), 'E1 has floating types')
    for ty in E1:
        B = tile.pose(ty)
        require(tile.relative_type(B, tile.root) in E1, 'E1 not reciprocal')
        for f in range(len(tile.frames[tile.root[0]])):
            require(tile.relative_type(tile.root, B, f) in E1, 'E1 not stabilizer closed')
    p, c, n = compile_cnf(tile, [tile.root], 1, E1)
    audit_pool(tile, [tile.root], 1, p, E1)
    info = data['final_root']
    require((len(p), len(c), n) == (info['pool'], info['clauses'], info['variables']) and
            hashlib.sha256(dimacs(c, n)).hexdigest() == info['cnf_sha256'], 'final root CNF changed')
    proof = (here/'root-E1.rup').read_text()
    require(hashlib.sha256(proof.encode()).hexdigest() == info['proof_sha256'], 'final proof changed')
    RupChecker(c, n).verify(proof)
    rejected = reject(lambda: RupChecker([[1]], 1).verify('0\n'))
    rejected += reject(lambda: audit_pool(tile, [tile.root], 1, p[:-1], E1))
    rejected += reject(lambda: audit_pool(tile, [tile.root], 1, p+[p[0]], E1))
    return {'published_shape_index': data['shape_index'], 'E0_types': len(pool),
            'first_support': len(F), 'first_support_all_integral': True,
            'reciprocal_first_support': len(reciprocal), 'E1_types': len(E1),
            'E1_all_integral': True, 'pair_rejections': len(reciprocal)-len(E1),
            'support_RUP_steps': steps, 'pair_RUP_steps': pair_steps,
            'final_root_candidates': len(p), 'final_root_clauses': len(c),
            'certified_Hh': 1, 'status': 'known value reproduced with phase-safe peeling',
            'rejected_controls': rejected}


def main():
    here = Path(__file__).resolve().parent
    data = json.loads((here/'cases.json').read_text())
    cases = [[(0, 0)], [(0, 0), (1, 0)]] + data['published_heptominoes'] + [data['record_seed_17']]
    result = {'agent': 'six-heesch-1', 'role': 'researcher',
              'scope': 'finite contact universe and anchored compression; no new Heesch bound',
              'inventories': [inventory(cells) for cells in cases],
              'phase_fixture': phase_fixture(),
              'calibration': calibration(here, data['published_heptominoes'][2])}
    expected = here/'expected.json'
    if expected.exists():
        require(result == json.loads(expected.read_text()), 'expected summary mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
