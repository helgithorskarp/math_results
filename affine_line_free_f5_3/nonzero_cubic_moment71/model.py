"""Exact moment-profile model and necessary point/line incidence inequalities."""
from collections import Counter
from itertools import product
from field import POINTS, determinant, dot, monomials, require
from quadratic import FORMS, IDENTITY, congruence, multiply

AFFINE = tuple(product(range(5), repeat=3))
ALLOWED = {0:(0,1,4), 1:(0,1,3), 4:(0,1,3), 2:(1,2,3), 3:(1,2,3)}


def quadratic_values(diagonal):
    return tuple(sum(a*x*x for a,x in zip(diagonal,v)) % 5 for v in POINTS)


def profile_deficits(q, u):
    residue = tuple((t**4+q*t*t+u) % 5 for t in range(5))
    require(u in ALLOWED[q], 'inadmissible zero-cubic moment values')
    if sum(residue) == 9:
        return (residue,)
    require(sum(residue) == 4, 'parallel residue sum')
    return tuple(tuple(r+5*int(i==j) for i,r in enumerate(residue))
                 for j in range(5))


def signature(qvalues, word):
    return tuple(sorted(Counter((0 if q == 0 else 1 if q in (1,4) else 2, int(u))
                                for q,u in zip(qvalues,word)).items()))


def feasible_memberships(profile_signature):
    """Exact necessary energy and origin-star totals, with no geometric cuts."""
    states = {(0,0)}
    for (q,u), count in profile_signature:
        options = {(sum(x*x for x in d), d[0]) for d in profile_deficits(q,u)}
        for _ in range(count):
            states = {(e+x,c+y) for e,c in states for x,y in options
                      if e+x <= 1269 and c+y <= 70}
    return tuple(eps for eps in (0,1) if (1269,70-25*eps) in states)


def isometry_generators(diagonal):
    matrices = []
    for a in POINTS:
        q = sum(c*x*x for c,x in zip(diagonal,a)) % 5
        if q:
            matrices.append(tuple(tuple((int(i==j)-2*a[i]*a[j]*diagonal[j]*pow(q,-1,5)) % 5
                                        for j in range(3)) for i in range(3)))
    if diagonal[0] == 0:
        matrices.extend((((0,1,0),(0,0,1),(1,0,0)),
                         ((1,1,0),(0,1,0),(0,0,1)),
                         ((2,0,0),(0,1,0),(0,0,1))))
    elif diagonal[1] == 0:
        matrices.extend((((1,0,0),(0,0,1),(0,1,0)),
                         ((1,0,0),(0,1,1),(0,0,1)),
                         ((1,0,0),(0,2,0),(0,0,1))))
    elif diagonal[2] == 0:
        matrices.append(((1,0,0),(0,1,0),(0,0,2)))
    form = tuple(tuple(diagonal[i] if i==j else 0 for j in range(3)) for i in range(3))
    permutations = []
    for matrix in matrices:
        require(determinant(*matrix) != 0 and congruence(form,matrix) == form,
                'valid linear isometry generator')
        permutation = []
        for p in POINTS:
            v = tuple(dot(row,p) for row in matrix)
            scalar = pow(next(x for x in v if x),-1,5)
            permutation.append(POINTS.index(tuple(scalar*x % 5 for x in v)))
        require(len(set(permutation)) == 31, 'projective permutation')
        permutations.append(tuple(permutation))
    return tuple(matrices), tuple(permutations)


def partition(diagonal, candidates, memberships, chosen, inverse):
    """Partition by a verified subgroup and audit a matrix transport for each word."""
    matrices, permutations = isometry_generators(diagonal)
    qvalues = quadratic_values(diagonal)
    monomial_table = {
        v: tuple(pow(v[0],a,5)*pow(v[1],b,5)*pow(v[2],c,5) % 5
                 for a,b,c in monomials(4)) for v in AFFINE
    }
    remaining, result = set(candidates), []
    while remaining:
        representative = min(remaining)
        transport, pending = {representative: IDENTITY}, [representative]
        while pending:
            word = pending.pop()
            for matrix, permutation in zip(matrices,permutations):
                image = ''.join(word[i] for i in permutation)
                if image not in transport:
                    require(image in candidates, 'candidate closure under isometries')
                    transport[image] = multiply(transport[word],matrix)
                    pending.append(image)
        require(set(transport) <= remaining, 'disjoint orbit partition')
        information = tuple(int(representative[i]) for i in chosen)
        coefficients = tuple(dot(row,information) for row in inverse)
        # Evaluate the original polynomial on matrix-transformed vectors;
        # this check does not compose the projective permutations.
        for word, matrix in transport.items():
            require(determinant(*matrix) != 0, 'invertible transport matrix')
            values = ''.join(str(dot(coefficients,monomial_table[
                tuple(dot(row,p) for row in matrix)])) for p in POINTS)
            require(values == word, 'independent polynomial transport audit')
        remaining.difference_update(transport)
        result.append({'representative':representative, 'size':len(transport),
                       'epsilon':list(memberships[signature(qvalues,representative)])})
    require(sum(row['size'] for row in result) == len(candidates), 'complete candidate cover')
    return result


