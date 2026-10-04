"""Fresh literal maximum-star envelope audit; standard library, exact arithmetic.

No author executable, EXPECTED file or envelope weights are read. The written
target proof and prior seed audit are exposed. The seed positivity is a premise.
"""
import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def outer_add(matrix, u, v, coefficient=1):
    for i, a in u.items():
        for j, b in v.items():
            matrix[i][j] += coefficient * a * b
            matrix[j][i] += coefficient * a * b


def sparse_basis(u, v):
    out = Counter()
    for i, a in u.items():
        for j, b in v.items():
            out[i, j] += a * b
            out[j, i] += a * b
    return {ij: x for ij, x in out.items() if x}


def coordinates(members, n):
    require(members[0] == 0, 'actual empty member')
    require(all((b ^ (1 << i)) in members for b in members
                for i in range(n) if b >> i & 1), 'downward closure')
    require(all((1 << i) in members for i in range(n)), 'active ground')
    sizes = [sum(bool(b >> i & 1) for b in members) for i in range(n)]
    s = max(sizes)
    maximum = [i for i, count in enumerate(sizes) if count == s]
    anchors = [1 << i for i in maximum]
    residual = [b for b in members if b and b not in anchors]
    proper = anchors + residual
    original = [0] + proper
    pos = {b: j for j, b in enumerate(proper)}
    f = []
    a = []
    for b in residual:
        u = {pos[b]: 1}
        u.update({j: -1 for j, i in enumerate(maximum) if b >> i & 1})
        f.append(u)
        lifted = {j + 1: x for j, x in u.items()}
        empty = -sum(u.values())
        if empty:
            lifted[0] = empty
        a.append(lifted)
    return dict(members=members, original=original, proper=proper,
                residual=residual, maximum=maximum, sizes=sizes, s=s,
                h=len(members)-s, f=f, a=a)


def edges_for(c, frozen=()):
    return [(i, j) for i, b in enumerate(c['residual'])
            for j in range(i + 1, len(c['residual']))
            if not b & c['residual'][j] and b not in frozen
            and c['residual'][j] not in frozen]


def envelope(c, edges, damage=None):
    size = len(c['proper'])
    p = [[0] * size for _ in range(size)]
    corner = [[0] * size for _ in range(size)]
    sign = [-1 if i < len(c['maximum']) else 1 for i in range(size)]
    if damage == 'anchor-sign':
        sign[0] = 1
    checked = 0
    for i, j in edges:
        u, v = c['f'][i], c['f'][j]
        outer_add(corner, u, v)
        outer_add(p, {k: abs(x) for k, x in u.items()},
                  {k: abs(x) for k, x in v.items()})
        block = sparse_basis(u, v)
        for (row, col), x in block.items():
            require(sign[row] * sign[col] * x >= 0, 'common sign conjugation')
            require(row != col and not c['proper'][row] & c['proper'][col],
                    'proper basis support')
        for mark in c['maximum']:
            action = Counter()
            for (row, col), x in block.items():
                if c['proper'][col] >> mark & 1:
                    action[row] += x
            require(all(x == 0 for x in action.values()), 'all proper star actions')
        require(block.get((len(c['maximum'])+i, len(c['maximum'])+j)) == 1,
                'independent residual pivot')
        # The literal empty lift is checked separately, never replaced by F.
        lifted = sparse_basis(c['a'][i], c['a'][j])
        rows = Counter()
        for (row, col), x in lifted.items():
            rows[row] += x
            require(not c['original'][row] & c['original'][col],
                    'full original support')
        require(all(x == 0 for x in rows.values()), 'full original row sums')
        for mark in c['maximum']:
            action = Counter()
            for (row, col), x in lifted.items():
                if c['original'][col] >> mark & 1:
                    action[row] += x
            require(all(x == 0 for x in action.values()), 'full original star actions')
        checked += len(lifted)
    for i in range(size):
        for j in range(size):
            require(sign[i] * sign[j] * corner[i][j] == p[i][j],
                    'entire corner/envelope congruence')
            require(p[i][j] >= 0 and p[i][j] == p[j][i], 'nonnegative symmetric P')
    return p, corner, checked


def solve(matrix, rhs):
    rows = [[Q(x) for x in row] + [Q(b)] for row, b in zip(matrix, rhs)]
    size = len(rows)
    for j in range(size):
        pivot = next((i for i in range(j, size) if rows[i][j]), None)
        require(pivot is not None, 'nonsingular resolvent')
        rows[j], rows[pivot] = rows[pivot], rows[j]
        divisor = rows[j][j]
        rows[j] = [x / divisor for x in rows[j]]
        for i in range(size):
            if i != j and rows[i][j]:
                multiplier = rows[i][j]
                rows[i] = [x - multiplier * y for x, y in zip(rows[i], rows[j])]
    return [row[-1] for row in rows]


