"""Fresh independent third-boundary algebra. Written formulas exposed, not blind.

No author executable, arithmetic, EXPECTED record or controls is opened/imported.
Our own previously published Fraction cubic/Gaussian and row routines are reused.
All new Newton/anchor, order-four recursion, scalar and tangent work is here.
"""
from pathlib import Path
from fractions import Fraction as Q
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from exact import C,F,Z,Poly,need
from retained import constants,eval_z,derivative_z
from stationary import derive_stationary,fixed_jet


def trunc(p,n=4):
    return Poly(p.n,{k:v for k,v in p.d.items() if k[0]<=n})


def s_power(p,e,n=4):
    need(p.d.get((0,),F(0))==1,'Constant-one scalar series')
    t=Poly.const(1,1);out=t;q=Q(1)
    for k in range(1,n+1):
        t=trunc(t*(p-1),n);q=q*(e-k+1)/k;out=out+t*q
    return trunc(out,n)


def columns(p,order):
    return [{j:p.d.get((r,j),F(0)) for j in range(10)} for r in range(order+1)]


def formal_newton(damage=None):
    # ETA followed by TEN independent real parameters; no producer jet is read.
    names=['U0','H','W','D','J21','J4','U3','J22','J41','J6']
    eta=Poly.var(11,0);v=[Poly.var(11,i+1) for i in range(10)]
    U0,H,W,D,J21,J4,U3,J22,J41,J6=v
    powers=[None,U0*eta+W*eta**2,-H*eta+D*eta**2,
            -3*J21*eta**2+U3*eta**3,J4*eta**2-6*J22*eta**3,
            5*J41*eta**3,-J6*eta**3,Poly.const(11,0),Poly.const(11,0)]
    if damage=='newton':powers[4]=J4*eta**2-5*J22*eta**3
    elementary=[Poly.const(11,1)]
    for m in range(1,9):
        value=Poly.const(11,0)
        for i in range(1,m+1):value=value+trunc(elementary[m-i]*powers[i],3)*((-1)**(i-1))
        elementary.append(value/m)
    # Integrate derivative coefficient by coefficient; retain all TEN z columns.
    primitive={9-m:elementary[m]*(9*Q((-1)**m,9-m)) for m in range(9)}
    anchor=Poly.const(11,0)
    for j,p in primitive.items():anchor=anchor+trunc(p*(1-eta)**j,3)
    primitive[0]=-anchor
    output={}
    for r in range(4):
        output[r]={}
        for j in range(10):
            p=primitive.get(j,Poly.const(11,0))
            output[r][j]=Poly(10,{k[1:]:a for k,a in p.d.items() if k[0]==r})
    need(all(output[0][j].same(1 if j==9 else -1 if j==0 else 0) for j in range(10)),'All base columns')
    # Independent direct known order-one/two map, still all parameters moving.
    def const(a):return Poly.const(10,a)
    u,h,w,d,j21,j4=[Poly.var(10,i) for i in range(6)]
    first={8:-9*u/8,7:9*h/14}
    first[0]=const(9)+9*u/8-9*h/14
    second={8:-9*w/8,7:9*(u*u-d)/14,
            6:-3*u*h/4+3*j21/2,5:9*h*h/40-9*j4/20}
    second[0]=const(-36)-9*u+9*h/2-sum(second.values(),const(0))
    need(all(output[1][j].same(first.get(j,0)) for j in range(10)),'Entire moving first Newton jet')
    need(all(output[2][j].same(second.get(j,0)) for j in range(10)),'Entire moving second Newton jet')
    return names,output


def root_jets(cols,order=4):
    """Fresh implicit recursion by series composition, for ALL nine labels."""
    omega=Z(2*C*C-1,2*C)
    need(omega**9==1 and omega!=1,'Physical ninth roots')
    def mul(a,b,n):
        out=[Z(0) for _ in range(n+1)]
        for i,x in enumerate(a):
            for j,y in enumerate(b):
                if i+j<=n:out[i+j]=out[i+j]+x*y
        return out
    def equation(r,n):
        powers=[[Z(1)]+[Z(0) for _ in range(n)]]
        for j in range(1,10):powers.append(mul(powers[-1],r,n))
        value=Z(0)
        for k in range(n+1):
            for j,a in cols[k].items():
                if a!=0:value=value+Z(a)*powers[j][n-k]
        return value
    records=[];arrays=[]
    for j in range(9):
        w=omega**j;r=[w]
        need(eval_z(cols[0],w)==0,'Every original base root equation')
        for n in range(1,order+1):
            r.append(Z(0));r[n]=-equation(r,n)/(9*w**8)
            need(equation(r,n)==0,'Every original-root coefficient equation')
        normals=[]
        for n in range(1,order+1):
            a=sum((r[i]*r[n-i].conjugate() for i in range(n+1)),Z(0))/2
            need(a.t==0,'Every radial coefficient real')
            normals.append(a.r)
        records.append(dict(j=j,root_series=[a.serial() for a in r],half_normals=[a.serial() for a in normals]))
        arrays.append(r)
    need(all(arrays[9-j][n]==arrays[j][n].conjugate() for j in range(1,5) for n in range(order+1)),'All reflected root jets')
    return records,arrays


