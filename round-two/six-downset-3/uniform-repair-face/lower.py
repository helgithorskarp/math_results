"""Whole original zero-endpoint lower derivatives, including the kernel gauge.

Only exact integer polynomials and stdlib rational arithmetic are used.
An unsuccessful coefficient sign test is retained as a failed proposal.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import argparse, hashlib, json
import input as inputs
z, r, require = inputs.ipoly, inputs.r, inputs.require
BASE = Path(__file__).resolve().parent
ONE = {(0,0):1}


def record(poly):
    return [[list(power),str(value)] for power,value in sorted(poly.items())]


def matrix_record(G):
    return [[record(poly) for poly in row] for row in G]


def extract(poly, degree):
    require(all(j in (0,1) and value.denominator==1 for (i,j),value in poly.items()),
            'ALL original cleared Gram coefficients integral and affine in kappa')
    return {(i,0):int(value) for (i,j),value in poly.items() if j==degree}


def submatrix(G, rows, cols=None):
    return [[G[i][j] for j in (rows if cols is None else cols)] for i in rows]


def solve_adjugate(B, X):
    """General fraction-free integer-polynomial determinant and full solve."""
    n, m = len(B), len(X[0])
    require(n>0 and all(len(row)==n for row in B) and len(X)==n
            and all(len(row)==m for row in X), 'ENTIRE solve dimensions')
    W=[[dict(poly) for poly in row+cross] for row,cross in zip(B,X)]
    previous=ONE
    for j in range(n-1):
        pivot=W[j][j]
        require(bool(pivot), 'nonzero exact leading polynomial pivot')
        for i in range(j+1,n):
            factor=W[i][j]
            for c in range(j+1,n+m):
                W[i][c]=z.divide(z.add(z.mul(pivot,W[i][c]),
                                      z.scale(z.mul(factor,W[j][c]),-1)),previous)
            W[i][j]={}
        previous=pivot
    det=W[-1][n-1]
    require(bool(det), 'nonzero complete determinant')
    Y=[[{} for _ in range(m)] for _ in range(n)]
    for i in range(n-1,-1,-1):
        for c in range(m):
            residual=z.add(z.mul(det,W[i][n+c]),
                           *(z.scale(z.mul(W[i][j],Y[j][c]),-1) for j in range(i+1,n)))
            Y[i][c]=z.divide(residual,W[i][i])
    # Separate multiplication of every original solve equation.
    require(all(z.add(*(z.mul(B[i][j],Y[j][c]) for j in range(n)))==z.mul(det,X[i][c])
                for i in range(n) for c in range(m)), 'ALL complete original polynomial solve equations')
    return det,Y


def bilinear(G, x, y=None):
    if y is None:y=x
    require(len(x)==len(y)==len(G), 'whole polynomial energy dimensions')
    return z.add(*(z.mul(z.mul(x[i],G[i][j]),y[j])
                   for i in range(len(G)) for j in range(len(G))))


def generated(phase):
    clearing,table,even,standard=inputs.portable_zero.cleared_grams()
    D=extract(clearing,0)
    require(not extract(clearing,1), 'clearing independent of kappa')
    whole=standard if phase=='nu' else even
    G0=[[extract(poly,0) for poly in row] for row in whole]
    G1=[[extract(poly,1) for poly in row] for row in whole]
    keep=list(range(5)) if phase=='nu' else list(range(1,7))
    target=5 if phase=='nu' else 7
    B=submatrix(G0,keep);X=submatrix(G0,keep,[target])
    det,Y=solve_adjugate(B,X)
    v=[{} for _ in G0]
    v[target]=det
    for i,row in zip(keep,Y):v[i]=z.scale(row[0],-1)
    raw_energy=bilinear(G1,v)
    if phase=='nu':
        numerator=raw_energy
        denominator=z.scale(z.mul(D,z.mul(det,det)),2)
        alpha,cross=None,None
    else:
        zz=[ONE,ONE,{},{},{},z.scale(ONE,-1),{},{}]
        require(all(not z.add(*(z.mul(G0[i][j],zz[j]) for j in range(8))) for i in range(8)),
                'ALL whole original zero-kappa kernel equations')
        alpha=bilinear(G1,zz);cross=bilinear(G1,zz,v)
        # alpha/(4D)=q(q+1)/2+3(q+1)/(3q+5), independently derived by counts.
        q={(1,0):1};linear=z.add(z.scale(q,3),{(0,0):5})
        expected=z.add(z.mul(z.mul(q,z.add(q,ONE)),linear),z.scale(z.add(q,ONE),6))
        require(z.scale(z.mul(alpha,linear),2)==z.mul(D,expected),
                'ENTIRE physical kernel orientation identity')
        numerator=z.add(z.mul(alpha,raw_energy),z.scale(z.mul(cross,cross),-1))
        denominator=z.mul(z.mul(q,D),z.mul(alpha,z.mul(det,det)))
    require(all(j==0 and type(value) is int for poly in (numerator,denominator)
                for (i,j),value in poly.items()), 'ENTIRE univariate integer derivative field')
    return {'clearing':D,'zero_Gram':G0,'slope_Gram':G1,'untouched':B,
            'determinant':det,'adjugate_solve':Y,'gauge_fixed_vector_numerator':v,
            'raw_slope_energy':raw_energy,'orientation':alpha,'kernel_cross_energy':cross,
            'numerator':numerator,'denominator':denominator}


def shifted(poly,offset):
    require(all(j==0 for i,j in poly), 'whole univariate shift domain')
    degree=max((i for i,j in poly),default=0)
    dense=[poly.get((j,0),0) for j in range(degree+1)]
    return {(i,0):value for i in range(degree+1)
            if (value:=sum(dense[j]*comb(j,i)*offset**(j-i) for j in range(i,degree+1)))}


def verify(phase):
    data=generated(phase);B=data['untouched'];det=data['determinant']
    # A complete interpolation grid verifies the determinant by two algorithms.
    bound=sum(max((i for poly in row for i,j in poly),default=0) for row in B)
    require(max(i for i,j in det)<=bound, 'full determinant degree bound')
    grid=[]
    for q in range(4,5+bound):
        A=[[z.evaluate(poly,q,0) for poly in row] for row in B]
        value=inputs.portable_zero.det_integer(A)
        require(value==inputs.portable_zero.det_fraction(A)==z.evaluate(det,q,0)>0,
                'ALL grid points: two original determinants, complete positivity')
        grid.append([q,str(value)])
    signs={}
    for offset in (4,21):
        coeff=shifted(z.scale(data['numerator'],-1),offset)
        pos=shifted(data['numerator'],offset)
        negative=[(power,value) for power,value in sorted(coeff.items()) if value<0]
        signs[str(offset)]={'entire_shifted_coefficients':record(coeff),
                            'negative_count':len(negative),
                            'positive_constant':coeff.get((0,0),0)>0,
                            'strict_negative_derivative_proved':not negative and coeff.get((0,0),0)>0,
                            'failed_proposal_is_not_absence':bool(negative),
                            'strict_positive_derivative_proved':bool(pos) and all(v>=0 for v in pos.values())
                                                               and pos.get((0,0),0)>0}
    controls=[]
    for q in (4,5,9,21,27,100):
        D=z.evaluate(data['clearing'],q,0)
        vv=[F(z.evaluate(poly,q,0),z.evaluate(det,q,0)) for poly in data['gauge_fixed_vector_numerator']]
        G0=[[F(z.evaluate(poly,q,0),D) for poly in row] for row in data['zero_Gram']]
        G1=[[F(z.evaluate(poly,q,0),D) for poly in row] for row in data['slope_Gram']]
        if phase=='tau':
            zz=[F(1),F(1),F(0),F(0),F(0),F(-1),F(0),F(0)]
            alpha=r.pair(G1,zz);shift=-r.pair(G1,zz,vv)/alpha
            vv=[a+shift*b for a,b in zip(vv,zz)]
            require(r.pair(G1,zz,vv)==0, 'exact best original trivial gauge control')
        value=r.pair(G1,vv)/(2 if phase=='nu' else q)
        field=F(z.evaluate(data['numerator'],q,0),z.evaluate(data['denominator'],q,0))
        require(value==field, 'whole rational derivative and original energy control')
        zero=r.pair(G0,vv)/(2 if phase=='nu' else q)
        credited=(inputs.coefficient.standard(q,F(0))[0] if phase=='nu'
                  else inputs.coefficient.trivial(q,F(0))[0])
        require(zero==credited, 'ENTIRE original zero scalar control')
        controls.append({'q':q,'derivative':str(value),'zero_coefficient':str(zero),
                         'complete_best_gauge_vector':[str(v) for v in vv]})
    return {'actual_agent':'six-downset-3','role':'researcher','phase':phase,
            'definition':'RIGHT derivative at kappa=0 of the credited full original shorted scalar',
            'all_generated_polynomials':{name:(matrix_record(value) if name in ('zero_Gram','slope_Gram','untouched','adjugate_solve')
                                              else [record(poly) for poly in value] if name=='gauge_fixed_vector_numerator'
                                              else record(value) if value is not None else None)
                                       for name,value in data.items()},
            'complete_determinant_grid':grid,'degree_bound':bound,'signs':signs,'controls':controls,
            'CAS_imported':False,'every_original_solve_coefficient_checked':True,
            'all_real_kappa_dual_slope_proved':False,'independent_review':False,
            'ordinary_envelope_kernel_and_fullspace_bridges_unformalized':True}


def boundary():
    """Prove the sign needed at q>=3k through one univariate boundary."""
    nu,tau=generated('nu'),generated('tau')
    closed=json.loads((inputs.PARENT/'CLOSED-ZERO.json').read_text())
    numer={row['name']:inputs.portable_zero.dense(row['numerator']) for row in closed['rows']}
    denom={row['name']:inputs.portable_zero.dense(row['denominator']) for row in closed['rows']}
    def integer(poly):
        require(all(v.denominator==1 for v in poly.values()), 'ENTIRE closed zero integer coefficients')
        return {power:int(v) for power,v in poly.items()}
    nn,nd,tn,td=(integer(poly) for poly in (numer['nu0'],denom['nu0'],numer['tau0'],denom['tau0']))
    # 2 nu'_0/nu_0^2 + tau'_0/tau_0^2. All denominator factors positive.
    num=z.add(z.scale(z.mul(z.mul(z.mul(nu['numerator'],z.mul(nd,nd)),tau['denominator']),z.mul(tn,tn)),2),
              z.mul(z.mul(z.mul(tau['numerator'],z.mul(td,td)),nu['denominator']),z.mul(nn,nn)))
    den=z.mul(z.mul(nu['denominator'],z.mul(nn,nn)),z.mul(tau['denominator'],z.mul(tn,tn)))
    coeff=shifted(z.scale(num,-1),4)
    negatives=[(power,v) for power,v in sorted(coeff.items()) if v<0]
    proof=not negatives and coeff.get((0,0),0)>0
    if proof:
        require(all(v>=0 for v in shifted(z.scale(nu['numerator'],-1),4).values()),
                'ENTIRE nu negative sign used in boundary extension')
    controls=[]
    for q,k in ((9,3),(21,7),(26,7),(27,7),(32,8),(100,20)):
        nv=F(z.evaluate(nu['numerator'],q,0),z.evaluate(nu['denominator'],q,0))
        tv=F(z.evaluate(tau['numerator'],q,0),z.evaluate(tau['denominator'],q,0))
        n0=F(z.evaluate(nn,q,0),z.evaluate(nd,q,0))
        t0=F(z.evaluate(tn,q,0),z.evaluate(td,q,0))
        value=2*nv/n0**2+tv/t0**2
        require(value==F(z.evaluate(num,q,0),z.evaluate(den,q,0)),
                'whole boundary rational field control')
        a0=inputs.recovery.zero_coefficients(q,k)[0]
        aprime=a0**2/F(q)*(F(q-k,k)*nv/n0**2+tv/t0**2)
        D=r.forms(q,k);C0,_=r.evaluate(D,F(0),F(0),F(0))
        T=[D['keys'].index(key) for key in r.T_KEYS]
        gauge=next(i for i,(core,z0,w0) in enumerate(D['keys']) if core==0 and z0+w0==1)
        O=[i for i in range(len(C0)) if i not in T and i!=gauge]
        anchors=[F(0),F(1),F(1),F(0),F(0)]
        yy=r.solve(r.submatrix(C0,O),r.multiply(r.submatrix(C0,O,T),[[x] for x in anchors]))
        v=[F(0)]*len(C0)
        for i,x in zip(T,anchors):v[i]=x
        for i,row in zip(O,yy):v[i]=-row[0]
        zz=[F(1-int(bool(core&1))-int(bool(core&2))-int(bool(core&4))+int(core.bit_count()>=2))
            for core,z0,w0 in D['keys']]
        alpha=r.pair(D['Delta'],zz);shift=-r.pair(D['Delta'],zz,v)/alpha
        v=[x+shift*y for x,y in zip(v,zz)]
        require(all(r.action(C0,v)[i]==0 for i in O) and r.pair(D['Delta'],zz,v)==0,
                'ALL original lower stationarity and best kernel gauge controls')
        require(r.pair(C0,v)==a0 and r.pair(D['Delta'],v)==aprime,
                'FULL original lower derivative equals separated reciprocal derivative')
        controls.append({'q':q,'k':k,'boundary_expression':str(value),'a0_derivative':str(aprime),
                         'whole_original_vector':[str(x) for x in v]})
    return {'actual_agent':'six-downset-3','role':'researcher',
            'exact_boundary_expression':'2 nu0_prime/nu0^2 + tau0_prime/tau0^2',
            'entire_numerator':record(num),'entire_positive_denominator':record(den),
            'entire_shifted_negative_numerator':record(coeff),'negative_count':len(negatives),
            'positive_constant':coeff.get((0,0),0)>0,'boundary_strict_negative_proved':proof,
            'ordinary_extension':'nu0_prime<0 and (q-k)/k>=2 imply a0_prime<0 on ALL integers q>=3k,k>=1,q>=4',
            'all_original_derivative_controls':controls,
            'independent_review':False,'CAS_imported':False,
            'ordinary_kernel_envelope_and_fullspace_bridge_unformalized':True,
            'joint_cap_derivative_not_proved':True}


def quadrant(poly,k0=7):
    """Complete q=3(k0+x)+u,k=k0+x substitution; coordinates(u,x)."""
    first={}
    for (i,j),value in poly.items():
        for m in range(i+1):
            power=m,i-m+j
            first[power]=first.get(power,0)+value*comb(i,m)*3**(i-m)
    return z.shift_k(z.clean(first),k0)


def boundary_bound():
    result=boundary()
    num={tuple(power):int(value) for power,value in result['entire_numerator']}
    den={tuple(power):int(value) for power,value in result['entire_positive_denominator']}
    margin=z.add(z.scale(z.mul({(5,0):1},num),-2),z.scale(den,-1))
    coeff=shifted(margin,21)
    strict=bool(coeff) and all(v>=0 for v in coeff.values()) and coeff.get((0,0),0)>0
    source=inputs.portable_fields.generated()
    an,ad=({tuple(power):int(value) for power,value in source['a0'][side]}
           for side in ('numerator','denominator'))
    aq=z.add(an,z.scale(z.mul({(1,0):1},ad),-1))
    acoeff=quadrant(aq)
    a_strict=bool(acoeff) and all(v>=0 for v in acoeff.values()) and acoeff.get((0,0),0)>0
    return {'actual_agent':'six-downset-3','role':'researcher',
            'exact_domain':'ALL integers k>=7,q>=3k (thus q>=21)',
            'boundary_expression_numerator':record(num),'boundary_expression_denominator':record(den),
            'entire_margin_polynomial':record(margin),'entire_margin_shift21':record(coeff),
            'margin_negative_count':sum(v<0 for v in coeff.values()),
            'boundary_less_than_minus_one_over_2q5_proved':strict,
            'original_a0_numerator':record(an),'original_a0_denominator':record(ad),
            'entire_a0_minus_q_numerator':record(aq),'entire_a0_minus_q_quadrant':record(acoeff),
            'a0_minus_q_negative_count':sum(v<0 for v in acoeff.values()),
            'a0_greater_than_q_proved':a_strict,
            'lower_derivative_less_than_minus_one_over_2q4_proved':strict and a_strict,
            'ordinary_inference':'a0_prime = a0^2/q * ((q-k)/k * nu0_prime/nu0^2 + tau0_prime/tau0^2)',
            'no_uniform_cap_or_joint_sign_inference':True,'CAS_imported':False,'independent_review':False,
            'ordinary_envelope_gauge_and_fullspace_bridge_unformalized':True}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=('nu','tau','boundary','bound'))
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    result=boundary_bound() if args.phase=='bound' else boundary() if args.phase=='boundary' else verify(args.phase)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'phase':args.phase,'signs':{key:{name:value for name,value in sign.items()
                                                    if name!='entire_shifted_coefficients'}
                                                for key,sign in result.get('signs',{}).items()},
                      'boundary_strict_negative_proved':result.get('boundary_strict_negative_proved'),
                      'negative_count':result.get('negative_count'),
                      'lower_derivative_less_than_minus_one_over_2q4_proved':result.get('lower_derivative_less_than_minus_one_over_2q4_proved'),
                      'new_margin_negative_count':result.get('margin_negative_count'),
                      'a0_minus_q_negative_count':result.get('a0_minus_q_negative_count'),
                      'degree_bound':result.get('degree_bound'),
                      'complete_exact_controls':len(result.get('controls',result.get('all_original_derivative_controls',[])))}))
