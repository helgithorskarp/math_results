#!/usr/bin/env python3
"""Produce exact rooted overlap profiles from the pinned complete catalog."""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
CATALOG_SHA='83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0'

def produce(path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=CATALOG_SHA:raise ValueError('catalog SHA256')
    rows=raw.splitlines()
    if len(rows)!=352366:raise ValueError('catalog count')
    retained=[];groups=collections.defaultdict(list);hist=collections.Counter()
    for index,s in enumerate(rows):
        if len(s)!=47 or s[0]!=87 or any(c<63 or c>126 for c in s):raise ValueError('graph6')
        m=sum((c-63).bit_count() for c in s[1:]);hist[m]+=1
        if m<128:continue
        retained.append(s.decode('ascii'))
        a=[set() for _ in range(24)];k=0
        for j in range(1,24):
            for i in range(j):
                if (s[1+k//6]-63)>>(5-k%6)&1:a[i].add(j);a[j].add(i)
                k+=1
        for u in range(24):
            common=a[u];ds={w:len(a[w]&common) for w in common}
            p=sum(len(a[w]) for w in common)
            q=sum(ds[w]*len(a[w]) for w in common)-sum(len(a[w]&a[z]) for w,z in itertools.combinations(common,2) if z in a[w])
            key=(len(common),tuple(sorted(ds.values())))
            groups[key].append((p,q))
    buckets=[];rejected=[0,0]
    for (c,ds),profiles in sorted(groups.items()):
        e=sum(ds)//2;t1=c*(29-c)+2*e;t2=sum(x*x for x in ds)+(40-c)*e
        values=sorted(set(profiles));fails=[0,0]
        for x,y in itertools.combinations_with_replacement(values,2):
            if x[0]+y[0]<t1:fails[0]+=1
            elif x[1]+y[1]<t2:fails[1]+=1
            else:raise ValueError('Unexcluded overlap profile pair')
        for i in (0,1):rejected[i]+=fails[i]
        buckets.append({'common_order':c,'common_degree_sequence':list(ds),'root_count':len(profiles),'profiles':[list(x) for x in values],'degree_budget':t1,'edge_budget':t2,'rejected_by_first_then_second':fails})
    certificate={'schema':1,'status':'COMPLETE_REGULAR18_AND24_GOOD43_EXCLUSION','catalog_sha256':CATALOG_SHA,'catalog_count':len(rows),'edge_histogram':{str(k):v for k,v in sorted(hist.items())},'retained_count':len(retained),'root_count':sum(len(x) for x in groups.values()),'bucket_count':len(groups),'distinct_bucket_profiles':sum(len(b['profiles']) for b in buckets),'profile_pair_count':sum(rejected),'rejected_by_first_then_second':rejected,'buckets':buckets}
    return certificate,'\n'.join(retained)+'\n'

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--catalog',required=True);parser.add_argument('--output-dir',required=True);args=parser.parse_args()
    cert,retained=produce(args.catalog);out=Path(args.output_dir);out.mkdir(parents=True,exist_ok=True)
    (out/'CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n')
    (out/'RETAINED.g6').write_text(retained)
    print(json.dumps({k:v for k,v in cert.items() if k not in ('buckets','edge_histogram')},sort_keys=True))
