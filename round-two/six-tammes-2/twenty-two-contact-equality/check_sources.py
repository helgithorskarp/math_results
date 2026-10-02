"""Identify checked source bytes and compare compact actual arithmetic results.

Prerequisite hashes identify premises; this does not execute their proofs.
Run from the repository root. No private corpus or ledger input is used.
"""
import argparse
import hashlib
import json
from pathlib import Path
import signal
from arithmetic import require
import check

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def verify_sources():
    count=0
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ')
        path=HERE/name
        require(path.parent==HERE and not path.is_symlink(), 'literal compact source path')
        require(hashlib.sha256(path.read_bytes()).hexdigest()==digest, 'own source pin '+name)
        count+=1
    inputs=json.loads((HERE/'INPUTS.json').read_text())
    for entry in inputs['source_files']:
        path=ROOT/entry['source']
        require(not path.is_symlink(), 'literal prerequisite source')
        require(hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256'],
                'prerequisite source pin '+entry['source'])
    actual=check.verify()
    expected=json.loads((HERE/'EXPECTED.json').read_text())
    require(actual==expected, 'actual native computation matches the compact expected output')
    return dict(status='CHECKED_SOURCE_PINS_AND_ACTUAL_NATIVE_RESULT',
                agent='six-tammes-2',role='researcher',own_pins=count,
                prerequisite_pins=len(inputs['source_files']),actual_native_check=True,
                prerequisite_proofs_rerun=False,independent_researcher_review=False)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt',type=Path)
    args=parser.parse_args()
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(
        TimeoutError('160-second source/arithmetic guard: incomplete evidence')))
    signal.alarm(160)
    try: result=verify_sources()
    finally: signal.alarm(0)
    if args.receipt:args.receipt.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
