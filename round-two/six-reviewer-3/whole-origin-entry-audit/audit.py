"""Independent all-sector audit; exact rational interpolation and owned polynomial kernel."""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import hashlib, json, sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from polys import cast, symbol, need
from radial import coefficients, radial

E=F(1,65536)
L=8+3*E
A=4+3*E

def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

def constant(p):
    need(not p.terms or set(p.terms)=={()},'constant polynomial expected')
    return p.terms.get((),(F(0),F(0)))

def real(p):
    z=constant(p);need(z[1]==0,'real scalar expected');return z[0]

def product(xs):
    out=cast(1)
    for x in xs:out*=x
    return out

def integrate(p,lo=0,hi=1):
    ant=p.integral('t')
    return ant.substitute({'t':hi})-ant.substitute({'t':lo})

def nc_weights(n=10):
    """Integrals of EVERY Lagrange basis; no numerical quadrature approximation."""
    u=symbol('t');nodes=[F(j,n-1) for j in range(n)];out=[]
    for j,x in enumerate(nodes):
        basis=product((u-y)/(x-y) for i,y in enumerate(nodes) if i!=j)
        for i,y in enumerate(nodes):need(real(basis.substitute({'t':y}))==int(i==j),'cardinal interpolation')
        out.append(real(integrate(basis)))
    for d in range(n):need(sum(w*x**d for w,x in zip(out,nodes))==F(1,d+1),'whole quadrature moment '+str(d))
    return nodes,out

def sectors():
    t=symbol('t');nodes,weights=nc_weights();rows=[];bounds={}
    for m,h in [(7,1),(6,2)]:
        total=F(0)
        for k in range(m+1):
            R=F(1,2)+A/k if k else None
            lo=1/R if k else F(0)
            p=9*t**h*(1-t/2)**(m-k)
            if k:p*=(R*t-1)**k
            value=real(integrate(p,lo,1))
            other=(1-lo)*sum(w*real(p.substitute({'t':lo+(1-lo)*x})) for w,x in zip(weights,nodes))
            need(value==other and value>=0,'entire supported sector interpolation')
            rows.append({'m':m,'h':h,'k':k,'radius_average':None if R is None else str(R),
                         'support_start':str(lo),'whole_integrand_coefficients':list(map(str,coefficients(p,'t'))),
                         'integral':str(value),'exact_interpolatory_integral':str(other)})
            total+=value
        correction=36*sum((F(1,20)**k/F(factorial(k)*(h+k+1)) for k in range(1,m+1)),F(0))
        margin=2-(total+correction)/(1-E)
        need(margin>0,'whole-origin derivative budget')
        bounds[str(m)+','+str(h)]={'I':str(total),'J':str(correction),'margin_below_2':str(margin)}
    return {'quadrature_nodes':list(map(str,nodes)),'quadrature_weights':list(map(str,weights)),
            'full_sector_rows':rows,'derivative_envelopes':bounds}

def newton():
    v=symbol('v');rho=F(3,8)
    B=[cast(1),cast(0),v/2,rho*v/3,v**2/8]
    for k in range(5,8):B.append(v*sum((B[k-s]*rho**(s-2) for s in range(2,k+1)),cast(0))/k)
    rows=[]
    for k in range(2,8):
        q=B[k].divide_monomial({'v':1});cs=coefficients(q,'v')
        need(all(c>=0 for c in cs),'all higher coefficients nonnegative')
        rows.append({'degree':k,'whole_majorant':B[k].record(),'quotient_by_v':q.record(),
                     'endpoint_quotient':str(real(q.substitute({'v':F(9,64)})))})
    gamma=F(27,56)-sum((1-F((-1)**k,comb(8,k)))*real(B[k].divide_monomial({'v':1}).substitute({'v':F(9,64)})) for k in range(3,8))
    need(gamma==F(22673913,73400320),'full radial coercivity coefficient')
    return {'whole_majorants':rows,'balanced_gap_coefficients':[str(F((-1)**k,comb(8,k))-1) for k in range(9)],
            'gamma':str(gamma),'normalized_variance_budget':str(F(117,10)/gamma)}

