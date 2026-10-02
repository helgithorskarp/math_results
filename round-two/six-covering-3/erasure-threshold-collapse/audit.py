"""Separate literal10080 engine and rational/explicit-subset collapse audit.

No import of the cofactor checker, model, separator, encoder or solver.
The general normalization/monotonicity bridges remain written proofs.
"""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import ceil
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def scalar_audit(D):
    def k(q, b):
        return max(0, ceil(Fraction(16*q-12-(2*q-1)*b, 4*q)))
    table = [[b] + [k(q, b) for q in range(2, 7)] for b in range(13)]
    rays = []
    for b in range(13):
        K = k(6, b)
        def upper(q):
            return 4*q*K - (16*q-12-(2*q-1)*b)
        def lower(q):
            return (16*q-12-(2*q-1)*b) - 4*q*(K-1)
        upper_slope = upper(7)-upper(6)
        require(upper_slope >= 0 and upper(6) >= 0, 'upper affine ray failed')
        if K:
            lower_slope = lower(7)-lower(6)
            require(lower_slope >= 0 and lower(6) > 0, 'strict lower ray failed')
            lower_at6 = lower(6)
        else:
            lower_slope = lower_at6 = None
        rays.append([b, K, upper_slope, upper(6), lower_slope, lower_at6])
    families = [(2,1,3),(2,3,2),(2,6,1),(3,2,3),(3,4,2),(3,7,1),
                (4,5,2),(5,3,3),(6,1,4)]
    retained = []; counts = []
    for q, b, needed in families:
        count = 0
        for rest in combinations(D[1:], b-1):
            forbidden = {1, *rest}
            mask = sum(1 << D.index(d) for d in forbidden)
            retained.append((q-1, mask, needed)); count += 1
        counts.append(count)
    implications = legal1 = zero = 0
    for q in range(2, 7):
        for B in range(1 << len(D)):
            K = k(q, B.bit_count())
            if not B & 1:
                require(4*q*7+(2*q-1)*B.bit_count() >= 16*q-12, 'legal1 failed')
                legal1 += 1
            elif not K:
                zero += 1
            else:
                require(any(arity <= q-1 and mask & B == B and needed >= K
                            for arity, mask, needed in retained), 'literal subset implication missing')
                implications += 1
    return {'scalar_threshold_table':table, 'infinite_affine_rays':rays,
            'finite_families':[list(v)+[n] for v,n in zip(families,counts)],
            'original_predicates':len(retained), 'new_predicates_beyond_q2_q3':sum(counts[-3:]),
            'five_threshold_subset_cases':5*(1 << 12), 'monotone_subset_implications':implications,
            'trivial_legal1_cases':legal1, 'trivial_zero_cases':zero}


def literal_cuts(fibers, D):
    progressions = {d:[{y for y in range(315) if y % d == a} for a in range(d)] for d in D}
    singles = []; pairs = []
    for H in fibers:
        singles.append([1 << D.index(d) for d in D if any(H <= C for C in progressions[d])])
        pairs.append([(1 << D.index(d)) | (1 << D.index(e)) for d,e in combinations(D,2)
                      if any(H <= C | E for C in progressions[d] for E in progressions[e])])
    low2 = low3 = 10**9
    for B in range(1 << len(D)):
        legal = ((1 << len(D))-1) ^ B
        Q1 = sum(any(s & legal == s for s in S) for S in singles)
        Q2 = sum(any(s & legal == s for s in S) or any(t & legal == t for t in T)
                 for S,T in zip(singles,pairs))
        # Empty sets use zero classes even when no labels remain legal.
        for i,H in enumerate(fibers):
            if not H:
                if not any(s & legal == s for s in singles[i]):Q1 += 1
                if not (any(s & legal == s for s in singles[i]) or
                        any(t & legal == t for t in pairs[i])):Q2 += 1
        low2 = min(low2,8*Q1+3*B.bit_count())
        low3 = min(low3,24*Q2+10*B.bit_count())
    require(low2 >= 20 and low3 >= 72,'literal support cuts fail')
    return [low2,low3]


