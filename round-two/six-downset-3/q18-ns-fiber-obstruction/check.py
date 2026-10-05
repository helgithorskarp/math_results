"""Exact original q18 candidate and weighted NS-fiber certificate.

Standard library only. Fresh literal carrier/entries/rows and physical action
of the NEW rational candidate. The physical seed/basis mechanism is openly
adapted from own published10296/check.py (source40c0527...). No ancestor
program, PSD factor, EXPECTED, numerical package or solver is imported.
Representation completeness is an ordinary explicitly cited bridge.
"""
from fractions import Fraction as F
from itertools import combinations
from math import lcm
from pathlib import Path
import hashlib
import json
import sys


def require(ok,msg):
    if not ok:raise ValueError(msg)


def carrier():
    X=[]
    for rank in (1,2,3):
        for bits in combinations(range(21),rank):
            m=sum(1<<i for i in bits);core=m&7
            if rank==3 and (core.bit_count()<2 or
                            (core==6 and (m&((1<<12)-8)))):continue
            X.append(m)
    X.sort()
    O=[(m&7,((m>>3)&511).bit_count(),(m>>12).bit_count()) for m in X]
    S=[i for i,m in enumerate(X) if m&1];T=[i for i,m in enumerate(X) if not m&1]
    bad={(0,2,0),(0,0,2),(6,0,1)}
    B=[i for i in T if O[i] in bad];G=[i for i in T if O[i] not in bad]
    require((len(X),len(S),len(T),len(B),len(G))==(277,58,219,81,138),'literal full carrier')
    require([sum(bool(m&(1<<p)) for m in X) for p in range(21)]==[58,49,49]+[23]*9+[24]*9,
            'ALL original point-star sizes')
    keys=sorted({tuple(sorted((O[i],O[j]))) for i,m in enumerate(X)
                 for j in range(i+1,len(X)) if not m&X[j] and m!=1 and X[j]!=1})
    require(len(keys)==143 and X[0]==1,'literal whole free orbit order')
    return X,O,S,T,B,G,keys


def matrix(X,O,S,T,keys,values,D):
    require(len(values)==143 and all(type(x) is int for x in values),'whole143 integer coefficients')
    table=dict(zip(keys,values));C=[]
    for i,m in enumerate(X):
        row=[]
        for j,v in enumerate(X):
            if i==j:c=57*D
            elif m&v:c=-D
            elif m==1 or v==1:c=0
            else:c=table[tuple(sorted((O[i],O[j])))]
            row.append(c)
        C.append(row)
    for i in T:C[i][0]=C[0][i]=-sum(C[i][j] for j in S if j)
    require(all(sum(row[j] for j in S)==0 for row in C),'ALL original star kernel rows')
    require(all(C[i][j]==C[j][i] for i in range(len(X)) for j in range(len(X))),
            'ALL original proper symmetric positions')
    return C


def physical(X,O):
    K=sorted(set(O))
    TT=[[int(o==key) for o in O] for key in K]
    seed={'TT':TT}
    for name,offset,countpos in (('Z',3,1),('W',12,2)):
        order=[o for o in K if o[countpos]>0]
        seed[name]=[[(int(bool(m&(1<<offset)))-int(bool(m&(1<<(offset+1)))))*int(o==key)
                      for m,o in zip(X,O)] for key in order]
    for name,offset in (('ZZ',3),('WW',12)):
        weights={(0,1):1,(2,3):1,(0,2):-1,(1,3):-1}
        seed[name]=[[weights.get(tuple(i for i in range(9) if m&(1<<(offset+i))),0)
                      if m&7==0 and m.bit_count()==2 else 0 for m in X]]
    seed['ZW']=[[(int(bool(m&8))-int(bool(m&16)))*
                  (int(bool(m&(1<<12)))-int(bool(m&(1<<13))))
                  if m&7==0 and m.bit_count()==2 else 0 for m in X]]
    require({k:len(v) for k,v in seed.items()}=={'TT':23,'Z':8,'W':9,'ZZ':1,'WW':1,'ZW':1},
            'whole new physical seed dimensions')
    return K,seed


def image(C,v):
    sp=[(i,x) for i,x in enumerate(v) if x]
    return [sum(row[i]*x for i,x in sp) for row in C]


