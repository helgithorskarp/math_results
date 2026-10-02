"""Cold standard-library verification of every coefficient and typed field."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time
import resource
sys.path.insert(0,str(Path(__file__).resolve().parent))
from audit import run


def pairs(items):
    out={}
    for k,v in items:
        if k in out:
            raise ValueError('duplicate fixture key: '+k)
        out[k]=v
    return out


def reject_constant(value):
    raise ValueError('nonfinite fixture value: '+value)


def equal(a,b,path='record'):
    if type(a) is not type(b):
        raise ValueError('type mismatch: '+path)
    if isinstance(a,dict):
        if set(a)!=set(b):
            raise ValueError('field set mismatch: '+path)
        for k in a:
            equal(a[k],b[k],path+'.'+k)
    elif isinstance(a,list):
        if len(a)!=len(b):
            raise ValueError('list length mismatch: '+path)
        for i,(v,w) in enumerate(zip(a,b)):
            equal(v,w,path+'['+str(i)+']')
    elif a!=b:
        raise ValueError('value mismatch: '+path)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('EXPECTED.json'))
    parser.add_argument('--export',type=Path)
    args=parser.parse_args();start=time.monotonic()
    expected=json.loads(args.expected.read_text(),object_pairs_hook=pairs,parse_constant=reject_constant)
    record=run();equal(record,expected)
    raw=json.dumps(record,sort_keys=True,separators=(',',':')).encode()
    if args.export:
        args.export.write_bytes(raw+b'\n')
    print(json.dumps({'agent':'six-reviewer-1','canonical_sha256':hashlib.sha256(raw).hexdigest(),
                      'canonical_bytes':len(raw),'whole_identities':len(record['universal_whole_identities']),
                      'complex_recovery_charts':len(record['complex_recovery_charts']),
                      'bridge_controls':len(record['bridge_controls']),
                      'chart_controls':len(record['chart_controls']),
                      'determinant_degrees':[len(v)-1 for v in record['primitive_determinants']],
                      'independent_prime':record['prime'],'wall_seconds':time.monotonic()-start,
                      'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__=='__main__':
    main()
