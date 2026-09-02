#!/usr/bin/env python3
"""Build or verify the certificate for the exact minimum order of a 5-chromatic subgraph of an
accumulative unit-distance graph A* = V ∪ P (V = Parts-509 vertices, P = added completion points).

Mathematics.  Let F ⊆ A* be the vertices u with A* − u 4-colourable (forced vertices: every
5-chromatic subgraph of A* contains u), R = A* \ F.  A set D ⊆ R is a killing set if A* − D is
4-colourable.  For X ⊆ R the subgraph F ∪ X is 5-chromatic iff X meets every killing set (if X misses
D then F ∪ X ⊆ A* − D is 4-colourable; if F ∪ X were 4-colourable then R \ X would be a killing set
missed by X).  Hence the minimum order of a 5-chromatic subgraph of A* is |F| + m, where m is the
minimum size of a set meeting every killing set, and for any subfamily H of killing sets
m ≥ min hitting set of H.  The certificate contains: exact coordinates of A* (K = Q(√3,√5,√11)),
a proper 4-colouring of A* − u for every u ∈ F, a proper 4-colouring of A* − D for every D in a
family H ⊆ killing sets, the value m* = min hitting set of H (recomputable exactly with --rc2/--milp,
or checked solver-free with --drat-card against a DRAT proof of the cardinality CNF), and an
optimal set X* with F ∪ X* not 4-colourable (pinned CNF hash, DRAT proof hash; --drat-final checks a
supplied proof).  The theorem certified: min order = |F| + m*, so in particular no 5-chromatic
subgraph of A* has fewer than |F| + m* vertices.

Closure constraint (field 'min_points').  The committed closures of the Parts graph (vertex-criticality,
delete-2-add-1, delete-3-add-2, delete-4-add-3) show that every 5-chromatic unit-distance graph with at most
508 vertices shares at most 504 vertices with V, hence contains at least 4 points outside V.  A 5-chromatic
subgraph H ⊆ A* with |H| ≤ 508 contains a vertex-critical 5-chromatic H' ⊇ F, and H' has at least 4 points
of P; so X = H \ F contains at least 4 points of P.  When min_points = 4 the certificate bounds the hitting
sets X with |X ∩ P| ≥ 4 only: if every such X has |X| ≥ m and |F| + m ≥ 509, no 5-chromatic subgraph of A*
has at most 508 vertices (the unconstrained minimum order is then exactly 509, attained by G itself).
With min_points = 0 the certificate gives the plain minimum order |F| + m.

Verification recomputes the complete unit-distance edge list of A* by exhaustive exact arithmetic
(all pairs), so the lower bound does not depend on any previously computed edge list.
"""
import argparse, hashlib, json, sys, time, importlib.util
from fractions import Fraction
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parent if (HERE.parent / 'hadwiger_nelson_parts509_criticality' / 'parts509.vtx').exists() else Path.home() / 'math_results'
K = 4
PRIMES = (3, 5, 11)

# ---------- exact arithmetic in K = Q(sqrt3, sqrt5, sqrt11): elements are 8 Fractions indexed by subset masks ----------
def f_mul(x, y):
    out = [Fraction(0)] * 8
    for sx, a in enumerate(x):
        if not a:
            continue
        for sy, b in enumerate(y):
            if not b:
                continue
            c = a * b
            common = sx & sy
            if common & 1: c *= 3
            if common & 2: c *= 5
            if common & 4: c *= 11
            out[sx ^ sy] += c
    return out

def f_sub(x, y):
    return [a - b for a, b in zip(x, y)]

def d2(p, q):
    dx = f_sub(p[0], q[0]); dy = f_sub(p[1], q[1])
    xx = f_mul(dx, dx); yy = f_mul(dy, dy)
    return [a + b for a, b in zip(xx, yy)]

ONE = [Fraction(1)] + [Fraction(0)] * 7

def parse(strs):
    return [Fraction(s) for s in strs]

def to_strings(x):
    return [str(a) for a in x]

def to_float(x):
    import math
    r = 0.0
    for m, a in enumerate(x):
        v = float(a)
        for bit in range(3):
            if (m >> bit) & 1:
                v *= math.sqrt(PRIMES[bit])
        r += v
    return r

