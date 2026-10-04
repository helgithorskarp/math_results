"""Check source pins before importing the independent reviewer program."""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def require(ok,label):
    if not ok:raise ValueError(label)


def identical(a,b):
    if type(a)is not type(b):return False
    if isinstance(a,dict):return set(a)==set(b)and all(identical(a[k],b[k])for k in a)
    if isinstance(a,list):return len(a)==len(b)and all(identical(x,y)for x,y in zip(a,b))
    return a==b


def main():
    p=argparse.ArgumentParser();p.add_argument('--cover',type=Path)
    p.add_argument('--expected',type=Path);p.add_argument('--damage');p.add_argument('--record',type=Path)
    args=p.parse_args();root=Path(__file__).resolve().parent
    seal=json.loads((root/'PRIMARY_SEAL.json').read_text())
    require(set(seal['files'])=={'check.py','arithmetic.py','literal.py','COVER.json','EXPECTED.json'},
            'complete five-file preimport seal')
    require(all(hashlib.sha256((root/name).read_bytes()).hexdigest()==digest
                for name,digest in seal['files'].items()),'preimport source pin')
    sys.path.insert(0,str(root))
    from check import run
    from arithmetic import encode
    summary,record=run(args.cover or root/'COVER.json',args.damage)
    expected=json.loads((args.expected or root/'EXPECTED.json').read_text())
    require(identical(encode(summary),expected),'whole typed independent summary and record seal')
    if args.record:args.record.write_bytes(record)
    print(json.dumps(encode(summary),sort_keys=True,indent=2))


if __name__=='__main__':main()
