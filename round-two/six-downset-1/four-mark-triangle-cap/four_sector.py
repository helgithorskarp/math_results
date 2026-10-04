"""New four-mark whole original physical-sector and mean-dual control.

The declared data are the full saved original Gram, with no constructor
import, no quotient loss, and no transported three-mark cap. Exact
primitives and the anti/facet-standard row algorithms are credited to4dd.
The twenty aggregate directions and light S3 split are fresh data.
"""
import os
for _n in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
           'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_n] = '1'
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, time, resource, signal
from exact import require, vecadd, scale, dot, matvec, psd_rank, zero, nullspace, fingerprint

def diagonal(values):
    return [[F(v) if i == j else F(0) for j in range(len(values))]
            for i, v in enumerate(values)]

def frame(metric, rows):
    d = len(metric)
    out = zero(d)
    for row, count in rows:
        require(len(row) == d and count >= 0 and
                not isinstance(count, float) and
                not any(isinstance(x, float) for x in row),
                'every whole exact aggregate row and multiplicity')
        image = matvec(metric, row)
        for i in range(d):
            for j in range(d):
                out[i][j] += count * image[i] * image[j]
    return out

def sectors(q, h, l, groups):
    q, h, l = F(q), F(h), F(l)
    require(q >= 8 and h > l >= 2 and len(groups) == 4,
            'fresh four-mark rational sector domain')
    s, D, d = q + 3*h, 3*h, h-l
    N, ell = 2*q + 6*(h+3*l), 3*(h+3*l)+1
    sizes = (h, l, l, l)
    meanS = sum(k*g['mu'] for k, g in zip(sizes, groups))
    grams, frames, recipes = {}, {}, {}
    for label, k, g in zip(('x','y','z','w'), sizes, groups):
        a, b, c, alpha, beta, nu = [g[t] for t in ('a','b','c','alpha','beta','nu')]
        G = diagonal([2*s, alpha])
        rr = [([F(1,2),0],1),([F(-1,2),0],1),
              ([-c/2,F(1,2)],1),([c/2,F(-1,2)],1)]
        name = 'anti-'+label
        grams[name], frames[name], recipes[name] = G, frame(G,rr), rr
        G = diagonal([2*s/3,12*s,2*beta,2*nu])
        rr = [([F(1,2),F(1,12),0,0],4),
              ([F(1,2),F(-1,6),0,0],2),
              ([a/2,c/12,F(-1,4),F(1,2)],4),
              ([b/2,c/(6*(k-1)),F(1,2),F(1,2)],2)]
        name = 'standard-'+label
        grams[name], frames[name], recipes[name] = G, frame(G,rr), rr
    mux, muy = groups[0]['mu'], groups[1]['mu']
    tau = mux*muy/meanS
    b0 = s*d/(3*h*l)
    mean_diag = l*muy-l*l*muy*muy/meanS
    G = diagonal([4*(q-1),4*D,4*D*(q-4),12*q*D,2*q*D,6*q*D,
        b0,b0,b0,6*h*s,6*l*s,6*l*s,6*l*s,
        h*groups[0]['beta'],l*groups[1]['beta'],l*groups[2]['beta'],l*groups[3]['beta'],
        3*h*l*tau,mean_diag,mean_diag])
    G[17][18] = G[18][17] = G[17][19] = G[19][17] = -h*l*tau
    G[18][19] = G[19][18] = -l*l*muy*muy/meanS
    rr = []
    for ix, iy, iz, iw in product((0,1), repeat=4):
        count = q/8-int(ix == iy == iz == iw)
        row = [1/(2*(q-1)),0,(4-2*(ix+iy+iz+iw))/(4*(q-4)),
               (-3*ix+iy+iz+iw)/(6*q),(iz-iy)/q,(2*iw-iy-iz)/(3*q)]+[0]*14
        rr.append((row,count))
    rr.append(([F(-1,2),F(1,2)]+[0]*18,1))
    z = [-1/(2*ell),3*l/(2*h*ell),-(h+3*l)/(4*h*ell),
         -(h-l)/(4*h*ell),0,0,-3*l/ell,-3*l/ell,-3*l/ell]+[0]*11
    for group, k, g in zip(range(4), sizes, groups):
        mark = [0,-1/(2*D),1/(4*D),
                1/(4*D) if group == 0 else -1/(12*D),
                0 if group in (0,3) else (1 if group == 1 else -1)/(2*D),
                0 if group == 0 else -1/(3*D) if group == 3 else 1/(6*D),
                int(group == 1),int(group == 2),int(group == 3)]+[0]*11
        leaf, full = mark[:], mark[:]
        leaf[9+group], full[9+group] = 1/(6*k), -1/(3*k)
        rr.extend([(leaf,2*k),(full,k)])
        leaf, full = z[:], z[:]
        leaf[9+group], full[9+group] = g['c']/(6*k), -g['c']/(3*k)
        leaf[13+group], full[13+group] = -1/(2*k), 1/k
        mi = ([1/h,0,0] if group == 0 else [0,1/l,0] if group == 1
              else [0,0,1/l] if group == 2 else [-1/l,-1/l,-1/l])
        leaf[17:], full[17:] = mi, mi
        rr.extend([(leaf,2*k),(full,k)])
    rr.append((z,1))
    require(sum(count for row,count in rr) == N,
            'all original aggregate multiplicities including actual empty')
    grams['aggregate'], frames['aggregate'], recipes['aggregate'] = G, frame(G,rr), rr
    even = [([r[0],r[1],r[2],r[3],F(1,3)*sum(r[6:9])], count) for r,count in rr]
    Ge = diagonal([4*(q-1),4*D,4*D*(q-4),12*q*D,3*b0])
    grams['first-even-five'], frames['first-even-five'] = Ge, frame(Ge,even)
    # Each light contrast profile has a two-direction physical block,
    # times its ENTIRE squared profile norm, not a bare quotient block.
    Gstd = diagonal([q*D,b0])
    Sstd = [[2*q*D*D+3*l*q*q,3*l*q*b0],
            [3*l*q*b0,3*l*b0*b0]]
    grams['first-light-standard-two'], frames['first-light-standard-two'] = Gstd,Sstd
    return dict(q=q,h=h,l=l,s=s,D=D,N=N,ell=ell,tau=tau,b0=b0),grams,frames,recipes

