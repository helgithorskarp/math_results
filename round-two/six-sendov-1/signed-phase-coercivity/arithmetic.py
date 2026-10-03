"""Whole finite evidence for the ordinary signed-phase proof.
Actual six-sendov-1 / researcher. Standard-library rational arithmetic,
same-author implementation. build_record has no filesystem/network/clock
access. Universal analytic implications are in PROOF.md, not formalized.
"""
from fractions import Fraction as F
from math import comb

class VerificationError(ValueError):
    pass

DAMAGE_CASES = (
    "fourth-order-sign", "omit-eighth-order", "insufficient-Hessian-scale",
    "wrong-Hessian-center", "delete-imaginary-mean", "invalid-fixed-energy-radius",
)

def require(condition, message):
    if not condition:
        raise VerificationError(message)

def cmul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])

def cadd(a, b):
    return (a[0]+b[0], a[1]+b[1])

def coefficient_record(damage=None):
    shifted=[]
    for k in range(9):
        direct={k+l:9*F((-1)**(k+l)*comb(8-k,l), k+l+1) for l in range(9-k)}
        other={j:F(9*(-1)**j*comb(8,j)*comb(j,k), comb(8,k)*(j+1)) for j in range(k,9)}
        require(direct == other, 'complete general-a shifted coefficient mismatch')
        at1=sum(direct.values())
        require(at1 == F((-1)**k,comb(8,k)), 'shifted endpoint coefficient mismatch')
        shifted.append({'k':k, 'complete_a_coefficients':[[j,str(c)] for j,c in sorted(direct.items())],
                        'two_routes_equal':True, 'at_a1':str(at1)})
    center=F(1,27) if damage == 'wrong-Hessian-center' else F(1,28)
    require(center == F(shifted[2]['at_a1']), 'Hessian center differs from defining whole polynomial')
    mixed=[]
    for k in range(1,9):
        row=[]
        for ell in range(9-k):
            direct=F(comb(8-k,ell),comb(8,k+ell))
            other=F(comb(k+ell,k),comb(8,k))
            require(direct == other, 'whole mixed coefficient ratio mismatch')
            row.append(str(direct))
        mixed.append({'k':k,'remaining':8-k,'all_majorant_coefficients':row})
    return {'shifted':shifted,'shifted_coefficient_count':sum(len(x['complete_a_coefficients']) for x in shifted),
            'mixed':mixed,'mixed_coefficient_count':sum(len(x['all_majorant_coefficients']) for x in mixed),
            'Hessian_center':str(center),'mean_square_coefficient':str(center/2)}

def scalar_record(damage=None):
    classes=[]
    total_checks={}
    def margin(checks,name,value,closed=False):
        value=F(value)
        valid=value>=0 if closed else value>0
        require(valid,'receiving margin rejected: '+name)
        checks[name]={'value':str(value),'closed':closed,'passes':valid}
    for label,rho,b1,b2,b4,b6,target in [
        ('broad',F(1,16),F(1,40),F(13,500),F(127,4000),F(9,200),F(1,8)),
        ('fine',F(1,40),F(1,100),F(1,94),F(13,1000),F(19,1000),F(7,48))
    ]:
        if damage == 'insufficient-Hessian-scale' and label == 'broad':b2=F(1,100)
        checks={};cap=F(1,1000);sigma=rho+cap
        for k,b in [(1,b1),(2,b2),(4,b4),(6,b6)]:
            margin(checks,'RMS_order'+str(k),(8-k)*b*b-sigma*sigma,k==4)
        g=F(1,8)-sum(F(j+1,8)*b1**j for j in range(1,8))
        h=sum(F((j+1)*(j+2),56)*b2**j for j in range(1,7))
        c=F(1,56)-F(7,2)*h
        D4=sum(F(comb(j+4,4),70)*b4**j for j in range(5))
        D6=sum(F(comb(j+6,6),28)*b6**j for j in range(3))
        splus=2*(1+rho);sminus=2*(1-rho)-cap
        tail=F(70,64)*D4*splus**2*cap+F(28,512)*D6*splus**3*cap**2+splus**4*cap**3/4096
        A=g+c*sminus-tail
        margin(checks,'negative_gradient',g)
        margin(checks,'negative_imaginary_energy',c)
        margin(checks,'imaginary_energy_floor',sminus)
        margin(checks,'complete_coercivity_gap',A-target)
        classes.append({'name':label,'radial_norm_cap':str(rho),'phase_cap':str(cap),'real_path_norm_cap':str(sigma),
                        'RMS_scales':[str(b1),str(b2),str(b4),str(b6)],'target_lambda':str(target),
                        'negative_gradient':str(g),'Hessian_variation':str(h),'negative_imaginary_energy':str(c),
                        'D4':str(D4),'D6':str(D6),'S_over_Delta_bounds':[str(sminus),str(splus)],
                        'all_even_tail_per_Delta':str(tail),'full_coercivity':str(A),'margins':checks})
        total_checks.update({label+'.'+key:row for key,row in checks.items()})
    checks={};e=F(1,12000);amin=1-e;h0=F(1,320)
    root=F(1,20) if damage == 'invalid-fixed-energy-radius' else F(7,125)
    f0=amin-root
    margin(checks,'entry_H37_below_fixed_h',h0-37*e)
    margin(checks,'actual_fixedH_root_bound',root**2-h0)
    margin(checks,'actual_fixedH_divisor',f0)
    margin(checks,'actual_broad_norm_class',F(1,16)**2-h0/f0**2)
    margin(checks,'actual_phase_class',F(1,1000)-F(17,2)*e)
    tau=F(1,50);tstar=F(13,15)*e
    f1=amin-tstar-tau;h1=5+8*F(169,225)*e
    margin(checks,'LC_centered_radius',tau**2-F(7,8)*5*e)
    margin(checks,'LC_reciprocal_divisor',f1)
    margin(checks,'actual_fine_norm_class',F(1,40)**2-h1*e/f1**2)
    ycoef=(F(8,3)+h1/f1)/amin**2
    margin(checks,'actual_imaginary_sum8',8-ycoef)
    total_checks.update({'actual.'+key:row for key,row in checks.items()})
    return {'classes':classes,'actual':{'eta_cap':str(e),'amin':str(amin),'fixed_H_cap':str(h0),
                'fixed_H_root_bound':str(root),'broad_divisor':str(f0),'LC_centered_radius':str(tau),
                'LC_tstar':str(tstar),'LC_H_coefficient':str(h1),'fine_divisor':str(f1),
                'imaginary_sum_coefficient':str(ycoef),'margins':checks},
            'margin_count':len(total_checks),'strict_margin_count':sum(not row['closed'] for row in total_checks.values()),
            'closed_margin_count':sum(row['closed'] for row in total_checks.values())}

