"""Independent near-cube partition, intertwiner and spectral certificates.

Actual agent six-reviewer-1, independent mathematical reviewer.
CPython3.11+ standard library. No author executable/fixture is imported.
All-order conclusions require REVIEW.md; finite checks do not prove them.
"""
import argparse
from fractions import Fraction as F
from functools import reduce
from itertools import permutations, product
import hashlib
import json
from math import gcd, lcm
from pathlib import Path


def need(value, label):
    if not value:
        raise ValueError(label)


class P:
    """Sparse integer polynomials in n,t,z,l; no symbolic package."""
    def __init__(self, value=0):
        self.d = {k: v for k, v in value.items() if v} if isinstance(value, dict) else ({(0,0,0,0): value} if value else {})
    def __add__(self, other):
        other = other if isinstance(other, P) else P(other)
        d = self.d.copy()
        for k,v in other.d.items(): d[k] = d.get(k,0)+v
        return P(d)
    __radd__ = __add__
    def __neg__(self): return P({k:-v for k,v in self.d.items()})
    def __sub__(self, other): return self+-P(other) if not isinstance(other,P) else self+-other
    def __rsub__(self, other): return P(other)+-self
    def __mul__(self, other):
        other = other if isinstance(other,P) else P(other)
        d = {}
        for a,x in self.d.items():
            for b,y in other.d.items():
                k = tuple(u+v for u,v in zip(a,b));d[k] = d.get(k,0)+x*y
        return P(d)
    __rmul__ = __mul__
    def __pow__(self, power):
        out = P(1)
        for _ in range(power): out = out*self
        return out
    def __eq__(self, other): return self.d == (other if isinstance(other,P) else P(other)).d
    def evaluate(self, values):
        return sum(c*reduce(lambda a,b:a*b,(v**e for v,e in zip(values,k)),1) for k,c in self.d.items())
    def records(self): return [[list(k),v] for k,v in sorted(self.d.items())]


def determinant_permutations(a):
    out = 0
    for perm in permutations(range(len(a))):
        sign = (-1)**sum(perm[i]>perm[j] for i in range(len(a)) for j in range(i+1,len(a)))
        out += sign*reduce(lambda x,y:x*y,(a[i][perm[i]] for i in range(len(a))),1)
    return out


