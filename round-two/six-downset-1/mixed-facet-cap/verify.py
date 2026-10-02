"""Standalone uniform sign replay and original whole-matrix checks.

Every all-n completeness/PSD/empty-row bridge is written in PROOF.md.
Checks do not rely on Python assertions; -O must reproduce every field.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,signal,time,sys,resource
from mixed import build
from model import model
from closure import construct,cube
from symbolic import uniform,damages,rejects
from exact import require,gram,matvec,vecadd,scale,dot,unit,nullspace,psd_rank,lift,check

def alarm(signum,frame):raise TimeoutError('private mixed-facet60s fixture guard')
signal.signal(signal.SIGALRM,alarm)

def run(n):
    signal.alarm(60);start=time.monotonic()
    family,s,C,W,original=build(n);N=len(family);q=1<<(n-1);width=N-1;oldN=2*q-1
    Gmodel,Fmodel,p=model(F(q))
    G=[F(i<oldN) for i in range(width)];full=unit(width,oldN-1)
    h0=scale(F(-1,2),vecadd(G,full));gp=vecadd(G,h0)
    H=[[-F(i<oldN and bool(family[i+1]&(1<<j))) for i in range(width)] for j in range(2)]
    A=[vecadd(x,scale(-1,h0)) for x in H]
    U=[unit(width,oldN+2*j) for j in range(4)];V=[unit(width,oldN+2*j+1) for j in range(4)]
    h=scale(F(1,3),vecadd(*V[:3]));T=[vecadd(v,scale(-1,h)) for v in V[:3]]
    K=vecadd(G,*V);Z=vecadd(V[3],scale(F(-1,3),H[1]))
    tA=vecadd(V[0],scale(-1,V[1]));tS=vecadd(V[0],V[1],scale(-2,V[2]))
    wA=vecadd(U[0],scale(-1,U[1]),scale(p['c'],tA))
    w3=vecadd(U[2],scale(F(1,5),K),scale(-p['d'],h),scale(-p['e'],V[3]))
    w4=vecadd(U[3],scale(F(1,5),K),scale(-p['f'],h),scale(-p['g'],V[3]),scale(-p['c'],T[2]))
    coords=[gp,h0,*A,Z,tA,tS,wA,w3,w4]
    images=[matvec(C,x) for x in coords]
    actualG=[[dot(x,y) for y in images] for x in coords]
    empty=[-sum(x) for x in images]
    actualF=[[dot(x,y)+empty[i]*empty[j] for j,y in enumerate(images)] for i,x in enumerate(images)]
    require(actualG==Gmodel and actualF==Fmodel,'all original ten-coordinate Gram/frame entries including empty')
    require(psd_rank(actualG)==10,'changed-space independence')
    require(psd_rank([[(N-1)*actualG[i][j]-actualF[i][j] for j in range(10)] for i in range(10)])==10,'strict changed-space gap1')
    pairs=[(a,(2*q-1)^a) for a in range(1,2*q-1) if a<((2*q-1)^a)]
    high=[vecadd(unit(width,a-1),unit(width,b-1),scale(-1,unit(width,pairs[0][0]-1)),scale(-1,unit(width,pairs[0][1]-1))) for a,b in pairs[1:]]
    constraints=[[-F(bool(a&(1<<i)))+F(bool(b&(1<<i))) for a,b in pairs] for i in range(2)]
    low=[]
    for weights in nullspace(constraints,len(pairs)):
        z=[F(0)]*width
        for weight,(a,b) in zip(weights,pairs):z[a-1]+=weight;z[b-1]-=weight
        low.append(z)
    for vectors,eigenvalue,count in [(high,2*q,q-2),(low,6,q-3)]:
        require(len(vectors)==count,'complete untouched count')
        for z in vectors:
            require(matvec(C,z)==scale(eigenvalue,z),'all untouched original eigenactions')
            require(all(dot(image,z)==0 for image in images) and sum(z)==0,'all untouched changed/empty cross terms')
    require(10+len(high)+len(low)==psd_rank(C)==N-3,'full seed span census')
    M=lift(C,s);seed=check(family,M,s)
    P=[[F(i==j)-F(1,N) for j in range(N)] for i in range(N)]
    def gap_rank(M,amount):
        return psd_rank([[(N-s)*(F(i==j)-M[i][j])-amount*P[i][j] for j in range(N)] for i in range(N)])
    require(seed['lower_rank']==N-2 and seed['upper_rank']==N-1,'seed full ranks')
    require(gap_rank(M,F(1))==N-1,'actual original full seed gap1')
    rf,raw,rawM,rawout=construct(n,[(0,cube(2)),(1,cube(1))])
    require(rf==family and rawout['s']==s,'raw rank-repair uses same actual family')
    trace=(N-1)*(s-1)+sum(map(sum,raw));epsilon=F(1,2*(1+trace))
    require(trace==2*q*q+20*q-4+F(36,q),'explicit raw trace')
    require(epsilon==F(q,4*q**3+40*q*q-6*q+72),'explicit uniform mixture coefficient')
    mixture=[[(1-epsilon)*C[i][j]+epsilon*raw[i][j] for j in range(width)] for i in range(width)]
    mixed=lift(mixture,s);result=check(family,mixed,s)
    require(result['lower_rank']==result['upper_rank']==N-1 and gap_rank(mixed,F(1,2))==N-1,'original repair rank and gap1/2')
    signal.alarm(0)
    return {'n':n,'q':q,'seed':seed,'mixed':result,'changed_Gram_positions':100,'changed_frame_positions':100,'untouched_high':len(high),'untouched_low':len(low),'epsilon':str(epsilon),'raw_trace':str(trace)}


def full_damages():
    family,s,C,W,_=build(3);N=len(family);M=lift(C,s)
    bad=[row[:] for row in M];bad[0][0]+=1
    out=[rejects(lambda:check(family,bad,s),'actual empty-loop row tamper')]
    omitted=[row[:] for row in M]
    omitted[0]=[F(0)]*N
    for row in omitted:row[0]=F(0)
    out.append(rejects(lambda:check(family,omitted,s),'actual empty row omitted'))
    support=[row[:] for row in M]
    i,j=1,3
    support[i][j]+=1;support[j][i]+=1;support[i][i]-=1;support[j][j]-=1
    out.append(rejects(lambda:check(family,support,s),'row-preserving forbidden support'))
    nonfamily=family[:];nonfamily.remove(1)
    out.append(rejects(lambda:check(nonfamily,M,s),'missing downset face'))
    cap=[[F(N*(i==j)-1)-C[i][j] for j in range(N-1)] for i in range(N-1)]
    cap[0][0]=-1
    out.append(rejects(lambda:psd_rank(cap),'negative cap pivot'))
    G,A,_=model(F(4));A[0][0]+=1
    out.append(rejects(lambda:require(A==model(F(4))[1],'frame'),'wrong frame entry'))
    out.append(rejects(lambda:require(10+(4-2)+(4-4)==N-3,'census'),'omitted untouched direction'))
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',type=Path)
    parser.add_argument('--write',type=Path)
    args=parser.parse_args();start=time.monotonic()
    symbolic=uniform()
    rows=[]
    for n in [3,4,5,6]:
        rows.append(run(n));print('original n='+str(n)+' passed',file=sys.stderr,flush=True)
    damage=damages()+full_damages()
    result={'agent':'six-downset-1','role':'researcher',
            'claim':'all n>=3 mixed triangle facet and distinct-mark pendant: rational capped H, both greatest ranksN-1,scaled gap>=1/2',
            'trust_boundary':'exact symbolic certificate; complete real PSD/full-space/actual-empty bridge ordinary and unformalized; no independent review',
            'uniform_certificate':symbolic,'original_fixtures':rows,
            'rejected_damages':damage,'literal_guards':{'n_max':6,'N_max':80,'stage_seconds':60},
            'threads':1}
    if args.check:require(result==json.loads(args.check.read_text()),'complete frozen mathematical record')
    if args.write:args.write.write_text(json.dumps(result,indent=2)+'\n')
    from hashlib import sha256
    canonical=json.dumps(result,sort_keys=True,separators=(',',':')).encode()
    print(json.dumps({'record_sha256':sha256(canonical).hexdigest(),'original_fixtures':len(rows),'symbolic_minors':sum(len(r['minors']) for r in symbolic['records']),'damages':len(damage),'seconds':time.monotonic()-start,'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
