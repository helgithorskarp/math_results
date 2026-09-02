#!/usr/bin/env python3
"""Independent check of the closure certificate for chosen vertices, importing none of the branching enumeration.

For a vertex u it (a) re-validates the certificate rows of u as proper colourings by a direct edge scan, (b) computes
free-colour masks of all universe points from the neighbour lists directly, (c) brute-forces, by complete enumeration
over all 4-subsets of the set E(u) = union of the empty-list points of all rows, every point set of size <= 4 whose
points all have an empty list in every row... more precisely every 4-subset of E(u) that hits the empty-list set of
every row (these are exactly the independent uncovered sets contained in E(u); an independent uncovered set of size
<= 4 always has a minimal member inside E(u)), and (d) samples many further sets (perturbations of certificate-declared
sets, sets around failing unit edges / triangles, random sets of 'hot' points) and decides coverage by a direct
recursive list colouring (cluster_U.extends of the triple closure).  Every uncovered set found must contain a
declared set (sibling certificates + this certificate).
usage: independent_check.py CERT u1 [u2 ...] [--samples S]
"""
import argparse, base64, gzip, hashlib, itertools, json, random, sys, time, importlib.util
import numpy as np
from paths import TRIPLE, N, K
import build_universe
from known_declared import load_known_declared
import libraries