def defining_primitive(K,J,m=0,g=0,fourth=0,damage=None):
    eta=Poly.var(2,0);z=Poly.var(2,1)
    A=eta*J['uz']+eta**2*(J['W']/8)+eta**3*m+eta**4*fourth
    B=eta*J['up']+eta**2*(J['W']/8)+eta**3*m+eta**4*fourth
    if damage=='critical_multiplicity':count=5
    else:count=6
    factor=Poly.const(2,1)
    for _ in range(count):factor=trunc(factor*(z-A))
    pair=trunc((z-B)**2+eta*(K['H']/2)*(1+eta*J['Gamma']+eta**2*g)**2)
    factor=trunc(factor*pair)*9
    primitive=Poly(2,{(r,j+1):a/(j+1) for (r,j),a in factor.d.items()})
    e=Poly.var(1,0);anchor=Poly.const(1,0)
    marked=1-e*(2 if damage=='anchor' else 1)
    for (r,j),a in primitive.d.items():anchor=anchor+trunc(e**r*marked**j)*a
    primitive=primitive-Poly(2,{(r[0],0):a for r,a in anchor.d.items()})
    return primitive


def third_normal(cols,j):
    w=Z(2*C*C-1,2*C)**j
    g1,g2,g3=cols[1:4]
    L=-eval_z(g1,w)/(9*w**8)
    d=-(eval_z(g2,w)+eval_z(derivative_z(g1),w)*L+36*w**7*L*L)/(9*w**8)
    e=-(eval_z(g3,w)+eval_z(derivative_z(g2),w)*L+eval_z(derivative_z(g1),w)*d+
         eval_z(derivative_z(derivative_z(g1)),w)*L*L/2+72*w**7*L*d+84*w**6*L**3)/(9*w**8)
    return (e/w).r+(L*d.conjugate()).r


def scalar_and_normalization(K,J,jet,damage=None):
    c,H,rho,sigma=(K[k] for k in ['c','H','rho','sigma'])
    weights=[F(2)/3*(7-(2-2*c*c)/(c+2*c*c-1)),1/(c+2*c*c-1)]
    normals=[third_normal(jet,j) for j in (3,4)]
    def f3(u,h2):return (1+u)**3-3*(1+u)**2*h2+15*(1+u)*h2**2/8-5*h2**3/16
    scalar=2*J['W']-3*J['U2']/2+3*J['D']/2+6*f3(J['uz'],F(0))+2*f3(J['up'],H/2)
    mean=J['uz']*J['W']
    norm=(rho*J['up']+sigma*H)*(J['U2']-J['D'])
    if damage=='mean_payment':mean=F(0)
    if damage=='norm_payment':norm=F(0)
    total=scalar+sum((w*a for w,a in zip(weights,normals)),F(0))+mean+norm
    expected=F(Q(-60800959,17496))-Q(307083769,17496)*c+Q(10980067,486)*c*c
    need(total==expected,'Whole third coefficient incl BOTH payments')
    need((total+19).sign()>0 and (total+18).sign()<0,'Exact -19<Tstar<-18')
    need(scalar==F(Q(71291,243))+Q(281287,162)*c-Q(177590,81)*c*c,'Independent scalar third term')
    need(mean+norm==F(Q(-1014038,243))-Q(203841881,9720)*c+Q(10946887,405)*c*c,'Full normalization cost')
    need(normals[0]==F(Q(475963,15120))+Q(413713,3780)*c-Q(27221,180)*c*c,'Original third normal3')
    need(normals[1]==F(Q(-6786659,51030))-Q(43058189,68040)*c+Q(14053721,17010)*c*c,'Original third normal4')
    need(all(a.sign()>0 for a in weights),'Both dual weights positive')
    return dict(scalar=scalar.serial(),mean_payment=mean.serial(),norm_payment=norm.serial(),normalization=(mean+norm).serial(),normals=[a.serial() for a in normals],weights=[a.serial() for a in weights],Tstar=total.serial()),total


