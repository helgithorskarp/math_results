"""Independent Laurent/cube-field and exact-budget corroboration.

All arithmetic is Fraction. A monomial is (cube phase, sorted (token,power)
pairs), with omega**2=-1-omega. Powers of u may be negative: the ordinary
proof first establishes |u|>0. Complex conjugation exchanges explicit
formal tokens and omega with omega**2. No author source is imported.
Finite controls corroborate identities, not actual original-disk feasibility.
"""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import hashlib,json,sys

def need(x,msg):
    if not x: raise ValueError(msg)

def clean(p): return {k:v for k,v in p.items() if v}
def add(*ps):
    d={}
    for p in ps:
        for k,v in p.items():d[k]=d.get(k,Q(0))+v
    return clean(d)
def sc(p,x): return clean({k:v*x for k,v in p.items()})
def cn(x): return {(0,()):Q(x)} if x else {}
def tok(v,n=1): return {(0,((v,n),)):Q(1)} if n else cn(1)
def phase(n):
    n%=3
    return {(n,()):Q(1)} if n<2 else {(0,()):Q(-1),(1,()):Q(-1)}
def mul(p,q):
    out={}
    for (a,ka),x in p.items():
        for (b,kb),y in q.items():
            k=dict(ka)
            for v,n in kb:k[v]=k.get(v,0)+n
            k=tuple(sorted((v,n) for v,n in k.items() if n))
            for (c,_),z in phase(a+b).items():out[(c,k)]=out.get((c,k),Q(0))+x*y*z
    return clean(out)
def prod(ps):
    o=cn(1)
    for p in ps:o=mul(o,p)
    return o
def pw(p,n):return prod([p]*n)
REAL={'a','eta','V','Q','J','R2','E','g','tail','M2','b','c','F'}
def barname(v):return v if v in REAL else v[4:] if v.startswith('bar_') else 'bar_'+v
def cj(p):
    out={}
    for (a,k),x in p.items():out=add(out,sc(mul(phase(-a),{(0,tuple(sorted((barname(v),n) for v,n in k))):Q(1)}),x))
    return out
def re(p):return sc(add(p,cj(p)),Q(1,2))
def sub(p,mapping):
    out={}
    for (a,k),x in p.items():
        t=sc(phase(a),x)
        for v,n in k:
            if v in mapping:
                need(n>=0,'negative substitution power')
                t=mul(t,pw(mapping[v],n))
            else:t=mul(t,tok(v,n))
        out=add(out,t)
    return out
