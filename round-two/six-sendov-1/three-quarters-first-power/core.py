"""Standalone CLOSED[29/40,3/4] exact core kernels.
Own ab3798362ba9a701f68923aad5af2ed7dc608863 method provenance only.
No ancestor numerical exclusions, discovery records or peer/reviewer runtime inputs.
Ordinary/unformalized and independently unreviewed; full argument in PROOF.md.
"""
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from math import comb,factorial,isqrt
from pathlib import Path
HERE=Path(__file__).resolve().parent
_spec=importlib.util.spec_from_file_location('private_three_quarters_local_origin',HERE/'origin.py')
origin=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(origin)
LOW=Q(29,40);H=Q(3,4);C=Q(719,1600)
BM=Q(7,16);BX=Q(759,1600);AB=Q(21,64);TM=Q(72,7)
ENERGY=Q(47,10);MASS=Q(149,20);GAMMA=Q(51,80)


def require(ok,message):
    if not ok: raise ValueError(message)

def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

def digest(x): return sha256(canonical(x)).hexdigest()

def add(a,b):
    out=[Q(0)]*max(len(a),len(b))
    for j,x in enumerate(a):out[j]+=x
    for j,x in enumerate(b):out[j]+=x
    return out

def scale(a,c):return [x*c for x in a]