def margins():
    e=E;a=1-e;d0=F(256*344,5);g=F(22673913,73400320)
    first=sum(F(k+1,8)*F(1,6)**k for k in range(8))
    second=sum(F((k+1)*(k+2),56)*F(1,6)**k for k in range(7))
    cap=65*F(38,64)
    Dq=cap+18+F(9,2)*e
    ms={
      'positive_a':a,'A_below_9_over_2':F(9,2)-A,
      'sector_k1_below_4':4-(A-F(1,2)),
      'sector_k2_below_4':4-(A/2-F(1,2))**2,
      'sector_k3_below_1':1-(A/3-F(1,2)),
      'phase_path_1_over_20':F(1,400)-(160+60*e)*e,
      'whole_P_derivative_2':2-((L-F(1,2))/7)**7,
      'initial_E2_7_over_4':28*a*a-26-F(7,4),
      'first_bootstrap_9_over_4':F(9,4)-8*d0*e,
      'E2_after_first_23':28*a*a-2*F(9,4)-23,
      'second_bootstrap_1_over_6':F(1,6)-F(14,23)*d0*e,
      'E2_after_second_27':28*a*a-2*F(1,6)-27,
      'third_bootstrap_9_over_64':F(9,64)-F(14,27)*d0*e,
      'radial_l2_37_over_256':F(37,256)-F(65,64)*F(9,64)-F(9,2)*e*e,
      'individual_radius_3_over_8':(F(3,8)-3*e/4)**2-F(7,8)*F(65,64)*F(9,64),
      'radial_sqrt_49_over_128':F(49,128)**2-F(37,256),
      'phase_sqrt_21_over_1024':F(21,1024)**2-F(55,2)*e,
      'scale_sqrt_8_below_3':9-8,
      'whole_complex_region_1_over_6':F(1,6)-(F(49,128)+F(21,1024)+3*e)**2,
      'local_gradient_1_over_5':F(1,5)-first,
      'local_hessian_1_over_16':F(1,16)-second,
      'real_signed_gradient_negative':-F(9,100)-(-F(1,8)+(F(3,8)+15*e)/28+F(1,75)),
      'directional_gradient_negative':F(9,100)*a*(1-20*e)-F(1,320),
      'local_P_derivative_3_over_2':F(3,2)-(F(59,56)+3*e/7)**7,
      'radial_coercivity_3_over_10':g-F(3,10),
      'original_V_below_40':40-F(65,64)*39,
      'reciprocal_radius_39_over_40':(F(1,40)-3*e/4)**2-35*e,
      'reciprocal_radius_positive_base':F(1,40)-3*e/4,
      'sqrt59_below_31_over_4':F(31,4)**2-59,
      'sqrt8_sqrteta_below_3_over_256':F(3,256)**2-8*e,
      'original_H64':8-(F(3,256)+F(310,39)),
      'new_Vprime38':38*g-F(117,10),
      'new_q_norm_301_over_40':F(301,40)**2-Dq,
      'new_H60':60-(F(3,256)+F(301,39))**2,
      'new_collar_entry_1_over_25_squared':F(1,625)-60*e,
      'old_collar_entry_1_over_25_squared':F(1,625)-64*e,
      'collar_eta_window':F(1,16384)-e,
      'sharp_C_below_3_lower_cos':3-(F(8,3)+F(2,9)),
      'triple_angle_at_47_over_50':8*F(47,50)**3-6*F(47,50)-1,
      'conditional_slope_111_over_40':F(8,3)+F(50,291)-F(1,16)-F(111,40)
    }
    for name,value in ms.items():need(value>0,'strict rational margin '+name)
    need(sum((F(k+1,8)*F(1,6)**k for k in range(2,50)),F(0))<F(1,75),'finite tail below whole infinite bound')
    return {'strict_margins':{k:str(v) for k,v in sorted(ms.items())},'first_beta_bound':str(first),
            'second_beta_bound':str(second),'d0':str(d0),'bootstrap_budgets':[str(8*d0),str(F(14,23)*d0),str(F(14,27)*d0)],
            'new_Vprime_budget':'38','new_V_budget':str(cap),'new_q_norm_squared_budget':str(Dq),
            'new_direct_H_budget':'60','credited_collar_H_budget':'25'}

def elementary(xs):
    out=[cast(1)]
    for x in xs:
        out.append(cast(0))
        for k in range(len(out)-1,0,-1):out[k]+=x*out[k-1]
    return out

def origin(q,a):
    t=symbol('t')
    return 9*integrate(product(1-a*t*x for x in q))

def derivatives(q,a):
    t=symbol('t');first=[];mixed=[]
    for j in range(8):first.append(-9*a*integrate(t*product(1-a*t*q[k] for k in range(8) if k!=j)))
    for i in range(8):
        mixed.append([cast(0) if i==j else 9*a*a*integrate(t*t*product(1-a*t*q[k] for k in range(8) if k not in (i,j))) for j in range(8)])
    return first,mixed

