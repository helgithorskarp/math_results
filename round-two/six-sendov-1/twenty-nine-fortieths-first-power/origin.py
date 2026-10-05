"""Standalone CLOSED[7/10,29/40] exact origin kernels.
Own c1cf4584119f20ac6c6447541429eaa6717e48de method provenance; no ancestor, peer, reviewer or discovery corpus runtime input.
Unformalized and independently unreviewed; ordinary proof/trust in PROOF.md.
"""
from fractions import Fraction as Q
from math import comb, factorial, isqrt

CAP=[Q(1),Q(0),Q(1,2),Q(151,512),Q(3,16),Q(5,64),
     Q(1,54),Q(13,4096),Q(1,4096)]

def require(test,message):
    if not test:raise ValueError(message)

def quartic_cap_payment(damage=''):
    # For p1=0, Newton gives e4=p2^2/8-p4/4.  Put Xj=zj^2-p2/8:
    # sum Xj^2=p4-p2^2/8 and sum |Xj|^2=M4-|p2|^2/8.
    # Consequently |e4|<=M4/4+|p2|^2/16.
    # The published centered coordinate/moment proof pays M4<=25S^2/32,
    # while |p2|<=S; all complex directions remain in these inequalities.
    n=8;variance_shift=Q(1,n)
    if damage=='quartic-variance-coefficient':variance_shift=Q(1,7)
    require(variance_shift==Q(1,8),'whole squared-variable centering coefficient')
    rewritten=Q(1,8)-variance_shift/4
    require(rewritten==Q(3,32),'whole Newton quartic substitution')
    moment_cap=Q(7,8)**2+Q(1,8)**2
    require(moment_cap==Q(25,32) and Q(1,2)<=moment_cap,
            'whole previously paid centered fourth absolute moment')
    coefficient=rewritten-variance_shift/4
    require(coefficient==Q(1,16) and coefficient>=0,
            'whole quartic variance-norm compensation')
    result=moment_cap/4+coefficient
    require(result==Q(33,128),'whole improved quartic amplitude payment')
    return result

def hilbert_quartic_payment(damage=''):
    # Ordinary external input: Banach's real-Hilbert symmetric norm identity,
    # Carando--Rodriguez1810.09373, Introduction equation(2).
    # For real centered z, p4 in[S^2/8,25S^2/32] and p2=S.
    low,high=Q(1,8)-Q(25,32)/4,Q(1,8)-Q(1,8)/4
    real_norm=max(abs(low),abs(high))
    if damage=='quartic-real-norm-underpay':real_norm=Q(9,128)
    require((low,high,real_norm)==(Q(-9,128),Q(3,32),Q(3,32)),
            'whole real centered quartic norm payment')
    # Re P(x+iy)=P(x)-6L(x,x,y,y)+P(y).
    coefficients=[Q(1),Q(6),Q(1)]
    if damage=='quartic-cross-coefficient':coefficients[1]=Q(5)
    require(coefficients==[Q(comb(4,j)) for j in (0,2,4)],
            'whole real quartic complexification coefficients')
    # 2(X+Y)^2-(X^2+6XY+Y^2)=(X-Y)^2 for X,Y>=0.
    gap=[2-x for x in coefficients]
    gap[1]=Q(4)-coefficients[1]
    require(gap==[Q(1),Q(-2),Q(1)],'whole nonnegative Hilbert norm compensation')
    factor=Q(2)
    if damage=='quartic-Hilbert-factor':factor=Q(1)
    require(factor==2,'whole real-to-complex Hilbert quartic factor')
    cap=factor*real_norm
    require(cap==Q(3,16),'whole literature-assisted complex quartic payment')
    return cap
def add(a,b):
    out=[Q(0)]*max(len(a),len(b))
    for i,x in enumerate(a):out[i]+=x
    for i,x in enumerate(b):out[i]+=x
    return out