def pack(p):return [[a,[[v,n] for v,n in k],str(x)] for (a,k),x in sorted(p.items())]
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def identities():
    rows={};damages=[]
    def equal(name,lhs,rhs):
        need(lhs==rhs,name);rows[name]=pack(lhs)
    def reject(name,lhs,rhs):
        need(lhs!=rhs,'unrejected '+name);damages.append(name)
    u,m,T=map(tok,['u','m','T']);ub,mb,Tb=map(cj,[u,m,T]);a,eta=tok('a'),tok('eta')
    d={j:tok('d'+str(j)) for j in range(1,8)}
    # Delta from full centered anchored polynomial; no omission before reduction.
    delta={}
    for j in d:delta=add(delta,sc(prod([d[j],tok('u',j-8),add(phase(j-8),sc(phase(-8),-1))]),Q(-1,9)))
    evalp=add(*[prod([d[j],pw(u,j),add(phase(j),cn(-1))]) for j in d])
    equal('complete-linear-displacement',prod([delta,sc(pw(u,8),9),phase(8)]),sc(evalp,-1))
    for j in [3,6]:
        equal('cube-cancellation-'+str(j),sub(evalp,{('d'+str(k)):cn(k==j) for k in d}),{})
    lead=re(prod([ub,phase(-1),delta]))
    def flip(p):
        out={}
        for (ph,k),x in p.items():out=add(out,sc(mul(phase(-ph),{(0,k):Q(1)}),x))
        return out
    avg=sc(add(lead,flip(lead)),Q(1,2))
    expected=add(*[sc(re(prod([d[j],tok('u',j-8),ub])),Q(1,6)) for j in [1,2,4,5,7]])
    equal('whole-paired-linear-normal',avg,expected)
    top=sub(lead,{('d'+str(j)):sc(T,Q(-9,14)) if j==7 else {} for j in d}|{('bar_d'+str(j)):sc(Tb,Q(-9,14)) if j==7 else {} for j in d})
    signed=prod([T,ub,tok('u',-1)])
    equal('whole-individual-top-normal',top,sc(re(mul(signed,add(phase(1),cn(-1)))),Q(1,14)))
    equal('paired-top-normal',sc(add(top,flip(top)),Q(1,2)),sc(re(signed),Q(-3,28)))
    reject('lost-individual-phase',top,sc(re(signed),Q(-3,28)))
    reject('lost-conjugation',top,sc(re(mul(prod([T,u,tok('u',-1)]),add(phase(1),cn(-1)))),Q(1,14)))
    reject('wrong-top-sign',top,sc(top,-1))
    # Complete actual base half normals after u=a-m, with no conjugation assumption.
    Z=add(m,mul(u,phase(1)))
    base=sc(add(mul(Z,cj(Z)),cn(-1)),Q(1,2))
    anchored=sub(base,{'u':add(a,sc(m,-1)),'bar_u':add(a,sc(mb,-1))})
    averaged=sc(add(anchored,flip(anchored)),Q(1,2))
    M=re(m);M2=mul(m,mb)
    expectedbase=add(sc(add(pw(a,2),cn(-1)),Q(1,2)),sc(mul(a,M),Q(-3,2)),sc(M2,Q(3,2)))
    equal('actual-base-pair',averaged,expectedbase)
    difference=sc(add(anchored,sc(flip(anchored),-1)),Q(1,2))
    equaldifference=sc(prod([a,add(mb,sc(m,-1)),add(phase(1),phase(1),cn(1))]),Q(1,4))
    equal('actual-unaveraged-complex-mean',difference,equaldifference)
    reject('assume-real-mean',anchored,averaged)
    r2=mul(add(a,sc(m,-1)),add(a,sc(mb,-1)))
    equal('base-through-radius',expectedbase,sc(add(sc(r2,3),sc(pw(a,2),-1),cn(-2),sc(M2,3)),Q(1,4)))
    # Full critical product/elementary, variance, and translation at formal tokens.
    z=[tok('z'+str(k)) for k in range(8)]; U=add(*z);mean=sc(U,Q(1,8))
    coeff=[cn(1)]
    for t in z:
        n=[{} for _ in range(len(coeff)+1)]
        for j,c in enumerate(coeff):n[j]=add(n[j],sc(mul(c,t),-1));n[j+1]=add(n[j+1],c)
        coeff=n
    pcoeff=[{}]+[sc(coeff[j-1],Q(9,j)) for j in range(1,10)]
    H=add(*[mul(t,cj(t)) for t in z]);nu=[add(t,sc(mean,-1)) for t in z]
    variance=add(*[mul(t,cj(t)) for t in nu]);centT=add(*[pw(t,2) for t in nu])
    equal('whole-energy-decomposition',H,add(variance,sc(mul(mean,cj(mean)),8)))
    equal('whole-centered-trace',centT,add(*[pw(t,2) for t in z],sc(pw(U,2),Q(-1,8))))
    equal('whole-original-c8',pcoeff[8],sc(mean,-9))
    c7=sc(add(sc(pw(mean,2),56),sc(centT,-1)),Q(9,14))
    equal('whole-original-c7',pcoeff[7],c7)
    reject('wrong-c7-centered-trace',pcoeff[7],sc(add(sc(pw(mean,2),56),centT),Q(9,14)))
    rows['complete-critical-polynomial']=[pack(q) for q in coeff]
    # Degree-two Legendre coefficient by direct binomial expansion.
    x,y,R=tok('x'),tok('bar_x'),tok('R2')
    direct=add(sc(mul(x,y),Q(1,4)),sc(add(pw(x,2),pw(y,2)),Q(3,8)))
    expectedsecond=sc(add(mul(x,y),sc(re(pw(x,2)),3)),Q(1,4))
    equal('complete-Legendre-degree2',direct,expectedsecond)
    reject('missing-isotropic-variance',direct,sc(re(pw(x,2)),Q(3,4)))
    # Inequality bookkeeping: these full formal identities precede monotone bounds.
    V,Qv,gs,E,tail,M2s=map(tok,['V','Q','g','E','tail','M2'])
    baseline=add(sc(eta,Q(8,3)),sc(pw(eta,2),Q(-4,3)))
    radius_upper=add(cn(1),sc(eta,Q(-2,3)),sc(pw(eta,2),Q(1,3)),sc(M2s,-1),sc(Qv,Q(1,7)),sc(E,Q(4,3)))
    convex=add(sc(add(radius_upper,cn(-1)),-4),sc(mul(add(V,sc(Qv,3)),gs),Q(1,4)),sc(tail,-1))
    cleanrow=add(baseline,sc(M2s,4),sc(E,Q(-16,3)),sc(mul(V,gs),Q(1,4)),mul(Qv,add(sc(gs,Q(3,4)),cn(Q(-4,7)))),sc(tail,-1))
    equal('whole-variance-combination',convex,cleanrow)
    equal('Q-lower-elimination',sub(cleanrow,{'Q':sc(V,-1)}),add(baseline,sc(M2s,4),sc(E,Q(-16,3)),mul(V,add(cn(Q(4,7)),sc(gs,Q(-1,2)))),sc(tail,-1)))
    reject('Q-direction-reversal',sub(cleanrow,{'Q':sc(V,-1)}),sub(cleanrow,{'Q':V}))
    q=tok('Q'); equal('complete-ellipse-square',add(pw(add(cn(12),sc(q,-5)),2),sc(pw(q,2),-49)),add(cn(294),sc(pw(add(q,cn(Q(5,2))),2),-24)))
    # Whole convexity at a^2, then individual-normal slack substitution.
    # Input r^2-a^2 = -2aM+|m|^2. Treat a positive formal Laurent token.
    av=tok('a');inv_a=tok('a',-1);a3=pw(av,3)
    Ms=tok('M');D2=tok('M2');Fv=tok('F')
    objective_lower=add(sc(tok('a',-1),8),sc(mul(Ms,tok('a',-2)),8),sc(mul(D2,tok('a',-3)),-4),sc(prod([add(V,sc(q,3)),tok('a',-3)]),Q(1,4)),sc(tail,-1))
    solved_M=sc(prod([pw(av,2),add(Fv,sc(tok('a',-1),-8),sc(mul(D2,tok('a',-3)),4),sc(prod([add(V,sc(q,3)),tok('a',-3)]),Q(-1,4)),tail)]),Q(1,8))
    equal('whole-mean-convexity-solution',sub(objective_lower,{'M':solved_M}),Fv)
    slack=add(eta,sc(pw(eta,2),Q(-1,2)),sc(mul(av,Ms),Q(3,2)),sc(D2,Q(-3,2)),sc(q,Q(3,28)),E)
    substituted=sub(sub(slack,{'M':solved_M}),{'F':add(cn(8),sc(eta,3))})
    # Expand a=1-eta after eliminating negative a powers by cancellations.
    simplified=sub(substituted,{'a':add(cn(1),sc(eta,-1))})
    residual=add(sc(eta,Q(1,16)),sc(pw(eta,2),Q(13,16)),sc(pw(eta,3),Q(3,16)),sc(pw(eta,4),Q(-9,16)),sc(D2,Q(-3,4)),sc(V,Q(-3,64)),sc(q,Q(-15,448)),sc(mul(a3,tail),Q(3,16)),E)
    residual=sub(residual,{'a':add(cn(1),sc(eta,-1))})
    equal('whole-individual-slack-substitution',simplified,residual)
    reject('underestimated-slack-eta2',simplified,add(residual,sc(pw(eta,2),-1)))
    reject('missing-slack-complex-trace',simplified,add(residual,sc(q,Q(15,448))))
    return {'identities':rows,'mathematical_damages_rejected':damages}

