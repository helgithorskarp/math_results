"""full original physical control of every proposed asymmetric sector."""
from pathlib import Path
from fractions import Fraction as F
import json,time,signal,resource
from completion_harmonic import build,alarm
from sectors_harmonic import sectors
from exact import require,vecadd,scale,dot,matvec,psd_rank,zero,nullspace,fingerprint


def control(n,h):
    seed,defining,C,M,family=build(n,h)
    p,grams,frames,caps,_=sectors(F(2**(n-1)),F(h))
    rows=[[F(z) for z in row] for row in defining['all_physical_rows']]
    metric=[[F(z) for z in row] for row in defining['physical_metric']]
    q,s,N,l,D=p['q'],p['s'],int(p['N']),h-1,p['D']
    oldsize=2**n-1;m=6*h-3;offset=1+oldsize+m
    old=rows[1:1+oldsize]
    G=vecadd(*old);gF=old[-1]
    Hx=scale(-1,vecadd(*(old[i] for i in range(oldsize) if (i+1)&1)))
    Hy=scale(-1,vecadd(*(old[i] for i in range(oldsize) if (i+1)&2)))
    E=vecadd(G,scale(-1,gF));U=vecadd(G,gF)
    R=vecadd(Hx,Hy,G,gF);A=vecadd(Hx,scale(-1,Hy))
    B,T,TS,WA,WF,means,private=[],[],[],[],[],[],[]
    for fi in range(h+l):
        mark=Hx if fi<h else Hy
        V=rows[1+oldsize+3*fi:1+oldsize+3*(fi+1)]
        bi=vecadd(scale(F(1,3),vecadd(*V)),scale(-1/D,mark))
        ti=[vecadd(v,scale(-1/D,mark),scale(-1,bi)) for v in V]
        B.append(bi);T.append(ti)
    bymean=scale(F(1,l),vecadd(*B[h:]))
    contrasts=B[:h]+[vecadd(b,scale(-1,bymean)) for b in B[h:]]
    for fi in range(h+l):
        group=int(fi>=h);start=0 if group==0 else h
        k=p['groups'][group]['k'];a=p['groups'][group]['a']
        b=p['groups'][group]['b'];c=p['groups'][group]['c']
        projected=[vecadd(rows[0],scale(a,contrasts[fi]),scale(c,T[fi][1-leaf])) for leaf in range(2)]
        other=vecadd(*(T[j][2] for j in range(start,start+int(k)) if j!=fi))
        projected.append(vecadd(rows[0],scale(b,contrasts[fi]),scale(c/(k-1),other)))
        ws=[vecadd(rows[offset+3*fi+leaf],scale(-1,projected[leaf])) for leaf in range(3)]
        mi=scale(F(1,3),vecadd(*ws))
        TS.append(vecadd(T[fi][0],T[fi][1],scale(-2,T[fi][2])))
        WA.append(vecadd(ws[0],scale(-1,ws[1])))
        WF.append(vecadd(ws[2],scale(-1,mi)));means.append(mi)
    blocks=[]
    for fi in range(h+l):
        label='x' if fi<h else 'y'
        blocks.append(('anti-'+label, [vecadd(T[fi][0],scale(-1,T[fi][1])),WA[fi]],F(1)))
    for label,start,k in (('x',0,h),('y',h,l)):
        for j in range(1,k):
            coeff=[F(1)]*j+[F(-j)]+[F(0)]*(k-j-1)
            vectors=[vecadd(*(scale(coeff[i],source[start+i]) for i in range(k)))
                     for source in (contrasts,TS,WF,means)]
            blocks.append(('standard-'+label,vectors,F(j*(j+1),2)))
    aggregate=[E,U,R,A,bymean,vecadd(*TS[:h]),vecadd(*TS[h:]),
               vecadd(*WF[:h]),vecadd(*WF[h:]),vecadd(*means[:h])]
    blocks.append(('aggregate',aggregate,F(1)))
    pairs=[(a,oldsize^a) for a in range(1,oldsize) if a<(oldsize^a)]
    pair_sums=[vecadd(old[a-1],old[b-1]) for a,b in pairs]
    pair_diffs=[vecadd(old[a-1],scale(-1,old[b-1])) for a,b in pairs]
    peven=[vecadd(pair_sums[i],scale(-1,pair_sums[-1])) for i in range(len(pairs)-1)]
    r=[F(1-int(bool(a&1))-int(bool(a&2))) for a,b in pairs]
    aa=[F(int(bool(a&2))-int(bool(a&1))) for a,b in pairs]
    kernel=nullspace([r,aa],len(pairs))
    podd=[vecadd(*(scale(t,v) for t,v in zip(z,pair_diffs))) for z in kernel]
    require(len(peven)==q-2 and len(podd)==q-3,'every untouched old direction')
    blocks.append(('untouched-even',peven,None));blocks.append(('untouched-odd',podd,None))
    basis=[v for name,b,sc in blocks for v in b]
    require(len(basis)==N-3,'ENTIRE row-span dimension, including light mean')
    images=[matvec(metric,v) for v in basis]
    fullG=[[dot(v,im) for im in images] for v in basis]
    pairing=[[dot(row,im) for row in rows] for im in images]
    fullS=[[dot(x,y) for y in pairing] for x in pairing]
    require(psd_rank(fullG)==N-3 and psd_rank(C)==N-3,
            'independent complete basis spans original rows')
    expectedG=zero(N-3);expectedS=zero(N-3);index=0;block_records=[]
    for name,b,sc in blocks:
        if sc is None:
            lam=2*q if name=='untouched-even' else 2*D
            Gblock=[[fullG[index+i][index+j] for j in range(len(b))] for i in range(len(b))]
            Sblock=[[lam*v for v in row] for row in Gblock]
        else:
            Gblock=[[sc*v for v in row] for row in grams[name]]
            Sblock=[[sc*v for v in row] for row in frames[name]]
        for i in range(len(b)):
            for j in range(len(b)):
                expectedG[index+i][index+j]=Gblock[i][j]
                expectedS[index+i][index+j]=Sblock[i][j]
        block_records.append(dict(name=name,dimension=len(b),scale=None if sc is None else str(sc)))
        index+=len(b)
    require(fullG==expectedG,'EVERY original sector metric and all cross entries')
    require(fullS==expectedS,'EVERY original frame and all cross entries, actual empty included')
    fullcap=[[(N-1)*fullG[i][j]-fullS[i][j] for j in range(N-3)] for i in range(N-3)]
    require(psd_rank(fullcap)==N-3,'whole original changed and untouched cap floor1')
    for name,cap in caps.items():require(psd_rank(cap)==len(cap),'all candidate rational sector caps')
    nx,ny=p['groups'][0]['nu'],p['groups'][1]['nu'];tau=p['tau']
    betay=p['groups'][1]['beta']
    tx=[F(int(i==0))-F(1,h) for i in range(h)]
    ty=[F(1,l)-F(int(i==l-1)) for i in range(l)]
    dual=vecadd(*(scale(t/nx,v) for t,v in zip(tx,means[:h])),
        *(scale(t/ny,v) for t,v in zip(ty,means[h:])),
        scale(1/(h*l*tau),vecadd(*means[:h])),scale(-2/betay,WF[-1]))
    dual_image=matvec(metric,dual)
    scores=[dot(row,dual_image) for row in rows]
    desired=[F(offset<=i<offset+3)-3*F(i==N-1) for i in range(N)]
    require(scores==desired,'EVERY original residual-dual score including actual empty')
    closed_kappa=F(h-1,h)/nx+F(l-1,l)/ny+1/(h*l*tau)+4/betay
    require(dot(dual,dual_image)==closed_kappa,'full physical residual-dual squared norm')
    record=dict(agent='six-downset-1',role='researcher',n=n,h=h,N=int(N),s=int(s),
        status='EXACT FINITE FULL ORIGINAL SECTOR CONTROL; uniform completeness bridge is in PROOF.md',
        basis=basis,blocks=block_records,residual_dual=[str(v) for v in dual],
        closed_kappa=str(closed_kappa),whole_residual_dual_scores_checked=True,complete_dimension=N-3,
        metric=fullG,frame=fullS,cap=fullcap,all_original_rows=len(rows),
        all_metric_and_frame_positions=2*(N-3)**2,
        metric_sha256=fingerprint(fullG),frame_sha256=fingerprint(fullS),
        cap_sha256=fingerprint(fullcap),seed_matrix_sha256=seed['matrix_sha256'])
    return record


if __name__=='__main__':
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    record=control(4,3)
    folder=Path.cwd()
    packed=json.dumps(record,indent=2,default=str)+'\n'
    require(len(packed.encode())<=32*1024*1024,'unchanged32MiB packing guard')
    (folder/'HARMONIC-FIRST-SECTOR-CONTROL.json').write_text(packed)
    signal.alarm(0)
    print(json.dumps({k:v for k,v in record.items() if k not in ('basis','metric','frame','cap')}|
        dict(seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             optimized=not __debug__),default=str),flush=True)