def mul(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out
def power(a,n):
    out=[Q(1)]
    for _ in range(n):out=mul(out,a)
    return out
def scale(a,x):return [x*y for y in a]
def pad(a,n):
    require(len(a)<=n,'exact degree bound')
    return a+[Q(0)]*(n-len(a))
def evaluate(a,x):
    out=Q(0)
    for y in reversed(a):out=out*x+y
    return out
def ceiling(x,den=4096):
    require(x>=0,'nonnegative square-root operand')
    n=isqrt(x.numerator*den*den//x.denominator)
    if Q(n,den)**2<x:n+=1
    require(Q(n,den)**2>=x and (n==0 or Q(n-1,den)**2<x),
            'whole minimal rational ceiling')
    return Q(n,den)
def bmul(a,b):
    out={}
    for (i,j),x in a.items():
        if not x:continue
        for (k,l),y in b.items():
            if not y:continue
            key=(i+k,j+l);out[key]=out.get(key,Q(0))+x*y
    return out
def bpower(a,n):
    out={(0,0):Q(1)}
    for _ in range(n):out=bmul(out,a)
    return out
def counts(total,slots):
    if slots==1:
        yield (total,);return
    for first in range(total+1):
        for rest in counts(total-first,slots-1):yield (first,)+rest
def multinomial(terms,n):
    # Independent direct multiplicity enumeration, not repeated convolution.
    items=list(terms.items());out={}
    for multiplicities in counts(n,len(items)):
        exponent=[0,0];value=Q(factorial(n))
        for amount,((i,j),coefficient) in zip(multiplicities,items):
            value*=coefficient**amount/factorial(amount)
            exponent[0]+=i*amount;exponent[1]+=j*amount
        key=tuple(exponent);out[key]=out.get(key,Q(0))+value
    return out
def matrix(polynomial):
    out=[[Q(0)]*10 for _ in range(9)]
    for (i,j),x in polynomial.items():
        require(0<=i<=8 and 0<=j<=9,'whole u8/t9 degree bound')
        out[i][j]+=x
    return out
def integral_rows(rows):
    return [sum((x/Q(j+1) for j,x in enumerate(row)),Q(0)) for row in rows]
def bernstein(a,low,high):
    a=pad(a,9);width=high-low
    translated=[sum((a[j]*comb(j,k)*low**(j-k)*width**k for j in range(k,9)),Q(0))
                for k in range(9)]
    alternate=[Q(0)]*9
    for j,x in enumerate(a):alternate=add(alternate,pad(scale(power([low,width],j),x),9))
    require(translated==alternate,'ALL9 whole interval translation coefficients')
    controls=[sum((translated[k]*Q(comb(i,k),comb(8,k)) for k in range(i+1)),Q(0))
              for i in range(9)]
    reconstructed=[Q(0)]*9
    for i,x in enumerate(controls):
        basis=pad([Q(0)]*i+scale(power([Q(1),Q(-1)],8-i),x*comb(8,i)),9)
        reconstructed=add(reconstructed,basis)
    require(reconstructed==translated,'ALL9 Bernstein reconstruction coefficients')
    return translated,controls

def bernstein10(a,low,high):
    a=pad(a,10);width=high-low
    shifted=[sum((a[j]*comb(j,k)*low**(j-k)*width**k for j in range(k,10)),Q(0))
             for k in range(10)]
    other=[Q(0)]*10
    for j,x in enumerate(a):other=add(other,pad(scale(power([low,width],j),x),10))
    require(shifted==other,'ALL10 cleared interval translation coefficients')
    controls=[sum((shifted[k]*Q(comb(i,k),comb(9,k)) for k in range(i+1)),Q(0))
              for i in range(10)]
    recovered=[Q(0)]*10
    for i,x in enumerate(controls):
        recovered=add(recovered,pad([Q(0)]*i+scale(power([Q(1),Q(-1)],9-i),x*comb(9,i)),10))
    require(recovered==shifted,'ALL10 cleared Bernstein reconstruction')
    return shifted,controls

def payment(box,channel='energy',damage=''):
    contour_cap_payment(damage)
    direct=quartic_cap_payment(damage);hilbert=hilbert_quartic_payment(damage)
    require(CAP[4]==min(direct,hilbert),'quartic amplitude independently paid')
    al,ah,el,eh,fl,fh,L,U,Wl,Wh=map(Q,box[:10])
    tl,th=map(Q,box[10:])
    require(0<al<=ah<1 and 0<L<=U<=1 and 0<=Wl<=Wh and 0<fh<=8,
            'whole conditional marked/mean hypotheses')
    sm=min(Q(1),U**2+Wh,(fh/8)**2)
    anchor=min(al,2*L/(L**2+Wh)-ah,2*U/(U**2+Wh)-ah)
    if anchor<=0:return dict(status='unavailable-nonpositive-anchor')
    original_anchor=anchor
    if damage=='drop-upper-anchor':anchor=min(al,2*L/(L**2+Wh)-ah)
    if damage=='drop-lower-anchor':anchor=min(al,2*U/(U**2+Wh)-ah)
    if damage=='anchor-above-marked':anchor=ah+Q(1,100)
    require(anchor==original_anchor,'BOTH exact endpoint anchor payments')
    require(0<anchor<=al and 2*L>=(anchor+ah)*(L**2+Wh)
            and 2*U>=(anchor+ah)*(U**2+Wh),'whole concave anchor endpoint signs')
    if channel=='energy':
        sp=[eh-8-8*Wl,Q(16),Q(-8)];smin=evaluate(sp,L);smax=evaluate(sp,U)
        expected_sp=[eh-8*(1+Wl),Q(16),Q(-8)]
    elif channel=='joint':
        sp=[th+2*fh-8-8*Wl,Q(0),Q(-8)];smin=evaluate(sp,U);smax=evaluate(sp,L)
        expected_sp=[th+2*fh-8*(1+Wl),Q(0),Q(-8)]
    else:raise ValueError('explicit single polynomial centered-energy channel')
    if damage=='centered-energy-decouple':sp[0]=eh
    require(sp==expected_sp,'whole retained centered-energy identity')
    if smin<0:return dict(status='unavailable-negative-whole-energy-envelope',
                          channel=channel,Sminimum=smin)
    require(0<=smin<=smax,'whole centered-energy envelope signs')
    beta={(0,0):Q(1),(1,1):-2*anchor,(2,2):anchor**2,(0,2):anchor**2*Wh}
    root={(0,0):Q(1),(1,1):-anchor,(0,2):anchor**2*Wh/(2*(1-anchor*U))}
    expected_root=anchor**2*Wh/(2-2*anchor*U)
    if damage=='odd-root-underpay':root[(0,2)]*=Q(999,1000)
    require(root[(0,2)]==expected_root and 1-anchor*U>0,'whole odd square-root payment')
    endpoint=[Q(1)+anchor**2*Wh,-2*anchor,anchor**2]
    bl=evaluate(endpoint,L)
    require(0<evaluate(endpoint,U)<=bl<1,'whole endpoint beta monotonicity and signs')
    dm,db,dS=ceiling(sm),ceiling(bl),ceiling(smax)
    if damage=='synchronized-denominator':dm=ceiling(min(sm,L**2+Wh))
    require(dm==ceiling(min(Q(1),U**2+Wh,(fh/8)**2)),
            'actual mean norm must remain separate from beta envelope')
    require(dm>0 and 1-db*bl**4>0,'whole positive diagonal gate')
    ordinary4=pad(power(endpoint,4),9)
    # Independent direct3-term endpoint multinomial, including zero slots.
    other4=matrix(multinomial({(i,0):v for i,v in enumerate(endpoint)},4))
    require(ordinary4==[row[0] for row in other4],'ALL9 diagonal endpoint coefficients')
    D=scale(ordinary4,-db/(ah*dm));D[0]+=1/(ah*dm)
    if damage=='diagonal-last-coefficient':D[-1]+=Q(1,1000)
    expectedD=[((Q(1) if i==0 else Q(0))-db*x)/(ah*dm) for i,x in enumerate(ordinary4)]
    require(D==expectedD,'ALL9 diagonal coefficients')
    St={(i,0):x for i,x in enumerate(sp)}
    terms=[];R=[Q(0)]*9
    for k in range(2,9):
        n=(8-k)//2;factor=9*ah**k*CAP[k]*(dS if k%2 else 1)
        base=bmul(bpower(beta,n),bpower(St,k//2))
        if k%2:base=bmul(base,root)
        primary=matrix({(i,j+k):v*factor for (i,j),v in base.items()})
        if damage=='last-bivariate-coefficient' and k==8:primary[-1][-1]+=Q(1,1000)
        # Separately enumerate multiplicities in BOTH polynomial powers,
        # then integrate the raw monomial terms before merging coefficients.
        be=multinomial(beta,n);se=multinomial(St,k//2)
        choices=list(root.items()) if k%2 else [((0,0),Q(1))]
        alternate=[[Q(0)]*10 for _ in range(9)];second_integral=[Q(0)]*9
        for (i,j),x in be.items():
            for (r,s),y in se.items():
                for (v,w),z in choices:
                    a,b=i+r+v,j+s+w+k;value=factor*x*y*z
                    require(a<=8 and b<=9,'multinomial whole degree bounds')
                    alternate[a][b]+=value;second_integral[a]+=value/Q(b+1)
        require(primary==alternate,'ALL90 centered u/t coefficients order'+str(k))
        value=integral_rows(primary)
        require(value==second_integral,'ALL9 integrated coefficients order'+str(k))
        if damage=='drop-eighth' and k==8:continue
        terms.append(dict(order=k,coefficients=primary,integral_coefficients=value))
        R=add(R,value)
    require([t['order'] for t in terms]==list(range(2,9)),'ALL seven centered orders')
    lower=[d-r for d,r in zip(D,R)]
    shifted,controls=bernstein(lower,L,U)
    if damage=='last-Bernstein-control':controls[-1]+=Q(1,1000)
    # Reconstruct the full whole-u polynomial after any proposed controls.
    recovered=[Q(0)]*9
    for i,x in enumerate(controls):
        recovered=add(recovered,pad([Q(0)]*i+scale(power([Q(1),Q(-1)],8-i),x*comb(8,i)),9))
    require(recovered==shifted,'ALL9 final Bernstein controls paid')
    # Retain u in the ACTUAL mean-norm denominator too.  For u>=L>0,
    # |mu|<=sqrt(u^2+Wh)<=u+Wh/(2u)<=u+Wh/(2L).
    denominator=[ah*Wh/(2*L),ah]
    if damage=='linear-norm-root-underpay':denominator[0]*=Q(999,1000)
    require(denominator==[ah*Wh/(2*L),ah] and evaluate(denominator,L)>0,
            'whole positive linear mean-norm payment')
    numerator=pad(scale(ordinary4,-db),10);numerator[0]+=1
    require(numerator==pad(scale(D,ah*dm),10),'ALL10 diagonal numerator coefficients')
    cleared=pad(add(numerator,scale(mul(denominator,add([Q(1)],R)),-1)),10)
    loss_rows=[[Q(0)]*10 for _ in range(10)]
    aggregate={}
    for term in terms:
        for i,row in enumerate(term['coefficients']):
            for j,x in enumerate(row):
                aggregate[i,j]=aggregate.get((i,j),Q(0))+x
                for k,y in enumerate(denominator):loss_rows[i+k][j]+=x*y
    product=bmul({(i,0):x for i,x in enumerate(denominator)},aggregate)
    require(loss_rows==[[product.get((i,j),Q(0)) for j in range(10)] for i in range(10)],
            'ALL100 linear-denominator remainder coefficients')
    alternate=add(numerator,scale(pad(denominator,10),-1))
    alternate=add(alternate,scale([sum((x/Q(j+1) for j,x in enumerate(row)),Q(0))
                                  for row in loss_rows],-1))
    if damage=='last-cleared-coefficient':cleared[-1]+=Q(1,1000)
    require(cleared==alternate,'ALL10 cleared origin coefficients')
    cleared_shift,cleared_controls=bernstein10(cleared,L,U)
    if damage=='tenth-Bernstein-control':cleared_controls[-1]+=Q(1,1000)
    cleared_recovered=[Q(0)]*10
    for i,x in enumerate(cleared_controls):
        cleared_recovered=add(cleared_recovered,pad([Q(0)]*i+
            scale(power([Q(1),Q(-1)],9-i),x*comb(9,i)),10))
    require(cleared_recovered==cleared_shift,'ALL10 final cleared Bernstein controls paid')
    pmin=min(cleared_controls)
    dmin,dmax=evaluate(denominator,L),evaluate(denominator,U)
    require(0<dmin<=dmax,'whole strictly positive linear denominator endpoints')
    # Sign matters when dividing the lower criterion by a variable denominator.
    rational_score=1+pmin/(dmax if pmin>=0 else dmin)
    return dict(status='bounded',channel=channel,anchor=anchor,
        anchor_lower_slack=2*L-(anchor+ah)*(L**2+Wh),
        anchor_upper_slack=2*U-(anchor+ah)*(U**2+Wh),
        beta=matrix(beta),odd_root=matrix(root),actual_mean_norm_bound=sm,
        mean_root=dm,beta_root=db,centered_root=dS,
        S_polynomial=sp,Sminimum=smin,Smaximum=smax,
        D_coefficients=D,R_coefficients=R,lower_coefficients=lower,
        rescaled_lower_coefficients=shifted,bernstein_controls=controls,
        score=max(min(controls),rational_score),polynomial_score=min(controls),
        linear_mean_denominator=denominator,diagonal_numerator=numerator,
        cleared_loss_coefficients=loss_rows,cleared_coefficients=cleared,
        rescaled_cleared_coefficients=cleared_shift,cleared_Bernstein_controls=cleared_controls,
        cleared_minimum=pmin,rational_denominator_score=rational_score,
        all_ten_cleared_controls=True,terms=terms,all_whole_coefficients_compared=True,
        all_seven_orders=True,all_nine_controls=True,
        original_feasibility_asserted=False,formalized=False,independent_review=False)

def clean(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [clean(v) for v in x]
    return x


def contour_cap_payment(damage=''):
    # Coefficient contour + AM-GM for ALL8 complex zero-sum slots:
    # |e_k| <= r^-k (1+r^2*S/8)^4, r^2=8k/((8-k)S).
    # The continuum argument is in PROOF_DRAFT.md and the credited literature.
    rows=[]
    exact={5:Q(512,84375),6:Q(1,2916),7:Q(8,823543)}
    for k in range(2,8):
        square=Q(8**(8-k), k**k*(8-k)**(8-k))
        stationary=Q(8*k,8-k)
        alternative=(1+stationary/8)**8/stationary**k
        require(square==alternative,'whole optimized contour normalization order'+str(k))
        if k in exact:
            require(square==exact[k],'whole explicit high-order contour square')
            cap=ceiling(square) if k!=6 else Q(1,54)
            if damage=='contour-underpay-'+str(k):cap-=Q(1,4096)
            require(cap>=0 and cap**2>=square,'whole paid high-order contour cap order'+str(k))
            require(cap==CAP[k],'whole final centered contour cap order'+str(k))
        else:cap=None
        rows.append(dict(order=k,stationary_radius_square_times_S=stationary,
                         full_contour_cap_square=square,selected_cap=cap))
    require(CAP[5:8]==[Q(5,64),Q(1,54),Q(13,4096)],'all three selected contour payments')
    return rows