def origin_product(q):
    p=[(F(1),F(0))]
    for z in q:
        out=[(F(0),F(0))]*(len(p)+1)
        for j,c in enumerate(p):
            out[j]=cadd(out[j],c)
            out[j+1]=cadd(out[j+1],cmul(c,(-z[0],-z[1])))
        p=out
    # A second complete construction enumerates every subset of all eight factors.
    other=[(F(0),F(0))]*9
    for mask in range(256):
        c=(F(1),F(0))
        for j in range(8):
            if mask & (1<<j):c=cmul(c,(-q[j][0],-q[j][1]))
        k=mask.bit_count();other[k]=cadd(other[k],c)
    require(p == other,'literal entire complex origin coefficients differ')
    value=(F(0),F(0))
    for j,c in enumerate(p):value=cadd(value,(9*c[0]/(j+1),9*c[1]/(j+1)))
    return p,value

def algebra_record(damage=None):
    # Entire 16-real-variable product: B and y masks are disjoint, square-free.
    poly={(0,0):(F(1),F(0))}
    for j in range(8):
        out={}
        for (bm,ym),c in poly.items():
            for key,factor in [((bm,ym),(F(1),F(0))),((bm|1<<j,ym),(F(-1),F(0))),
                               ((bm,ym|1<<j),(F(0),F(-1)))]:
                out[key]=cadd(out.get(key,(F(0),F(0))),cmul(c,factor))
        poly=out
    whole={(bm,ym):-9*c[0]/((bm|ym).bit_count()+1) for (bm,ym),c in poly.items() if ym and c[0]}
    other={}
    for ym in range(1,256):
        k=ym.bit_count()
        if k%2:continue
        if damage == 'omit-eighth-order' and k==8:continue
        sign=(-1)**(k//2+1)
        if damage == 'fourth-order-sign' and k==4:sign=-sign
        for bm in range(256):
            if bm&ym:continue
            ell=bm.bit_count();other[(bm,ym)]=sign*F(9*(-1)**(k+ell),k+ell+1)
    require(whole == other,'entire 16-real-variable even phase identity differs')
    rows=[[bm,ym,str(c)] for (bm,ym),c in sorted(whole.items())]
    # The whole paired balanced unit-circle family, retaining all s,d powers.
    factor={(0,0):F(1),(1,0):F(-2),(2,0):F(1),(1,1):F(2)}
    family={(0,0):F(1)}
    for _ in range(4):
        out={}
        for (s,d),c in family.items():
            for (u,v),b in factor.items():out[(s+u,d+v)]=out.get((s+u,d+v),F(0))+c*b
        family={key:c for key,c in out.items() if c}
    # Independent binomial construction of [(1-s)^2+2ds]^4.
    binomial={}
    for d in range(5):
        for j in range(2*(4-d)+1):
            key=(d+j,d);binomial[key]=F(comb(4,d)*2**d*comb(2*(4-d),j)*(-1)**j)
    require(family == binomial,'entire balanced-family product differs')
    integrated={}
    for (s,d),c in family.items():integrated[d]=integrated.get(d,F(0))+9*c/F(s+1)
    expected={0:F(1),1:F(9,7),2:F(72,35),3:F(24,5),4:F(144,5)}
    require(integrated == expected,'entire balanced-family integration differs')
    require(integrated[1]/8 == F(9,56),'limiting envelope curvature coefficient differs')
    w=(F(999999,1000001),F(2000,1000001))
    require(w[0]**2+w[1]**2 == 1,'literal control phase is not unit')
    controls=[]
    for name,radii,signs in [
        ('total_real_collision',[F(1)]*8,[0]*8),
        ('coherent_imaginary_mean',[F(1)]*8,[1]*8),
        ('balanced_four_plus_four',[F(1)]*8,[1]*4+[-1]*4),
        ('nonconjugate_five_plus_three',[1+F((-1)**j,2000) for j in range(8)],[1]*5+[-1]*3),
        ('closed_fine_radial_zero_phase',[1+F(1,40)]+[F(1)]*7,[0]*8),
        ('closed_broad_radial_zero_phase',[1+F(1,16)]+[F(1)]*7,[0]*8)
    ]:
        z=[(r,F(0)) if sign==0 else (r*w[0],sign*r*w[1]) for r,sign in zip(radii,signs)]
        p,value=origin_product(z);pr,realvalue=origin_product([(r,F(0)) for r in radii])
        delta=sum(r-q[0] for r,q in zip(radii,z));Y=sum(q[1] for q in z)
        normsq=sum((r-1)**2 for r in radii);loss=realvalue[0]-value[0]
        active=[]
        for rho,lam in [(F(1,16),F(1,8)),(F(1,40),F(7,48))]:
            if normsq<=rho**2 and delta<=F(1,1000):
                mean_weight=F(0) if damage == 'delete-imaginary-mean' else F(1,56)
                gap=-lam*delta+mean_weight*Y**2-loss
                require(gap>=0,'allowed literal phase bound fails: '+name)
                active.append({'rho':str(rho),'complete_bound_margin':str(gap)})
        require(bool(active),'literal control outside both claimed classes')
        controls.append({'name':name,'radii':[str(r) for r in radii],'z':[[str(x),str(y)] for x,y in z],
                         'whole_complex_t_coefficients':[[str(x),str(y)] for x,y in p],
                         'whole_radial_t_coefficients':[[str(x),str(y)] for x,y in pr],
                         'complex_origin_value':[str(x) for x in value],
                         'radial_origin_value':[str(x) for x in realvalue],
                         'Delta':str(delta),'Y':str(Y),'radial_norm_squared':str(normsq),
                         'phase_loss':str(loss),'active_class_margins':active,'two_full_product_routes_equal':True})
    coherent=next(x for x in controls if x['name']=='coherent_imaginary_mean')
    require(F(coherent['phase_loss'])>0,'mean-necessity control lost its positive loss')
    return {'full_even_identity_common_map':rows,'map_encoding':'[real_B_mask, imaginary_y_mask, exact_coefficient]; disjoint eight-bit masks',
            'two_routes_equal':True,'common_map_terms':len(rows),
            'terms_by_even_order':{str(k):sum(ym.bit_count()==k for _,ym in whole) for k in (2,4,6,8)},
            'full_balanced_s_d_coefficients':[[s,d,str(c)] for (s,d),c in sorted(family.items())],
            'full_integrated_balanced_family':[[d,str(c)] for d,c in sorted(integrated.items())],
            'limiting_envelope_lambda_upper_bound':'9/56','literal_controls':controls,
            'controls_scope':'Algebraic envelope tuples only; no actual original-disk feasibility claim'}

def build_record(damage=None):
    if damage is not None:require(damage in DAMAGE_CASES,'unknown mathematical damage')
    return {'schema':1,'agent':'six-sendov-1','role':'researcher',
            'proof_status':'Complete ordinary author lemma, unformalized and independently unreviewed; same-author exact corroboration',
            'domain':'Every finite complex eight-tuple: radial norm<=1/16 or1/40, Delta<=1/1000; actual corollaries ONLY after9930 and9974 on0<eta<=1/12000',
            'coefficients':coefficient_record(damage),'scalars':scalar_record(damage),'algebra':algebra_record(damage)}
