#!/usr/bin/env python3
"""Independent solver-free replay of the two-point augmentation closure.

Imports none of the primary code.  Coordinates of the 509 Parts vertices are
parsed into SymPy's AlgebraicField Q(sqrt3, sqrt5, sqrt11); the completion
points are rebuilt from their rational coefficient vectors in the same field.
Point-vertex and point-point unit distances are decided exactly: a pair is
rejected only if its squared distance differs from 1 under two ring
homomorphisms K -> F_p (p prime with 3, 5, 11 quadratic residues; a true unit
pair can never be rejected because homomorphisms preserve equality), and every
surviving pair is confirmed or refuted by exact AlgebraicField arithmetic.  The
coefficient vectors used by the homomorphisms are checked against the
AlgebraicField elements.  Rows are decoded with an own decoder; the pair
coverage is replayed with pure Python bitmask arithmetic; triple witnesses are
checked directly.

  python independent_pair_check.py completion_points.json pair_certificate.json
"""
from __future__ import annotations
import base64, hashlib, itertools, json, sys, time
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import sympy
from sympy import QQ, sqrt, sympify, Rational

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'hadwiger_nelson_parts509_criticality'
if not (BASE / 'parts509.vtx').exists():
    BASE = Path.home() / 'math_results' / 'hadwiger_nelson_parts509_criticality'
SW = HERE.parent / 'hadwiger_nelson_parts509_swap_closure'
if not (SW / 'swap_certificate.json').exists():
    SW = Path.home() / 'math_results' / 'hadwiger_nelson_parts509_swap_closure'
