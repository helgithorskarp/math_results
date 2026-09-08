"""Audit the entire decision table; optionally recheck all actual proofs."""
import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path
import audit
import encode

HERE = Path(__file__).resolve().parent

def proof_path(directory, result):
    if 'proof_file' in result:
        name = result['proof_file']
        audit.require(name in ('tail.drat.bin', 'tail.drat'), 'Unexpected proof filename')
        return directory / name
    paths = [directory / name for name in ('tail.drat.bin', 'tail.drat') if (directory / name).is_file()]
    audit.require(len(paths) == 1, 'Exactly one proof required')
    return paths[0]

def check_proof(checker, cnf, proof):
    run = subprocess.run([str(checker), str(cnf), str(proof)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    audit.require(run.returncode == 0 and 's VERIFIED' in run.stdout.decode().splitlines(), 'Proof checker rejected input')
    return hashlib.sha256(run.stdout).hexdigest()

def verify(catalog, run_root=None, checker=None):
    lines = encode.catalog(catalog)
    records = json.loads((HERE / 'RESULTS.json').read_text())
    witnesses = json.loads((HERE / 'TAIL_WITNESSES.json').read_text())
    audit.require([r['index'] for r in records] == list(range(640)), 'Complete ordered core coverage')
    total_clauses = total_tests = 0
    negative = []
    positive = []
    for row in records:
        i = row['index']
        raw = encode.dimacs(encode.decode(lines[i]))
        result = audit.formula(lines[i], raw)
        audit.require(result['sha256'] == row['cnf_sha256'] and result['clauses'] == row['clauses'], 'Recorded formula changed')
        total_clauses += result['clauses']
        total_tests += result['gate_truth_assignments']
        audit.require(row['tail_status'] in ('UNSAT', 'SAT'), 'Non-decision in table')
        if row['tail_status'] == 'SAT':
            positive.append(i)
            word = witnesses[str(i)]
            audit.witness(lines[i], word)
            g = encode.graph(encode.decode(lines[i]), word)
            audit.require(audit.holds(encode.formula(encode.decode(lines[i])), encode.assignment(g)), 'Saved witness violates ordered CNF')
        else:
            negative.append(i)
        if run_root is not None:
            directory = Path(run_root) / f'canonical-{i:04d}'
            actual = json.loads((directory / 'result.json').read_text())
            audit.require(actual['index'] == i and actual['core'] == lines[i], 'Run core mismatch')
            audit.require((directory / 'tail.cnf').read_bytes() == raw, 'Run formula mismatch')
            if row['tail_status'] == 'SAT':
                audit.require(actual['status'] == 'SAT', 'Run status mismatch')
                audit.witness(lines[i], actual['free_edges'])
            else:
                audit.require(actual['status'] in ('UNSAT_CHECKED_PENDING_ENCODER_AUDIT', 'UNSAT_CHECKED'), 'Run status mismatch')
                path = proof_path(directory, actual)
                audit.require(hashlib.sha256(path.read_bytes()).hexdigest() == actual['proof_sha256'], 'Run proof digest')
                audit.require(checker is not None, 'Proof checker is required for run audit')
                check_proof(checker, directory / 'tail.cnf', path)
    audit.require(set(witnesses) == {str(i) for i in positive}, 'Witness table scope')
    tasks = json.loads((HERE / 'TASKS.json').read_text())
    audit.require(tasks['excluded_core_indices'] == negative and tasks['retained_core_indices'] == positive, 'Physical status interface mismatch')
    audit.require(tasks['remaining_global_tasks'] == 2189178 - len(negative), 'Global registry arithmetic')
    return {'status': 'VERIFIED_ALL_640_TAIL_DECISIONS' if run_root is not None else 'VERIFIED_ENCODINGS_AND_SAT_WITNESSES',
            'tail_cases': 640, 'tail_unsat': len(negative), 'tail_sat': len(positive),
            'physical43_tasks_excluded': len(negative), 'physical43_tasks_remaining_globally': 2189178 - len(negative),
            'literal_clauses_audited': total_clauses, 'comparator_truth_assignments': total_tests,
            'unsat_proofs_rechecked': len(negative) if run_root is not None else 0, 'good43': False}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--catalog', required=True)
    p.add_argument('--run')
    p.add_argument('--drat-trim')
    p.add_argument('--report')
    a = p.parse_args()
    t = time.monotonic()
    result = verify(a.catalog, a.run, a.drat_trim)
    if a.report:
        Path(a.report).write_text(json.dumps(dict(result, seconds=time.monotonic() - t), indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))
