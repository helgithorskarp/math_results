#!/usr/bin/env python3
"""Mutation controls tied to the second fixed prefix and full inherited base."""
import argparse
import json
from pathlib import Path
import audit
import cube


def run(base, work):
    work.mkdir(parents=True,exist_ok=True)
    raw={}
    for branch in ('one','multiple'):
        p=work/(branch+'.cnf');cube.make(base,p,branch);audit.check(base,p,branch);raw[branch]=p.read_bytes();p.unlink()
    one=raw['one'];multiple=raw['multiple']
    prefix=one[:-len(b'222 223 224 225 0\n')]
    mutants={
        'missing_disjunction_literal':('one',prefix+b'222 223 224 0\n'),
        'first_row_instead_of_second':('one',prefix+b'211 212 213 214 0\n'),
        'opposite_disjunction':('one',prefix+b'-222 -223 -224 -225 0\n'),
        'extra_empty_clause':('one',one+b'0\n'),
        'changed_base_prefix':('one',one.split(b'\n',1)[0]+b'\n0\n'+one.split(b'\n',2)[2]),
        'missing_multiple_unit':('multiple',multiple.rsplit(b'-225 0\n',1)[0]),
        'wrong_multiple_polarity':('multiple',multiple[:-len(b'-225 0\n')]+b'225 0\n')}
    rejected=[]
    for name,(branch,data) in mutants.items():
        p=work/(name+'.cnf');p.write_bytes(data)
        try:audit.check(base,p,branch)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted malformed formula '+name)
        finally:p.unlink()
    return dict(verified=True,rejected=rejected,partition=audit.split_control())


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--work',type=Path,required=True)
    a=p.parse_args();r=run(a.base,a.work);(a.work/'controls.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps(r,sort_keys=True))
