"""Complete centered affine face and invariant blocks for Kr join K_(u,v).

Integers r>=3,2<=u<=v. These formulas alone make no PSD/cap assertion.
THREE_CENTER_BIPARTITE.md proves the production r=3 parameters separately.
"""
from fractions import Fraction as F
from itertools import combinations,product
from maxrank_mixtures import integer_at_least


def scope(r,u,v,shift=0):
    integer_at_least(r,3,'r');integer_at_least(u,2,'u')
    integer_at_least(v,u,'v');integer_at_least(shift,0,'shift')


def family(r,u,v,shift=0):
    scope(r,u,v,shift);h=u+v;A=[1 << (h+i) for i in range(r)]
    members=[0]+A+[a|b for a,b in combinations(A,2)]+[1 << i for i in range(h)]
    members += [a|(1 << i) for a in A for i in range(h)]
    members += [(1 << i)|(1 << (u+j)) for i,j in product(range(u),range(v))]
    return sorted(x << shift for x in members)


def centered_face(r,u,v,jL=0,jR=0,eta=0,kL=0,kR=0,kT=0,aL=0,aR=0,tL=0,tR=0,bL=0,bR=0,bT=0,qL=0,qR=0):
    scope(r,u,v)
    raw=(jL,jR,eta,kL,kR,kT,aL,aR,tL,tR,bL,bR,bT,qL,qR)
    if any(not isinstance(x,(int,F)) or isinstance(x,bool) for x in raw):
        raise ValueError('Exact rational coordinates required')
    jL,jR,eta,kL,kR,kT,aL,aR,tL,tR,bL,bR,bT,qL,qR=map(F,raw)
    if r==3 and eta:raise ValueError('No disjoint center-edge orbit at r=3')
    e=r*(r-1)//2;f=(r-1)*(r-2)//2
    qAF=2-(r-3)*eta-u*jL-v*jR
    pL=2-(r-2)*jL-(u-1)*kL-v*kT;pR=2-(r-2)*jR-(v-1)*kR-u*kT
    bA=1-(r-2)*qAF-u*pL-v*pR
    qA=-(r-1-f*qAF+u*qL+v*qR)/F(u*v)
    rL=(1-(u-1)*aL-v*tL-qL)/F(r-1);rR=(1-(v-1)*aR-u*tR-qR)/F(r-1)
    wL=(v-(r-2)+f*jL-(u-1)*aL-v*tR)/F(v*(u-1))
    wR=(u-(r-2)+f*jR-(v-1)*aR-u*tL)/F(u*(v-1))
    qF=(2-(u-1)*wL-(v-1)*wR-qA)/F(r-1)
    cL=-(u+r-1-e*rL+(u-1)*bL+v*bT)/F(v*(u-1))
    cR=-(v+r-1-e*rR+(v-1)*bR+u*bT)/F(u*(v-1))
    z=(e*qF-(r-1)-(u-1)*cL-(v-1)*cR)/F((u-1)*(v-1))
    return dict(jL=jL,jR=jR,eta=eta,kL=kL,kR=kR,kT=kT,aL=aL,aR=aR,tL=tL,tR=tR,
                bL=bL,bR=bR,bT=bT,qL=qL,qR=qR,qAF=qAF,pL=pL,pR=pR,bA=bA,qA=qA,
                rL=rL,rR=rR,wL=wL,wR=wR,qF=qF,cL=cL,cR=cR,z=z)


def validate_weights(r,u,v,w):
    scope(r,u,v)
    if not isinstance(w,dict) or set(w)!=set(centered_face(r,u,v)) or any(
            not isinstance(x,(int,F)) or isinstance(x,bool) for x in w.values()):
        raise ValueError('Invalid exact weights')
    free=('jL','jR','eta','kL','kR','kT','aL','aR','tL','tR','bL','bR','bT','qL','qR')
    if w!=centered_face(r,u,v,**{k:w[k] for k in free}):
        raise ValueError('Weights do not lie on the centered affine face')