def witness(K,J,Tstar,damage=None):
    base=columns(defining_primitive(K,J),4)
    dm=columns(defining_primitive(K,J,m=1),4)
    dg=columns(defining_primitive(K,J,g=1),4)
    rhs=[-third_normal(base,j) for j in (3,4)]
    a,b,d,e=[third_normal(p,j)-third_normal(base,j) for j in (3,4) for p in (dm,dg)]
    det=a*e-b*d
    need(det==2*C-1 and det.sign()>0,'Actual repair determinant')
    m=(rhs[0]*e-b*rhs[1])/det;g=(a*rhs[1]-rhs[0]*d)/det
    need(m==F(Q(-17403419,34992))-Q(45702565,17496)*C+Q(180635,54)*C*C,'Independently solved common third shift')
    need(g==F(Q(-1162307,23328))-Q(5484833,11664)*C+Q(52426519,93312)*C*C,'Independently solved pair second scale')
    if damage=='repair':g=g+1
    primitive=defining_primitive(K,J,m,g,100,damage)
    cols=columns(primitive,4)
    roots,arrays=root_jets(cols)
    g1,g2=fixed_jet(K,J)
    need(all(cols[1][j]==g1.get(j,F(0)) and cols[2][j]==g2.get(j,F(0)) for j in range(10)),'Whole fixed first/second witness columns')
    for j,r in enumerate(roots):
        normals=[F(v) for v in r['half_normals']]
        if j in (3,4,5,6):
            need(normals[:3]==[F(0)]*3 and normals[3].sign()<0,'All4 active roots zero then strictly inward')
        else:need(normals[0].sign()<0,'All5 inactive first inward normals')
    q3=F(Q(77000544293,6718464))+Q(371513219527,6718464)*C-Q(483693373045,6718464)*C*C
    q4=F(Q(-17159240005,13436928))-Q(90073161839,13436928)*C+Q(18744138719,2239488)*C*C
    need(F(roots[3]['half_normals'][3])==q3 and F(roots[4]['half_normals'][3])==q4,'Both whole fourth normal constants')
    need(arrays[0]==[Z(1),Z(-1),Z(0),Z(0),Z(0)],'Exact marked original series')
    e=Poly.var(1,0)
    real=1-(1+J['uz'])*e-J['W']/8*e**2-m*e**3-100*e**4
    pair=1-(1+J['up'])*e-J['W']/8*e**2-m*e**3-100*e**4
    square=trunc(pair**2+e*(K['H']/2)*(1+J['Gamma']*e+g*e**2)**2)
    objective=6*s_power(real,Q(-1))+2*s_power(square,Q(-1) if damage=='power' else Q(-1,2))
    need([objective.d.get((r,),F(0)) for r in range(4)]==[F(8),K['C'],K['Bstar'],Tstar],'Complete actual FIRST-power through3')
    # PROVED independent refinement for this fixed repaired analytic family:
    # replacing fourth common shift100 by M changes active q by -A_k(M-100).
    slopes=[]
    changed=columns(defining_primitive(K,J,m,g,101),4)
    # All lower jets equal; fourth-root change comes solely from coefficient4.
    for j in (3,4):
        w=arrays[j][0]
        delta=-eval_z({k:changed[4][k]-cols[4][k] for k in range(10)},w)/(9*w**8)
        slope=(delta/w).r
        need(slope==-(1-w.r),'Actual fourth common shift radial slope')
        slopes.append(slope)
    thresholds=[100-q/sl for q,sl in zip((q3,q4),slopes)]
    need((thresholds[1]-thresholds[0]).sign()>0,'Exact dominant threshold label4')
    threshold=thresholds[1]
    def actual_objective(M):
        real_M=1-(1+J['uz'])*e-J['W']/8*e**2-m*e**3-M*e**4
        pair_M=1-(1+J['up'])*e-J['W']/8*e**2-m*e**3-M*e**4
        square_M=trunc(pair_M**2+e*(K['H']/2)*(1+J['Gamma']*e+g*e**2)**2)
        return 6*s_power(real_M,Q(-1))+2*s_power(square_M,Q(-1,2))
    endpoint_objective=actual_objective(threshold)
    endpoint_coeff=endpoint_objective.d.get((4,),F(0))
    need(endpoint_coeff==objective.d.get((4,),F(0))+8*(threshold-100),'Exact fourth objective slope')
    need(endpoint_coeff.sign()<0,'Strict negative fourth objective at limiting containment threshold')
    Mstar=threshold-endpoint_coeff/16
    if damage=='equality_cap':Mstar=threshold-1
    equality_primitive=defining_primitive(K,J,m,g,Mstar)
    equality_roots,equality_arrays=root_jets(columns(equality_primitive,4))
    for j,rj in enumerate(equality_roots):
        normal=[F(v) for v in rj['half_normals']]
        if j in (3,4,5,6):need(normal[:3]==[F(0)]*3 and normal[3].sign()<0,'NEW equality-cap all4 inward originals')
        else:need(normal[0].sign()<0,'NEW equality-cap all5 inactive originals')
    equality_objective=actual_objective(Mstar)
    need((Mstar-threshold).sign()>0,'Strictly above actual threshold')
    need(equality_objective.d.get((4,),F(0))==endpoint_coeff/2 and (endpoint_coeff/2).sign()<0,'NEW strict equality-cap FIRST-power witness')
    need([equality_objective.d.get((r,),F(0)) for r in range(4)]==[F(8),K['C'],K['Bstar'],Tstar],'NEW equality-cap all lower coefficients')
    return dict(complete_primitive=primitive.serial(),repair_matrix=[[a.serial(),b.serial()],[d.serial(),e.serial()]],repair_determinant=det.serial(),third_shift=m.serial(),pair_second_scale=g.serial(),all9_root_jets=roots,real_distance=real.serial(),pair_distance_squared=square.serial(),objective=objective.serial(),fourth_shift_slopes=[v.serial() for v in slopes],fourth_shift_thresholds=[v.serial() for v in thresholds],dominant_threshold=threshold.serial(),dominant_threshold_label=4,fourth_objective_at_threshold=endpoint_coeff.serial(),fourth_objective_at_threshold_sign=endpoint_coeff.sign(),NEW_equality_cap=dict(common_fourth_shift=Mstar.serial(),complete_primitive=equality_primitive.serial(),all9_root_jets=equality_roots,entire_objective=equality_objective.serial(),strict_fourth_objective=(endpoint_coeff/2).serial()))


