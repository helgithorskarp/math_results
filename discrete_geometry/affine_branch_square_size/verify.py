#!/usr/bin/env python3
"""Enumerate boundary-edge assignment polytopes exactly, including singular ones.

The all-function lower bound is proved in PROOF.md. This program independently
checks sharpness over every orientation for small rational polygon fixtures.
Python 3.11+, standard library only.
"""
from fractions import Fraction as F
from itertools import product, combinations
from collections import Counter
import json
from pathlib import Path
from hashlib import sha256
import sys

# Coordinates of c+v, c+Jv, c-v, c-Jv in z=(cx,cy,vx,vy).
X=((1,0,1,0),(1,0,0,-1),(1,0,-1,0),(1,0,0,1))
Y=((0,1,0,1),(0,1,1,0),(0,1,0,-1),(0,1,-1,0))

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

def square(z):return tuple((dot(x,z),dot(y,z)) for x,y in zip(X,Y))
def side2(z):return 2*(z[2]**2+z[3]**2)

def enumerate_polygon(points):
    points=[tuple(map(F,p)) for p in points]
    edges=list(zip(points,points[1:]+points[:1]))
    nonzero=set();stats=Counter();maxq=F(0)
    for assignment in product(range(len(edges)),repeat=4):
        rows=[];rhs=[];ineq=[]
        for k,e in enumerate(assignment):
            a,b=edges[e];dx=b[0]-a[0];dy=b[1]-a[1]
            assert dx or dy
            rows.append([dy*x-dx*y for x,y in zip(X[k],Y[k])])
            rhs.append(dy*a[0]-dx*a[1])
            coord=X[k] if dx else Y[k]
            j=0 if dx else 1
            lo,hi=sorted((a[j],b[j]))
            ineq.extend(((coord,hi),(tuple(-x for x in coord),-lo)))
        verts,d=vertices(rows,rhs,ineq)
        stats['assignments']+=1
        if d is None:stats['inconsistent_lines']+=1;continue
        stats['affine_dimension_'+str(d)]+=1
        if not verts:continue
        stats['feasible_assignments']+=1
        if d:stats['singular_feasible_assignments']+=1
        for z in verts:
            # Independent geometric checks from the decoded four points.
            pts=square(z)
            for p,e in zip(pts,assignment):
                a,b=edges[e]
                assert (p[0]-a[0])*(b[1]-a[1])==(p[1]-a[1])*(b[0]-a[0])
                assert all(min(a[j],b[j])<=p[j]<=max(a[j],b[j]) for j in (0,1))
            q=side2(z);maxq=max(maxq,q)
            if q:
                nonzero.add(tuple(sorted(pts)))
                if d:stats['positive_square_singular_assignments']+=1
    stats.setdefault('positive_square_singular_assignments',0)
    return {'stats':dict(sorted(stats.items())),'max_side_squared':str(maxq),
            'nonzero_vertex_squares':[[[str(x),str(y)] for x,y in sq] for sq in sorted(nonzero)]}

def run():
    fixture_path=Path(__file__).with_name('fixtures.json')
    fixtures=json.loads(fixture_path.read_text())
    results={}
    for name,case in fixtures.items():
        result=enumerate_polygon(case['polygon'])
        assert result['max_side_squared']==case['max_side_squared'],name
        if 'unique_square' in case:
            expected=sorted(tuple(map(F,p)) for p in case['unique_square'])
            actual=result['nonzero_vertex_squares']
            assert len(actual)==1 and sorted(tuple(map(F,p)) for p in actual[0])==expected,name
            # All positive-dimensional assignment polytopes contain only
            # zero-size squares. Thus the vertex list is the whole solution
            # set of nondegenerate squares, not only their convex extremes.
            assert result['stats']['positive_square_singular_assignments']==0,name
        if 'baseline_slope' in case:
            slope=F(case['baseline_slope'])
            wanted=F(case['required_baseline_square_squared'])
            found=False
            for square_points in result['nonzero_vertex_squares']:
                pts=[tuple(map(F,p)) for p in square_points]
                lengths={(a[0]-b[0])**2+(a[1]-b[1])**2 for a,b in combinations(pts,2)}
                edge_length=min(lengths)
                if edge_length!=wanted:continue
                found |= any(a[1]==slope*a[0] and b[1]==slope*b[0] and
                             (a[0]-b[0])**2+(a[1]-b[1])**2==edge_length
                             for a,b in combinations(pts,2))
            assert found,name
        if case.get('require_singular_positive'):
            assert result['stats']['positive_square_singular_assignments']>0,name
        results[name]=result
    # Coordinate robustness: an exact rotation and translation of the sharp
    # fixture has the same maximum, despite no longer using its special axes.
    poly=fixtures['sharp']['polygon']
    moved=[]
    for x,y in poly:
        x,y=F(x),F(y)
        moved.append((F(3,5)*x-F(4,5)*y+F(7,3),
                      F(4,5)*x+F(3,5)*y-F(2,7)))
    transformed=enumerate_polygon(moved)
    assert transformed['max_side_squared']=='4/9'
    assert len(transformed['nonzero_vertex_squares'])==1
    assert transformed['stats']['positive_square_singular_assignments']==0
    return {'fixture_sha256':sha256(fixture_path.read_bytes()).hexdigest(),
            'fixtures':results,'rigid_motion_control':transformed,
            'total_assignments':sum(x['stats']['assignments'] for x in results.values())+
                                transformed['stats']['assignments']}


if __name__=='__main__':
    result=run()
    if '--emit' not in sys.argv[1:]:
        expected=json.loads(Path(__file__).with_name('expected.json').read_text())
        assert result==expected
        print('PASS: exact edge-assignment checks match expected.json')
    print(json.dumps(result,indent=2,sort_keys=True))
