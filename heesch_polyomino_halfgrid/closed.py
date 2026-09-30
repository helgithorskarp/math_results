"""Complete first-disc search through half-grid packings and ordered phase lifts.

Negative claims require exhausted primary-model enumeration, independently
checked final UNSAT, and every canonical phase lift checked geometrically.
Guards return no theorem when a computation is incomplete.
"""
import argparse
from collections import Counter
from dataclasses import replace
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import factorial
import os
from pathlib import Path
import subprocess
import time

from halfgrid import decode_cover, double_cells, load_dependencies


def ordered_phase_count(k):
    row = [1]
    for n in range(1, k+1):
        row = [0]+[(row[j-1] if j-1 < len(row) else 0)
                   +j*(row[j] if j < len(row) else 0) for j in range(1, n+1)]
    return sum(number*factorial(j) for j, number in enumerate(row))


def ordered_labels(k):
    """Every ordered equality partition once, represented by a surjective word."""
    if k == 0:
        yield ()
    for classes in range(1, k+1):
        required = set(range(1, classes+1))
        for labels in product(range(1, classes+1), repeat=k):
            if set(labels) == required:
                yield labels


def canonical_lifts(poses):
    groups = [[i for i, p in enumerate(poses) if getattr(p, axis) % 1]
              for axis in ('tx', 'ty')]
    for xs, ys in product(ordered_labels(len(groups[0])), ordered_labels(len(groups[1]))):
        lifted = list(poses)
        for axis, indices, labels in zip(('tx', 'ty'), groups, (xs, ys)):
            for i, rank in zip(indices, labels):
                t = getattr(lifted[i], axis)
                lifted[i] = replace(lifted[i], **{axis: Fraction(t//1)+Fraction(rank, len(indices)+1)})
        yield lifted


def check_lift(tile, poses, motion, pixel_checker):
    """Require independent arrangement and raster/Euler validity to agree."""
    valid = []
    reasons = []
    try:
        motion.check_corona(tile, 1, poses, holes_last=False)
        valid.append(True);reasons.append('disc')
    except ValueError as error:
        valid.append(False);reasons.append(str(error))
    # Operational raster guard errors are incompleteness, not rejection.
    enlarged, records = motion.rasterize(tile, poses)
    try:
        pixel_checker(enlarged, 1, records, strict_disc=True, holes_last=False)
        valid.append(True)
    except ValueError:
        valid.append(False)
    if valid[0] != valid[1]:
        raise RuntimeError('independent geometry checkers disagree on a phase lift')
    holes = None
    if valid[0]:
        holes = 0
    elif reasons[0] == 'invalid prefix topology':
        # Also distinguish actual holes from a mere final-boundary pinch.
        motion.check_corona(tile, 1, poses, holes_last=True)
        relaxed = pixel_checker(enlarged, 1, records, strict_disc=True, holes_last=True)
        holes = relaxed[-1]['holes']
    return valid[0], reasons[0], holes


def census(tile, prior, motion_directory, work, checker, max_models=100, max_lifts=10000):
    cover, motion = load_dependencies(prior, motion_directory)
    from corona import check_witness
    from pysat.solvers import Solver
    work = Path(work).resolve()
    if work.is_relative_to(Path(__file__).resolve().parent):
        raise ValueError('generated output must stay outside the public source directory')
    work.mkdir(parents=True, exist_ok=True)
    enlarged = double_cells(tile)
    circuit, candidates, statistics = cover.build_cover(enlarged, 1)
    target = cover.dilation(enlarged, 1)-set(enlarged)
    assert all(target.intersection(q['cells']) for q in candidates)
    models = []
    rejected = Counter()
    lift_count = disc_lifts = holefree_lifts = 0
    holes_histogram = Counter()
    with Solver(name='glucose4', bootstrap_with=circuit.clauses, with_proof=True) as solver:
        while True:
            solver.conf_budget(10000)
            sat = solver.solve_limited()
            if sat is None:
                raise RuntimeError('UNKNOWN: primary enumeration is incomplete')
            if not sat:
                proof = solver.get_proof() or ['0']
                break
            if len(models) >= max_models:
                raise RuntimeError('model guard: primary enumeration is incomplete')
            positive = {x for x in solver.get_model() if x > 0}
            chosen = [q for q in candidates if q['variable'] in positive]
            poses, _ = decode_cover(tile, [enlarged]+[q['cells'] for q in chosen], motion)
            phase_counts = [sum(bool(getattr(p, axis)%1) for p in poses) for axis in ('tx', 'ty')]
            planned = ordered_phase_count(phase_counts[0])*ordered_phase_count(phase_counts[1])
            if lift_count+planned > max_lifts:
                raise RuntimeError('lift guard: canonical phase enumeration is incomplete')
            before = lift_count
            successful = holefree = 0
            for lifted in canonical_lifts(poses):
                valid, reason, holes = check_lift(tile, lifted, motion, check_witness)
                lift_count += 1
                if holes is not None:
                    holes_histogram[holes] += 1
                    if holes == 0:
                        holefree += 1;holefree_lifts += 1
                if valid:
                    successful += 1;disc_lifts += 1
                else:
                    rejected[reason] += 1
            assert lift_count-before == planned
            selections = tuple(q['variable'] for q in chosen)
            assert selections
            models.append({'selected_variables': selections, 'phase_counts': phase_counts,
                           'canonical_lifts': planned, 'valid_disc_lifts': successful,
                           'valid_holefree_lifts': holefree})
            # Every candidate contains a required target cell. All such cells
            # are already uniquely occupied, so no satisfying proper superset
            # of this model exists. This short block removes exactly this model.
            solver.add_clause([-z for z in selections])
    models.sort(key=lambda q: q['selected_variables'])
    circuit.clauses.extend([[-z for z in q['selected_variables']] for q in models])
    formula, trace = work/'closed_exhaust.cnf', work/'closed_exhaust.drat'
    circuit.write_dimacs(formula)
    trace.write_text('\n'.join(proof)+'\n')
    env = os.environ.copy()
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[name] = '1'
    run = subprocess.run([str(Path(checker).resolve()), str(formula), str(trace)],
                         capture_output=True, text=True, timeout=30, env=env)
    log = run.stdout.replace('\r', '\n')
    (work/'closed_checker.log').write_text(log+run.stderr)
    if run.returncode not in (0, 1) or 's VERIFIED' not in log.splitlines():
        raise RuntimeError('final primary census contradiction not verified')
    result = {'agent': 'six-heesch-1', 'role': 'researcher',
              'primary_models': len(models), 'models': models,
              'canonical_lifts_checked_twice': lift_count, 'valid_disc_lifts': disc_lifts,
              'valid_holefree_lifts': holefree_lifts,
              'valid_relaxed_lifts_by_holes': {str(k): v for k, v in sorted(holes_histogram.items())},
              'rejected_by_arrangement_reason': dict(sorted(rejected.items())),
              'final_primary_unsat_verified': True,
              'final_cnf_sha256': hashlib.sha256(formula.read_bytes()).hexdigest(),
              'native_proof_sha256': hashlib.sha256(trace.read_bytes()).hexdigest(),
              'native_proof_bytes': trace.stat().st_size,
              'scope': 'complete unrestricted first-disc existence; plane tiling needs its separate obstruction'}
    (work/'closed_result.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    return result


def main():
    a = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parent.parent
    a.add_argument('--prior-dir', type=Path, default=root/'heesch_polyomino_euler_cnf')
    a.add_argument('--motion-dir', type=Path, default=root/'heesch_polyomino_motion_bridge')
    a.add_argument('--examples', type=Path, default=Path(__file__).parent/'fractional_examples.json')
    a.add_argument('--expected', type=Path, default=Path(__file__).parent/'closed_expected.json')
    a.add_argument('--checker', type=Path, required=True)
    a.add_argument('--work-dir', type=Path, required=True)
    a.add_argument('--write-expected', action='store_true')
    args = a.parse_args()
    start = time.monotonic()
    cases = []
    for example in json.loads(args.examples.read_text())['cases']:
        result = census(example['cells'], args.prior_dir, args.motion_dir,
                        args.work_dir/str(example['i']), args.checker)
        result['i'] = example['i']
        cases.append(result)
    encoded = json.dumps({'agent': 'six-heesch-1', 'role': 'researcher', 'cases': cases},
                         sort_keys=True, indent=2)+'\n'
    if args.write_expected:
        args.expected.write_text(encoded)
    else:
        expected = json.loads(args.expected.read_text())
        # Complete model sets and geometry counts are canonical. A different
        # valid native proof may be emitted by another compatible platform.
        actual_cases = json.loads(encoded)['cases']
        for actual, wanted in zip(actual_cases, expected['cases']):
            for key in ('native_proof_sha256', 'native_proof_bytes'):
                actual.pop(key);wanted.pop(key)
        assert len(actual_cases)==len(expected['cases']) and actual_cases==expected['cases'], 'closed census mismatch'
    print(encoded, end='')
    print(json.dumps({'seconds': round(time.monotonic()-start, 3)}))


if __name__ == '__main__':
    main()
