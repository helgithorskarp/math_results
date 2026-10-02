"""Independent rational frame reconstructed from the displayed vectors.

No author module/fixture import. All matrices are in the physical ten-vector
basis; the original-set lift is checked separately in physical.py.
"""
from fractions import Fraction as F
from rational import R
from linear import need,digest

def zero(n):return [R(0)for _ in range(n)]
def unit(n,i):v=zero(n);v[i]=R(1);return v
def plus(a,b):return [x+y for x,y in zip(a,b)]
def scale(a,z):return [x*z for x in a]
def inner(G,a,b):
    return sum((a[i]*G[i][j]*b[j]for i in range(len(a))for j in range(len(b))if a[i].p!=(0,)and b[j].p!=(0,)),R(0))

def model():
    q=R((4,1));n=10;e=[unit(n,i)for i in range(n)];G=[[R(0)for _ in range(n)]for _ in range(n)]
    norms=[q-1,R(3),3*(q-1),3*(q-1),2*(q+3)/3,2*(q+3),6*(q+3)]
    for i,x in enumerate(norms):G[i][i]=x
    G[2][3]=G[3][2]=R(-3)
    H=scale(plus(e[1],e[2]),F(1,3));V4=plus(scale(plus(e[1],e[3]),F(1,3)),e[4])
    K=plus(e[0],plus(scale(e[1],F(1,3)),plus(e[2],plus(scale(e[3],F(1,3)),e[4]))))
    T1=plus(scale(e[5],F(1,2)),scale(e[6],F(1,6)))
    T2=plus(scale(e[5],F(-1,2)),scale(e[6],F(1,6)));T3=scale(e[6],F(-1,3))
    d=3*(q-6)/(5*q);g=(q-4)/(5*(q+2))
    b=(d*(q-1)/(q+1)-g)/2;a=-b*(q+1)/(q-1);ee=-g-2*b
    f=-g*(q+1)/(q-1);c=(a-d)*q/(q+3)
    need(f==-2*a-d,'balanced full-mark coefficient identity')
    PU=plus(scale(K,F(-1,5)),plus(scale(H,a),plus(scale(V4,b),scale(T2,c))))
    PV=plus(scale(K,F(-1,5)),plus(scale(H,a),plus(scale(V4,b),scale(T1,c))))
    PUV=plus(scale(K,F(-1,5)),plus(scale(H,d),scale(V4,ee)))
    PB=plus(scale(K,F(-1,5)),plus(scale(H,f),plus(scale(V4,g),scale(T3,c))))
    p=[PU,PV,PUV,PB];eta=[q+2-inner(G,x,x)for x in p]
    rr=-1-inner(G,PU,PUV);tt=(eta[2]+2*rr-eta[3])/2
    W=[[R(0)for _ in range(4)]for _ in range(4)]
    for i,x in enumerate(eta):W[i][i]=x
    W[0][2]=W[2][0]=W[1][2]=W[2][1]=rr
    W[0][3]=W[3][0]=W[1][3]=W[3][1]=tt
    W[2][3]=W[3][2]=-eta[2]-2*rr;W[0][1]=W[1][0]=-eta[0]-rr-tt
    need(all(sum(row,R(0))==0 for row in W),'full private residual row sums')
    G[7][7]=2*(eta[0]-W[0][1]);G[8][8]=eta[2];G[9][9]=eta[3];G[8][9]=G[9][8]=W[2][3]
    residual=[plus(scale(e[7],F(1,2)),plus(scale(e[8],F(-1,2)),scale(e[9],F(-1,2)))),
              plus(scale(e[7],F(-1,2)),plus(scale(e[8],F(-1,2)),scale(e[9],F(-1,2)))),e[8],e[9]]
    need(all(inner(G,residual[i],residual[j])==W[i][j]
             for i in range(4)for j in range(4)),'entire four-residual realization')
    marked=[plus(H,T1),plus(H,T2),plus(H,T3),V4];private=[plus(x,y)for x,y in zip(p,residual)]
    empty=scale(K,F(-1,5));vectors=marked+private+[empty]
    oldframe=[[R(0)for _ in range(n)]for _ in range(n)]
    oldframe[0][0]=q*q-1;oldframe[0][1]=oldframe[1][0]=3*(q-1);oldframe[1][1]=R(9)
    for i in [2,3]:
        for j in [2,3]:oldframe[i][j]=6*G[i][j]
    FF=[row[:]for row in oldframe]
    for v in vectors:
        image=[sum((G[i][j]*v[j]for j in range(n)),R(0))for i in range(n)]
        for i in range(n):
            for j in range(n):FF[i][j]+=image[i]*image[j]
    BB=[[(2*q+7)*G[i][j]-FF[i][j]for j in range(n)]for i in range(n)]
    antisym=[5,7];sym=[i for i in range(n)if i not in antisym]
    need(all(BB[i][j]==0 for i in antisym for j in sym),'entire sector cross zero')
    need(inner(G,K,K)==5*q-4,'K actual norm')
    need(inner(G,K,H)==q-1 and inner(G,K,V4)==q+1,'marked projections')
    need(all(inner(G,K,plus(v,scale(K,F(1,5))))==0 for v in p),'all K-orthogonal contrasts')
    need(all(x==0 for x in plus(sum_vectors(private),scale(K,F(4,5)))),'all private vector sum')
    need(inner(G,K,K)*(2*q+7)-inner(FF,K,K)==17*q-F(6,5),'complete physical K slack')
    for i,j in [(0,0),(0,2),(1,1),(1,2),(2,0),(2,1),(2,2),(3,3)]:
        need(inner(G,private[i],marked[j])==-1,'mandatory private/marked intersection')
    need(inner(G,private[0],private[2])==-1 and inner(G,private[1],private[2])==-1,'private intersections')
    need(all(inner(G,v,v)==q+2 for v in marked+private),'every actual new norm')
    return {'gram':G,'frame':FF,'cap':BB,'residual':W,'projected':p,'marked':marked,'private':private,
            'empty':empty,'K':K,'parameters':[a,b,c,d,ee,f,g],
            'blocks':[('private_residual',[row[7:]for row in G[7:]]),
                      ('cap_antisymmetric',[[BB[i][j]for j in antisym]for i in antisym]),
                      ('cap_symmetric',[[BB[i][j]for j in sym]for i in sym])]}

def sum_vectors(vs):
    out=zero(len(vs[0]))
    for v in vs:out=plus(out,v)
    return out

def evaluate(A,q):return [[x.value(F(q)-4)for x in row]for row in A]
