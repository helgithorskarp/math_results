"""Completeness by literal one-row extensions, not producer DFS traversal."""
import argparse,json
from literal import graph,need,digest
def check(proposal):
    supports,V,D,sq,ns,A,columns=graph()
    need(proposal['supports']==supports and proposal['V']==sorted(V) and proposal['D']==sorted(D),'full independently derived graph')
    tuples=proposal['tuples'];need(digest(tuples)==proposal['tuple_sha256'],'whole tuple hash')
    records={};visits=[0]*8;trials=[0]*8
    for raw_rows,raw_common in tuples:
        rows=tuple(raw_rows);common=frozenset(raw_common)
        need(1<=len(rows)<=7 and rows[0]==1 and list(rows)==sorted(set(rows)) and set(rows)<=set(sq),'actual ordered anchored rows')
        need(list(raw_common)==sorted(common) and len(common)>=6 and common<=set(ns),'actual entire column domain')
        actual=set(ns)
        for q in rows:actual.intersection_update(A[q])
        need(actual==set(common),'literal whole common neighborhood')
        need(rows not in records,'duplicate anchored state');records[rows]=common;visits[len(rows)]+=1
    need(records.get((1,))==frozenset(A[1]),'actual full anchored seed')
    for rows,common in records.items():
        if len(rows)>1:need(rows[:-1] in records,'missing actual prefix')
        if len(rows)==7:continue
        for q in sq:
            if q<=rows[-1]:continue
            trials[len(rows)+1]+=1;actual=common.intersection(A[q]);extension=rows+(q,)
            if len(actual)>=6:need(records.get(extension)==actual,'missing or false legal extension')
            else:need(extension not in records,'false retained extension')
    need(visits==proposal['visits'] and trials==proposal['trials'],'entire prefix/extension cover')
    need(visits[7]==0,'literal K7,6 counterexample')
    family=set(records.values());hist={};retained=0;max_closure=0
    for common in family:
        closure=[q for q in sq if common<=A[q]];max_closure=max(max_closure,len(closure))
        key=f'{len(closure)},{len(common)}';hist[key]=hist.get(key,0)+1
        for q in sq:
            C=common.intersection(A[q])
            if len(C)>=6:need(C in family,'entire literal intersection transition missing');retained+=1
    five=[(rows,sorted(common)) for rows,common in sorted(records.items()) if len(rows)==5]
    need(max(len(C) for rows,C in five)<=8,'actual K5,9 witness')
    cores=[]
    from itertools import combinations
    for a,b in ((10,13),(11,12)):
        for rows,C in five:
            for size in range(b-5,len(C)+1):
                for B0 in combinations(C,size):cores.append([a,b,list(rows),list(B0),C])
    result=dict(schema=1,method='literal complete one-row extension validation; entire common sets and closure/transitions',visits=visits,trials=trials,tuple_count=len(records),tuple_sha256=digest(tuples),distinct_intersections=len(family),closure_histogram=hist,max_closure=max_closure,all_state_transitions=len(family)*len(sq),retained_transitions=retained,complete_five_tuples=len(five),five_tuple_sha256=digest(five),core_count=len(cores),case10_13=sum(r[0]==10 for r in cores),case11_12=sum(r[0]==11 for r in cores),core_sha256=digest(cores),no_K5_9=True,no_K6_7=not any(len(rows)==6 and len(C)>=7 for rows,C in records.items()),no_K7_6=True)
    return result,cores
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--cores',required=True);args=ap.parse_args()
    result,cores=check(json.load(open(args.input)))
    open(args.cores,'w').write(json.dumps(cores,separators=(',',':'))+'\n')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
