#!/usr/bin/env python3
"""Compare every physical domain entry with the later author-source replay.

The complete Xi row-domain is independently reconstructed here from literal
Python neighbor sets, not copied from either native output or the author.
"""
import argparse
from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path
from reproduce import canonical, require

UNIVERSE=frozenset(range(22))
EP=tuple(range(9,16))

def key(row):
    return (row[0],tuple(row[1:6]),tuple(row[6:12])+((6,5) if row[0]==0 else (5,6)),
            row[12],row[13],tuple(row[14:20]))

def build(row):
    r=[set() for _ in range(22)]
    def e(i,j):r[i].add(j);r[j].add(i)
    for v in range(1,11):e(0,v)
    for v in [2,11,12]:e(1,v)
    for v in range(9,16):e(2,v)
    for i,j in [(0,4),(4,3),(3,1),(1,2),(2,5),(5,0)]:e(i+3,j+3)
    for s,own in [(9,[6,8]),(10,[5,7])]:
        for v in own:e(s,v)
    columns=list(row[6:12])+([6,5] if row[0]==0 else [5,6])
    for i,c in enumerate(columns):
        for t in range(3):
            if c&(1<<t):e(i+3,13+t)
    for s,c in [(11,6),(12,3)]:
        for t in range(3):
            if c&(1<<t):e(s,13+t)
    for s,c in [(11,row[12]),(12,row[13])]:
        for i in range(6):
            if c&(1<<i):e(s,3+i)
    return tuple(frozenset(v) for v in r)

def complete(seed,i,mask):
    red=seed[i]|frozenset(16+y for y in range(6) if mask&(1<<y))
    return red,UNIVERSE-red-{i}

def valid(seed,i,j,left,right):
    color=0 if j in seed[i] else 1
    return len(left[color]&right[color])<=(3 if color==0 else 6)

def check_x(row,seed):
    low=row[1:6]
    degrees=[10,10,9]+[10]*8+[10-low[3],10-low[4]]+[10-l for l in low[:3]]
    q=[degrees[i]-len(seed[i]) for i in range(16)]
    require(q==[0,6,0]+[3+b for b in row[14:20]]+[4,4,2,2,3,2,3],'literal row budget')
    require(sum(row[14:20])==1+sum(low),'tagged cut')
    for i,j in combinations(range(16),2):
        if j in seed[i]:
            require(len(seed[i]&seed[j])+max(0,q[i]+q[j]-6)<=3,'X red projected cap')
        else:
            bi=frozenset(range(16))-seed[i]-{i};bj=frozenset(range(16))-seed[j]-{j}
            require(len(bi&bj)+max(0,6-q[i]-q[j])<=6,'X blue projected cap')
    return q

