"""Independent original-set audit of LEMMA9361; no target-code imports.

Defining formulae are credited to the public proof. Physical sets, sparse
Gram congruence, rational pivoting, complete kernel and literal clique census
are reviewer implementations. CPython 3.11+, standard library, assert-free.
"""
from fractions import Fraction as F
from itertools import combinations
import argparse,json,signal
from linear import need,psd,mv,dot,digest,canonical

def rank(A):
    return len(rref(A)[1])

def rref(A):
    B=[[F(x) for x in row] for row in A]; m=len(B)
    n=len(B[0]) if m else 0; piv=[];r=0
    for col in range(n):
        p=next((i for i in range(r,m) if B[i][col]),None)
        if p is None:continue
        B[r],B[p]=B[p],B[r];d=B[r][col];B[r]=[x/d for x in B[r]]
        for i in range(m):
            if i!=r and B[i][col]:
                d=B[i][col];B[i]=[x-d*y for x,y in zip(B[i],B[r])]
        piv.append(col);r+=1
        if r==m:break
    return B,piv

def nullspace(A):
    B,piv=rref(A);n=len(A[0]);free=[j for j in range(n) if j not in piv]
    out=[]
    for j in free:
        v=[F(0)]*n;v[j]=1
        for i,p in enumerate(piv):v[p]=-B[i][j]
        need(all(x==0 for x in mv(A,v)),'nullspace residual');out.append(v)
    return out

def downset(sets):
    need(0 in sets and len(set(sets))==len(sets),'actual unique empty vertex')
    for a in sets:
        need(type(a) is int and a>=0,'literal bit mask')
        b=a
        while True:
            need(b in sets,'downward closure')
            if b==0:break
            b=(b-1)&a

def stars(sets):
    support=0
    for a in sets:support|=a
    bits=[1<<i for i in range(support.bit_length()) if support>>i&1]
    return {b:sum(bool(a&b) for a in sets) for b in bits}

def core_check(sets,C,t):
    downset(sets);st=stars(sets);need(st and max(st.values())==t,'true private star')
    v=[a for a in sets if a];need(len(C)==len(v),'core dimension')
    for i,a in enumerate(v):
        need(C[i][i]==t-1,'private norm')
        for j,b in enumerate(v):
            if i!=j and a&b:need(C[i][j]==-1,'private intersection')
    return psd(C)

def cube(h):
    need(h>=1,'nontrivial cube');S=list(range(1<<h));v=S[1:];t=1<<(h-1);full=(1<<h)-1
    C=[[F(t*(a==b)+t*(a^b==full)-1) for b in v] for a in v]
    return S,C,t

def singles(h):
    S=[0]+[1<<i for i in range(h)];return S,[[F(0)]*h for _ in range(h)],1

def uniform_two(h):
    need(h>=3,'uniform baseline order');S=[0]+[1<<i for i in range(h)]
    S += [(1<<i)|(1<<j) for i,j in combinations(range(h),2)];v=S[1:]
    C=[[F(h-1) if a==b else F(-1) if a&b or a.bit_count()==b.bit_count()==1
        else F(2,h-2) for b in v] for a in v]
    return S,C,h

def partition(h,edges,colors):
    S=[0]+[1<<i for i in range(h)]+[(1<<i)|(1<<j) for i,j in edges]
    t=max(stars(S).values());need(len(colors)==len(S)-1 and set(colors)==set(range(t)),'private classes')
    for i,a in enumerate(S[1:]):
        for j,b in enumerate(S[1:]):
            if i!=j and colors[i]==colors[j]:need(a&b==0,'private disjoint class')
    return S,[[F(t*(a==b)-1) for b in colors] for a in colors],t

def relocate(S,offset):return [a<<offset for a in S]

