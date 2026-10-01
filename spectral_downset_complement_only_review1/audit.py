#!/usr/bin/env python3
"""Independent literal-set audit; no campaign code or author input imports."""
import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def mv(a, x):
    return [dot(row, x) for row in a]


def quadratic(a, x):
    return dot(x, mv(a, x))


def inertia(matrix):
    """Exact symmetric congruence, including indefinite 2x2 pivots."""
    a = [[F(x) for x in row] for row in matrix]
    n = len(a)
    require(all(len(row) == n for row in a), 'not square')
    require(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)),
            'not symmetric')
    positive = negative = zero = 0
    while a:
        m = len(a)
        k = next((i for i in range(m) if a[i][i]), None)
        if k is not None:
            order = [k] + [i for i in range(m) if i != k]
            a = [[a[i][j] for j in order] for i in order]
            pivot = a[0][0]
            positive += pivot > 0
            negative += pivot < 0
            a = [[a[i][j] - a[i][0]*a[0][j]/pivot
                  for j in range(1, m)] for i in range(1, m)]
        else:
            pair = next(((i, j) for i in range(m) for j in range(i)
                         if a[i][j]), None)
            if pair is None:
                zero += m
                break
            i, j = pair
            order = [i, j] + [k for k in range(m) if k not in pair]
            a = [[a[i][j] for j in order] for i in order]
            pivot = a[0][1]
            positive += 1
            negative += 1
            a = [[a[i][j] - (a[i][0]*a[1][j]+a[i][1]*a[0][j])/pivot
                  for j in range(2, m)] for i in range(2, m)]
    return [positive, negative, zero]


def determinant(a):
    # Tiny permutation definition, used only in independent backend controls.
    n = len(a)
    total = 0
    for p in itertools.permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i+1, n))
        term = (-1)**inversions
        for i, j in enumerate(p):
            term *= a[i][j]
        total += term
    return total


def controls():
    count = psd = 0
    for entries in itertools.product([-1, 0, 1], repeat=6):
        a, b, c, d, e, f = entries
        m = [[a,b,c],[b,d,e],[c,e,f]]
        principals = [determinant([[m[i][j] for j in s] for i in s])
                      for k in [1,2,3] for s in itertools.combinations(range(3), k)]
        signature = inertia(m)
        require((signature[1] == 0) == all(x >= 0 for x in principals),
                'principal-minor mismatch')
        require((signature[0] == 0) == all((-1)**len(s)*determinant(
            [[m[i][j] for j in s] for i in s]) >= 0
            for k in [1,2,3] for s in itertools.combinations(range(3), k)),
            'negative principal-minor mismatch')
        count += 1
        psd += signature[1] == 0
    require(inertia([[0,2],[2,0]]) == [1,1,0], '2x2 pivot failure')
    rejected = 0
    for malformed in [[[1,2]], [[1,0],[1,1]]]:
        try:
            inertia(malformed)
        except ValueError:
            rejected += 1
    require(rejected == 2, 'malformed acceptance')
    return {'ternary_symmetric_matrices': count, 'psd': psd,
            'malformed_rejections': rejected, 'off_diagonal_pivot': True}


def data(n):
    # Tuples and literal set intersections; no bit-mask incidence representation.
    ground = tuple(range(n, 0, -1))
    singles = [frozenset([i]) for i in ground]
    middle = [frozenset(c) for k in range(n-2, 1, -1)
              for c in itertools.combinations(ground, k)]
    universe = frozenset(ground)
    pairs = []
    seen = set()
    for a in middle:
        if a not in seen:
            b = universe-a
            pairs.append((a,b))
            seen.update([a,b])
    vertices = [frozenset()] + singles + middle
    N = len(vertices)
    s = sum(ground[0] in a for a in vertices)
    require(len(pairs)+1 == s and N == n+2*len(pairs)+1, 'counts')
    index = {a:i for i,a in enumerate(vertices)}
    # Full lift columns E[-R;I], derived directly from centered-star equations.
    columns = [[len(a)-1] + [-int(i in a) for i in ground]
               + [int(a == b) for b in middle] for a in middle]
    rows = [list(r) for r in zip(*columns)]
    return {'n':n, 'ground':ground, 'middle':middle, 'pairs':pairs,
            'vertices':vertices,'index':index,'N':N,'s':s,'columns':columns,
            'rows':rows}


def lift(d, q):
    rows = d['rows']
    qr = [mv(q, r) for r in rows]
    return [[1+dot(rows[i], qr[j]) for j in range(d['N'])]
            for i in range(d['N'])]


def base_lift(d):
    rows = d['rows']
    sums = [sum(r) for r in rows]
    return [[1+d['s']*dot(a,b)-sums[i]*sums[j]
             for j,b in enumerate(rows)] for i,a in enumerate(rows)]


