"""Independent literal Laurent/Fourier and uniform budget audit of LEMMA9588.

Defining mathematics is visible; no author executable or fixture is an input.
The exact polynomial kernel is owned reuse from REVIEW9598/9506.
"""
from fractions import Fraction as F
from math import comb
from polys import Poly, cast, symbol, need

def conj(p):
    return p.conjugate_coefficients()

def real(p):
    return (p+conj(p))/2

def norm2(p):
    return p*conj(p)

def cx(name):
    return symbol(name+'R')+cast((0,1))*symbol(name+'I')

def product(xs):
    out=cast(1)
    for x in xs:out*=x
    return out

def convolve(a,b):
    out=[cast(0) for _ in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def polynomial_roots(roots):
    p=[cast(1)]
    for r in roots:p=convolve(p,[-r,cast(1)])
    return p

def evaluate(p,z):
    out=cast(0)
    for x in reversed(p):out=out*z+x
    return out

def scalar(p):
    need(not any(k for k in p.terms),'constant required')
    return p.terms.get((),(F(0),F(0)))

def audit():
    checks=[];damages=[];records={}
    def equal(a,b,label):
        need(a==b,label);checks.append(label)
    def damaged(a,b,label):
        need(a!=b,label+' did not reject');damages.append(label)
    # Build the FULL degree-nine polynomial before reducing at ninth roots.
    d=[cx('d'+str(i)) for i in range(9)]
    p=[d[0]-1]+d[1:]+[cast(1)]
    rows=[cast(0) for _ in range(9)]
    for k,pk in enumerate(p):
        for l,pl in enumerate(p):rows[(k-l)%9]+=(k+l-9)*pk*conj(pl)
    # A second route derives each row from its complete literal pair table.
    tables=[]
    for m in range(9):
        terms=[];expected=cast(0)
        for k in range(9):
            if k==m:expected+=9*d[k]
            if (-k)%9==m:expected+=9*conj(d[k])
            for l in range(9):
                if (k-l)%9==m:
                    terms.append([k,l,k+l-9]);expected+=(k+l-9)*d[k]*conj(d[l])
        equal(rows[m],expected,'full cyclic row '+str(m));tables.append(terms)
    diag=18*real(d[0])+sum(((2*k-9)*norm2(d[k]) for k in range(9)),cast(0))
    equal(rows[0],diag,'complete zero row')
    q1=sum(((2*j-8)*d[j+1]*conj(d[j]) for j in range(8)),cast(0))-d[0]*conj(d[8])
    q2=sum(((2*j-7)*d[j+2]*conj(d[j]) for j in range(7)),cast(0))-2*d[0]*conj(d[7])
    equal(rows[1],9*(d[1]+conj(d[8]))+q1,'complete first wrap')
    equal(rows[2],9*(d[2]+conj(d[7]))+q2,'complete second wrap')
    for m in range(1,9):equal(rows[9-m],conj(rows[m]),'cyclic reality '+str(m))
    damaged(rows[1],9*(d[1]+conj(d[8]))+q1+d[0]*conj(d[8]),'missing first wrap')
    damaged(rows[2],9*(d[2]+conj(d[7]))+q2+d[1]*conj(d[8]),'invented second extra wrap')
    damaged(rows[1],9*(d[1]+d[8])+q1,'lost top complex conjugate')
    records['rows']=[x.record() for x in rows];records['literal_pair_tables']=tables

    # Root positivity is an ordinary product theorem; certify its local
    # factor identity universally on the circle, without any division.
    u,v=symbol('u'),symbol('v');w=u+cast((0,1))*v;r=cx('r')
    circle=2*real(w*conj(w-r))-norm2(w-r)-(1-norm2(r))
    equal(circle,u*u+v*v-1,'universal individual root factor')
    equal(circle.reduce_square('v',1-u*u),cast(0),'whole circle quotient')
    damaged(circle+norm2(r),u*u+v*v-1,'lost root norm factor')

    # Genuine rational complex root products, boundary zeros and collisions.
    anchor=F(65535,65536)
    controls=[
        [(0,0)]*9,[(1,0)]*9,[(anchor,0)]+[(0,0)]*8,
        [(anchor,0),(1,0),(-1,0),(0,1),(0,-1),(F(3,5),F(4,5)),(F(3,5),F(-4,5)),(0,0),(0,0)],
        [(anchor,0)]+[(F(1,3),F(1,4))]*4+[(F(-1,5),F(2,5))]*4,
        [(anchor,0),(F(1,4),F(1,2)),(F(1,4),F(1,2)),(F(-2,3),F(1,7)),(F(1,2),0),(0,F(1,2)),(0,0),(F(-1,4),0),(0,F(-1,4))],
    ]
    points=[(1,0),(-1,0),(0,1),(0,-1),(F(3,5),F(4,5)),(F(5,13),F(12,13))]
    root_records=[]
    for ci,root_values in enumerate(controls):
        roots=[cast(x) for x in root_values];coeff=polynomial_roots(roots)
        derivative=[k*coeff[k] for k in range(1,10)]
        values=[]
        for wi,point in enumerate(points):
            z=cast(point);pz=evaluate(coeff,z)
            direct=2*real(z*evaluate(derivative,z)*conj(pz))-9*norm2(pz)
            rhs=sum(((1-norm2(roots[i]))*product(norm2(z-roots[j]) for j in range(9) if j!=i) for i in range(9)),cast(0))
            equal(direct,rhs,'literal root product '+str(ci)+'/'+str(wi))
            re,im=scalar(direct);need(im==0 and re>=0,'root weight nonnegative')
            values.append(str(re))
        root_records.append({'roots':[[str(a),str(b)] for a,b in root_values],'weights':values})
    records['literal_root_controls']=root_records

    # All anchor geometric inequalities are whole polynomial identities.
    eta=symbol('eta');a=1-eta
    anchor_coeff=[symbol('c'+str(k)) for k in range(1,9)]
    c0=-a**9-sum((anchor_coeff[k-1]*a**k for k in range(1,9)),cast(0))
    equal(a**9+c0+sum((anchor_coeff[k-1]*a**k for k in range(1,9)),cast(0)),cast(0),'entire anchored polynomial')
    for m in range(1,10):
        geom=sum((a**j for j in range(m)),cast(0))
        equal(1-a**m,eta*geom,'all anchor power difference '+str(m))
    equal(8*a*a-(8+3*eta)*a**3,5*eta-7*eta**2-eta**3+3*eta**4,'full low sublevel slack')

    # Newton derivation via monic derivative coefficients, not root matching.
    U,T2,T3=symbol('U'),symbol('T2'),symbol('T3')
    b1=-U;b2=(U**2-T2)/2;b3=(-U**3+3*U*T2-2*T3)/6
    equal(U+b1,cast(0),'Newton first')
    equal(T2+b1*U+2*b2,cast(0),'Newton second')
    equal(T3+b1*T2+b2*U+3*b3,cast(0),'Newton third')
    equal(F(9,6)*b3,-U**3/4+F(3,4)*U*T2-T3/2,'whole c6 Newton')
    damaged(F(9,6)*b3,-U**3/4-F(3,4)*U*T2-T3/2,'Newton mixed sign')
    records['newton']=[x.record() for x in [b1,b2,b3]]

    # Rebuild each norm envelope from the literal pair table. Internal lower
    # products have absolute coefficient <=8 or7; their selected sum <=L².
    e,x,y,L,v1,v2=[symbol(s) for s in ['eta','x','y','L','v1','v2']]
    D0=9*e+x+y+L
    bounds=[D0,v1,v2,L,L,L,L,y,x]
    qnorm=[];categories=[]
    for m,max_internal in [(1,8),(2,7)]:
        costs={'lower':[], 'special':[]};total=cast(0)
        for k,l,c in tables[m]:
            if not c:continue
            if 1<=k<=6 and 1<=l<=6:
                need(abs(c)<=max_internal,'complete lower norm coefficient');costs['lower'].append([k,l,c])
            else:
                costs['special'].append([k,l,c]);total+=abs(c)*bounds[k]*bounds[l]
        total+=max_internal*L**2;qnorm.append(total);categories.append(costs)
    equal(qnorm[0],D0*x+6*x*y+8*D0*v1+8*L**2+4*y*L,'entire Q1 norm envelope')
    equal(qnorm[1],2*D0*y+7*D0*v2+7*L**2+3*y*L+5*x*L,'entire Q2 norm envelope')
    kap=F(113,512);alpha=F(151,1024)
    need(F(14,9)*kap-F(5,18)==F(151,2304),'mean y coefficient')
    mean=F(45,8)*e+F(151,2048)*y-9*e**2-F(8,9)*x**2-e*x
    diagonal_bound=(18*(9*e-mean+8*e*x+7*e*y+L)+7*x**2+5*y**2+3*L**2)/9
    diag_expected=F(27,4)*e-alpha*y+18*e**2+18*e*x+14*e*y+2*L+F(23,9)*x**2+F(5,9)*y**2+L**2/3
    equal(diagonal_bound,diag_expected,'complete D/9 bound')
    nx=diagonal_bound+qnorm[0]/9+v1
    ny=diagonal_bound+qnorm[1]/9+v2
    manual_x=F(27,4)*e-alpha*y+18*e**2+19*e*x+14*e*y+2*L+F(8,3)*x**2+F(5,9)*y**2+F(7,9)*x*y+L*x/9+F(11,9)*L**2+F(4,9)*y*L+v1*(1+F(8,9)*D0)
    manual_y=diag_expected+F(2,9)*D0*y+F(7,9)*D0*v2+F(7,9)*L**2+y*L/3+F(5,9)*x*L+v2
    equal(nx,manual_x,'whole top first norm bound')
    equal(ny,manual_y,'whole top second norm bound')
    damaged(nx+alpha*y,manual_x,'lost favorable mean term')
    damaged(nx-D0*x/9,manual_x,'lost first norm wrap cost')
    damaged(ny+F(2,9)*D0*y,manual_y,'duplicated second norm wrap cost')
    records['norm_categories']=categories;records['norm_bounds']=[nx.record(),ny.record()]

    # Reprove the convergent binomial-square envelope with its whole sign
    # numerator. The infinite-series/triangle bridge is written in REVIEW.
    r=symbol('rho')
    equal((4-7*r)**2-16*(1-2*r)*(1-r)**2,r*(8-31*r+32*r*r),'whole square-tail sign polynomial')
    need(8-F(31,6)>0,'whole rho<=1/6 sign floor')
    need(F(5,8)/(1-F(1,6))==F(3,4),'cubic tail budget')
    need(F(1,4)-F(5,4)*F(3,128)==kap,'full square energy coefficient')
    # Monotonicity: b[n+1]/b[n]=(2n+1)/(2n+2)<1 universally n>=0.
    need(F(comb(6,3),4**3)==F(5,16),'binomial cubic coefficient')

    budgets={}
    for h in [30,32]:
        E=F(1,256);endpoint=E**2;dsmall=F(1,1000);Y0=F(9,2)*h
        lower=[F(9,k)*comb(8,9-k)*2**(9-k)*E**(7-k) for k in range(1,7)]
        need(sum(lower)<3 and max(lower[:2])<dsmall,'whole initial lower budget')
        # h=32 permits equality in sqrt(h/8)<=2; strict budgets remain strict.
        need(h<=32 and F(h)*(F(256,255))**2<36,'uniform critical radius')
        K0=18+14*Y0+F(5,9)*Y0**2+11+F(4,9)*Y0*3+F(8,9)*(9+Y0+3)*dsmall
        constant=F(27,4)+6+dsmall+endpoint*K0
        lam=F(8,3)*18*E+(19+F(7,9)*Y0+F(1,3)+F(8,9)*dsmall)*endpoint
        need(constant<13 and lam<F(1,5),'uniform first mean bootstrap')
        X,Y,C,u3,cube=(F(17),F(20),F(3,8),F(16),F(165)) if h==30 else (F(17),F(21),F(2,5),F(15),F(182))
        ybound=F(9,14)*(h+F(64,81)*17**2*endpoint)
        need(ybound<Y and F(8,9)*F(65,4)<u3,'mean and second coefficient scales')
        need(cube*cube>h**3,'uniform third moment constant')
        tail=sum(lower[:5])+u3**3*endpoint**2/4+F(3,4)*u3*h*endpoint+cube*E/2
        need(tail<C,'improved whole lower tail')
        # Extract the ENTIRE quadratic cost from derived multivariate bounds.
        subst={'x':X*e,'y':Y*e,'L':C*e,'v1':dsmall*e,'v2':dsmall*e}
        final_x=(nx+alpha*y).substitute(subst)
        final_y=(ny+alpha*y).substitute(subst)
        base=F(27,4)+2*C+dsmall
        Kx=scalar(final_x.coefficient('eta',2))[0];Ky=scalar(final_y.coefficient('eta',2))[0]
        equal(final_x,base*e+Kx*e**2,'entire final x budget '+str(h))
        equal(final_y,base*e+Ky*e**2,'entire final y budget '+str(h))
        need(max(Kx,Ky)<2000,'whole final quadratic budget')
        cap=base+2000*endpoint;need(cap<F(31,4),'strict full-window cap')
        budgets[str(h)]={k:str(v) for k,v in {'Y0':Y0,'initial_constant':constant,'lambda':lam,'first_x_cap':F(65,4),'y_bound':ybound,'y_cap':Y,'U_cap':u3,'third_moment_constant':cube,'lower_tail':tail,'lower_cap':C,'Kx':Kx,'Ky':Ky,'cap':cap,'strict_cap_margin':F(31,4)-cap}.items()}
        budgets[str(h)]['initial_lower']=[str(v) for v in lower]
        damaged(final_x+e**2,base*e+Kx*e**2,'quadratic cost damage '+str(h))
    need(F(budgets['30']['initial_constant'])==F(2543621,196608),'entire original first constant')
    need(F(budgets['30']['lambda'])==F(3490969,18432000),'entire original lambda')
    need(F(budgets['30']['lower_tail'])==F(394463351305,1099511627776),'entire original lower sum')
    need(F(budgets['30']['Kx'])==F(135546343,72000) and F(budgets['30']['Ky'])==F(14216983,8000),'both original quadratic costs')
    records['budgets']=budgets
    records['checks']=checks;records['damage_rejections']=damages
    return records
