"""Literal original vertices and primitive rational Gram; independent h2/h3 checks."""
from fractions import Fraction as F
from itertools import combinations
import argparse, hashlib, json
from pathlib import Path

def require(test,message):
    if not test: raise ValueError(message)

def canonical(obj):
    def encode(x):
        if isinstance(x,F): return [x.numerator,x.denominator]
        if isinstance(x,dict): return {str(k):encode(v) for k,v in sorted(x.items(),key=lambda p:str(p[0]))}
        if isinstance(x,(list,tuple)): return [encode(v) for v in x]
        return x
    return (json.dumps(encode(obj),sort_keys=True,separators=(',',':'))+'\n').encode()

def digest(x): return hashlib.sha256(canonical(x)).hexdigest()

def rank_psd(matrix):
    a=[row[:] for row in matrix]
    n=len(a); rank=0; pivots=[]
    for k in range(n):
        require(a[k][k]>=0,'PSD diagonal')
        if a[k][k]==0:
            require(all(a[k][j]==0 for j in range(k,n)),'zero diagonal must have zero Schur row')
            pivots.append(F(0)); continue
        pivot=a[k][k]; rank+=1; pivots.append(pivot)
        for i in range(k+1,n):
            for j in range(i,n):
                a[i][j]-=a[i][k]*a[k][j]/pivot
                a[j][i]=a[i][j]
    return rank,pivots

def solve(matrix,rhs):
    a=[row[:]+[v] for row,v in zip(matrix,rhs)]
    n=len(a)
    for k in range(n):
        require(a[k][k]!=0,'SPD principal Gaussian pivot')
        for i in range(k+1,n):
            factor=a[i][k]/a[k][k]
            for j in range(k+1,n+1): a[i][j]-=factor*a[k][j]
            a[i][k]=F(0)
    x=[F(0)]*n
    for k in reversed(range(n)):
        x[k]=(a[k][n]-sum((a[k][j]*x[j] for j in range(k+1,n)),F(0)))/a[k][k]
    require(all(sum((matrix[i][j]*x[j] for j in range(n)),F(0))==rhs[i] for i in range(n)),
            'whole original principal solution')
    return x

