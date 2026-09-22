#!/usr/bin/env python3
"""Exact sharpness certificate and local-action controls; standard library only.

The affine/polytope kernel is reused from square_peak_localization_obstruction
(source 0304625ef7389aea66942690ed14d7befdf6b22b), itself adapted from
affine_branch_square_size (2538cb79365caa81520e3fb7345dc7dc2a16330d).
This file is self-contained. Finite checks do not verify the imported Floer
theorems or prove the universal lower bound. No assertions are test-critical.
"""
from fractions import Fraction as F
from itertools import product, combinations
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


def pl_value(points,x):
    require(points[0][0]<=x<=points[-1][0],'point outside PL interval')
    for (u,v),(w,z) in zip(points,points[1:]):
        if u<=x<=w:return v+(z-v)*(x-u)/(w-u)
    raise ValueError('no segment')


def pl_interval(points,lo,hi):
    require(lo<=hi and points[0][0]<=lo and hi<=points[-1][0],'invalid integral interval')
    return [(lo,pl_value(points,lo))]+[(x,y) for x,y in points if lo<x<hi]+[(hi,pl_value(points,hi))]


def integral(points):
    return sum((x1-x0)*(y0+y1)/2 for (x0,y0),(x1,y1) in zip(points,points[1:]))


def arc_lambda(points):
    return sum((x0*y1-y0*x1)/2 for (x0,y0),(x1,y1) in zip(points,points[1:]))


def validate_graph(points):
    require(len(points)>=2 and all(x<y for (x,_),(y,_) in zip(points,points[1:])), 'knots not increasing')
    require(all(abs(v-u)<=y-x for (x,u),(y,v) in zip(points,points[1:])), 'not 1-Lipschitz')


def envelopes(a,b):
    require(a>0 and abs(b)<=a,'invalid chord')
    return ([(F(0),F(0)),((a-b)/2,-(a-b)/2),(a,b)],
            [(F(0),F(0)),((a+b)/2,(a+b)/2),(a,b)])


def envelope_checks():
    cases=0;actions=0;lower_equal=0;upper_equal=0
    for a in [F(1,2),F(1),F(7,3)]:
        for b in [a*F(j,4) for j in range(-3,4)]:
            lo,hi=envelopes(a,b)
            validate_graph(lo);validate_graph(hi)
            trap=a*b/2;err=(a*a-b*b)/4
            require(integral(lo)==trap-err and integral(hi)==trap+err,'envelope integration')
            knots=sorted(set(x for x,_ in lo+hi))
            for w in [F(0),F(1,3),F(1,2),F(1)]:
                path=[(x,(1-w)*pl_value(lo,x)+w*pl_value(hi,x)) for x in knots]
                require(abs(integral(path)-trap)<=err,'chord bound');cases+=1
            # Shift two independently selected extremal arcs to square endpoints.
            for low,up in product([lo,hi],repeat=2):
                t=F(2,7);y=F(-3,5)
                f=[(t+x,y+z) for x,z in low]
                g=[(t-b+x,y+a+z) for x,z in up]
                val=integral(g)-integral(f)-(a*a-b*b)/2
                lam=arc_lambda(f)-arc_lambda(g)
                require(val==lam,'action convention')
                require(b*b<=val<=a*a,'local action bound')
                lower_equal+=val==b*b;upper_equal+=val==a*a;actions+=1
    # Independent grid enumeration of PL paths, not just mixtures of envelopes.
    grid=0
    for increments in product([-1,0,1],repeat=6):
        path=[(F(0),F(0))]
        for j,v in enumerate(increments):path.append((F(j+1,6),path[-1][1]+F(v,6)))
        b=path[-1][1];trap=b/2;err=(1-b*b)/4
        require(abs(integral(path)-trap)<=err,'grid path envelope');grid+=1
    return {'chord_cases':cases,'action_normalizations':actions,'lower_equality':lower_equal,
            'upper_equality':upper_equal,'independent_grid_paths':grid}


def analyze_polygon(edges):
    return enumerate_assignments(edges,product(range(len(edges)),repeat=4),CX,CY)


def q_of_canonical(sq):
    return min((a[0]-b[0])**2+(a[1]-b[1])**2 for a,b in combinations(sq,2))


