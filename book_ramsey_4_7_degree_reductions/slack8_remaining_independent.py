#!/usr/bin/env python3
"""Standalone separate audit of the two remaining surplus-eight histograms.

Domain: ordered positive compositions and multisets of unit center edges.
No author/predecessor imports. Expected signed masks are validation fixtures;
they do not select the mathematical normal-form domain or square survivors.
"""
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from math import lcm
from pathlib import Path

HISTOGRAMS = ((7,10,5),(9,4,9))
DEGREE = []


def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def serialize(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()

def elimination(matrix, want_determinant=False):
    a = [[Fraction(x) for x in row] for row in matrix]
    rank, answer = 0, Fraction(1)
    for col in range(len(a[0])):
        pivot_row = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot_row is None:
            continue
        if pivot_row != rank:
            a[pivot_row], a[rank] = a[rank], a[pivot_row]
            answer = -answer
        pivot = a[rank][col]
        answer *= pivot
        for i in range(rank + 1, len(a)):
            multiplier = a[i][col] / pivot
            for j in range(col + 1, len(a[0])):
                a[i][j] -= multiplier * a[rank][j]
            a[i][col] = 0
        rank += 1
        if rank == len(a):
            break
    if not want_determinant:
        return rank
    need(len(a) == len(a[0]), "nonsquare determinant")
    if rank != len(a):
        return 0
    need(answer.denominator == 1, "nonintegral determinant")
    return answer.numerator

def sqrt_floor(value):
    need(value > 0, "nonpositive determinant")
    low, high = 0, 1 << ((value.bit_length() + 1) // 2)
    while high - low > 1:
        mid = (low + high) // 2
        if mid * mid <= value:
            low = mid
        else:
            high = mid
    need(low * low <= value < high * high, "wrong square-root interval")
    return low

def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for head in range(1, total - length + 2):
            for tail in compositions(total - head, length - 1):
                yield (head,) + tail

def domain():
    """Unit-edge multisets; includes every ordered colored surplus support."""
    canonical, raw_counts, all_profiles = {}, Counter(), set()
    for k in range(1, 5):
        pairs = list(combinations(range(k), 2))
        relabelings = list(permutations(range(k)))
        for units in compositions(4, k):
            for colors in product((8, 9, 10), repeat=k):
                if any(colors.count(d) > DEGREE.count(d) for d in (8, 9, 10)):
                    continue
                typed = tuple((d, 2 * u) for d, u in zip(colors, units))
                all_profiles.add(tuple(sorted(typed)))
                demand = [d % 2 + 2 * u for d, u in zip(colors, units)]
                available_odd = DEGREE.count(9) - colors.count(9)
                for m in range(sum(demand) // 2 + 1):
                    for multiset in combinations_with_replacement(range(len(pairs)), m):
                        weights = Counter(multiset)
                        adjacent = [[0] * k for _ in range(k)]
                        incident = [0] * k
                        for slot, w in weights.items():
                            i, j = pairs[slot]
                            adjacent[i][j] = adjacent[j][i] = w
                            incident[i] += w
                            incident[j] += w
                        leaves = [a - b for a, b in zip(demand, incident)]
                        if min(leaves) < 0 or sum(leaves) > available_odd:
                            continue
                        if (available_odd - sum(leaves)) % 2:
                            continue
                        keys = [(tuple(typed[p[i]] for i in range(k)),
                                 tuple(adjacent[p[i]][p[j]] for i, j in pairs)) for p in relabelings]
                        key = min(keys)
                        raw_counts[key[0]] += 1
                        if key not in canonical:
                            canonical[key] = (typed, adjacent)
    return canonical, raw_counts, all_profiles

def labeled_defect(typed, adjacent):
    # Choose labels in reverse order; no canonical labels from the generator.
    available = {d: [i for i, value in enumerate(DEGREE) if value == d] for d in (8, 9, 10)}
    centers = [available[d].pop() for d, q in typed]
    links = {}
    for i, j in combinations(range(len(typed)), 2):
        if adjacent[i][j]:
            links[tuple(sorted((centers[i], centers[j])))] = adjacent[i][j]
    for i, (d, q) in enumerate(typed):
        remaining = d % 2 + q - sum(adjacent[i])
        for _ in range(remaining):
            leaf = available[9].pop()
            links[tuple(sorted((centers[i], leaf)))] = 1
    while available[9]:
        i, j = available[9].pop(), available[9].pop()
        links[tuple(sorted((i, j)))] = 1
    return links

def normalize(links):
    rows = [{} for _ in DEGREE]
    for (i, j), w in links.items():
        need(0 <= i < j < 22 and isinstance(w, int) and w > 0, "malformed defect")
        rows[i][j] = rows[j][i] = w
    surplus = [sum(row.values()) - d % 2 for d, row in zip(DEGREE, rows)]
    need(sum(surplus) == 8 and all(x >= 0 and x % 2 == 0 for x in surplus), "wrong surplus")
    centers = [i for i, value in enumerate(surplus) if value]
    pairs = list(combinations(range(len(centers)), 2))
    candidates = []
    for ordered in permutations(centers):
        types = tuple((DEGREE[i], surplus[i]) for i in ordered)
        weights = tuple(rows[ordered[i]].get(ordered[j], 0) for i, j in pairs)
        candidates.append(((types, weights), ordered))
    key, centers = min(candidates)
    leaves, remaining = [], {i for i, d in enumerate(DEGREE) if d == 9 and i not in centers}
    for i in centers:
        local = sorted(j for j in rows[i] if j not in centers)
        need(all(j in remaining and rows[i][j] == 1 for j in local), "nonunit/shared odd leaf")
        leaves.extend(local)
        remaining.difference_update(local)
    matching = []
    while remaining:
        i = min(remaining)
        need(len(rows[i]) == 1, "wrong normal odd vertex")
        j, w = next(iter(rows[i].items()))
        need(j in remaining - {i} and w == 1, "wrong residual matching")
        matching.extend((i, j))
        remaining.difference_update((i, j))
    order = []
    for d in (8, 9, 10):
        order.extend(i for i in centers if DEGREE[i] == d)
        order.extend(leaves + matching if d == 9 else
                     [i for i, value in enumerate(DEGREE) if value == d and i not in centers])
    need(len(order) == 22 and set(order) == set(range(22)) and [DEGREE[i] for i in order] == DEGREE,
         "wrong degree-preserving normalization")
    F = [[rows[i].get(j, 0) for j in order] for i in order]
    literal_H = [[(2 * DEGREE[i] - 17) ** 2 + 4 * DEGREE[i] if i == j
                  else 4 * (DEGREE[i] + DEGREE[j] - 14) - 4 * rows[i].get(j, 0)
                  for j in range(22)] for i in range(22)]
    H = [[literal_H[i][j] for j in order] for i in order]
    need(sum(links.values()) == (8 + DEGREE.count(9)) // 2, "wrong total defect")
    return key, F, H

def orbit_size(key):
    types, weights = key
    pairs = list(combinations(range(len(types)), 2))
    adjacent = [[0] * len(types) for _ in types]
    for (i, j), w in zip(pairs, weights):
        adjacent[i][j] = adjacent[j][i] = w
    values = {tuple(adjacent[p[i]][p[j]] for i, j in pairs) for p in permutations(range(len(types)))
              if tuple(types[p[i]] for i in range(len(types))) == types}
    return len(values)

def multiply(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def inverse(matrix):
    n = len(matrix)
    rows = [[Fraction(x) for x in row]+[Fraction(i==j) for j in range(n)]
            for i,row in enumerate(matrix)]
    for column in range(n):
        p = next((i for i in range(column,n) if rows[i][column]),None)
        need(p is not None,"singular inverse")
        rows[p],rows[column] = rows[column],rows[p]
        pivot = rows[column][column]
        rows[column] = [v/pivot for v in rows[column]]
        for i in range(n):
            if i!=column:
                pivot = rows[i][column]
                rows[i] = [v-pivot*w for v,w in zip(rows[i],rows[column])]
    return [row[n:] for row in rows]


def certificate(F,H):
    heavy = [(i,j) for i,j in combinations(range(22),2) if F[i][j]>=2]
    if heavy:
        need(len(heavy)==2,"unexpected heavy square pattern")
        plane = []
        for i,j in heavy:
            v = [int(k==i)-int(k==j) for k in range(22)]
            need([sum(x*y for x,y in zip(row,v)) for row in H]==[33*x for x in v],"wrong33 eigenvector")
            plane.append(v)
        shifted = [[H[i][j]-33*(i==j) for j in range(22)] for i in range(22)]
        rank = elimination(shifted)
        gram = [[sum(x*y for x,y in zip(v,w)) for w in plane] for v in plane]
        need(rank==20 and gram==[[2,0],[0,2]],"wrong complete33 eigenspace")
        residues = [(a,b,c) for a,b,c in product(range(9),repeat=3)
                    if (a*a+b*b-33*c*c)%9==0]
        need(len(residues)==27 and all(a%3==b%3==c%3==0 for a,b,c in residues),"primitive mod9 norm")
        return {"mechanism":"rational33_plane","basis_pairs":[list(p) for p in heavy],
                "rank_H_minus33I":rank,"gram":gram,"norm_mod9_solutions":len(residues),
                "primitive_norm_mod9_solutions":0}
    groups = [[i for i,d in enumerate(DEGREE) if d==t] for t in (8,9,10)]
    need(list(map(len,groups))==[9,4,9],"wrong quotient groups")
    need(all(F[i][j]==int(i!=j and DEGREE[i]==DEGREE[j]==9)
             for i in range(22) for j in range(22)),"unexpected unit square pattern")
    indicators = [[int(i in group) for i in range(22)] for group in groups]
    contrast = [[int(i==v)-int(i==group[-1]) for i in range(22)]
                for group in groups for v in group[:-1]]
    need(elimination(indicators+contrast)==22,"incomplete rational decomposition")
    for v in contrast:
        need([sum(x*y for x,y in zip(row,v)) for row in H]==[25*x for x in v],"contrast eigenvalue")
    q_rows = [[[sum(H[i][j] for j in other) for other in groups] for i in group] for group in groups]
    need(all(all(row==rows[0] for row in rows) for rows in q_rows),"quotient not invariant")
    Q = [rows[0] for rows in q_rows]
    shifted = [[Q[i][j]-25*(i==j) for j in range(3)] for i in range(3)]
    det_shift = sum((-1)**sum(p[i]>p[j] for i,j in combinations(range(3),2))*
                    shifted[0][p[0]]*shifted[1][p[1]]*shifted[2][p[2]] for p in permutations(range(3)))
    rank = elimination([[H[i][j]-25*(i==j) for j in range(22)] for i in range(22)])
    need(det_shift==82944 and rank==3,"image bridge failed")
    trace = sum(Q[i][i] for i in range(3))
    second = sum(Q[i][i]*Q[j][j]-Q[i][j]*Q[j][i] for i,j in combinations(range(3),2))
    det_q = elimination(Q,True)
    root_det = sqrt_floor(det_q)
    need(root_det**2==det_q,"quotient determinant not square")
    bound = sqrt_floor(3*trace)
    solutions = [(t,(t*t-trace)//2,c) for t in range(-bound,bound+1) if (t*t-trace)%2==0
                 for c in (-root_det,root_det) if ((t*t-trace)//2)**2-2*t*c==second]
    need(solutions==[(-19,-25,187),(19,-25,-187)],"quotient root coefficient control")
    t,s,c = solutions[1]
    L = multiply([[t*Q[i][j]+c*(i==j) for j in range(3)] for i in range(3)],
                 inverse([[Q[i][j]+s*(i==j) for j in range(3)] for i in range(3)]))
    need(multiply(L,L)==Q and all(v.denominator==1 for row in L for v in row),"derived quotient root failed")
    L = [[int(v) for v in row] for row in L]
    classes = [next(a for a,group in enumerate(groups) if i in group) for i in range(22)]
    root = [[Fraction(5*(i==j))+Fraction(L[classes[i]][classes[j]]-5*(classes[i]==classes[j]),len(groups[classes[j]]))
             for j in range(22)] for i in range(22)]
    need(all(root[i][j]==root[j][i] for i in range(22) for j in range(22)) and multiply(root,root)==H,
         "full rational symmetric positive control")
    scale = lcm(*map(len,groups))
    scaled = [[v*scale for v in row] for row in root]
    need(all(v.denominator==1 for row in scaled for v in row),"wrong root scale")
    scaled = [[int(v) for v in row] for row in scaled]
    cases = sorted([[k,a,4*a,(4*a)%9] for a in range(10) for k in range(4) if 2*a+k==9])
    need(len(cases)==2 and all(not any(9*z==v[2] for z in range(5)) for v in cases),"equitable incidence survivor")
    root_trace = sum(root[i][i] for i in range(22))
    need(root_trace.denominator==1,"fractional root trace")
    return {"mechanism":"equitable_degree_partition","quotient":Q,"quotient_gram":list(map(len,groups)),
            "det_quotient_minus25I":det_shift,"rank_H_minus25I":rank,"incidence_cases":cases,
            "rational_root_quotient":L,"rational_root_scale":scale,"rational_root_scaled_matrix":scaled,
            "rational_root_trace":int(root_trace)}


def controls(fixtures):
    need(elimination([[0,1],[2,3]],True)==-2 and elimination([[1,2],[2,4]],True)==0,"determinant controls")
    need(elimination([[0,1],[2,3]])==2 and elimination([[1,2],[2,4]])==1,"rank controls")
    rows = Path(__file__).with_name("baseline21.rows").read_text().split()
    need(len(rows)==21 and all(len(row)==21 and set(row)<={"0","1"} for row in rows),"bad baseline")
    R = [[int(c) for c in row] for row in rows]
    B = [[1-R[i][j]-(i==j) for j in range(21)] for i in range(21)]
    need(all(R[i][i]==0 and R[i][j]==R[j][i] for i in range(21) for j in range(21)),"baseline symmetry")
    hist = Counter(map(sum,R))
    maxima = [max(sum(A[i][k]*A[j][k] for k in range(21)) for i,j in combinations(range(21),2) if A[i][j])
              for A in (R,B)]
    need(hist=={8:4,9:16,10:1} and maxima==[3,6],"baseline differs")
    allowed = [len(s) for size in range(4) for s in combinations_with_replacement((0,),size) if len(s)<=2]
    pairs = list(combinations(range(22),2))
    signed = []
    need(len(fixtures)==2,"wrong signed fixture families")
    for histogram,item in zip(HISTOGRAMS,fixtures):
        need(tuple(item["histogram"])==histogram,"wrong signed histogram")
        degrees = [d for d,n in zip((8,9,10),histogram) for _ in range(n)]
        need(len(item["red_masks"])==len(set(item["red_masks"]))==24,"wrong fixture count")
        for mask in item["red_masks"]:
            need(isinstance(mask,int) and 0<=mask<(1<<231),"bad control mask")
            A = [[0]*22 for _ in range(22)]
            for bit,(i,j) in enumerate(pairs):
                A[i][j]=A[j][i]=(mask>>bit)&1
            need(list(map(sum,A))==degrees,"control degrees differ")
            B22 = [[int(i!=j)-A[i][j] for j in range(22)] for i in range(22)]
            defect = [[0]*22 for _ in range(22)]
            for i,j in pairs:
                value = 3-sum(A[i][k]*A[j][k] for k in range(22)) if A[i][j] else 6-sum(B22[i][k]*B22[j][k] for k in range(22))
                defect[i][j]=defect[j][i]=value
            K = [[2*A[i][j]+(2*degrees[i]-17)*(i==j) for j in range(22)] for i in range(22)]
            for i in range(22):
                triangles = sum(A[i][j]*A[i][k]*A[j][k]+B22[i][j]*B22[i][k]*B22[j][k]
                                for j,k in pairs if i!=j and i!=k)
                need(sum(defect[i])==3*degrees[i]+6*(21-degrees[i])-2*triangles,"literal triangle row")
                need(sum(defect[i])==sum(degrees)-294+38*degrees[i]-degrees[i]**2-
                     2*sum(A[i][j]*degrees[j] for j in range(22)),"literal incident row")
                for j in range(22):
                    expected = (2*degrees[i]-17)**2+4*degrees[i] if i==j else 4*(degrees[i]+degrees[j]-14)-4*defect[i][j]
                    need(sum(K[i][k]*K[j][k] for k in range(22))==expected,"literal square row product")
            need(sum(map(sum,defect))-histogram[1]==8,"wrong signed surplus")
        signed.append({"histogram":list(histogram),"red_masks":item["red_masks"],"graphs":24,
                       "incident_identity_checks":528,"square_identity_entries":11616})
    return {"determinant_controls":[-2,0],"rank_controls":[2,1],"two_center_weights":allowed,
            "baseline21_red_edges":sum(map(sum,R))//2,"baseline21_degree_histogram":[hist[d] for d in (8,9,10)],
            "baseline21_max_pages":maxima,"signed":signed}


def compute_histogram(histogram):
    global DEGREE
    DEGREE = [d for d,n in zip((8,9,10),histogram) for _ in range(n)]
    candidates,raw_counts,all_profiles = domain()
    profiles = sorted(all_profiles,key=lambda p:(len(p),p))
    indices = {p:i for i,p in enumerate(profiles)}
    metadata = [{"types":[list(x) for x in p],"forms":0,"fixed_type_labeled_cores":0,
                 "all_ordered_type_cores":raw_counts[p]} for p in profiles]
    records,full,squares = [],[],[]
    for key in sorted(candidates,key=lambda x:(len(x[0]),x)):
        normalized,F,H = normalize(labeled_defect(*candidates[key]))
        need(normalized==key,"domain normalization disagrees")
        value,orbit = elimination(H,True),orbit_size(key)
        root = sqrt_floor(value)
        index = indices[key[0]]
        records.append([index,list(key[1]),orbit,value,root,sha256(serialize([F,H])).hexdigest()])
        full.append({"histogram":list(histogram),"profile":[list(x) for x in key[0]],"weights":list(key[1]),"F":F,"H":H})
        metadata[index]["forms"] += 1
        metadata[index]["fixed_type_labeled_cores"] += orbit
        if root*root==value:
            squares.append({"profile_index":index,"weights":list(key[1]),"certificate":certificate(F,H)})
    need(len(metadata)==51 and len(records)==(768 if histogram==(7,10,5) else 343) and
         len(squares)==(0 if histogram==(7,10,5) else 3),"census mismatch")
    return {"degree_histogram":list(histogram),"red_edges":sum(DEGREE)//2,"incident_parity_surplus":8,
            "total_defect":(8+histogram[1])//2,"profiles":metadata,"records":records,"square_cases":squares},full


def compare(expected,actual):
    need(serialize(expected)==serialize(actual),"complete entry-level certificate differs")


def compare_matrices(author,separate):
    need(len(author)==len(separate)==1111,"wrong full matrix count")
    for a,b in zip(author,separate):
        need(set(a)==set(b) and a["histogram"]==b["histogram"] and a["profile"]==b["profile"] and a["weights"]==b["weights"],"wrong full matrix key")
        need(a["F"]==b["F"] and a["H"]==b["H"],"full matrix entries differ")


def corruptions(expected,actual,full):
    mutations = [
        ("missing form",lambda x:x["histograms"][0]["records"].pop()),
        ("duplicate form",lambda x:x["histograms"][1]["records"].append(deepcopy(x["histograms"][1]["records"][0]))),
        ("wrong center weight",lambda x:x["histograms"][0]["records"][-1][1].__setitem__(0,99)),
        ("wrong orbit",lambda x:x["histograms"][0]["records"][0].__setitem__(2,99)),
        ("wrong determinant",lambda x:x["histograms"][0]["records"][0].__setitem__(3,0)),
        ("wrong floor root",lambda x:x["histograms"][0]["records"][0].__setitem__(4,0)),
        ("wrong matrix digest",lambda x:x["histograms"][1]["records"][0].__setitem__(5,"0"*64)),
        ("wrong histogram",lambda x:x["histograms"][0].__setitem__("degree_histogram",[5,16,1])),
        ("omitted profile",lambda x:x["histograms"][1]["profiles"].pop()),
        ("missing square",lambda x:x["histograms"][1]["square_cases"].pop()),
        ("wrong plane rank",lambda x:x["histograms"][1]["square_cases"][0]["certificate"].__setitem__("rank_H_minus33I",19)),
        ("wrong norm residue",lambda x:x["histograms"][1]["square_cases"][1]["certificate"].__setitem__("primitive_norm_mod9_solutions",1)),
        ("wrong image rank",lambda x:x["histograms"][1]["square_cases"][2]["certificate"].__setitem__("rank_H_minus25I",4)),
        ("false divisible incidence",lambda x:x["histograms"][1]["square_cases"][2]["certificate"]["incidence_cases"][0].__setitem__(2,18)),
        ("wrong quotient",lambda x:x["histograms"][1]["square_cases"][2]["certificate"]["quotient"][0].__setitem__(0,98)),
        ("wrong rational root",lambda x:x["histograms"][1]["square_cases"][2]["certificate"]["rational_root_scaled_matrix"][0].__setitem__(0,0)),
        ("changed signed mask",lambda x:x["controls"]["signed"][0]["red_masks"].__setitem__(0,0)),
    ]
    rejected = []
    for label,mutate in mutations:
        candidate = deepcopy(expected);mutate(candidate)
        try:compare(candidate,actual)
        except RuntimeError:rejected.append(label)
        else:raise RuntimeError("accepted corrupt certificate:"+label)
    forged = deepcopy(full)
    forged[0]["F"][0][0]=1
    try:compare_matrices(forged,full)
    except RuntimeError:rejected.append("full matrix loop")
    else:raise RuntimeError("accepted corrupt full matrix")
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected",type=Path,default=Path(__file__).with_name("slack8_remaining_expected.json"))
    parser.add_argument("--matrices",type=Path,help="private author matrices compared in every entry")
    args = parser.parse_args()
    results,full = [],[]
    for histogram in HISTOGRAMS:
        result,matrices = compute_histogram(histogram)
        results.append(result);full.extend(matrices)
    expected = json.loads(args.expected.read_text())
    actual = {"agent":"six-books-1","role":"researcher","record_fields":
              ["profile_index","center_edge_weights","fixed_type_orbit_size","det_H","floor_sqrt_det","F_H_sha256"],
              "histograms":results,"controls":controls(expected["controls"]["signed"])}
    compare(expected,actual)
    if args.matrices:
        compare_matrices(json.loads(args.matrices.read_text()),full)
    rejected = corruptions(expected,actual,full)
    print(json.dumps({"complete":True,"separate_domain":"ordered compositions and unit-edge multisets",
                      "profiles":[len(x["profiles"]) for x in results],"forms":[len(x["records"]) for x in results],
                      "all_ordered_type_cores":[sum(p["all_ordered_type_cores"] for p in x["profiles"]) for x in results],
                      "positive_nonsquare":1108,"square_cases":3,"adjacency_survivors":0,
                      "full_F_H_entry_comparison":args.matrices is not None,"corruptions_rejected":rejected}))


if __name__=="__main__":
    main()
