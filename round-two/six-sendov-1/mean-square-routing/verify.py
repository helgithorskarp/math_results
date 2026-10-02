#!/usr/bin/env python3
"""Whole exact algebra and full-window budgets; ordinary universal bridges in PROOF.md.
Unchanged Gaussian/product helpers credited to own9731/9776; no peer code/data imported."""
import argparse
from fractions import Fraction as R
from math import comb, factorial
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
E = R(1, 16000)
EPS = R(1, 9)
A = 4 + 3*E
FILES = ['.gitignore', 'PROOF.md', 'README.md', 'LITERATURE.md',
         'verify.py', 'validate.py', 'EXPECTED.json']

def require(condition, message):
    if not condition:
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

def beta(i,j):
    return R(factorial(i)*factorial(j),factorial(i+j+1))

def sector(m,s,k):
    radial=R(1,2)+A/k if k else R(1)
    lower=1/radial if k else R(0)
    p=pmul(ppow([1,R(-1,2)],m-k),ppow([-1,radial],k)) if k else ppow([1,R(-1,2)],m)
    first=9*sum((v*(1-lower**(i+s+1))/R(i+s+1) for i,v in enumerate(p)),R(0))
    # Positive shifted Bernstein/beta evaluation; no monomial coefficients used.
    second=R(0)
    for j in range(m-k+1):
        for l in range(s+1):
            second+=comb(m-k,j)*comb(s,l)*(1-lower/2)**(m-k-j)*R(1,2)**j*lower**(s-l)*beta(k+j+l,m-k-j+s-l)
    second*=9*(1-lower)*((radial-1)**k if k else 1)
    require(first==second,'whole sector integral mismatch')
    require(first>=0,'negative sector integral')
    return {'k':k,'radial':str(radial),'support_lower':str(lower),
            'whole_polynomial':[str(v) for v in p], 'monomial_integral':str(first),
            'positive_bernstein_integral':str(second)}