# ---------- CNF helpers ----------
def pinned_cnf(verts, edges, tri):
    """Pinned proper-4-colouring CNF of the graph on `verts` (sorted list) with the given edges; triangle tri pinned to 0,1,2."""
    idx = {v: i for i, v in enumerate(verts)}
    var = lambda v, c: idx[v] * K + c + 1
    vs = set(verts)
    clauses = [[var(v, c) for c in range(K)] for v in verts]
    for a, b in edges:
        if a in vs and b in vs:
            for c in range(K):
                clauses.append([-var(a, c), -var(b, c)])
    for i, v in enumerate(tri):
        clauses.append([var(v, i)])
    return f'p cnf {len(verts)*K} {len(clauses)}\n' + ''.join(' '.join(map(str, cl)) + ' 0\n' for cl in clauses)

def atmost_seq(x, k, nv):
    """Sinz sequential counter: clauses forcing at most k of the literals x to be true; fresh variables start
    at nv + 1.  Returns (clauses, new nv)."""
    n = len(x)
    if k >= n:
        return [], nv
    if k == 0:
        return [[-l] for l in x], nv
    s = lambda i, j: nv + i * k + j + 1          # "at least j+1 of x_0..x_i are true"
    clauses = [[-x[0], s(0, 0)]]
    for j in range(1, k):
        clauses.append([-s(0, j)])
    for i in range(1, n):
        clauses.append([-x[i], s(i, 0)])
        clauses.append([-s(i - 1, 0), s(i, 0)])
        for j in range(1, k):
            clauses.append([-x[i], -s(i - 1, j - 1), s(i, j)])
            clauses.append([-s(i - 1, j), s(i, j)])
        clauses.append([-x[i], -s(i - 1, k - 1)])
    return clauses, nv + n * k

def cardinality_cnf(R, family, k, pool=(), min_points=0):
    """CNF: every set of the family is hit (clause per set), at most k of the |R| selector variables are true,
    and at least min_points of the selectors of `pool` are true (at most |pool| − min_points false).
    UNSAT ⟺ no hitting set of size ≤ k with ≥ min_points pool elements."""
    xvar = {v: i + 1 for i, v in enumerate(R)}
    n = len(R)
    if k >= n:
        return None
    clauses = [[xvar[v] for v in D] for D in family]
    c1, nv = atmost_seq([xvar[v] for v in R], k, n)
    clauses += c1
    if min_points > 0:
        pl = [xvar[v] for v in pool]
        assert min_points <= len(pl)
        c2, nv = atmost_seq([-l for l in pl], len(pl) - min_points, nv)
        clauses += c2
    return f'p cnf {nv} {len(clauses)}\n' + ''.join(' '.join(map(str, cl)) + ' 0\n' for cl in clauses)

def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()

def decision_opb(R, family, k, pool=(), min_points=0):
    """Pseudo-Boolean decision instance (OPB): x_v for v in R (x1.. in the order of R); every family set is hit;
    at least min_points of the pool selectors; at most k selectors in total.  UNSAT (VeriPB-checked RoundingSat
    proof) ⟺ no hitting set of size ≤ k with ≥ min_points pool elements."""
    var = {v: i + 1 for i, v in enumerate(R)}
    lines = [' '.join(f'+1 x{var[v]}' for v in sorted(D)) + ' >= 1 ;' for D in family]
    if min_points > 0:
        lines.append(' '.join(f'+1 x{var[v]}' for v in pool) + f' >= {min_points} ;')
    lines.append(' '.join(f'-1 x{var[v]}' for v in R) + f' >= {-k} ;')
    return f'* #variable= {len(R)} #constraint= {len(lines)} #equal= 0 intsize= 8\n' + '\n'.join(lines) + '\n'

