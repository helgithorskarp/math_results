"""Independent exact rational face reconstruction from the written formulas and COVER DATA.
No author program/EXPECTED/validator import. Two-variable sparse polynomial algebra.
"""
from fractions import Fraction as Q
from math import comb,factorial,isqrt
import hashlib,json

def need(ok,message):
    if not ok:raise ValueError(message)

def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def digest(x):return hashlib.sha256(canon(x)).hexdigest()
def fq(x):
    need(type(x) is str,'rational string')
    v=Q(x);need(str(v)==x,'canonical rational string');return v

def root(x,den,upper):
    need(x>=0 and type(den) is int and den>0,'root domain')
    z=isqrt(x.numerator*den*den//x.denominator)
    need(Q(z,den)**2<=x<Q(z+1,den)**2,'minimal rational root bracket')
    if upper and Q(z,den)**2<x:z+=1
    return Q(z,den)

class Poly:
    # Coordinates (v,t); v is u for mean, d for polar. Exact sparse arithmetic.
    def __init__(self,a=0):
        self.a={k:Q(v) for k,v in a.items() if v} if isinstance(a,dict) else ({(0,0):Q(a)} if a else {})
    def __add__(self,other):
        other=other if isinstance(other,Poly) else Poly(other);d=self.a.copy()
        for k,v in other.a.items():d[k]=d.get(k,Q(0))+v
        return Poly(d)
    __radd__=__add__
    def __neg__(self):return Poly({k:-v for k,v in self.a.items()})
    def __sub__(self,b):return self+-aspoly(b)
    def __rsub__(self,b):return aspoly(b)+-self
    def __mul__(self,other):
        other=aspoly(other);d={}
        for (i,j),a in self.a.items():
            for (k,l),b in other.a.items():
                key=(i+k,j+l);d[key]=d.get(key,Q(0))+a*b
        return Poly(d)
    __rmul__=__mul__
    def __truediv__(self,b):return self*Q(1,b)
    def __pow__(self,n):
        need(type(n) is int and n>=0,'polynomial power');r=Poly(1);b=self
        while n:
            if n%2:r=r*b
            n//=2
            if n:b=b*b
        return r
    def integrated_t(self):
        d={}
        for (i,j),a in self.a.items():d[i]=d.get(i,Q(0))+a/Q(j+1)
        return [d.get(i,Q(0)) for i in range(max(d,default=0)+1)]
    def matrix(self,nv,nt):
        need(all(0<=i<nv and 0<=j<nt for i,j in self.a),'complete declared polynomial shape')
        return [[str(self.a.get((i,j),Q(0))) for j in range(nt)] for i in range(nv)]
    def value(self,v,t):return sum(a*v**i*t**j for (i,j),a in self.a.items())

def aspoly(x):return x if isinstance(x,Poly) else Poly(x)
V=Poly({(1,0):1});T=Poly({(0,1):1})

def eval1(coeff,x):
    r=Q(0)
    for a in reversed(coeff):r=r*x+a
    return r

def bernstein(coeff,lo,hi,n):
    need(lo<=hi and len(coeff)<=n+1,'Bernstein degree/interval')
    # Direct binomial translation; verify the entire reconstruction independently.
    b=[sum(coeff[j]*comb(j,k)*lo**(j-k)*(hi-lo)**k for j in range(k,len(coeff))) for k in range(n+1)]
    ctr=[sum(b[k]*Q(comb(i,k),comb(n,k)) for k in range(i+1)) for i in range(n+1)]
    rec=[sum(ctr[i]*comb(n,i)*comb(n-i,k-i)*(-1)**(k-i) for i in range(k+1)) for k in range(n+1)]
    need(rec==b,'whole Bernstein polynomial identity')
    need(eval1(b,Q(0))==eval1(coeff,lo) and eval1(b,Q(1))==eval1(coeff,hi),'both endpoint anchors')
    return ctr

def constants():
    eta={2:Q(1),4:Q(25,32),6:Q(43,64),8:Q(1201,2048)}
    for j in (3,5,7):eta[j]=root(eta[j-1]*eta[j+1],1024,True)
    c={0:Q(1),1:Q(0)};rr=root(Q(1,8),1024,True)
    for k in range(2,9):c[k]=min(sum(c[k-j]*eta[j] for j in range(2,k+1))/k,Q(comb(8,k),8**(k//2))*rr**(k%2))
    need([c[k] for k in range(2,9)]==[Q(1,2),Q(151,512),Q(41,128),Q(1497,5120),Q(7,128),Q(363,65536),Q(1,4096)],'complete Newton/Maclaurin recurrence')
    before=c.copy();c[4]=Q(3,16)
    need(Q(3,32)*(Q(1,2)**2+6*Q(1,2)**2+Q(1,2)**2)==c[4],'real Banach complexification budget')
    return c,dict(power_coefficients={str(k):str(v) for k,v in eta.items()},old_centered={str(k):str(before[k]) for k in range(2,9)},centered={str(k):str(c[k]) for k in range(2,9)},external_ordinary_premise='Banach REAL Hilbert symmetric multilinear/polynomial norm equality; arXiv1810.09373,Introduction(2). No independent finite norm proof claimed.')


def enclosure(raw):
    A,B,E0,E1,u0,u1,w0,w1=raw;F0=F1=Q(8)
    history=[]
    for _ in range(4):
        before=[A,B,E0,E1,F0,F1,u0,u1,w0,w1]
        u1=min(u1,F1/8);u0=max(u0,F0/8-E1/16)
        F0=max(F0,8*u0);F1=min(F1,8*u1+E1/2)
        E0=max(E0,2*max(Q(0),F0-8*u1),8*((1-u1)**2+w0))
        w1=min(w1,(F1/8)**2-u0*u0,E1/8-(1-u1)**2)
        after=[A,B,E0,E1,F0,F1,u0,u1,w0,w1]
        need(all(after[j]>=before[j] for j in (0,2,4,6,8)) and all(after[j]<=before[j] for j in (1,3,5,7,9)),'monotone necessary enclosure')
        history.append([str(x) for x in after])
    need(A<=B and E0<=E1 and F0<=F1 and u0<=u1 and w0<=w1,'nonempty necessary enclosure')
    need(F0==F1==8,'defining exact mass eight, not altered interval')
    m=1/(1+B);need(F0>=Q(37,5)>7*m+1,'radius variance endpoint license')
    tl=max(Q(0),E0-2*F1+16*u0,(8-F1)**2/8)
    th=min(E1-2*max(Q(0),F0-8*u1),(F1-7*m-1)**2+7*(m-1)**2)
    need(0<=tl<=th,'full necessary radial variance interval')
    return dict(A=A,B=B,E0=E0,E1=E1,F0=F0,F1=F1,u0=u0,u1=u1,w0=w0,w1=w1,tl=tl,th=th,history=history)

def polar_setup(e):
    A,B,tl,th,F1=e['A'],e['B'],e['tl'],e['th'],e['F1']
    bm=1-B*B;bp=1-A*A;aa=min(A*(1-A*A),B*(1-B*B));c=A+1-A*A-B
    D=min(root(7*th/8,256,True),F1-7/(1+B)-1)
    mc=B+bp*(1+D);mb=B+c;nu=bp*(1+D)/mc;alpha=c/mb
    need(D>=0 and c>0 and 0<=nu<1 and 0<=alpha<1 and bm>0 and aa>0,'polar denominators/sign gates')
    G2=sum((j+1)*nu**j*(1-T)**j for j in range(5))/(mc*mc)
    G1=sum(alpha**j*(1-T)**j for j in range(5))/mb
    return bm,bp,aa,c,D,G1,G2

def standard_polar(e,P):
    bm,bp,aa,c,D,G1,G2=polar_setup(e);delta=root(e['tl']/56,1024,False)
    need(c-bm*delta>0 and P>=0,'standard radial positive kernel')
    R=(e['B']+(c+7*bm*delta)*T)*(e['B']+(c-bm*delta)*T)**7
    K=aa*P*T*G2+Q(3,4)*bm*(8-e['F1'])*T*G1
    Qp=R*(1-K+K*K/2);vec=Qp.matrix(1,19)[0]
    val=Qp.integrated_t()[0]
    # Integral again as exact endpoint antiderivative; every coefficient retained.
    need(val==sum(Q(x)/Q(j+1) for j,x in enumerate(vec)),'whole scalar polar integral')
    return val,dict(vector=vec,integral=str(val),delta=str(delta),P=str(P),D=str(D))

def joint_polar(e):
    bm,bp,aa,c,D,G1,G2=polar_setup(e);dl=root(e['tl']/56,4096,False);dh=root(e['th']/56,4096,True)
    need(e['E0']/2-28*dh*dh>=0 and c-bm*dh>0,'joint polar license')
    rad=(e['B']+(c+7*bm*V)*T)*(e['B']+(c-bm*V)*T)**7
    kernel=aa*(e['E0']/2-28*V*V)*T*G2+Q(3,4)*bm*(8-e['F1'])*T*G1
    expr=rad*(1-kernel+kernel*kernel/2);matrix=expr.matrix(13,19);integ=expr.integrated_t()
    need(len(integ)<=13,'joint polar degree');controls=bernstein(integ,dl,dh,12)
    return max(controls),dict(matrix=matrix,integrals=[str(x) for x in integ],controls=[str(x) for x in controls],dl=str(dl),dh=str(dh))

def scalar_origin(e,c):
    A,B,U0,U1,W0,W1=e['A'],e['B'],e['u0'],e['u1'],e['w0'],e['w1']
    sm=min(Q(1),U1*U1+W1,(e['F1']/8)**2);sb=min(sm,U0*U0+W1)
    Sp=min(e['E1']-8*((1-U1)**2+W0),e['th']+2*e['F1']-8-8*(U0*U0+W0))
    need(Sp>=0 and sb>0,'scalar centered envelope')
    a0=min(A,2*U0/sb-B);beta=1-2*a0*U0*T+a0*a0*sb*T*T
    be=beta.value(0,1)
    need(U0*U0<=sb<=sm<=1 and Q(0)<a0<=A<=B and U0>a0*sb and 0<be<1 and 1-a0*U0>0,'scalar actual/beta distinction and anchor gates')
    odd=1-a0*U0*T+a0*a0*(sb-U0*U0)/(2*(1-a0*U0))*T*T
    ds=root(sm,4096,True);db=root(be,4096,True);dS=root(Sp,4096,True)
    need(1-db*be**4>0 and ds>0,'scalar diagonal numerator/actual denominator')
    Di=(1-db*be**4)/(B*ds);records=[];R=Q(0)
    for k in range(2,9):
        h=beta**((8-k)//2) if not k%2 else beta**((7-k)//2)*odd
        part=9*B**k*c[k]*Sp**(k//2)*dS**(k%2)*T**k*h
        val=part.integrated_t()[0];need(val>=0,'every scalar centered order nonnegative')
        records.append(dict(order=k,vector=part.matrix(1,10)[0],integral=str(val)));R+=val
    return Di-R,dict(diagonal=str(Di),remainder=str(R),orders=records,a0=str(a0),s_actual=str(sm),s_beta=str(sb),S=str(Sp))

def retained_mean(e,c,kind):
    A,B,L,U,Wl,Wh=e['A'],e['B'],e['u0'],e['u1'],e['w0'],e['w1']
    a0=min(A,2*L/(L*L+Wh)-B,2*U/(U*U+Wh)-B)
    need(a0>0 and a0<=A and 2*L>=(a0+B)*(L*L+Wh) and 2*U>=(a0+B)*(U*U+Wh) and 1-a0*U>0,'retained both endpoint anchor gates')
    beta=1-2*a0*V*T+a0*a0*(V*V+Wh)*T*T
    odd=1-a0*V*T+a0*a0*Wh/(2*(1-a0*U))*T*T
    if kind=='energy':
        S=e['E1']-8*((1-V)**2+Wl);smin=S.value(L,0);smax=S.value(U,0)
    else:
        S=e['th']+2*e['F1']-8-8*(V*V+Wl);smin=S.value(U,0);smax=S.value(L,0)
    need(0<=smin<=smax,'retained chosen polynomial energy gate')
    dS=root(smax,4096,True);dm=root(min(Q(1),U*U+Wh,(e['F1']/8)**2),4096,True)
    be=beta.value(L,1);db=root(be,4096,True)
    need(dm>0 and be>0 and 1-db*be**4>0,'retained diagonal/actual denominator gates')
    N=1-db*(1-2*a0*V+a0*a0*(V*V+Wh))**4
    R=Poly(0);orders=[]
    for k in range(2,9):
        h=beta**((8-k)//2) if not k%2 else beta**((7-k)//2)*odd
        part=9*B**k*c[k]*S**(k//2)*dS**(k%2)*T**k*h
        integrals=part.integrated_t();orders.append(dict(order=k,matrix=part.matrix(9,10),integrals=[str(x) for x in integrals]))
        R+=Poly({(i,0):v for i,v in enumerate(integrals)})
    lowpoly=N/(B*dm)-R
    lowcontrols=bernstein(lowpoly.integrated_t(),L,U,8)
    denominator=B*(V+Wh/(2*L));dL=denominator.value(L,0);dU=denominator.value(U,0)
    need(0<dL<=dU,'positive retained variable denominator')
    cleared=N-denominator*(1+R);controls=bernstein(cleared.integrated_t(),L,U,9);minimum=min(controls)
    low9=1+minimum/(dU if minimum>=0 else dL);low8=min(lowcontrols)
    return max(low8,low9),dict(kind=kind,a0=str(a0),S_min=str(smin),S_max=str(smax),all_orders=orders,degree8_controls=[str(v) for v in lowcontrols],numerator=N.matrix(10,1),cleared=cleared.matrix(10,1),degree9_controls=[str(v) for v in controls],denominator=[str(dL),str(dU)],lower8=str(low8),lower9=str(low9))

def product_cap(e):
    m=1/(1+e['B']);floorcap=e['F1']-7*m
    rv=Q(7,8)*(e['th']-(e['F1']-8)**2/8);need(rv>=0,'radial product root domain')
    cen=root(rv,4096,True);R=max(Q(1),min(floorcap,e['F1']/8+cen))
    z=8-e['F1']+e['tl']/(2*R);need(z>=0,'product exponential sign')
    parts=[z**j/factorial(j) for j in range(5)];C=1/sum(parts)
    need(C>0 and sum(parts)>=1,'full positive lower exponential')
    return C,dict(R=str(R),z=str(z),terms=[str(x) for x in parts],cap=str(C))

def closed_cover(data):
    need(type(data) is dict and set(data)=={'root','splits','leaves'},'entire COVER schema')
    need(type(data['root']) is list and len(data['root'])==8,'COVER root shape')
    rootbox=[fq(x) for x in data['root']];need(rootbox==[Q(27,40),Q(11,16),Q(0),Q(23,5),Q(51,80),Q(1),Q(0),Q(23,40)],'original complete closed root box')
    splits=data['splits'];leaves=data['leaves'];need(type(splits) is dict and type(leaves) is dict,'COVER tree objects');need(not(set(splits)&set(leaves)),'split/leaf exclusive')
    roles={'scalar-product-origin','retained-mean-product-origin','joint-energy-polar','standard-polar'}
    need(all(type(k) is str and set(k)<=set('01') for k in list(splits)+list(leaves)),'tree paths');visited=[];out=[]
    def visit(path,box):
        need(path not in visited,'unique reachable closed node');visited.append(path)
        if path in leaves:
            need(leaves[path] in roles,'known mathematical role');out.append((path,leaves[path],box));return
        need(path in splits,'no missing/unpaid child');row=splits[path];need(type(row) is dict and set(row)=={'axis','cut'},'split schema')
        axis=row['axis'];need(type(axis) is int and 0<=axis<4,'strict integer axis');cut=fq(row['cut']);need(box[2*axis]<cut<box[2*axis+1],'strict rational cut')
        left=box.copy();right=box.copy();left[2*axis+1]=cut;right[2*axis]=cut
        visit(path+'0',left);visit(path+'1',right)
    visit('',rootbox);need(set(visited)==set(splits)|set(leaves),'all source nodes reachable')
    return out,dict(nodes=len(visited),splits=len(splits),leaves=len(leaves),max_depth=max(len(x) for x in visited))

def floor_fraction(x,den=10**9):return str(Q(x.numerator*den//x.denominator,den))

def make(data):
    c,cconstants=constants();leaves,tree=closed_cover(data)
    energy=[]
    for j in range(75):
        lo=Q(j,8);hi=min(Q(j+1,8),Q(6776,729));need(lo<=hi,'closed energy shell')
        e=dict(A=Q(27,40),B=Q(11,16),tl=lo,th=hi,F1=Q(8));val,rec=standard_polar(e,max(Q(0),(Q(23,5)-hi)/2))
        need(val<Q(2199,2200),'all closed energy entry shells paid');energy.append(rec)
    need(Q(75,8)>=Q(6776,729) and Q(74,8)<Q(6776,729),'whole T-shell coverage endpoint')
    full=[];compact=[];rolecount={k:0 for k in ('scalar-product-origin','retained-mean-product-origin','joint-energy-polar','standard-polar')};origins=[];polars=[]
    for path,role,box in leaves:
        e=enclosure(box);low,scalar=scalar_origin(e,c);pcap,prod=product_cap(e);rec=dict(path=path,role=role,enclosure={k:v if k=='history' else str(v) for k,v in e.items()},scalar=scalar,product=prod)
        if role=='retained-mean-product-origin':
            pay=[]
            for kind in ('energy','polar'):
                val,record=retained_mean(e,c,kind);pay.append(val);rec[kind]=record
            low=max(low,*pay)
        if role in ('scalar-product-origin','retained-mean-product-origin'):
            margin=low-pcap;need(margin>Q(1,3100),'defining whole origin leaf margin');origins.append((margin,path));bound=margin
        else:
            if role=='standard-polar':val,record=standard_polar(e,max(Q(0),(e['E0']-e['th'])/2))
            else:val,record=joint_polar(e)
            need(val<Q(2199,2200),'defining whole polar leaf margin');rec['polar']=record;bound=1-val;polars.append((bound,path))
        full.append(rec);rolecount[role]+=1;compact.append(dict(path=path,role=role,payment_lower=floor_fraction(bound),complete_polynomial_record_sha256=digest(rec)))
    need(tree==dict(nodes=313,splits=156,leaves=157,max_depth=13),'full source closed tree census')
    need(rolecount=={'scalar-product-origin':98,'retained-mean-product-origin':21,'joint-energy-polar':37,'standard-polar':1},'defining source role census')
    fullrecord=dict(energy=energy,leaves=full,constants=cconstants)
    raw=canon(fullrecord);summary=dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',scope='NEW adjacent degree9 annulus[27/40,11/16], no runtime/ancestor theorem input',tree=tree,role_counts=rolecount,constants=cconstants,all_closed_energy_shells=75,all_scalar_centered_orders=7*len(full),all_full_joint_matrices=37,full_mean_channels=42,full_mean_order_matrices=294,all_defining_origin_leaves=119,all_defining_polar_leaves=38,all_full_coefficients_before_summary=True,least_origin=dict(path=min(origins)[1],exact=str(min(origins)[0])),least_polar=dict(path=min(polars)[1],exact=str(min(polars)[0])),full_polynomial_record_bytes=len(raw),full_polynomial_record_sha256=hashlib.sha256(raw).hexdigest(),payments=compact)
    return summary,fullrecord