def run():
    xs=list(map(F,['-3/4','-1/4','0','1/4','3/4']))
    hs=list(map(F,['0','1/4','1/2','1/4','0']))
    lower=list(zip(xs,[-x for x in hs]));upper=list(zip(xs,hs))
    validate_graph(lower);validate_graph(upper)
    require(max(2*h for h in hs)==1,'maximum gap')
    edges=list(zip(lower,lower[1:]))+list(zip(upper,upper[1:]))
    found,stats,_,trace=analyze_polygon(edges)
    wanted=canonical(tuple(product([F(-1,4),F(1,4)],repeat=2)))
    require(found=={wanted},'extremizer square vertices')
    require(max(map(q_of_canonical,found))==F(1,4),'sharp maximum')
    positive_singletons=0;zero_families=0
    for assignment,dim,vs in trace:
        if any(F(v[2]) or F(v[3]) for v in vs):
            require(len(vs)==1,'unaccounted nonzero square family')
            positive_singletons+=1
        elif len(vs)>1:zero_families+=1
    require(stats['assignments']==4096 and stats['positive_square_singular_assignments']==4,'singular audit')
    # The same exact enumeration after a rational Euclidean isometry.
    def move(p):return (F(3,5)*p[0]-F(4,5)*p[1]+F(7,3),F(4,5)*p[0]+F(3,5)*p[1]-F(2,7))
    moved,ms,_,_=analyze_polygon([(move(a),move(b)) for a,b in edges])
    require(moved=={canonical(tuple(move(v) for v in wanted))},'rigid-motion invariance')
    require(max(map(q_of_canonical,moved))==F(1,4),'rigid side')
    # A positive singular continuum must NOT be discarded by the enumerator.
    rect=[(F(0),F(0)),(F(2),F(0)),(F(2),F(1)),(F(0),F(1))]
    rf,rs,_,_=analyze_polygon(list(zip(rect,rect[1:]+rect[:1])))
    require(rs['positive_square_singular_assignments']>0,'missing rectangle continuum')
    require(max(map(q_of_canonical,rf))==1,'rectangle maximum')
    # Nonzero b and nonaffine branches: values from the earlier localization witness.
    xx=list(map(F,[0,4,6,8,10]))
    ff=list(zip(xx,map(F,['0','-9/5','-18/5','-93/50','0'])))
    gg=list(zip(xx,map(F,['0','9/5','0','9/5','0'])))
    actions=[]
    for t,y,a,b in [tuple(map(F,z)) for z in [
        ['1016/497','-2286/2485','1206/497','-648/497'],
        ['104/49','-234/245','18/7','-72/49'],
        ['44202/10439','-104958/52195','37872/10439','324/10439']]]:
        fl=pl_interval(ff,t,t+a);gu=pl_interval(gg,t-b,t+a-b)
        require(fl[0][1]==y and fl[-1][1]==y+b and gu[0][1]==y+a and gu[-1][1]==y+a+b,'square endpoints')
        val=integral(gu)-integral(fl)-(a*a-b*b)/2
        require(val==arc_lambda(fl)-arc_lambda(gu) and b*b<=val<=a*a,'fixture action')
        actions.append(str(val))
    # Diagonal-winding crossing: one common abscissa, strictly positive height.
    winding=0
    for a in [F(1),F(7,3)]:
        for b in [a*F(j,5) for j in range(-4,5)]:
            u=(a-b)/(2*a)
            require(0<u<1 and a-b-2*a*u==0,'capping crossing')
            require(a-b>0 and a+b>0,'quadrant endpoints');winding+=1
    rejected=0
    for bad in [[(F(0),F(0)),(F(0),F(1))],[(F(0),F(0)),(F(1),F(2))]]:
        try:validate_graph(bad)
        except ValueError:rejected+=1
        else:raise ValueError('bad graph accepted')
    for a,b in [(F(0),F(0)),(F(1),F(2))]:
        try:envelopes(a,b)
        except ValueError:rejected+=1
        else:raise ValueError('bad chord accepted')
    return {'status':'pass','universal_proof_checked_by_code':False,
            'max_gap':'1','max_side_squared':'1/4','square':strings(found),
            'sharpness_stats':stats,'positive_singleton_assignments':positive_singletons,
            'degenerate_multivertex_assignments':zero_families,'rigid_motion_stats':ms,
            'rectangle_control_stats':rs,'envelope_checks':envelope_checks(),
            'prior_witness_actions':actions,'winding_endpoint_controls':winding,
            'invalid_inputs_rejected':rejected,
            'sharpness_trace_sha256':sha256(json.dumps(trace,separators=(',',':')).encode()).hexdigest()}


if __name__=='__main__':
    require(sys.argv[1:] in [[],['--emit'],['--check']],'usage: verify.py [--emit|--check]')
    result=run()
    if '--emit' not in sys.argv:
        require(result==json.loads(Path(__file__).with_name('EXPECTED.json').read_text()),'expected evidence differs')
    print(json.dumps(result,indent=2,sort_keys=True))
