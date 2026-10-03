"""six-reviewer-3: independent full symbolic identities/budgets for LEMMA9894.
Written formulas exposed, target executable and fixtures unopened at creation.
Own credited polys.py from REVIEW9845; no target import. Python3.12 stdlib.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib,json,sys
from polys import Poly,symbol,cast,need

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def identity(name,lhs,rhs,record):
    need(lhs==rhs,'identity '+name)
    record[name]={'lhs':lhs.record(),'rhs':rhs.record()}
def positivity(name,value,record):
    need(value>0,'strict budget '+name);record[name]=str(value)

def reduce_c(p):
    """Exact minimal cubic c^3=3c/4+1/8; no floating root substitution."""
    out=cast(0)
    for key,value in p.terms.items():
        m=dict(key);n=m.pop('c',0);a=[F(1),F(0),F(0)]
        for _ in range(n):a=[a[2]/8,a[0]+3*a[2]/4,a[1]]
        for k,v in enumerate(a):out+=Poly({tuple(sorted(m.items())):value})*symbol('c')**k*v
    return out

def cyclic(coefs):
    out=[F(0)]*9
    for n,v in coefs:out[n%9]+=F(v)
    # Reduce z^6+z^3+1; real conjugation z^j -> z^(-j).
    for n in range(8,5,-1):v=out[n];out[n]=0;out[n-3]-=v;out[n-6]-=v
    return out[:6]

def build():
    maps={};margins={};records={}
    X=[symbol('x'+str(j)) for j in range(8)];Y=[symbol('y'+str(j)) for j in range(8)]
    A,B=symbol('A'),symbol('B');Sx=sum(X);Sy=sum(Y)
    E=sum(x*x for x in X);V=sum(x*x+y*y for x,y in zip(X,Y));S4=sum((x*x+y*y)**2 for x,y in zip(X,Y))
    f=[A*x*x-B*y*y for x,y in zip(X,Y)];fbar=sum(f)/8;fc=[z-fbar for z in f]
    R=sum(x*z for x,z in zip(X,f));Rc=sum(x*z for x,z in zip(X,fc));variance=sum(z*z for z in fc)
    # Free variables first: stronger universal Lagrange identity, then Sx=0.
    wedges=sum((X[j]*fc[k]-X[k]*fc[j])**2 for j,k in combinations(range(8),2))
    identity('full_centered_Lagrange',E*variance-Rc**2,wedges,maps)
    identity('centering_correction',Rc,R-Sx*fbar,maps)
    identity('quadratic_sum',sum(f),(A+B)*E-B*V,maps)
    identity('quadratic_square_sum',sum(z*z for z in f),B*B*S4-(B*B-A*A)*sum(x**4 for x in X)-2*B*(A+B)*sum(x*x*y*y for x,y in zip(X,Y)),maps)
    quartic_pair=sum((X[j]**2+Y[j]**2)*sum((X[k]-X[l])**2+(Y[k]-Y[l])**2 for k,l in combinations([i for i in range(8) if i!=j],2)) for j in range(8))
    correction=2*sum((X[j]**2+Y[j]**2)*(Sx*X[j]+Sy*Y[j]) for j in range(8))-(Sx*Sx+Sy*Sy)*V
    identity('free_quartic_with_mean_correction',quartic_pair,7*V**2-8*S4+correction,maps)
    identity('scalar_fourth_variance',8*sum(x**4 for x in X)-E**2,sum((X[j]**2-X[k]**2)**2 for j,k in combinations(range(8),2)),maps)
    bound=F(3,4)*B*B*V**2+B*(A+B)*E*(V-E)/4
    remainder=B*B*(F(7,8)*V**2-S4)+(B*B-A*A)*(sum(x**4 for x in X)-E**2/8)+2*B*(A+B)*sum(x*x*y*y for x,y in zip(X,Y))
    identity('full_variance_remainder',bound-variance,remainder,maps)
    x,y=symbol('x'),symbol('y')
    identity('real_cube_pointwise',9*x*x*(x*x+y*y)**2-(x**3-3*x*y*y)**2,8*x**6+24*x**4*y*y,maps)
    # Any n>=2 variant: generic aggregate identities, all real |A|<=|B|.
    nn,ee,vv,ss,hh,zz=[symbol(k) for k in ('n','e','v','s4','x4','xy')]
    nvar=nn*(B*B*ss-(B*B-A*A)*hh-2*B*(A+B)*zz)-((A+B)*ee-B*vv)**2
    nbound=(nn-2)*B*B*vv**2+2*B*(A+B)*ee*(vv-ee)
    nrem=B*B*((nn-1)*vv**2-nn*ss)+(B*B-A*A)*(nn*hh-ee**2)+2*nn*B*(A+B)*zz
    identity('all_n_variance_remainder_cleared',nbound-nvar,nrem,maps)
    # Rebuild the combined SIGNED P3 and phase-four normal before absolute values.
    t,w=symbol('t'),symbol('w')
    pc=x**3-F(3,2)*x*y*y;uc=x**3-3*x*y*y
    aa=t**-4-w*t**-1/12;bb=F(3,2)*t**-4-w*t**-1/4
    identity('combined_signed_cube',pc*t**-4-w*uc*t**-1/12,x*(aa*x*x-bb*y*y),maps)
    # Entire p = integral9*p'; coefficients d7=-9T/14,d6=-U/2.
    z,uu,TT,UU=symbol('z'),symbol('u'),symbol('T'),symbol('U')
    primitive=z**9-F(9,14)*TT*z**7-UU*z**6/2
    identity('centered_polynomial_derivative',primitive.derivative('z'),9*(z**8-TT*z**6/2-UU*z**5/3),maps)
    # delta3 = U/(18u^2)(omega^-2-omega); paired half-normal coefficient.
    phases=[]
    for kphase in range(9):
        coeff=cyclic([(-3*kphase,F(1,36)),(3*kphase,F(1,36)),(0,-F(1,18))])
        expected=[F(0) if kphase%3==0 else -F(1,12)]+[F(0)]*5
        need(coeff==expected,'full9 paired cubic sign');phases.append([str(v) for v in coeff])
    records['nine_paired_cube_coefficients']=phases
    # Exact prior dual/profile identities, checked after clearing denominators.
    c=symbol('c');d=2*c*c-1;den=c+d
    w4num=cast(1);w3num=F(2,3)*(7*den-(1-d));ynum=cast(1);yden=3*(1+c)
    xnum=F(2,3)*yden-ynum
    a3=b3=cast(F(3,2));a4=1+c;b4=1-d
    identity('dual_M',reduce_c(w3num*a3+w4num*a4),reduce_c(8*den),maps)
    identity('dual_Q',reduce_c(w3num*b3+w4num*b4),reduce_c(7*den),maps)
    identity('dual_C',reduce_c((8*den-w3num-w4num)*yden),reduce_c(den*(F(8,3)*yden+ynum)),maps)
    identity('profile3',reduce_c(a3*xnum+b3*ynum),reduce_c(yden),maps)
    identity('profile4',reduce_c(a4*xnum+b4*ynum),reduce_c(yden),maps)
    identity('cramer_determinant',a3*b4-a4*b3,-F(3,2)*den,maps)
    lo,hi=F(15,16),F(47,50);fpoly=lambda q:8*q**3-6*q-1
    positivity('root_left',-fpoly(lo),margins);positivity('root_right',fpoly(hi),margins);positivity('root_monotonic',24*lo**2-6,margins)
    # Cramer endpoint EQUALITIES, strict inside by positive monotonic derivatives.
    need(F(3,2)*(lo+2*lo**2-1)==F(651,256),'Cramer left equality')
    need(2-2*lo**2==F(31,128),'B4 left equality')
    records['cramer_endpoint_equalities']={'det':'651/256','B4':'31/128','strict_reason':'c>15/16; det derivative 3(1+4c)/2>0, B4 derivative -4c<0'}
    weight3=lambda t:F(2,3)*(7-2*(1-t)/(2*t-1))
    positivity('w3_lower4',weight3(lo)-4,margins)
    positivity('w3_upper23over5',F(23,5)-weight3(hi),margins)
    positivity('w4_lowerhalf',1/(hi+2*hi**2-1)-F(1,2),margins)
    positivity('w4_upper3over5',F(3,5)-1/(lo+2*lo**2-1),margins)
    need(1+hi==F(97,50),'A4 endpoint equality')
    records['weight_endpoint_equalities']={'w4_at_hi':'625/1067','A4_at_hi':'97/50','y_at_lo':'16/93'}
    e=F(1,16000);amin=1-e;rp=1+e;v=5*e;tau=F(1,60);G=1/((amin-tau)*amin**4);beta=F(271,200);kap=3*beta**2/4;qq=beta*(1+beta)/4
    params={'e':e,'a_star':amin,'r_plus':rp,'v':v,'tau':tau,'G':G,'beta_upper':beta,'k':kap,'q':qq}
    records['parameters']={k:str(val) for k,val in params.items()}
    # At upper c endpoint w4=625/1067 EXACTLY, strictness follows decreasing w4.
    need(1/(hi+2*hi**2-1)==F(625,1067),'w4 upper-c endpoint equality')
    positivity('A_positive',rp**-4-F(3,5)/(12*amin),margins)
    positivity('B_minus_A_positive',F(1,2)*rp**-4-F(3,5)/(6*amin),margins)
    positivity('A_upper1',1-(amin**-4-F(625,1067)/(12*rp)),margins)
    positivity('B_upper',beta-(F(3,2)*amin**-4-F(625,1067)/(4*rp)),margins)
    positivity('coordinate_tau',tau*tau-F(7,8)*5*e,margins)
    positivity('noncubic_conversion36',36-(8*F(4,5)*(2-e)/amin**2+4*F(169,225)/amin**3+20),margins)
    positivity('normal_cost190',190-(36+29*F(23,5)+33*F(3,5)),margins)
    es,vs=symbol('E'),symbol('V')
    pairs={'physical':(F(1,4),F(69,50),F(247)),'objective':(F(1,2),F(69,100),F(230)),
           'refined_physical':(F(1,4),F(1379,1000),F(987,4)), 'refined_objective':(F(1,2),F(551,800),F(459,2))}
    certs={}
    for name,(delta,lam,error) in pairs.items():
        a0=delta**2-qq*v;b0=delta*lam-kap/2;det=a0*lam**2-b0*b0
        positivity(name+'_a0',a0,margins);positivity(name+'_det',det,margins)
        lhs=(delta*es+lam*vs**2)**2-es*(kap*vs**2+qq*es*vs)
        rhs=a0*(es+b0/a0*vs**2)**2+(lam*lam-b0*b0/a0)*vs**4+qq*(v-vs)*es**2
        identity(name+'_completion',lhs,rhs,maps)
        cost=190+25*(F(7,8)*G+lam);positivity(name+'_cost_margin',error-cost,margins)
        certs[name]={k:str(val) for k,val in {'delta':delta,'lambda':lam,'a0':a0,'b0':b0,'det':det,'cost':cost,'error':error,'cost_margin':error-cost}.items()}
    records['absorption_certificates']=certs
    need(certs['physical']['a0']=='31872359/512000000' and certs['physical']['det']=='1411954173/2560000000000','entire physical constants')
    need(certs['objective']['a0']=='127872359/512000000' and certs['objective']['det']=='4647004749/5120000000000','entire objective constants')
    positivity('C_upper3',3-(F(8,3)+1/(3*(1+lo))),margins)
    for name,error in [('original',F(230)),('refined',F(459,2))]:positivity(name+'_slope141over50',F(826,291)-error*e-F(141,50),margins)
    # Rebuild every stability scalar for both physical defects; no230->physical swap.
    for label,Dcoef in [('original',F(247)),('refined',F(987,4))]:
        budget={
            'sqrt_D_gt31over2':Dcoef-F(31,2)**2,
            'residual3':F(3,8)-(F(1,4)+29/Dcoef),
            'residual4':F(1,2)-(33/Dcoef+5/(31*amin)),
            'mean_cramer':F(8,5)-(F(62,651)*F(3,8)+F(128,217)*F(5,2)),
            'trace_cramer':F(9,5)-(F(24832,32550)*F(3,8)+F(128,217)*F(5,2)),
            'Q26':26-14*F(9,5),'V34':34-(8+14*F(9,5)),
            'H35':35-(34+8*F(169,225)/Dcoef),
            'cube_error26':26-(F(13,15)*5/6+25),
            'D_sqrt':1-F(9,1)/(14*amin),'D_delta':1-F(7,24)/amin,
            'D_eta2':31-F(7,6)*26/amin,
            'real_energy13':1-(F(384,25)+4*e/amin**2)/Dcoef,
            'mu3_21over2':F(21,2)**2-F(7,8)*125,
            'root88':88-(62+25+F(896,1395)/amin),
            'root_delta19over2':F(19,2)-(F(26,5)+26/(7*amin)+88/Dcoef),
            'root_sqrt7over2':F(7,2)-(2+9/(7*amin)+7/(93*amin**2)),
            'u_real_positive':amin-F(4,5)*e,
            'y_upper':F(16,93)-1/(3*(1+lo)),
        }
        # y_upper is zero at left c endpoint. Record equality; strict by c>lo.
        need(budget.pop('y_upper')==0,'y endpoint equality')
        for name,val in budget.items():positivity(label+'_stability_'+name,val,margins)
    # Fresh exact arbitrary-critical controls, not actual disk feasibility.
    controls=[]
    data=[([0]*8,[0]*8,F(0),F(0)),([0]*8,[7]+[-1]*7,F(0),F(2)),([7]+[-1]*7,[0]*8,F(1),F(2)),([3,-2,1,-3,2,-1,4,-4],[1,2,-3,4,-2,3,-4,-1],F(2,3),F(3,2)),([2,-1,3,-2,1,-3,4,-4],[3,-2,1,-3,2,-1,4,-4],-F(2,3),-F(3,2)),([7]+[-1]*7,[0]*8,-F(1),F(2))]
    for xx,yy,ac,bc in data:
        xx=list(map(F,xx));yy=list(map(F,yy));need(sum(xx)==sum(yy)==0,'control zero-sum');need(abs(ac)<=abs(bc),'extended parameter premise')
        ec=sum(q*q for q in xx);vc=ec+sum(q*q for q in yy);ff=[ac*x*x-bc*y*y for x,y in zip(xx,yy)];rc=sum(x*z for x,z in zip(xx,ff));fv=sum(ff)/8;var=sum((q-fv)**2 for q in ff)
        bd=F(3,4)*bc*bc*vc*vc+bc*(ac+bc)*ec*(vc-ec)/4
        need(bd>=var and ec*var>=rc*rc,'control full variance/Cauchy')
        controls.append({'X':list(map(str,xx)),'Y':list(map(str,yy)),'A':str(ac),'B':str(bc),'E':str(ec),'V':str(vc),'R':str(rc),'variance':str(var),'bound':str(bd),'variance_margin':str(bd-var),'Cauchy_margin':str(ec*var-rc*rc)})
    records['fresh_literal_controls']=controls
    return {'agent':'six-reviewer-3','role':'independent mathematical reviewer','symbolic_maps':maps,'strict_margins':margins,'records':records,'trust':'ordinary proof; exact maps corroborate, not finite sampling or formalization'}

def summary(out):
    return {'record_sha256':hashlib.sha256(canonical(out)).hexdigest(),'identities':len(out['symbolic_maps']),'whole_lhs_monomials':sum(len(m['lhs']) for m in out['symbolic_maps'].values()),'strict_budgets':len(out['strict_margins']),'controls':len(out['records']['fresh_literal_controls']),'phases':9,'absorption':out['records']['absorption_certificates'],'status':'PASS'}
if __name__=='__main__':
    result=build()
    if '--record' in sys.argv:Path(sys.argv[sys.argv.index('--record')+1]).write_bytes(canonical(result)+b'\n')
    print(json.dumps(summary(result),sort_keys=True))
