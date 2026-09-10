#!/usr/bin/env python3
"""Classify every P83 profile and reproduce the complete remaining anchor cover."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
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
EXPECTED=json.loads((SOURCE/'expected.json').read_text())

def run(command):
    r=subprocess.run(list(map(str,command)),capture_output=True,text=True,check=True)
    return json.loads(r.stdout)

def build(source,target,sanitize=False):
    flags=['-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer'] if sanitize else ['-O3']
    subprocess.run(['g++','-std=c++20','-Wall','-Wextra','-Wconversion','-Wshadow','-Werror',*flags,str(source),'-o',str(target)],check=True)

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def same(a,b):
    with a.open('rb')as x,b.open('rb')as y:
        while True:
            p,q=x.read(1<<20),y.read(1<<20)
            assert p==q,(a,b)
            if not p:return

def sidon(a):
    sums=[x+y for i,x in enumerate(a)for y in a[i:]]
    return len(sums)==len(set(sums))

def bitmask(a):return sum(1<<x for x in a)

def partition_check(domain,parts,sizes):
    assert sorted(map(len,parts))==sorted(sizes)
    assert all(sidon(a)for a in parts)
    points=[x for a in parts for x in a]
    assert len(points)==len(set(points)) and sorted(points)==sorted(domain)

def profiles(count,total,maximum):
    if not count:
        if not total:yield ()
        return
    for size in range(min(maximum,total),0,-1):
        if total-size<=size*(count-1):
            for tail in profiles(count-1,total-size,size):yield(size,)+tail

def canonical(rows,weights):
    masks={bitmask(a):tuple(a)for a in rows};orbits=[]
    assert len(masks)==len(rows)==15958
    for m,a in masks.items():
        b=tuple(sorted(82-x for x in a));r=bitmask(b)
        assert r in masks and r!=m
        if m<r:orbits.append((sum(weights[x]for x in a),m,a,b))
    orbits.sort(key=lambda row:(-row[0],row[1]))
    return [a for row in orbits for a in row[2:]]

def controls28(program,work):
    rows=json.loads((SOURCE/'positive28.json').read_text());reports=[]
    profiles28=[[10,10,8],[10,9,9],[11,10,7],[11,11,6],[11,9,8]]
    assert sorted(row['sizes']for row in rows)==sorted(profiles28)
    for row in rows:
        partition_check(row['points'],row['classes'],row['sizes'])
        profile=profiles28.index(row['sizes']);dp=work/f'positive28_{profile}.txt'
        dp.write_text(' '.join(map(str,row['points']))+'\n')
        for method in [0,1]:
            prefix=work/f'positive28_{program.name}_{profile}_{method}'
            record=run([program,method,dp,prefix.with_suffix('.bin'),prefix.with_suffix('.jsonl'),profile])
            answer=json.loads(prefix.with_suffix('.jsonl').read_text())
            assert record['complete'] and record['found']==record['domains']==1 and answer['found']
            partition_check(row['points'],answer['partition'],row['sizes']);record['profile']=row['sizes'];reports.append(record)
    return reports

def controls39(program,generator,work,weights_padded):
    seed=[[18,20,32,39,47,50,63,67,72,73],[11,12,17,21,34,37,45,52,64,66],
          [8,10,19,25,26,46,49,54,68,80],[6,9,16,27,35,40,60,62,76,77]]
    reports=[]
    for shift in [0,3]:
        parts=[[x-1+shift for x in a]for a in seed];full=sorted(x for a in parts for x in a)
        assert len(set(full))==40 and min(full)>=0 and max(full)<83 and all(sidon(a)for a in parts)
        dp=work/f'control40_{shift}.txt';dp.write_text(' '.join(map(str,full))+'\n')
        catalog=work/f'control40_{shift}.bin';generation=run([generator,0,dp,catalog,10,weights_padded])
        rows=[]
        for tens in [1,2,3]:
            for deleted in parts[0]:
                blocks=[[x for x in parts[0]if x!=deleted],*parts[1:tens+1]]
                rows.append((sorted(x for a in blocks for x in a),[9]+[10]*tens))
        domains=work/f'controls39_{shift}.txt';domains.write_text(''.join(' '.join(map(str,a))+'\n'for a,_ in rows))
        for method in [0,1]:
            output=work/f'controls39_{program.name}_{shift}_{method}.jsonl'
            record=run([program,'control',method,SOURCE/'weights.txt',catalog,domains,output])
            answers=[json.loads(line)for line in output.read_text().splitlines()]
            assert record['complete'] and len(answers)==record['domains']==len(rows)==30
            for (domain,sizes),answer in zip(rows,answers):
                assert answer['found'];partition_check(domain,answer['partition'],sizes)
            reports.append(dict(shift=shift,method=method,domains=30,ten_catalog_sets=generation['sets']))
    return reports

def collision(a):
    seen={}
    for i,x in enumerate(a):
        for y in a[i:]:
            if x+y in seen:return [seen[x+y],[x,y]]
            seen[x+y]=[x,y]
    return None

def main():
    if not __debug__:raise SystemExit('Assertions are proof checks: do not use -O/PYTHONOPTIMIZE.')
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--work',type=Path,required=True);parser.add_argument('--jobs',type=int,default=4);parser.add_argument('--sanitizers',action='store_true');args=parser.parse_args()
    work=args.work.resolve();assert PARENT not in [work,*work.parents] and 1<=args.jobs<=12
    work.mkdir(parents=True,exist_ok=True);start=time.monotonic();reports={}
    weights=list(map(int,(SOURCE/'weights.txt').read_text().split()));v=list(map(int,(PARENT/'p84_profiles/weights.txt').read_text().split()))
    assert weights==[a+b for a,b in zip(v,v[1:])];assert len(weights)==83 and sum(weights)==31134774 and max(weights)==444444 and weights==weights[::-1]
    wp=work/'weights_padded.txt';wp.write_text(' '.join(map(str,weights+[0]))+'\n');dp=work/'domain83.txt';dp.write_text(' '.join(map(str,range(83)))+'\n')
    programs={'enumerate':PARENT/'enumerate.cpp','reference':PARENT/'reference.cpp','catalog':PARENT/'p84_weight_certificates/weighted_catalog.cpp',**{name:SOURCE/(name+'.cpp')for name in ['pack_five','pack_five_reference','complete28','exclude_four','count_three']}}
    for name,source in programs.items():build(source,work/name)
    reports['positive28']=controls28(work/'complete28',work)
    reports['positive39']=controls39(work/'exclude_four',work/'catalog',work,wp)
    if args.sanitizers:
        for name in ['complete28','exclude_four']:
            build(SOURCE/(name+'.cpp'),work/(name+'_sanitized'),True)
        reports['sanitizer28']=controls28(work/'complete28_sanitized',work)
        reports['sanitizer39']=controls39(work/'exclude_four_sanitized',work/'catalog',work,wp)
    print('Profile-specific positive controls passed.',flush=True)
    reports['eleven']=run([work/'enumerate',83,11,'all',work/'raw11.txt',SOURCE/'weights.txt'])
    reports['eleven_reference']=run([work/'reference',83,11,work/'reference11.txt'])
    rows=[tuple(map(int,s.split()))for s in(work/'raw11.txt').read_text().splitlines()]
    other=[tuple(map(int,s.split()))for s in(work/'reference11.txt').read_text().splitlines()]
    assert len(rows)==len(set(rows))==len(other)==len(set(other))==15958 and set(rows)==set(other)
    assert all(len(a)==11 and max(a)<83 and min(a)>=0 and tuple(sorted(set(a)))==a and sidon(a)for a in rows)
    assert reports['eleven']['max_weight']==3999979 and max(sum(weights[x]for x in a)for a in rows)==3999979
    reports['twelve']=run([work/'enumerate',83,12,'all','-']);reports['twelve_reference']=run([work/'reference',83,12])
    assert reports['twelve']['complete'] and reports['twelve_reference']['complete'] and reports['twelve']['sets']==reports['twelve_reference']['sets']==0
    initial=list(profiles(8,83,11));assert len(initial)==7 and all(a.count(11)>=3 for a in initial)
    ordered=sorted(rows,key=lambda a:(-sum(weights[x]for x in a),bitmask(a)));regular=work/'ordered11.txt';regular.write_text(''.join(' '.join(map(str,a))+'\n'for a in ordered))
    orbit=canonical(rows,weights);orbitpath=work/'orbit11.txt';orbitpath.write_text(''.join(' '.join(map(str,a))+'\n'for a in orbit))
    reports['five_packing']=run([work/'pack_five',regular,SOURCE/'weights.txt',work/'five.txt'])
    reports['five_reference']=run([work/'pack_five_reference',83,11,5,work/'raw11.txt',SOURCE/'weights.txt',work/'five_reference.txt'])
    same(work/'five.txt',work/'five_reference.txt');same(regular,work/'five_reference.txt.sets')
    tuples=[tuple(map(int,line.split()))for line in(work/'five.txt').read_text().splitlines()];assert len(tuples)==len(set(tuples))==2142
    domains=[]
    for ids in tuples:
        assert len(ids)==5 and tuple(sorted(set(ids)))==ids
        union=set()
        for i in ids:
            assert 0<=i<len(ordered) and not union.intersection(ordered[i]);union.update(ordered[i])
        assert sum(weights[x]for x in union)>=19134774
        domains.append(tuple(sorted(set(range(83))-union)))
    assert len(set(domains))==2142 and all(len(a)==28 for a in domains)
    (work/'five_domains.txt').write_text(''.join(' '.join(map(str,a))+'\n'for a in domains))
    reports['five_completion']=[]
    for method in [0,1]:
        record=run([work/'complete28',method,work/'five_domains.txt',work/f'five_trace_{method}.bin',work/f'five_decisions_{method}.jsonl'])
        assert record['complete'] and record['domains']==2142 and record['found']==0 and record['ten_occurrences']==66 and record['nine_occurrences']==2 and record['eleven_occurrences']==0
        reports['five_completion'].append(record)
    same(work/'five_trace_0.bin',work/'five_trace_1.bin');same(work/'five_decisions_0.jsonl',work/'five_decisions_1.jsonl')
    print('All five-eleven profiles excluded; regenerating full tens.',flush=True)
    def full_tens(method):
        full,heavy=work/f'full_{method}.bin',work/f'heavy_{method}.bin'
        record=run([work/'catalog',method,dp,full,10,wp]);assert record['complete'] and record['sets']==24751806 and record['max_weight']==3999980
        filtered=run([work/'exclude_four','filter',SOURCE/'weights.txt',full,heavy]);assert filtered==dict(sets=24751806,kept=4832138,cutoff=3567387,maximum=3999980,complete=True)
        return dict(generation=record,filter=filtered,full_sha256=digest(full),heavy_sha256=digest(heavy))
    with ThreadPoolExecutor(max_workers=min(2,args.jobs))as pool:reports['ten_catalogs']=list(pool.map(full_tens,[0,1]))
    same(work/'full_0.bin',work/'full_1.bin');same(work/'heavy_0.bin',work/'heavy_1.bin')
    print('Both full ten catalogs match; completing all four-eleven cases.',flush=True)
    def sweep(task):
        method,shard=task;prefix=work/f'four_{method}_{shard}';marker=prefix.with_suffix('.done')
        if marker.exists():marker.unlink()
        record=run([work/'exclude_four',method,orbitpath,SOURCE/'weights.txt',work/f'heavy_{method}.bin',shard,args.jobs,prefix.with_suffix('.csv'),prefix.with_suffix('.bin'),prefix.with_suffix('.jsonl'),marker])
        assert record['complete'] and record['found']==0 and marker.read_text()=='complete\n'
        record.update(shard=shard,parts=args.jobs,trace_sha256=digest(prefix.with_suffix('.bin')),trace_bytes=prefix.with_suffix('.bin').stat().st_size)
        print(f'Completed four-eleven method {method}, shard {shard}.',flush=True)
        return record
    with ThreadPoolExecutor(max_workers=args.jobs)as pool:reports['four_sweeps']=list(pool.map(sweep,[(m,s)for m in [0,1]for s in range(args.jobs)]))
    four_rows=[]
    for method in [0,1]:
        rows4=[]
        for shard in range(args.jobs):rows4 += [{k:int(v)for k,v in r.items()}for r in csv.DictReader((work/f'four_{method}_{shard}.csv').open())]
        rows4.sort(key=lambda r:r['orbit']);assert [r['orbit']for r in rows4]==list(range(2701))
        totals={k:sum(r[k]for r in rows4)for k in EXPECTED['four_totals']};assert totals==EXPECTED['four_totals'],totals
        four_rows.append(rows4)
    assert four_rows[0]==four_rows[1]
    terminals=[]
    for shard in range(args.jobs):
        same(work/f'four_0_{shard}.bin',work/f'four_1_{shard}.bin');same(work/f'four_0_{shard}.jsonl',work/f'four_1_{shard}.jsonl')
        terminals += [json.loads(s)for s in(work/f'four_0_{shard}.jsonl').read_text().splitlines()]
    terminals.sort(key=lambda r:(r['eleven_ids'],r['chosen_tens']))
    assert len(terminals)==380
    for r in terminals:
        elevens=[orbit[i]for i in r['eleven_ids']];tens=r['chosen_tens'];nine=r['residual']
        assert len(elevens)==4 and len(tens)==3 and len(nine)==9
        assert all(sidon(a)for a in [*elevens,*tens]) and not sidon(nine) and not r['sidon']
        assert sorted(x for a in [*elevens,*tens,nine]for x in a)==list(range(83))
        tw=[sum(weights[x]for x in a)for a in tens];assert tw==sorted(tw,reverse=True)
        r['collision']=collision(nine);assert sum(r['collision'][0])==sum(r['collision'][1])
    reports['terminal_occurrences']=len(terminals);reports['terminal_distinct_nines']=len({tuple(r['residual'])for r in terminals})
    (work/'terminal_examples.json').write_text(json.dumps(terminals[:2]+terminals[-2:],indent=2)+'\n')
    (work/'all_terminals.json').write_text(json.dumps(terminals)+'\n');reports['all_terminals_sha256']=digest(work/'all_terminals.json')
    with (work/'cases_four.csv').open('w')as f:
        writer=csv.DictWriter(f,fieldnames=list(four_rows[0][0]),lineterminator='\n');writer.writeheader();writer.writerows(four_rows[0])
    print('The four-eleven profile is excluded; checking the remaining global triple cover.',flush=True)
    reports['three_counts']=[]
    for method in [0,1]:
        record=run([work/'count_three',method,orbitpath,SOURCE/'weights.txt',work/f'three_{method}.csv'])
        assert record['complete'] and record['cases']==5364 and record['nonempty']==5157 and record['packings']==65073232
        reports['three_counts'].append(record)
    same(work/'three_0.csv',work/'three_1.csv')
    with (work/'cases_three.csv').open('w')as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['orbit','packings'])
        for r in csv.DictReader((work/'three_0.csv').open()):writer.writerow([int(r['orbit']),int(r['packings'])])
    landscape={'initial_profiles':[list(a)for a in initial],'max_sidon_size':11,'five_or_more_elevens':'excluded','four_elevens':'excluded','only_remaining_profile':[11,11,11,10,10,10,10,10],'eligible_anchor_cases':5364,'packing_empty_cases':207,'nonempty_cases':5157,'anchored_triples':65073232,'P83_decided':False}
    (work/'landscape.json').write_text(json.dumps(landscape,indent=2)+'\n')
    hashes={name:digest(work/name)for name in ['raw11.txt','ordered11.txt','orbit11.txt','five.txt','five_domains.txt','five_trace_0.bin','cases_four.csv','cases_three.csv','terminal_examples.json','landscape.json']}
    for name in ['cases_four.csv','cases_three.csv','terminal_examples.json','landscape.json']:
        if(SOURCE/name).exists():same(work/name,SOURCE/name)
    reports.update(verified=True,profile_only=True,landscape=landscape,hashes=hashes,seconds=time.monotonic()-start,jobs=args.jobs,python=sys.version,compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0],child_max_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    (work/'verification.json').write_text(json.dumps(reports,indent=2)+'\n')
    print(json.dumps(dict(verified=True,remaining_profile=landscape['only_remaining_profile'],nonempty_cases=5157,anchored_triples=65073232,seconds=reports['seconds'])))

if __name__=='__main__':main()
