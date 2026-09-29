"""Independent small exact-cover checks for the finite covering reduction."""
import json
from pathlib import Path

from cover import build_cover, check_cover
from circuit import Circuit
from corona import at_most_one, normalize, orientations
from periodic import check_periodic, find_periodic
from topology import FOUR, flood_counts, local_counts


def independent_variants(tile):
    maps = (lambda x, y: (x, y), lambda x, y: (-y, x),
            lambda x, y: (-x, -y), lambda x, y: (y, -x),
            lambda x, y: (-x, y), lambda x, y: (y, x),
            lambda x, y: (x, -y), lambda x, y: (-y, -x))
    out = set()
    for transform in maps:
        moved = [transform(x, y) for x, y in tile]
        x0, y0 = min(x for x, y in moved), min(y for x, y in moved)
        out.add(tuple(sorted((x - x0, y - y0) for x, y in moved)))
    return sorted(out)


def reference_target(tile, radius):
    return {(x, y)
            for x in range(min(a for a, b in tile) - radius,
                           max(a for a, b in tile) + radius + 1)
            for y in range(min(b for a, b in tile) - radius,
                           max(b for a, b in tile) + radius + 1)
            if any(abs(x - a) <= radius and abs(y - b) <= radius for a, b in tile)}


def reference_copies(tile, radius):
    """Anchor a copy cell at each target cell, without a candidate-envelope bound."""
    root = set(tile)
    target = reference_target(tile, radius)
    copies = set()
    for shape in independent_variants(tile):
        shifts = {(x - a, y - b) for x, y in target - root for a, b in shape}
        for tx, ty in shifts:
            cells = tuple(sorted((a + tx, b + ty) for a, b in shape))
            if not root.intersection(cells):
                copies.add(cells)
    return target, sorted(copies)


def reference_cover(tile, radius):
    """Direct exact-cover backtracking on occupied cells, independent of CNF."""
    target, copies = reference_copies(tile, radius)
    universe = sorted(target | set(tile) | set().union(*(set(q) for q in copies)))
    positions = {p: i for i, p in enumerate(universe)}

    def mask(cells):
        return sum(1 << positions[p] for p in cells)

    footprints = [mask(q) for q in copies]
    root_mask = mask(tile)
    wanted = mask(target) & ~root_mask
    coverers = {positions[p]: [i for i, q in enumerate(copies) if p in q]
                for p in target - set(tile)}
    nodes = 0
    failed = set()

    def search(remaining, occupied):
        nonlocal nodes
        nodes += 1
        if nodes > 500000:
            raise RuntimeError('reference search incomplete; no validation conclusion')
        if not remaining:
            return []
        if occupied in failed:
            return None
        pivot = None
        bits = remaining
        while bits:
            low = bits & -bits
            options = [i for i in coverers[low.bit_length() - 1]
                       if not footprints[i] & occupied]
            if not options:
                failed.add(occupied)
                return None
            if pivot is None or len(options) < len(pivot):
                pivot = options
            bits -= low
        pivot.sort(key=lambda i: (-(footprints[i] & remaining).bit_count(), i))
        for i in pivot:
            result = search(remaining & ~footprints[i], occupied | footprints[i])
            if result is not None:
                return [i] + result
        failed.add(occupied)
        return None

    result = search(wanted, root_mask)
    if result is not None:
        check_cover(tile, radius, [tile] + [copies[i] for i in result])
    return result is not None, nodes


