"""Independent arithmetic, exhaustive small matrices, and physical consumers."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from itertools import combinations, product
from math import comb
import json
import random

import counts
from direct_span import target_counts
from quadruple import audit as quadruple_audit
from model import classify, physical, dot, PAIRS, INTERNAL
from extract import extract, clique
from verify import decode, verify


def need(ok, message):
    if not ok:
        raise ArithmeticError(message)


def dense_rank(rows, width):
    """Literal matrix elimination, separate from the factor model's basis map."""
    a = [[(row >> j)&1 for j in range(width)] for row in rows]
    pivot = 0
    for col in range(width):
        found = next((i for i in range(pivot,len(a)) if a[i][col]),None)
        if found is None:
            continue
        a[pivot],a[found] = a[found],a[pivot]
        for i in range(pivot+1,len(a)):
            if a[i][col]:
                a[i] = [x^y for x,y in zip(a[i],a[pivot])]
        pivot += 1
    return pivot


def arithmetic():
    independent = target_counts()
    entries = 0
    for cap in (3,4,5,23):
        for length in range(24):
            need(independent['nonzero'][cap][length] == counts.nonzero_span(length,5,cap),
                 'nonzero word count disagreement')
            entries += 1
            if length:
                need(independent['affine'][cap][length] == counts.affine_span(length,5,cap),
                     'affine word count disagreement')
                entries += 1
    for length in range(24):
        need(independent['all_vectors'][length] == counts.total_span(length,5),
             'unrestricted spanning word disagreement')
        entries += 1
    gl = 31*30*28*24*16
    def quotient(numerator):
        q,r = divmod(numerator,gl)
        need(r==0,'independent factor quotient')
        return q
    def nonzero(length,cap):
        return independent['nonzero'][23 if cap>=20 else cap][length]
    def affine(length,cap):
        return independent['affine'][23 if cap>=20 else cap][length]
    def low(ac,bc):
        return quotient(31*16*affine(20,ac)*affine(23,bc))
    total = quotient(independent['all_vectors'][20]*independent['all_vectors'][23])
    stages = [(total,low(20,23))]
    for name,ac,bc,az,bz in counts.STAGES:
        numerator = 0
        for i in range(az+1):
            for j in range(bz+1):
                if i and j:
                    continue
                numerator += comb(20,i)*comb(23,j)*nonzero(20-i,ac)*nonzero(23-j,bc)
        stages.append((quotient(numerator),low(ac,bc)))
    actual = counts.compute()
    for expected,(raw,lower) in zip(actual['stages'],stages):
        need((expected['raw'],expected['complement_rank_four'],expected['remaining']) ==
             (raw,lower,raw-lower),'target stage disagreement')
    need(len(actual['stages'])==len(stages),'stage coverage')
    remaining = [x-y for x,y in stages]
    need(all(x>y>0 for x,y in zip(remaining,remaining[1:])),'strict stage reductions')
    f = Fraction(remaining[0]-remaining[-1],remaining[0])
    need(actual['removed_fraction']==[f.numerator,f.denominator],'fraction mismatch')
    need(f>Fraction(39,100),'declared substantial global gate')
    return {'counts':actual,'independent_spanning_word_entries':entries,
            'independent_algorithm':'positive DP over actual vector labels and concrete linear spans',
            'all_target_stage_fields_checked':3*len(stages)}


