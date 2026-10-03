"""Fresh exact sign/trace/full-projector audit. No author module imports."""
import argparse,json
from fractions import Fraction as Q
from itertools import combinations
from math import comb


def need(ok,msg):
    if not ok:raise ValueError(msg)
def add(a,b):return [(a[i]if i<len(a)else 0)+(b[i]if i<len(b)else 0)for i in range(max(len(a),len(b)))]
def scale(a,c):return [v*c for v in a]
def mul(a,b):
    z=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i+j]+=x*y
    return z
def power(a,n):
    z=[Q(1)]
    for _ in range(n):z=mul(z,a)
    return z
def ev(a,x):
    y=Q(0)
    for v in a[::-1]:y=y*x+v
    return y
def div(a,b):
    z=a[:];out=[Q(0)]*max(1,len(a)-len(b)+1)
    while len(z)>=len(b):
        c=z[-1]/b[-1];j=len(z)-len(b);out[j]=c
        for k,x in enumerate(b):z[j+k]-=c*x
        while z and not z[-1]:z.pop()
    return out,z
def solve(A,b):
    n=len(b);R=[list(A[i])+[b[i]]for i in range(n)]
    for j in range(n):
        pivot=next((i for i in range(j,n)if R[i][j]),None);need(pivot is not None,'nonsingular exact solve')
        R[j],R[pivot]=R[pivot],R[j];R[j]=[x/R[j][j]for x in R[j]]
        for i in range(n):
            if i!=j:
                t=R[i][j];R[i]=[x-t*y for x,y in zip(R[i],R[j])]
    return [r[-1]for r in R]
def bernstein(a,L,R):
    n=len(a)-1;raw=[Q(0)]*(n+1)
    for i,x in enumerate(a):raw=add(raw,scale(power([L,R-L],i),x))
    first=[sum((raw[i]*Q(comb(j,i),comb(n,i))for i in range(j+1)),Q(0))for j in range(n+1)]
    grid=[Q(j,n)for j in range(n+1)]if n else [Q(0)]
    rows=[[comb(n,j)*t**j*(1-t)**(n-j)for j in range(n+1)]for t in grid]
    second=solve(rows,[ev(a,L+(R-L)*t)for t in grid])
    need(first==second,'whole Bernstein conversion by separate interpolation')
    return first
def tr(A):return sum((A[i][i]for i in range(len(A))),Q(0))
def ident(n):return [[Q(i==j)for j in range(n)]for i in range(n)]
def transpose(A):return [list(x)for x in zip(*A)]
def matmul(A,B):
    return [[sum((x*y for x,y in zip(row,col)),Q(0))for col in transpose(B)]for row in A]
def matadd(A,B,c=Q(1)):return [[x+c*y for x,y in zip(a,b)]for a,b in zip(A,B)]
def matscale(A,c):return [[c*x for x in a]for a in A]
def matpoly(p,A):
    I=ident(len(A));z=matscale(I,Q(0))
    for x in p[::-1]:z=matadd(matmul(z,A),I,x)
    return z
def nullspace(A):
    R=[r[:]for r in A];n=len(R[0]);row=0;pivots=[]
    for j in range(n):
        p=next((i for i in range(row,len(R))if R[i][j]),None)
        if p is None:continue
        R[row],R[p]=R[p],R[row];R[row]=[v/R[row][j]for v in R[row]]
        for i in range(len(R)):
            if i!=row:
                t=R[i][j];R[i]=[x-t*y for x,y in zip(R[i],R[row])]
        pivots.append(j);row+=1
    columns=[]
    for j in range(n):
        if j in pivots:continue
        v=[Q(0)]*n;v[j]=1
        for i,p in enumerate(pivots):v[p]=-R[i][j]
        columns.append(v)
    return transpose(columns)
def gram_projector(N):
    G=matmul(transpose(N),N);m=len(G)
    inv=transpose([solve(G,[Q(i==j)for i in range(m)])for j in range(m)])
    return matmul(matmul(N,inv),transpose(N))
def charpoly(A):
    n=len(A);I=ident(n);B=I;c=[Q(1)]
    for k in range(1,n+1):
        AB=matmul(A,B);x=-tr(AB)/k;c.append(x);B=matadd(AB,I,x)
    need(B==matscale(I,Q(0)),'whole Cayley--Hamilton matrix')
    return c[::-1]
