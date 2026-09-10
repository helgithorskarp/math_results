#!/usr/bin/env python3
"""Exclude every eight-class Sidon partition of [84] with five or more elevens."""
import argparse
import concurrent.futures
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

SOURCE=Path(__file__).resolve().parent
EXPECTED=json.loads((SOURCE/'expected.json').read_text())

def run(args):
    p=subprocess.run(list(map(str,args)),capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def check_hash(path,name=None):
    h=hashlib.sha256(path.read_bytes()).hexdigest()
    assert h==EXPECTED['hashes'][name or path.name],(path,h)

def sidon(a):
    sums=[x+y for x,y in itertools.combinations_with_replacement(a,2)]
    return len(sums)==len(set(sums))

def main():
    if not __debug__:
        raise SystemExit('Run without -O or PYTHONOPTIMIZE: proof checks use assertions.')
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--jobs',type=int,default=4)
    p.add_argument('--independent',action='store_true')
    args=p.parse_args();work=args.work.resolve()
    assert 1<=args.jobs<=32
    assert work!=SOURCE.parent and SOURCE.parent not in work.parents
    work.mkdir(parents=True,exist_ok=True);start=time.monotonic();reports={}
    programs={'enumerate':SOURCE.parent/'enumerate.cpp','packing':SOURCE/'packing.cpp','complete':SOURCE/'complete.cpp'}
    if args.independent:
        programs.update({'catalog_reference':SOURCE.parent/'reference.cpp','packing_reference':SOURCE/'packing_reference.cpp','complete_reference':SOURCE/'complete_reference.cpp'})
    for name,path in programs.items():
        subprocess.run(['g++','-std=c++20','-O3','-Wall','-Wextra','-Wconversion','-Wshadow','-Werror',str(path),'-o',str(work/name)],check=True)
    weights=list(map(int,(SOURCE/'weights.txt').read_text().split()))
    assert len(weights)==84 and min(weights)>=0 and max(weights)==222222 and sum(weights)==15685948
    for k in (10,11,12):
        output=work/'sets84_11.txt' if k==11 else '-'
        command=[work/'enumerate',84,k,'all',output]
        if k!=12:command.append(SOURCE/'weights.txt')
        r=run(command);assert r['complete'] and r['sets']==EXPECTED['catalog_counts'][str(k)]
        if k!=12:assert r['max_weight']==1999990
        reports[f'enumerate_{k}']=r;print(json.dumps(r),flush=True)
    check_hash(work/'sets84_11.txt')
    rows=[tuple(map(int,s.split())) for s in (work/'sets84_11.txt').read_text().splitlines()]
    assert len(rows)==len(set(rows))==30510
    for row in rows:assert len(row)==11 and tuple(sorted(set(row)))==row and 0<=row[0]<row[-1]<84 and sidon(row)
    rows.sort(key=lambda r:(-sum(weights[x] for x in r),sum(1<<x for x in r)))
    (work/'ordered84_11.txt').write_text(''.join(' '.join(map(str,r))+'\n' for r in rows));check_hash(work/'ordered84_11.txt')
    r=run([work/'packing',work/'ordered84_11.txt',SOURCE/'weights.txt',work/'packings84_five.txt'])
    assert r['complete'] and r['packings']==160244;reports['packing']=r;check_hash(work/'packings84_five.txt')
    tuples=[tuple(map(int,s.split())) for s in (work/'packings84_five.txt').read_text().splitlines()]
    assert len(tuples)==len(set(tuples))==160244
    masks=[sum(1<<x for x in r) for r in rows];representatives={}
    for ids in tuples:
        assert len(ids)==5 and tuple(sorted(set(ids)))==ids
        union=0
        for i in ids:
            assert 0<=i<len(rows) and not union&masks[i]
            union|=masks[i]
        assert sum(sum(weights[x] for x in rows[i]) for i in ids)>=9685948
        representatives.setdefault(((1<<84)-1)^union,ids)
    unique=list(representatives.values());assert len(unique)==160242
    (work/'unique_five_tuples.txt').write_text(''.join(' '.join(map(str,r))+'\n' for r in unique));check_hash(work/'unique_five_tuples.txt')
    for fixture in json.loads((SOURCE/'positive_controls.json').read_text()):
        sizes=fixture['sizes'];residual=fixture['points']
        assert len(residual)==len(set(residual))==29 and residual==sorted(residual)
        path=work/('positive_'+'_'.join(map(str,sizes))+'.txt');path.write_text(' '.join(map(str,residual))+'\n')
        result=run([work/'complete','--residual',path]);assert result['found']
        parts=[[x-1 for x in part] for part in result['partition']]
        assert sorted(map(len,parts))==sizes
        assert sorted(x for part in parts for x in part)==residual and all(sidon(part) for part in parts)
        if args.independent:assert run([work/'complete_reference','--residual',path])['found']
    for i in range(args.jobs):(work/f'chunk_{i}.txt').write_text(''.join(' '.join(map(str,r))+'\n' for r in unique[i::args.jobs]))
    def decide(i,reference=False):
        command=[work/'complete_reference'] if reference else [work/'complete',84]
        r=run(command+[work/'ordered84_11.txt',work/f'chunk_{i}.txt'])
        if reference:assert r['all_unsatisfiable'] and r['tested']==len(unique[i::args.jobs])
        else:assert not r['found'] and r['input_read_complete'] and r['tuples']==r['unique_residuals']==len(unique[i::args.jobs])
        (work/(('reference_' if reference else '')+f'completion_{i}.json')).write_text(json.dumps(r)+'\n')
        return r
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        reports['completions']=list(pool.map(decide,range(args.jobs)))
    assert sum(r['ten_sets'] for r in reports['completions'])==41022
    assert sum(r['eleven_sets'] for r in reports['completions'])==0
    if args.independent:
        r=run([work/'catalog_reference',84,11,work/'reference_sets.txt']);assert r['complete'] and r['sets']==30510
        other={tuple(map(int,s.split())) for s in (work/'reference_sets.txt').read_text().splitlines()};assert other==set(rows)
        r=run([work/'catalog_reference',84,12]);assert r['complete'] and r['sets']==0
        r=run([work/'packing_reference',84,11,5,work/'sets84_11.txt',SOURCE/'weights.txt',work/'other_packings.txt']);assert r['complete'] and r['packings']==160244
        check_hash(work/'other_packings.txt','packings84_five.txt');check_hash(work/'other_packings.txt.sets','ordered84_11.txt')
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            reports['reference_completions']=list(pool.map(lambda i:decide(i,True),range(args.jobs)))
        for a,b in zip(reports['completions'],reports['reference_completions']):
            assert a['ten_sets']==b['ten_sets'] and a['eleven_sets']==b['eleven_sets']
    reports['seconds']=time.monotonic()-start;reports['verified']=True
    reports['conclusion']='Every eight-class Sidon partition of [84] has size profile (11,11,11,11,10,10,10,10).'
    (work/'verification.json').write_text(json.dumps(reports,indent=2)+'\n')
    print(json.dumps({'verified':True,'profile_only':True,'independent':args.independent,'seconds':reports['seconds']}))

if __name__=='__main__':main()
