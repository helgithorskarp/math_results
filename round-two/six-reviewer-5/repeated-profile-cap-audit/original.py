"""Fresh exact original-vertex audit, including the rebuilt empty row/loop."""
import hashlib,json
from fractions import Fraction as F
from frame import build,DIM

def solve(a,b):
    a=[list(row)+[v] for row,v in zip(a,b)]
    for k in range(len(a)):
        p=next(i for i in range(k,len(a)) if a[i][k]);a[k],a[p]=a[p],a[k]
        c=a[k][k];a[k]=[v/c for v in a[k]]
        for i in range(len(a)):
            if i!=k:
                c=a[i][k]
                if c:a[i]=[x-c*y for x,y in zip(a[i],a[k])]
    return [r[-1] for r in a]
def psd_rank(a):
    a=[list(row) for row in a];rank=0
    while a:
        p=max(range(len(a)),key=lambda i:a[i][i]);diagonal=a[p][p]
        if diagonal<0:raise ValueError('negative PSD pivot')
        if not diagonal:
            if any(any(x for x in row) for row in a):raise ValueError('zero diagonal with nonzero coupling')
            break
        indices=[i for i in range(len(a)) if i!=p]
        a=[[a[i][j]-a[i][p]*a[p][j]/diagonal for j in indices] for i in indices];rank+=1
    return rank
def canonical_matrix(a):return [[str(x) for x in row] for row in a]
def digest(a):return hashlib.sha256(json.dumps(canonical_matrix(a),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def lift(c):
    sums=[sum(row) for row in c];total=sum(sums)
    return [[total]+[-x for x in sums]]+[[ -sums[i]]+row[:] for i,row in enumerate(c)]
def fixture(n):
    q=2**(n-1);m=build(F(q));N=2*q+18;s=q+6;h=q+12
    old=list(range(1,2*q));full=2*q-1
    marks=[0,0,1];private_masks=[];marked_masks=[]
    for i,mark in enumerate(marks):
        pair=[1<<(n+2*i),1<<(n+2*i+1)]
        for a in [pair[0],pair[1],pair[0]|pair[1]]:
            private_masks.append(a);marked_masks.append(a|(1<<mark))
    vertices=[0]+old+marked_masks+private_masks
    direct=set(range(2*q))
    for i,mark in enumerate(marks):
        bits=[mark,n+2*i,n+2*i+1]
        direct.update(sum(1<<bits[j] for j in range(3) if mask>>j&1) for mask in range(8))
    if set(vertices)!=direct or len(vertices)!=N:raise ValueError('actual domain census')
    vectors=m['marked']+m['private'];c=[]
    for i,A in enumerate(old):
        row=[]
        for j,B in enumerate(old):
            row.append(F(s if i==j else q-6 if A!=full and B!=full and A^B==full else 0)-1)
        moments=[1 if A!=full else -(q-1),0 if A!=full else -6,
                 6*(1-2*bool(A&1)) if A!=full else 0,
                 6*(1-2*bool(A&2)) if A!=full else 0]
        row += [sum(v[j]*moments[j] for j in range(4)) for v in vectors]
        c.append(row)
    for i,v in enumerate(vectors):
        c.append([c[j][len(old)+i] for j in range(len(old))]+[m['dot'](v,w) for w in vectors])
    W=[[m['dot'](v,w) for w in m['residual']] for v in m['residual']]
    kappa=sum(solve([row[:8] for row in W[:8]],[F(1) if i<3 else F(0) for i in range(8)])[:3])
    if kappa!=m['kappa']:raise ValueError('deleted inverse kappa')
    delta=1/(4*(8+kappa));sharp=[row[:] for row in c];start=len(old)+9
    for i in range(3):sharp[start+i][start+8]+=delta;sharp[start+8][start+i]+=delta
    seedQ=lift(c);sharpQ=lift(sharp)
    pp=[F(-3)]+[F(1) if start<=i<start+3 else F(0) for i in range(N-1)]
    vv=[F(-1)]+[F(1) if i==start+8 else F(0) for i in range(N-1)]
    if sum(x*x for x in pp)!=12 or sum(x*x for x in vv)!=2 or sum(x*y for x,y in zip(pp,vv))!=3:raise ValueError('whole repair vectors')
    for i in range(N):
        for j in range(N):
            if sharpQ[i][j]-seedQ[i][j]!=delta*(pp[i]*vv[j]+vv[i]*pp[j]):raise ValueError('whole lift perturbation')
    P=[[F(i==j)-F(1,N) for j in range(N)] for i in range(N)]
    records=[]
    for label,Q,core,expected_rank in [('seed',seedQ,c,N-2),('sharp',sharpQ,sharp,N-1)]:
        L=[[1+Q[i][j] for j in range(N)] for i in range(N)]
        M=[[(L[i][j]-s*(i==j))/h for j in range(N)] for i in range(N)]
        if any(sum(row)!=1 for row in M):raise ValueError('original row one')
        if any(M[i][j] for i,A in enumerate(vertices) for j,B in enumerate(vertices) if A&B):raise ValueError('mandatory original support')
        if any(M[i][j]!=M[j][i] for i in range(N) for j in range(N)):raise ValueError('symmetry')
        rank=psd_rank(L)
        if rank!=expected_rank or psd_rank(core)!=expected_rank-1:raise ValueError('original lower ranks')
        upper=[[N*P[i][j]-Q[i][j] for j in range(N)] for i in range(N)]
        if psd_rank(upper)!=N-1:raise ValueError('whole original upper rank')
        # Stronger margin verified exactly on literal samples; all-order proof is separate.
        margin=F(2) if label=='seed' else F(7,4)
        if psd_rank([[upper[i][j]-margin*P[i][j] for j in range(N)] for i in range(N)])!=N-1:
            raise ValueError('literal stronger cap gap')
        star=[F(bool(A&1))-F(s,N) for A in vertices]
        if any(sum(row[j]*star[j] for j in range(N)) for row in L):raise ValueError('forced star kernel')
        sorted_indices=sorted(range(N),key=vertices.__getitem__)
        records.append(dict(label=label,rank_lower=rank,rank_upper=N-1,
            complete_positions=N*N,hash_original_M_sorted_by_mask=digest([[M[i][j] for j in sorted_indices] for i in sorted_indices]),
            empty_loop=str(M[0][0]),gap_checked=str(margin)))
    # The specific invalid repair that keeps the old empty coordinates must fail row one.
    bad=[row[:] for row in sharpQ];bad[0]=seedQ[0][:]
    for i in range(N):bad[i][0]=seedQ[i][0]
    if all(sum(row)==0 for row in bad):raise ValueError('retained old empty damage accepted')
    return dict(n=n,q=q,N=N,s=s,h=h,kappa=str(kappa),delta=str(delta),
        original_vertices=vertices,records=records,whole_repair_positions=N*N,
        private_gram_rank=psd_rank(W),repair_schur=str(6*delta-kappa*delta*delta),
        invalid_retained_empty_rejected=True)

if __name__=='__main__':
    print(json.dumps(dict(fixtures=[fixture(n) for n in (3,4,5)]),sort_keys=True))
