#!/usr/bin/env python3
"""Reproduce the global P82 profile theorem and remaining balanced case cover."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import resource
import sys
import time
from checks import SOURCE,PARENT,run,build,digest,same,mask,sidon,profiles,rows,write_rows,canonical,controls,verify,audit_pairs


def main():
    if not __debug__:raise SystemExit('Assertions are proof checks; do not use -O/PYTHONOPTIMIZE.')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work',type=Path,required=True);parser.add_argument('--jobs',type=int,default=4);parser.add_argument('--workers',type=int,default=6);parser.add_argument('--sanitizers',action='store_true')
    args=parser.parse_args();work=args.work.resolve()
    assert PARENT not in [work,*work.parents]and 1<=args.jobs<=12 and 1<=args.workers<=12
    work.mkdir(parents=True,exist_ok=True);start=time.monotonic();records={}
    programs={'enumerate':PARENT/'enumerate.cpp','reference':PARENT/'reference.cpp','catalog':PARENT/'p84_weight_certificates/weighted_catalog.cpp',**{s:SOURCE/(s+'.cpp')for s in ['landscape','reference_weighted','pack_five','pack_five_reference']}}
    for name,source in programs.items():build(source,work/name)
    weights=list(map(int,(SOURCE/'weights.txt').read_text().split()))
    v=list(map(int,(PARENT/'p84_profiles/weights.txt').read_text().split()))
    assert weights==[v[i]+v[i+2]for i in range(82)]and len(weights)==82 and sum(weights)==30884468 and max(weights)==444444 and weights==weights[::-1]
    padded=work/'weights_padded.txt';padded.write_text(' '.join(map(str,weights+[0,0]))+'\n');domain=work/'domain82.txt';write_rows(domain,[range(82)])
    records['eleven']=run([work/'enumerate',82,11,'all',work/'raw11.txt',SOURCE/'weights.txt'])
    records['eleven_reference']=run([work/'reference',82,11,work/'reference11.txt'])
    raw,other=rows(work/'raw11.txt'),rows(work/'reference11.txt')
    assert set(raw)==set(other)and len(raw)==len(other)==len(set(raw))==8214
    assert all(len(a)==11 and tuple(sorted(set(a)))==a and min(a)>=0 and max(a)<82 and sidon(a)for a in raw)
    assert records['eleven']['complete']and records['eleven_reference']['complete']and records['eleven']['max_weight']==max(sum(weights[x]for x in a)for a in raw)==3999978
    records['twelve']=run([work/'enumerate',82,12,'all','-']);records['twelve_reference']=run([work/'reference',82,12])
    assert all(records[k]['complete']and records[k]['sets']==0 for k in ['twelve','twelve_reference'])
    initial=list(profiles(8,82,11));assert len(initial)==11
    assert [a.count(11)for a in initial]==[7,6,6,6,5,5,5,4,4,3,2]
    records['initial_profiles']=initial
    orbit=canonical(raw,weights);write_rows(work/'orbit11.txt',orbit)
    ordered=sorted(raw,key=lambda a:(-sum(weights[x]for x in a),mask(a)));write_rows(work/'ordered11.txt',ordered)
    records['nine_cap']=run([work/'enumerate',82,9,'all','-',SOURCE/'weights.txt'])
    records['nine_cap_reference']=run([work/'reference_weighted',82,9,'-',SOURCE/'weights.txt'])
    assert all(records[k]['complete']and records[k]['sets']==431916048 and records[k]['max_weight']==3776423 for k in ['nine_cap','nine_cap_reference'])
    def catalog(method):
        record=run([work/'catalog',method,domain,work/f'full_{method}.bin',10,padded])
        assert record['complete']and record['sets']==17249580 and record['max_weight']==3999979
        return record
    with ThreadPoolExecutor(max_workers=min(2,args.workers))as pool:records['ten_catalogs']=list(pool.map(catalog,[0,1]))
    same(work/'full_0.bin',work/'full_1.bin')
    records['five']=run([work/'pack_five',work/'ordered11.txt',SOURCE/'weights.txt',work/'five.txt'])
    records['five_reference']=run([work/'pack_five_reference',82,11,5,work/'raw11.txt',SOURCE/'weights.txt',work/'five_reference.txt'])
    assert all(records[k]['complete']and records[k]['packings']==10 for k in ['five','five_reference'])
    same(work/'five.txt',work/'five_reference.txt');same(work/'ordered11.txt',work/'five_reference.txt.sets')
    tuples=rows(work/'five.txt');assert len(tuples)==len(set(tuples))==10;domains=[]
    for ids in tuples:
        assert len(ids)==5 and ids==tuple(sorted(set(ids)))and all(0<=i<len(ordered)for i in ids)
        used=[x for i in ids for x in ordered[i]]
        assert len(used)==len(set(used))==55 and sum(weights[x]for x in used)>=18884468
        domains.append(sorted(set(range(82))-set(used)))
    assert len(set(map(tuple,domains)))==10
    write_rows(work/'five_domains.txt',domains);ps=list(profiles(3,27,11));assert len(ps)==7;write_rows(work/'profiles27.txt',ps)
    records['five_completion']=[]
    for method in [0,1]:
        pre=work/f'five_completion_{method}'
        r=run([work/'landscape','complete',method,SOURCE/'weights.txt',work/'profiles27.txt',work/'five_domains.txt',pre.with_suffix('.bin'),pre.with_suffix('.jsonl'),pre.with_suffix('.done')])
        assert r['complete']and r['domains']==10 and r['found']==0
        records['five_completion'].append(r)
    same(work/'five_completion_0.bin',work/'five_completion_1.bin');same(work/'five_completion_0.jsonl',work/'five_completion_1.jsonl')
    records['controls']=controls(work/'landscape',work,work/'catalog')
    if args.sanitizers:
        build(SOURCE/'landscape.cpp',work/'landscape_sanitized',True)
        records['sanitizer_controls']=controls(work/'landscape_sanitized',work,work/'catalog')
    print('Catalogs, five-eleven profiles and controls verified.',flush=True)
    for k in [2,3,4]:
        for method in [0,1]:
            run([work/'landscape','count',method,k,work/'orbit11.txt',SOURCE/'weights.txt',work/f'count{k}_{method}.csv'])
    def sweep(task):
        k,m,shard=task;pre=work/f'sweep{k}_{m}_{shard}'
        args0=[work/'landscape','sweep',m,k,work/'orbit11.txt',SOURCE/'weights.txt',work/f'full_{m}.bin',shard,args.jobs,pre.with_suffix('.csv'),pre.with_suffix('.bin'),pre.with_suffix('.jsonl'),pre.with_suffix('.done')]
        if pre.with_suffix('.done').exists():pre.with_suffix('.done').unlink()
        r=run(args0);pre.with_suffix('.out').write_text(json.dumps(r)+'\n')
        assert r['complete']and r['found']==0
        print(f'Complete: {k} elevens, method {m}, shard {shard}',flush=True)
        return dict(anchors=k,method=m,shard=shard,result=r)
    with ThreadPoolExecutor(max_workers=args.workers)as pool:records['sweeps']=list(pool.map(sweep,[(k,m,j)for k in [4]for m in [1,0]for j in range(args.jobs)]))
    records['pair_audit']=audit_pairs(orbit,weights,work/'count2_0.csv')
    records['verification']=verify(work,args.jobs)
    expected=json.loads((SOURCE/'expected.json').read_text());assert records['verification']==expected
    for k in [2,3,4]:same(work/f'cases_{k}.csv',SOURCE/f'cases_{k}.csv')
    same(work/'terminal_examples.json',SOURCE/'terminal_examples.json')
    records['hashes']={p:digest(work/p)for p in ['raw11.txt','reference11.txt','orbit11.txt','ordered11.txt','five.txt','five_domains.txt','full_0.bin','full_1.bin']}
    records.update(verified=True,seconds=time.monotonic()-start,python=sys.version,child_max_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    (work/'validation.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(dict(verified=True,remaining_profiles=[[11,11,11,10,10,10,10,9],[11,11,10,10,10,10,10,10]],remaining_cases=records['verification']['2']['nonempty_cases']+records['verification']['3']['nonempty_cases'],seconds=records['seconds'])),flush=True)
if __name__=='__main__':main()
