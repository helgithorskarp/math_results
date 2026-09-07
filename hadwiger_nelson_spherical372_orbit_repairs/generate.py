"""Discover compact colour words for the entire orbit-repair gate."""
import argparse
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def source():
    edges=[tuple(map(int,line.split())) for line in (HERE/'source.edges').read_text().splitlines()]
    generators=json.loads((HERE/'generators.json').read_text())
    return edges,generators


def edge_orbits(edges,generators):
    index={e:i for i,e in enumerate(edges)}
    seen=set();orbits=[]
    for start in range(len(edges)):
        if start in seen:
            continue
        orbit={start};queue=[start]
        for i in queue:
            a,b=edges[i]
            for g in generators:
                j=index[tuple(sorted((g[a],g[b])))]
                if j not in orbit:
                    orbit.add(j);queue.append(j)
        seen|=orbit
        orbits.append(sorted(orbit))
    return orbits


def wheel_list(edges,orbits):
    index={e:i for i,e in enumerate(edges)}
    eo={e:k for k,orbit in enumerate(orbits) for e in orbit}
    adj=[set() for _ in range(372)]
    for a,b in edges:
        adj[a].add(b);adj[b].add(a)
    wheels=[]
    for centre in range(372):
        # Enumerate 5-cycles directly, independently of component decomposition.
        for a in sorted(adj[centre]):
            def extend(path):
                v=path[-1]
                if len(path)==5:
                    if a in adj[v] and path[1]<path[-1]:
                        es=[index[tuple(sorted((centre,b)))] for b in path]
                        es += [index[tuple(sorted((path[i],path[(i+1)%5])))] for i in range(5)]
                        mask=sum(1<<k for k in {eo[e] for e in es})
                        wheels.append(dict(centre=centre,rim=path[:],mask=mask))
                    return
                for b in sorted(adj[v]&adj[centre]):
                    if b>a and b not in path:
                        extend(path+[b])
            extend([a])
    return wheels


def maximal_masks(n,forbidden):
    family={(1<<n)-1}
    for f in forbidden:
        candidates=set()
        for m in family:
            if m&f != f:
                candidates.add(m)
            else:
                bits=f
                while bits:
                    b=bits&-bits;bits-=b;candidates.add(m^b)
        family=[]
        for m in sorted(candidates,key=lambda m:(-m.bit_count(),m)):
            if not any(m&z==m for z in family):
                family.append(m)
    return sorted(family)


def generate(output):
    from pysat.solvers import Cadical195
    edges,gens=source();orbits=edge_orbits(edges,gens);wheels=wheel_list(edges,orbits)
    minimal=[]
    for m in sorted({w['mask'] for w in wheels},key=lambda m:(m.bit_count(),m)):
        if not any(m&z==z for z in minimal):
            minimal.append(m)
    witnesses=[next(w for w in wheels if w['mask']==m) for m in minimal]
    masks=maximal_masks(len(orbits),minimal);words=[];search=[]
    for num,mask in enumerate(masks):
        selected=[edges[e] for k,orbit in enumerate(orbits) if mask>>k&1 for e in orbit]
        clauses=[[4*v+c+1 for c in range(4)] for v in range(372)]
        clauses += [[-4*a-c-1,-4*b-c-1] for a,b in selected for c in range(4)]
        clauses.append([1])
        with Cadical195(bootstrap_with=clauses) as solver:
            solver.conf_budget(300000)
            status=solver.solve_limited()
            if status is not True:
                raise RuntimeError(f'Unresolved candidate {num}: {status}')
            model=set(solver.get_model())
            word=''.join(str(next(c for c in range(4) if 4*v+c+1 in model)) for v in range(372))
            if any(word[a]==word[b] for a,b in selected):
                raise ValueError('invalid decoded colouring')
            search.append(dict(mask=mask,edges=len(selected),conflicts=solver.accum_stats()['conflicts']))
        words.append(dict(mask=mask,word=word))
    certificate=dict(wheels=witnesses,colourings=words)
    output.mkdir(parents=True,exist_ok=True)
    (output/'certificate.json').write_text(json.dumps(certificate,sort_keys=True,indent=2)+'\n')
    (output/'search.json').write_text(json.dumps(search,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(orbits=len(orbits),wheels=len(wheels),minimal_masks=minimal,
                          maximal_supports=len(masks),max_conflicts=max(s['conflicts'] for s in search))))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=HERE/'out')
    generate(p.parse_args().out)
