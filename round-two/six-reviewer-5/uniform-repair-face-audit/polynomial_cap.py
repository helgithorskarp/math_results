"""Common-denominator QQ[q,k] cap vectors/energies; no repeated field gcds.

Every polynomial division is multiplied back. Stored original solve
stages are reviewer-generated, never producer certificates.
"""
import sys
import original_field as O
from stages import load
q,k=O.q,O.k;RP=q.numer.ring;Q,K=RP.gens
P=4*Q*(Q-1)*(Q-2)*(Q-3)*(3*Q+5)

def degree(poly):return max((sum(e) for e in poly),default=-1)
def exquo(a,b):
    c=a.exquo(b);O.require(c*b==a,'entire exact polynomial division');return c

def clear(M):
    dens=[];seen=set()
    for row in M:
        for x in row:
            key=str(x.denom)
            if key not in seen:seen.add(key);dens.append(x.denom)
    den=RP.one
    for d in dens:den=den.lcm(d)
    V=[[x.numer*exquo(den,x.denom) for x in row] for row in M]
    return den,V

def fieldpoly(v):
    if isinstance(v,dict):return {a:fieldpoly(b) for a,b in v.items()}
    if isinstance(v,list):return [fieldpoly(x) for x in v]
    O.require(all(e==(0,0) for e in v.denom),'stored polynomial has constant denominator')
    result=v.numer.quo_ground(v.denom[(0,0)])
    O.require(result*v.denom==v.numer,'all polynomial rational coefficients exact')
    return result

def cleared_delta(A):
    out=[]
    for row in A:
        rr=[]
        for a in row:
            n=a.numer*P;rr.append(exquo(n,a.denom))
        out.append(rr)
    return out

def energies(D,V):
    r=len(V[0]);n=len(D)
    # First matrix-times-vectors, then dot products, all in QQ[q,k].
    W=[[sum((D[i][j]*V[j][a] for j in range(n) if D[i][j] and V[j][a]),RP.zero) for a in range(r)] for i in range(n)]
    out=[[sum((V[i][a]*W[i][b] for i in range(n) if V[i][a] and W[i][b]),RP.zero) for b in range(r)] for a in range(r)]
    O.require(all(out[i][j]==out[j][i] for i in range(r) for j in range(r)), 'whole polynomial energy symmetric')
    return out

def vectors():
    std=load('standard-stage');tri=load('trivial-stage')
    T,H=clear(tri['H4']);D,V4=clear(tri['V4'])
    print('cleared H4/V4',degree(T),degree(D),flush=True)
    nu=std['nu'];r=Q-K
    C=H[3][3]*nu.denom*r+K*Q*nu.numer*T
    B=[-H[3][i]*nu.denom*r for i in range(3)]
    den=D*C
    V=[[row[i]*C+row[3]*B[i] for i in range(3)] for row in V4]
    common=den
    for row in V:
        for v in row:
            if v:common=common.gcd(v)
    rawden=den;den=exquo(den,common);V=[[exquo(v,common) for v in row] for row in V]
    ds,Vs=clear(std['V'])
    O.write('cap-vector-polynomials',dict(denominator=den,V=V,standard_denominator=ds,standard_V=Vs,
        H4_denominator=T,H4=H,removed_common_factor=common,raw_vector_denominator=rawden))
    print('polynomial vectors saved; degrees',degree(den),degree(ds),'coordinates',sum(bool(v) for row in V for v in row),flush=True)

def derivative():
    vec=fieldpoly(load('cap-vector-polynomials'));std=load('standard-stage');tri=load('trivial-stage')
    dt,ds=vec['denominator'],vec['standard_denominator'];V,Vs=vec['V'],vec['standard_V']
    Es=energies(cleared_delta(std['Delta']),Vs)[0][0]
    O.require(Es*std['Delta_energy'].denom==2*P*ds**2*std['Delta_energy'].numer,'complete standard polynomial energy binding')
    Dt=cleared_delta(tri['Delta']);diff=[row[1]-row[2] for row in V]
    O.require(all(sum((Dt[i][j]*diff[j] for j in range(11)),RP.zero)==0 for i in range(11)), 'WHOLE trivial cap derivative kernel map')
    O.require(V[10][1]==V[10][2],'WHOLE standard deletion correction null direction')
    two=energies(Dt,[row[:2] for row in V])
    Et=[[two[min(i,1)][min(j,1)] for j in range(3)] for i in range(3)]
    r=Q-K
    cap=[[2*r*ds**2*Et[i][j]+K*Q*V[10][i]*V[10][j]*Es for j in range(3)] for i in range(3)]
    den=2*P*r*dt**2*ds**2
    O.require(all(cap[i][1]==cap[i][2] for i in range(3)) and all(cap[1][j]==cap[2][j] for j in range(3)), 'WHOLE cap derivative null direction')
    O.write('cap-derivative-polynomials',dict(numerator=cap,denominator=den,trivial_energy=Et,standard_energy=Es))
    print('original complete cap derivative saved; numerator degrees',[[degree(v) for v in row] for row in cap],'denominator',degree(den),flush=True)

def psi():
    cap=fieldpoly(load('cap-derivative-polynomials'));num=cap['numerator'];den=cap['denominator']
    A=2*Q**4*num[0][0]+den;B=2*Q**4*num[0][1]-den;C=2*Q**4*num[1][1]+den
    common=A.gcd(B).gcd(C)
    AA,BB,CC=(exquo(v,common) for v in (A,B,C))
    determinant=AA*CC-BB**2
    O.write('psi-polynomials',dict(raw_leading=A,raw_cross=B,raw_other=C,denominator=2*Q**4*den,
            common_factor=common,reduced_leading=AA,reduced_cross=BB,reduced_other=CC,reduced_determinant=determinant))
    print('Psi full leading degree',degree(A),'determinant degree',degree(determinant),'removed square-factor degree',degree(common),flush=True)

def cap_short():
    vec=fieldpoly(load('cap-vector-polynomials'));std=load('standard-stage')
    H=vec['H4'];T=vec['H4_denominator'];nu=std['nu'];r=Q-K
    C=H[3][3]*nu.denom*r+K*Q*nu.numer*T
    B=[-H[3][i]*nu.denom*r for i in range(3)]
    num=[[H[i][j]*C+H[i][3]*B[j] for j in range(3)] for i in range(3)];den=T*C
    common=den
    for row in num:
        for v in row:
            if v:common=common.gcd(v)
    rawden=den;den=exquo(den,common);num=[[exquo(v,common) for v in row] for row in num]
    O.require(all(num[i][j]==num[j][i] for i in range(3) for j in range(3)), 'ENTIRE original cap short symmetry')
    O.write('cap-short-polynomials',dict(numerator=num,denominator=den,removed_common_factor=common,raw_denominator=rawden))
    print('complete original M0 degrees',[[degree(v) for v in row] for row in num],degree(den),flush=True)

if __name__=='__main__':{'vectors':vectors,'derivative':derivative,'psi':psi,'short':cap_short}[sys.argv[1]]()
