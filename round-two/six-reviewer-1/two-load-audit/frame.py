"""Independent literal full S_k x S_r frame and census controls.

Unnormalized difference bases avoid square roots and do not use researcher
frames. Every entry is computed from original set vectors and the actual empty
lift. Symbolic sign proof supplies the unbounded range; these finite controls
check reduction, boundaries, indices and every cross-sector entry.
"""
import literal as L
from fractions import Fraction as F


def audit(d):
    q,k,r,D,t,m,N=(d[x] for x in ['q','k','r','D','t','m','N'])
    a,u=k*D,r*t;c=d['seed'];size=N-1;oldn=2*q-1
    G=[F(i<oldn) for i in range(size)]
    h0=L.lin((-F(1,2),G),(-F(1,2),L.unit(size,oldn-1)))
    gp=L.lin((1,G),(1,h0))
    H=[row+[F()]*(size-oldn) for row in d['H']]
    A=[L.lin((1,v),(-1,h0)) for v in H]
    S=[L.unit(size,i) for i in d['Sindices']];U=[L.unit(size,i) for i in d['Uindices']]
    loads=[D]*k+[t]*r;starts=[];j=0
    for load in loads:starts.append(j);j+=load
    means=[L.lin(*[(F(1,load),v) for v in S[start:start+load]]) for start,load in zip(starts,loads)]
    leafmeans=[L.lin(*[(F(1,load),v) for v in U[start:start+load]]) for start,load in zip(starts,loads)]
    Z=[L.lin((1,means[i]),(-F(1,D),H[i])) for i in range(k,k+r)]
    LH=L.lin(*[(F(1,k),v) for v in means[:k]])
    ell=L.lin(*[(F(1,r),v) for v in means[k:]])
    K=L.lin((1,G),*[(1,v) for v in S]);ch,cl=d['c'];zh,zl=d['zeta']
    mean_contrast=L.lin((F(u,m)*ch,LH),(-F(u,m)*cl,ell))
    Ws=L.lin(*[(F(1,k),v) for v in leafmeans[:k]],(F(1,m+1),K),(-1,mean_contrast))
    coords=[gp,h0,L.lin(*[(F(1,k),v) for v in A[:k]]),L.lin(*[(F(1,r),v) for v in A[k:]]),L.lin(*[(F(1,r),v) for v in Z]),Ws]
    blocks=[]
    # Within a type use coefficient basis e_i-e_0. Its Gram is1+delta.
    for start,count,load,ci,zi,tag in [(0,k,D,ch,zh,'heavy_standard'),(k,r,t,cl,zl,'light_standard')]:
        if count==1:continue
        hs=[L.lin((1,H[i]),(-1,H[start])) for i in range(start+1,start+count)]
        ss=[L.lin((1,means[i]),(-1,means[start])) for i in range(start+1,start+count)]
        ww=[L.lin((1,leafmeans[i]),(-1,leafmeans[start]),(-ci,ss[i-start-1])) for i in range(start+1,start+count)]
        if tag=='heavy_standard':
            vectors=[hs,ww];norms=[F(q*D),zi/D];pp=[F(q),F()]
        else:
            zz=[L.lin((1,v),(-F(1,D),hs[j])) for j,v in enumerate(ss)]
            vectors=[hs,zz,ww];norms=[F(q*D),(q+D)*(F(1,t)-F(1,D)),zi/t];pp=[F(q),norms[1],F()]
        vv=[ci*x for x in pp];vv[-1]+=norms[-1]
        action=[[F(2*D)*norms[0]*int(i==0 and j==0)+load*(pp[i]*pp[j]+vv[i]*vv[j]) for j in range(len(norms))] for i in range(len(norms))]
        offset=len(coords);coords.extend(v for rows in vectors for v in rows)
        blocks.append((offset,count-1,norms,action,tag))
    for mark,(start,load) in enumerate(zip(starts,loads)):
        if load==1:continue
        ci,zi=(ch,zh) if mark<k else (cl,zl)
        tt=[L.lin((1,S[j]),(-1,S[start])) for j in range(start+1,start+load)]
        ww=[L.lin((1,U[j]),(-1,U[start]),(-ci,tt[j-start-1])) for j in range(start+1,start+load)]
        offset=len(coords);coords.extend(tt+ww)
        norms=[F(q+D),zi]
        action=[[(q+D)**2*(1+ci*ci),ci*(q+D)*zi],[ci*(q+D)*zi,zi*zi]]
        blocks.append((offset,load-1,norms,action,'internal_'+str(mark)))
    changed=len(coords)
    mask=2*q-1;pairs=[(a,mask^a) for a in range(1,mask) if a<(mask^a)]
    plus=[L.lin((1,L.unit(size,a-1)),(1,L.unit(size,b-1))) for a,b in pairs]
    highs=[L.lin((1,v),(-1,plus[0])) for v in plus[1:]]
    minus=[L.lin((1,L.unit(size,a-1)),(-1,L.unit(size,b-1))) for a,b in pairs]
    constraints=[[L.dot(h,L.image(c,v)) for v in minus] for h in H]
    lows=[L.lin(*[(co,v) for co,v in zip(row,minus)]) for row in L.kernel(constraints)]
    L.need(len(highs)==q-2 and len(lows)==q-k-r-1,'both complete untouched multiplicities')
    coords+=highs+lows
    L.need(len(coords)==N-k-2,'complete physical frame dimension census')
    images=[L.image(c,v) for v in coords]
    metric=[[L.dot(v,img) for img in images] for v in coords]
    L.need(L.psd(metric)==len(coords),'ALL physical frame directions independent')
    expected=[[F() for _ in coords] for _ in coords]
    norms=[q-1,D,D*(F(q,k)-1),D*(F(q,r)-1),(q+D)*(F(1,t)-F(1,D))/r,F(u,a*m*m)*(u*zh+a*zl)]
    for i,x in enumerate(norms):expected[i][i]=x
    expected[2][3]=expected[3][2]=-D
    for offset,dim,norms,action,tag in blocks:
        for v,x in enumerate(norms):
            for i in range(dim):
                for j in range(dim):expected[offset+v*dim+i][offset+v*dim+j]=x*(1+int(i==j))
    for start,rows,eigen in [(changed,highs,2*q),(changed+len(highs),lows,2*D)]:
        for i,x in enumerate(rows):
            for j,y in enumerate(rows):expected[start+i][start+j]=eigen*L.dot(x[:oldn],y[:oldn])
    L.need(metric==expected,'ALL whole-frame Gram entries and cross-sector zeros')
    full=[[L.dot(x,y)+sum(x)*sum(y) for y in images] for x in images]
    predicted=[[F() for _ in coords] for _ in coords]
    updates=[LH,ell,K,L.lin((1,mean_contrast),(1,Ws))]
    updateimages=[L.image(c,v) for v in updates]
    products=[[L.dot(v,img) for img in updateimages] for v in coords[:6]]
    weights=[F(a),F(u),F(1,m+1),F(a*m,u)]
    for i in range(6):
        for j in range(6):predicted[i][j]=L.dot(images[i][:oldn],images[j][:oldn])+sum(weights[z]*products[i][z]*products[j][z] for z in range(4))
    for offset,dim,norms,action,tag in blocks:
        for v in range(len(norms)):
            for w in range(len(norms)):
                for i in range(dim):
                    for j in range(dim):predicted[offset+v*dim+i][offset+w*dim+j]=action[v][w]*(1+int(i==j))
    for start,rows,eigen in [(changed,highs,2*q),(changed+len(highs),lows,2*D)]:
        for i in range(len(rows)):
            for j in range(len(rows)):predicted[start+i][start+j]=eigen*metric[start+i][start+j]
    L.need(full==predicted,'ALL full physical frame entries INCLUDING actual empty and cross-sector zeros')
    L.need(any(sum(row) for row in images),'actual empty contribution nonzero')
    omitted=[[L.dot(x,y) for y in images] for x in images]
    L.need(omitted!=predicted,'omitted empty vector detected')
    for start,rows,eigen in [(changed,highs,2*q),(changed+len(highs),lows,2*D)]:
        for j in range(len(rows)):
            cv=images[start+j]
            L.need(L.image(c,L.lin((1,cv),(sum(cv),[F(1)]*size)))==L.lin((eigen,cv)),'actual full untouched action')
    return {'frame_dimension':len(coords),'changed_dimension':changed,'untouched_high':len(highs),'untouched_low':len(lows),
            'whole_metric_entries':len(coords)**2,'whole_full_frame_entries':len(coords)**2,
            'whole_metric_sha256':L.fingerprint(metric),'whole_full_frame_sha256':L.fingerprint(full),
            'sectors':[(tag,dim*len(norms)) for offset,dim,norms,action,tag in blocks]}


