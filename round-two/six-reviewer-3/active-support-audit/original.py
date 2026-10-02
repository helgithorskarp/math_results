"""Full original-index empty-loop, lift, star and physical metric controls."""
from fractions import Fraction as F
from exact import need
from face import base,forms,profiles,quad,key


def run():
    n=6;T=2**(n-1);s=T-n;h=T-1;N=2*T-n-1
    vertices=[a for a in range(1<<n) if a.bit_count()<=n-2];sizes=[a.bit_count() for a in vertices];need(vertices[0]==0 and len(vertices)==N,'all actual downset vertices')
    B=base(n);L=[];checks=0
    def check(ok,label):
        nonlocal checks
        need(ok,label);checks+=1
    for i,A in enumerate(vertices):
        row=[]
        for j,D in enumerate(vertices):
            value=F(1) if not A or not D else (F(s) if A==D else (F(0) if A&D else B.get(key(sizes[i],sizes[j]),F(0))))
            row.append(value)
        L.append(row)
    M=[[(x-s*int(i==j))/h for j,x in enumerate(row)] for i,row in enumerate(L)]
    C=[[L[i+1][j+1]-1 for j in range(N-1)] for i in range(N-1)]
    U=[[N*int(i==j)-1-C[i][j] for j in range(N-1)] for i in range(N-1)]
    for i,A in enumerate(vertices):
        check(sum(L[i])==N and sum(M[i])==1,'every original row, regularity and lift')
        for j,D in enumerate(vertices):
            check(L[i][j]==L[j][i] and M[i][j]==M[j][i],'every original symmetry entry')
            if A&D:check(M[i][j]==0,'every actual intersection support entry')
        for bit in range(n):
            star=[j for j,D in enumerate(vertices) if D&(1<<bit)]
            check(len(star)==s and sum(L[i][j] for j in star)==s,'every star action, original empty coordinate included')
    check(M[0][0]==F(1-s,h) and M[0][0]<0,'actual permitted negative empty loop')
    for i,row in enumerate(C):
        check(sum(row)==0,'every core centering row')
        for bit in range(n):check(sum(row[j] for j,D in enumerate(vertices[1:]) if D&(1<<bit))==0,'every original core star kernel')
    # Entry-level ECE/EUE reconstruction, using literal E top row=-ones.
    for i in range(N):
        for j in range(N):
            lift=sum(map(sum,C),F(0)) if i==j==0 else (-sum(C[j-1]) if i==0 else (-sum(C[i-1]) if j==0 else C[i-1][j-1]))
            upper=sum(map(sum,U),F(0)) if i==j==0 else (-sum(U[j-1]) if i==0 else (-sum(U[i-1]) if j==0 else U[i-1][j-1]))
            check(L[i][j]==1+lift and N*int(i==j)-L[i][j]==upper,'every entry of both full E lifts')
    K,U0=forms(n,B);actualK=[];actualU=[]
    for a in range(1,n-1):
        ix=[i for i,A in enumerate(vertices[1:]) if A.bit_count()==a];kr=[];ur=[]
        for b in range(1,n-1):
            jx=[j for j,A in enumerate(vertices[1:]) if A.bit_count()==b]
            kr.append(sum((C[i][j] for i in ix for j in jx),F(0)));ur.append(sum((U[i][j] for i in ix for j in jx),F(0)))
        actualK.append(kr);actualU.append(ur)
    check(actualK==K and actualU==U0,'both complete physical forms reconstructed from every actual index')
    p,q=profiles(n,2);fullp=[p[A.bit_count()-1] for A in vertices[1:]];fullq=[q[A.bit_count()-1] for A in vertices[1:]]
    check(quad(C,fullp)==quad(K,p) and quad(U,fullq)==quad(U0,q),'both rank-one pairings in the original Euclidean metric')
    check(sum(fullp)==n,'unmatched singleton mass: -J contributes -n squared')
    bad=M[0][:];bad[0]=F(0)
    try:need(sum(bad)==1,'damaged object: omitted actual empty loop')
    except ValueError:damages=['omitted_actual_empty_loop']
    else:raise ValueError('missing empty loop accepted')
    return {'n':n,'original_vertex_masks':vertices,'original_sizes':sizes,'empty_loop':str(M[0][0]),'checks':checks,'whole_original_L':[[str(x) for x in row] for row in L],'whole_physical_lower':[[str(x) for x in row] for row in K],'whole_physical_upper':[[str(x) for x in row] for row in U0],'original_lower_pairing':str(quad(C,fullp)),'original_upper_pairing':str(quad(U,fullq)),'nonempty_p_sum':str(sum(fullp)),'mathematical_damage_rejections':damages,'PSD_of_the_baseline_claimed':False}
