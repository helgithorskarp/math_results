"""Deterministic full-registry physical tests and small definition-level controls."""
from itertools import combinations
from pathlib import Path
import argparse,hashlib,json,time
from inputs import need
from reference import Domain,literal_count
from contact_codec import Contacts,PhysicalCarrier
import verify_physical as independent

def small_controls():
    tested=assignments=0
    for n in range(4):
        for word in range(1<<(n*(n-1)//2)):
            got=Domain(n,word).count();expected=literal_count(n,word)
            need(got==expected,'literal cube count');tested+=1;assignments+=1<<(4*n)
    # Two disjoint red edges: both literal augmentation and mixed red triangles are exercised.
    for word in (33,47):
        d=Domain(4,word,True);need(d.count()==literal_count(4,word,True),'literal augmentation cube')
        tested+=1;assignments+=1<<16
    return dict(complete_small_cubes=tested,literal_assignments=assignments)

def run(cache,tables,out,limit=362,counts=None):
    out=Path(out);out.mkdir();start=time.monotonic();domains=Contacts(cache,tables,counts);cores=independent.cores(cache)
    contact_tests=physical_tests=five_tests=0;fixture_hash=hashlib.sha256();cases=[];bad_hash=hashlib.sha256()
    rejected=0
    with (out/'physical.jsonl').open('w') as stream:
        for c in range(limit):
            for joint in (False,True):
                size=domains.size(c,joint);prefix=domains._prefix(c,joint)
                indices={0,1,size//2,size-2,size-1}
                # Deterministic bucket boundaries test zero buckets and equality multiplicities.
                for i in range(0,len(prefix),1031):
                    if prefix[i]<size:indices.add(prefix[i])
                    if prefix[i]>0:indices.add(prefix[i]-1)
                for index in sorted(indices):
                    rows=domains.unrank(c,joint,index);need(domains.rank(c,joint,rows)==index,'contact rank round trip');contact_tests+=1
                for code in (-1,size,True):
                    try:domains.unrank(c,joint,code)
                    except ValueError:rejected+=1
                    else:raise ValueError('accepted contact out of range')
            for r in range(5,10):
                task=f'bo1-q9-r{r}-c{c:06d}';carrier=PhysicalCarrier(task,cache,domains)
                for index in (0,carrier.size//2,carrier.size-1):
                    g=carrier.unrank(index);need(carrier.rank(g)==index,'physical round trip')
                    item=dict(task=task,code=index,graph=g);receipt=independent.validate(item,cores)
                    encoded=json.dumps(item,sort_keys=True,separators=(',',':'))+'\n';stream.write(encoded);fixture_hash.update(encoded.encode())
                    bad_hash.update((json.dumps(receipt,sort_keys=True,separators=(',',':'))+'\n').encode())
                    physical_tests+=1;five_tests+=receipt['tested_local_five_sets']
                    if (c,r,index) in ((0,5,0),(181,7,carrier.size//2),(361,9,carrier.size-1)):cases.append(item)
            if c%40==39:print(json.dumps(dict(completed_cores=c+1,seconds=time.monotonic()-start)),flush=True)
    for i,item in enumerate(cases):(out/f'fixture{i}.json').write_text(json.dumps(item,indent=2,sort_keys=True)+'\n')
    result=dict(status='VERIFIED_COMPLETE_Q9_PHYSICAL_INTERFACE' if limit==362 else 'PARTIAL_PHYSICAL_CONTROL',
        core_count=limit,task_count=limit*5,contact_roundtrips=contact_tests,physical_roundtrips=physical_tests,
        literal_local_five_sets=five_tests,out_of_range_rejections=rejected,
        physical_sha256=fixture_hash.hexdigest(),bad_witnesses_sha256=bad_hash.hexdigest(),fixture_count=len(cases),
        target_found=False,new_task_decisions=0)
    (out/'PHYSICAL.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('tables');p.add_argument('out');p.add_argument('--limit',type=int,default=362);p.add_argument('--small',action='store_true');a=p.parse_args()
    print(json.dumps(small_controls() if a.small else run(a.cache,a.tables,a.out,a.limit),sort_keys=True))
