"""Exact tail carrier and sparse branch certificate.
six-code-1, researcher, 2026-10-01. No numerical solver is used.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json
import time

HERE = Path(__file__).resolve().parent
FIXTURE_SHA = 'c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7'


class Incomplete(RuntimeError):
    pass


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def bits(word):
    return tuple(x for x in range(18) if word >> x & 1)


def mask(points):
    return sum(1 << x for x in points)


def load():
    raw = (HERE / 'TWENTY_STARS.json').read_bytes()
    require(sha256(raw).hexdigest() == FIXTURE_SHA, 'twenty-star manifest differs')
    d = json.loads(raw)
    require(d['agent'] == 'six-code-2' and len(d['stars']) == len(d['groups']) == 23,
            'wrong manifest shape or provenance')
    stars = tuple(tuple(sorted(mask(q) for q in Q)) for Q in d['stars'])
    groups = tuple(tuple(tuple(g) for g in G) for G in d['groups'])
    info = []
    for Q, group in zip(stars, groups):
        require(len(Q) == len(set(Q)) == 20 and all(q.bit_count() == 4 and q >> 17 == 0 for q in Q),
                'invalid star')
        pairs = [p for q in Q for p in combinations(bits(q), 2)]
        require(len(pairs) == len(set(pairs)) == 120, 'repeated pair')
        rho = tuple(sum(q >> x & 1 for q in Q) for x in range(17))
        H = tuple(x for x in range(17) if rho[x] < 5)
        require(max(rho) <= 5 and sum(5-r for r in rho) == 5, 'wrong replications')
        leave = set(combinations(range(17), 2)) - set(pairs)
        require(all(x in H or y in H for x,y in leave), 'low-low leave')
        core = tuple(p for p in sorted(leave) if set(p) <= set(H))
        require(len(core) == len(H)-1, 'high-core count')
        if group:
            require(len(group) == len(set(group)) and tuple(range(17)) in group, 'invalid group')
            for g in group:
                require(sorted(g) == list(range(17)) and
                        tuple(sorted(mask(g[x] for x in bits(q)) for q in Q)) == Q,
                        'map does not preserve all actual blocks')
            require(all(tuple(a[b[x]] for x in range(17)) in group for a in group for b in group),
                    'group is not closed')
        info.append(dict(rho=rho, H=H, leave=leave, core=core))
    return stars, groups, info


def quotient(values, group):
    remaining = set(values)
    output = []
    for key in sorted(values):
        if key not in remaining:
            continue
        orbit = {tuple(g[x] for x in key) for g in group}
        require(orbit and orbit <= remaining, 'orbit escape or overlap')
        remaining -= orbit
        output.append((key, len(orbit)))
    require(not remaining, 'incomplete quotient')
    return output


def tail_maps(Q, P, f, s, nodes=200000, seconds=10):
    require(type(nodes) is int and 0<=nodes<=200000 and 0<seconds<=10, 'invalid finite guard')
    start = time.monotonic()
    _,u,a,v,_ = f
    _,u2,v2,b,_ = s
    target = tuple(tuple(x for x in bits(q) if x != a) for q in Q if q >> a & 1)
    source = tuple(tuple(x for x in bits(q) if x != b) for q in P if q >> b & 1)
    require(len(source) == len(target) == 4 and
            all(len(set().union(*map(set,t))) == 12 for t in (source,target)), 'wrong common tails')
    ti = next(i for i,t in enumerate(target) if u in t)
    si = next(i for i,t in enumerate(source) if u2 in t)
    require(all(v not in t for t in target) and all(v2 not in t for t in source), 'v in common tails')
    result = []
    for order in permutations(i for i in range(4) if i != ti):
        assignment = dict(zip((i for i in range(4) if i != si), order))
        assignment[si] = ti
        choices = [tuple(p for p in permutations(target[assignment[i]])
                         if u2 not in source[i] or p[source[i].index(u2)] == u) for i in range(4)]
        require(sorted(map(len, choices)) == [2,6,6,6], 'tail choices')
        for moved in product(*choices):
            if len(result) >= nodes or time.monotonic()-start > seconds:
                raise Incomplete('INCOMPLETE tail guard; no exclusion')
            mapping = [-1]*17
            mapping[b], mapping[u2], mapping[v2] = 17,u,v
            for tail, image in zip(source,moved):
                for x,y in zip(tail,image):
                    mapping[x] = y
            require(sum(x >= 0 for x in mapping) == len({x for x in mapping if x >= 0}) == 14,
                    'noninjective partial map')
            result.append(tuple(mapping))
    require(len(result) == len(set(result)) == 2592, 'incomplete carrier')
    return tuple(sorted(result))


def problem(Q, P, f, s):
    a,b = f[2],s[3]
    first = tuple(q | 1 << 17 for q in Q if not q >> a & 1)
    triples = tuple(sorted({mask(t) for q in P if not q >> b & 1 for t in combinations(bits(q),3)}))
    forbidden = {mask(t) for q in first for t in combinations(bits(q),3)}
    common = set(x for q in Q if q >> a & 1 for x in bits(q) if x != a)
    extra = tuple(sorted(set(range(18)) - common - {17,a}))
    require(len(extra) == 4 and f[3] in extra, 'wrong unmatched target set')
    return triples, forbidden, extra


def collision(mapping, triples, forbidden):
    for t in triples:
        p = bits(t)
        if all(mapping[x] >= 0 for x in p) and mask(mapping[x] for x in p) in forbidden:
            return t
    return None


def cases(stars, groups, info):
    first=[]; second={'M':[], 'S':[]}; raw={'M':[], 'S':[]}
    for fi,r in enumerate(info):
        G=groups[fi] or (tuple(range(17)),)
        for u in r['H']:
            if r['rho'][u] not in (3,4) or any(u in edge for edge in r['core']):continue
            if any(r['rho'][x]!=4 for x in r['H'] if x!=u):continue
            marks={(a,v) for a in r['H'] if a!=u for v in range(17)
                   if r['rho'][v]==5 and tuple(sorted((a,v))) in r['leave']}
            require(all(g[u]==u for g in G),'first hub moved')
            for (a,v),mass in quotient(marks,G):first.append((fi,u,a,v,mass))
        for kind in ('M','S'):
            marks=set()
            for u in r['H']:
                if kind=='M':
                    if r['rho'][u]!=4 or any(u in edge for edge in r['core']):continue
                else:
                    if sum(u in edge for edge in r['core'])!=1:continue
                    if any(r['rho'][x]!=4 for x in r['H'] if x!=u):continue
                for b in r['H']:
                    if b==u or r['rho'][b]!=4 or tuple(sorted((u,b))) in r['leave']:continue
                    for v in range(17):
                        if v in (u,b):continue
                        if kind=='M':
                            if r['rho'][v]!=3:continue
                            if any(r['rho'][x]!=4 for x in r['H'] if x!=v):continue
                        elif r['rho'][v]!=5:continue
                        if tuple(sorted((v,b))) not in r['leave']:continue
                        require(tuple(sorted((u,v))) not in r['leave'],'u-v must be covered')
                        marks.add((u,v,b))
            raw[kind].extend((fi,*mark) for mark in sorted(marks))
            for (u,v,b),mass in quotient(marks,G) if marks else []:
                second[kind].append((fi,u,v,b,mass))
    first.sort()
    require(first==[(9,13,11,2,6),(17,14,8,4,8)],'first mark coverage changed')
    require(second['M']==[(8,13,14,11,1),(8,13,14,12,1)],'M mark coverage changed')
    require(len(second['S'])==44 and len(raw['S'])==231 and sum(s[-1] for s in second['S'])==231,
            'S mark coverage changed')
    domain=[(kind,f,s) for kind in ('M','S') for f in first for s in second[kind]]
    require(len(domain)==92,'product coverage changed')
    return domain,dict(first=first,raw_second=raw,second_orbits=second)


def produce():
    stars,groups,info=load();domain,marks=cases(stars,groups,info)
    cert={'format':'TWO_UNSATURATED_TAIL_PAIRS_V1','cases':[]}
    records=[];stream=sha256()
    for kind,f,s in domain:
        started=time.monotonic();Q,P=stars[f[0]],stars[s[0]]
        triples,forbidden,extra=problem(Q,P,f,s)
        exceptions=[];direct=0
        for i,mapping in enumerate(tail_maps(Q,P,f,s)):
            if time.monotonic()-started>10:raise Incomplete('INCOMPLETE case guard; no exclusion')
            stream.update(encode([kind,f,s,mapping]))
            if collision(mapping,triples,forbidden) is not None:
                direct+=1;continue
            unknown=tuple(x for x in range(17) if mapping[x]<0)
            available=tuple(x for x in extra if x!=f[3])
            require(len(unknown)==len(available)==3,'three residual points required')
            proof=[]
            for image in permutations(available):
                full=list(mapping)
                for x,y in zip(unknown,image):full[x]=y
                witness=collision(full,triples,forbidden)
                require(witness is not None,'compatible pair; claimed lemma is not established')
                proof.append(witness)
            exceptions.append([i,proof])
        cert['cases'].append(dict(kind=kind,first=list(f),second=list(s),exceptions=exceptions))
        records.append(dict(kind=kind,first=list(f),second=list(s),partial_maps=2592,
                            direct=direct,exceptional=len(exceptions),full_branches=6*len(exceptions)))
    raw=encode(cert)
    result=dict(actual_agent='six-code-1',role='researcher',status='COMPLETE_EXACT_TWO_PAIR_CERTIFICATES',
                marks=marks,cases=records,partial_maps=92*2592,represented_full_maps=92*2592*6,
                partial_input_sha256=stream.hexdigest(),certificate_sha256=sha256(raw).hexdigest(),
                certificate_bytes=len(raw))
    return result,raw


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true')
    args=parser.parse_args();start=time.monotonic();result,raw=produce()
    if args.write:
        (HERE/'CERTIFICATE.json').write_bytes(raw)
        (HERE/'expected.json').write_bytes(encode(result))
    else:
        require((HERE/'CERTIFICATE.json').read_bytes()==raw,'certificate bytes changed')
        require(json.loads((HERE/'expected.json').read_text())==json.loads(encode(result)),'expected record changed')
    print(json.dumps({'status':result['status'],'cases':len(result['cases']),
        'partial_maps':result['partial_maps'],'represented_full_maps':result['represented_full_maps'],
        'exceptional_partials':sum(c['exceptional'] for c in result['cases']),
        'certificate_bytes':len(raw),'certificate_sha256':result['certificate_sha256'],
        'seconds':time.monotonic()-start},sort_keys=True))


if __name__=='__main__':main()
