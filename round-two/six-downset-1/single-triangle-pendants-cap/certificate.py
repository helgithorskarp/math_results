"""Exact uniform quadrant sign proofs with unchanged resource guards.

The original-space, scalar-inverse and exhaustive-frame implications are
ordinary proofs in PROOF.md. Polynomial identities have full degree-bounded
Gaussian grids. No external mathematical package or private input is used.
"""
from fractions import Fraction as F
from bivariate import P,R,ATOMS,PROBES,DEN_CACHE,atom,value,rational_value
from polynomial import clear_rows,bareiss_minors,identity
from model import parameters,fixed
from exact import require
import signal,time

def component_certificate():
    def alarm(*_):raise TimeoutError('fixed60s single-heavy stage guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    ATOMS.clear();PROBES.clear();DEN_CACHE.clear()
    u=R(P({(1,0):1}));v=R(P({(0,1):1}));l=2+u;q=4*l-4+v
    for z in (l,l-1,l+4,q,q-1,q+1,q+2,q+3,2*q+5+2*l,2*q-1+2*l):atom(z.num)
    p=parameters(q,l,fraction=lambda a,b=1:R(a)/b)
    # Direct exact comparisons at bounded independent rational scalar inputs.
    scalar_controls=0
    for L,Q in ((2,4),(2,5),(3,8),(3,9),(4,16),(5,32)):
        direct=parameters(Q,L)
        for name in ('etaL','etaF','etaP','mu','alpha','beta','nuL','c','d','g','A','Fp'):
            require(rational_value(p[name],(L-2,Q-4*L+4))==direct[name], 'symbolic/scalar value '+name)
            scalar_controls+=1
    norms=[]
    for name in ('etaL','etaF','etaP','mu','alpha','beta','nuL'):
        z=p[name]
        require(z.num.positive(),'positive residual numerator '+name)
        require(all(ATOMS[a].positive() for a in z.den),'positive residual denominators '+name)
        key,unit=atom(z.num);require(unit>0 and ATOMS[key].positive(),'positive norm factor '+name)
        norms.append({'name':name,'terms':len(z.num.a),'degree':z.num.degree(),
                      'polynomial':[[list(ex),str(co)] for ex,co in sorted(z.num.a.items())],
                      'denominator':z.num.den,'fingerprint':z.num.fingerprint()})
    rows=[]
    for name in ('anti','standard'):
        M=p[name];require(M[0][1]==M[1][0],'symmetric Schur form')
        A,domains,removals,constants=clear_rows(M)
        minors=bareiss_minors(A);records=[]
        for order,minor in enumerate(minors,1):
            require(minor.positive(),'positive quadrant cap coefficients '+name+'/'+str(order))
            bounds,count=identity([row[:order] for row in A[:order]],minor)
            records.append({'order':order,'terms':len(minor.a),'degree':minor.degree(),
                            'bounds':bounds,'full_grid_points':count,'fingerprint':minor.fingerprint(),
                            'polynomial':[[list(ex),str(co)] for ex,co in sorted(minor.a.items())],
                            'denominator':minor.den})
        rows.append({'name':name,'minors':records,'positive_row_factors':str(domains),
                     'removed_factors':str(removals),'primitive_multipliers':constants})
    signal.alarm(0)
    data={'agent':'six-downset-1','role':'researcher','domain':'l=2+u,q=4l-4+v,u,v>=0',
          'norms':norms,'cap_component_certificates':rows,'scalar_identity_controls':scalar_controls,
          'proof_status':'exact residual/anti/standard signs; original-space bridge in PROOF.md'}
    return data

def fixed_certificate():
    def alarm(*_):raise TimeoutError('fixed60s fixed8 certificate stage')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    ATOMS.clear();PROBES.clear();DEN_CACHE.clear()
    u=R(P({(1,0):1}));v=R(P({(0,1):1}));l=2+u;q=4*l-4+v
    N=2*q+6+2*l;J=(N-q-2)*(N-4)-3*(q-1)
    for z in (l,l-1,l+4,q,q-1,q+1,q+2,q+3,N-1,N-7,N-1-(q+3),J):atom(z.num)
    S3,S2,p,info=fixed(q,l,fraction=lambda a,b=1:R(a)/b,compute_tau=False)
    norms=[]
    for name in ('mu','alpha','beta','nuL'):
        z=p[name];require(z.num.positive(),'positive norm reused '+name)
        atom(z.num);norms.append({'name':name,'fingerprint':z.num.fingerprint()})
    # First add h-rho*v to the last augmented coordinate. This replaces
    # all inverse pairings there by the simple weight pairings. Then use
    # h-v,3h+lv,G=K-3h-lv for the first3 coordinates. The exact invertible
    # congruence has determinant l+3 and gives an arrow base3 matrix.
    m=l+3;s=q+3;D=N-7;E=N-1;A0=N-q-2;rho=(q-1)/(q+1)
    aa=(m-q*(l+1)/D-2*s/E)/(3*l)
    zz=2*(2*l-1)/(D*E)
    bb=m-m*m*A0/(3*J)-((l+9)*q-m*m)/(3*D)-2*l*s/(3*E)
    cc=-m*(1-(2*l+5)/J)
    dd=2*m+1-((q-1)*(N-10)+3*A0)/J
    arrow=[[aa,zz,R(0)],[zz,bb,cc],[R(0),cc,dd]]
    change=[[R(1),R(3),R(-3)],[R(-1),l,-l],[R(0),R(0),R(1)]]
    transformed=[[sum(change[a][i]*S3[a][b]*change[b][j] for a in range(3) for b in range(3))
                  for j in range(3)] for i in range(3)]
    require(transformed==arrow,'ALL9 exact rational arrow congruence positions')
    cross=[R(F(1,3))+rho/l,1-rho,rho-1]
    aug=[row+[cross[i]] for i,row in enumerate(arrow)]
    aug.append(cross+[info['tau_bound']+R(F(1,3))+rho*rho/l])
    # Positive definite aug4 implies S3>0 and the exact Woodbury inverse
    # scalar tau < (l+3)/(3l), so final2 with that bound is sufficient.
    matrices=[('base-and-inverse-bound',aug),('final-two-update-bound',S2)]
    numeric=0
    for L,Q in ((2,4),(2,5),(3,8),(3,9),(4,16),(5,32),(10,100)):
        base,tail,p0,source=fixed(Q,L,compute_tau=False)
        change0=[[F(1),F(3),F(-3)],[F(-1),F(L),F(-L)],[F(0),F(0),F(1)]]
        arr0=[[sum(change0[a][i]*base[a][b]*change0[b][j] for a in range(3) for b in range(3))
               for j in range(3)] for i in range(3)]
        rho0=F(Q-1,Q+1);cross0=[F(1,3)+rho0/L,1-rho0,rho0-1]
        aug0=[row+[cross0[i]] for i,row in enumerate(arr0)]
        aug0.append(cross0+[source['tau_bound']+F(1,3)+rho0*rho0/L])
        for symbolic,literal in ((aug,aug0),(S2,tail)):
            for row1,row2 in zip(symbolic,literal):
                for a0,b0 in zip(row1,row2):
                    require(rational_value(a0,(L-2,Q-4*L+4))==b0,'every closed Schur scalar matrix identity')
                    numeric+=1
    rows=[]
    for label,M in matrices:
        require(all(M[i][j]==M[j][i] for i in range(len(M)) for j in range(len(M))),'rational sector symmetry')
        A,domains,removals,constants=clear_rows(M)
        minors=bareiss_minors(A);result=[]
        for j,minor in enumerate(minors,1):
            require(minor.positive(),'uniform positive coefficients '+label+'/'+str(j))
            bounds,count=identity([row[:j] for row in A[:j]],minor)
            result.append({'order':j,'terms':len(minor.a),'degree':minor.degree(),
                           'constant':str(value(minor,(0,0))),'bounds':bounds,'identity_grid_points':count,
                           'polynomial':[[list(ex),str(z)] for ex,z in sorted(minor.a.items())],
                           'coefficient_denominator':minor.den,'fingerprint':minor.fingerprint()})
        rows.append({'label':label,'dimension':len(M),'minors':result,
                     'row_factors':str(domains),'removed_positive_factors':str(removals),
                     'primitive_row_multipliers':constants})
    signal.alarm(0)
    data={'agent':'six-downset-1','role':'researcher','domain':'l=2+u,q=4l-4+v,u,v>=0',
          'scalar_inverse_bound':'tau<(l+3)/(3l)','certificate':rows,'numeric_identity_positions':numeric,
          'exact_arrow_congruence_identity_positions':9,
          'norm_factors':norms,'status':'exact fixed8 reduced sign certificate; ordinary original-space bridge separate',
          'term_guard':512,'packing_bytes':32*1024*1024}
    return data
