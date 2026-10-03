"""Exact finite corroboration of the minimal-input receiving proof.
Actual six-sendov-1 / researcher. Same-author Fraction/sparse-polynomial
backend, not independent review or analytic formalization. No network,
private imports, clocks or filesystem writes occur in record construction.
"""
from fractions import Fraction as F
Q = F

class VerificationError(ValueError):
    pass

DAMAGE_CASES = (
    "old-W7-tail", "old-W5-tail", "old-joint-Q", "first-joint-Q",
    "old-individual-slack", "real-energy-square-sign", "cube-principal-denominator",
)

def algebra(n,root=None):
 z=(0,)*n
 def C(c):return {z:F(c)} if c else {}
 def X(i):
  x=list(z);x[i]=1;return {tuple(x):F(1)}
 def add(*args):
  out={}
  for p in args:
   for k,v in p.items():out[k]=out.get(k,F(0))+v
  return {k:v for k,v in out.items() if v}
 def scale(p,c):return {k:v*F(c) for k,v in p.items() if v*c}
 def neg(p):return scale(p,-1)
 def sub(p,q):return add(p,neg(q))
 def mul(p,q):
  out={}
  for a,c in p.items():
   for b,d in q.items():
    k=[x+y for x,y in zip(a,b)];value=c*d
    if root is not None:
     pos,number=root;value*=F(number)**(k[pos]//2);k[pos]%=2
    t=tuple(k);out[t]=out.get(t,F(0))+value
  return {k:v for k,v in out.items() if v}
 def power(p,k):
  out=C(1)
  for _ in range(k):out=mul(out,p)
  return out
 return C,X,add,scale,neg,sub,mul,power


def scalar_record(damage=None):
    e=Q(1,12000);h=Q(1,320);rho=Q(1,50);t0=Q(1,320);alpha=Q(7,8)
    checks={};rejected={};values={}
    def margin(name,x,closed=False):
     x=Q(x);checks[name]={'value':str(x),'closed':closed,'positive':x>=0 if closed else x>0}
     return x
    def val(name,x):values[name]=str(Q(x));return Q(x)
    # ONLY receiving1/12000 after actual9930 H37 / retained-square input.
    margin('entry_h_minus37e',h-37*e)
    margin('rational_sqrt_e',(Q(11,1200))**2-e)
    margin('rational_sqrt_mean',Q(13,45)**2-(Q(1,12)+e/3))
    tsqrt=val('t_over_sqrt_eta',Q(74,15)*Q(11,1200)+Q(13,45))
    margin('fresh_t_square_9over80',Q(9,80)-tsqrt**2)
    margin('t0_positive_before_squaring',t0-Q(74,15)*e)
    margin('mean_t0_squared',(t0-Q(74,15)*e)**2-(e/12+e**2/3))
    r0=val('receiving_early_rminus',1-Q(63,20)*e)
    upper=val('early_rsquare_coefficient',Q(37,7)+Q(4,15)*rho*37+(Q(1,3)+Q(16,15)*37**2)*e)
    margin('early_r_upper3',6-upper)
    margin('inversecube_D10',10-3*Q(63,20)/r0**4)
    tau0=Q(21,400);margin('early_tau_squared',tau0**2-alpha*37*e);margin('early_tail_divisor',r0-tau0)
    K0=val('K37',Q(3,2)/r0**4);G0=val('G37',1/((r0-tau0)*r0**4))
    B0=val('B37',Q(976,225)+alpha*(G0+Q(7,10)*K0**2))
    c0=val('W37_coercivity',Q(1,14)-10*e-B0*37*e)
    margin('early_coercivity_positive',c0)
    margin('direct_W7',7*c0-(Q(1,3)+4*e/3))
    margin('W7_lower_r_implies_amin',1-Q(9,10)*e-(1-e))
    upper7=val('W7_rsquare_coefficient',Q(1,3)+Q(4,15)*rho*7+(Q(1,3)+Q(16,15)*7**2)*e)
    margin('W7_r_upper1',2-upper7)
    a=val('amin',1-e);margin('local_inversecube_D4',4-3/a**4)
    tau7=Q(1,50) if damage=="old-W7-tail" else Q(3,125);margin('W7_receiving_tail_squared',tau7**2-alpha*7*e)
    margin('W7_tail_divisor',a-tau7)
    K7=val('K7',Q(3,2)/a**4);G7=val('G7',1/((a-tau7)*a**4));B7=val('B7',Q(976,225)+alpha*(G7+Q(7,10)*K7**2))
    c7=val('W7_coercivity',Q(1,14)-4*e-B7*7*e)
    margin('W7_coercivity_positive',c7)
    margin('direct_W5',5*c7-(Q(1,3)+4*e/3))
    tauf=Q(1,60) if damage=="old-W5-tail" else Q(1,50);margin('W5_receiving_tail_squared',tauf**2-alpha*5*e)
    rejected['OLD_W7_tau1over50_squared']=str(Q(1,50)**2-alpha*7*e)
    rejected['OLD_W5_tau1over60_squared']=str(Q(1,60)**2-alpha*5*e)
    qstar=val('qstar_W5',tauf/((a-tauf)*a**3))
    ap=val('initial_Ep_over_eta',t0+20*e);ai=val('initial_Ei_over_eta',t0+Q(175,8)*e)
    margin('initial_M_lower4',4-(Q(2,3)+Q(5,14)+Q(2,3)*ap)/a)
    margin('initial_M_negative',a**2/4-Q(9,160)/a)
    # r>a and r<1+eta =>0<1-a³/r³<6eta<7eta, exact entire interval.
    margin('a3cube_loss7',7-6)
    coarse_slack=val('initial_cube_slack_over_eta',Q(1,16)+(Q(45,16)+Q(21,16)*5)*e+Q(3,16)*5*qstar+ai)
    margin('initial_cube_slack7over80',Q(7,80)-coarse_slack)
    margin('initial_D_bound15over4',Q(15,4)-(Q(5,14)+Q(7,6)*Q(7,80))/a)
    margin('coarse_complex_mean_square',Q(11,2)**2-(4**2+Q(15,4)**2))
    Ep=Q(51,2);Ei=Q(219,8)
    # Retain BOTH whole variance/second-moment and individual cube substitutions.
    qbudget=val('final_7Wplus5Q_coefficient',Q(28,3)+(Q(112,3)+112*5)*e+28*5*qstar+Q(448,3)*Ep*e)
    qtarget=Q(12) if damage=='old-joint-Q' else Q(25,2) if damage=='first-joint-Q' else Q(63,5)
    margin('fresh_7Wplus5Q_63over5',qtarget-qbudget)
    rejected['first_new_7Wplus5Q25over2']=str(Q(25,2)-qbudget)
    rejected['OLD_7Wplus5Q12']=str(12-qbudget)
    margin('fresh_J_13over5_squared',Q(13,5)**2-Q(63,5)**2/24)
    finalslack=val('final_cube_slack_over_eta',Q(1,16)+(Q(45,16)+Q(21,16)*5)*e+Q(3,16)*5*qstar+Ei*e)
    slack_target=Q(1,12) if damage=='old-individual-slack' else Q(7,80)
    margin('final_cube_slack7over80',slack_target-finalslack)
    rejected['OLD_cube_slack1over12']=str(Q(1,12)-finalslack)
    margin('final_D_1over3',Q(1,3)-(Q(13,5)/14+Q(7,6)*Q(7,80))/a)
    margin('final_M_lower4over5',Q(4,5)-(Q(2,3)+Q(21,20)/14+Q(2,3)*Ep*e)/a)
    margin('final_mean_exact_square',Q(13,15)**2-(Q(4,5)**2+Q(1,3)**2),closed=True)
    # Entire eta polynomial identities behind sign/normal corrections.
    # (1+eta)^3-(1-eta)^3 =6eta+2eta³ <6eta(1+eta)^3 for eta>0.
    # All coefficients of the difference after removing eta² are strictly positive.
    margin('a3_loss_eta2_coefficient',18)
    margin('a3_loss_eta3_coefficient',16)
    margin('a3_loss_eta4_coefficient',6)

    for name,entry in checks.items():
     if not entry['positive']:raise VerificationError('receiving margin rejected: '+name)
    if any(Q(v)>=0 for v in rejected.values()):raise VerificationError('failed-target provenance changed')
    return {'values':values,'margins':checks,'rejected_receiving_targets':rejected,'strict_margin_count':sum(not r['closed'] for r in checks.values()),'closed_margin_count':sum(r['closed'] for r in checks.values()),'guard_scope':'Exact endpoints plus ordinary monotonicity/positivity; no sampled original-disk feasibility'}

def identity_record(damage=None):
    records=[]
    def record(name,variables,left,right,root=None):
     if left!=right:raise VerificationError('entire identity rejected: '+name)
     def serialize(p):return [[list(k),str(v)] for k,v in sorted(p.items())]
     records.append({'name':name,'variables':variables,'root_relation':root,'left':serialize(left),'right':serialize(right),'whole_equal':True})

    C,X,A,S,N,D,M,P=algebra(2);t,w=X(0),X(1)
    record('complete_mean_square',['t','W'],A(S(P(t,2),4),S(M(t,w),-F(16,15)),S(P(w,2),-F(64,15))),A(S(P(D(t,S(w,F(2,15))),2),4),S(P(w,2),-F(976,225))))
    q=X(0)
    record('retained_real_second_moment',['Q','W'],D(S(A(w,S(q,3)),F(1,4)),S(q,F(4,7))),A(S(w,F(1,14)),S(A(w,q),F(5,28))))
    C,X,A,S,N,D,M,P=algebra(3);y,b,w=X(0),X(1),X(2)
    record('complete_real_energy_square',['sqrtE','b','W'],A(S(P(y,2),F(5,14)),N(M(M(b,w),y)),S(M(P(b,2),P(w,2)),F(7,10))),S(P(D(y,S(M(b,w),-F(7,5) if damage=='real-energy-square-sign' else F(7,5))),2),F(5,14)))
    C,X,A,S,N,D,M,P=algebra(2);x,y=X(0),X(1)
    record('complete_pointwise_signed_cubic',['X','Y'],D(S(M(P(x,2),P(A(P(x,2),P(y,2)),2)),F(9,4)),P(D(P(x,3),S(M(x,P(y,2)),F(3,2))),2)),A(S(P(x,6),F(5,4)),S(M(P(x,4),P(y,2)),F(15,2))))
    C,X,A,S,N,D,M,P=algebra(14);xs=[X(i) for i in range(7)];ys=[X(i+7) for i in range(7)]
    left=D(S(A(*(P(v,2) for v in xs+ys)),7),A(P(A(*xs),2),P(A(*ys),2)))
    right=A(*(A(P(D(xs[j],xs[k]),2),P(D(ys[j],ys[k]),2)) for j in range(7) for k in range(j+1,7)))
    record('whole_seven_value_Cauchy_Lagrange',['X'+str(i) for i in range(7)]+['Y'+str(i) for i in range(7)],left,right)

    # Complete Q[sqrt3,i] cube normals; no finite numerical phase evaluation.
    C,X,A,S,N,D,M,P=algebra(6,root=(5,3));eta,mr,mi,q,j,s=[X(i) for i in range(6)];a=D(C(1),eta)
    def cmul(z,w):return (D(M(z[0],w[0]),M(z[1],w[1])),A(M(z[0],w[1]),M(z[1],w[0])))
    def cadd(z,w):return (A(z[0],w[0]),A(z[1],w[1]))
    principal=A(N(eta),S(P(eta,2),F(1,2)),S(M(a,mr),-F(3,2)),S(A(P(mr,2),P(mi,2)),F(3,2)),S(q,-F(3,28)))
    odd=S(M(s,D(M(a,mi),S(j,F(1,14)))),F(1,2))
    normal=[]
    for sign in (1,-1):
     omega=(C(-F(1,2)),S(s,F(sign,2)))
     base=cadd((M(a,omega[0]),M(a,omega[1])),cmul((mr,mi),(D(C(1),omega[0]),N(omega[1]))))
     half=S(D(A(P(base[0],2),P(base[1],2)),C(1)),F(1,2))
     correction=S(cmul((q,j),(D(omega[0],C(1)),omega[1]))[0],F(1,13) if damage=='cube-principal-denominator' else F(1,14))
     actual=A(half,correction);normal.append(actual)
     record('entire_cube_normal_sign'+str(sign),['eta','M','D','Q','J','sqrt3'],actual,A(principal,S(odd,sign)),root='sqrt3²=3')
    record('whole_paired_cube_normal',['eta','M','D','Q','J','sqrt3'],S(A(*normal),F(1,2)),principal,root='sqrt3²=3')
    record('whole_individual_cube_difference',['eta','M','D','Q','J','sqrt3'],S(M(s,D(normal[0],normal[1])),F(1,3)),D(M(a,mi),S(j,F(1,14))),root='sqrt3²=3')

    C,X,A,S,N,D,M,P=algebra(6);eta,z,w,q,c,tail=[X(i) for i in range(6)];a=D(C(1),eta)
    common=A(eta,S(P(eta,2),-F(1,2)),S(M(P(a,3),eta),-F(15,16)),S(z,-F(3,4)),S(M(P(a,3),tail),F(3,16)))
    left=A(common,S(M(c,A(w,S(q,3))),-F(3,64)),S(q,F(3,28)))
    right=A(common,S(w,-F(3,64)),S(q,-F(15,448)),S(M(D(C(1),c),A(w,S(q,3))),F(3,64)))
    record('whole_low_cut_mean_substitution',['eta','t²','W','Q','a³/r³','T3'],left,right)
    C,X,A,S,N,D,M,P=algebra(1);eta=X(0);a=D(C(1),eta)
    term=A(eta,S(P(eta,2),-F(1,2)),S(M(P(a,3),eta),-F(15,16)))
    record('whole_eta_majorant_remainder',['eta'],D(A(S(eta,F(1,16)),S(P(eta,2),F(45,16))),term),A(S(P(eta,2),F(1,2)),S(M(P(eta,3),D(C(3),eta)),F(15,16))))
    record('whole_inverse_cube_loss',['eta'],D(S(M(eta,P(A(C(1),eta),3)),6),D(P(A(C(1),eta),3),P(a,3))),A(S(P(eta,2),18),S(P(eta,3),16),S(P(eta,4),6)))
    C,X,A,S,N,D,M,P=algebra(2);eta,q=X(0),X(1);k=F(63,5)
    record('whole_QJ_ellipse',['eta','Q'],D(P(D(S(eta,k),S(q,5)),2),S(P(q,2),49)),D(S(P(eta,2),F(49,24)*k*k),S(P(A(q,S(eta,F(5,24)*k)),2),24)))


    return {'identities':records,'identity_count':len(records),'left_monomials':sum(len(r['left']) for r in records),'all_whole_maps_match':True,'algebra_scope':'All rational coefficients of both sides; classical signs and parent feasibility remain ordinary bridges'}

def build_record(damage=None):
    if damage is not None and damage not in DAMAGE_CASES:
        raise VerificationError("unknown mathematical damage")
    return {
        "agent": "six-sendov-1", "role": "researcher", "schema": 1,
        "status": "Complete ordinary alternative bootstrap; unformalized and independently unreviewed; shared conclusion with LEMMA9954",
        "domain": "All actual complex monic degree9, all9 originals closed disk, marked a=1-eta, every0<eta<=1/12000, all8 critical multiplicities, only F<=8+3eta",
        "sole_numerical_input": {
            "graph_ref": "bafkreigxaj6xryqvuuqybrsjayb6cb3sggqowxpw4wyfgnj5rnfs2qkdwy",
            "source_commit": "f7851176d3acd8ec4fb3256ada4f53a50a6afdc2",
            "scope": "Genuine H<37eta then separate fixedH1/320 retained square, broad cube paired4/5 and individual7/8, all-degree Legendre tail",
        },
        "conclusion": "W<5eta, -4eta/5<M<0, |D|<eta/3, |m|<13eta/15, 1-eta<r<1+eta",
        "scalars": scalar_record(damage), "algebra": identity_record(damage),
        "trust": "Finite records corroborate the written proof. Actual entry, all-nine parent normals, convergence, classical inequalities, monotonicity, implication order and full-domain coverage are ordinary proof bridges, not formalized or independently reviewed here.",
    }
