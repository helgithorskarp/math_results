"""Exact factored arrow determinants and positive full-quadrant coefficients."""
from fractions import Fraction as F
from trivariate import P,R,ATOMS,PROBES,DEN_CACHE,atom
from model import arrow,base_pairing
from polynomial import clear_rows
from exact import require

def shift(p):
    u,v,w=P({(1,0,0):1}),P({(0,1,0):1}),P({(0,0,1):1})
    substitution=(3+u,2+v,12+4*u+4*v+w)
    powers={};result=P(0)
    for ex,co in sorted(p.a.items()):
        term=P(co)
        for index,degree in enumerate(ex):
            key=(index,degree)
            if key not in powers:powers[key]=substitution[index]**degree
            term=term*powers[key]
        result=result+term
    return P(result.a,result.den*p.den)

def encode(p):
    return {'denominator':p.den,'terms':[[list(e),str(c)] for e,c in sorted(p.a.items())]}

def generate():
    ATOMS.clear();PROBES.clear();DEN_CACHE.clear()
    r,l,q=R(P({(1,0,0):1})),R(P({(0,1,0):1})),R(P({(0,0,1):1}))
    m=3*r+l;N=2*q+2*m;H=N-1;D=N-7;A=N-q-2
    J=A*(N-4)-3*(q-1)
    for z in (r,l,r-1,l-1,q,q-1,q+1,m,m+1,H,D,q+3,A,J):atom(z.num)
    aug,_=arrow(q,r,l,fraction=lambda a,b=1:R(a)/b)
    aa,zz,bb,cc,dd,a,b,e=aug[0][0],aug[0][1],aug[1][1],aug[1][2],aug[2][2],aug[0][3],aug[1][3],aug[3][3]
    rows=[];d3=sub=None
    for order in range(1,5):
        if order==1:det=aa
        elif order==2:det=aa*bb-zz*zz
        elif order==3:
            sub=bb*dd-cc*cc;d3=det=aa*sub-zz*zz*dd
        else:det=e*d3-a*a*sub+2*a*b*zz*(dd+cc)-b*b*(aa*(dd+bb+2*cc)-zz*zz)
        num=shift(det.num)
        require(num.positive(),'all positive quadrant coefficients, minor '+str(order))
        factors=[]
        for key,power in sorted(det.den.items()):
            quarter=shift(ATOMS[key])
            require(quarter.positive(),'strict positive denominator factor')
            factors.append({'original':encode(ATOMS[key]),'shifted':encode(quarter),'power':power})
        rows.append({'order':order,'original':encode(det.num),'shifted':encode(num),
                     'denominator_factors':factors,'fingerprint':num.fingerprint()})
    # Exact symbolic13 identities in ORIGINAL variables, before shifting.
    S,b,EE,src=base_pairing(q,r,l,fraction=lambda a,b=1:R(a)/b)
    rho=(q-1)/(q+1);ev=[R(1),-rho,R(0)]
    cross=[b[i]+sum(S[i][j]*ev[j] for j in range(3)) for i in range(3)]
    last=m/(3*r*l)-EE+2*sum(ev[i]*b[i] for i in range(3))+sum(ev[i]*S[i][j]*ev[j] for i in range(3) for j in range(3))
    change=[[R(1),3*r,-3*r],[R(-1),l,-l],[R(0),R(0),R(1)]]
    transformed=[[sum(change[a][i]*S[a][b0]*change[b0][j] for a in range(3) for b0 in range(3)) for j in range(3)] for i in range(3)]
    require(transformed==[row[:3] for row in aug[:3]],'all9 exact original-variable arrow identities')
    xc=[sum(change[a][i]*cross[a] for a in range(3)) for i in range(3)]
    require(xc==aug[3][:3] and last==aug[3][3],'all4 exact original-variable augmented identities')
    # Clear each principal prefix separately on the positive quadrant.
    # Positive multipliers only; no oversized full determinant is expanded.
    ATOMS.clear();PROBES.clear();DEN_CACHE.clear()
    u,v,w=R(P({(1,0,0):1})),R(P({(0,1,0):1})),R(P({(0,0,1):1}))
    r,l,q=3+u,2+v,12+4*u+4*v+w
    m=3*r+l;N=2*q+2*m;H=N-1;D=N-7;A=N-q-2
    J=A*(N-4)-3*(q-1)
    for z in (r,l,r-1,l-1,q,q-1,q+1,m,m+1,H,D,q+3,A,J):
        require(z.num.positive(),'positive quadrant atom')
        atom(z.num)
    mat,_=arrow(q,r,l,fraction=lambda a,b=1:R(a)/b)
    for order,row in enumerate(rows,1):
        cleared,domains,removals,constants=clear_rows([v[:order] for v in mat[:order]])
        row['cleared_matrix']=[[encode(p) for p in v] for v in cleared]
        row['positive_row_domains']=[[[encode(ATOMS[k]),e] for k,e in sorted(d.items())] for d in domains]
        row['positive_removed_row_factors']=[[[encode(ATOMS[k]),e] for k,e in sorted(d.items())] for d in removals]
        row['positive_row_constants']=constants
    return {'agent':'six-downset-1','role':'researcher','domain':'r=3+u,l=2+v,q=12+4u+4v+w;u,v,w>=0',
            'rows':rows,'arrow_identity_positions':9,'augmented_identity_positions':4,
            'arithmetic':'exact characteristic-zero integer/Fraction; no modular reconstruction',
            'ordinary_bridge':'complete original-space proof in PROOF.md; unformalized'}
