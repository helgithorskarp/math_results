#!/usr/bin/env python3
"""Exact finite corroboration; ordinary sector/norm/Taylor bridges are in PROOF.md."""
import argparse
from fractions import Fraction as R
from math import comb, factorial
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
E = R(1, 65536)
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

def build_record():
    envelopes={}
    for m,s in [(7,1),(6,2)]:
        rows=[sector(m,s,k) for k in range(m+1)]
        total=sum((R(r['monomial_integral']) for r in rows),R(0))
        correction=36*sum((R(1,20)**k/R(factorial(k)*(s+k+1)) for k in range(1,m+1)),R(0))
        envelopes[f'{m}:{s}']={'all_sectors':rows,'whole_real_integral':str(total),
                             'whole_complex_correction':str(correction),
                             'full_a_uniform_bound':str((total+correction)/(1-E))}
    d0=R(256*344,5);v0=8*d0;v1=R(14,23)*d0;v2=R(14,27)*d0
    margins={
     'global_gradient_under2':2-R(envelopes['7:1']['full_a_uniform_bound']),
     'global_hessian_under2':2-R(envelopes['6:2']['full_a_uniform_bound']),
     'whole_phase_l1_under1over20_squared':R(1,400)-161*E,
     'product_gradient_under2':2-((8+3*E-R(1,2))/7)**7,
     'initial_e2_over7over4':28*(1-E)**2-26-R(7,4),
     'coarse_v_under9over4':R(9,4)-v0*E,
     'e2_after9over4_over23':28*(1-E)**2-R(9,2)-23,
     'second_v_under1over6':R(1,6)-v1*E,
     'e2_after1over6_over27':28*(1-E)**2-R(1,3)-27,
     'third_v_under9over64':R(9,64)-v2*E,
     'actual_radial_norm_under37over256':R(37,256)-R(65,64)*R(9,64)-R(9,2)*E*E,
     'individual_radial_deviation_under3over8_squared':(R(3,8)-R(3,4)*E)**2-R(7,8)*R(65,64)*R(9,64),
     'radial_norm_under49over128_squared':R(49,128)**2-R(37,256),
     'phase_norm_under21over1024_squared':R(21,1024)**2-R(55,2)*E,
     'full_local_ball_under1over6':R(1,6)-(R(49,128)+R(21,1024)+3*E)**2,
     'local_gradient_under1over5':R(1,5)-sum((R(k+1,8)*R(1,6)**k for k in range(8)),R(0)),
     'local_hessian_under1over16':R(1,16)-sum((R((k+1)*(k+2),56)*R(1,6)**k for k in range(7)),R(0)),
     'real_gradient_below_minus9over100':R(1,8)-(R(3,8)+15*E)/28-R(1,75)-R(9,100),
     'phase_radial_derivative_negative':R(9,100)*(1-E)*(1-20*E)-R(1,320),
     'local_product_gradient_under3over2':R(3,2)-(R(59,56)+3*E/7)**7,
    }
    rho=R(3,8);v=R(9,64)
    b={0:R(1),1:R(0),2:v/2,3:rho*v/3,4:v*v/8}
    for k in range(5,8):b[k]=v*sum((b[k-s]*rho**(s-2) for s in range(2,k+1)),R(0))/k
    bp={0:[R(1)],1:[R(0)],2:[R(0),R(1,2)],3:[R(0),rho/3],4:[R(0),R(0),R(1,8)]}
    for k in range(5,8):
        z=[R(0)]*5
        for s in range(2,k+1):
            for j,c in enumerate(bp[k-s]):z[j+1]+=c*rho**(s-2)/k
        while len(z)>1 and z[-1]==0:z.pop()
        bp[k]=z
    for k,z in bp.items():
        require(all(c>=0 for c in z),'negative complete Newton-majorant coefficient')
        require(sum((c*v**j for j,c in enumerate(z)),R(0))==b[k],'whole polynomial/endpoint Newton mismatch')
    gap=R(27,56)-sum(((1-R((-1)**k,comb(8,k)))*b[k]/v for k in range(3,8)),R(0))
    require(gap==R(22673913,73400320),'whole radial gap discrepancy')
    margins.update({
     'whole_local_radial_gap_over3over10':gap-R(3,10),
     'after_local_var_under40eta':40-R(65,64)*39,
     'reciprocal_norm_under59eta':59-58-R(9,2)*E,
     'after_local_radius_over39over40_squared':(R(1,40)-R(3,4)*E)**2-35*E,
     'sqrt59_below31over4_squared':R(31,4)**2-59,
     'energy_sqrt_under8':8-R(310,39)-R(3,256),
     'new_full_window_fixed_energy_entry':R(1,512)-64*E,
     'uniform_sector_parameter_under9over2':R(9,2)-A,
     'positive_radius_square_side':R(1,40)-3*E/4,
     'triple_angle_at47over50_positive':8*R(47,50)**3-6*R(47,50)-1,
     'full_window_first_power_over111over40':R(8,3)+R(50,291)-R(1,16)-R(111,40),
    })
    for key,value in margins.items():require(value>0,'nonpositive strict margin: '+key)
    controls=[
     literal_control('balanced',[ga(1)]*8,R(1)),
     literal_control('balanced_at_endpoint',[ga(1)]*8,1-E),
     literal_control('wide_floor_variance',[ga(R(3,4)),ga(R(17,4))]+[ga(R(1,2))]*6,R(1)),
     literal_control('zero_coordinates',[ga(0)]*8,1-E),
     literal_control('full_gaussian',[ga(R(3,4)+R(j,20),R((j%3)-1,30)) for j in range(8)],1-E),
     literal_control('mixed_collisions',[ga(1,R(1,10))]*4+[ga(1,R(-1,10))]*4,R(3,4)),
    ]
    wide=controls[2]
    require(R(wide['all_eight_gradients'][0][0])>0,'global sign damage witness lost')
    damages={
      'gradient_bound19over10':R(19,10)-R(envelopes['7:1']['full_a_uniform_bound']),
      'hessian_bound17over10':R(17,10)-R(envelopes['6:2']['full_a_uniform_bound']),
      'phase_l1_square1over500':R(1,500)-161*E,
      'initial_variance_cut2':2-v0*E,
      'third_variance_cut1over8':R(1,8)-v2*E,
      'radial_coercivity1over3':gap-R(1,3),
      'initial_gradient_globally_negative':-R(wide['all_eight_gradients'][0][0]),
    }
    for key,value in damages.items():require(value<=0,'damage not rejected: '+key)
    return {'version':1,'eta_endpoint':str(E),'whole_envelopes':envelopes,
            'strict_full_window_margins':{k:str(v) for k,v in margins.items()},
            'bootstrap_variance_coefficients':[str(z) for z in (v0,v1,v2)],
            'whole_radial_gap_coefficients':[str(R((-1)**k,comb(8,k))-1) for k in range(2,9)],
            'whole_newton_endpoint_majorants':{str(k):str(v) for k,v in b.items()},
            'whole_newton_majorant_polynomials':{str(k):[str(c) for c in p] for k,p in bp.items()},
            'whole_local_radial_gap':str(gap),'whole_literal_controls':controls,
            'rejected_mathematical_budgets':{k:str(v) for k,v in damages.items()}}

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
        expected_manifest={'schema':'weighted-origin-routing-source-v1',
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
                      'rejected_mathematical_budgets':len(record['rejected_mathematical_budgets'])},sort_keys=True))

if __name__=='__main__':main()