def partition(p):
    """Canonical row-sum refinement; proposals checked in the literal space."""
    colors = [0] * len(p)
    stages = []
    while True:
        count = max(colors) + 1
        signatures = []
        for i, row in enumerate(p):
            sums = [0] * count
            for j, x in enumerate(row):
                sums[colors[j]] += x
            signatures.append((colors[i], *sums))
        keys = sorted(set(signatures))
        encoding = {key: i for i, key in enumerate(keys)}
        updated = [encoding[key] for key in signatures]
        stages.append(len(keys))
        if updated == colors:
            break
        require(len(stages) <= len(p) + 1, 'finite partition refinement')
        colors = updated
    cells = [[i for i, col in enumerate(colors) if col == k]
             for k in range(max(colors)+1)]
    quotient = [[sum(p[cell[0]][j] for j in other) for other in cells]
                for cell in cells]
    for cell, row in zip(cells, quotient):
        for i in cell:
            require([sum(p[i][j] for j in other) for other in cells] == row,
                    'literal row-sum proposals')
    return cells, quotient, stages


def q16(damage=None):
    # Two structurally different complete generators, with no input data.
    members = [b for b in range(1 << 19)
               if b.bit_count() <= 2 or
               (b.bit_count() == 3 and (b & 7).bit_count() >= 2 and
                not (b & 7 == 6 and b & ((1 << 11) - 8)))]
    union = {0}
    for size in [1, 2]:
        union.update(sum(1 << i for i in ids)
                     for ids in itertools.combinations(range(19), size))
    for x, y, z in itertools.combinations(range(19), 3):
        if sum(i < 3 for i in (x, y, z)) >= 2:
            if not (x == 1 and y == 2 and 3 <= z <= 10):
                union.add((1 << x) | (1 << y) | (1 << z))
    require(members == sorted(union), 'two complete literal carrier generators')
    c = coordinates(members, 19)
    require(c['sizes'] == [52,44,44]+[21]*8+[22]*8 and c['maximum'] == [0],
            'every star count and unique maximum')
    free = edges_for(c)
    require(len(free) == 20103, 'whole free coordinate set')
    used = free[:-1] if damage == 'missing-edge' else free
    p, corner, positions = envelope(c, used, damage)
    size = len(c['proper'])
    # Independently construct the one-star block envelope directly from sets.
    star = [i for i,b in enumerate(c['proper']) if b & 1 and b != 1]
    nonstar = [i for i,b in enumerate(c['proper']) if not b & 1]
    literal = [[0]*size for _ in range(size)]
    neighbours = []
    for i in nonstar:
        degree = sum(not c['proper'][i] & c['proper'][j] for j in star)
        neighbours.append(degree)
        literal[0][i] = literal[i][0] = degree
    for i in range(1,size):
        for j in range(i+1,size):
            if not c['proper'][i] & c['proper'][j]:
                literal[i][j] = literal[j][i] = 1
    require(p == literal, 'basis sum equals independent entire block P')
    require(sum(x*x for x in neighbours) == 314850, 'literal anchor squares')
    require(sum(x*x for row in p for x in row) == 669906, 'sharp Frobenius comparison')
    cells, quotient, stages = partition(p)
    resolvent = [[(641 if i==j else 0)-x for j,x in enumerate(row)]
                 for i,row in enumerate(quotient)]
    proposal = solve(resolvent, [1]*len(cells))
    v = [None]*size
    for cell, x in zip(cells, proposal):
        for i in cell:
            v[i] = x
    if damage == 'vector-row':
        v[0] += 1
    if damage == 'nonpositive-vector':
        v[0] = 0
    require(all(x > 0 for x in v), 'strictly positive original vector')
    pv = [sum(Q(x)*y for x,y in zip(row,v)) for row in p]
    bound = 640 if damage == 'false-upper-640' else 641
    slack = [bound*x-y for x,y in zip(v,pv)]
    require(all(x == 1 for x in slack), 'every literal original resolvent row')
    denominator = sum(x*x for x in v)
    rayleigh = sum(x*y for x,y in zip(v,pv))/denominator
    lower = 641 if damage == 'false-lower-641' else 640
    require(rayleigh > lower, 'full original Rayleigh lower bound')
    refined_upper = max(y/x for x,y in zip(v,pv))
    require(rayleigh <= refined_upper < 641, 'exact two-sided vector enclosure')
    # Literal full A corner: its empty loop proves the proper budget is NOT
    # a bound on the norm of the original N-by-N repair.
    empty_loop = sum(2*c['a'][i].get(0,0)*c['a'][j].get(0,0) for i,j in free)
    if damage == 'wrong-empty':
        empty_loop += 1
    require(empty_loop == 2*sum(not c['residual'][i]&1 and not c['residual'][j]&1 for i,j in free), 'literal original empty loop')
    require(empty_loop > 641,
            'actual empty lift has a distinct operator budget')
    r = [bool(b&1) for b in c['residual']]
    b = [not x for x in r]
    sizeq = len(r)
    g = [[int(i==j)+int(r[i] and r[j])+int(b[i] and b[j])
          for j in range(sizeq)] for i in range(sizeq)]
    inv = [[Q(i==j)-Q(int(r[i] and r[j]),52)-
            Q(int(b[i] and b[j]),180) for j in range(sizeq)]
           for i in range(sizeq)]
    if damage == 'omit-empty-metric':
        g[0][0] -= int(b[0])
    # Gram binding by sparse original columns on every entry, plus inverse
    # using the exact rank-two product formula on every entry.
    rsum = [sum(inv[k][j] for k in range(sizeq) if r[k]) for j in range(sizeq)]
    bsum = [sum(inv[k][j] for k in range(sizeq) if b[k]) for j in range(sizeq)]
    for i in range(sizeq):
        for j in range(sizeq):
            dot = sum(x*c['a'][j].get(k,0) for k,x in c['a'][i].items())
            require(g[i][j] == dot, 'entire actual original Gram')
            product = inv[i][j]+int(r[i])*rsum[j]+int(b[i])*bsum[j]
            require(product == int(i==j), 'every inverse position')
    radius = Q(1,164096)
    mu = Q(1,128)
    if damage == 'wrong-core-floor':
        mu /= 2
    require(641*radius == mu/2 == Q(1,256), 'explicit proper seed gap units')
    require(Q(1,256)/180 == Q(1,46080), 'physical M gap conversion')
    difference = Q(583,1024)-Q(1,105)-radius
    require(difference > Q(1,2), 'credited sparse entry comparison')
    return dict(N=len(members),s=c['s'],h=c['h'],proper=size,
                free_coordinates=len(free),original_basis_positions=positions,
                gram_positions=sizeq**2,corner_positions=size**2,
                neighbour_histogram=sorted(Counter(neighbours).items()),
                equitable_cell_sizes=[len(cell) for cell in cells],
                refinement_counts=stages, vector=[str(x) for x in proposal],
                literal_rows_checked=size, resolvent_slack='1',
                rayleigh=str(rayleigh), refined_upper=str(refined_upper),
                original_empty_corner_diagonal=empty_loop,
                radius=str(radius),both_core_and_original_floors='1/256',
                both_M_gaps='1/46080',sparse_entry_distance=str(difference))


