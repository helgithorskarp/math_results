#!/usr/bin/env python3
"""six-reviewer-3: independent rank-five polynomial and literal audit.

No target code imports. Published rational/sign witnesses are checked data.
Newton traces replace the author's principal-minor polynomial algorithm.
Ballot matching products replace its finite harmonic nullspace basis.
"""
from fractions import Fraction as F
from math import comb, factorial, prod
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent.parent / 'six-downset-2/uniform_rank_five'
INPUT_HASHES = {
    'BOUNDARY_CERTIFICATES.json': 'a0acb6d81b0f9c606937120b99cd8c41dd5d28af7fa4102a63a4ae23ede0b5d1',
    'POSITIVITY_CERTIFICATE.json': 'ac6ab532e3e5ea9691611521b5ac4c2fafaf96117c6fa966689dc29c5d94ca1f',
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


class Poly:
    """Dense ascending Q[u] coefficients, independent implementation."""
    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.v = value.v
            return
        a = list(map(F, value)) if isinstance(value, (list, tuple)) else [F(value)]
        while len(a)>1 and a[-1]==0:
            a.pop()
        self.v = tuple(a)
    def __add__(self, other):
        b = Poly(other).v
        a = [F(0)]*max(len(self.v),len(b))
        for i,x in enumerate(self.v): a[i]+=x
        for i,x in enumerate(b): a[i]+=x
        return Poly(a)
    __radd__=__add__
    def __neg__(self): return Poly([-x for x in self.v])
    def __sub__(self,b): return self+-Poly(b)
    def __rsub__(self,b): return Poly(b)+-self
    def __mul__(self, other):
        b=Poly(other).v
        a=[F(0)]*(len(self.v)+len(b)-1)
        for i,x in enumerate(self.v):
            if x:
                for j,y in enumerate(b):
                    if y: a[i+j]+=x*y
        return Poly(a)
    __rmul__=__mul__
    def __truediv__(self,scalar): return Poly([x/F(scalar) for x in self.v])
    def __pow__(self,n):
        need(type(n) is int and n>=0,'polynomial exponent')
        out=Poly(1)
        for _ in range(n): out=out*self
        return out
    def __eq__(self,b): return self.v==Poly(b).v
    def record(self): return [str(x) for x in self.v]


def binom_poly(n,k):
    return prod((n-i for i in range(k)),start=Poly(1))/factorial(k)


def counting(n):
    return 1+sum(binom_poly(n,k) for k in range(1,6)),sum(binom_poly(n-1,k) for k in range(5))


def witness_parts(n):
    # Literal rational witness from target PROOF.md; never imports matrices.py.
    return {
        (1,4): (-(n-6)*(3*n*n-5*n+16),(2,3,4)),
        (1,5): (n**4+6*n**3-69*n*n+166*n-360,(2,3,4,5)),
        (2,4): (-2*(n**4-10*n**3+23*n*n-62*n+36),(2,3,4,5)),
        (2,5): (n**4+6*n**3-9*n*n+66*n-40,(2,3,4,5)),
        (3,4): (-(n**4-14*n**3+23*n*n-106*n+48),(3,4,5,6)),
        (3,5): (n**5-5*n**4-15*n**3+5*n*n-346*n+120,(3,4,5,6,7)),
        (4,4): (8*(2*n**5-12*n**4+14*n**3-279*n*n+335*n-942),(2,3,4,5,6,7)),
        (4,5): (n**7-15*n**6+51*n**5-165*n**4+684*n**3+6420*n*n-8416*n+27840,(2,3,4,5,6,7,8)),
        (5,5): (n**8-24*n**7+226*n**6-1064*n**5+3649*n**4-8096*n**3-15396*n*n+24544*n-102720,(2,3,4,5,6,7,8,9)),
    }


def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def elementary_traces(A):
    """Newton identities, not signed-permutation/principal-minor expansion."""
    size=len(A)
    power=A
    traces=[]
    for k in range(1,size+1):
        traces.append(sum(power[i][i] for i in range(size)))
        if k<size: power=matmul(power,A)
    e=[Poly(1) if isinstance(A[0][0],Poly) else F(1)]
    for k in range(1,size+1):
        e.append(sum((-1)**(i-1)*e[k-i]*traces[i-1] for i in range(1,k+1))/k)
    return e


def read_witnesses():
    answer={}
    for name,digest in INPUT_HASHES.items():
        raw=(TARGET/name).read_bytes()
        need(hashlib.sha256(raw).hexdigest()==digest,'changed input:'+name)
        answer[name]=json.loads(raw)
    return answer


def stable_audit(certificate):
    n=Poly([12,1]);N,s=counting(n)
    D=120*prod((n-i for i in range(2,10)),start=Poly(1))
    B=[[Poly() for _ in range(5)] for _ in range(5)]
    for (a,b),(p,den) in witness_parts(n).items():
        B[a-1][b-1]=B[b-1][a-1]=120*p*prod((n-i for i in range(2,10) if i not in den),start=Poly(1))
    for a in range(1,6):
        need(sum(B[a-1][b-1]*binom_poly(n-a-1,b-1) for b in range(1,6))==s*D,'star count')
        need(sum(B[a-1][b-1]*binom_poly(n-a,b) for b in range(1,6))==(N-1-s)*D,'center count')
    for a in range(1,5):
        det=binom_poly(n-a-1,3)*binom_poly(n-a,5)-binom_poly(n-a-1,4)*binom_poly(n-a,4)
        need(det==-(n-a)*binom_poly(n-a-1,3)*binom_poly(n-a-1,4)/20,'sequential affine uniqueness determinant')
        need(all(x<0 for x in det.v),'affine pivot is strictly negative at every n>=12')
    need(N-2*s==binom_poly(n-1,5),'strict half density')
    records=[];names=set()
    for j in range(6):
        layers=list(range(max(1,j),6))
        H=[[s*D*int(a==b)+(-1)**j*B[a-1][b-1]*binom_poly(n-a-j,b-j)
            -(D*binom_poly(n,b) if j==0 else 0) for b in layers] for a in layers]
        g=[binom_poly(n-2*j,a-j) for a in layers]
        for i in range(len(layers)):
            for k in range(len(layers)):
                need(g[i]*H[i][k]==g[k]*H[k][i],'metric symmetry')
        if j<=1:
            need(all(sum(row)==0 for row in H),'constant harmonic kernel')
            if j==0: need(all(sum(a*x for a,x in zip(layers,row))==0 for row in H),'cardinality harmonic kernel')
        rank=len(layers)-(2 if j==0 else 1 if j==1 else 0)
        e=elementary_traces(H)
        need(all(x==0 for x in e[rank+1:]),'trailing zero coefficients')
        for k in range(1,rank+1):
            low=sum((-1)**(k-l)*comb(rank-l,k-l)*e[l]*D**(k-l) for l in range(k+1))
            high=sum((-1)**l*comb(rank-l,k-l)*e[l]*((N-1)*D)**(k-l) for l in range(k+1))
            for label,value in [('lower',low),('upper',high)]:
                name=f'{label}_{j}_{k}';names.add(name);rec=certificate[name]
                need(type(rec['shift']) is int and rec['shift']==12,'shift')
                p,q=rec['numerator_ascending'],rec['denominator_ascending']
                need(p and q and all(type(x) is int and x>=0 for x in p+q) and p[0]>0 and q[0]>0 and p[-1]>0 and q[-1]>0,'positive coefficient proof')
                need(Poly(p)*D**k==Poly(q)*value,'infinite identity:'+name)
                if name=='lower_0_1':
                    damaged=p[:];damaged[0]+=1
                    need(Poly(damaged)*D**k!=Poly(q)*value,'altered sign witness must fail its identity')
                records.append({'name':name,'numerator_degree':len(p)-1,'denominator_degree':len(q)-1,'newton_polynomial_sha256':hashlib.sha256(json.dumps(value.record()).encode()).hexdigest()})
    need(names==set(certificate) and len(names)==34,'complete certificate scope')
    return records


def choose(n,k): return comb(n,k) if n>=k>=0 else 0


def weights(n,boundary):
    B=[[F(0) for _ in range(5)] for _ in range(5)]
    if n<12:
        for key,value in boundary[str(n)]['beta'].items():
            a,b=map(int,key);B[a-1][b-1]=B[b-1][a-1]=F(value)
        need(all(B[a-1][b-1]!=0 or str(a)+str(b) in boundary[str(n)]['beta'] or a+b>n for a in range(1,6) for b in range(a,6)),'unlisted boundary entries')
    else:
        for (a,b),(p,den) in witness_parts(F(n)).items():B[a-1][b-1]=B[b-1][a-1]=p/prod(n-i for i in den)
    return B


def sectors(n,B):
    s=sum(comb(n-1,k) for k in range(5));out=[]
    for j in range(min(5,n//2)+1):
        layers=list(range(max(1,j),min(5,n-j)+1));g=[comb(n-2*j,a-j) for a in layers]
        K=[[F(s*int(a==b)-(comb(n,b) if j==0 else 0))+(-1)**j*B[a-1][b-1]*choose(n-a-j,b-j) for b in layers] for a in layers]
        need(all(g[i]*K[i][k]==g[k]*K[k][i] for i in range(len(g)) for k in range(len(g))),'finite metric symmetry')
        out.append((j,layers,g,K))
    return out


def ldlt_rank(A):
    """Direct rational symmetric elimination, distinct from integer Bareiss."""
    A=[[F(x) for x in row] for row in A];need(all(A[i][j]==A[j][i] for i in range(len(A)) for j in range(len(A))),'symmetry')
    rank=0
    while A:
        need(all(A[i][i]>=0 for i in range(len(A))),'negative diagonal')
        pivot=next((i for i in range(len(A)) if A[i][i]>0),None)
        if pivot is None:
            need(all(x==0 for row in A for x in row),'zero diagonal residual');break
        indices=[i for i in range(len(A)) if i!=pivot];p=A[pivot][pivot]
        A=[[A[i][j]-A[i][pivot]*A[pivot][j]/p for j in indices] for i in indices];rank+=1
    return rank


def finite_audit(n,boundary):
    B=weights(n,boundary);N=sum(comb(n,k) for k in range(6));m=N-1;s=sum(comb(n-1,k) for k in range(5))
    for a in range(1,6):
        need(sum(B[a-1][b-1]*choose(n-a-1,b-1) for b in range(1,6))==s,'finite star')
        need(sum(B[a-1][b-1]*choose(n-a,b) for b in range(1,6))==m-s,'finite center')
    bs=sectors(n,B);record=[];core_rank=0
    alpha=F((n-2)*(n-3)*(2*n-1),2);bneg=(n-1)*(n-3);epsilon=F(n,72*m*(n-1)*(n-2)*(n-3))
    for j,layers,g,K in bs:
        r=len(layers)-(2 if j==0 else 1 if j==1 else 0);e=elementary_traces(K)
        need(all(x==0 for x in e[r+1:]),'finite zero eigenvalues')
        low=[sum((-1)**(k-l)*comb(r-l,k-l)*e[l] for l in range(k+1)) for k in range(1,r+1)]
        high=[sum((-1)**l*comb(r-l,k-l)*(N-1)**(k-l)*e[l] for l in range(k+1)) for k in range(1,r+1)]
        need(all(x>0 for x in low+high),'finite strict windows');core_rank+=r*(comb(n,j)-(comb(n,j-1) if j else 0))
        record.append({'j':j,'layers':layers,'positive_rank':r,'elementary':list(map(str,e)),'lower':list(map(str,low)),'upper':list(map(str,high))})
    need(core_rank==N-n-2,'core rank completeness')
    endpoints=[]
    for t in [epsilon,1/alpha]:
        Bt=[row[:] for row in B];Bt[0][0]+=t*(n-2)*(n-3);Bt[0][1]-=t*(n-3);Bt[1][0]-=t*(n-3);Bt[1][1]+=t
        ranks=[0,0]
        for j,layers,g,K in sectors(n,Bt):
            A=[[g[i]*K[i][k] for k in range(len(g))] for i in range(len(g))]
            U=[[g[i]*(N*int(a==b)-(comb(n,b) if j==0 else 0)-K[i][k]) for k,b in enumerate(layers)] for i,a in enumerate(layers)]
            lr,ur=ldlt_rank(A),ldlt_rank(U);need(lr==len(g)-(1 if j<=1 else 0) and ur==len(g),'repaired endpoints')
            mult=comb(n,j)-(comb(n,j-1) if j else 0);ranks[0]+=lr*mult;ranks[1]+=ur*mult
        need(ranks==[N-n-1,N-1],'repaired ranks')
        endpoints.append({'t':str(t),'lower_rank':ranks[0]+1,'upper_rank':ranks[1]})
    return {'n':n,'N':N,'s':s,'sectors':record,'endpoints':endpoints,'interval_to_original_ratio':str(1/(alpha*epsilon)),'trade_spectrum':{'positive':str(alpha),'negative':str(-bneg),'degree_two':1}}


def members(n,a): return [sum(1<<i for i in A) for A in combinations(range(n),a)]


def ballot_vectors(n,j):
    """Disjoint pair products, triangular on the ballot top-set coordinates."""
    if j==0:return [{0:1}]
    output=[];tops=[]
    for B in combinations(range(n),j):
        if any(b+1<2*(i+1) for i,b in enumerate(B)):continue
        used=set(B);pairs=[]
        for b in B:
            a=next(i for i in range(b) if i not in used);used.add(a);pairs.append((a,b))
        h={}
        for signs in product([0,1],repeat=j):
            mask=sum(1<<pairs[i][sign] for i,sign in enumerate(signs));h[mask]=(-1)**sum(signs)
        need(all(sum(v for mask,v in h.items() if mask&R==R)==0 for R in members(n,j-1)),'harmonic pair product')
        top=sum(1<<b for b in B);need(h[top]==(-1)**j,'leading top coefficient');output.append(h);tops.append(top)
    need(len(output)==comb(n,j)-comb(n,j-1),'ballot harmonic dimension')
    need(all(output[i].get(tops[k],0)==0 for i in range(len(output)) for k in range(i+1,len(output))),'triangular harmonic basis')
    return output


def literal_harmonics(n=7):
    layers={a:members(n,a) for a in range(1,6)};actions=0;norms=0;grams=0;vectors=[]
    for j in range(n//2+1):
        hs=ballot_vectors(n,j);lifted_sets=[]
        for h in hs:
            lifted={a:[sum(v for J,v in h.items() if J&A==J) for A in layers[a]] for a in layers}
            lifted_sets.append((h,lifted))
            for a,values in lifted.items():
                need(sum(x*x for x in values)==choose(n-2*j,a-j)*sum(v*v for v in h.values()),'literal lift norm');norms+=1
            active=list(range(max(1,j),min(5,n-j)+1))
            for b in active:
                for a in layers:
                    factor=(-1)**j*choose(n-a-j,b-j)
                    got=[sum(v for B,v in zip(layers[b],lifted[b]) if not A&B) for A in layers[a]]
                    need(got==[factor*v for v in lifted[a]],'literal disjoint action');actions+=1
                vector=[]
                for a in layers:vector+=lifted[a] if a==b else [0]*len(layers[a])
                vectors.append((j,b,vector))
        for a in range(max(1,j),min(5,n-j)+1):
            for h,left in lifted_sets:
                for k,right in lifted_sets:
                    need(sum(x*y for x,y in zip(left[a],right[a]))==choose(n-2*j,a-j)*sum(v*k.get(J,0) for J,v in h.items()),'complete lifted Gram identity')
                    grams+=1
    need(len(vectors)==sum(len(x) for x in layers.values()),'full original-index dimension')
    orth=0
    for i,(j,a,v) in enumerate(vectors):
        for k,b,w in vectors[i+1:]:
            if a==b and j!=k:need(sum(x*y for x,y in zip(v,w))==0,'cross degree orthogonality');orth+=1
    return {'n':n,'complete_lifted_basis_size':len(vectors),'disjointness_actions':actions,'norm_checks_including_zero_lifts':norms,'complete_Gram_checks':grams,'cross_degree_checks':orth,'basis_method':'triangular ballot matching products'}


def trade_symbolic():
    n=Poly([7,1]);R=(n-2)*(n-3)/2;alpha=R*(2*n-1);negative=-(n-1)*(n-3)
    T0=[[2*(n-1)*R,-(n-1)*R],[-2*R,R]]
    T1=[[-(n-2)*(n-3),(n-2)*(n-3)],[n-3,-(n-3)]]
    need(elementary_traces(T0)==[Poly(1),alpha,Poly(0)],'degree0 trade spectrum')
    need(elementary_traces(T1)==[Poly(1),negative,Poly(0)],'degree1 trade spectrum')
    need(all(sum(x*b for x,b in zip(row,[1,2]))==0 for row in T0),'trade cardinality kernel')
    need(all(sum(row)==0 for row in T1),'trade degree1 star kernel')
    need(all(x>0 for x in (alpha+negative).v),'positive norm dominance')
    N,s=counting(n);next_N,next_s=counting(n+1)
    density_difference=s*next_N-next_s*N
    need(all(x>0 for x in density_difference.v),'density strictly decreases for every n>=7')
    return {'alpha_coefficients_at_n7':alpha.record(),'negative_coefficients_at_n7':negative.record(),'zero_multiplicity':'m-binomial(n,2)','repair_interval':'0<t<=2/((n-2)(n-3)(2*n-1))','density_difference_numerator_at_n7':density_difference.record(),'kernel_bridge':'Ordinary PSD sums on degrees0/2; norm-controlled degree1; strict cap endpoint follows from disjoint equality kernels.'}


def literal_definition(boundary,n=7):
    """Reconstruct E C' E^T directly; compare with all explicit entry cases."""
    B=weights(n,boundary);V=[0]+sum([members(n,a) for a in range(1,6)],[])
    N=len(V);m=N-1;s=sum(comb(n-1,k) for k in range(5));delta=F(n*(n-1)*(n-2)*(n-3),4)
    alpha=F((n-2)*(n-3)*(2*n-1),2);epsilon=F(n,72*m*(n-1)*(n-2)*(n-3));records=[]
    for t in [epsilon,1/alpha]:
        C=[]
        for A in V[1:]:
            a=A.bit_count();row=[]
            for Z in V[1:]:
                b=Z.bit_count();trade=(n-2)*(n-3) if a==b==1 else -(n-3) if {a,b}=={1,2} else 1 if a==b==2 else 0
                row.append(F(s*int(A==Z)-1)+(B[a-1][b-1]+t*trade if not A&Z else 0))
            C.append(row)
        row_sums=[sum(row) for row in C]
        L=[[1+sum(row_sums)]+[1-x for x in row_sums]]
        for i,row in enumerate(C):L.append([1-row_sums[i]]+[1+x for x in row])
        need(all(sum(row)==N for row in L),'literal lifted row sums')
        need(all(L[i][k]==L[k][i] for i in range(N) for k in range(N)),'literal lifted symmetry')
        need(L[0][0]==1+t*delta,'literal empty loop')
        for i,A in enumerate(V[1:],1):
            a=A.bit_count();empty=1-t*F((n-1)*(n-2)*(n-3),2) if a==1 else 1+t*F((n-2)*(n-3),2) if a==2 else F(1)
            need(L[0][i]==empty and empty>0,'literal empty off diagonal')
            for k,Z in enumerate(V[1:],1):
                if A&Z:need(L[i][k]==s*int(i==k),'literal support')
        for point in range(n):
            star=[i for i,A in enumerate(V) if A>>point&1]
            need(len(star)==s and all(sum(row[i] for i in star)==s for row in L),'literal forced stars')
        digest=hashlib.sha256(json.dumps([[str(x) for x in row] for row in L],separators=(',',':')).encode()).hexdigest()
        if t==epsilon:need(digest=='29923513a94555b5a1566f9812704255defb44ff9314b51ee659945334d23717','original literal matrix reproduction')
        bad=[row[:] for row in L];bad[0][0]+=1
        need(sum(bad[0])!=N,'corrupt empty loop must fail')
        records.append({'n':n,'t':str(t),'N':N,'L_sha256':digest,'empty_loop':str(L[0][0]),'empty_singleton':str(L[0][1]),'empty_pair':str(L[0][n+1])})
    return records


def controls():
    cases=[[[0,1],[1,0]],[[-1]],[[1,2],[0,1]]];count=0
    for A in cases:
        try:ldlt_rank(A)
        except ValueError:count+=1
        else:raise ValueError('invalid PSD accepted')
    need(ldlt_rank([[1,1],[1,1]])==1,'singular PSD positive control')
    return count


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write-expected',action='store_true');args=parser.parse_args()
    data=read_witnesses()
    out={'reviewer':'six-reviewer-3','role':'independent mathematical reviewer','input_hashes':INPUT_HASHES,'stable_margins':stable_audit(data['POSITIVITY_CERTIFICATE.json']),'finite_cases':[finite_audit(n,data['BOUNDARY_CERTIFICATES.json']) for n in range(7,13)],'literal_harmonic_completeness':literal_harmonics(),'literal_definition_routes':literal_definition(data['BOUNDARY_CERTIFICATES.json']),'trade_refinement':trade_symbolic(),'rejected_PSD_controls':controls(),'additional_corruption_controls':['altered polynomial sign witness','altered empty loop at both tested repair parameters'],'trust_boundary':'Exact finite and polynomial algebra; ordinary harmonic exhaustion, real-root interpretation, endpoint kernel and rank/equality/tensor proofs are outside a formal kernel.'}
    text=json.dumps(out,indent=2,sort_keys=True)+'\n'
    if args.write_expected:(HERE/'expected.json').write_text(text)
    else:need((HERE/'expected.json').read_text()==text,'complete expected record mismatch')
    print('PASS:34 infinite Newton-trace margins; six exact boundary/stable orders;119 ballot lifts; larger closed repair interval')


if __name__=='__main__':main()
