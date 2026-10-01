#!/usr/bin/env python3
"""Independent exact audit of committed cyclic13 cap claim 8446.

six-reviewer-3, independent reviewer. Python standard library only.
No researcher modules, solver results or floating point enter --check.
--propose is explicitly exploratory and supplies no certificate.
"""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, product, permutations
import json
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
V = 13
COHORTS = {4: (20, 2, 151), 5: (18, 3, 183), 6: (18, 4, 220)}
# Fixed rational proposals: every upper bound is checked exactly below.
REAL_UPPER = {4: F(1997,100), 5: F(8817,500), 6: F(8817,500)}
REFINED_CAP = {4: F(37647,250), 5: F(91157,500), 6: F(54779,250)}
PATHS = {
    4: (23768, [(((0,5),(1,4),(2,8)),True), (((0,5),(1,12),(2,3)),False)]),
    5: (40920, [(((0,2),(1,3),(9,10)),False), (((0,5),(1,4),(2,10)),True),
               (((0,5),(1,12),(2,3)),False)]),
    6: (988913, [(((0,4),(1,3),(2,7)),False), (((0,2),(1,4),(3,9)),True),
                (((0,4),(1,5),(2,3)),True), (((0,4),(1,6),(2,3)),False)]),
}
WITNESSES = {
    4: (19, (0,5,2,-1,-1,-3,-2,-2,-3,-1,-1,2,5), 8, -82756145440215468),
    5: (17, (0,6,1,-2,-2,-2,-1,-1,-2,-2,-2,1,6), 8, -10262329952840524),
    6: (17, (0,-2,-2,6,-2,-1,1,1,-1,-2,6,-2,-2), 11, -125845303518730284769852),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def partition():
    triples = set(combinations(range(V), 3))
    orbits = []
    while triples:
        t = min(triples)
        orbit = tuple(sorted({tuple(sorted((x+k) % V for x in t)) for k in range(V)}))
        require(len(orbit) == V and set(orbit) <= triples, 'orbit partition')
        triples.difference_update(orbit)
        orbits.append(orbit)
    require(len(orbits) == 22, '22 triple orbits')
    signatures = []
    for orbit in orbits:
        sig = [0]*6
        for a, b in combinations(orbit[0], 2):
            sig[min((b-a) % V, (a-b) % V)-1] += 1
        # Independently verify that a representative signature is the degree
        # of EACH pair, not a total degree or an orbit-size multiple.
        degrees = {p: 0 for p in combinations(range(V), 2)}
        for t in orbit:
            for p in combinations(t, 2):
                degrees[p] += 1
        require(all(degrees[a,b] == sig[min(b-a, V-(b-a))-1]
                    for a,b in degrees), 'orbit pair signature')
        signatures.append(tuple((j, x) for j,x in enumerate(sig) if x))
    return orbits, signatures


def census(signatures):
    """Visit EVERY mask exactly once in reflected Gray order; no pruning."""
    degrees = [0]*6
    previous = 0
    accepted = {l: [] for l in COHORTS}
    for step in range(1, 1 << 22):
        mask = step ^ (step >> 1)
        flipped = mask ^ previous
        require(flipped and not (flipped & (flipped-1)), 'Gray adjacency')
        j = flipped.bit_length()-1
        direction = 1 if mask & flipped else -1
        for d, value in signatures[j]:
            degrees[d] += direction*value
        l = degrees[0]
        if l in accepted and all(x == l for x in degrees):
            require(mask.bit_count() == 2*l, 'selected orbit count')
            accepted[l].append(mask)
        previous = mask
    # Empty mask is visited as the initial state, and cannot be in these cohorts.
    require(previous == 1 << 21, 'Gray traversal endpoint')
    for masks in accepted.values():
        masks.sort()
        require(len(masks) == len(set(masks)), 'duplicate design')
    return accepted


def literal(orbits, mask, l):
    blocks = tuple(sorted(t for j,orbit in enumerate(orbits) if mask >> j & 1 for t in orbit))
    require(len(blocks) == 26*l and len(set(blocks)) == len(blocks), 'block count/simple')
    pairs = tuple(combinations(range(V), 2))
    pair_index = {p: j for j,p in enumerate(pairs)}
    pair_degrees = [0]*len(pairs)
    links = [0]*V
    for t in blocks:
        for p in combinations(t, 2):
            pair_degrees[pair_index[p]] += 1
        for x in t:
            p = tuple(y for y in t if y != x)
            links[x] |= 1 << pair_index[p]
    require(all(n == l for n in pair_degrees), 'literal pair multiplicities')
    r, u = 6*l, l*(l-1)//2
    require(all(link.bit_count() == r for link in links), 'replication')
    Z = [[(links[x] & links[y]).bit_count() - (r-u if x==y else 0) - u
          for y in range(V)] for x in range(V)]
    require(all(Z[x][x] == 0 and sum(Z[x]) == 0 for x in range(V)), 'point defect diagonal/row')
    row = tuple(Z[0])
    require(all(Z[x][y] == Z[y][x] == row[(y-x) % V]
                for x in range(V) for y in range(V)), 'literal circulant entries')
    return row, blocks


def unit_class(row):
    return min(tuple(row[(k*j) % V] for j in range(V)) for k in range(1,V))


def determinant(matrix):
    """Integer Bareiss elimination, exact division, row pivots if necessary."""
    A = [list(row) for row in matrix]
    n = len(A)
    if n == 0:
        return 1
    sign, old = 1, 1
    for k in range(n-1):
        pivot_row = next((i for i in range(k,n) if A[i][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            A[k], A[pivot_row] = A[pivot_row], A[k]
            sign = -sign
        pivot = A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator = pivot*A[i][j] - A[i][k]*A[k][j]
                q, rem = divmod(numerator, old)
                require(rem == 0, 'nonexact Bareiss division')
                A[i][j] = q
            A[i][k] = 0
        old = pivot
    return sign*A[-1][-1]


def point_form(row, gamma):
    p,q = gamma.numerator, gamma.denominator
    return [[13*p*int(i==j)-p-13*q*row[(j-i) % V]
             for j in range(V)] for i in range(V)]


def leading_point_minors(row, gamma):
    matrix = point_form(row, gamma)
    require(all(sum(r) == 0 for r in matrix), 'scaled point row sum')
    return [determinant([r[1:n+1] for r in matrix[1:n+1]]) for n in range(1,V)]


def rational_minors(matrix):
    result = []
    for n in range(1,len(matrix)+1):
        denominators = [matrix[i][j].denominator for i in range(n) for j in range(n)]
        from math import lcm
        scale = lcm(*denominators)
        result.append(F(determinant([[int(scale*matrix[i][j]) for j in range(n)]
                                      for i in range(n)]), scale**n))
    return result


def weights(l):
    v = V
    r, u, s, m = F(l*(v-1),2), F(l*(l-1),2), F(v+l*(v-1)//2), F(v*(v-1),2)
    D0 = l*(v*v-10*v+27)-6
    c = F(v*v-(l+3)*v, (v-2)*(v-3)) + F(11*l, 3*(v-2)*(v-3))
    d = F(v*v-v-4, (v-4)*(v-3))
    t = F((v-1)*(l*(v-3)-6), D0)
    w = s-(v-3)*c-(r-2*l)*d
    h = s-(v-4)*d-(r-3*l)*t
    require(all(z > 0 for z in (c,d,t,h)), 'weight signs')
    return c,d,t,w,h


def comparison(l, gamma, bound):
    v = V
    r, u, s, m = F(l*(v-1),2), F(l*(l-1),2), F(v+l*(v-1)//2), F(v*(v-1),2)
    N = 1+v+m+F(l*v*(v-1),6)
    c,d,t,w,h = weights(l)
    alpha = (v-5)*r-(v-6)*u+3*l*l-l
    rho = [w*w*(v-2)+d*d*(r-u)-2*w*d*l+d*d*gamma,
           h*h*(r-l)-6*h*t*u+t*t*alpha+(2*h*t+t*t*(v-6))*gamma,
           d*d*F((v-4)**2*(2*v-6),4)]
    require(all(z >= 0 for z in rho), 'negative cross norm bound')
    a12, a13, a23 = [F(isqrt(z.numerator//z.denominator)+1) for z in rho]
    A = [a12,a13,a23]
    require(all(a>0 and a*a>z for a,z in zip(A,rho)), 'strict cross margins')
    diagonal = [s+F(l,3)+t*gamma, s+c, s+t*(v-5)]
    G = [[diagonal[0],a12,a13],[a12,diagonal[1],a23],[a13,a23,diagonal[2]]]
    M = [[F(bound)*int(i==j)-G[i][j] for j in range(3)] for i in range(3)]
    minors = rational_minors(M)
    g = m*F((v-2)*(v-3),2*v*v)
    require(all(x>0 for x in minors) and N-bound>g>0, 'joint cap/repair margin')
    require(all(bound>x for x in diagonal), 'strict diagonal bound')
    return {'gamma':str(gamma), 'B':str(bound), 'G':[[str(z) for z in row] for row in G],
            'comparison_leading_minors':[str(z) for z in minors],
            'cross_square_margins':[str(a*a-z) for a,z in zip(A,rho)],
            'delta':str(N-bound), 'half_gap_margin':str((N-bound-g)/2),
            'old_row_criterion_sufficient':N-max(map(sum,G))>g}


def transpose(A):
    return [list(x) for x in zip(*A)]


def multiply(A,B):
    columns = transpose(B)
    return [[sum(a*b for a,b in zip(row,col)) for col in columns] for row in A]


def gram(A):
    return multiply(A,transpose(A))


def incidences(blocks,l):
    blocks = tuple(sorted(blocks))
    require(len(blocks)==26*l and len(set(blocks))==len(blocks), 'fixture simplicity')
    pairs = tuple(combinations(range(V),2))
    present = set(blocks)
    missing = tuple(t for t in combinations(range(V),3) if t not in present)
    P = [[int(x in p) for p in pairs] for x in range(V)]
    C = [[int(x not in p and tuple(sorted(p+(x,))) in present) for p in pairs] for x in range(V)]
    B = [[int(x in a) for a in blocks] for x in range(V)]
    R = [[int(set(p)<=set(a)) for a in blocks] for p in pairs]
    Rq = [[int(set(p)<=set(a)) for a in missing] for p in pairs]
    require(all(sum(row)==l for row in R), 'fixture pair degrees')
    r,u = 6*l, l*(l-1)//2
    require(all(sum(row)==r for row in B), 'fixture replication')
    CC = gram(C)
    Z = [[CC[x][y]-(r-u)*int(x==y)-u for y in range(V)] for x in range(V)]
    require(all(sum(row)==0 for row in Z), 'fixture defect rows')
    CR = multiply(C,R)
    H = [[CR[x][j]-B[x][j] for j in range(len(blocks))] for x in range(V)]
    Fm = multiply(C,Rq)
    return P,C,B,R,Rq,H,Fm,Z


def check_grams(blocks,l):
    P,C,B,R,Rq,H,Fm,Z = incidences(blocks,l)
    v,r,u = V,6*l,l*(l-1)//2
    PP,BB,CP,PR,RB,HB = gram(P),gram(B),multiply(C,transpose(P)),multiply(P,R),multiply(R,transpose(B)),multiply(H,transpose(B))
    for x in range(v):
        for y in range(v):
            I = int(x==y)
            require(PP[x][y]==(v-2)*I+1, 'PP Gram')
            require(BB[x][y]==(r-l)*I+l, 'BB Gram')
            require(CP[x][y]==l*(1-I), 'CP Gram')
            require(HB[x][y]==Z[x][y]+3*u*(1-I), 'HB Gram')
        require(PR[x]==[2*z for z in B[x]], 'PR incidence')
    for j in range(len(R)):
        require(RB[j]==[l*P[x][j]+C[x][j] for x in range(v)], 'RB incidence')
    RR,RRq,PtP = gram(R),gram(Rq),gram(transpose(P))
    require(all(RR[i][j]+RRq[i][j]==(v-4)*int(i==j)+PtP[i][j]
                for i in range(len(R)) for j in range(len(R))), 'complete-pair identity')
    HH,FF = gram(H),gram(Fm)
    alpha = (v-5)*r-(v-6)*u+3*l*l-l
    beta = (v-6)*u+l*l*(v-4)+l
    require(all(HH[x][y]==alpha*int(x==y)+(v-6)*Z[x][y]+beta-FF[x][y]
                for x in range(v) for y in range(v)), 'whole HH Gram')
    c,d,t,w,h = weights(l)
    A = [[w*a+d*b for a,b in zip(prow,crow)] for prow,crow in zip(P,C)]
    T = [[h*a+t*b for a,b in zip(brow,hrow)] for brow,hrow in zip(B,H)]
    AA,TT = gram(A),gram(T)
    mu12 = w*w*(v-2)+d*d*(r-u)-2*w*d*l
    nu12 = w*w+d*d*u+2*w*d*l
    mu13 = h*h*(r-l)-6*h*t*u+t*t*alpha
    nu13 = h*h*l+6*h*t*u+t*t*beta
    zcoef = 2*h*t+t*t*(v-6)
    require(all(AA[x][y]==mu12*int(x==y)+d*d*Z[x][y]+nu12
                for x in range(v) for y in range(v)), 'whole point/pair cross Gram')
    require(all(TT[x][y]==mu13*int(x==y)+zcoef*Z[x][y]+nu13-t*t*FF[x][y]
                for x in range(v) for y in range(v)), 'whole point/triple cross Gram')
    # Constant rows and columns are what makes all sum-zero restrictions valid.
    for matrix in (P,C,B,R,Rq,H,Fm,A,T):
        require(len({sum(row) for row in matrix})==1, 'regular rows')
        require(len({sum(col) for col in zip(*matrix)})==1, 'regular columns')
    return digest({'blocks':sorted(blocks),'Z':Z,'AA':[[str(z) for z in row] for row in AA],
                   'TT':[[str(z) for z in row] for row in TT]})


def fixture_checks(orbits):
    # Published witness masks use the increasing minimum bitmask representative.
    # Decode this documented input convention, without importing author code.
    bit_order = sorted(range(22), key=lambda j:min(sum(1<<x for x in t) for t in orbits[j]))
    results = {}
    for l,(old_mask,moves) in PATHS.items():
        mask = sum(1<<j for k,j in enumerate(bit_order) if old_mask>>k&1)
        row,blocks = literal(orbits,mask,l)
        require(row==WITNESSES[l][1], 'published path starts at the witness row')
        blocks = set(blocks)
        initial_hash = check_grams(blocks,l)
        states = {tuple(sorted(blocks))}
        minima = []
        for step in range(len(moves)+1):
            Z = incidences(blocks,l)[-1]
            gamma = REAL_UPPER[l]+F(50*step,3)
            p,q = gamma.numerator,gamma.denominator
            matrix = [[13*p*int(x==y)-p-13*q*Z[x][y] for y in range(V)] for x in range(V)]
            minors = [determinant([r[1:n+1] for r in matrix[1:n+1]]) for n in range(1,V)]
            require(all(z>0 for z in minors), 'literal accumulated point PSD')
            minima.append(minors)
            if step==len(moves):
                break
            groups,reverse = moves[step]
            require(len({x for g in groups for x in g})==6, 'six distinct trade points')
            even,odd = set(),set()
            for bits in product(range(2),repeat=3):
                a = tuple(sorted(groups[j][bits[j]] for j in range(3)))
                (odd if sum(bits)%2 else even).add(a)
            removed,added = (odd,even) if reverse else (even,odd)
            require(removed<=blocks and added.isdisjoint(blocks), 'literal trade legality')
            blocks = blocks-removed|added
            state = tuple(sorted(blocks))
            require(state not in states, 'literal repeated state')
            states.add(state)
        require(len({tuple(sorted(r)) for r in Z})==13, 'noncyclic final row invariants')
        results[str(l)] = {'legal_moves':len(moves), 'point_states':len(minima),
                           'final_point_row_invariants':13, 'initial_whole_gram_sha256':initial_hash,
                           'final_whole_gram_sha256':check_grams(blocks,l),
                           'point_minor_transcript_sha256':digest(minima)}
    return results


def controls():
    # A different determinant definition checks pivot signs and singular cases.
    samples = [[[0,2],[3,4]], [[1,2],[2,4]], [[4,-1,2],[3,0,-2],[1,5,7]],
               [[0,1,2,3],[4,5,6,1],[2,0,7,3],[1,4,0,6]]]
    for A in samples:
        n = len(A)
        value = 0
        for perm in permutations(range(n)):
            inversions = sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
            term = 1
            for i,j in enumerate(perm):
                term *= A[i][j]
            value += (-1 if inversions%2 else 1)*term
        require(value==determinant(A), 'Leibniz determinant control')


def build(propose=False, author_expected=None):
    controls()
    orbits, signatures = partition()
    masks = census(signatures)
    rows = {l:{} for l in COHORTS}
    point_transcript = []
    for l in COHORTS:
        for mask in masks[l]:
            row, blocks = literal(orbits,mask,l)
            rows[l].setdefault(row,mask)
            point_transcript.append([l,mask,row])
    require([len(masks[l]) for l in COHORTS] == [762,1305,1305], 'census counts')
    require([len(rows[l]) for l in COHORTS] == [335,575,575], 'ordered point rows')
    full = (1<<22)-1
    require({full^m for m in masks[5]} == set(masks[6]), 'complete complement-mask bijection')
    require(set(rows[5]) == set(rows[6]), 'complement point equality')
    # Reconstruct every complement explicitly, rather than relying only on row sets.
    for mask in masks[5]:
        require(literal(orbits,mask,5)[0] == literal(orbits,full^mask,6)[0], 'entrywise complement')
    classes = {l: sorted({unit_class(row) for row in rows[l]}) for l in COHORTS}
    require([len(classes[l]) for l in COHORTS] == [59,98,98], 'unit point classes')
    if propose:
        from math import cos, pi, ceil
        proposal = {}
        for l in COHORTS:
            eig, row, mode = max((sum(row[j]*cos(2*pi*k*j/V) for j in range(V)),row,k)
                                for row in rows[l] for k in range(1,7))
            proposal[l] = {'exploratory_eigenvalue':eig, 'row':row, 'mode':mode,
                           'suggested_upper':str(F(ceil(1000*eig),1000))}
        return {'status':'FLOATING-POINT EXPLORATION ONLY; NO CERTIFICATE', 'proposals':proposal}

    positive_transcript, real_transcript, cohort = [], [], {}
    for l,(integer_budget,max_moves,bound) in COHORTS.items():
        witness_gamma,row,n,expected_det = WITNESSES[l]
        require(row in rows[l], 'integer obstruction must occur in literal census')
        det = leading_point_minors(row,F(witness_gamma))[n-1]
        require(det == expected_det and det < 0, 'integer sharpness witness')
        for row in classes[l]:
            minors = leading_point_minors(row,F(integer_budget))
            require(all(x>0 for x in minors), 'integer budget positive certificate')
            if l != 6:
                positive_transcript.append([l,row,minors])
            real_minors = leading_point_minors(row,REAL_UPPER[l])
            require(all(x>0 for x in real_minors), 'rational upper certificate')
            if l != 6:
                real_transcript.append([l,row,real_minors])
        lower = REAL_UPPER[l]-F(1,1000)
        obstruction = None
        for row in sorted(rows[l]):
            minors = leading_point_minors(row,lower)
            negative = next((j for j,z in enumerate(minors) if z<0),None)
            if negative is not None:
                obstruction = {'gamma':str(lower), 'row':list(row), 'mask':rows[l][row],
                               'points':list(range(1,negative+2)),
                               'scaled_integer_determinant':minors[negative]}
                break
        require(obstruction is not None, 'rational lower obstruction not established')
        comparisons = []
        for moves in range(max_moves+1):
            record = comparison(l,F(integer_budget)+F(50*moves,3),bound)
            record['moves'] = moves
            comparisons.append(record)
        refined = []
        for moves in range(max_moves+1):
            record = comparison(l,REAL_UPPER[l]+F(50*moves,3),REFINED_CAP[l])
            record['moves'] = moves
            refined.append(record)
        cohort[str(l)] = {'designs':len(masks[l]), 'ordered_rows':len(rows[l]),
                         'unit_row_classes':len(classes[l]), 'integer_budget':integer_budget,
                         'integer_negative_witness':{'row':list(WITNESSES[l][1]),'gamma':witness_gamma,
                            'points':list(range(1,n+1)),'determinant':det},
                         'real_budget_strict_lower':str(lower), 'real_budget_strict_upper':str(REAL_UPPER[l]),
                         'real_negative_witness':obstruction, 'original_comparisons':comparisons,
                         'refined_point_comparisons':refined}
    if author_expected is not None:
        author = json.loads(Path(author_expected).read_text())
        for l in COHORTS:
            theirs = author['cohorts'][str(l)]
            ours = cohort[str(l)]
            require(theirs['fixed_shift_labelled_designs']==ours['designs'], 'author count mismatch')
            require(theirs['ordered_circulant_point_rows']==ours['ordered_rows'], 'author row mismatch')
            require(theirs['unit_point_row_classes']==ours['unit_row_classes'], 'author unit mismatch')
            require(theirs['mean_point_budget']==ours['integer_budget'], 'author budget mismatch')
            for a,b in zip(theirs['all_shorter_path_comparisons'],ours['original_comparisons']):
                require(all(b[key]==value for key,value in a.items()), 'author comparison mismatch')
            require(len(theirs['all_shorter_path_comparisons'])==len(ours['original_comparisons']), 'author paths')
    return {'reviewer':'six-reviewer-3', 'role':'independent mathematical reviewer',
            'method':'unpruned complete reflected-Gray orbit-subset enumeration; literal tuple incidences; exact Bareiss determinants',
            'visited_masks':1<<22, 'triple_orbits':22, 'designs':sum(map(len,masks.values())),
            'point_entries_checked':169*sum(map(len,masks.values())),
            'pair_degrees_checked':78*sum(map(len,masks.values())),
            'complement_pairs_checked':len(masks[5]),
            'distinct_integer_positive_forms':len(positive_transcript),
            'integer_positive_minors':12*len(positive_transcript),
            'distinct_rational_positive_forms':len(real_transcript),
            'rational_positive_minors':12*len(real_transcript),
            'determinant_definition_controls':4,
            'original_joint_comparisons':sum(COHORTS[l][1]+1 for l in COHORTS),
            'literal_path_checks':fixture_checks(orbits),
            'cohorts':cohort, 'point_transcript_sha256':digest(point_transcript),
            'integer_minor_transcript_sha256':digest(positive_transcript),
            'rational_minor_transcript_sha256':digest(real_transcript)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--propose',action='store_true')
    p.add_argument('--write-expected',action='store_true')
    p.add_argument('--author-expected',type=Path)
    args = p.parse_args()
    result = build(propose=args.propose,author_expected=args.author_expected)
    if args.propose:
        print(json.dumps(result,indent=2,sort_keys=True))
    elif args.write_expected:
        (HERE/'expected.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
        print('Exact audit complete; wrote compact expected.json')
    else:
        expected = json.loads((HERE/'expected.json').read_text())
        require(result==expected, 'frozen independent transcript mismatch')
        print('PASS: complete census, exact point certificates, sharp integer budgets, joint caps and rational refinements')


if __name__ == '__main__':
    main()