def original(h,keep_internal=False):
    s,D,ell,N=3*h+4,3*h,6*h+1,12*h+8
    w=F(s-1); s=F(s); D=F(D)
    a=F(3*h*(3*h-1),ell*s*(h-1)); b=-2*a; c=F(9*(3*h-1),ell*s)
    c0=F(3+15*h,ell**2); B2=F(s*(h-1),3*h)
    etaL=w-c0-a*a*B2-2*s*c*c/3
    etaF=w-c0-b*b*B2-2*s*c*c/(3*(h-1))
    p=-1-c0-a*b*B2; mu=(2*p+etaF)/3
    alpha=2*(2*etaL-p-etaF); beta=etaF-mu; nu=2*h*mu/(2*h-1)
    require(mu>0 and alpha>0 and beta>0,'primitive Gram positivity')
    names=[('old',mask) for mask in range(1,8)]
    names += [('B',g,i) for g in range(2) for i in range(h)]
    names += [('T',g,i,j) for g in range(2) for i in range(h) for j in range(3)]
    names += [(kind,g,i) for kind in ['M','WA','WF'] for g in range(2) for i in range(h)]
    index={x:i for i,x in enumerate(names)}
    n=len(names)
    metric=[[F(0)]*n for _ in range(n)]
    for i,x in enumerate(names):
        for j,y in enumerate(names):
            if x[0]!=y[0]: continue
            kind=x[0]
            if kind=='old': value=(4+D)*int(x==y)+(4-D)*int(x[1]+y[1]==7)-1
            elif kind=='B': value=s/3*(F(int(x[2]==y[2]))-F(1,h)) if x[1]==y[1] else F(0)
            elif kind=='T': value=s*(F(int(x[3]==y[3]))-F(1,3)) if x[1:3]==y[1:3] else F(0)
            elif kind=='M': value=nu*(F(int(x==y))-F(1,2*h))
            else: value=(alpha if kind=='WA' else beta)*int(x==y)
            metric[i][j]=value
    def vector(terms):
        v=[F(0)]*n
        for key,coefficient in terms: v[index[key]]+=coefficient
        return v
    def oldvec(coefficients): return vector([(('old',m),F(v)) for m,v in enumerate(coefficients,1)])
    H=[oldvec([-int(mask&(1<<g)!=0) for mask in range(1,8)]) for g in range(2)]
    K=oldvec([1-int(mask&1!=0)-int(mask&2!=0) for mask in range(1,8)])
    z=[-v/ell for v in K]
    rows=[oldvec([int(mask==m) for m in range(1,8)]) for mask in range(1,8)]
    labels=[frozenset(j for j in range(3) if mask&(1<<j)) for mask in range(1,8)]
    roles=[('old',mask) for mask in range(1,8)]
    for kind in ['marked','private']:
        for group in range(2):
            for i in range(h):
                private=[3+2*(group*h+i),4+2*(group*h+i)]
                sets=[{private[0]},{private[1]},set(private)]
                for leaf,base_set in enumerate(sets):
                    terms=[]
                    if kind=='marked':
                        v=[x/D for x in H[group]]
                        terms=[(('B',group,i),F(1)),(('T',group,i,leaf),F(1))]
                        base_set=base_set|{group}
                    else:
                        v=z[:]
                        terms=[(('B',group,i),a if leaf<2 else b),(('M',group,i),F(1))]
                        if leaf<2:
                            terms += [(('T',group,i,1-leaf),c),
                                      (('WA',group,i),F(1 if leaf==0 else -1,2)),
                                      (('WF',group,i),F(-1,2))]
                        else:
                            terms += [(('T',group,j,2),c/(h-1)) for j in range(h) if j!=i]
                            terms += [(('WF',group,i),F(1))]
                    addition=vector(terms)
                    rows.append([x+y for x,y in zip(v,addition)])
                    labels.append(frozenset(base_set)); roles.append((kind,group,i,leaf))
    rows.insert(0,[-sum(row[k] for row in rows) for k in range(n)])
    labels.insert(0,frozenset()); roles.insert(0,('empty',))
    require(len(rows)==N and len(set(labels))==N,'entire original downset')
    require(all(frozenset(subset) in labels for label in labels for k in range(len(label)+1)
                for subset in combinations(label,k)),'original down closure')
    row_metric=[[sum((row[k]*metric[k][j] for k in range(n) if row[k]),F(0))
                 for j in range(n)] for row in rows]
    gram=[[sum((row_metric[i][k]*rows[j][k] for k in range(n) if rows[j][k]),F(0))
           for j in range(N)] for i in range(N)]
    require(all(sum(row,F(0))==0 for row in gram),'whole empty negative-row lift')
    require(gram[0][0]==c0,'actual empty diagonal')
    require(all(gram[i][i]==w for i in range(1,N)),'every nonempty diagonal')
    require(all(gram[i][j]==-1 for i in range(N) for j in range(N)
                if i!=j and labels[i]&labels[j]),'every original intersecting pair')
    seed_rank,seed_pivots=rank_psd(gram)
    require(seed_rank==N-4,'whole seed rank')
    seed_cap=[[F(N*int(i==j)-1)-gram[i][j] for j in range(N)] for i in range(N)]
    cap_rank,seed_cap_pivots=rank_psd(seed_cap)
    require(cap_rank==N-1,'whole seed cap rank')
    # Verify the stronger seed floor claimed in the written argument.
    floor=[[F((N-1)*int(i==j))-F(N-1,N)-gram[i][j] for j in range(N)] for i in range(N)]
    require(rank_psd(floor)[0]==N-1,'whole seed floor P')
    last=roles.index(('private',1,h-1,2))
    retained=[i for i in range(1,N) if roles[i] not in [('old',1),('old',2)] and i!=last]
    principal=[[gram[i][j] for j in retained] for i in retained]
    require(rank_psd(principal)[0]==N-4,'whole retained original SPD principal')
    r=[F(int(roles[i][:3]==('private',0,0))) for i in retained]
    solved=solve(principal,r)
    kappa=sum((x*y for x,y in zip(r,solved)),F(0))
    require(kappa==2/nu+4/beta,'original principal inverse kappa')
    coeff=[]
    for i in retained:
        role=roles[i]
        if role[0]=='private': coefficient=F(-1)
        elif role[0]=='old': coefficient=-F(6*h,ell)*(1-int(role[1]&1!=0)-int(role[1]&2!=0))
        else: coefficient=F(0)
        coeff.append(coefficient)
    bc=[sum((principal[i][j]*coeff[j] for j in range(N-4)),F(0)) for i in range(N-4)]
    require(bc==[gram[i][last] for i in retained],'whole deleted original column')
    require(sum((x*y for x,y in zip(coeff,bc)),F(0))==w and
            sum((x*y for x,y in zip(r,coeff)),F(0))==-3,'deleted norm and repair cross term')
    u=[F(0)]*N; v=[F(0)]*N
    for leaf in range(3): u[roles.index(('private',0,0,leaf))]=1
    u[0]=-3; v[last]=1; v[0]=-1
    dot=lambda x,y: sum((i*j for i,j in zip(x,y)),F(0))
    require(dot(u,u)==12 and dot(v,v)==2 and dot(u,v)==3 and sum(u)==sum(v)==0,
            'whole repair norm and unit-orthogonality')
    runs=[]
    for name,delta,loss_constant in [
        ('author',1/(4*(8+kappa)),F(8)),
        ('reviewer_larger',1/(4*(F(79,10)+kappa/6)),F(79,10))]:
        change=[[delta*(u[i]*v[j]+v[i]*u[j]) for j in range(N)] for i in range(N)]
        repaired=[[gram[i][j]+change[i][j] for j in range(N)] for i in range(N)]
        L=[[1+repaired[i][j] for j in range(N)] for i in range(N)]
        M=[[(L[i][j]-s*int(i==j))/(N-s) for j in range(N)] for i in range(N)]
        require(all(sum(row,F(0))==1 for row in M),'all original unit rows after repair')
        require(all(M[i][j]==0 for i in range(N) for j in range(N)
                    if labels[i]&labels[j]),'all original support including diagonals after repair')
        stars=[]
        for mark in range(2):
            indicator=[F(int(mark in label))-s/N for label in labels]
            require(sum(int(mark in label) for label in labels)==s,'literal maximum star size')
            require(all(sum((L[i][j]*indicator[j] for j in range(N)),F(0))==0
                        for i in range(N)),'entire centered star kernel after repair')
            stars.append(indicator)
        lower_rank,lower_pivots=rank_psd(L)
        cap=[[F(N*int(i==j)-1)-repaired[i][j] for j in range(N)] for i in range(N)]
        upper_rank,upper_pivots=rank_psd(cap)
        margin=1-loss_constant*delta
        gap_matrix=[[cap[i][j]-margin*(F(int(i==j))-F(1,N)) for j in range(N)] for i in range(N)]
        gap_rank,gap_pivots=rank_psd(gap_matrix)
        require(lower_rank==N-2 and upper_rank==N-1 and gap_rank==N-1 and margin>F(3,4),
                'all original repaired ranks and unit-M gap')
        require(6*delta-kappa*delta*delta>0,'whole exact principal Schur margin')
        runs.append(dict(name=name,delta=delta,schur=6*delta-kappa*delta*delta,
                         cap_floor=margin,unit_M_gap=margin/(N-s),
                         lower_rank=lower_rank,cap_rank=upper_rank,
                         whole_Q_digest=digest(repaired),whole_L_digest=digest(L),whole_M_digest=digest(M),
                         whole_gap_digest=digest(gap_matrix),lower_pivots=lower_pivots,
                         cap_pivots=upper_pivots,gap_pivots=gap_pivots,stars=stars))
    require(runs[1]['delta']/runs[0]['delta']>F(80,79),'strict larger rational repair amplitude')
    record=dict(h=h,N=N,s=s,ground=4*h+3,original_labels=[sorted(x) for x in labels],
                primitive_names=names,primitive_gram_digest=digest(metric),
                whole_row_coordinate_digest=digest(rows),whole_seed_Q_digest=digest(gram),
                seed_pivots=seed_pivots,seed_cap_pivots=seed_cap_pivots,
                kappa=kappa,principal_inverse_r=solved,deleted_coefficients=coeff,
                deleted_column=bc,u=u,v=v,repairs=runs)
    if keep_internal: return record,dict(names=names,metric=metric,rows=rows)
    return record

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    record=dict(schema='reviewer5-q4-balanced-original-vertices-v1',controls=[original(2),original(3)])
    payload=canonical(record); args.output.write_bytes(payload)
    print(json.dumps(dict(status='every original entry/support/row/star/PSD/principal checked',
                          whole_record_bytes=len(payload),whole_record_sha256=hashlib.sha256(payload).hexdigest()),sort_keys=True))

if __name__=='__main__': main()