def trace_words(n,damage):
    counts={};rows=[]
    for mask in range(1,1<<n):
        if damage=='trace-word' and n==4 and mask==5:continue
        positions=[i for i in range(n)if mask>>i&1]
        gaps=sorted((positions[(j+1)%len(positions)]-positions[j])%n or n for j in range(len(positions)))
        key=tuple(gaps);sign=(-1)**len(positions);counts[key]=counts.get(key,0)+sign
        rows.append({'mask':mask,'cyclic_moment_gaps':gaps,'sign':sign})
    wanted={(2,):-2,(1,1):1}if n==2 else {(4,):-4,(1,3):4,(2,2):2,(1,1,2):-4,(1,1,1,1):1}
    need(counts==wanted,'entire cyclic rank-one word contraction')
    return rows,counts


def run(damage=None):
    cases=[]
    for n in [7,8]:
        for k in [1,2,3]:
            m=n-1-k;L,R=Q(m,k+1),Q(m+1,k)
            a=add(add([Q(-m)],power([Q(m),Q(-k)],3)),[Q(0),Q(0),Q(0),Q(k)])
            if damage=='cubic-leading' and (n,k)==(7,2):a[-1]+=1
            direct=[Q(m**3-m),Q(-3*m*m*k),Q(3*m*k*k),Q(k-k**3)]
            need(a==direct,'every raw third-moment coefficient')
            while len(a)>1 and not a[-1]:a.pop()
            factors=[];quotient=a
            if (n,k)==(7,3):
                quotient,rem=div(a,[Q(-1),Q(1)]);need(not rem,'complete interior-root division');factors=[Q(1)]
                root=Q(1,2)if damage=='root-middle' else Q(1)
                need(L<root<R and ev(a,root)==0 and m-k*root==0,'only interior root is a zero middle coordinate')
            elif (n,k)==(8,3):
                quotient,rem=div(a,power([Q(-1),Q(1)],2));need(not rem and L==1,'complete excluded-endpoint double-root division');factors=[Q(1),Q(1)]
            b=bernstein(quotient,L,R);need(all(x>0 for x in b),'strict entire closed interval quotient')
            rebuilt=quotient
            for root in factors:rebuilt=mul(rebuilt,[-root,Q(1)])
            need(rebuilt==a,'every complete cubic reconstructed from its factors')
            cases.append(dict(n=n,m=m,k=k,closed_enclosing_interval=[L,R],whole_polynomial=a,
                              divided_roots=factors,whole_quotient=quotient,whole_Bernstein=b))
    if damage=='missing-case':cases.pop()
    need([(x['n'],x['k'])for x in cases]==[(n,k)for n in [7,8]for k in [1,2,3]],'all six legal minimum strata')
    I=ident(8);E=[[Q(1,8)]*8 for _ in range(8)];P=matadd(I,E,-1)
    v=[Q(x)for x in [1,1,1,-1,-1,-1,0,0]];V=[[v[i]*Q(i==j)for j in range(8)]for i in range(8)];H=matmul(matmul(P,V),P)
    p=[Q(1)]
    for x in v:p=mul(p,[-x,Q(1)])
    derivative=[i*p[i]/8 for i in range(1,len(p))]
    need(charpoly(H)==[Q(0)]+derivative,'entire ambient characteristic = z*fprime/8')
    eigenvalues=list(map(Q,[-1,Q(-1,2),0,Q(1,2),1]));projections=[];rho=[]
    for lam in eigenvalues:
        f=[Q(1)]
        for other in eigenvalues:
            if other!=lam:f=scale(mul(f,[-other,Q(1)]),1/(lam-other))
        A=matpoly(f,H)
        if damage=='projector-zero' and lam==0:A=matadd(A,E,-1)
        N=nullspace(matadd(H,I,-lam));B=gram_projector(N)
        need(A==B,'ALL64 projector entries from polynomial and nullspace/Gram routes')
        need(matmul(A,A)==A and transpose(A)==A and matmul(H,A)==matscale(A,lam),'full symmetric idempotent eigenspace')
        mass=sum((v[i]*A[i][j]*v[j]for i in range(8)for j in range(8)),Q(0));norm=Q(8)if damage=='mass-normalization' else Q(6)
        r=mass/norm;rho.append(r);projections.append(dict(eigenvalue=lam,full_ambient_projector=A,rank=tr(A),unnormalized_full_mass=mass,normalized_mass=r))
    summed=matscale(I,Q(0))
    for x in projections:summed=matadd(summed,x['full_ambient_projector'])
    need(summed==I and [x['rank']for x in projections]==[2,1,2,1,2],'entire ambient eigenspace census including zero')
    for i,j in combinations(range(5),2):need(matmul(projections[i]['full_ambient_projector'],projections[j]['full_ambient_projector'])==matscale(I,Q(0)),'full projector pair orthogonality')
    X=Q(sum(x**4 for x in v),36);D=X-Q(1,8);eta=sum(x*x for x in rho)
    need(sum(rho)==1 and rho==[0,Q(1,2),0,Q(1,2),0]and eta==Q(1,2)and(1-eta)/D==12,'entire normalized equality angular value')
    M=matscale(I,Q(0));vv=[[v[i]*v[j]/6 for j in range(8)]for i in range(8)]
    for row in projections:
        A=row['full_ambient_projector'];M=matadd(M,matmul(matmul(A,vv),A))
    normalized_H2=matscale(matmul(H,H),Q(1,6))
    centered_M=matadd(M,P,-Q(1,7));centered_H2=matadd(normalized_H2,P,-Q(3,28))
    inner=tr(matmul(centered_M,centered_H2));normM=tr(matmul(centered_M,centered_M));normH=tr(matmul(centered_H2,centered_H2))
    need(tr(M)==1 and tr(matmul(M,M))==eta and tr(matmul(M,normalized_H2))==D,'entire grouped-mass operator traces')
    need(inner==D-Q(3,28)and normM==eta-Q(1,7)and normH==D/2+Q(3,224)and inner*inner<=normM*normH,'whole centered Hilbert--Schmidt identities')
    word2,c2=trace_words(2,damage);word4,c4=trace_words(4,damage)
    controls=[]
    for raw in [[1,-1,0,0,0,0,0,0],[1,1,1,-1,-1,-1,0,0],[1,1,1,1,-1,-1,-1,-1],
                [7,-1,-1,-1,-1,-1,-1,-1],[-4,-3,-2,-1,1,2,3,4],[2,1,-1,-2,0,0,0,0]]:
        need(sum(raw)==0,'all literal trace controls balanced')
        s=sum(Q(x*x)for x in raw);x4=sum(Q(x**4)for x in raw)
        A=matmul(matmul(P,[[Q(raw[i])*Q(i==j)for j in range(8)]for i in range(8)]),P);A2=matmul(A,A);A4=matmul(A2,A2)
        need(tr(A2)==3*s/4 and tr(A4)==x4/2+s*s/32,'full literal traces before normalization')
        w=[[Q(x)]for x in raw];energy=matmul(matmul(transpose(w),A2),w)[0][0]
        need(energy==x4-s*s/8,'full actual weighted second spectral moment')
        controls.append(dict(raw_original_slopes=raw,whole_compression=A,whole_square=A2,whole_fourth=A4,
                             trace2=tr(A2),trace4=tr(A4),weighted_energy=energy))
    # Complete rational covariance simplification, not evaluation at a mesh.
    den=[Q(3,224),Q(1,2)];mu=Q(3,28)
    numerator=add(scale(den,Q(6,7)),scale(power([-mu,Q(1)],2),-1))
    expected=[Q(0),Q(9,14),Q(-1)]
    if damage=='covariance-payment':expected[1]+=Q(1,1000)
    need(numerator==expected,'whole covariance-to-angular envelope identity')
    bound=(Q(9,14)-D)/ev(den,D);derivative=add(scale(den,-1),scale([Q(9,14),Q(-1)],-Q(1,2)))
    need(derivative==[Q(-75,224),Q(0)]and bound==Q(404,23)and 12<bound<Q(144,7)<Q(49,2),'whole monotonicity and strict improved threshold')
    return dict(agent='six-reviewer-1',role='independent mathematical reviewer',written_proof_exposed_NOT_BLIND=True,
                new_native_target_modules_imported=False,all_six_minimum_cases=cases,equality_original_polynomial=p,
                equality_entire_ambient_characteristic=charpoly(H),all_five_full_ambient_projectors=projections,
                equality_X=X,equality_D=D,equality_eta=eta,equality_C=Q(12),all_trace2_words=word2,all_trace4_words=word4,
                full_mass_operator=M,full_centered_mass_operator=centered_M,full_centered_H_square=centered_H2,
                HS_inner=inner,HS_mass_square=normM,HS_compression_square=normH,
                all_six_original_trace_controls=controls,covariance_numerator=numerator,envelope_denominator=den,
                envelope_derivative_numerator=derivative,strict_sign_sector_threshold=bound,
                universal_envelope='C <= (9/14-D)/(D/2+3/224), balanced real8 norm1 D>0; full spectral groups',
                general_first_power_claim=False)


def encode(v):
    if isinstance(v,Q):return str(v)
    if isinstance(v,dict):return {str(k):encode(x)for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [encode(x)for x in v]
    return v
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--damage',choices=['missing-case','cubic-leading','root-middle',
        'projector-zero','mass-normalization','trace-word','covariance-payment']);a=p.parse_args()
    print(json.dumps(encode(run(a.damage)),sort_keys=True,separators=(',',':')))