def ga(a,b=0):return (R(a),R(b))
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def mul(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def scale(x,t):return (x[0]*t,x[1]*t)
def gp(q,a):
    p=[ga(1)]
    for v in q:
        out=[ga(0)]*(len(p)+1)
        for j,c in enumerate(p):
            out[j]=add(out[j],c)
            out[j+1]=add(out[j+1],scale(mul(c,v),-a))
        p=out
    return p
def symmetric(q):
    e=[ga(1)]+[ga(0)]*len(q)
    for n,v in enumerate(q,1):
        for k in range(n,0,-1):e[k]=add(e[k],mul(v,e[k-1]))
    return e
def gint(p,shift,factor):
    out=ga(0)
    for j,c in enumerate(p):out=add(out,scale(c,R(factor,j+shift+1)))
    return out
def enc(x):return [str(x[0]),str(x[1])]

def literal_control(name,q,a):
    direct=gint(gp(q,a),0,9)
    e=symmetric(q);alternative=ga(0)
    for k,c in enumerate(e):alternative=add(alternative,scale(c,R(9,k+1)*(-a)**k))
    require(direct==alternative,'complete origin control mismatch')
    gradients=[];hessians=[]
    for i in range(8):
        rest=q[:i]+q[i+1:]
        gd=scale(gint(gp(rest,a),1,9),-a)
        es=symmetric(rest); ge=ga(0)
        for k,c in enumerate(es,1):ge=add(ge,scale(c,R(9,k+1)*(-a)**k))
        require(gd==ge,'complete first derivative control mismatch')
        gradients.append(enc(gd))
        row=[]
        for j in range(8):
            if i==j:
                row.append(enc(ga(0)));continue
            rest2=[v for n,v in enumerate(q) if n not in (i,j)]
            hd=scale(gint(gp(rest2,a),2,9),a*a)
            es2=symmetric(rest2);he=ga(0)
            for k,c in enumerate(es2,2):he=add(he,scale(c,R(9,k+1)*(-a)**k))
            require(hd==he,'complete mixed derivative control mismatch')
            row.append(enc(hd))
        hessians.append(row)
    mean=ga(0)
    for z in q:mean=add(mean,scale(z,R(1,8)))
    x=[add(z,scale(mean,-1)) for z in q]
    esx=symmetric(x);traces=[ga(8)]
    for k in range(1,9):
        value=ga(0)
        for z in x:
            zk=ga(1)
            for _ in range(k):zk=mul(zk,z)
            value=add(value,zk)
        traces.append(value)
    require(esx[1]==ga(0),'centered trace control')
    for k in range(2,9):
        rhs=ga(0)
        for s in range(2,k+1):rhs=add(rhs,scale(mul(esx[k-s],traces[s]),(-1)**(s-1)))
        require(scale(esx[k],k)==rhs,'whole centered Newton identity')
    require(esx[4]==add(scale(mul(traces[2],traces[2]),R(1,8)),scale(traces[4],R(-1,4))),'complete fourth Newton cancellation')
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
def polar_record():
    a=[R(1),R(-1)];b=padd([R(1)],pscale(ppow(a,2),-1));L=[R(8),R(3)]
    d=pscale(pmul(ppow(a,7),b),R(1,2));T=[R(0)]
    for k in range(2,9):
        T=padd(T,pscale(pmul(pmul(ppow(a,8-k),ppow(b,k)),ppow(pscale(L,R(1,8)),k)),R(comb(8,k),k+1)))
    B=padd(ppow(a,8),pmul(d,L),T)
    mean=padd([R(1)],pscale(ppow(a,16),-1),pscale(pmul(ppow(d,2),ppow(L,2)),-1),
              pscale(pmul(padd(ppow(a,8),pmul(d,L)),T),-2),pscale(ppow(T,2),-1),
              pscale(pmul([R(8),R(-6)],pmul(ppow(a,15),b)),-1))
    modulus=padd([R(1),R(0),R(9)],pscale(B,-1))
    variance=padd(pscale(pmul(ppow(a,6),ppow(b,2)),13),pscale(padd(B,[R(-1)]),-6))
    factor={(i,0):c for i,c in enumerate(a) if c}
    for i,c in enumerate(pmul(b,pscale(L,R(1,8)))):
        if c:factor[i,1]=c
    raw={(0,0):R(1)}
    for _ in range(8):raw=bmul(raw,factor)
    direct=[R(0)]*(max(i for i,t in raw)+1)
    for (i,t),c in raw.items():direct[i]+=c/(t+1)
    require(direct==B,'whole polar balanced integration identity')
    require(padd(direct,pscale(ppow(a,8),-1),pscale(pmul(d,L),-1))==T,'whole polar higher tail identity')
    certs={}
    for name,p,head,threshold in [('mean',mean,R(4,3),R(1)),('modulus',modulus,R(2,3),R(1,2)),('variance',variance,R(2),R(1))]:
        require(p[:2]==[0,0] and p[2]==head,'whole polar cancellation '+name)
        certs[name]={'polynomial':p,'head':head,'threshold':threshold}
    return {'whole_balanced_integral':list(map(str,B)), 'whole_tail':list(map(str,T)),
            'scalar_certificates':certs}

def build_record():
    e=E;eps=EPS
    margins={}
    def c(n,x):margins[n]=x
    rec=polar_record()
    for n,z in rec['scalar_certificates'].items():
     p=z['polynomial'];c('complete_polar_'+n,z['head']-sum((abs(x)*e**(k-2) for k,x in enumerate(p) if k>=3),R(0))-z['threshold'])
    sectors={}
    for m,s in [(7,1),(6,2)]:
     rows=[sector(m,s,k) for k in range(m+1)];real=sum((R(v['monomial_integral']) for v in rows),R(0))/(1-e)
     correction=36*sum((eps**k/R(factorial(k)*(s+k+1)) for k in range(1,m+1)),R(0))/(1-e)
     sectors[f'{m}:{s}']={'all_sectors':rows,'real':str(real),'correction':str(correction),'complex':str(real+correction)}
     c('real_gradient_7over5',R(7,5)-real) if m==7 else None
     c('complex_gradient_14over5',R(14,5)-real-correction) if m==7 else c('complex_hessian_7over3',R(7,3)-real-correction)
    c('whole_phase_eps',eps**2-161*e);c('phase_cost_real_dominates_hessian',R(7,5)-R(7,6));c('product_grad2',2-(R(15,14)+3*e/7)**7)
    c('whole_origin253eta',253-(160*R(7,5)+6*(R(14,5)+2)))
    # Eight COMPLETE near-boundary radial face polynomials, using bivariate eta,t.
    a=[R(1),R(-1)];floor={(0,0):R(2),(1,0):R(-1),(0,1):R(-1),(1,1):R(1)}
    faces=[]
    for m in range(1,9):
     free=dict(floor)
     for j,x in enumerate(ppow(a,2)):free[(j,1)]=free.get((j,1),R(0))-R(8,m)*x
     prod={(0,0):R(1)}
     for k in range(8):prod=bmul(prod,free if k<m else floor)
     op=[R(0)]*(max(i for i,j in prod)+1)
     for (i,j),x in prod.items():op[i]+=9*x/R(j+1)
     dm=R(64*(m-1),m)-R(256*(m-1)*(m-2),3*m*m)
     residual=padd(op,pscale(ppow([1+R(8,m),R(-8,m)],m),-1),[-8],pscale(ppow(a,9),8),pscale(ppow(a,3),-R(39,5)*dm))
     # Second WHOLE algebra route: expand only the extra free-factor term,
     # then the common floor factor and integrate every t power.
     alt=[R(0)]
     for ell in range(m+1):
      for j in range(9-ell):
       term=pscale(pmul(ppow([2,-1],8-ell-j),ppow(a,2*ell+j)),R(9,ell+j+1)*comb(m,ell)*comb(8-ell,j)*R(-8,m)**ell*(-1)**j)
       alt=padd(alt,term)
     require(op==alt,'entire radial face origin routes differ')
     leading=next(i for i,x in enumerate(residual) if x)
     low=residual[leading]-sum((abs(x)*e**(k-leading) for k,x in enumerate(residual) if k>leading),R(0))
     c('radial_face_'+str(m),low)
     faces.append({'m':m,'whole_scaled_origin':[str(x) for x in op],'whole_residual':[str(x) for x in residual],'leading_degree':leading,'lower':str(low),'defect_coefficient':str(dm)})
    # Every coarse bootstrap step starts from actual global variance<13.
    d0=R(256*253*5,39)
    c('initial_E2_over7over4',28*(1-e)**2-26-R(7,4))
    steps=[(8,5,17),(R(14,17),R(43,100),27),(R(14,27),R(27,100),None)]
    for i,(factor,ball,e2) in enumerate(steps):
     c('bootstrap_var_'+str(i),ball-factor*d0*e)
     if e2 is not None:c('bootstrap_E2_'+str(i),28*(1-e)**2-2*ball-e2)
    v0=R(27,100);rho1=R(1,2);t1=R(6,25)
    c('first_radial_squared_7over25',R(7,25)-R(65,64)*v0-R(9,2)*e**2)
    c('first_individual_radius', (rho1-R(3,4)*e)**2-R(7,8)*R(65,64)*v0)
    c('first_radial_root53over100',R(53,100)**2-R(7,25))
    c('first_phase_root9over200',R(9,200)**2-30*e)
    c('first_whole_ball1over3',R(1,3)-(R(53,100)+R(9,200)+3*e)**2)
    c('first_maclaurin_scale',t1**2-R(1,3)/6)
    g1=R(2,9);h1=R(1,12)
    c('first_gradient2over9',g1-sum((R(k+1,8)*t1**k for k in range(8)),R(0)))
    c('first_hessian1over12',h1-sum((R((k+1)*(k+2),56)*t1**k for k in range(7)),R(0)))
    tail=1/(8*(1-t1)**2)-R(1,8)-t1/4
    c('first_signed_gradient3over40',R(1,8)-(rho1+15*e)/28-tail-R(3,40))
    c('first_complex_samephase_sign',R(3,40)*(1-e)*(1-20*e)-h1*eps)
    c('first_skew_factor1over7',R(1,7)**2-v0/14)
    b1={0:R(1),1:R(0),2:v0/2,3:v0/7,4:R(3,32)*v0*v0}
    for k in range(5,8):b1[k]=(v0*b1[k-2]+R(3,7)*v0*b1[k-3]+R(7,8)*v0*v0*sum((rho1**(s-4)*b1[k-s] for s in range(4,k+1)),R(0)))/k
    gap1=R(27,56)-sum(((1-R((-1)**k,comb(8,k)))*b1[k]/v0 for k in range(3,8)),R(0))
    c('first_full_gap1over6',gap1-R(1,6))
    B1=11*g1+6+80*h1
    c('first_var_under91eta',91-6*B1);c('first_entry1over128',R(1,128)-6*B1*e)
    # Second local region: all new radial, phase, scale, product and sign budgets.
    v2=R(1,128);rho2=R(1,10);t2=R(1,18);g2=R(1,7);h2=R(1,23);pg2=R(10,9)
    c('second_radial_root9over100',R(9,100)**2-R(65,64)*v2-R(9,2)*e**2)
    c('second_individual_radius',(rho2-R(3,4)*e)**2-R(7,8)*R(65,64)*v2)
    c('second_phase_root3over80',R(3,80)**2-22*e)
    c('second_whole_ball1over60',R(1,60)-(R(9,100)+R(3,80)+3*e)**2)
    c('second_maclaurin_scale',t2**2-R(1,60)/6)
    c('second_gradient1over7',g2-sum((R(k+1,8)*t2**k for k in range(8)),R(0)))
    c('second_hessian1over23',h2-sum((R((k+1)*(k+2),56)*t2**k for k in range(7)),R(0)))
    c('second_product10over9',pg2-(R(71,70)+3*e/7)**7)
    b2={0:R(1),1:R(0),2:v2/2,3:rho2*v2/3,4:v2*v2/8}
    for k in range(5,8):b2[k]=v2*sum((rho2**(s-2)*b2[k-s] for s in range(2,k+1)),R(0))/k
    gap2=R(27,56)-sum(((1-R((-1)**k,comb(8,k)))*b2[k]/v2 for k in range(3,8)),R(0))
    c('second_full_gap4over9',gap2-R(4,9))
    B2=11*g2+3*pg2+80*h2
    c('Vr_under77over4eta',R(77,4)-R(65,64)*B2*R(9,4))
    c('actual_reciprocal_norm_under38eta',38-R(77,4)-18-R(9,2)*e)
    c('actual_radius24over25',(R(1,25)-R(3,4)*e)**2-R(539,32)*e)
    c('sqrt38_under37over6',R(37,6)**2-38)
    c('sqrt8eta_under9over400',R(9,400)**2-8*e)
    c('actual_energy42eta',42-(R(925,144)+R(9,400))**2)
    c('absoluteH_entry1over375',R(1,375)-42*e)

    # Earlier polar transfer conditions remain required and are recomputed.
    c('a_over255over256',R(1,256)-e)
    c('transfer65over64',R(65,64)-R(256,255)**2)
    c('delta10',10-9*(1+R(3,2)*e))
    for k in range(9):require(9*beta(k,8-k)==R(1,comb(8,k)),'complete radial beta coefficient')
    for k in range(8):require(9*comb(7,k)*beta(k+1,7-k)==R(k+1,8),'complete gradient beta coefficient')
    for k in range(7):require(9*comb(6,k)*beta(k+2,6-k)==R((k+1)*(k+2),56),'complete Hessian beta coefficient')
    # Complete first/second nonnegative majorant polynomial streams.
    firstpoly={0:[R(1)],1:[R(0)],2:[0,R(1,2)],3:[0,R(1,7)],4:[0,0,R(3,32)]}
    secondpoly={0:[R(1)],1:[R(0)],2:[0,R(1,2)],3:[0,rho2/3],4:[0,0,R(1,8)]}
    for k in range(5,8):
     firstpoly[k]=pscale(padd([0]+firstpoly[k-2],pscale([0]+firstpoly[k-3],R(3,7)),*[pscale([0,0]+firstpoly[k-s],R(7,8)*rho1**(s-4)) for s in range(4,k+1)]),R(1,k))
     secondpoly[k]=pscale(padd(*[pscale([0]+secondpoly[k-s],rho2**(s-2)) for s in range(2,k+1)]),R(1,k))
    for polys,endpoint,values in [(firstpoly,v0,b1),(secondpoly,v2,b2)]:
     for k,p in polys.items():
      require(all(x>=0 for x in p),'negative majorant coefficient')
      if k>=2:require(p[0]==0,'majorant variance division is a polynomial')
      require(pvalue(p,endpoint)==values[k],'entire majorant endpoint differs')
    # NEW fixed-energy mechanism: preserve the mean-square until completing it.
    hm=R(1,375);rho=R(1,54);tau=R(1,19);rzero=R(3999,4000);Lcircle=R(1,2);dcube=R(1,5)
    rminus=1-e-rho;rplus=1+rho;s=rplus+Lcircle*hm
    aj={j:R(9,8*j)*comb(8,9-j)*rho**(7-j) for j in range(1,7)};aj[7]=R(9,14)
    cd=sum((j*aj[j]*s**(j-1) for j in aj),R(0))
    bd=9*rminus**8-36*s**7*Lcircle*hm-cd*hm
    nc=R(7,4)*sum((aj[j]*rplus**j for j in (1,2,4,5,7)),R(0))
    be=4*s**7*dcube**2/rminus**8+cd*dcube/(9*rminus**8)
    bj={5:R(63,32),4:R(63,32)*rho,2:R(9,128)*rho*hm,1:R(9,4096)*hm**2}
    betac=R(4,7)-R(1,2)/rzero**3-tau/((rzero-tau)*rzero**3)
    kappa=betac-R(1216,225)*hm
    for name,value in {
     'fixed_RMS_and_mean_bound':8*rho**2-hm,'fixed_centered_tau':tau**2-hm,
     'fixed_rminus_tau_positive':rminus-tau,
     'fixed_full_Rouche':9*rminus**8*Lcircle-36*s**7*Lcircle**2*hm-sum((aj[j]*(s**j+rplus**j) for j in aj),R(0)),
     'fixed_nine_circle_separation':R(4,9)*rminus-2*Lcircle*hm,'fixed_positive_Bd':bd,
     'fixed_cube_displacement':dcube*bd-nc,'fixed_cube_linear_displacement':dcube*9*rminus**8-nc,
     'fixed_full_pair_normal':1-(1+2*rho)*be-dcube**2/2-R(1,6)*sum((bj[j]*rminus**(j-7) for j in bj),R(0)),
     'fixed_full_individual_normal':1-(1+2*rho)*be-dcube**2/2-R(1,5)*sum((bj[j]*rminus**(j-7) for j in bj),R(0)),
     'fixed_initial_tail3over5':R(3,5)-R(1,2)/rminus**3-tau/((rminus-tau)*rminus**3),
     'fixed_initial_rzero':1-rzero-(3*e+R(3,5)*hm)/8,
     'fixed_Q_coefficient_sign':R(3,4)/rplus**3-R(4,7),
     'fixed_retained_mean_divisor1over1000':kappa-R(1,1000),
     'fixed_slope13over5':R(8,3)-R(4,3)*e-R(13,5),
    }.items():c(name,value)
    # Entire two-variable square, both coefficients and Gaussian evaluations.
    square={ (2,0):R(4),(1,1):R(-16,15),(0,2):R(-16,3)}
    expanded={(2,0):R(4),(1,1):R(-16,15),(0,2):4*R(2,15)**2-R(1216,225)}
    require(square==expanded,'whole retained-mean square identity')
    square_controls=[]
    for t,w in [(R(0),R(0)),(R(1,54),R(1,375)),(R(2,5625),R(1,375)),(R(1,1000),R(1,10000))]:
     lhs=4*t*t-R(16,15)*t*w-R(16,3)*w*w;rhs=4*(t-R(2,15)*w)**2-R(1216,225)*w*w
     require(lhs==rhs,'retained-mean square control');square_controls.append({'t':t,'W':w,'left':lhs,'right':rhs})
    skew_controls=[]
    for k in range(1,8):
     x=[R(8-k)]*k+[R(-k)]*(8-k);v=sum((z*z for z in x),R(0));p3=sum((z**3 for z in x),R(0));ratio=p3*p3/v**3
     require(sum(x)==0 and ratio==R((8-2*k)**2,8*k*(8-k)),'whole two-level skew identity')
     require(ratio<=R(9,14),'eight-slot skew maximum')
     skew_controls.append({'positive_count':k,'whole_tuple':list(map(str,x)),'variance':v,'p3':p3,'skew_ratio_squared':ratio})
    balanced_e4=[ga(1)]*4+[ga(-1)]*4;require(symmetric(balanced_e4)[4]==ga(6),'fourth-moment sharp control')
    controls=[literal_control('balanced',[ga(1)]*8,R(1)),literal_control('new_band_balanced',[ga(1)]*8,1-E),literal_control('wide_floor_variance',[ga(R(3,4)),ga(R(17,4))]+[ga(R(1,2))]*6,R(1)),literal_control('zero_coordinates',[ga(0)]*8,1-E),literal_control('full_gaussian',[ga(R(3,4)+R(j,20),R((j%3)-1,30)) for j in range(8)],1-E),literal_control('mixed_collisions',[ga(1,R(1,10))]*4+[ga(1,R(-1,10))]*4,R(3,4)),literal_control('extremal_positive_fourth',balanced_e4,R(1))]
    damages={
     'old_phase_eps1over10':R(1,100)-161*E,
     'complex_gradient5over2':R(5,2)-R(sectors['7:1']['complex']),
     'first_radial_gap1over4':gap1-R(1,4),'second_radial_gap9over20':gap2-R(9,20),
     'old_absoluteH1over512':R(1,512)-42*E,'old_cube_delta1over6':bd/6-nc,
     'discarded_mean_divisor':betac-R(16,3)*(rho*dcube+hm),
     'penalty8_at_m2_a1':R(faces[1]['whole_residual'][0])-R(1,5)*R(faces[1]['defect_coefficient']),
     'global_gradient_negative':-R(controls[2]['all_eight_gradients'][0][0]),
     'skew_square_cap1over2':R(1,2)-R(9,14),'e4_v_squared_over16':R(1,16)*64-6,
    }
    for name,value in margins.items():require(value>0,'strict whole-window margin failed: '+name)
    for name,value in damages.items():require(value<=0,'mathematical counter-budget not rejected: '+name)
    def strings(value):
     if isinstance(value,R):return str(value)
     if isinstance(value,dict):return {str(k):strings(v) for k,v in value.items()}
     if isinstance(value,list):return list(map(strings,value))
     return value
    return strings({'version':1,'agent':'six-sendov-1','role':'researcher','eta_endpoint':E,
     'whole_polar':rec,'whole_envelopes':sectors,'whole_radial_faces':faces,'strict_full_window_margins':margins,
     'whole_radial_gap_coefficients':[R((-1)**k,comb(8,k))-1 for k in range(2,9)],
     'first_majorant_polynomials':firstpoly,'second_majorant_polynomials':secondpoly,'first_majorants':b1,'second_majorants':b2,
     'first_gap':gap1,'second_gap':gap2,'B1':B1,'B2':B2,'whole_skew_controls':skew_controls,'whole_literal_controls':controls,
     'whole_mean_square_coefficients':{str(k):v for k,v in square.items()},'mean_square_controls':square_controls,
     'local_basic_coefficients':{'A':aj,'Cd':cd,'Bd':bd,'Nc':nc,'errorB':be,'Bj':bj,'beta':betac,'kappa':kappa},
     'rejected_mathematical_budgets':damages})

def duplicate_guard(pairs):
    out={}
    for k,v in pairs:
        require(k not in out,'duplicate JSON key')
        out[k]=v
    return out
def no_float(value):raise ValueError('floating/nonfinite fixture token')
def load(path):
    return json.loads(path.read_text(),object_pairs_hook=duplicate_guard,
                      parse_float=no_float,parse_constant=no_float)
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--fixture',type=Path,default=ROOT/'EXPECTED.json')
    parser.add_argument('--export',type=Path)
    parser.add_argument('--bootstrap',action='store_true')
    args=parser.parse_args()
    if not args.bootstrap:
        manifest=load(ROOT/'MANIFEST.json')
        expected_manifest={'schema':'mean-square-routing-source-v1',
                           'agent':'six-sendov-1','role':'researcher',
                           'sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in FILES},
                           'bytes':{f:(ROOT/f).stat().st_size for f in FILES}}
        require(canonical(manifest)==canonical(expected_manifest),'entire source pin manifest mismatch')
    record=build_record()
    if args.export:
        args.export.write_text(json.dumps(record,indent=2)+'\n')
    elif canonical(load(args.fixture))!=canonical(record):
        raise ValueError('entire typed expected record mismatch')
    print(json.dumps({'status':'PASS','whole_record_sha256':hashlib.sha256(canonical(record)).hexdigest(),
                      'complete_sector_integrals':15,'complete_radial_faces':8,'strict_window_margins':len(record['strict_full_window_margins']),
                      'whole_literal_controls':len(record['whole_literal_controls']),
                      'whole_skew_controls':len(record['whole_skew_controls']),
                      'rejected_mathematical_budgets':len(record['rejected_mathematical_budgets'])},sort_keys=True))

if __name__=='__main__':main()
