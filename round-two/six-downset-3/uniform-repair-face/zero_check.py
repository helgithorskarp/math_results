"""Stdlib exact binding and bounded original controls for the new rank-one dual.

The seven-deletion baseline is credited; controls are not all-count signs.
No solver or CAS is imported. Failed signs are saved as failed proposals.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, json
import input as inputs
r, require = inputs.r, inputs.require
p = r.poly
ip = inputs.portable_fields.f.cap.c.r.poly
BASE = Path(__file__).resolve().parent
import zero_generator


def decode(rows):
    out={}
    for power,value in rows:
        key=tuple(power); number=F(value)
        require(len(key)==2 and min(key)>=0 and all(type(x) is int for x in key)
                and key not in out and number.denominator==1, 'complete integral polynomial encoding')
        if number: out[key]=int(number)
    return out


def matrix_decode(G): return [[decode(v) for v in row] for row in G]
def record(v): return [[list(power),str(value)] for power,value in sorted(v.items())]
def digest(v): return hashlib.sha256(json.dumps(v,separators=(',',':'),sort_keys=True).encode()).hexdigest()


def integer_tools():
    import ipoly
    return ipoly


def polynomial_det(G):
    z=integer_tools()
    if len(G)==1: return G[0][0]
    return z.add(*(z.scale(z.mul(G[0][j],polynomial_det([row[:j]+row[j+1:] for row in G[1:]])),(-1)**j)
                   for j in range(len(G))))


def bind():
    z=integer_tools(); data=zero_generator.generated()
    raw=inputs.portable_frame.generated() | inputs.portable_fields.generated()
    frame=inputs.portable_frame.verify(raw); fields=inputs.portable_fields.fields(raw)
    d=decode(raw['complete_seven_determinant']); H=matrix_decode(raw['complete_four_short_numerator'])
    g=decode(data['short_common_factor']); dc=decode(data['reduced_seven_determinant'])
    HH=matrix_decode(data['complete_reduced_four_short'])
    require(z.mul(g,dc)==d and all(z.mul(g,HH[i][j])==H[i][j] for i in range(4) for j in range(4)),
            'ALL compact whole polynomial shorting divisions multiplied back')
    W=matrix_decode(data['complete_border_minors'])
    require(all(z.mul(dc,W[i][j])==z.add(z.mul(HH[i][j],HH[3][3]),z.scale(z.mul(HH[i][3],HH[j][3]),-1))
                for i in range(3) for j in range(3)), 'ALL whole target-border Jacobi divisions')
    Q,K={(1,0):1},{(0,1):1}
    nn,nd=(decode(raw['nu_U'][side]) for side in ('numerator','denominator'))
    an,ad=(decode(raw['a0'][side]) for side in ('numerator','denominator'))
    require(decode(data['lower_numerator'])==an and decode(data['lower_denominator'])==ad,
            'ALL complete regenerated original lower field coefficients')
    T=z.add(z.scale(z.mul(z.mul(z.mul(Q,dc),K),nn),4),z.mul(z.mul(z.add(Q,z.scale(K,-1)),HH[3][3]),nd))
    P=[[z.add(z.scale(z.mul(z.mul(z.mul(Q,K),nn),HH[i][j]),4),
             z.mul(z.mul(z.add(Q,z.scale(K,-1)),nd),W[i][j])) for j in range(3)] for i in range(3)]
    require(decode(data['cap_target'])==T and matrix_decode(data['complete_zero_cap_numerator'])==P,
            'ALL9 entire rational zero cap polynomials regenerated')
    PH=z.divide(z.add(z.mul(P[0][0],P[2][2]),z.scale(z.mul(P[0][2],P[0][2]),-1)),T)
    adj=[[z.scale(polynomial_det([[P[ii][jj] for jj in range(3) if jj!=i]
                                  for ii in range(3) if ii!=j]),(-1)**(i+j))
          for j in range(3)] for i in range(3)]
    ss=(-1,1,1)
    Aq=z.divide(z.add(*(z.scale(adj[i][j],ss[i]*ss[j]) for i in range(3) for j in range(3))),T)
    dp=z.divide(polynomial_det(P),z.mul(T,T))
    num=z.add(z.mul(ad,dp),z.scale(z.mul(an,Aq),4))
    den=z.add(z.mul(ad,PH),z.scale(z.mul(an,z.add(P[0][0],P[2][2],z.scale(P[0][2],2))),4))
    require(num==decode(data['joint_numerator_before_gcd']) and den==decode(data['joint_denominator_before_gcd']),
            'ALL complete rank-one optimized original residual coefficients')
    gg=decode(data['joint_gcd']); n=decode(data['joint_residual_numerator']); dd=decode(data['joint_residual_denominator'])
    twoN=z.add(z.mul(Q,Q),z.scale(Q,13),{(0,0):16},z.scale(K,-2))
    require(gg==z.mul(Q,z.mul(twoN,twoN)), 'ENTIRE compact cancellation factor q(2N)^2')
    # Discovery normalizes the compact denominator at q27,k7; no sign is inferred.
    flip=1 if z.evaluate(den,27,7)>0 else -1
    require(z.mul(gg,n)==z.scale(num,flip) and z.mul(gg,dd)==z.scale(den,4*flip),
            'ALL compact residual gcd divisions multiplied back')
    hx=z.scale(z.add(z.mul(ad,z.divide(z.add(z.mul(P[2][2],P[0][1]),z.scale(z.mul(P[0][2],P[1][2]),-1)),T)),
                    z.scale(z.mul(an,z.add(z.scale(P[2][2],-1),P[0][1],z.scale(P[0][2],-1),P[1][2])),4)),-1)
    hz=z.scale(z.add(z.mul(ad,z.divide(z.add(z.mul(P[0][0],P[1][2]),z.scale(z.mul(P[0][2],P[0][1]),-1)),T)),
                    z.scale(z.mul(an,z.add(P[0][0],P[1][2],P[0][2],P[0][1])),4)),-1)
    require(hx==decode(data['optimizer_a_numerator']) and hz==decode(data['optimizer_abac_numerator']) and
            den==decode(data['optimizer_common_denominator']), 'ALL optimizer polynomial coefficients')
    return {'actual_agent':'six-downset-3','role':'researcher','entire_new_coefficients_bound':True,
            'complete_28_original_solve_equations_checked':frame['complete_solve_coefficient_identity'],
            'complete_16_original_short_equations_checked':frame['complete_Schur_coefficient_identity'],
            'complete_original_determinant_grid_count':frame['full_exact_grid_count'],
            'complete_original_scalar_field_binding':fields['whole_nu_U_coefficient_identity'] and fields['whole_a0_coefficient_identity'],
            'new_residual_numerator_count':len(n),'new_residual_denominator_count':len(dd),
            'new_optimizer_counts':[len(hx),len(hz)],
            'complete_residual_polynomials_sha256':[digest(record(n)),digest(record(dd))],
            'compact_gcd_is_q_times_4N_squared':True,
            'CAS_not_imported':True,'uniform_signs_proved':False,
            'original_kappa_slope_uniformly_proved':False,'independent_review':False,
            'ordinary_fullspace_bridges_unformalized':True}


def minimize(A, support, anchors, excluded=()):
    O=[i for i in range(len(A)) if i not in support and i not in excluded]
    Y=r.solve(r.submatrix(A,O),r.multiply(r.submatrix(A,O,support),[[x] for x in anchors]))
    x=[F(0)]*len(A)
    for i,value in zip(support,anchors): x[i]=F(value)
    for i,row in zip(O,Y): x[i]=-row[0]
    require(all(r.action(A,x)[i]==0 for i in O), 'ALL original untouched stationarity equations')
    return x


def control(q,k):
    data=zero_generator.generated();z=integer_tools()
    M,receipt=inputs.cap.reduced(q,k)
    require(M==inputs.cap.direct(q,k), 'ALL9 direct original23 unrepaired cap positions')
    T=z.evaluate(decode(data['cap_target']),q,k)
    require(T>0 and [[F(z.evaluate(v,q,k),4*T) for v in row] for row in matrix_decode(data['complete_zero_cap_numerator'])]==M,
            'ALL9 bound original23 polynomial cap positions')
    a,_,_=inputs.recovery.zero_coefficients(q,k);b=r.odd_coefficient(q)
    require(inputs.coefficient.direct(q,k,F(0))==a, 'complete original zero lower coefficient')
    H=r.submatrix(M,[0,2]);u=[M[0][1],M[2][1]];w=[F(-1),F(1)]
    require(r.schur_psd(H)==2 and r.polynomial_psd(H)[0]==2, 'whole fixed-order H control positive')
    K=[[H[i][j]+a*w[i]*w[j] for j in range(2)] for i in range(2)]
    y=[u[i]+a*w[i] for i in range(2)]
    h=[-row[0] for row in r.solve(K,[[v] for v in y])]
    R=M[1][1]+a+sum(y[i]*h[i] for i in range(2))
    den=z.evaluate(decode(data['joint_residual_denominator']),q,k)
    require(den!=0 and F(z.evaluate(decode(data['joint_residual_numerator']),q,k),den)==R,
            'ENTIRE original optimized joint residual normalization')
    hd=z.evaluate(decode(data['optimizer_common_denominator']),q,k)
    require([F(z.evaluate(decode(data[name]),q,k),hd) for name in ('optimizer_a_numerator','optimizer_abac_numerator')]==h,
            'BOTH whole original optimizer coordinates')
    ell=sum(w[i]*h[i] for i in range(2)); t=a*(1+ell)/2
    Hi_u=[row[0] for row in r.solve(H,[[v] for v in u])]
    Hi_w=[row[0] for row in r.solve(H,[[v] for v in w])]
    c0=(M[1][1]-sum(u[i]*Hi_u[i] for i in range(2)))/2
    c1=2-2*sum(w[i]*Hi_u[i] for i in range(2))
    c2=-2*sum(w[i]*Hi_w[i] for i in range(2))-2/a
    require(c2<0 and t==-c1/(2*c2) and R==2*(c0-c1*c1/(4*c2)),
            'ENTIRE rank-one and optimized concave-quadratic identities')
    D=r.forms(q,k);C0,U0=r.evaluate(D,F(0),F(0),F(0));Tix=[D['keys'].index(key) for key in r.T_KEYS]
    gauge=next(i for i,(core,z0,w0) in enumerate(D['keys']) if core==0 and z0+w0==1)
    low=minimize(C0,Tix[1:],[1,1,ell,ell],[Tix[0],gauge])
    zeta=[F(1-int(bool(core&1))-int(bool(core&2))-int(bool(core&4))+int(core.bit_count()>=2)) for core,_,_ in D['keys']]
    require(not any(r.action(C0,zeta)) and all(r.pair(D[n],zeta)==0 for n in ('Rb','Rc','B')),
            'full original lower gauge kernel and repair independence')
    orientation=r.pair(D['Delta'],zeta)
    require(orientation>0, 'original orientation control')
    shift=-r.pair(D['Delta'],zeta,low)/orientation
    low=[x+shift*y for x,y in zip(low,zeta)]
    require(r.pair(D['Delta'],zeta,low)==0, 'complete original best gauge derivative equation')
    upper=minimize(U0,Tix,[h[0],1,1,h[1],h[1]])
    lowplane=[r.pair(C0,low),r.pair(D['Delta'],low),r.pair(D['Rb'],low),r.pair(D['Rc'],low),r.pair(D['B'],low)]
    capplane=[r.pair(U0,upper),-r.pair(D['Delta'],upper),-r.pair(D['Rb'],upper),-r.pair(D['Rc'],upper),-r.pair(D['B'],upper)]
    combined=[x+y for x,y in zip(lowplane,capplane)]
    require(combined[0]==R and combined[2:]==[F(0)]*3,
            'ALL original constant, independent tb, independent tc, and sigma joint dual coefficients')
    half_t=a/2;half_sigma=-a/2+F(1,4)
    half=inputs.cap.direct(q,k,half_t,half_sigma)
    half_lower=r.lower_cone(a,b,half_t,half_sigma)
    half_cross=[half[0][1],half[2][1]]
    half_minimum=half[1][1]-sum(x*row[0] for x,row in zip(half_cross,r.solve(H,[[v] for v in half_cross])))
    wHiw=sum(w[i]*Hi_w[i] for i in range(2))
    require(half_minimum==R-a*ell*ell*(1+a*wHiw)-F(1,2),
            'ENTIRE half-coefficient repair loss identity in original cap normalization')
    half_cap_positive=half_minimum>0
    if half_cap_positive:
        require(r.schur_psd(half)==3 and r.polynomial_psd(half)[0]==3,
                'two complete exact PSD algorithms confirm positive half-repair control')
    return {'q':q,'k':k,'a0':a,'b':b,'H':H,'H_positive_both_algorithms':True,
            'optimized_joint_residual':R,'maximum_compatibility_gap':R/2,'quadratic':[c0,c1,c2],
            'optimizer':h,'lower_anchor_ell':ell,'optimum_t':t,
            'vertex_in_strict_lower_interval':0<t<2*a*b/(a+b),
            'original_lower_vector':low,'original_cap_vector':upper,
            'original_gauge_orientation':orientation,'original_best_gauge_shift':shift,
            'original_lower_plane':lowplane,'original_cap_plane':capplane,
            'combined_original_dual_coefficients':combined,
            'all_real_dual_absence_control':R<0 and combined[1]<=0,
            'kappa_slope_uniform_claim':False,
            'half_coefficient_repair':{'t':half_t,'sigma':half_sigma,'lower_strict':half_lower,'even_cap_positive':half_cap_positive,
                                      'exact_even_cap_residual':half_minimum,'whole_rank_one_loss_identity':True},
            'full_polynomial_and_original_binding_control':True,'not_a_uniform_sign_proof':True}


def verify_original_plane(row):
    q,k=row['q'],row['k'];D=r.forms(q,k);C0,U0=r.evaluate(D,F(0),F(0),F(0))
    T=[D['keys'].index(key) for key in r.T_KEYS];O=[i for i in range(len(D['keys'])) if i not in T]
    a=inputs.recovery.zero_coefficients(q,k)[0]
    low=[F(x) for x in row['original_lower_vector']];upper=[F(x) for x in row['original_cap_vector']]
    h=[F(x) for x in row['optimizer']];ell=F(row['lower_anchor_ell'])
    require(len(low)==len(upper)==len(D['keys']) and ell==h[1]-h[0], 'whole original plane vector dimensions and shared trade restriction')
    require([low[i] for i in T]==[F(0),F(1),F(1),ell,ell] and
            [upper[i] for i in T]==[h[0],F(1),F(1),h[1],h[1]], 'ALL original prescribed plane anchors')
    require(all(r.action(C0,low)[i]==0 and r.action(U0,upper)[i]==0 for i in O),
            'ALL complete original stationarity equations of both planes')
    zeta=[F(1-int(bool(core&1))-int(bool(core&2))-int(bool(core&4))+int(core.bit_count()>=2)) for core,_,_ in D['keys']]
    require(r.pair(D['Delta'],zeta)>0 and F(row['original_gauge_orientation'])==r.pair(D['Delta'],zeta),
            'actual original orientation')
    require(r.pair(D['Delta'],zeta,low)==0, 'actual best original lower gauge derivative')
    lp=[r.pair(C0,low),r.pair(D['Delta'],low),r.pair(D['Rb'],low),r.pair(D['Rc'],low),r.pair(D['B'],low)]
    cp=[r.pair(U0,upper),-r.pair(D['Delta'],upper),-r.pair(D['Rb'],upper),-r.pair(D['Rc'],upper),-r.pair(D['B'],upper)]
    total=[x+y for x,y in zip(lp,cp)]
    require(lp==[F(x) for x in row['original_lower_plane']] and cp==[F(x) for x in row['original_cap_plane']] and
            total==[F(x) for x in row['combined_original_dual_coefficients']] and total[2:]==[F(0)]*3,
            'ALL original energies and individually cancelled tb,tc,sigma coefficients')
    M=inputs.cap.direct(q,k);H=r.submatrix(M,[0,2]);u=[M[0][1],M[2][1]];w=[F(-1),F(1)]
    K=[[H[i][j]+a*w[i]*w[j] for j in range(2)] for i in range(2)]
    y=[u[i]+a*w[i] for i in range(2)]
    require([row0[0] for row0 in r.solve(K,[[-x] for x in y])]==h, 'ENTIRE two-dimensional optimizer equation')
    R=M[1][1]+a+sum(x*v for x,v in zip(y,h))
    require(R==total[0]==F(row['optimized_joint_residual']) and
            row['all_real_dual_absence_control']==(R<0 and total[1]<=0), 'whole original optimized constant and precise absence flag')
    return True


def damage():
    import copy
    row=control(32,8);require(verify_original_plane(row), 'complete new original32,8 dual baseline')
    cases=[]
    def reject(name,change):
        mutated=copy.deepcopy(row);change(mutated)
        try: verify_original_plane(mutated)
        except (ValueError,KeyError,TypeError,IndexError): cases.append(name);return
        raise ValueError('accepted damaged original certificate: '+name)
    reject('changed original cap coordinate',lambda x:x['original_cap_vector'].__setitem__(0,F(x['original_cap_vector'][0])+1))
    reject('changed lower gauge coordinate',lambda x:x['original_lower_vector'].__setitem__(0,F(x['original_lower_vector'][0])+1))
    reject('changed original constant',lambda x:x.__setitem__('optimized_joint_residual',F(x['optimized_joint_residual'])+1))
    reject('false kappa slope',lambda x:x['combined_original_dual_coefficients'].__setitem__(1,F(1)))
    def trade_decoy(x):
        x['original_lower_plane'][2]+=1;x['original_lower_plane'][3]-=1
    reject('trade-sum preserving corruption of separate tb and tc',trade_decoy)
    reject('uncancelled bc repair',lambda x:x['combined_original_dual_coefficients'].__setitem__(4,F(1)))
    reject('wrong original orientation',lambda x:x.__setitem__('original_gauge_orientation',F(-1)))
    reject('false absence flag',lambda x:x.__setitem__('all_real_dual_absence_control',False))
    return {'actual_agent':'six-downset-3','role':'researcher','entire_original32_8_control_verified':True,
            'semantic_damage_count':len(cases),'all_semantic_damages_rejected':cases,
            'independent_person_review':False,'finite_certificate_scope_only':True}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['bind','controls','damage']);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    value=bind() if args.phase=='bind' else damage() if args.phase=='damage' else {'actual_agent':'six-downset-3','role':'researcher',
        'controls':[control(q,k) for q,k in ((21,7),(26,7),(27,7),(32,8),(100,20))],
        'control_scope':'five exact original controls only; not a classification or all-count sign proof'}
    args.out.write_text(json.dumps(r.encode(value),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'phase':args.phase,'complete':True,'out_bytes':args.out.stat().st_size}))
