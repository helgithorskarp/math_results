"""Direct rational and pixel/Euler checks of the three explicit lower witnesses.

No solver verdict or phase-collapse statement is used to validate a surround.
The finite upper is conditional on the separately checked coarse obstruction.
"""
import argparse
import json
from pathlib import Path
import time

from halfgrid import load_dependencies


def check(prior, motion_directory, examples):
    _, motion = load_dependencies(prior, motion_directory)
    from corona import check_witness
    result = []
    for example in examples['cases']:
        tile = motion.normalize(example['cells'])
        poses = motion.load_poses(tile, example['placements'])
        rational = motion.check_corona(tile, 1, poses, holes_last=True)
        enlarged, records = motion.rasterize(tile, poses)
        pixels = check_witness(enlarged, 1, records, strict_disc=True, holes_last=True)
        upper = motion.unrestricted_upper(tile, 1)
        assert upper == example['conditional_unrestricted_upper']
        assert len(tile) == 20 and len(poses) == 8
        fractional = sum(bool(p.tx % 1 or p.ty % 1) for p in poses)
        assert fractional > 0
        assert all(p.tx.denominator in (1, 2) and p.ty.denominator in (1, 2) for p in poses)
        result.append({'i': example['i'], 'cells': len(tile), 'copies': len(poses),
                       'fractional_copies': fractional,
                       'rational_prefixes': rational, 'pixel_prefixes': pixels,
                       'conditional_unrestricted_upper': upper,
                       'exact_Hh_claimed': False, 'disc_corona_claimed': rational[-1]['disc']})
    return {'agent': 'six-heesch-1', 'role': 'researcher',
            'scope': 'definition-level positive geometry; upper requires coarse obstruction',
            'cases': result}


def main():
    a = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parent.parent
    a.add_argument('--prior-dir', type=Path, default=root/'heesch_polyomino_euler_cnf')
    a.add_argument('--motion-dir', type=Path, default=root/'heesch_polyomino_motion_bridge')
    a.add_argument('--examples', type=Path, default=Path(__file__).parent/'fractional_examples.json')
    a.add_argument('--expected', type=Path, default=Path(__file__).parent/'examples_expected.json')
    a.add_argument('--write-expected', action='store_true')
    args = a.parse_args()
    start = time.monotonic()
    result = check(args.prior_dir, args.motion_dir, json.loads(args.examples.read_text()))
    encoded = json.dumps(result, sort_keys=True, indent=2)+'\n'
    if args.write_expected:
        args.expected.write_text(encoded)
    else:
        assert result == json.loads(args.expected.read_text()), 'examples expected mismatch'
    print(encoded, end='')
    print(json.dumps({'seconds': round(time.monotonic()-start, 3)}))


if __name__ == '__main__':
    main()
