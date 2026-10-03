"""PRIVATE whole original physical-sector correspondence, no extrapolation."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from exact import require,unit,vecadd,scale,matvec,dot,psd_rank
from model import construct
from sectors import sectors
import argparse,json,signal,time,resource

def verify(h):
    p,G,S,cap,C,v=construct(h);params,grams,frames,caps=sectors(h)
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
    blocks.append(('fixed-even',[e(0),e(1),vecadd(*TS),vecadd(*WF)],F(1)))
    sign=[F(1) if i<h else F(-1) for i in range(2*h)]
    blocks.append(('fixed-odd',[e(2)]+[vecadd(*(scale(sign[i],row[i]) for i in range(2*h))) for row in (TS,WF,means)],F(1)))
    basis=[b for name,rows,mult in blocks for b in rows]
    require(len(basis)==size==12*h,'whole physical sector dimension12h')
    matrices=(G,S,cap);catalogues=(grams,frames,caps)
    images=[[matvec(A,row) for row in basis] for A in matrices]
    internal=0;cross=0;starts=[];start=0
    for name,rows,mult in blocks:
        stop=start+len(rows);starts.append((start,stop));
        for ai,(A,catalogue) in enumerate(zip(matrices,catalogues)):
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
    actualG=[[dot(a,image) for image in images[0]] for a in basis];require(psd_rank(actualG)==size,'complete independent sector basis, no omitted original direction')
    require(all(psd_rank(A)==len(A) for A in caps.values()),'every complete representative cap positive definite')
    return dict(h=h,N=p['N'],physical_dimension=size,anti_count=2*h,standard_count=2*(h-1),fixed_even=4,fixed_odd=4,all_internal_G_frame_cap_positions=internal,all_cross_G_frame_cap_positions=cross,complete_sector_basis_verified=True)

def main():
    def alarm(a,b):raise TimeoutError('unchanged60s complete physical sector guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    ap=argparse.ArgumentParser();ap.add_argument('--h',type=int,default=2);args=ap.parse_args();result=verify(args.h);signal.alarm(0)
    out=dict(agent='six-downset-1',role='researcher',scope='PRIVATE finite original complete physical-sector validation only; unbounded proof not established',result=result,seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=sys.flags.optimize)
    (Path(__file__).resolve().parent/'work'/f'sectors-h{args.h}-O{sys.flags.optimize}.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