def geometry():
    """Return sparse point stars and line pencils with deterministic indexing."""
    stars = tuple(tuple(5*j+dot(v,x) for j,v in enumerate(POINTS)) for x in AFFINE)
    lines = tuple(sorted({tuple(sorted(tuple((x[i]+t*v[i]) % 5 for i in range(3))
                                       for t in range(5)))
                          for x in AFFINE for v in POINTS}))
    require(len(lines) == 775, 'complete affine-line catalogue')
    pencils = []
    for line in lines:
        anchor = line[0]
        direction = tuple((line[1][i]-anchor[i]) % 5 for i in range(3))
        pencil = tuple(5*j+dot(v,anchor) for j,v in enumerate(POINTS)
                       if dot(v,direction) == 0)
        require(len(pencil) == 6, 'six planes in a pencil')
        require(all(all(dot(POINTS[h//5],p) == h%5 for p in line) for h in pencil),
                'direct line-plane incidence')
        pencils.append(pencil)
    return stars, lines, tuple(pencils)


def instance(diagonal, word, epsilon, incidence):
    """C z <= d, D z = 1, z >= 0; every actual candidate gives a feasible z."""
    require(epsilon in (0,1) and len(word) == 31, 'case input')
    stars, _, pencils = incidence
    qvalues = quadratic_values(diagonal)
    require(all(int(u) in ALLOWED[q] for q,u in zip(qvalues,word)), 'quartic value constraints')
    residue = tuple((t**4+q*t*t+int(u)) % 5
                    for q,u in zip(qvalues,word) for t in range(5))
    eligible = tuple(j for j in range(31) if sum(residue[5*j:5*j+5]) == 4)
    options = tuple(5*j+t for j in eligible for t in range(5))
    positions = {h:i for i,h in enumerate(options)}
    n = len(options)

    def indicator(indices, sign=1):
        row = [0]*n
        for h in indices:
            if h in positions:
                row[positions[h]] = sign
        return row

    residual_stars = [70-sum(residue[h] for h in star) for star in stars]
    residual_pencils = [sum(residue[h] for h in pencil) for pencil in pencils]
    require(all(k % 5 == 0 for k in residual_stars+residual_pencils),
            'field-polynomial divisibility of point and line sums')
    K = [k//5 for k in residual_stars]
    C = [indicator(star) for star in stars]
    d = list(K)
    C.extend(indicator(star,-1) for star in stars)
    d.extend(5-k for k in K)
    C.extend(indicator(pencil,-1) for pencil in pencils)
    d.extend(k//5-1 for k in residual_pencils)
    C.extend((indicator(stars[0]), indicator(stars[0],-1)))
    d.extend((K[0]-5*epsilon, -K[0]+5*epsilon))
    energy = [25+10*residue[h] for h in options]
    energy_rhs = 1269-sum(r*r for r in residue)
    C.extend((energy,[-e for e in energy]))
    d.extend((energy_rhs,-energy_rhs))
    D = [[int(h//5 == j) for h in options] for j in eligible]
    require(len(C) == len(d) == 1029 and all(sum(row)==5 for row in D),
            'constraint dimensions')
    return C, d, D


def check_certificate(certificate, diagonal, incidence):
    C,d,D = instance(diagonal, certificate['representative'], certificate['epsilon'],incidence)
    n = len(C[0])
    columns = [0]*n
    rhs, nonzeros = 0, 0
    for label,rows,bounds,nonnegative in (
            ('inequality_multipliers',C,d,True),
            ('equality_multipliers',D,[1]*len(D),False)):
        pairs = certificate[label]
        require(all(isinstance(pair,list) and len(pair)==2 and
                    all(type(x) is int for x in pair) for pair in pairs), 'integer multiplier pairs')
        require([i for i,v in pairs] == sorted(set(i for i,v in pairs)), 'ordered unique multiplier rows')
        for i,value in pairs:
            require(0 <= i < len(rows) and value != 0 and (not nonnegative or value > 0),
                    'valid signed multiplier')
            columns = [a+value*b for a,b in zip(columns,rows[i])]
            rhs += value*bounds[i]
            nonzeros += 1
    require(all(v >= 0 for v in columns), 'exact Farkas column inequality')
    require(rhs == certificate['contradiction'] and rhs < 0, 'strict exact Farkas contradiction')
    return {'variables':n, 'nonzero_multipliers':nonzeros, 'rhs':rhs,
            'smallest_column':min(columns)}
