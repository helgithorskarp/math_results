#!/usr/bin/env python3
"""Producer-independent audit: literal catalog coverage, matrices and edge scores."""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
PIN='83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0'

def need(ok,message):
    if not ok:raise ValueError(message)

def decode(s):
    need(len(s)==47 and s[0]==87,'graph6 header')
    word=0
    for ch in s[1:]:
        need(63<=ch<=126,'graph6 alphabet');word=64*word+ch-63
    m=[[0]*24 for _ in range(24)];p=275
    for j in range(24):
        for i in range(j):m[i][j]=m[j][i]=(word>>p)&1;p-=1
    return word,m

def has_clique(m,color,k):
    n=len(m);adj=[sum(1<<j for j in range(n) if i!=j and m[i][j]==color) for i in range(n)]
    def go(mask,left):
        if left==0:return True
        while mask.bit_count()>=left:
            bit=mask&-mask;mask-=bit
            if go(mask&adj[bit.bit_length()-1],left-1):return True
        return False
    return go((1<<n)-1,k)

def check(catalog,certificate,retained):
    raw=Path(catalog).read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'catalog hash')
    lines=raw.splitlines();need(len(lines)==352366,'full catalog count')
    hist=collections.Counter();chosen=[]
    for line in lines:
        need(len(line)==47 and line[0]==87,'catalog shape')
        code=0
        for ch in line[1:]:need(63<=ch<=126,'catalog character');code=64*code+ch-63
        edges=code.bit_count();hist[edges]+=1
        if edges>=128:chosen.append(line)
    need(Path(retained).read_bytes()==b'\n'.join(chosen)+b'\n','complete retained list')
    cert=json.loads(Path(certificate).read_text());groups=collections.defaultdict(list)
    for line in chosen:
        _,m=decode(line);degrees=list(map(sum,m))
        need(not has_clique(m,1,4) and not has_clique(m,0,5),'retained Ramsey membership')
        for u in range(24):
            c=[v for v in range(24) if m[u][v]]
            ds=[sum(m[v][w] for w in c) for v in c]
            need(all(not(m[x][y] and m[x][z] and m[y][z]) for x,y,z in itertools.combinations(c,3)),'common graph triangle')
            p=sum(degrees[v] for v in c);q=0
            for v,w in itertools.combinations(c,2):
                if m[v][w]:
                    # Edge-by-edge score, independent of the producer's vertex-weight formula.
                    q+=degrees[v]+degrees[w]-sum(m[v][z]*m[w][z] for z in range(24))
            groups[(len(c),tuple(sorted(ds)))].append((p,q))
    expected=[];fail=[0,0]
    for (c,ds),rows in sorted(groups.items()):
        need(sum(ds)%2==0,'handshake');e=sum(ds)//2
        first=c*(29-c)+2*e;second=sum(d*d for d in ds)+(40-c)*e
        profiles=sorted(set(rows));counts=[0,0]
        for i,x in enumerate(profiles):
            for y in profiles[i:]:
                if x[0]+y[0]<first:counts[0]+=1
                else:need(x[1]+y[1]<second,'surviving profile pair');counts[1]+=1
        expected.append({'common_order':c,'common_degree_sequence':list(ds),'root_count':len(rows),'profiles':[list(x) for x in profiles],'degree_budget':first,'edge_budget':second,'rejected_by_first_then_second':counts})
        for i in (0,1):fail[i]+=counts[i]
    regenerated={'schema':1,'status':'COMPLETE_REGULAR18_AND24_GOOD43_EXCLUSION','catalog_sha256':PIN,'catalog_count':len(lines),'edge_histogram':{str(k):v for k,v in sorted(hist.items())},'retained_count':len(chosen),'root_count':sum(map(len,groups.values())),'bucket_count':len(groups),'distinct_bucket_profiles':sum(len(b['profiles']) for b in expected),'profile_pair_count':sum(fail),'rejected_by_first_then_second':fail,'buckets':expected}
    need(cert==regenerated,'certificate entry mismatch')
    return {'status':'VERIFIED_COMPLETE_REGULAR18_AND24_EXCLUSION','catalog_records':len(lines),'checked_retained_ramsey_graphs':len(chosen),'rooted_graphs':sum(map(len,groups.values())),'degree_sequence_buckets':len(groups),'bucket_profiles':regenerated['distinct_bucket_profiles'],'profile_pairs':sum(fail),'rejected_by_first_then_second':fail,'whole_h3887_tasks_decided':0,'regular_degree_strata_excluded':[18,24]}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--catalog',required=True);p.add_argument('--certificate',required=True);p.add_argument('--retained',required=True);a=p.parse_args()
    print(json.dumps(check(a.catalog,a.certificate,a.retained),indent=2))
