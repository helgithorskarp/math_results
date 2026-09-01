#!/usr/bin/env python3
"""Independent solver-free replay of the swap-closure certificate.

This checker imports none of the primary code (parts509.py, kfield.py, udg.py,
swap_certificate.py).  It parses the published coordinates into SymPy's
AlgebraicField Q(sqrt3, sqrt5, sqrt11), recomputes all unit pairs exactly,
enumerates completion points with a different algorithm (double-precision
screening of pairwise circle intersections followed by exact circumcentre
confirmation and exact rescans), decodes the base deletion colourings and the
certificate rows with its own decoder, and replays the coverage argument.

  python independent_check.py completion_points.json swap_certificate.json
"""
from __future__ import annotations
import base64, hashlib, json, math, sys, time
from collections import defaultdict
from pathlib import Path
import sympy
from sympy import QQ, sqrt, sympify

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'hadwiger_nelson_parts509_criticality'
if not (BASE / 'parts509.vtx').exists():
    BASE = Path.home() / 'math_results' / 'hadwiger_nelson_parts509_criticality'
N, K = 509, 4
ROW_BYTES = 127


def log(msg):
    print(msg, flush=True)


def split_pair(body):
    expr = body.replace('Sqrt[', 'sqrt(').replace(']', ')')
    depth = 0
    for i, ch in enumerate(expr):
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        elif ch == ',' and depth == 0:
            return expr[:i], expr[i + 1:]
    raise ValueError(body)


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    t0 = time.time()
    comp_path, cert_path = Path(sys.argv[1]), Path(sys.argv[2])
    Kf = QQ.algebraic_field(sqrt(3), sqrt(5), sqrt(11))
    exprs = []
    for line in (BASE / 'parts509.vtx').read_text().splitlines():
        s = line.strip()
        if s:
            a, b = split_pair(s[1:-1])
            exprs.append((sympify(a), sympify(b)))
    pts = [(Kf.from_sympy(sympy.sqrtdenest(a)), Kf.from_sympy(sympy.sqrtdenest(b))) for a, b in exprs]
    assert len(pts) == N and len(set(pts)) == N
    fl = [(float(a.evalf(30)), float(b.evalf(30))) for a, b in exprs]
    one = Kf.one
    log(f'parsed {N} points ({time.time()-t0:.0f}s)')

    def unit(p, q):
        dx = p[0] - q[0]
        dy = p[1] - q[1]
        return dx * dx + dy * dy == one

    edges = [(i, j) for i in range(N) for j in range(i + 1, N) if unit(pts[i], pts[j])]
    edge_hash = hashlib.sha256(''.join(f'{u} {v}\n' for u, v in edges).encode()).hexdigest()
    adj = [set() for _ in range(N)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    log(f'exact unit pairs: {len(edges)}, canonical edge sha256 {edge_hash} ({time.time()-t0:.0f}s)')

    # --- completion points by float screen + exact circumcentre ---------------
    cell = defaultdict(list)
    for i, (x, y) in enumerate(fl):
        cell[(math.floor(x), math.floor(y))].append(i)

    def near_unit(qx, qy, tol=1e-6):
        cx, cy = math.floor(qx), math.floor(qy)
        out = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for k in cell.get((cx + dx, cy + dy), ()):
                    if abs(math.hypot(fl[k][0] - qx, fl[k][1] - qy) - 1.0) < tol:
                        out.append(k)
        return out

    triples = set()
    near_tangent = 0
    for i in range(N):
        xi, yi = fl[i]
        for j in range(i + 1, N):
            xj, yj = fl[j]
            dx, dy = xj - xi, yj - yi
            d2 = dx * dx + dy * dy
            if d2 >= 4.0 - 1e-3:
                near_tangent += d2 <= 4.0 + 1e-3
                continue
            mx, my = (xi + xj) / 2, (yi + yj) / 2
            h = math.sqrt(1.0 - d2 / 4.0) / math.sqrt(d2)
            for s in (1, -1):
                qx, qy = mx - s * h * dy, my + s * h * dx
                for k in near_unit(qx, qy):
                    if k != i and k != j:
                        triples.add(tuple(sorted((i, j, k))))
    assert near_tangent == 0, 'near-tangent pairs would need exact handling'

    def circumcentre(a, b, c):
        ax, ay = a; bx, by = b; cx, cy = c
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        if d == Kf.zero:
            return None
        na, nb, nc = ax * ax + ay * ay, bx * bx + by * by, cx * cx + cy * cy
        return ((na * (by - cy) + nb * (cy - ay) + nc * (ay - by)) / d,
                (na * (cx - bx) + nb * (ax - cx) + nc * (bx - ax)) / d)

    points_by_key = {}
    vertex_keys = set(pts)
    for (i, j, k) in sorted(triples):
        q = circumcentre(pts[i], pts[j], pts[k])
        if q is None or not (unit(q, pts[i]) and unit(q, pts[j]) and unit(q, pts[k])):
            continue
        if q in points_by_key or q in vertex_keys:
            continue
        nb = frozenset(idx for idx in range(N) if unit(q, pts[idx]))
        assert {i, j, k} <= nb
        points_by_key[q] = nb
    q3_sets = set(points_by_key.values())
    hist = defaultdict(int)
    for nb in q3_sets:
        hist[len(nb)] += 1
    log(f'independent Q3: {len(q3_sets)} points, histogram {dict(sorted(hist.items()))} ({time.time()-t0:.0f}s)')

    comp = json.loads(comp_path.read_text())
    prim = {frozenset(r['neighbors']) for r in comp['points']}
    assert prim == q3_sets, 'completion-point families differ'
    assert len(prim) == len(comp['points']) == comp['q3_count']
    q4 = [tuple(sorted(nb)) for nb in q3_sets if len(nb) >= 4]
    log(f'completion points agree with the committed file; Q4 = {len(q4)}')

    # --- base deletion rows ----------------------------------------------------
    base = json.loads((BASE / 'certificate.json').read_text())
    payload = base64.b64decode(base['deletion_colorings_base64'], validate=True)
    assert hashlib.sha256(payload).hexdigest() == base['packed_deletion_colorings_sha256']
    assert len(payload) == N * ROW_BYTES

    def decode_row(raw, deleted):
        vals = [(b >> s) & 3 for b in raw for s in (0, 2, 4, 6)]
        row = []
        cur = 0
        for v in range(N):
            if v == deleted:
                row.append(-1)
            else:
                row.append(vals[cur])
                cur += 1
        return row

    def check_proper(row, deleted):
        for u, v in edges:
            if u != deleted and v != deleted and row[u] == row[v]:
                raise ValueError(f'monochromatic edge {(u, v)} with {deleted} deleted')

    rows = []
    for d in range(N):
        row = decode_row(payload[d * ROW_BYTES:(d + 1) * ROW_BYTES], d)
        check_proper(row, d)
        rows.append(row)
    log(f'base deletion rows verified ({time.time()-t0:.0f}s)')

    # --- certificate rows --------------------------------------------------------
    cert = json.loads(cert_path.read_text())
    assert cert['completion_points_sha256'] == sha256_file(comp_path)
    assert cert['edge_sha256'] == edge_hash
    fam_payload = base64.b64decode(cert['family_rows_base64'], validate=True)
    assert hashlib.sha256(fam_payload).hexdigest() == cert['packed_rows_sha256']
    sizes = cert['family_sizes']
    assert len(sizes) == N and len(fam_payload) == sum(sizes) * ROW_BYTES
    declared = {(tuple(sorted(s['q_neighbors'])), s['u']) for s in cert['swaps']}

    def short(row, nb, u):
        return len({row[w] for w in nb if w != u}) < K

    offset = 0
    covered_base = covered_family = 0
    uncovered = set()
    for u in range(N):
        fam = []
        for _ in range(sizes[u]):
            row = decode_row(fam_payload[offset:offset + ROW_BYTES], u)
            offset += ROW_BYTES
            check_proper(row, u)
            fam.append(row)
        for nb in q4:
            if short(rows[u], nb, u):
                covered_base += 1
            elif any(short(r, nb, u) for r in fam):
                covered_family += 1
            else:
                uncovered.add((nb, u))
    assert uncovered == declared, 'uncovered instances differ from declared swaps'
    per_point = defaultdict(int)
    for nb, u in declared:
        per_point[nb] += 1
    assert max(per_point.values(), default=0) <= 1
    log(json.dumps({
        'all_checks': True,
        'exact_unit_pairs': len(edges), 'q3_points': len(q3_sets), 'q4_points': len(q4),
        'instances': len(q4) * N, 'covered_by_base_rows': covered_base, 'covered_by_family_rows': covered_family,
        'declared_swaps': len(declared), 'max_swaps_per_point': max(per_point.values(), default=0),
        'certificate_sha256': sha256_file(cert_path), 'seconds': round(time.time() - t0),
    }, indent=2))


if __name__ == '__main__':
    main()