def face_check(n):
    d = data(n)
    vertices = d['vertices']
    N,s = d['N'], d['s']
    m = len(d['middle'])
    l = base_lift(d)
    require(all(sum(row) == N for row in l), 'base row sums')
    require(all(l[i][j] == s*int(i==j) for i,a in enumerate(vertices)
                for j,b in enumerate(vertices) if a & b), 'base support')
    stars = [[F(int(g in a))-F(s,N) for a in vertices] for g in d['ground']]
    require(all(mv(l,x) == [0]*N for x in stars), 'base star kernel')
    w = [F({0:0,1:1,2:F(4,5),3:1,4:F(2,3)}[len(a)]) for a in vertices] if n==6 else None
    u = [F(int(2 <= len(a) <= 4))-F(50,57) for a in vertices] if n==6 else None
    constant = None
    if n == 6:
        constant = N*dot(w,w)-quadratic(l,w)+4*quadratic(l,u)
        require(constant == F(-86,15), 'dual constant')
    histogram = {}
    for i,a in enumerate(d['middle']):
        for j,b in enumerate(d['middle'][:i]):
            if a & b:
                continue
            ca,cb = d['columns'][i], d['columns'][j]
            # Each basis direction changes exactly one free middle entry.
            require(sum(ca) == sum(cb) == 0, 'basis row sum')
            require(all(dot(x,ca) == dot(x,cb) == 0 for x in stars), 'basis star')
            require(all(ca[r]*cb[t]+cb[r]*ca[t] == 0
                        for r,A in enumerate(vertices) for t,B in enumerate(vertices)
                        if A & B), 'basis support')
            require(ca[d['index'][a]]*cb[d['index'][b]] == 1, 'free-coordinate bridge')
            typ = tuple(sorted([len(a),len(b)]))
            key = '/'.join(map(str,typ))
            histogram[key] = histogram.get(key,0)+1
            if n==6:
                coefficient = -2*dot(w,ca)*dot(w,cb)+8*dot(u,ca)*dot(u,cb)
                expected = {(2,2):F(128,25),(2,3):F(16,5),
                            (2,4):F(0),(3,3):F(0)}[typ]
                require(coefficient == expected, 'dual free coefficient')
    require(len(stars) == n, 'stars')
    return {'n':n,'N':N,'middle':m,'free_directions':sum(histogram.values()),
            'edge_types':histogram,'dual_constant':str(constant) if constant else None}


def weighted_lift(d, weights):
    require(len(weights) == len(d['pairs']), 'parameter count')
    # Q=sI-J plus disjoint complement updates. Use the sparse full lift
    # columns directly, avoiding cubic dense Fraction products.
    l=base_lift(d)
    middle_index={a:i for i,a in enumerate(d['middle'])}
    for (a,b),z in zip(d['pairs'],weights):
        ca=d['columns'][middle_index[a]]
        cb=d['columns'][middle_index[b]]
        support_a=[(i,x) for i,x in enumerate(ca) if x]
        support_b=[(i,x) for i,x in enumerate(cb) if x]
        coefficient=d['s']-z
        for i,x in support_a:
            for j,y in support_b:
                term=coefficient*x*y
                l[i][j]+=term
                l[j][i]+=term
    return l


def literal_architecture(d, weights):
    vertices = d['vertices']
    s,N = d['s'],d['N']
    pair_weight = {a:z for pair,z in zip(d['pairs'],weights) for a in pair}
    k = [[F(0) for _ in vertices[1:]] for _ in vertices[1:]]
    universe = frozenset(d['ground'])
    for i,a in enumerate(vertices[1:]):
        for j,b in enumerate(vertices[1:]):
            if i==j:
                k[i][j] = s
            elif len(a) == len(b) == 1:
                g,h = next(iter(a)),next(iter(b))
                k[i][j] = s-sum(z for (x,y),z in zip(d['pairs'],weights)
                                 if (g in x) != (h in x))
            elif len(a)==1 or len(b)==1:
                singleton,mid = (a,b) if len(a)==1 else (b,a)
                k[i][j] = 0 if singleton & mid else pair_weight[mid]
            elif a|b == universe and not a&b:
                k[i][j] = s-pair_weight[a]
    # Row sums alone recover every empty entry, including the loop.
    empty = [N-sum(row) for row in k]
    return [[N-sum(empty)] + empty] + [[empty[i]]+row for i,row in enumerate(k)]


