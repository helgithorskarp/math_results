"""Fresh FOUR-mark original-set Gram construction; own three-mark vector/LDL/control scaffolding source61516022faa5df5f379af89637b7d3c74f410d10 is reused and credited. New four-mark geometry, sectors and repair coefficients are derived independently; no target executable or old verdict is imported."""
from fractions import Fraction as Q
import json,hashlib,sys,signal
from pathlib import Path


def vecplus(a,b):
    c=a.copy()
    for i,v in b.items():
        c[i]=c.get(i,0)+v
        if c[i]==0:del c[i]
    return c


def vc(a,c):return {i:v*c for i,v in a.items()if v*c}


def vsum(a):
    out={}
    for v in a:out=vecplus(out,v)
    return out


def ldl(A):
    # Complete exact rational symmetric elimination, no floating eigenvalues.
    A=[row[:]for row in A];positive=zero=0;pivots=[]
    for k in range(len(A)):
        pivot=A[k][k]
        if pivot<0:raise ValueError('negative whole original pivot')
        if not pivot:
            if any(A[k][j]for j in range(k+1,len(A))):raise ValueError('zero pivot has nonzero remaining row')
            zero+=1;continue
        positive+=1;pivots.append(str(pivot))
        for i in range(k+1,len(A)):
            if not A[i][k]:continue
            factor=A[i][k]/pivot
            for j in range(i,len(A)):
                A[i][j]-=factor*A[k][j];A[j][i]=A[i][j]
    return {'positive':positive,'zero':zero,'pivots':pivots}

def solve_positive(A,rhs):
    """A new original-coordinate one-RHS elimination, independent of physical dual."""
    A=[row[:]for row in A];rhs=rhs[:];size=len(A);pivots=[]
    for k in range(size):
        pivot=A[k][k]
        if pivot<=0:raise ValueError('original principal solve positive pivot')
        pivots.append(str(pivot))
        for i in range(k+1,size):
            factor=A[i][k]/pivot;rhs[i]-=factor*rhs[k]
            for j in range(i,size):A[i][j]-=factor*A[k][j];A[j][i]=A[i][j]
    x=[Q(0)]*size
    for k in reversed(range(size)):x[k]=(rhs[k]-sum(A[k][j]*x[j]for j in range(k+1,size)))/A[k][k]
    return x,pivots


