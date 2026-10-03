"""Independent stdlib binding of EVERY regenerated seven-family coefficient."""
from pathlib import Path
from fractions import Fraction as F
import json
import cap
p=cap.r.poly;require=cap.require
Q,K=p.Q,p.K
C,A,M,S=p.constant,p.add,p.mul,p.scale
z=cap.v.z


def decode(xs):
    # SymPy exports its zero polynomial with this single conventional
    # monomial. Accept that representation only in its entirety.
    if xs==[[[0,0],'0']]:return {}
    out={}
    for power,value in xs:
        key=tuple(power)
        require(len(key)==2 and all(type(x) is int and x>=0 for x in key) and key not in out,
                'unique complete bivariate monomial powers')
        value=F(value);require(value!=0,'no spurious zero polynomial coefficient')
        out[key]=value
    return out


def matrix_decode(xs):return [[decode(v) for v in row] for row in xs]
def record(poly):return [[list(power),str(value)] for power,value in sorted(poly.items())]
def matrix_record(G):return [[record(v) for v in row] for row in G]


def choose(n,r):return C(1) if r==0 else n if r==1 else S(M(n,A(n,C(-1))),F(1,2))


def original_full11():
    D,tab=z.clearing()
    tab={key:{power:value for power,value in poly.items() if power[1]==0} for key,poly in tab.items()}
    height=A(S(M(Q,Q),F(1,2)),S(Q,F(7,2)),C(4),S(K,-1))
    mass=[S(choose(Q,t[1]),len(gs)) for gs,t in zip(cap.GROUPS,cap.TYPES)]
    G=[]
    for i,t in enumerate(cap.TYPES):
        row=[]
        for j,tt in enumerate(cap.TYPES):
            count=sum(not(a&b) for a in cap.GROUPS[i] for b in cap.GROUPS[j])
            value=S(M(M(D,height),mass[i]),4*int(i==j))
            if count:
                value=A(value,S(M(M(choose(Q,t[1]),choose(A(Q,C(-t[1])),tt[1])),tab[tuple(sorted((t,tt)))]),-4*count))
            actual=p.divide(value,D)
            require(all(v.denominator==1 for v in actual.values()),'EVERY full11 integer polynomial coefficient')
            row.append(actual)
        G.append(row)
    require(all(G[i][j]==G[j][i] for i in range(11) for j in range(11)),
            'EVERY complete full11 polynomial reciprocity coefficient')
    return G


def multiply(A,B):
    return [[p.add(*(p.mul(A[i][t],B[t][j]) for t in range(len(B)))) for j in range(len(B[0]))] for i in range(len(A))]


def submatrix(G,rows,cols=None):return [[G[i][j] for j in (rows if cols is None else cols)] for i in rows]
def transpose(G):return [list(row) for row in zip(*G)]


def matrix_evaluate(G,q,k):
    values=[[p.evaluate(v,q,k) for v in row] for row in G]
    require(all(v.denominator==1 for row in values for v in row),'EVERY evaluated integer polynomial position')
    return [[int(v) for v in row] for row in values]


def degree_bound(G,variable):
    return sum(max((power[variable] for poly in row for power in poly),default=0) for row in G)


def generated():
    import regenerate
    G=original_full11()
    d,Y,H=regenerate.seven(G)
    return {'complete_full11_gram4':matrix_record(G),
            'complete_seven_determinant':record(d),
            'complete_seven_solve_adjugate_action':matrix_record(Y),
            'complete_four_short_numerator':matrix_record(H)}


def verify(raw=None):
    if raw is None:raw=generated()
    G=original_full11();supplied=matrix_decode(raw['complete_full11_gram4'])
    require(G==supplied,'ALL supplied full11 coefficients equal independent cleared original table')
    d=decode(raw['complete_seven_determinant'])
    Y=matrix_decode(raw['complete_seven_solve_adjugate_action'])
    short=matrix_decode(raw['complete_four_short_numerator'])
    R=list(range(3,10));T=[0,1,2,10]
    B=submatrix(G,R);X=submatrix(G,R,T);target=submatrix(G,T)
    require(len(Y)==7 and all(len(row)==4 for row in Y),'entire seven-by-four solve shape')
    lhs=multiply(B,Y);rhs=[[p.mul(d,v) for v in row] for row in X]
    require(lhs==rhs,'EVERY polynomial coefficient of all28 original solve equations')
    cross=multiply(transpose(X),Y)
    expected=[[p.add(p.mul(d,target[i][j]),p.scale(cross[i][j],-1)) for j in range(4)] for i in range(4)]
    require(short==expected,'EVERY polynomial coefficient of all16 source Schur numerators')
    qdegree,kdegree=degree_bound(B,0),degree_bound(B,1)
    require(all(i<=qdegree and j<=kdegree for i,j in d),'proved full determinant coordinate-degree bounds')
    points=[]
    # Complete rectangular grid inside the ORIGINAL proved integer domain.
    for kk in range(3,4+kdegree):
        for qq in range(3*(3+kdegree),3*(3+kdegree)+qdegree+1):
            value=matrix_evaluate(B,qq,kk)
            actual=z.det_integer(value)
            require(actual==z.det_fraction(value)==p.evaluate(d,qq,kk)>0,
                    'EVERY grid point: two exact determinants and full positive original minor')
            points.append([qq,kk,str(actual)])
    # A critical mathematical cancellation: the 2x2 minors of the
    # short numerator carry the original seven determinant, by Jacobi.
    border=[]
    for i in range(3):
        row=[]
        for j in range(3):
            numerator=p.add(p.mul(short[i][j],short[3][3]),p.scale(p.mul(short[i][3],short[j][3]),-1))
            row.append(p.divide(numerator,d))
        border.append(row)
    return {'actual_agent':'six-downset-3','role':'researcher',
            'ordinary_domain':'ALL integerk>=3,q>=3k; original untouched positivity is credited',
            'complete_solve_coefficient_identity':True,'complete_Schur_coefficient_identity':True,
            'determinant_degree_bounds':[qdegree,kdegree],'full_exact_grid_count':len(points),
            'full_two_algorithm_grid_sha256':cap.r.exact.digest(points),
            'complete_border_minors_divided_by_original_determinant':matrix_record(border),
            'full_input11_sha256':cap.r.exact.digest(matrix_record(G)),
            'all_rectangular_grid_points_in_original_domain':True,
            'all_polynomial_divisions_multiplied_back':True,
            'CAS_not_imported':True,'independent_person_review':False,
            'ordinary_symmetry_fullspace_bridges_unformalized':True}


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    value=verify();args.out.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'degree_bounds':value['determinant_degree_bounds'],'complete_exact_points':value['full_exact_grid_count'],'all_solve_and_Schur_coefficients_checked':True}))