def budgets():
    e=Q(1,65536);rho=Q(1,64);v=Q(1,512);am=1-e;lo=am-rho;hi=1+rho;s=hi+v/2;r0=Q(6399,6400)
    A={j:Q(9*comb(8,9-j),8*j)*rho**(7-j) for j in range(1,7)}|{7:Q(9,14)}
    Cd=sum(j*A[j]*s**(j-1) for j in A);Bd=9*lo**8-18*s**7*v-Cd*v
    Nc=Q(7,4)*sum(A[j]*hi**j for j in [1,2,4,5,7]);B=(s**7/9+Cd/54)/lo**8
    Bs={5:Q(63,32),4:Q(63,32)*rho,2:Q(9,128)*rho*v,1:Q(9,4096)*v**2}
    margins={}
    def pos(name,x):need(x>0,name);margins[name]=str(x)
    pos('nonzero-u',lo);pos('all-criticals-below-anchor',am**2-v)
    pos('centered-radius17/384',Q(17,384)**2-v)
    pos('Rouche-whole',9*lo**8/2-9*s**7*v-sum(A[j]*(s**j+hi**j) for j in A))
    pos('Rouche-disjoint',4*lo/9-v)
    pos('motion-positive-divisor',Bd)
    pos('motion-linear-norm-V/6',Bd-6*Nc)
    pos('motion-leading-norm-V/6',9*lo**8-6*Nc)
    pos('sqrt3-upper',Q(7,4)**2-3)
    pos('individual-phase-1/5',Q(1,5)**2-Q(3,81))
    for coef,name in [(Q(1,6),'paired'),(Q(1,5),'individual')]:pos(name+'-whole-halfnormal-error',1-(1+2*rho)*B-Q(1,72)-coef*sum(Bs[j]*lo**(j-7) for j in Bs))
    t=Q(17,384)
    pos('initial-reciprocal-3/5',Q(3,5)-(Q(1,2)+t/(lo-t))/lo**3)
    pos('objective-radius6399/6400',Q(1,6400)-(3*e+Q(3,5)*v)/8)
    pos('Q-coefficient-positive',Q(3,4)/hi**3-Q(4,7))
    profiles=[]
    for name,b,c,t,k in [('initial',rho,v,Q(17,384),700),('second',Q(1,800),v,Q(17,384),26),('third',Q(1,800),26*e,Q(1,50),8),('fourth',Q(1,800),8*e,Q(1,90),6)]:
        lam=Q(4,7)-1/(2*r0**3)-t/((r0-t)*r0**3)-Q(16,3)*(b/6+c)
        pos(name+'-variance-divisor',lam);pos(name+'-variance-conclusion',k*lam-Q(1,3)-4*e/3)
        profiles.append({'stage':name,'b':str(b),'c':str(c),'tau':str(t),'k':k,'lambda':str(lam)})
    pos('mean-square-eta/11',Q(1,11)-Q(1,12)-e/3)
    pos('mean1/800',Q(1,800)**2-e/11)
    for name,k,t in [('third',26,Q(1,50)),('fourth',8,Q(1,90)),('final',6,Q(1,96))]:pos(name+'-centered-radius',t*t-k*e)
    pos('strict-F13/5',Q(8,3)-4*e/3-Q(13,5))
    pos('negative-real-mean',am**2/10-1/(22*am))
    ep=Q(1,800)+36*e;tf=Q(1,96)/((am-Q(1,96))*am**3)
    pos('radius-upper',2-Q(6,7)-4*ep/3)
    pos('radius-derivative4',4-3/am**4)
    pos('ellipse12',12-Q(28,3)-Q(112,3)*e-28*(24*e+6*tf)-Q(448,3)*ep)
    pos('J-five-halves',Q(25,4)-6)
    pos('whole-slack1/12',Q(1,12)-Q(1,16)-Q(171,16)*e-Q(9,8)*tf-ep)
    pos('whole-slack-polynomial-majorant',2-Q(3,16)*e)
    pos('real-mean4/5',Q(4,5)-(Q(2,3)+Q(1,14)+2*ep/3)/am)
    pos('imag-mean1/3',Q(1,3)-(Q(5,28)+Q(7,72))/am)
    pos('two-over-sqrt3',Q(7,6)**2-Q(4,3))
    need(Q(16,25)+Q(1,9)==Q(169,225),'mean-norm13/15')
    pos('original-c7-four',4-Q(9,14)*(6+56*Q(169,225)*e))
    pos('original-H-seven',7-6-8*Q(169,225)*e)
    # Whole lower-six coefficient checks, squared to avoid irrational roots.
    lower_squared=[]
    for j in range(1,7):
        value=(Q(9,j)*comb(8,9-j))**2*Q(7,8)**(9-j)*e**(7-j)
        pos('original-c'+str(j)+'-eight-squared',64-value);lower_squared.append(str(value))
    # Independent proved refinement; only after complete original contraction.
    pos('improved-real3/4',Q(3,4)-(Q(2,3)+Q(1,14)+2*ep/3)/am)
    pos('improved-imag5/18',Q(5,18)-(Q(5,28)+Q(7,72))/am)
    pos('improved-mean4/5-squared',Q(16,25)-Q(9,16)-Q(25,324))
    lam=Q(4,7)-1/(2*am**3)-Q(1,96)/((am-Q(1,96))*am**3)-Q(16,3)*(Q(4,5)*e/6+6*e)
    pos('improved-V28/5',Q(28,5)*lam-Q(1,3)-4*e/3)
    pos('improved-H45/8',Q(45,8)-Q(28,5)-Q(128,25)*e)
    pos('improved-c7-29/8',Q(29,8)-Q(9,14)*(Q(28,5)+Q(896,25)*e))
    pos('improved-sqrtH8',Q(27,32)**2-Q(45,64))
    lower=[Q(9,j)*comb(8,9-j)*Q(27,32)**(9-j)*Q(1,256)**(7-j) for j in range(1,7)]
    pos('improved-lower-six-1/5',Q(1,5)-sum(lower))
    return {'constants':{k:str(val) for k,val in {'e':e,'mean_rho':rho,'absolute_H':v,'rminus':lo,'rplus':hi,'s':s,'Cd':Cd,'Bd':Bd,'Nc':Nc,'B':B,'epsilon':ep,'final_tail':tf,'improved_lambda':lam}.items()},'A':[[j,str(A[j])] for j in sorted(A)],'B_lower':[[j,str(Bs[j])] for j in sorted(Bs)],'profiles':profiles,'strict_margins':margins,'original_lower_squared':lower_squared,'improved_lower_six':[str(x) for x in lower],'improved_lower_sum':str(sum(lower))}

