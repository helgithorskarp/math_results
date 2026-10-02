"""Uniform sign certificate with independent determinant identities.

Bareiss gives all leading determinant polynomials. A separate scalar
Fraction Gaussian determinant verifies each at degree-bound+1 points.
The polynomial identity theorem makes this an exact identity check,
not interpolation guessing or sampling a sign on the half-line.
"""
from fractions import Fraction as F
import random
import signal
from univariate import P,R,atom,ATOMS,denominator,value,rational_value
from model import model
from exact import require,psd_rank

def alarm(signum,frame):raise TimeoutError('fixed symbolic60s stage guard')
signal.signal(signal.SIGALRM,alarm)

def reference_product(a,b):
    out={}
    for (i,),x in a.a.items():
        for (j,),y in b.a.items():out[(i+j,)]=out.get((i+j,),0)+x*y
    return P(out,a.den*b.den)

def arithmetic_controls():
    rng=random.Random(20261002);count=0
    for degree in [0,6,24,60]:
        for repeat in range(4):
            a=P({(i,):rng.randrange(-(1<<70),1<<70) for i in range(degree+1)},7)
            b=P({(i,):rng.randrange(-10000,10001) for i in range(degree+1)},11)
            product=a*b
            require(product==reference_product(a,b),'all packed/reference coefficients')
            require(product.exact_div(a)==b,'exact polynomial cancellation')
            for t in [0,1,5]:require(value(product,t)==value(a,t)*value(b,t),'Horner/product identity')
            count+=1
    require(not P() and P(-1)*P(-1)==P(1),'zero and negative products')
    require(P(1).exact_div(P({(1,):1})) is None,'reject nonexact polynomial division')
    return count

def clear_rows(matrix):
    out=[];domains=[]
    for row in matrix:
        powers={}
        for z in row:
            for a,e in z.den.items():powers[a]=max(powers.get(a,0),e)
        require(all(ATOMS[a].positive() for a in powers),'strict clearing factors on t>=0')
        domains.append(powers)
        out.append([z.num*denominator({a:e-z.den.get(a,0) for a,e in powers.items() if e>z.den.get(a,0)}) for z in row])
    return out,domains

def bareiss_minors(a):
    a=[row[:] for row in a];prior=P(1);out=[]
    for k in range(len(a)):
        pivot=a[k][k];require(bool(pivot),'nonzero symbolic leading minor')
        out.append(pivot)
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                top=pivot*a[i][j]-a[i][k]*a[k][j]
                result=top.exact_div(prior)
                require(result is not None,'exact Bareiss division')
                a[i][j]=result
        prior=pivot
    return out

def scalar_determinant(a):
    a=[[F(x) for x in row] for row in a];out=F(1)
    for k in range(len(a)):
        r=next((i for i in range(k,len(a)) if a[i][k]),None)
        if r is None:return F(0)
        if r!=k:a[k],a[r]=a[r],a[k];out=-out
        pivot=a[k][k];out*=pivot
        for i in range(k+1,len(a)):
            factor=a[i][k]/pivot
            for j in range(k+1,len(a)):a[i][j]-=factor*a[k][j]
    return out

def determinant_identity(matrix,minor):
    bound=sum(max(z.degree() for z in row) for row in matrix)
    require(minor.degree()<=bound,'determinant degree bound')
    for t in range(bound+1):
        actual=scalar_determinant([[value(z,t) for z in row] for row in matrix])
        require(actual==value(minor,t),'independent exact determinant identity')
    return bound+1

