"""Separate point carrier, literal branch checks, and scalar enumeration.
six-code-1, researcher, 2026-10-01. Standard library, exact arithmetic.
"""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json
import resource
import time

HERE=Path(__file__).resolve().parent
FIXTURE_SHA='c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7'


class Incomplete(RuntimeError):
    pass


def check(ok,message):
    if not ok:raise ValueError(message)


def encode(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()


def vertices(word):
    check(type(word) is int and 0 <= word < 1<<18,'invalid point mask')
    return frozenset(x for x in range(18) if word & (1<<x))


def literal_star(raw):
    check(type(raw) is list and len(raw)==20,'invalid star length')
    for q in raw:
        check(type(q) is list and len(q)==4 and all(type(x) is int and 0<=x<17 for x in q)
              and q==sorted(set(q)),'invalid quadruple')
    Q=tuple(frozenset(q) for q in raw)
    check(len(set(Q))==20 and all(len(q&r)<=1 for q,r in combinations(Q,2)),'repeated star pair')
    rho=tuple(sum(x in q for q in Q) for x in range(17))
    check(max(rho)<=5 and sum(5-r for r in rho)==5,'star replication condition')
    H=frozenset(x for x,r in enumerate(rho) if r<5)
    owner={frozenset(p) for q in Q for p in combinations(q,2)}
    leave={frozenset(p) for p in combinations(range(17),2)}-owner
    check(all(p&H for p in leave),'low-low leave')
    core=frozenset(p for p in leave if p<=H)
    check(len(core)==len(H)-1,'high-core count')
    return Q,rho,H,leave,core


def literal_group(Q,raw):
    G=tuple(tuple(g) for g in raw)
    if not G:return G
    check(len(G)==len(set(G)) and tuple(range(17)) in G,'group identities/distinctness')
    for g in G:
        check(all(type(x) is int for x in g) and sorted(g)==list(range(17)),'invalid point map')
        check({frozenset(g[x] for x in q) for q in Q}==set(Q),'map changes an actual block')
    check(all(tuple(g[h[x]] for x in range(17)) in G for g in G for h in G),'group closure')
    return G


def quotient(values,G):
    used=set();result=[]
    for key in sorted(values):
        if key in used:continue
        orbit={tuple(g[x] for x in key) for g in G}
        check(orbit and orbit<=values and not orbit&used,'invalid action or overlap')
        used.update(orbit);result.append((*key,len(orbit)))
    check(used==values,'incomplete mark cover')
    return result


def literal_cases(data):
    first=[];second=[];stars=[]
    for fi,raw in enumerate(data['stars']):
        Q,rho,H,leave,core=literal_star(raw);stars.append(Q)
        G=literal_group(Q,data['groups'][fi])
        for u in sorted(H):
            if rho[u] in (3,4) and all(u not in p for p in core) and all(rho[y]==4 for y in H-{u}):
                check(all(g[u]==u for g in G),'isolated hub moved')
                V={(a,v) for a in H-{u} for v in range(17)
                   if rho[v]==5 and frozenset((a,v)) in leave}
                for a,v,mass in quotient(V,G):first.append((fi,u,a,v,mass))
        V=set()
        for u,v,b in permutations(sorted(H),3):
            if not all(rho[x]==4 for x in H-{u}):continue
            if sum(u in p for p in core)!=1:continue
            if frozenset((u,v)) in leave or frozenset((u,b)) in leave:continue
            if frozenset((v,b)) not in core:continue
            V.add((u,v,b))
        if V:
            for u,v,b,mass in quotient(V,G):second.append((fi,u,v,b,mass))
    first.sort();second.sort()
    check(first==[(9,13,11,2,6),(17,14,8,4,8)],'complete first mark list changed')
    check(len(second)==10 and sum(r[-1] for r in second)==18,'complete second mark list changed')
    return stars,[(f,s) for f in first for s in second]


def point_carrier(Q,P,f,s,nodes=200000,seconds=10):
    check(type(nodes) is int and 0<=nodes<=200000 and 0<seconds<=10,'invalid finite guard')
    _,u,a,v,_=f;_,u2,v2,b,_=s
    source=tuple(sorted((q-{b} for q in P if b in q),key=lambda q:tuple(sorted(q))))
    target=tuple(sorted((q-{a} for q in Q if a in q),key=lambda q:tuple(sorted(q))))
    check(len(source)==len(target)==4 and all(len(t)==3 for t in source+target),'common tail shape')
    check(all(len(set().union(*t))==12 for t in (source,target)),'tail disjointness')
    si=next(i for i,t in enumerate(source) if u2 in t);ti=next(i for i,t in enumerate(target) if u in t)
    check(all(v2 not in t for t in source) and all(v not in t for t in target),'v in common words')
    order=sorted(source[si]-{u2})
    for i,t in enumerate(source):
        if i!=si:order.extend(sorted(t))
    owner={x:i for i,t in enumerate(source) for x in t}
    current={b:17,u2:u,v2:v};used={17,u,v};block_map={si:ti};used_blocks={ti}
    result=[];count=0;start=time.monotonic()
    def visit(depth):
        nonlocal count
        count+=1
        if count>nodes or time.monotonic()-start>seconds:raise Incomplete('INCOMPLETE point guard')
        if depth==len(order):
            result.append(tuple(current.get(x,-1) for x in range(17)));return
        x=order[depth];i=owner[x]
        options=(block_map[i],) if i in block_map else tuple(j for j in range(4) if j not in used_blocks)
        for j in options:
            fresh=i not in block_map
            if fresh:block_map[i]=j;used_blocks.add(j)
            for y in sorted(target[j]-used):
                current[x]=y;used.add(y);visit(depth+1);used.remove(y);del current[x]
            if fresh:used_blocks.remove(j);del block_map[i]
    visit(0)
    check(len(result)==len(set(result))==2592,'point carrier incomplete or repeated')
    return tuple(sorted(result)),count


def partial_collision(mapping,first,second):
    for q in second:
        image={mapping[x] for x in q if mapping[x]>=0}
        if any(len(image&r)>=3 for r in first):return True
    return False


def witness_check(witness,mapping,first,second):
    t=vertices(witness)
    check(len(t)==3 and any(t<=q for q in second),'source witness triple missing')
    check(all(x<17 and mapping[x]>=0 for x in t),'unmapped witness point')
    image=frozenset(mapping[x] for x in t)
    check(len(image)==3 and any(image<=q for q in first),'image witness triple absent')


def scalar_inventory():
    coarse=[];final=[]
    for p,k,c,z in __import__('itertools').product(range(9),range(9),range(5),range(5)):
        if not 0<=c<=k<=p or c+z>4:continue
        if (6+k)*2>p*(p-1) or (5*p+k-21)*2>p*(p-1):continue
        R=4-z+c;Q=max(12-k,2*c);h=R-Q;a=16-p-z
        if h<0 or a<0 or 5*a-20+c>26+4*h:continue
        row=[p,k,c,z,h];coarse.append(row)
        if 12-k+2*c-z-2*(8-p)<=R:final.append(row)
    check(len(coarse)==29 and final==[[7,7,1,0,0],[8,8,0,0,0]],'scalar domain changed')
    # The first remaining case has nine good A points, each of degree>=3.
    check(3*(16-7)>26,'first degree contradiction fails')
    # In the second, T is empty and the A degree total is20 rather than>=24.
    check(5*(16-8)-20 < 3*(16-8),'second degree contradiction fails')
    return dict(coarse=coarse,after_new_charge=final)


def verify(data,stars,domain,expected,compare=False):
    check(type(data) is dict and set(data)=={'format','cases'} and data['format']=='ONE_U_CHARGE_V1',
          'wrong certificate format')
    check(type(data['cases']) is list and len(data['cases'])==len(domain),'missing/repeated cases')
    primary=None
    if compare:import primary
    records=[];stream=sha256();total_nodes=0
    for case,(f,s) in zip(data['cases'],domain):
        started=time.monotonic()
        check(type(case) is dict and set(case)=={'first','second','exceptions'} and
              case['first']==list(f) and case['second']==list(s),'wrong case marks/order')
        Q,P=stars[f[0]],stars[s[0]];a,b=f[2],s[3]
        first=tuple(q|{17} for q in Q if a not in q);second=tuple(q for q in P if b not in q)
        maps,nodes=point_carrier(Q,P,f,s);total_nodes+=nodes
        if compare:
            masks=lambda qs:tuple(sorted(sum(1<<x for x in q) for q in qs))
            check(maps==primary.tail_maps(masks(Q),masks(P),f,s),'actual point domains differ entrywise')
        ex=case['exceptions'];check(type(ex) is list,'invalid exception list')
        exceptions={}
        for item in ex:
            check(type(item) is list and len(item)==2,'invalid exception')
            i,proof=item
            check(type(i) is int and 0<=i<len(maps) and i not in exceptions and
                  type(proof) is list and len(proof)==6,'invalid exception index/full coverage')
            exceptions[i]=proof
        check(list(exceptions)==sorted(exceptions),'exception order')
        common=set().union(*(q-{a} for q in Q if a in q))
        available=tuple(sorted(set(range(18))-common-{17,a,f[3]}))
        check(len(available)==3,'residual target count')
        direct=0
        for i,mapping in enumerate(maps):
            if time.monotonic()-started>10:raise Incomplete('INCOMPLETE literal case guard')
            stream.update(encode([f,s,mapping]))
            if i not in exceptions:
                check(partial_collision(mapping,first,second),'unproved partial branch')
                direct+=1;continue
            check(not partial_collision(mapping,first,second),'redundant exception changes record')
            unknown=tuple(x for x in range(17) if mapping[x]<0)
            check(len(unknown)==3,'residual source count')
            for image,witness in zip(permutations(available),exceptions[i]):
                moved=list(mapping)
                for x,y in zip(unknown,image):moved[x]=y
                check(len(set(moved))==17 and -1 not in moved,'invalid completed map')
                witness_check(witness,moved,first,second)
        records.append(dict(first=list(f),second=list(s),partial_maps=len(maps),direct=direct,
                            exceptional=len(exceptions),full_branches=6*len(exceptions)))
    check(records==expected['cases'] and stream.hexdigest()==expected['partial_input_sha256'],
          'complete input stream/readout differs')
    check(scalar_inventory()==expected['inventories'],'scalar producers differ')
    return dict(cases=len(records),partial_maps=sum(r['partial_maps'] for r in records),
                direct=sum(r['direct'] for r in records),exceptional=sum(r['exceptional'] for r in records),
                checked_full_branches=sum(r['full_branches'] for r in records),point_dfs_nodes=total_nodes)


def controls(data,stars,domain,expected):
    rejected=[]
    def reject(name,callback,kind=ValueError):
        try:callback()
        except kind:rejected.append(name)
        else:raise ValueError('negative control accepted: '+name)
    bad=deepcopy(data);bad['cases'].pop();reject('missing-case',lambda:verify(bad,stars,domain,expected))
    bad=deepcopy(data);bad['cases'][1]=deepcopy(bad['cases'][0]);reject('repeated-case',lambda:verify(bad,stars,domain,expected))
    bad=deepcopy(data);bad['format']='BAD';reject('wrong-format',lambda:verify(bad,stars,domain,expected))
    bad=deepcopy(data);bad['cases'][0]['exceptions'].pop();reject('missing-exception',lambda:verify(bad,stars,domain,expected))
    bad=deepcopy(data);bad['cases'][0]['exceptions'][0][1].pop();reject('missing-full-branch',lambda:verify(bad,stars,domain,expected))
    bad=deepcopy(data);bad['cases'][0]['exceptions'][0][1][0]=0;reject('invalid-witness',lambda:verify(bad,stars,domain,expected))
    raw=json.loads((HERE/'TWENTY_STARS.json').read_text())['stars'][9];bad=deepcopy(raw);bad[-1]=bad[0]
    reject('duplicate-template-block',lambda:literal_star(bad))
    reject('false-positive-collision',lambda:witness_check(7,tuple(range(17)),(),(frozenset((0,1,2,3)),)))
    f,s=domain[0];reject('zero-point-guard',lambda:point_carrier(stars[f[0]],stars[s[0]],f,s,nodes=0),Incomplete)
    import primary
    Q,P=primary.load()[0][f[0]],primary.load()[0][s[0]]
    reject('zero-tail-guard',lambda:primary.tail_maps(Q,P,f,s,nodes=0),primary.Incomplete)
    # A genuine compatible35-word pair validates the literal intersection layer.
    fixture=json.loads((HERE/'positive_joint.json').read_text())['word_masks']
    words=tuple(vertices(w) for w in fixture)
    check(len(words)==len(set(words))==35 and all(len(w)==5 for w in words) and
          all(len(w&q)<=2 for w,q in combinations(words,2)),'positive packing fails')
    check([sum(x in w for w in words) for x in (0,17)]==[20,20] and
          sum({0,17}<=w for w in words)==5,'positive marked counts')
    baseline=(HERE/'acl69.txt').read_bytes()
    check(sha256(baseline).hexdigest()=='cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d','ACL69 hash')
    strings=baseline.decode().split();check(len(strings)==len(set(strings))==69,'ACL69 count')
    check(all(len(w)==18 and set(w)<={'0','1'} and w.count('1')==5 for w in strings),'ACL69 weights')
    distances=Counter(sum(x!=y for x,y in zip(a,b)) for a,b in combinations(strings,2))
    check(distances=={6:1264,8:637,10:445},'ACL69 distances')
    return dict(rejected=rejected,positive_joint_words=35,acl69_distance_counts={str(k):v for k,v in distances.items()})


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--compare-primary',action='store_true')
    p.add_argument('--out',type=Path);args=p.parse_args();start=time.monotonic()
    raw=(HERE/'TWENTY_STARS.json').read_bytes();check(sha256(raw).hexdigest()==FIXTURE_SHA,'manifest hash')
    fixtures=json.loads(raw);stars,domain=literal_cases(fixtures)
    expected=json.loads((HERE/'expected.json').read_text());raw=(HERE/'CERTIFICATE.json').read_bytes()
    check(len(raw)==expected['certificate_bytes'] and sha256(raw).hexdigest()==expected['certificate_sha256'],
          'certificate bytes differ')
    data=json.loads(raw);record=verify(data,stars,domain,expected,args.compare_primary)
    record.update(agent='six-code-1',role='researcher',status='COMPLETE_SEPARATE_LITERAL_CHECK',
                  controls=controls(data,stars,domain,expected),inventories=scalar_inventory(),
                  entrywise_carrier_comparison=args.compare_primary)
    if args.out:args.out.write_bytes(encode(record))
    print(json.dumps(dict(**{k:v for k,v in record.items() if k not in ('inventories',)},
                          seconds=time.monotonic()-start,peak_RSS_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)),flush=True)


if __name__=='__main__':main()
