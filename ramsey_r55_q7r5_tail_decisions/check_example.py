"""Check one included full-task certificate without a SAT solver or bulk proofs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import audit
import encode

HERE = Path(__file__).resolve().parent

def run(catalog, scratch):
    scratch = Path(scratch)
    scratch.mkdir(exist_ok=False)
    spec = json.loads((HERE / 'EXAMPLE.json').read_text())
    line = encode.catalog(catalog)[spec['index']]
    raw = encode.dimacs(encode.decode(line))
    audit.formula(line, raw)
    audit.require(hashlib.sha256(raw).hexdigest() == spec['source_cnf_sha256'], 'Example full formula')
    core = (HERE / 'example145.cnf').read_bytes()
    proof = (HERE / 'example145.rup').read_bytes()
    audit.require(hashlib.sha256(core).hexdigest() == spec['core_sha256'] and hashlib.sha256(proof).hexdigest() == spec['proof_sha256'], 'Example digest')
    source_rows = raw.decode().splitlines()[1:]
    core_rows = core.decode().splitlines()[1:]
    positions = spec['core_source_clause_positions_1based']
    audit.require(len(positions) == len(core_rows) and len(set(positions)) == len(positions), 'Example source positions')
    for row, position in zip(core_rows, positions):
        audit.require(1 <= position <= len(source_rows) and sorted(map(int, row.split())) == sorted(map(int, source_rows[position - 1].split())), 'Example source clause')
    binary = scratch / 'check_rup'
    subprocess.run(['g++', '-std=c++17', '-O2', '-DNDEBUG', '-Wall', '-Wextra', '-Werror', str(HERE / 'check_rup.cpp'), '-o', str(binary)], check=True)
    control = subprocess.run([str(binary), '--controls'], check=True, stdout=subprocess.PIPE, text=True)
    checked = subprocess.run([str(binary), str(HERE / 'example145.cnf'), str(HERE / 'example145.rup')], check=True, stdout=subprocess.PIPE, text=True)
    counts = json.loads(checked.stdout)
    audit.require(counts['rup_additions'] == spec['rup_additions'], 'Example proof additions')
    return {'status': 'VERIFIED_EXAMPLE_FULL_PHYSICAL_TASK_UNSAT', 'task': 'bo1-q7-r5-c000145',
            'source_clauses': len(positions), 'proof': counts, 'checker_controls': json.loads(control.stdout), 'good43': False}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--catalog', required=True)
    p.add_argument('--scratch', required=True)
    a = p.parse_args()
    print(json.dumps(run(a.catalog, a.scratch), sort_keys=True))
