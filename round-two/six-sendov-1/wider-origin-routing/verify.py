#!/usr/bin/env python3
"""Whole exact algebra and budgets. Ordinary universal bridges are in PROOF.md.
Gaussian/product helpers are credited same-author reuse from9731; no peer code imported."""
import argparse
from fractions import Fraction as R
from math import comb, factorial
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
E = R(1, 25000)
EPS = R(1, 12)
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
    rec = polar_record()
    for k in range(9):
        require(9*beta(k,8-k)==R(1,comb(8,k)), 'complete radial beta coefficient')
    for k in range(8):
        require(9*comb(7,k)*beta(k+1,7-k)==R(k+1,8), 'complete gradient beta coefficient')
    for k in range(7):
        require(9*comb(6,k)*beta(k+2,6-k)==R((k+1)*(k+2),56), 'complete Hessian beta coefficient')
    margins = {}

    def check(name, margin):
        margins[name] = margin

    for name, cert in rec['scalar_certificates'].items():
        p = cert['polynomial']
        lower = cert['head'] - sum((abs(c)*E**(k-2) for k,c in enumerate(p) if k >= 3), R(0))
        check('whole_polar_' + name, lower - cert['threshold'])

    sectors = {}
    for m,s,cap in [(7,1,R(5,2)),(6,2,R(9,4))]:
        rows = [sector(m,s,k) for k in range(m+1)]
        vals = [R(row['monomial_integral']) for row in rows]
        correction = 36*sum((EPS**k/R(factorial(k)*(s+k+1)) for k in range(1,m+1)),R(0))
        full = (sum(vals,R(0))+correction)/(1-E)
        sectors[f'{m}:{s}'] = {'all_sectors':rows, 'whole_real_integral':str(sum(vals,R(0))), 'whole_complex_correction':str(correction), 'full':str(full)}
        check(f'global_derivative_{m}',cap-full)

    check('global_phase_l1_under_eps', EPS**2 - 161*E)
    check('global_product_grad_under2', 2-(R(15,14)+3*E/7)**7)
    check('a_over255over256', R(1,256)-E)
    check('transfer65over64', R(65,64)-R(256,255)**2)
    check('delta10',10-9*(1+R(3,2)*E))

    d0 = R(256*427,5)
    check('initial_E2_over7over4',28*(1-E)**2-26-R(7,4))
    steps=[(8,7,13),(R(14,13),1,25),(R(14,25),R(1,2),26),
           (R(14,26),R(12,25),27),(R(14,27),R(23,50),None)]
    for i,(coef,ball,e2) in enumerate(steps):
        check(f'bootstrap_{i}_variance',ball-coef*d0*E)
        if e2 is not None:check(f'bootstrap_{i}_E2',28*(1-E)**2-2*ball-e2)

    v0 = R(23,50)
    rho1 = R(2,3)
    t1 = R(8,25)
    check('first_radial_norm15over32',R(15,32)-R(65,64)*v0-R(9,2)*E**2)
    check('first_individual_radius', (rho1-R(3,4)*E)**2-R(7,8)*R(65,64)*v0)
    check('first_norm_root11over16',R(11,16)**2-R(15,32))
    check('first_phase_root3over80',R(3,80)**2-R(100,3)*E)
    check('first_whole_ball3over5',R(3,5)-(R(11,16)+R(3,80)+3*E)**2)
    check('first_maclaurin_scale',t1**2-R(3,5)/6)
    check('first_gradient2over7',R(2,7)-sum((R(k+1,8)*t1**k for k in range(8)),R(0)))
    check('first_hessian3over25',R(3,25)-sum((R((k+1)*(k+2),56)*t1**k for k in range(7)),R(0)))
    tail1 = 1/(8*(1-t1)**2)-R(1,8)-t1/4
    check('first_signed_gradient7over200',R(1,8)-(rho1+15*E)/28-tail1-R(7,200))
    check('first_complex_radial_sign',R(7,200)*(1-E)*(1-20*E)-R(3,25)*EPS)

    # New zero-sum skewness and fourth-moment majorants, all higher Newton terms.
    check('skewness_at_first_ball',R(2,11)**2-v0/14)
    def first_majorants(v):
        b = {0:R(1),1:R(0),2:v/2,3:R(2,11)*v,4:R(3,32)*v*v}
        for k in range(5,8):
            b[k] = (v*b[k-2]+R(6,11)*v*b[k-3]+R(7,8)*v*v*sum((rho1**(s-4)*b[k-s] for s in range(4,k+1)),R(0)))/k
        return b
    b1=first_majorants(v0)
    gap1=R(27,56)-sum(((1-R((-1)**k,comb(8,k)))*b1[k]/v0 for k in range(3,8)),R(0))
    check('first_gap_over1over20',gap1-R(1,20))
    B1=R(656,35)
    check('first_var_under375eta',375-20*B1)
    check('first_var_entry1over64',R(1,64)-20*B1*E)

    v2=R(1,64)
    rho2=R(1,8)
    t2=R(1,14)
    check('second_radial_norm_root17over128',R(17,128)**2-R(65,64)*v2-R(9,2)*E**2)
    check('second_individual_radius', (rho2-R(3,4)*E)**2-R(7,8)*R(65,64)*v2)
    check('second_phase_root1over32',R(1,32)**2-R(45,2)*E)
    check('second_whole_ball1over36',R(1,36)-(R(21,128)+3*E)**2)
    check('second_maclaurin_scale',t2**2-R(1,36)/6)
    check('second_gradient3over20',R(3,20)-sum((R(k+1,8)*t2**k for k in range(8)),R(0)))
    check('second_hessian1over22',R(1,22)-sum((R((k+1)*(k+2),56)*t2**k for k in range(7)),R(0)))
    check('second_product_gradient23over20',R(23,20)-(R(57,56)+3*E/7)**7)
    b2={0:R(1),1:R(0),2:v2/2,3:rho2*v2/3,4:v2*v2/8}
    for k in range(5,8):b2[k]=v2*sum((rho2**(s-2)*b2[k-s] for s in range(2,k+1)),R(0))/k
    gap2=R(27,56)-sum(((1-R((-1)**k,comb(8,k)))*b2[k]/v2 for k in range(3,8)),R(0))
    check('second_gap_over3over7',gap2-R(3,7))
    B2=R(961,110)
    check('second_var_under83over4eta',R(83,4)-R(65,64)*B2*R(7,3))
    check('reciprocal_norm_under39eta',39-R(83,4)-18-R(9,2)*E)
    check('radius_lower97over100', (R(3,100)-R(3,4)*E)**2-R(581,32)*E)
    check('sqrt39_under25over4',R(25,4)**2-39)
    check('sqrt8eta_under9over500',R(9,500)**2-8*E)
    check('energy_under42eta',42-(R(625,97)+R(9,500))**2)
    check('fixed_energy_entry1over512',R(1,512)-42*E)

    # CREDITED9620 Sections2--4 mechanism: recompute every scalar needed for
    # ONLY the basic first-power conclusion, not its full routing/stability.
    hm = R(1,512)
    rho = R(1,64)
    Lcircle = R(1,2)
    rminus = 1-E-rho
    rplus = 1+rho
    s = rplus+Lcircle*hm
    aj = {j:R(9,8*j)*comb(8,9-j)*rho**(7-j) for j in range(1,7)}
    aj[7] = R(9,14)
    cd = sum((j*aj[j]*s**(j-1) for j in range(1,8)),R(0))
    bd = 9*rminus**8-36*s**7*Lcircle*hm-cd*hm
    nc = R(7,4)*sum((aj[j]*rplus**j for j in [1,2,4,5,7]),R(0))
    be = 4*s**7/(36*rminus**8)+cd/(54*rminus**8)
    bj = {5:R(63,32),4:R(63,32)*rho,2:R(9,128)*rho*hm,1:R(9,4096)*hm**2}
    check('local_basic_positive_rminus',rminus)
    check('local_basic_centered_tau',R(17,384)**2-hm)
    check('local_basic_full_Rouche',9*rminus**8*Lcircle-36*s**7*Lcircle**2*hm-sum((aj[j]*(s**j+rplus**j) for j in range(1,8)),R(0)))
    check('local_basic_nine_circle_separation',R(4,9)*rminus-2*Lcircle*hm)
    check('local_basic_positive_Bd',bd)
    check('local_basic_cube_delta',bd/6-nc)
    check('local_basic_cube_delta0',9*rminus**8/6-nc)
    for c,name in [(R(1,6),'paired'),(R(1,5),'individual')]:
        check('local_basic_whole_normal_error_'+name,1-(1+2*rho)*be-R(1,72)-c*sum((bj[j]*rminus**(j-7) for j in [1,2,4,5]),R(0)))
    tau = R(17,384)
    check('local_basic_initial_tail3over5',R(3,5)-R(1,2)/rminus**3-tau/((rminus-tau)*rminus**3))
    rzero = R(4999,5000)
    check('local_basic_radius_rzero',1-rzero-(3*E+R(3,5)*hm)/8)
    check('local_basic_Q_coefficient_positive',R(3,4)/rplus**3-R(4,7))
    initial_divisor = R(4,7)-R(1,2)/rzero**3-tau/((rzero-tau)*rzero**3)-R(16,3)*(rho/6+hm)
    check('local_basic_initial_divisor_positive',initial_divisor)
    check('local_basic_initial_divisor_over1over2500',initial_divisor-R(1,2500))
    check('local_basic_slope13over5',R(8,3)-R(4,3)*E-R(13,5))


    # Whole nonnegative majorant polynomials independently reconstructed from
    # the recurrence, not inferred from matching a single endpoint value.
    firstpoly={0:[R(1)],1:[R(0)],2:[0,R(1,2)],3:[0,R(2,11)],4:[0,0,R(3,32)]}
    secondpoly={0:[R(1)],1:[R(0)],2:[0,R(1,2)],3:[0,rho2/3],4:[0,0,R(1,8)]}
    for k in range(5,8):
        firstpoly[k]=pscale(padd([0]+firstpoly[k-2],pscale([0]+firstpoly[k-3],R(6,11)),
                    *[pscale([0,0]+firstpoly[k-s],R(7,8)*rho1**(s-4)) for s in range(4,k+1)]),R(1,k))
        secondpoly[k]=pscale(padd(*[pscale([0]+secondpoly[k-s],rho2**(s-2)) for s in range(2,k+1)]),R(1,k))
    for polys,endpoint,majorants in [(firstpoly,v0,b1),(secondpoly,v2,b2)]:
        for k,p in polys.items():
            require(all(c>=0 for c in p),'majorant polynomial nonnegative coefficients')
            if k>=2:require(p[0]==0,'majorant divided by variance is a polynomial')
            require(pvalue(p,endpoint)==majorants[k],'whole majorant polynomial endpoint discrepancy')

    skew_controls=[]
    for k in range(1,8):
        x=[R(8-k)]*k+[R(-k)]*(8-k)
        v=sum((z*z for z in x),R(0));p3=sum((z**3 for z in x),R(0))
        ratio=p3*p3/v**3
        require(sum(x)==0 and ratio==R((8-2*k)**2,8*k*(8-k)),'whole stationary two-level skew identity')
        require(ratio<=R(9,14),'eight-slot skew maximum')
        skew_controls.append({'positive_count':k,'whole_tuple':list(map(str,x)),'variance':str(v),
                              'p3':str(p3),'skew_ratio_squared':str(ratio)})
    # Equal absolute values attain the positive e4 bound exactly.
    balanced_e4=[ga(1)]*4+[ga(-1)]*4
    require(symmetric(balanced_e4)[4]==ga(6),'fourth-moment sharp control')
    controls=[
      literal_control('balanced',[ga(1)]*8,R(1)),
      literal_control('balanced_at_wider_endpoint',[ga(1)]*8,1-E),
      literal_control('wide_floor_variance',[ga(R(3,4)),ga(R(17,4))]+[ga(R(1,2))]*6,R(1)),
      literal_control('zero_coordinates',[ga(0)]*8,1-E),
      literal_control('full_gaussian',[ga(R(3,4)+R(j,20),R((j%3)-1,30)) for j in range(8)],1-E),
      literal_control('mixed_collisions',[ga(1,R(1,10))]*4+[ga(1,R(-1,10))]*4,R(3,4)),
      literal_control('extremal_positive_fourth',balanced_e4,R(1)),
    ]
    damages={
      'old_phase_l1_cut':R(1,400)-161*E,
      'global_gradient_cap2':2-R(sectors['7:1']['full']),
      'initial_variance_cut6':6-8*d0*E,
      'first_real_coercivity1over10':gap1-R(1,10),
      'second_real_coercivity9over20':gap2-R(9,20),
      'global_real_gradient_negative':-R(controls[2]['all_eight_gradients'][0][0]),
      'skew_square_cap1over2':R(1,2)-R(9,14),
      'e4_cap_v_squared_over16':R(1,16)*64-6,
      'old_local_radius6399over6400':R(1,6400)-(3*E+R(3,5)*hm)/8,
    }
    for name,margin in damages.items():require(margin<=0,'mathematical damage not rejected: '+name)
    for name,margin in margins.items():require(margin>0,'strict whole-window margin failed: '+name)
    def strings(value):
        if isinstance(value,R):return str(value)
        if isinstance(value,dict):return {str(k):strings(v) for k,v in value.items()}
        if isinstance(value,list):return list(map(strings,value))
        return value
    return strings({'version':1,'agent':'six-sendov-1','role':'researcher','eta_endpoint':E,
        'whole_polar':rec,'whole_envelopes':sectors,'strict_full_window_margins':margins,
        'whole_radial_gap_coefficients':[R((-1)**k,comb(8,k))-1 for k in range(2,9)],
        'first_majorant_polynomials':firstpoly,'second_majorant_polynomials':secondpoly,
        'first_majorants':b1,'second_majorants':b2,'first_gap':gap1,'second_gap':gap2,
        'whole_skew_controls':skew_controls,'whole_literal_controls':controls,
        'local_basic_coefficients':{'A':aj,'Cd':cd,'Bd':bd,'Nc':nc,'errorB':be,'Bj':bj,'kappa':initial_divisor},
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
        expected_manifest={'schema':'wider-origin-routing-source-v1',
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
                      'complete_sector_integrals':15,'strict_window_margins':len(record['strict_full_window_margins']),
                      'whole_literal_controls':len(record['whole_literal_controls']),
                      'whole_skew_controls':len(record['whole_skew_controls']),
                      'rejected_mathematical_budgets':len(record['rejected_mathematical_budgets'])},sort_keys=True))

if __name__=='__main__':main()
