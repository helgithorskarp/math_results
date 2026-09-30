# Tammes-15: exclude the complete single-three profile (1,3,1)

**six-tammes-1, researcher.** [PROOF.md](PROOF.md) excludes the F-U
noncontact subcase using the original face stars and the three's full
contact set. Together with the preceding committed contact exclusion
h8054 it removes the whole row, leaving four necessary r=1 count profiles.

The hypotheses are fifteen unit points, 1/2<c<3/5, a complete connected
degree-3..5 contact graph with simple strictly convex hemispherical
triangle/quadrilateral cells, nine Qs, and exactly one degree three.
Global numerical bounds, global optimality, and larger-face or unrestricted
optimizer coverage remain unchanged. Both checks below are by the author;
independent mathematical review and formalization remain pending.

Use CPython 3.11.2 or a compatible Python 3 with only its standard library.
From this directory, run the following commands sequentially:

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B check.py > /tmp/tammes15-three-one-check.json
    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O check.py > /tmp/tammes15-three-one-check-O.json
    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B audit.py > /tmp/tammes15-three-one-audit.json
    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O audit.py > /tmp/tammes15-three-one-audit-O.json
    sha256sum -c SHA256SUMS

Each program checks its entire recomputed result against its saved fixture
before printing it. No Python assertion is used for correctness checks.

Production EXPECTED.json contains 82 exact covers, 15,608 total RGS nodes:
52 unpaired covers close; 28 paired basic covers have four partial survivors
in two covers; their forced final quadrilateral closes both. Each of the
thirteen labelled role cases includes all four three-of-four U contact sets.
Every additional deficient original is assigned before later alias pruning.
No fifteen-class cutoff is used; the largest final patch permits twenty.

AUDIT_EXPECTED.json contains a separate exhaustive 68,306-raw-tuple audit.
It imports no production predicate, schema or enumerator. It specifies
reversed actual face words and explicit roles, checks unoriented cells
with orientation parity preserved under coalescence, bitset links and
signed-dual orientability, then compares every initial, two-slot
block-boundary and final partition entrywise. It omits the production
K4 and global face-count shortcuts. Positive fifteen-/sixteen-class
partial patches and separate-contact controls prevent an overconstrained
prefix from being mistaken for a contradiction.

Recorded normal/optimized production times were 1.380/1.417 seconds;
normal/optimized audit times were 5.764/5.915 seconds. Maximum child RSS
was 18,452 KiB. Each run completed within a 45-second timeout, the existing
1CPU/2GiB scope, native threads one, and one mathematical job at a time.
The fixed production and raw-block node budgets are 200,000; exceeding a
budget raises INCOMPLETE and is never a nonexistence proof.

Written geometry, anchor classification, face forcing and pruning bridges
are in PROOF.md. Prior angular and contact-subcase results are explicit
dependencies there. Standard-library checks require no private inputs,
solver output, floating sign decision, CAS, omitted corpus or external
certificate. SHA256SUMS covers the other seven compact text files.
