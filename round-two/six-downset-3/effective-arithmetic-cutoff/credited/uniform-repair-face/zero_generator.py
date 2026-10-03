"""Regenerate the entire residual and optimizer using stdlib integer arithmetic.

No CAS, private coefficient table or generated discovery input is read.
All exact divisions use the credited algorithm with a full multiply-back.
"""
from functools import lru_cache
import input as inputs
import factors
z, require = inputs.ipoly, inputs.require

def decode(rows):
    return factors.decode(rows) if rows else {}

def record(poly):
    return [[list(power),str(value)] for power,value in sorted(poly.items())]

def matrix_record(matrix):
    return [[record(value) for value in row] for row in matrix]

def det(matrix):
    if len(matrix)==1:return matrix[0][0]
    return z.add(*(z.scale(z.mul(matrix[0][j],det([row[:j]+row[j+1:] for row in matrix[1:]])),(-1)**j)
                   for j in range(len(matrix))))

@lru_cache(maxsize=1)
def generated():
    raw=inputs.portable_frame.generated() | inputs.portable_fields.generated()
    d=decode(raw['complete_seven_determinant'])
    H=[[decode(poly) for poly in row] for row in raw['complete_four_short_numerator']]
    g=factors.factor('zero_short_common')
    dc=z.divide(d,g);HH=[[z.divide(poly,g) for poly in row] for row in H]
    nn,nd=(decode(raw['nu_U'][side]) for side in ('numerator','denominator'))
    an,ad=(decode(raw['a0'][side]) for side in ('numerator','denominator'))
    W=[[z.divide(z.add(z.mul(HH[i][j],HH[3][3]),z.scale(z.mul(HH[i][3],HH[j][3]),-1)),dc)
        for j in range(3)] for i in range(3)]
    Q,K={(1,0):1},{(0,1):1};survivors=z.add(Q,z.scale(K,-1))
    T=z.add(z.scale(z.mul(z.mul(z.mul(Q,dc),K),nn),4),z.mul(z.mul(survivors,HH[3][3]),nd))
    P=[[z.add(z.scale(z.mul(z.mul(z.mul(Q,K),nn),HH[i][j]),4),z.mul(z.mul(survivors,nd),W[i][j]))
        for j in range(3)] for i in range(3)]
    PH=z.divide(z.add(z.mul(P[0][0],P[2][2]),z.scale(z.mul(P[0][2],P[0][2]),-1)),T)
    adj=[[z.scale(det([[P[ii][jj] for jj in range(3) if jj!=i]
                      for ii in range(3) if ii!=j]),(-1)**(i+j)) for j in range(3)] for i in range(3)]
    ss=(-1,1,1)
    Aq=z.divide(z.add(*(z.scale(adj[i][j],ss[i]*ss[j]) for i in range(3) for j in range(3))),T)
    dp=z.divide(det(P),z.mul(T,T))
    num=z.add(z.mul(ad,dp),z.scale(z.mul(an,Aq),4))
    den=z.add(z.mul(ad,PH),z.scale(z.mul(an,z.add(P[0][0],P[2][2],z.scale(P[0][2],2))),4))
    hx=z.scale(z.add(z.mul(ad,z.divide(z.add(z.mul(P[2][2],P[0][1]),z.scale(z.mul(P[0][2],P[1][2]),-1)),T)),
                    z.scale(z.mul(an,z.add(z.scale(P[2][2],-1),P[0][1],z.scale(P[0][2],-1),P[1][2])),4)),-1)
    hz=z.scale(z.add(z.mul(ad,z.divide(z.add(z.mul(P[0][0],P[1][2]),z.scale(z.mul(P[0][2],P[0][1]),-1)),T)),
                    z.scale(z.mul(an,z.add(P[0][0],P[1][2],P[0][2],P[0][1])),4)),-1)
    twoN=z.add(z.mul(Q,Q),z.scale(Q,13),{(0,0):16},z.scale(K,-2))
    gg=z.mul(Q,z.mul(twoN,twoN))
    n,d0=z.divide(num,gg),z.divide(den,gg)
    flip=1 if z.evaluate(d0,27,7)>0 else -1
    n,d0=z.scale(n,flip),z.scale(d0,flip)
    return {'actual_agent':'six-downset-3','role':'researcher','CAS_not_imported':True,
        'domain':'ZZ[q,k], characteristic0, lex q then k','entire_committed_input_gate':inputs.SOURCE,
        'short_common_factor':record(g),'reduced_seven_determinant':record(dc),
        'complete_reduced_four_short':matrix_record(HH),'complete_border_minors':matrix_record(W),
        'cap_target':record(T),'complete_zero_cap_numerator':matrix_record(P),
        'lower_numerator':record(an),'lower_denominator':record(ad),
        'joint_numerator_before_gcd':record(num),'joint_denominator_before_gcd':record(den),
        'joint_gcd':record(gg),'joint_residual_numerator':record(n),'joint_residual_denominator':record(z.scale(d0,4)),
        'optimizer_a_numerator':record(hx),'optimizer_abac_numerator':record(hz),
        'optimizer_common_denominator':record(den),'full_repair_gap_numerator':record(n),
        'full_repair_gap_denominator':record(z.scale(d0,8)),
        'new_gcd_exact_divisions_multiplied_back':True,'independent_review':False,
        'ordinary_fullspace_bridges_unformalized':True}
