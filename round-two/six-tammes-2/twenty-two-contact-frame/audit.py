"""Separate exact frame audit with sparse integer polynomials in t,z.

No CAS, rational-function simplifier or production interval imports.
The radical h=(1+t)^2*f has the polynomial square printed below.
All coordinate denominators are kept explicit and cleared in identities.
Actual author six-tammes-2, researcher; same-author arithmetic audit.
"""
import json,signal,time
def need(ok,message):
    if not ok:raise ValueError(message)
def c(n):return {} if n==0 else {(0,0):n}
def add(a,b):
    v=a.copy()
    for x,n in b.items():
        v[x]=v.get(x,0)+n
        if not v[x]:del v[x]
    return v
def neg(a):return {x:-n for x,n in a.items()}
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    if not a or not b:return {}
    v={}
    for (i,j),n in a.items():
        for (k,h),m in b.items():
            x=(i+k,j+h);v[x]=v.get(x,0)+n*m
    return {x:n for x,n in v.items() if n}
def power(a,n):
    v=c(1)
    for _ in range(n):v=mul(v,a)
    return v
def total(rows):
    v={}
    for x in rows:v=add(v,x)
    return v
def divide_tplus1(a):
    quotient={};remaining=a.copy()
    for j in sorted({x[1] for x in a}):
        degree=max(i for i,h in a if h==j)
        for i in range(degree,0,-1):
            n=remaining.get((i,j),0)
            if n:
                quotient[(i-1,j)]=n
                remaining.pop((i,j))
                previous=(i-1,j);remaining[previous]=remaining.get(previous,0)-n
                if not remaining[previous]:del remaining[previous]
    need(not remaining,'exact polynomial division by 1+t')
    return quotient
