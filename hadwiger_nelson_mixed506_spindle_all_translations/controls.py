"""Direct strict geometry for the unique old-library residual and circle controls."""
from itertools import combinations
from pathlib import Path
from fractions import Fraction as Q
import json
import audit as A
import square_field as F

KEY=(16,-14,0,-3,0,-9,0,-2,0)
CONTACTS=[17073,18143,19132,44679,53453,61585]

def graph():
    B,V=A.source();D=KEY[0];raw=[[str(Q(x,D)) for x in KEY[1:5]],[str(Q(x,D)) for x in KEY[5:]]]
    hd,h=A.hcart(raw);A.require(576%hd==0,'unexpected control denominator')
    pts=[A.cs(A.cart(p),8) for p in B]+[A.ca(A.cm(A.UNUM,A.cart(q)),A.cs(h,576//hd)) for q in V]
    A.require(len(pts)==len(set(pts))==506,'control has an overlap')
    edges=[]
    for i,j in combinations(range(506),2):
        if A.cn(A.ca(pts[i],A.cs(pts[j],-1)))==A.scale(A.ONE,576**2):edges.append((i,j))
    cross=[214*i+j-292 for i,j in edges if i<292<=j]
    A.require(cross==CONTACTS,'full strict contact list differs')
    A.require(sum(j<292 for i,j in edges)==1251 and sum(i>=292 for i,j in edges)==977,'full strict source edges differ')
    return B,V,edges

def run():
    B,V,edges=graph();EB,EV=A.source_edges(B),A.source_edges(V);libs=A.libraries(B,V,EB,EV)
    A.require(A.witness(CONTACTS,[libs[0][:-1],libs[1][:-1]]) is None,'inherited library covers control')
    w=A.witness(CONTACTS,libs);A.require(w is not None,'new library misses control')
    ib,iv,ip=w;pi=list(A.permutations(range(4)))[ip]
    colours=list(libs[0][ib])+[pi[c] for c in libs[1][iv]]
    A.require(all(colours[i]!=colours[j] for i,j in edges),'full positive colouring invalid')
    wrong=colours.copy();wrong[edges[0][1]]=wrong[edges[0][0]]
    A.require(not all(wrong[i]!=wrong[j] for i,j in edges),'mutated colouring accepted')
    # Zero, tangent, two-circle, and nonintersection cases in exact K arithmetic.
    zero=(0,0,0,0)
    cases=[('coincident',(0,0,0,0),zero,0),('unit_separation',(72,0,0,0),zero,2),('tangent',(144,0,0,0),zero,1),('separated',(216,0,0,0),zero,0)]
    circle_rows=[]
    for name,x,y,n in cases:
        hs=F.circles(x,y);A.require(len(hs)==n,'circle boundary case failed')
        for h in hs:
            D,z=A.hcart(F.encode(h));wn=A.wnum(x,y);L=A.lcm(D,576)
            A.require(A.cn(z)==A.scale(A.ONE,D*D) and A.cn(A.ca(A.cs(z,L//D),A.cs(wn,-L//576)))==A.scale(A.ONE,L*L),'independent boundary centre invalid')
        circle_rows.append([name,n])
    # Exhaustive bounded square inputs: the generator must retain every square.
    checks=0
    for a,b,c,d in A.product(range(-1,2),repeat=4):
        x=tuple(map(Q,(a,b,c,d)));sq=F.mul(x,x);r=F.sqrt(sq)
        A.require(r is not None and F.mul(r,r)==sq,'square generator missed an explicit square');checks+=1
    A.require(F.sqrt(tuple(map(Q,(3,0,0,0)))) is None,'sqrt3 incorrectly lies in F')
    return {'vertices':506,'physical_pairs_checked':127765,'strict_edges':len(edges),'contacts':CONTACTS,
            'translation_K_basis':KEY,'old_library_fails':True,'new_witness':w,'positive_four_colouring':True,
            'edge_sha256':A.digest(edges),'colour_sha256':A.digest(colours),'one_colour_mutation_rejected':True,
            'circle_boundary_cases':circle_rows,'exhaustive_small_square_controls':checks,'sqrt3_field_boundary_checked':True}
if __name__=='__main__':print(json.dumps(run(),indent=2))
