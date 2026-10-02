"""Independent third-derivative and literal whole-critical-family controls."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import prod
from exact_numbers import I,need,convolution,power,evaluate,derivative
from third import T
from system import system,anchored_integral


def run():
    checks=0
    def check(ok,label):
        nonlocal checks
        need(ok,label);checks+=1
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
        powers=list(ex);factor=F(1)
        for axis in axes:
            if not powers[axis]:return F(0)
            factor*=powers[axis];powers[axis]-=1
        return factor*prod(v**n for v,n in zip(base,powers))
    for ex in sorted(exponents):
        val=T(F(1))
        for i,n in enumerate(ex):val*=T.variable(base[i],i)**n
        check(val.v==literal(ex,()),'literal monomial value')
        for i in range(7):check(val.g.get(i,0)==literal(ex,(i,)),'all seven first partials')
        for i in range(7):
            for j in range(i,7):check(val.h.get((i,j),0)==literal(ex,(i,j)),'all twenty-eight second partials')
        for axes in combinations_with_replacement(range(7),3):check(val.t.get(axes,0)==literal(ex,axes),'all eighty-four third partials')
    samples=[];v=list(map(F,(F(-2,3),F(1,2),F(6,5),F(-1,6),F(1,3),F(-3,4))))
    for eta in (F(1,128),F(1,64),F(1,32)):
        _,_,aux=system(T(eta),list(map(T,v)),F(15,16));p=[x.v for x in aux['poly']];sigma=F(2,5);a=1-eta;r=eta*v[0];s=eta*v[1]
        # Two distinct literal labelled critical multisets at rational delta.
        delta=F(2,7);us=[v[0]+delta,v[0]-delta]+[v[0]]*4
        small=[F(1)]
        for u in us:small=convolution(small,[-eta*u,F(1)])
        heavy=[s*s+eta*v[2],-2*s,F(1)];raw=[9*x for x in convolution(small,heavy)];actual=anchored_integral(list(map(T,raw)),T(a))
        split=[x.v for x in aux['divided_split']];predicted=[p[j]+eta*eta*delta*delta*(split[j] if j<len(split) else 0) for j in range(len(p))]
        check([x.v for x in actual]==predicted,'whole literal split primitive and eta squared normalization')
        check(derivative(predicted)==raw,'whole split derivative critical factor')
        check(evaluate(predicted,a)==0 and evaluate(split,a)==0,'both actual and divided marked anchors')
        generic=[v[0]+F(2*j-5,17) for j in range(6)];generic_factor=[F(1)]
        for u in generic:generic_factor=convolution(generic_factor,[-eta*u,F(1)])
        for j in range(5):
            perm=generic[:];perm[j],perm[j+1]=perm[j+1],perm[j];factor=[F(1)]
            for u in perm:factor=convolution(factor,[-eta*u,F(1)])
            check(factor==generic_factor,'all adjacent label-transposition generators on six distinct inputs')
        # Independent literal antiderivative in shifted X coordinates.
        delta_r=r-s;opening=delta_r*delta_r+eta*v[2]
        reference=[F(0)]*8
        from math import comb
        for n,m in ((7,-F(9,7)),(6,-3*delta_r),(5,-F(9,5)*opening)):
            for j in range(n+1):reference[j]+=m*comb(n,j)*(-r)**(n-j)
        reference[0]=-sum(reference[j]*a**j for j in range(1,8))
        check(reference==split,'entire shifted closed forcing versus literal product integration')
        samples.append({'eta':str(eta),'divided_sigma_forcing':list(map(str,split)),'literal_split_delta':str(delta),'whole_eta_squared_normalization':True})
    check(sum(x*x for x in (1,-1,0,0,0,0))==2 and sum(x*x for x in (1,)*6)==6,'literal centered/common squared norms')
    # A generic permutation-invariant six-real quadratic form reconstructs
    # the split/common factors separately from the analytic response code.
    a,b=F(7,3),F(-1,9);H=[[a*int(i==j)+b for j in range(6)] for i in range(6)]
    split=(1,-1,0,0,0,0);common=(1,)*6
    check(sum(split[i]*H[i][j]*split[j] for i in range(6) for j in range(6))/2==a,'split Rayleigh factor2')
    check(sum(common[i]*H[i][j]*common[j] for i in range(6) for j in range(6))/6==a+6*b,'common Rayleigh factor6')
    damages=[]
    def reject(name,ok):
        try:need(ok,'damaged mathematical object '+name)
        except ValueError:damages.append(name);return
        raise ValueError('damaged object accepted: '+name)
    test=T.variable(F(2),0)**3;wrong=dict(test.t);wrong[(0,0,0)]/=6
    reject('third-derivative-Taylor-confusion',wrong[(0,0,0)]==6)
    test=T.variable(F(2),0)**2*T.variable(F(3),1);wrong=dict(test.t);wrong[(0,0,1)]=0
    reject('omitted-second-eta-mixed',wrong[(0,0,1)]==2)
    test=T.variable(F(2),0)*T.variable(F(3),1)*T.variable(F(4),2);wrong=dict(test.t);wrong[(0,1,2)]=2
    reject('distinct-third-multiplicity',wrong[(0,1,2)]==1)
    bad=predicted[:];bad[0]+=1
    reject('unanchored-split-constant',evaluate(bad,F(31,32))==0)
    bad=[p[j]+eta*delta*delta*(reference[j] if j<len(reference) else 0) for j in range(len(p))]
    reject('lost-eta-split-factor',bad==predicted)
    reject('lost-split-metric-factor2',sum(split[i]*H[i][j]*split[j] for i in range(6) for j in range(6))==a)
    reject('lost-common-metric-factor6',sum(common[i]*H[i][j]*common[j] for i in range(6) for j in range(6))==a+6*b)
    check(len(damages)==7,'all seven changed mathematical objects reject')
    return {'checks':checks,'seven_axis_monomials':len(exponents),'third_entries_per_monomial':84,'third_order_samples':samples,'mathematical_damage_rejections':damages,'literal_split_squared_norm':2,'literal_common_squared_norm':6}
