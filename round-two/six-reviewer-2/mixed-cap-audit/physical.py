"""Independent complete original-set Gram/frame/lift and rank-repair checks.

Primitive old Gram + four marked residuals + four private residuals, rather
than translating the author's literal core constructor. No author imports.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,signal
from frame import model,evaluate
from linear import need,mv,dot,psd,digest,canonical

def unit(n,i):v=[F(0)]*n;v[i]=1;return v
def add(a,b):return [x+y for x,y in zip(a,b)]
def scale(a,z):return [x*z for x in a]
def gram(B,rows):
    sparse=[[(i,x)for i,x in enumerate(v)if x]for v in rows]
    images=[[sum(B[i][j]*x for j,x in v)for i in range(len(B))]for v in sparse]
    return [[sum(x*images[j][i]for i,x in v)for j in range(len(rows))]for v in sparse]
def kernel(A):
    B=[list(map(F,r))for r in A];m=len(B);n=len(B[0]);piv=[];r=0
    for j in range(n):
        p=next((i for i in range(r,m)if B[i][j]),None)
        if p is None:continue
        B[r],B[p]=B[p],B[r];d=B[r][j];B[r]=[x/d for x in B[r]]
        for i in range(m):
            if i!=r and B[i][j]:
                z=B[i][j];B[i]=[x-z*y for x,y in zip(B[i],B[r])]
        piv.append(j);r+=1
    out=[]
    for j in range(n):
        if j in piv:continue
        v=unit(n,j)
        for i,p in enumerate(piv):v[p]=-B[i][j]
        need(not any(mv(A,v)),'kernel residual');out.append(v)
    return out
def lift(C,s):
    m=len(C);N=m+1;rows=[sum(r)for r in C];energy=sum(rows)
    L=[[F(1)+energy]+[F(1)-x for x in rows]]
    L += [[F(1)-rows[i]]+[F(1)+x for x in r]for i,r in enumerate(C)]
    M=[[(x-s*(i==j))/(N-s)for j,x in enumerate(r)]for i,r in enumerate(L)]
    return M,L,energy
def check(S,M,s,gap=0):
    N=len(S);need(len(set(S))==N and S[0]==0,'actual empty and unique sets')
    support=0
    for T in S:
        support|=T;b=T
        while True:
            need(b in S,'downward closure')
            if not b:break
            b=(b-1)&T
    ss=[sum(bool(T&(1<<i))for T in S)for i in range(support.bit_length())]
    need(max(ss)==s and ss.count(s)==1,'unique largest original star')
    need(all(sum(row)==1 for row in M),'actual whole row sums')
    for i,T in enumerate(S):
        for j,U in enumerate(S):
            need(M[i][j]==M[j][i],'whole symmetry')
            if T&U:need(M[i][j]==0,'every original intersection including diagonal')
    L=[[(N-s)*x+s*(i==j)for j,x in enumerate(row)]for i,row in enumerate(M)]
    cap=[[(N-s)*((i==j)-x)-gap*(F(i==j)-F(1,N))for j,x in enumerate(row)]for i,row in enumerate(M)]
    return {'lower':psd(L),'cap_with_gap':psd(cap),'lower_sha256':digest(L),'matrix_sha256':digest(M)}

def raw_core(q,old,labels):
    # Credited ordinary9361/own9412 entry table, specialized to D3.
    s=q+3;full=2*q-1;private=[[1,1,-1],[1,1,-1],[-1,-1,1]]
    residual=[[F(q+3,q)*(private[i][j]+(q-2)*(i==j))for j in range(3)]for i in range(3)]
    C=[]
    for kind,i,T in labels:
        row=[]
        for other,j,U in labels:
            if kind==other=='old':z=s*(T==U)+(q-3)*(T^U==full)-1
            elif kind=='old' or other=='old':
                A=T if kind=='old'else U;kk=other if kind=='old'else kind;index=j if kind=='old'else i
                mark=0 if index<3 else 1;z=F(1-2*bool(A&(1<<mark)))
                if kk=='private':z=-F(3,q)*z
            else:
                same=(i<3)==(j<3)
                if kind==other=='marked':z=F(s*(i==j)-1)if same else F(0)
                elif kind==other=='private':
                    z=F(3,q)*same
                    if i<3 and j<3:z+=residual[i][j]
                    elif i==j==3:z+=F(q+3,q)*(q-1)
                else:z=F(-int(same))
            row.append(F(z))
        C.append(row)
    return C

def original(n,M):
    need(3<=n<=6,'original n guard');q=1<<(n-1);N=2*q+8;s=q+3;old=list(range(1,2*q));no=len(old);dim=no+8
    B=[[F(0)]*dim for _ in range(dim)]
    for i,T in enumerate(old):
        for j,U in enumerate(old):B[i][j]=F(s*(T==U)+(q-3)*(T^U==2*q-1)-1)
    for i in range(3):
        for j in range(3):B[no+i][no+j]=F(s)*((i==j)-F(1,3))
    B[no+3][no+3]=F(2*s,3);W=evaluate(M['residual'],q)
    for i in range(4):
        for j in range(4):B[no+4+i][no+4+j]=W[i][j]
    oldrows=[unit(dim,i)for i in range(no)];G=[F(int(i<no))for i in range(dim)];f=oldrows[-1]
    Hx=[-F(bool(T&1))for T in old]+[F(0)]*8
    Hz=[-F(bool(T&2))for T in old]+[F(0)]*8
    H=scale(Hx,F(1,3));V4=add(scale(Hz,F(1,3)),unit(dim,no+3))
    marked=[add(H,unit(dim,no+i))for i in range(3)]+[V4]
    K=add(G,add(Hx,V4));a,b,c,d,ee,ff,g=[x.value(q-4)for x in M['parameters']]
    PU=add(scale(K,F(-1,5)),add(scale(H,a),add(scale(V4,b),scale(unit(dim,no+1),c))))
    PV=add(scale(K,F(-1,5)),add(scale(H,a),add(scale(V4,b),scale(unit(dim,no),c))))
    PUV=add(scale(K,F(-1,5)),add(scale(H,d),scale(V4,ee)))
    PB=add(scale(K,F(-1,5)),add(scale(H,ff),add(scale(V4,g),scale(unit(dim,no+2),c))))
    private=[add(v,unit(dim,no+4+i))for i,v in enumerate([PU,PV,PUV,PB])]
    rows=oldrows+marked+private;displayed_empty=scale(K,F(-1,5))
    actual_sum=[sum(v[i]for v in rows)for i in range(dim)]
    empty=scale(actual_sum,-1)
    # Primitive coordinates include two null relations, sum(T_i)=sum(w_i)=0.
    # Compare represented vectors in the Gram quotient, not formal coefficients.
    difference=add(empty,scale(displayed_empty,-1))
    need(not any(mv(B,difference)),'actual empty equals displayed vector in Gram quotient')
    u=1<<n;v=1<<(n+1);bb=1<<(n+2);new=[u,v,u|v,bb];marks=[1,1,1,2]
    S=[0]+old+[T|mark for T,mark in zip(new,marks)]+new
    labels=[('old',-1,T)for T in old]+[('marked',i,T)for i,T in enumerate(new)]+[('private',i,T)for i,T in enumerate(new)]
    C=gram(B,rows);whole,L,energy=lift(C,s);seed=check(S,whole,s,F(1))
    need(psd(B)['rank']==N-3 and psd(C)['rank']==N-3 and seed['lower']['rank']==N-2,'complete seed ranks')
    need(seed['cap_with_gap']['rank']==N-1,'whole seed scaled gap1')
    h0=scale(add(G,f),F(-1,2));gp=add(G,h0)
    basis=[gp,h0,add(Hx,scale(h0,-1)),add(Hz,scale(h0,-1)),unit(dim,no+3),
           add(unit(dim,no),scale(unit(dim,no+1),-1)),
           add(add(unit(dim,no),unit(dim,no+1)),scale(unit(dim,no+2),-2)),
           add(unit(dim,no+4),scale(unit(dim,no+5),-1)),unit(dim,no+6),unit(dim,no+7)]
    Gamma=gram(B,basis);need(Gamma==evaluate(M['gram'],q),'all physical ten-Gram entries')
    # Whole frame is summed from all actual rows including the actual empty.
    joint=gram(B,basis+[empty]+rows);images=[r[:10]for r in joint[10:]]
    FF=[[sum(v[i]*v[j]for v in images)for j in range(10)]for i in range(10)]
    need(FF==evaluate(M['frame'],q),'all actual complete-frame entries')
    pairs=[(T,(2*q-1)^T)for T in old[:-1]if T<((2*q-1)^T)]
    high=[]
    for a,bb in pairs[1:]:
        z=[F(0)]*N
        for T in [a,bb]:z[S.index(T)]+=1
        for T in pairs[0]:z[S.index(T)]-=1
        high.append(z)
    constraints=[[F(bool(a&mark))-F(bool(bb&mark))for a,bb in pairs]for mark in [1,2]]
    low=[]
    for z in kernel(constraints):
        row=[F(0)]*N
        for t,(aa,bb)in zip(z,pairs):row[S.index(aa)]=t;row[S.index(bb)]=-t
        low.append(row)
    need(len(high)==q-2 and len(low)==q-3,'complete untouched sector dimensions')
    for eigen,vectors in [(2*q,high),(6,low)]:
        for z in vectors:need(mv(L,z)==[eigen*x for x in z],'full original untouched eigenaction including empty/new rows')
    RC=raw_core(q,old,labels);raw,rawL,rawenergy=lift(RC,s);rawinfo=psd(rawL)
    need(psd(RC)['rank']==N-2 and rawinfo['rank']==N-1,'credited raw ordinary greatest rank')
    T=sum(rawL[i][i]-1 for i in range(N));formula=2*q*q+20*q-4+F(36,q)
    need(T==formula and rawenergy==9*q-18+F(36,q),'original complete raw trace and empty energy')
    A=T-N+1;need(A>1,'positive enlarged interval denominator')
    repaired=[]
    for tag,epsilon,gap in [('original',1/(2*(1+T)),F(1,2)),
                            ('new-quarter',F(3,4)/A,F(1,4)),('new-half',F(1,2)/A,F(1,2)),
                            ('new-three-quarters',F(1,4)/A,F(3,4))]:
        mix=[[(1-epsilon)*x+epsilon*y for x,y in zip(row,rr)]for row,rr in zip(C,RC)]
        mat,_,_=lift(mix,s);checks=check(S,mat,s,gap)
        need(checks['lower']['rank']==N-1 and checks['cap_with_gap']['rank']==N-1,'full repaired lower and guaranteed upper ranks')
        repaired.append({'tag':tag,'epsilon':epsilon,'guaranteed_scaled_gap':gap,'whole_matrix_sha256':digest(mat)})
    return {'n':n,'N':N,'s':s,'seed_core_rank':N-3,'seed_lower_rank':N-2,'raw_lower_rank':N-1,
            'actual_empty_energy':energy,'seed_empty_loop':whole[0][0],
            'raw_empty_loop':raw[0][0],'raw_trace':T,'enlarged_interval_denominator':A,
            'physical_gram_sha256':digest(Gamma),'physical_full_frame_sha256':digest(FF),
            'seed_core_sha256':digest(C),'seed_whole_sha256':digest(whole),
            'raw_core_sha256':digest(RC),'repaired':repaired,'high_actions':len(high),'low_actions':len(low)},S,whole

def main():
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('60s original phase guard')));signal.alarm(60)
    p=argparse.ArgumentParser();p.add_argument('--expected');a=p.parse_args();M=model();records=[];kept=None
    for n in [3,4,5,6]:
        row,S,mat=original(n,M);records.append(row)
        if n==3:kept=(S,mat,row['s'])
    S,mat,s=kept;rejections=[]
    def reject(name,fn):
        try:fn()
        except ValueError:rejections.append(name);return
        raise ValueError('damage accepted '+name)
    def damage(kind):
        B=[r[:]for r in mat]
        if kind=='empty-loop':B[0][0]+=1
        if kind=='support':B[1][1]+=1;B[1][0]-=1
        if kind=='row-sum':B[1][0]+=1
        if kind=='symmetry':B[0][1]+=1;B[0][0]-=1
        check(S,B,s,F(1))
    for name in ['empty-loop','support','row-sum','symmetry']:reject(name,lambda name=name:damage(name))
    reject('whole-scaled-gap-excess',lambda:check(S,mat,s,F(100)))
    reject('n2-domain',lambda:original(2,M));reject('zero-pivot-residual',lambda:psd([[0,1],[1,0]]))
    out={'agent':'six-reviewer-2','role':'independent mathematical reviewer','original_families':records,
         'gram_positions':400,'full_frame_positions':400,'whole_repair_checks':16,
         'high_eigenactions':sum(r['high_actions']for r in records),'low_eigenactions':sum(r['low_actions']for r in records),
         'rejections':rejections,'trust':'independent primitive Gram assembly; original sets/whole empty lift; no author modules'}
    if a.expected:need(canonical(out)==json.loads(Path(a.expected).read_text()),'complete frozen physical record')
    print(json.dumps(canonical(out),sort_keys=True,indent=2));signal.alarm(0)

if __name__=='__main__':main()