def small_matrices():
    cases = [(2,3),(3,3),(3,4),(4,3),(4,4)]
    configurations = [(4,4,4,4),(2,2,1,1),(1,3,0,2),(3,1,2,0)]
    examined = 0
    results = []
    for m,n in cases:
        observed = Counter()
        for bits in range(1 << (m*n)):
            rows = [(bits >> (i*n)) & ((1<<n)-1) for i in range(m)]
            cols = [sum(((row >> j)&1) << i for i,row in enumerate(rows)) for j in range(n)]
            r = dense_rank(rows,n)
            br = dense_rank([row ^ ((1<<n)-1) for row in rows],n)
            examined += 1
            if not r:
                continue
            observed[(r,'total')] += 1
            if br==r-1:
                observed[(r,'total_low')] += 1
            ca,cb = Counter(rows),Counter(cols)
            for k,(ac,bc,az,bz) in enumerate(configurations):
                cap_ok = (ca[0]<=az and cb[0]<=bz and
                          max((v for x,v in ca.items() if x),default=0)<=ac and
                          max((v for x,v in cb.items() if x),default=0)<=bc)
                if cap_ok and not(ca[0] and cb[0]):
                    observed[(r,k,'raw')] += 1
                if cap_ok and br==r-1:
                    observed[(r,k,'low')] += 1
        checks = 0
        for r in range(1,min(m,n)+1):
            total = counts.total_span(m,r)*counts.total_span(n,r)//counts.group_order(r)
            need(total==observed[(r,'total')],'small total rank count')
            need(counts.lower_complement(m,n,r,m,n)==observed[(r,'total_low')],
                 'small unfiltered complement overlap')
            checks += 2
            for k,(ac,bc,az,bz) in enumerate(configurations):
                raw = counts.pair_count(m,n,r,ac,bc,min(m,az),min(n,bz))
                low = counts.lower_complement(m,n,r,ac,bc)
                need(raw==observed[(r,k,'raw')],'small capped factor count')
                need(low==observed[(r,k,'low')],'small capped complement overlap')
                checks += 2
        results.append({'shape':[m,n],'matrices':1 << (m*n),'exact_counts_checked':checks})
    return {'all_binary_matrices':examined,'cases':results}


def fibers():
    results = []
    for m,n,r in [(2,3,2),(3,3,3)]:
        left = [x for x in product(range(1<<r),repeat=m) if dense_rank(x,r)==r]
        right = [x for x in product(range(1<<r),repeat=n) if dense_rank(x,r)==r]
        multiplicities = Counter()
        for a in left:
            for b in right:
                bits = sum((sum(((x>>j)&1)*((y>>j)&1) for j in range(r))%2) << (i*n+k)
                           for i,x in enumerate(a) for k,y in enumerate(b))
                multiplicities[bits] += 1
        expected = counts.group_order(r)
        need(set(multiplicities.values())=={expected},'constant physical factor fiber')
        results.append({'shape':[m,n],'rank':r,'factor_pairs':len(left)*len(right),
                        'distinct_matrices':len(multiplicities),'each_fiber':expected})
    return results


