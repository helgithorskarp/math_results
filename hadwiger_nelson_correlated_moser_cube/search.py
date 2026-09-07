"""Optional deterministic producer of the compact positive colouring certificate."""
import argparse
from itertools import combinations,product
import json
from pathlib import Path
from pysat.solvers import Cadical195
import algebra as A
import model as M


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    data=json.loads((args.work/'contacts.json').read_text())
    rows=json.loads((args.work/'factorizations.json').read_text())
    factors=sorted({tuple(map(tuple,f))for r in rows for f,e in r['factors']})
    lookup={f:i for i,f in enumerate(factors)}
    cases=[{'roots':A.real_roots(f),'edges':[],'equal':[]}for f in factors]
    for r in rows:
        name='contacts'if r['kind']=='unit'else'collision_norms'
        key='edges'if r['kind']=='unit'else'equal'
        for f,e in r['factors']:
            cases[lookup[tuple(map(tuple,f))]][key].extend(data[name][r['index']]['pairs'])
    infinity={'roots':1,'edges':[],'equal':[]}
    points=[tuple(a-b+c for a,b,c in zip(M.M[i],M.M[j],M.M[k]))for i,j,k in data['addresses']]
    for a,b in combinations(range(343),2):
        norm=M.norm(tuple(x-y for x,y in zip(points[a],points[b])))
        if norm==(1296,0):infinity['edges'].append([a,b])
        if norm==(0,0):infinity['equal'].append([a,b])
    cases.append(infinity)
    active=sorted((i for i,c in enumerate(cases)if c['roots']),
                  key=lambda i:(-len(cases[i]['equal']),-len(cases[i]['edges']),i))
    medges=[(i,j)for i,j in combinations(range(7),2)
            if M.norm(tuple(a-b for a,b in zip(M.M[i],M.M[j])))==(1296,0)]
    mw=next((0,1,2)+tail for tail in product(range(4),repeat=4)
            if all(((0,1,2)+tail)[a]!=((0,1,2)+tail)[b]for a,b in medges))
    words=[''.join(str(mw[i]^mw[j]^mw[k])for i,j,k in product(range(7),repeat=3))]
    assignment=[-1]*len(cases);generic=data['generic_edges'];calls=0;conflicts=[]
    def proper(c,w):
        return all(w[a]==w[b]for a,b in c['equal'])and all(w[a]!=w[b]for a,b in c['edges'])
    for i in active:
        c=cases[i];found=next((j for j,w in enumerate(words)if proper(c,w)),None)
        if found is not None:
            assignment[i]=found;continue
        parent=list(range(343))
        def root(v):
            while parent[v]!=v:
                parent[v]=parent[parent[v]];v=parent[v]
            return v
        for a,b in c['equal']:
            a,b=root(a),root(b)
            if a!=b:parent[max(a,b)]=min(a,b)
        mapping={v:j for j,v in enumerate(sorted({root(v)for v in range(343)}))}
        local=[mapping[root(v)]for v in range(343)];n=len(mapping)
        edges={tuple(sorted((local[a],local[b])))for a,b in generic+c['edges']}
        if any(a==b for a,b in edges):raise ValueError('collapsed unit edge')
        var=lambda v,k:4*v+k+1
        clauses=[]
        for v in range(n):
            clauses.append([var(v,k)for k in range(4)])
            clauses.extend([-var(v,k),-var(v,j)]for k in range(4)for j in range(k))
        clauses.extend([-var(a,k),-var(b,k)]for a,b in sorted(edges)for k in range(4))
        clauses.extend([[var(local[v],k)]for v,k in [(0,0),(49,1),(98,2)]])
        with Cadical195(bootstrap_with=clauses)as solver:
            solver.conf_budget(2000000);answer=solver.solve_limited();calls+=1
            conflicts.append(solver.accum_stats()['conflicts'])
            if answer is not True:
                raise RuntimeError(f'No positive certificate for case {i}: answer={answer!r}')
            positive={v for v in solver.get_model()if v>0}
            word=''.join(str(next(k for k in range(4)if var(local[v],k)in positive))for v in range(343))
        if not proper(c,word)or any(word[a]==word[b]for a,b in generic):
            raise ValueError('invalid positive model')
        words.append(word);assignment[i]=len(words)-1
    cert={'version':'correlated-moser-cube-v1','words':words,'assignment':assignment,
          'generic_word':0,'M_colour_word':list(mw)}
    args.output.write_text(json.dumps(cert,separators=(',',':'))+'\n')
    print(json.dumps({'positive_cases':len(active),'words':len(words),'SAT_calls':calls,
                      'largest_conflict_count':max(conflicts),'requested_conflict_budget':2000000}))


if __name__=='__main__':
    main()