def convert(full):
    native=full['records'];xrows=native['x'];xs=sorted(key(r) for r in xrows)
    xi={x:i for i,x in enumerate(xs)};physical={key(r):r for r in xrows}
    for r in xrows:
        check_x(r,build(r))
    def frame(r):return (xi[key(r)],(r[20]&r[21]).bit_count(),*r[24:27],*r[22:24])
    ys=sorted(frame(r) for r in native['frames']);yi={v:i for i,v in enumerate(ys)}
    require(len(yi)==len(ys),'duplicate physical frame')
    rows=[];last=None;checked_pairs=0;cartesian=0
    for index,v in enumerate(ys):
        xindex,intersection,t0,t1,t2,sy0,sy1=v
        if xindex!=last:
            last=xindex;row=physical[xs[xindex]];seed=build(row);q=check_x(row,seed)
            options=[[(mask,complete(seed,3+i,mask)) for mask in range(64) if mask.bit_count()==q[3+i]] for i in range(6)]
            cache={}
        masks=[15,51 if intersection==2 else 23,sy0,sy1,t0,t1,t2]
        endpoints=[]
        for e,mask in zip(EP,masks):
            if (e,mask) not in cache:cache[e,mask]=complete(seed,e,mask)
            endpoints.append(cache[e,mask])
        for i,j in combinations(range(7),2):
            require(valid(seed,EP[i],EP[j],endpoints[i],endpoints[j]),'literal endpoint cap')
            checked_pairs+=1
        candidate=[]
        for i in range(6):
            candidate.append(tuple(mask for mask,color in options[i]
                                   if all(valid(seed,3+i,e,color,other) for e,other in zip(EP,endpoints))))
        if all(candidate):
            count=1
            for c in candidate:count*=len(c)
            cartesian+=count;rows.append((index,tuple(candidate)))
    require(cartesian==full['metadata']['cartesian_tuples'],'complete Cartesian volume')
    joins=[];witnesses={};bad_hist=Counter();spine_types=Counter();sy_sums=Counter();sy_pages=Counter()
    for r in native['joins']:
        v=(yi[frame(r)],tuple(r[27:33]),sum(b<<y for y,b in enumerate(r[33:39])))
        joins.append(v)
        seed=[set(a) for a in build(r)]
        for i,mask in enumerate([0,63,0]+list(r[27:33])+list(r[20:27])):
            for y in range(6):
                if mask&(1<<y):seed[i].add(16+y);seed[16+y].add(i)
        require(all(not(seed[y]&set(range(16,22))) for y in range(16,22)),'Q-internal edge entered')
        violations=[]
        for i,j in combinations(range(22),2):
            if j in seed[i] and len(seed[i]&seed[j])>=4:
                pages=sorted(seed[i]&seed[j]);violations.append((i,j,pages))
                spine_types['K-Q' if j>=16 else 'K-K']+=1
        require(violations,'missing known-edge red book')
        i,j,pages=violations[0]
        require([i,j,sum(1<<p for p in pages)]==r[39:42],'native whole first witness')
        require([len(violations),sum(len(p)-3 for _,_,p in violations)]==r[42:44],'native all-violation inventory')
        witnesses[v]=(i,j,tuple(pages[:4]));bad_hist[len(violations)]+=1
        require(r[12]&r[13]==0 and r[12]|r[13]==63,'surviving SY-X partition')
        sy_counts=[len(seed[s]&seed[y]) for s in (11,12) for y in sorted(seed[s]&set(range(16,22)))]
        require(len(sy_counts)==4 and sum(sy_counts)>12,'four-SY-spine aggregate obstruction')
        sy_sums[sum(sy_counts)]+=1;sy_pages[tuple(sorted(sy_counts))]+=1
    joins.sort();books=[(i,*witnesses[v]) for i,v in enumerate(joins)]
    values={'X':xs,'Y_endpoints':ys,'XY_rows':rows,'XY_joins':joins,'red_books':books}
    return values,{'literal_endpoint_pairs_checked':checked_pairs,'literal_X_interfaces_checked':len(xs),
                   'complete_cartesian_volume':cartesian,'all_join_witnesses_checked':len(joins),
                   'violating_red_spines_histogram':dict(sorted(bad_hist.items())),
                   'violating_red_spine_types':dict(spine_types),
                   'four_SY_Q_spine_page_sum_histogram':dict(sorted(sy_sums.items())),
                   'four_SY_Q_sorted_page_vectors':[{'pages':list(k),'joins':v} for k,v in sorted(sy_pages.items())],
                   'all_surviving_SY_X_rows_partition_six':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--independent',type=Path,required=True)
    ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    full=json.loads(a.independent.read_text());author=json.loads(a.author.read_text())
    values,checks=convert(full)
    receipt={}
    for name,domain in values.items():
        require(canonical(domain)==canonical(author['domains'][name]),f'whole physical {name} mismatch')
        receipt[name]={'count':len(domain),'every_entry_equal':True,
                       'author_format_sha256':hashlib.sha256(json.dumps(domain,separators=(',',':')).encode()).hexdigest()}
    record={'complete':True,'domains':receipt,'checks':checks,'comparison_basis':'every decoded physical entry, not counts alone'}
    a.out.write_bytes(canonical(record));print(json.dumps(record,indent=2))

if __name__=='__main__':main()