def small_cases(damage=None):
    totals = Counter()
    records = []
    for n in range(1,5):
        # All 2^(2^n) indicator strings: exhaustive only for n<=4.
        for code in range(1 << (1 << n)):
            members = [b for b in range(1<<n) if code >> b & 1]
            if not members or members[0] != 0 or any((1<<i) not in members for i in range(n)):
                continue
            if any((b^(1<<i)) not in members for b in members for i in range(n) if b>>i&1):
                continue
            c = coordinates(members,n)
            pairs = [(b, ((1<<n)-1)^b) for b in members if b and
                     b < (((1<<n)-1)^b) and (((1<<n)-1)^b) in members
                     and b in c['residual'] and (((1<<n)-1)^b) in c['residual']]
            selections = [()] + [(pair,) for pair in pairs]
            if len(pairs) > 1:
                selections.append(tuple(pairs))
            for selected in selections:
                frozen = {b for pair in selected for b in pair}
                require(all(b in c['residual'] for b in frozen), 'selected endpoints retained')
                edges = edges_for(c,frozen)
                p, corner, count = envelope(c,edges)
                if damage == 'multi-star-sign' and len(c['maximum'])>1 and edges:
                    i,j=edges[0]
                    sign=[-1 if k==0 else 1 for k in range(len(c['proper']))]
                    block=sparse_basis(c['f'][i],c['f'][j])
                    require(all(sign[a]*sign[b]*x>=0 for (a,b),x in block.items()),
                            'all maximum singleton signs needed')
                for b in frozen:
                    col=c['proper'].index(b)
                    require(all(row[col]==0 for row in corner),'frozen actual columns')
                if damage == 'frozen-endpoints' and selected and edges:
                    allp,allcorner,_=envelope(c,edges_for(c))
                    require(all(allcorner[c['proper'].index(b)][j]==0 for b in frozen
                                for j in range(len(c['proper']))),'cannot reopen saturated endpoints')
                # Exhaustive real-cube corners only in small dimensions. The
                # continuum and eigenvalue theorem is the written proof.
                if len(edges)<=7:
                    for signs in itertools.product((-1,1),repeat=len(edges)):
                        matrix=[[0]*len(p) for _ in p]
                        for (i,j),x in zip(edges,signs):
                            outer_add(matrix,c['f'][i],c['f'][j],x)
                        require(all(abs(matrix[i][j])<=p[i][j]
                                    for i in range(len(p)) for j in range(len(p))),
                                'every small corner entry domination')
                        totals['exhaustive_corners']+=1
                totals['faces']+=1
                totals['basis_positions']+=count
                totals['proper_matrix_positions']+=len(p)**2
            totals['systems']+=1
            totals['multi_maximum_systems']+=len(c['maximum'])>1
            totals['empty_repair_systems']+=not edges_for(c)
            if (n==4 and len(c['maximum'])>1 and
                    any(not any(b>>i&1 for i in c['maximum']) for b in c['residual']) and
                    any(sum(b>>i&1 for i in c['maximum'])>=2 for b in c['residual'])):
                records.append(dict(members=members,maximum=c['maximum'],
                                    residual_hits=[sum(b>>i&1 for i in c['maximum']) for b in c['residual']]))
    require(records, 'mixed actual-empty sign cases tested')
    return dict(totals),records[0]


