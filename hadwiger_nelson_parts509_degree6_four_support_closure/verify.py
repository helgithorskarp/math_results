#!/usr/bin/env python3
"""Rebuild four exact instances and check complete supplied PB proofs."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
from engine import HERE,SELECTION,compute,require


def verify(proof_dir,checker):
    facts,instances,_=compute()
    require(facts==json.loads((HERE/'expected.json').read_text()),'expected exact facts differ')
    manifest=json.loads((HERE/'manifest.json').read_text());checks=[]
    with tempfile.TemporaryDirectory(prefix='hn-four-closures-') as d:
        for q in SELECTION:
            path=Path(d)/f'{q}.opb';path.write_bytes(instances[q])
            proof=proof_dir/str(q)/'selector.pb';require(proof.is_file(),('missing complete proof',q))
            r=subprocess.run([str(checker.resolve()),str(path),str(proof.resolve())],capture_output=True,text=True)
            require(r.returncode==0 and 's VERIFIED UNSATISFIABLE' in r.stdout,('proof rejected',q,r.stderr))
            digest=sha256(proof.read_bytes()).hexdigest()
            checks.append(dict(q=q,proof_checked=True,proof_bytes=proof.stat().st_size,proof_sha256=digest,
                               matches_recorded_native_hash=digest==manifest['instances'][str(q)]['proof_sha256']))
    return dict(status='FOUR SUPPORTS CLOSED THROUGH 508; MINIMUM ORDERS 509',closed_points=SELECTION,
                minimum_five_chromatic_subgraph_orders={str(q):509 for q in SELECTION},
                proof_checks=checks,record_improvement=False)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--proof-dir',type=Path,required=True)
    ap.add_argument('--veripb',type=Path,required=True);args=ap.parse_args()
    print(json.dumps(verify(args.proof_dir,args.veripb),indent=2,sort_keys=True))