def mul(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for j,x in enumerate(a):
        for k,y in enumerate(b):out[j+k]+=x*y
    return out

def power(a,n):
    out=[Q(1)]
    for _ in range(n):out=mul(out,a)
    return out

def integral(a):return sum((x/Q(j+1) for j,x in enumerate(a)),Q(0))

def strings(a):return [str(x) for x in a]

def ceiling(x,den):
    require(x>=0,'nonnegative square operand')
    n=isqrt(x.numerator*den*den//x.denominator)
    if Q(n,den)**2<x:n+=1
    r=Q(n,den)
    require(r*r>=x and (n==0 or Q(n-1,den)**2<x),'complete rational ceiling')
    return r

def typed_equal(x,y,where='expected'):
    require(type(x) is type(y),'type '+where)
    if isinstance(x,dict):
        require(set(x)==set(y),'keys '+where)
        for k in x:typed_equal(x[k],y[k],where+'.'+k)
    elif isinstance(x,list):
        require(len(x)==len(y),'length '+where)
        for k,(a,b) in enumerate(zip(x,y)):typed_equal(a,b,where+'.'+str(k))
    else:require(x==y,'value '+where)

def floor_root(x,den):
    require(x>=0,'nonnegative lower square operand')
    n=isqrt(x.numerator*den*den//x.denominator);r=Q(n,den)
    require(r*r<=x<(r+Q(1,den))**2,'complete rational lower root')
    return r

def polar_payment(al,ah,tl,th,fh,P,label,damage):
    bm,bx=1-ah**2,1-al**2;ab=min(al*(1-al**2),ah*(1-ah**2))
    c=al+1-al**2-ah
    if damage=='chord-slope':c+=Q(1,1000)
    require(c==al+1-al**2-ah and Q(1,2)<=al<=ah<1,'whole chord endpoint identity')
    require(0<=tl<=th<=TM and 0<=P and 0<fh<=8,'polar input signs '+label)
    delta=floor_root(tl/56,1024);ds=ceiling(Q(7,8)*th,256)
    if damage=='radial-lower-cap':delta+=Q(1,1024)
    require(delta**2<=tl/56<(delta+Q(1,1024))**2,'radial lower root '+label)
    cap=fh-7/(1+ah)-1;D=min(ds,cap)
    require(D>=0 and c-bm*delta>0,'radial positive factors '+label)
    mc=ah+bx*(1+D);nu=bx*(1+D)/mc;mb=ah+c;alpha=c/mb
    require(0<=nu<1 and 0<=alpha<1,'positive reciprocal expansions '+label)
    g2=[Q(0)];g1=[Q(0)]
    for n in range(5):
        z=power([Q(1),-Q(1)],n)
        value=(n+1)*nu**n/mc**2
        if damage=='drop-polar-series' and n==4:value=Q(0)
        g2=add(g2,scale(z,value))
        g1=add(g1,scale(z,alpha**n/mb))
    phase=ab*P;deficit=Q(3,4)*bm*(8-fh)
    if damage=='drop-deficit' and deficit>0:deficit=Q(0)
    K=add(scale([Q(0)]+g2,phase),scale([Q(0)]+g1,deficit))
    radial=mul([ah,c+7*bm*delta],power([ah,c-bm*delta],7))
    if damage=='radial-coefficient':radial[-1]+=Q(1,1000)
    full=mul(radial,add(add([Q(1)],scale(K,-1)),scale(mul(K,K),Q(1,2))))
    if damage=='last-polar-coefficient':full[-1]+=1
    # Independent binomial radial vector and reciprocal basis coefficients.
    factors=[]
    for i in range(9):
        value=Q(0)
        if i<=7:value+=comb(7,i)*ah**(8-i)*(c-bm*delta)**i
        if i>=1:value+=(c+7*bm*delta)*comb(7,i-1)*ah**(8-i)*(c-bm*delta)**(i-1)
        factors.append(value)
    require(radial==factors,'all radial coefficients '+label)
    kernels=[ab*P*(n+1)*nu**n/mc**2+Q(3,4)*bm*(8-fh)*alpha**n/mb for n in range(5)]
    alternateK=[Q(0)]*6
    for n,v in enumerate(kernels):
        for j in range(n+1):alternateK[j+1]+=v*comb(n,j)*(-1)**j
    require(K==alternateK,'all phase/deficit coefficients '+label)
    terms=[(1,n,v) for n,v in enumerate(kernels)]
    weighted=[(0,0,Q(1))]+[(r,n,-v) for r,n,v in terms]
    weighted +=[(r+s,n+k,v*w/2) for r,n,v in terms for s,k,w in terms]
    alternate=[Q(0)]*19;beta_area=Q(0)
    for r,n,v in weighted:
        for i,f in enumerate(factors):
            for j in range(n+1):alternate[i+r+j]+=f*v*comb(n,j)*(-1)**j
            beta_area+=f*v*Q(factorial(i+r)*factorial(n),factorial(i+r+n+1))
    require(len(full)==19 and full==alternate,'whole19 polar coefficients '+label)
    area=integral(full)
    require(area==beta_area,'coefficient/beta integral '+label)
    return dict(label=label,a=strings([al,ah]),T=strings([tl,th]),F_upper=str(fh),phase_lower=str(P),delta=str(delta),max_e_upper=str(D),sqrt_e_upper=str(ds),radius_e_upper=str(cap),kernel_coefficients=strings(K),radial_coefficients=strings(radial),all_coefficients=strings(full),integral=str(area))

def enclose(box,damage):
    al,ah,el,eh,fl,fh,ul,uh,wl,wh=box;steps=[]
    for iteration in range(4):
        old=(al,ah,el,eh,fl,fh,ul,uh,wl,wh)
        uh=min(uh,fh/8);ul=max(ul,fl/8-eh/16)
        fl=max(fl,8*ul);fh=min(fh,8*uh+eh/2)
        el=max(el,2*max(Q(0),fl-8*uh),8*((1-uh)**2+wl))
        wh=min(wh,(fh/8)**2-ul*ul,eh/8-(1-uh)**2)
        new=(al,ah,el,eh,fl,fh,ul,uh,wl,wh)
        # Each step is an enclosing intersection; no retained interval grows.
        require(all(new[2*j]>=old[2*j] and new[2*j+1]<=old[2*j+1] for j in range(5)),'enclosing intersection monotonicity')
        steps.append(dict(iteration=iteration,before=strings(old),after=strings(new)))
        failed=[j for j in range(5) if new[2*j]>new[2*j+1]]
        if failed:return dict(status='empty-necessary-inequalities',steps=steps,empty_axes=failed,tightened=strings(new))
    tl=max(Q(0),el-2*(fh-8*ul),(8-fh)**2/8)
    if damage=='wrong-T-lower':tl+=Q(1,1000)
    independent_tl=max(Q(0),el-2*fh+16*ul,(fh**2-16*fh+64)/8)
    require(tl==independent_tl,'retained full lower radial/energy coupling')
    floor=1/(1+ah)
    th=min(eh-2*max(Q(0),fl-8*uh),(fh-7*floor-1)**2+7*(floor-1)**2)
    independent_th=min(eh-max(Q(0),2*fl-16*uh),fh**2-2*fh*(7*floor+1)+56*floor**2+8)
    require(th==independent_th,'retained full upper radial/energy coupling')
    require(fl>=MASS and fh<=8 and floor<=Q(5,8) and fl>7*floor+1,'convex radius-budget endpoint regime')
    out=dict(status='empty-derived-T' if tl>th else 'nonempty-enclosure',steps=steps,tightened=strings(new),T=strings([tl,th]))
    if damage=='false-empty' and out['status']=='nonempty-enclosure':
        require(tl>th,'false whole-box pruning rejected')
    return out

def multinomial_quadratic(a,n):
    out=[Q(0)]*(2*n+1)
    for j in range(n+1):
        for k in range(n-j+1):
            i=n-j-k
            out[j+2*k]+=Q(factorial(n),factorial(i)*factorial(j)*factorial(k))*a[0]**i*a[1]**j*a[2]**k
    return out

def clean(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [clean(v) for v in x]
    return x

def centered_constants(damage):
    p={2:Q(1),4:Q(25,32),6:Q(43,64),8:Q(1201,2048)}
    for m in (2,3,4):
        require(p[2*m]==Q(7,8)**m+Q(1,8)**m and p[2*m]>=Q(1,2)**(m-1),
                'whole even absolute-moment endpoint payment')
    for k in (3,5,7):p[k]=ceiling(p[k-1]*p[k+1],1024)
    require([p[k] for k in (3,5,7)]==[Q(453,512),Q(371,512),Q(643,1024)],
            'whole odd absolute-moment payments')
    tau=ceiling(Q(1,8),1024);c=[Q(1),Q(0)];rows=[]
    require(tau==Q(363,1024),'centered subset root payment')
    for k in range(2,9):
        n=sum((c[k-j]*p[j] for j in range(2,k+1)),Q(0))/k
        cs=Q(comb(8,k),8**(k//2))*(tau if k%2 else 1)
        choice=min(n,cs)
        if damage=='centered-third-underpay' and k==3:choice-=Q(1,1000)
        if damage=='newton-eighth' and k==8:choice-=Q(1,1000)
        c.append(choice)
        rows.append(dict(order=k,moment_caps={j:p[j] for j in range(2,k+1)},
                         newton=n,cauchy_maclaurin=cs,chosen=choice))
    require(c==[Q(1),Q(0),Q(1,2),Q(151,512),Q(41,128),Q(1497,5120),
                Q(7,128),Q(363,65536),Q(1,4096)],'all seven centered Newton payments')
    # A boundary witness genuinely needs the convex anchor below the marked a.
    A=B=H;U=GAMMA;sm=Q(1);a0=min(A,2*U/sm-B)
    if damage=='unsafe-anchor':a0=A
    require(a0==2*GAMMA-H and 0<a0<LOW and 2*U>=(a0+B)*sm,
            'convex anchor boundary payment')
    old_quartic=c[4];c[4]=origin.hilbert_quartic_payment(damage)
    require(old_quartic==Q(41,128),'whole prior quartic payment')
    contour=origin.contour_cap_payment(damage)
    for order in (5,6,7):c[order]=origin.CAP[order]
    rows.append(dict(method='credited published centered coefficient contour',payments=contour))
    require(c==origin.CAP,'whole final centered amplitude agreement')
    rows.append(dict(order=4,old_payment=old_quartic,
                     squared_variance_payment=origin.quartic_cap_payment(damage),
                     real_Hilbert_payment=c[4],
                     trust='ordinary published REAL Hilbert Banach norm identity'))
    return c,rows

def origin_payment(path,tight,T,constants,damage):
    al,ah,el,eh,fl,fh,ul,uh,wl,wh=map(Q,tight);tl,th=map(Q,T)
    sm=min(Q(1),uh**2+wh,(fh/8)**2)
    sb=min(sm,ul**2+wh)
    energyS=eh-8*((1-uh)**2+wl);jointS=th+2*fh-8-8*(ul**2+wl)
    SM=min(energyS,jointS)
    if damage=='uncouple-energy':SM=eh
    require(SM==min(eh-8+16*uh-8*uh**2-8*wl,th+2*fh-8-8*ul**2-8*wl),
            'whole mean/energy coupling '+path)
    require(0<ul**2<=sb<=sm<=1 and 0<=ul<=uh<=1 and wh>=0,
            'separate actual norm and synchronized envelope signs '+path)
    if SM<0:return dict(status='empty-negative-centered-energy',Smax=str(SM))
    anchor=min(al,2*ul/sb-ah)
    require(0<anchor<=al<=ah<=H,'whole convex anchor containment '+path)
    require(2*ul>=(anchor+ah)*sb and ul>anchor*sb,
            'whole convex endpoint and derivative payments '+path)
    beta=[Q(1),-2*anchor*ul,anchor**2*sb];b1=sum(beta)
    require(0<b1<1 and 1-anchor*ul>0,'whole beta and odd-root signs '+path)
    ds,db,dS=ceiling(sm,4096),ceiling(b1,4096),ceiling(SM,4096)
    if damage=='synchronized-denominator':ds=ceiling(sb,4096)
    require(ds==ceiling(min(Q(1),uh**2+wh,(fh/8)**2),4096),
            'actual mean denominator must not use envelope coefficient '+path)
    require(1-db*b1**4>0 and ah*ds>0,'whole diagonal signs '+path)
    D=(1-db*b1**4)/(ah*ds)
    root=[Q(1),-anchor*ul,anchor**2*(sb-ul**2)/(2*(1-anchor*ul))]
    if damage=='origin-odd-root':root[-1]*=2
    otherroot=[Q(1),beta[1]/2,(beta[2]-beta[1]**2/4)/(2+beta[1])]
    require(root==otherroot,'whole odd square-root coefficients '+path)
    rows=[];R=Q(0)
    for l in range(2,9):
        pol=power(beta,(8-l)//2)
        if l%2:pol=mul(pol,root)
        factor=9*ah**l*constants[l]*SM**(l//2)*(dS if l%2 else 1)
        pol=[Q(0)]*l+scale(pol,factor)
        other=multinomial_quadratic(beta,(8-l)//2)
        if l%2:
            paid=[Q(0)]*(len(other)+2)
            for j,x in enumerate(other):
                for k,y in enumerate(otherroot):paid[j+k]+=x*y
            other=paid
        other=[Q(0)]*l+scale(other,factor)
        require(pol==other,'ALL centered coefficients '+path+' order'+str(l))
        value=integral(pol);second=Q(0);n=(8-l)//2
        for j in range(n+1):
            for k in range(n-j+1):
                i=n-j-k
                z=Q(factorial(n),factorial(i)*factorial(j)*factorial(k))*beta[0]**i*beta[1]**j*beta[2]**k
                base=l+j+2*k+1;v=Q(1,base)
                if l%2:v+=otherroot[1]/(base+1)+otherroot[2]/(base+2)
                second+=factor*z*v
        require(value==second and value>=0,'ALL nonnegative centered integrals '+path)
        if damage=='origin-drop-eighth' and l==8:continue
        rows.append(dict(order=l,coefficients=pol,integral=value));R+=value
    require([r['order'] for r in rows]==list(range(2,9)),'ALL seven centered orders '+path)
    return clean(dict(status='bounded',path=path,smax=sm,beta_s=sb,
                      envelope_is_not_actual_mean_norm=True,Smax=SM,energyS=energyS,
                      jointS=jointS,anchor=anchor,anchor_gap=2*ul-(anchor+ah)*sb,
                      beta=beta,beta1=b1,odd_root=root,dmean=ds,dbeta=db,dS=dS,
                      D=D,R=R,score=D-R,terms=rows))

def bernstein(coefficients,low,high):
    n=len(coefficients)-1;width=high-low
    translated=[sum((coefficients[j]*comb(j,k)*low**(j-k)*width**k
                     for j in range(k,n+1)),Q(0)) for k in range(n+1)]
    controls=[sum((translated[k]*Q(comb(i,k),comb(n,k))
                   for k in range(i+1)),Q(0)) for i in range(n+1)]
    return translated,controls

def badd(a,b):
    out=a.copy()
    for k,x in b.items():out[k]=out.get(k,Q(0))+x
    return out

def bmul(a,b):
    out={}
    for (d,t),x in a.items():
        for (e,s),y in b.items():
            key=(d+e,t+s);out[key]=out.get(key,Q(0))+x*y
    return out

def energy_payment(path,tight,T,damage):
    al,ah,el,eh,fl,fh,ul,uh,wl,wh=map(Q,tight);tl,th=map(Q,T)
    dl,dh=floor_root(tl/56,4096),ceiling(th/56,4096)
    bm,bx=1-ah**2,1-al**2;ab=min(al*(1-al**2),ah*(1-ah**2));c=al+1-al**2-ah
    D=min(ceiling(Q(7,8)*th,256),fh-7/(1+ah)-1)
    require(0<=tl<=th<=TM and 0<fh<=8 and D>=0 and c-bm*dh>0,
            'whole coupled radial input signs '+path)
    require(el/2-28*dh**2>=0,'whole E/T phase sign '+path)
    mc,mb=ah+bx*(1+D),ah+c;nu,alpha=bx*(1+D)/mc,c/mb
    require(0<=nu<1 and 0<=alpha<1,'positive coupled reciprocal kernels '+path)
    g2=[Q(0)];g1=[Q(0)]
    for n in range(5):
        z=power([Q(1),-Q(1)],n)
        g2=add(g2,scale(z,(n+1)*nu**n/mc**2))
        g1=add(g1,scale(z,alpha**n/mb))
    k0=add(scale([Q(0)]+g2,ab*el/2),scale([Q(0)]+g1,Q(3,4)*bm*(8-fh)))
    k2=scale([Q(0)]+g2,-28*ab)
    H2={0:add(add([Q(1)],scale(k0,-1)),scale(mul(k0,k0),Q(1,2))),
        2:add(scale(k2,-1),mul(k0,k2)),4:scale(mul(k2,k2),Q(1,2))}
    radial=[]
    for i in range(9):
        z=comb(7,i)*(-1)**i if i<=7 else 0
        if i:z+=7*comb(7,i-1)*(-1)**(i-1)
        radial.append([Q(0)]*i+scale(power([ah,c],8-i),z*bm**i))
    matrix=[[Q(0)]*19 for _ in range(13)]
    for i,p in enumerate(radial):
        for j,h in H2.items():
            for k,z in enumerate(mul(p,h)):matrix[i+j][k]+=z
    if damage=='last-bivariate-coefficient':matrix[-1][-1]+=Q(1,1000)
    if damage=='uncouple-T':
        for i in range(9,13):matrix[i]=[Q(0)]*19
    # Distinct representation: eight literal bivariate factors and kernels
    # in the unexpanded t^r(1-t)^n basis, followed by exact beta integrals.
    actualrad={(0,0):Q(1)}
    for j in range(8):
        actualrad=bmul(actualrad,{(0,0):ah,(0,1):c,(1,1):(7 if j==0 else -1)*bm})
    kernels=[];K={}
    for n in range(5):
        coeff={0:ab*el*(n+1)*nu**n/(2*mc**2)+Q(3,4)*bm*(8-fh)*alpha**n/mb,
               2:-28*ab*(n+1)*nu**n/mc**2}
        kernels.append((n,coeff))
        for d,x in coeff.items():
            for k in range(n+1):
                key=(d,k+1);K[key]=K.get(key,Q(0))+x*comb(n,k)*(-1)**k
    h=badd({(0,0):Q(1)},{k:-x for k,x in K.items()})
    h=badd(h,{k:x/2 for k,x in bmul(K,K).items()})
    alt=bmul(actualrad,h)
    require(all(0<=d<=12 and 0<=t<=18 for d,t in alt),'whole coupled bivariate degree '+path)
    other=[[alt.get((d,t),Q(0)) for t in range(19)] for d in range(13)]
    require(matrix==other,'ALL13x19 coupled coefficient identities '+path)
    weights={(0,0,0):Q(1)}
    for n,coeff in kernels:
        for d,x in coeff.items():
            key=(d,1,n);weights[key]=weights.get(key,Q(0))-x
    for n,coeff in kernels:
        for q,othercoeff in kernels:
            for d,x in coeff.items():
                for e,y in othercoeff.items():
                    key=(d+e,2,n+q);weights[key]=weights.get(key,Q(0))+x*y/2
    integrated=[Q(0)]*13
    for (d,t),x in actualrad.items():
        for (e,r,n),y in weights.items():
            integrated[d+e]+=x*y*Q(factorial(t+r)*factorial(n),factorial(t+r+n+1))
    full=[integral(p) for p in matrix]
    if damage=='energy-integral-coefficient':full[-1]+=Q(1,1000)
    require(full==integrated,'ALL13 coupled beta integral identities '+path)
    translated,controls=bernstein(full,dl,dh)
    if damage=='last-Bernstein-control':controls[-1]+=Q(1,1000)
    reverse=[sum((controls[i]*comb(12,i)*comb(12-i,k-i)*(-1)**(k-i)
                  for i in range(k+1)),Q(0)) for k in range(13)]
    require(reverse==translated,'ALL13 Bernstein reconstruction coefficients '+path)
    othertranslation=[Q(0)]*13
    for j,x in enumerate(integrated):
        for k,y in enumerate(power([dl,dh-dl],j)):othertranslation[k]+=x*y
    require(othertranslation==translated,'ALL13 rational interval translation coefficients '+path)
    return clean(dict(path=path,delta_interval=[dl,dh],phase_minimum=el/2-28*dh**2,
                      full_t_by_delta_coefficients=matrix,full_delta_coefficients=full,
                      rescaled_delta_coefficients=translated,bernstein_controls=controls,
                      integral_upper=max(controls),D=D))
