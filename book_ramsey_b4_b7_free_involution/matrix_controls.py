"""Exact vector/Gram audits of the two analytic six-pair contradictions.
Author: six-books-2, role researcher. Standard library; no spectral numerics.
These validate written arguments, not all order22 graph signings.
"""
from itertools import product,combinations
from fractions import Fraction
import json,time

def check(ok,message):
    if not ok:raise RuntimeError(message)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def lin(*terms):return tuple(sum(c*v[i] for c,v in terms) for i in range(6))
def coords(basis,image):
    n=len(basis);g=[[Fraction(dot(x,y)) for y in basis]+[Fraction(dot(x,image))] for x in basis]
    for i in range(n):
        pivot=next((j for j in range(i,n) if g[j][i]),None);check(pivot is not None,'independent basis')
        g[i],g[pivot]=g[pivot],g[i];s=g[i][i];g[i]=[x/s for x in g[i]]
        for j in range(n):
            if j==i:continue
            s=g[j][i];g[j]=[a-s*b for a,b in zip(g[j],g[i])]
    result=[g[i][-1] for i in range(n)]
    check(all(sum(result[j]*basis[j][i] for j in range(n))==image[i] for i in range(6)),'invariant image')
    return result
start=time.monotonic();balanced=[v for v in product([-1,1],repeat=6) if sum(v)==0]
check(len(balanced)==20,'balanced row universe')
rank_one=0
for values in product([-1,1],repeat=4):
    p=[values[:2],values[2:]]
    # A same-group dot product is2 modulo4 and equals minus this row dot.
    if dot(p[0],p[1])==0:continue
    check(values[0]*values[3]==values[1]*values[2],'rank-one sign block')
    switched=[[p[i][j]*p[i][0]*p[0][j]*p[0][0] for j in range(2)] for i in range(2)]
    check(switched==[[1,1],[1,1]],'all-positive switch')
    rank_one+=1
check(rank_one==8,'eight rank-one sign blocks')
a_cases=0
for p1,p2 in product(balanced,repeat=2):
    if dot(p1,p2)!=-2:continue
    candidates=[v for v in balanced if dot(v,p1)==dot(v,p2)==-2]
    for q1,q2 in product(candidates,repeat=2):
        if dot(q1,q2)!=-2:continue
        p=lin((1,p1),(1,p2));q=lin((1,q1),(1,q2))
        check(lin((1,p),(1,q))==(0,)*6,'four-row zero sum')
        check(dot(p,p)==8,'nonzero U sum')
        pc=lin((-3,p),(-2,q));qc=lin((-1,q),(-2,p))
        check(pc==lin((-1,p)) and qc==q,'opposite required eigenvalues')
        check(qc!=lin((-1,pc)),'contradiction to linearity')
        a_cases+=1
check(a_cases==720,'all normalized A vector cases')
a=(1,)*6;twoplus=[v for v in product([-1,1],repeat=6) if sum(v)==-2]
b_cases=0
for r1,r2 in product(twoplus,repeat=2):
    if dot(r1,r2)!=-2:continue
    rows=[v for v in balanced if dot(v,r1)==dot(v,r2)==0]
    for r0,r3 in product(rows,repeat=2):
        if dot(r0,r3)!=-2:continue
        first=[a,r1,r2];second=[r0,r3]
        check([[dot(x,y) for y in first] for x in first]==[[6,-2,-2],[-2,6,-2],[-2,-2,6]],'B first Gram')
        check([[dot(x,y) for y in second] for x in second]==[[6,-2],[-2,6]],'B second Gram')
        check(all(dot(x,y)==0 for x in first for y in second),'orthogonal spaces')
        images_first=[lin((-1,a),(-1,r1),(-1,r2)),lin((-1,a),(-3,r1),(-1,r2)),lin((-1,a),(-1,r1),(-3,r2))]
        images_second=[lin((-2,r0),(-1,r3)),lin((-1,r0),(-2,r3))]
        cf=[coords(first,im) for im in images_first];cs=[coords(second,im) for im in images_second]
        check(sum(cf[i][i] for i in range(3))==-7,'three-space trace')
        check(sum(cs[i][i] for i in range(2))==-4,'two-space trace')
        forced_last=-(sum(cf[i][i] for i in range(3))+sum(cs[i][i] for i in range(2)))
        check(forced_last==11 and abs(forced_last)>5,'C sign-row bound violated')
        b_cases+=1
check(b_cases==2160,'all normalized B vector cases')
result={'agent':'six-books-2','role':'researcher','complete':True,'rank_one_sign_blocks':rank_one,'shape_A_all_normalized_vector_cases':a_cases,'shape_B_all_normalized_vector_cases':b_cases,'shape_B_invariant_space_traces':[-7,-4],'forced_remaining_eigenvalue':11,'maximum_sign_matrix_eigenvalue_absolute_bound':5,'exact_fraction_coordinates':True,'wall_seconds':time.monotonic()-start,'full_graph_enumeration':False}
print(json.dumps(result,indent=2))
