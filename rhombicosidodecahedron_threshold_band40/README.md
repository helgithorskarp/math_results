# RID threshold-to-threshold exclusion at receiving height 2/5

**six-rupert-3, researcher.** The [complete proof](PROOF.md) excludes every
strict passage whose original source and receiving normals lie in the
two proper threshold signed-region families and whose original receiving
height f(n)=min_{v∈V}|v·n| is at least2/5. It includes every proper
rotation, full roll, planar translation and scale≥1. A small full spatial
angle is derived from containment.

The standard60-vertex edge-two rhombicosidodecahedron remains **globally
unresolved**. This is a conditional intermediate theorem. The winning
and both mixed branches at2/5 are not proved; the current global
receiving cutoff remains83/200, with squared-height gap1/28. The new
proof is **unformalized, author-checked and independently unreviewed**.
No historical priority or optimal constant is asserted.

At the new height, simply enlarging the old normal-cap rectangle
invalidates some HIGH receiving supports. The new proof retains all60
original vertex-height inequalities. Exact halfplane intersection gives
a four-vertex outer receiving polygon for each class, restoring all
needed original supports. Their fixed signed covers certify168 patches
and8736 strict coefficients. The normal and full-angle bounds, complete
8/12 original candidate pools and all6144 antipodal assignments are
freshly checked. The wider26/25 matching tolerance and sufficient94/25
moment coefficient are credited to
[six-reviewer-1's scoped review8346](../rhombicosidodecahedron_threshold_band_review1/REVIEW.md).
They are not new claims of this researcher, and that review does not
review this new theorem.

The raw references are exactly

    r_L=(0,(2−φ)/3,−1), r_H=(0,1,(3φ−1)/11), φ=(1+√5)/2.

Both originals r_L+(1/50,0,0) and r_H+(1/50,0,0), after unit
normalization, satisfy2/5≤f(n)<83/200 and retain all original reference
signs. Thus the new band contains actual receivers below the old cutoff.
The result does not assert new closed equality counts or a larger HIGH
exceptional-plane classification.

From the repository root, Python3.11+ standard library, run **separately**:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
 timeout 55s python3 -B rhombicosidodecahedron_threshold_band40/verify.py
~~~

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
 timeout 55s python3 -B -O rhombicosidodecahedron_threshold_band40/verify.py
~~~

Both modes compare every byte of [expected.json](expected.json),71258bytes,
SHA256 `b54fe946e103f678f005969e73cd69bf13f7abd8502d03146cc46e29757153ec`.
All21 malformed controls must reject in both modes. `--emit` deterministically
regenerates the compact expected record from public source and fixed
witnesses, without private exploration or adaptive cover search.

[dependencies.json](dependencies.json) fixes all65 previous mathematical
inputs before imports. [certificates.json](certificates.json) supplies the
new exact constants and complete fixed signed covers. [verify.py](verify.py)
freshly regenerates both original tangent disks, original circles and
all60 eligible heights, all6144 assignments and first rejection hashes,
all four proper class alignments, both positive original moment matrices,
96 exact trace regressions, both original-height polygons and480 height
gates,7680 original supports,128 displacement identities and6048 direct
vector/Bernstein audits. All160 outward rational root records and duplicate
full original geometry are checked and hashed rather than stored repeatedly.

No old mathematical file, guard or module global is changed. The source
reuses pinned author kernels and adapts their explicit pool/cover algorithms;
it is not an independent implementation or review. Full previous global
and closed-classifier replays are outside this checker. Trust includes the
original named body, exact Q(φ)/Fraction arithmetic, inherited original
interfaces, complete finite checks and the unformalized continuum proof.
No solver or floating predicate is used. Timeouts, kills, UNKNOWN and
incomplete searches never prove nonexistence.

Complete final-byte ordinary and optimized replays took23.286seconds
(25752KiB maximum child RSS) and18.067seconds (27404KiB), respectively,
on Python3.11.2. Exact generation took17.853seconds (25872KiB).
All mathematical jobs use one CPU, numerical threads1 and the unchanged
55-second deadline. No resource cap is raised.

Current primary literature and complementary named-solid proofs are
cited with their exact scopes in [PROOF.md](PROOF.md). The next useful
step is a fresh winning-source→threshold-receiver mixed exclusion at2/5
on these polygons, then the opposite mixed and winning same-class branches.
