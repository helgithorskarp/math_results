"""Exact endpoint and definition-level derivative controls for the enclosure kernel."""
from fractions import Fraction as F
from math import prod

from arithmetic import K
from series import series_ring
from system import system
from interval import I,J,C,DEN,require,evaluate
from centered import forcing


def contains(interval,lower,upper):
    return F(interval.lo,DEN)<=lower<=upper<=F(interval.hi,DEN)


def audit(damage=None):
    checks=0

    def check(ok,label):
        nonlocal checks
        require(ok,label);checks+=1

    points=[F(-2),F(-1),F(0),F(1,3),F(1),F(2)]
    boxes=[(a,b) for a in points for b in points if a<=b]
    for a,b in boxes:
        v=I.bounds(a,b)
        check(contains(v,a,b),'rational input rounds outward')
        check(contains(-v,-b,-a),'interval negation')
        check(contains(v.square(),0 if a<=0<=b else min(a*a,b*b),max(a*a,b*b)),
              'square handles zero crossing')
        if a*b>0:
            check(contains(v.inv(),1/b,1/a),'signed reciprocal rounds outward')
        if a>=0:
            root=v.sqrt()
            check(root.lo>=0 and F(root.lo,DEN)**2<=a and F(root.hi,DEN)**2>=b,
                  'integer square root brackets both exact endpoints')
        for d,e in boxes:
            w=I.bounds(d,e);ends=[a*d,a*e,b*d,b*e]
            check(contains(v*w,min(ends),max(ends)),'all four rational product corners')
            check(contains(v+w,a+d,b+e),'all rational sum endpoints')
    # The irrational-looking fractions below are exact rational inputs.
    third=I(F(1,3))
    if damage=='rounding':
        third=I.raw(third.lo,third.lo)
    check(contains(third,F(1,3),F(1,3)),'non-dyadic point requires both directed endpoints')
    rejected=[]
    for name,operation in [('float',lambda:I(0.1)),('zero-inverse',lambda:I.bounds(-1,1).inv()),
                           ('negative-sqrt',lambda:I.bounds(-1,0).sqrt()),
                           ('negative-power',lambda:I(2)**(-1))]:
        try:
            operation()
        except (RuntimeError,ValueError):
            rejected.append(name)
    check(len(rejected)==4,'all arithmetic domain violations reject')

    # Derivatives of monomials are reconstructed from falling factorials,
    # rather than another differentiation jet or an interval fit.
    base=[F(1,2),F(3,2),F(-1,4),F(2),F(-1),F(1,3),F(3,4)]
    inputs=[J.eta(base[0])]+[J.parameter(v,i) for i,v in enumerate(base[1:])]
    exponents=set()
    for n in range(6):
        for i in range(6):
            for m in range(1,4):
                ex=[n]+[0]*6;ex[i+1]=m;exponents.add(tuple(ex))
        for i in range(6):
            for j in range(i+1,6):
                ex=[n]+[0]*6;ex[i+1]=1;ex[j+1]=2;exponents.add(tuple(ex))

    def derivative(ex,axes):
        powers=list(ex);factor=F(1)
        for axis in axes:
            if powers[axis]==0:
                return F(0)
            factor*=powers[axis];powers[axis]-=1
        return factor*prod(v**n for v,n in zip(base,powers))

    for ex in sorted(exponents):
        value=J(1)
        for v,n in zip(inputs,ex):
            value*=v**n
        check(all(contains(v,w,w) for v,w in zip(value.f,
              (derivative(ex,()),derivative(ex,(0,)),derivative(ex,(0,0))/2))),
              'all eta Taylor coefficients match monomial definition')
        for i in range(6):
            g1=value.g[1][i];g2=value.g[2][i]
            if damage=='second-mixed' and ex==(2,1,0,0,0,0,0) and i==0:
                g2=2*g2
            if damage=='mixed-jet' and ex==(1,1,0,0,0,0,0) and i==0:
                g1=I(0)
            expected=derivative(ex,(i+1,));mixed=derivative(ex,(0,i+1));second_mixed=derivative(ex,(0,0,i+1))/2
            check(contains(value.g[0][i],expected,expected) and contains(g1,mixed,mixed) and contains(g2,second_mixed,second_mixed),
                  'parameter, first mixed and normalized second mixed derivatives match monomial definition')

    # Full finite-eta anchoring and derivative-factor coefficients. These
    # controls detect the high-order b_0 anchoring error invisible to J(0).
    sample_data=[]
    for eta in (F(1,128),F(1,64),F(1,32)):
        values=[F(-2,3),F(1,2),F(6,5),F(-1,6),F(1,3),F(-3,4)]
        c=F(15,16)
        _,aux=system(eta,values,c);p=aux['poly'];a=1-eta;x,y,T=values[:3]
        if damage=='anchor':
            r=eta*x;delta=eta*(x-y);B=delta*delta+eta*T
            p[0]+=(-r)**9+F(9,4)*delta*(-r)**8+F(9,7)*B*(-r)**7
        check(evaluate(p,a)==0,'exact finite-eta marked-root anchor')
        r=eta*x;s=eta*y
        factor=[F(1)]
        for _ in range(6):
            nextrow=[F(0)]*(len(factor)+1)
            for j,v in enumerate(factor):
                nextrow[j]-=r*v;nextrow[j+1]+=v
            factor=nextrow
        expected=[F(0)]*9
        for j,v in enumerate(factor):
            for k,w in enumerate((s*s+eta*T,-2*s,F(1))):
                expected[j+k]+=9*v*w
        check([(j+1)*p[j+1] for j in range(9)]==expected,'all derivative-factor coefficients')
        sample_data.append({'eta':str(eta),'anchor':'0','derivative_coefficients':[str(v) for v in expected]})
        Dual=series_ring(1,K)
        for axis in range(3):
            vdual=[Dual([v,int(i==axis)]) for i,v in enumerate(values)]
            _,data=system(Dual(eta),vdual,K(c))
            check(all(data['poly'][j].a[1]==eta*data['partials'][axis][j].a[0] for j in range(10)),
                  'full finite-eta scaled partial versus exact dual differentiation')
    Coeff=series_ring(3,K);t=Coeff([0,1])
    check(1-(1-t)**3==Coeff([0,3,-3,1]),'whole cleared A-cube quotient identity')
    check((1+t)**2-1==Coeff([0,2,1]),'whole cleared W-square quotient identity')
    split_controls=[]
    for eta in (F(1,128),F(1,64),F(1,32)):
        variables=[F(-2,3),F(1,2),F(6,5),F(-1,6),F(1,3),F(-3,4)];c=F(15,16)
        forced,primitive=forcing(eta,variables,c)
        if damage=='split-factor':primitive[7]*=F(7,9)
        if damage=='split-anchor':primitive[0]+=F(1,1000)
        check(evaluate(primitive,1-eta)==0,'full split-forcing marked-root anchor')
        # Literal derivative factors over a separate exact sigma dual number.
        D=series_ring(1,K);sigma=D([0,1]);r=eta*variables[0];s=eta*variables[1];T=variables[2]
        power=[D(1)]
        def times_linear(p,root):
            q=[D(0)]*(len(p)+1)
            for j,v in enumerate(p):q[j]-=root*v;q[j+1]+=v
            return q
        for _ in range(4):power=times_linear(power,r)
        split=[D(0)]*7
        for j,v in enumerate(power):
            for k,b in enumerate((r*r-eta*eta*sigma,-2*r,1)):split[j+k]+=v*b
        derivative=[D(0)]*9
        for j,v in enumerate(split):
            for k,b in enumerate((s*s+eta*T,-2*s,1)):derivative[j+k]+=9*v*b
        literal=[D(0)]+[v/F(j+1) for j,v in enumerate(derivative)]
        literal[0]=-sum((literal[j]*(1-eta)**j for j in range(1,10)),D(0))
        check(all(literal[j].a[1]==eta*eta*(primitive[j] if j<8 else 0) for j in range(10)),
              'every sigma derivative of the literal anchored critical-factor primitive')
        split_controls.append({'eta':str(eta),'divided_sigma_derivative':[str(v) for v in primitive]})
    z=C(F(1,2),F(1,3));inverse=z.inv();identity=z*inverse
    check(contains(identity.re,1,1) and contains(identity.im,0,0),'complex reciprocal covers the exact identity')
    return {'exact_kernel_checks':checks,'rational_interval_boxes':len(boxes),
            'derivative_monomials':len(exponents),'rejected_domains':rejected,
            'finite_eta_controls':sample_data,'full_split_controls':split_controls,'jet_components':21}
