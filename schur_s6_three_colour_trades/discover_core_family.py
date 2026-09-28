"""Optional untrusted regeneration of the compact fixed-core certificate."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import random


def minimize(c,cases,trials):
    A={d:{v for v in range(1,537) if c[v]==d} for d in range(1,7)}
    supports={}
    for d in range(1,7):
        targets=set().union(*(set(r['vertices']) for r in cases if d not in r['palette']))
        for v in targets:supports['block',d,v]=set()
        for a in A[d]:
            if a%2==0 and a//2 in targets:supports['block',d,a//2].add((a,))
            for b in A[d]:
                if a<=b and a+b in targets:supports['block',d,a+b].add(tuple(sorted({a,b})))
                if a<b and b-a in targets:supports['block',d,b-a].add((a,b))
    for i,j in combinations(range(1,7),2):supports['pair',i,j]=set()
    for z in range(2,537):
        for x in range(1,z//2+1):
            y=z-x;labels=sorted({c[x],c[y],c[z]})
            if len(labels)==2:supports['pair',*labels].add(tuple(sorted({x,y,z})))
    rows=[];counts=[];incidence=[[] for _ in range(537)]
    for key,choices in sorted(supports.items()):
        if not choices:raise ValueError(('uncovered support target',key))
        ci=len(counts);counts.append(len(choices))
        for S in sorted(choices):
            j=len(rows);rows.append((ci,S))
            for v in S:incidence[v].append(j)
    best=None
    for seed in range(trials):
        rng=random.Random(44000+seed);order=list(range(1,537));rng.shuffle(order)
        if seed==0:order.sort(key=lambda v:len(incidence[v]))
        active=[True]*len(rows);remaining=counts.copy();B=set(order)
        for v in order:
            lost=[j for j in incidence[v] if active[j]]
            loss=Counter(rows[j][0] for j in lost)
            if any(remaining[ci]<=n for ci,n in loss.items()):continue
            B.remove(v)
            for j in lost:active[j]=False
            for ci,n in loss.items():remaining[ci]-=n
        if best is None or len(B)<len(best):best=B
    return {str(d):sorted(best&A[d]) for d in range(1,7)}


def independent_switches(c,cores,trials):
    fixed=set().union(*(set(A) for A in cores.values()))
    edges=[];incidence=[[] for _ in c]
    for z in range(2,537):
        for x in range(1,z//2+1):
            E=sorted({x,z-x,z});j=len(edges);edges.append(E)
            for v in E:incidence[v].append(j)
    def allowed(v,d,masks):
        bit=1<<(d-1)
        return not any(all(masks[w]&bit for w in edges[j] if w!=v) for j in incidence[v])
    initial=[0]+[1<<(d-1) for d in c[1:]]
    candidates=[(v,d) for v in range(1,537) if v not in fixed
                for d in range(1,7) if d!=c[v] and allowed(v,d,initial)]
    best={}
    for seed in range(trials):
        rng=random.Random(45000+seed);order=candidates.copy();rng.shuffle(order)
        masks=initial.copy();chosen={}
        for v,d in order:
            if v in chosen or not allowed(v,d,masks):continue
            chosen[v]=d;masks[v]|=1<<(d-1)
        if len(chosen)>len(best):best=chosen
    return [{'vertex':v,'old':c[v],'alternative':best[v]} for v in sorted(best)]


def generate(directory,trials=128):
    fixtures=(directory/'fixtures.json').read_bytes()
    kernels=(directory/'class_splitting.json').read_bytes()
    c=[0]+list(map(int,json.loads(fixtures)['baseline']['colours']))
    cases=[r for r in json.loads(kernels)['cases'] if r['input']=='baseline']
    cores=minimize(c,cases,trials)
    switches=independent_switches(c,cores,trials)
    partial=[0]*538
    for d,A in cores.items():
        for v in A:partial[v]=int(d)
    pairs={}
    for z in range(2,537):
        for x in range(1,z//2+1):
            y=z-x;labels={partial[x],partial[y],partial[z]}
            if 0 not in labels and len(labels)==2:pairs.setdefault(tuple(sorted(labels)),[x,y,z])
    if set(pairs)!=set(combinations(range(1,7),2)):raise RuntimeError('lost a nonmerge pair')
    return {'format':1,'fixtures_sha256':sha256(fixtures).hexdigest(),
            'kernel_certificate_sha256':sha256(kernels).hexdigest(),'cores':cores,
            'nonmerge':[{'palette':list(pair),'triple':pairs[pair]} for pair in sorted(pairs)],
            'product_switches':switches}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',required=True)
    p.add_argument('--trials',type=int,default=128)
    args=p.parse_args()
    if args.trials<1:raise ValueError('at least one trial is required')
    cert=generate(Path(__file__).resolve().parent,args.trials)
    raw=(json.dumps(cert,indent=2)+'\n').encode()
    Path(args.output).write_bytes(raw)
    print('UNVERIFIED regenerated certificate sha256='+sha256(raw).hexdigest())


if __name__=='__main__':main()
