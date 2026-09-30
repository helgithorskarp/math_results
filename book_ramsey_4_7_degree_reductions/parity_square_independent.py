#!/usr/bin/env python3
"""Separate exact determinant and literal-page checks. No main imports."""
from itertools import combinations
from math import isqrt
from pathlib import Path
import json
import random


def require(ok,message):
    if not ok:
        raise RuntimeError(message)


def determinant(mat):
    """Fraction-free Bareiss elimination with explicit divisibility checks."""
    a = [row[:] for row in mat]
    previous,sign = 1,1
    for k in range(len(a)-1):
        if a[k][k] == 0:
            row = next((i for i in range(k+1,len(a)) if a[i][k] != 0),None)
            if row is None:
                return 0
            a[k],a[row] = a[row],a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                numerator = pivot*a[i][j]-a[i][k]*a[k][j]
                require(numerator % previous == 0,"inexact determinant division")
                a[i][j] = numerator//previous
        for i in range(k+1,len(a)):
            a[i][k] = 0
        previous = pivot
    return sign*a[-1][-1]


def certificate(expected):
    # Diagonal is the literal squared length of a K-row; off-diagonal
    # comes from either color's common-page formula, which gives the same value.
    a,b,c = (expected['degree_counts'][str(d)] for d in (8,9,10))
    degree = [8]*a+[9]*b+[10]*c
    match = {a+2*i:a+2*i+1 for i in range(b//2)}
    match.update({b:a for a,b in list(match.items())})
    H = []
    for i in range(22):
        row = []
        for j in range(22):
            if i == j:
                value = (2*degree[i]-17)**2+4*degree[i]
            else:
                value = 4*(degree[i]+degree[j]-14)-4*int(match.get(i) == j)
            row.append(value)
        H.append(row)
    detH = determinant(H)
    require(detH == expected["forced_square_matrix_determinant"],"22x22 determinant mismatch")
    quotient = [[sum(H[i][j] for j in block) for block in (range(a),range(a,a+b),range(a+b,22))]
                for i in (0,a,a+b)]
    require(quotient == expected["quotient"],"quotient entries differ")
    require(determinant(quotient) == expected["quotient_determinant"],"quotient determinant differs")
    require(detH == 25**(a+c-2+b//2)*17**(b//2-1)*determinant(quotient),"factorization mismatch")
    value,exponent = detH,0
    while value % 17 == 0:
        value //= 17
        exponent += 1
    require(detH > 0 and isqrt(detH)**2 != detH,"square obstruction failed")
    if (a,b,c) == (7,12,3):
        require(exponent == 5,"97-edge valuation")
    elif (a,b,c) == (9,6,7):
        qdet = determinant(quotient)
        require(256**2 < qdet < 257**2 and expected["square_obstruction"]["remaining_factor_is_square"],
                "98-edge quotient obstruction")
    else:
        raise RuntimeError("unexpected histogram target")
    return {"determinant":detH,"valuation17":exponent,"integer_square":False,"forced_matrix":H}


def literal_controls():
    counts = {"graphs":0,"spines":0,"matrix_entries":0,"incident_parities":0}
    for seed in range(96):
        rng = random.Random(197000+seed)
        neighbors = [set() for _ in range(22)]
        for i,j in combinations(range(22),2):
            if rng.randrange(100) < 25+seed % 51:
                neighbors[i].add(j)
                neighbors[j].add(i)
        degree = list(map(len,neighbors))
        blue = [set(range(22))-neighbors[i]-{i} for i in range(22)]
        unused = [[0]*22 for _ in range(22)]
        K = [[(2*degree[i]-17 if i == j else 2*int(j in neighbors[i]))
              for j in range(22)] for i in range(22)]
        monochromatic = 0
        for a,b,c in combinations(range(22),3):
            colors = (b in neighbors[a],c in neighbors[a],c in neighbors[b])
            monochromatic += colors[0] == colors[1] == colors[2]
        for i,j in combinations(range(22),2):
            red = j in neighbors[i]
            page_set = neighbors[i] & neighbors[j] if red else blue[i] & blue[j]
            defect = (3 if red else 6)-len(page_set)
            unused[i][j] = unused[j][i] = defect
        for i in range(22):
            local_triangles = sum((j in neighbors[i]) == (k in neighbors[i]) == (k in neighbors[j])
                                  for j,k in combinations([v for v in range(22) if v != i],2))
            require(sum(unused[i]) == 3*degree[i]+6*(21-degree[i])-2*local_triangles,
                    "literal incident defect identity")
            require(sum(unused[i]) % 2 == degree[i] % 2,"literal parity")
            for j in range(22):
                value = sum(K[i][q]*K[j][q] for q in range(22))
                if i == j:
                    want = (2*degree[i]-17)**2+4*degree[i]
                else:
                    want = 4*(degree[i]+degree[j]-14)-4*unused[i][j]
                require(value == want,"literal page-to-square identity")
        edges = sum(degree)//2
        total = sum(unused[i][j] for i,j in combinations(range(22),2))
        require(total == 3*edges+6*(231-edges)-3*monochromatic,"literal global defect count")
        require(2*total == 132-3*sum((d-10)**2 for d in degree),"global quadratic count")
        counts["graphs"] += 1
        counts["spines"] += 231
        counts["matrix_entries"] += 484
        counts["incident_parities"] += 22
    return counts


def histograms(expected):
    result = []
    for entry in expected["boundaries"]:
        edges = entry["edges"]
        before = []
        for c in range(23):
            for b in range(23-c):
                a = 22-b-c
                if 8*a+9*b+10*c != 2*edges:
                    continue
                defect = 3*edges+6*(231-edges)-3*(1540-(8*13*a+9*12*b+10*11*c)//2)
                if 2*defect >= b:
                    before.append([a,b,c])
        before.sort()
        require(before == entry["before"] and before[:-1] == entry["after"],"histogram records differ")
        result.append({"edges":edges,"remaining":before[:-1]})
    equality = []
    for c in range(23):
        for b in range(23-c):
            a = 22-b-c
            degrees = [8]*a+[9]*b+[10]*c
            if sum(degrees) % 2:
                continue
            edges = sum(degrees)//2
            triangles = 1540-sum(d*(21-d) for d in degrees)//2
            defect = 3*edges+6*(231-edges)-3*triangles
            if 2*defect == b:
                equality.append([a,b,c])
    equality.sort()
    require(equality == expected["parity_equality_before"],"equality histogram coverage")
    require(expected["parity_equality_after"] == [[11,0,11]]
            and expected["remaining_equality_edges"] == 99
            and expected["remaining_equality_spine_defect"] == 0
            and expected["remaining_equality_red_neighbors_in_degree8_class"] == 4,
            "remaining equality certificate")
    # The remaining equality class has y=2 or0; solving K^2 1 from (3)
    # gives A y=8*1, hence exactly four neighbors in the y=2 class.
    for y in (0,2):
        rhs = 25+24*22-4*(22*y+22)+4*(y*y-2*y)
        Ay = (529-104*y+8*y*y-rhs)//8
        require(Ay == 8,"remaining equality neighbor relation")
    return result


def main():
    expected = json.loads(Path(__file__).with_name("parity_square_expected.json").read_text())
    require(len(expected["certificates"]) == len(expected["forced_square_matrices"]) == 2,
            "certificate domain length")
    require([tuple(cert["degree_counts"][str(d)] for d in (8,9,10)) for cert in expected["certificates"]]
            == [(7,12,3),(9,6,7)],"certificate histogram domain")
    results = []
    for cert,mat in zip(expected["certificates"],expected["forced_square_matrices"]):
        result = certificate(cert)
        require(result["forced_matrix"] == mat,"forced matrix entry mismatch")
        results.append({k:v for k,v in result.items() if k != 'forced_matrix'})
    require(literal_controls() == expected["controls"]["counts"],"control domains differ")
    remaining = histograms(expected["histograms"])
    print(json.dumps({"verified":True,"certificates":results,
                      "remaining_boundary_histograms":remaining,
                      "controls":expected["controls"]["counts"]},indent=2))


if __name__ == "__main__":
    main()