def weighted_check(n, label, weights, full_inertia=True):
    d=data(n)
    N,s,p = d['N'],d['s'],len(d['pairs'])
    weights=list(map(F,weights))
    l=weighted_lift(d,weights)
    require(l == literal_architecture(d,weights), 'independent constructors differ')
    require(all(sum(row)==N for row in l), 'weighted row sums')
    vertices=d['vertices']
    require(all(l[i][j]==s*int(i==j) for i,a in enumerate(vertices)
                for j,b in enumerate(vertices) if a&b), 'weighted support')
    # Literal middle pair congruence gives complete lower inertia.
    G=[[((2*s-weights[i]) if i==j else 0)-2 for j in range(p)] for i in range(p)]
    lower=inertia(G)
    zsignature=[sum(z>0 for z in weights),sum(z<0 for z in weights),sum(z==0 for z in weights)]
    predicted=[1+lower[0]+zsignature[0],lower[1]+zsignature[1],n+lower[2]+zsignature[2]]
    actual=inertia(l) if full_inertia else predicted
    require(actual==predicted, 'lower full inertia')
    # Direct sum/difference congruence of the literal middle principal block.
    for r,(a,b) in enumerate(d['pairs']):
        ia,ib=d['index'][a],d['index'][b]
        for t,(c,e) in enumerate(d['pairs']):
            ic,ie=d['index'][c],d['index'][e]
            aa,ab,ba,bb=(l[ia][ic]-1,l[ia][ie]-1,
                         l[ib][ic]-1,l[ib][ie]-1)
            require(aa+ab+ba+bb==2*G[r][t], 'symmetric pair congruence')
            require(aa-ab-ba+bb==2*weights[r]*int(r==t), 'antisymmetric pair congruence')
            require(aa+ab-ba-bb==0, 'pair parity cross term')
    denominators=[2*s-z for z in weights]
    domain=all(0<=z<=s for z in weights) and 2*sum(1/d for d in denominators)<=1
    require(domain == (actual[1]==0), 'PSD domain')
    if domain:
        delta=int(2*sum(1/d for d in denominators)==1)
        require(actual[2]==n+sum(z==0 for z in weights)+delta, 'rank strata')
        kernel=[[F(int(g in a))-F(s,N) for a in vertices] for g in d['ground']]
        for (a,b),z in zip(d['pairs'],weights):
            if not z:
                kernel.append([F(int(c==a)-int(c==b)) for c in vertices])
        if delta:
            extra=[F(0)]*N
            for (a,b),den in zip(d['pairs'],denominators):
                extra[d['index'][a]]=extra[d['index'][b]]=1/den
            mean=sum(extra)/N
            kernel.append([x-mean for x in extra])
        require(len(kernel)==actual[2] and all(mv(l,x)==[0]*N for x in kernel),
                'explicit complete lower kernel')
    # Build the upper core independently, eliminate literal pair blocks.
    k=[row[1:] for row in l[1:]]
    V=[[N*int(i==j)-k[i][j] for j in range(N-1)] for i in range(N-1)]
    midindex={a:i for i,a in enumerate(vertices[1:])}
    W=[[F(V[i][j]) for j in range(n)] for i in range(n)]
    require(all(V[midindex[a]][midindex[b]]==0 for pa in d['pairs']
                for pb in d['pairs'] if pa!=pb for a in pa for b in pb),
            'upper middle cross blocks')
    for (a,b),z in zip(d['pairs'],weights):
        ia,ib=midindex[a],midindex[b]
        sum_pivot=V[ia][ia]+V[ib][ib]+2*V[ia][ib]
        diff_pivot=V[ia][ia]+V[ib][ib]-2*V[ia][ib]
        require(sum_pivot==2*(n-1+z) and diff_pivot==2*(N-z), 'pair pivots')
        require(sum_pivot>0 and diff_pivot>0, 'positive elimination domain')
        bsum=[V[i][ia]+V[i][ib] for i in range(n)]
        bdiff=[V[i][ia]-V[i][ib] for i in range(n)]
        for i in range(n):
            for j in range(n):
                W[i][j]-=bsum[i]*bsum[j]/sum_pivot+bdiff[i]*bdiff[j]/diff_pivot
    B=s-F(n-1,2)*sum(z/(n-1+z) for z in weights)
    orientations=[[2*int(g in a)-1 for a,b in d['pairs']] for g in d['ground']]
    formula=[[N*int(i==j)-F(N,2)*sum(orientations[i][r]*orientations[j][r]*z/(N-z)
              for r,z in enumerate(weights))-B for j in range(n)] for i in range(n)]
    require(W==formula, 'upper Schur formula')
    upper=inertia(W)
    if full_inertia:
        full_upper=inertia([[N*int(i==j)-l[i][j] for j in range(N)] for i in range(N)])
        require(full_upper==[2*p+upper[0],upper[1],1+upper[2]], 'upper full inertia')
    else:
        full_upper=[2*p+upper[0],upper[1],1+upper[2]]
    return {'n':n,'label':label,'weights_sha256':hashlib.sha256(
        json.dumps(list(map(str,weights))).encode()).hexdigest(),
        'lower_inertia':actual,'ordinary_H':domain,'upper_inertia':full_upper,
        'capped':domain and upper[1]==0,'unit_multiplicity':1+upper[2],
        'explicit_lower_kernel_checked':domain,'literal_pair_congruence_checked':True,
        'full_inertia_checked':full_inertia}


