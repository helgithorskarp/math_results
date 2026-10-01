"""Literal full-frame and greatest-rank H validation for loads(D,t,t).

Finite regression checks; uniform positivity is the symbolic source and proof.
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

def sectors(q,D,t):
    base.require(type(q) is int and q>=4 and type(D) is int and type(t) is int and D>t>=1,'three-mark parameter domain')
    m=D+2*t;N=2*q+2*m;w=F(q+D-1);h=F(N-1)
    ch=F(m*(w-D-m-1),m+1)/((m-1)*w-1+D)
    cl=F(m*(w-t-m-1),m+1)/((m-1)*w-1+t)
    normK=w+m*(q+D)-D*D-2*t*t-2*m
    ky=F(2*t,m)*(ch*(q-1)-cl*(w-t))
    y2=F(4*t*t,m*m)*(ch*ch*F(q,D)+cl*cl*F(q+D-t,2*t))
    sm2=F(q+D-t,2*t)
    eh=w-normK/(m+1)**2-y2-ch*ch*(q+D)*(1-F(1,D))+2*ky/(m+1)
    el=w-normK/(m+1)**2-F(D*D,4*t*t)*y2-cl*cl*sm2-cl*cl*(q+D)*(1-F(1,t))-F(D,t)*ky/(m+1)
    totaleta=D*eh+2*t*el
    zh=F(m,m-2)*(eh-totaleta/(m*(m-1)))
    zl=F(m,m-2)*(el-totaleta/(m*(m-1)))
    alpha=F(2*t,D*m*m)*(2*t*zh+D*zl)
    metric=[[F(0)]*6 for _ in range(6)]
    det=(h-q-1)*(h-D)-D*(q-1)
    metric[0][0]=F(q-1)*(h-D)/det
    metric[0][1]=metric[1][0]=F(D*(q-1))/det
    metric[1][1]=F(D)*(h-q-1)/det
    metric[2][2]=F(D*(q-1))/(h-2*D)
    metric[2][3]=metric[3][2]=-F(D)/(h-2*D)
    metric[3][3]=F(D)*(F(q,2)-1)/(h-2*D)
    metric[4][4]=F(q+D)*(F(1,t)-F(1,D))/(2*h)
    metric[5][5]=alpha/h
    vectors=[[F(0),F(1),F(1),F(0),F(0),F(0)],
             [F(0),F(1,D),F(0),F(1,D),F(1),F(0)],
             [F(1),F(2*t,D),F(1),F(2*t,D),F(2*t),F(0)],
             [F(0),F(2*t,m*D)*(ch-cl),F(2*t,m*D)*ch,-F(2*t,m*D)*cl,-F(2*t,m)*cl,F(1)]]
    weights=[F(D),F(1,2*t),F(m+1),F(2*t,D*m)]
    budget=[[weights[i]*int(i==j)-sum(vectors[i][a]*metric[a][b]*vectors[j][b] for a in range(6) for b in range(6)) for j in range(4)] for i in range(4)]
    beta=F(q,2*D)/(h-2*D)+F(q+D)*(F(1,t)-F(1,D))/(2*h)
    anti1=1-2*t*beta
    anti2=anti1*(1-zl/h)-2*t*cl*cl*beta
    within_h=1-ch*ch*(q+D)/(h-q-D)-zh/h
    within_l=1-cl*cl*(q+D)/(h-q-D)-zl/h
    base.require(min(eh,el,zh,zl,within_h,within_l,anti1,anti2)>0,'sample scalar positivity')
    base.require(2*t*beta<F(1,2),'sample antisymmetric first half margin')
    base.require(base.psd_rank(budget)==4,'sample symmetric Schur budget')
    scalars={'q':q,'D':D,'t':t,'m':m,'N':N,'ch':ch,'cl':cl,'normK':normK,'ky':ky,'y2':y2,'sm2':sm2,'eta_heavy':eh,'eta_light':el,'zeta_heavy':zh,'zeta_light':zl,'alpha':alpha,'beta':beta,'heavy_within_slack':within_h,'light_within_slack':within_l,'antisymmetric_first':anti1,'antisymmetric_determinant':anti2}
    return scalars,budget


def build(n,loads):
    base.require(type(n) is int and 3<=n<=6 and len(loads)==3,'literal marks/cube guard')
    base.require(all(type(t) is int and t>=1 for t in loads),'positive integer loads')
    base.require(loads[0]>loads[1] and loads[1]==loads[2],'one heavy and two equal light loads')
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


def check(n,D,t):
    start=time.monotonic();signal.alarm(60)
    family,s,c,raw,Traw,params=build(n,[D,t,t]);q=params['q'];N=len(family);coreN=N-1;oldN=2*q-1;m=D+2*t
    scalars,budget=sectors(q,D,t)
    ch,cl=scalars['ch'],scalars['cl'];zh,zl=scalars['zeta_heavy'],scalars['zeta_light']
    base.require(min(scalars['eta_heavy'],scalars['eta_light'])==F(params['minimum_eta']),'literal/scalar eta including light difference')
    base.require(min(zh,zl)==F(params['minimum_zeta']),'literal/scalar zeta')
    oldsum=[F(i<oldN) for i in range(coreN)]
    h0=scale(F(-1,2),vecadd(oldsum,unit(coreN,oldN-1)));gp=vecadd(oldsum,h0)
    hi=[[-F(i<oldN and bool(family[i+1]&(1<<mark))) for i in range(coreN)] for mark in range(3)]
    ai=[vecadd(v,scale(-1,h0)) for v in hi]
    spokes=[unit(coreN,oldN+2*u+1) for u in range(m)];leaves=[unit(coreN,oldN+2*u) for u in range(m)]
    lights=[scale(F(1,t),vecadd(*spokes[a:a+t])) for a in [D,D+t]]
    zs=[vecadd(v,scale(F(-1,D),hi[i+1])) for i,v in enumerate(lights)]
    light=scale(F(1,2),vecadd(*lights));zbar=scale(F(1,2),vecadd(*zs));abar=scale(F(1,2),vecadd(ai[1],ai[2]))
    k=vecadd(oldsum,*spokes);y=scale(F(2*t,m),vecadd(scale(ch/D,hi[0]),scale(-cl,light)))
    ws=vecadd(scale(F(1,D),vecadd(*leaves[:D])),scale(F(1,m+1),k),scale(-1,y))
    hm=scale(F(1,2),vecadd(hi[1],scale(-1,hi[2])))
    zm=scale(F(1,2),vecadd(zs[0],scale(-1,zs[1])))
    sm=scale(F(1,2),vecadd(lights[0],scale(-1,lights[1])))
    wm=vecadd(scale(F(1,2*t),vecadd(*leaves[D:D+t],*map(lambda v:scale(-1,v),leaves[D+t:]))),scale(-cl,sm))
    coords=[gp,h0,ai[0],abar,zbar,ws,hm,zm,wm];groups=[]
    for a,size,coefficient,variance in [(0,D,ch,zh),(D,t,cl,zl),(D+t,t,cl,zl)]:
        ts=[vecadd(spokes[u],scale(-1,spokes[a+size-1])) for u in range(a,a+size-1)]
        ww=[vecadd(leaves[u],scale(-1,leaves[a+size-1]),scale(-coefficient,ts[u-a])) for u in range(a,a+size-1)]
        offset=len(coords);coords+=ts+ww;groups.append((offset,size-1,coefficient,variance))
    generators=len(coords);images=[two.matvec(c,v) for v in coords]
    gram=[[dot(coords[i],images[j]) for j in range(generators)] for i in range(generators)]
    expected=[[F(0)]*generators for _ in range(generators)]
    expected[0][0]=q-1;expected[1][1]=D;expected[2][2]=D*(q-1)
    expected[2][3]=expected[3][2]=-D;expected[3][3]=D*(F(q,2)-1)
    expected[4][4]=F(q+D)*(F(1,t)-F(1,D))/2;expected[5][5]=scalars['alpha']
    expected[6][6]=F(q*D,2);expected[7][7]=expected[4][4];expected[8][8]=zl/(2*t)
    for offset,dim,coefficient,variance in groups:
        for i in range(dim):
            for j in range(dim):
                b=1+int(i==j)
                expected[offset+i][offset+j]=(q+D)*b
                expected[offset+dim+i][offset+dim+j]=variance*b
    base.require(gram==expected,'all literal symmetric/anti/internal Gram entries')
    base.require(base.psd_rank(gram)==generators,'independent complete changed-sector generators')
    empty=[-sum(v) for v in images]
    base.require(all(empty[i]==0 for i in range(6,generators)),'actual empty vector is symmetric')
    frame=[[dot(images[i],images[j])+empty[i]*empty[j] for j in range(generators)] for i in range(generators)]
    target=[[F(0)]*generators for _ in range(generators)]
    target[0][0]=(q+1)*(q-1);target[0][1]=target[1][0]=D*(q-1);target[1][1]=D*D
    for i in [2,3]:
        for j in [2,3]:target[i][j]=2*D*expected[i][j]
    for weight,v in zip([F(1,D),F(2*t),F(1,m+1),F(D*m,2*t)],[hi[0],light,k,vecadd(y,ws)]):
        products=[dot(images[i],v) for i in range(6)]
        for i in range(6):
            for j in range(6):target[i][j]+=weight*products[i]*products[j]
    target[6][6]=2*D*expected[6][6]
    for v in [sm,vecadd(scale(cl,sm),wm)]:
        products=[dot(images[i],v) for i in range(6,9)]
        for i in range(3):
            for j in range(3):target[6+i][6+j]+=2*t*products[i]*products[j]
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
    constraints=[[-F(bool(a&(1<<mark)))+F(bool(b&(1<<mark))) for a,b in pairs] for mark in range(3)]
    lows=[]
    for weights in nullspace(constraints,len(pairs)):
        v=[F(0)]*coreN
        for weight,(a,b) in zip(weights,pairs):v[a-1]+=weight;v[b-1]-=weight
        lows.append(v)
    for label,rows,eigenvalue,count in [('high',highs,2*q,q-2),('low',lows,2*D,q-4)]:
        base.require(len(rows)==count,'complete untouched '+label+' count')
        for v in rows:
            base.require(two.matvec(c,v)==scale(eigenvalue,v),'literal untouched '+label+' eigen-action')
            base.require(all(dot(image,v)==0 for image in images),'all changed/untouched '+label+' products zero')
    base.require(generators+len(highs)+len(lows)==N-3,'complete full-frame dimension exhaustion')
    # The involution swaps old marks1/2 and the two light fresh groups.
    def swap_mask(a):
        pairsbits=[(1,2)]+[(n+D+j,n+D+t+j) for j in range(t)]
        for b,d in pairsbits:
            if bool(a&(1<<b))!=bool(a&(1<<d)): a^=(1<<b)|(1<<d)
        return a
    index={a:i for i,a in enumerate(family)};permutation=[index[swap_mask(a)] for a in family]
    matrix=base.lift(c,s)
    base.require(all(matrix[i][j]==matrix[permutation[i]][permutation[j]] for i in range(N) for j in range(N)),'actual full original-index S2 invariance')
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
    return {'n':n,'q':q,'loads':[D,t,t],'N':N,'changed_symmetric_dimension':6,'changed_antisymmetric_dimension':3,'changed_internal_dimension':2*(D-1)+4*(t-1),'untouched_high':len(highs),'untouched_low':len(lows),'full_frame_dimension':N-3,'all_frame_action_scalars':generators**2,'actual_empty_and_all_cross_sectors_matched':True,'actual_full_S2_invariance':True,'seed':literal,'raw_core_rank':N-2,'seed_empty_energy':params['seed_empty_energy'],'raw_empty_energy':str(sum(map(sum,raw))),'raw_full_trace':str(Traw),'epsilon':str(epsilon),'mixed':mixed_checks,'seed_unit_gap':True,'mixed_half_unit_gap':True,'intersecting_entry_corruption_rejected':True,'empty_loop_corruption_rejected':True}

def stable(record):return {k:v for k,v in record.items() if k not in ['elapsed_seconds','peak_RSS_KiB']}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',type=Path);parser.add_argument('--expected',type=Path)
    args=parser.parse_args();start=time.monotonic();records=[]
    for n,D,t in [(3,3,2),(3,8,7),(4,3,2),(4,8,1),(6,2,1)]:
        signal.alarm(60);records.append(check(n,D,t));signal.alarm(0)
    out={'agent':'six-downset-1','role':'researcher','status':'finite original-index checks; uniform coverage is PROOF.md plus verify_signs.py','records':records,'elapsed_seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.expected:base.require(stable(out)==stable(json.loads(args.expected.read_text())['full']),'frozen full-frame/matrix certificate mismatch')
    if args.write:args.write.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
