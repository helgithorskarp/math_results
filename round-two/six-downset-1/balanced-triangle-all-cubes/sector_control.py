"""PRIVATE complete variable-q original-row decomposition controls.

All old pair-constant and pair-antisymmetric directions are constructed,
with exact Gram-Schmidt in the latter two-constraint complement. The
checks cover every internal and cross pairing, then the actual matrix.
"""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[v]='1'
from pathlib import Path
import sys,argparse,json,signal,time,resource
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from exact import require,unit,vecadd,scale,matvec,dot,psd_rank,nullspace
from probe import construct,actual
from sectors import sectors

def verify(n,h):
    p,G,S,cap,C,v=construct(n,h);q=2**(n-1)
    params,grams,frames,caps=sectors(q,h)
    for name in ('s','N','ell','a','b','c','common','mu','alpha','beta','nu'):
        require(p[name]==params[name],'variable-q scalar '+name)
    size=len(G);e=lambda i:unit(size,i)
    TS=[vecadd(t[0],t[1],scale(-2,t[2])) for t in v['Ts']]
    W=[vecadd(u,scale(-1,p)) for u,p in zip(v['U'],v['P'])]
    means=[scale(F(1,3),vecadd(*W[3*i:3*i+3])) for i in range(2*h)]
    WA=[vecadd(W[3*i],scale(-1,W[3*i+1])) for i in range(2*h)]
    WF=[vecadd(W[3*i+2],scale(-1,means[i])) for i in range(2*h)]
    blocks=[]
    for i in range(2*h):
        blocks.append(('anti',[vecadd(v['Ts'][i][0],scale(-1,v['Ts'][i][1])),WA[i]],F(1)))
    for group in range(2):
        for k in range(1,h):
            t=[F(1) if i<k else F(-k) if i==k else F(0) for i in range(h)]
            terms=[vecadd(*(scale(t[i],rows[group*h+i]) for i in range(h))) for rows in (TS,WF,means)]
            Bt=vecadd(*(scale(t[i],v['Bs'][group][i]) for i in range(h)))
            blocks.append(('standard',[Bt]+terms,F(k*(k+1),2)))
    Gsum=vecadd(*(e(i) for i in range(2*q-1)));full=e(2*q-2)
    E=vecadd(Gsum,scale(-1,full));U=vecadd(Gsum,full)
    R=vecadd(v['Hx'],v['Hy'],Gsum,full);A=vecadd(v['Hx'],scale(-1,v['Hy']))
    blocks.append(('fixed-even',[E,U,R,vecadd(*TS),vecadd(*WF)],F(1)))
    sign=[F(1) if i<h else F(-1) for i in range(2*h)]
    blocks.append(('fixed-odd',[A]+[vecadd(*(scale(sign[i],row[i]) for i in range(2*h))) for row in (TS,WF,means)],F(1)))
    fullmask=2*q-1
    pairs=[(a,fullmask^a) for a in range(1,fullmask) if a<(fullmask^a)]
    require(len(pairs)==q-1,'all proper complementary pairs')
    plus=[vecadd(e(a-1),e(b-1)) for a,b in pairs]
    minus=[vecadd(e(a-1),scale(-1,e(b-1))) for a,b in pairs]
    for k in range(1,q-1):
        t=[F(1) if i<k else F(-k) if i==k else F(0) for i in range(q-1)]
        row=vecadd(*(scale(t[i],plus[i]) for i in range(q-1)))
        blocks.append(('untouched-even',[row],F(k*(k+1),2)))
    constraints=[[F(1-int(bool(a&1))-int(bool(a&2))) for a,b in pairs],
                 [F(int(bool(a&2))-int(bool(a&1))) for a,b in pairs]]
    require(dot(constraints[0],constraints[1])==0 and dot(constraints[0],constraints[0])==F(q-2,2) and dot(constraints[1],constraints[1])==F(q,2),'two surviving old antisymmetric directions')
    complement=[]
    for row in nullspace(constraints,q-1):
        for other in complement:
            row=vecadd(row,scale(-dot(row,other)/dot(other,other),other))
        require(dot(row,row)>0 and all(dot(row,z)==0 for z in constraints+complement),'exact full old complement orthogonalization')
        complement.append(row)
        physical=vecadd(*(scale(row[i],minus[i]) for i in range(q-1)))
        blocks.append(('untouched-odd',[physical],dot(row,row)))
    require(len(complement)==q-3,'entire old antisymmetric complement')
    basis=[b for name,rows,mult in blocks for b in rows]
    require(len(basis)==size==2*q+12*h-4,'complete physical dimension N-4')
    matrices=(G,S,cap);catalogues=(grams,frames,caps)
    images=[[matvec(A,row) for row in basis] for A in matrices]
    internal=0;cross=0;starts=[];start=0
    for name,rows,mult in blocks:
        stop=start+len(rows);starts.append((start,stop))
        for ai,catalogue in enumerate(catalogues):
            got=[[dot(basis[i],images[ai][j]) for j in range(start,stop)] for i in range(start,stop)]
            target=[[mult*z for z in row] for row in catalogue[name]]
            require(got==target,'EVERY original Gram/frame/cap sector '+name);internal+=len(rows)**2
        start=stop
    for ai in range(3):
        for bi,(a,b) in enumerate(starts):
            for bj,(c,d) in enumerate(starts):
                if bi==bj:continue
                for i in range(a,b):
                    for j in range(c,d):
                        require(dot(basis[i],images[ai][j])==0,'EVERY cross-sector pairing zero');cross+=1
    actualG=[[dot(a,image) for image in images[0]] for a in basis]
    require(psd_rank(actualG)==size,'complete independent sector basis')
    require(all(psd_rank(A)==len(A) for A in caps.values()),'all complete representative caps PD')
    original,M=actual(n,h)
    if (n,h)==(4,2):
        require(original['repaired']['matrix_sha256']=='6090acd333a5cb22d5b0a28157eaa8cbc398068febcbd6fe0b15c59377d4602d','saved full original n4,h2 finite pilot')
    return dict(n=n,q=q,h=h,N=p['N'],physical_dimension=size,anti_count=2*h,standard_count=2*(h-1),fixed_even=5,fixed_odd=4,untouched_even=q-2,untouched_odd=q-3,all_internal_G_frame_cap_positions=internal,all_cross_G_frame_cap_positions=cross,complete_sector_basis_verified=True,original=original)

def main():
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational barrier')
    def alarm(a,b):raise TimeoutError('unchanged60s full variable-q original control guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=4);ap.add_argument('--h',type=int,default=2);args=ap.parse_args()
    require((args.n,args.h) in ((4,2),(4,3)),'two next complete original fixtures only')
    result=verify(args.n,args.h);signal.alarm(0)
    out=dict(agent='six-downset-1',role='researcher',scope='PRIVATE finite original complete-sector validation; uniform physical bridge remains ordinary proof obligation',result=result,seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=sys.flags.optimize)
    (Path(__file__).resolve().parent/'work'/f'sectors-n{args.n}-h{args.h}-O{sys.flags.optimize}.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
    print(json.dumps(out,default=str))
if __name__=='__main__':main()
