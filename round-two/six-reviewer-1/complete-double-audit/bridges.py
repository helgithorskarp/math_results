"""Exact original equations, Hermite minors, range gaps, and root controls."""
from fractions import Fraction as Q
from ring import constant,add,scale,mul,power,degree,original,listpoly

def det(M):
    states={0:constant(1)}
    for row in M:
        fresh={}
        for mask,c in states.items():
            for j,x in enumerate(row):
                if mask&(1<<j):continue
                key=mask|(1<<j);sign=(-1)**((mask>>(j+1)).bit_count())
                fresh[key]=add(fresh.get(key,{}),scale(mul(c,x),sign))
        states=fresh
    return states[(1<<len(M))-1]

def sturm(p):
    def trim(a):
        while a and not a[-1]:a.pop()
        return a
    def remainder(a,b):
        a=a[:]
        while a and len(a)>=len(b):
            n=len(a)-len(b);v=a[-1]/b[-1]
            for j,c in enumerate(b):a[n+j]-=v*c
            trim(a)
        return a
    p=trim(p[:]);seq=[p,[j*p[j]for j in range(1,len(p))]]
    while seq[-1]:
        r=[-c for c in remainder(seq[-2],seq[-1])]
        if not r:break
        seq.append(r)
    def variations(positive):
        signs=[(1 if a[-1]>0 else -1)*(-1 if not positive and (len(a)-1)%2 else 1)for a in seq]
        return sum(a!=b for a,b in zip(signs,signs[1:]))
    return variations(False)-variations(True),len(seq[-1])-1

def evaluate(p,point):return sum(Q(c)*point[0]**i*point[1]**j*point[2]**k for (i,j,k),c in p.items())

