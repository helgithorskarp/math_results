"""Exact controls for the written regular page-deficit identities."""
import argparse
import hashlib
import json
from pathlib import Path


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(a)))
             for j in range(len(a))] for i in range(len(a))]


def matrix_controls():
    n = 22
    a = [[int(i != j and (i - j) % n in (1, 2, 3, 4, 11, 18, 19, 20, 21))
          for j in range(n)] for i in range(n)]
    records = []
    for case in range(24):
        if any(sum(row) != 9 for row in a):
            raise ValueError("degree-preserving control failed")
        a2 = mm(a, a)
        d = [[5 * (i == j) - a[i][j] + 4 - a2[i][j] for j in range(n)] for i in range(n)]
        if any(d[i][i] != 0 or sum(d[i]) != 3 for i in range(n)):
            raise ValueError("deficit diagonal/row identity")
        if mm(a, d) != mm(d, a):
            raise ValueError("commutation identity")
        for i in range(n):
            for j in range(i + 1, n):
                pages = sum((a[i][k] == a[i][j] == a[j][k])
                            for k in range(n) if k != i and k != j)
                if d[i][j] != (3 if a[i][j] else 6) - pages:
                    raise ValueError("literal deficit identity")
        energy = []
        for phase in range(3):
            x = [(i * 7 + phase * 5) % 13 - 6 for i in range(n)]
            lhs_minus = 3 * sum(t * t for t in x) - sum(x[i] * d[i][j] * x[j] for i in range(n) for j in range(n))
            lhs_plus = 3 * sum(t * t for t in x) + sum(x[i] * d[i][j] * x[j] for i in range(n) for j in range(n))
            rhs_minus = sum(d[i][j] * (x[i] - x[j]) ** 2 for i in range(n) for j in range(i + 1, n))
            rhs_plus = sum(d[i][j] * (x[i] + x[j]) ** 2 for i in range(n) for j in range(i + 1, n))
            if (lhs_minus, lhs_plus) != (rhs_minus, rhs_plus):
                raise ValueError("energy identity")
            energy.append([lhs_minus, lhs_plus])
        records.append({"case": case, "adjacency_sha256": hashlib.sha256(json.dumps(a).encode()).hexdigest(),
                        "nonnegative_deficits": all(t >= 0 for row in d for t in row),
                        "energy": energy})
        # Deterministic first legal switch in a rotating order; exact domain stays nine-regular.
        changed = False
        order = [(i + case) % n for i in range(n)]
        for u in order:
            for v in order:
                if not a[u][v]:
                    continue
                for w in order:
                    for z in order:
                        if len({u, v, w, z}) == 4 and a[w][z] and not a[u][w] and not a[v][z]:
                            for p, q, bit in ((u, v, 0), (w, z, 0), (u, w, 1), (v, z, 1)):
                                a[p][q] = a[q][p] = bit
                            changed = True
                            break
                    if changed:
                        break
                if changed:
                    break
            if changed:
                break
        if not changed:
            raise ValueError("no control switch")
    return records


def balance_controls():
    tested = 0
    for cap in range(1, 10):
        dp = {0: 0}
        for _ in range(12):
            new = {}
            for total, cost in dp.items():
                for load in range(cap + 1):
                    n = total + load
                    v = cost + load * (load - 1) // 2
                    new[n] = min(new.get(n, v), v)
            dp = new
        for total, value in dp.items():
            q, r = divmod(total, 12)
            if value != 12 * q * (q - 1) // 2 + r * q:
                raise ValueError("load balancing formula disagrees with capped DP")
            tested += 1
    return tested


def generate():
    return {"regular_matrix_controls": matrix_controls(), "balance_dp_entries": balance_controls(),
            "scope": "exact signed identity controls; no constructed valid nine-regular 22-point host"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = (json.dumps(generate(), sort_keys=True, separators=(",", ":")) + "\n").encode()
    args.output.write_bytes(raw)
    print(json.dumps({"structure_sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}, sort_keys=True))


if __name__ == "__main__":
    main()