# ---------- build ----------
def build(args):
    union = json.loads(Path(args.union).read_text())
    forced = json.loads(Path(args.forced).read_text())
    res = json.loads(Path(args.results).read_text())
    amb = json.loads(Path(args.ambient).read_text())
    spec = importlib.util.spec_from_file_location('parts509', REPO / 'hadwiger_nelson_parts509_criticality' / 'parts509.py')
    parts = importlib.util.module_from_spec(spec); spec.loader.exec_module(parts)
    V = parts.parse_points(REPO / 'hadwiger_nelson_parts509_criticality' / 'parts509.vtx')
    coords = {}
    for i, (x, y) in enumerate(V):
        coords[i] = (to_strings(x), to_strings(y))
    if args.points:
        # explicit exact coordinates of every vertex of A* (union_graph.py output: 'points' = [[x_strs, y_strs], ...])
        pts_file = json.loads(Path(args.points).read_text())
        for j, (xs, ys) in enumerate(pts_file['points']):
            if j < 509:
                assert (xs, ys) == (list(coords[j][0]), list(coords[j][1])), f'Parts vertex {j} coordinates differ'
            else:
                coords[j] = (xs, ys)
        provenance = pts_file.get('provenance')
    else:
        provenance = None
        comp = json.loads(Path(args.completion).read_text())
        for j, r in enumerate(comp['points']):
            coords[509 + j] = (r['x'], r['y'])
        if args.level2:
            l2 = json.loads(Path(args.level2).read_text())
            for r in l2['points']:
                coords[r['index']] = (r['x'], r['y'])
    star = sorted(union['start'])
    F = sorted(forced['forced']); R = res['R']
    assert sorted(F + R) == star and set(F) == set(res['F'])
    fam = res['family']
    min_points = int(res.get('min_points', 0))
    if 'constrained_minimum' in res:
        m = int(res['constrained_minimum'])
    else:
        m = len(res['X_star'])
    pool_free = sorted(v for v in R if v in set(union['added_points']))
    cert = {
        'description': 'exact minimum order of a 5-chromatic subgraph of A* = V ∪ P (see tie_union_certificate.py)',
        'field': 'Q(sqrt3,sqrt5,sqrt11); coordinates are 8 rationals indexed by subset masks of (3,5,11): bit0=sqrt3, bit1=sqrt5, bit2=sqrt11',
        'vertices': star,
        'coordinates': {str(v): coords[v] for v in star},
        'pool': sorted(union['added_points']),
        'forced': F,
        'forced_witness': {str(u): forced['witness'][str(u)] for u in F},
        'free': R,
        'family': [{'D': row['D'], 'witness': row['witness']} for row in fam],
        'min_points': min_points,
        'pool_free': pool_free,
        'minimum_hitting_set': m,
        'target': 509 - len(F),
        'optimal_sets': res.get('all_optimal_X', [res['X_star']] if 'X_star' in res else []),
        'X_star': res.get('X_star'),
        'pinned_triangle': res['pinned_triangle'],
        'final_cnf_sha256': res.get('final_cnf_sha256'),
        'final_proof_sha256': args.final_proof_sha,
        'final_proof_bytes': args.final_proof_bytes,
        'minimum_order': len(F) + m if min_points == 0 else None,
        'rc2_cross_check': res.get('rc2_cross_check'),
        'witness_convention': 'a witness colouring is a string of digits 0-3 over the surviving vertices in increasing ambient index',
        'search_history': res['history'],
        'provenance': provenance,
    }
    text = json.dumps(cert)
    Path(args.out).write_text(text)
    print(f'wrote {args.out}: |A*|={len(star)}, |F|={len(F)}, |R|={len(R)}, family {len(fam)}, min_points {min_points}, m*={m}, |F|+m*={len(F)+m}, sha256 {sha(text)[:16]}')

