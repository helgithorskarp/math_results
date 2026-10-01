"""Exact generator for punctured F617, order-eight, log-defect constraints.

The solver is not imported here. Coordinates are one-based CNF variables.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path

P, M, ROOT = 617, 77, 3


def require(condition, message):
    if not condition:
        raise ValueError(message)


def field_edges():
    require(all(P % d for d in range(2, 25)), "617 must be prime")
    ids = [-1] * P
    for exponent in range(P-1):
        x = pow(ROOT, exponent, P)
        require(ids[x] == -1, "3 must be primitive")
        ids[x] = exponent % M
    require(ids[0] == -1 and all(x >= 0 for x in ids[1:]), "incomplete quotient")
    spacing_one = set()
    for a in range(P):
        terms = [(a+j) % P for j in range(7)]
        if 0 not in terms:
            spacing_one.add(tuple(sorted({ids[x] for x in terms})))
    # Multiplication by a nonzero difference adds its quotient coordinate.
    return sorted({tuple(sorted({(x+s) % M for x in edge}))
                   for edge in spacing_one for s in range(M)},
                  key=lambda edge: (len(edge), edge))


def counter(n, bound, first_input, first_aux):
    """Forward prefix counter; satisfiable iff at most bound inputs are true.

    s[i,j] (1 <= i <= n, 1 <= j <= bound+1) is forced true when
    at least j of the first i inputs are true. Reverse implications are
    unnecessary. Impossible prefix counts are explicitly false.
    """
    require(1 <= n <= 100 and 0 <= bound < n, "invalid counter dimensions")
    width = bound+1
    def s(i, j):
        return first_aux + (i-1)*width + j-1
    clauses = []
    for i in range(1, n+1):
        x = first_input + i-1
        for j in range(1, width+1):
            if j > i:
                clauses.append([-s(i, j)])
            if i > 1:
                clauses.append([-s(i-1, j), s(i, j)])
            if j == 1:
                clauses.append([-x, s(i, j)])
            elif i > 1:
                clauses.append([-x, -s(i-1, j-1), s(i, j)])
    clauses.append([-s(n, width)])
    return clauses, first_aux+n*width-1


def encoding(bound):
    require(0 <= bound < M, "invalid log-defect bound")
    edges = field_edges()
    clauses = []
    for edge in edges:
        vertices = [v+1 for v in edge]
        clauses.extend([vertices, [-v for v in vertices]])
    # Every odd cyclic binary word has an equal pair. Rotation and color
    # complement move a pair to y[0]=y[1]=0 without changing defect count.
    clauses.extend([[-1], [-2]])
    for i in range(M):
        x, y, z = i+1, (i+1) % M+1, M+i+1
        # z iff x == y, checked against all eight truth assignments.
        clauses.extend([[x, y, z], [-x, -y, z],
                        [x, -y, -z], [-x, y, -z]])
    count_clauses, nv = counter(M, bound, M+1, 2*M+1)
    clauses.extend(count_clauses)
    meta = {"p": P, "index": M, "subgroup_order": 8,
            "equal_bound": bound, "variables": nv,
            "clauses": len(clauses), "field_edges": len(edges),
            "rank_histogram": dict(sorted(collections.Counter(map(len, edges)).items())),
            "counter_clauses": len(count_clauses)}
    return clauses, meta


def write_cnf(path, bound):
    clauses, meta = encoding(bound)
    text = f"p cnf {meta['variables']} {len(clauses)}\n"
    text += "".join(" ".join(map(str, c))+" 0\n" for c in clauses)
    path.write_text(text)
    meta["cnf_sha256"] = hashlib.sha256(text.encode()).hexdigest()
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("output", type=Path)
    ap.add_argument("--bound", type=int, default=9)
    args = ap.parse_args()
    print(json.dumps(write_cnf(args.output, args.bound), sort_keys=True))


if __name__ == "__main__":
    main()
