"""Independent complete10240 audit. No author executable is read or imported.

Arithmetic.py is unchanged reviewer1 source from the credited 10168 audit.
The new estimates are implemented from the signed ordinary mathematics.
Complete intermediate records belong in scratch, not publication.
"""
import argparse
import hashlib
import json
from math import comb, isqrt
from pathlib import Path
from arithmetic import (F, require, add, scale, mul, power, integrate, pad,
                        bproduct, bpower, btopower, bintegrate, elevate,
                        kernel_bernstein, ceiling, encode)

ROOT = list(map(F, ['13/20','2/3','0','23/5','37/5','8','51/80','1','0','23/40']))
JP, OP = F(99999,100000), F(10001,10000)


def parse_fraction(x):
    require(type(x) is str, 'fraction string type')
    y=F(x);require(str(y)==x, 'canonical rational');return y


def floorroot(x, d):
    require(x>=0, 'floor root domain');y=x*d*d;k=isqrt(y.numerator//y.denominator)
    require(F(k*k)<=y<F((k+1)**2), 'whole lower square bracket')
    return F(k,d)


def constants():
    eta=[F(0)]*9;eta[2]=F(1)
    for k in [4,6,8]:eta[k]=F(7,8)**(k//2)+F(1,8)**(k//2)
    for k in [3,5,7]:eta[k]=ceiling(eta[k-1]*eta[k+1],1024)
    tau=ceiling(F(1,8),1024);c=[F(1),F(0)]
    for k in range(2,9):
        c.append(min(sum((c[k-j]*eta[j] for j in range(2,k+1)),F(0))/k,
                     comb(8,k)*F(8)**(-(k//2))*tau**(k%2)))
    require(c[2:]==list(map(F,['1/2','151/512','41/128','1497/5120','7/128','363/65536','1/4096'])),
            'all Newton/Maclaurin budgets')
    original_c=c[:];c[4]=F(3,16)
    p=power([F(2,3),F(673,1200)*F(37,40)],8)
    i=integrate(p)
    endpoint=F(2,3)+F(673,1200)*F(37,40)
    require(i==(endpoint**9-F(2,3)**9)/(9*F(673,1200)*F(37,40))<1,
            'scalar closed mass bound')
    return c, {'eta':eta[2:],'c':c[2:],'pre_quartic_c':original_c[2:],'external_real_Hilbert_M':F(3,32),'tau':tau,'mass_coefficients':p,'mass_integral':i}


def tighten(box):
    x=box[:];steps=[]
    for _ in range(4):
        before=x[:];a,b,el,eh,fl,fh,ul,uh,wl,wh=x
        uh=min(uh,fh/8);ul=max(ul,fl/8-eh/16)
        fl=max(fl,8*ul);fh=min(fh,8*uh+eh/2)
        el=max(el,2*max(0,fl-8*uh),8*((1-uh)**2+wl))
        wh=min(wh,(fh/8)**2-ul**2,eh/8-(1-uh)**2)
        x=[a,b,el,eh,fl,fh,ul,uh,wl,wh]
        require(all(x[i]>=before[i] and x[i+1]<=before[i+1] for i in range(0,10,2)),
                'every necessary intersection encloses')
        steps.append(x[:])
        require(all(x[i]<=x[i+1] for i in range(0,10,2)), 'empty necessary box')
    a,b,el,eh,fl,fh,ul,uh,wl,wh=x;m=1/(1+b)
    require(fl>7*m+1, 'radius upper bound monotonic domain')
    tl=max(F(0),el-2*fh+16*ul,(8-fh)**2/8)
    th=min(eh-2*max(F(0),fl-8*uh),(fh-7*m-1)**2+7*(m-1)**2)
    require(0<=tl<=th, 'whole necessary T interval')
    return x,tl,th,steps


def origin(x,tl,th,c,damage):
    a,b,el,eh,fl,fh,u,U,w,W=x
    sm=min(F(1),U*U+W,(fh/8)**2);sb=min(sm,u*u+W)
    se=eh-8*((1-U)**2+w);sj=th+2*fh-8-8*(u*u+w);S=min(se,sj)
    require(0<=S and u*u<=sb<=sm<=1 and sb>0, 'actual norm versus beta domain')
    anchor=min(a,2*u/sb-b);beta=[F(1),-2*anchor*u,anchor*anchor*sb]
    beta1=sum(beta);gap=2*u-(anchor+b)*sb
    require(F(73,120)<=anchor<=a<=b<=F(2,3) and gap>=0 and u>anchor*sb and
            0<beta1<1 and 1-anchor*u>0, 'closed convex endpoint anchor')
    Q=[F(1),-anchor*u,anchor*anchor*(sb-u*u)/(2*(1-anchor*u))]
    qb=[Q[0],Q[0]+Q[1]/2,sum(Q)]
    betab=[F(1),1-anchor*u,beta1]
    ds,db,dS=ceiling(sm,4096),ceiling(beta1,4096),ceiling(S,4096)
    require(1-db*beta1**4>0, 'positive diagonal numerator')
    actual_den=ceiling(sb,4096) if damage=='beta-as-norm' else ds
    diagonal=(1-db*beta1**4)/(b*actual_den);R=F(0);vectors=[]
    for k in range(2,9):
        h=power(beta,(8-k)//2) if k%2==0 else mul(power(beta,(7-k)//2),Q)
        hb=bpower(betab,(8-k)//2) if k%2==0 else bproduct(bpower(betab,(7-k)//2),qb)
        hp=pad([F(0)]*k+h,10);hp2=pad(btopower(bproduct(kernel_bernstein([(k,0,F(1))],k),hb)),10)
        require(hp==hp2, 'entire centered monomial/Bernstein polynomial')
        integ=integrate(hp);bi=bintegrate(bproduct(kernel_bernstein([(k,0,F(1))],k),hb))
        require(integ==bi and integ>=0, 'whole centered integral and sign')
        amplitude=9*b**k*c[k]*S**(k//2)*dS**(k%2)
        if damage=='lost-eighth' and k==8:amplitude=F(0)
        R+=amplitude*integ;vectors.append(hp)
    return {'anchor':anchor,'anchor_gap':gap,'beta':beta,'beta1':beta1,'beta_s':sb,'smax':sm,
            'energyS':se,'jointS':sj,'Smax':S,'odd_root':Q,'dmean':ds,'dbeta':db,'dS':dS,
            'D':diagonal,'R':R,'score':diagonal-R,'vectors':vectors}


def kernels(a,b,tl,th,fh,P):
    bm=1-b*b;bp=1-a*a;c=a+1-a*a-b;star=min(a*(1-a*a),b*(1-b*b))
    delta=floorroot(tl/56,1024);sqrtcap=ceiling(7*th/8,256);radius=fh-7/(1+b)-1
    D=min(sqrtcap,radius);MB=b+c;MC=b+bp*(1+D);alpha=c/MB;nu=bp*(1+D)/MC
    require(D>=0 and c-bm*delta>0 and 0<=alpha<1 and 0<=nu<1 and P>=0,
            'whole reciprocal/radial domain')
    g2=[(1,n,F(n+1)*nu**n/MC**2)for n in range(5)]
    g1=[(1,n,alpha**n/MB)for n in range(5)]
    return bm,bp,c,star,delta,D,sqrtcap,radius,g2,g1


def standard(a,b,tl,th,fh,P,damage):
    bm,bp,c,star,d,D,sqrtcap,radius,g2,g1=kernels(a,b,tl,th,fh,P)
    terms=[(r,s,v*star*P)for r,s,v in g2]+[(r,s,v*F(3,4)*bm*(8-fh))for r,s,v in g1]
    if damage=='reciprocal-terminal':terms=[x for x in terms if x[1]<4]
    Kb=kernel_bernstein(terms,5);K=btopower(Kb)
    radial=mul([b,c+7*bm*d],power([b,c-bm*d],7))
    rb=bproduct([b,b+c+7*bm*d],bpower([b,b+c-bm*d],7))
    correction=add(add([F(1)],scale(K,-1)),scale(mul(K,K),F(1,2)))
    cb=add(add([F(1)]*11,scale(elevate(Kb,10),-1)),scale(bproduct(Kb,Kb),F(1,2)))
    full=pad(mul(radial,correction),18);fullb=bproduct(rb,cb)
    require(full==btopower(fullb) and integrate(full)==bintegrate(fullb),
            'entire standard polar coefficients and independent integral')
    return {'a':[a,b],'T':[tl,th],'F_upper':fh,'phase_lower':P,'delta':d,
            'max_e_upper':D,'sqrt_e_upper':sqrtcap,'radius_e_upper':radius,
            'vector':full,'integral':integrate(full)}


def matrixmul(a,b):
    z={}
    for (i,j),x in a.items():
        for (k,l),y in b.items():z[i+k,j+l]=z.get((i+k,j+l),F(0))+x*y
    return {ij:x for ij,x in z.items()if x}


def coupled(a,b,tl,th,fh,el,damage):
    bm,bp,c,star,d,D,sqrtcap,radius,g2,g1=kernels(a,b,tl,th,fh,F(0))
    dl=floorroot(tl/56,4096);dh=ceiling(th/56,4096)
    phase=el/2-28*dh*dh
    require(phase>=0 and c-bm*dh>0, 'coupled phase/radial domain')
    k0terms=[(r,s,v*star*el/2)for r,s,v in g2]+[(r,s,v*F(3,4)*bm*(8-fh))for r,s,v in g1]
    k2terms=[(r,s,-28*star*v)for r,s,v in g2]
    k0b=kernel_bernstein(k0terms,5);k2b=kernel_bernstein(k2terms,5)
    k0=btopower(k0b);k2=btopower(k2b)
    if damage=='lost-phase-coupling':k2=scale(k2,F(0));k2b=scale(k2b,F(0))
    K={(0,i):v for i,v in enumerate(k0)if v};K.update({(2,i):v for i,v in enumerate(k2)if v})
    cor={(0,0):F(1)}
    for ij,v in K.items():cor[ij]=cor.get(ij,F(0))-v
    for ij,v in matrixmul(K,K).items():cor[ij]=cor.get(ij,F(0))+v/2
    rm={(0,0):F(1)}
    for s in [7]+[-1]*7:rm=matrixmul(rm,{(0,0):b,(0,1):c,(1,1):s*bm})
    prod=matrixmul(rm,cor);vectors=[[prod.get((i,j),F(0))for j in range(19)]for i in range(13)]
    require(all(i<=12 and j<=18 for i,j in prod), 'full bivariate degree')
    # Second route: separated d orders, Bernstein t products and beta integrals.
    c0=add(add([F(1)]*11,scale(elevate(k0b,10),-1)),scale(bproduct(k0b,k0b),F(1,2)))
    c2=add(scale(elevate(k2b,10),-1),bproduct(k0b,k2b));c4=scale(bproduct(k2b,k2b),F(1,2))
    separated=[[F(0)]*19 for _ in range(13)]
    h=[F(comb(7,i)*(-1)**i+(7*comb(7,i-1)*(-1)**(i-1)if i else 0))if i<=7 else F(-7)for i in range(9)]
    require(h==list(map(F,[1,0,-28,112,-210,224,-140,48,-7])), 'whole radial expansion')
    for i in range(9):
        ri=bproduct(kernel_bernstein([(i,0,h[i]*bm**i)],i),bpower([b,b+c],8-i))
        for k,ck in [(0,c0),(2,c2),(4,c4)]:separated[i+k]=add(separated[i+k],bproduct(ri,ck))
    require(vectors==[btopower(row)for row in separated], 'whole13x19 monomial versus Bernstein matrix')
    ints=[integrate(row)for row in vectors];require(ints==[bintegrate(row)for row in separated], 'whole13 beta integrals')
    translated=[sum((ints[j]*comb(j,k)*dl**(j-k)*(dh-dl)**k for j in range(k,13)),F(0))for k in range(13)]
    separate=[F(0)]*13
    for j,g in enumerate(ints):separate=add(separate,pad(scale(power([dl,dh-dl],j),g),12))
    require(translated==separate, 'whole d translation')
    controls=[sum((translated[k]*F(comb(i,k),comb(12,k))for k in range(i+1)),F(0))for i in range(13)]
    require(btopower(controls)==translated, 'entire closed Bernstein reconstruction')
    return {'D':D,'delta_interval':[dl,dh],'phase_minimum':phase,'matrix':vectors,'integral_vector':ints,
            'translated_vector':translated,'Bernstein_vector':controls,'integral_upper':max(controls)}


def mpower(a,n):
    z={(0,0):F(1)}
    for _ in range(n):z=matrixmul(z,a)
    return z


def tbmul(a,b):
    """Second representation: u powers carrying complete t Bernstein vectors."""
    degree=len(next(iter(a.values())))+len(next(iter(b.values())))-2
    z={}
    for i,x in a.items():
        for j,y in b.items():z[i+j]=add(z.get(i+j,[F(0)]*(degree+1)),bproduct(x,y))
    return {i:row for i,row in z.items()if any(row)}


def tbpower(a,n):
    z={0:[F(1)]}
    for _ in range(n):z=tbmul(z,a)
    return z


def bernstein_interval(p,lo,hi,degree):
    require(lo<=hi,'closed Bernstein interval')
    p=pad(p,degree);n=degree
    translated=[sum((p[j]*comb(j,k)*lo**(j-k)*(hi-lo)**k for j in range(k,n+1)),F(0))for k in range(n+1)]
    separate=[F(0)]*(n+1)
    for j,v in enumerate(p):separate=add(separate,pad(scale(power([lo,hi-lo],j),v),n))
    require(translated==separate,'all translated coefficients')
    controls=[sum((translated[k]*F(comb(i,k),comb(n,k))for k in range(i+1)),F(0))for i in range(n+1)]
    require(btopower(controls)==translated,'all reconstructed interval controls')
    return translated,controls


def retained_mean(x,tl,th,c,energy,damage):
    a,b,el,eh,fl,fh,L,U,Wl,Wh=x
    require(0<L<=U<=1 and 0<=Wl<=Wh,'actual mean domain')
    anchor=min(a,2*L/(L*L+Wh)-b,2*U/(U*U+Wh)-b)
    gaps=[2*v-(anchor+b)*(v*v+Wh)for v in [L,U]]
    require(0<anchor<=a<=b<=F(2,3)and min(gaps)>=0 and 1-anchor*U>0,
            'both retained-mean convex anchor endpoints')
    beta={(0,0):F(1),(1,1):-2*anchor,(2,2):anchor*anchor,(0,2):anchor*anchor*Wh}
    Q={(0,0):F(1),(1,1):-anchor,(0,2):anchor*anchor*Wh/(2*(1-anchor*U))}
    betab={0:[F(1),F(1),1+anchor*anchor*Wh],1:[F(0),-anchor,-2*anchor],2:[F(0),F(0),anchor*anchor]}
    Qb={0:[F(1),F(1),1+Q[0,2]],1:[F(0),-anchor/2,-anchor]}
    S=[eh-8*(1+Wl),F(16),F(-8)]if energy=='energy'else[th+2*fh-8-8*Wl,F(0),F(-8)]
    def ev(p,v):return sum((p[i]*v**i for i in range(len(p))),F(0))
    sLo,sHi=ev(S,L),ev(S,U);require(min(sLo,sHi)>=0,'whole chosen polynomial energy nonnegative')
    require((sHi>=sLo if energy=='energy'else sLo>=sHi),'chosen energy direction')
    Sm=max(sLo,sHi);dS=ceiling(Sm,4096)
    sm=min(F(1),U*U+Wh,(fh/8)**2);dm=ceiling(sm,4096)
    beta_one=[1+anchor*anchor*Wh,-2*anchor,anchor*anchor]
    betaL=ev(beta_one,L);db=ceiling(betaL,4096)
    require(0<betaL<1 and 1-db*betaL**4>0,'whole retained-mean positive diagonal numerator')
    N=pad(add([F(1)],scale(power(beta_one,4),-db)),8)
    matrices=[];integrals=[];R=[F(0)]*9;Rb={};complete={}
    for k in range(2,9):
        H=mpower(beta,(8-k)//2)if k%2==0 else matrixmul(mpower(beta,(7-k)//2),Q)
        H=matrixmul(H,{(i,0):v for i,v in enumerate(power(S,k//2))if v})
        H={(i,j+k):v for (i,j),v in H.items()}
        Hb=tbpower(betab,(8-k)//2)if k%2==0 else tbmul(tbpower(betab,(7-k)//2),Qb)
        sp=power(S,k//2);second={}
        for i,row in Hb.items():
            for j,v in enumerate(sp):
                second[i+j]=add(second.get(i+j,[F(0)]*len(row)),scale(row,v))
        second={i:elevate(bproduct(row,kernel_bernstein([(k,0,F(1))],k)),9)for i,row in second.items()}
        first=[[H.get((i,j),F(0))for j in range(10)]for i in range(9)]
        alternate=[btopower(second.get(i,[F(0)]*10))for i in range(9)]
        require(all(i<=8 and j<=9 for i,j in H)and first==alternate,'all retained-mean9x10 entries')
        ints=[integrate(row)for row in first];alt=[bintegrate(second.get(i,[F(0)]*10))for i in range(9)]
        require(ints==alt,'all retained-mean integrated u coefficients')
        amp=9*b**k*c[k]*dS**(k%2)
        if damage=='mean-lost-eighth'and k==8:amp=F(0)
        R=add(R,scale(ints,amp))
        for ij,v in H.items():complete[ij]=complete.get(ij,F(0))+amp*v
        for i,row in second.items():Rb[i]=add(Rb.get(i,[F(0)]*10),scale(row,amp))
        matrices.append(first);integrals.append(ints)
    diagonal=scale(N,1/(b*dm));degree8=add(diagonal,scale(R,-1))
    translate8,controls8=bernstein_interval(degree8,L,U,8)
    d=[b*Wh/(2*L),b]
    if damage=='mean-wrong-denominator':d=[b*Wh/(2*U),b]
    dL,dU=ev(d,L),ev(d,U);require(0<dL<=dU,'positive actual linear norm denominator')
    cleared=pad(add(N,scale(mul(d,add([F(1)],R)),-1)),9)
    # Full10x10 cleared remainder in independent t representations.
    product=matrixmul({(i,0):v for i,v in enumerate(d)if v},complete)
    alternate={}
    for i,row in Rb.items():
        for j,v in enumerate(d):alternate[i+j]=add(alternate.get(i+j,[F(0)]*10),scale(row,v))
    matrix=[[product.get((i,j),F(0))for j in range(10)]for i in range(10)]
    second_matrix=[btopower(alternate.get(i,[F(0)]*10))for i in range(10)]
    require(matrix==second_matrix and [integrate(r)for r in matrix]==pad(mul(d,R),9),
            'whole100 actual-denominator remainder entries and integrals')
    translate9,controls9=bernstein_interval(cleared,L,U,9)
    pmin=min(controls9);den=dU if pmin>=0 else dL
    if damage=='mean-wrong-sign-endpoint':den=dU
    score9=1+pmin/den;score=max(min(controls8),score9)
    return {'energy':energy,'anchor':anchor,'anchor_gaps':gaps,'S_polynomial':S,'S_endpoints':[sLo,sHi],
            'dS':dS,'actual_norm_square':sm,'dmean':dm,'dbeta':db,'beta_L':betaL,
            'whole7_matrices':matrices,'whole7_integrals':integrals,
            'numerator':N,'remainder':R,'degree8':degree8,'translation8':translate8,'controls8':controls8,
            'actual_denominator':d,'denominator_endpoints':[dL,dU],
            'cleared_remainder_matrix':matrix,'cleared_degree9':cleared,
            'translation9':translate9,'controls9':controls9,'score8':min(controls8),'score9':score9,'score':score}



def run(path,damage=None):
    raw=json.loads(path.read_text());require(type(raw)is dict and set(raw)=={'root','leaves','splits'}, 'complete cover schema')
    root=[parse_fraction(v)for v in raw['root']];require(root==ROOT, 'whole closed root domain')
    cuts,leaves=raw['splits'],raw['leaves'];require(type(cuts)is dict and type(leaves)is dict and not(set(cuts)&set(leaves)), 'disjoint tree node maps')
    require(all(type(p)is str and set(p)<=set('01')and len(p)<=18 for p in list(cuts)+list(leaves)), 'whole tree path schema')
    require(all(v in ['origin-passes','polar-excluded','energy-polar-excluded','mean-dependent-origin-passes']for v in leaves.values()), 'leaf scope/type')
    if damage=='missing-leaf':del leaves[next(iter(leaves))]
    c,meta=constants();shell=[]
    for k in range(72):
        l=F(k,8);u=min(F(k+1,8),F(224,25));P=max(F(0),(F(23,5)-u)/2)
        row=standard(F(13,20),F(2,3),l,u,F(8),P,damage)
        require(row['integral']<1, 'entire closed energy shell cell');shell.append(row)
    require(shell[0]['T'][0]==0 and shell[-1]['T'][1]==F(224,25)and
            all(shell[i]['T'][1]==shell[i+1]['T'][0]for i in range(71)), 'no energy gap/shared endpoint lost')
    stack=[('',root)];seen=set();records=[];cutrecords=[];statuses={s:0 for s in ['origin-passes','polar-excluded','energy-polar-excluded','mean-dependent-origin-passes']}
    while stack:
        p,box=stack.pop();require(p not in seen, 'duplicate reachable node');seen.add(p)
        x,tl,th,steps=tighten(box)
        if p in cuts:
            entry=cuts[p];require(type(entry)is dict and set(entry)=={'axis','cut'}, 'typed exact cut')
            axis=entry['axis'];require(type(axis)is int and 0<=axis<5, 'cut axis');cut=parse_fraction(entry['cut']);i=2*axis
            require(cut==(x[i]+x[i+1])/2 and box[i]<cut<box[i+1], 'strict tightened midpoint of original full parent')
            left=box[:];right=box[:];left[i+1]=cut;right[i]=cut
            require(left[i+1]==right[i] and left[i]==box[i] and right[i+1]==box[i+1], 'both closed children exhaust original parent')
            stack.extend([(p+'1',right),(p+'0',left)]);cutrecords.append({'path':p,'axis':axis,'cut':cut,'original':box,'tightened':x,'steps':steps})
        else:
            require(p in leaves, 'unvisited/missing branch');status=leaves[p];statuses[status]+=1
            row={'path':p,'status':status,'original':box,'tightened':x,'T':[tl,th],'steps':steps,'origin':origin(x,tl,th,c,damage)}
            if status=='origin-passes':require(row['origin']['score']>OP, 'strict whole origin leaf')
            elif status=='mean-dependent-origin-passes':
                row['mean']=[retained_mean(x,tl,th,c,energy,damage) for energy in ['energy','joint']]
                require(max(r['score'] for r in row['mean'])>OP,'strict retained-mean whole-u leaf')
            else:
                P=max(F(0),(x[2]-th)/2,x[4]-8*x[7]);row['standard']=standard(x[0],x[1],tl,th,x[5],P,damage)
                if status=='polar-excluded':require(row['standard']['integral']<JP, 'strict standard polar leaf')
                else:
                    row['coupled']=coupled(x[0],x[1],tl,th,x[5],x[2],damage)
                    require(row['coupled']['integral_upper']<JP, 'strict whole E/T polar leaf')
            records.append(row)
    require(seen==set(cuts)|set(leaves), 'all listed and reachable nodes exactly agree')
    require((len(seen),len(cuts),len(leaves))==(1029,514,515), 'target complete tree counts')
    require(statuses=={'origin-passes':213,'polar-excluded':57,'energy-polar-excluded':218,'mean-dependent-origin-passes':27}, 'whole claimed leaf accounting')
    Mshell=max(row['integral']for row in shell)
    epsilon=F(1,2**22)
    require(Mshell<1-64*epsilon and meta['mass_integral']<1-64*epsilon,
            'fresh mass and whole energy shell perturbation margins')
    # The actual independently paid cover margins support more than the advertised targets.
    polar_score=max(max(r['standard']['integral'] for r in records if r['status']=='polar-excluded'),
                    max(r['coupled']['integral_upper'] for r in records if r['status']=='energy-polar-excluded'))
    origin_score=min([r['origin']['score'] for r in records if r['status']=='origin-passes']+
                     [max(m['score'] for m in r['mean']) for r in records if r['status']=='mean-dependent-origin-passes'])
    require(1-64*epsilon>polar_score and 1+578*epsilon<origin_score,
            'fresh whole actual polar/origin clipping margins')
    require(F(2,3)+F(231,400)*F(9,7)<2 and 1+F(2,3)*F(9,7)<2 and F(9,8)**8<3,
            'whole seven-factor Lipschitz/AMGM chord domains')
    record={'constants':meta,'energy_shell':shell,'cuts':cutrecords,'leaves':records,
            'annular_gap':{'epsilon':epsilon,'J_Lipschitz':64,'O_Lipschitz':576,'AMGM_chord':2}}
    encoded=json.dumps(encode(record),sort_keys=True,separators=(',',':')).encode()
    op_scores=[r['origin']['score'] for r in records if r['status']=='origin-passes']+[
        max(m['score'] for m in r['mean']) for r in records if r['status']=='mean-dependent-origin-passes']
    summary={'agent':'six-reviewer-1','role':'independent mathematical reviewer','nodes':len(seen),
             'cuts':len(cuts),'leaves':len(leaves),'statuses':statuses,'energy_cells':len(shell),
             'whole_centered_vectors':7*len(leaves),'whole_standard_vectors':72+275,
             'whole_coupled13x19_matrices':218,'whole_mean9x10_matrices':54*7,
             'whole_mean_degree8_controls':54*9,'whole_mean_degree9_controls':54*10,
             'least_defining_origin_score':min(op_scores),
             'worst_standard_success':max(r['standard']['integral']for r in records if r['status']=='polar-excluded'),
             'worst_coupled_success':max(r['coupled']['integral_upper']for r in records if r['status']=='energy-polar-excluded'),
             'max_energy_shell':Mshell,'mass_integral':meta['mass_integral'],
             'explicit_new_annular_gap':epsilon,'complete_record_bytes':len(encoded),
             'complete_record_sha256':hashlib.sha256(encoded).hexdigest()}
    return summary,encoded


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--cover',type=Path,default=Path(__file__).with_name('COVER.json'));parser.add_argument('--record',type=Path);parser.add_argument('--damage');parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('EXPECTED.json'));args=parser.parse_args()
    summary,record=run(args.cover,args.damage)
    require(encode(summary)==json.loads(args.expected.read_text()), 'entire independent summary and whole coefficient-record seal')
    if args.record:args.record.write_bytes(record)
    print(json.dumps(encode(summary),sort_keys=True,indent=2))
