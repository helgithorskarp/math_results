"""Original q8,k3,kappa0 physical repair Schur forms.

Fixed finite82/84 PD solves, four RHS, no symbolic inverse/cofactor
expansion. One phase per fixed60s process; whole original N=89.
"""
from fractions import Fraction as F
from math import lcm
import sys,json
import inputs
from literal import require,core_data,domain,action
from exact import digest

def solve_pd(A,B):
    n=len(A);r=len(B[0]);require(n in (82,84) and len(B)==n and all(len(row)==r for row in B) and r==4,'bounded physical solve')
    require(all(A[i][j]==A[j][i] for i in range(n) for j in range(n)),'physical symmetric matrix')
    den=lcm(*(x.denominator for row in A+B for x in row))
    a=[[int(x*den) for x in A[i]+B[i]] for i in range(n)]
    require(all(F(a[i][j],den)==x for i in range(n) for j,x in enumerate(A[i]+B[i])),'integral augmented conversion')
    prev=1;pivots=[]
    for h in range(n):
        pivot=a[h][h];require(pivot>0,'strictly positive physical Bareiss pivot')
        pivots.append(pivot)
        for i in range(h+1,n):
            for j in range(h+1,n+r):
                value=pivot*a[i][j]-a[i][h]*a[h][j]
                a[i][j],rem=divmod(value,prev);require(rem==0,'exact augmented Bareiss division')
            a[i][h]=0
        prev=pivot
    result=[[F(0)]*r for _ in range(n)]
    for i in reversed(range(n)):
        for h in range(r):
            result[i][h]=(a[i][n+h]-sum(a[i][j]*result[j][h] for j in range(i+1,n)))/F(a[i][i])
    require(all(sum(A[i][j]*result[j][h] for j in range(n))==B[i][h] for i in range(n) for h in range(r)),'all original physical solve residuals')
    return result,{'PD_rank':n,'denominator':den,'positive_pivot_digest':digest(pivots),'last_pivot_digits':len(str(pivots[-1])),'solution_digest':digest([[str(x) for x in row] for row in result])}


def phase(which,raw=False):
    require(which in ('lower','upper'),'two bounded physical phases only')
    X,N,s,C0,delta,R,U0=core_data(8,3)
    require(X==domain(8,3,scan=True),'literal full membership scan')
    n=N-1;ix={A:i for i,A in enumerate(X[1:])};active=[ix[A] for A in (2,4,3,5)]
    special={1,2,4,3,5};K=[tuple(ix[A] for A in (1,3,5))]+[(i,) for i,A in enumerate(X[1:]) if A not in special]
    require(len(K)==84 and len(active)==4,'full kerR plus four-coordinate complement')
    require(all(sum(R[i][j] for j in group)==0 for i in range(n) for group in K),'every original kerR basis action')
    Ra=[[R[i][j] for j in active] for i in active]
    require(Ra==[[0,0,0,-1],[0,0,-1,0],[0,-1,0,0],[-1,0,0,0]],'full rank-four repair block')
    Sa=[F(bool(A&1)) for A in X[1:]]
    FF=[F(A.bit_count()==3 or A.bit_count()==2 and A&7==A) for A in X[1:]]
    Sb=[F(bool(A&2)) for A in X[1:]];Sc=[F(bool(A&4)) for A in X[1:]]
    z=[1-Sb[i]-Sc[i]+FF[i] for i in range(n)]
    vb=[Sb[i]-FF[i] for i in range(n)];vc=[Sc[i]-FF[i] for i in range(n)]
    require(all(not any(action(C0,v)) for v in (Sa,z,vb,vc)),'all four original zero lower kernel vectors')
    require(all(not any(action(R,v)) for v in (Sa,z)),'unmoved original lower null vectors')
    if which=='lower':
        outside_anchor=next(i for i,g in enumerate(K) if g==(ix[8],))
        require(Sa[ix[1]]==z[ix[1]]==z[ix[8]]==1 and Sa[ix[8]]==0,'determinant-one lower null anchor map')
        K=[g for i,g in enumerate(K) if i not in (0,outside_anchor)]
        target=C0
    else:target=U0
    H=[[sum(target[i][j] for i in a for j in b) for b in K] for a in K]
    B=[[sum(target[i][j] for i in a) for j in active] for a in K]
    Q=[[target[i][j] for j in active] for i in active]
    Y,meta=solve_pd(H,B)
    S=[[Q[i][j]-sum(B[h][i]*Y[h][j] for h in range(len(K))) for j in range(4)] for i in range(4)]
    require(all(S[i][j]==S[j][i] for i in range(4) for j in range(4)),'original Schur symmetry')
    swap=[1,0,3,2]
    require(all(S[i][j]==S[swap[i]][swap[j]] for i in range(4) for j in range(4)),'physical b-c exchange symmetry')
    P=[[1,1,0,0],[0,0,1,1],[1,-1,0,0],[0,0,1,-1]]
    transform=lambda M:[[sum(a[i]*M[i][j]*b[j] for i in range(4) for j in range(4)) for b in P] for a in P]
    T=transform(S);RT=transform(Ra)
    require(all(T[i][j]==0 for i in range(2) for j in range(2,4)),'complete even-odd cross cancellation')
    require(RT==[[0,-2,0,0],[-2,0,0,0],[0,0,0,2],[0,0,2,0]],'both physical two-coordinate repair blocks')
    blocks=[[[str(T[i+offset][j+offset]) for j in range(2)] for i in range(2)] for offset in (0,2)]
    if which=='lower':
        for block,sign in zip(blocks,(1,-1)):
            a,b,c=F(block[0][0]),F(block[0][1]),F(block[1][1]);require(a==c>0 and b==sign*a,'exact rank-one lower forms')
    rec={'agent':'six-downset-3','role':'researcher','q':8,'k':3,'kappa':'0','N':N,'phase':which,'kerR_dimension':84,'null_count':2 if which=='lower' else 0,'PD_compression':meta,
         'active_Schur':[[str(x) for x in row] for row in S],'even_odd_blocks':blocks,'repair_blocks':[[['0','-2'],['-2','0']],[['0','2'],['2','0']]],
         'original_target_digest':digest([[str(x) for x in row] for row in target]),'physical_compression_digest':digest([[str(x) for x in row] for row in H]),
         'all_original_rhs_residuals_verified':True,'physical_full_basis_status':'explicit unimodular map; lower null replacement has anchor determinant1; bridge unformalized','scope':'exact original q8,k3,kappa0 slice only; no global kappa optimality'}
    rec['record_sha256']=digest(rec)
    if raw:return rec,X,K,active,Y
    return rec

if __name__=='__main__':print(json.dumps(phase(sys.argv[1]),sort_keys=True,indent=2))