def construct(n,h,l,defect=None):
    if not(4<=n<=4 and h>l>=2 and h<=4):raise ValueError('fixed literal-control scope')
    q=2**(n-1);F=h+3*l;ell=3*F+1;s=q+3*h;N=2*q+6*F
    if N>80:raise ValueError('fixed N80 literal guard')
    old=list(range(1,2**n));oi={a:i for i,a in enumerate(old)};D=3*h;w=s-1
    groups=[list(range(h))]+[list(range(h+(g-1)*l,h+g*l))for g in range(1,4)]
    group_of={i:g for g,facets in enumerate(groups)for i in facets}
    offset=len(old);Boff=offset;Toff=Boff+F;Moff=Toff+2*F;Aoff=Moff+F;Woff=Aoff+F;dimension=Woff+F
    metric=[[Q(0)for _ in range(dimension)]for _ in range(dimension)]
    for a in old:
        for b in old:metric[oi[a]][oi[b]]=Q(s*(a==b)+(q-D)*(b==((2**n-1)^a))-1)
    def Bvec(i):return {Boff+i:Q(1)}
    def Tvec(i,t):
        if t<2:return {Toff+2*i+t:Q(1)}
        return {Toff+2*i:Q(-1),Toff+2*i+1:Q(-1)}
    H=[{oi[a]:Q(-1)for a in old if a&(1<<g)}for g in range(4)]
    for facets in groups:
        for i in facets:
            for j in facets:metric[Boff+i][Boff+j]=Q(s,3)*(Q(i==j)-Q(1,h))
    for i in range(F):
        for j in range(2):
            for k in range(2):metric[Toff+2*i+j][Toff+2*i+k]=s*(Q(j==k)-Q(1,3))
    oldrows=[{oi[a]:Q(1)}for a in old];marks=[]
    masks=old[:];rowvecs=oldrows[:];private_masks=[];private_vecs=[]
    for i in range(F):
        g=group_of[i];u=1<<(n+2*i);v=1<<(n+2*i+1);mark=1<<g
        for a,mask in enumerate([mark|u,mark|v,mark|u|v]):
            row=vecplus(vecplus(vc(H[g],Q(1,D)),Bvec(i)),Tvec(i,a));marks.append(row);rowvecs.append(row);masks.append(mask)
    K=vsum(oldrows+marks);z=vc(K,Q(-1,ell))
    def dot(a,b):
        return sum(x*y*metric[i][j]for i,x in a.items()for j,y in b.items()if metric[i][j])
    z2=dot(z,z)
    expected_z2=Q(q*ell+27*l*(h-l)-3*h-18*l-1,ell**2)
    if z2!=expected_z2:raise ValueError('whole common-vector norm')
    scalar=[];group_r=[]
    for g,facets in enumerate(groups):
        k=len(facets);Bbar=vc(vsum([Bvec(i)for i in facets]),Q(1,k));B2=Q(s*(k-1),3*k)
        mark_score=dot(z,marks[3*facets[0]])
        r=1+mark_score;a=r/(2*B2);b=-2*a;c=Q(9,2*s)*r
        group_r.append(r)
        etaL=w-z2-a*a*B2-Q(2*s,3)*c*c
        etaF=w-z2-b*b*B2-Q(2*s,3*(k-1))*c*c
        p0=-1-z2-a*b*B2;mu=(2*p0+etaF)/3
        alpha=2*(2*etaL-p0-etaF);beta=etaF-mu
        if mu!=Q(s-3,3)-z2-Q(9,2*s*(k-1))*r*r or alpha!=2*s-Q(27*(2*k-3),s*(k-1))*r*r or beta!=Q(2*s,3)-Q(3*(k+3),s*(k-1))*r*r:
            raise ValueError('full original residual scalar identities')
        if not(mu>Q(s,5) and mu<Q(s,3)and s<alpha<=2*s and Q(s,2)<beta<=Q(2*s,3)):
            raise ValueError('full original scalar bounds')
        scalar.append((mu,alpha,beta))
        for i in facets:
            Btilde=vecplus(Bvec(i),vc(Bbar,-1));u=1<<(n+2*i);v=1<<(n+2*i+1)
            Ps=[vecplus(vecplus(z,vc(Btilde,a)),vc(Tvec(i,1),c)),
                vecplus(vecplus(z,vc(Btilde,a)),vc(Tvec(i,0),c)),
                vecplus(vecplus(z,vc(Btilde,b)),vc(vsum([Tvec(j,2)for j in facets if j!=i]),c/(k-1)))]
            Ws=[{Moff+i:Q(1),Aoff+i:Q(1,2),Woff+i:Q(-1,2)},
                {Moff+i:Q(1),Aoff+i:Q(-1,2),Woff+i:Q(-1,2)},
                {Moff+i:Q(1),Woff+i:Q(1)}]
            for row,wr,mask in zip(Ps,Ws,[u,v,u|v]):private_vecs.append(vecplus(row,wr));private_masks.append(mask)
    Smean=sum(len(groups[g])*scalar[g][0]for g in range(4))
    for i in range(F):
        g=group_of[i];mu,alpha,beta=scalar[g];k=len(groups[g]);metric[Aoff+i][Aoff+i]=alpha;metric[Woff+i][Woff+i]=beta
        for j in range(F):
            gj=group_of[j];mj=scalar[gj][0]
            metric[Moff+i][Moff+j]=mu if i==j else (-k*mu*mu/(Smean*(k-1))if g==gj else -mu*mj/Smean)
    masks+=private_masks;rowvecs+=private_vecs
    if len(masks)!=N-1 or len(set(masks))!=N-1:raise ValueError('literal proper census')
    original=sorted(set(range(2**n))|set(masks))
    if len(original)!=N or any((a^(1<<j))not in original for a in original for j in range(n+2*F)if a&(1<<j)):raise ValueError('literal downset')
    stars=[sum(bool(a&(1<<j))for a in original)for j in range(n+2*F)]
    if defect=='star-census':stars[1]=s
    if stars!=[s]+[q+3*l]*3+[q]*(n-4)+[4]*(2*F)or stars.count(s)!=1:raise ValueError('all original star sizes')
    # Compute every actual original Gram position, including empty.
    vectors=[z]+rowvecs;allmasks=[0]+masks
    if defect=='empty-row':vectors[0]={}
    G=[[dot(a,b)for b in vectors]for a in vectors]
    if any(sum(row)for row in G):raise ValueError('actual empty negative-row-sum Gram')
    if any(G[i][i]!=w for i in range(1,N)):raise ValueError('all original proper norms')
    if any(G[i][j]!=-1 for i in range(1,N)for j in range(1,N)if i!=j and allmasks[i]&allmasks[j]):raise ValueError('all mandatory original intersections')
    C=[row[1:]for row in G[1:]];chi=[Q(bool(a&1))for a in masks];rho=[Q(3*F,ell)if i<len(old)+3*F else Q(1)for i in range(N-1)]
    if any(sum(C[i][j]*chi[j]for j in range(N-1))or sum(C[i][j]*rho[j]for j in range(N-1))for i in range(N-1)):
        raise ValueError('both complete original kernel relations')
    # Independently form complete even-five physical scores and compare closed fields.
    gold=vsum(oldrows);gX=oldrows[-1];U=vecplus(gold,gX);E=vecplus(gold,vc(gX,-1))
    R=vecplus(vsum(H),vc(U,2));Hc=vecplus(vc(H[0],3),vc(vsum(H[1:]),-1))
    Bsum=vc(vsum([Bvec(i)for facets in groups[1:]for i in facets]),Q(1,l))
    if defect=='light-mean-omitted':Bsum=vc(vsum([Bvec(i)for i in groups[1]]),Q(1,l))
    basis=[E,U,R,Hc,Bsum];g5=[[dot(a,b)for b in basis]for a in basis]
    expected_g5=[4*(q-1),4*D,4*D*(q-4),12*q*D,Q(s*(h-l),h*l)]
    if g5!=[[Q(i==j)*expected_g5[i]for j in range(5)]for i in range(5)]:
        raise ValueError('all original physical five-block metric entries')
    scores=[[dot(row,b)for b in basis]for row in vectors];S5=[[sum(v[i]*v[j]for v in scores)for j in range(5)]for i in range(5)]
    from polynomials import original_forms,value
    form,_=original_forms();coords=(h-l-1,l-2,q-8)
    for i in range(5):
        for j in range(5):
            want=Q(value(form[i][j][0],coords),value(form[i][j][1],coords))
            actual=((N-1)*g5[i][j]-S5[i][j])/g5[i][i]
            if actual!=want:raise ValueError('all original physical five-block entries')
    # Complete original physical sectors, not a selected principal submatrix.
    odd=[]
    for profile in [(1,-1,0),(1,1,-2)]:
        Hd=vsum([vc(H[g],t)for g,t in enumerate(profile,1)])
        Bdiff=vsum([vc(vsum([Bvec(i)for i in groups[g]]),Q(t,l))for g,t in enumerate(profile,1)])
        odd.append([Hd,Bdiff])
    TS=[vecplus(vecplus(Tvec(i,0),Tvec(i,1)),vc(Tvec(i,2),-2))for i in range(F)]
    blocks=[];labels=[]
    def block(label,rows):
        if rows:labels.append(label);blocks.append(rows)
    for i in range(F):block('leaf '+str(i),[vecplus(Tvec(i,0),vc(Tvec(i,1),-1)),{Aoff+i:Q(1)}])
    for g,facets in enumerate(groups):
        for j in range(1,len(facets)):
            weights=[Q(1)]*j+[Q(-j)]+[Q(0)]*(len(facets)-j-1)
            block('standard '+str((g,j)),[vsum([vc(Bvec(i),t)for i,t in zip(facets,weights)]),
                  vsum([vc(TS[i],t)for i,t in zip(facets,weights)]),
                  {Woff+i:t for i,t in zip(facets,weights)if t},
                  {Moff+i:t for i,t in zip(facets,weights)if t}])
    block('even-five',basis)
    for i,rows in enumerate(odd):block('light-standard '+str(i),rows)
    for g,facets in enumerate(groups):block('trace '+str(g),[vsum([TS[i]for i in facets]),{Woff+i:Q(1)for i in facets}])
    block('whole means',[{Moff+i:Q(1)for i in facets}for facets in groups[:3]])
    def orthogonal(rows,project):
        paid=[]
        for row in rows:
            for p in project+paid:row=vecplus(row,vc(p,-dot(row,p)/dot(p,p)))
            if dot(row,row):paid.append(row)
        return paid
    pairs=[(a,(2**n-1)^a)for a in old if a<((2**n-1)^a)]
    sums=orthogonal([vecplus(oldrows[oi[a]],oldrows[oi[b]])for a,b in pairs],[E,U])
    diffs=orthogonal([vecplus(oldrows[oi[a]],vc(oldrows[oi[b]],-1))for a,b in pairs],[R,Hc]+[row[0]for row in odd])
    if len(sums)!=q-2 or len(diffs)!=q-5:raise ValueError('complete untouched old dimensions')
    block('old sum',sums);block('old difference',diffs)
    flat=[v for rows in blocks for v in rows]
    if len(flat)!=N-3:raise ValueError('complete original physical dimension')
    scores2=[[dot(row,b)for row in vectors]for b in flat]
    blockpos=[];start=0
    for rows in blocks:
        pos=list(range(start,start+len(rows)));blockpos.append(pos);start+=len(rows)
        mg=[[dot(flat[i],flat[j])for j in pos]for i in pos]
        if ldl(mg)['positive']!=len(rows):raise ValueError('each complete physical metric block')
    cross=0
    for bi,positions in enumerate(blockpos):
        for other in blockpos[bi+1:]:
            for i in positions:
                for j in other:
                    if dot(flat[i],flat[j])or sum(a*b for a,b in zip(scores2[i],scores2[j])):raise ValueError('every original physical metric and frame cross entry')
                    cross+=1
    # New separate binding of EVERY complete non-five-block frame position.
    # The prototype construction uses only full coordinate rows/counts.
    from blocks import literal_prototype,evaluate
    frame_bindings=0
    for label,positions in zip(labels,blockpos):
        mg=[[dot(flat[i],flat[j])for j in positions]for i in positions]
        sf=[[sum(a*b for a,b in zip(scores2[i],scores2[j]))for j in positions]for i in positions]
        proto=literal_prototype(label,s,scalar,groups,h,l,q)
        if proto is not None:
            kind,g,k,proto_metric,polys,factor=proto;r=group_r[g];a=Q(3*k,2*s*(k-1))*r;c=Q(9,2*s)*r;t=Q(1,k-1)
            if mg!=[[Q(i==j)*factor*proto_metric[i]for j in range(len(positions))]for i in range(len(positions))]:
                raise ValueError('every original non-five prototype metric binding')
            for i in range(len(positions)):
                for j in range(len(positions)):
                    want=evaluate(polys[i][j],a,c,t)*proto_metric[j]
                    if sf[i][j]/mg[i][i]!=want:raise ValueError('every original non-five prototype frame binding')
                    frame_bindings+=1
        elif label.startswith('light-standard '):
            b0=Q(s*(h-l),3*h*l);factor=2 if label.endswith('0')else 6
            if mg!=[[factor*q*D,0],[0,factor*b0]]:raise ValueError('both whole original light-standard metrics')
            expected=[[factor*(2*q*D*D+3*l*q*q),factor*3*l*q*b0],
                      [factor*3*l*q*b0,factor*3*l*b0*b0]]
            if sf!=expected:raise ValueError('both whole original light-standard frames')
            frame_bindings+=4
        elif label in ['old sum','old difference']:
            lam=2*q if label=='old sum'else 2*D
            if sf!=[[lam*v for v in row]for row in mg]:raise ValueError('every untouched old frame position')
            frame_bindings+=len(positions)**2
        elif label=='whole means':
            S=sum(len(f)*scalar[g][0]for g,f in enumerate(groups));mx=scalar[0][0];my=scalar[1][0];tau=mx*my/S
            z=my-l*my*my/S;e=-l*my*my/S
            expected_mg=[[3*h*l*tau,-h*l*tau,-h*l*tau],[-h*l*tau,l*z,l*e],[-h*l*tau,l*e,l*z]]
            if mg!=expected_mg:raise ValueError('every original full mean metric position')
            rowtypes=[(h,[3*l*tau,-l*tau,-l*tau]),(l,[-h*tau,z,e]),(l,[-h*tau,e,z]),(l,[-h*tau,e,e])]
            expected=[[3*sum(count*row[i]*row[j]for count,row in rowtypes)for j in range(3)]for i in range(3)]
            if sf!=expected:raise ValueError('every original full mean frame position')
            frame_bindings+=9
        elif label!='even-five':raise ValueError('complete prototype frame coverage')
    # All generators available on the literal instance, including both adjacent
    # light exchanges which together generate the complete light S3.
    generators=[]
    for i in range(F):generators.append({n+2*i:n+2*i+1,n+2*i+1:n+2*i})
    for facets in groups:
        for i,j in zip(facets,facets[1:]):generators.append({n+2*i:n+2*j,n+2*i+1:n+2*j+1,n+2*j:n+2*i,n+2*j+1:n+2*i+1})
    for left,right in [(1,2),(2,3)]:
        light={left:right,right:left}
        for i,j in zip(groups[left],groups[right]):light.update({n+2*i:n+2*j,n+2*i+1:n+2*j+1,n+2*j:n+2*i,n+2*j+1:n+2*i+1})
        generators.append(light)
    where={a:i for i,a in enumerate(allmasks)}
    for perm in generators:
        images=[where[sum(1<<perm.get(j,j)for j in range(n+2*F)if a&(1<<j))]for a in allmasks]
        if any(G[i][j]!=G[images[i]][images[j]]for i in range(N)for j in range(N)):raise ValueError('complete original invariant Gram')
    # Fresh original pseudoinverse dual as a physical vector, not a solver input.
    tau=scalar[0][0]*scalar[1][0]/Smean
    dual=vecplus({Moff+i:Q(1,3*h*l)/tau for i in groups[0]},
                 {Woff+i:Q(-2,3*l)/scalar[1][2]for facets in groups[1:]for i in facets})
    # Use actual facet private masks to avoid bit-class ambiguity.
    aset={private_masks[j]for j in range(3*F)if group_of[j//3]==0}
    bset={private_masks[j]for j in range(3*F)if group_of[j//3]in[1,2,3]and j%3==2}
    aa=[Q(1,h)if mask in aset else Q(0)for mask in masks];bb=[Q(1,3*l)if mask in bset else Q(0)for mask in masks]
    pp=[a-3*b for a,b in zip(aa,bb)];cc=[(a+3*b)/6 for a,b in zip(aa,bb)]
    if defect=='light-dual':dual={k:v for k,v in dual.items()if k<Moff+F}
    if [dot(row,dual)for row in vectors]!=[Q(0)]+pp:raise ValueError('every original dual score and actual empty')
    kappa=dot(dual,dual)
    if kappa!=1/(h*scalar[0][0])+1/(3*l*scalar[1][0])+Q(4,3*l)/scalar[1][2]or not 0<kappa<Q(23,102):raise ValueError('whole dual norm')
    if sum(aa)!=3 or sum(bb)!=1 or sum(chi[i]*pp[i]for i in range(N-1))or sum(rho[i]*pp[i]for i in range(N-1))or sum(rho[i]*cc[i]for i in range(N-1))!=1:
        raise ValueError('full repair null relations')
    seed=ldl(C)
    cap=[[(N-1)*(Q(i==j)-Q(1,N))-G[i][j]for j in range(1,N)]for i in range(1,N)]
    cap_record=ldl(cap)
    if seed['positive']!=N-3 or seed['zero']!=2 or cap_record['positive']!=N-1:raise ValueError('original full seed ranks and cap')
    # Exactly two deleted rows distinguish the independent kernel relations.
    deleted=[masks.index(1),len(old)+3*F];keep=[i for i in range(N-1)if i not in deleted]
    kernel_minor=chi[deleted[0]]*rho[deleted[1]]-chi[deleted[1]]*rho[deleted[0]]
    if kernel_minor!=1:raise ValueError('original two-kernel deletion minor')
    solution,solve_pivots=solve_positive([[C[i][j]for j in keep]for i in keep],[pp[i]for i in keep])
    x=[Q(0)]*(N-1)
    for i,z in zip(keep,solution):x[i]=z
    if defect=='deleted-inverse-row':x[deleted[0]]=1
    if any(sum(C[i][j]*x[j]for j in range(N-1))!=pp[i]for i in range(N-1)):
        raise ValueError('every original inverse equation including deleted rows')
    if sum(p*z for p,z in zip(pp,x))!=kappa:raise ValueError('original inverse norm agrees with fresh physical dual')
    cx=sum(c*z for c,z in zip(cc,x));endpoint=[z-cx*r for z,r in zip(x,rho)]
    if sum(c*z for c,z in zip(cc,endpoint))or sum(p*z for p,z in zip(pp,endpoint))!=kappa:
        raise ValueError('complete original endpoint projection')
    outside=[]
    fullA=[Q(-3)]+aa;fullB=[Q(-1)]+bb
    for delta,proper,want in [(Q(-1),rho,Q(-6)),(7/kappa,endpoint,-kappa/6)]:
        lifted=[Q(0)]+proper;mean=sum(lifted)/N;centered=[v-mean for v in lifted]
        if defect=='outside-empty-lift':centered[0]=Q(0)
        L=[[1+G[i][j]+delta*(fullA[i]*fullB[j]+fullB[i]*fullA[j])for j in range(N)]for i in range(N)]
        energy=sum(centered[i]*L[i][j]*centered[j]for i in range(N)for j in range(N))
        if sum(centered)or energy!=want or energy>=0:raise ValueError('complete original centered outside-line witness')
        outside.append({'delta':str(delta),'whole_original_coordinates':N,'centered_vector':[str(v)for v in centered],'negative_energy':str(energy)})
    records=[]
    for delta in [Q(1,32),Q(3,20),6/kappa]:
        changed=[[C[i][j]+delta*(aa[i]*bb[j]+bb[i]*aa[j])for j in range(N-1)]for i in range(N-1)]
        rnk=ldl(changed)
        if rnk['positive']!=(N-3 if delta==6/kappa else N-2):raise ValueError('whole real-line original lower rank')
        fullA=[Q(-3)]+aa;fullB=[Q(-1)]+bb
        if sum(fullA)or sum(fullB)or sum(a*b for a,b in zip(fullA,fullB))!=3:
            raise ValueError('complete actual zero-sum repair vectors')
        a2=sum(a*a for a in fullA);b2=sum(b*b for b in fullB)
        if a2>10 or b2>Q(7,6)or a2*b2>=Q(55,16)**2:
            raise ValueError('complete actual rank-two norm bound')
        L=[[1+G[i][j]+delta*(fullA[i]*fullB[j]+fullB[i]*fullA[j])for j in range(N)]for i in range(N)]
        M=[[(L[i][j]-s*Q(i==j))/(N-s)for j in range(N)]for i in range(N)]
        centered=[Q(bool(mask&1))-Q(s,N)for mask in allmasks]
        if any(sum(row)!=1 for row in M)or any(M[i][j]for i in range(N)for j in range(N)if allmasks[i]&allmasks[j]):
            raise ValueError('every actual supported stochastic position')
        if any(sum(L[i][j]*centered[j]for j in range(N))for i in range(N)):
            raise ValueError('complete centered-heavy-star lower kernel')
        actual_lower=ldl(L)
        if actual_lower['positive']!=(N-2 if delta==6/kappa else N-1):
            raise ValueError('complete actual lower rank')
        cap_result=None;floor=None
        if delta!=6/kappa:
            floor=1-Q(103,16)*delta
            cap2=[[(N-floor)*(Q(i==j)-Q(1,N))-(L[i][j]-1)for j in range(1,N)]for i in range(1,N)]
            cap_result=ldl(cap2)
            if cap_result['positive']!=N-1:raise ValueError('new actual-empty cap floor')
            if delta==Q(3,20):caps=cap_result
        records.append({'delta':str(delta),'proper_lower':rnk,'actual_lower':actual_lower,
                        'all_original_M_positions':N*N,'all_actual_rows_support_and_centered_star':True,
                        'actual_upper_cap_floor':str(floor)if floor else None,'actual_upper_cap':cap_result})
    digest=lambda a:hashlib.sha256(json.dumps([[str(v)for v in row]for row in a],separators=(',',':')).encode()).hexdigest()
    return {'n':n,'h':h,'l':l,'N':N,'s':s,'all_actual_Gram_positions':N*N,'proper_positions':(N-1)**2,
            'actual_empty_retained':True,'all_support_rows_kernels_and_star_sizes_checked':True,
            'five_complete_physical_form_positions':25,'whole_original_Gram_sha256':digest(G),
            'full_physical_dimension':len(flat),'physical_block_dimensions':dict(zip(labels,map(len,blocks))),
            'all_cross_metric_and_frame_positions':cross,'literal_invariance_generators':len(generators),
            'all_additional_original_block_frame_bindings':frame_bindings,
            'original_inverse':{'deleted_rows':deleted,'kernel_minor':str(kernel_minor),'all_original_equations':N-1,'positive_pivots':solve_pivots,'norm':str(kappa),'whole_solution':[str(v)for v in x]},
            'outside_line_witnesses':outside,
            'seed':seed,'seed_cap':cap_record,'kappa':str(kappa),'line_records':records,
            'all_original_star_sizes':stars,'new_cap':caps,
            'new_delta_three_twentieths_cap_floor':'11/320','all_original_dual_positions':N}


if __name__=='__main__':
    signal.alarm(45);a=list(map(int,sys.argv[1:4]));out=construct(*a);Path(sys.argv[4]).write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print({k:v for k,v in out.items()if k not in ['seed','seed_cap','line_records','new_cap']})
