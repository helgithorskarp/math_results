"""Original-data physical-sector control, six-downset-1/researcher.

Reads the WHOLE saved new original geometry. It does not import the new
constructor or transport any two-mark cap. Exact primitives are credited.
All cross positions and the actual empty frame contribution are paid.
"""
from fractions import Fraction as F
from pathlib import Path
import json, time, resource, signal
from exact import require, vecadd, scale, dot, matvec, psd_rank, zero, nullspace, fingerprint


def diagonal(values):
    return [[F(v) if i==j else F(0) for j in range(len(values))]
            for i,v in enumerate(values)]


def frame(metric, rows):
    d = len(metric)
    output = zero(d)
    for row, count in rows:
        require(len(row)==d and count>=0, 'complete rational aggregate row count')
        require(not any(isinstance(x,float) for x in row)
                and not isinstance(count,float), 'only exact rational frame data')
        image = matvec(metric,row)
        for i in range(d):
            for j in range(d): output[i][j] += count*image[i]*image[j]
    return output


def sectors(q,h,l,groups):
    q,h,l = F(q),F(h),F(l)
    s,D = q+3*h,3*h
    N,ell = 2*q+6*(h+2*l),3*(h+2*l)+1
    sizes = (h,l,l)
    meanS = sum(k*g['mu'] for k,g in zip(sizes,groups))
    grams,frames,recipes = {},{},{}
    for label,k,g in zip(('x','y','z'),sizes,groups):
        a,b,c,alpha,beta,nu = [g[key] for key in ('a','b','c','alpha','beta','nu')]
        G = diagonal([2*s,alpha])
        rows = [([F(1,2),0],1),([F(-1,2),0],1),
                ([-c/2,F(1,2)],1),([c/2,F(-1,2)],1)]
        name = 'anti-'+label
        grams[name],frames[name],recipes[name] = G,frame(G,rows),rows
        G = diagonal([2*s/3,12*s,2*beta,2*nu])
        rows = [([F(1,2),F(1,12),0,0],4),
                ([F(1,2),F(-1,6),0,0],2),
                ([a/2,c/12,F(-1,4),F(1,2)],4),
                ([b/2,c/(6*(k-1)),F(1,2),F(1,2)],2)]
        name = 'standard-'+label
        grams[name],frames[name],recipes[name] = G,frame(G,rows),rows
    mux,muy = groups[0]['mu'],groups[1]['mu']
    tau = mux*muy/meanS
    Bbar2 = s*(h-l)/(3*h*l)
    G = diagonal([4*(q-1),4*D,3*D*(q-3),6*q*D,2*q*D,
        Bbar2,Bbar2,6*h*s,6*l*s,6*l*s,
        h*groups[0]['beta'],l*groups[1]['beta'],l*groups[2]['beta'],
        2*h*l*tau,l*muy-l*l*muy*muy/meanS])
    G[13][14] = G[14][13] = -h*l*tau
    rows = []
    for ix in (0,1):
        for iy in (0,1):
            for iz in (0,1):
                count = q/4-int(ix==iy==iz)
                row = [1/(2*(q-1)),0,(3-2*(ix+iy+iz))/(3*(q-3)),
                    (-2*ix+iy+iz)/(3*q),(iz-iy)/q]+[0]*10
                rows.append((row,count))
    rows.append(([F(-1,2),F(1,2)]+[0]*13,1))
    z = [-1/(2*ell),l/(h*ell),-(h+2*l)/(3*h*ell),
         -(h-l)/(3*h*ell),0,-3*l/ell,-3*l/ell]+[0]*8
    for group,k,g in zip(range(3),sizes,groups):
        mark = [0,-1/(2*D),1/(3*D),
                1/(3*D) if group==0 else -1/(6*D),
                0 if group==0 else (1 if group==1 else -1)/(2*D),
                int(group==1),int(group==2)]+[0]*8
        leaf,full = mark[:],mark[:]
        leaf[7+group],full[7+group] = 1/(6*k),-1/(3*k)
        rows.extend([(leaf,2*k),(full,k)])
        leaf,full = z[:],z[:]
        leaf[7+group],full[7+group] = g['c']/(6*k),-g['c']/(3*k)
        leaf[10+group],full[10+group] = -1/(2*k),1/k
        mi = [1/h,0] if group==0 else [0,1/l] if group==1 else [-1/l,-1/l]
        leaf[13:] = mi
        full[13:] = mi
        rows.extend([(leaf,2*k),(full,k)])
    rows.append((z,1))
    require(sum(count for row,count in rows)==N, 'all new actual aggregate row multiplicities')
    grams['aggregate'],frames['aggregate'],recipes['aggregate'] = G,frame(G,rows),rows
    # First SEVEN directions, freshly derived. Equal-light mark exchange
    # gives an even FIVE and odd TWO after all original rows are counted.
    even,odd = [],[]
    for row,count in rows:
        even.append(([row[0],row[1],row[2],row[3],F(1,2)*(row[5]+row[6])],count))
        odd.append(([row[4],F(1,2)*(row[5]-row[6])],count))
    Ge = diagonal([4*(q-1),4*D,3*D*(q-3),6*q*D,2*Bbar2])
    Go = diagonal([2*q*D,2*Bbar2])
    grams['first-even-five'],frames['first-even-five'] = Ge,frame(Ge,even)
    grams['first-odd-two'],frames['first-odd-two'] = Go,frame(Go,odd)
    return dict(q=q,h=h,l=l,s=s,D=D,N=N,ell=ell,tau=tau),grams,frames,recipes


