"""Reproduce the all-color/all-state bent-four-hex cover/tiling dichotomy.

Check the twelve compact periodic tilings and the radius-four sharpness cover
without a solver. Generate the radius-five formula, or solve it with a proof.
Large generated inputs and proof traces belong in the chosen output directory.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

import color_state as cs
import equivalence_state as es
import hex_domain as hd
import marked_corona


def checked_instance(path):
    instance = json.loads(path.read_text())
    if instance['grid'] != 'hex' or instance['state_mode'] != 'all_ternary':
        raise ValueError('all-ternary hex instance required')
    tile, motifs = instance['tile'], instance['motifs']
    n = len(hd.boundary(tile))
    checks = []
    for motif in motifs:
        row = cs.check_periodic(tile, [1]*n, [0]*n, motif['patch'], *motif['period'])
        if row != motif['checks']:
            raise ValueError('stored contacts differ from independent inverse decoding')
        checks.append(row)
    return instance, checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['check', 'generate', 'solve'])
    parser.add_argument('--instance', type=Path,
                        default=Path(__file__).with_name('bend4_directed_cover_tiling.json'))
    parser.add_argument('--unmarked-source', type=Path,
                        default=Path(__file__).resolve().parent.parent/'heesch_polyomino_euler_cnf')
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    instance, motif_checks = checked_instance(args.instance)
    tile, motifs = instance['tile'], instance['motifs']
    if args.mode == 'check':
        witness = json.loads(Path(__file__).with_name('bend4_fivecolor_radius4.cover.json').read_text())
        corona = json.loads(Path(__file__).with_name('bend4_fivecolor_depth2.witness.json').read_text())
        if witness['tile'] != tile or witness['radius'] != 4 or witness['colors'] != corona['colors'] or witness['signs'] != corona['signs']:
            raise ValueError('sharpness cover differs from the previously certified finite example')
        print(json.dumps({'motifs': len(motifs), 'ports': len(hd.boundary(tile)),
                          'determinants': [x['determinant'] for x in motif_checks],
                          'boundary_incidences': [x['boundary_incidences'] for x in motif_checks],
                          'sharpness_cover': cs.check_cover(witness),
                          'known_two_coronas': cs.check_corona(corona)}, sort_keys=True, indent=2))
        return
    if args.output_dir is None:
        parser.error('--output-dir is required for generated files')
    marked_corona.check_encoding_dependencies(args.unmarked_source)
    sys.path.insert(0, str(args.unmarked_source.resolve()))
    from circuit import Circuit
    started = time.monotonic()
    circuit, candidates, pairs, signs, compatibility, stats = es.build_cover(tile, instance['radius'], Circuit)
    for motif in motifs:
        es.exclude_motif(circuit, compatibility, motif['checks']['matching_port_pairs'])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.output_dir/args.instance.stem
    cnf = prefix.with_suffix('.cnf')
    circuit.write_dimacs(cnf)
    stats.update(variables=circuit.nv, clauses=len(circuit.clauses), motifs=len(motifs),
                 cnf_sha256=hashlib.sha256(cnf.read_bytes()).hexdigest(),
                 assumptions='none', result='GENERATED')
    if args.mode == 'solve':
        from pysat.solvers import Solver
        from pysat import __version__
        stats.update(python_sat=__version__, solver='glucose4', conflict_budget=20000)
        with Solver(name='glucose4', bootstrap_with=circuit.clauses, with_proof=True) as solver:
            solver.conf_budget(20000)
            result = solver.solve_limited()
            stats.update(result='SAT' if result else 'UNSAT; independent proof checking required'
                         if result is False else 'UNKNOWN', solver_stats=solver.accum_stats())
            if result is False:
                proof = prefix.with_suffix('.drat')
                proof.write_text('\n'.join(solver.get_proof())+'\n')
                stats.update(proof_bytes=proof.stat().st_size,
                             proof_sha256=hashlib.sha256(proof.read_bytes()).hexdigest())
            elif result:
                positive = {x for x in solver.get_model() if x > 0}
                witness = es.decode_cover(tile, instance['radius'], candidates, pairs, signs, positive)
                prefix.with_suffix('.cover.json').write_text(json.dumps(witness, indent=2)+'\n')
    stats.update(seconds=round(time.monotonic()-started, 3),
                 peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    prefix.with_suffix('.summary.json').write_text(json.dumps(stats, sort_keys=True, indent=2)+'\n')
    print(json.dumps(stats, sort_keys=True, indent=2), flush=True)


if __name__ == '__main__':
    main()
