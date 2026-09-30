#!/usr/bin/env python3
"""Integer-square obstructions classify parity-tight degrees 8,9,10.

The proof is analytic (parity_square.md). This program checks its matrix
decomposition and identities; no host enumeration or solver is used.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import random

N = 22


def require(ok,message):
    if not ok:
        raise RuntimeError(message)


def encode(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()


def multiply(a,b):
    return [[sum(x*b[k][j] for k,x in enumerate(row)) for j in range(len(b[0]))] for row in a]


def determinant3(mat):
    result = 0
    for order in permutations(range(3)):
        inversions = sum(order[i] > order[j] for i in range(3) for j in range(i+1,3))
        term = 1
        for i in range(3):
            term *= mat[i][order[i]]
        result += (-1 if inversions % 2 else 1)*term
    return result


def vector(plus,minus=()):
    return [int(i in plus)-int(i in minus) for i in range(N)]


def rank(mat):
    a = [[Fraction(x) for x in row] for row in mat]
    pivot = 0
    for col in range(len(a[0])):
        row = next((i for i in range(pivot,len(a)) if a[i][col]),None)
        if row is None:
            continue
        a[pivot],a[row] = a[row],a[pivot]
        for i in range(pivot+1,len(a)):
            if a[i][col]:
                q = a[i][col]/a[pivot][col]
                a[i] = [x-q*y for x,y in zip(a[i],a[pivot])]
        pivot += 1
    return pivot


def valuation(value,prime):
    require(value != 0,"zero determinant")
    exponent = 0
    while value % prime == 0:
        value //= prime
        exponent += 1
    return exponent


def matrix_certificate(a,b,c):
    groups = (tuple(range(a)),tuple(range(a,a+b)),tuple(range(a+b,N)))
    pairs = tuple((a+2*i,a+2*i+1) for i in range(b//2))
    y = (2,)*a+(1,)*b+(0,)*c
    F = [[0]*N for _ in range(N)]
    for i,j in pairs:
        F[i][j] = F[j][i] = 1
    H = [[25*(i == j)+24-4*(y[i]+y[j])
          +4*(y[i]*y[i]-2*y[i])*(i == j)-4*F[i][j]
          for j in range(N)] for i in range(N)]
    eig25 = [vector((i,),(group[-1],)) for group in (groups[0],groups[2]) for i in group[:-1]]
    eig25 += [vector((i,),(j,)) for i,j in pairs]
    eig17 = [vector(pair,pairs[-1]) for pair in pairs[:-1]]
    group_vectors = [vector(group) for group in groups]
    for value,basis in ((25,eig25),(17,eig17)):
        for v in basis:
            require([sum(row[j]*v[j] for j in range(N)) for row in H]
                    == [value*x for x in v],"wrong invariant eigenvector")
    quotient = []
    for group in groups:
        quotient.append([sum(H[group[0]][j] for j in other) for other in groups])
    for index,group in enumerate(groups):
        for i in group:
            require([sum(H[i][j] for j in other) for other in groups] == quotient[index],
                    "group-constant space not invariant")
    basis = eig25+eig17+group_vectors
    require(len(eig25) == a+c-2+b//2 and len(eig17) == b//2-1 and rank(basis) == N,"direct-sum coverage")
    qdet = determinant3(quotient)
    detH = 25**len(eig25)*17**len(eig17)*qdet
    if (a,b,c) == (7,12,3):
        require(qdet == 114177 and valuation(detH,17) == 5,"97-edge square obstruction")
        obstruction = {"prime":17,"valuation":5}
    elif (a,b,c) == (9,6,7):
        require(qdet == 65681 and 256**2 < qdet < 257**2,"98-edge square obstruction")
        obstruction = {"nonsquare_quotient":qdet,"lower_square":256**2,"upper_square":257**2,
                       "remaining_factor_is_square":True}
    else:
        raise RuntimeError("unexpected certificate target")
    return {"degree_counts":{"8":a,"9":b,"10":c},"edges":(8*a+9*b+10*c)//2,
            "total_spine_defect":b//2,"defect_matching":pairs,
            "basis_rank":N,"eigenvalue25_dimension":len(eig25),"eigenvalue17_dimension":len(eig17),
            "quotient":quotient,"quotient_determinant":qdet,"quotient_det_mod17":qdet % 17,
            "forced_square_matrix_determinant":detH,"square_obstruction":obstruction,
            "forced_square_sha256":sha256(encode(H)).hexdigest()},H


def controls():
    counts = Counter()
    fingerprint = sha256()
    for seed in range(96):
        rng = random.Random(197000+seed)
        adj = [[0]*N for _ in range(N)]
        neighbors = [0]*N
        for i,j in combinations(range(N),2):
            if rng.randrange(100) < 25+seed % 51:
                adj[i][j] = adj[j][i] = 1
                neighbors[i] |= 1 << j
                neighbors[j] |= 1 << i
        degree = list(map(sum,adj))
        y = [10-d for d in degree]
        blue = [((1 << N)-1) ^ neighbors[i] ^ (1 << i) for i in range(N)]
        F = [[0]*N for _ in range(N)]
        triangles = sum((neighbors[i] & neighbors[j]).bit_count()
                        if adj[i][j] else (blue[i] & blue[j]).bit_count()
                        for i,j in combinations(range(N),2))//3
        for i,j in combinations(range(N),2):
            pages = ((neighbors[i] & neighbors[j]).bit_count() if adj[i][j]
                     else (blue[i] & blue[j]).bit_count())
            F[i][j] = F[j][i] = (3 if adj[i][j] else 6)-pages
        K = [[2*adj[i][j]+(3-2*y[i])*(i == j) for j in range(N)] for i in range(N)]
        square = multiply(K,K)
        predicted = [[25*(i == j)+24-4*(y[i]+y[j])
                      +4*(y[i]*y[i]-2*y[i])*(i == j)-4*F[i][j]
                      for j in range(N)] for i in range(N)]
        require(square == predicted,"universal integer-square identity")
        total = sum(F[i][j] for i,j in combinations(range(N),2))
        require(2*total == 132-3*sum(value*value for value in y),"total spine-defect identity")
        require(triangles == 1540-sum(d*(21-d) for d in degree)//2,"monochromatic triangles")
        for i in range(N):
            require(sum(F[i]) % 2 == degree[i] % 2,"incident parity identity")
        counts["graphs"] += 1
        counts["matrix_entries"] += N*N
        counts["incident_parities"] += N
        counts["spines"] += N*(N-1)//2
        fingerprint.update(encode([seed,degree,total,square])+b"\n")
    return {"counts":dict(sorted(counts.items())),"sha256":fingerprint.hexdigest()}


def histogram_audit():
    boundaries = []
    equality = []
    for edges in (97,98):
        before = []
        for a in range(23):
            for b in range(23-a):
                c = 22-a-b
                if 8*a+9*b+10*c != 2*edges:
                    continue
                twice_defect = 132-3*(4*a+b)
                if twice_defect >= b:
                    before.append([a,b,c])
        boundaries.append({"edges":edges,"before":before,"after":before[:-1]})
        require(before[-1] == ([7,12,3] if edges == 97 else [9,6,7]),"removed boundary histogram")
    for a in range(23):
        for b in range(23-a):
            c = 22-a-b
            if b % 2 == 0 and 132-3*(4*a+b) == b:
                equality.append([a,b,c])
    require(equality == [[7,12,3],[9,6,7],[11,0,11]],"complete parity-equality histograms")
    for y in (0,2):
        rhs = 25+24*22-4*(22*y+22)+4*(y*y-2*y)
        require(529-104*y+8*y*y-8*8 == rhs,"remaining equality A-y relation")
    return {"degrees_considered":[8,9,10],"boundaries":boundaries,
            "parity_equality_before":equality,"parity_equality_after":[[11,0,11]],
            "remaining_equality_edges":99,"remaining_equality_spine_defect":0,
            "remaining_equality_red_neighbors_in_degree8_class":4,
            "corollary_dependency":"The committed degree-eight lower bound and degree-eleven-implies-at-least106-edges theorem; see parity_square.md."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-expected",type=Path)
    args = parser.parse_args()
    certificates,matrices = [],[]
    for histogram in ((7,12,3),(9,6,7)):
        certificate,H = matrix_certificate(*histogram)
        certificates.append(certificate)
        matrices.append(H)
    output = {"agent":"six-books-1","role":"researcher","proof_kind":"written analytic determinant obstruction; exact checks only",
              "certificates":certificates,"forced_square_matrices":matrices,
              "histograms":histogram_audit(),"controls":controls()}
    if args.write_expected:
        args.write_expected.write_text(json.dumps(output,indent=2)+"\n")
    else:
        expected = json.loads(Path(__file__).with_name("parity_square_expected.json").read_text())
        require(encode(output) == encode(expected),"compact expected output mismatch")
    print(json.dumps(output,indent=2))


if __name__ == "__main__":
    main()
