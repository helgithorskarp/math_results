"""Generate and check all 640 UNSAT proofs; large artifacts stay outside git."""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import time
from encode import cores, graph6, formula, dimacs, CATALOG_SHA256
from reference import literal_formula


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def certify_one(args):
    index, record, directory, solver, checker = args
    start = time.monotonic()
    directory = Path(directory)
    stem = directory/f'core{index:03d}'
    clauses = formula(graph6(record))
    if clauses != literal_formula(record):
        raise ValueError(f'encoding mismatch: {index}')
    raw = dimacs(15,clauses)
    stem.with_suffix('.cnf').write_bytes(raw)
    solved = subprocess.run([solver,'--no-binary',str(stem.with_suffix('.cnf')),str(stem.with_suffix('.drat'))],
                            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=300)
    stem.with_suffix('.solve.log').write_bytes(solved.stdout)
    if solved.returncode != 20 or b's UNSATISFIABLE' not in solved.stdout:
        raise ValueError(f'not UNSAT: {index}')
    proof = stem.with_suffix('.drat').read_bytes()
    checked = subprocess.run([checker,str(stem.with_suffix('.cnf')),str(stem.with_suffix('.drat')),'-t','300'],
                             stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=320)
    stem.with_suffix('.check.log').write_bytes(checked.stdout)
    if checked.returncode != 0 or b's VERIFIED' not in checked.stdout:
        raise ValueError(f'proof check failed: {index}')
    result = dict(index=index,graph6=record.decode(),variables=60,clauses=len(clauses),
                  cnf_sha256=sha(raw),cnf_bytes=len(raw),proof_sha256=sha(proof),proof_bytes=len(proof),
                  independent_encoding_match=True,verdict='UNSAT',drat_verified=True)
    stem.with_suffix('.json').write_text(json.dumps(dict(result,seconds=time.monotonic()-start),indent=2)+'\n')
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('catalog'); p.add_argument('output'); p.add_argument('cadical'); p.add_argument('drat_trim')
    p.add_argument('--workers',type=int,default=4)
    args = p.parse_args()
    checker = str(Path(args.drat_trim).resolve())
    solver = str(Path(args.cadical).resolve())
    directory = Path(args.output).resolve(); directory.mkdir(parents=True,exist_ok=False)
    start = time.monotonic(); records = cores(args.catalog)
    jobs = [(i,r,str(directory),solver,checker) for i,r in enumerate(records)]
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for result in pool.map(certify_one,jobs):
            results.append(result)
            if len(results)%64 == 0:
                print(f'{len(results)}/640 independently grounded and DRAT verified',flush=True)
    raw = (json.dumps(results,sort_keys=True,indent=2)+'\n').encode()
    (directory/'CERTIFICATES.json').write_bytes(raw)
    summary = dict(status='ALL_640_CORES_UNSAT_DRAT_VERIFIED',catalog_sha256=CATALOG_SHA256,
                   certificates_sha256=sha(raw),cores=640,independent_encoding_matches=640,
                   cnf_bytes=sum(r['cnf_bytes'] for r in results),proof_bytes=sum(r['proof_bytes'] for r in results),
                   clauses_min=min(r['clauses'] for r in results),clauses_max=max(r['clauses'] for r in results),
                   total_clauses=sum(r['clauses'] for r in results),
                   solver='CaDiCaL 1.9.5 standalone',cadical_sha256=sha(Path(solver).read_bytes()),
                   drat_trim_sha256=sha(Path(checker).read_bytes()))
    (directory/'EXPECTED.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(summary,wall_seconds=time.monotonic()-start),indent=2),flush=True)


if __name__ == '__main__':
    main()