# ---------- verify ----------
def verify(args):
    t0 = time.time()
    cert = json.loads(Path(args.certificate).read_text())
    star = cert['vertices']; S = set(star)
    pts = {v: (parse(cert['coordinates'][str(v)][0]), parse(cert['coordinates'][str(v)][1])) for v in star}
    # cross-check the Parts vertices against the committed exact coordinates when available
    crit = REPO / 'hadwiger_nelson_parts509_criticality'
    if (crit / 'parts509.vtx').exists():
        spec = importlib.util.spec_from_file_location('parts509', crit / 'parts509.py')
        parts = importlib.util.module_from_spec(spec); spec.loader.exec_module(parts)
        V = parts.parse_points(crit / 'parts509.vtx')
        bad = sum(1 for v in star if v < 509 and (list(V[v][0]), list(V[v][1])) != (pts[v][0], pts[v][1]))
        print(f'(0) Parts vertices in A*: {sum(1 for v in star if v < 509)}; coordinate mismatches against parts509.vtx: {bad}')
        assert bad == 0
    # (1) exhaustive exact edge list of A*
    n = len(star)
    fl = [(to_float(pts[v][0]), to_float(pts[v][1])) for v in star]
    edges = []
    screened = 0
    for i in range(n):
        xi, yi = fl[i]
        for j in range(i + 1, n):
            dx = xi - fl[j][0]; dy = yi - fl[j][1]
            dd = dx * dx + dy * dy
            if abs(dd - 1.0) < 1e-6:
                screened += 1
                if d2(pts[star[i]], pts[star[j]]) == ONE:
                    edges.append((star[i], star[j]))
            # points closer than 1e-6 in the float screen and exactly at distance 1 are impossible to miss: the
            # coordinates are bounded (|x|,|y| < 8) so the double-precision error of dd is below 1e-12
    adj = {v: set() for v in star}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    print(f'(1) exact edge list of A*: {n} vertices, {len(edges)} unit-distance pairs ({screened} float candidates checked exactly) ({time.time()-t0:.0f}s)')
    edge_set = set(edges)

    def proper(colstr, verts):
        assert len(colstr) == len(verts)
        col = {v: int(c) for v, c in zip(verts, colstr)}
        assert all(0 <= c < K for c in col.values())
        for v in verts:
            cv = col[v]
            for w in adj[v]:
                if w in col and col[w] == cv:
                    return False
        return True
    # (2) forced vertices
    F = cert['forced']; R = cert['free']
    assert sorted(F + R) == sorted(star) and not (set(F) & set(R))
    for u in F:
        verts = [v for v in star if v != u]
        assert proper(cert['forced_witness'][str(u)], verts), f'forced witness for {u} improper'
    print(f'(2) forced vertices: {len(F)} witness colourings replayed (A* − u is 4-colourable for each) ; free part R = {len(R)} ({time.time()-t0:.0f}s)')
    # (3) killing sets
    Rset = set(R)
    fam = []
    for row in cert['family']:
        D = row['D']
        assert set(D) <= Rset and len(set(D)) == len(D)
        verts = [v for v in star if v not in set(D)]
        assert proper(row['witness'], verts), f'killing-set witness improper: {D}'
        fam.append(sorted(D))
    keys = set(frozenset(D) for D in fam)
    minimal = [D for D in fam if not any(k < frozenset(D) for k in keys)]
    print(f'(3) killing sets: {len(fam)} witness colourings replayed ({len(keys)} distinct, {len(minimal)} inclusion-minimal); sizes {min(map(len,fam))}..{max(map(len,fam))} ({time.time()-t0:.0f}s)')
    m = cert['minimum_hitting_set']
    min_points = int(cert.get('min_points', 0)); pool = cert.get('pool_free', [])
    assert set(pool) <= Rset and all(v >= 509 for v in pool)
    # every optimal set hits every killing set (so it is a hitting set of size m: upper bound on the family minimum)
    for X in cert['optimal_sets']:
        assert len(X) == m and set(X) <= Rset and all(set(X) & set(D) for D in fam) and len(set(X) & set(pool)) >= min_points
    print(f'    recorded minimum hitting set m* = {m} (hitting sets with at least {min_points} pool points; pool = {len(pool)} free points); '
          f'{len(cert["optimal_sets"])} recorded optimal hitting sets all hit the family')
    lb_status = 'recorded (solver-trusted)'
    if args.rc2 or args.milp:
        vals = {}
        if args.rc2:
            from pysat.examples.rc2 import RC2
            from pysat.formula import WCNF
            xvar = {v: i + 1 for i, v in enumerate(R)}
            w = WCNF()
            for D in minimal:
                w.append([xvar[v] for v in D])
            if min_points > 0:
                from pysat.card import CardEnc, EncType
                card = CardEnc.atleast(lits=[xvar[v] for v in pool], bound=min_points, top_id=len(R), encoding=EncType.seqcounter)
                for cl in card.clauses:
                    w.append(cl)
            for v in R:
                w.append([-xvar[v]], weight=1)
            t = time.time()
            with RC2(w, solver='cd19', adapt=True, exhaust=False, minz=False) as rc2:
                mdl = rc2.compute(); vals['RC2'] = rc2.cost
            print(f'    RC2 recomputed minimum hitting set: {vals["RC2"]} ({time.time()-t:.0f}s)')
        if args.milp:
            import numpy as np
            from scipy.optimize import milp, LinearConstraint, Bounds
            from scipy.sparse import lil_matrix
            xi = {v: i for i, v in enumerate(R)}
            A = lil_matrix((len(minimal) + 1, len(R)))
            for r, D in enumerate(minimal):
                for v in D:
                    A[r, xi[v]] = 1
            for v in pool:
                A[len(minimal), xi[v]] = 1
            lbv = np.ones(len(minimal) + 1); lbv[len(minimal)] = min_points
            t = time.time()
            resm = milp(c=np.ones(len(R)), constraints=LinearConstraint(A.tocsr(), lb=lbv), integrality=np.ones(len(R)), bounds=Bounds(0, 1), options={'mip_rel_gap': 0.0})
            vals['HiGHS'] = int(round(resm.fun))
            print(f'    HiGHS MILP recomputed minimum hitting set: {vals["HiGHS"]} ({time.time()-t:.0f}s)')
        assert all(v >= m for v in vals.values()), f'recomputed values {vals} below the recorded bound {m}'
        lb_status = 'recomputed exactly by ' + ', '.join(f'{k}={v}' for k, v in vals.items()) + (' (equal)' if all(v == m for v in vals.values()) else ' (>= recorded bound)')
    if args.drat_card:
        text = cardinality_cnf(R, minimal, m - 1, pool, min_points)
        cnf = Path(args.cnf_out).with_name('card.cnf'); cnf.write_text(text)
        import subprocess
        t = time.time()
        r = subprocess.run([args.drat_trim, str(cnf), args.drat_card], capture_output=True, text=True)
        ok = 's VERIFIED' in r.stdout
        print(f'    cardinality CNF (family + at most {m-1} selectors + at least {min_points} pool selectors, {len(R)} selector variables) sha256 {sha(text)[:16]}; drat-trim {"VERIFIED" if ok else "FAILED"} ({time.time()-t:.0f}s)')
        assert ok
        lb_status = 'DRAT-checked (no hitting set of size ≤ %d with ≥ %d pool points)' % (m - 1, min_points)
    if args.veripb:
        text = decision_opb(R, minimal, m - 1, pool, min_points)
        opb = Path(args.cnf_out).with_name('card.opb'); opb.write_text(text)
        import subprocess
        t = time.time()
        r = subprocess.run([args.veripb_bin, str(opb), args.veripb], capture_output=True, text=True)
        ok = 's VERIFIED UNSATISFIABLE' in r.stdout
        print(f'    decision OPB (family + at least {min_points} pool selectors + at most {m-1} selectors, {len(R)} variables) sha256 {sha(text)[:16]}; VeriPB {"VERIFIED UNSATISFIABLE" if ok else "FAILED"} ({time.time()-t:.0f}s)')
        assert ok
        lb_status = ('DRAT- and ' if lb_status.startswith('DRAT') else '') + 'VeriPB-checked (no hitting set of size ≤ %d with ≥ %d pool points)' % (m - 1, min_points)
    # (4) upper bound (optional): F ∪ X* not 4-colourable (pinned CNF rebuilt byte-for-byte)
    X = cert.get('X_star')
    ub_status = 'no optimal instance recorded'
    if X is not None:
        verts = sorted(set(F) | set(X))
        tri = cert['pinned_triangle']
        assert all(v in set(F) for v in tri)
        assert all(tuple(sorted((a, b))) in edge_set for a in tri for b in tri if a < b)
        text = pinned_cnf(verts, edges, tri)
        h = sha(text)
        print(f'(4) optimal set X* ({len(X)} of R) : F ∪ X* has {len(verts)} vertices; pinned 4-colouring CNF sha256 {h[:16]} ({"matches" if h == cert["final_cnf_sha256"] else "DIFFERS FROM"} the recorded hash)')
        assert h == cert['final_cnf_sha256']
        ub_status = f'recorded CaDiCaL/drat-trim run (proof sha256 {str(cert["final_proof_sha256"])[:16]}..., {cert["final_proof_bytes"]} bytes)'
        if args.drat_final:
            import subprocess
            cnf = Path(args.cnf_out); cnf.write_text(text)
            t = time.time()
            r = subprocess.run([args.drat_trim, str(cnf), args.drat_final], capture_output=True, text=True)
            ok = 's VERIFIED' in r.stdout
            print(f'    drat-trim on the supplied proof: {"VERIFIED" if ok else "FAILED"} ({time.time()-t:.0f}s)')
            assert ok
            ub_status = 'DRAT-checked'
    target = 509 - len(F)
    print(f'summary: every 5-chromatic subgraph of A* contains the {len(F)} forced vertices and meets every killing set;')
    if min_points > 0:
        print(f'         every hitting set of the certified family with >= {min_points} pool points has size >= {m} [{lb_status}];')
        print(f'         by the committed closures a 5-chromatic subgraph on <= 508 vertices would need >= {min_points} pool points and |X| <= {target - 1};')
        assert m >= target, 'bound below target: no theorem'
        print(f'         => A* has NO 5-chromatic subgraph with at most 508 vertices (minimum order exactly 509, attained by G)')
    else:
        print(f'         minimum hitting set of the certified family = {m} [{lb_status}]; F ∪ X* not 4-colourable [{ub_status}]')
        print(f'         => minimum order of a 5-chromatic subgraph of A* = {len(F)} + {m} = {len(F)+m}')
    print('all_checks=true')