spec = importlib.util.spec_from_file_location('cu', TRIPLE / 'cluster_U.py')
cu = importlib.util.module_from_spec(spec); spec.loader.exec_module(cu)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('cert'); ap.add_argument('vertices', type=int, nargs='+')
    ap.add_argument('--samples', type=int, default=20000); ap.add_argument('--seed', type=int, default=1)
    args = ap.parse_args(); t0 = time.time()
    p = args.cert
    cert = json.loads(gzip.open(p, 'rb').read() if p.endswith('.gz') else open(p, 'rb').read())
    U = build_universe.build()
    n3, nk = U['n_q3'], U['n_q3'] + U['n_q2k']
    nbrs = U['nbrs'] + U['nonk_nbrs']
    lab_index = {tuple(l): i for i, l in enumerate(U['nonk_labels'])}
    adj = {}
    for a, b in U['kedges'] + [(nk + a, nk + b) for a, b in U['nonk_edges']]:
        adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    def decode(ref):
        f = ref.split(':')
        return int(f[1]) if f[0] == 'q3' else (n3 + int(f[1]) if f[0] == 'k2' else nk + lab_index[(int(f[1]), int(f[2]), int(f[3]))])
    parts, edges, lib, qnb, qq_edges, counts = libraries.load_libraries()
    known, src = load_known_declared()
    RB = (N - 1) // 4
    packed = base64.b64decode(cert['family_rows_base64'], validate=True)
    assert hashlib.sha256(packed).hexdigest() == cert['packed_rows_sha256']
    offsets = np.cumsum([0] + cert['family_sizes'])
    rng = random.Random(args.seed)
    all_ok = True
    for u in args.vertices:
        t1 = time.time()
        rows = list(lib[u])
        for i in range(cert['family_sizes'][u]):
            raw = packed[(offsets[u] + i) * RB:(offsets[u] + i + 1) * RB]
            vals = [(b >> s) & 3 for b in raw for s in (0, 2, 4, 6)]
            it = iter(vals); row = [-1 if v == u else next(it) for v in range(N)]
            assert all(row[a] != row[b] for a, b in edges if a != u and b != u), 'certificate row not proper'
            rows.append(row)
        declared = set(frozenset(B) for B in known[u]) | set(frozenset(decode(r) for r in A) for A, st in cert['declared_sets'][u])
        def has_declared(A):
            return any(frozenset(S) in declared for k in range(1, len(A) + 1) for S in itertools.combinations(A, k))
        def uncovered(A):
            nb = [nbrs[p] for p in A]
            internal = [(i, j) for i, j in itertools.combinations(range(len(A)), 2) if A[j] in adj.get(A[i], ())]
            return not any(cu.extends(row, u, nb, internal) for row in rows)
        # (c) complete enumeration of the independent sets of at most four points inside E(u) that hit the empty-list
        #     set of every row (= the independent uncovered sets inside E(u); an independent uncovered set of size <= 4
        #     contains a minimal one, which lies inside E(u)).  Meet-in-the-middle over Python-integer row bitmasks:
        #     no branching, no failing-set machinery.
        E_rows = []
        for row in rows:
            def used_bits(p):
                b = 0
                for w in nbrs[p]:
                    if w != u:
                        b |= 1 << row[w]
                return b
            mask = [15 & ~used_bits(p) for p in range(nk)]
            E_rows.append(frozenset(p for p in range(nk) if mask[p] == 0))
        Eu = sorted(set().union(*E_rows))
        R = len(rows); ALL = (1 << R) - 1
        hit = {p: sum(1 << i for i, E in enumerate(E_rows) if p in E) for p in Eu}      # rows hit by p
        n_ind = n_ind_unc = n_ind_bad = 0
        found = set()
        def record(A):
            nonlocal n_ind_unc, n_ind_bad
            A = tuple(sorted(A))
            if A in found:
                return
            found.add(A); n_ind_unc += 1
            assert uncovered(A), ('hitting set not uncovered?', A)
            if not has_declared(A):
                n_ind_bad += 1; print(f'  ERROR u={u}: independent uncovered set {A} without declared subset', flush=True)
        indep = lambda A: not any(A[j] in adj.get(A[i], ()) for i, j in itertools.combinations(range(len(A)), 2))
        # minimal hitting sets only (every uncovered set contains a minimal one): each point must hit a row that
        # the earlier points miss; the last point must hit every remaining row, so it is searched among the points
        # of the lowest remaining row.
        m = len(Eu)
        pos = {p: i for i, p in enumerate(Eu)}
        row_pts = [sorted(E, key=pos.get) for E in E_rows]
        n_ind = 0
        for i in range(m):
            p = Eu[i]
            if hit[p] == ALL: record((p,)); continue
            for j in range(i + 1, m):
                q = Eu[j]
                if q in adj.get(p, ()) or not (hit[q] & ~hit[p]): continue
                h2 = hit[p] | hit[q]
                if h2 == ALL: record((p, q)); continue
                need2 = ALL & ~h2
                for k in range(j + 1, m):
                    r = Eu[k]
                    if not (hit[r] & need2) or r in adj.get(p, ()) or r in adj.get(q, ()): continue
                    h3 = h2 | hit[r]
                    if h3 == ALL: record((p, q, r)); continue
                    need = ALL & ~h3
                    low = (need & -need).bit_length() - 1
                    for s_ in row_pts[low]:
                        n_ind += 1
                        if pos[s_] > k and (hit[s_] & need) == need and indep((p, q, r, s_)):
                            record((p, q, r, s_))
        # (d) sampled sets with direct list colouring
        hot = sorted(set(p for E in E_rows for p in E) | set(p for A, st in cert['declared_sets'][u] for p in map(decode, A)) | set(p for B in known[u] for p in B))
        hot_nb = sorted(set(q for p in hot for q in adj.get(p, ())))
        pool_pts = hot + hot_nb
        trials = set()
        for A, st in cert['declared_sets'][u]:
            A = sorted(map(decode, A))
            for _ in range(20):
                B = list(A); B[rng.randrange(4)] = rng.choice(pool_pts)
                if len(set(B)) == 4: trials.add(tuple(sorted(B)))
        while len(trials) < args.samples:
            trials.add(tuple(sorted(rng.sample(pool_pts, 4))))
        n_s_unc = n_s_bad = 0
        for A in trials:
            if uncovered(A):
                n_s_unc += 1
                if not has_declared(A):
                    n_s_bad += 1; print(f'  ERROR u={u}: sampled uncovered set {A} without declared subset', flush=True)
        ok = n_ind_bad == 0 and n_s_bad == 0
        all_ok &= ok
        print(f'u={u}: rows {len(rows)} (certificate {cert["family_sizes"][u]}), |E(u)| {len(Eu)}, last-level probes {n_ind} (minimal independent uncovered sets of size <= 4 found {n_ind_unc}, undeclared {n_ind_bad}); '
              f'sampled {len(trials)} (uncovered {n_s_unc}, undeclared {n_s_bad}); ok={ok} ({time.time()-t1:.0f}s)', flush=True)
    print(f'all_ok={"true" if all_ok else "false"} ({time.time()-t0:.0f}s)')


if __name__ == '__main__':
    main()