def projection_check():
    d=data(6)
    vertices=d['vertices']
    N,s=d['N'],d['s']
    ones=[F(1)]*N
    stars=[[F(int(i in a))-F(s,N) for a in vertices] for i in d['ground']]
    gram=[[dot(a,b) for b in stars] for a in stars]
    require(gram==[[F(806 if i==j else -49,57) for j in range(6)]
                   for i in range(6)], 'literal star Gram')
    w=[F({0:0,1:1,2:F(4,5),3:1,4:F(2,3)}[len(a)]) for a in vertices]
    u=[F(int(2<=len(a)<=4))-F(50,57) for a in vertices]
    require(all(dot(w,x)==F(-13,57) and dot(u,x)==F(125,57) for x in stars),
            'projection inner products')
    star_total=[sum(x[i] for x in stars) for i in range(N)]
    p_w=[-F(13,561)*x for x in star_total]
    p_u=[F(125,561)*x for x in star_total]
    v=[w[i]-F(48,57)-p_w[i] for i in range(N)]
    u0=[u[i]-p_u[i] for i in range(N)]
    require(all(dot(x,ones)==0 and all(dot(x,y)==0 for y in stars)
                for x in [v,u0]), 'projection residual')
    pw2=dot(p_w,p_w)
    v2,u2,c=dot(v,v),dot(u0,u0),dot(v,u0)
    require((pw2,v2,u2,c)==(F(338,10659),F(1696,935),F(600,187),F(112,561)),
            'projection norms')
    total=v2+4*u2
    lower=F(25,496)*(F(86,15)+N*pw2+N*4*c*c/total)
    require(lower==F(510305,1240558) and lower>F(2,5)>F(215,744), 'strengthening')
    # Rank-two eigenvalue identity underlying the sharp relaxed lower bound.
    trace=4*u2-v2
    det=-4*(u2*v2-c*c)
    require(trace**2-4*det==total**2-16*c*c and det<0, 'rank-two discriminant')
    require(total**2-16*c*c>0, 'radical domain')
    return {'star_projection_norm2':str(pw2),'v_norm2':str(v2),
            'u0_norm2':str(u2),'inner_product':str(c),'S':str(total),
            'rational_orbit_bound':str(lower),'excess_over_two_fifths':str(lower-F(2,5)),
            'relaxed_radical_discriminant':str(total**2-16*c*c),
            'projection_residual_checks':True}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    result={'method':'literal tuple-set face/lift; exact rational symmetric congruence; independent projected dual',
            'backend_controls':controls(),
            'full_affine_faces':[face_check(n) for n in [4,5,6]],
            'projection':projection_check(),'weighted_cases':[]}
    for n in [4,5,6,7]:
        p=2**(n-1)-n-1
        s=p+1
        cases=[('partition',[0]*p),('barycenter',[1]*p),('all_two',[2]*p),
               ('one_flip',[s]+[0]*(p-1)),('one_half_flip',[F(s,2)]+[0]*(p-1)),
               ('asymmetric_interior',[F(1)+F(i%3,2*p) for i in range(p)])]
        if n==4:
            cases.append(('asymmetric_cap',[F(3,2),F(8,5),F(7,5)]))
        if n==5:
            cases.append(('asymmetric_cap',[F(19,10)+F((i%3)-1,100) for i in range(p)]))
        for label,weights in cases:
            record=weighted_check(n,label,weights,full_inertia=(n<=6))
            if label=='asymmetric_cap':require(record['capped'],'small asymmetric cap')
            if n==6:require(not record['capped'],'six-point complement-only cap')
            result['weighted_cases'].append(record)
    # Extra singular and invalid sign strata at a small order.
    for label, weights, wanted in [('negative',[-1,0,0],False),
                                  ('reciprocal_failure',[3,3,3],False),
                                  ('domain_failure',[5,0,0],False),
                                  ('mixed_zero',[0,1,2],True)]:
        record=weighted_check(4,label,weights)
        require(record['ordinary_H']==wanted,'domain control verdict')
        result['weighted_cases'].append(record)
    result['weighted_cases_count']=len(result['weighted_cases'])
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    with open(args.output,'w') as stream:
        stream.write(text)
    print(json.dumps({'weighted_cases':len(result['weighted_cases']),
                      'affine_free_directions':sum(x['free_directions'] for x in result['full_affine_faces']),
                      'orbit_bound':result['projection']['rational_orbit_bound'],
                      'sha256':hashlib.sha256(text.encode()).hexdigest()},sort_keys=True))


if __name__=='__main__':
    main()
