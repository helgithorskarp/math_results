"""Exact original-variable certificates for the single-pendant uniform domain."""
from fractions import Fraction as F
from math import gcd,lcm,prod
from bivariate import P,R,ATOMS,PROBES,DEN_CACHE,atom,denominator
from model import forms,base_pairing
from exact import require

def shift(p):
    u,v=P({(1,0):1}),P({(0,1):1});substitution=(2+u,8+4*u+v)
    powers={};result=P()
    for ex,co in sorted(p.a.items()):
        term=P(co)
        for j,d in enumerate(ex):
            if (j,d) not in powers:powers[j,d]=substitution[j]**d
            term=term*powers[j,d]
        result=result+term
    return P(result.a,result.den*p.den)

def encode(p):return {'denominator':p.den,'terms':[[list(e),str(c)] for e,c in sorted(p.a.items())]}

def positive_factor(p):
    shifted=shift(p)
    if shifted.positive():return p,shifted,1
    require((-shifted).positive(),'strict coefficientwise denominator orientation')
    return -p,-shifted,-1

def clear_original(matrix):
    # Multiply each ORIGINAL row by a positive-on-domain common denominator,
    # then divide only by exact positive common factors. Shift only afterward.
    positive={}
    for key,p in ATOMS.items():
        s=shift(p)
        if s.positive():positive[key]=(p,s,1)
        elif (-s).positive():positive[key]=(-p,-s,-1)
    rows=[];domains=[];removed=[];constants=[]
    for row in matrix:
        powers={}
        for z in row:
            for key,e in z.den.items():powers[key]=max(powers.get(key,0),e)
        require(all(k in positive for k in powers),'all row denominators positive on stated domain')
        sign=prod(positive[k][2]**e for k,e in powers.items())
        cleared=[sign*z.num*denominator({k:e-z.den.get(k,0) for k,e in powers.items() if e>z.den.get(k,0)}) for z in row]
        removals={}
        for k,(factor,_,_) in positive.items():
            while True:
                quotients=[z.exact_div(factor) for z in cleared]
                if any(z is None for z in quotients):break
                cleared=quotients;removals[k]=removals.get(k,0)+1
        den=1
        for z in cleared:den=lcm(den,z.den)
        content=0
        for z in cleared:
            for v in z.a.values():content=gcd(content,abs(v*(den//z.den)))
        require(content>0,'nonzero row and positive normalization')
        rows.append([P({e:v*(den//z.den)//content for e,v in z.a.items()}) for z in cleared])
        def data(items):
            return [{'original':encode(positive[k][0]),'shifted':encode(positive[k][1]),'power':e} for k,e in sorted(items.items())]
        domains.append(data(powers));removed.append(data(removals));constants.append(str(F(den,content)))
    return rows,domains,removed,constants

def generate():
    ATOMS.clear();PROBES.clear();DEN_CACHE.clear()
    r,q=R(P({(1,0):1})),R(P({(0,1):1}));m=3*r+1;N=2*q+2*m
    H=N-1;D=N-7;s=q+3;A=N-q-2;J=A*(N-4)-3*(q-1)
    for z in (r,r-1,q,q-1,q+1,m,m+1,H,D,s,A,J,H-q-6,H-q-3,H-s):atom(z.num)
    frac=lambda a,b=1:R(a)/b
    f=forms(q,r,1,frac);p=f['p'];rows=[]
    def record(group,k,det,mat):
        numerator=det.num;den=[]
        for key,power in sorted(det.den.items()):
            original,shifted,orientation=positive_factor(ATOMS[key]);numerator=numerator*(orientation**power)
            den.append({'original':encode(original),'shifted':encode(shifted),'power':power})
        shifted=shift(numerator);require(shifted.positive(),'whole positive sign polynomial '+group+'/'+str(k))
        cleared,domains,removals,constants=clear_original(mat)
        rows.append({'group':group,'order':k,'original':encode(numerator),'shifted':encode(shifted),'fingerprint':shifted.fingerprint(),
                     'denominator_factors':den,'cleared_original_matrix':[[encode(z) for z in v] for v in cleared],
                     'positive_row_domains':domains,'positive_removed_row_factors':removals,'positive_row_constants':constants})
    for name in ('mu','alpha','beta','etaP','nuT'):record(name,1,p[name],[[p[name]]])
    for name in ('anti','triangle','final'):
        a=f[name];record(name,1,a[0][0],[a[0][:1]])
        record(name,2,a[0][0]*a[1][1]-a[0][1]*a[1][0],a)
    a=f['augmented'];aa,z,b,c,d,x,y,e=a[0][0],a[0][1],a[1][1],a[1][2],a[2][2],a[0][3],a[1][3],a[3][3]
    sub=b*d-c*c;d3=aa*sub-z*z*d
    determinants=(aa,aa*b-z*z,d3,e*d3-x*x*sub+2*x*y*z*(d+c)-y*y*(aa*(d+b+2*c)-z*z))
    for order,det in enumerate(determinants,1):record('augmented',order,det,[v[:order] for v in a[:order]])
    # All13 complete original-field base arrow/inverse positions.
    S,b,EE,src=base_pairing(q,r,1,frac);rho=(q-1)/(q+1);ev=[R(1),-rho,R(0)]
    cross=[b[i]+sum(S[i][j]*ev[j] for j in range(3)) for i in range(3)]
    last=m/(3*r)-EE+2*sum(ev[i]*b[i] for i in range(3))+sum(ev[i]*S[i][j]*ev[j] for i in range(3) for j in range(3))
    change=[[R(1),3*r,-3*r],[R(-1),R(1),R(-1)],[R(0),R(0),R(1)]]
    transformed=[[sum(change[i][a0]*S[i][j]*change[j][b0] for i in range(3) for j in range(3)) for b0 in range(3)] for a0 in range(3)]
    require(transformed==[row[:3] for row in a[:3]],'all9 original-field arrow positions')
    xc=[sum(change[i][j]*cross[i] for i in range(3)) for j in range(3)]
    require(xc==a[3][:3] and last==a[3][3],'all4 original-field augmented positions')
    mu=(q-3*p['common']-p['d']**2*q/9-p['d']*p['g']*rho*p['w']/r-2*s*p['c']**2*(r-1)/(3*r*r))/3
    eta=p['w']-p['common']-p['g']**2*(p['w']+q/(3*r*rho*rho))-2*s*p['c']**2/(3*r)
    X=p['A']**2*p['E2']+p['ast']**2*p['Di2'];Y=p['d']**2*(p['E2']+p['Di2']);Z=p['A']*p['d']*p['E2']+p['ast']*p['d']*p['Di2']
    alpha=2*s-4*X+2*Z+2*Y-8*s*p['c']**2/3+4*s*p['c']**2*(r-1)/(3*r*r)
    beta=2*s/3-8*p['d']**2*q/27+p['d']*p['g']*rho*p['w']/(3*r)-p['d']**2*rho*rho*p['w']-4*s*p['c']**2*(r-1)/(9*r*r)
    require((mu,eta,alpha,beta)==tuple(p[k] for k in ('mu','etaP','alpha','beta')),'all4 exact residual cancellation identities')
    require(p['etaL']==mu+(alpha+beta)/4 and p['etaF']==mu+beta,'both residual diagonal identities')
    return {'agent':'six-downset-1','role':'researcher','domain':'r=2+u,q=8+4u+v;u,v>=0;single pendant',
            'rows':rows,'arrow_identity_positions':9,'augmented_identity_positions':4,'residual_identity_positions':6,
            'arithmetic':'exact characteristic-zero integer/Fraction; modular probes only reject candidate factors; every accepted division exact',
            'ordinary_bridge':'complete original-space/rank/repair proof; unformalized'}
