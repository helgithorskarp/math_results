"""Full exact 505-point reconstruction of both SAT discovery controls."""
from itertools import combinations,permutations
import json
import audit as A
import census as C

def full_points(B,V,m,n):
    # Each complex coordinate has eight real radical coefficients /576.
    pts=[tuple(A.scale(z,8) for z in A.cartesian(p)) for p in B]
    mx,my=pts[m];right={n:m}
    for j,q in enumerate(V):
        if j==n:continue
        x,y=A.cartesian(A.delta(q,V[n]))
        re=A.add(mx,A.add(A.scale(x,7),A.scale(A.mul(A.SQ15,y),-1)))
        im=A.add(my,A.add(A.mul(A.SQ15,x),A.scale(y,7)))
        right[j]=len(pts);pts.append((re,im))
    return pts,right

def strict_edges(pts):
    ee=[]
    for i,j in combinations(range(len(pts)),2):
        re=A.add(pts[i][0],A.scale(pts[j][0],-1));im=A.add(pts[i][1],A.scale(pts[j][1],-1))
        if A.add(A.mul(re,re),A.mul(im,im))==(576**2,0,0,0,0,0,0,0):ee.append((i,j))
    return ee

def run():
    B,V=A.source();EB,EV=A.source_edges(B),A.source_edges(V)
    cb,cv=A.library(B,EB,'B'),A.library(V,EV,'V')
    B0,V0,_,_=C.sources();I,J=C.differences(B0),C.differences(V0)
    pairs,_=C.contact_pairs(I,J);all_edges=C.project(I,J,pairs)
    # Independently count failures of the two inherited positive libraries.
    failures=[]
    for sizes in ((3,2),(8,7)):
        count=sum(C.witness(*divmod(label,214),ee,[cb[:sizes[0]],cv[:sizes[1]]]) is None for label,ee in enumerate(all_edges))
        failures.append({'library_sizes':sizes,'uncovered':count})
    A.require([r['uncovered'] for r in failures]==[858,82],'baseline residual count differs')
    rows=[]
    for number,(m,n) in enumerate(((119,169),(79,167))):
        pts,right=full_points(B,V,m,n)
        A.require(len(pts)==len(set(pts))==505,'overlap count or coordinates wrong')
        actual=strict_edges(pts)
        predicted=sorted(set(tuple(sorted(e)) for e in EB+[(right[i],right[j]) for i,j in EV]+[(i,right[j]) for i,j in all_edges[214*m+n]]))
        A.require(actual==predicted,'strict full graph differs from census')
        ee=all_edges[214*m+n]
        A.require(C.witness(m,n,ee,[cb[:8],cv[:7]]) is None,'control already covered by inherited library')
        left,other=cb[8+number],cv[7+number]
        pi=next(p for p in permutations(range(4)) if left[m]==p[other[n]] and all(left[i]!=p[other[j]] for i,j in ee))
        col=list(left)+[pi[other[j]] for j in range(214) if j!=n]
        A.require(all(col[i]!=col[j] for i,j in actual),'positive full colouring failed')
        bad=col.copy();bad[actual[0][1]]=bad[actual[0][0]]
        A.require(not all(bad[i]!=bad[j] for i,j in actual),'mutated colour certificate accepted')
        rows.append({'anchors':[m,n],'vertices':len(pts),'pairs_checked':len(pts)*(len(pts)-1)//2,
                     'strict_edges':len(actual),'strict_edge_sha256':A.digest(actual),
                     'colouring_sha256':A.digest(col),'new_cross_edges':len(ee),'inherited_library_fails':True,
                     'positive_colouring_verified':True,'one_colour_mutation_rejected':True})
    # A hand-checkable contact: x=y=2, since |2-2u|^2=1.
    x=(144,0,0,0)
    A.require(A.exact_contact(x,x) and not A.exact_contact((72,0,0,0),(72,0,0,0)),'scale control failed')
    A.require(C.slope((0,0,72,0))==C.slope((0,0,-72,0))==(0,),'imaginary axis normalization failed')
    A.require(C.slope((72,0,0,0))==C.slope((-72,0,0,0))==(1,0,0),'real-axis sign normalization failed')
    return {'baseline_libraries':failures,'full_geometry_controls':rows,'total_full_pairs_checked':254520,
            'unit_and_nonunit_scale_controls':True,'projective_axis_and_sign_controls':True}
if __name__=='__main__':print(json.dumps(run(),indent=2))
