"""Preimport source and complete typed-record checks, retained under -O."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
DAMAGES=('newton','mean_payment','norm_payment','freeze_moving','critical_multiplicity','anchor','repair','power','tangent','equality_cap')

def unique_object(pairs):
    out={}
    for k,v in pairs:
        if k in out:raise ValueError('Duplicate JSON key')
        out[k]=v
    return out

def read_json(p):return json.loads(p.read_text(),object_pairs_hook=unique_object)
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode()

def main():
    a=argparse.ArgumentParser();a.add_argument('--expected',type=Path,default=ROOT/'EXPECTED.json');a.add_argument('--damage',choices=DAMAGES);a.add_argument('--record',action='store_true');args=a.parse_args()
    m=read_json(ROOT/'MANIFEST.json')
    names={'exact.py','retained.py','stationary.py','audit.py','verify.py','controls.py','EXPECTED.json','PROOF.md'}
    if set(m['core_files'])!=names:raise ValueError('Core seal census')
    for n,v in m['core_files'].items():
        b=(ROOT/n).read_bytes()
        if len(b)!=v['bytes'] or hashlib.sha256(b).hexdigest()!=v['sha256']:raise ValueError('Core source seal mismatch: '+n)
    expected=canonical(read_json(args.expected))
    if hashlib.sha256(expected).hexdigest()!=m['canonical_record_sha256']:raise ValueError('Entire typed fixture mismatch before import')
    from audit import run
    actual=canonical(run(args.damage))
    if actual!=expected:raise ValueError('Entire independent mathematical record mismatch')
    if args.record:sys.stdout.buffer.write(actual)
    else:print('PASS: whole third-boundary and equality-cap record; '+str(len(actual))+'B SHA256 '+hashlib.sha256(actual).hexdigest())

if __name__=='__main__':main()
