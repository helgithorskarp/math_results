#!/usr/bin/env python3
"""Whole exact receiving budgets. All universal bridges are in PROOF.md.
Actual six-sendov-1, researcher. Standard-library author validation only.
Polynomial/Gaussian primitives explicitly adapted from own9818; no peer
executable, fixture, seal, numerical endpoint, or review verdict imported.
"""
import argparse
import hashlib
import json
from fractions import Fraction as R
from math import comb, factorial
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parent
FILES = [".gitignore", "verify.py", "validate.py", "PROOF.md", "README.md", "LITERATURE.md", "EXPECTED.json"]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def pmul(p,q):
    z=[R(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q): z[i+j]+=a*b
    return z

def ppow(p,n):
    z=[R(1)]
    for _ in range(n):z=pmul(z,p)
    return z

def ga(a,b=0):return (R(a),R(b))
def ga_add(x,y):return (x[0]+y[0],x[1]+y[1])
def ga_mul(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def ga_scale(x,t):return (x[0]*t,x[1]*t)
def gp(q,a):
    p=[ga(1)]
    for v in q:
        out=[ga(0)]*(len(p)+1)
        for j,c in enumerate(p):
            out[j]=ga_add(out[j],c)
            out[j+1]=ga_add(out[j+1],ga_scale(ga_mul(c,v),-a))
        p=out
    return p
def symmetric(q):
    e=[ga(1)]+[ga(0)]*len(q)
    for n,v in enumerate(q,1):
        for k in range(n,0,-1):e[k]=ga_add(e[k],ga_mul(v,e[k-1]))
    return e
def gint(p,shift,factor):
    out=ga(0)
    for j,c in enumerate(p):out=ga_add(out,ga_scale(c,R(factor,j+shift+1)))
    return out
def enc(x):return [str(x[0]),str(x[1])]

def literal_control(name,q,a):
    direct=gint(gp(q,a),0,9)
    e=symmetric(q);alternative=ga(0)
    for k,c in enumerate(e):alternative=ga_add(alternative,ga_scale(c,R(9,k+1)*(-a)**k))
    require(direct==alternative,'complete origin control mismatch')
    gradients=[];hessians=[]
    for i in range(8):
        rest=q[:i]+q[i+1:]
        gd=ga_scale(gint(gp(rest,a),1,9),-a)
        es=symmetric(rest); ge=ga(0)
        for k,c in enumerate(es,1):ge=ga_add(ge,ga_scale(c,R(9,k+1)*(-a)**k))
        require(gd==ge,'complete first derivative control mismatch')
        gradients.append(enc(gd))
        row=[]
        for j in range(8):
            if i==j:
                row.append(enc(ga(0)));continue
            rest2=[v for n,v in enumerate(q) if n not in (i,j)]
            hd=ga_scale(gint(gp(rest2,a),2,9),a*a)
            es2=symmetric(rest2);he=ga(0)
            for k,c in enumerate(es2,2):he=ga_add(he,ga_scale(c,R(9,k+1)*(-a)**k))
            require(hd==he,'complete mixed derivative control mismatch')
            row.append(enc(hd))
        hessians.append(row)
    mean=ga(0)
    for z in q:mean=ga_add(mean,ga_scale(z,R(1,8)))
    x=[ga_add(z,ga_scale(mean,-1)) for z in q]
    esx=symmetric(x);traces=[ga(8)]
    for k in range(1,9):
        value=ga(0)
        for z in x:
            zk=ga(1)
            for _ in range(k):zk=ga_mul(zk,z)
            value=ga_add(value,zk)
        traces.append(value)
    require(esx[1]==ga(0),'centered trace control')
    for k in range(2,9):
        rhs=ga(0)
        for s in range(2,k+1):rhs=ga_add(rhs,ga_scale(ga_mul(esx[k-s],traces[s]),(-1)**(s-1)))
        require(ga_scale(esx[k],k)==rhs,'whole centered Newton identity')
    require(esx[4]==ga_add(ga_scale(ga_mul(traces[2],traces[2]),R(1,8)),ga_scale(traces[4],R(-1,4))),'complete fourth Newton cancellation')
    return {'name':name,'a':str(a),'whole_q':[enc(v) for v in q],
            'whole_origin_product_coefficients':[enc(v) for v in gp(q,a)],
            'origin':enc(direct),'all_eight_gradients':gradients,'whole_ordered_hessian':hessians,
            'whole_centered_tuple':[enc(v) for v in x],'all_centered_elementary_coefficients':[enc(v) for v in esx],
            'all_centered_traces':[enc(v) for v in traces]}


def padd(*ps):
    z=[R(0)]*max(map(len,ps))
    for p in ps:
        for k,c in enumerate(p):z[k]+=c
    while len(z)>1 and not z[-1]:z.pop()
    return z
def pscale(p,t):return [t*c for c in p]
def pvalue(p,x):
    z=R(0)
    for c in reversed(p):z=z*x+c
    return z
def bmul(p,q):
    z={}
    for (i,j),c in p.items():
        for (k,l),d in q.items():z[i+k,j+l]=z.get((i+k,j+l),R(0))+c*d
    return {k:c for k,c in z.items() if c}
def polar_record(sigma):
    a=[R(1),R(-1)];b=padd([1],pscale(ppow(a,2),-1));L=[R(8),R(3)]
    d=pscale(pmul(ppow(a,7),b),R(1,2));T=[R(0)]
    for k in range(2,9):
        T=padd(T,pscale(pmul(pmul(ppow(a,8-k),ppow(b,k)),ppow(pscale(L,R(1,8)),k)),R(comb(8,k),k+1)))
    B=padd(ppow(a,8),pmul(d,L),T)
    factor={(i,0):c for i,c in enumerate(a) if c}
    for i,c in enumerate(pmul(b,pscale(L,R(1,8)))):
        if c:factor[i,1]=c
    raw={(0,0):R(1)}
    for _ in range(8):raw=bmul(raw,factor)
    direct=[R(0)]*(max(i for i,t in raw)+1)
    for (i,t),c in raw.items():direct[i]+=c/R(t+1)
    require(direct==B,"whole binomial/balanced polar integration")
    mean=padd([1],pscale(ppow(a,16),-1),pscale(pmul(ppow(d,2),ppow(L,2)),-1),
              pscale(pmul(padd(ppow(a,8),pmul(d,L)),T),-2),pscale(ppow(T,2),-1),
              pscale(pmul([R(8),-sigma],pmul(ppow(a,15),b)),-1))
    mean_alt=padd([1],pscale(ppow(direct,2),-1),pscale([0]+pmul(ppow(a,15),b),sigma+3))
    require(mean==mean_alt,"whole squared-mean routes")
    modulus=padd([1,0,9],pscale(B,-1))
    variance=padd(pscale(pmul(ppow(a,6),ppow(b,2)),13),pscale(padd(B,[-1]),-6))
    for name,p,head in [("mean",mean,R(1,3)),("modulus",modulus,R(2,3)),("variance",variance,R(2))]:
        require(p[:2]==[0,0] and p[2]==head,"whole cancellation "+name)
    return {"whole_balanced_integral":B,"whole_tail":T,
            "scalar_certificates":{"mean":{"polynomial":mean},"modulus":{"polynomial":modulus},"variance":{"polynomial":variance}}}

add,mul,powp,scale,value = padd,pmul,ppow,pscale,pvalue

def build_record():
    E=R(1,12000);sigma=R(11,2);mu_cap=sigma/8;beta=sigma+3
    beta_prime=beta*(1+sigma*E/4)
    phase_prime=16*beta_prime;phase_all=2*(8+3*E)*beta_prime
    budget={}
    def keep(name,margin):
        budget[name]=margin

    # Complete receiving polar streams, including all canceled initial orders.
    old=polar_record(sigma);a=[R(1),R(-1)];b=[R(0),R(2),R(-1)]
    Nm=old['scalar_certificates']['mean']['polynomial']
    polar={'mean':Nm,'modulus':old['scalar_certificates']['modulus']['polynomial'],
           'variance':old['scalar_certificates']['variance']['polynomial']}
    polar_bounds={}
    for name,p in polar.items():
        threshold={'mean':0,'modulus':R(1,2),'variance':1}[name]
        lower=p[2]-sum((abs(c)*E**(k-2) for k,c in enumerate(p) if k>=3),R(0))
        keep('whole_polar_'+name,lower-threshold)
        polar_bounds[name]={'whole_polynomial':p,'complete_tail_lower':lower,'threshold':threshold}
    keep('a_above255over256',R(1,256)-E)
    keep('variance_transfer65over64',R(65,64)-R(256,255)**2)
    keep('full_derivative_class_a99over100',R(1,100)-E)
    keep('full_derivative_class_total803over100',R(3,100)-3*E)
    keep('global_real_product_gradient2',2-(R(753,700))**7)
    keep('all_path_complex_epsilon1over8',R(1,64)-phase_all*E)
    global_cost=R(9,16)*beta_prime+R(3,8)*phase_prime+sigma*(R(2,3)+2)
    keep('global_cost_under71',71-global_cost)

    # All8 receiving real penalty faces, complete polynomial routes and tails.
    floor={(0,0):R(2),(1,0):R(-1),(0,1):R(-1),(1,1):R(1)}
    faces=[]
    for m in range(1,9):
        free=dict(floor)
        for j,c in enumerate(powp(a,2)):
            free[j,1]=free.get((j,1),R(0))-R(8,m)*c
        prod={(0,0):R(1)}
        for j in range(8):
            prod=bmul(prod,free if j<m else floor)
        op=[R(0)]*(max(i for i,j in prod)+1)
        for (i,j),c in prod.items():
            op[i]+=9*c/R(j+1)
        alternate=[R(0)]
        for ell in range(m+1):
            for j in range(9-ell):
                alternate=add(alternate,scale(mul(powp([2,-1],8-ell-j),powp(a,2*ell+j)),
                              R(9,ell+j+1)*math.comb(m,ell)*math.comb(8-ell,j)*R(-8,m)**ell*(-1)**j))
        if op!=alternate:
            raise ValueError('receiving full face routes differ')
        dm=R(64*(m-1),m)-R(256*(m-1)*(m-2),3*m*m)
        residual=add(op,scale(powp([1+R(8,m),R(-8,m)],m),-1),[-8],
                     scale(powp(a,9),8),scale(powp(a,3),-R(39,5)*dm))
        leading=next(j for j,c in enumerate(residual) if c)
        lower=residual[leading]-sum((abs(c)*E**(j-leading) for j,c in enumerate(residual) if j>leading),R(0))
        keep('full_receiving39over5_face_'+str(m),lower)
        faces.append({'m':m,'whole_origin':op,'whole_residual':residual,
                      'leading':leading,'full_tail_lower':lower,'defect_coefficient':dm})

    # Genuine coarse implications precede every new local small-variance use.
    d0=R(256*71*5,39)
    keep('initial_E2_over7over4',28*(1-E)**2-26-R(7,4))
    keep('coarse_v_under8over5',R(8,5)-8*d0*E)
    keep('coarse_E2_over99over4',28*(1-E)**2-R(16,5)-R(99,4))
    keep('coarse_v_under11over100',R(11,100)-R(56,99)*d0*E)
    keep('coarse_E2_over111over4',28*(1-E)**2-R(22,100)-R(111,4))
    keep('coarse_v_under1over10',R(1,10)-R(56,111)*d0*E)

    # First complete local phase/radial/scaling ball and derivative signs.
    v0=R(1,10);rho1=R(3,10);rad1=R(8,25);phi1=R(9,200)
    ball1=R(4,25);t1=R(1,6);g1=R(1,5);h1=R(1,16)
    keep('first_real_radial_root',rad1**2-R(65,64)*v0-8*mu_cap**2*E**2)
    keep('first_individual_radius',(rho1-mu_cap*E)**2-R(7,8)*R(65,64)*v0)
    keep('all_first_path_normr_under3',9-R(65,64)*v0-8*(1+R(3,8)*E)**2)
    keep('first_phase_squared_root',phi1**2-2*(1+rho1)*beta_prime*E)
    keep('first_all_scaled_paths_ball4over25',ball1-(rad1+phi1+3*E)**2)
    keep('first_complete_maclaurin_scale',t1**2-ball1/6)
    keep('first_complete_gradient1over5',g1-sum((R(k+1,8)*t1**k for k in range(8)),R(0)))
    keep('first_complete_hessian1over16',h1-sum((R((k+1)*(k+2),56)*t1**k for k in range(7)),R(0)))
    U1=1/(8*(1-t1)**2)-R(1,8)-t1/4
    keep('first_signed_real_gradient1over10',R(1,8)-(rho1+15*E)/28-U1-R(1,10))
    keep('first_phase_cosine18eta',18-2*beta_prime)
    keep('first_complex_phase_radial_sign',R(1,10)*(1-E)*(1-18*E)-h1/8)
    keep('first_real_normalized_skew_v11',R(1,11)**2-v0/14)

    # Whole nonnegative first Newton stream, full exact gap retained.
    p1={0:[R(1)],1:[R(0)],2:[0,R(1,2)],3:[0,R(1,11)],4:[0,0,R(3,32)]}
    for k in range(5,8):
        p1[k]=scale(add([0]+p1[k-2],scale([0]+p1[k-3],R(3,11)),
                       *[scale([0,0]+p1[k-s],R(7,8)*rho1**(s-4)) for s in range(4,k+1)]),R(1,k))
    c1=R(27,56)-sum(((1-R((-1)**k,math.comb(8,k)))*value(p1[k],v0)/v0 for k in range(3,8)),R(0))
    B1=11*g1+6+phase_prime*h1/2
    keep('first_full_radial_gap_positive',c1)
    keep('first_actual_variance_under34eta',34*c1-B1)
    keep('first_actual_entry_v1over350',R(1,350)-34*E)

    # New second receiving region, all path and product margins.
    v2=R(1,350);rho_x2=R(1,20);rho_path2=R(51,1000)
    rad2=R(11,200);phi2=R(1,25)
    ball2=R(1,100);t2=R(1,24);g2=R(1,7);h2=R(1,24);pg2=R(16,15)
    keep('second_real_radial_root',rad2**2-R(65,64)*34*E-8*mu_cap**2*E**2)
    keep('second_individual_radius',(rho_path2-mu_cap*E)**2-R(7,8)*R(65,64)*34*E)
    keep('second_normalized_x_radius',rho_x2**2-R(7,8)*v2)
    keep('second_phase_squared_root',phi2**2-2*(1+rho_path2)*beta_prime*E)
    keep('second_all_scaled_paths_ball1over100',ball2-(rad2+phi2+3*E)**2)
    keep('second_complete_maclaurin_scale',t2**2-ball2/6)
    keep('second_complete_gradient1over7',g2-sum((R(k+1,8)*t2**k for k in range(8)),R(0)))
    keep('second_complete_hessian1over24',h2-sum((R((k+1)*(k+2),56)*t2**k for k in range(7)),R(0)))
    keep('second_real_product_gradient16over15',pg2-((7+rho_path2+3*E)/7)**7)
    p2={0:[R(1)],1:[R(0)],2:[0,R(1,2)],3:[0,rho_x2/3],4:[0,0,R(3,32)]}
    for k in range(5,8):
        p2[k]=scale(add(*[scale([0]+p2[k-s],rho_x2**(s-2)) for s in range(2,k+1)]),R(1,k))
    c2=R(27,56)-sum(((1-R((-1)**k,math.comb(8,k)))*value(p2[k],v2)/v2 for k in range(3,8)),R(0))
    B2=11*g2+3*pg2+phase_prime*h2/2
    Av=B2/c2;Ar=R(65,64)*Av
    for stream in [p1,p2]:
        if any(any(c<0 for c in p) for p in stream.values()):
            raise ValueError('whole Newton stream has a negative coefficient')
    keep('second_full_radial_gap_positive',c2)
    keep('actual_reciprocal_norm_under34eta',34-Ar-2*beta-8*mu_cap**2*E)
    keep('actual_each_reciprocal_radius27over28',(R(1,28)-mu_cap*E)**2-R(7,8)*Ar*E)
    keep('sqrt34_under35over6',R(35,6)**2-34)
    keep('sqrt8eta_under13over500',R(13,500)**2-8*E)
    keep('actual_energy_under37eta',37-(R(490,81)+R(13,500))**2)
    keep('actual_absolute_energy_h1over320',R(1,320)-37*E)

    # Receiving actual original root circles and complete cube-normal errors.
    hm=R(1,320);rhoc=R(1,50);tau=R(21,400);rzero=R(9997,10000);Lc=R(1,2)
    rminus=1-E-rhoc;rplus=1+rhoc;sc=rplus+Lc*hm
    Aj={j:R(9,8*j)*math.comb(8,9-j)*rhoc**(7-j) for j in range(1,7)}
    Aj[7]=R(9,14)
    Cd=sum((j*Aj[j]*sc**(j-1) for j in Aj),R(0))
    Bd=9*rminus**8-36*sc**7*Lc*hm-Cd*hm
    Nc=R(7,4)*sum((Aj[j]*rplus**j for j in [1,2,4,5,7]),R(0))
    Be=4*sc**7/(25*rminus**8)+Cd/(45*rminus**8)
    Bj={5:R(63,32),4:R(63,32)*rhoc,2:R(9,128)*rhoc*hm,1:R(9,4096)*hm**2}
    bp=(1+2*rhoc)*Be+R(1,50)+sum((Bj[j]*rminus**(j-7) for j in Bj),R(0))/6
    bi=(1+2*rhoc)*Be+R(1,50)+sum((Bj[j]*rminus**(j-7) for j in Bj),R(0))/5
    keep('centered_mean_radius',8*rhoc**2-hm)
    keep('centered_zero_sum_tail_radius',tau**2-R(7,8)*hm)
    keep('all9_full_original_Rouche',9*rminus**8*Lc-36*sc**7*Lc**2*hm-sum((Aj[j]*(sc**j+rplus**j) for j in Aj),R(0)))
    keep('all9_original_circles_disjoint',R(4,9)*rminus-2*Lc*hm)
    keep('full_original_root_divisor',Bd)
    keep('full_true_cube_displacement_Wover5',Bd/5-Nc)
    keep('full_linear_cube_displacement_Wover5',9*rminus**8/5-Nc)
    keep('complete_paired_actual_normal4over5',R(4,5)-bp)
    keep('complete_individual_actual_normal7over8',R(7,8)-bi)
    keep('whole_Legendre_radius_below_rminus',rminus-tau)
    keep('whole_Legendre_first_coefficient3over5',R(3,5)-1/(2*rminus**3)-tau/((rminus-tau)*rminus**3))
    keep('receiving_radial_lower_rzero',1-rzero-(3*E+R(3,5)*hm)/8)
    keep('retained_Q_coefficient_positive',R(3,4)/rplus**3-R(4,7))
    betac=R(4,7)-1/(2*rzero**3)-tau/((rzero-tau)*rzero**3)
    kappa=betac-R(976,225)*hm
    keep('retained_square_variance_kappa1over600',kappa-R(1,600))
    fullsquare={(2,0):R(4),(1,1):R(-16,15),(0,2):R(-64,15)}
    expanded={(2,0):R(4),(1,1):R(-16,15),(0,2):4*R(2,15)**2-R(976,225)}
    if fullsquare!=expanded:
        raise ValueError('whole mean-square coefficient identity differs')

    # Whole exact cube-field coefficients, not a numerical phase sample.
    def cmul(x,y):
        c=x[1]*y[1]
        return (x[0]*y[0]-c,x[0]*y[1]+x[1]*y[0]-c)
    def cpow(n):
        z=(R(1),R(0))
        for _ in range(n):z=cmul(z,(R(0),R(1)))
        return z
    cube=[]
    for j in range(1,8):
        z=cpow(j);zc=cpow(2*j)
        normal=( -(z[0]-1)/9,-z[1]/9 )
        pair=( -(z[0]+zc[0]-2)/18,-(z[1]+zc[1])/18 )
        require(pair==(R(0) if j%3==0 else R(1,6),R(0)),"full cube pair coefficient")
        norm2=normal[0]**2-normal[0]*normal[1]+normal[1]**2
        require(norm2==(0 if j%3==0 else R(1,27)),"full cube individual norm")
        cube.append({"j":j,"omega_power":z,"omega_conjugate_power":zc,
                     "full_individual_coefficient":normal,"full_pair_coefficient":pair,"individual_norm_squared":norm2})
    require(R(-9,14)*cube[6]["full_pair_coefficient"][0]==R(-3,28),"principal signed paired normal")
    keep('individual_cube_field_weight1over5',R(1,25)-R(1,27))

    # Whole two-level real moment controls cover all seven Lagrange levels.
    skew=[]
    for k in range(1,8):
        x=[R(8-k)]*k+[R(-k)]*(8-k)
        pv=sum(t*t for t in x);p3=sum(t**3 for t in x)
        ratio=R(p3*p3,pv**3)
        formula=R((8-2*k)**2,8*k*(8-k))
        require(sum(x)==0 and ratio==formula and ratio<=R(9,14),"whole two-level skew")
        skew.append({"level":k,"whole_tuple":x,"variance":pv,"third_moment":p3,"squared_skew_ratio":ratio})

    # Complete Gaussian origin/gradient/ordered Hessian/Newton controls.
    controls=[literal_control("total_collision",[ga(1)]*8,R(1)),
              literal_control("unequal_real",[ga(R(9,8))]+[ga(R(55,56))]*7,1-E),
              literal_control("complex_unrestricted",[ga(R(21,20),R(1,40)),ga(R(19,20),R(-1,100)),
                             ga(R(41,40),R(1,200)),ga(R(39,40),R(1,300))]+[ga(1)]*4,1-E)]
    negative={"first33eta_target":33*c1-B1,
              "discarded_mean_on_receiving_domain":betac-R(16,3)*(rhoc/5+R(4,5)*hm)}
    require(all(x<0 for x in negative.values()),"rejected mathematical shortcut unexpectedly positive")
    nonnegative={'second_normalized_x_radius'}
    for name,margin in budget.items():
        require(margin>=0 if name in nonnegative else margin>0,"receiving budget failed "+name)
    return {'agent':'six-sendov-1','role':'researcher','status':'complete ordinary unformalized author proof; independently unreviewed',
            'eta_endpoint':E,'sigma':sigma,'whole_polar':old,'polar_certificates':polar_bounds,'whole_faces':faces,
            'first_whole_Newton_stream':p1,'second_whole_Newton_stream':p2,
            'complete_constants':{'beta':beta,'beta_prime':beta_prime,'phase_prime':phase_prime,
              'phase_all':phase_all,'global_cost':global_cost,'d0':d0,'first_gap':c1,'first_cost':B1,
              'second_gap':c2,'second_cost':B2,'Av':Av,'Ar':Ar,'mean_absorption':betac,'kappa':kappa,
              'first_actual_v_coefficient':34,'second_moment_rho':rho_x2,'second_path_rho':rho_path2,
              'root_h':hm,'root_rho':rhoc,'centered_tau':tau,'rzero':rzero,
              'Aj':Aj,'Bj':Bj,'Cd':Cd,'Bd':Bd,'Nc':Nc,'Be':Be,'paired_bp':bp,'individual_bi':bi},
            'whole_mean_square':{'lhs':[[i,j,c] for (i,j),c in sorted(fullsquare.items())],
                                 'expanded_rhs':[[i,j,c] for (i,j),c in sorted(expanded.items())]},
            'all_full_window_margins':budget,'nonnegative_closed_case':sorted(nonnegative),
            'whole_cube_field':cube,'all_seven_real_skew_controls':skew,
            'whole_literal_controls':controls,'rejected_mathematical_budgets':negative}

def stringify(obj):
    if isinstance(obj,R):return str(obj)
    if isinstance(obj,dict):return {str(k):stringify(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)):return list(map(stringify,obj))
    return obj

def duplicate_guard(pairs):
    out={}
    for key,value in pairs:
        require(key not in out,"duplicate JSON key")
        out[key]=value
    return out

def invalid_numeric(value):raise ValueError("floating or nonfinite JSON token")

def load(path):
    return json.loads(path.read_text(),object_pairs_hook=duplicate_guard,
                      parse_float=invalid_numeric,parse_constant=invalid_numeric)

def canonical(record):
    return json.dumps(record,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--expected",type=Path,default=ROOT/"EXPECTED.json")
    p.add_argument("--export",type=Path)
    p.add_argument("--bootstrap",action="store_true",help="explicit author-only frozen record regeneration")
    args=p.parse_args()
    record=stringify(build_record())
    if args.bootstrap:
        (ROOT/"EXPECTED.json").write_text(json.dumps(record,indent=2)+"\n")
    else:
        manifest=load(ROOT/"MANIFEST.json")
        require(canonical(sorted(manifest['sha256']))==canonical(sorted(FILES)),"whole source manifest coverage")
        for name in FILES:
            require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==manifest['sha256'][name],"source pin mismatch "+name)
        require(canonical(load(args.expected))==canonical(record),"entire typed exact record mismatch")
    if args.export:args.export.write_bytes(canonical(record))
    print(json.dumps({'status':'PASS','eta_endpoint':record['eta_endpoint'],
           'whole_record_sha256':hashlib.sha256(canonical(record)).hexdigest(),
           'whole_polar_coefficients':sum(len(x['whole_polynomial']) for x in record['polar_certificates'].values()),
           'all_penalty_faces':len(record['whole_faces']),
           'full_receiving_margins':len(record['all_full_window_margins']),
           'whole_cube_coefficients':len(record['whole_cube_field']),
           'all_real_skew_controls':len(record['all_seven_real_skew_controls']),
           'whole_complex_controls':len(record['whole_literal_controls'])}))

if __name__=="__main__":main()