def derive():
    zero={};one=c(1);t={(1,0):1};z={(0,1):1};L=power(add(one,t),2)
    D=mul(power(sub(one,t),2),add(one,mul(c(2),t)))
    A=mul(sub(one,t),add(one,mul(c(2),t)))
    kn=mul(t,sub(sub(mul(c(9),power(t,2)),mul(c(2),t)),c(3)))
    M0=add(L,kn)
    mn=mul(mul(sub(t,one),add(t,one)),mul(add(mul(c(2),t),one),sub(mul(c(3),t),one)))
    def vcross(a,b):return [sub(mul(a[1],b[2]),mul(a[2],b[1])),sub(mul(a[2],b[0]),mul(a[0],b[2])),sub(mul(a[0],b[1]),mul(a[1],b[0]))]
    def vscale(x,q):return [mul(a,q) for a in x]
    def vadd(a,b):return [add(x,y) for x,y in zip(a,b)]
    def Mv(x):return [sub(mul(add(one,mul(c(2),t)),a),mul(t,total(x))) for a in x]
    basis={i:[one if j==s else zero for j in range(3)] for s,i in enumerate((1,2,4))}
    B={i:vscale(v,L) for i,v in basis.items()}
    for n,i,j,o in ((8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,8,4)):
        B[n]=[sub(divide_tplus1(mul(mul(c(2),t),add(a,b))),v) for a,b,v in zip(B[i],B[j],B[o])]
    C=add(one,mul(D,power(z,2)))
    S=add(mul(D,sub(mul(t,power(z,2)),mul(c(2),z))),mul(t,sub(mul(c(2),t),one)))
    E=sub(power(C,2),power(S,2))
    radical=mul(D,add(sub(mul(power(L,2),sub(sub(power(C,2),power(S,2)),mul(power(t,2),power(C,2)))),mul(power(kn,2),power(C,2))),mul(mul(mul(mul(c(2),kn),t),L),mul(S,C))))
    # NW/L/C is the reciprocal-chart W. D*H^-1=(1-t)*M.
    NW=vadd(vadd(vscale(B[12],mul(t,C)),vscale([sub(mul(L,a),mul(t,b)) for a,b in zip(basis[1],B[12])],sub(mul(D,power(z,2)),one))),vscale(Mv(vcross(B[12],basis[1])),mul(mul(c(2),sub(one,t)),z)))
    base=vadd(vscale(NW,sub(mul(kn,C),mul(mul(t,S),L))),vscale(B[10],mul(sub(mul(mul(t,C),L),mul(kn,S)),C)))
    V0=vscale(base,mul(A,L));V1=Mv(vcross(NW,B[10]));DW=mul(L,C);DV=mul(mul(E,A),power(L,3))
    def pa(a,b):return add(a[0],b[0]),add(a[1],b[1])
    def ps(a,q):return mul(a[0],q),mul(a[1],q)
    def pm(a,b):return add(mul(a[0],b[0]),mul(radical,mul(a[1],b[1]))),add(mul(a[0],b[1]),mul(a[1],b[0]))
    def pt(rows):
        v=(zero,zero)
        for x in rows:v=pa(v,x)
        return v
    def pM(x):return [pa(ps(a,add(one,mul(c(2),t))),ps(pt(x),neg(t))) for a in x]
    def px(a,b):return [pa(pm(a[1],b[2]),ps(pm(a[2],b[1]),c(-1))),pa(pm(a[2],b[0]),ps(pm(a[0],b[2]),c(-1))),pa(pm(a[0],b[1]),ps(pm(a[1],b[0]),c(-1)))]
    def pd(a,b):return pa(ps(pt([pm(x,y) for x,y in zip(a,b)]),sub(one,t)),ps(pm(pt(a),pt(b)),t))
    W=[(a,zero) for a in NW];V=list(zip(V0,V1))
    DU=mul(mul(M0,A),mul(DW,DV));AD=mul(sub(mul(c(9),power(t,2)),one),DU)
    CONTACTS=[(0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),(2,4),(2,8),(2,10),(2,13),(4,8),(5,7),(5,9),(5,11),(6,11),(7,12),(8,13),(9,10),(9,11),(10,12)]
    count_units=count_contacts=0;maximum=[0,0]
    for eta in (-1,1):
        normal=pM(px(W,V))
        U=[pa(ps(pa(ps(w,DV),ps(v,DW)),mul(kn,A)),ps(n,mul(c(eta),mn))) for w,v,n in zip(W,V,normal)]
        Wu=[ps(a,mul(mul(M0,A),DV)) for a in W];Vu=[ps(a,mul(mul(M0,A),DW)) for a in V]
        P={i:([(a,zero) for a in b],L) for i,b in B.items()};P[6]=(U,DU);P[7]=(W,DW);P[9]=(V,DV)
        for label,coeffs in ((0,(mul(c(2),t),mul(c(2),t),sub(one,t))),(5,(sub(one,t),mul(c(2),t),mul(c(2),t))),(11,(mul(c(2),t),sub(one,t),mul(c(2),t)))):
            P[label]=([ps(pt([ps(x[j],a) for x,a in zip((U,Wu,Vu),coeffs)]),add(one,t)) for j in range(3)],AD)
        for i,(x,q) in sorted(P.items()):
            if eta==1 and i not in (0,5,6,11):continue
            need(pd(x,x)==(power(q,2),zero),'integer coefficient unit identity '+str((eta,i)));count_units+=1
        for i,j in CONTACTS:
            if eta==1 and not {i,j}.intersection((0,5,6,11)):continue
            x,a=P[i];y,b=P[j]
            need(pd(x,y)==(mul(t,mul(a,b)),zero),'integer coefficient contact '+str((eta,i,j)));count_contacts+=1
        for x,q in P.values():
            for p in [q]+[v for a in x for v in a]:
                for i,j in p:maximum=[max(maximum[0],i),max(maximum[1],j)]
    need(count_units==17 and count_contacts==31,'complete distinct orientation identities')
    return {'status':'EXACT_INTEGER_COORDINATE_IDENTITIES','domain':'Z[t,z,h]/(h^2-(1+t)^4*D*G)','unit_identities':count_units,'contact_identities':count_contacts,'epsilon_conjugates_covered':[-1,1],'eta_choices_covered':[-1,1],'coordinate_and_denominator_degree_bounds':maximum,'imports_production_geometry_or_intervals':False}
if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda s,f:(_ for _ in ()).throw(TimeoutError('160-second integer-audit guard; incomplete')))
    signal.alarm(160)
    print(json.dumps(derive(),indent=2))
