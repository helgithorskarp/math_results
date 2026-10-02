"""Exact ordinary root-cut and degree-profile bridge checks for the candidate."""
from argparse import ArgumentParser
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import hashlib, json, time, resource

def derive():
    roots=[]
    for high_A in range(3):
        degree_sum=81+3*high_A
        for h in range(0,13,3):
            k=102-degree_sum+h
            if 30<=k<=66:
                roots.append(dict(high_A=high_A,A_degree_sum=degree_sum,H_edges=h,K_edges=k))
    expected=[(0,81,9,30),(0,81,12,33),(1,84,12,30)]
    if [tuple(r.values()) for r in roots]!=expected:
        raise ValueError('Complete root cuts differ')

    # Symbolic degree capacity, independently compared with every literal H word.
    degree9=[]
    for d in product(range(4),repeat=3):
        if sum(d)==6:
            capacity=99-3*sum(x*(x-1)//2 for x in d)
            if capacity>90:
                raise ValueError('H9 capacity bound')
            degree9.append(dict(orbit_degrees=list(d),capacity=capacity,column_overlap=96))
    pairs=list(combinations(range(9),2))
    h9_words=[]
    h12_words=[]
    for word in range(4096):
        H=[]
        for u in range(9):
            row=set()
            i,t=divmod(u,3)
            for v in range(9):
                if u==v:continue
                j,s=divmod(v,3)
                bit=i if i==j else {(0,1):3,(0,2):6,(1,2):9}[min(i,j),max(i,j)]+((s-t)%3 if i<j else (t-s)%3)
                if word>>bit&1:row.add(v)
            H.append(row)
        h=sum(map(len,H))//2
        if h not in [9,12] or max(map(len,H))>3:continue
        caps=[]
        for u,v in pairs:
            if v in H[u]:caps.append(2-len(H[u]&H[v]))
            else:
                blue_A=sum(w not in H[u] and w not in H[v] for w in range(9) if w not in [u,v])
                caps.append(6-blue_A-(12-(8-len(H[u]))-(8-len(H[v]))))
        formula=108-h-sum(len(r)*(len(r)-1)//2 for r in H)
        if sum(caps)!=formula:
            raise ValueError('Literal all-nine capacity identity')
        if h==9:
            if formula>90:raise ValueError('Literal H9 bound')
            h9_words.append(word)
        else:
            if formula!=75:raise ValueError('Literal H12 bound')
            h12_words.append(word)

    # Ten ordered K degree patterns, only global-degree-preserving transports.
    DB=(9,9,10,10)
    reps={'rejected_seven_at9':(7,5,5,5),'G7':(5,5,7,5),
          'rejected_both_sixes_at9':(6,6,5,5),'GM':(6,5,6,5),'G6':(5,5,6,6)}
    transports=[(a,b,c,d) for a,b in [(0,1),(1,0)] for c,d in [(2,3),(3,2)]]
    beta_records=[]
    for beta in product(range(5,8),repeat=4):
        if sum(beta)!=22:continue
        images={tuple(beta[i] for i in order) for order in transports}
        names=[name for name,rep in reps.items() if rep in images]
        if len(names)!=1:raise ValueError('Entire marked K transport partition')
        size=[d-b for d,b in zip(DB,beta)]
        overlap=3*sum(s*(s-1)//2 for s in size)
        retained=overlap<=75
        if retained!=(not names[0].startswith('rejected')):
            raise ValueError('Complete K marking/capacity cut')
        beta_records.append(dict(orbit_degrees=list(beta),column_sizes=size,column_overlap=overlap,
                                 retained=retained,mode=names[0]))

    # Classification-free corollary only: seven free orbit marks in7..10 sum65.
    all_marks=[]
    hist=Counter()
    for marks in product(range(7,11),repeat=7):
        if sum(marks)!=65:continue
        all_marks.append(marks)
        hist[tuple(marks.count(d) for d in range(7,11))]+=1
    independent=[]
    def recurse(prefix,total):
        left=7-len(prefix)
        if not 7*left<=65-total<=10*left:return
        if left==0:
            independent.append(tuple(prefix));return
        for degree in range(7,11):recurse(prefix+[degree],total+degree)
    recurse([],0)
    if all_marks!=independent:raise ValueError('Entire ordered degree domains differ')
    profiles=[]
    for counts,n in sorted(hist.items()):
        global_counts=[3*c+(1 if d==9 else 0) for d,c in zip(range(7,11),counts)]
        square=sum(c*d*d for d,c in zip(range(7,11),global_counts))
        doubled_W=-6468+120*102-3*square
        b,a,_,c=counts
        if c!=a+2*b+2 or doubled_W!=2*(42-9*a-27*b):
            raise ValueError('Literal degree/deficit profile identity')
        profiles.append(dict(free_degree_counts=list(counts),global_degree_counts=global_counts,
                             ordered_marks=n,deficit_weight=doubled_W//2))
    if len(profiles)!=5:raise ValueError('Five E102 profiles')
    record=dict(root_cuts=roots,H9_degree_capacity_cases=degree9,
                H9_literal_words=len(h9_words),H12_literal_words=len(h12_words),
                K33_ordered_marks=beta_records,ordered_degree_domain=16384,
                degree_sum_matches=len(all_marks),profiles=profiles,
                whole_degree_domains_equal=True)
    return record,dict(H9_words=h9_words,H12_words=h12_words,ordered_free_degree_marks=all_marks)

def main():
    parser=ArgumentParser();parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args();args.work.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();record,domains=derive()
    raw=json.dumps(record,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n'
    (args.work/'analytic.json').write_text(raw)
    (args.work/'analytic-domains.json').write_text(json.dumps(domains,indent=2)+'\n')
    if time.monotonic()-start>25:raise RuntimeError('INCOMPLETE analytic guard; no exclusion')
    print(json.dumps(dict(status='COMPLETE_ORDINARY_BRIDGE_AUDIT',agent='six-books-2',role='researcher',
                         mathematical_bytes=len(raw.encode()),sha256=hashlib.sha256(raw.encode()).hexdigest(),
                         seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                         record=record),indent=2))

if __name__=='__main__':main()