# Gaussian rationals provide an independent definition-level literal bridge.
def ga(x,y=0):return Q(x),Q(y)
def gadd(x,y):return x[0]+y[0],x[1]+y[1]
def gmul(x,y):return x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def gsc(x,q):return x[0]*q,x[1]*q
def gcj(x):return x[0],-x[1]
def gn(x):return x[0]**2+x[1]**2
def gp(x,n):
    out=ga(1)
    for _ in range(n):out=gmul(out,x)
    return out
def gsum(xs):
    out=ga(0)
    for x in xs:out=gadd(out,x)
    return out
def gpoly(roots):
    p=[ga(1)]
    for x in roots:
        n=[ga(0) for _ in range(len(p)+1)]
        for j,c in enumerate(p):n[j]=gadd(n[j],gsc(gmul(c,x),-1));n[j+1]=gadd(n[j+1],c)
        p=n
    return p
def ge(p,x):return gsum(gmul(c,gp(x,j)) for j,c in enumerate(p))
def literal_controls():
    fixtures=[[ga(0)]*8,[ga(Q(1,1000),Q(1,2000))]*8,[ga(Q(1,32))]+[ga(0)]*7,
              [ga(Q(k-3,2000),Q((-1)**k,3000)) for k in range(8)],
              [ga(Q(1,2000),Q(1,2000)),ga(Q(-1,2000),Q(-1,2000))]*4,
              [ga(Q(-1,32))]+[ga(0)]*7]
    out=[]
    for rs in fixtures:
        a=ga(Q(65535,65536));m=gsc(gsum(rs),Q(1,8));u=gadd(a,gsc(m,-1));nus=[gadd(z,gsc(m,-1)) for z in rs]
        H=sum(gn(z) for z in rs);V=sum(gn(z) for z in nus);T=gsum(gp(z,2) for z in nus)
        need(H==V+8*gn(m),'literal full energy')
        q=gpoly(rs);p=[ga(0)]+[gsc(q[j-1],Q(9,j)) for j in range(1,10)];p[0]=gsc(ge(p,a),-1)
        n=gpoly(nus);c=[ga(0)]+[gsc(n[j-1],Q(9,j)) for j in range(1,10)];c[0]=gsc(ge(c,u),-1)
        # Full binomial translation c(z-m), every original coefficient.
        shift=[ga(0) for _ in range(10)]
        for j,v in enumerate(c):
            for k in range(j+1):shift[k]=gadd(shift[k],gsc(gmul(v,gp(gsc(m,-1),j-k)),comb(j,k)))
        need(p==shift,'literal whole translated polynomial')
        need(c[8]==ga(0) and c[7]==gsc(T,Q(-9,14)),'literal centered Newton')
        need(ge(p,a)==ga(0),'literal actual anchor')
        need(all(ge(q,z)==ga(0) for z in rs),'literal all counted criticals')
        out.append({'criticals':[[str(v) for v in z] for z in rs],'original_coefficients':[[str(v) for v in z] for z in p],'centered_coefficients':[[str(v) for v in z] for z in c],'H':str(H),'V':str(V),'disk_feasibility_asserted':False})
    need(any(gn(z)>Q(1,4096) for z in fixtures[2]),'radius-inclusion is proper for critical data')
    # Dropping only actual disk-rootedness destroys the low-sublevel result.
    eta=Q(1,65536);a=1-eta;c8=Q(9,256)
    p=[ga(-a**9-c8*a**8)]+[ga(0)]*7+[ga(c8),ga(1)]
    Fval=7/a+1/(a+Q(1,32));w=ga(-1)
    val=ge(p,w);deriv=ge([gsc(p[j],j) for j in range(1,10)],w)
    physical=2*gmul(gmul(w,deriv),gcj(val))[0]-9*gn(val)
    need(Q(1,1024)<=Q(1,512) and Fval<8+3*eta and c8>Q(39,5)*eta and physical<0,'nondisk necessity control')
    return {'translation_controls':out,'nondisk_control':{'eta':str(eta),'H':'1/1024','F':str(Fval),'c8':str(c8),'disk_weight_at_minus_one':str(physical),'removes_only_disk_hypothesis':True}}