def physical_checks():
    rng = random.Random(907205)
    families = {
        'zero_pair':([0]+list(range(1,20)),[0]+list(range(1,23))),
        'zero_multiplicity':([0,0]+list(range(1,19)),list(range(1,24))),
        'previous_row_cap':([1]*5+list(range(2,17)),list(range(1,24))),
        'column_class':(list(range(1,21)),[1]*6+list(range(2,19))),
        'new_quadruple_obstruction':([1]*4+list(range(2,18)),list(range(1,24))),
    }
    fixture = None
    tests = basis_changes = negatives = 0
    def rejects(fn):
        nonlocal negatives
        try:
            fn()
        except (ValueError,ArithmeticError,TypeError):
            negatives += 1
            return
        raise ArithmeticError('corrupted input was accepted')
    for name,(left,right) in families.items():
        for trial in range(8):
            a,b = left[:],right[:]
            rng.shuffle(a);rng.shuffle(b)
            data = {'rows':a,'columns':b,'internal_hex':format(rng.getrandbits(443),'0111x')}
            need(classify(data)=={'baseline':True,'keep':False,'reason':name},'physical filter branch')
            graph,cert = extract(data)
            need(verify(graph,cert)=='VERIFIED_PHYSICAL_MONOCHROMATIC_FIVE','literal certificate')
            adj = decode(graph)
            cross = [sum(adj[i][20+j] << j for j in range(23)) for i in range(20)]
            need(dense_rank(cross,23)==5 and dense_rank([x^((1<<23)-1) for x in cross],23)>=5,
                 'physical baseline ranks')
            p,q = rng.sample(range(5),2)
            changed = deepcopy(data)
            changed['rows'] = [x ^ (((x >> q)&1) << p) for x in a]
            changed['columns'] = [y ^ (((y >> p)&1) << q) for y in b]
            need(physical(changed)==graph and classify(changed)==classify(data),
                 'basis-change invariance')
            basis_changes += 1
            bad = deepcopy(cert);bad['vertices'][1]=bad['vertices'][0]
            rejects(lambda:verify(graph,bad))
            bad = deepcopy(cert);bad['color']='blue' if cert['color']=='red' else 'red'
            rejects(lambda:verify(graph,bad))
            if name=='new_quadruple_obstruction' and trial==0:
                fixture = {'parameters':data,'graph':graph,'certificate':cert}
            tests += 1
    need(fixture is not None,'missing quadruple fixture')
    retained = [
        {'rows':list(range(1,21)),'columns':list(range(1,24)),'internal_hex':'0'*111},
        {'rows':list(range(16,32))+list(range(16,20)),
         'columns':list(range(1,32,2))+list(range(1,14,2)),'internal_hex':'0'*111},
    ]
    retained_ranks = []
    for data in retained:
        need(classify(data)['keep'],'retained boundary unexpectedly rejected')
        adj = decode(physical(data))
        retained_ranks.append(dense_rank([sum((not adj[i][20+j]) << j for j in range(23))
                                         for i in range(20)],23))
        rejects(lambda:extract(data))
    need(retained_ranks==[6,5],'both allowed complementary ranks')
    low = {'rows':list(range(16,32))+list(range(16,20)),
           'columns':list(range(16,32))+list(range(16,23)),'internal_hex':'0'*111}
    need(classify(low)=={'baseline':False,'reason':'complement_rank_four'},'rank-four overlap input')
    rejects(lambda:extract(low))
    data = fixture['parameters']
    zero = deepcopy(data);zero['internal_hex']='0'*111
    basebits = int(physical(zero)['red_hex'],16)
    for k,pair in enumerate(INTERNAL):
        changed = deepcopy(zero);changed['internal_hex']=format(1 << k,'0111x')
        need(int(physical(changed)['red_hex'],16)^basebits == 1 << PAIRS.index(pair),
             'internal coordinate map')
    adj = decode(physical(zero))
    for i,x in enumerate(zero['rows']):
        for j,y in enumerate(zero['columns']):
            need(adj[i][20+j] == (sum(((x>>k)&1)*((y>>k)&1) for k in range(5))%2),
                 'cross coordinate map')
    bads=[]
    for field,value in [('rows',[1]*20),('columns',[1]*23),('internal_hex','0'),
                        ('internal_hex','f'*111),('internal_hex',0)]:
        bad=deepcopy(data);bad[field]=value;bads.append(bad)
    for value in (-1,32,True,1.0):
        bad=deepcopy(data);bad['rows'][0]=value;bads.append(bad)
    bad=deepcopy(data);bad['claimed_keep']=True;bads.append(bad)
    for bad in bads:
        rejects(lambda bad=bad:classify(bad))
    bad=deepcopy(fixture['graph']);bad['n']=42;rejects(lambda:verify(bad,fixture['certificate']))
    bad=deepcopy(fixture['graph']);bad['red_hex']='f'*226;rejects(lambda:verify(bad,fixture['certificate']))
    return {'fixtures_checked':tests,'basis_changes':basis_changes,
            'internal_coordinates_checked':len(INTERNAL),'cross_coordinates_checked':460,
            'retained_complementary_ranks':retained_ranks,
            'negative_controls':negatives,'fixture':fixture}


def clique_checks():
    examined = 0
    pairs = list(combinations(range(5),2))
    for bits in range(1024):
        for color in (0,1):
            adj = [[False]*5 for _ in range(5)]
            rows = [0]*5
            for k,(u,v) in enumerate(pairs):
                if ((bits >> k)&1)==color:
                    adj[u][v]=adj[v][u]=True
                    rows[u] |= 1 << v;rows[v] |= 1 << u
            for size in range(1,6):
                expected = next((list(vs) for vs in combinations(range(5),size)
                                 if all(adj[u][v] for u,v in combinations(vs,2))),None)
                need(clique(rows,31,size)==expected,'literal clique comparison')
                examined += 1
    return examined


def run():
    return {'status':'VERIFIED_RANK5_GLOBAL_SIEVE',
            'arithmetic':arithmetic(),'quadruple':quadruple_audit(),
            'small_matrices':small_matrices(),'factor_fibers':fibers(),
            'physical':physical_checks(),'literal_clique_comparisons':clique_checks()}


if __name__ == '__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
