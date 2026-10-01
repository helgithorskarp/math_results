"""Literal full frame validation for loads(D,t,...,t).

Finite regression checks; uniform coverage is PROOF.md plus verify_signs.py.
Credits the exact definition and Gram helpers accompanying9005.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,importlib.util,json,resource,signal,time
HELPER=Path(__file__).resolve().parent.parent/'two-unequal-loads'/'verify_full.py'
spec=importlib.util.spec_from_file_location('two_load_full_helpers',HELPER)
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
base,two=helper.base,helper.two
vecadd,scale,dot,unit,nullspace=helper.vecadd,helper.scale,helper.dot,helper.unit,helper.nullspace
def alarm(signum,frame):raise TimeoutError('literal stage60s guard reached')
signal.signal(signal.SIGALRM,alarm)

def sectors(q,r,D,t):
    base.require(type(r) is int and r>=2 and type(q) is int and q>=r+2,'mark-count/cube parameter domain')
    base.require(type(D) is int and type(t) is int and D>t>=1,'unequal-load parameter domain')
    u=r*t;m=D+u;N=2*q+2*m;w=F(q+D-1);h=F(N-1)
    ch=F(m*(w-D-m-1),m+1)/((m-1)*w-1+D)
    cl=F(m*(w-t-m-1),m+1)/((m-1)*w-1+t)
    B=w+m*(q+D)-D*D-u*t-2*m
    b=F(u,m)*(ch*(q-1)-cl*(w-t))
    v=F(u*u,m*m)*(ch*ch*F(q,D)+cl*cl*F(q+D-t,u))
    eh=w-B/(m+1)**2-v-ch*ch*(q+D)*(1-F(1,D))+2*b/(m+1)
    el=w-B/(m+1)**2-F(D*D,u*u)*v-cl*cl*F((r-1)*(q+D-t),u)-cl*cl*(q+D)*(1-F(1,t))-F(2*D,u)*b/(m+1)
    simple_el=w-B/(m+1)**2-ch*ch*F(q*D,m*m)-cl*cl*w+cl*cl*F((q+D-t)*(2*D+u),m*m)-F(2*D,m*(m+1))*(ch*(q-1)-cl*(w-t))
    base.require(el==simple_el,'total-light-load simplification')
    totaleta=D*eh+u*el
    zh=F(m,m-2)*(eh-totaleta/(m*(m-1)))
    zl=F(m,m-2)*(el-totaleta/(m*(m-1)))
    alpha=F(u,D*m*m)*(u*zh+D*zl)
    metric=[[F(0)]*6 for _ in range(6)]
    delta=(h-q-1)*(h-D)-D*(q-1)
    metric[0][0]=F(q-1)*(h-D)/delta
    metric[0][1]=metric[1][0]=F(D*(q-1))/delta
    metric[1][1]=F(D)*(h-q-1)/delta
    metric[2][2]=F(D*(q-1))/(h-2*D)
    metric[2][3]=metric[3][2]=-F(D)/(h-2*D)
    metric[3][3]=F(D)*(F(q,r)-1)/(h-2*D)
    metric[4][4]=F(q+D)*(F(1,t)-F(1,D))/(r*h)
    metric[5][5]=alpha/h
    vectors=[[F(0),F(1),F(1),F(0),F(0),F(0)],
             [F(0),F(1,D),F(0),F(1,D),F(1),F(0)],
             [F(1),F(u,D),F(1),F(u,D),F(u),F(0)],
             [F(0),F(u,m*D)*(ch-cl),F(u,m*D)*ch,-F(u,m*D)*cl,-F(u,m)*cl,F(1)]]
    weights=[F(D),F(1,u),F(m+1),F(u,D*m)]
    budget=[[weights[i]*int(i==j)-sum(vectors[i][a]*metric[a][b]*vectors[j][b] for a in range(6) for b in range(6)) for j in range(4)] for i in range(4)]
    beta=F(q,D)/(h-2*D)+F(q+D)*(F(1,t)-F(1,D))/h
    a=t*beta
    within_h=1-ch*ch*(q+D)/(h-q-D)-zh/h
    within_l=1-cl*cl*(q+D)/(h-q-D)-zl/h
    standard_det=(1-a)*(1-zl/h)-a*cl*cl
    base.require(min(eh,el,zh,zl,within_h,within_l,1-a,standard_det)>0,'sample scalar positivity')
    base.require(a<F(q+D)/h<F(1,2),'strict standard half margin')
    base.require(base.psd_rank(budget)==4,'sample symmetric Schur budget')
    return {'q':q,'r':r,'D':D,'t':t,'m':m,'N':N,'ch':ch,'cl':cl,'normK':B,'eta_heavy':eh,'eta_light':el,'zeta_heavy':zh,'zeta_light':zl,'alpha':alpha,'standard_a':a,'heavy_within_slack':within_h,'light_within_slack':within_l,'standard_determinant':standard_det},budget


def build(n,loads):
    base.require(type(n) is int and 3<=n<=6 and 3<=len(loads)<=n,'literal marks/cube guard')
    base.require(all(type(t) is int and t>=1 for t in loads),'positive integer loads')
    base.require(loads[0]>loads[1] and all(v==loads[1] for v in loads[1:]),'one heavy and r equal light loads')
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


def check(n,r,D,t):
    start=time.monotonic();signal.alarm(60)
    loads=[D]+[t]*r
    family,s,c,raw,Traw,params=build(n,loads)
    q=params['q'];N=len(family);coreN=N-1;oldN=2*q-1;m=D+r*t
    scalars,budget=sectors(q,r,D,t)
    ch,cl=scalars['ch'],scalars['cl'];zh,zl=scalars['zeta_heavy'],scalars['zeta_light']
    base.require(min(scalars['eta_heavy'],scalars['eta_light'])==F(params['minimum_eta']),'literal/scalar eta including light differences')
    base.require(min(zh,zl)==F(params['minimum_zeta']),'literal/scalar zeta')
    oldsum=[F(i<oldN) for i in range(coreN)]
    h0=scale(F(-1,2),vecadd(oldsum,unit(coreN,oldN-1)));gp=vecadd(oldsum,h0)
    hi=[[-F(i<oldN and bool(family[i+1]&(1<<mark))) for i in range(coreN)] for mark in range(r+1)]
    ai=[vecadd(v,scale(-1,h0)) for v in hi]
    spokes=[unit(coreN,oldN+2*u+1) for u in range(m)];leaves=[unit(coreN,oldN+2*u) for u in range(m)]
    lights=[scale(F(1,t),vecadd(*spokes[D+i*t:D+(i+1)*t])) for i in range(r)]
    zs=[vecadd(v,scale(F(-1,D),hi[i+1])) for i,v in enumerate(lights)]
    light=scale(F(1,r),vecadd(*lights));zbar=scale(F(1,r),vecadd(*zs));abar=scale(F(1,r),vecadd(*ai[1:]))
    k=vecadd(oldsum,*spokes);y=scale(F(r*t,m),vecadd(scale(ch/D,hi[0]),scale(-cl,light)))
    ws=vecadd(scale(F(1,D),vecadd(*leaves[:D])),scale(F(1,m+1),k),scale(-1,y))
    wmeans=[vecadd(scale(F(1,t),vecadd(*leaves[D+i*t:D+(i+1)*t])),scale(-cl,lights[i])) for i in range(r)]
    std=[]
    for i in range(r-1):
        std.append([vecadd(hi[i+1],scale(-1,hi[r])),vecadd(zs[i],scale(-1,zs[-1])),vecadd(wmeans[i],scale(-1,wmeans[-1]))])
    coords=[gp,h0,ai[0],abar,zbar,ws]+[v for block in std for v in block];groups=[]
    for a,size,coefficient,variance in [(0,D,ch,zh)]+[(D+i*t,t,cl,zl) for i in range(r)]:
        ts=[vecadd(spokes[u],scale(-1,spokes[a+size-1])) for u in range(a,a+size-1)]
        ww=[vecadd(leaves[u],scale(-1,leaves[a+size-1]),scale(-coefficient,ts[u-a])) for u in range(a,a+size-1)]
        offset=len(coords);coords+=ts+ww;groups.append((offset,size-1,coefficient,variance))
    generators=len(coords);images=[two.matvec(c,v) for v in coords]
    gram=[[dot(coords[i],images[j]) for j in range(generators)] for i in range(generators)]
    expected=[[F(0)]*generators for _ in range(generators)]
    expected[0][0]=q-1;expected[1][1]=D;expected[2][2]=D*(q-1)
    expected[2][3]=expected[3][2]=-D;expected[3][3]=D*(F(q,r)-1)
    expected[4][4]=F(q+D)*(F(1,t)-F(1,D))/r;expected[5][5]=scalars['alpha']
    norms=[F(q*D),F(q+D)*(F(1,t)-F(1,D)),zl/t]
    for i in range(r-1):
        for j in range(r-1):
            for a in range(3):expected[6+3*i+a][6+3*j+a]=(1+int(i==j))*norms[a]
    for offset,dim,coefficient,variance in groups:
        for i in range(dim):
            for j in range(dim):
                b=1+int(i==j)
                expected[offset+i][offset+j]=(q+D)*b
                expected[offset+dim+i][offset+dim+j]=variance*b
    base.require(gram==expected,'every literal symmetric/standard/internal Gram entry')
    base.require(base.psd_rank(gram)==generators,'independent complete changed-sector generators')
    empty=[-sum(v) for v in images]
    base.require(all(empty[i]==0 for i in range(6,generators)),'actual empty vector is symmetric')
    frame=[[dot(images[i],images[j])+empty[i]*empty[j] for j in range(generators)] for i in range(generators)]
    target=[[F(0)]*generators for _ in range(generators)]
    target[0][0]=(q+1)*(q-1);target[0][1]=target[1][0]=D*(q-1);target[1][1]=D*D
    for i in [2,3]:
        for j in [2,3]:target[i][j]=2*D*expected[i][j]
    for weight,v in zip([F(1,D),F(r*t),F(1,m+1),F(D*m,r*t)],[hi[0],light,k,vecadd(y,ws)]):
        products=[dot(images[i],v) for i in range(6)]
        for i in range(6):
            for j in range(6):target[i][j]+=weight*products[i]*products[j]
    sv=[F(1,D),F(1),F(0)];fv=[cl/D,cl,F(1)]
    for i in range(r-1):
        for j in range(r-1):
            b=1+int(i==j)
            for a in range(3):
                for d in range(3):
                    val=2*D*norms[0]*int(a==d==0)+t*norms[a]*norms[d]*(sv[a]*sv[d]+fv[a]*fv[d])
                    target[6+3*i+a][6+3*j+d]=b*val
    for offset,dim,coefficient,variance in groups:
        for i in range(dim):
            for j in range(dim):
                b=1+int(i==j)
                target[offset+i][offset+j]=(q+D)**2*(1+coefficient**2)*b
                target[offset+i][offset+dim+j]=target[offset+dim+j][offset+i]=coefficient*(q+D)*variance*b
                target[offset+dim+i][offset+dim+j]=variance**2*b
    base.require(frame==target,'every full frame action including all cross sectors and actual empty')
    full=oldN;pairs=[(a,full^a) for a in range(1,full) if a<(full^a)]
    highs=[vecadd(unit(coreN,a-1),unit(coreN,b-1),scale(-1,unit(coreN,pairs[0][0]-1)),scale(-1,unit(coreN,pairs[0][1]-1))) for a,b in pairs[1:]]
    constraints=[[-F(bool(a&(1<<mark)))+F(bool(b&(1<<mark))) for a,b in pairs] for mark in range(r+1)]
    lows=[]
    for weights in nullspace(constraints,len(pairs)):
        v=[F(0)]*coreN
        for weight,(a,b) in zip(weights,pairs):v[a-1]+=weight;v[b-1]-=weight
        lows.append(v)
    for label,rows,eigenvalue,count in [('high',highs,2*q,q-2),('low',lows,2*D,q-r-2)]:
        base.require(len(rows)==count,'complete untouched '+label+' count')
        for v in rows:
            base.require(two.matvec(c,v)==scale(eigenvalue,v),'literal untouched '+label+' eigen-action')
            base.require(all(dot(image,v)==0 for image in images),'all changed/untouched '+label+' products zero')
    base.require(generators+len(highs)+len(lows)==N-3,'complete full-frame dimension exhaustion')
    matrix=base.lift(c,s);index={a:i for i,a in enumerate(family)}
    for mark in range(1,r):
        def swap_mask(a):
            pairsbits=[(mark,mark+1)]+[(n+D+(mark-1)*t+j,n+D+mark*t+j) for j in range(t)]
            for b,d in pairsbits:
                if bool(a&(1<<b))!=bool(a&(1<<d)):a^=(1<<b)|(1<<d)
            return a
        permutation=[index[swap_mask(a)] for a in family]
        base.require(all(matrix[i][j]==matrix[permutation[i]][permutation[j]] for i in range(N) for j in range(N)),'actual original-index Sr generator invariance')
    literal=base.check(family,matrix,s)
    base.require(literal['lower_rank']==N-2 and literal['upper_rank']==N-1,'literal seed endpoint ranks')
    gap=[[(N-s)*(int(i==j)-matrix[i][j])-(int(i==j)-F(1,N)) for j in range(N)] for i in range(N)]
    base.require(base.psd_rank(gap)==N-1,'original-index unit seed gap')
    base.require(any(empty),'nonzero actual empty contribution')
    base.require(base.psd_rank(raw)==N-2,'raw core has only forced heavy-star kernel')
    epsilon=F(1,2)/(1+Traw)
    mixed=[[(1-epsilon)*c[i][j]+epsilon*raw[i][j] for j in range(N-1)] for i in range(N-1)]
    mixed_matrix=base.lift(mixed,s);mixed_checks=base.check(family,mixed_matrix,s)
    base.require(mixed_checks['lower_rank']==N-1 and mixed_checks['upper_rank']==N-1,'mixed greatest endpoint ranks')
    half_gap=[[(N-s)*(int(i==j)-mixed_matrix[i][j])-F(1,2)*(int(i==j)-F(1,N)) for j in range(N)] for i in range(N)]
    base.require(base.psd_rank(half_gap)==N-1,'actual full mixed half-unit gap')
    bad=[row[:] for row in c];bad[oldN][oldN+1]+=1;bad[oldN+1][oldN]+=1
    try:base.check(family,base.lift(bad,s),s)
    except ValueError:pass
    else:raise ValueError('changed intersecting core entry was accepted')
    bad=[row[:] for row in mixed_matrix];bad[0][0]+=1
    try:base.check(family,bad,s)
    except ValueError:pass
    else:raise ValueError('changed empty loop was accepted')
    signal.alarm(0)
    return {'n':n,'r':r,'q':q,'loads':loads,'N':N,'symmetric_dimension':6,'standard_dimension':3*(r-1),'internal_dimension':2*(D-1)+2*r*(t-1),'untouched_high':len(highs),'untouched_low':len(lows),'full_frame_dimension':N-3,'all_frame_action_scalars':generators**2,'Sr_generators':r-1,'all_cross_sectors_and_actual_empty_matched':True,'seed':literal,'raw_core_rank':N-2,'mixed':mixed_checks,'seed_unit_gap':True,'mixed_half_unit_gap':True,'seed_empty_energy':params['seed_empty_energy'],'intersecting_entry_corruption_rejected':True,'empty_loop_corruption_rejected':True,'elapsed_seconds':time.monotonic()-start}


def stable(d):
    if isinstance(d,dict):return {k:stable(v) for k,v in d.items() if k not in ['elapsed_seconds','peak_RSS_KiB']}
    if isinstance(d,list):return [stable(v) for v in d]
    return d

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',type=Path);parser.add_argument('--expected',type=Path)
    args=parser.parse_args();start=time.monotonic();records=[]
    for n,r,D,t in [(3,2,3,2),(4,3,3,2),(5,4,4,1),(4,3,8,7),(6,5,2,1)]:
        records.append(check(n,r,D,t))
    out={'agent':'six-downset-1','role':'researcher','status':'finite full original-index checks;uniform scope follows PROOF.md and exact signs','records':records,'elapsed_seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.expected:base.require(stable(out)==stable(json.loads(args.expected.read_text())['full']),'frozen full-frame/matrix certificate mismatch')
    if args.write:args.write.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
