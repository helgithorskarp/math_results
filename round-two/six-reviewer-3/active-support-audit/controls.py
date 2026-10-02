"""Meaningful independent kernel, changed-certificate and real-face controls."""
from fractions import Fraction as F
from math import comb
from exact import P,R,A,need
from face import profiles,complete,base,forms,quad


def run():
    count=0
    def check(ok,label):
        nonlocal count
        need(ok,label);count+=1
    x=P([0,1]);values=(F(-5,4),F(2,3),F(7,2))
    for i in range(10):
        for j in range(10):
            p=(x+2)**i*(2*x-1)**j
            for t in values:check(p.evaluate(t)==(t+2)**i*(2*t-1)**j,'all polynomial coefficients versus direct rational powers')
    for i in range(1,5):
        a=(x+1)**i*(x*x+2);b=(x+1)**(i+1)*(x-3)
        g=a.gcd(b);check(g==(x+1)**i,'nontrivial exact polynomial gcd')
        q,r=a.divide(x*x+1);check(q*(x*x+1)+r==a and len(r.c)<3,'whole quotient/remainder identity and remainder degree')
        z=R(a,b);check(z*R(b,a)==1,'rational function inverse identity')
        for t in values:check(z.evaluate(t)==a.evaluate(t)/b.evaluate(t),'whole normalized rational function evaluation')
    # Exact signed raw-coordinate checks distinguish a=b from a!=b.
    n=12;k=4;p,q=profiles(n,k);c=F(2,n);d=-F(2*n+5,n*n)
    f=[z-1 for z in p];g=[z-c-d*a for a,z in enumerate(q,1)]
    for a,b in ((5,5),(5,6)):
        delta=complete(n,{(a,b):1},True);K,U=forms(n,delta,True)
        pairing=quad(K,p)+quad(U,q)
        coefficient=(2-int(a==b))*comb(n,a)*comb(n-a,b)*(f[a-1]*f[b-1]-g[a-1]*g[b-1])
        check(coefficient==pairing and coefficient!=0,'actual outside-support signed functional, including layer diagonal')
    rejected=[]
    def damage(name,ok):
        try:need(ok,'changed mathematical object '+name)
        except ValueError:rejected.append(name);return
        raise ValueError('damage accepted '+name)
    damage('circle-cubic-factor',x**6+(1+3*x*x)**2==(1+4*x*x)*(1+x*x)**2)
    test=A(1,R(P([0,1])));damage('missing-formal-T-coefficient',test==A(1))
    # Literal Rademacher enumeration is independent of its moment formula.
    N=7;sums=[2*a.bit_count()-N for a in range(1<<N)]
    check(sum(z*z for z in sums)==(1<<N)*N,'literal second moment')
    check(sum(z**4 for z in sums)==(1<<N)*(3*N*N-2*N),'literal fourth moment')
    damage('incorrect-fourth-moment',sum(z**4 for z in sums)==(1<<N)*(3*N*N))
    B=base(n);K,U=forms(n,B);lower=quad(K,p);damage('omitted-unmatched-singleton-J',lower+n*n==4*(2**(n-1)-n-1))
    bad=profiles(n,k)[1];bad[n//2-1]+=1
    gamma=-1-F(1,2*n);damage('changed-central-circle-profile',p[n//2-1]**2+(bad[n//2-1]-gamma)**2==1)
    beta=base(n);beta[(1,2)]+=1;badK,_=forms(n,beta)
    damage('changed-low-affine-completion',all(sum(row)==0 for row in badK))
    damage('lost-original-upper-metric',2*quad(U,q)==quad(U,q))
    for name,operation in (('zero-polynomial-divisor',lambda:P(1).divide(0)),('zero-rational-denominator',lambda:R(1,0)),('floating-polynomial-input',lambda:P(.5)),('unsupported-affine-T-square',lambda:A(0,1)**2)):
        try:operation()
        except (TypeError,ValueError):rejected.append(name)
        else:raise ValueError('invalid domain accepted '+name)
    need(len(rejected)==11,'all seven mathematical and four domain damages reject')
    return {'exact_kernel_checks':count,'polynomial_degree_pairs':100,'direct_rational_sample_points':list(map(str,values)),'literal_Rademacher_order':N,'mathematical_damage_rejections':rejected[:7],'domain_rejections':rejected[7:]}
