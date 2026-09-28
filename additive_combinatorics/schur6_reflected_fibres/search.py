"""Exact search for the reflected-fibre construction described in README.md.

The generic triple projection is copied from the audited local literal model.
UNKNOWN is not an exclusion. Every positive full word is checked by verify.py.
"""
import argparse
import itertools
import json
import math
import time
from pathlib import Path
from pysat.solvers import Solver
from verify import check

def triple_clauses(m,xyz):
    out=[]
    for c in range(m['k']):
        required={}
        for x in xyz:
            j,pi=m['point'][x];state=pi[c]
            if j in required and required[j]!=state:break
            required[j]=state
        else:out.append(tuple(sorted(-m['k']*j-t-1 for j,t in required.items())))
    return out


def clauses_for(m,require_moved=False):
    k,n=m['k'],m['n'];clauses=set()
    for j in range(len(m['cells'])):
        clauses.add(tuple(k*j+c+1 for c in range(k)))
        for c,d in itertools.combinations(range(k),2):
            clauses.add(tuple(sorted((-k*j-c-1,-k*j-d-1))))
    for b in range(1,len(m['half'])+1):
        clauses.add((k*m['index'][0,b]+m['half'][b-1]+1,))
    literal_pairs=0
    for x in range(1,n):
        for y in range(x,n):
            z=(x+y)%n
            if not z:continue
            literal_pairs+=1
            clauses.update(triple_clauses(m,(x,y,z)))
    if require_moved:
        moved=[k*j+c+1 for j,(a,b) in enumerate(m['cells']) if a and b
               for c in range(k) if m['permutations'][b][c]!=c]
        clauses.add(tuple(moved))
    return [list(c) for c in sorted(clauses)],literal_pairs


def decode(m,states):
    # point maps actual colours to state labels. Inverting also permits the
    # non-involutive affine maps used by the separate common-phase model.
    return [pi.index(states[j]) for j,pi in m['point'][1:]]


def axis_edges(a):
    edges=set()
    for x in range(1,a):
        for y in range(x,a):
            z=(x+y)%a
            if z:
                edges.add(tuple(sorted({min(s,a-s) for s in (x,y,z)})))
    return tuple(sorted(edges))


