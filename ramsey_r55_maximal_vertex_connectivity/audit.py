#!/usr/bin/env python3
"""Independent dense physical/certificate auditor; imports no producer."""
import argparse,hashlib,json
from pathlib import Path
from itertools import combinations,permutations
from collections import Counter

def need(ok,message):
    if not ok:raise ValueError(message)

def matrix(n,word):
    need(type(word) is int and 0<=word<1<<(n*(n-1)//2),'physical graph code')
    a=[[False]*n for _ in range(n)]
    for k,(u,v) in enumerate(combinations(range(n),2)):
        a[u][v]=a[v][u]=bool(word>>k&1)
    return a

def independent(a,q):
    return all(not a[u][v] for u,v in combinations(q,2))

def certify_graph(record):
    need(set(record)=={'n','h','core','code','beta','triangle','cover'},'witness fields')
    n,h=record['n'],record['h']
    need((n,h) in ((10,6),(10,7),(10,8),(11,7),(11,8)),'marked order')
    a=matrix(n,record['code'])
    core=matrix(h,record['core'])
    need(all(a[u][v]==core[u][v] for u,v in combinations(range(h),2)),'physical core mismatch')
    need(independent(a,range(h,n)),'mark not independent')
    need(not any(all(a[u][v] for u,v in combinations(t,2)) for t in combinations(range(n),3)),'physical triangle')
    need(not any(independent(a,t) for t in combinations(range(n),5)),'physical independent five')
    triples=[q for q in combinations(range(n),3) if independent(a,q)]
    values={}
    for q in triples:
        contacts=[sum(a[v][u] for u in q) for v in range(n) if v not in q]
        values[sum(1<<u for u in q)]=2*n+1-2*contacts.count(3)-contacts.count(2)
    beta=min(values.values())
    need(record['beta']==beta and values.get(record['triangle'])==beta,'triangle/contact identity witness mismatch')
    need(beta<20 if n==10 else beta<21,'marked degree-bound theorem failed')
    cover=record['cover']
    if n==10 or beta<19:
        need(cover==[],'unexpected cover on degree-excluded graph')
        return beta,0
    need(isinstance(cover,list) and len(cover) in (1,2) and len(set(cover))==len(cover),'cover shape')
    cost=0
    for mask in cover:
        need(mask in values,'cover is not a red triangle')
        q=[v for v in range(n) if mask>>v&1]
        common=sum(all(not a[u][v] for u in q) for v in range(n) if v not in q)
        cost+=4-common
    need(cost<=6,'triangle cover exceeds six')
    fours=[set(q) for q in combinations(range(n),4) if independent(a,q)]
    specials=0
    # Test ALL independent contact-complements of sizes0..4, including the
    # smaller sizes omitted by the producer using the Ramsey(3,4) bound.
    for size in range(5):
        for q in combinations(range(n),size):
            if not independent(a,q) or any(set(q).isdisjoint(t) for t in fours):continue
            specials+=1
            red_set=set(range(n))-set(q)
            need(any(all(v in red_set for v in range(n) if mask>>v&1) for mask in cover),'uncovered special attachment')
    need(specials>0,'missing marked attachment')
    return beta,cost

def core_audit(summary,path):
    literal={n:set() for n in (6,7,8)}
    for line in Path(path).read_text().splitlines():
        tag,n,code=line.split();n=int(n);code=int(code)
        need(tag=='C' and n in literal and code not in literal[n],'native core stream')
        literal[n].add(code)
    total=0
    for n in (6,7,8):
        union=set()
        for row in summary['core_orbits'][str(n)]:
            a=matrix(n,row['code']);orbit=set()
            for p in permutations(range(n)):
                orbit.add(sum(int(a[p[u]][p[v]])<<k for k,(u,v) in enumerate(combinations(range(n),2))))
            need(len(orbit)==row['orbit_size'] and not(union&orbit),'core orbit size/disjointness')
            union|=orbit
        need(union==literal[n],'complete labeled core sets differ')
        total+=len(union)
    counts=[]
    for n in range(1,6):
        count=0
        for word in range(1<<(n*(n-1)//2)):
            a=matrix(n,word)
            if any(all(a[u][v] for u,v in combinations(q,2)) for q in combinations(range(n),3)):continue
            if any(independent(a,q) for q in combinations(range(n),4)):continue
            count+=1
        counts.append(count)
    need(counts+[len(literal[n]) for n in (6,7,8)]==summary['labeled_core_counts_n1_to_n8'],'labeled induction counts')
    return total

def global_cases():
    rows=[]
    for k in range(19,24):
        for a in range(7,14):
            b=43-k-a
            if not a<=b<=13:continue
            row={'separator_size':k,'component_orders':[a,b]}
            if a<=9:
                need(2*a+1<k,'small order inequality')
                row.update(reason='triangle_contact_identity',upper=2*a+1)
            elif a==10 and k>=21:
                row.update(reason='independent_triple_with_common_blue_neighbor',upper=20)
            elif (k,a,b)==(21,11,11):
                row.update(reason='marked11_degree_bound_forbids_all_specials',special_upper=0)
            elif (k,a,b)==(20,10,13):
                row.update(reason='marked10_degree_bound_forbids_all_specials',special_upper=0)
            elif (k,a,b)==(20,11,12):
                row.update(reason='special_cover',special_upper=10)
            elif (k,a,b)==(19,11,13):
                row.update(reason='special_cover',special_upper=6)
            elif (k,a,b)==(19,12,12):
                row.update(reason='special_cover',special_upper=8)
            else:raise ValueError(('uncovered global order pair',k,a,b))
            if 'special_upper' in row:need(row['special_upper']<k,'failed special capacity contradiction')
            rows.append(row)
    need(len(rows)==14,'global order coverage count')
    return rows

def audit(directory,cores,marked):
    directory=Path(directory)
    summary=json.loads((directory/'SUMMARY.json').read_text())
    core_total=core_audit(summary,cores)
    expected_jobs=[(n,h,c['code']) for n in (10,11) for h in range(n-4,9) for c in summary['core_orbits'][str(h)]]
    jobs=[tuple(map(int,line.split())) for line in (directory/'jobs.txt').read_text().splitlines()]
    need(jobs==expected_jobs,'complete marked job registry')
    row_data={job:{'hist':Counter(),'covers':0,'count':0,'digest':hashlib.sha256()} for job in jobs}
    costs=Counter();fixture_records=[];total=0;last=None
    with (directory/'witnesses.jsonl').open() as source,Path(marked).open() as native:
        while True:
            line=source.readline();other=native.readline()
            need(bool(line)==bool(other),'marked stream length mismatch')
            if not line:break
            record=json.loads(line);parts=other.split()
            need(len(parts)==5 and parts[0]=='M','native marked stream syntax')
            key=tuple(map(int,parts[1:]))
            need(key==(record['n'],record['h'],record['core'],record['code']),'entry-level marked graph mismatch')
            need(last is None or key>last,'duplicate/out-of-order marked graph')
            last=key;job=key[:3];need(job in row_data,'unknown marked job')
            beta,cost=certify_graph(record)
            row=row_data[job];row['hist'][beta]+=1;row['covers']+=bool(record['cover']);row['count']+=1;row['digest'].update(line.encode())
            if record['cover']:costs[cost]+=1
            if len(fixture_records)<1 or (record['cover'] and not any(x['cover'] for x in fixture_records)):fixture_records.append(record)
            total+=1
    reconstructed=[]
    for n,h,core in jobs:
        row=row_data[n,h,core]
        reconstructed.append({'n':n,'h':h,'core':core,'marked_graphs':row['count'],'beta_histogram':{str(k):v for k,v in sorted(row['hist'].items())},'cover_certificates':row['covers'],'witness_stream_sha256':row['digest'].hexdigest()})
    need(reconstructed==summary['rows'],'per-job complete statistics/hashes mismatch')
    need(total==summary['marked10']+summary['marked11'] and sum(costs.values())==summary['covers'],'summary totals')
    # Corrupt physical, degree, mark and cover certificates; no expected hash
    # substitutes for checking the content of these mutations.
    import copy
    bad=[]
    x=copy.deepcopy(fixture_records[0]);x['beta']+=1;bad.append(x)
    x=copy.deepcopy(fixture_records[0]);x['triangle']=0;bad.append(x)
    x=copy.deepcopy(fixture_records[0]);x['core']^=1;bad.append(x)
    x=copy.deepcopy(fixture_records[1]);x['cover']=[];bad.append(x)
    x=copy.deepcopy(fixture_records[1]);x['cover']=[0];bad.append(x)
    for x in bad:
        try:certify_graph(x)
        except ValueError:continue
        raise ValueError('false graph/capacity certificate accepted')
    return {'status':'VERIFIED_MAXIMAL_VERTEX_CONNECTIVITY_FINITE_PROOF','complete_labeled_core_graphs':core_total,'complete_marked_jobs':len(jobs),'physical_marked_graphs_checked':total,'marked10':summary['marked10'],'marked11':summary['marked11'],'triangle_cover_certificates':sum(costs.values()),'cover_cost_histogram':dict(sorted(costs.items())),'global_order_cases':global_cases(),'rejected_witness_mutations':len(bad),'fixture_records':fixture_records,'catalog_completeness_required':False,'new_physical_packing_tasks_decided':0,'good43_found':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('cores',type=Path);p.add_argument('marked',type=Path);a=p.parse_args()
    print(json.dumps(audit(a.directory,a.cores,a.marked),indent=2,sort_keys=True))
