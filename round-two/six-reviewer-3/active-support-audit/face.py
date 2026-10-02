"""Direct finite binomial forms and low completion, independent of author code."""
from fractions import Fraction as F
from math import comb
from exact import need


def choose(n,k):return comb(n,k) if 0<=k<=n else 0


def key(a,b):return tuple(sorted((a,b)))


def complete(n,middle,homogeneous=False):
    """Solve original row and size-kernel equations; no closed base input."""
    T=2**(n-1);s=T-n;beta={key(a,b):F(x) for (a,b),x in middle.items()}
    def get(a,b):return beta.get(key(a,b),F(0))
    for a in range(3,n-1):
        z=sum((get(a,b)*choose(n-a,b) for b in range(3,n-1)),F(0))
        w=sum((b*get(a,b)*choose(n-a,b) for b in range(3,n-1)),F(0))
        r0=(0 if homogeneous else T-2)-z
        r1=(0 if homogeneous else (n-a)*s)-w
        beta[key(1,a)]=(2*r0-r1)/(n-a)
        beta[key(2,a)]=(r1-r0)/choose(n-a,2)
    r0=(0 if homogeneous else T-2)-sum((get(1,a)*choose(n-1,a) for a in range(3,n-1)),F(0))
    r1=(0 if homogeneous else (n-1)*s)-sum((a*get(1,a)*choose(n-1,a) for a in range(3,n-1)),F(0))
    beta[(1,2)]=(r1-r0)/choose(n-1,2);beta[(1,1)]=(2*r0-r1)/(n-1)
    r2=(0 if homogeneous else T-2)-sum((get(2,a)*choose(n-2,a) for a in range(3,n-1)),F(0))
    beta[(2,2)]=(r2-(n-2)*get(1,2))/choose(n-2,2)
    for a in range(1,n-1):
        need(sum((get(a,b)*choose(n-a,b) for b in range(1,n-1)),F(0))==(0 if homogeneous else T-2),'every literal affine row')
        need(sum((b*get(a,b)*choose(n-a,b) for b in range(1,n-1)),F(0))==(0 if homogeneous else (n-a)*s),'every literal size row')
    return {k:v for k,v in beta.items() if v}


def base(n):return complete(n,{(a,n-a):2**(n-1)-n for a in range(3,(n//2)+1)})


def closed_base(n):
    T=2**(n-1);s=T-n;b={}
    for a in range(3,n-2):
        b[key(1,a)]=F(2*(n-2),n-a);b[key(2,a)]=F(-2*(n-2),(n-a)*(n-a-1))
        b[key(a,n-a)]=F(s)
    b[(1,n-2)]=F(n-2);b[(2,n-2)]=F(s-(n-2))
    b[(1,1)]=F(T*n*n-9*T*n+16*T-n**3+9*n*n-8*n-16,n*(n-1))
    b[(1,2)]=F(2*(-T*n+4*T+2*n*n-4*n-4),n*(n-1))
    b[(2,2)]=F(-4*(-T*n+2*T+2*n*n-2*n-2),n*(n-3)*(n-1))
    return {k:v for k,v in b.items() if v}


def profiles(n,k):
    need(type(n)is int and n>=6 and type(k)is int and 2<=k and 2*k<n,'profile integer domain')
    c=F(2,n);d=-F(2*n+5,n*n);p=[];q=[]
    for a in range(1,n-1):
        if a<=k:p.append(F(1));q.append(c+d*a)
        elif n-a<=k:p.append(F(-1));q.append(c+d*(n-a))
        else:
            z=2*a-n;V=16*n**4+(2*n+5)**2*z*z
            p.append(F((2*n+5)**3*z**3,2*n*n*V));q.append(-F(1,2*n)+F(2*(2*n+5)**2*z*z,V))
    return p,q


def forms(n,beta,homogeneous=False):
    sizes=list(range(1,n-1));weights=[comb(n,a) for a in sizes];T=2**(n-1);s=T-n;h=T-1
    K=[];U=[]
    for a,ga in zip(sizes,weights):
        kr=[];ur=[]
        for b,gb in zip(sizes,weights):
            coupling=beta.get(key(a,b),F(0))*choose(n-a,b)
            kr.append(ga*(coupling if homogeneous else s*int(a==b)-gb+coupling))
            ur.append(ga*(-coupling if homogeneous else h*int(a==b)-coupling))
        K.append(kr);U.append(ur)
    need(all(K[i][j]==K[j][i] and U[i][j]==U[j][i] for i in range(n-2) for j in range(n-2)),'physical form symmetry')
    return K,U


def quad(H,x):return sum((a*x[i]*x[j] for i,row in enumerate(H) for j,a in enumerate(row)),F(0))


def finite_case(n,k):
    B=base(n);need(B==closed_base(n),'every independently solved base coefficient versus credited closed formula')
    K,U=forms(n,B);p,q=profiles(n,k);c=F(2,n);d=-F(2*n+5,n*n)
    f=[x-1 for x in p];g=[x-c-d*a for a,x in enumerate(q,1)];gamma=-1-F(1,2*n)
    for a in range(3,n-2):
        b=n-a;need(p[a-1]==-p[b-1] and q[a-1]==q[b-1],'all paired layers and central self-complement')
        need(p[a-1]**2+(q[a-1]-gamma)**2==1+d*d*(2*a-n)**2/4,'all literal layer circle identities')
    directions=[]
    for a in range(3,n-2):
        for b in range(a,n-2):
            if a+b>n or (a+b<n and min(a,b)>k):continue
            delta=complete(n,{(a,b):1},True);dK,dU=forms(n,delta,True)
            need(all(sum(row)==0 and sum(x*(j+1) for j,x in enumerate(row))==0 for row in dK),'every entry of both variation kernels')
            need(all(dU[i][j]==-dK[i][j] for i in range(n-2) for j in range(n-2)),'all upper variations are negative lower variations')
            pl,pu=quad(dK,p),quad(dU,q);rl,ru=quad(dK,f),quad(dU,g)
            need(pl==rl and pu==ru and pl+pu==0,'whole independent lower/upper pairings for every permitted direction')
            coefficient=(2-int(a==b))*comb(n,a)*choose(n-a,b)*(f[a-1]*f[b-1]-g[a-1]*g[b-1])
            need(coefficient==pl+pu,'literal ordered-pair multiplicity of residual coordinate')
            directions.append({'free_coordinate':[a,b],'all_nonzero_completed_coefficients':[[*ij,str(x)] for ij,x in sorted(delta.items())],'lower_pairing':str(pl),'upper_pairing':str(pu),'residual_lower_pairing':str(rl),'residual_upper_pairing':str(ru),'coefficient':str(coefficient)})
    need(quad(K,p)==4*(2**(n-1)-n-1),'entire finite odd lower energy')
    return {'n':n,'k':k,'base_coefficients':[[*ij,str(x)] for ij,x in sorted(B.items())],'p':list(map(str,p)),'q':list(map(str,q)),'whole_lower_form':[[str(x) for x in row] for row in K],'whole_upper_form':[[str(x) for x in row] for row in U],'all_permitted_directions':directions,'lower_energy':str(quad(K,p)),'upper_energy':str(quad(U,q)),'combined_energy':str(quad(K,p)+quad(U,q))}
