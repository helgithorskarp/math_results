"""Reproduce exact finite diagnostics, using only the Python standard library."""
import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
import sys

from motion import (Pose, arrangement, check_corona, check_covering, check_dependency, contact_graph,
                    floor_poses, load_poses, mesh_denominator, normalize,
                    phase_compress, rasterize, unrestricted_upper)


def rejected(fn):
    try:
        fn()
    except ValueError as exc:
        return str(exc)
    raise AssertionError("invalid input was accepted")


def validate():
    base = Path(__file__).parent
    raw = json.loads((base/'fractional_square.json').read_text())
    tile = normalize(raw['cells'])
    original = load_poses(tile, raw['patch'])
    budget = mesh_denominator(tile, raw['depth'])
    moved = phase_compress(original, budget)
    first = check_corona(tile, raw['depth'], original)
    second = check_corona(tile, raw['depth'], moved)
    assert first == second
    assert contact_graph(original) == contact_graph(moved)
    assert all((t*budget).denominator == 1 for p in moved for t in (p.tx, p.ty))
    failed_floor = rejected(lambda: check_corona(tile, 1, floor_poses(original)))
    assert failed_floor == 'incomplete surround'

    # Whole-cell coverage is stronger than an infinitesimal surround.
    failed_cell = rejected(lambda: check_covering(original, [(1, 1)]))
    assert failed_cell == 'incomplete whole-cell coverage'

    values = [Fraction(n)+Fraction(f, 5) for n in range(-2, 3) for f in range(5)]
    inequalities = 0
    for x, y, n in product(values, values, range(-3, 4)):
        if x-y <= n:
            assert x//1-y//1 <= n
            inequalities += 1

    # Direct unit-rectangle separation versus compressed-grid occupancy.
    coords = [Fraction(n)+Fraction(f, 3) for n in (-1, 0, 1) for f in range(3)]
    positions = list(product(coords, repeat=2))
    separated = 0
    for (x, y), (u, v) in combinations(positions, 2):
        if abs(x-u) >= 1 or abs(y-v) >= 1:
            pair = [Pose(0, tile, x, y), Pose(0, tile, u, v)]
            arrangement(floor_poses(pair))
            separated += 1

    # Unit-periodic rank compression preserves all endpoint orders, not just
    # the contacts which happened to occur in the seven-square example.
    phases = [Fraction(0), Fraction(1, 7), Fraction(2, 7), Fraction(5, 7), Fraction(6, 7)]
    coordinate_list = [n+f for n in range(-2, 3) for f in phases]
    dummy = [Pose(0, tile, q, -q) for q in coordinate_list]
    compressed = phase_compress(dummy, 11)
    order_pairs = 0
    for axis in ('tx', 'ty'):
        for i, j in product(range(len(dummy)), repeat=2):
            a, b = getattr(dummy[i], axis), getattr(dummy[j], axis)
            c, d = getattr(compressed[i], axis), getattr(compressed[j], axis)
            assert (a < b, a == b) == (c < d, c == d)
            order_pairs += 1

    # Four shapes with shifted rectangular lattice covers. Every target is
    # covered in the continuum, and coordinate flooring covers it exactly.
    whole_covers = 0
    for w, h in [(1, 1), (2, 1), (1, 2), (2, 2)]:
        shape = tuple(product(range(w), range(h)))
        target = list(shape)
        for a, b in product(range(5), repeat=2):
            poses = [Pose(0, shape, Fraction(i*w)+Fraction(a, 5),
                          Fraction(j*h)+Fraction(b, 5)) for i, j in product((-1, 0), repeat=2)]
            check_covering(poses, target)
            check_covering(floor_poses(poses), target)
            whole_covers += 1

    # The rows above and below an integer root can carry independent phases.
    rooted_covers = 0
    target = list(product(range(-1, 2), repeat=2))
    for a, b in product(range(5), repeat=2):
        poses = []
        for row, phase in [(-1, Fraction(a, 5)), (0, Fraction(0)), (1, Fraction(b, 5))]:
            poses += [Pose(0, tile, Fraction(col)+phase, Fraction(row)) for col in range(-2, 3)]
        check_covering(poses, target)
        check_covering(floor_poses(poses), target)
        assert any(p.tx == p.ty == 0 for p in poses)
        rooted_covers += 1

    bad = [
        rejected(lambda: phase_compress(original, 1)),
        rejected(lambda: check_corona(tile, 1, original[:-1])),
        rejected(lambda: check_corona(tile, 1, original+[original[0]])),
        rejected(lambda: check_corona(tile, 1, [Pose(0, tile, Fraction(1, 3), Fraction(0)), *original[1:]])),
        rejected(lambda: check_covering([original[0], original[0]], [(0, 0)])),
    ]
    return {'agent': 'six-heesch-1', 'role': 'researcher',
            'scope': 'finite exact diagnostics; universal geometry is proved in proof.md',
            'fractional_example': {'copy_budget': budget, 'copies': len(original),
                                   'prefixes': first, 'compressed_prefixes': second,
                                   'contact_graph_preserved': True,
                                   'flooring_corona_failure': failed_floor,
                                   'whole_cell_requirement_detected': failed_cell},
            'integer_threshold_floor_inequalities': inequalities,
            'nonoverlap_floor_pairs': separated,
            'phase_order_pairs': order_pairs,
            'shifted_rectangular_whole_covers': whole_covers,
            'rooted_independent_row_covers': rooted_covers,
            'invalid_inputs_rejected': len(bad)}


