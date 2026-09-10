#!/usr/bin/env python3
"""Verify one complete P84 case exclusion and exact relaxation obstructions."""
import argparse
import copy
import csv
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import time
from check_certificates import check_exclusion, check_fractional, sidon

SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE.parent/'p84_global_cases'))
from orbits import orbit_catalog

def run(command):
    result=subprocess.run(list(map(str,command)),capture_output=True,text=True,check=True)
    return json.loads(result.stdout)

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def build(source,target,sanitize=False):
    flags=['-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer'] if sanitize else ['-O3']
    subprocess.run(['g++','-std=c++20','-Wall','-Wextra','-Wconversion','-Wshadow','-Werror',*flags,str(source),'-o',str(target)],check=True)

def small_checks(program,work):
    reports=[]
    domains=[list(range(11)),[0,2,3,5,11,22,36,57,66,83],[1,4,8,15,31,43,62,70,79,82]]
    weights=[(17*x*x+13*x+5)%997 for x in range(84)]
    (work/'small_weights.txt').write_text(' '.join(map(str,weights))+'\n')
    for i,domain in enumerate(domains):
        path=work/f'small_{i}.txt';path.write_text(' '.join(map(str,domain))+'\n')
        for size in [3,4]:
            expected=sorted((row for row in combinations(domain,size) if sidon(row)),key=lambda row:sum(1<<x for x in row))
            data=bytes(x for row in expected for x in row)
            maximum=max(sum(weights[x] for x in row) for row in expected)
            for method in [0,1]:
                out=work/f'small_{i}_{size}_{method}.bin'
                record=run([program,method,path,out,size,work/'small_weights.txt'])
                assert record['complete'] and record['sets']==len(expected) and record['max_weight']==maximum
                assert out.read_bytes()==data
                reports.append({'domain':i,'size':size,'method':method,'sets':len(expected),'verified':True})
    return reports

def main():
    if not __debug__:raise SystemExit('Run without -O/PYTHONOPTIMIZE: assertions check certificates.')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True);p.add_argument('--sanitizers',action='store_true');a=p.parse_args()
    work=a.work.resolve();assert SOURCE.parent not in [work,*work.parents];work.mkdir(parents=True,exist_ok=True);start=time.monotonic();reports={}
    build(SOURCE.parent/'enumerate.cpp',work/'enumerate')
    build(SOURCE/'weighted_catalog.cpp',work/'weighted_catalog')
    reports['small_checks']=small_checks(work/'weighted_catalog',work)
    record=run([work/'enumerate',84,11,'all',work/'sets84_11.txt'])
    assert record['complete'] and record['sets']==30510
    assert digest(work/'sets84_11.txt')=='e1541890c78cb206076fbcd6067b2da24884b044f902c1c03ffc0da7ccdc0720'
    raw=[list(map(int,line.split())) for line in (work/'sets84_11.txt').read_text().splitlines()]
    old_weights=list(map(int,(SOURCE.parent/'p84_profiles/weights.txt').read_text().split()))
    ordered=orbit_catalog(raw,old_weights)
    canonical=''.join(' '.join(map(str,row))+'\n' for row in ordered)
    assert hashlib.sha256(canonical.encode()).hexdigest()=='4cdac43dae88dfde56506152b01fce145bf2a7e878b486933f11b0c3dba4e3df'
    (work/'orbit_catalog.txt').write_text(canonical);reports['eleven_catalog']=record
    reports['fractional_certificates']=[]
    for name in ['fractional_0.json','fractional_600.json','fractional_joint_21.json']:
        certificate=json.loads((SOURCE/name).read_text())
        reports['fractional_certificates'].append(check_fractional(certificate,ordered,old_weights))
        corrupted=copy.deepcopy(certificate);corrupted['classes'][0]['numerator']+=1
        try:check_fractional(corrupted,ordered,old_weights)
        except AssertionError:pass
        else:raise AssertionError('corrupted coefficient accepted')
    certificate=json.loads((SOURCE/'exclusion_1226.json').read_text())
    (work/'domain.txt').write_text(' '.join(map(str,certificate['domain']))+'\n')
    (work/'weights.txt').write_text(' '.join(map(str,certificate['weights']))+'\n')
    reports['ten_catalogs']=[]
    for method in [0,1]:
        record=run([work/'weighted_catalog',method,work/'domain.txt',work/f'tens_{method}.bin',10,work/'weights.txt'])
        assert record['complete'] and record['sets']==5906761 and record['max_weight']==1000705
        maximizer=record['maximizer'];assert len(maximizer)==10 and sidon(maximizer)
        assert not set(maximizer)&set(certificate['anchor'])
        assert sum(certificate['weights'][x] for x in maximizer)==record['max_weight']
        reports['ten_catalogs'].append(record)
    assert digest(work/'tens_0.bin')==digest(work/'tens_1.bin')=='288672a1f728e3f2532be4e3f5ce7813567ef7fd27db44c482e5f63a9d31914d'
    reports['exclusion']=check_exclusion(certificate,ordered,reports['ten_catalogs'][0]['max_weight'])
    ledger=list(csv.DictReader((SOURCE.parent/'p84_global_cases/cases.csv').open()))
    unresolved=[int(row['orbit']) for row in ledger if row['status']=='unresolved']
    assert len(unresolved)==1211 and 1226 in unresolved
    remaining=[j for j in unresolved if j!=1226]
    assert len(remaining)==1210 and all(j in remaining for j in [0,21,600])
    (work/'remaining_cases.txt').write_text(''.join(f'{j}\n' for j in remaining))
    assert (work/'remaining_cases.txt').read_bytes()==(SOURCE/'remaining_cases.txt').read_bytes()
    reports['trace_sha256']=digest(work/'tens_0.bin');reports['remaining_cases']=len(remaining)
    if a.sanitizers:
        build(SOURCE/'weighted_catalog.cpp',work/'weighted_sanitized',True)
        reports['sanitizer_checks']=small_checks(work/'weighted_sanitized',work)
    reports.update({'verified':True,'seconds':time.monotonic()-start,'numerical_bound_improved':False})
    (work/'verification.json').write_text(json.dumps(reports,indent=2)+'\n')
    print(json.dumps({'verified':True,'remaining_cases':1210,'fractional_certificates':len(reports['fractional_certificates']),'seconds':reports['seconds']}))

if __name__=='__main__':main()
