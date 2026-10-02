"""Exact implementation of the star-bounded one-point H closure.

Inputs include actual private H cores; no solver or numerical input is used.
Finite guards bound validation, not the quantified ordinary proof.
"""
from fractions import Fraction as F
from exact import require, psd_rank, family_star, fingerprint, lift, gram, matvec

def cube(a):
    require(type(a) is int and 1<=a<=6,'private cube finite guard')
    family=list(range(1<<a));t=1<<(a-1);full=(1<<a)-1
    C=[[F(t*(A==B)+t*(A^B==full)-1) for B in family[1:]] for A in family[1:]]
    return {'kind':'cube','parameter':a,'family':family,'s':t,'core':C}

def singletons(a):
    require(type(a) is int and 1<=a<=20,'singleton finite guard')
    family=[0]+[1<<i for i in range(a)]
    return {'kind':'singletons','parameter':a,'family':family,'s':1,'core':[[F(0)]*a for _ in range(a)]}

def uniform_rank_two(a):
    require(type(a) is int and 3<=a<=6,'uniform two-skeleton finite guard')
    family=[x for x in range(1<<a) if x.bit_count()<=2]
    C=[]
    for A in family[1:]:
        row=[]
        for B in family[1:]:
            if A==B:z=a-1
            elif A&B or A.bit_count()==B.bit_count()==1:z=-1
            else:z=F(2,a-2)
            row.append(F(z))
        C.append(row)
    return {'kind':'uniform_rank_two','parameter':a,'family':family,'s':a,'core':C}

def validate_core(family,C,s):
    require(family_star(family)==s,'private largest star')
    d=len(family)-1
    require(len(C)==d and all(len(row)==d for row in C),'private core dimensions')
    for i,A in enumerate(family[1:]):
        require(C[i][i]==s-1,'private core diagonal')
        for j,B in enumerate(family[1:]):
            require(C[i][j]==C[j][i],'private symmetry')
            if i!=j and A&B:require(C[i][j]==-1,'private core intersection')
    return psd_rank(C)

def check_h(family,M,s):
    N=len(family)
    require(len(M)==N and family_star(family)==s,'whole dimension/star')
    for i,A in enumerate(family):
        require(sum(M[i])==1,'whole row sum')
        for j,B in enumerate(family):
            require(M[i][j]==M[j][i],'whole symmetry')
            if A&B:require(M[i][j]==0,'whole original intersection')
    L=[[(N-s)*M[i][j]+s*(i==j) for j in range(N)] for i in range(N)]
    return {'N':N,'s':s,'lower_rank':psd_rank(L),'matrix_sha256':fingerprint(M),
            'actual_empty_loop':str(M[0][0])}

def construct(n,attachments):
    require(type(n) is int and 2<=n<=6,'literal n<=6 guard')
    require(attachments,'at least one attachment')
    q=1<<(n-1);old=list(range(1,2*q));oldN=2*q-1
    loads=[0]*n;private=[];offset=n;family=list(range(2*q));records=[('old',None,None,A) for A in old]
    input_rows=[]
    for j,(mark,E) in enumerate(attachments):
        require(type(mark) is int and 0<=mark<n,'old mark')
        ef=E['family'];t=E['s'];Cj=E['core'];d=len(ef)-1
        require(t<=q,'private star exceeds construction bound')
        rank=validate_core(ef,Cj,t);loads[mark]+=d
        input_rows.append({'mark':mark,'kind':E['kind'],'parameter':E['parameter'],'N':len(ef),
                           's':t,'core_rank':rank,'core_sha256':fingerprint(Cj)})
        for T in ef[1:]:
            fresh=T<<offset;family.extend([fresh,fresh|(1<<mark)])
            records.extend([('U',mark,j,T),('V',mark,j,T)])
        offset+=max(ef).bit_length();private.append(E)
    N=len(family);require(N<=80,'literal original N<=80 guard')
    m=sum(loads);D=max(loads);s=q+D;w=F(s-1);k=loads.count(D)
    require(N==2*q+2*m and family_star(family)==s,'family exact N/s')
    full=2*q-1
    oldcore=[[F(s*(A==B)+(q-D)*(A^B==full)-1) for B in old] for A in old]
    require(psd_rank(oldcore)==oldN,'old cube PD')
    # Literal closed entry table.
    index=[{T:a for a,T in enumerate(E['family'][1:])} for E in private]
    residuals=[]
    for E in private:
        d=len(E['core']);t=E['s']
        residuals.append([[(1+F(D,q))*(E['core'][i][j]+(q-t)*(i==j)) for j in range(d)] for i in range(d)])
    def entry(A,B):
        kind,i,j,T=A;kind2,i2,j2,T2=B
        if kind=='old' and kind2=='old':return oldcore[T-1][T2-1]
        if kind2=='old':return entry(B,A)
        if kind=='old':return F(1-2*bool(T&(1<<i2))) if kind2=='V' else F(D,q)*(2*bool(T&(1<<i2))-1)
        if kind==kind2=='V':return F(s*(A==B)-1) if i==i2 else F(0)
        if kind=='V' or kind2=='V':return F(-(i==i2))
        value=F(D,q)*(i==i2)
        if j==j2:value+=residuals[j][index[j][T]][index[j][T2]]
        return value
    C=[[entry(A,B) for B in records] for A in records]
    # A separate Gram-factor assembly using old-coordinate projections.
    H=[[-F(bool(A&(1<<i))) for A in old] for i in range(n)]
    co=[];independent=[[F(0)]*(N-1) for _ in range(N-1)]
    for kind,i,j,T in records:
        if kind=='old':co.append([F(A==T) for A in old])
        elif kind=='V':co.append([z/D for z in H[i]])
        else:co.append([-z/q for z in H[i]])
    for a,A in enumerate(records):
        for b,B in enumerate(records):
            kind,i,j,T=A;kind2,i2,j2,T2=B
            if kind==kind2=='V' and i==i2:independent[a][b]=s*((a==b)-F(1,D))
            elif kind==kind2=='U' and j==j2:independent[a][b]=residuals[j][index[j][T]][index[j][T2]]
    factor=gram(oldcore,co,independent)
    require(factor==C,'every literal/factor Gram entry')
    nu=sum(len(E['core'])-r['core_rank'] for E,r in zip(private,input_rows) if E['s']==q)
    expected_rank=N-1-k-nu
    require(validate_core(family,C,s)==expected_rank,'full original core rank')
    heavy=[i for i,d in enumerate(loads) if d==D]
    for i in heavy:
        star=[F(bool(A&(1<<i))) for A in family[1:]]
        require(not any(matvec(C,star)),'each forced heavy kernel')
    M=lift(C,s);out=check_h(family,M,s)
    require(out['lower_rank']==N-k-nu,'original whole rank')
    private_energy=sum(sum(map(sum,E['core']))+(q-E['s'])*len(E['core']) for E in private)
    Bempty=w-2*m+F(2*D*m,q)+s*m+(F(D,q)-3)*sum(d*d for d in loads)+(1+F(D,q))*private_energy
    require(sum(map(sum,C))==Bempty,'separate actual empty energy')
    require(M[0][0]==(Bempty+1-s)/(N-s),'actual empty-loop formula')
    out.update(n=n,q=q,loads=loads,k=k,strict=all(E['s']<q for E in private),
               equality_input_nullity=nu,core_rank=expected_rank,inputs=input_rows,
               core_sha256=fingerprint(C),ordered_core_positions=(N-1)**2,
               actual_empty_energy=str(Bempty))
    return family,C,M,out