def build():return {'schema':1,'agent':'six-reviewer-1','method':'fresh Laurent/cube-phase full identities and Gaussian-rational translation plus whole exact scalar budgets','symbolic':identities(),'budgets':budgets(),'literal_controls':literal_controls()}
def typed(x,y):
    need(type(x) is type(y),'fixture type')
    if isinstance(x,dict):
        need(x.keys()==y.keys(),'fixture key set')
        for k in x:typed(x[k],y[k])
    elif isinstance(x,list):
        need(len(x)==len(y),'fixture length')
        for a,b in zip(x,y):typed(a,b)
    else:need(x==y,'fixture value')
def main():
    result=build();path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('EXPECTED.json')
    if '--write' in sys.argv:path=Path(__file__).with_name('EXPECTED.json');path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        def pairs(items):
            d={}
            for k,v in items:
                need(k not in d,'duplicate fixture key');d[k]=v
            return d
        def nonfinite(value):raise ValueError('nonfinite fixture token')
        typed(result,json.loads(path.read_text(),object_pairs_hook=pairs,parse_constant=nonfinite))
    print(json.dumps({'status':'PASS','whole_identities':len(result['symbolic']['identities']),'strict_margins':len(result['budgets']['strict_margins']),'literal_controls':len(result['literal_controls']['translation_controls']),'record_sha256':digest(result)},sort_keys=True))
if __name__=='__main__':main()
