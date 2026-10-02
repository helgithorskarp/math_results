"""Independent whole integer Sylvester determinant, rational unit and ranks."""
from fractions import Fraction as F
from math import gcd, lcm
from polys import Poly, cast, symbol, need

def trim(a):
    a=list(a)
    while a and a[-1]==0:a.pop()
    return a
def add(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def scale(a,s):return trim([x*s for x in a])
def mul(a,b):
    out=[F(0)]*max(0,len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return trim(out)
def divrem(a,b):
    a=trim(a);b=trim(b);need(bool(b),'nonzero Euclidean divisor');q=[F(0)]*max(0,len(a)-len(b)+1)
    while a and len(a)>=len(b):
        k=len(a)-len(b);c=a[-1]/b[-1];q[k]+=c
        for j,x in enumerate(b):a[k+j]-=c*x
        a=trim(a)
    return trim(q),a
def primitive(poly):
    a=[]
    for key,value in poly.terms.items():
        need(value[1]==0 and all(name=='r' for name,_ in key),'univariate real r primitive')
        k=dict(key).get('r',0)
        while len(a)<=k:a.append(F(0))
        a[k]=value[0]
    a=trim(a);need(bool(a),'nonzero primitive');den=lcm(*(x.denominator for x in a));ints=[int(x*den) for x in a]
    content=gcd(*ints);content=content if ints[-1]>0 else -content
    return [v//content for v in ints]
def egcd(a,b):
    aa=[F(x) for x in a];bb=[F(x) for x in b]
    u,v,uu,vv=[F(1)],[],[],[F(1)]
    while bb:
        q,r=divrem(aa,bb);aa,bb=bb,r
        u,uu=uu,add(u,scale(mul(q,uu),-1));v,vv=vv,add(v,scale(mul(q,vv),-1))
    need(len(aa)==1,'coprime rational pair')
    return scale(u,1/aa[0]),scale(v,1/aa[0])
def bareiss(matrix):
    a=[list(row) for row in matrix];n=len(a);last=1;sign=1;pivots=[]
    for k in range(n-1):
        i=next((i for i in range(k,n) if a[i][k]),None)
        if i is None:return 0,pivots
        if i!=k:a[i],a[k]=a[k],a[i];sign=-sign
        pivot=a[k][k];pivots.append(pivot)
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=a[i][j]*pivot-a[i][k]*a[k][j]
                need(numerator%last==0,'whole exact Bareiss division')
                a[i][j]=numerator//last
            a[i][k]=0
        last=pivot
    return sign*a[-1][-1],pivots
def rank(matrix):
    a=[[F(x) for x in row] for row in matrix];r=0
    for j in range(3):
        i=next((i for i in range(r,len(a)) if a[i][j]),None)
        if i is None:continue
        a[r],a[i]=a[i],a[r];pivot=a[r][j];a[r]=[v/pivot for v in a[r]]
        for i in range(len(a)):
            if i!=r:
                z=a[i][j];a[i]=[x-z*y for x,y in zip(a[i],a[r])]
        r+=1
    return r
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def classify(matrix):
    n=rank(matrix)
    if n==3:return n,False,None
    if n==0:return n,True,'every positive t; feasibility retained'
    rows=[[F(x) for x in row] for row in matrix]
    if n==2:
        c=next(cross(a,b) for a in rows for b in rows if any(cross(a,b)))
        X,Y,Z=c
        if Z==0 or X*Z!=Y*Y or Y/Z<=0:return n,False,None
        t=Y/Z;need(all(a*t*t+b*t+c==0 for a,b,c in rows),'all five full rows at positive conic root')
        return n,True,str(t)
    a,b,c=next(row for row in rows if any(row))
    if a==0:return n,b!=0 and -c/b>0,None
    if a<0:a,b,c=-a,-b,-c
    return n,b*b-4*a*c>=0 and (b<0 or c<0),None

def audit_slices(slices):
    P=primitive(slices[1].coefficient('t',1))
    A2,B2=slices[0].coefficient('t',2),slices[0].coefficient('t',0)
    A0,B0=slices[2].coefficient('t',2),slices[2].coefficient('t',0)
    S=primitive(A2*B0-A0*B2)
    need(P==[157599,1459368,4606896,4934272],'whole stated cubic from actual residual')
    need(S==[22016043,343903887,2215220832,7523113824,14186807040,14058198784,5704007680],'whole stated eliminant from undivided cross product')
    m,n=len(P)-1,len(S)-1;matrix=[]
    for i in range(n):matrix.append([0]*i+list(reversed(P))+[0]*(n-1-i))
    for i in range(m):matrix.append([0]*i+list(reversed(S))+[0]*(m-1-i))
    determinant,pivots=bareiss(matrix);need(determinant!=0,'nonzero exact integer Sylvester determinant')
    U,V=egcd(P,S);unit=add(mul(U,[F(x) for x in P]),mul(V,[F(x) for x in S]));need(unit==[1],'entire rational unit')
    # The visible finite-field proof is checked from regenerated P,S too.
    up=[5,8,12,7,0,8];vp=[4,0,11]
    modunit=[int(c)%13 for c in add(mul(up,P),mul(vp,S))]
    while modunit and modunit[-1]==0:modunit.pop()
    need(modunit==[1] and P[-1]%13 and S[-1]%13,'entire visible mod13 unit and preserved degrees')
    damages={}
    bad=U[:];bad[0]+=1
    damaged_unit=add(mul(bad,[F(x) for x in P]),mul(V,[F(x) for x in S]))
    need(damaged_unit!=[1],'wrong rational unit rejected');damages['rational_unit_coefficient']=list(map(str,damaged_unit))
    need(bareiss([row[:] for row in matrix[:8]]+[matrix[0][:]])[0]==0,'duplicate Sylvester row rejected');damages['lost_sylvester_row']='determinant zero'
    return {'whole_P':P,'whole_S':S,'whole_cross_eliminant':(A2*B0-A0*B2).record(),
            'whole_integer_sylvester':matrix,'integer_resultant':str(determinant),'whole_bareiss_pivots':list(map(str,pivots)),
            'whole_rational_U':list(map(str,U)),'whole_rational_V':list(map(str,V)),
            'whole_rational_unit':list(map(str,unit)),'whole_mod13_unit':modunit,'damage_rejections':damages}

def rank_controls():
    cases=[]
    def take(name,rows,expected):
        answer=classify(rows);need(answer[:2]==expected,name);cases.append({'name':name,'matrix':rows,'rank':answer[0],'positive_scalar_root':answer[1],'root':answer[2]})
    zero=[[0,0,0]]*5
    take('whole rank zero',zero,(0,True))
    take('rank three despite first two positive-compatible rows',[[1,-2,0],[0,1,-2],[0,0,1],[2,1,3],[0,0,0]],(3,False))
    for name,point,ok in [('positive finite',[4,2,1],True),('negative finite',[9,-3,1],False),('nonconic',[3,1,1],False),('infinity',[1,0,0],False),('zero only',[0,0,1],False)]:
        X,Y,Z=point
        if Z:a=[Z,0,-X];b=[0,Z,-Y]
        elif X:a=[0,1,0];b=[0,0,1]
        else:raise ValueError('nonzero projective point')
        rows=[[0,0,0],b,[3*x-2*y for x,y in zip(a,b)],[-5*x for x in a],a]
        take('rank2 '+name,rows,(2,ok))
    for name,row,ok in [('irrational two positive',[1,-3,1],True),('double positive',[1,-4,4],True),('zero plus positive',[1,-1,0],True),('zero plus negative',[1,1,0],False),('opposite irrational',[1,0,-2],True),('double negative',[1,2,1],False),('negative discriminant',[1,-1,1],False),('constant',[0,0,7],False),('linear positive',[0,1,-3],True),('linear negative',[0,1,3],False),('linear zero only',[0,2,0],False),('row sign normalization',[-1,3,-1],True)]:
        take('rank1 '+name,[[0,0,0],row,[-7*x for x in row],[3*x for x in row],[0,0,0]],(1,ok))
    return cases
