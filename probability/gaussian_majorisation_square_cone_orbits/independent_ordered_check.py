#!/usr/bin/env python3
"""Reconstruct prefix orders, then check every pair of upper sets exactly.

Imports neither verify.py nor verify_ordered_weights.py. Signed matrices,
repeated polynomial multiplication, breadth-first enumeration, and direct
intersection counts replace the constructor's algorithms. Algorithmic
independence here does not mean independent authorship or peer review.
"""
from pathlib import Path
import argparse
import hashlib
import json

N = 48
A = ((1,0,1),(0,1,1),(-1,0,1),(0,-1,1))
B = ((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1))


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def matrices():
    out = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if len({i,j,k}) != 3:
                    continue
                for bits in range(8):
                    m = [[0]*3 for _ in range(3)]
                    for row,col in enumerate((i,j,k)):
                        m[row][col] = 1 if bits >> (2-row) & 1 else -1
                    out.append(tuple(tuple(row) for row in m))
    return out


def shifted_monomial(powers):
    polynomial = {(0,0,0):1}
    for axis,power in enumerate(powers):
        need(0 <= power <= (2,4,6)[axis], "Uncleared or out-of-range exponent")
        for _ in range(power):
            result = dict(polynomial)
            for key,value in polynomial.items():
                other = list(key)
                other[axis] += 1
                other = tuple(other)
                result[other] = result.get(other,0) + value
            polynomial = result
    return polynomial


def coefficient_data(points, group):
    data = []
    for matrix in group:
        row = []
        for point in points:
            e = [sum(point[i]*matrix[i][j] for i in range(3)) for j in range(3)]
            row.append(shifted_monomial((1+e[0],2+e[0]+e[1],3+sum(e))))
        data.append(row)
    return data


def rebuild_order(points, group):
    data = coefficient_data(points, group)
    keys = [(i,j,k) for i in range(3) for j in range(5) for k in range(7)]
    rows = []
    for lower in range(N):
        mask = 0
        for upper in range(N):
            valid = True
            for key in keys:
                running = 0
                for direction in range(4):
                    running += (data[upper][direction].get(key,0)
                                - data[lower][direction].get(key,0))
                    if running < 0:
                        valid = False
                        break
                if not valid:
                    break
            if valid:
                mask |= 1 << upper
        rows.append(mask)
    return rows


def audit_order(rows):
    need(len(rows) == N, "Wrong number of order rows")
    for lower,row in enumerate(rows):
        need(isinstance(row,int) and 0 <= row < (1 << N), "Invalid order bit mask")
        need(row >> lower & 1, "Missing reflexivity")
        for upper in range(N):
            if row >> upper & 1:
                need(lower == upper or not (rows[upper] >> lower & 1), "Order cycle")
                need(rows[upper] & ~row == 0, "Missing transitive edge")


def breadth_first_upper_sets(rows):
    seen,queue = {0},[0]
    for s in queue:
        for vertex in range(N):
            bit = 1 << vertex
            if s & bit == 0 and rows[vertex] & ~(s|bit) == 0:
                new = s|bit
                if new not in seen:
                    seen.add(new)
                    queue.append(new)
    return sorted(seen)


def audit():
    raw = Path(__file__).with_name("ORDERED_CERTIFICATE.json").read_bytes()
    cert = json.loads(raw)
    need(cert["schema"] == "square-cone-ordered-weights-v1", "Unknown schema")
    need(cert["group_size"] == N, "Wrong group size")
    need(cert["points_A"] == [list(p) for p in A]
         and cert["points_B"] == [list(p) for p in B], "Wrong centers")
    need(cert["weight_order_A"] == cert["weight_order_B"] == [0,1,2,3],
         "Wrong directional order")
    need(cert["prefix_generators"] == [[1]*k+[0]*(4-k) for k in range(1,5)],
         "Wrong cone generators")
    need(cert["clearing_monomial_powers"] == [1,2,3]
         and cert["coefficient_degree_box"] == [2,4,6], "Wrong polynomial domain")
    group = matrices()
    index = {matrix:i for i,matrix in enumerate(group)}
    need(len(index) == N, "Signed-matrix enumeration failed")
    negative = [index[tuple(tuple(-x for x in row) for row in m)] for m in group]
    need(all(negative[negative[i]] == i and negative[i] != i for i in range(N)),
         "Antipode is not a fixed-point-free involution")
    orders = {}
    for name,points in (("A",A),("B",B)):
        rows = rebuild_order(points, group)
        audit_order(rows)
        need(rows == cert["orders"][name], "An order entry differs from its definition")
        orders[name] = rows

    aa = breadth_first_upper_sets(orders["A"])
    bb = breadth_first_upper_sets(orders["B"])
    opposite_b = [sum(1 << negative[i] for i in range(N) if s >> i & 1) for s in bb]
    hist = {}
    minimum = N
    digest = hashlib.sha256()
    for s in aa:
        for t,opposite in zip(bb,opposite_b):
            gap = (s&t).bit_count() - (s&opposite).bit_count()
            need(gap >= 0, "The universal correlation fails")
            minimum = min(minimum,gap)
            hist[gap] = hist.get(gap,0) + 1
            digest.update(bytes([gap+N]))

    # A corrupt certificate reversing a strict edge must be rejected.
    invalid = list(orders["A"])
    i,j = next((i,j) for i in range(N) for j in range(N)
               if i != j and invalid[i] >> j & 1)
    invalid[j] |= 1 << i
    rejected = False
    try:
        audit_order(invalid)
    except RuntimeError:
        rejected = True
    need(rejected, "A cyclic comparison was accepted")
    return {
        "status":"ORDERED_WEIGHT_ALL_UPPER_SETS_CROSSCHECK_PASS",
        "certificate_sha256":hashlib.sha256(raw).hexdigest(),
        "complete_order_entries_reconstructed":2*N*N,
        "ordered_pairs":{name:sum(row.bit_count() for row in rows)
                         for name,rows in orders.items()},
        "A_upper_sets":len(aa), "B_upper_sets":len(bb),
        "upper_set_pairs":len(aa)*len(bb), "minimum_correlation_gap":minimum,
        "correlation_gap_histogram":hist, "all_pair_digest":digest.hexdigest(),
        "invalid_comparison_rejected":rejected,
        "trust_boundary":"Separate exact polynomial expansion, full order reconstruction, and all-pairs enumeration. The universal Gaussian and geometric transfer is the written author proof; not peer review or formalization.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = encoded(audit())
    if args.check:
        need(result == Path(__file__).with_name("ORDERED_INDEPENDENT_EXPECTED.json").read_bytes(),
             "Independent audit record differs")
        print("ORDERED_WEIGHT_ALL_UPPER_SETS_CROSSCHECK_PASS",hashlib.sha256(result).hexdigest())
    else:
        print(result.decode(),end="")


if __name__ == "__main__":
    main()
