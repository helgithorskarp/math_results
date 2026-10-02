"""Original-index finite validation of the uniform arbitrary-pendant proof.

The literal Gram constructor below is credited to published9229/9153;
only its type-count scope guard is extended. All numerical resource guards
are unchanged. Analytic uniform coverage is an ordinary proof, not these
finite checks. No floating point or solver is a proof input.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,importlib.util,json,resource,signal,time
import exact as base
import exact as two
from exact import vecadd,scale,dot,unit,nullspace,zero,mm,transpose,require
from verify_bounds import parameters

def alarm(signum,frame):raise TimeoutError('arbitrary-pendant literal60s guard')
signal.signal(signal.SIGALRM,alarm)
def build(n,loads):
    base.require(type(n) is int and 3<=n<=6 and 3<=len(loads)<=n,'literal marks/cube guard')
    base.require(all(type(t) is int and t>=1 for t in loads),'positive integer loads')
    base.require(len(set(loads))>=3 and loads==sorted(loads,reverse=True),'at least three decreasing load types')
    q=1<<(n-1);D=max(loads);M=sum(loads);N=2*q+2*M;s=q+D;w=F(s-1);k=loads.count(D)
    base.require(M>=3 and N<=80,'residual and literal guards')
    oldN=2*q-1;full=oldN;old=list(range(1,2*q));marks=[i for i,t in enumerate(loads) for _ in range(t)]
    c0=[[F((q+D)*int(a==b)+(q-D)*int(a^b==full)-1) for b in old] for a in old]
    hs=[[F(-bool(a&(1<<mark))) for a in old] for mark in range(len(loads))]
    oldco=[[F(i==j) for j in range(oldN)] for i in range(oldN)]+[[x/D for x in hs[mark]] for mark in marks]
    ti=[[F(q+D)*(int(u==v)-F(1,D)) if marks[u]==marks[v] else F(0) for v in range(M)] for u in range(M)]
    residual=[[F(0)]*(oldN+M) for _ in range(oldN+M)]
    for u in range(M):
        for v in range(M):residual[oldN+u][oldN+v]=ti[u][v]
    b=two.gram(c0,oldco,residual)
    cs=[F(M*(w-loads[mark]-M-1),M+1)/((M-1)*w-1+loads[mark]) for mark in marks]
    csum=[F(0)]*oldN+cs
    leafco=[[-F(1,M+1)+cs[u]*int(j==oldN+u)-csum[j]/M for j in range(oldN+M)] for u in range(M)]
    lg=two.gram(b,leafco,[[F(0)]*M for _ in range(M)]);eta=[w-lg[u][u] for u in range(M)]
    totaleta=sum(eta);zeta=[F(M,M-2)*(x-totaleta/(M*(M-1))) for x in eta]
    W=[[zeta[u]*int(u==v)-(zeta[u]+zeta[v])/M+sum(zeta)/(M*M) for v in range(M)] for u in range(M)]
    base.require(all(sum(row)==0 for row in W),'row-zero general residual')
    base.require([W[u][u] for u in range(M)]==eta,'exact general residual diagonals')
    base.require(base.psd_rank(W)==M-1,'positive full residual simplex')
    family=list(range(2*q));coeff=[[F(i==j) for j in range(oldN+M)] for i in range(oldN)]
    for u in range(M):
        fresh=1<<(n+u);family.extend([fresh,fresh|(1<<marks[u])]);coeff.extend([leafco[u],[F(j==oldN+u) for j in range(oldN+M)]])
    residual=[[F(0)]*(N-1) for _ in range(N-1)]
    for u in range(M):
        for v in range(M):residual[oldN+2*u][oldN+2*v]=W[u][v]
    seed=two.gram(b,coeff,residual)
    A2=sum(t*t for t in loads);B=w+M*(q+D)-A2-2*M
    base.require(sum(map(sum,seed))==B/(M+1)**2,'general centered empty energy')
    rawcoeff=[[F(i==j) for j in range(oldN+M)] for i in range(oldN)]
    rawres=[[F(0)]*(N-1) for _ in range(N-1)]
    for u in range(M):
        rawcoeff.extend([[-F(j==oldN+u)/w for j in range(oldN+M)],[F(j==oldN+u) for j in range(oldN+M)]])
        rawres[oldN+2*u][oldN+2*u]=w-1/w
    raw=two.gram(b,rawcoeff,rawres)
    raw_B=w+(1-1/w)**2*(M*(q+D)-A2)-2*M*(1-1/w)+M*(w-1/w)
    base.require(sum(map(sum,raw))==raw_B,'actual raw empty energy')
    Traw=(N-1)*w+raw_B
    return family,s,seed,raw,Traw,{'n':n,'q':q,'loads':loads,'N':N,'s':s,'k':k,'minimum_eta':str(min(eta)),'minimum_zeta':str(min(zeta)),'minimum_c':str(min(cs)),'maximum_c':str(max(cs)),'seed_empty_energy':str(B/(M+1)**2)}

def inverse(A):
    n=len(A);B=[r[:]+[F(i==j) for j in range(n)] for i,r in enumerate(A)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if B[i][j]),None)
        require(pivot is not None,'physical inverse nonsingular')
        B[j],B[pivot]=B[pivot],B[j];p=B[j][j]
        B[j]=[x/p for x in B[j]]
        for i in range(n):
            if i!=j:
                f=B[i][j];B[i]=[x-f*y for x,y in zip(B[i],B[j])]
    require(all(B[i][j]==int(i==j) for i in range(n) for j in range(n)),'physical inverse identity')
    return [row[n:] for row in B]

def check(n,loads):
    started=time.monotonic();signal.alarm(60)
    family,s,c,raw,Traw,params=build(n,loads)
    q=params['q'];N=len(family);coreN=N-1;oldN=2*q-1
    D=max(loads);m=sum(loads);R=len(loads);k=loads.count(D)
    model=parameters(q,loads);ci,zeta=model['ci'],model['zeta'];h=model['h']
    require(min(model['eta'])==F(params['minimum_eta']) and min(zeta)==F(params['minimum_zeta']),'physical/scalar variances')
    oldsum=[F(i<oldN) for i in range(coreN)]
    h0=scale(F(-1,2),vecadd(oldsum,unit(coreN,oldN-1)));gp=vecadd(oldsum,h0)
    hi=[[-F(i<oldN and bool(family[i+1]&(1<<mark))) for i in range(coreN)] for mark in range(R)]
    ai=[vecadd(x,scale(-1,h0)) for x in hi]
    spokes=[unit(coreN,oldN+2*j+1) for j in range(m)];leaves=[unit(coreN,oldN+2*j) for j in range(m)]
    offsets=[];offset=0
    for d in loads:offsets.append(offset);offset+=d
    L=[scale(F(1,d),vecadd(*spokes[o:o+d])) for o,d in zip(offsets,loads)]
    nonheavy=[i for i,d in enumerate(loads) if d<D]
    for i,d in enumerate(loads):
        if d==D:require(two.matvec(c,L[i])==scale(F(1,D),two.matvec(c,hi[i])),'every saturated heavy spoke mean')
    Z=[vecadd(L[i],scale(F(-1,D),hi[i])) for i in nonheavy]
    K=vecadd(oldsum,*spokes);Csum=vecadd(*(scale(d*a,l) for d,a,l in zip(loads,ci,L)))
    oldcontrasts=[vecadd(scale(a,l),scale(F(-1,m),Csum)) for a,l in zip(ci,L)]
    W=[vecadd(scale(F(1,d),vecadd(*leaves[o:o+d])),scale(F(1,m+1),K),scale(-1,y)) for o,d,y in zip(offsets,loads,oldcontrasts)]
    require(not any(two.matvec(c,vecadd(*(scale(d,w) for d,w in zip(loads,W))))),'weighted W relation')
    sigma=[vecadd(y,w) for y,w in zip(oldcontrasts,W)]
    require(not any(two.matvec(c,vecadd(*(scale(d,y) for d,y in zip(loads,sigma))))),'weighted singleton relation')
    before=[gp,h0,*ai,*Z];a0=len(before)
    require(a0==2*R-k+2,'old/spoke mean dimension')
    im0=[two.matvec(c,x) for x in before]
    G0=[[dot(x,y) for y in im0] for x in before]
    F0=[[sum((x[t]*y[t] for t in range(oldN)),F(0)) for y in im0] for x in im0]
    baseframe=[row[:] for row in F0]
    for weight,update in zip([*map(F,loads),F(1,m+1)],L+[K]):
        projection=[dot(image,update) for image in im0]
        for i in range(a0):
            for j in range(a0):baseframe[i][j]+=weight*projection[i]*projection[j]
    basebudget=[[h*G0[i][j]-baseframe[i][j] for j in range(a0)] for i in range(a0)]
    require(base.psd_rank(basebudget)==a0,'literal positive old/spoke/common budget')
    inv=inverse(basebudget);projections=[[dot(image,l) for image in im0] for l in L]
    gamma_physical=mm(mm(projections,inv),transpose(projections))
    require(gamma_physical==model['Gamma'],'every physical updated marked-mean resolvent entry')
    # The common update has its own independently reconstructed Schur slack.
    before_K=[row[:] for row in F0]
    for d,l in zip(loads,L):
        projection=[dot(image,l) for image in im0]
        for i in range(a0):
            for j in range(a0):before_K[i][j]+=d*projection[i]*projection[j]
    invK=inverse([[h*G0[i][j]-before_K[i][j] for j in range(a0)] for i in range(a0)])
    kp=[dot(image,K) for image in im0]
    require(F(m+1)-dot(kp,[dot(row,kp) for row in invK])==model['Kgap'],'physical K Schur slack')
    coords=before+W[:-1];mean=len(coords);groups=[]
    require(mean==3*R-k+1,'all individual-mark mean dimension')
    for o,d,a,z in zip(offsets,loads,ci,zeta):
        ts=[vecadd(spokes[j],scale(-1,spokes[o+d-1])) for j in range(o,o+d-1)]
        ww=[vecadd(leaves[j],scale(-1,leaves[o+d-1]),scale(-a,ts[j-o])) for j in range(o,o+d-1)]
        groups.append((len(coords),d-1,a,z));coords+=ts+ww
    changed=len(coords);images=[two.matvec(c,x) for x in coords]
    gram=[[dot(x,y) for y in images] for x in coords]
    expected=zero(changed)
    expected[0][0]=q-1;expected[1][1]=D
    for i in range(R):
        for j in range(R):expected[2+i][2+j]=D*(q*int(i==j)-1)
    for j,mark in enumerate(nonheavy):expected[2+R+j][2+R+j]=F(q+D)*(F(1,loads[mark])-F(1,D))
    for i in range(R-1):
        for j in range(R-1):expected[a0+i][a0+j]=F(zeta[i],loads[i])*int(i==j)-(zeta[i]+zeta[j])/m+sum(d*z for d,z in zip(loads,zeta))/m**2
    for o,d,a,z in groups:
        for i in range(d):
            for j in range(d):
                expected[o+i][o+j]=(q+D)*(1+int(i==j));expected[o+d+i][o+d+j]=z*(1+int(i==j))
    require(gram==expected and base.psd_rank(gram)==changed,'every changed-sector Gram entry and independence')
    empty=[-sum(x) for x in images]
    require(all(empty[i]==0 for i in range(mean,changed)) and any(empty[:mean]),'actual empty only in means and nonzero')
    frame=[[dot(x,y)+empty[i]*empty[j] for j,y in enumerate(images)] for i,x in enumerate(images)]
    target=zero(changed)
    for i in range(mean):
        for j in range(mean):target[i][j]=sum((images[i][t]*images[j][t] for t in range(oldN)),F(0))
    for weight,update in zip([*map(F,loads),F(1,m+1),*map(F,loads)],L+[K]+sigma):
        products=[dot(image,update) for image in images[:mean]]
        for i in range(mean):
            for j in range(mean):target[i][j]+=weight*products[i]*products[j]
    for o,d,a,z in groups:
        for i in range(d):
            for j in range(d):
                b=1+int(i==j);target[o+i][o+j]=(q+D)**2*(1+a*a)*b
                target[o+i][o+d+j]=target[o+d+j][o+i]=a*(q+D)*z*b
                target[o+d+i][o+d+j]=z*z*b
    require(frame==target,'every mean/internal/cross frame entry including actual empty')
    require(any(frame[i][j]!=dot(images[i],images[j]) for i in range(mean) for j in range(mean)),'omitting actual empty changes frame')
    require(base.psd_rank([[h*gram[i][j]-frame[i][j] for j in range(changed)] for i in range(changed)])==changed,'whole changed-sector cap')
    full=oldN;pairs=[(x,full^x) for x in range(1,full) if x<(full^x)]
    highs=[vecadd(unit(coreN,x-1),unit(coreN,z-1),scale(-1,unit(coreN,pairs[0][0]-1)),scale(-1,unit(coreN,pairs[0][1]-1))) for x,z in pairs[1:]]
    constraints=[[-F(bool(x&(1<<mark)))+F(bool(z&(1<<mark))) for x,z in pairs] for mark in range(R)]
    lows=[]
    for weights in nullspace(constraints,len(pairs)):
        x=[F(0)]*coreN
        for weight,(a,b) in zip(weights,pairs):x[a-1]+=weight;x[b-1]-=weight
        lows.append(x)
    for label,rows,eigenvalue,count in [('high',highs,2*q,q-2),('low',lows,2*D,q-R-1)]:
        require(len(rows)==count,'complete untouched '+label+' count')
        for x in rows:
            require(two.matvec(c,x)==scale(eigenvalue,x),'physical untouched '+label+' action')
            require(all(dot(image,x)==0 for image in images),'every changed/untouched '+label+' cross product')
    require(changed+len(highs)+len(lows)==N-k-2,'complete full seed frame census')
    centered=[]
    for mark in range(k):
        star=[F(bool(x&(1<<mark))) for x in family[1:]]
        require(sum(star)==s and not any(two.matvec(c,star)) and not any(two.matvec(raw,star)),'each heavy-star size and both kernels')
        centered.append([F(bool(x&(1<<mark)))-F(s,N) for x in family])
    matrix=base.lift(c,s);literal=base.check(family,matrix,s)
    require(literal['lower_rank']==N-k-1 and literal['upper_rank']==N-1,'seed endpoint ranks')
    gap=[[(N-s)*(int(i==j)-matrix[i][j])-(int(i==j)-F(1,N)) for j in range(N)] for i in range(N)]
    require(base.psd_rank(gap)==N-1 and base.psd_rank(raw)==N-k-1,'seed unit gap and raw rank')
    epsilon=F(1,2)/(1+Traw)
    mixed=[[(1-epsilon)*c[i][j]+epsilon*raw[i][j] for j in range(N-1)] for i in range(N-1)]
    mixedM=base.lift(mixed,s);mixed_check=base.check(family,mixedM,s)
    require(mixed_check['lower_rank']==N-k and mixed_check['upper_rank']==N-1,'repaired greatest endpoint ranks')
    for star in centered:require(two.matvec(mixedM,star)==scale(F(-s,N-s),star),'each centered heavy-star endpoint action')
    half=[[(N-s)*(int(i==j)-mixedM[i][j])-F(1,2)*(int(i==j)-F(1,N)) for j in range(N)] for i in range(N)]
    require(base.psd_rank(half)==N-1,'full repaired half-unit gap')
    bad=[row[:] for row in c];bad[oldN][oldN+1]+=1;bad[oldN+1][oldN]+=1
    try:base.check(family,base.lift(bad,s),s)
    except ValueError:pass
    else:raise ValueError('intersecting-entry damage accepted')
    bad=[row[:] for row in mixedM];bad[0][0]+=1
    try:base.check(family,bad,s)
    except ValueError:pass
    else:raise ValueError('empty-loop damage accepted')
    signal.alarm(0)
    return {'n':n,'loads':loads,'q':q,'N':N,'s':s,'heavy_count':k,'distinct_load_values':len(set(loads)),'old_spoke_mean_dimension':a0,'mean_dimension':mean,'internal_dimension':2*(m-R),'changed_dimension':changed,'untouched_high':len(highs),'untouched_low':len(lows),'seed_frame_dimension':N-k-2,'every_Gram_and_frame_entry':changed**2,'all_cross_sectors_checked':True,'actual_empty_checked':True,'physical_Gamma_entries':R**2,'physical_Kgap':str(model['Kgap']),'seed':literal,'raw_core_rank':N-k-1,'mixed':mixed_check,'seed_unit_gap':True,'mixed_half_unit_gap':True,'balanced_budget_margin':'1/6','damage_checks':2,'elapsed_seconds':time.monotonic()-started}

def stable(obj):
    if isinstance(obj,dict):return {k:stable(v) for k,v in obj.items() if k not in ['elapsed_seconds','peak_RSS_KiB']}
    if isinstance(obj,list):return [stable(v) for v in obj]
    return obj
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--case',nargs='+',type=int);parser.add_argument('--write',type=Path);parser.add_argument('--expected',type=Path);args=parser.parse_args();start=time.monotonic()
    cases=[(args.case[0],args.case[1:])] if args.case else [(4,[3,2,1,1]),(4,[3,2,2,1]),(4,[3,3,2,1]),(4,[4,3,2,1]),(4,[10,3,2,1]),(5,[4,3,2,1,1]),(5,[3,3,2,1,1]),(5,[3,3,3,2,1]),(5,[8,6,4,3,1]),(6,[3,2,1,1])]
    rows=[]
    for n,loads in cases:
        row=check(n,loads);rows.append(row);print(json.dumps({'n':n,'loads':loads,'seconds':row['elapsed_seconds']}),flush=True)
        if args.write:args.write.write_text(json.dumps({'agent':'six-downset-1','role':'researcher','status':'partial original-frame validation','fixtures':rows},indent=2)+'\n')
    result={'agent':'six-downset-1','role':'researcher','status':'finite exact original-frame validation; uniform coverage requires the ordinary analytic proof','fixtures':rows,'baseline_constructor':'9229 and9153 published original Gram','per_fixture_seconds_guard':60,'literal_n_guard':6,'literal_N_guard':80,'elapsed_seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.expected:require(stable(result)==stable(json.loads(args.expected.read_text())['full']),'complete frozen original-frame record')
    if args.write:args.write.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
