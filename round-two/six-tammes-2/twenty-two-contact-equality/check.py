"""Reconstruct the boundary core and check its labeled incumbent Gram matrix.

Python standard library only. This is separate arithmetic from the QQ(t)
SymPy derivation, by the same author; it is not independent researcher review.
The geometric deduction that z=z0 is external and stated in PROOF.md.
"""
import argparse
import hashlib
import json
import os
from itertools import combinations, permutations
from pathlib import Path
import signal
import time
for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
             'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
import arithmetic as a
from arithmetic import E, T, Q, ZERO, ONE, require

G22 = {(0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),
       (2,4),(2,8),(2,10),(2,13),(4,8),(5,7),(5,9),(5,11),
       (6,11),(7,12),(8,13),(9,10),(9,11),(10,12)}
DELETED = {(6,8),(9,13)}
G24 = G22 | DELETED
STEPS = ((6,0,11,5),(7,0,5,11),(9,5,11,0),(8,2,4,1),
         (10,1,2,4),(12,1,10,2),(13,2,8,4))

def dot(x, y):
    return (1-T)*sum(v*w for v,w in zip(x,y)) + T*sum(x)*sum(y)

def cross(x, y):
    return (x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2],
            x[0]*y[1]-x[1]*y[0])

def hinverse(x):
    return tuple(v/(1-T)-T*sum(x)/((1-T)*(1+2*T)) for v in x)

def hmap(x):
    return tuple((1-T)*v+T*sum(x) for v in x)

def determinant(matrix):
    out = ZERO
    for p in permutations(range(3)):
        term = ONE
        for i in range(3): term = term*matrix[i][p[i]]
        inversions = sum(p[i] > p[j] for i in range(3) for j in range(i+1,3))
        out = out + (-1 if inversions % 2 else 1)*term
    return out

def intersection(points, labels):
    matrix = [hmap(points[i]) for i in labels]
    det = determinant(matrix)
    require(det.sign() != 0, 'independent contact planes')
    return tuple(determinant([[T if j==k else matrix[i][j]
                              for j in range(3)] for i in range(3)])/det
                 for k in range(3))

def boundary_core(radical_orientation=-1, boundary_shift=0, u_orientation=1):
    r = 2*T/(1+T)
    D = (1-T)**2*(1+2*T)
    A = T**3-3*T**2+T+1
    z = 2*T**2/A + E(boundary_shift)
    C = 1+D*z*z
    k = T*(9*T*T-2*T-3)/(1+T)**2
    gamma = k/(1+k)
    mu = (T-1)*(T+1)*(2*T+1)*(3*T-1)/(9*T**3-T*T-T+1)
    require((1-T).sign()>0 and (1+2*T).sign()>0, 'positive definite H')
    require((z-E('9/10')).sign()>0 and (E('7/5')-z).sign()>0,
            'boundary parameter in the checked closed strip')
    points = {label:tuple(ONE if i==j else ZERO for j in range(3))
              for i,label in enumerate((1,2,4))}
    for n,i,j,o in STEPS[3:]:
        points[n] = tuple(r*(x+y)-v for x,y,v in zip(points[i],points[j],points[o]))
    normal = hinverse(cross(points[12],points[1]))
    W = tuple(T*x+(D*z*z-1)/C*(y-T*x)+2*D*z/C*n
              for x,y,n in zip(points[12],points[1],normal))
    s = dot(W,points[10])
    delta = 1-s*s
    g = delta-k*k-T*T+2*s*k*T
    p4 = 8*T**4-3*T**3-T*T+3*T+1
    p5 = 4*T**5-19*T**4-2*T**3+4*T*T-2*T-1
    root = -(T-1)**2*(2*T+1)*(3*T+1)*p5/((T+1)**2*p4)
    require(delta.sign()>0 and g.sign()>0, 'regular boundary reconstruction')
    require(root.sign()>0 and root*root==D*g, 'selected positive radical')
    normal = hinverse(cross(W,points[10]))
    V = tuple(((k-s*T)*x+(T-s*k)*y+radical_orientation*root*n)/delta
              for x,y,n in zip(W,points[10],normal))
    normal = hinverse(cross(W,V))
    U = tuple(gamma*(x+y)+u_orientation*mu*n for x,y,n in zip(W,V,normal))
    points.update({6:U,7:W,9:V})
    den = (2*r-1)*(r+1)
    for label, weights in ((0,(r,r,1-r)),(5,(1-r,r,r)),(11,(r,1-r,r))):
        points[label] = tuple(sum(w*v[j] for w,v in zip(weights,(U,W,V)))/den
                              for j in range(3))
    return points, z, root

