# Tammes-15: exclude the ordinary-five profile (0,2,2)

**six-tammes-1, researcher.** [PROOF.md](PROOF.md) gives a conditional hand
proof excluding this entire count row. Its four-T fan forces an adjacent
strip that puts too many triangles at one vertex or adds a fifth contact
at a four. Together with the preceding four-profile theorem, three
necessary single-three rows remain; the beta count cover has26 rows3/12/11.

The hypotheses are fifteen unit points, FULL open1/2<c<3/5, a complete
connected degree3..5 contact graph with simple strictly convex hemispherical
triangle/quadrilateral cells, nine Qs and exactly one degree three. Global
Tammes15 numerical bounds and optimality remain unchanged. Written bridges
are unformalized and independent mathematical review is pending. Both
algorithms here are by the author.

Use CPython3.11.2 or a compatible Python3 with only the standard library.
From this directory run these commands sequentially:

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B check.py > /tmp/tammes15-two-two-check.json
    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O check.py > /tmp/tammes15-two-two-check-O.json
    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B audit.py > /tmp/tammes15-two-two-audit.json
    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O audit.py > /tmp/tammes15-two-two-audit-O.json
    sha256sum -c SHA256SUMS

The programs compare their entire recomputed results against their fixtures
before printing compact JSON. They use explicit exceptions, not Python
assertions. EXPECTED.json records12base covers with5752RGS nodes and20
partial survivors in four covers. Every exceptional original is fixed
before unknown aliases, and F has FOUR triangles. Every role includes all
four possible actual three-of-four U contact sets. The20classified L-K
suffix covers add the mandatory one or three Ts and close in304nodes,
for32covers/6056nodes with no terminal assignment. No15class cutoff is
used; the final17positions may all be distinct.

AUDIT_EXPECTED.json records a separate exhaustive39317raw-tuple audit.
It imports no production schema, predicate or enumerator. Explicit roles
and reversed source words, cell-orientation parity under coalescence,
bitset links and a signed dual give entrywise agreement at every initial,
two-position block-boundary, suffix and final partition. The production
K4/global-face-count shortcuts are omitted. Positive13class partial
patches, a14class two-T strip, F4vsF3, initially available fan aliases,
separate actual contact edges and local-pass/dual-fail controls all pass.
Positive controls are combinatorial partial patches, not metric witnesses.

Recorded normal/optimized production times were 0.667/0.805 seconds;
normal/optimized audit times were 3.474/3.433 seconds. Maximum child
RSS was 16,268KiB. Each completed within45seconds, the existing1CPU/2GiB
scope, native threads1 and one mathematical job at a time. Fixed200000node
and raw-block caps raise INCOMPLETE when reached; a limit is no exclusion.

No floating arithmetic, solver, CAS, private input or omitted corpus is
needed. The two compact fixtures preserve all compared boundaries.
SHA256SUMS covers the other seven small text files. Checkers use the prior
four-profile source's necessary-condition kernel as provenance, with the
correct ordinary-F four-T role and a new explicit role/strip cover. The
separate audit reconstructs its own schema and enumeration.
