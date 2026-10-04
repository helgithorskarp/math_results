"""Whole source closure before imports, then whole exact coefficient record."""
import argparse, hashlib, json, sys
from pathlib import Path

SOURCE_FILES=tuple(sorted(('.gitignore','algebra.py','audit.py','derive.py','signs.py','verify.py','validate.py',
 'FRESH-BASE.json','PROOF.md','REVIEW.md','README.md','DEPENDENCIES.json','PROVENANCE.json','VALIDATION.json')))


def require(ok, label):
    if not ok:raise ValueError(label)


def source_gate(root):
    rows=[]
    for line in (root/'SHA256SUMS').read_text().splitlines():
        parts=line.split('  ');require(len(parts)==2,'source seal syntax')
        digest,name=parts;require(len(digest)==64 and all(x in '0123456789abcdef' for x in digest),'source seal digest')
        rows.append((name,digest))
    require(tuple(name for name,digest in rows)==SOURCE_FILES,'source seal complete census')
    for name,digest in rows:
        require(hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,'source seal '+name)


def exact_tree(value):
    if type(value) in (str,int):return
    if type(value) is list:
        for item in value:exact_tree(item)
        return
    if type(value) is dict:
        require(all(type(k) is str for k in value),'strict record keys')
        for item in value.values():exact_tree(item)
        return
    raise ValueError('strict exact record type')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--record');parser.add_argument('--damage',default='none');args=parser.parse_args()
    root=Path(__file__).resolve().parent;source_gate(root)
    raw=(root/'FRESH-BASE.json').read_bytes();expected=json.loads(raw);exact_tree(expected)
    canonical=lambda v:json.dumps(v,sort_keys=True,separators=(',',':')).encode()
    require(canonical(expected)+b'\n'==raw,'whole canonical fixture')
    sys.dont_write_bytecode=True;sys.path.insert(0,str(root))
    from derive import make
    from audit import core, columns
    if args.damage!='none':
        require(args.damage in ('third','pair-third','fourth','pair-fourth','M','beta','inward','balance','multiplicity','anchor','cost-multiplicity','column'),'known intended semantic defect')
        if args.damage=='column':columns(args.damage)
        else:core(args.damage)
        raise ValueError('intended defect escaped')
    actual=make();exact_tree(actual);b=canonical(actual)
    require(b==canonical(expected),'every field of whole exact record')
    if args.record:Path(args.record).write_bytes(b+b'\n')
    print(json.dumps(dict(complete=True,whole_record_bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),
      whole_rows=len(actual['rows']),all_original_labels=9,ordinary_and_repaired_original_jets=18,
      both_repair_orders_all_labels=True,threads=1)))


if __name__=='__main__':main()
