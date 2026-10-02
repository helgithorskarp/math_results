"""Independent rational inverse/Newton checks, root tangents, and domain controls."""
from fractions import Fraction as F
from polys import need

def trim(p):
    p=list(map(F,p))
    while p and p[-1]==0:p.pop()
    return p
def at(p,k):return p[k] if k<len(p) else F(0)
def add(p,q):return trim([at(p,i)+at(q,i) for i in range(max(len(p),len(q)))])
def scale(p,c):return trim([x*c for x in p])
def mul(p,q):
    r=[F(0)]*max(0,len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):r[i+j]+=x*y
    return trim(r)
def derivative(p):return trim([i*p[i] for i in range(1,len(p))])
def division(p,q):
    p=trim(p);q=trim(q);need(q,'nonzero divisor');r=[F(0)]*max(0,len(p)-len(q)+1)
    while len(p)>=len(q):
        j=len(p)-len(q);v=p[-1]/q[-1];r[j]+=v
        for i,x in enumerate(q):p[j+i]-=v*x
        p=trim(p)
    return trim(r),p
def rem(p,h):return division(p,h)[1]
def inverse(p,h):
    r0,r1=h,p;s0,s1=[],[F(1)]
    while r1:
        q,r=division(r0,r1);r0,r1=r1,r;s0,s1=s1,add(s0,scale(mul(q,s1),-1))
    need(len(r0)==1,'squarefree inverse domain');v=rem(scale(s0,1/r0[0]),h)
    need(rem(mul(p,v),h)==[1],'whole inverse identity');return v
def evaluate(p,x):
    out=F(0)
    for y in reversed(p):out=out*x+y
    return out
def powers(h,count):
    n=len(h)-1;out=[F(n)]
    for k in range(1,count+1):
        out.append(-sum(at(h,n-j)*(k if j==k else out[k-j]) for j in range(1,min(k,n)+1)))
    return out
def trace(p,h):
    p=rem(p,h);t=powers(h,len(p)-1);return sum((c*t[i] for i,c in enumerate(p)),F(0))
def pair(p,h):return at(rem(p,h),len(h)-2)
def adjoint(p,h):
    n=len(h)-1;need(len(trim(p))<=n,'normal adjoint domain')
    G=[[pair([F(0)]*(i+j)+[F(1)],h) for j in range(n)] for i in range(n)]
    b=[F(0)]+[j*sum((G[j-1][i]*at(p,i) for i in range(n)),F(0)) for j in range(1,n)]
    x=[F(0)]*n
    for i in range(n):
        c=n-1-i;need(G[i][c]==1,'unit numeric Gram pivot')
        x[c]=b[i]-sum(G[i][j]*x[j] for j in range(c+1,n))
    return trim(x)
def kernel(f,h,p):
    Q,r=division(add(scale(f,8),mul(p,derivative(h))),h);need(not r,'actual mass quotient identity')
    k=add(scale(p,-16),scale(adjoint(adjoint(rem(mul(p,p),h),h),h),-F(1,4)))
    k=add(k,scale(adjoint(rem(mul(p,add(Q,scale(derivative(p),-1))),h),h),F(1,4)))
    return Q,k
def mass(f):
    h=scale(derivative(f),F(1,8));inv=inverse(derivative(h),h);p=rem(scale(mul(f,inv),-8),h)
    Q,K=kernel(f,h,p);return h,inv,p,Q,K
def moving(f,q,data):
    h,inv,p,Q,K=data;dh=scale(derivative(q),F(1,8));dhp=derivative(dh)
    dp=rem(mul(add(add(mul(Q,dh),scale(mul(p,dhp),-1)),scale(q,-8)),inv),h)
    pulled=rem(add(dp,scale(mul(mul(derivative(p),dh),inv),-1)),h)
    direct=2*trace(mul(p,pulled),h);residue=pair(mul(K,q),h)
    need(direct==residue,'full inverse/Newton motion versus independent Gram kernel')
    return direct,2*trace(mul(p,dp),h)
