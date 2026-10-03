"""PRIVATE q4 complete literal frame control; no uniform extrapolation."""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[v]='1'
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from exact import require,unit,vecadd,scale,matvec,dot,psd_rank
from probe import construct,actual
from sectors import sectors
import argparse,json,signal,time,resource

def verify(h):
    p,G,S,cap,C,v=construct(3,h);params,grams,frames,caps=sectors(h)
    for name in ('s','N','ell','a','b','c','common','mu','alpha','beta','nu'):require(p[name]==params[name],'new complete sector scalar '+name)
    size=len(G);e=lambda i:unit(size,i)
    TS=[vecadd(t[0],t[1],scale(-2,t[2])) for t in v['Ts']]
    W=[vecadd(u,scale(-1,p)) for u,p in zip(v['U'],v['P'])]
    means=[scale(F(1,3),vecadd(*W[3*i:3*i+3])) for i in range(2*h)]
    WA=[vecadd(W[3*i],scale(-1,W[3*i+1])) for i in range(2*h)]
    WF=[vecadd(W[3*i+2],scale(-1,means[i])) for i in range(2*h)]
    blocks=[]
    for i in range(2*h):blocks.append(('anti',[vecadd(v['Ts'][i][0],scale(-1,v['Ts'][i][1])),WA[i]],F(1)))
    for group in range(2):
        for k in range(1,h):
            t=[F(1) if i<k else F(-k) if i==k else F(0) for i in range(h)]
            terms=[vecadd(*(scale(t[i],rows[group*h+i]) for i in range(h))) for rows in (TS,WF,means)]
            Bt=vecadd(*(scale(t[i],v['Bs'][group][i]) for i in range(h)))
            blocks.append(('standard',[Bt]+terms,F(k*(k+1),2)))
    Gsum=vecadd(*(e(i) for i in range(7)));full=e(6)
    E=vecadd(Gsum,scale(-1,full));U=vecadd(Gsum,full)
    R=vecadd(v['Hx'],v['Hy'],Gsum,full);A=vecadd(v['Hx'],scale(-1,v['Hy']))
    blocks.append(('fixed-even',[E,U,R,vecadd(*TS),vecadd(*WF)],F(1)))
    sign=[F(1) if i<h else F(-1) for i in range(2*h)]
    blocks.append(('fixed-odd',[A]+[vecadd(*(scale(sign[i],row[i]) for i in range(2*h))) for row in (TS,WF,means)],F(1)))
    pairs=[vecadd(e(i-1),e(j-1)) for i,j in ((1,6),(2,5),(3,4))]
    v1=vecadd(pairs[0],scale(-1,pairs[1]))
    v2=vecadd(pairs[0],pairs[1],scale(-2,pairs[2]))
    va=vecadd(e(0),scale(-1,e(5)),e(1),scale(-1,e(4)))
    blocks.extend([('untouched-even',[v1],F(1)),('untouched-even',[v2],F(3)),('untouched-odd',[va],F(1))])
    basis=[b for name,rows,mult in blocks for b in rows]
    require(len(basis)==size==12*h+4,'whole physical sector dimension N-4')
    matrices=(G,S,cap);catalogues=(grams,frames,caps)
    images=[[matvec(A,row) for row in basis] for A in matrices]
    internal=0;cross=0;starts=[];start=0
    for name,rows,mult in blocks:
        stop=start+len(rows);starts.append((start,stop))
        for ai,catalogue in enumerate(catalogues):
            got=[[dot(basis[i],images[ai][j]) for j in range(start,stop)] for i in range(start,stop)]
            target=[[mult*z for z in row] for row in catalogue[name]]
            require(got==target,'EVERY original physical Gram/frame/cap sector '+name);internal+=len(rows)**2
        start=stop
    for ai in range(3):
        for bi,(a,b) in enumerate(starts):
            for bj,(c,d) in enumerate(starts):
                if bi==bj:continue
                for i in range(a,b):
                    for j in range(c,d):require(dot(basis[i],images[ai][j])==0,'EVERY cross-sector pairing zero');cross+=1
    actualG=[[dot(a,image) for image in images[0]] for a in basis]
    require(psd_rank(actualG)==size,'complete independent sector basis, no omitted original direction')
    require(all(psd_rank(A)==len(A) for A in caps.values()),'every complete representative cap positive definite')
    original,M=actual(3,h)
    if h==2:require(original['repaired']['matrix_sha256']=='dc9b80b22d43b8e67abf8d5da444c4228d9e48cb8fc68c793fcf08a7f964a8c1','full saved q4 original h2 baseline')
    return dict(h=h,N=p['N'],physical_dimension=size,anti_count=2*h,standard_count=2*(h-1),fixed_even=5,fixed_odd=4,untouched_even=2,untouched_odd=1,all_internal_G_frame_cap_positions=internal,all_cross_G_frame_cap_positions=cross,complete_sector_basis_verified=True,original=original)

def main():
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational pause/handover barrier')
    def alarm(a,b):raise TimeoutError('unchanged60s q4 full original control guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    ap=argparse.ArgumentParser();ap.add_argument('--h',type=int,default=2);args=ap.parse_args()
    require(args.h in (2,3),'two bounded decomposition fixtures only')
    result=verify(args.h);signal.alarm(0)
    out=dict(agent='six-downset-1',role='researcher',scope='PRIVATE finite original complete-sector validation only; unbounded proof not established',result=result,seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=sys.flags.optimize)
    (Path(__file__).resolve().parent/'work'/f'sectors-h{args.h}-O{sys.flags.optimize}.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps(out,default=str))
if __name__=='__main__':main()