def one(args):
    n,k,r,D,t,marks=args;d=L.build(*args);frame=audit(d)
    permutation_generators=0
    # Adjacent generators act on actual old marks AND entire fresh groups.
    # Verify every original-index entry, without a representation assumption.
    family=d['canonical'];index={v:i for i,v in enumerate(family)}
    loads=[D]*k+[t]*r;starts=[];offset=0
    for load in loads:starts.append(offset);offset+=load
    for begin,end in [(0,k),(k,k+r)]:
        for left in range(begin,end-1):
            right=left+1;bits={marks[left]:marks[right],marks[right]:marks[left]}
            for j in range(loads[left]):
                x=n+starts[left]+j;y=n+starts[right]+j;bits[x]=y;bits[y]=x
            perm=[]
            for A in family:
                moved=sum(1<<bits.get(b,b) for b in range(n+d['m']) if A&(1<<b))
                perm.append(index[moved])
            for tag in ('seed','raw'):
                full=L.lift(d[tag])
                L.need(all(full[perm[i]][perm[j]]==full[i][j] for i in range(d['N']) for j in range(d['N'])),
                       'ALL actual original-index '+tag+' adjacent type permutation entries')
            permutation_generators+=1
    N,s,family=d['N'],d['s'],d['canonical'];seed,raw=L.lift(d['seed']),L.lift(d['raw'])
    seedresult=L.validate(family,seed,s,N-k-1,F(1))
    rawresult=L.validate(family,raw,s,N-k,None)
    trace=sum(raw[i][i] for i in range(N));L.need(trace==d['raw_trace'],'whole raw trace with actual empty')
    loss=trace-N+1;eps=F(1,2*(trace+1));epsnew=F(1,2*loss)
    beta=1-eps*loss;L.need(beta==F(1,2)+F(N,2*(trace+1)) and 0<eps<epsnew<1,'quantified full-rank repair weights')
    mixtures=[]
    for e,margin in [(eps,beta),(epsnew,F(1,2))]:
        Q=[[(1-e)*seed[i][j]+e*raw[i][j] for j in range(N)] for i in range(N)]
        result=L.validate(family,Q,s,N-k,margin)
        lower=[[x+1 for x in row] for row in Q]
        stars=[[F(bool(A&(1<<p)))-F(s,N) for A in family] for p in marks[:k]]
        L.need(all(sum(bool(A&(1<<p)) for A in family)==s for p in marks[:k]),'all maximum heavy star sizes')
        L.need(all(L.image(lower,z)==[0]*N for z in stars),'ALL heavy kernel vectors')
        L.need(L.psd([[L.dot(x,y) for y in stars] for x in stars])==k,'all centered stars independent')
        mixtures.append(result)
    return {'n':n,'k':k,'r':r,'D':D,'t':t,'marks':marks,'N':N,'s':s,'frame':frame,'seed':seedresult,'raw':rawresult,
            'actual_type_permutation_generators':permutation_generators,
            'mixed':mixtures[0],'improved_mixed':mixtures[1],'epsilon':str(eps),'epsilon_improved':str(epsnew),'Traw':str(trace)}


def run():
    L.CHECKS=0
    cases=[(3,2,1,2,1,[2,0,1]),(4,2,2,3,1,[3,1,0,2]),(3,2,1,5,2,[1,2,0]),(5,3,2,3,2,[4,2,0,3,1])]
    records=[one(args) for args in cases]
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer','records':records,'exact_checks':L.CHECKS,
            'whole_frame_entries':sum(z['frame']['whole_full_frame_entries'] for z in records),'literal_instances':len(records),
            'scope':'complete finite original-domain frame controls; unbounded range requires written decomposition plus uniform signs'}