def core(r,u,v,w):
    validate_weights(r,u,v,w)
    h=u+v;centers=((1 << r)-1) << h;left=(1 << u)-1;D=family(r,u,v)[1:]
    def kind(x):
        if x.bit_count()==1:return 'A' if x & centers else 'C'
        return 'F' if x & centers==x else 'P' if x & centers else 'E'
    def part(x):return 'L' if x & left else 'R'
    answer=[]
    for x in D:
        row=[]
        for y in D:
            a,b=kind(x),kind(y);types=''.join(sorted((a,b)))
            if x==y:z=F(h+r-1)
            elif x & y:z=F(-1)
            elif types=='AF':z=w['qAF']
            elif types=='FF':z=w['eta']
            elif types=='FP':z=w['j'+part(x if a=='P' else y)]
            elif types=='AA':z=w['bA']
            elif types=='AC':z=w['q'+part(y if a=='A' else x)]
            elif types=='AP':z=w['p'+part(y if a=='A' else x)]
            elif types=='AE':z=w['qA']
            elif types=='CF':z=w['r'+part(x if a=='C' else y)]
            elif types=='EF':z=w['qF']
            elif types=='CC':z=w['b'+part(x)] if part(x)==part(y) else w['bT']
            elif types=='CP':
                c=x if a=='C' else y;p=y if a=='C' else x
                z=w[('a' if part(c)==part(p) else 't')+part(c)]
            elif types=='CE':z=w['c'+part(x if a=='C' else y)]
            elif types=='PP':z=w['k'+part(x)] if part(x)==part(y) else w['kT']
            elif types=='EP':z=w['w'+part(x if a=='P' else y)]
            elif types=='EE':z=w['z']
            else:raise ValueError('Missing disjoint orbit '+types)
            row.append(F(z))
        answer.append(row)
    return answer


def _congruence(T,M):
    return [[sum(F(T[i][a])*M[a][b]*T[j][b] for a in range(len(M)) for b in range(len(M)))
             for j in range(len(T))] for i in range(len(T))]


def blocks(r,u,v,w):
    validate_weights(r,u,v,w)
    h=u+v;d=h+r-1;e=r*(r-1)//2;f=(r-1)*(r-2)//2;g=(r-2)*(r-3)//2
    def leaf(q,side):
        return [[r*(h+1-(r-1)*w['k'+side]),-r*(1+w['a'+side]),-r*q*(1+w['w'+side])],
                [-r*(1+w['a'+side]),d-w['b'+side],-q*(1+w['c'+side])],
                [-r*q*(1+w['w'+side]),-q*(1+w['c'+side]),q*(h+r+1+w['z']-(1+w['z'])*q)]]
    Kstd=[[d-w['bA'],-(r-2)*(1+w['qAF']),-u*(1+w['pL'])],
          [-(r-2)*(1+w['qAF']),(r-2)*(h+3-(r-3)*w['eta']),-(r-2)*u*(1+w['jL'])],
          [-u*(1+w['pL']),-(r-2)*u*(1+w['jL']),u*(h+r+1-u-(u-1)*w['kL'])]]
    Fs=[[1,0,0],[0,1,0],[0,0,1],[-1,-1,-1]]
    K=[[r*(d+(r-1)*w['bA']),r*(-(r-1)+f*w['qAF']),r*u*(-1+(r-1)*w['pL']),r*u*w['qL'],r*v*w['qR']],
       [r*(-(r-1)+f*w['qAF']),e*(h-r+3+g*w['eta']),e*u*(-2+(r-2)*w['jL']),e*u*w['rL'],e*v*w['rR']],
       [r*u*(-1+(r-1)*w['pL']),e*u*(-2+(r-2)*w['jL']),r*u*(h+1-u+(r-1)*(u-1)*w['kL']),r*u*(-1+(u-1)*w['aL']),r*u*v*w['tR']],
       [r*u*w['qL'],e*u*w['rL'],r*u*(-1+(u-1)*w['aL']),u*(d+(u-1)*w['bL']),u*v*w['bT']],
       [r*v*w['qR'],e*v*w['rR'],r*u*v*w['tR'],u*v*w['bT'],v*(d+(v-1)*w['bR'])]]
    Fc=[[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[-1,-2,-1,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,1,0,-1,-1]]
    return dict(left=leaf(v,'L'),right=leaf(u,'R'),center_active=Kstd,center=_congruence(Fs,Kstd),
                constant_active=K,constant=_congruence(Fc,K),
                constant_norms=list(map(F,(r,e,r*u,r*v,u,v,u*v))),center_norms=list(map(F,(1,r-2,u,v))),
                scalars=list(map(F,(h+r+1+w['kL'],h+r+1+w['kR'],h+r+1+w['z'],h+r+1+w['eta']))))
