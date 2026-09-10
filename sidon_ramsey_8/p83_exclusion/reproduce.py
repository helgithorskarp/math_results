#!/usr/bin/env python3
"""Regenerate and verify the globally complete balanced P83 exclusion."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

SOURCE=Path(__file__).resolve().parent
PARENT=SOURCE.parent
PROFILE=PARENT/'p83_profiles'

def digest(path):
    h=hashlib.sha256()
    with path.open('rb')as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def same(a,b):
    with a.open('rb')as x,b.open('rb')as y:
        while True:
            u,v=x.read(1<<20),y.read(1<<20)
            assert u==v,(a,b)
            if not u:return

def run(cmd):
    r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,check=True)
    return json.loads(r.stdout)

def build(source,target,sanitized=False):
    flags=['-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer']if sanitized else ['-O3']
    subprocess.run(['g++','-std=c++20','-Wall','-Wextra','-Wconversion','-Wshadow','-Werror',*flags,str(source),'-o',str(target)],check=True)

def sidon(a):
    pairs=[x+y for i,x in enumerate(a)for y in a[i:]]
    return len(pairs)==len(set(pairs))

def mask(a):return sum(1<<x for x in a)

def collision(a):
    sums={}
    for i,x in enumerate(a):
        for y in a[i:]:
            if x+y in sums:return [sums[x+y],[x,y]]
            sums[x+y]=[x,y]
    return None

def partition(domain,classes,size):
    assert all(len(a)==size and sidon(a)for a in classes)
    points=[x for a in classes for x in a]
    assert len(points)==len(set(points)) and sorted(points)==sorted(domain)

def controls(program,generator,work):
    reports=[];wp=work/'small_weights.txt'
    wp.write_text(' '.join(str((17*x*x+13*x+5)%997)for x in range(83))+'\n')
    for size,totals in [(3,[3,6,9,12]),(4,[4,8,12])]:
        family=sorted((a for a in combinations(range(12),size)if sidon(a)),key=mask)
        fp=work/f'small_{size}.bin';fp.write_bytes(bytes(x for a in family for x in a));fm=[mask(a)for a in family]
        @lru_cache(None)
        def exact(r):
            if not r:return True
            point=r&-r
            return any(a&point and a&r==a and exact(r^a)for a in fm)
        domains=[a for n in totals for a in combinations(range(12),n)];expected=[exact(mask(a))for a in domains]
        assert any(expected) and not all(expected)
        dp=work/f'small_domains_{size}.txt';dp.write_text(''.join(' '.join(map(str,a))+'\n'for a in domains))
        for method in [0,1]:
            out=work/f'small_{program.name}_{size}_{method}.jsonl';record=run([program,'control',method,wp,fp,size,dp,out]);answers=[json.loads(line)for line in out.read_text().splitlines()]
            assert record['complete'] and record['domains']==len(domains)==len(answers)
            assert [a['found']for a in answers]==expected
            for domain,answer in zip(domains,answers):
                if answer['found']:partition(domain,answer['partition'],size)
            reports.append(dict(size=size,method=method,domains=len(domains),positive=sum(expected),negative=len(domains)-sum(expected)))
        bad=work/f'bad_{size}.bin';bad.write_bytes(fp.read_bytes()+fp.read_bytes()[:size]);r=subprocess.run(list(map(str,[program,'control',0,wp,bad,size,dp,work/'bad.jsonl'])),capture_output=True,text=True)
        assert r.returncode!=0 and 'catalog' in r.stderr
    seed=[list(map(int,line.split()))for line in(PARENT/'p80_extension_barrier/partition80.txt').read_text().splitlines()]
    partition(range(80),[[x-1 for x in a]for a in seed],10)
    for shift in [0,3]:
        classes=[[x-1+shift for x in a]for a in seed[:5]];domain=sorted(x for a in classes for x in a);partition(domain,classes,10);assert min(domain)>=0 and max(domain)<83
        dp=work/f'positive50_{shift}.txt';dp.write_text(' '.join(map(str,domain))+'\n');fp=work/f'positive50_{shift}.bin'
        padded=work/'weights84.txt';padded.write_text((PROFILE/'weights.txt').read_text().strip()+' 0\n');generation=run([generator,0,dp,fp,10,padded])
        for method in [0,1]:
            out=work/f'positive50_{program.name}_{shift}_{method}.jsonl';record=run([program,'control',method,PROFILE/'weights.txt',fp,10,dp,out]);answer=json.loads(out.read_text())
            assert record['complete'] and answer['found'];partition(domain,answer['partition'],10)
            reports.append(dict(size=50,shift=shift,method=method,ten_sets=generation['sets'],positive=True))
    return reports

def controls20(program,work):
    seed=[list(map(int,line.split()))for line in(PARENT/'p80_extension_barrier/partition80.txt').read_text().splitlines()]
    reports=[]
    for shift in [0,3]:
        classes=[[x-1+shift for x in a]for a in seed[:2]];domain=sorted(x for a in classes for x in a);partition(domain,classes,10)
        dp=work/f'positive20_{shift}.txt';dp.write_text(' '.join(map(str,domain))+'\n')
        for method in [0,1]:
            prefix=work/f'positive20_{program.name}_{shift}_{method}'
            record=run([program,method,dp,prefix.with_suffix('.bin'),prefix.with_suffix('.jsonl')]);answer=json.loads(prefix.with_suffix('.jsonl').read_text())
            assert record['complete'] and record['found']==1 and answer['found'];partition(domain,answer['partition'],10)
            reports.append(dict(shift=shift,method=method,ten_sets=record['ten_sets'],verified=True))
    return reports

def orbit_catalog(raw,weights):
    masks={mask(a):tuple(a)for a in raw};orbits=[];assert len(masks)==len(raw)==15958
    for m,a in masks.items():
        b=tuple(sorted(82-x for x in a));r=mask(b);assert r in masks and r!=m
        if m<r:orbits.append((sum(weights[x]for x in a),m,a,b))
    orbits.sort(key=lambda a:(-a[0],a[1]));return [a for o in orbits for a in o[2:]]

def verify(work,jobs,orbitpath):
    expected=json.loads((SOURCE/'expected.json').read_text())
    weights=list(map(int,(PROFILE/'weights.txt').read_text().split()));orbit=[list(map(int,l.split()))for l in orbitpath.read_text().splitlines()]
    assert len(weights)==83 and sum(weights)==31134774 and weights==weights[::-1]
    assert len(orbit)==15958 and all(len(a)==11 and sidon(a)for a in orbit)
    assert digest(orbitpath)==json.loads((PROFILE/'validation.json').read_text())['hashes']['orbit11.txt']
    rows_by_method=[];sweeps=[]
    for method in [0,1]:
        rows=[]
        for shard in range(jobs):
            prefix=work/f'full_{method}_{shard}';record=json.loads(prefix.with_suffix('.out').read_text())
            assert record['complete'] is True and record['found']==0 and prefix.with_suffix('.done').read_text()=='complete\n'
            part=[{k:int(v)for k,v in r.items()}for r in csv.DictReader(prefix.with_suffix('.csv').open())]
            assert all(r['orbit']%jobs==shard for r in part)
            assert record['packings']==sum(r['packings']for r in part)
            rows+=part;sweeps.append(dict(method=method,shard=shard,result=record,trace_bytes=prefix.with_suffix('.bin').stat().st_size,trace_sha256=digest(prefix.with_suffix('.bin'))))
        rows.sort(key=lambda r:r['orbit']);assert [r['orbit']for r in rows]==list(range(5364))
        totals={k:sum(r[k]for r in rows)for k in expected['totals']};assert totals==expected['totals'],totals
        for r in rows:
            assert r['calls5']==r['packings'] and r['found']==r['candidates1']==0
            assert all(r[f'candidates{k}']==r[f'calls{k-1}']for k in range(2,6))
        rows_by_method.append(rows)
    assert rows_by_method[0]==rows_by_method[1]
    profile=list(csv.DictReader((PROFILE/'cases_three.csv').open()));assert len(profile)==5364
    assert all(r['orbit']==int(q['orbit']) and r['packings']==int(q['packings'])for r,q in zip(rows_by_method[0],profile))
    terminals=[]
    for shard in range(jobs):
        same(work/f'full_0_{shard}.bin',work/f'full_1_{shard}.bin');same(work/f'full_0_{shard}.jsonl',work/f'full_1_{shard}.jsonl')
        terminals += [json.loads(l)for l in(work/f'full_0_{shard}.jsonl').read_text().splitlines()]
    assert len(terminals)==totals['calls1']
    terminals.sort(key=lambda r:(r['eleven_ids'],r['chosen_tens']))
    for r in terminals:
        ids=r['eleven_ids'];assert len(ids)==3 and ids==sorted(set(ids)) and ids[0]%2==0 and all(0<=i<len(orbit)for i in ids)
        elevens=[orbit[i]for i in ids];tens=r['chosen_tens'];last=r['residual']
        assert len(tens)==4 and len(last)==10 and all(len(a)==10 and sidon(a)for a in tens)
        assert not r['sidon'] and not sidon(last)
        assert sorted(x for a in [*elevens,*tens,last]for x in a)==list(range(83))
        assert sum(weights[x]for a in elevens for x in a)>=11134774
        tw=[sum(weights[x]for x in a)for a in [*tens,last]];assert tw==sorted(tw,reverse=True) and tw[0]<=4000000
        for i,w in enumerate(tw[:-1]):assert w>=(sum(tw[i:])+4-i)//(5-i) and w>=3567387
        r['ten_weights']=tw;r['collision']=collision(last);assert r['collision']and sum(r['collision'][0])==sum(r['collision'][1])
    output=work/'cases.csv'
    with output.open('w')as f:
        fields=['orbit','packings','calls4','calls3','calls2','calls1'];writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',lineterminator='\n');writer.writeheader();writer.writerows(rows_by_method[0])
    examples=terminals[:2]+terminals[-2:];(work/'terminal_examples.json').write_text(json.dumps(examples,indent=2)+'\n')
    (work/'all_terminals.json').write_text(json.dumps(terminals)+'\n')
    residual20=sorted({tuple(sorted(r['chosen_tens'][-1]+r['residual']))for r in terminals})
    domain20=work/'terminal20_domains.txt';domain20.write_text(''.join(' '.join(map(str,a))+'\n'for a in residual20))
    checks20=[]
    for method in [0,1]:
        record=run([work/'complete20',method,domain20,work/f'terminal20_{method}.bin',work/f'terminal20_{method}.jsonl'])
        assert record['complete'] and record['domains']==len(residual20) and record['found']==0
        checks20.append(record)
    same(work/'terminal20_0.bin',work/'terminal20_1.bin');same(work/'terminal20_0.jsonl',work/'terminal20_1.jsonl')
    for name in ['cases.csv','terminal_examples.json']:
        if(SOURCE/name).exists():same(work/name,SOURCE/name)
    return dict(verified=True,terminal20_direct_checks=checks20,terminal20_domains_sha256=digest(domain20),terminal20_trace_sha256=digest(work/'terminal20_0.bin'),totals=totals,cases=5364,nonempty_cases=sum(r['packings']>0 for r in rows_by_method[0]),sweeps=sweeps,terminal_occurrences=len(terminals),terminal_distinct_residuals=len({tuple(r['residual'])for r in terminals}),terminal_distinct_triples=len({tuple(r['eleven_ids'])for r in terminals}),cases_sha256=digest(output),terminal_examples_sha256=digest(work/'terminal_examples.json'),all_terminals_sha256=digest(work/'all_terminals.json'),complete_query_traces_bytewise_equal=True,case_records_equal=True)

def main():
    if not __debug__:raise SystemExit('Do not use -O/PYTHONOPTIMIZE; assertions are proof checks.')
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--work',type=Path,required=True);parser.add_argument('--jobs',type=int,default=6);parser.add_argument('--workers',type=int,default=8);parser.add_argument('--sanitizers',action='store_true');args=parser.parse_args()
    work=args.work.resolve();assert PARENT not in [work,*work.parents] and 1<=args.jobs<=12 and 1<=args.workers<=12;work.mkdir(parents=True,exist_ok=True);start=time.monotonic();records={}
    for source,name in [(SOURCE/'exclude.cpp','exclude'),(SOURCE/'complete20.cpp','complete20'),(PARENT/'enumerate.cpp','enumerate'),(PARENT/'p84_weight_certificates/weighted_catalog.cpp','catalog')]:build(source,work/name)
    records['controls']=controls(work/'exclude',work/'catalog',work)
    records['positive20']=controls20(work/'complete20',work)
    if args.sanitizers:
        build(SOURCE/'exclude.cpp',work/'exclude_sanitized',True);records['sanitizer_controls']=controls(work/'exclude_sanitized',work/'catalog',work)
        build(SOURCE/'complete20.cpp',work/'complete20_sanitized',True);records['sanitizer20']=controls20(work/'complete20_sanitized',work)
    print('Definition-level and five-ten positive controls passed.',flush=True)
    wp=PROFILE/'weights.txt';weights=list(map(int,wp.read_text().split()));prior=json.loads((PROFILE/'validation.json').read_text())
    records['eleven_catalog']=run([work/'enumerate',83,11,'all',work/'raw11.txt',wp]);assert records['eleven_catalog']['complete'] and records['eleven_catalog']['sets']==15958 and records['eleven_catalog']['max_weight']==3999979
    assert digest(work/'raw11.txt')==prior['hashes']['raw11.txt'];raw=[list(map(int,l.split()))for l in(work/'raw11.txt').read_text().splitlines()];orbit=orbit_catalog(raw,weights)
    orbitpath=work/'orbit11.txt';orbitpath.write_text(''.join(' '.join(map(str,a))+'\n'for a in orbit));assert digest(orbitpath)==prior['hashes']['orbit11.txt']
    padded=work/'weights84.txt';padded.write_text(wp.read_text().strip()+' 0\n');domain=work/'domain83.txt';domain.write_text(' '.join(map(str,range(83)))+'\n')
    def catalogs(method):
        full,heavy=work/f'catalog_full_{method}.bin',work/f'catalog_heavy_{method}.bin';r=run([work/'catalog',method,domain,full,10,padded]);f=run([work/'exclude','filter',wp,full,heavy])
        assert r['complete'] and r['sets']==24751806 and r['max_weight']==3999980
        assert f==dict(sets=24751806,kept=4832138,cutoff=3567387,maximum=3999980,complete=True)
        assert digest(full)==prior['ten_catalogs'][0]['full_sha256'] and digest(heavy)==prior['ten_catalogs'][0]['heavy_sha256']
        return dict(method=method,generation=r,filter=f,full_sha256=digest(full),heavy_sha256=digest(heavy))
    with ThreadPoolExecutor(max_workers=min(2,args.workers))as pool:records['catalogs']=list(pool.map(catalogs,[0,1]))
    same(work/'catalog_full_0.bin',work/'catalog_full_1.bin');same(work/'catalog_heavy_0.bin',work/'catalog_heavy_1.bin')
    print('Full P83 catalogs agree. Starting both complete traversals.',flush=True)
    def sweep(task):
        method,shard=task;prefix=work/f'full_{method}_{shard}';marker=prefix.with_suffix('.done')
        if marker.exists():marker.unlink()
        cmd=[work/'exclude',method,orbitpath,wp,work/f'catalog_heavy_{method}.bin',shard,args.jobs,prefix.with_suffix('.csv'),prefix.with_suffix('.bin'),prefix.with_suffix('.jsonl'),marker]
        with prefix.with_suffix('.out').open('w')as out,prefix.with_suffix('.err').open('w')as err:r=subprocess.run(list(map(str,cmd)),stdout=out,stderr=err)
        assert r.returncode==0,(method,shard,r.returncode,prefix.with_suffix('.err').read_text())
        print(f'Completed method {method}, shard {shard}.',flush=True)
    with ThreadPoolExecutor(max_workers=args.workers)as pool:list(pool.map(sweep,[(m,s)for m in [0,1]for s in range(args.jobs)]))
    records.update(verify(work,args.jobs,orbitpath));records.update(seconds=time.monotonic()-start,jobs=args.jobs,workers=args.workers,compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0],python=sys.version,child_max_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,imported_p83_profile=True,P80_witness_verified=True,numerical_conclusion='81 <= SR(8) <= 83')
    (work/'verification.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(dict(verified=True,packings=65073232,found=0,seconds=records['seconds'])))

if __name__=='__main__':main()