def tangent(K,damage=None):
    # Fresh complete six-transverse balanced cubic/quartic identities after
    # eliminating r=-sum(t)/2. No square-root variable is introduced.
    e=Poly.var(7,0);t=[Poly.var(7,i+1) for i in range(6)]
    r=-sum(t,Poly.const(7,0))/2
    T2=sum((v*v for v in t),Poly.const(7,0))
    q2=K['H']/2-e**2*(T2/2+r*r)
    J3=2*(e*r)**3+6*e*r*q2+e**3*sum((v**3 for v in t),Poly.const(7,0))
    J4=2*(e*r)**4+12*(e*r)**2*q2+2*q2*q2+e**4*sum((v**4 for v in t),Poly.const(7,0))
    cost=K['alpha']*(J4-K['H']**2/2)+K['tau']*J3*J3/K['H']
    leading=K['H']*(-K['alpha']*T2+(9*K['tau']+4*K['alpha'])*r*r)
    square=9*K['H']*K['kappa']*r*r-K['alpha']*K['H']*sum(((v+r/3)**2 for v in t),Poly.const(7,0))
    if damage=='tangent':square=square+1
    need(leading.same(square),'Whole balanced quadratic nonnegative form')
    need(trunc(cost,3).same(e**2*leading),'Whole cubic/quartic tangent expansion')
    need(trunc(J3,2).same(3*K['H']*e*r),'Whole leading cubic relation')
    need(K['kappa'].sign()>0 and K['alpha'].sign()<0,'Strict tangent coefficients')
    return dict(balanced_J3=J3.serial(),balanced_J4=J4.serial(),entire_projected_cost=cost.serial(),leading_nonnegative_form=square.serial())


def run(damage=None):
    K=constants();J,rows=derive_stationary(K)
    names,formal=formal_newton(damage)
    values=[K['U0'],K['H'],J['W'],J['D'],J['J21'],J['J4'],6*J['uz']**3+2*J['up']**3,K['H']*J['up']**2,K['H']**2*J['up']/2,K['H']**3/4]
    fixed=[{j:formal[r][j].evaluate(values) for j in range(10)} for r in range(4)]
    g1,g2=fixed_jet(K,J)
    need(all(fixed[1][j]==g1.get(j,F(0)) and fixed[2][j]==g2.get(j,F(0)) for j in range(10)),'Entire stationary formal maps')
    offsets,Tstar=scalar_and_normalization(K,J,fixed,damage)
    if damage=='freeze_moving':fixed[3][0]=fixed[3][0]+1
    # Recheck a changed whole formal moment direction, not a diagnostic hash.
    need(third_normal(fixed,3)==F(offsets['normals'][0]),'Complete third root map retained')
    actual=witness(K,J,Tstar,damage)
    chart=tangent(K,damage)
    return dict(actual_agent='six-reviewer-4',role='independent mathematical reviewer',embedding='8c^3-6c-1=0,15/16<c<47/50; T=i sin(pi/9)',formal_parameter_names=names,entire_formal_real_jet={str(r):{str(j):p.serial() for j,p in col.items()} for r,col in formal.items()},fixed_real_jet=[{str(j):v.serial() for j,v in col.items()} for col in fixed],stationary_values={k:v.serial() for k,v in J.items()},third_offsets=offsets,actual_witness=actual,full_tangent=chart)


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,separators=(',',':')))
