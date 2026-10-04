"""Regenerate the whole independent exact record; no external math inputs."""
import argparse, hashlib, json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from audit import core, root, columns


def clean(row):
    row.pop('raw_normal',None);row.pop('raw_root',None)
    return row


def make():
    rows=[core(),core(repairs=True),columns()]
    for repairs in (False,True):
        rows.extend(clean(root(j,repairs=repairs)) for j in range(9))
    return dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',
                coefficient_domain='Q[W]/(W^12-W^6+1)[mu]; epsilon through degree10',
                independent_parameters='mu degree<=2; independent affine fourth repairs encoded as powers3/4',
                rows=rows)


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    b=canonical(make());Path(args.output).write_bytes(b+b'\n')
    print(json.dumps(dict(complete=True,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),whole_rows=21)))
