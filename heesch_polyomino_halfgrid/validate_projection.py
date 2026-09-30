"""All 65536 projected selection assignments for the doubled monomino.

The reference computes union and nonoverlap of full cell footprints by integers,
then compares with SAT after fixing only the 16 primary selection variables.
No auxiliary-gate evaluation or partial-model convention is borrowed.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import time

from halfgrid import double_cells, load_dependencies


def verify(prior, motion_directory):
    cover, motion = load_dependencies(prior, motion_directory)
    from pysat.solvers import Solver
    tile = double_cells([(0, 0)])
    circuit, candidates, _ = cover.build_cover(tile, 1)
    assert len(candidates) == 16
    cells = sorted(set(tile).union(*(q['cells'] for q in candidates)))
    indices = {p: i for i, p in enumerate(cells)}

    def bitset(points):
        return sum(1 << indices[p] for p in points)

    root = bitset(tile)
    # The metric target is explicitly the four-by-four root neighbourhood.
    target = bitset((x, y) for x in range(-1, 3) for y in range(-1, 3))
    footprints = [bitset(q['cells']) for q in candidates]
    variables = [q['variable'] for q in candidates]
    counts = Counter()
    with Solver(name='glucose4', bootstrap_with=circuit.clauses) as solver:
        for mask in range(1 << len(candidates)):
            occupied = root
            selected = []
            valid = True
            assumptions = []
            for j, (footprint, variable) in enumerate(zip(footprints, variables)):
                take = bool(mask & (1 << j))
                assumptions.append(variable if take else -variable)
                if take:
                    valid &= not bool(occupied & footprint)
                    occupied |= footprint
                    selected.append(candidates[j]['cells'])
            valid &= occupied & target == target
            sat = solver.solve(assumptions=assumptions)
            assert sat == valid, 'projection mismatch at '+str(mask)
            if valid:
                counts[len(selected)] += 1
                _, statistics = __import__('halfgrid').decode_cover([(0, 0)], [tile]+selected, motion)
                assert len(statistics) == 2
    return {'agent': 'six-heesch-1', 'role': 'researcher',
            'scope': 'complete primary-selection projection for doubled monomino only',
            'selection_variables': 16, 'projected_assignments': 65536,
            'matching_assignments': 65536,
            'valid_models_by_new_copies': {str(k): v for k, v in sorted(counts.items())},
            'every_positive_model_directly_decoded': True}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parent.parent
    p.add_argument('--prior-dir', type=Path, default=root/'heesch_polyomino_euler_cnf')
    p.add_argument('--motion-dir', type=Path, default=root/'heesch_polyomino_motion_bridge')
    p.add_argument('--expected', type=Path, default=Path(__file__).parent/'projection_expected.json')
    p.add_argument('--write-expected', action='store_true')
    args = p.parse_args()
    start = time.monotonic()
    result = verify(args.prior_dir, args.motion_dir)
    encoded = json.dumps(result, sort_keys=True, indent=2)+'\n'
    if args.write_expected:
        args.expected.write_text(encoded)
    else:
        assert result == json.loads(args.expected.read_text()), 'projection expected mismatch'
    print(encoded, end='')
    print(json.dumps({'seconds': round(time.monotonic()-start, 3)}))


if __name__ == '__main__':
    main()
