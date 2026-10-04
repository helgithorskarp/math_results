"""Exact count model for the ordinary proofs in STRUCTURAL.md/PROOF.md.

Only the 143 defining coefficients from published q17/source65580698 are
input. No endpoint factors, floors, validators or peer executable is input.
The count scale (48-k-m)/32 is an experimental comparison rule.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
import hashlib
import json
from pathlib import Path

TAU_MAX = F(219061, 3080192)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def choose(n, r):
    return comb(n, r) if 0 <= r <= n else 0


def coefficient_input(path):
    raw = Path(path).read_bytes()
    require(hashlib.sha256(raw).hexdigest() ==
            '65f2b0a5170e0a7585d4892c33d72aca7e4479d0e3484dc98ee32b0ad27f1105',
            'whole defining q17 table input')
    data = json.loads(raw)
    require((data['q'], data['k'], data['denominator'], data['free_pair_type_count']) ==
            (17, 8, 32768, 143), 'exact comparison table provenance and units')
    table = {}
    for item in data['free_pair_values']:
        key = tuple(map(tuple, item['types']))
        numerator = item['numerator']
        require(key == tuple(sorted(key)) and key not in table and
                type(numerator) is int and numerator % 31 == 0, 'exact u/1024 recovery')
        table[key] = numerator // 31
    require(len(table) == 143, 'all independent defining coefficients')
    return table


def parameters(k, m):
    require(type(k) is int and type(m) is int and k >= 4 and m >= 4, 'count domain')
    q = k + m
    N = (q*q + 13*q + 16)//2 - k
    s = 3*q + 4
    return N, s, N-s


def type_of(member, k):
    return (sum(1 << i for i in member if i < 3),
            sum(3 <= i < k+3 for i in member), sum(i >= k+3 for i in member))


def members(k, m):
    parameters(k, m)
    out = []
    for size in range(4):
        for member in combinations(range(k+m+3), size):
            if size <= 2 or (sum(i < 3 for i in member) >= 2 and
                             not (1 in member and 2 in member and
                                  any(3 <= i < k+3 for i in member))):
                out.append(member)
    return sorted(out, key=lambda a: sum(1 << i for i in a))


def types_of(table):
    out = sorted({t for pair in table for t in pair})
    require(len(out) == 22 and (0, 0, 0) not in out and (1, 0, 0) not in out,
            '22 actual residual types')
    return out


def comparison(raw_table, k, m):
    parameters(k, m)
    return {pair: F((48-k-m)*u, 32768) for pair, u in raw_table.items()}


def type_budgets(table, k, m):
    N, s, h = parameters(k, m)
    types = types_of(table)
    weights = {t: choose(k, t[1])*choose(m, t[2]) for t in types}
    nn = [t for t in types if not t[0] & 1]
    stars = [t for t in types if t[0] & 1]
    require(sum(weights.values()) == N-2 and sum(weights[t] for t in nn) == h-1 and
            sum(weights[t] for t in stars) == s-1, 'all count weights')
    ell = {}
    for t in types:
        total = F(0)
        for u in nn:
            number = 0 if t[0] & u[0] else choose(k-t[1], u[1])*choose(m-t[2], u[2])
            key = tuple(sorted((t, u)))
            require(number == 0 or key in table, 'each parametric NN disjoint pair')
            if number:
                total += number*(1+table[key])
        ell[t] = F(h if t in stars else h-s) - total
    ea = F(s)-sum(weights[t]*ell[t] for t in stars)
    e0 = F(h-s)-sum(weights[t]*ell[t] for t in nn)
    bad = [t for t in nn if ell[t] < 0]
    D = -sum(weights[t]*ell[t] for t in bad)
    return dict(k=k, m=m, N=N, s=s, h=h, types=types, weights=weights,
                ell=ell, anchor=ea, loop=e0, bad_nn=bad,
                bad_stars=[t for t in stars if ell[t] < 0], D=D, P0=(D-e0)/2)


def literal_point(table, k, m):
    N, s, h = parameters(k, m)
    all_members = members(k, m)
    require(len(all_members) == N and all_members[:2] == [(), (0,)], 'literal count/anchor')
    sets = list(map(frozenset, all_members))
    proper, pts = all_members[1:], sets[1:]
    C = []
    keys = set()
    for i, v in enumerate(proper):
        row = []
        for j, w in enumerate(proper):
            if i == j:
                val = F(s-1)
            elif not pts[i].isdisjoint(pts[j]):
                val = F(-1)
            elif i == 0 or j == 0:
                val = F(0)
            else:
                key = tuple(sorted((type_of(v, k), type_of(w, k))))
                keys.add(key)
                require(key in table, 'complete literal free key')
                val = table[key]
            row.append(val)
        C.append(row)
    require(keys == set(table), 'all143 free keys present, no unused type')
    star = [i for i, v in enumerate(proper) if 0 in v]
    for i, v in enumerate(proper):
        if 0 not in v:
            C[i][0] = C[0][i] = -sum(C[i][j] for j in star if j != 0)
    rows = list(map(sum, C))
    L = [[1+sum(rows)] + [1-a for a in rows]] + [
        [1-rows[i]] + [1+a for a in row] for i, row in enumerate(C)]
    centered = [N*int(0 in v)-s for v in all_members]
    require(all(sum(C[i][j] for j in star) == 0 for i in range(N-1)), 'literal proper star kernel')
    require(all(sum(row) == N and sum(a*b for a,b in zip(row,centered)) == 0 for row in L),
            'every original row and centered-star equation')
    require(all(L[i][j] == L[j][i] and
                (sets[i].isdisjoint(sets[j]) or L[i][j] == s*int(i == j))
                for i in range(N) for j in range(N)), 'every original support/symmetry position')
    sizes = [sum(a in v for v in all_members) for a in range(k+m+3)]
    require(sizes == [s, s-k, s-k]+[k+m+5]*k+[k+m+6]*m, 'all literal star sizes')
    return dict(N=N,s=s,h=h,members=all_members,C=C,T=[row[1:] for row in C[1:]],L=L)


def budget_record(b):
    return dict(k=b['k'],m=b['m'],N=b['N'],s=b['s'],h=b['h'],
                type_budgets=[dict(type=t,weight=b['weights'][t],ell=str(b['ell'][t])) for t in b['types']],
                anchor=str(b['anchor']),loop=str(b['loop']),bad_nn=b['bad_nn'],bad_stars=b['bad_stars'],
                bad_vertex_count=sum(b['weights'][t] for t in b['bad_nn']),D=str(b['D']),P0=str(b['P0']))


def check_literal_budgets(point, b):
    N, s = point['N'], point['s']
    require((N,s,point['h']) == (b['N'],b['s'],b['h']), 'same original parameters')
    observed = {t: [] for t in b['types']}
    for i,v in enumerate(point['members'][2:], 2):
        t = type_of(v, b['k'])
        observed[t].append(point['L'][0][i])
        require(point['L'][0][i] == b['ell'][t], 'each actual empty-row budget')
    require(all(len(observed[t]) == b['weights'][t] for t in b['types']), 'entire literal type census')
    require(point['L'][0][1] == b['anchor'] and point['L'][0][0]-s == b['loop'],
            'actual anchor and loop budgets')
    return dict(all_positions=N*N,individual_empty_budget_checks=N,
                original_L_sha256=digest([[str(a) for a in row] for row in point['L']]),
                every_original_budget_matches=True)


def q19_candidate(raw_table, tau):
    """Exact extended recipe. Its full physical proof is a separate obligation."""
    require(type(tau) is F and tau >= 0, 'nonnegative exact affine recipe parameter; feasibility separate')
    k,m = 9,10
    old = comparison(raw_table,k,m)
    b = type_budgets(old,k,m)
    require(b['bad_nn'] == [(0,0,2),(2,0,1),(4,0,1),(6,0,1)], 'fresh four bad NN types')
    yy,by,cy,bcy = (0,0,2),(2,0,1),(4,0,1),(6,0,1)
    beta = (-b['ell'][bcy]+tau)/choose(m-1,2)
    eta = (-b['ell'][by]+tau)/(m-1)
    alpha = (-b['ell'][yy]+tau-(m-2)*beta)/choose(m-2,2)
    P = b['P0']+38*tau
    changed = old.copy()
    def add(t,u,a):
        key = tuple(sorted((t,u)))
        require(key in changed, 'actual recipe coordinate')
        changed[key] += a
    add(yy,yy,-alpha)
    add(yy,bcy,-beta)
    add(by,cy,-eta)
    # Three separate positive good components with masses P/4,P/2,P/4.
    add((0,2,0),(0,2,0), P/(12*choose(k,4)))
    add((0,1,0),(0,1,0), P/(2*choose(k,2)))
    add((0,0,1),(0,0,1), P/(4*choose(m,2)))
    trades = []
    # Include aY as a source of star-empty slack for the actual anchor.
    for t in [(1,0,1),(3,0,1),(5,0,1),(7,0,0)]:
        change = (b['ell'][t]-tau)/k
        add(t,(0,1,0),change)
        trades.append(dict(type=t,total_per_vertex=str(k*change),weight=b['weights'][t]))
    # New unpenalized orbit: remove the fixed anchor/YY bottleneck.
    # Anchor completion induces C_a,YY += tau on every45 YY pair.
    add((7,0,0),yy,-tau)
    return changed,dict(tau=str(tau),alpha=str(alpha),beta=str(beta),eta=str(eta),
                        P=str(P),bad_count=75,positive_mass_shares=['1/4','1/2','1/4'],
                        star_trades=trades,extra_abc_YY_trade_per_pair=str(-tau),
                        extra_unordered_star_trades=45,entry_PSD_obligations_separate=True)


def sector_forms(table,k,m):
    """Exact block actions; their all-count completeness proof is STRUCTURAL.md."""
    N,s,h = parameters(k,m)
    types = types_of(table)
    w = [choose(k,t[1])*choose(m,t[2]) for t in types]
    r = [int(bool(t[0]&1)) for t in types]
    b = [1-a for a in r]
    H = []
    GI = []
    for i,t in enumerate(types):
        row=[];g=[]
        for j,u in enumerate(types):
            number = 0 if t[0]&u[0] else choose(k-t[1],u[1])*choose(m-t[2],u[2])
            key=tuple(sorted((t,u)))
            require(number == 0 or key in table, 'complete trivial coordinate')
            row.append(F(s*int(i==j)-w[j])+number*(1+table.get(key,0)))
            g.append(F(int(i==j))-F(r[i]*r[j]*w[j],s)-F(b[i]*b[j]*w[j],h))
        H.append(row);GI.append(g)
    trivial_lower=[[w[i]*a for a in H[i]] for i in range(22)]
    trivial_upper=[[w[i]*(N*GI[i][j]-H[i][j]) for j in range(22)] for i in range(22)]
    result={}
    for tag,matrix in [('trivial_lower',trivial_lower),('trivial_upper',trivial_upper)]:
        require(all(matrix[i][j] == matrix[j][i] for i in range(22) for j in range(22)),
                'physical weighted trivial symmetry')
        result[tag]=dict(types=types,metric=w,matrix=matrix,multiplicity=1)
    for pool in (1,2):
        dims=k if pool==1 else m
        selected=[t for t in types if t[pool]>0]
        weights=[choose(k-2,t[1]-1)*choose(m,t[2]) if pool==1 else
                 choose(k,t[1])*choose(m-2,t[2]-1) for t in selected]
        action=[]
        for i,t in enumerate(selected):
            row=[]
            for j,u in enumerate(selected):
                if t[0]&u[0]:
                    number=0
                elif pool==1:
                    number=choose(k-t[1]-1,u[1]-1)*choose(m-t[2],u[2])
                else:
                    number=choose(k-t[1],u[1])*choose(m-t[2]-1,u[2]-1)
                key=tuple(sorted((t,u)))
                require(number==0 or key in table,'complete standard coordinate')
                row.append(F(s*int(i==j))-number*(1+table.get(key,0)))
            action.append(row)
        for side in ('lower','upper'):
            matrix=[[weights[i]*(action[i][j] if side=='lower' else N*int(i==j)-action[i][j])
                     for j in range(len(selected))] for i in range(len(selected))]
            require(all(matrix[i][j]==matrix[j][i] for i in range(len(selected)) for j in range(len(selected))),
                    'physical weighted standard symmetry')
            tag=('X' if pool==1 else 'Y')+'_standard_'+side
            result[tag]=dict(types=selected,metric=weights,matrix=matrix,multiplicity=dims-1)
    for name,t,dimension in [('XX_harmonic',(0,2,0),k*(k-3)//2),
                              ('YY_harmonic',(0,0,2),m*(m-3)//2),
                              ('XY_mixed',(0,1,1),(k-1)*(m-1))]:
        a=s+1+table[(t,t)]
        result[name+'_lower']=dict(types=[t],metric=[1],matrix=[[a]],multiplicity=dimension)
        result[name+'_upper']=dict(types=[t],metric=[1],matrix=[[N-a]],multiplicity=dimension)
    require(sum(result[tag]['multiplicity']*len(result[tag]['types']) for tag in result if tag.endswith('lower'))==N-2,
            'all proposed sector dimensions')
    return result


def exact_ldl(matrix,metric,margin):
    """Fresh exact pivots, with a complete rational negative-vector control."""
    require(type(margin) is F and margin>=0,'exact margin')
    n=len(matrix)
    require(len(metric)==n and all(len(row)==n for row in matrix) and
            all(type(a) in (int,F) for row in matrix for a in row) and
            all(type(a) in (int,F) and a>0 for a in metric) and
            all(matrix[i][j]==matrix[j][i] for i in range(n) for j in range(n)),
            'ENTIRE exact symmetric form and positive physical metric domain')
    A=[[F(matrix[i][j])-margin*metric[i]*int(i==j) for j in range(n)] for i in range(n)]
    L=[[F(int(i==j)) for j in range(n)] for i in range(n)]
    D=[]
    for j in range(n):
        pivot=A[j][j]-sum(L[j][a]**2*D[a] for a in range(j))
        D.append(pivot)
        if pivot<=0:
            v=[F(0)]*n;v[j]=F(1)
            for i in range(j-1,-1,-1):
                v[i]=-sum(L[a][i]*v[a] for a in range(i+1,j+1))
            value=sum(v[i]*A[i][a]*v[a] for i in range(n) for a in range(n))
            require(value==pivot,'entire physical block witness quadratic')
            return dict(positive_definite=False,dimension=n,margin=str(margin),
                        pivots=[str(a) for a in D],failed_pivot=j,
                        witness=[str(a) for a in v],witness_quadratic=str(value))
        for i in range(j+1,n):
            L[i][j]=(A[i][j]-sum(L[i][a]*L[j][a]*D[a] for a in range(j)))/pivot
    require(all(sum(L[i][a]*D[a]*L[j][a] for a in range(n))==A[i][j]
                for i in range(n) for j in range(n)),'ENTIRE fresh LDL identity')
    return dict(positive_definite=True,dimension=n,margin=str(margin),
                pivots=[str(a) for a in D],factor_sha256=digest([[str(a) for a in row] for row in L]),
                matrix_sha256=digest([[str(a) for a in row] for row in A]),
                all_factor_positions=n*n)