def bareiss(a):
    need(a and all(len(r)==len(a) for r in a), 'square determinant input')
    need(all(type(x) is int for r in a for x in r), 'integer determinant input')
    a = [r[:] for r in a];previous = 1;sign = 1
    for k in range(len(a)-1):
        pivot = next((i for i in range(k,len(a)) if a[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];sign=-sign
        d=a[k][k]
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                numerator = d*a[i][j]-a[i][k]*a[k][j]
                need(numerator%previous==0,'Bareiss exact division')
                a[i][j]=numerator//previous
            a[i][k]=0
        previous=d
    return sign*a[-1][-1]


def quotient(n,t,z):
    p,s,q,N=2*t-n-1,2*t-n,t-2,4*t-n-1
    K=s*(n-2)**2-(n-1)*(n-3)
    D=(n-1)*((n-4)*q+2*(n-3))
    H=N-n*s+((n-1)*q-p)*z
    A=n-1-(n-1)*z
    B=n*((n+1)*t-n*n+n-2)
    return [[K-D*z,n*H,2*p*(n-1)-p*(n-2)*z,A*n*p+z*B],
            [H,n*s-(n-1)*q*z,p*z,(n-1)*q*z],
            [A,n*z,2*s-z,n*(s-z)],
            [z,-z,0,z]]


def symbolic():
    n,t,z,l=[P({tuple(int(i==j) for i in range(4)):1}) for j in range(4)]
    N=4*t-n-1;p=2*t-n-1
    T=p*(n*n-3*n+4)+2-(n-1)*(n-3)*t*z
    J=4*t*t-(n*n-2*n+5)*t+1
    Q=quotient(n,t,z)
    char=determinant_permutations([[l*int(i==j)-Q[i][j] for j in range(4)] for i in range(4)])
    expected=l*(l-N)*(l*l-T*l+J*z*(2-z))
    need(char==expected,'universal full quotient characteristic polynomial')
    q3=[[13-6*z,-20+12*z,18-6*z],[-5+3*z,16-6*z,3*z],[3-z,2*z,8-z]]
    char3=determinant_permutations([[l*int(i==j)-q3[i][j] for j in range(3)] for i in range(3)])
    need(char3==l*(l-11)*(l-13*(2-z)),'exceptional n4 characteristic polynomial')
    R=(n-1)*2*t-n**3+2*n*n-1
    T2=p*(n*n-3*n+4)+2-2*(n-1)*(n-3)*t
    need(T2-N==R,'exact optimal excess identity')
    need((T2-N)-((n-2)*2*t-(n-1)**3+1)==2*t-n*n+3*n-3,'spectral versus empty witness gap')
    return {'universal_quotient_polynomial':char.records(),'exceptional_n4_polynomial':char3.records(),
            'T':T.records(),'J':J.records(),'optimal_excess':R.records(),'identities':4}


def counts(n):
    need(type(n) is int and n>=4,'n>=4')
    t=2**(n-2);p=2*t-n-1;s=p+1;N=4*t-n-1;q=t-2
    return p,s,N,q,t


def partition_matrices(n):
    """Construct the family from literal clique partitions, in bitmask order."""
    p,s,N,q,t=counts(n);allbits=2**n-1
    labels=[a for a in range(1,2**n) if a.bit_count()<=n-2]
    ix={a:i for i,a in enumerate(labels)};singles=[1<<i for i in range(n)]
    pairs=[(a,allbits^a) for a in labels if a.bit_count()>=2 and a&(1<<(n-1))]
    need(len(labels)==N-1 and len(pairs)==p,'complete bitmask domain')
    base=[singles]+[list(pair) for pair in pairs]
    partitions=[base]
    for a,b in pairs:
        partitions.append([[a]+[v for v in singles if not a&v],
                           [b]+[v for v in singles if not b&v]]+
                          [list(pair) for pair in pairs if pair!=(a,b)])
    def cc(part):
        need(len(part)==s and sorted(v for block in part for v in block)==labels,'partition coverage')
        out=[[0]*len(labels) for _ in labels]
        for block in part:
            need(block and all(not a&b for a in block for b in block if a!=b),'disjoint clique classes')
            for a in block:
                for b in block:out[ix[a]][ix[b]]=1
        return out
    co0=cc(base);total=[[0]*len(labels) for _ in labels]
    for part in partitions:
        co=cc(part)
        for i,row in enumerate(co):
            for j,v in enumerate(row):total[i][j]+=v
    C0=[[s*v-1 for v in row] for row in co0]
    C1=[[v-1 for v in row] for row in total]
    return labels,pairs,C0,C1


def core(n,z,labels,C0,C1):
    p,s,N,q,t=counts(n);allbits=2**n-1
    C=[[(1-z)*a+z*b for a,b in zip(x,y)] for x,y in zip(C0,C1)]
    for i,a in enumerate(labels):
        for j,b in enumerate(labels):
            value=(s if a==b else s-q*z if a.bit_count()==b.bit_count()==1 else
                   z*int(not a&b) if min(a.bit_count(),b.bit_count())==1 else
                   (s-z)*int(a^b==allbits))
            need(C[i][j]+1==value,'all architecture entries from partitions')
    return C


def lower(C):
    K=[[1+x for x in r] for r in C];N=len(K)+1
    empty=[N-sum(r) for r in K]
    return [[N-sum(empty)]+empty]+[[empty[i]]+r for i,r in enumerate(K)]


def multiply(a,v):
    entries=[(i,x) for i,x in enumerate(v) if x]
    return [sum(row[i]*x for i,x in entries) for row in a]


def nullbasis(a):
    a=[[F(x) for x in r] for r in a];row=0;pivots=[]
    for col in range(len(a[0])):
        hit=next((i for i in range(row,len(a)) if a[i][col]),None)
        if hit is None:continue
        a[row],a[hit]=a[hit],a[row];d=a[row][col];a[row]=[x/d for x in a[row]]
        for i in range(len(a)):
            if i!=row and a[i][col]:
                d=a[i][col];a[i]=[x-d*y for x,y in zip(a[i],a[row])]
        pivots.append(col);row+=1
        if row==len(a):break
    basis=[]
    for col in range(len(a[0])):
        if col in pivots:continue
        v=[F(0)]*len(a[0]);v[col]=F(1)
        for i,c in enumerate(pivots):v[c]=-a[i][col]
        scale=lcm(*(x.denominator for x in v));basis.append([int(scale*x) for x in v])
    return row,basis


def family_check(n,z,labels,pairs,C0,C1):
    p,s,N,q,t=counts(n);C=core(n,z,labels,C0,C1);L=lower(C);full=[0]+labels
    need(all(sum(r)==N for r in L),'full row sums with empty loop')
    need(all(L[i][j]==L[j][i] for i in range(N) for j in range(N)),'full symmetry')
    for i,a in enumerate(full):
        for j,b in enumerate(full):
            if a&b:need(L[i][j]==s*int(i==j),'full supported M')
    for point in range(n):
        star=[N*int(bool(a&(1<<point)))-s for a in full]
        need(multiply(L,star)==[0]*N,'forced full centered star')
    sign=[[2*int(bool(a&(1<<i)))-1 for a,b in pairs] for i in range(n)]
    need(all(sum(x*y for x,y in zip(sign[i],sign[j]))==2*q*int(i==j)-(n-3)
             for i in range(n) for j in range(n)),'full sign Gram')
    vectors=0
    def eigen(v,e):
        nonlocal vectors
        need(multiply(L,v)==[e*x for x in v],'literal spectral intertwiner');vectors+=1
    for i in range(n-1):
        weights=[int(j==i)-int(j==n-1) for j in range(n)]
        v=[0]+[q*weights[a.bit_length()-1] if a.bit_count()==1 else
                 -sum(weights[j] for j in range(n) if a&(1<<j)) for a in labels]
        eigen(v,z*(q+1))
    for a,b in pairs[1:]:
        c,d=pairs[0];eigen([int(x==a or x==b)-int(x==c or x==d) for x in full],2*s-z)
    rank,basis=nullbasis(sign)
    need(rank==n-int(n==4) and len(basis)==p-rank,'complete sign nullspace')
    for weights in basis:
        mapping={}
        for w,(a,b) in zip(weights,pairs):mapping[a]=w;mapping[b]=-w
        eigen([mapping.get(x,0) for x in full],z)
    columns=[[int(a==0) for a in full],[int(a.bit_count()==1) for a in full],
             [int(a.bit_count()>=2) for a in full]]
    if n>=5:columns.append([a.bit_count()*int(a.bit_count()>=2) for a in full])
    Q=quotient(n,t,z) if n>=5 else [[13-6*z,-20+12*z,18-6*z],[-5+3*z,16-6*z,3*z],[3-z,2*z,8-z]]
    for j,col in enumerate(columns):
        need(multiply(L,col)==[sum(columns[k][i]*Q[k][j] for k in range(len(columns))) for i in range(N)],'full quotient lift')
    return C,L,{'n':n,'z':str(z),'N':N,'sign_rank':rank,'complete_sign_nullity':len(basis),'nonzero_block_basis_vectors':vectors,'quotient_dimension':len(columns)}


def expected_det(n,z,scale,ell):
    p,s,N,q,t=counts(n)
    if n==4:return ell**4*(ell-scale*N)*(ell-scale*3*z)**3*(ell-scale*(8-z))**2*(ell-scale*13*(2-z))
    T=p*(n*n-3*n+4)+2-(n-1)*(n-3)*t*z;J=4*t*t-(n*n-2*n+5)*t+1
    return ell**n*(ell-scale*N)*(ell-scale*z*(q+1))**(n-1)*(ell-scale*(2*s-z))**(p-1)*(ell-scale*z)**(p-n)*(ell*ell-scale*T*ell+scale*scale*J*z*(2-z))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',type=Path);args=parser.parse_args()
    sym=symbolic();backend=0
    for a,b,c,d,e,f in product((-1,0,1),repeat=6):
        matrix=[[a,b,c],[b,d,e],[c,e,f]]
        need(bareiss(matrix)==determinant_permutations(matrix),'Bareiss versus Leibniz');backend+=1
    rows=[];dets=[];digests=[]
    for n in range(4,9):
        labels,pairs,C0,C1=partition_matrices(n)
        for z in [F(0),F(1),F(2),F(3,2)]:
            C,L,row=family_check(n,z,labels,pairs,C0,C1);rows.append(row)
            data=json.dumps([[str(x) for x in r] for r in L],separators=(',',':')).encode()
            digests.append({'n':n,'z':str(z),'lower_sha256':hashlib.sha256(data).hexdigest()})
            if n<=6:
                scale=z.denominator;integer=[[int(scale*x) for x in r] for r in L]
                for ell in [-1,-3]:
                    got=bareiss([[ell*int(i==j)-integer[i][j] for j in range(len(integer))] for i in range(len(integer))])
                    need(got==expected_det(n,z,scale,ell),'full determinant versus complete spectrum')
                    dets.append({'n':n,'z':str(z),'scale':scale,'ell':ell,'determinant':str(got)})
    scalar=[]
    for n in range(5,81):
        p,s,N,q,t=counts(n);T0=p*(n*n-3*n+4)+2;b=(n-1)*(n-3)*t;T2=T0-2*b
        J=4*t*t-(n*n-2*n+5)*t+1
        need(T2>0 and J>0 and b*T2>2*J,'endpoint Rayleigh strictness')
        if n>=6:
            R=(n-1)*2**(n-1)-n**3+2*n*n-1
            need(R==T2-N>0,'optimal cap failure')
            nextR=n*2**n-(n+1)**3+2*(n+1)**2-1
            need(nextR-2*R==2**n+n**3-5*n*n+n+2,'all-orders excess recurrence')
            need(T2>N>max(2*s-2,2*(q+1),2),'largest endpoint eigenvalue')
            scalar.append({'n':n,'T2':T2,'excess':str(F(R,N-s))})
    controls=0
    def rejects(operation):
        try:operation()
        except (ValueError,TypeError):return True
        return False
    need(rejects(lambda:bareiss([[1,2],[3]])),'reject nonsquare');controls+=1
    need(rejects(lambda:bareiss([[F(1,2)]])),'reject fractional determinant input');controls+=1
    n=5;labels,pairs,C0,C1=partition_matrices(n);L=lower(C1);old=[r[:] for r in L];L[0][0]+=1
    need(L!=old and any(sum(r)!=len(L) for r in L),'reject damaged empty loop');controls+=1
    bad=quotient(5,8,F(1));bad[0][0]+=1
    good=quotient(5,8,F(1))
    need(determinant_permutations([[-int(i==j)-bad[i][j] for j in range(4)] for i in range(4)])!=determinant_permutations([[-int(i==j)-good[i][j] for j in range(4)] for i in range(4)]),'reject changed quotient');controls+=1
    result={'agent':'six-reviewer-1','role':'independent mathematical reviewer','arithmetic':'CPython3.11+ integer/Fraction, sparse Z[n,t,z,l]','symbolic':sym,'literal_family_intertwiners':rows,'full_lower_matrix_hashes':digests,'full_determinants':dets,'determinant_backend_controls':backend,'rejected_controls':controls,'optimal_excess_scalar_checks':scalar,'all_order_trust':'Written decomposition and Rayleigh proof in REVIEW.md; no inference from finite checks.'}
    data=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.check:need(args.check.read_text()==data,'complete expected output comparison')
    print(data,end='')


if __name__=='__main__':main()
