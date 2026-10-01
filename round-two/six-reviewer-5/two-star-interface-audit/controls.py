"""Semantic controls and entrywise cross-check of mask pruning.

The older independent mapper uses explicit source triples and dictionary
owners. Two additional carriers are expanded with no pruning at all and
compared with direct checks of every actual pair of complete words.
"""
import copy
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import time
import audit
import slow_mapper

HERE=Path(__file__).resolve().parent

def unpruned(Q,P,f,s):
    _,u,y,v=f; _,su,sv,sx,*_=s
    source=sorted(tuple(sorted(w-{sx})) for w in P if sx in w)
    target=sorted(tuple(sorted(w-{y})) for w in Q if y in w)
    si=next(i for i,w in enumerate(source) if su in w)
    ti=next(i for i,w in enumerate(target) if u in w)
    rest=[w for i,w in enumerate(source) if i!=si]
    tails=[w for i,w in enumerate(target) if i!=ti]
    rs=sorted(set(range(17))-set().union(*map(set,source))-{sx,sv})
    rt=sorted(set(range(18))-set().union(*map(set,target))-{17,y,v})
    first=set(audit.mask(w|{17}) for w in Q)
    accepted=[];count=0;start=time.monotonic()
    for tiny in permutations(sorted(set(target[ti])-{u})):
        for order in permutations(range(3)):
            for a,b,c in product(range(6),repeat=3):
                phi={sx:17,su:u,sv:v}
                phi.update(zip(sorted(set(source[si])-{su}),tiny))
                for src,k,j in zip(rest,order,(a,b,c)):
                    phi.update(zip(src,list(permutations(tails[k]))[j]))
                for image in permutations(rt):
                    count+=1
                    if time.monotonic()-start>30: raise audit.Incomplete('unpruned control incomplete')
                    phi.update(zip(rs,image))
                    family=first|{(1<<y)|audit.mask(phi[p] for p in w) for w in P}
                    if len(family)==36 and all((a&b).bit_count()<=2 for a,b in combinations(family,2)):
                        accepted.append(tuple(phi[p] for p in range(17)))
    audit.need(count==15552,'unpruned full domain')
    return sorted(accepted),count

