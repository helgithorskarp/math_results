"""Recheck saved proof files, without invoking a SAT solver or producer encoder."""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
from reference import literal_formula


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def audit_one(args):
    row,record,directory,checker=args
    stem=Path(directory)/f"core{row['index']:03d}"
    clauses=literal_formula(record)
    reference=(f'p cnf 60 {len(clauses)}\n'+''.join(' '.join(str(x) for x in c)+' 0\n' for c in clauses)).encode()
    cnf=stem.with_suffix('.cnf').read_bytes();proof=stem.with_suffix('.drat').read_bytes()
    if cnf!=reference or sha(cnf)!=row['cnf_sha256'] or sha(proof)!=row['proof_sha256']:
        raise ValueError('saved formula or certificate mismatch')
    out=subprocess.run([checker,str(stem.with_suffix('.cnf')),str(stem.with_suffix('.drat')),'-t','300'],
                       stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=320)
    if out.returncode!=0 or b's VERIFIED' not in out.stdout:
        raise ValueError('saved proof failed')
    return row['index']


def main():
    p=argparse.ArgumentParser();p.add_argument('catalog');p.add_argument('archive');p.add_argument('checker')
    p.add_argument('--workers',type=int,default=4);args=p.parse_args()
    here=Path(__file__).resolve().parent
    manifest=(here/'CERTIFICATES.json').read_bytes();expected=json.loads((here/'EXPECTED.json').read_text())
    if sha(manifest)!=expected['certificates_sha256']:raise ValueError('manifest hash')
    raw=Path(args.catalog).read_bytes()
    if sha(raw)!=expected['catalog_sha256']:raise ValueError('catalogue hash')
    records=raw.splitlines();rows=json.loads(manifest)
    if len(records)!=len(rows) or len(rows)!=640 or [r['index'] for r in rows]!=list(range(640)):
        raise ValueError('complete coverage')
    checker=str(Path(args.checker).resolve());jobs=[]
    for row,record in zip(rows,records):
        if row['graph6']!=record.decode():raise ValueError('core identity')
        jobs.append((row,record,str(Path(args.archive).resolve()),checker))
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        checked=list(pool.map(audit_one,jobs))
    if checked!=list(range(640)):raise ValueError('incomplete proof audit')
    print(json.dumps(dict(status='ALL_640_SAVED_PROOFS_RECHECKED',solver_calls=0,
                         independent_groundings=640,proofs_verified=640,manifest_sha256=sha(manifest)),sort_keys=True))


if __name__=='__main__':main()