def reference_core(reference_shift=0):
    # Credited incumbent cross Gram coefficients from 8755/generate.py.
    aa = E(['-27/2','-3','35','-24','117/2']) + E(reference_shift)
    bb = E(['-31/4','-19/2','34','-53/2','195/4'])
    cc = E(['81/4','21/2','-69','101/2','-429/4'])
    M = ((aa,bb,cc),(cc,aa,bb),(bb,cc,aa))
    points = {label:tuple(ONE if i==j else ZERO for j in range(3))
              for i,label in enumerate((0,5,11))}
    for j,label in enumerate((1,2,4)):
        points[label] = hinverse(tuple(M[i][j] for i in range(3)))
    r = 2*T/(1+T)
    for n,i,j,o in STEPS:
        points[n] = tuple(r*(x+y)-v for x,y,v in zip(points[i],points[j],points[o]))
    points[3] = tuple(r*(x+y)-v for x,y,v in zip(points[1],points[4],points[2]))
    return points

def verify(radical_orientation=-1, boundary_shift=0, u_orientation=1, reference_shift=0):
    derivative_lower = a.verify_root()
    points,z,root = boundary_core(radical_orientation,boundary_shift,u_orientation)
    reference = reference_core(reference_shift)
    require(sorted(points)==[0,1,2,4,5,6,7,8,9,10,11,12,13], 'literal thirteen labels')
    require(len(G22)==22 and len(G24)==24, 'literal contact counts')
    for label,point in points.items():
        require(dot(point,point)==ONE, 'exact unit norm '+str(label))
    normal_forms, noncontacts = {}, 0
    for i,j in combinations(sorted(points),2):
        gap = dot(points[i],points[j])-T
        if (i,j) in G24:
            require(gap==ZERO, 'exact contact '+str((i,j)))
        else:
            require(gap.sign()<0, 'strict noncontact packing gap '+str((i,j)))
            noncontacts += 1
        if (i,j) in DELETED: normal_forms[f'{i},{j}'] = list(map(str,gap.c))
    gram_count = 0
    for i in sorted(points):
        for j in sorted(points):
            if j<i: continue
            require(dot(points[i],points[j])==dot(reference[i],reference[j]),
                    'incumbent labeled Gram equality '+str((i,j)))
            gram_count += 1
    critical = intersection(points,(1,4,7))
    require(dot(critical,critical)==ONE, 'critical147 is unit at the boundary')
    critical_contacts = []
    for i in sorted(points):
        gap = dot(critical,points[i])-T
        require(gap.sign()<=0, 'critical147 avoids the entire core')
        if gap==ZERO: critical_contacts.append(i)
        require(dot(critical,points[i])==dot(reference[3],reference[i]),
                'critical147 agrees with reference p3 under the core congruence')
    require(critical_contacts==[1,4,7], 'exact critical147 contact labels')
    long1,long2 = (intersection(points,labels) for labels in ((0,4,6),(0,4,7)))
    normal = tuple(x+y+E('4/5')*v for x,y,v in zip(long1,long2,critical))
    nn, projection = dot(normal,normal), dot(normal,critical)
    require(nn.sign()>0, 'nonzero avoidance-cut normal')
    require(projection.sign()<=0 or (E('893/1000')**2*nn-projection**2).sign()>0,
            'critical147 lies strictly inside the closed cut halfspace')
    canonical = {str(i):[list(map(str,x.c)) for x in point] for i,point in sorted(points.items())}
    digest = hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return dict(status='CHECKED_G22_BOUNDARY_CONTACTS_AND_INCUMBENT_GRAM',
                agent='six-tammes-2',role='researcher',domain='Q[X]/(F), characteristic zero',
                irreducibility_assumed=False,root_bracket=[str(a.LO),str(a.HI)],
                full_J_derivative_lower=derivative_lower,unit_norms=13,
                prescribed_contacts=22,recovered_contacts=2,strict_noncontact_gaps=noncontacts,
                labeled_Gram_equalities=gram_count,critical147_unit=True,
                critical147_reference_Gram_equalities=13,
                critical147_contact_labels=critical_contacts,critical147_inside_cut=True,
                deleted_gap_normal_forms=normal_forms,
                boundary_parameter_coefficients=list(map(str,z.c)),
                positive_radical_coefficients=list(map(str,root.c)),
                coordinate_sha256=digest,checked_distinct_Bezout_inverses=len(a.INVERSES),
                geometric_boundary_forcing_checked_by_program=False,
                independent_researcher_review=False)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt',type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(
        TimeoutError('160-second arithmetic guard: incomplete evidence')))
    signal.alarm(160)
    try:
        result = verify()
    finally:
        signal.alarm(0)
    result['seconds'] = round(time.monotonic()-started,3)
    if args.receipt: args.receipt.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