def gram_action(C,V):
    Av=[image(C,v) for v in V]
    gram=[[sum(x*y for x,y in zip(v,col)) for col in Av] for v in V]
    norms=[sum(x*x for x in v) for v in V]
    require(all(sum(x*y for x,y in zip(v,w))==norms[i]*int(i==j)
                for i,v in enumerate(V) for j,w in enumerate(V)),
            'ALL physical seed metric positions')
    clear=lcm(*norms);count=0
    for j,col in enumerate(Av):
        for i,y in enumerate(col):
            require(clear*y==sum(V[k][i]*gram[k][j]*(clear//norms[k]) for k in range(len(V))),
                    'new original physical action at EVERY coordinate')
            count+=1
    return gram,norms,count


def factor(A):
    n=len(A);L=[[F(int(i==j)) for j in range(n)] for i in range(n)];p=[]
    for j in range(n):
        pivot=F(A[j][j])-sum(L[j][k]*L[j][k]*p[k] for k in range(j))
        require(pivot>0,'EVERY exact weighted lower-cone pivot')
        p.append(pivot)
        for i in range(j+1,n):
            L[i][j]=(F(A[i][j])-sum(L[i][k]*L[j][k]*p[k] for k in range(j)))/pivot
    positions=0
    for i in range(n):
        for j in range(n):
            require(F(A[i][j])==sum(L[i][k]*p[k]*L[j][k] for k in range(n)),
                    'EVERY exact complete factor identity')
            positions+=1
    return [str(x) for x in p],positions


def check(data,comparison):
    X,O,S,T,B,G,keys=carrier();n=len(X);D=data['denominator']
    require(D==1<<32 and comparison['comparison_free_denominator']==16384,'named exact denominators')
    nums=comparison['comparison_free_numerators']
    require(hashlib.sha256(json.dumps(nums,separators=(',',':')).encode()).hexdigest()==
            '14cca17e8c9dcf4be01d7abe5700745fc120ea782e84bcc73d25b7df176a4e7d',
            'entire attributed143 comparison list')
    C=matrix(X,O,S,T,keys,data['free_numerators'],D)
    old=matrix(X,O,S,T,keys,[x*(D//16384) for x in nums],D)
    rows=list(map(sum,C));total=sum(rows)
    M=[[total-57*D]+[D-x for x in rows]]
    for i in range(n):M.append([D-rows[i]]+[C[i][j]+D-58*D*int(i==j) for j in range(n)])
    actual=[0]+X;count=0;surplus=[]
    for i,m in enumerate(actual):
        require(sum(M[i])==220*D,'EVERY original stochastic row')
        for j,v in enumerate(actual):
            require(M[i][j]==M[j][i],'EVERY actual symmetric position')
            if m&v:require(M[i][j]==0,'EVERY original forbidden position')
            else:
                require(M[i][j]>=D//256,'EVERY actual positive floor including loop')
                surplus.append(M[i][j]);count+=1
    require(count==60597,'ALL actual ordered allowed floors')
    K,seeds=physical(X,O);actions=0;identities=0;pivots={}
    for name,V in seeds.items():
        H,norms,paid=gram_action(C,V);actions+=paid
        if name=='TT':
            anchor=K.index((1,0,0));ids=[i for i in range(23) if i!=anchor]
            u=[norms[i] if K[i][0]&1 else 0 for i in ids]
            H2=[[H[i][j]-u[b]*H[i][anchor]-u[a]*H[anchor][j]+u[a]*u[b]*H[anchor][anchor]
                 for b,j in enumerate(ids)] for a,i in enumerate(ids)]
            metric=[[norms[i]*int(a==b)+u[a]*u[b] for b,j in enumerate(ids)] for a,i in enumerate(ids)]
        else:
            H2=H;metric=[[norms[i]*int(i==j) for j in range(len(norms))] for i in range(len(norms))]
        A=[[2048*x-D*metric[i][j] for j,x in enumerate(row)] for i,row in enumerate(H2)]
        pivots[name],paid=factor(A);identities+=paid
    require(actions==277*43 and identities==22**2+8**2+9**2+3,'ALL paid new action/factor positions')
    # Weights1/4 on ZZ/WW and1 on bcW; all81 original rows individually bound.
    w={i:4 if O[i]==(6,0,1) else 1 for i in B}
    v=[sum(C[s][i]*w[i] for i in B) for s in S]
    require(sum(v)==0,'NEW exact whole weighted NS vector kernel')
    Q=F(sum(x*x for x in v),58*16*D*D)
    cap=F(sum(w[i]*old[i][j]*w[j] for i in B for j in B),16*D)
    newBB=F(sum(w[i]*C[i][j]*w[j] for i in B for j in B),16*D)
    require(Q<=newBB,'NEW exact literal weighted Schur inequality')
    alpha=max(F(w[i]*w[j],16) for p,i in enumerate(B) for j in B[p+1:] if not X[i]&X[j])
    require(alpha==F(1,4) and Q-cap>F(1249,2),'NEW genuine weighted crossing and original maximum edge product')
    require(58*Q>F(1111,4)**2 and 58*cap<F(811,4)**2,
            'NEW exact rational norm separators for EVERY optimizer')
    require(sum(w.values())==108 and F(sum(x*x for x in w.values()),16)==F(27,2)
            and 58*F(27*220,640)**2<75**2,'NEW literal weight norms and original NS entry displacement')
    P=F(0);WBB=F(0);WGG=F(0);mixed=F(0);nncounts=[0,0,0]
    for p,i in enumerate(T):
        for j in T[p+1:]:
            if X[i]&X[j]:continue
            r=F(C[i][j]-old[i][j],D);k=int(i in w)+int(j in w);nncounts[k]+=1
            P+=max(r,0)
            if k==2:WBB+=max(r,0)
            elif k==0:WGG+=max(-r,0)
            else:mixed+=abs(r)
    require(nncounts==[7885,9009,2628] and Q-cap<=2*alpha*WBB,'WHOLE original NN weighted crossing budget')
    endpoint=[]
    for tau in (F(0),F(1,256)):
        sigma=sum(F(M[0][i+1],D)-tau for i in B)
        loop=F(M[0][0],D)-tau
        Delta=P-F(476335,32768)-41*tau
        require(min(sigma,loop)>=0 and 2*Delta==sigma+loop+mixed+2*(WBB+WGG),
                'NEW complete original endpoint dual identity')
        require(Delta>=2*(Q-cap)>1249,'NEW exact fiber gap at stated endpoints')
        endpoint.append({'tau':str(tau),'P':str(P),'Delta':str(Delta)})
    return {'actual_agent':'six-downset-3','role':'researcher','status':'Exact NEW witness checks; ordinary completeness/Schur bridges unformalized and independently unreviewed',
            'carrier':[278,58],'candidate_denominator':D,'allowed_ordered_original_floors':count,
            'actual_entry_floor_C_units':'1/256','actual_entry_floor_M_units':'1/56320',
            'actual_min_entry_C_units':str(F(min(surplus),D)),
            'new_original_physical_actions':actions,'new_complete_factor_positions':identities,
            'proper_C_starperp_floor':'1/2048','complete_new_factor_pivots':pivots,
            'weight_ZZ_WW':'1/4','weight_bcW':'1','maximum_original_E2_weight_product':str(alpha),
            'Q':str(Q),'old_BB_cap':str(cap),'weighted_gap':str(Q-cap),'fiber_Delta_lower':str(2*(Q-cap)),
            'fiber_Delta_clean_lower':1249,'v_S_complete58_denominator':4*D,'v_S_complete58_numerators':v,
            'weighted_NS_vector_norm_distance_to_every_optimizer_strict_lower':75,
            'actual_NS_entry_max_distance_to_every_optimizer_strict_lower':'1/640',
            'weight_l1':'27','weight_l2_squared':'27/2',
            'new_NN_counts_E0_E1_E2':nncounts,'input_dual_endpoints':endpoint,
            'solver_is_not_proof':True,'ordinary_real_interval':'every real0<=tau<=1/256 for the same fixed candidate',
            'independent_review_claimed':False}


def main():
    root=Path(__file__).resolve().parent
    result=check(json.loads((root/'CANDIDATE.json').read_bytes()),json.loads((root/'COMPARISON.json').read_bytes()))
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
