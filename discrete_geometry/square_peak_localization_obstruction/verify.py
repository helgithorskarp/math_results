#!/usr/bin/env python3
"""Exact square enumeration in two coordinate systems; standard library only.

The rational elimination kernel is adapted from affine_branch_square_size/verify.py
in this repository (source commit2538cb79365caa81520e3fb7345dc7dc2a16330d).
No import from that directory, external data, floating point, or solver is used.
"""
from fractions import Fraction as F
from itertools import product, combinations, combinations_with_replacement
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json
import sys

# z=(t,y,a,b): P,Q lower and R,S upper, with S left of R.
BX=((1,0,0,0),(1,0,1,0),(1,0,1,-1),(1,0,0,-1))
BY=((0,1,0,0),(0,1,0,1),(0,1,1,1),(0,1,1,0))
# z=(cx,cy,vx,vy): c+v,c+Jv,c-v,c-Jv, no branch assumption.
CX=((1,0,1,0),(1,0,0,-1),(1,0,-1,0),(1,0,0,1))
CY=((0,1,0,1),(0,1,1,0),(0,1,0,-1),(0,1,-1,0))


def require(ok, message):
    if not ok:raise ValueError(message)

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def affine_solution(rows, rhs, n):
    a=[[F(x) for x in row]+[F(b)] for row,b in zip(rows,rhs)]
    piv=[];r=0
    for j in range(n):
        i=next((i for i in range(r,len(a)) if a[i][j]),None)
        if i is None:continue
        a[r],a[i]=a[i],a[r]
        q=a[r][j];a[r]=[x/q for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][j]:
                q=a[i][j];a[i]=[x-q*y for x,y in zip(a[i],a[r])]
        piv.append(j);r+=1
    if any(not any(row[:n]) and row[n] for row in a):return None
    free=[j for j in range(n) if j not in piv]
    p=[F(0)]*n
    for i,j in enumerate(piv):p[j]=a[i][n]
    basis=[]
    for j in free:
        v=[F(0)]*n;v[j]=1
        for i,k in enumerate(piv):v[k]=-a[i][j]
        basis.append(v)
    return p,basis

def vertices(rows,rhs,ineq):
    sol=affine_solution(rows,rhs,4)
    if sol is None:return [],None
    p,basis=sol;d=len(basis)
    # Each inequality is A*z <= b. Substitute z=p+sum(t_i*basis_i).
    sub=[([dot(a,v) for v in basis],b-dot(a,p)) for a,b in ineq]
    found=set()
    for active in combinations(range(len(sub)),d):
        s=affine_solution([sub[i][0] for i in active],[sub[i][1] for i in active],d)
        if s is None or s[1]:continue
        t=s[0]
        if all(dot(a,t)<=b for a,b in sub):
            found.add(tuple(p[j]+sum(t[i]*basis[i][j] for i in range(d)) for j in range(4)))
    return sorted(found),d


def square(z, X, Y):
    return tuple((dot(x,z),dot(y,z)) for x,y in zip(X,Y))


def squared_side(points):
    p,q=points[:2]
    return (p[0]-q[0])**2+(p[1]-q[1])**2


def canonical(points):return tuple(sorted(points))


def check_square(points, segments):
    e=[tuple(b[j]-a[j] for j in (0,1))
       for a,b in zip(points,points[1:]+points[:1])]
    q=dot(e[0],e[0])
    require(all(dot(v,v)==q for v in e), 'unequal square sides')
    require(all(dot(e[i],e[(i+1)%4])==0 for i in range(4)), 'nonorthogonal sides')
    for p,(a,b) in zip(points,segments):
        require((p[0]-a[0])*(b[1]-a[1])==(p[1]-a[1])*(b[0]-a[0]), 'off line')
        require(all(min(a[j],b[j])<=p[j]<=max(a[j],b[j]) for j in (0,1)), 'off segment')
    return q


def enumerate_assignments(edges, assignments, X, Y, extra=()):
    found=set();stats=Counter();parameters=[];trace=[]
    for assignment in assignments:
        rows=[];rhs=[];ineq=list(extra)
        segments=[edges[e] for e in assignment]
        for k,(u,v) in enumerate(segments):
            dx=v[0]-u[0];dy=v[1]-u[1]
            require(dx or dy, 'zero length polygon edge')
            rows.append([dy*x-dx*y for x,y in zip(X[k],Y[k])])
            rhs.append(dy*u[0]-dx*u[1])
            coord=X[k] if dx else Y[k];j=0 if dx else 1
            lo,hi=sorted((u[j],v[j]))
            ineq.extend(((coord,hi),(tuple(-x for x in coord),-lo)))
        verts,d=vertices(rows,rhs,ineq)
        stats['assignments']+=1
        if d is None:stats['inconsistent_lines']+=1
        else:stats['affine_dimension_'+str(d)]+=1
        if verts:
            stats['feasible_assignments']+=1
            if d:stats['singular_feasible_assignments']+=1
        positive=[]
        for z in verts:
            pts=square(z,X,Y);q=check_square(pts,segments)
            if q:
                found.add(canonical(pts));positive.append(z)
        if positive:
            if d:stats['positive_square_singular_assignments']+=1
            parameters.append({'edges':list(assignment),'z':[[str(x) for x in z] for z in positive]})
        trace.append([list(assignment),d,[[str(x) for x in z] for z in verts]])
    for key in ['inconsistent_lines','singular_feasible_assignments','positive_square_singular_assignments']:
        stats.setdefault(key,0)
    return found,dict(sorted(stats.items())),parameters,trace


