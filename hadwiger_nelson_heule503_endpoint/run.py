#!/usr/bin/env python3
"""One frozen exact graph decision; no adaptive follow-up query."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'hadwiger_nelson_heule632_pair_pilot'))
import build as B
import independent as I


def save(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    temporary.replace(path)


def native(command, logfile, timeout, limits):
    def bounds():
        resource.setrlimit(resource.RLIMIT_AS, (limits['address_space_bytes'],) * 2)
        resource.setrlimit(resource.RLIMIT_FSIZE, (limits['output_file_bytes'],) * 2)
    start = time.monotonic()
    with logfile.open('wb') as log:
        try:
            process = subprocess.run(list(map(str, command)), stdout=log, stderr=subprocess.STDOUT,
                                     timeout=timeout, preexec_fn=bounds)
            code = process.returncode
        except subprocess.TimeoutExpired:
            code = None
    return code, time.monotonic() - start


def run(out, kissat, checker):
    start = time.monotonic()
    plan = json.loads((HERE / 'plan.json').read_text())
    for name, digest in plan['input_files'].items():
        I.check(sha256((ROOT / name).read_bytes()).hexdigest() == digest, 'input identity')
    for executable, kind in ((kissat, 'solver'), (checker, 'checker')):
        I.check(sha256(executable.read_bytes()).hexdigest() == plan[kind]['sha256'], 'frozen executable')
    _, edges, _ = B.geometry()
    _, other, _ = I.geometry()
    I.check(edges == other, 'complete independent unit graph')
    clauses, raw, vertices, triangle = B.formula(plan['retained'], edges, 4)
    I.check(raw == I.formula(vertices, other, 4)[1] and sha256(raw).hexdigest() == plan['cnf_sha256'], 'independent frozen CNF')
    I.check(len(vertices) == 503 and triangle == plan['triangle'], 'frozen support')
    out.mkdir(parents=True, exist_ok=False)
    cnf, proof, log = out / 'four.cnf', out / 'four.drat', out / 'four.log'
    cnf.write_bytes(raw)
    save(out / 'checkpoint.json', {'phase': 'ONE COLOURING QUERY IN FLIGHT', 'vertices': 503})
    code, elapsed = native([kissat, *plan['solver']['options'], cnf, proof], log, plan['solver']['outer_seconds'], plan['limits'])
    output = log.read_text()
    status = ('SAT' if code == 10 and 's SATISFIABLE' in output.splitlines() else
              'UNSAT' if code == 20 and 's UNSATISFIABLE' in output.splitlines() else 'UNKNOWN')
    certificate = {'status': status, 'vertices': 503, 'edges': plan['edges'], 'retained': vertices,
                   'endpoint_vertices': plan['endpoint_vertices'], 'four_cnf_sha256': sha256(raw).hexdigest(),
                   'whole560_family_closed': False, 'record_improvement': False}
    if status == 'SAT':
        colours = B.decode(output, vertices, 4, clauses)
        checked = B.check_colouring(colours, vertices, edges, 4)
        text = ''.join(str(colours[v]) if v in colours else '.' for v in range(632))
        I.check(I.colouring(text, sorted(set(range(632)) - set(vertices)), other, 4) == checked, 'independent edge witness')
        certificate.update(four_colouring=text, four_colouring_edge_checks=checked, chromatic_number_upper_bound=4)
    elif status == 'UNSAT':
        save(out / 'checkpoint.json', {'phase': 'NEGATIVE PROOF CHECK IN FLIGHT', 'vertices': 503})
        check_code, check_seconds = native([checker, cnf, proof, *plan['checker']['options']], out / 'drat.log', plan['checker']['outer_seconds'], plan['limits'])
        I.check(check_code == 0 and 's VERIFIED' in (out / 'drat.log').read_text().splitlines(), 'real DRAT verification required')
        inherited = json.loads((ROOT / 'hadwiger_nelson_heule632_minimize/certificate.json').read_text())['five_colouring']
        text = ''.join(c if v in vertices else '.' for v, c in enumerate(inherited))
        checked = I.colouring(text, sorted(set(range(632)) - set(vertices)), other, 5)
        certificate.update(status='UNSAT_VERIFIED', chromatic_number=5, five_colouring=text,
                           five_colouring_edge_checks=checked, proof_bytes=proof.stat().st_size,
                           proof_sha256=sha256(proof.read_bytes()).hexdigest(), checker_seconds=check_seconds,
                           record_improvement=True)
    save(out / 'certificate.json', certificate)
    result = {'status': certificate['status'], 'native_colouring_queries': 1, 'solver_exit_code': code,
              'solver_seconds': elapsed, 'elapsed_seconds': time.monotonic() - start,
              'vertices': 503, 'edges': plan['edges'], 'record_improvement': certificate['record_improvement'],
              'whole560_family_closed': False, 'additional_support_queried': False}
    save(out / 'result.json', result)
    save(out / 'checkpoint.json', {'phase': 'BOUNDED DECISION COMPLETE', 'result': result})
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--kissat', type=Path, required=True)
    parser.add_argument('--drat-trim', type=Path, required=True)
    args = parser.parse_args()
    run(args.out, args.kissat, args.drat_trim)