def control(folder, input_name='FOUR-MARK-FIRST-MATRIX.json'):
    raw = json.loads((folder/input_name).read_text())
    n,h,l = raw['n'],raw['h'],raw['l']
    q,s,N = 2**(n-1),2**(n-1)+3*h,len(raw['family'])
    require(type(n) is int and 4 <= n <= 6 and type(h) is int and 3 <= h <= 10
            and type(l) is int and 2 <= l < h and N == 2*q+6*(h+3*l) <= 80,
            'unchanged full original control guard')
    rows = [[F(x) for x in r] for r in raw['all_physical_rows']]
    metric = [[F(x) for x in r] for r in raw['physical_metric']]
    C = [[F(x) for x in r] for r in raw['core_C']]
    groups = [{k:F(v) for k,v in g.items()} for g in raw['parameters']['groups']]
    p,grams,frames,recipes = sectors(q,h,l,groups)
    sizes,starts = (h,l,l,l),(0,h,h+l,h+2*l)
    oldsize, m = 2*q-1, 3*(h+3*l)
    private_start = 1+oldsize+m
    old = rows[1:1+oldsize]
    G,gF = vecadd(*old),old[-1]
    H = [scale(-1,vecadd(*(old[i] for i in range(oldsize) if (i+1)&mark)))
         for mark in (1,2,4,8)]
    E,U = vecadd(G,scale(-1,gF)),vecadd(G,gF)
    R = vecadd(*H,scale(2,U))
    Hc = vecadd(scale(3,H[0]),*(scale(-1,v) for v in H[1:]))
    Hd1 = vecadd(H[1],scale(-1,H[2]))
    Hd2 = vecadd(H[1],H[2],scale(-2,H[3]))
    B,T = [],[]
    for group,k,start in zip(range(4),sizes,starts):
        for i in range(k):
            facet = start+i
            V = rows[1+oldsize+3*facet:1+oldsize+3*(facet+1)]
            bi = vecadd(scale(F(1,3),vecadd(*V)),scale(F(-1,3*h),H[group]))
            ti = [vecadd(v,scale(F(-1,3*h),H[group]),scale(-1,bi)) for v in V]
            B.append(bi);T.append(ti)
    bmeans = [scale(F(1,k),vecadd(*B[start:start+k])) for k,start in zip(sizes,starts)]
    contrasts = [vecadd(B[start+i],scale(-1,bmeans[g]))
                 for g,k,start in zip(range(4),sizes,starts) for i in range(k)]
    TS,WA,WF,means = [],[],[],[]
    for group,k,start in zip(range(4),sizes,starts):
        g = groups[group]
        for i in range(k):
            fi = start+i
            projected = [vecadd(rows[0],scale(g['a'],contrasts[fi]),
                         scale(g['c'],T[fi][1-leaf])) for leaf in range(2)]
            other = vecadd(*(T[start+j][2] for j in range(k) if j != i))
            projected.append(vecadd(rows[0],scale(g['b'],contrasts[fi]),scale(g['c']/(k-1),other)))
            ws = [vecadd(rows[private_start+3*fi+j],scale(-1,projected[j])) for j in range(3)]
            mi = scale(F(1,3),vecadd(*ws))
            TS.append(vecadd(T[fi][0],T[fi][1],scale(-2,T[fi][2])))
            WA.append(vecadd(ws[0],scale(-1,ws[1])))
            WF.append(vecadd(ws[2],scale(-1,mi)));means.append(mi)
    blocks = []
    for label,k,start in zip(('x','y','z','w'),sizes,starts):
        for fi in range(start,start+k):
            blocks.append(('anti-'+label,[vecadd(T[fi][0],scale(-1,T[fi][1])),WA[fi]],F(1)))
        for j in range(1,k):
            coeff = [F(1)]*j+[F(-j)]+[F(0)]*(k-j-1)
            vectors = [vecadd(*(scale(coeff[i],source[start+i]) for i in range(k)))
                       for source in (contrasts,TS,WF,means)]
            blocks.append(('standard-'+label,vectors,F(j*(j+1),2)))
    traces = lambda source: [vecadd(*source[start:start+k]) for start,k in zip(starts,sizes)]
    aggregate = [E,U,R,Hc,Hd1,Hd2,*bmeans[1:]]+traces(TS)+traces(WF)+traces(means)[:3]
    require(len(aggregate) == 20, 'whole fresh twenty aggregate directions')
    blocks.append(('aggregate',aggregate,F(1)))
    pairs = [(a,oldsize^a) for a in range(1,oldsize) if a < (oldsize^a)]
    pair_sums = [vecadd(old[a-1],old[b-1]) for a,b in pairs]
    pair_diffs = [vecadd(old[a-1],scale(-1,old[b-1])) for a,b in pairs]
    peven = [vecadd(pair_sums[i],scale(-1,pair_sums[-1])) for i in range(len(pairs)-1)]
    constraints = [[F(1-2*bool(a&mark)) for a,b in pairs] for mark in (1,2,4,8)]
    kernel = nullspace(constraints,len(pairs))
    podd = [vecadd(*(scale(t,v) for t,v in zip(coeff,pair_diffs))) for coeff in kernel]
    require(len(peven) == q-2 and len(podd) == q-5,
            'every untouched original old direction')
    blocks.extend([('untouched-even',peven,None),('untouched-odd',podd,None)])
    basis = [v for name,b,sc in blocks for v in b]
    d = N-3
    require(len(basis) == d, 'whole physical dimension with ALL THREE light means')
    images = [matvec(metric,v) for v in basis]
    fullG = [[dot(v,im) for im in images] for v in basis]
    scores = [[dot(row,im) for row in rows] for im in images]
    fullS = [[dot(x,y) for y in scores] for x in scores]
    require(psd_rank(fullG) == d and psd_rank(C) == d, 'entire independent original span')
    expectedG,expectedS = zero(d),zero(d)
    index,blocks_record = 0,[]
    for name,b,sc in blocks:
        if sc is None:
            lam = 2*q if name == 'untouched-even' else 2*p['D']
            Gblock = [row[index:index+len(b)] for row in fullG[index:index+len(b)]]
            Sblock = [[lam*v for v in row] for row in Gblock]
        else:
            Gblock = [[sc*v for v in row] for row in grams[name]]
            Sblock = [[sc*v for v in row] for row in frames[name]]
        for i in range(len(b)):
            for j in range(len(b)):
                expectedG[index+i][index+j] = Gblock[i][j]
                expectedS[index+i][index+j] = Sblock[i][j]
        blocks_record.append(dict(name=name,dimension=len(b),scale=None if sc is None else str(sc)))
        index += len(b)
    require(fullG == expectedG, 'ALL whole metric and cross-sector positions')
    require(fullS == expectedS, 'ALL whole frame and cross-sector positions including empty')
    fullcap = [[(N-1)*fullG[i][j]-fullS[i][j] for j in range(d)] for i in range(d)]
    require(psd_rank(fullcap) == d, 'whole finite fresh physical cap floor one')
    even = [E,U,R,Hc,vecadd(*bmeans[1:])]
    lights = [
        [Hd1,vecadd(bmeans[1],scale(-1,bmeans[2]))],
        [Hd2,vecadd(bmeans[1],bmeans[2],scale(-2,bmeans[3]))],
    ]
    split = [('first-even-five',even,F(1))]+[
        ('first-light-standard-two',v,F(scale_)) for v,scale_ in zip(lights,(2,6))]
    split_images = [[matvec(metric,v) for v in vectors] for _,vectors,_ in split]
    split_scores = [[[dot(row,im) for row in rows] for im in images] for images in split_images]
    for i in range(len(split)):
        for j in range(i+1,len(split)):
            require(all(dot(v,im) == 0 for v in split[i][1] for im in split_images[j]),
                    'every metric cross position between ALL light split copies')
            require(all(dot(v,im) == 0 for v in split_scores[i] for im in split_scores[j]),
                    'every frame cross position between ALL light split copies')
    for (name,vectors,sc),images,scores_ in zip(split,split_images,split_scores):
        GG = [[dot(v,im) for im in images] for v in vectors]
        SS = [[dot(x,y) for y in scores_] for x in scores_]
        require(GG == [[sc*x for x in row] for row in grams[name]] and
                SS == [[sc*x for x in row] for row in frames[name]],
                'every fresh light split block entry and squared profile multiplicity')
        require(psd_rank([[(N-1)*GG[i][j]-SS[i][j] for j in range(len(vectors))]
                          for i in range(len(vectors))]) == len(vectors), 'finite split cap')
    aggS = frames['aggregate']
    require(all(aggS[i][j] == 0 for i in range(9) for j in range(9,20)),
            'ALL first-nine/remaining-eleven aggregate frame positions')
    require(all(aggS[i][j] == 0 for i in range(9,17) for j in range(17,20)),
            'ALL aggregate trace/mean frame positions')
    meanx = traces(means)[0]
    dual = vecadd(scale(1/(3*h*l*p['tau']),meanx),
                  scale(-F(2,3*l)/groups[1]['beta'],vecadd(*WF[h:])))
    image = matvec(metric,dual)
    dual_scores = [dot(row,image) for row in rows]
    target = [F(0)]*N
    for i in range(private_start,private_start+3*h):
        target[i] = F(1,h)
    for i in range(private_start+3*h,N):
        if (i-private_start)%3 == 2:
            target[i] = F(-1,l)
    require(dual_scores == target, 'ALL fresh original mean-dual scores including actual empty')
    kappa = F(1,h)/groups[0]['mu']+F(1,3*l)/groups[1]['mu']+F(4,3*l)/groups[1]['beta']
    require(dot(dual,image) == kappa, 'whole fresh four-mark residual mean-dual norm')
    record = dict(agent='six-downset-1',role='researcher',private=True,
        status='EXACT FINITE FOUR-MARK ORIGINAL SECTOR/DUAL; uniform proof is ordinary/unformalized in PROOF.md; independent review pending',
        n=n,counts=[h,l,l,l],N=N,s=s,physical_dimension=d,
        first_even_dimension=5,light_standard_copies=2,light_standard_dimension=2,
        light_profile_squared_norms=[2,6],aggregate_dimension=20,blocks=blocks_record,
        all_metric_and_frame_positions=2*d*d,all_actual_empty_scores=N,
        all_cross_sector_positions_checked=True,all_three_light_means_retained=True,
        all_light_split_cross_positions_checked=True,
        aggregate_first_trace_mean_cross_checked=True,kappa=str(kappa),
        M_sha256=raw['record']['M_sha256'],metric_sha256=fingerprint(fullG),
        frame_sha256=fingerprint(fullS),cap_sha256=fingerprint(fullcap))
    defining = dict(record=record,basis=basis,metric=fullG,frame=fullS,cap=fullcap,
                    grams=grams,frames=frames,recipes=recipes,residual_dual=dual,
                    residual_dual_scores=dual_scores,kappa=kappa)
    return record,defining

def alarm(signum,frame):
    raise TimeoutError('unchanged60s guard; incomplete is not absence')

if __name__ == '__main__':
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60)
    start = time.monotonic();folder = Path(__file__).resolve().parent
    result,defining = control(folder)
    packed = json.dumps(defining,indent=2,default=str)+'\n'
    require(len(packed.encode()) <= 32*1024*1024, 'unchanged32MiB packing guard')
    (folder/'FOUR-MARK-FIRST-SECTOR.json').write_text(packed)
    (folder/'FOUR-MARK-FIRST-SECTOR-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    result['execution'] = dict(seconds=time.monotonic()-start,
        peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        optimized=not __debug__,one_mathematical_child=True,native_threads_one=True)
    signal.alarm(0);print(json.dumps(result),flush=True)