N, K = 509, 4
ROW_BYTES = 127
RADICALS = [sympy.Integer(1), sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165)]  # basis index = bitmask over (3, 5, 11)


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
    one = Kf.one

    def unit(p, q):
        dx = p[0] - q[0]
        dy = p[1] - q[1]
        return dx * dx + dy * dy == one

    edges = [(i, j) for i in range(N) for j in range(i + 1, N) if unit(pts[i], pts[j])]
    edge_hash = hashlib.sha256(''.join(f'{u} {v}\n' for u, v in edges).encode()).hexdigest()
    log(f'parsed {N} points, {len(edges)} exact unit pairs, edge sha256 {edge_hash} ({time.time()-t0:.0f}s)')

    comp = json.loads(comp_path.read_text())

    def from_coeffs(strs):
        expr = sum(Rational(Fraction(s).numerator, Fraction(s).denominator) * r for s, r in zip(strs, RADICALS))
        return Kf.from_sympy(sympify(expr))

    qpts = [(from_coeffs(r['x']), from_coeffs(r['y'])) for r in comp['points']]
    nq = len(qpts)
    assert len(set(qpts)) == nq and not (set(qpts) & set(pts))

    # --- coefficient vectors in the radical basis, checked against the field elements
    basis_elems = [Kf.from_sympy(r) for r in RADICALS]

    # The field elements are polynomials in the primitive element (power basis,
    # ANP.to_list gives the coefficients in decreasing degree).  The eight radical
    # basis elements form an invertible 8x8 matrix over Q in that basis, so the
    # radical coefficient vector of an element is a rational linear solve, and
    # every conversion is confirmed by rebuilding the element from the vector.
    def power_coeffs(el):
        lst = [Fraction(int(c.numerator), int(c.denominator)) for c in el.to_list()]
        return [Fraction(0)] * (8 - len(lst)) + lst

    Mrad = sympy.Matrix([[Rational(c.numerator, c.denominator) for c in power_coeffs(b)] for b in basis_elems]).T
    Minv = Mrad.inv()

    def coeff_vector(elem):
        v = Minv * sympy.Matrix([Rational(c.numerator, c.denominator) for c in power_coeffs(elem)])
        vec = [Fraction(int(x.p), int(x.q)) for x in v]
        recon = sum((Kf.from_sympy(Rational(c.numerator, c.denominator)) * b for c, b in zip(vec, basis_elems)), Kf.zero)
        assert recon == elem, 'coefficient vector does not reproduce the field element'
        return vec

    vvec = [(coeff_vector(x), coeff_vector(y)) for x, y in pts]
    qvec = []
    for r, (qx, qy) in zip(comp['points'], qpts):
        vx = [Fraction(v) for v in r['x']]
        vy = [Fraction(v) for v in r['y']]
        for vec, elem in ((vx, qx), (vy, qy)):
            recon = sum((Kf.from_sympy(Rational(v.numerator, v.denominator)) * b for v, b in zip(vec, basis_elems)), Kf.zero)
            assert recon == elem
        qvec.append((vx, vy))
    log(f'coefficient vectors of all {N + nq} points checked against the field elements ({time.time()-t0:.0f}s)')

    # --- exact rejection screen through ring homomorphisms K -> F_p -------------
    import numpy as np

    def sqrt_mod(a, p):
        assert pow(a, (p - 1) // 2, p) == 1
        if p % 4 == 3:
            r = pow(a, (p + 1) // 4, p)
        else:  # Tonelli-Shanks
            q, s = p - 1, 0
            while q % 2 == 0:
                q //= 2; s += 1
            z = 2
            while pow(z, (p - 1) // 2, p) != p - 1:
                z += 1
            m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
            while t != 1:
                i, t2 = 0, t
                while t2 != 1:
                    t2 = t2 * t2 % p; i += 1
                b = pow(c, 1 << (m - i - 1), p)
                m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
        assert r * r % p == a % p
        return r

    def homomorphism_primes(count):
        out, p = [], (1 << 31) - 1
        while len(out) < count:
            if sympy.isprime(p) and all(pow(a, (p - 1) // 2, p) == 1 for a in (3, 5, 11)):
                out.append(p)
            p -= 2
        return out

    def images(vecs, p):
        r3, r5, r11 = sqrt_mod(3, p), sqrt_mod(5, p), sqrt_mod(11, p)
        rad = [1, r3, r5, r3 * r5 % p, r11, r3 * r11 % p, r5 * r11 % p, r3 * r5 * r11 % p]
        def img(vec):
            tot = 0
            for c, rr in zip(vec, rad):
                assert c.denominator % p != 0
                tot = (tot + c.numerator * pow(c.denominator, -1, p) % p * rr) % p
            return tot
        return np.array([[img(x), img(y)] for x, y in vecs], dtype=np.int64)

    primes = homomorphism_primes(2)
    cand_qv = None
    cand_qq = None
    for p in primes:
        V = images(vvec, p)
        Q = images(qvec, p)
        # squared distances mod p (all entries < p < 2^31, so int64 products and sums do not overflow)
        dx = (Q[:, None, 0] - V[None, :, 0]) % p
        dy = (Q[:, None, 1] - V[None, :, 1]) % p
        d2 = (dx * dx % p + dy * dy % p) % p
        m = d2 == 1
        cand_qv = m if cand_qv is None else (cand_qv & m)
        dx = (Q[:, None, 0] - Q[None, :, 0]) % p
        dy = (Q[:, None, 1] - Q[None, :, 1]) % p
        d2 = (dx * dx % p + dy * dy % p) % p
        m = d2 == 1
        cand_qq = m if cand_qq is None else (cand_qq & m)
    log(f'homomorphism screen with primes {primes}: {int(cand_qv.sum())} point-vertex and {int(np.triu(cand_qq, 1).sum())} point-point candidates ({time.time()-t0:.0f}s)')
    qnb = []
    for a in range(nq):
        nb = tuple(i for i in np.nonzero(cand_qv[a])[0].tolist() if unit(qpts[a], pts[i]))
        qnb.append(nb)
    assert all(len(nb) >= 3 for nb in qnb)
    assert qnb == [tuple(r['neighbors']) for r in comp['points']], 'point-vertex incidences differ from the committed lists'
    qq = set()
    for a, b in zip(*np.nonzero(np.triu(cand_qq, 1))):
        if unit(qpts[int(a)], qpts[int(b)]):
            qq.add((int(a), int(b)))
    log(f'{nq} completion points: incidences agree; {len(qq)} exact point-point unit pairs ({time.time()-t0:.0f}s)')
    qadj = [set() for _ in range(nq)]
    for a, b in qq:
        qadj[a].add(b); qadj[b].add(a)

    def decode_row(raw, deleted):
        vals = [(b >> s) & 3 for b in raw for s in (0, 2, 4, 6)]
        it = iter(vals)
        return [-1 if v in deleted else next(it) for v in range(N)], vals

    def check_proper(row, deleted):
        for u, v in edges:
            if u not in deleted and v not in deleted and row[u] == row[v]:
                raise ValueError(f'monochromatic edge {(u, v)} with {deleted} deleted')

    base = json.loads((BASE / 'certificate.json').read_text())
    payload = base64.b64decode(base['deletion_colorings_base64'], validate=True)
    assert hashlib.sha256(payload).hexdigest() == base['packed_deletion_colorings_sha256']
    assert len(payload) == N * ROW_BYTES
    rows = []
    for d in range(N):
        row, _ = decode_row(payload[d * ROW_BYTES:(d + 1) * ROW_BYTES], {d})
        check_proper(row, {d})
        rows.append(row)
    swap = json.loads((SW / 'swap_certificate.json').read_text())
    spayload = base64.b64decode(swap['family_rows_base64'], validate=True)
    assert hashlib.sha256(spayload).hexdigest() == swap['packed_rows_sha256']
    cert = json.loads(cert_path.read_text())
    assert cert['edge_sha256'] == edge_hash
    assert cert['completion_points_sha256'] == sha256_file(comp_path) == swap['completion_points_sha256']
    assert cert['swap_certificate_sha256'] == sha256_file(SW / 'swap_certificate.json')
    assert cert['q3q3_unit_pairs'] == len(qq)
    fpayload = base64.b64decode(cert['family_rows_base64'], validate=True)
    assert hashlib.sha256(fpayload).hexdigest() == cert['packed_rows_sha256']
    assert len(fpayload) == sum(cert['family_sizes']) * ROW_BYTES
    assert len(spayload) == sum(swap['family_sizes']) * ROW_BYTES
    log(f'base rows verified; certificate hashes consistent ({time.time()-t0:.0f}s)')

    # --- coverage replay with bitmasks ------------------------------------------
    def free_mask(row, q, u):
        used = 0
        for w in qnb[q]:
            if w != u:
                used |= 1 << row[w]
        return 15 - used

    U = defaultdict(list)
    soff = foff = 0
    total_rows = 0
    declared_total = 0
    for u in range(N):
        fam = [rows[u]]
        for _ in range(swap['family_sizes'][u]):
            row, _ = decode_row(spayload[soff:soff + ROW_BYTES], {u})
            soff += ROW_BYTES
            check_proper(row, {u})
            fam.append(row)
        for _ in range(cert['family_sizes'][u]):
            row, _ = decode_row(fpayload[foff:foff + ROW_BYTES], {u})
            foff += ROW_BYTES
            check_proper(row, {u})
            fam.append(row)
        total_rows += len(fam)
        R = len(fam)
        masks = [[free_mask(row, q, u) for row in fam] for q in range(nq)]
        okbits = [sum(1 << r for r in range(R) if masks[q][r]) for q in range(nq)]
        uncovered = set()
        for q1 in range(nq):
            b1 = okbits[q1]
            for q2 in range(q1 + 1, nq):
                bits = b1 & okbits[q2]
                if bits and q2 in qadj[q1]:
                    for r in range(R):
                        if (bits >> r) & 1 and masks[q1][r] == masks[q2][r] and masks[q1][r] in (1, 2, 4, 8):
                            bits &= ~(1 << r)
                if not bits:
                    uncovered.add((q1, q2))
        assert uncovered == {tuple(p) for p in cert['declared_pairs'][u]}, f'vertex {u}: uncovered set differs from the declared instances'
        declared_total += len(uncovered)
        for p in uncovered:
            U[p].append(u)
        if u % 50 == 0:
            log(f'  u={u}: {len(uncovered)} uncovered pairs ({time.time()-t0:.0f}s)')
    hist = defaultdict(int)
    for s in U.values():
        hist[len(s)] += 1
    log(f'coverage replayed: {total_rows} colourings, {declared_total} declared instances, |U| histogram {dict(sorted(hist.items()))} ({time.time()-t0:.0f}s)')

    # --- triple witnesses ---------------------------------------------------------
    tpayload = base64.b64decode(cert['triple_rows_base64'], validate=True)
    assert hashlib.sha256(tpayload).hexdigest() == cert['packed_triple_rows_sha256']
    tw = cert['triple_witnesses']
    assert len(tpayload) == len(tw) * ROW_BYTES
    have = set()
    for i, w in enumerate(tw):
        A, D = tuple(w['A']), tuple(sorted(w['D']))
        Dset = set(D)
        row, vals = decode_row(tpayload[i * ROW_BYTES:(i + 1) * ROW_BYTES], Dset)
        qc = vals[N - 3:N - 1]
        check_proper(row, Dset)
        for q, c in zip(A, qc):
            assert all(row[w] != c for w in qnb[q] if w not in Dset), f'triple witness {A} {D}: point clash'
        if (A[0], A[1]) in qq:
            assert qc[0] != qc[1], f'triple witness {A} {D}: adjacent points coloured alike'
        have.add((A, D))
    needed = 0
    for A, s in U.items():
        if len(s) >= 3:
            for D in itertools.combinations(sorted(s), 3):
                needed += 1
                assert (A, D) in have, f'missing triple witness for {A} {D}'
    assert not cert['candidates_508']
    log(json.dumps({'all_checks': True, 'q3_points': nq, 'q3q3_unit_pairs': len(qq), 'colourings': total_rows,
                    'declared_instances': declared_total, 'pairs_with_nonempty_U': len(U),
                    'U_histogram': {str(k): v for k, v in sorted(hist.items())}, 'triple_instances_needed': needed,
                    'triple_witnesses_checked': len(tw), 'certificate_sha256': sha256_file(cert_path),
                    'seconds': round(time.time() - t0)}, indent=2))


if __name__ == '__main__':
    main()
