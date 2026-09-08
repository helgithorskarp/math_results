"""Optional deterministic SAT certificate discovery, outside verification trust."""
import argparse
import itertools
import json
from pathlib import Path
from pysat.solvers import Solver
ROOT=Path(__file__).resolve().parent

def geometry(name):
    points = json.loads((ROOT / (name+'.json')).read_text())
    pairs = {1296: [], 432: [], 4752: []}
    for i,j in itertools.combinations(range(len(points)),2):
        a,b,c,d = [x-y for x,y in zip(points[i],points[j])]
        num = 3*a*a+11*b*b+c*c+33*d*d
        if a*b+c*d == 0 and num in pairs:
            pairs[num].append((i,j))
    small = set(pairs[432])
    triangles = [t for t in itertools.combinations(range(len(points)),3)
                 if all(e in small for e in itertools.combinations(t,2))]
    return points, pairs[1296], pairs[4752], triangles

def var(v,c): return 4*v+c+1

def query(n,edges,constraints,equal):
    cnf=[]
    for v in range(n):
        cnf.append([var(v,c) for c in range(4)])
        cnf.extend([[-var(v,c),-var(v,d)] for c,d in itertools.combinations(range(4),2)])
    for u,v in edges:
        cnf.extend([[-var(u,c),-var(v,c)] for c in range(4)])
    cnf.extend([[var(0,0)],[var(1,0 if equal else 1)]])
    for t in constraints:
        cnf.extend([[-var(v,c) for v in t] for c in range(4)])
    with Solver(name='cadical195',bootstrap_with=cnf) as solver:
        solver.conf_budget(100000)
        sat=solver.solve_limited()
        out={'sat':sat,'stats':solver.accum_stats()}
        if sat:
            model=set(solver.get_model())
            word=[next(c for c in range(4) if var(v,c) in model) for v in range(n)]
            if any(word[u]==word[v] for u,v in edges):raise ValueError('Invalid word')
            if any(len({word[v] for v in t})==1 for t in constraints):raise ValueError('Invalid constraints')
            out['word']=''.join(map(str,word))
        return out

def produce():
    certificate={}
    for name in ('g40','g49'):
        pts,edges,longs,triangles=geometry(name)
        cons=triangles if name=='g49' else longs
        rows=[query(len(pts),edges,cons[:i]+cons[i+1:],name=='g49') for i in range(len(cons))]
        if any(r['sat'] is None for r in rows):raise RuntimeError('A capped query was unresolved')
        essential=[i for i,r in enumerate(rows) if r['sat']]
        certificate[name]={'essential':essential,'essential_words':[rows[i]['word'] for i in essential]}
        if name=='g49':continue
        optional=[i for i in range(len(cons)) if i not in essential]
        cnf=[]
        for v in range(40):
            cnf.append([var(v,c) for c in range(4)])
            cnf.extend([[-var(v,c),-var(v,d)] for c,d in itertools.combinations(range(4),2)])
        for u,v in edges+[cons[i] for i in essential]:
            cnf.extend([[-var(u,c),-var(v,c)] for c in range(4)])
        cnf.extend([[var(0,0)],[var(1,1)]])
        for j,i in enumerate(optional):
            b=161+j;u,v=cons[i]
            for c in range(4):
                cnf.extend([[-b,-var(u,c),var(v,c)],[b,-var(u,c),-var(v,c)]])
        patterns={}
        with Solver(name='cadical195',bootstrap_with=cnf) as solver:
            while solver.solve():
                model=set(solver.get_model())
                mask=sum(1<<j for j in range(len(optional)) if 161+j in model)
                word=''.join(str(next(c for c in range(4) if var(v,c) in model)) for v in range(40))
                patterns[mask]=word
                solver.add_clause([-(161+j) if mask>>j&1 else 161+j for j in range(len(optional))])
        minima=sorted(m for m in patterns if not any(k!=m and k&m==k for k in patterns))
        covers=[m for m in range(1<<len(optional)) if all(m&p for p in minima)]
        cover_set=set(covers)
        minimal_covers=[m for m in covers if all(not(m>>j&1) or (m^(1<<j)) not in cover_set for j in range(len(optional)))]
        size=min(m.bit_count() for m in covers)
        packing=next(t for t in itertools.combinations(minima,size) if all(not(a&b) for a,b in itertools.combinations(t,2)))
        certificate[name].update({'optional':optional,'patterns':[{'mask':m,'word':patterns[m]} for m in minima],
                                  'minimal_covers':minimal_covers,'disjoint_obstructions':list(packing)})
    return certificate

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('output',type=Path,help='Destination outside the repository for the regenerated certificate')
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError(args.output)
    args.output.write_text(json.dumps(produce(),indent=2,sort_keys=True)+'\n')
