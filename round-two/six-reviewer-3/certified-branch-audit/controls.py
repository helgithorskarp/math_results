"""Definition-level controls; no author's modules, jets or interval engine."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import prod
from exact_numbers import K,I,D,Z,need,down,up,embedding,equations,evaluate,derivative


def run():
    checks=0
    def check(ok,label):
        nonlocal checks
        need(ok,label);checks+=1
    def enclosed(v,a,b):return v.lo<=a<=b<=v.hi
    points=tuple(map(F,(-2,-1,0,1,2)))+(F(1,3),)
    boxes=[I(a,b) for a in points for b in points if a<=b]
    for a in boxes:
        check(enclosed(a.square(),0 if a.lo<=0<=a.hi else min(a.lo**2,a.hi**2),max(a.lo**2,a.hi**2)),'literal square extrema')
        if not a.lo<=0<=a.hi:check(enclosed(a.inv(),1/a.hi,1/a.lo),'signed exact reciprocal')
        if a.lo>=0:
            s=a.sqrt();check(s.lo>=0 and s.lo**2<=a.lo and s.hi**2>=a.hi,'root brackets exact rational endpoints')
        for b in boxes:
            corners=[x*y for x in (a.lo,a.hi) for y in (b.lo,b.hi)]
            check(enclosed(a*b,min(corners),max(corners)),'four product corners')
            check(enclosed(a+b,a.lo+b.lo,a.hi+b.hi),'exact sum endpoints')
    for a in (F(-7,3),F(1,3),F(1001,999)):
        check(down(a)<=a<=up(a),'signed recording endpoints')
    domains=[]
    for name,op in (
        ('float',lambda:I(0.1)),('zero-divisor',lambda:I(-1,1).inv()),
        ('negative-root',lambda:I(-1,0).sqrt()),('negative-power',lambda:I(2)**-1),
        ('field-zero',lambda:K(0).inv()),('complex-zero',lambda:Z(1)/Z(0)),
        ('nonconstant-tensor-divisor',lambda:D(1)/D.variable(F(2),1))):
        try:op()
        except ValueError:domains.append(name)
    check(len(domains)==7,'all arithmetic domain violations reject')
    c=K((0,1,0));check(8*c**3-6*c-1==0,'literal cubic relation')
    for x in (K(1),c,c*c,1+c,2-c,1+c+c*c):
        check(x*x.inv()==1 and x.inv()*x==1,'cubic multiplication matrix inverse')
    base=(F(2,3),F(-5,4),F(3,2),F(7,5),F(-2,7),F(1,6),F(9,8))
    exponents=set()
    for degree in range(4):
        for axes in combinations_with_replacement(range(7),degree):
            ex=[0]*7
            for axis in axes:ex[axis]+=1
            exponents.add(tuple(ex))
    for axis in range(7):
        for degree in range(4,10):
            ex=[0]*7;ex[axis]=degree;exponents.add(tuple(ex))
    def literal(ex,axes):
        p=list(ex);f=F(1)
        for i in axes:
            if not p[i]:return F(0)
            f*=p[i];p[i]-=1
        return f*prod(v**n for v,n in zip(base,p))
    for ex in sorted(exponents):
        value=D(F(1))
        for i,n in enumerate(ex):value*=D.variable(base[i],i)**n
        check(value.v==literal(ex,()),'monomial value from powers')
        for i in range(7):check(value.g.get(i,0)==literal(ex,(i,)),'all seven monomial first derivatives')
        for i in range(7):
            for j in range(i,7):check(value.h.get((i,j),0)==literal(ex,(i,j)),'all twenty-eight symmetric Hessian entries')
    finite=[]
    for eta in (F(1,128),F(1,64),F(1,32)):
        v=[F(-2,3),F(1,2),F(6,5),F(-1,6),F(1,3),F(-3,4)]
        _,a=equations(D.variable(eta,0),[D.variable(x,i+1) for i,x in enumerate(v)],F(15,16))
        p=[x.v for x in a['poly']];marked=1-eta
        check(evaluate(p,marked)==0,'literal positive-eta marked root')
        r=eta*v[0];s=eta*v[1]
        # Binomial coefficients from the derivative factor, independently of
        # the main shifted-power convolution and differential tensors.
        from math import comb
        powers=[comb(6,j)*(-r)**(6-j) for j in range(7)]
        expected=[F(0)]*9
        for j,t in enumerate(powers):
            for k,b in enumerate((s*s+eta*v[2],-2*s,F(1))):expected[j+k]+=9*t*b
        check(derivative(p)==expected,'all literal derivative-factor coefficients')
        for axis in range(3):
            check(all(coef.g.get(axis+1,0)==eta*partial.v for coef,partial in zip(a['poly'],a['partials'][axis])),'finite-eta anchored partials versus full Hessian engine')
        finite.append({'eta':str(eta),'marked_root_value':'0','derivative_factor_coefficients':list(map(str,expected))})
    # G(0,v)=0 throughout parameter space, not only at v0. Its polynomial
    # divisibility is proved in REVIEW.md; these are whole-definition controls.
    for j in range(5):
        v=[K(F((i+2)*(j+1),i+j+3)) for i in range(6)]
        G,_=equations(D.variable(K(0),0),[D.variable(x,i+1) for i,x in enumerate(v)],c)
        check(all(g.v==0 and all(g.g.get(i,0)==0 for i in range(1,7)) for g in G),'generic eta-zero numerator and parameter-gradient vanish')
    identity=Z(F(2,3),F(-3,7))/Z(F(2,3),F(-3,7))
    check(enclosed(identity.re,1,1) and enclosed(identity.im,0,0),'complex division includes literal unit')
    damages=[]
    def reject(name,op):
        try:op()
        except ValueError:damages.append(name);return
        raise ValueError('damaged mathematics accepted: '+name)
    bad_cube=K((0,1,0));reject('wrong-cubic-sign',lambda:need(8*bad_cube**3-6*bad_cube+1==0,'altered field relation'))
    a=I(2).sqrt();reject('root-rounded-inward',lambda:need(a.lo**2>=2,'lower endpoint promoted to upper bound'))
    mixed=D.variable(F(2),0)*D.variable(F(3),1);mixed.h[(0,1)]=0
    reject('erased-mixed-derivative',lambda:need(mixed.h[(0,1)]==1,'literal mixed derivative of xy'))
    diagonal=D.variable(F(2),0)**2;diagonal.h[(0,0)]=1
    reject('halved-diagonal-Hessian',lambda:need(diagonal.h[(0,0)]==2,'literal second derivative of x squared'))
    _,a=equations(D(F(1,32)),list(map(D,(F(-2,3),F(1,2),F(6,5),F(-1,6),F(1,3),F(-3,4)))),F(15,16))
    p=[x.v for x in a['poly']];r=F(1,32)*F(-2,3);delta=F(1,32)*(F(-2,3)-F(1,2));opening=delta**2+F(1,32)*F(6,5)
    p[0]+=(-r)**9+F(9,4)*delta*(-r)**8+F(9,7)*opening*(-r)**7
    reject('retained-unanchored-constant',lambda:need(evaluate(p,F(31,32))==0,'actual finite-eta anchor'))
    p=[x.v for x in a['poly']];p[8]+=1
    reject('altered-critical-factor',lambda:need(derivative(p)==expected,'damaged derivative coefficients'))
    px=[x.v for x in a['partials'][0]];px[0]+=1
    reject('altered-anchored-partial',lambda:need(evaluate(px,F(31,32))==0,'damaged scaled partial anchor'))
    G[0].v+=1
    reject('nondivisible-equation-numerator',lambda:need(all(g.v==0 for g in G),'literal eta-zero numerator'))
    check(len(damages)==8,'all eight altered mathematical objects reject')
    return {'checks':checks,'interval_boxes':len(boxes),'seven_axis_monomials':len(exponents),
            'hessian_entries_per_monomial':28,'domain_rejections':domains,'mathematical_damage_rejections':damages,
            'finite_eta_controls':finite,'eta_zero_generic_parameter_controls':5}