def main():
    start=time.monotonic()
    data=json.loads((HERE/'TWENTY_STARS.json').read_text())
    seeds=json.loads((HERE/'SEED_CERTIFICATES.json').read_text())
    stars,first,second=audit.domains(data)
    comparisons=[]
    selected=[(f,s) for f in first for s in (second[0],second[len(second)//2],second[-1])]
    f=(9,13,11,2);s=(11,6,0,13,11)
    audit.need(f in first and s in second,'positive carrier is actual raw domain')
    selected.append((f,s))
    for f0,s0 in selected:
        fast=audit.maps(stars[f0[0]],stars[s0[0]],f0,s0)
        slow=slow_mapper.compatible_maps(stars[f0[0]],stars[s0[0]],f0,s0)
        audit.need(sorted(phi for phi,_ in fast['solutions'])==sorted(slow['solutions']) and fast['full_maps']==slow['full_maps'] and fast['collision_maps']==slow['collision_maps'],'entrywise slow-triple comparison')
        comparisons.append([f0,s0,fast['full_maps'],len(fast['solutions'])])
    brute=[]
    for f0,s0 in [(f,s),(first[-1],second[-1])]:
        literals,count=unpruned(stars[f0[0]],stars[s0[0]],f0,s0)
        fast=audit.maps(stars[f0[0]],stars[s0[0]],f0,s0)
        audit.need(literals==sorted(phi for phi,_ in fast['solutions']),'unpruned literal pair comparison')
        brute.append({'full_maps':count,'solutions':len(literals)})
    # Unrelated affine label maps on the first and second stars.
    positive=audit.maps(stars[f[0]],stars[s[0]],f,s)
    relabels=[]
    for multiplier,offset in [(3,4),(5,9)]:
        a=[(multiplier*p+offset)%17 for p in range(17)]
        b=[(7*p+offset+2)%17 for p in range(17)]
        Q=tuple(frozenset(a[p] for p in w) for w in stars[f[0]])
        P=tuple(frozenset(b[p] for p in w) for w in stars[s[0]])
        ff=(f[0],a[f[1]],a[f[2]],a[f[3]])
        ss=(s[0],b[s[1]],b[s[2]],b[s[3]],b[s[4]])
        relabeled=audit.maps(Q,P,ff,ss)
        expected=[]
        for phi,_ in positive['solutions']:
            im=[-1]*17
            for p in range(17): im[b[p]]=17 if phi[p]==17 else a[phi[p]]
            expected.append(tuple(im))
        audit.need(sorted(expected)==sorted(phi for phi,_ in relabeled['solutions']),'arbitrary full-map relabeling')
        relabels.append(len(expected))
    damages=[]
    def reject(name,fn,exception=ValueError):
        try: fn()
        except exception: damages.append(name)
        else: raise ValueError('accepted semantic damage: '+name)
    reject('zero states',lambda:audit.maps(stars[f[0]],stars[s[0]],f,s,nodes=0),audit.Incomplete)
    reject('larger state guard',lambda:audit.maps(stars[f[0]],stars[s[0]],f,s,nodes=200001))
    reject('larger time guard',lambda:audit.maps(stars[f[0]],stars[s[0]],f,s,seconds=11))
    bad=copy.deepcopy(data);bad['stars'][0][0]=bad['stars'][0][1]
    reject('duplicated star block',lambda:audit.domains(bad))
    bad=copy.deepcopy(data);bad['stars'].pop()
    reject('omitted generic fixture',lambda:audit.domains(bad))
    bad=copy.deepcopy(seeds);bad['seeds'][0]['colors'].pop()
    reject('missing residual color',lambda:audit.seed_caps(bad))
    bad=copy.deepcopy(seeds);bad['seeds'][0]['colors']=[0]*bad['seeds'][0]['candidate_count']
    reject('compatible words share a color',lambda:audit.seed_caps(bad))
    bad=copy.deepcopy(seeds);bad['seeds'][0]['candidate_count']-=1
    reject('omitted residual candidate',lambda:audit.seed_caps(bad))
    bad=copy.deepcopy(seeds);bad['seeds'][0]['upper_bound']-=1
    reject('incorrect total bound',lambda:audit.seed_caps(bad))
    survivor=next(family for _,family in positive['solutions'] if not audit.triangles(f,family))
    bad=copy.deepcopy(data);bad['groups'][9]=[]
    reject('missing positive transport',lambda:audit.transport(f,survivor,stars,bad,seeds))
    # The sampler deliberately reports no proof-complete status.
    sample=audit.run(data,seeds,1)
    audit.need('exact' not in sample and 'status' not in sample,'partial run never claims theorem')
    boundary=json.loads((HERE/'TRIANGLE_BOUNDARY.json').read_text())
    family=boundary['family'];ff=tuple(boundary['first']);i,u,y,v=ff
    need=audit.need
    need(len(family)==len(set(family))==36 and all(type(w) is int and 0<w<(1<<18) and w.bit_count()==5 for w in family),'boundary word domain')
    need(all((a&b).bit_count()<=2 for a,b in combinations(family,2)),'boundary literal packing')
    pair=lambda p,q:sum(w>>p&1 and w>>q&1 for w in family)
    triple=lambda p,q,r:any(w>>p&1 and w>>q&1 and w>>r&1 for w in family)
    need(len({17,u,y,v})==4 and sum(w>>17&1 for w in family)==sum(w>>y&1 for w in family)==20,'boundary centers')
    need(pair(17,y)==4 and pair(17,v)==5 and not triple(17,v,y),'boundary hypothesis1')
    need(pair(17,u)==4 and all(pair(17,p) in (4,5) for p in range(18) if p not in (17,u)),'boundary hypothesis2 row')
    high={p for p in range(18) if p!=17 and pair(17,p)<5}
    need(all(triple(17,u,p) for p in high-{u}),'boundary isolated high u')
    need(pair(y,u)==pair(y,v)==5 and all(pair(y,p) in (4,5) for p in range(18) if p!=y),'boundary hypothesis3')
    ts=audit.triangles(ff,family)
    need(ts==boundary['triangles'] and ts,'boundary omitted hypothesis4 is false')
    result={'status':'PASS_SEMANTIC_CONTROLS','agent':'six-reviewer-5','role':'independent mathematical reviewer',
            'slow_comparison_products':len(comparisons),'slow_comparison_sha256':sha256(audit.encoded(comparisons)).hexdigest(),
            'unpruned_carriers':brute,'arbitrary_relabeling_positive_counts':relabels,'damage_rejections':damages,
            'triangle_boundary':{'words':36,'deficient_pair_count':4,'triangle_points':ts,'hypotheses1_2_3_verified':True},
            'seconds':time.monotonic()-start}
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