def build(n,inputs):
    need(2<=n<=6 and inputs,'guarded nonempty old cube');q=1<<(n-1)
    old=list(range(1,2*q));offset=n;families=[];labels=[('old',-1,a) for a in old]
    masks=list(old);load=[0]*n;priv=[]
    for j,(mark,data) in enumerate(inputs):
        need(0<=mark<n,'old mark');S,C,t=data;info=core_check(S,C,t)
        need(t<=q,'star bound');width=max(S).bit_length();Y=((1<<width)-1)<<offset
        raw=relocate(S,offset);offset+=width;v=raw[1:]
        need(all(a for a in v),'private rows');d=len(v);load[mark]+=d
        try:
            psd([[F(len(S)*(a==b)-1)-c for b,c in enumerate(row)] for a,row in enumerate(C)])
            capped=True
        except ValueError:capped=False
        families.append({'mark':mark,'sets':raw,'core':C,'t':t,'d':d,'info':info,'Y':Y,'capped':capped})
        for a in v:labels.append(('marked',j,a));masks.append(a|(1<<mark))
        for a in v:labels.append(('private',j,a));masks.append(a)
        priv.append(v)
    need(len(masks)+1<=80,'whole dimension guard');need(len(set(masks))==len(masks),'private supports')
    downset([0]+masks);D=max(load);s=q+D;m=sum(load);N=2*q+2*m
    heavy=[i for i,d in enumerate(load) if d==D];k=len(heavy);no=len(old);nt=len(labels)
    need(N==nt+1 and max(stars([0]+masks).values())==s and 0<s<=N//2,'whole size/star')
    oldC=[[F((q+D)*(a==b)+(q-D)*(a^b==2*q-1)-1) for b in old] for a in old]
    old_info=psd(oldC);need(old_info['rank']==no,'old positive definite')
    local=[{a:i for i,a in enumerate(v)} for v in priv]
    R=[[[F(q+D,q)*(c+F(q-f['t'])*(a==b)) for b,c in enumerate(row)]
        for a,row in enumerate(f['core'])] for f in families]
    C=[[F(0)]*nt for _ in range(nt)]
    # Literal physical entry table, independently indexed by actual set masks.
    for a,(kind,j,T) in enumerate(labels):
        for b,(other,l,U) in enumerate(labels):
            if kind==other=='old':value=oldC[a][b]
            elif kind=='old':
                mark=families[l]['mark'];value=F(1-2*bool(T&(1<<mark)))
                if other=='private':value=-F(D,q)*value
            elif other=='old':
                mark=families[j]['mark'];value=F(1-2*bool(U&(1<<mark)))
                if kind=='private':value=-F(D,q)*value
            else:
                same=families[j]['mark']==families[l]['mark']
                if kind==other=='marked':value=F(s*(a==b)-1) if same else F(0)
                elif kind==other=='private':
                    value=F(D,q)*same
                    if j==l:value+=R[j][local[j][T]][local[l][U]]
                else:value=F(-int(same))
            C[a][b]=value
    # Separate sparse projection/congruence in the physical old-row basis.
    P=[]
    for kind,j,T in labels:
        if kind=='old':P.append({old.index(T):F(1)})
        else:
            mark=families[j]['mark'];scale=-F(1,D) if kind=='marked' else F(1,q)
            P.append({i:scale for i,A in enumerate(old) if A&(1<<mark)})
    PA=[[sum(v*oldC[i][b] for i,v in row.items()) for b in range(no)] for row in P]
    G=[[sum(PA[a][i]*v for i,v in P[b].items()) for b in range(nt)] for a in range(nt)]
    for a,(kind,j,T) in enumerate(labels):
        for b,(other,l,U) in enumerate(labels):
            if kind==other=='marked' and families[j]['mark']==families[l]['mark']:
                G[a][b]+=F(s)*((a==b)-F(1,D))
            if kind==other=='private' and j==l:G[a][b]+=R[j][local[j][T]][local[j][U]]
    need(C==G,'literal/congruence complete entry equality')
    check=core_check([0]+masks,C,s)
    # Independently parameterized full nonempty kernel, including equality inputs.
    kernels=[]
    for i in heavy:kernels.append([F(bool(a&(1<<i))) for a in masks])
    private_nullities=[]
    for j,f in enumerate(families):
        K=nullspace(f['core']);private_nullities.append(len(K))
        if f['t']==q:
            for v in K:
                total=sum(v);z=[F(0)]*nt
                for a,(kind,l,T) in enumerate(labels):
                    if kind=='old' and T&(1<<f['mark']):z[a]=-total/q
                    if kind=='private' and l==j:z[a]=v[local[j][T]]
                kernels.append(z)
    nu=sum(x for x,f in zip(private_nullities,families) if f['t']==q)
    need(rank(kernels)==k+nu and all(all(x==0 for x in mv(C,z)) for z in kernels),'complete kernel basis')
    need(check['rank']==N-1-k-nu,'exact core rank')
    # Actual empty row is built directly from all core row sums.
    rows=[sum(row) for row in C];energy=sum(rows)
    L=[[F(1)+energy]+[F(1)-x for x in rows]]
    L += [[F(1)-rows[i]]+[F(1)+x for x in row] for i,row in enumerate(C)]
    whole=psd(L);need(whole['rank']==N-k-nu,'whole exact rank')
    M=[[(v-F(s)*(i==j))/(N-s) for j,v in enumerate(row)] for i,row in enumerate(L)]
    check_whole([0]+masks,M,s)
    for z in kernels:
        centered=[-sum(z)/N]+[x-sum(z)/N for x in z]
        need(all(x==0 for x in mv(L,centered)),'actual centered kernel lift')
    A2=sum(d*d for d in load);w=s-1
    formula=w-2*m+F(2*D*m,q)+s*m+(F(D,q)-3)*A2
    formula+=F(q+D,q)*sum(sum(sum(row) for row in f['core'])+(q-f['t'])*f['d'] for f in families)
    need(formula==energy,'empty energy formula')
    record={'n':n,'N':N,'s':s,'load':load,'k':k,'strict':all(f['t']<q for f in families),
            'private_t':[f['t'] for f in families],'private_d':[f['d'] for f in families],
            'private_input_upper_cap':[f['capped'] for f in families],
            'private_core_nullity':private_nullities,'boundary_nu':nu,'core_rank':check['rank'],
            'lower_rank':whole['rank'],'empty_energy':energy,'empty_loop':M[0][0],
            'ordered_core_positions':nt*nt,'core_sha256':digest(C),'lower_sha256':digest(L),
            'kernel_basis_sha256':digest(kernels),'physical_masks_sha256':digest([0]+masks),
            'core_pivots_sha256':check['pivot_record_sha256'],'lower_pivots_sha256':whole['pivot_record_sha256']}
    return record,[0]+masks,M,s,kernels,labels,C

def check_whole(S,M,s):
    N=len(S);need(len(M)==N and all(len(r)==N for r in M),'whole dimensions')
    need(all(sum(r)==1 for r in M),'actual row sums')
    for i,a in enumerate(S):
        for j,b in enumerate(S):
            need(M[i][j]==M[j][i],'whole symmetry')
            if a&b:need(M[i][j]==0,'original intersection including diagonal')
    return psd([[(N-s)*v+F(s)*(i==j) for j,v in enumerate(row)] for i,row in enumerate(M)])

def census(S):
    # All cliques, literal adjacency, no symmetry quotient or imported DAG.
    v=S[1:];adj=[sum(1<<j for j,b in enumerate(v) if i!=j and a&b) for i,a in enumerate(v)]
    best=0;winners=[];states=0
    def walk(chosen,candidates):
        nonlocal best,winners,states
        states+=1;need(states<=1000000,'finite clique guard')
        if chosen.bit_count()+candidates.bit_count()<best:return
        if not candidates:
            size=chosen.bit_count()
            if size>best:best=size;winners=[chosen]
            elif size==best:winners.append(chosen)
            return
        b=candidates&-candidates;i=b.bit_length()-1;rest=candidates^b
        walk(chosen|b,rest&adj[i]);walk(chosen,rest)
    walk(0,(1<<len(v))-1)
    winners=sorted(set(winners))
    return {'maximum':best,'count':len(winners),'families_sha256':digest(winners),'states':states},winners

def fixtures():
    path=lambda:partition(3,[(0,1),(1,2)],[1,2,0,0,1])
    triangle=lambda:partition(3,[(0,1),(0,2),(1,2)],[2,1,0,0,1,2])
    matching=lambda:partition(4,[(0,1),(2,3)],[1,1,1,1,0,0])
    return [
      ('q2-pendant',2,[(0,singles(1))]),
      ('q2-private-large',2,[(1,singles(7))]),
      ('q2-two-heavy',2,[(0,singles(1)),(1,singles(1))]),
      ('q2-boundary',2,[(0,cube(2))]),
      ('q2-two-boundary',2,[(0,cube(2)),(1,cube(2))]),
      ('q2-repeat-boundary',2,[(0,cube(2)),(0,cube(2))]),
      ('q2-boundary-plus-strict',2,[(0,cube(2)),(1,singles(1))]),
      ('q2-boundary-unbalanced-nonBoolean',2,[(1,matching())]),
      ('q4-mixed',3,[(0,cube(2)),(1,singles(1))]),
      ('q4-unequal-core',3,[(2,path()),(0,triangle())]),
      ('q4-unbalanced-partition',3,[(0,matching()),(1,singles(2))]),
      ('q4-cube-boundary',3,[(1,cube(3))]),
      ('q4-uniform-boundary',3,[(2,uniform_two(4))]),
      ('q4-boundary-uniform-mixed',3,[(2,uniform_two(4)),(0,singles(1))]),
      ('q8-uniform-strict',4,[(1,uniform_two(5))]),
      ('q8-repeated',4,[(0,path()),(0,singles(2)),(2,cube(2))]),
      ('q8-three-heavy',4,[(0,cube(2)),(1,cube(2)),(3,cube(2))]),
      ('q16-strict',5,[(4,cube(2)),(2,singles(2))]),
      ('q32-pendant',6,[(5,singles(1))])]

def main():
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('60s phase guard')));signal.alarm(60)
    parser=argparse.ArgumentParser();parser.add_argument('--expected');args=parser.parse_args()
    records=[];censuses=[];kept=None
    for name,n,inputs in fixtures():
        r,S,M,s,K,labels,C=build(n,inputs);r['name']=name;records.append(r)
        if len(S)<=18:
            cr,winners=census(S);st=stars(S);star_masks=sorted(sum(1<<i for i,a in enumerate(S[1:]) if a&b) for b,t in st.items() if t==s)
            need(cr['maximum']==s and winners==star_masks,'complete maximum families including boundary')
            cr['name']=name;cr['strict']=r['strict'];censuses.append(cr)
        if name=='q4-mixed':kept=(S,M,s)
    S,M,s=kept;N=len(S);perm=list(reversed(range(N)));R=[[M[i][j] for j in perm] for i in perm]
    check_whole([S[i] for i in perm],R,s)
    # Semantic controls exercise original constraints and PSD without asserts.
    rejects=[]
    def reject(name,call):
        try:call()
        except ValueError:rejects.append(name);return
        raise ValueError('damage accepted: '+name)
    reject('old-n1',lambda:build(1,[(0,singles(1))]))
    reject('empty-attachments',lambda:build(3,[]))
    reject('private-t-above-q',lambda:build(2,[(0,cube(3))]))
    reject('mark-outside-X',lambda:build(3,[(3,singles(1))]))
    def input_damage(kind):
        S,C,t=cube(2);C=[r[:] for r in C]
        if kind=='norm':C[0][0]+=1
        if kind=='intersection':C[0][2]=C[2][0]=0
        if kind=='symmetry':C[0][1]+=1
        if kind=='PSD':C[0][1]=C[1][0]=10
        if kind=='star':t+=1
        if kind=='downset':S=[0,1,3];C=[[F(1),F(-1)],[F(-1),F(1)]]
        core_check(S,C,t)
    for name in ['norm','intersection','symmetry','PSD','star','downset']:
        reject('private-'+name,lambda name=name:input_damage(name))
    def whole_damage(kind):
        B=[r[:] for r in M]
        if kind=='empty-row':B[0][0]+=1
        if kind=='symmetry':B[0][1]+=1;B[0][0]-=1
        if kind=='support':
            i=next(i for i,a in enumerate(S) if a);B[i][i]+=1;B[i][0]-=1
        check_whole(S,B,s)
    for name in ['empty-row','symmetry','support']:reject('whole-'+name,lambda name=name:whole_damage(name))
    # A zero-diagonal off-diagonal residual must not pass exact PSD elimination.
    reject('zero-pivot-offdiagonal',lambda:psd([[0,1],[1,0]]))
    reject('indefinite-positive-diagonal',lambda:psd([[1,2],[2,1]]))
    n1,n1winners=census([0,1,2,3]);need(n1['maximum']==2 and len(n1winners)==2,'n1 boundary counterexample')
    out={'agent':'six-reviewer-2','role':'independent mathematical reviewer','fixtures':records,
         'censuses':censuses,'rejections':rejects,'permuted_positions':N*N,
         'n1_boundary_classification_counterexample':n1,
         'totals':{'fixtures':len(records),'ordered_core_positions':sum(r['ordered_core_positions'] for r in records),
                   'boundary_fixtures':sum(not r['strict'] for r in records),'censuses':len(censuses)}}
    if args.expected:need(canonical(out)==json.loads(open(args.expected).read()),'complete frozen record equality')
    print(json.dumps(canonical(out),sort_keys=True,indent=2));signal.alarm(0)

if __name__=='__main__':main()
