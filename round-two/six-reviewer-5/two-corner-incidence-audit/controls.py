"""Independent arithmetic and polygon calibration; no target inputs."""
from fractions import Fraction as Q
from itertools import product,combinations
import json
import independent as I
K=I.K

def main():
    checks=0
    def check(ok,name):
        nonlocal checks
        K.need(ok,name);checks+=1
    for roots in product(range(-2,3),repeat=3):
        p=K.ONE
        for r in roots:p=K.mul(p,(-r,1))
        n,_=K.sturm(p,Q(-5,2),Q(5,2))
        check(n==len(set(roots)),'Sturm distinct/repeated calibration')
    for endpoint in (Q(18,29),Q(19,25)):
        try:K.sturm((-endpoint,1),Q(18,29),Q(19,25))
        except ValueError:checks+=1
        else:raise ValueError('closed endpoint root missed')
    for degree in range(16):
        p=tuple(Q((-1)**i*(i+1)) for i in range(degree+1))
        check(K.interpolate([K.value(p,j) for j in range(degree+1)])==p,'independent Newton calibration')
    # At r=0 the reflected recurrence alternates orthogonal anchor vectors.
    for m in (3,4):
        prev,current,out=K.E
        result=K.fan_at(0,m,K.E)
        check(result==(current,tuple(-v for v in out),tuple(-v for v in prev)) if m==3 else result==(current,prev,tuple(-v for v in out)),'zero reflection control')
    # Complete noncrossing diagonal-subset checker, separate from root recursion.
    for n,cat in ((3,1),(4,2),(5,5),(6,14),(7,42),(8,132)):
        root=I.triangulations(tuple(range(n)))
        check(len(root)==cat,'Catalan count')
        edges={tuple(sorted((i,(i+1)%n))) for i in range(n)}
        diagonals=[e for e in combinations(range(n),2) if e not in edges]
        independent=[]
        for ds in combinations(diagonals,n-3):
            if any(a<c<b<d or c<a<d<b for (a,b),(c,d) in combinations(ds,2)):continue
            ee=edges|set(ds)
            triangles=tuple(t for t in combinations(range(n),3) if all(e in ee for e in combinations(t,2)))
            check(len(triangles)==n-2,'complete planar triangle extraction')
            independent.append(triangles)
        check(set(independent)==set(root),'root recursion vs noncrossing diagonal subsets')
    # Every length-six mixed placement, including absent nonalternating controls.
    for n in range(3,7):
        for mixed in combinations(range(n),3):
            c=I.cap(dict(length=n,mixed=mixed))
            expected=n==3 or (n==6 and mixed in ((0,2,4),(1,3,5)))
            check(bool(c['valid'])==expected,'all possible mixed vertex placements')
    check(Q(9,29)==(Q(65,29)-1)/4 and 65**2>5*29**2,'strict upper-alpha comparison')
    check(Q(19,50)<Q(1,2),'strict lower-alpha comparison')
    check(Q(2)*Q(9,20)/(1+Q(9,20))==Q(18,29),'lower cosine transform')
    check(Q(2)*Q(19,31)/(1+Q(19,31))==Q(19,25),'upper cosine transform')
    print(json.dumps(dict(calibration_checks=checks,closed_endpoint_rejections=2,rooted_polygon_vs_diagonal_sets='complete3..8',author_inputs_used=False),sort_keys=True))
if __name__=='__main__':main()