def run(fixture):
    prefix = [[8,0],[9,0],[10,1],[14,1],[12,10]]
    D = [d for d in range(1,316) if 315 % d == 0]
    base = [n for n in range(8,2521) if 2520 % n == 0 and n not in {v[0] for v in prefix}]
    require(fixture['agent']=='six-covering-3' and fixture['role']=='researcher' and
            fixture['schema']==1 and fixture['prefix']==prefix and fixture['tail_pools']==[D,D],
            'wrong declared original-resource model')
    phases = fixture['base_phases']
    require(isinstance(phases,list) and len(phases)==len(base) and all(isinstance(v,list) and
            len(v)==2 and type(v[0]) is int and type(v[1]) is int and 0 <= v[1] < v[0] for v in phases)
            and sorted(v[0] for v in phases)==base,'wrong original BASE phase inventory')
    U = {x for x in range(10080) if all(x % n != a for n,a in prefix+phases)}
    fibers = []
    for r in range(1,8):
        four = [{x % 315 for x in U if x % 32 == r+8*j} for j in range(4)]
        require(all(v==four[0] for v in four), 'wrong four physical child replication')
        fibers.append(four[0])
    require(not any(x % 8 == 0 for x in U) and len(U)==4*sum(map(len,fibers)) and
            [r for r,H in enumerate(fibers,1) if not H]==[1,3,5], 'wrong hole geometry')
    witness = fixture['five_class_ability_witness']
    require(set(witness)=={'parent','classes'} and type(witness['parent']) is int and
            witness['parent'] in (2,4,6,7),'wrong erasure parent')
    classes = witness['classes']
    require(isinstance(classes,list) and 1 <= len(classes) <= 5 and all(isinstance(v,list) and
            len(v)==2 and type(v[0]) is int and type(v[1]) is int and v[0] in D and v[0]!=1 and
            0 <= v[1] < v[0] for v in classes) and len({v[0] for v in classes})==len(classes),
            'wrong DISTINCT legal ability witness labels')
    require(all(any(y % d == a for d,a in classes) for y in fibers[witness['parent']-1]),
            'ability witness misses actual cofactor point')
    K = fixture['kernel']
    require(isinstance(K,list) and len(K)==7 and all(isinstance(H,list) and H==sorted(set(H)) and
            all(type(y) is int and 0 <= y < 315 for y in H) for H in K), 'malformed kernel')
    require([r for r,H in enumerate(K,1) if H]==[2,4,6,7] and sorted(len(H) for H in K if H)==[3,3,3,4],
            'wrong kernel support cardinalities')
    W = {x for x in range(10080) if x % 8 != 0 and x % 315 in K[x % 8-1]}
    require(W <= U and len(W)==52,'kernel is not actual52-point subset')
    require(all(len({y % d for y in H})==len(H) for H in K for d in (5,7,9)), 'rainbow condition fails')
    require(all(y % 3==2 for r in (2,6) for y in fibers[r-1]), 'wrong monochromatic parent')
    require([18,6] in phases and [36,30] in phases and all(x % 3==2 for x in range(2520)
            if x % 8 in (2,6) and all(x % n!=a for n,a in prefix+[[18,6],[36,30]])),
            'original18/36 partial-stage bridge fails')
    used = {n for n,a in prefix+phases}
    tail = [n for n in range(8,10081) if 10080 % n==0 and n not in used]
    require(tail==sorted([16*d for d in D]+[32*d for d in D]), 'wrong remaining24 ORIGINAL resources')
    def capacity(points):
        output=[]
        for n in tail:
            counts=[0]*n
            for x in points:counts[x % n]+=1
            output.append([n,max(counts)])
        return output
    SC=capacity(U);KC=capacity(W)
    require(sum(v[1] for v in KC)==51<52 and sum(v[1] for v in SC)<len(U),'no strict capacity gap')
    lower={x for x in W if x<2520}
    require(len(lower)==13,'wrong lower-period thirteen points')
    terms=[[n,a] for n in base for a in range(n) if any(x % n==a for x in lower)]
    require(not any(v in terms for v in phases),'stage meets learned kernel clause')
    # Mono mod3 makes every triple at parent2 fail the credited mixed3 test.
    require(len({y % 3 for y in fibers[1]})==1,'old12-test false-negative bridge fails')
    vectors=0
    for total in range(13):
        for a in range(total+1):
            for b in range(total-a+1):
                for c in range(total-a-b+1):
                    d=total-a-b-c;vectors+=1
                    if total:
                        M1=max(a,b,c,d);M3=max(a,c,ceil(Fraction(b,3)),ceil(Fraction(d,3)))
                        require(3*(M1+M3+10)>=4*total,'universal twelve-point lower bound fails')
    best=sorted([len({y for y in range(315) if y % d==0}) for d in D if d!=1],reverse=True)[:5]
    require(sum(best)==269<315,'q6 negative calibration fails')
    return {'agent':'six-covering-3','role':'researcher','collapse':scalar_audit(D),
            'stage_sizes':list(map(len,fibers)),'stage_physical_points':len(U),'stage_capacities':SC,
            'stage_capacity_budget':sum(v[1] for v in SC),'single_ability_witness':witness,
            'stage_all_integer_q_at_least2_passed':True,'stage_all4096_each_q2_q3_minima':literal_cuts(fibers,D),
            'kernel_sizes':list(map(len,K)),'kernel_physical_points':len(W),'kernel_capacities':KC,
            'kernel_capacity_budget':sum(v[1] for v in KC),'kernel_all_integer_q_at_least2_passed':True,
            'kernel_clause_terms':len(terms),'kernel_clause_sha256':sha256(json.dumps(terms,separators=(',',':')).encode()).hexdigest(),
            'prior12_test_passed':True,'minimality_vectors_through12':vectors,
            'abstract_full315_five_class_capacity':sum(best),'abstract_q6_B1_left_right':[83,84]}


def verify(fixture,expected):
    observed=run(fixture)
    require(observed==expected,'separate literal evidence differs')
    return observed


if __name__=='__main__':
    here=Path(__file__).resolve().parent
    print(json.dumps(verify(json.loads((here/'fixture.json').read_text()),
                            json.loads((here/'expected.json').read_text())),sort_keys=True))
