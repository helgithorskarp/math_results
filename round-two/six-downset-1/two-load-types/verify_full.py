"""Literal physical-frame validation for k heavy and r light marks.

Finite validation; uniform coverage uses PROOF.md and verify_signs.py.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,importlib.util,json,resource,signal,time
HELPER=Path(__file__).resolve().parent.parent/'one-heavy-many-lights'/'verify_full.py'
spec=importlib.util.spec_from_file_location('one_heavy_full',HELPER)
previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)
base,two=previous.base,previous.two
vecadd,scale,dot,unit,nullspace=previous.vecadd,previous.scale,previous.dot,previous.unit,previous.nullspace
def alarm(signum,frame):raise TimeoutError('literal stage60s guard reached')
signal.signal(signal.SIGALRM,alarm)

def sectors(q,k,r,D,t):
    base.require(type(k) is int and k>=1 and type(r) is int and r>=1,'positive multiplicities')
    base.require(type(q) is int and q>k+r and type(D) is int and type(t) is int and D>t>=1,'physical parameter domain')
    a=k*D;u=r*t;m=a+u;N=2*q+2*m;w=F(q+D-1);h=F(N-1)
    ch=F(m*(w-D-m-1),m+1)/((m-1)*w-1+D)
    cl=F(m*(w-t-m-1),m+1)/((m-1)*w-1+t)
    B=w+m*(q+D)-a*D-u*t-2*m
    csquare=ch*ch*a*q+cl*cl*u*(q+D-t)
    kc=ch*a*(q-1)+cl*u*(w-t)
    def eta(ci,di):
        return w-B/(m+1)**2-ci*ci*w+2*ci*ci*(q+D-di)/m-csquare/m**2+2*ci*(w-di)/(m+1)-2*kc/(m*(m+1))
    eh,el=eta(ch,D),eta(cl,t);totaleta=a*eh+u*el
    zh=F(m,m-2)*(eh-totaleta/(m*(m-1)))
    zl=F(m,m-2)*(el-totaleta/(m*(m-1)))
    alpha=F(u,a*m*m)*(u*zh+a*zl)
    metric=[[F(0)]*6 for _ in range(6)]
    delta=(h-q-1)*(h-D)-D*(q-1)
    metric[0][0]=F(q-1)*(h-D)/delta
    metric[0][1]=metric[1][0]=F(D*(q-1))/delta
    metric[1][1]=F(D)*(h-q-1)/delta
    metric[2][2]=F(D)*(F(q,k)-1)/(h-2*D)
    metric[2][3]=metric[3][2]=-F(D)/(h-2*D)
    metric[3][3]=F(D)*(F(q,r)-1)/(h-2*D)
    metric[4][4]=F(q+D)*(F(1,t)-F(1,D))/(r*h)
    metric[5][5]=alpha/h
    vectors=[[F(0),F(1,D),F(1,D),F(0),F(0),F(0)],
             [F(0),F(1,D),F(0),F(1,D),F(1),F(0)],
             [F(1),F(m,D)-1,F(a,D),F(u,D),F(u),F(0)],
             [F(0),F(u,m*D)*(ch-cl),F(u,m*D)*ch,-F(u,m*D)*cl,-F(u,m)*cl,F(1)]]
    inverse_weights=[F(1,a),F(1,u),F(m+1),F(u,a*m)]
    budget=[[inverse_weights[i]*int(i==j)-sum(vectors[i][b]*metric[b][c]*vectors[j][c] for b in range(6) for c in range(6)) for j in range(4)] for i in range(4)]
    within_h=1-ch*ch*(q+D)/(h-q-D)-zh/h
    within_l=1-cl*cl*(q+D)/(h-q-D)-zl/h
    heavy_a=F(q)/(h-2*D)
    light_a=F(t)*(F(q,D)/(h-2*D)+F(q+D)*(F(1,t)-F(1,D))/h)
    det_h=(1-heavy_a)*(1-zh/h)-heavy_a*ch*ch
    det_l=(1-light_a)*(1-zl/h)-light_a*cl*cl
    base.require(min(eh,el,zh,zl,within_h,within_l,1-heavy_a,1-light_a,det_h,det_l)>0,'sample scalar positivity')
    base.require(max(heavy_a,light_a)<F(q+D)/h<F(1,2),'strict standard half margins')
    base.require(base.psd_rank(budget)==4,'sample invariant Schur budget')
    # Literal 24-permutation determinant versus the proposed cofactor reduction.
    from itertools import permutations
    def det(A):
        z=F(0)
        for p in permutations(range(len(A))):
            sign=(-1)**sum(p[i]>p[j] for i in range(len(A)) for j in range(i+1,len(A)))
            v=F(sign)
            for i,j in enumerate(p):v*=A[i][j]
            z+=v
        return z
    A=budget;d3=det([row[:3] for row in A[:3]])
    C00=A[1][1]*A[2][2]-A[1][2]*A[2][1]
    C11=A[0][0]*A[2][2]-A[0][2]*A[2][0]
    C01=A[0][2]*A[1][2]-A[0][1]*A[2][2]
    reduced=(F(u,a*m)-alpha/h)*d3+F(u*u,m*m)*ch*ch*(d3/a-C00/(a*a))+cl*cl/F(m*m)*(u*d3-C11)+F(2*u,a*m*m)*ch*cl*C01
    base.require(det(budget)==reduced,'literal determinant/cofactor identity')
    return {'q':q,'k':k,'r':r,'D':D,'t':t,'m':m,'N':N,'ch':ch,'cl':cl,'normK':B,'eta_heavy':eh,'eta_light':el,'zeta_heavy':zh,'zeta_light':zl,'alpha':alpha,'heavy_standard_a':heavy_a,'light_standard_a':light_a,'heavy_within_slack':within_h,'light_within_slack':within_l,'heavy_standard_determinant':det_h,'light_standard_determinant':det_l},budget

def build(n,loads):
    base.require(type(n) is int and 3<=n<=6 and 3<=len(loads)<=n,'literal marks/cube guard')
    base.require(all(type(t) is int and t>=1 for t in loads),'positive integer loads')
    base.require(len(set(loads))==2 and loads==sorted(loads,reverse=True),'two decreasing load types')
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

def check(n,k,r,D,t):
    start=time.monotonic();signal.alarm(60)
    loads=[D]*k+[t]*r
    family,s,c,raw,Traw,params=build(n,loads)
    q=params['q'];N=len(family);coreN=N-1;oldN=2*q-1;a=k*D;u=r*t;m=a+u
    scalars,budget=sectors(q,k,r,D,t)
    ch,cl=scalars['ch'],scalars['cl'];zh,zl=scalars['zeta_heavy'],scalars['zeta_light']
    base.require(min(scalars['eta_heavy'],scalars['eta_light'])==F(params['minimum_eta']),'literal/scalar eta')
    base.require(min(zh,zl)==F(params['minimum_zeta']),'literal/scalar zeta')
    oldsum=[F(i<oldN) for i in range(coreN)]
    h0=scale(F(-1,2),vecadd(oldsum,unit(coreN,oldN-1)));gp=vecadd(oldsum,h0)
    hi=[[-F(i<oldN and bool(family[i+1]&(1<<mark))) for i in range(coreN)] for mark in range(k+r)]
    ai=[vecadd(v,scale(-1,h0)) for v in hi]
    spokes=[unit(coreN,oldN+2*j+1) for j in range(m)];leaves=[unit(coreN,oldN+2*j) for j in range(m)]
    heavysp=[scale(F(1,D),vecadd(*spokes[i*D:(i+1)*D])) for i in range(k)]
    lights=[scale(F(1,t),vecadd(*spokes[a+i*t:a+(i+1)*t])) for i in range(r)]
    for i in range(k):base.require(two.matvec(c,heavysp[i])==scale(F(1,D),two.matvec(c,hi[i])),'actual saturated heavy spoke mean')
    zs=[vecadd(v,scale(F(-1,D),hi[k+i])) for i,v in enumerate(lights)]
    lh=scale(F(1,k),vecadd(*heavysp));light=scale(F(1,r),vecadd(*lights))
    ah=scale(F(1,k),vecadd(*ai[:k]));al=scale(F(1,r),vecadd(*ai[k:]));zbar=scale(F(1,r),vecadd(*zs))
    K=vecadd(oldsum,*spokes);y=scale(F(u,m),vecadd(scale(ch,lh),scale(-cl,light)))
    ws=vecadd(scale(F(1,a),vecadd(*leaves[:a])),scale(F(1,m+1),K),scale(-1,y))
    wh=[vecadd(scale(F(1,D),vecadd(*leaves[i*D:(i+1)*D])),scale(-ch,heavysp[i])) for i in range(k)]
    wl=[vecadd(scale(F(1,t),vecadd(*leaves[a+i*t:a+(i+1)*t])),scale(-cl,lights[i])) for i in range(r)]
    sh=[[vecadd(hi[i],scale(-1,hi[k-1])),vecadd(wh[i],scale(-1,wh[-1]))] for i in range(k-1)]
    sl=[[vecadd(hi[k+i],scale(-1,hi[-1])),vecadd(zs[i],scale(-1,zs[-1])),vecadd(wl[i],scale(-1,wl[-1]))] for i in range(r-1)]
    coords=[gp,h0,ah,al,zbar,ws]+[v for block in sh+sl for v in block];groups=[]
    for start0,size,coefficient,variance in [(i*D,D,ch,zh) for i in range(k)]+[(a+i*t,t,cl,zl) for i in range(r)]:
        ts=[vecadd(spokes[j],scale(-1,spokes[start0+size-1])) for j in range(start0,start0+size-1)]
        ww=[vecadd(leaves[j],scale(-1,leaves[start0+size-1]),scale(-coefficient,ts[j-start0])) for j in range(start0,start0+size-1)]
        offset=len(coords);coords+=ts+ww;groups.append((offset,size-1,coefficient,variance))
    generators=len(coords);images=[two.matvec(c,v) for v in coords]
    gram=[[dot(coords[i],images[j]) for j in range(generators)] for i in range(generators)]
    expected=[[F(0)]*generators for _ in range(generators)]
    expected[0][0]=q-1;expected[1][1]=D
    expected[2][2]=D*(F(q,k)-1);expected[2][3]=expected[3][2]=-D;expected[3][3]=D*(F(q,r)-1)
    expected[4][4]=F(q+D)*(F(1,t)-F(1,D))/r;expected[5][5]=scalars['alpha']
    standards=[(6,k-1,[F(q*D),zh/D],D,[F(1,D),F(0)],[ch/D,F(1)]),
               (6+2*(k-1),r-1,[F(q*D),F(q+D)*(F(1,t)-F(1,D)),zl/t],t,[F(1,D),F(1),F(0)],[cl/D,cl,F(1)])]
    for offset,count,norms,size,sv,fv in standards:
        dim=len(norms)
        for i in range(count):
            for j in range(count):
                for b in range(dim):expected[offset+dim*i+b][offset+dim*j+b]=(1+int(i==j))*norms[b]
    for offset,dim,coefficient,variance in groups:
        for i in range(dim):
            for j in range(dim):
                b=1+int(i==j)
                expected[offset+i][offset+j]=(q+D)*b;expected[offset+dim+i][offset+dim+j]=variance*b
    base.require(gram==expected,'every full invariant/standard/internal Gram entry')
    base.require(base.psd_rank(gram)==generators,'independent complete changed-sector generators')
    empty=[-sum(v) for v in images]
    base.require(all(empty[i]==0 for i in range(6,generators)),'actual empty vector is invariant')
    frame=[[dot(images[i],images[j])+empty[i]*empty[j] for j in range(generators)] for i in range(generators)]
    target=[[F(0)]*generators for _ in range(generators)]
    target[0][0]=(q+1)*(q-1);target[0][1]=target[1][0]=D*(q-1);target[1][1]=D*D
    for i in [2,3]:
        for j in [2,3]:target[i][j]=2*D*expected[i][j]
    for weight,v in zip([F(a),F(u),F(1,m+1),F(a*m,u)],[lh,light,K,vecadd(y,ws)]):
        products=[dot(images[i],v) for i in range(6)]
        for i in range(6):
            for j in range(6):target[i][j]+=weight*products[i]*products[j]
    for offset,count,norms,size,sv,fv in standards:
        dim=len(norms)
        for i in range(count):
            for j in range(count):
                b=1+int(i==j)
                for z in range(dim):
                    for d in range(dim):
                        val=2*D*norms[0]*int(z==d==0)+size*norms[z]*norms[d]*(sv[z]*sv[d]+fv[z]*fv[d])
                        target[offset+dim*i+z][offset+dim*j+d]=b*val
    for offset,dim,coefficient,variance in groups:
        for i in range(dim):
            for j in range(dim):
                b=1+int(i==j)
                target[offset+i][offset+j]=(q+D)**2*(1+coefficient**2)*b
                target[offset+i][offset+dim+j]=target[offset+dim+j][offset+i]=coefficient*(q+D)*variance*b
                target[offset+dim+i][offset+dim+j]=variance**2*b
    base.require(frame==target,'every full frame action including all cross sectors and actual empty')
    full=oldN;pairs=[(x,full^x) for x in range(1,full) if x<(full^x)]
    highs=[vecadd(unit(coreN,x-1),unit(coreN,z-1),scale(-1,unit(coreN,pairs[0][0]-1)),scale(-1,unit(coreN,pairs[0][1]-1))) for x,z in pairs[1:]]
    constraints=[[-F(bool(x&(1<<mark)))+F(bool(z&(1<<mark))) for x,z in pairs] for mark in range(k+r)]
    lows=[]
    for weights in nullspace(constraints,len(pairs)):
        v=[F(0)]*coreN
        for weight,(x,z) in zip(weights,pairs):v[x-1]+=weight;v[z-1]-=weight
        lows.append(v)
    for label,rows,eigenvalue,count in [('high',highs,2*q,q-2),('low',lows,2*D,q-k-r-1)]:
        base.require(len(rows)==count,'complete untouched '+label+' count')
        for v in rows:
            base.require(two.matvec(c,v)==scale(eigenvalue,v),'literal untouched '+label+' eigen-action')
            base.require(all(dot(image,v)==0 for image in images),'all changed/untouched '+label+' products zero')
    base.require(generators+len(highs)+len(lows)==N-k-2,'complete full-frame dimension exhaustion')
    # The k actual stars and their centered indicators, without using a dimension guess.
    starcore=[];centered=[]
    for mark in range(k):
        v=[F(bool(x&(1<<mark))) for x in family[1:]]
        base.require(sum(v)==s,'actual heavy-star size')
        base.require(not any(two.matvec(c,v)) and not any(two.matvec(raw,v)),'actual star kernel in both cores')
        starcore.append(v);centered.append([F(bool(x&(1<<mark)))-F(s,N) for x in family])
    base.require(base.psd_rank([[dot(v,w) for w in centered] for v in centered])==k,'independent k centered star kernels')
    matrix=base.lift(c,s);index={x:i for i,x in enumerate(family)}
    swaps=[]
    for mark in range(k-1):swaps.append((mark,mark+1,mark*D,(mark+1)*D,D,'Sk'))
    for mark in range(r-1):swaps.append((k+mark,k+mark+1,a+mark*t,a+(mark+1)*t,t,'Sr'))
    for b,d,p0,p1,size,label in swaps:
        def swap_mask(x):
            for b0,d0 in [(b,d)]+[(n+p0+j,n+p1+j) for j in range(size)]:
                if bool(x&(1<<b0))!=bool(x&(1<<d0)):x^=(1<<b0)|(1<<d0)
            return x
        permutation=[index[swap_mask(x)] for x in family]
        base.require(all(matrix[i][j]==matrix[permutation[i]][permutation[j]] for i in range(N) for j in range(N)),'actual original-index '+label+' generator invariance')
    literal=base.check(family,matrix,s)
    base.require(literal['lower_rank']==N-k-1 and literal['upper_rank']==N-1,'literal seed endpoint ranks')
    gap=[[(N-s)*(int(i==j)-matrix[i][j])-(int(i==j)-F(1,N)) for j in range(N)] for i in range(N)]
    base.require(base.psd_rank(gap)==N-1,'original-index unit seed gap')
    base.require(any(empty),'nonzero actual empty contribution')
    base.require(base.psd_rank(raw)==N-k-1,'raw core has exactly forced k star kernels')
    epsilon=F(1,2)/(1+Traw)
    mixed=[[(1-epsilon)*c[i][j]+epsilon*raw[i][j] for j in range(N-1)] for i in range(N-1)]
    mixed_matrix=base.lift(mixed,s);mixed_checks=base.check(family,mixed_matrix,s)
    base.require(mixed_checks['lower_rank']==N-k and mixed_checks['upper_rank']==N-1,'mixed greatest endpoint ranks')
    for v in centered:
        base.require(two.matvec(mixed_matrix,v)==scale(F(-s,N-s),v),'actual centered maximum-star endpoint action')
    half_gap=[[(N-s)*(int(i==j)-mixed_matrix[i][j])-F(1,2)*(int(i==j)-F(1,N)) for j in range(N)] for i in range(N)]
    base.require(base.psd_rank(half_gap)==N-1,'actual full mixed half-unit gap')
    bad=[row[:] for row in c];bad[oldN][oldN+1]+=1;bad[oldN+1][oldN]+=1
    try:base.check(family,base.lift(bad,s),s)
    except ValueError:pass
    else:raise ValueError('changed intersecting core entry accepted')
    bad=[row[:] for row in mixed_matrix];bad[0][0]+=1
    try:base.check(family,bad,s)
    except ValueError:pass
    else:raise ValueError('changed empty loop accepted')
    signal.alarm(0)
    return {'n':n,'k':k,'r':r,'q':q,'loads':loads,'N':N,'symmetric_dimension':6,'heavy_standard_dimension':2*(k-1),'light_standard_dimension':3*(r-1),'internal_dimension':2*k*(D-1)+2*r*(t-1),'untouched_high':len(highs),'untouched_low':len(lows),'full_frame_dimension':N-k-2,'all_frame_action_scalars':generators**2,'Sk_generators':k-1,'Sr_generators':r-1,'independent_centered_heavy_star_kernels':k,'all_cross_sectors_and_actual_empty_matched':True,'seed':literal,'raw_core_rank':N-k-1,'mixed':mixed_checks,'seed_unit_gap':True,'mixed_half_unit_gap':True,'seed_empty_energy':params['seed_empty_energy'],'intersecting_entry_corruption_rejected':True,'empty_loop_corruption_rejected':True,'elapsed_seconds':time.monotonic()-start}

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',type=Path);p.add_argument('--expected',type=Path);p.add_argument('--case',nargs=5,type=int)
    args=p.parse_args();start=time.monotonic()
    cases=[tuple(args.case)] if args.case else [(3,2,1,3,2),(4,2,2,3,1),(4,3,1,2,1),(5,3,2,4,3),(5,4,1,2,1),(6,2,3,2,1)]
    rows=[]
    for case in cases:
        row=check(*case);rows.append(row);print(json.dumps({'completed_case':case,'elapsed_seconds':row['elapsed_seconds']},sort_keys=True),flush=True)
        if args.write:args.write.write_text(json.dumps({'agent':'six-downset-1','role':'researcher','status':'partial finite validation','fixtures':rows},indent=2)+'\n')
    out={'agent':'six-downset-1','role':'researcher','status':'finite exact validation;uniform coverage is ordinary proof plus exact signs','fixtures':rows,'elapsed_seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.write:args.write.write_text(json.dumps(out,indent=2)+'\n')
    if args.expected:
        expected=json.loads(args.expected.read_text())['full']
        for result in [out,expected]:
            result.pop('elapsed_seconds',None);result.pop('peak_RSS_KiB',None)
            for row in result['fixtures']:row.pop('elapsed_seconds',None)
        base.require(out==expected,'frozen full-frame results mismatch')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