def uniform():
    signal.alarm(60)
    controls=arithmetic_controls()
    q=R(P({(1,):1,(0,):4}))
    for z in [q,q-1,q+1,q+2,q+3]:atom(z.num)
    G,frame,p=model(q,fraction=lambda a,b=1:R(F(a,b)))
    B=[[(2*q+7)*G[i][j]-frame[i][j] for j in range(10)] for i in range(10)]
    require(all(G[i][j]==G[j][i] and B[i][j]==B[j][i] for i in range(10) for j in range(10)),'symbolic symmetry')
    anti=[5,7];sym=[0,1,2,3,4,6,8,9]
    require(all(not G[i][j] and not B[i][j] for i in anti for j in sym),'complete2+8 sector split')
    require(p['a']*(q-1)+p['b']*(q+1)==0 and p['d']*(q-1)+p['e']*(q+1)==0 and p['f']*(q-1)+p['g']*(q+1)==0,'three K-orthogonal contrasts')
    K=[R(1),R(F(1,3)),R(1),R(F(1,3)),R(1)]+[R(0)]*5
    def form(A):return sum(K[i]*A[i][j]*K[j] for i in range(10) for j in range(10))
    require(form(G)==5*q-4 and form(B)==17*q-F(6,5),'complete scalar K slack identity')
    records=[]
    for label,matrix,indices in [('residual-Gram',G,[7,8,9]),('cap-antisymmetric',B,anti),('cap-symmetric',B,sym)]:
        signal.alarm(60)
        sub=[[matrix[i][j] for j in indices] for i in indices]
        A,domains=clear_rows(sub);minors=bareiss_minors(A);rows=[]
        for k,z in enumerate(minors,1):
            require(z.positive(),'all determinant coefficients nonnegative and constant positive')
            points=determinant_identity([row[:k] for row in A[:k]],z)
            rows.append({'order':k,'degree':z.degree(),'coefficients':len(z.a),
                         'strictly_positive_coefficients':all(v>0 for v in z.a.values()),
                         'constant':str(value(z,0)),'fingerprint':z.fingerprint(),
                         'independent_identity_points':points})
        records.append({'label':label,'indices':indices,'minors':rows,
                        'row_clearing_domains':[[{'factor':[[k[0],str(v)] for k,v in sorted(ATOMS[a].a.items())],'exponent':e} for a,e in sorted(d.items())] for d in domains]})
    signal.alarm(0)
    scalar=[]
    for qv in [4,8,16,32,64,128,1024,1000000,1<<100]:
        signal.alarm(60)
        g0,f0,_=model(F(qv));tv=qv-4
        require([[rational_value(z,tv) for z in row] for row in G]==g0,'every symbolic/reference Gram entry')
        require([[rational_value(z,tv) for z in row] for row in frame]==f0,'every symbolic/reference frame entry')
        cap=[[(2*qv+7)*g0[i][j]-f0[i][j] for j in range(10)] for i in range(10)]
        require(psd_rank(g0)==psd_rank(cap)==10,'scalar full changed-space PD')
        scalar.append({'q':str(qv),'Gram_positions':100,'frame_positions':100,'Gram_rank':10,'gap1_cap_rank':10})
        signal.alarm(0)
    return {'domain':'q=4+t,t>=0','arithmetic_controls':controls,'records':records,
            'symbolic_sector_cross_positions':64,'K_slack':'17*q-6/5',
            'scalar_controls':scalar,'scalar_role':'validation; q1000000 is auxiliary, no literal huge cube'}

def rejects(action,label):
    try:action()
    except (ValueError,ZeroDivisionError):return label
    raise ValueError('damage accepted: '+label)

def damages():
    a=P({(0,):2,(1,):3})
    return [rejects(lambda:require(P({(0,):-1,(1,):3}).positive(),'sign'),'negative constant'),
            rejects(lambda:require(P({(1,):3}).positive(),'strict sign'),'boundary-zero constant'),
            rejects(lambda:require(P({(0,):2,(1,):-3}).positive(),'coefficient sign'),'negative nonconstant coefficient'),
            rejects(lambda:clear_rows([[R(1)/R(P({(1,):1}))]]),'boundary denominator'),
            rejects(lambda:determinant_identity([[a]],a+1),'wrong determinant polynomial')]