def identity_controls():
    cases=[('center',[1]*8,F(1)),
           ('balanced_real',[F(15,16)]*4+[F(17,16)]*4,1-E),
           ('complex_center',[(F(1),F((-1)**j,100)) for j in range(8)],1-E),
           ('rational_same_phase',[(F(9999,10001),F(200,10001))]*8,1-E),
           ('zero_real_factors',[F(1,2)]*7+[F(9,2)],F(1)),
           ('abstract_global_positive_gradient',[F(1,2)]*7+[F(9,2)],1-E)]
    rows=[]
    for name,literal,a in cases:
        q=list(map(cast,literal));es=elementary(q);O=origin(q,a)
        need(O==9*sum((F((-1)**k,k+1)*a**k*es[k] for k in range(9)),cast(0)),'entire origin coefficient identity')
        ds,hs=derivatives(q,a);center=elementary([x-1 for x in q])
        if a==1:need(O==sum((F((-1)**k,comb(8,k))*center[k] for k in range(9)),cast(0)),'entire centered beta identity')
        for j in range(8):
            remaining=elementary([q[k] for k in range(8) if k!=j])
            need(ds[j]==-9*a*sum((F((-1)**k,k+2)*a**k*remaining[k] for k in range(8)),cast(0)),'whole first derivative')
            for i in range(8):
                if i==j:need(hs[i][j]==0,'pure second zero');continue
                rem=elementary([q[k] for k in range(8) if k not in (i,j)])
                need(hs[i][j]==9*a*a*sum((F((-1)**k,k+3)*a**k*rem[k] for k in range(7)),cast(0)),'whole mixed derivative')
        if name=='abstract_global_positive_gradient':need(any(constant(x)[0]>0 for x in ds),'local phase sign cannot be assumed globally')
        rows.append({'name':name,'abstract_only':True,'a':str(a),'q':[x.record() for x in q],
                     'whole_origin':O.record(),'whole_centered_elementary':[x.record() for x in center],
                     'all_first_derivatives':[x.record() for x in ds],
                     'all_ordered_second_derivatives':[[x.record() for x in row] for row in hs]})
    # Newton identities and phase radial loss checked symbolically, without sampled roots.
    x,y,r=symbol('x'),symbol('y'),symbol('r')
    need((x-r)**2+y*y==x*x+y*y-2*r*x+r*r,'exact phase distance')
    need((x-1)**2+y*y==x*x+y*y-2*x+1,'exact reciprocal distance')
    v,p4=symbol('v'),symbol('p4')
    need(4*(v*v/8-p4/4)==v*v/2-p4,'full fourth Newton identity')
    return rows

def broken_budgets():
    e=E;d0=F(256*344,5)
    bad={'phase_allowance_double_window':F(1,400)-(160+120*e)*2*e,
         'one_step_local_bootstrap':F(9,64)-8*d0*e,
         'two_step_local_bootstrap':F(9,64)-F(14,23)*d0*e,
         'local_gradient_1_over_6':F(1,6)-sum(F(k+1,8)*F(1,6)**k for k in range(8)),
         'new_H59_from_rounding':59-(F(3,256)+F(301,39))**2}
    for label,value in bad.items():need(value<0,'insufficient mathematical budget '+label)
    return {k:{'margin':str(v),'reason':'insufficient displayed budget; not physical nonexistence'} for k,v in sorted(bad.items())}

def build():
    return {'schema':1,'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer',
            'method':'complete rational polynomial integration cross-checked by all-moment Lagrange quadrature; owned9719 algebraic kernel',
            'window':str(E),'sectors':sectors(),'newton':newton(),'margins':margins(),
            'controls':identity_controls(),'credited_owned_radial_faces':radial(),
            'damaged_mathematical_budgets':broken_budgets(),
            'zero_variance_division':False,'original_disk_assumed_on_normalized_tuple':False}

def typed_equal(a,b):
    if type(a)!=type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(typed_equal(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b

def main():
    root=Path(__file__).resolve().parent;r=build();b=canonical(r)
    if '--generate' in sys.argv:(root/'EXPECTED.json').write_bytes(b+b'\n')
    else:
        need(typed_equal(json.loads((root/'EXPECTED.json').read_text()),r),'entire typed external fixture differs')
        for line in (root/'CORE.sha256').read_text().splitlines():
            h,name=line.split('  ',1);need(hashlib.sha256((root/name).read_bytes()).hexdigest()==h,'frozen core pin differs '+name)
    print(json.dumps({'whole_record_sha256':hashlib.sha256(b).hexdigest(),'record_bytes':len(b),
                      'full_sectors':15,'whole_controls':len(r['controls']),'strict_margins':len(r['margins']['strict_margins']),
                      'owned_radial_faces':8,'direct_H':'60','native_threads':'1 (runner enforced)'},sort_keys=True))

if __name__=='__main__':main()
