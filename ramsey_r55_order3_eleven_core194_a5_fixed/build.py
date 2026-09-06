#!/usr/bin/env python3
"""Nineteen complete full-star refinements; no solver is invoked here."""
from pathlib import Path
import argparse
import json
import shutil
import sys
import audit_fixed

ROOT = Path(__file__).resolve().parent
ATTACH = ROOT.parent / 'ramsey_r55_order3_eleven_core194_attachments'
sys.path.insert(0, str(ATTACH))
import prepare as attach
need = audit_fixed.need
identity = attach.generator.identity
atomic = attach.atomic
IDS = tuple('a%d_b%d_c%d_x%d_y%d_z%d' % tuple(row['counts']) for row in audit_fixed.expected()[0])


def profiles():
    rows=[r for r in attach.profiles.certificate()['profiles'] if r['counts'][:3] in ([5,0,2],[5,1,1])]
    wanted,census=audit_fixed.expected(); audit_fixed.verify(rows,wanted)
    return rows,census,audit_fixed.controls(rows,wanted)


def write_child(base,path,case):
    with base.open('rb') as f,path.open('wb') as g:
        need(f.readline()==b'p cnf 320 366069\n','complete BLUE base header')
        g.write(b'p cnf 320 366099\n'); shutil.copyfileobj(f,g)
        for x in case['units']:g.write(f'{x} 0\n'.encode())


def check_child(base,path,counts):
    units=audit_fixed.physical.normalized_units(counts,True)
    need(len(units)==30,'fourteen moving and sixteen fixed physical units')
    with base.open('rb') as f,path.open('rb') as g:
        need(f.readline()==b'p cnf 320 366069\n','base header')
        need(g.readline()==b'p cnf 320 366099\n','full child header')
        while block:=f.read(1<<20):need(g.read(len(block))==block,'complete base body retained')
        for x in units:need(g.readline()==f'{x} 0\n'.encode(),'physical star unit')
        need(not g.read(),'exact child EOF')
    return identity(path)


def file_controls(base,path,case,work):
    original=path.read_bytes(); head,body=original.split(b'\n',1)
    units=case['units']; tail=b''.join(f'{x} 0\n'.encode() for x in units)
    need(original.endswith(tail),'production full tail')
    altered=list(units);altered[-1]*=-1
    moving=list(units);moving[0]*=-1
    samples=dict(wrong_header=b'p cnf 320 366098\n'+body,lost_base=head+b'\n'+body[1:],
      missing_fixed_unit=original[:-len(tail)]+b''.join(f'{x} 0\n'.encode() for x in units[:-1]),
      wrong_fixed_sign=original[:-len(tail)]+b''.join(f'{x} 0\n'.encode() for x in altered),
      wrong_moving_sign=original[:-len(tail)]+b''.join(f'{x} 0\n'.encode() for x in moving),
      extra_clause=original+b'166 0\n',only_moving=original[:-len(tail)]+b''.join(f'{x} 0\n'.encode() for x in units[:14]))
    bad=work/'bad.cnf'; rejected=[]
    for name,data in samples.items():
        bad.write_bytes(data)
        try: check_child(base,bad,case['counts'])
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted malformed '+name)
    bad.unlink();return rejected


def build(work):
    work.mkdir(parents=True,exist_ok=True)
    rows,census,corrupt=profiles();atomic(work/'profiles.json',rows)
    base=work/'blue.cnf'; gen=attach.generator.write('blue',base); independent=attach.checker.audit(base,'blue')
    pin=dict(bytes=14883777,sha256='f3314485280b2080f3459774b944e010beeb175788673d53703d60cba091e84c')
    need(gen['formula']==pin and independent['sha256']==pin['sha256'],'reviewed complete direct base identity')
    symmetry=audit_fixed.base_symmetries(base)
    cases=[]
    for key,row in zip(IDS,rows):
        need(key=='a%d_b%d_c%d_x%d_y%d_z%d'%tuple(row['counts']),'complete case labels')
        path=work/(key+'.cnf');write_child(base,path,row)
        cases.append(dict(id=key,counts=row['counts'],formula=check_child(base,path,row['counts']),status='untested'))
    rejected=file_controls(base,work/(IDS[0]+'.cnf'),rows[0],work)
    return json.loads(json.dumps(dict(profiles=rows,census=census,profile_controls=corrupt,
        file_controls=rejected,base_symmetries=symmetry,base_generation=gen,base_audit=independent,cases=cases)))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
    work=a.work.resolve();need(not work.is_relative_to(ROOT.parent),'external work')
    answer=build(work);atomic(work/'preparation.json',answer)
    print('PASS complete nineteen-profile census, physical tails, and full formulas')
