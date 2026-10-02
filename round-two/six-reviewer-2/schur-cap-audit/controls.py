"""Literal full harmonic action controls and semantic corruptions; no author inputs."""
from fractions import Fraction as F
from itertools import combinations,permutations
from affine import matrices,table,family,parameters
from sectors import choose,full_sectors
from linear import need,mv,psd,digest

def rref(A):
    B=[list(map(F,row))for row in A];r=0;piv=[]
    for j in range(len(B[0])):
        p=next((i for i in range(r,len(B))if B[i][j]),None)
        if p is None:continue
        B[r],B[p]=B[p],B[r];z=B[r][j];B[r]=[x/z for x in B[r]]
        for i in range(len(B)):
            if i==r:continue
            z=B[i][j];B[i]=[x-z*y for x,y in zip(B[i],B[r])]
        piv.append(j);r+=1
    return B,piv

def literal_harmonics(kap):
    q=4;S,Z,C,D,R,U=matrices(q,0);C=[[a+kap*b for a,b in zip(row,rr)]for row,rr in zip(C,D)]
    non=S[1:];types=[(0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(3,0)];Q=table(q,kap);s=3*q+4
    corehs=[[1,-1,0],[0,1,-1]];ouths=[[int(i==j)-int(i==q-1)for i in range(q)]for j in range(q-1)]
    edges=list(combinations(range(q),2));incidence=[[int(i in edge)for edge in edges]for i in range(q)]
    red,piv=rref(incidence);edgehs=[]
    for j in range(len(edges)):
        if j in piv:continue
        v=[F(i==j)for i in range(len(edges))]
        for i,p in enumerate(piv):v[p]=-red[i][j]
        need(not any(mv(incidence,v)),'actual outside edge harmonic');edgehs.append(v)
    allcols=[];actions=0
    for j,l in [(0,0),(1,0),(0,1),(1,1),(0,2)]:
        kept=[t for t in types if j<=t[0]<=3-j and l<=t[1]<=q-l]
        weights=[choose(3-2*j,a-j)*choose(q-2*l,b-l)for a,b in kept]
        operator=[]
        for i,(a,b)in enumerate(kept):
            row=[]
            for m,(c,d)in enumerate(kept):
                z=F(s*(i==m))+Q.get(tuple(sorted(((a,b),(c,d)))),F(0))*((-1)**(j+l))*choose(3-a-j,c-j)*choose(q-b-l,d-l)
                if j==l==0:z-=weights[m]
                row.append(z)
            operator.append(row)
        for ch in [None]if j==0 else corehs:
            for oh in [None]if l==0 else(ouths if l==1 else edgehs):
                cols=[]
                for wanted in kept:
                    col=[]
                    for A in non:
                        typ=((A&7).bit_count(),(A&~7).bit_count())
                        if typ!=wanted:col.append(F(0));continue
                        cv=1 if ch is None else sum(ch[i]for i in range(3)if A>>i&1)
                        outside=tuple(i for i in range(q)if A>>(i+3)&1)
                        ov=1 if oh is None else(sum(oh[i]for i in outside)if l==1 else oh[edges.index(outside)])
                        col.append(F(cv*ov))
                    cols.append(col)
                for m,col in enumerate(cols):
                    image=[sum(operator[i][m]*cols[i][a]for i in range(len(cols)))for a in range(len(non))]
                    need(mv(C,col)==image,'every full original harmonic eigenaction');actions+=1
                allcols+=cols
    transposed=[[col[i]for col in allcols]for i in range(len(non))];_,piv=rref(transposed)
    need(len(allcols)==len(piv)==41,'full literal harmonic spanning census')
    return {'q':4,'kappa':kap,'original_vectors':len(allcols),'all_original_action_positions':actions*41,'basis_sha256':digest(allcols),'whole_core_sha256':digest(C)}

def controls():
    records=[literal_harmonics(F(0)),literal_harmonics(F(1,1024))];rejections=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,ZeroDivisionError):rejections.append(name);return
        raise ValueError('damage accepted '+name)
    reject('q3',lambda:family(3,1));reject('q24-literal-guard',lambda:family(24,5));reject('k-too-large',lambda:family(5,6))
    reject('float-table',lambda:table(4,0.125));reject('zero-table-denominator-domain',lambda:table(3,0))
    reject('negative-PSD-diagonal',lambda:psd([[1,0],[0,-1]]));reject('zero-diagonal-nonzero-row',lambda:psd([[0,1],[1,0]]))
    reject('nonsymmetric-PSD',lambda:psd([[1,0],[1,1]]))
    S,Z,C,D,R,U=matrices(4,2);p=parameters(4,2);transports=0
    for permutation in permutations(range(3,7)):
        def transport(A):return (A&7)|sum(1<<permutation[i]for i in range(4)if A>>(i+3)&1)
        moved=[transport(A)for A in S];movedZ=transport(Z)
        membership=[A for A in range(1<<7)if A.bit_count()<=2 or(A.bit_count()==3 and(A&7).bit_count()>=2 and not(A&7==6 and A&movedZ))]
        need(sorted(moved)==membership,'every original transported deletion domain')
        Q=table(4,0)
        for i,A in enumerate(moved[1:]):
            for j,B in enumerate(moved[1:]):
                ta=((A&7).bit_count(),(A&~7).bit_count());tb=((B&7).bit_count(),(B&~7).bit_count())
                value=F(15)if i==j else(F(-1)if A&B else Q[tuple(sorted((ta,tb)))]-1)
                need(C[i][j]==value,'all transported original core entries')
        transports+=1
    from audit import vectors
    one,y,yz,yw,extra,sa,z=vectors(S,Z)
    v=mv(C,z);need(not any(v),'positive lower action control')
    C[0][0]+=1;reject('damaged-zero-lower-action',lambda:need(not any(mv(C,z)),'corrupt lower action'))
    U[0][0]+=1
    from affine import quad
    reject('damaged-mean-action',lambda:need(quad(U,one)==p['e'],'corrupt upper mean'))
    zero=full_sectors(4,F(0));positive=full_sectors(4,F(1,1024))
    reject('wrong-finite-nullity',lambda:need(positive['nullity']==5,'lost positive parameter direction'))
    reject('negative-norm-metric',lambda:psd([[-1]]))
    need(len(rejections)==12,'all semantic controls executed')
    return {'literal_harmonics':records,'full_action_positions':sum(r['all_original_action_positions']for r in records),'finite_q4_sector_records':[zero,positive],'point_transports':transports,'transported_core_positions':transports*(len(S)-1)**2,'semantic_rejections':rejections,'trust':'literal full spanning and original-entry actions, not only a reduced formula comparison'}