def roots_polynomial(u):
    f=[F(1)]
    for x in u:f=mul(f,[-F(x),F(1)])
    return f
def sturm(p):
    out=[trim(p),derivative(p)]
    while out[-1]:
        r=scale(division(out[-2],out[-1])[1],-1)
        if not r:break
        out.append(r)
    return out
def variation(signs):
    signs=[s for s in signs if s];return sum(x!=y for x,y in zip(signs,signs[1:]))
def roots_count(p,lo=None,hi=None):
    s=sturm(p)
    def signs(x,right):
        vals=[]
        for q in s:
            v=evaluate(q,x) if x is not None else q[-1]*((-1)**(len(q)-1) if not right else 1)
            vals.append((v>0)-(v<0))
        return vals
    return variation(signs(lo,False))-variation(signs(hi,True))
def serial(p):return [str(x) for x in p]
def domain(f,data):
    h,inv,p,Q,K=data;N=-2*at(f,6);D=F(3,8)*N*N-4*at(f,4);eta=trace(mul(p,p),h)
    C=(N*N-eta)/D;residual=add(K,[4*N,0,-4*C])
    ode=add(mul(p,derivative(derivative(h))),add(mul(add(derivative(p),scale(Q,-1)),derivative(h)),mul(add([F(64)],scale(derivative(Q),-1)),h)))
    return N,D,eta,C,residual,ode

