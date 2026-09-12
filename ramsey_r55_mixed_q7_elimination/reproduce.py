"""Replay compact mathematical controls, optionally all saved UNSAT proofs."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import time
from controls import controls
from carrier import carrier
from transport_controls import transport_controls
HERE=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser();p.add_argument('catalog_directory');p.add_argument('output')
    p.add_argument('--proof-directory');p.add_argument('--drat-trim');args=p.parse_args()
    start=time.monotonic()
    output=Path(args.output).resolve();output.mkdir(parents=True,exist_ok=False)
    for name,digest in json.loads((HERE/'DEPENDENCIES.json').read_text()).items():
        if hashlib.sha256((HERE.parent/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('dependency changed: '+name)
    results={}
    for name,got in [('CONTROLS.json',controls()),('CARRIER.json',carrier()),
                     ('TRANSPORT_EXPECTED.json',transport_controls(args.catalog_directory,output/'transport'))]:
        if got!=json.loads((HERE/name).read_text()):raise ValueError('expected result differs: '+name)
        results[name]=hashlib.sha256((HERE/name).read_bytes()).hexdigest()
    manifest=(HERE/'CERTIFICATES.json').read_bytes();expected=json.loads((HERE/'EXPECTED.json').read_text())
    if hashlib.sha256(manifest).hexdigest()!=expected['certificates_sha256']:
        raise ValueError('certificate manifest hash')
    rows=json.loads(manifest)
    if [r['index'] for r in rows]!=list(range(640)) or any(r['verdict']!='UNSAT' or not r['drat_verified'] or not r['independent_encoding_match'] for r in rows):
        raise ValueError('reported complete coverage')
    status='COMPACT_CONTROLS_VERIFIED_NOT_UNSAT_REPLAY'
    if args.proof_directory:
        if not args.drat_trim:raise ValueError('--drat-trim required with --proof-directory')
        cmd=[sys.executable,'-B',str(HERE/'audit_saved.py'),str(Path(args.catalog_directory)/'r44_15.g6'),
             args.proof_directory,args.drat_trim,'--workers','4']
        subprocess.run(cmd,check=True)
        status='COMPLETE_640_PROOF_AND_CONTROL_REPLAY_VERIFIED'
    out=dict(status=status,compact_expected_hashes=results,certificate_manifest_sha256=expected['certificates_sha256'],
             wall_seconds=time.monotonic()-start)
    (output/'REPLAY.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps(out,sort_keys=True,indent=2))


if __name__=='__main__':main()