def strings(squares):return [[[str(x),str(y)] for x,y in sq] for sq in sorted(squares)]


def run():
    path=Path(__file__).with_name('fixture.json');fixture=json.loads(path.read_text())
    xs=list(map(F,fixture['knots']));f=list(map(F,fixture['lower']));g=list(map(F,fixture['upper']))
    require(len(xs)==len(f)==len(g)==5 and all(a<b for a,b in zip(xs,xs[1:])), 'bad knots')
    require(f[0]==g[0] and f[-1]==g[-1] and all(a<b for a,b in zip(f[1:-1],g[1:-1])), 'not two ordered branches')
    slopes=[[ (h[i+1]-h[i])/(xs[i+1]-xs[i]) for i in range(4)] for h in (f,g)]
    require(max(abs(m) for row in slopes for m in row)==F(93,100), 'Lipschitz check')
    gap=[b-a for a,b in zip(f,g)]
    require(gap[3]==F(183,50) and all(h<gap[3] for i,h in enumerate(gap) if i!=3), 'unique peak')
    lower=list(zip(xs,f));upper=list(zip(xs,g))
    edges=list(zip(lower,lower[1:]))+list(zip(upper,upper[1:]))
    pairs=list(combinations_with_replacement(range(4),2))
    assignments=((i,j,4+l,4+k) for (i,j),(k,l) in product(pairs,repeat=2))
    # a>=0 and |b|<=a; these are non-strict solely to retain degenerate boundary cells.
    extra=[((0,0,-1,0),F(0)),((0,0,-1,1),F(0)),((0,0,-1,-1),F(0))]
    branch,bs,parameters,trace=enumerate_assignments(edges,assignments,BX,BY,extra)
    wanted={canonical(square(tuple(map(F,z)),BX,BY)) for z in fixture['parameters']}
    require(len(wanted)==3 and branch==wanted,'three-square list mismatch')
    require(bs['assignments']==100 and bs['positive_square_singular_assignments']==0,'branch completeness')
    full,fs,_,_=enumerate_assignments(edges,product(range(8),repeat=4),CX,CY)
    require(full==branch and fs['positive_square_singular_assignments']==0,'full orientation check')
    right=max(p[0] for sq in full for p in sq)
    require(right==F(82074,10439) and right<F(63,8),'empty vertical band')
    require(xs[3]-right==F(1438,10439),'peak separation')
    qmax=max(min((a[0]-b[0])**2+(a[1]-b[1])**2 for a,b in combinations(sq,2)) for sq in full)
    require(qmax==F(1434393360,108972721),'max squared side')
    # Full enumeration after a rational rigid motion tests coordinate/order invariance.
    def move(p):return (F(3,5)*p[0]-F(4,5)*p[1]+F(7,3),F(4,5)*p[0]+F(3,5)*p[1]-F(2,7))
    moved,ms,_,_=enumerate_assignments([(move(a),move(b)) for a,b in edges],product(range(8),repeat=4),CX,CY)
    require(moved=={canonical(tuple(move(p) for p in sq)) for sq in wanted},'rigid motion changed squares')
    require(ms['positive_square_singular_assignments']==0,'rigid motion completeness')
    # A rectangle has a continuum of squares, so a checker dropping singular systems fails.
    rect=[(F(0),F(0)),(F(2),F(0)),(F(2),F(1)),(F(0),F(1))]
    _,rs,_,_=enumerate_assignments(list(zip(rect,rect[1:]+rect[:1])),product(range(4),repeat=4),CX,CY)
    require(rs['positive_square_singular_assignments']>0,'singular positive control')
    return {'status':'pass','fixture_sha256':sha256(path.read_bytes()).hexdigest(),
            'lower_slopes':list(map(str,slopes[0])),'upper_slopes':list(map(str,slopes[1])),
            'peak_x':'8','max_gap':'183/50','max_square_x':str(right),'separation':'1438/10439',
            'max_side_squared':str(qmax),'nondegenerate_squares':strings(full),
            'branch_parameters':parameters,'branch_stats':bs,'full_stats':fs,
            'rigid_motion_stats':ms,'rectangle_control_stats':rs,
            'branch_trace_sha256':sha256(json.dumps(trace,separators=(',',':')).encode()).hexdigest()}


if __name__=='__main__':
    result=run()
    if '--emit' not in sys.argv[1:]:
        require(result==json.loads(Path(__file__).with_name('expected.json').read_text()), 'expected output mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))