def identities():
    a={(1,0,0):1};A=power(a,2);D={(0,1,0):1};s=add(A,constant(Q(-1,8)))
    B=add(constant(Q(1,4)),scale(A,-1));e=add(scale(power(s,2),2),scale(D,Q(-1,4)))
    coeff=[constant(1),scale(a,Q(2,3)),scale(B,Q(-4,3)),scale(mul(a,B),Q(-2,3)),scale(add(power(B,2),e),Q(1,3))]
    p=[constant(4)]
    for k in range(1,7):
        v={}
        for j in range(1,min(k,4)+1):
            v=add(v,scale(coeff[j],-k)if j==k else scale(mul(coeff[j],p[k-j]),-1))
        p.append(v)
    minors=[det([[p[i+j]for j in range(n)]for i in range(n)])for n in range(1,5)]
    expected=[constant(4),scale(add(constant(9),scale(s,-56)),Q(1,6)),
      scale(add(add(add(add(scale(mul(D,s),-504),scale(D,81)),scale(power(s,3),3136)),scale(power(s,2),-392)),add(scale(s,-34),constant(2))),Q(1,162))]
    F={}
    for i,j,c in [(0,3,-6912),(2,2,173376),(1,2,-2736),(0,2,117),(4,1,-1455104),(3,1,30464),(2,1,3888),(1,1,-752),(0,1,32),(6,0,4214784),(5,0,-150528),(4,0,-20160),(3,0,4224),(2,0,-192)]:
        F=add(F,scale(mul(power(s,i),power(D,j)),c))
    expected.append(scale(F,Q(1,46656)))
    if minors!=expected:raise ValueError('every whole Hermite minor')
    H,r,f,Qp=original();moments=[constant(8)]
    for k in range(1,6):
        v=scale(f[8-k],Q(-k,64))
        for j in range(1,k):v=add(v,scale(mul(f[8-j],moments[k-j]),Q(-1,64)))
        moments.append(v)
    if moments[1:]!=[{},constant(1),{},add(constant(Q(1,8)),D),{}]:raise ValueError('complete moment identities')
    # Scalar gap identities checked as full multivariate polynomials.
    h={(1,0,0):1};x={(0,1,0):1};one=constant(1)
    if add(power(h,4),scale(mul(power(x,2),power(add(scale(h,2),scale(x,-1)),2)),-1))!=mul(power(add(h,scale(x,-1)),2),add(power(h,2),mul(x,add(scale(h,2),scale(x,-1))))):raise ValueError('positive-q0 gap identity')
    k=h;y=x
    if add(mul(power(k,2),power(add(constant(2),scale(k,-1)),2)),scale(mul(power(k,2),add(add(one,scale(k,-1)),y)),-4))!=mul(power(k,2),add(power(k,2),scale(y,-4))):raise ValueError('real-q0 first gap identity')
    if add(one,scale(mul(power(k,2),power(add(constant(2),scale(k,-1)),2)),-1))!=mul(power(add(k,constant(-1)),2),add(add(one,scale(k,2)),scale(power(k,2),-1))):raise ValueError('real-q0 second gap identity')
    # Written range exclusions are rational endpoints, not numerical samples.
    margins=[2*(Q(21,100)-Q(1,8))**2-Q(5,564)-Q(1,1875)-Q(4,1125),
      8*Q(3,40)**2-4*Q(17,200)**4/Q(104,1875)-Q(5,141),
      8*Q(17,250)**2-Q(960,17)*Q(17,250)**4-Q(5,141),
      8*Q(71,1000)**2-Q(33600,199)*Q(71,1000)**4-Q(5,141)]
    if margins!=[Q(2531,1692000),Q(54193817,9384960000),Q(2227829,6884765625),Q(10108107559,17536875000000)]:raise ValueError('all written rational range margins')
    def ell(A):return A+(Q(1,4)-A)/3+Q(18,175)
    small=[]
    for lo,hi in [(Q(1,25),Q(9,200)),(Q(9,200),Q(1,20))]:
        JL=ell(lo)**2-4*(Q(1,8)-lo)**2
        margin=(2*(Q(1,8)-hi)**2-Q(5,564))*JL-(Q(1,8)-lo)**4
        if JL<=0 or margin<=0:raise ValueError('negative height range inequality')
        small.append([str(JL),str(margin)])
    if small!=[['201/12250','45549377/3684800000000'],['4661/220500','29379437/3109050000000']]:raise ValueError('all small-A margins')
    if not(Q(1,72)**2<Q(1,625*8) and Q(1,123)**2<Q(1,625*24)and Q(1,26)**2>Q(5,141*24)and Q(7,4)**2>3):raise ValueError('full box coverage')
    # Derivatives of the two scalar lower bounds remain positive at the
    # largest h: after dividing by h the derivative is decreasing in h^2.
    if min(16-4*c*Q(3,40)**2 for c in [Q(960,17),Q(33600,199)])<=0:raise ValueError('range monotonicity')
    fixtures=[]
    for av,dv,uv in [(Q(2,5),Q(9799,10**6),Q(-1,2000000)),(Q(1,4),Q(781,25000),Q(-1,10**6)),(Q(1,3),Q(1,100),Q(-1,10**9))]:
        point=(av,dv,uv);qp=[evaluate(c,point)/64 for c in Qp];hp=[evaluate(c,point)/64 for c in H]
        fixtures.append({'a_D_u':[str(z)for z in point],'original_Q_real_and_gcd':list(sturm(qp)), 'active_H_real_and_gcd':list(sturm(hp)), 'Q_at_a':str(sum(c*av**i for i,c in enumerate(qp)))})
    if any(z['original_Q_real_and_gcd']!=[6,0]or z['active_H_real_and_gcd']!=[6,0]or Q(z['Q_at_a'])==0 for z in fixtures[:2]):raise ValueError('actual positive-q0 original controls')
    if fixtures[2]['original_Q_real_and_gcd']!=[4,0]or fixtures[2]['active_H_real_and_gcd']!=[6,0]:raise ValueError('critical-reality-only negative control')
    return {'all_Hermite_minors':[listpoly(p)for p in minors],'original_moments':[listpoly(p)for p in moments],
      'whole_gap_identities':True,'range_margins':[str(x)for x in margins],'small_A_margins':small,
      'range_monotonicity_and_box_coverage':True,'literal_root_controls':fixtures}
