#!/usr/bin/env python3
"""Materialize and check nine full extension formulas; perform no solver search."""
from pathlib import Path
import argparse
import importlib.util
import json
import os
import resource
import shutil
import subprocess
import sys
import time
import audit
import profiles

ROOT=Path(__file__).resolve().parent
DIRECT=ROOT.parent/'ramsey_r55_order3_eleven_core194_direct'


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


generator=module('direct_generator',DIRECT/'generate.py')
checker=module('direct_checker',DIRECT/'check.py')


def atomic(path,data):
    tmp=path.with_suffix(path.suffix+'.partial')
    with tmp.open('w') as f:
        json.dump(data,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)


def sources():
    paths=[ROOT/n for n in ('profiles.py','audit.py','prepare.py','verify.py','PROOF.md','five_fixed19.edges')]
    paths += [DIRECT/n for n in ('generate.py','check.py','PROOF.md','result.json','boundary.json')]
    review=ROOT.parent/'ramsey_r55_order3_eleven_core194_direct_review1'
    paths += [review/n for n in ('README.md','result.json')]
    return {str(p.relative_to(ROOT.parent)):generator.identity(p) for p in sorted(paths)}


def write_child(base,path,case):
    with base.open('rb') as f,path.open('wb') as g:
        profiles.require(f.readline()==b'p cnf 320 366069\n','exact direct BLUE header')
        g.write(b'p cnf 320 366083\n');shutil.copyfileobj(f,g)
        for x in case['units']:g.write(f'{x} 0\n'.encode())


def check_child(base,path,case):
    # Expected tail is reconstructed independently from physical graph incidences.
    expected=audit.normalized_units(case['counts'])
    with base.open('rb') as f,path.open('rb') as g:
        profiles.require(f.readline()==b'p cnf 320 366069\n','base header')
        profiles.require(g.readline()==b'p cnf 320 366083\n','child header')
        while block:=f.read(1<<20):profiles.require(g.read(len(block))==block,'complete base retained')
        for x in expected:profiles.require(g.readline()==f'{x} 0\n'.encode(),'physical moving unit')
        profiles.require(not g.read(),'exact child EOF')
    return generator.identity(path)


def full_controls(base,path,case,work):
    original=path.read_bytes();header,body=original.split(b'\n',1);tail=b''.join(f'{x} 0\n'.encode() for x in case['units'])
    bad=work/'bad.cnf';rejected=[]
    samples=dict(wrong_header=b'p cnf 321 366083\n'+body,lost_base=header+b'\n'+body[1:],
        missing_unit=original[:original.rfind(b'\n',0,len(original)-1)+1],
        wrong_sign=original[:-len(tail)]+f'{-case["units"][0]} 0\n'.encode()+tail.split(b'\n',1)[1],
        extra_clause=original+b'166 0\n',wrong_fixed_unit=original[:-len(tail)]+b'167 0\n'+tail.split(b'\n',1)[1])
    for name,data in samples.items():
        bad.write_bytes(data)
        try:check_child(base,bad,case)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted malformed '+name)
    bad.unlink();profiles.require(len(rejected)==6,'six full child controls');return rejected


def build(work):
    work.mkdir(parents=True,exist_ok=True);cert=profiles.certificate();atomic(work/'certificate.json',cert)
    for label,flags in [('normal',[]),('optimized',['-O'])]:
        with (work/(label+'.log')).open('w') as log:
            subprocess.run([sys.executable,'-B',*flags,str(ROOT/'audit.py'),'--certificate',str(work/'certificate.json'),
                '--fixture',str(ROOT/'five_fixed19.edges'),'--work',str(work/('controls_'+label)),'--report',str(work/(label+'.json'))],
                stdout=log,stderr=subprocess.STDOUT,check=True)
    profiles.require((work/'normal.json').read_bytes()==(work/'optimized.json').read_bytes(),'normal/optimized cover checks')
    base=work/'blue.cnf';generated=generator.write('blue',base);independent=checker.audit(base,'blue')
    pin=dict(bytes=14883777,sha256='f3314485280b2080f3459774b944e010beeb175788673d53703d60cba091e84c')
    profiles.require(generated['formula']==pin and independent['sha256']==pin['sha256'],'accepted full direct BLUE identity')
    rows=[]
    for case in cert['moving_cases']:
        path=work/(case['id']+'.cnf');write_child(base,path,case)
        rows.append(dict(id=case['id'],counts=case['counts'],formula=check_child(base,path,case),status='untested'))
    corrupt=full_controls(base,work/(cert['moving_cases'][0]['id']+'.cnf'),cert['moving_cases'][0],work)
    return dict(certificate=cert,local_audit=json.loads((work/'normal.json').read_text()),base_generation=generated,
        base_audit=independent,cases=rows,full_corruptions_rejected=corrupt,solver_calls=0,whole_core_exclusions=[])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args();work=a.work.resolve()
    profiles.require(not work.is_relative_to(ROOT.parent),'generated formulas outside Git')
    work.mkdir(parents=True,exist_ok=True);profiles.require(not (work/'contract.json').exists(),'fresh work path required')
    before=time.monotonic();contract=dict(format='r55-core194-blue-attachment-cover-v1',sources=sources(),python=sys.version.split()[0],solver_calls=0)
    atomic(work/'contract.json',contract);answer=build(work)
    profiles.require(sources()==contract['sources'],'source identities unchanged')
    answer.update(contract=contract,complete=True,seconds=round(time.monotonic()-before,6),largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    atomic(work/'result.json',answer)
    print('PASS119joint profiles,9complete UNTESTED full cases; no solver calls; '+str(answer['seconds'])+'s')
