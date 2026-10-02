"""Original sets, Gram entries and physical frames, independently reconstructed.
Defining mathematical formulas are credited to LEMMA9305; no author module.
"""
from itertools import combinations
from linear import F,need,digest,psd,mv,dot,form,inverse
from scalars import profile

def plus(*terms):return [sum(a*v[j] for a,v in terms) for j in range(len(terms[0][1]))]
def unit(n,j):return [F(i==j) for i in range(n)]
def gram(A,cols):
    products=[mv(A,v) for v in cols]
    return [[dot(v,w) for w in products] for v in cols]
def physical_frame(A,left,right=None):
    right=left if right is None else right
    l=[mv(A,x) for x in left];r=[mv(A,x) for x in right]
    # The ACTUAL empty vector is minus the sum of original nonempty vectors.
    return [[dot(x,y)+sum(x)*sum(y) for y in r] for x in l]
def qlift(C):
    sums=[sum(row) for row in C]
    return [[sum(sums)]+[-x for x in sums]]+[[-sums[i]]+row for i,row in enumerate(C)]
def audit(q,loads,marks):
    p=profile(q,loads);R=p['R'];D=p['D'];m=p['m'];k=loads.count(D);w=p['w'];h=p['h'];s=w+1
    n=q.bit_length();need(q==2**(n-1) and n>=R and 4<=n<=6,'bounded Boolean domain')
    need(type(marks) is list and len(marks)==R and len(set(marks))==R and all(type(i) is int and 0<=i<n for i in marks),'distinct marks')
    old=[frozenset(A) for r in range(1,n+1) for A in combinations(range(n),r)]
    old.reverse() # Deliberately different from binary sorted author order.
    nold=len(old);full=frozenset(range(n));oi={A:i for i,A in enumerate(old)}
    ylist=[(i,u,n+sum(loads[:i])+u) for i,d in enumerate(loads) for u in range(d)]
    spoke=[frozenset([marks[i],y]) for i,u,y in ylist];single=[frozenset([y]) for i,u,y in ylist]
    sets=[frozenset()]+old+spoke+single;N=len(sets);a=nold+m;t=N-1
    need(N==2*q+2*m and len(set(sets))==N,'whole domain cardinality/unique actual sets')
    domain=set(sets)
    need(all(A-frozenset([x]) in domain for A in sets for x in A),'downset deletion closure')
    actual_stars=[[F(x in A) for A in sets] for x in range(n+m)]
    sizes=[sum(v) for v in actual_stars];need(max(sizes)==s and sum(z==s for z in sizes)==k,'actual maximum stars')
    B=[[F(0)]*a for _ in range(a)]
    for i,A in enumerate(old):
        for j,E in enumerate(old):B[i][j]=F(s*int(i==j)+(q-D)*int(A!=full and A|E==full and not A&E)-1)
    for z,(i,u,y) in enumerate(ylist):
        for j,A in enumerate(old):B[j][nold+z]=B[nold+z][j]=F(-1 if marks[i] in A else 1)
        for zz,(j,v,yy) in enumerate(ylist):B[nold+z][nold+zz]=F((s*int(z==zz)-1) if i==j else 0)
    G=[F(i<nold) for i in range(a)];ff=unit(a,oi[full]);Hi=[[-F(j<nold and marks[i] in old[j]) for j in range(a)] for i in range(R)]
    K=[F(1)]*a;Cs=[F(0)]*nold+[p['c'][i] for i,u,y in ylist]
    need(form(B,K,K)==p['B0'] and form(B,Cs,Cs)==p['C2'] and form(B,K,Cs)==p['KC'],'literal K/C scalar identities')
    need(gram(B,[G,ff]+Hi)==[[F(w),F(D+1-q)]+[-F(D)]*R,[F(D+1-q),F(w)]+[-F(D)]*R]+[[-F(D),-F(D)]+[F(q*D*int(i==j)) for j in range(R)] for i in range(R)],'literal complete old G,f,H Gram')
    bk=mv(B,K);bc=mv(B,Cs);zall=[p['zeta'][i] for i,u,y in ylist];ztotal=sum(zall)
    C=[[F(0)]*t for _ in range(t)];Raw=[[F(0)]*t for _ in range(t)]
    for i in range(a):
        C[i][:a]=B[i][:];Raw[i][:a]=B[i][:]
    for z,(mark,u,y) in enumerate(ylist):
        c=p['c'][mark];zi=zall[z];v=nold+z;ii=a+z
        for j in range(a):
            C[ii][j]=C[j][ii]=-bk[j]/(m+1)+c*B[v][j]-bc[j]/m
            Raw[ii][j]=Raw[j][ii]=-B[v][j]/w
        for zz,(markj,u2,y2) in enumerate(ylist):
            cj=p['c'][markj];vj=nold+zz;jj=a+zz
            W=F(z==zz)*zi-(zi+zall[zz])/m+ztotal/m**2
            C[ii][jj]=F(p['B0'],(m+1)**2)+c*cj*B[v][vj]+p['C2']/m**2-(c*bk[v]+cj*bk[vj])/(m+1)+2*p['KC']/(m*(m+1))-(c*bc[v]+cj*bc[vj])/m+W
            Raw[ii][jj]=B[v][vj]/w**2+F(z==zz)*(w-F(1,w))
    need(all(C[i][i]==w and Raw[i][i]==w for i in range(t)),'all seed/raw norms')
    need(all(not sets[i+1]&sets[j+1] or C[i][j]==Raw[i][j]==-1 for i in range(t) for j in range(i)),'all actual intersecting off-diagonals')
    Qs=qlift(C);Qr=qlift(Raw);Traw=sum(Qr[i][i] for i in range(N))
    Braw=w+(1-F(1,w))**2*(m*s-sum(d*d for d in loads))-2*m*(1-F(1,w))+m*(w-F(1,w))
    need(Traw==(N-1)*w+Braw,'actual raw trace includes empty loop')
    eps=F(1,2*(1+Traw));Q=[[ (1-eps)*x+eps*y for x,y in zip(row,other)] for row,other in zip(Qs,Qr)]
    L=[[x+1 for x in row] for row in Q];M=[[(L[i][j]-s*int(i==j))/(N-s) for j in range(N)] for i in range(N)]
    for i,A in enumerate(sets):
        need(sum(Q[i])==0 and sum(L[i])==N and sum(M[i])==1,'all actual full row sums')
        need(all(not A&E or M[i][j]==0 for j,E in enumerate(sets)),'actual full H support/loops')
    stars=[]
    for i,d in enumerate(loads):
        if d!=D:continue
        star=actual_stars[marks[i]];center=[v-F(s,N) for v in star];stars.append(center)
        need(mv(Qs,star)==[0]*N and mv(Qr,star)==[0]*N and mv(L,center)==[0]*N,'actual heavy stars and centered lower kernel')
    need(psd([[dot(x,y) for y in stars] for x in stars])['rank']==k,'centered actual star independence')
    ranks={name:psd(matrix) for name,matrix in [('seed_core',C),('raw_core',Raw),('mixed_lower',L)]}
    need(ranks['seed_core']['rank']==N-k-2 and ranks['raw_core']['rank']==N-k-1 and ranks['mixed_lower']['rank']==N-k,'all exact lower ranks')
    P=[[F(i==j)-F(1,N) for j in range(N)] for i in range(N)]
    seedgap=[[h*P[i][j]-Qs[i][j] for j in range(N)] for i in range(N)]
    margin=F(1,2)+F(N,2*(Traw+1))
    mixedgap=[[(N-margin)*P[i][j]-Q[i][j] for j in range(N)] for i in range(N)]
    gaps={'seed':psd(seedgap),'mixed':psd(mixedgap)}
    need(all(z['rank']==N-1 for z in gaps.values()),'whole physical strict endpoint caps')
    # ORIGINAL-COORDINATE physical means. Recover W from singleton entries.
    extend=lambda v:v+[F(0)]*m
    G=extend(G);ff=extend(ff);Hi=[extend(v) for v in Hi];K=extend(K);Cs=extend(Cs)
    Li=[];Wi=[];Ai=[];Zi=[]
    for i,d in enumerate(loads):
        inds=[z for z,(mark,u,y) in enumerate(ylist) if mark==i]
        Li.append([F(j in [nold+z for z in inds],d) for j in range(t)])
        Umean=[F(j in [a+z for z in inds],d) for j in range(t)]
        Wi.append(plus((1,Umean),(F(1,m+1),K),(-p['c'][i],Li[-1]),(F(1,m),Cs)))
    h0=plus((F(-1,2),G),(F(-1,2),ff));Gp=plus((1,G),(1,h0))
    Ai=[plus((1,v),(-1,h0)) for v in Hi]
    for i,d in enumerate(loads):
        if d!=D:Zi.append(plus((1,Li[i]),(F(-1,D),Hi[i])))
    Bmean=[Gp,h0]+Ai+Zi;means=Bmean+Wi[:-1];metric=gram(C,means)
    need(psd(metric)['rank']==3*R-k+1,'independent complete physical mean basis')
    need(mv(C,plus(*[(d,v) for d,v in zip(loads,Wi)]))==[0]*t,'weighted residual means sum zero')
    # All physical frame entries compared to means plus complete global K term.
    sig=[plus((p['c'][i],Li[i]),(F(-1,m),Cs),(1,Wi[i])) for i in range(R)]
    cm=[mv(C,v) for v in means];ftarget=physical_frame(C,means)
    fdecl=[]
    for x in cm:
        row=[]
        for y in cm:
            oldterm=dot(x[:nold],y[:nold]);lterm=sum(d*dot(x,li)*dot(y,li) for d,li in zip(loads,Li));kterm=dot(x,K)*dot(y,K)/(m+1);sterm=sum(d*dot(x,v)*dot(y,v) for d,v in zip(loads,sig))
            row.append(oldterm+lterm+kterm+sterm)
        fdecl.append(row)
    need(ftarget==fdecl,'every literal changed mean-frame entry including actual empty')
    # Invert actual physical h*metric-Fbase, independent of displayed resolvent.
    gm=gram(C,Bmean);bp=[mv(C,v) for v in Bmean];f0=[[dot(x[:nold],y[:nold]) for y in bp] for x in bp]
    inv0=inverse([[h*x-y for x,y in zip(row,fr)] for row,fr in zip(gm,f0)])
    cov=lambda v:[dot(b,v) for b in bp]
    cg=cov(G);cl=[cov(li) for li in Li];ck=cov(K)
    need(form(inv0,cg,cg)==p['Rgg'],'physical Rgg')
    need(all(form(inv0,cg,z)==-p['rho'] for z in cl),'every physical G,Li resolvent')
    need(all(form(inv0,x,y)==F(i==j)*p['gamma'][i]/loads[i]-p['kap'] for i,x in enumerate(cl) for j,y in enumerate(cl)),'every initial physical Li,Lj resolvent')
    fs=[[f0[i][j]+sum(d*cl[z][i]*cl[z][j] for z,d in enumerate(loads)) for j in range(len(bp))] for i in range(len(bp))]
    invs=inverse([[h*x-y for x,y in zip(row,fr)] for row,fr in zip(gm,fs)])
    actualKgap=m+1-form(invs,ck,ck);need(actualKgap==p['Kgap'],'literal K Schur slack')
    need(all(form(invs,x,ck)==p['nu'][i] for i,x in enumerate(cl)),'every updated K cross product')
    fb=[[fs[i][j]+ck[i]*ck[j]/(m+1) for j in range(len(bp))] for i in range(len(bp))]
    invb=inverse([[h*x-y for x,y in zip(row,fr)] for row,fr in zip(gm,fb)])
    physicalGamma=[[form(invb,x,y) for y in cl] for x in cl]
    need(physicalGamma==p['Gamma'],'every doubly updated Gamma entry')
    # Every internal direction, all cross Gram/frame entries, exact counts.
    internal=[]
    for i,d in enumerate(loads):
        inds=[z for z,(mark,u,y) in enumerate(ylist) if mark==i]
        for z in inds[:-1]:
            last=inds[-1];v=plus((1,unit(t,nold+z)),(-1,unit(t,nold+last)))
            res=plus((1,unit(t,a+z)),(-1,unit(t,a+last)),(-p['c'][i],v))
            internal.extend([v,res])
    need(len(internal)==2*(m-R),'internal count')
    if internal:
        need(psd(gram(C,internal))['rank']==len(internal),'independent internal directions')
        need(all(x==0 for row in [[form(C,u,v) for v in means] for u in internal] for x in row),'all internal-mean Gram cross entries')
        need(all(x==0 for row in physical_frame(C,internal,means) for x in row),'all internal-mean FRAME cross entries')
    pairs=[]
    for A in old:
        comp=full-A
        if comp and oi[A]<oi[comp]:pairs.append((oi[A],oi[comp]))
    need(len(pairs)==q-1,'proper complement census')
    pc=[plus((1,unit(t,i)),(1,unit(t,j))) for i,j in pairs]
    high=[plus((1,v),(-1,pc[0])) for v in pc[1:]]
    low0=[plus((1,unit(t,i)),(-1,unit(t,j))) for i,j in pairs]
    iga=inverse(gram(C,Ai));low=[]
    for v in low0:
        weights=mv(iga,[form(C,a,v) for a in Ai]);low.append(plus((1,v),*[(-coef,col) for coef,col in zip(weights,Ai)]))
    for cols,eigen,dimension in [(high,2*q,q-2),(low,2*D,q-R-1)]:
        gg=gram(C,cols);fr=physical_frame(C,cols)
        need(psd(gg)['rank']==dimension and fr==[[eigen*x for x in row] for row in gg],'untouched actual full-frame eigenaction/rank')
        for other in [means,internal]:
            need(all(form(C,u,v)==0 for u in cols for v in other),'untouched cross Gram')
            need(all(z==0 for row in physical_frame(C,cols,other) for z in row),'untouched cross FRAME')
    need(3*R-k+1+len(internal)+q-2+q-R-1==N-k-2,'complete physical census')
    # These damage controls reach mandatory H equations, not expected fixtures.
    damages=0
    for mode in ['intersect','empty']:
        bad=[row[:] for row in M]
        if mode=='empty':bad[0][0]+=1
        else:
            ii=sets.index(single[0]);jj=sets.index(spoke[0]);bad[ii][jj]=bad[jj][ii]=1
        rejected=any(sum(row)!=1 for row in bad) or any(A&E and bad[i][j]!=0 for i,A in enumerate(sets) for j,E in enumerate(sets))
        need(rejected,'meaningful damaged whole matrix rejected');damages+=1
    return {'q':q,'loads':loads,'marks':marks,'N':N,'s':s,'k':k,'whole_ordered_positions':N*N,'original_set_sha256':digest([sorted(A) for A in sets]),'seed_Gram_sha256':digest(Qs),'raw_Gram_sha256':digest(Qr),'mixed_H_sha256':digest(M),'empty_H_loop':M[0][0],'Traw':Traw,'epsilon':eps,'scaled_upper_floor':margin,'ranks':ranks,'gaps':gaps,'mean_dimension':len(means),'mean_Gram_sha256':digest(metric),'whole_mean_frame_sha256':digest(ftarget),'mean_frame_positions':len(means)**2,'Gamma_positions':R*R,'physical_Gamma':physicalGamma,'physical_Kgap':actualKgap,'internal_dimension':len(internal),'old_high_dimension':q-2,'old_low_dimension':q-R-1,'sector_dimension':N-k-2,'damage_rejections':damages,'scalar_record_sha256':digest({key:p[key] for key in ['c','eta','zeta','Gamma','budget','Kgap']})}
