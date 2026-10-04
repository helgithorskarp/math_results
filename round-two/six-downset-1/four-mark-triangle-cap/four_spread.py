"""Data-only four-mark invariant repair and original inverse control.

No constructor import. Full N70 carrier and saved new physical dual are
read, then original proper inverse and ALL empty-lift positions checked.
This same-author validation is not independent review or a uniform cap.
"""
from fractions import Fraction as F
from pathlib import Path
import json, time, resource, signal
from exact import require, zero, dot, matvec, psd_rank, lift, fingerprint, family_star
from linear import solve


def outer(x,y):
    return [[a*b for b in y] for a in x]


def centered(v):
    mean = sum(v)/len(v)
    return [x-mean for x in v]


def lifted_indicator(v):
    return [-sum(v)]+v


def swap_bits(mask,pairs):
    output = mask
    for i,j in pairs:
        if bool(mask&(1<<i)) != bool(mask&(1<<j)):
            output ^= (1<<i)|(1<<j)
    return output


def verify_data(raw,sector):
    n,h,l = raw['n'],raw['h'],raw['l']
    family = raw['family']
    N,q,s = len(family),2**(n-1),2**(n-1)+3*h
    require(type(n) is int and 4<=n<=6 and type(h) is int and 3<=h<=10
            and type(l) is int and 2<=l<h and N==2*q+6*(h+3*l)<=80,
            'unchanged bounded four-mark original repair domain')
    require(family_star(family)==s and sum(bool(x&1) for x in family)==s,
            'entire new literal downset and heavy maximum star')
    C = [[F(x) for x in row] for row in raw['core_C']]
    metric = [[F(x) for x in row] for row in raw['physical_metric']]
    rows = [[F(x) for x in row] for row in raw['all_physical_rows']]
    Mseed = [[F(x) for x in row] for row in raw['original_M']]
    require(len(C)==N-1 and lift(C,s)==Mseed, 'EVERY seed original matrix position')
    require(fingerprint(Mseed)==raw['record']['M_sha256']==sector['record']['M_sha256'],
            'whole original seed commitment')
    require(len(rows)==N and len(metric)==N-3
            and all(len(row)==N-3 for row in rows+metric), 'ENTIRE new physical input dimensions')
    images = [matvec(metric,row) for row in rows]
    fullQ = [[dot(row,image) for image in images] for row in rows]
    require([[1+fullQ[i][j]-s*F(i==j) for j in range(N)] for i in range(N)]
            ==[[(N-s)*value for value in row] for row in Mseed],
            'ALL original physical Gram and actual empty lift positions')
    oldsize,m,ell = 2*q-1,3*(h+3*l),3*(h+3*l)+1
    proper_private = oldsize+m
    a,b = [F(0)]*(N-1),[F(0)]*(N-1)
    for i in range(proper_private,proper_private+3*h): a[i] = F(1,h)
    for i in range(proper_private+3*h,N-1):
        if (i-proper_private)%3==2: b[i] = F(1,3*l)
    p = [x-3*y for x,y in zip(a,b)]
    c = [(x+3*y)/6 for x,y in zip(a,b)]
    heavy = [F(bool(x&1)) for x in family[1:]]
    rho = [F(m,ell)]*(oldsize+m)+[F(1)]*m
    require(not any(matvec(C,heavy)) and not any(matvec(C,rho)),
            'entire new proper null relations')
    require(dot(p,heavy)==dot(c,heavy)==dot(p,rho)==0 and dot(c,rho)==1,
            'ALL actual repair-kernel couplings')
    dual = [F(x) for x in sector['residual_dual']]
    image = matvec(metric,dual)
    scores = [dot(row,image) for row in rows]
    require(scores==[F(0)]+p, 'EVERY original dual score incl empty')
    kappa = dot(dual,image)
    require(kappa==F(sector['kappa']) and kappa>0,
            'new entire physical dual norm')
    # Two distinct original null relations are anchored by old{x} and
    # the final private full member. Their deletion is PD exactly here.
    keep = [i for i in range(N-1) if i not in (0,N-2)]
    principal = [[C[i][j] for j in keep] for i in keep]
    require(psd_rank(principal)==N-3, 'new original deleted principal PD')
    solution = solve(principal,[p[i] for i in keep])
    fullsolution = [F(0)]*(N-1)
    for i,x in zip(keep,solution): fullsolution[i] = x
    require(matvec(C,fullsolution)==p,
            'EVERY original inverse equation, incl BOTH deleted rows')
    require(dot(p,fullsolution)==kappa, 'ENTIRE original inverse energy agrees with physical dual')
    upper_endpoint = 6/kappa
    P = [[F(i==j)-F(1,N) for j in range(N)] for i in range(N)]
    repaired = []
    matrices = [Mseed]
    symmetry_positions = 0
    inverse_positions = N-1
    endpoint_lower = []
    for delta in (F(1,32),F(1,8),upper_endpoint):
        require(0<delta<=upper_endpoint, 'exact new line interval')
        sharp = [[C[i][j]+delta*(a[i]*b[j]+b[i]*a[j])
                  for j in range(N-1)] for i in range(N-1)]
        require(sharp==[[C[i][j]-delta*p[i]*p[j]/6+6*delta*c[i]*c[j]
                    for j in range(N-1)] for i in range(N-1)], 'ALL exact signed rank-two positions')
        M = lift(sharp,s)
        aa,bb = lifted_indicator(a),lifted_indicator(b)
        L = [[s*F(i==j)+(N-s)*M[i][j] for j in range(N)] for i in range(N)]
        seedL = [[s*F(i==j)+(N-s)*Mseed[i][j] for j in range(N)] for i in range(N)]
        require(L==[[seedL[i][j]+delta*(aa[i]*bb[j]+bb[i]*aa[j])
                     for j in range(N)] for i in range(N)],
                'EVERY original perturbed empty lift position')
        require(aa[0]==-3 and bb[0]==-1 and sum(aa)==sum(bb)==0
                and dot(aa,bb)==3 and dot(aa,aa)==9+F(3,h)
                and dot(bb,bb)==1+F(1,3*l), 'ALL actual empty repair norm identities')
        for i in range(N):
            require(sum(M[i])==1, 'every repaired original stochastic row')
            for j in range(N):
                require(M[i][j]==M[j][i], 'every repaired original symmetric position')
                if family[i]&family[j]: require(M[i][j]==0, 'ALL repaired original support')
        lower_rank = psd_rank(L)
        core_rank = psd_rank(sharp)
        require(lower_rank==(N-2 if delta==upper_endpoint else N-1)
                and core_rank==lower_rank-1, 'new actual line endpoint/interior ranks')
        endpoint_lower.append(dict(delta=str(delta),core_rank=core_rank,lower_rank=lower_rank))
        if delta==upper_endpoint: continue
        upper = [[N*F(i==j)-L[i][j] for j in range(N)] for i in range(N)]
        floor = 1-7*delta
        require(floor>0 and psd_rank(upper)==N-1
                and psd_rank([[upper[i][j]-floor*P[i][j] for j in range(N)]
                              for i in range(N)])==N-1, 'WHOLE new original cap and floor')
        starcenter = centered([F(bool(x&1)) for x in family])
        require(not any(matvec(L,starcenter)), 'full actual centered heavy-star kernel')
        record = dict(delta=str(delta),lower_rank=lower_rank,upper_rank=N-1,
                      cap_floor=str(floor),M_sha256=fingerprint(M),C_sha256=fingerprint(sharp))
        repaired.append(record)
        matrices.append(M)
    # Exact ORIGINAL negative witnesses outside this candidate line,
    # not counterexamples to the matrix existence conjecture.
    tilted = [x-dot(c,fullsolution)*r for x,r in zip(fullsolution,rho)]
    require(dot(c,tilted)==0 and dot(p,tilted)==kappa
            and dot(tilted,matvec(C,tilted))==kappa, 'full tilted inverse cancellation')
    outside = []
    for delta,w in ((F(-1,32),rho),(upper_endpoint+F(1,32),tilted)):
        sharp = [[C[i][j]+delta*(a[i]*b[j]+b[i]*a[j])
                  for j in range(N-1)] for i in range(N-1)]
        fullw = centered([F(0)]+w)
        M = lift(sharp,s)
        L = [[s*F(i==j)+(N-s)*M[i][j] for j in range(N)] for i in range(N)]
        energy = dot(fullw,matvec(L,fullw))
        expected = 6*delta if delta<0 else kappa*(1-delta*kappa/6)
        require(energy==expected and energy<0 and sum(fullw)==0,
                'new OUTSIDE line whole original exact negative witness')
        outside.append(dict(delta=str(delta),original_vector=[str(x) for x in fullw],
                            energy=str(energy),scope='ONLY this candidate repair line'))
    generators = []
    facets = h+3*l
    for f in range(facets): generators.append([(n+2*f,n+2*f+1)])
    for k,start in ((h,0),(l,h),(l,h+l),(l,h+2*l)):
        for f in range(start,start+k-1):
            generators.append([(n+2*f,n+2*(f+1)),(n+2*f+1,n+2*(f+1)+1)])
    for gi in (1,2):
        left,right=h+(gi-1)*l,h+gi*l
        generators.append([(gi,gi+1)]+[(n+2*(left+i)+a,n+2*(right+i)+a)
                                       for i in range(l) for a in range(2)])
    for i in range(4,n-1): generators.append([(i,i+1)])
    lookup = {mask:i for i,mask in enumerate(family)}
    for pairs in generators:
        moved = [swap_bits(mask,pairs) for mask in family]
        require(set(moved)==set(family), 'every claimed generator preserves ENTIRE original carrier')
        permutation = [lookup[mask] for mask in moved]
        for M in matrices:
            for i in range(N):
                for j in range(N):
                    require(M[i][j]==M[permutation[i]][permutation[j]],
                            'EVERY original seed/interior invariant matrix position')
                    symmetry_positions += 1
    return dict(agent='six-downset-1',role='researcher',private=True,
        status='EXACT FINITE FOUR-MARK CAPPED GREATEST-RANK REPAIR; PRIVATE finite control; generic ordinary bridge UNFORMALIZED and independent review pending',
        n=n,counts=[h,l,l,l],N=N,s=s,seed_M_sha256=fingerprint(Mseed),
        deleted_principal_dimension=N-3,all_original_inverse_positions=inverse_positions,
        kappa=str(kappa),lower_line_upper_endpoint=str(upper_endpoint),
        lower_line_endpoints=endpoint_lower,repaired=repaired,
        complete_actual_empty_lift_positions=3*N*N,
        symmetry_generators=len(generators),all_original_symmetry_positions=symmetry_positions,
        outside_line_original_witnesses=outside,
        exact_real_interval_bridge='ordinary real Schur interval in PROOF.md; rational controls validate implementation only')


def alarm(signum,frame):
    raise TimeoutError('unchanged child60s guard; incomplete is not absence')


if __name__=='__main__':
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60)
    start = time.monotonic();folder = Path(__file__).resolve().parent
    raw = json.loads((folder/'FOUR-MARK-FIRST-MATRIX.json').read_text())
    sector = json.loads((folder/'FOUR-MARK-FIRST-SECTOR.json').read_text())
    result = verify_data(raw,sector)
    packed = json.dumps(result,indent=2)+'\n'
    require(len(packed.encode())<=32*1024*1024, 'unchanged32MiB packing guard')
    (folder/'FOUR-MARK-FIRST-SPREAD-RESULT.json').write_text(packed)
    result['execution'] = dict(seconds=time.monotonic()-start,
        peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        optimized=not __debug__,one_mathematical_child=True,native_threads_one=True)
    signal.alarm(0);print(json.dumps(result),flush=True)
