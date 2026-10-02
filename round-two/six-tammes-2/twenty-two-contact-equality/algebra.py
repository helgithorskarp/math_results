"""Independent arithmetic route over QQ(t), using SymPy 1.14.0.

All boundary unit/contact identities are rational-function identities.
The two deleted contacts vanish after specialization F(t)=0. The
positive radical branch and geometric reduction are separate premises.
No large certificate is required or written by default.
"""
import argparse
import hashlib
import json
import os
from itertools import combinations
from pathlib import Path
import signal
import time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
             'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
import sympy as sp
from sympy.polys.fields import field
from sympy.polys.domains import QQ

def require(condition, message):
    if not condition: raise ValueError(message)

def derive():
    K,t = field('t',QQ)
    x = sp.Symbol('t')
    F = 13*t**5-t**4+6*t**3+2*t*t-3*t-1
    modulus = sp.Poly(F.as_expr(),x,domain=QQ)
    def poly(p): return sp.Poly(p.as_expr(),x,domain=QQ)
    def reduced(q):
        n,d = poly(q.numer),poly(q.denom)
        require(sp.gcd(d,modulus).degree()==0, 'specialization denominator coprime to F')
        p = (n.rem(modulus)*sp.invert(d,modulus)).rem(modulus)
        return [str(p.nth(i)) for i in range(5)]
    def dot(a,b): return (1-t)*sum(v*w for v,w in zip(a,b))+t*sum(a)*sum(b)
    def cross(a,b): return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
    def him(a): return [v/(1-t)-t*sum(a)/((1-t)*(1+2*t)) for v in a]
    r = 2*t/(1+t)
    D = (1-t)**2*(1+2*t)
    A = t**3-3*t*t+t+1
    z = 2*t*t/A
    C = 1+D*z*z
    k = t*(9*t*t-2*t-3)/(1+t)**2
    gamma = k/(1+k)
    mu = (t-1)*(t+1)*(2*t+1)*(3*t-1)/(9*t**3-t*t-t+1)
    points = {label:[K(int(i==j)) for j in range(3)] for i,label in enumerate((1,2,4))}
    for n,i,j,o in ((8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,8,4)):
        points[n] = [r*(a+b)-v for a,b,v in zip(points[i],points[j],points[o])]
    normal = him(cross(points[12],points[1]))
    W = [t*a+(D*z*z-1)/C*(b-t*a)+2*D*z/C*v for a,b,v in zip(points[12],points[1],normal)]
    s = dot(W,points[10])
    delta = 1-s*s
    g = delta-k*k-t*t+2*s*k*t
    P4 = 8*t**4-3*t**3-t*t+3*t+1
    P5 = 4*t**5-19*t**4-2*t**3+4*t*t-2*t-1
    root = -(t-1)**2*(2*t+1)*(3*t+1)*P5/((t+1)**2*P4)
    require(root*root==D*g, 'exact rational radical square identity')
    normal = him(cross(W,points[10]))
    V = [((k-s*t)*a+(t-s*k)*b-root*n)/delta for a,b,n in zip(W,points[10],normal)]
    normal = him(cross(W,V))
    U = [gamma*(a+b)+mu*n for a,b,n in zip(W,V,normal)]
    points.update({6:U,7:W,9:V})
    den = (2*r-1)*(r+1)
    for label,weights in ((0,(r,r,1-r)),(5,(1-r,r,r)),(11,(r,1-r,r))):
        points[label] = [sum(w*v[j] for w,v in zip(weights,(U,W,V)))/den for j in range(3)]
    contacts = {(0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),
                (2,4),(2,8),(2,10),(2,13),(4,8),(5,7),(5,9),(5,11),
                (6,11),(7,12),(8,13),(9,10),(9,11),(10,12)}
    for label,p in points.items(): require(dot(p,p)==1, 'QQ(t) unit identity '+str(label))
    deleted = {}
    for i,j in combinations(sorted(points),2):
        gap = dot(points[i],points[j])-t
        if (i,j) in contacts: require(gap==0, 'QQ(t) contact identity '+str((i,j)))
        form = reduced(gap)
        if (i,j) in ((6,8),(9,13)):
            require(form==['0']*5, 'deleted contact zero modulo F '+str((i,j)))
            deleted[f'{i},{j}'] = form
    coordinates = {str(i):[reduced(q) for q in p] for i,p in sorted(points.items())}
    digest = hashlib.sha256(json.dumps(coordinates,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return dict(status='CHECKED_QQ_T_BOUNDARY_IDENTITIES',agent='six-tammes-2',role='researcher',
                domain='QQ(t), characteristic zero; specialization modulo F',
                sympy_version=sp.__version__,rational_unit_identities=13,
                rational_G22_contact_identities=22,all_pair_specialization_checks=78,
                coordinate_specialization_checks=39,deleted_gap_normal_forms=deleted,
                coordinate_sha256=digest,positive_radical_branch_checked_by_this_program=False,
                surrounding_geometric_theorem_checked_by_this_program=False,
                independent_researcher_review=False)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt',type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(
        TimeoutError('160-second rational algebra guard: incomplete evidence')))
    signal.alarm(160)
    try: result = derive()
    finally: signal.alarm(0)
    result['seconds'] = round(time.monotonic()-started,3)
    if args.receipt: args.receipt.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