def geometry(a):
    if a<3 or a%2!=1 or math.gcd(a,5)!=1:raise ValueError('bad CRT factors')
    cells=[(0,1),(0,2)]+[(u,0) for u in range(1,(a+1)//2)]+[(u,1) for u in range(1,a)]
    index={cell:j for j,cell in enumerate(cells)};point=[None]
    for x in range(1,5*a):
        aa,b=x%a,x%5;v=min(b,5-b)
        if not aa:j=index[0,v];pi=list(range(6))
        elif not b:j=index[min(aa,a-aa),0];pi=list(range(6))
        else:
            j=index[aa if b in (1,2) else -aa%a,1]
            pi=[1,0,2,3,4,5] if v==2 else list(range(6))
        point.append((j,pi))
    return dict(a=a,p=5,n=5*a,k=6,half=[0,1],cells=cells,index=index,point=point)


def build(a,normalize=False,require_asymmetric=False,mergeable=False,fixed_axis=None,hole_label=0):
    m=geometry(a);cnf,pairs=clauses_for(m);h=(a-1)//2
    for aa in range(1,a):cnf.append([-6*m['index'][aa,1]-2])
    ordered=[m['index'][aa,b] for u in range(1,h+1) for aa,b in ((u,1),(a-u,1),(u,0))]
    if fixed_axis is None:
        for t,j in enumerate(ordered):
            for c in (3,4,5):cnf.append([-6*j-c-1]+[6*i+c for i in ordered[:t]])
    else:
        if normalize:raise ValueError('do not normalize a fixed labelled axis')
        row=[-1]+fixed_axis['word']
        if fixed_axis['modulus']!=a or len(row)!=a or hole_label not in range(5):
            raise ValueError('incompatible fixed axis')
        if any(type(c) is not int or c not in range(5) for c in row[1:]):
            raise ValueError('bad fixed axis labels')
        if any(row[x]!=row[a-x] for x in range(1,a)):
            raise ValueError('fixed axis is not symmetric')
        if any((x+y)%a and row[x]==row[y]==row[(x+y)%a]
               for x in range(1,a) for y in range(x,a)):
            raise ValueError('fixed axis is not sum-free')
        palette={hole_label:0}
        palette.update({c:j+2 for j,c in enumerate(c for c in range(5) if c!=hole_label)})
        for u in range(1,h+1):cnf.append([6*m['index'][u,0]+palette[row[u]]+1])
    if normalize:
        if a<=45 or any(a%d==0 for d in range(2,math.isqrt(a)+1)):
            raise ValueError('normalization uses prime a>45 and S(4)=44')
        # E needs at least five labels, hence uses special colour 0 or 1.
        # Swap only E0/E1 (identical compatibility constraints), then scale A.
        cnf.append([6*m['index'][1,0]+1])
    top=6*len(m['cells'])
    if require_asymmetric:
        selectors=[]
        for u in range(1,h+1):
            top+=1;selectors.append(top)
            for c in (0,2,3,4,5):
                cnf.append([-top,-6*m['index'][u,1]-c-1,-6*m['index'][a-u,1]-c-1])
        cnf.append(selectors)
    if mergeable:
        for edge in axis_edges(a):
            for labels in itertools.product((0,1),repeat=len(edge)):
                cnf.append([-6*m['index'][u,0]-c-1 for u,c in zip(edge,labels)])
    return m,cnf,pairs


def run(a,budget,output,normalize=False,require_asymmetric=False,mergeable=False,fixed_axis=None,hole_label=0):
    start=time.monotonic();m,cnf,pairs=build(a,normalize,require_asymmetric,mergeable,fixed_axis,hole_label)
    report=dict(axis_factor=a,modulus=5*a,colours=6,family='reflected shared fibres',
                normalize_axis=normalize,require_asymmetric=require_asymmetric,
                require_mergeable_axis=mergeable,states=len(m['cells']),clauses=len(cnf),
                literal_pairs=pairs,solver='cadical195',budget=budget,
                setup_seconds=time.monotonic()-start)
    if fixed_axis is not None:
        report.update(fixed_axis_word=fixed_axis['word'],hole_label=hole_label)
    with Solver(name='cadical195',bootstrap_with=cnf) as solver:
        solver.conf_budget(budget);ans=solver.solve_limited()
        report.update(status={True:'SAT',False:'UNSAT',None:'UNKNOWN'}[ans],stats=solver.accum_stats())
        if ans:
            truth=set(solver.get_model())
            states=[next(c for c in range(6) if 6*j+c+1 in truth) for j in range(len(m['cells']))]
            report['word']=decode(m,states);report['check']=check(report)
            if mergeable and not report['check']['special_axis_mergeable']:
                raise RuntimeError('mergeability constraint mismatch')
    report['seconds']=time.monotonic()-start
    Path(output).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('word','fixed_axis_word')}),flush=True)
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--axis-factor',type=int,default=109)
    p.add_argument('--budget',type=int,default=100000);p.add_argument('--output',required=True)
    p.add_argument('--normalize-axis',action='store_true');p.add_argument('--require-asymmetric',action='store_true')
    p.add_argument('--mergeable-axis',action='store_true');p.add_argument('--fixed-axis')
    p.add_argument('--hole-label',type=int,choices=range(5),default=0);args=p.parse_args()
    run(args.axis_factor,args.budget,args.output,args.normalize_axis,args.require_asymmetric,args.mergeable_axis,
        json.loads(Path(args.fixed_axis).read_text()) if args.fixed_axis else None,args.hole_label)