def audit():
    results={};damage=[]
    seeds=[[-7,-4,-2,-1,0,2,5,7],[-10,-6,-3,-1,2,4,5,9],[-8,-5,-3,-2,1,4,6,7]]
    for number,u in enumerate(seeds):
        need(len(set(u))==8 and sum(u)==0,'eight distinct balanced seed')
        f=roots_polynomial(u);data=mass(f);N,D,eta,C,residual,ode=domain(f,data)
        need(N==sum(x*x for x in u) and D==sum(x**4 for x in u)-F(N*N,8),'original norm and fourth moment')
        need(not ode and trace(data[2],data[0])==N,'actual ODE and total mass')
        vals=[]
        for j in range(7):
            q=[F(0)]*j+[F(1)];v=[-evaluate(q,F(x))/evaluate(derivative(f),F(x)) for x in u]
            need(sum(v)==0 and 2*sum(x*y for x,y in zip(u,v))==-2*at(q,6),'whole original-root tangent constraints')
            dot=[]
            for i,x in enumerate(u):dot=add(dot,scale(roots_polynomial(u[:i]+u[i+1:]),-v[i]))
            need(dot==q,'whole original-root tangent polynomial')
            direct,frozen=moving(f,q,data)
            dotD=4*sum(x**3*y for x,y in zip(u,v))-N*sum(x*y for x,y in zip(u,v))/2
            need(dotD==F(3,4)*N*(-2*at(q,6))-4*at(q,4),'actual denominator derivative')
            vals.append({'q_degree':j,'dot_eta':str(direct),'coefficient_only_frozen_nodes':str(frozen),'dot_D':str(dotD),'root_velocities':serial(v)})
        R=add([F(0)]+derivative(f),scale(f,-8));dr,_=moving(f,R,data)
        need(dr==-4*eta,'full radial Euler identity')
        results['actual seed '+str(number)]={'u':u,'f':serial(f),'mass_polynomial':serial(data[2]),'N':str(N),'D':str(D),'eta':str(eta),'C':str(C),'all_seven_derivatives':vals,'kernel_residual':serial(residual),'radial_eta':str(dr)}
        if number==0:
            need(any(v['dot_eta']!=v['coefficient_only_frozen_nodes'] for v in vals),'frozen criticals damage rejects')
            damage.append('frozen critical roots omit an actual derivative term')
    hermite=[F(105),0,-420,0,210,0,-28,0,1];data=mass(hermite);N,D,eta,C,residual,ode=domain(hermite,data)
    need(roots_count(hermite)==8 and roots_count(data[0])==7,'full real Hermite domains')
    need(data[2]==[8] and C==8 and not ode and residual==[192,0,-32],'constant positive mass is NOT stationary')
    results['Hermite nonstationary']={'f':serial(hermite),'h':serial(data[0]),'p':serial(data[2]),'C':str(C),'kernel_residual':serial(residual)}
    damage.append('positive actual constant masses and ODE do not imply stationarity')
    # A different asymmetric primitive, centered by a full exact constant shift.
    f=list(map(F,hermite));f[5]=F(1,16);h,inv,p,Q,K=mass(f);kappa=rem(scale(inv,-8),h)
    need(at(kappa,6)!=0,'legal centering scalar pivot');delta=-at(p,6)/at(kappa,6);f[0]+=delta;f=trim(f);data=mass(f)
    need(roots_count(f)==8 and len(sturm(f)[-1])==1 and roots_count(data[0])==7,'actual simple-real centered asymmetric control')
    need(len(data[2])==6 and not domain(f,data)[5] and domain(f,data)[4],'degree-five centered actual profile is NOT stationary')
    results['asymmetric centered nonstationary']={'f':serial(f),'h':serial(data[0]),'p':serial(data[2]),'constant_shift':str(delta),'kernel_residual':serial(domain(f,data)[4]),'original_real_distinct_count':8}
    damage.append('degree-five centering alone is not full stationarity')
    f=add(hermite,[-1000000]);data=mass(f)
    need(roots_count(data[0],F(-5),F(5))==7 and roots_count(f)==2,'seven simple real criticals but only two real originals')
    bound=sum(abs(F(x))*F(5)**i for i,x in enumerate(hermite));need(bound<1000000,'all shifted critical values strictly negative')
    results['negative mass primitive']={'f':serial(f),'h':serial(data[0]),'formal_mass':serial(data[2]),'original_real_distinct_count':2,'critical_real_distinct_count':7,'critical_value_upper':str(bound-1000000)}
    damage.append('a real critical spectrum without positive masses does not reconstruct eight real originals')
    f=mul(mul(mul([-1,0,1],[-1,0,1]),[-4,0,1]),[-9,0,1]);data=mass(f)
    need(roots_count(f)==6 and roots_count(data[0])==7 and len(sturm(data[0])[-1])==1,'critical simplicity does not imply original simplicity')
    need(evaluate(data[2],F(1))==evaluate(data[2],F(-1))==0,'literal double-original zero masses')
    results['double originals']={'f':serial(f),'h':serial(data[0]),'p':serial(data[2]),'original_real_distinct_count':6,'critical_real_distinct_count':7,'zero_mass_original_nodes':[-1,1]}
    damage.append('simple critical spectrum cannot replace eight-distinct-original hypothesis')
    h=mass(hermite)[0];p=[F(1)];Q=[F(0),F(8)];f=scale(add(mul(Q,h),scale(mul(p,derivative(h)),-1)),F(1,8))
    defect=add(derivative(f),scale(h,-8));need(defect,'positive interpolant with real critical candidate fails full ODE')
    results['nonprimitive positive pair']={'h':serial(h),'p':serial(p),'Q':serial(Q),'f':serial(f),'whole_derivative_defect':serial(defect)}
    damage.append('positivity and real h without full ODE do not preserve actual critical polynomial')
    # Balance sharpens the quartic exception's sufficient contradiction.
    need(F(96,7)*F(3,4)-8==F(16,7) and F(16,7)<4,'quantitative exceptional quartic separation')
    results['balanced quartic separation']={'d_strict_upper':'3/4','C_strict_upper':'16/7','gap_below_four_strict':'12/7'}
    return {'results':results,'mathematical_domain_damage_rejections':damage,'actual_derivative_count':21}