def card(args):
    """Write the cardinality CNF of a certificate (family clauses + at most m*−1 selectors + at least min_points pool
    selectors); its UNSAT (DRAT proof regenerable with CaDiCaL) certifies the bound m*."""
    cert = json.loads(Path(args.certificate).read_text())
    R = cert['free']; fam = [row['D'] for row in cert['family']]
    keys = set(frozenset(D) for D in fam)
    minimal = [D for D in fam if not any(k < frozenset(D) for k in keys)]
    text = cardinality_cnf(R, minimal, cert['minimum_hitting_set'] - 1, cert.get('pool_free', []), int(cert.get('min_points', 0)))
    Path(args.out).write_text(text)
    print(f'wrote {args.out}: {len(minimal)} minimal killing sets, {len(R)} selectors, bound {cert["minimum_hitting_set"]}, min_points {cert.get("min_points", 0)}, sha256 {sha(text)[:16]}')


def pb(args):
    """Write the pseudo-Boolean decision instance of a certificate (see decision_opb); its UNSAT proof
    (RoundingSat --proof-log, checked by VeriPB) certifies the bound m*."""
    cert = json.loads(Path(args.certificate).read_text())
    R = cert['free']; fam = [row['D'] for row in cert['family']]
    keys = set(frozenset(D) for D in fam)
    minimal = [D for D in fam if not any(k < frozenset(D) for k in keys)]
    text = decision_opb(R, minimal, cert['minimum_hitting_set'] - 1, cert.get('pool_free', []), int(cert.get('min_points', 0)))
    Path(args.out).write_text(text)
    print(f'wrote {args.out}: {len(minimal)} minimal killing sets, {len(R)} variables, bound {cert["minimum_hitting_set"]}, min_points {cert.get("min_points", 0)}, sha256 {sha(text)[:16]}')


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('card'); c.add_argument('certificate'); c.add_argument('--out', default='card.cnf')
    q = sub.add_parser('pb'); q.add_argument('certificate'); q.add_argument('--out', default='card.opb')
    b = sub.add_parser('build')
    b.add_argument('--union', required=True); b.add_argument('--forced', required=True); b.add_argument('--results', required=True)
    b.add_argument('--ambient', required=True); b.add_argument('--completion'); b.add_argument('--level2'); b.add_argument('--points', help='union_graph.py output with exact coordinates of all vertices')
    b.add_argument('--final-proof-sha'); b.add_argument('--final-proof-bytes', type=int)
    b.add_argument('--out', required=True)
    v = sub.add_parser('verify')
    v.add_argument('certificate')
    v.add_argument('--rc2', action='store_true'); v.add_argument('--milp', action='store_true')
    v.add_argument('--drat-card', help='DRAT proof for the cardinality CNF (regenerable with CaDiCaL)')
    v.add_argument('--drat-final', help='DRAT proof for the pinned CNF of F ∪ X*')
    v.add_argument('--drat-trim', default='drat-trim'); v.add_argument('--cnf-out', default='final.cnf')
    v.add_argument('--veripb', help='pseudo-Boolean proof (RoundingSat --proof-log) of the decision OPB instance, checked with VeriPB')
    v.add_argument('--veripb-bin', default='veripb')
    args = ap.parse_args()
    {'build': build, 'verify': verify, 'card': card, 'pb': pb}[args.cmd](args)


if __name__ == '__main__':
    main()
