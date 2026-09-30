"""Check compact periodic motifs and reproduce their cover/tiling certificate.

The large CNF and proof are regenerated into an explicitly chosen directory.
No proof trace, solver environment or private ledger belongs in the source.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

import color_state as cs
import hex_domain as hd
import marked_corona


def checked_instance(path):
    instance = json.loads(path.read_text())
    if instance['grid'] != 'hex' or instance['state_mode'] != 'all_zero':
        raise ValueError('this published certificate covers zero-state polyhexes')
    tile, motifs = instance['tile'], instance['motifs']
    n = len(hd.boundary(tile))
    initial = instance['initial_motifs']
    if type(initial) is not int or not 1 <= initial <= len(motifs):
        raise ValueError('invalid initial motif count')
    result = []
    for motif in motifs:
        checks = cs.check_periodic(tile, [1] * n, [0] * n,
                                   motif['patch'], *motif['period'])
        if checks != motif['checks']:
            raise ValueError('stored motif data differs from direct inverse decoding')
        result.append(checks)
    return instance, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['check', 'generate', 'replay', 'check-corona', 'exclude-third'])
    parser.add_argument('--instance', type=Path)
    parser.add_argument('--unmarked-source', type=Path,
                        default=Path(__file__).resolve().parent.parent / 'heesch_polyomino_euler_cnf')
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    if args.instance is None:
        filename = 'bend4_fivecolor_depth2.witness.json' if args.mode in ('check-corona', 'exclude-third') else 'bend4_cover_tiling.json'
        args.instance = Path(__file__).with_name(filename)
    if args.mode in ('check-corona', 'exclude-third'):
        witness = json.loads(args.instance.read_text())
        checks = cs.check_corona(witness)
        if args.mode == 'check-corona':
            print(json.dumps(checks, sort_keys=True, indent=2))
            return
        if witness['depth'] != 2 or args.output_dir is None:
            parser.error('a two-corona fixture and --output-dir are required')
        marked_corona.check_encoding_dependencies(args.unmarked_source)
        sys.path.insert(0, str(args.unmarked_source.resolve()))
        from circuit import Circuit
        from pysat.solvers import Solver
        from pysat import __version__
        circuit, _, stats = cs.build_corona(witness['tile'], 3, witness['colors'], witness['signs'], Circuit)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        output = args.output_dir / 'bend4_fivecolor_depth3'
        cnf = output.with_suffix('.cnf')
        circuit.write_dimacs(cnf)
        stats.update(cnf_sha256=hashlib.sha256(cnf.read_bytes()).hexdigest(),
                     python_sat=__version__, solver='glucose4', conflict_budget=20000)
        with Solver(name='glucose4', bootstrap_with=circuit.clauses, with_proof=True) as solver:
            solver.conf_budget(20000)
            result = solver.solve_limited()
            stats.update(result='SAT' if result else 'UNSAT; independent proof checking required' if result is False else 'UNKNOWN',
                         solver_stats=solver.accum_stats())
            if result is False:
                proof = output.with_suffix('.drat')
                proof.write_text('\n'.join(solver.get_proof())+'\n')
                stats.update(proof_bytes=proof.stat().st_size,
                             proof_sha256=hashlib.sha256(proof.read_bytes()).hexdigest())
        output.with_suffix('.summary.json').write_text(json.dumps(stats,sort_keys=True,indent=2)+'\n')
        print(json.dumps(stats,sort_keys=True,indent=2),flush=True)
        return
    instance, motif_checks = checked_instance(args.instance)
    tile, motifs = instance['tile'], instance['motifs']
    n = len(hd.boundary(tile))
    if args.mode == 'check':
        print(json.dumps({'motifs': len(motifs), 'ports': n,
                          'determinants': [c['determinant'] for c in motif_checks],
                          'boundary_incidences': [c['boundary_incidences'] for c in motif_checks],
                          'original_port_inverse_decoding': True}, sort_keys=True, indent=2))
        return
    if args.output_dir is None:
        parser.error('--output-dir is required for generated CNF/proof files')
    marked_corona.check_encoding_dependencies(args.unmarked_source)
    sys.path.insert(0, str(args.unmarked_source.resolve()))
    from circuit import Circuit
    started = time.monotonic()
    circuit, _, bits, signs, stats = cs.build_cover_synthesis(tile, instance['radius'], Circuit, [0] * n)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / args.instance.stem

    def add(motif):
        cs.exclude_periodic_pairs(circuit, bits, signs, motif['checks']['matching_port_pairs'])

    if args.mode == 'generate':
        for motif in motifs:
            add(motif)
        result, trace = None, []
    else:
        from pysat.solvers import Solver
        from pysat import __version__
        stats.update(python_sat=__version__, solver='glucose4', conflicts_per_distinct_input=20000,
                     assumptions='none')
        initial = instance['initial_motifs']
        for motif in motifs[:initial]:
            add(motif)
        trace = []
        with Solver(name='glucose4', bootstrap_with=circuit.clauses, with_proof=True) as solver:
            for step in range(initial, len(motifs) + 1):
                solver.conf_budget(20000)
                result = solver.solve_limited()
                row = {'motifs': step,
                       'result': 'SAT' if result else 'UNSAT' if result is False else 'UNKNOWN',
                       'solver_stats': solver.accum_stats()}
                trace.append(row)
                print(json.dumps(row), flush=True)
                if result is not True or step == len(motifs):
                    break
                old = len(circuit.clauses)
                add(motifs[step])
                for clause in circuit.clauses[old:]:
                    solver.add_clause(clause)
            if result is False:
                proof = output.with_suffix('.drat')
                proof.write_text('\n'.join(solver.get_proof()) + '\n')
                stats.update(proof_bytes=proof.stat().st_size,
                             proof_sha256=hashlib.sha256(proof.read_bytes()).hexdigest())
            # Even an earlier UNSAT prefix proves the full formula UNSAT.
            # Complete its fixed original input so hashes are mode invariant.
            for motif in motifs[step:]:
                add(motif)
    cnf = output.with_suffix('.cnf')
    circuit.write_dimacs(cnf)
    stats.update(variables=circuit.nv, clauses=len(circuit.clauses), motifs=len(motifs),
                 initial_motifs=instance['initial_motifs'],
                 cnf_sha256=hashlib.sha256(cnf.read_bytes()).hexdigest(),
                 result='GENERATED' if args.mode == 'generate' else (
                     'SAT' if result else 'UNSAT; independent proof checking required' if result is False else 'UNKNOWN'),
                 trace=trace, seconds=round(time.monotonic()-started,3),
                 peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    output.with_suffix('.summary.json').write_text(json.dumps(stats,sort_keys=True,indent=2)+'\n')
    print(json.dumps(stats,sort_keys=True,indent=2),flush=True)


if __name__ == '__main__':
    main()