def main():
    from pysat.solvers import Solver
    layer = {((0, 0),)}
    shapes = []
    for size in range(1, 6):
        shapes.extend(sorted(layer))
        enlarged = set()
        for tile in layer:
            cells = set(tile)
            boundary = {(x + dx, y + dy) for x, y in cells for dx, dy in FOUR} - cells
            for p in boundary:
                enlarged.add(min(independent_variants(cells | {p})))
        layer = enlarged
    assert len(shapes) == 21
    fixture = json.loads((Path(__file__).parent / 'fixtures.json').read_text())['cells']
    cases = [(tile, r) for tile in shapes for r in range(3)]
    cases.extend((normalize(fixture), r) for r in (1, 2))
    total_nodes = 0
    sat_count = 0
    for tile, radius in cases:
        assert orientations(tile) == independent_variants(tile)
        target, copies = reference_copies(tile, radius)
        circuit, candidates, stats = build_cover(tile, radius)
        assert stats['target_cells'] == len(target)
        assert sorted(q['cells'] for q in candidates) == copies
        expected, nodes = reference_cover(tile, radius)
        total_nodes += nodes
        with Solver(name='glucose4', bootstrap_with=circuit.clauses) as solver:
            actual = solver.solve()
        assert actual == expected
        sat_count += actual
    # Deliberately corrupted raw witnesses must fail the geometry checker.
    for patch in ([], [((0, 0),), ((0, 0),)], [((1, 0),)]):
        try:
            check_cover([(0, 0)], 0, patch)
        except ValueError:
            pass
        else:
            raise AssertionError('malformed patch accepted')
    # Removing outside-target AMO constraints admits a false covering witness.
    tile = normalize(fixture)
    target, copies = reference_copies(tile, 1)
    collision = [((-4, 0), (-4, 1), (-4, 2), (-3, 2), (-3, 3), (-2, 2), (-1, 2)),
                 ((-4, -1), (-4, 0), (-4, 1), (-3, 1), (-3, 2), (-2, 1), (-1, 1))]
    shared = set(collision[0]) & set(collision[1])
    assert shared and not shared & target
    circuit, candidates, _ = build_cover(tile, 1)
    selected = {q['cells']: q['variable'] for q in candidates}
    with Solver(name='glucose4', bootstrap_with=circuit.clauses) as solver:
        assert solver.solve()  # A genuine covering exists.
        assert not solver.solve(assumptions=[selected[q] for q in collision])
    weak = Circuit()
    weak_vars = {q: weak.new() for q in copies}
    for p in sorted(target - set(tile)):
        covering = [weak_vars[q] for q in copies if p in q]
        weak.clause(covering)
        at_most_one(weak, covering)
    for q in collision:
        weak.clause([weak_vars[q]])
    with Solver(name='glucose4', bootstrap_with=weak.clauses) as solver:
        assert solver.solve()
        positive = {z for z in solver.get_model() if z > 0}
        patch = [tile] + [q for q in copies if weak_vars[q] in positive]
    try:
        check_cover(tile, 1, patch)
    except ValueError as error:
        assert 'overlapping' in str(error)
    else:
        raise AssertionError('outside-target overlap was missed')

    periodic_positive = 0
    for tile in shapes:
        cert, _ = find_periodic(tile, count=2)
        if cert:
            check_periodic(tile, cert)
            periodic_positive += 1
    rect = ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1))
    cert, _ = find_periodic(rect, count=1)
    assert cert and check_periodic(rect, cert)['determinant'] == 6
    tri = ((0, 0), (0, 1), (1, 0))
    bad_certificates = [(tri, {'a': 1, 'b': 0, 'c': 6,
                             'copies': [tri, tuple((x + 2, y) for x, y in tri)]}),
                        (rect, {'a': 0, 'b': 0, 'c': 6, 'copies': [rect]})]
    for bad_tile, bad in bad_certificates:
        try:
            check_periodic(bad_tile, bad)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid periodic certificate accepted')
    print(json.dumps({'cases': len(cases), 'sat': sat_count,
                      'unsat': len(cases) - sat_count, 'reference_nodes': total_nodes,
                      'candidate_sets_exactly_match': True,
                      'malformed_witnesses_rejected': 3,
                      'outside_target_overlap_mutation_detected': True,
                      'periodic_positive_certificates': periodic_positive,
                      'invalid_periodic_certificates_rejected': 2}, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