def control(folder,input_name='THREE-MARK-FIRST-MATRIX.json'):
    raw = json.loads((folder/input_name).read_text())
    n,h,l = raw['n'],raw['h'],raw['l']
    q,s,N = 2**(n-1),2**(n-1)+3*h,len(raw['family'])
    require(type(n) is int and 3<=n<=6 and type(h) is int and 3<=h<=10
            and type(l) is int and 2<=l<h and N==2*q+6*(h+2*l)<=80,
            'unchanged bounded three-mark original sector domain')
    rows = [[F(x) for x in row] for row in raw['all_physical_rows']]
    metric = [[F(x) for x in row] for row in raw['physical_metric']]
    C = [[F(x) for x in row] for row in raw['core_C']]
    groups = [{key:F(value) for key,value in g.items()} for g in raw['parameters']['groups']]
    p,grams,frames,recipes = sectors(q,h,l,groups)
    sizes,starts = (h,l,l),(0,h,h+l)
    oldsize = 2*q-1
    m = 3*(h+2*l)
    private_start = 1+oldsize+m
    old = rows[1:1+oldsize]
    G,gF = vecadd(*old),old[-1]
    H = [scale(-1,vecadd(*(old[i] for i in range(oldsize) if (i+1)&mark)))
         for mark in (1,2,4)]
    E,U = vecadd(G,scale(-1,gF)),vecadd(G,gF)
    R = vecadd(*H,scale(F(3,2),U))
    Hc = vecadd(scale(2,H[0]),scale(-1,H[1]),scale(-1,H[2]))
    Hd = vecadd(H[1],scale(-1,H[2]))
    B,T = [],[]
    for group,k,start in zip(range(3),sizes,starts):
        for i in range(k):
            facet = start+i
            V = rows[1+oldsize+3*facet:1+oldsize+3*(facet+1)]
            bi = vecadd(scale(F(1,3),vecadd(*V)),scale(F(-1,3*h),H[group]))
            ti = [vecadd(v,scale(F(-1,3*h),H[group]),scale(-1,bi)) for v in V]
            B.append(bi)
            T.append(ti)
    bmeans = [scale(F(1,k),vecadd(*B[start:start+k])) for k,start in zip(sizes,starts)]
    contrasts = [vecadd(B[start+i],scale(-1,bmeans[g]))
                 for g,k,start in zip(range(3),sizes,starts) for i in range(k)]
    TS,WA,WF,means = [],[],[],[]
    for group,k,start in zip(range(3),sizes,starts):
        g = groups[group]
        for i in range(k):
            fi = start+i
            projected = [vecadd(rows[0],scale(g['a'],contrasts[fi]),
                         scale(g['c'],T[fi][1-leaf])) for leaf in range(2)]
            other = vecadd(*(T[start+j][2] for j in range(k) if j!=i))
            projected.append(vecadd(rows[0],scale(g['b'],contrasts[fi]),
                                    scale(g['c']/(k-1),other)))
            ws = [vecadd(rows[private_start+3*fi+leaf],scale(-1,projected[leaf]))
                  for leaf in range(3)]
            mi = scale(F(1,3),vecadd(*ws))
            TS.append(vecadd(T[fi][0],T[fi][1],scale(-2,T[fi][2])))
            WA.append(vecadd(ws[0],scale(-1,ws[1])))
            WF.append(vecadd(ws[2],scale(-1,mi)))
            means.append(mi)
    blocks = []
    for label,k,start in zip(('x','y','z'),sizes,starts):
        for fi in range(start,start+k):
            blocks.append(('anti-'+label,[vecadd(T[fi][0],scale(-1,T[fi][1])),WA[fi]],F(1)))
        for j in range(1,k):
            coeff = [F(1)]*j+[F(-j)]+[F(0)]*(k-j-1)
            vectors = [vecadd(*(scale(coeff[i],source[start+i]) for i in range(k)))
                       for source in (contrasts,TS,WF,means)]
            blocks.append(('standard-'+label,vectors,F(j*(j+1),2)))
    traces = lambda source: [vecadd(*source[start:start+k]) for start,k in zip(starts,sizes)]
    aggregate = [E,U,R,Hc,Hd,bmeans[1],bmeans[2]]+traces(TS)+traces(WF)+traces(means)[:2]
    blocks.append(('aggregate',aggregate,F(1)))
    pairs = [(a,oldsize^a) for a in range(1,oldsize) if a < (oldsize^a)]
    pair_sums = [vecadd(old[a-1],old[b-1]) for a,b in pairs]
    pair_diffs = [vecadd(old[a-1],scale(-1,old[b-1])) for a,b in pairs]
    peven = [vecadd(pair_sums[i],scale(-1,pair_sums[-1])) for i in range(len(pairs)-1)]
    constraints = [[F(1-2*bool(a&mark)) for a,b in pairs] for mark in (1,2,4)]
    kernel = nullspace(constraints,len(pairs))
    podd = [vecadd(*(scale(t,v) for t,v in zip(coeff,pair_diffs))) for coeff in kernel]
    require(len(peven)==q-2 and len(podd)==q-4, 'ALL untouched old directions')
    blocks.extend([('untouched-even',peven,None),('untouched-odd',podd,None)])
    basis = [v for name,b,sc in blocks for v in b]
    d = N-3
    require(len(basis)==d, 'ENTIRE new physical dimension incl BOTH light means')
    images = [matvec(metric,v) for v in basis]
    fullG = [[dot(v,im) for im in images] for v in basis]
    pairing = [[dot(row,im) for row in rows] for im in images]
    fullS = [[dot(x,y) for y in pairing] for x in pairing]
    require(psd_rank(fullG)==d and psd_rank(C)==d, 'complete original independent span')
    expectedG,expectedS = zero(d),zero(d)
    index = 0
    blocks_record = []
    for name,b,sc in blocks:
        if sc is None:
            lam = 2*q if name=='untouched-even' else 2*p['D']
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
    require(fullG==expectedG, 'EVERY new metric and ALL cross-sector positions')
    require(fullS==expectedS, 'EVERY new frame and ALL cross-sector positions incl actual empty')
    fullcap = [[(N-1)*fullG[i][j]-fullS[i][j] for j in range(d)] for i in range(d)]
    require(psd_rank(fullcap)==d, 'WHOLE fresh cap floor on physical row span')
    # The first-seven cap has the two distinct light means. Verify the
    # parity splitting directly, and keep all other aggregate directions.
    ev = [E,U,R,Hc,vecadd(bmeans[1],bmeans[2])]
    od = [Hd,vecadd(bmeans[1],scale(-1,bmeans[2]))]
    evim,odim = [matvec(metric,v) for v in ev],[matvec(metric,v) for v in od]
    evscore = [[dot(row,im) for row in rows] for im in evim]
    odscore = [[dot(row,im) for row in rows] for im in odim]
    require(all(dot(v,im)==0 for v in ev for im in odim), 'ALL first parity metric cross')
    require(all(dot(v,im)==0 for v in evscore for im in odscore), 'ALL first parity frame cross')
    for name,b,im,scores in (('first-even-five',ev,evim,evscore),('first-odd-two',od,odim,odscore)):
        GG = [[dot(v,i) for i in im] for v in b]
        SS = [[dot(a,b) for b in scores] for a in scores]
        require(GG==grams[name] and SS==frames[name], 'ALL new parity block original positions')
        require(psd_rank([[(N-1)*GG[i][j]-SS[i][j] for j in range(len(b))]
                    for i in range(len(b))])==len(b), 'new finite parity cap')
    aggS = frames['aggregate']
    require(all(aggS[i][j]==0 for i in range(7) for j in range(7,15)),
            'ALL first-seven/remaining-eight aggregate frame cross')
    require(all(aggS[i][j]==0 for i in range(7,13) for j in range(13,15)),
            'ALL aggregate trace/mean frame cross')
    # Full ORIGINAL dual, including every actual empty score. The norm
    # formula is new to this THREE-group construction and checked here.
    meanx = traces(means)[0]
    dual = vecadd(scale(1/(2*h*l*p['tau']),meanx),
        scale(-1/(l*groups[1]['beta']),vecadd(*WF[h:])))
    dualim = matvec(metric,dual)
    scores = [dot(row,dualim) for row in rows]
    target = [F(0)]*N
    for i in range(private_start,private_start+3*h): target[i] = F(1,h)
    for i in range(private_start+3*h,N):
        if (i-private_start)%3==2: target[i] = F(-3,2*l)
    require(scores==target, 'EVERY new invariant-dual original score incl empty')
    kappa = F(1,h)/groups[0]['mu']+F(1,2*l)/groups[1]['mu']+F(2,l)/groups[1]['beta']
    require(dot(dual,dualim)==kappa, 'new full residual dual norm formula')
    record = dict(agent='six-downset-1',role='researcher',private=True,
        status='EXACT FINITE THREE-MARK ORIGINAL SECTOR AND DUAL CONTROL; generic ordinary proof in PROOF.md; unformalized/unreviewed',
        n=n,counts=[h,l,l],N=N,s=s,physical_dimension=d,
        first_even_dimension=5,first_odd_dimension=2,
        aggregate_dimension=15,blocks=blocks_record,
        all_metric_and_frame_positions=2*d*d,all_actual_empty_scores=N,
        all_cross_sector_positions_checked=True,both_light_means_retained=True,
        first_parity_cross_checked=True,aggregate_first_trace_mean_cross_checked=True,
        kappa=str(kappa),M_sha256=raw['record']['M_sha256'],
        metric_sha256=fingerprint(fullG),frame_sha256=fingerprint(fullS),cap_sha256=fingerprint(fullcap))
    defining = dict(record=record,basis=basis,metric=fullG,frame=fullS,cap=fullcap,
                    grams=grams,frames=frames,recipes=recipes,residual_dual=dual,
                    residual_dual_scores=scores,kappa=kappa)
    return record,defining


def alarm(signum,frame):
    raise TimeoutError('unchanged child60s guard; unfinished is incompleteness')


if __name__=='__main__':
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60)
    start = time.monotonic();folder = Path(__file__).resolve().parent
    result,defining = control(folder)
    packed = json.dumps(defining,indent=2,default=str)+'\n'
    require(len(packed.encode())<=32*1024*1024, 'unchanged32MiB packing guard')
    (folder/'THREE-MARK-FIRST-SECTOR.json').write_text(packed)
    (folder/'THREE-MARK-FIRST-SECTOR-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    result['execution'] = dict(seconds=time.monotonic()-start,
        peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        optimized=not __debug__,one_mathematical_child=True,native_threads_one=True)
    signal.alarm(0);print(json.dumps(result),flush=True)
