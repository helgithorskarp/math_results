"""Independent written-input audit of LEMMA10170. Standard library only.

No target executable, expected record or validation program is imported.
Closed boxes are bisected before leaf-only necessary intersections.
Polar integrals use both full monomials and t^i(1-t)^j beta moments.
Centered powers use both repeated multiplication and multinomial counting.
"""
from fractions import Fraction as Q
from math import comb, factorial, isqrt
from pathlib import Path
import json, hashlib, sys, resource, time

HERE = Path(__file__).resolve().parent
ZERO, ONE = Q(0), Q(1)

def require(ok, message):
    if not ok:
        raise ValueError(message)

def mul(a, b):
    c = [ZERO] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return c

def power(a, n):
    c = [ONE]
    for _ in range(n):
        c = mul(c, a)
    return c

def plus(a, b):
    c = [ZERO] * max(len(a), len(b))
    for i, x in enumerate(a): c[i] += x
    for i, x in enumerate(b): c[i] += x
    return c

def integral(a, shift=0):
    return sum((x/Q(i+shift+1) for i, x in enumerate(a)), ZERO)

def beta(i, j):
    return Q(factorial(i)*factorial(j), factorial(i+j+1))

def root_round(x, denominator, upper):
    require(x >= 0 and type(denominator) is int and denominator > 0,
            'square-root domain')
    k = isqrt((x.numerator*denominator**2)//x.denominator)
    require(Q(k,denominator)**2 <= x < Q(k+1,denominator)**2,
            'sqrt floor square enclosure')
    if upper and Q(k,denominator)**2 < x: k += 1
    result = Q(k,denominator)
    require((result**2 >= x and (k == 0 or Q(k-1,denominator)**2 < x))
            if upper else result**2 <= x < Q(k+1,denominator)**2,
            'sqrt chosen direction')
    return result

def multinomial_quadratic(a, n):
    """All n-fold choices of degrees 0,1,2, including signs and zero terms."""
    c = [ZERO]*(2*n+1)
    for j in range(n+1):
        for k in range(n-j+1):
            i = n-j-k
            c[j+2*k] += Q(factorial(n),factorial(i)*factorial(j)*factorial(k))*a[0]**i*a[1]**j*a[2]**k
    return c

def constants():
    rho, tau = Q(479,512), Q(363,1024)
    require(rho**2 >= Q(7,8) and tau**2 >= Q(1,8), 'classical sqrt constants')
    eta = {k:Q(7,8)**((k-2)//2)*rho**(k%2) for k in range(2,9)}
    c=[ONE,ZERO]; pairs=[]
    for l in range(2,9):
        newton=sum((c[l-k]*eta[k] for k in range(2,l+1)),ZERO)/l
        maclaurin=Q(comb(8,l))*Q(8)**(-(l//2))*tau**(l%2)
        c.append(min(newton,maclaurin)); pairs.append([newton,maclaurin,c[-1]])
    require(c[2:]==[Q(1,2),Q(479,1536),Q(11,32),Q(2541,8192),Q(7,128),Q(363,65536),Q(1,4096)], 'all seven recurrence minima')
    return c,pairs

def polar(A, H, L, U, F, P):
    require(Q(3,5)<=A<=H<=Q(5,8) and 0<=L<=U and F<=8 and P>=0, 'polar domain')
    bm,bp=1-H*H,1-A*A
    astar=min(A*bp,H*bm); chord=A+1-A*A-H
    delta=root_round(L/56,1024,False)
    caps=[root_round(7*U/8,256,True),F-7/(1+H)-1]
    D=min(caps)
    require(D>=0 and chord-bm*delta>0, 'polar cap and positive radial sign')
    left,right=chord+7*bm*delta,chord-bm*delta
    radial=mul([H,left],power([H,right],7))
    rb=[Q(comb(7,k))*H**(8-k)*right**k+
        (Q(comb(7,k-1))*H**(8-k)*left*right**(k-1) if k else 0)
        for k in range(9)]
    require(radial==rb,'entire radial vector')
    MC=H+bp*(1+D); MB=H+chord
    nu=bp*(1+D)/MC; alpha=chord/MB
    require(MC>0 and MB>0 and 0<=nu<1 and 0<=alpha<1,'reciprocal series signs')
    losses=[astar*P/MC**2*(n+1)*nu**n+Q(3,4)*bm*(8-F)/MB*alpha**n for n in range(5)]
    require(all(x>=0 for x in losses),'nonnegative exponential loss')
    kernel=[ZERO]*6
    for n,x in enumerate(losses):
        for j in range(n+1): kernel[j+1]+=x*comb(n,j)*(-1)**j
    quadratic=plus(plus([ONE],[-x for x in kernel]),[x/2 for x in mul(kernel,kernel)])
    full=mul(radial,quadratic)
    require(len(full)==19,'full degree eighteen vector')
    # Independent beta-moment route, including every ordered kernel pair.
    value=integral(radial)
    for i,r in enumerate(rb):
        for n,x in enumerate(losses): value-=r*x*beta(i+1,n)
        for n,x in enumerate(losses):
            for m,y in enumerate(losses): value+=r*x*y*beta(i+2,n+m)/2
    require(integral(full)==value,'entire polar integral')
    # Also reconstruct every coefficient through binomial kernel choices.
    second=rb+[ZERO]*10
    for i,r in enumerate(rb):
        for n,x in enumerate(losses):
            for j in range(n+1): second[i+j+1]-=r*x*comb(n,j)*(-1)**j
        for n,x in enumerate(losses):
            for m,y in enumerate(losses):
                for j in range(n+m+1): second[i+j+2]+=r*x*y*comb(n+m,j)*(-1)**j/2
    require(second==full,'all nineteen polar coefficients')
    return dict(value=value,vector=full,radial=radial,losses=losses,delta=delta,D=D,caps=caps)

def intersect(box):
    b=list(box); history=[]
    for iteration in range(4):
        a,h,el,eh,fl,fh,ul,uh,wl,wh=b
        uh=min(uh,fh/8);ul=max(ul,fl/8-eh/16)
        fl=max(fl,8*ul);fh=min(fh,8*uh+eh/2)
        el=max(el,2*max(ZERO,fl-8*uh),8*((1-uh)**2+wl))
        wh=min(wh,(fh/8)**2-ul**2,eh/8-(1-uh)**2)
        b=[a,h,el,eh,fl,fh,ul,uh,wl,wh]
        history.append(b[:])
        bad=[i for i in range(5) if b[2*i]>b[2*i+1]]
        if bad: return b,history,bad
    return b,history,[]

def origin(box, tlo, thi, c):
    a,h,el,eh,fl,fh,ul,uh,wl,wh=box
    s=min(ONE,uh*uh+wh,(fh/8)**2)
    S=min(eh-8*((1-uh)**2+wl),thi+2*fh-8-8*(ul*ul+wl))
    require(S>=0 and s>=ul**2 and ul>a*s,'centered necessary signs')
    bt=[ONE,-2*a*ul,a*a*s];b1=sum(bt)
    require(0<b1<1 and 1-a*ul>0,'beta positivity and endpoint')
    qt=[ONE,-a*ul,a*a*(s-ul*ul)/(2*(1-a*ul))]
    ds=root_round(s,1024,True);db=root_round(b1,1024,True);dS=root_round(S,1024,True)
    numerator=1-db*b1**4
    require(numerator>0 and h*ds>0,'diagonal signs')
    diagonal=numerator/(h*ds);R=ZERO;terms=[]
    for j in range(2,9):
        n=(8-j)//2;v=power(bt,n);ind=multinomial_quadratic(bt,n)
        require(v==ind,'entire centered beta power')
        if j%2: v=mul(v,qt);ind=mul(ind,qt)
        require(v==ind and len(v)==9-j+(j%2),'entire centered order '+str(j))
        weight=9*h**j*c[j]*S**(j//2)*dS**(j%2)
        exact=integral(v,j)
        # Integral directly from independent multinomial factors before convolution.
        other=ZERO
        for k in range(n+1):
            for l in range(n-k+1):
                z=n-k-l
                x=Q(factorial(n),factorial(z)*factorial(k)*factorial(l))*bt[0]**z*bt[1]**k*bt[2]**l
                if j%2:
                    other+=sum((x*q/Q(j+k+2*l+i+1) for i,q in enumerate(qt)),ZERO)
                else: other+=x/Q(j+k+2*l+1)
        require(exact==other and exact>=0,'full centered term integral')
        terms.append(dict(order=j,vector=v,integral=exact,weight=weight,contribution=weight*exact));R+=weight*exact
    return dict(value=diagonal-R,diagonal=diagonal,remainder=R,s=s,S=S,beta=bt,Q=qt,roundings=[ds,db,dS],terms=terms)

def audit(data):
    require(set(data)=={'root','leaves','splits'},'cover fields')
    require(type(data['root']) is list and all(type(x) is str for x in data['root']),'root types')
    root=list(map(Q,data['root']))
    require(root==[Q(3,5),Q(5,8),ZERO,Q(23,5),Q(184,25),Q(8),Q(253,400),ONE,ZERO,Q(23,40)],'entire closed root')
    splits,leaves=data['splits'],data['leaves']
    require(type(splits) is dict and type(leaves) is dict and len(splits)==491 and len(leaves)==492,'input census')
    require(not set(splits)&set(leaves),'disjoint leaves and splits')
    for p,axis in splits.items():
        require(type(p) is str and set(p)<={'0','1'} and type(axis) is int and 0<=axis<5,'split path and axis types')
    for p,s in leaves.items():
        require(type(p) is str and set(p)<={'0','1'} and type(s) is str and s in ('origin-passes','polar-excluded','empty-necessary-inequalities'),'leaf path and status types')
    c,recurrence=constants()
    low=integral(power([Q(5,8),Q(5,8)*Q(23,25)],8))
    require(low==Q(58643076666481,58982400000000) and low<1,'full low first-power integral')
    energy=[]
    for k in range(67):
        lo=Q(k,8);hi=min(Q(k+1,8),Q(1400,169))
        require(lo<hi and (k==0 or lo==energy[-1]['U']),'consecutive closed energy cells')
        p=max(ZERO,(Q(23,5)-hi)/2);v=polar(Q(3,5),Q(5,8),lo,hi,Q(8),p)
        require(v['value']<Q(9999,10000),'energy strict polar inequality '+str(k))
        energy.append(dict(L=lo,U=hi,P=p,**v))
    require(energy[0]['L']==0 and energy[-1]['U']==Q(1400,169),'entire energy coverage')
    seen=set();out=[]
    def visit(path,box):
        require(len(path)<=18 and path not in seen,'tree depth and unique visit');seen.add(path)
        if path in splits:
            axis=splits[path];i=2*axis;mid=(box[i]+box[i+1])/2
            lower=box[:];upper=box[:];lower[i+1]=mid;upper[i]=mid
            require(lower[i]==box[i] and upper[i+1]==box[i+1] and lower[i+1]==upper[i],'both closed children cover parent')
            visit(path+'0',lower);visit(path+'1',upper);return
        require(path in leaves,'both children reachable')
        status=leaves[path];b,hist,bad=intersect(box)
        item=dict(path=path,raw=box,intersections=hist,status=status,box=b)
        if bad:
            require(status=='empty-necessary-inequalities','declared status matches strict empty');item['empty_axes']=bad
        else:
            require(status!='empty-necessary-inequalities','nonempty is not declared empty')
            a,h,el,eh,fl,fh,ul,uh,wl,wh=b;m=1/(1+h)
            require(fl>=Q(184,25)>7*m+1,'radial cap monotonicity domain')
            tl=max(ZERO,el-2*fh+16*ul,(8-fh)**2/8)
            th=min(eh-2*max(ZERO,fl-8*uh),(fh-7*m-1)**2+7*(m-1)**2)
            require(tl<=th,'radial necessary interval is nonempty')
            item['T']=[tl,th];o=origin(b,tl,th,c);item['origin']=o
            if status=='origin-passes':
                require(o['value']>Q(2049,2048),'origin strict leaf '+path)
            else:
                p=max(ZERO,fl-8*uh);v=polar(a,h,tl,th,fh,p);item['polar']=v
                require(v['value']<Q(9999,10000),'polar strict leaf '+path)
        out.append(item)
    visit('',root)
    require(seen==set(splits)|set(leaves) and len(seen)==983,'every defining entry reached')
    census={s:sum(x['status']==s for x in out) for s in leaves.values()}
    require(census=={'origin-passes':230,'polar-excluded':246,'empty-necessary-inequalities':16},'entire status census')
    polar_count=len(energy)+sum('polar' in x for x in out)
    centered_count=sum(len(x['origin']['terms']) for x in out if 'origin' in x)
    require(polar_count==313 and centered_count==3332,'full vector census after entrywise checks')
    return dict(recurrence=recurrence,low_integral=low,energy=energy,leaves=out,census=census,nodes=len(seen),polar_vectors=polar_count,centered_vectors=centered_count)

def encode(x):
    if isinstance(x,Q):return str(x)
    raise TypeError(type(x).__name__)

if __name__=='__main__':
    started=time.monotonic();d=json.loads((HERE/'COVER-input.json').read_text());r=audit(d)
    raw=json.dumps(r,sort_keys=True,separators=(',',':'),default=encode).encode()
    (HERE/'computed-private.json').write_bytes(raw)
    print(json.dumps(dict(status='PASS',nodes=r['nodes'],census=r['census'],energy_cells=len(r['energy']),polar_vectors=r['polar_vectors'],centered_vectors=r['centered_vectors'],
       energy_max=str(max(x['value'] for x in r['energy'])),origin_min=str(min(x['origin']['value'] for x in r['leaves'] if x['status']=='origin-passes')),
       polar_max=str(max(x['polar']['value'] for x in r['leaves'] if x['status']=='polar-excluded')),record_sha256=hashlib.sha256(raw).hexdigest(),record_bytes=len(raw),
       elapsed_seconds=time.monotonic()-started,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),sort_keys=True))
