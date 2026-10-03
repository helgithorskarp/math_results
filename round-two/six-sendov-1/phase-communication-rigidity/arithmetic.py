"""Exact corroboration for phase/communication rigidity.
Actual six-sendov-1 / researcher. Self-contained standard-library arithmetic.
The defining analytic proof is PROOF.md. The complete multiaffine identity
scaffold is reused openly from this author's10010 arithmetic, source d3922598.
New endpoint budgets and new finite identities are separate from that scaffold.
build_record reads no files, clock, network, random source or external fixtures.
"""
from fractions import Fraction as F
from math import comb

class VerificationError(ValueError):
    pass

DAMAGE_CASES = (
    "phase-rigidity-too-small", "radial-norm-too-small", "centered-phase-too-small",
    "modulus-slack-too-small", "wrong-reciprocal-phase-sign", "fourth-order-sign",
    "omit-eighth-order", "wrong-Hessian-center", "delete-imaginary-mean",
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

def rigidity_scalar_record(damage=None):
    Q=F
    margins={};values={}
    def margin(name,value,closed=False):
     value=Q(value);good=value>=0 if closed else value>0
     margins[name]={'value':str(value),'closed':closed,'passes':good}
     require(good,'sufficient endpoint failed: '+name)
     return value
    def val(name,x):values[name]=str(Q(x));return Q(x)
    e=val('eta_cap',Q(1,12000));a=val('amin',1-e);tau=Q(1,50);ts=Q(13,15)*e
    f=val('reciprocal_floor',a-ts-tau);hc=val('H_coefficient',5+8*Q(169,225)*e)
    margin('LC_centered_radius',tau*tau-Q(7,8)*5*e)
    margin('divisor',f)
    margin('phase_cap8over3',Q(8,3)-hc/(2*f**3))
    margin('phase_class',Q(1,1000)-Q(8,3)*e)
    margin('scaled_radial_class',Q(1,40)**2-hc*e/f**2)
    margin('h0_bound5over2',Q(5,2)-Q(224,93))
    margin('sqrt13over190_bound4over15',Q(4,15)**2-Q(13,190))
    phase_cost=val('phase_rigidity_cost',24/a**3+2*hc/(5*a**4)+(2*hc**2/f+Q(15,4))/(190*a**4))
    margin('phase_rigidity27',(26 if damage=='phase-rigidity-too-small' else 27)-phase_cost)
    den=val('radial_exact_divisor',f*(a+f))
    radial_cost=val('radial_squared_norm_cost',(104+2*hc**2/190)/den**2)
    margin('radial_squared_norm30',(26 if damage=='radial-norm-too-small' else 30)-radial_cost)
    margin('r_unscaled_norm1over39',Q(1,39)-Q(1,40)/a)
    margin('negative_trace_cross',8-6)
    # Standalone COMPLETE centered even-phase remainder, fine norm/phase class.
    sigma=val('real_path_sigma',Q(13,500));rho=Q(1,40);cap=Q(1,1000)
    margin('gradient_RMS_scale',7*Q(5,13)**2-1)
    margin('Hessian_RMS_scale',6*Q(9,22)**2-1)
    G=val('gradient_tail_over_sigma',sum(Q(j+1,8)*Q(5,13)**j*sigma**(j-1) for j in range(1,8)))
    H=val('Hessian_tail_over_sigma',sum(Q((j+1)*(j+2),56)*Q(9,22)**j*sigma**(j-1) for j in range(1,7)))
    margin('gradient_tail_slope1over10',Q(1,10)-G)
    margin('Hessian_tail_slope1over21',Q(1,21)-H)
    b4=sigma/2;b6=Q(19,1000)
    margin('fourth_derivative_RMS',4*b4*b4-sigma*sigma,True)
    margin('sixth_derivative_RMS',2*b6*b6-sigma*sigma)
    D4=val('D4',sum(Q(comb(j+4,4),70)*b4**j for j in range(5)))
    D6=val('D6',sum(Q(comb(j+6,6),28)*b6**j for j in range(3)))
    splus=val('S_over_phase_upper',2*(1+rho));Smax=splus*cap
    higher=val('all_even_higher_coefficient',Q(70,64)*D4+Q(28,512)*D6*Smax+Smax**2/4096)
    margin('higher_tail1over50',Q(1,50)-higher)
    local_cost=val('local_centered_phase_cost',Q(1,10)+splus/6+Q(1,28)+splus**2/50)
    margin('local_centered_phase3over5',(Q(1,2) if damage=='centered-phase-too-small' else Q(3,5))-local_cost)
    margin('sqrt30over190_bound2over5',Q(2,5)**2-Q(30,190))
    actual_centered=val('actual_centered_phase_cost',Q(16,25)+Q(64,15*190))
    margin('actual_centered_phase2over3',Q(2,3)-actual_centered)
    # Whole reciprocal expansion + unrotated real energy, with physical D>=190eta^2.
    margin('sqrt13H_bound81over10',Q(81,10)**2-13*hc)
    margin('sqrtHcube_over190_bound5over6',Q(5,6)**2-hc**3/190)
    Yroot=val('imaginary_sum_sqrt_cost',8/a**2+Q(81,5)/a**3+Q(5,6)/(a**3*f))
    Ylinear=val('imaginary_sum_linear_cost',(8+Q(248,190))/a**2)
    margin('imaginary_sum_sqrt26',26-Yroot)
    margin('imaginary_sum_linear10',10-Ylinear)
    Ycoarse=val('imaginary_sum_coarse8_cost',(Q(8,3)+hc/f)/a**2)
    margin('imaginary_sum_coarse8',8-Ycoarse)
    margin('imaginary_square_piecewise1296',1296-64)
    loss_cost=val('signed_phase_loss_total_cost',Q(9,56)*27+Q(2,3)+1296*e/56+Q(3,8*190))
    margin('signed_phase_loss6',6-loss_cost)
    # Radial origin-product gap, ALL finite higher elementary-symmetric orders retained.
    torigin=Q(1,40)/Q(14,5);tproduct=Q(1,39)/Q(14,5)
    margin('rational_sqrt8_bound14over5',8-Q(14,5)**2)
    origin_tail=val('origin_tail_over_radial_norm_squared',sum(Q(1,8)*torigin**j for j in range(7)))
    margin('origin_tail13over100',Q(13,100)-origin_tail)
    product_tail=val('all_product_orders3through8_over_norm_squared',sum(Q(comb(8,k),8)*tproduct**(k-2) for k in range(3,9)))
    margin('product_tail1over15',Q(1,15)-product_tail)
    gap_precursor=val('gap_against_F_cost',Q(13,100)*30+Q(17,30)*30/a**2+Q(39,8*190))
    margin('gap_against_F21',21-gap_precursor)
    margin('actual_radial_gap23',23-(21+Q(9,8)))
    margin('actual_communication_slack29',29-(23+6),True)
    # The PRIMARY communication has a complex modulus. Retain both imaginary
    # coefficients through order two and every order three through eight.
    complex_norm_cost=val('complex_scaled_squared_norm_cost',hc/f**2)
    real_norm_cost=val('real_scaled_squared_norm_cost',(26+2*hc**2/190)/f**4)
    imag_norm_cost=val('imaginary_scaled_squared_norm_cost',hc/f**4)
    margin('complex_scaled_squared_norm21over4',Q(21,4)-complex_norm_cost)
    margin('real_scaled_squared_norm30',30-real_norm_cost)
    margin('imaginary_scaled_squared_norm11over2',Q(11,2)-imag_norm_cost)
    margin('whole_origin_tclass1over112',Q(1,112)-Q(1,40)/Q(14,5),True)
    margin('positive_origin_real99over100',Q(1,100)-Q(1,111))
    margin('large_defect_imaginary_square',1-Q(21,32)/(1-Q(1,112))**2)
    margin('small_defect_real_sum1over7',Q(1,7)**2-240*e)
    margin('sqrt165_bound13',13**2-165)
    margin('third_order_norm_cube3over5',Q(3,5)**2-Q(21,32)**3)
    margin('sqrt190_bound27over2',190-Q(27,2)**2)
    imag_origin_cost=val('small_defect_origin_imaginary_cost',Q(9,2)+Q(127,196)+Q(3,5)*Q(112,111)*Q(2,27))
    margin('small_defect_origin_imaginary6',6-imag_origin_cost)
    margin('small_defect_imaginary_square',1-36*e)
    margin('actual_modulus_communication_slack30',(29 if damage=='modulus-slack-too-small' else 30)-(29+Q(50,99)))
    # Uniform consequences on BOTH cuts with epsilon<=10eta, retaining the
    # closed physical190 convention separately from the older physical192.
    margin('band_phase_lower7over10',Q(7,6)-Q(27,60)-Q(7,10))
    margin('band_phase_upper5over3',Q(5,3)-Q(112,93)-Q(27,60))
    margin('band_phase_loss_lower_minus3over10',Q(3,10)-Q(9,8)*Q(16,93)-Q(6,60))
    margin('band_phase_loss_upper_minus1over12',Q(9,8)*Q(1,6)-Q(6,60)-Q(1,12))
    margin('band_radial_gap_negative9over5',2+Q(9,8)*Q(1,6)-Q(23,60)-Q(9,5))
    margin('band_modulus_slack_lower3over2',2-Q(30,60)-Q(3,2),True)
    margin('band_modulus_slack_upper5over2',Q(5,2)-2-Q(30,60),True)
    margin('scalar_F_positive',Q(8,3)-173*e)
    margin('selected_cosine_lower_cubic_sign',-(8*Q(15,16)**3-6*Q(15,16)-1))
    margin('selected_cosine_upper_cubic_sign',8*Q(47,50)**3-6*Q(47,50)-1)
    margin('universal_profile_construction_low_cut',3-Q(8,3)-Q(16,93)-10*e)
    return {'values':values,'margins':margins,'margin_count':len(margins),
            'strict_margin_count':sum(not row['closed'] for row in margins.values()),
            'closed_margin_count':sum(row['closed'] for row in margins.values()),
            'scope':'Full sufficient endpoint arithmetic for the uniform ordinary proof, not a proof assistant or an optimality certificate'}

"""Exact identities and endpoints for the ordinary new rigidity proof.
Actual six-sendov-1 / researcher; same-author corroboration, not review.
"""

def pconstant(n, value):
    return {(0,)*n: F(value)} if value else {}

def pvariable(n, index):
    key=[0]*n; key[index]=1
    return {tuple(key):F(1)}

def padd(*terms):
    out={}
    for poly in terms:
        for key,value in poly.items(): out[key]=out.get(key,F(0))+value
    return {key:value for key,value in out.items() if value}

def pscale(poly, coefficient):
    return {key:value*coefficient for key,value in poly.items() if value*coefficient}

def pmul(left,right,degree=None):
    out={}
    for a,x in left.items():
        for b,y in right.items():
            key=tuple(i+j for i,j in zip(a,b))
            if degree is None or sum(key)<=degree:
                out[key]=out.get(key,F(0))+x*y
    return {key:value for key,value in out.items() if value}

def ppow(poly,k,degree=None):
    n=len(next(iter(poly)))
    out=pconstant(n,1)
    for _ in range(k):out=pmul(out,poly,degree)
    return out

def pcproduct(left,right):
    return (padd(pmul(left[0],right[0]),pscale(pmul(left[1],right[1]),-1)),
            padd(pmul(left[0],right[1]),pmul(left[1],right[0])))

def new_algebra_record(damage=None):
    identities=[]
    def identity(name,left,right,variables=None):
        require(left==right,'whole polynomial identity differs: '+name)
        n=variables if variables is not None else len(next(iter(left),next(iter(right),(0,))))
        identities.append({'name':name,'variables':n,'terms':[[list(k),str(v)] for k,v in sorted(left.items())],
                           'whole_two_routes_equal':True})
    x=pvariable(2,0);v=pvariable(2,1)
    displacement=padd(pscale(x,-2),ppow(x,2),ppow(v,2))
    norm={}
    for k in range(4):
        norm=padd(norm,pscale(ppow(displacement,k,3),F((-1)**k*comb(2*k,k),4**k)))
    z=(x,v);zpow=(pconstant(2,1),{})
    geometric={}
    for k in range(4):
        geometric=padd(geometric,zpow[0]);zpow=pcproduct(zpow,z)
    identity('entire_reciprocal_norm_through_cubic',norm,
             padd(pconstant(2,1),x,ppow(x,2),pscale(ppow(v,2),F(-1,2)),
                  ppow(x,3),pscale(pmul(x,ppow(v,2)),F(-3,2))))
    identity('entire_real_geometric_through_cubic',geometric,
             padd(pconstant(2,1),x,ppow(x,2),pscale(ppow(v,2),-1),
                  ppow(x,3),pscale(pmul(x,ppow(v,2)),-3)))
    phasequadratic=F(-1,2) if damage=='wrong-reciprocal-phase-sign' else F(1,2)
    identity('reciprocal_phase_through_cubic',padd(norm,pscale(geometric,-1)),
             padd(pscale(ppow(v,2),phasequadratic),pscale(pmul(x,ppow(v,2)),F(3,2))))
    a=pvariable(3,0);x=pvariable(3,1);v=pvariable(3,2)
    b=padd(a,pscale(x,-1));dsq=padd(ppow(b,2),ppow(v,2))
    identity('radial_exact_numerator',padd(ppow(a,2),pscale(dsq,-1)),
             padd(pscale(pmul(a,x),2),pscale(ppow(x,2),-1),pscale(ppow(v,2),-1)))
    identity('phase_exact_numerator',padd(dsq,pscale(ppow(b,2),-1)),ppow(v,2))
    numerator=pcproduct((x,v),(b,v))
    identity('scaled_complex_real_numerator',numerator[0],
             padd(pmul(a,x),pscale(ppow(x,2),-1),pscale(ppow(v,2),-1)))
    identity('scaled_complex_imaginary_numerator',numerator[1],pmul(a,v))
    z=(x,v);den=(b,pscale(v,-1))
    n2=pcproduct((a,{}),den)
    n2=(padd(n2[0],pcproduct(z,den)[0],pcproduct(z,z)[0]),
        padd(n2[1],pcproduct(z,den)[1],pcproduct(z,z)[1]))
    identity('whole_complex_reciprocal_first_remainder_real',n2[0],ppow(a,2))
    identity('whole_complex_reciprocal_first_remainder_imaginary',n2[1],{},3)
    n3=pcproduct((ppow(a,2),{}),den)
    az=(pmul(a,x),pmul(a,v));z2=pcproduct(z,z);z3=pcproduct(z2,z)
    azden=pcproduct(az,den);z2den=pcproduct(z2,den)
    n3=(padd(n3[0],azden[0],z2den[0],z3[0]),padd(n3[1],azden[1],z2den[1],z3[1]))
    identity('whole_complex_reciprocal_second_remainder_real',n3[0],ppow(a,3))
    identity('whole_complex_reciprocal_second_remainder_imaginary',n3[1],{},3)
    w=[pvariable(8,j) for j in range(8)]
    e2=padd(*(pmul(w[j],w[k]) for j in range(8) for k in range(j+1,8)))
    identity('entire_real_e2_trace',e2,
             pscale(padd(ppow(padd(*w),2),pscale(padd(*(ppow(t,2) for t in w)),-1)),F(1,2)))
    X=[pvariable(16,j) for j in range(8)];v=[pvariable(16,8+j) for j in range(8)]
    e2im=padd(*(padd(pmul(X[j],v[k]),pmul(v[j],X[k])) for j in range(8) for k in range(j+1,8)))
    identity('entire_complex_e2_imaginary_trace',e2im,
             padd(pmul(padd(*X),padd(*v)),pscale(padd(*(pmul(xx,vv) for xx,vv in zip(X,v))),-1)))
    eta=pvariable(2,0);u=pvariable(2,1);one=pconstant(2,1);a=padd(one,pscale(eta,-1))
    identity('entire_scaled_radial_trace_cross',
             padd(pscale(pmul(eta,padd(pmul(a,padd(pconstant(2,8),u)),pconstant(2,-8))),2),pscale(ppow(eta,2),8)),
             padd(pscale(pmul(pmul(eta,a),u),2),pscale(ppow(eta,2),-8)))
    y=pvariable(1,0);C=padd(pconstant(1,F(8,3)),y)
    identity('radial_leading_coefficient',padd(pconstant(1,1),pscale(C,F(-9,8))),
             padd(pconstant(1,-2),pscale(y,F(-9,8))))
    identity('phase_leading_coefficient',pscale(pscale(y,14),F(1,2)),pscale(y,7))
    identity('signed_origin_phase_leading_coefficient',pscale(pscale(y,7),F(9,56)),pscale(y,F(9,8)))
    return {'identities':identities,'identity_count':len(identities),
            'scope':'Whole exact finite polynomials; analytic all-degree reciprocal tail is proved in PROOF.md, not formalized here'}

def new_centered_controls(algebra):
    controls=[]
    for item in algebra['literal_controls']:
        normsq=F(item['radial_norm_squared']);delta=F(item['Delta'])
        if normsq>F(1,40)**2 or (normsq and delta):continue
        error=F(item['phase_loss'])+F(9,56)*delta-F(item['Y'])**2/56
        rho=F(0) if normsq==0 else F(1,40)
        budget=F(3,5)*(rho+delta)*delta
        require(abs(error)<=budget,'literal centered phase bound fails: '+item['name'])
        controls.append({'name':item['name'],'whole_centered_error':str(error),
                         'whole_centered_budget':str(budget),'complete_margin':str(budget-abs(error)),
                         'scope':'Standalone algebraic tuple, no actual original feasibility claim'})
    require(len(controls)==4,'centered controls census')
    return controls

def build_record(damage=None):
    if damage is not None:require(damage in DAMAGE_CASES,'unknown mathematical damage')
    coefficients=coefficient_record(damage);scalars=rigidity_scalar_record(damage)
    algebra=algebra_record(damage);new_algebra=new_algebra_record(damage)
    return {'schema':1,'agent':'six-sendov-1','role':'researcher',
            'proof_status':'Complete ordinary author rigidity lemma; unformalized and independently unreviewed',
            'domain':'ALL nine closed disk originals, ALL eight critical multiplicities, BOTH cuts on EVERY0<eta<=1/12000; physical defect epsilon eta+190eta^2; arbitrary epsilon>=0',
            'standalone_domain':'Finite complex eight-tuples: norm2(|z|-1)<=1/40 and phase delta<=1/1000; centered phase remainder3/5',
            'coefficients':coefficients,'scalars':scalars,
            'algebra':algebra,'new_algebra':new_algebra,
            'new_centered_controls':new_centered_controls(algebra)}