def crosscheck(prior):
    """Compare the separate boundary-graph checker with prior pixel geometry."""
    check_dependency(prior)
    sys.path.insert(0, str(prior.resolve()))
    from corona import check_witness
    base = Path(__file__).parent
    raw = json.loads((base/'fractional_square.json').read_text())
    tile = normalize(raw['cells'])
    poses = load_poses(tile, raw['patch'])
    checks = []
    for name, moved in [('original', poses), ('compressed', phase_compress(poses, mesh_denominator(tile, 1)))]:
        pixel_tile, patch = rasterize(tile, moved)
        checks.append({'name': name, 'prefixes': check_witness(pixel_tile, 1, patch)})

    seed = json.loads((prior/'kaplan17.json').read_text())['cells']
    records = json.loads((prior/'kaplan17_depth3.witness.json').read_text())['patch']
    poses = []
    for r in records:
        tx, ty = min(x for x, y in r['cells']), min(y for x, y in r['cells'])
        poses.append(Pose(r['level'], normalize(r['cells']), Fraction(tx), Fraction(ty)))
    arrangement_stats = check_corona(seed, 3, poses)
    assert [x['tiles'] for x in arrangement_stats] == [1, 6, 12, 17]
    assert contact_graph(poses) == contact_graph(phase_compress(poses, mesh_denominator(seed, 3)))
    graph = contact_graph(poses)
    for i, ns in enumerate(graph):
        assert all(abs(poses[i].level-poses[j].level) <= 1 for j in ns)
    root = next(i for i, p in enumerate(poses) if p.level == 0)
    distances = {root: 0}
    frontier = [root]
    for i in frontier:
        for j in graph[i]:
            if j not in distances:
                distances[j] = distances[i]+1
                frontier.append(j)
    assert len(distances) == len(poses)
    assert all(distances[i] == p.level for i, p in enumerate(poses))
    pixel_tile, patch = rasterize(seed, poses)
    check_witness(pixel_tile, 3, patch)
    return {'pixel_geometry_comparisons': checks, 'kaplan17': {
        'independent_arrangement_prefixes': arrangement_stats,
        'copies': len(poses), 'mesh_budget': mesh_denominator(seed, 3),
        'conditional_upper_from_blocking_radius10': unrestricted_upper(seed, 10),
        'contact_edges': sum(map(len, graph))//2,
        'contact_distances_equal_levels': True,
        'nonconsecutive_contacts_absent': True}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prior-dir', type=Path)
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    result = validate()
    if args.prior_dir:
        result['dependency_crosscheck'] = crosscheck(args.prior_dir)
    if args.expected:
        assert result == json.loads(args.expected.read_text()), 'expected output mismatch'
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