def mixed_full_case(damage=None):
    """Exact obstruction to transporting the positive corner to full A."""
    c=coordinates([0,1,2,3,4,8],4)
    require(c['maximum']==[0,1] and c['residual']==[3,4,8],
            'mixed literal two-star carrier')
    edges=edges_for(c)
    plus=[[0]*6 for _ in range(6)]
    competitor=[[0]*6 for _ in range(6)]
    for i,j in edges:
        outer_add(plus,c['a'][i],c['a'][j])
        outer_add(competitor,c['a'][i],c['a'][j],-1 if i==0 else 1)
    def product(a,b):
        return [[sum(a[i][k]*b[k][j] for k in range(6))
                 for j in range(6)] for i in range(6)]
    polynomial=[[int(i==j) for j in range(6)] for i in range(6)]
    for root in (0,-1,-5,4):
        factor=[[plus[i][j]-root*int(i==j) for j in range(6)] for i in range(6)]
        polynomial=product(polynomial,factor)
    require(all(x==0 for row in polynomial for x in row),
            'whole full-corner annihilating polynomial')
    eigenvector=[4,-2,-2,2,-1,-1]
    require(all(sum(row[j]*eigenvector[j] for j in range(6)) == -5*eigenvector[i]
                for i,row in enumerate(plus)), 'exact minus-five original eigenvector')
    if damage=='false-full-corner':
        competitor=plus
    require(competitor[0][0]==6 and plus[0][0]==-2,
            'competing corner empty Rayleigh exceeds norm five')
    return dict(members=c['members'],original_order=c['original'],
                maximum=c['maximum'],residual=c['residual'],
                plus=plus,competitor=competitor,
                plus_annihilating_roots=[0,-1,-5,4],minus_five_vector=eigenvector,
                plus_operator_norm=5,competitor_empty_Rayleigh=6)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--record',required=True)
    parser.add_argument('--damage')
    args=parser.parse_args()
    record=dict(actual_author='six-reviewer-5',role='independent mathematical reviewer',
                q16=q16(args.damage),small=small_cases(args.damage),
                mixed_full=mixed_full_case(args.damage),
                seed_status='Explicit credited 10242/10252 proper floor premise; not replayed')
    data=(json.dumps(record,sort_keys=True,indent=2)+'\n').encode()
    Path(args.record).write_bytes(data)
    print(json.dumps(dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
                         q16={k:v for k,v in record['q16'].items() if k not in ('vector','rayleigh','refined_upper')},
                         small=record['small']),sort_keys=True))


if __name__=='__main__':
    main()
