"""Literal full-frame, capped-rank, empty-loop and mixture replay.

Finite original-index regression checks. The uniform theorem uses the
ordinary argument in PROOF.md and the exact universal signs verifier.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,resource,signal,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import verify as base
import verify_two_marks as two

def alarm(signum,frame):raise TimeoutError('stage60s guard reached')
signal.signal(signal.SIGALRM,alarm)

def vecadd(*terms):return [sum(z) for z in zip(*terms)]
def scale(a,x):return [a*z for z in x]
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def unit(length,i):return [F(j==i) for j in range(length)]


def nullspace(rows,width):
    rows=[[F(x) for x in row] for row in rows];pivots=[];row=0
    for col in range(width):
        pivot=next((i for i in range(row,len(rows)) if rows[i][col]),None)
        if pivot is None:continue
        rows[row],rows[pivot]=rows[pivot],rows[row];v=rows[row][col]
        rows[row]=[x/v for x in rows[row]]
        for i in range(len(rows)):
            if i!=row:rows[i]=[x-rows[i][col]*y for x,y in zip(rows[i],rows[row])]
        pivots.append(col);row+=1
        if row==len(rows):break
    answer=[]
    for col in range(width):
        if col in pivots:continue
        v=unit(width,col)
        for i,p in enumerate(pivots):v[p]=-rows[i][col]
        answer.append(v)
    return answer


def sectors(q,D,t):
    base.require(type(q) is int and q>=2 and type(D) is int and type(t) is int and D>t>=1,'two-mark domain')
    M=D+t;N=2*q+2*M;w=F(q+D-1);h=F(N-1)
    ch=F(M*(w-D-M-1),M+1)/((M-1)*w-1+D)
    cl=F(M*(w-t-M-1),M+1)/((M-1)*w-1+t)
    B=w+M*(q+D)-D*D-t*t-2*M
    b=F(t,M)*(ch*(q-1)-cl*(w-t))
    y2=F(t*t,M*M)*(ch*ch*F(q,D)+cl*cl*F(q+D-t,t))
    eh=w-B/(M+1)**2-y2-ch*ch*(q+D)*(1-F(1,D))+2*b/(M+1)
    el=w-B/(M+1)**2-F(D*D,t*t)*y2-cl*cl*(q+D)*(1-F(1,t))-F(2*D,t)*b/(M+1)
    totaleta=D*eh+t*el
    zh=F(M,M-2)*(eh-totaleta/(M*(M-1)))
    zl=F(M,M-2)*(el-totaleta/(M*(M-1)))
    alpha=F(t,D*M*M)*(t*zh+D*zl)
    metric=[[F(0)]*6 for _ in range(6)]
    det=(h-q-1)*(h-D)-D*(q-1)
    metric[0][0]=F(q-1)*(h-D)/det
    metric[0][1]=metric[1][0]=F(D*(q-1))/det
    metric[1][1]=F(D)*(h-q-1)/det
    for i in [2,3]:
        for j in [2,3]:metric[i][j]=F(D)*(q*int(i==j)-1)/(h-2*D)
    metric[4][4]=F(q+D)*(F(1,t)-F(1,D))/h
    metric[5][5]=alpha/h
    vectors=[[F(0),F(1),F(1),F(0),F(0),F(0)],
             [F(0),F(1,D),F(0),F(1,D),F(1),F(0)],
             [F(1),F(t,D),F(1),F(t,D),F(t),F(0)],
             [F(0),F(t,M*D)*(ch-cl),F(t,M*D)*ch,-F(t,M*D)*cl,-F(t,M)*cl,F(1)]]
    inverse_weights=[F(D),F(1,t),F(M+1),F(t,D*M)]
    budget=[[inverse_weights[i]*int(i==j)-sum(vectors[i][a]*metric[a][b]*vectors[j][b] for a in range(6) for b in range(6)) for j in range(4)] for i in range(4)]
    within_h=1-ch*ch*(q+D)/(h-q-D)-zh/h
    within_l=1-cl*cl*(q+D)/(h-q-D)-zl/h
    base.require(eh>0 and el>0 and zh>0 and zl>0,'positive parameter residuals')
    base.require(base.psd_rank(budget)==4,'complete four-vector symmetric Schur cap')
    base.require(within_h>0 and (t==1 or within_l>0),'within-mark Schur caps')
    return {'q':q,'D':D,'t':t,'N':N,'ch':str(ch),'cl':str(cl),'eta_heavy':str(eh),'eta_light':str(el),'zeta_heavy':str(zh),'zeta_light':str(zl),'heavy_within_slack':str(within_h),'light_within_slack':str(within_l),'symmetric_budget_rank':4,'seed_frame_dimension':N-3},budget


def build(n,loads):
    base.require(type(n) is int and 2<=n<=6 and len(loads)==2,'literal marks/cube guard')
    base.require(all(type(t) is int and t>=1 for t in loads),'positive integer loads')
    base.require(loads[0]>loads[1],'strict unequal-load order')
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
    family,s,c,raw,Traw,params=build(n,[D,t]);q=params['q'];N=len(family);coreN=N-1;oldN=2*q-1;M=D+t
    scalar,budget=sectors(q,D,t);ch,cl=F(scalar['ch']),F(scalar['cl'])
    zh,zl=F(scalar['zeta_heavy']),F(scalar['zeta_light']);alpha=F(t,D*M*M)*(t*zh+D*zl)
    oldsum=[F(i<oldN) for i in range(coreN)]
    h0=scale(F(-1,2),vecadd(oldsum,unit(coreN,oldN-1)));gp=vecadd(oldsum,h0)
    hi=[[-F(i<oldN and bool(family[i+1]&(1<<mark))) for i in range(coreN)] for mark in range(2)]
    ai=[vecadd(v,scale(-1,h0)) for v in hi]
    spokes=[unit(coreN,oldN+2*u+1) for u in range(M)];leaves=[unit(coreN,oldN+2*u) for u in range(M)]
    light=scale(F(1,t),vecadd(*spokes[D:]));z=vecadd(light,scale(F(-1,D),hi[1]));k=vecadd(oldsum,*spokes)
    y=scale(F(t,M),vecadd(scale(ch/D,hi[0]),scale(-cl,light)))
    ws=vecadd(scale(F(1,D),vecadd(*leaves[:D])),scale(F(1,M+1),k),scale(-1,y))
    coords=[gp,h0,*ai,z,ws];groups=[]
    for start,size,coefficient,variance in [(0,D,ch,zh),(D,t,cl,zl)]:
        ts=[vecadd(spokes[u],scale(-1,spokes[start+size-1])) for u in range(start,start+size-1)]
        ww=[vecadd(leaves[u],scale(-1,leaves[start+size-1]),scale(-coefficient,ts[u-start])) for u in range(start,start+size-1)]
        offset=len(coords);coords+=ts+ww;groups.append((offset,size-1,coefficient,variance))
    m=len(coords);gram=two.gram(c,coords,[[F(0)]*m for _ in range(m)])
    expected=[[F(0)]*m for _ in range(m)]
    expected[0][0]=q-1;expected[1][1]=D
    for i in [2,3]:
        for j in [2,3]:expected[i][j]=D*(q*int(i==j)-1)
    expected[4][4]=F(q+D)*(F(1,t)-F(1,D));expected[5][5]=alpha
    for offset,dim,coefficient,variance in groups:
        for i in range(dim):
            for j in range(dim):
                b=1+int(i==j)
                expected[offset+i][offset+j]=(q+D)*b
                expected[offset+dim+i][offset+dim+j]=variance*b
    base.require(gram==expected,'literal full changed-sector Gram')
    changed=(6 if q>=4 else 5)+2*(D-1)+2*(t-1)
    base.require(base.psd_rank(gram)==changed,'literal changed-sector rank including boundary')
    images=[two.matvec(c,v) for v in coords];empty=[-sum(v) for v in images]
    frame=[[dot(images[i],images[j])+empty[i]*empty[j] for j in range(m)] for i in range(m)]
    target=[[F(0)]*m for _ in range(m)]
    target[0][0]=(q+1)*(q-1);target[0][1]=target[1][0]=D*(q-1);target[1][1]=D*D
    for i in [2,3]:
        for j in [2,3]:target[i][j]=2*D*expected[i][j]
    for weight,v in zip([F(1,D),F(t),F(1,M+1),F(D*M,t)],[hi[0],light,k,vecadd(y,ws)]):
        products=[dot(two.matvec(c,x),v) for x in coords[:6]]
        for i in range(6):
            for j in range(6):target[i][j]+=weight*products[i]*products[j]
    for offset,dim,coefficient,variance in groups:
        for i in range(dim):
            for j in range(dim):
                b=1+int(i==j)
                target[offset+i][offset+j]=(q+D)**2*(1+coefficient**2)*b
                target[offset+i][offset+dim+j]=target[offset+dim+j][offset+i]=coefficient*(q+D)*variance*b
                target[offset+dim+i][offset+dim+j]=variance**2*b
    base.require(any(empty),'nonzero actual empty frame contribution')
    base.require(frame==target,'every literal full frame action matches all mean/internal sectors,including empty')
    full=2*q-1;pairs=[(a,full^a) for a in range(1,full) if a<(full^a)]
    highs=[vecadd(unit(coreN,a-1),unit(coreN,b-1),scale(-1,unit(coreN,pairs[0][0]-1)),scale(-1,unit(coreN,pairs[0][1]-1))) for a,b in pairs[1:]]
    constraints=[[-F(bool(a&(1<<mark)))+F(bool(b&(1<<mark))) for a,b in pairs] for mark in range(2)]
    lows=[]
    for weights in nullspace(constraints,len(pairs)):
        v=[F(0)]*coreN
        for weight,(a,b) in zip(weights,pairs):v[a-1]+=weight;v[b-1]-=weight
        lows.append(v)
    for label,rows,eigenvalue,count in [('high',highs,2*q,q-2),('low',lows,2*D,q-3 if q>=4 else 0)]:
        base.require(len(rows)==count,'complete untouched '+label+' count')
        for v in rows:
            base.require(two.matvec(c,v)==scale(eigenvalue,v),'literal full untouched '+label+' eigen-action')
            base.require(all(dot(two.matvec(c,x),v)==0 for x in coords),'all changed/untouched '+label+' orthogonal')
    base.require(changed+len(highs)+len(lows)==N-3,'complete dimension exhaustion')
    matrix=base.lift(c,s);literal=base.check(family,matrix,s)
    base.require(literal['lower_rank']==N-2 and literal['upper_rank']==N-1,'full literal seed endpoint ranks')
    gap=[[(N-s)*(int(i==j)-matrix[i][j])-(int(i==j)-F(1,N)) for j in range(N)] for i in range(N)]
    base.require(base.psd_rank(gap)==N-1,'original-index unit seed gap')
    base.require(base.psd_rank(raw)==N-2,'raw core rank, including only forced heavy-star kernel')
    epsilon=F(1,2)/(1+Traw)
    mixed=[[(1-epsilon)*c[i][j]+epsilon*raw[i][j] for j in range(N-1)] for i in range(N-1)]
    mixed_matrix=base.lift(mixed,s);mixed_checks=base.check(family,mixed_matrix,s)
    base.require(mixed_checks['lower_rank']==N-1 and mixed_checks['upper_rank']==N-1,'mixed greatest endpoint ranks')
    half_gap=[[(N-s)*(int(i==j)-mixed_matrix[i][j])-F(1,2)*(int(i==j)-F(1,N)) for j in range(N)] for i in range(N)]
    base.require(base.psd_rank(half_gap)==N-1,'literal full mixed half-unit gap')
    bad=[row[:] for row in c];bad[oldN][oldN+1]+=1;bad[oldN+1][oldN]+=1
    try:base.check(family,base.lift(bad,s),s)
    except ValueError:pass
    else:raise ValueError('changed intersecting core entry was accepted')
    bad=[row[:] for row in mixed_matrix];bad[0][0]+=1
    try:base.check(family,bad,s)
    except ValueError:pass
    else:raise ValueError('changed empty loop was accepted')
    return {'n':n,'q':q,'loads':[D,t],'N':N,'changed_dimension':changed,'untouched_high':len(highs),'untouched_low':len(lows),'full_frame_dimension':N-3,'changed_generator_count':m,'all_full_frame_action_scalars':m*m,'all_literal_actions_and_empty_frame_matched':True,'seed':literal,'raw_core_rank':N-2,'raw_empty_energy':str(sum(map(sum,raw))),'raw_full_trace':str(Traw),'epsilon':str(epsilon),'mixed':mixed_checks,'seed_unit_gap':True,'mixed_half_unit_gap':True,'intersecting_entry_corruption_rejected':True,'empty_loop_corruption_rejected':True}

def stable(record):return {k:v for k,v in record.items() if k not in ['elapsed_seconds','peak_RSS_KiB']}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',type=Path);parser.add_argument('--expected',type=Path)
    args=parser.parse_args();start=time.monotonic();records=[]
    for n,D,t in [(3,3,2),(2,8,7),(3,8,7),(4,5,1),(6,2,1)]:
        signal.alarm(60);records.append(check(n,D,t));signal.alarm(0)
    out={'agent':'six-downset-1','role':'researcher','status':'finite original-index checks; uniform coverage is PROOF.md plus verify_signs.py','records':records,'elapsed_seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.expected:base.require(stable(out)==stable(json.loads(args.expected.read_text())['full']),'frozen full-action/matrix certificate mismatch')
    if args.write:args.write.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
