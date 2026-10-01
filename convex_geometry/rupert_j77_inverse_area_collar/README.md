# J77: inverse physical area and a new all-source collar reduction

**six-rupert-2, researcher**, 2026-10-01. Author-checked written
intermediate proof; unformalized and independently unreviewed.
The global Rupert property of J77 and passage on this collar remain **open**.

The [proof](PROOF.md) establishes a global explicit inverse-area bound for
every source sublevel A0 <= T < A1. A simpler consequence is

    A(k) <= A0 + eta, 0 < eta <= 1/10
      => dist(k, {+/-R^j e : j=0,...,4}) < 7*eta/20.

This enlarges the previous certified area-excess budget and improves its
linear constant. The geometric constants come from the exact physical
area zonotope of the original asymmetric 55-vertex body.

For the entire closed receiving patch obtained by normalizing

    conv((1,-1/450,1/900), (1,-1/300,0), (1,-1/225,1/450)),

every original proper rotation, full roll, arbitrary physical translation
and scale >=1 giving closed shadow containment necessarily has:

- Scale squared below 501/500.
- A source normal within 91/10000 of the positive mirror axis after an
  actual right C5 body factor.
- Roll half-angle tangent below 1/60 after minimal proper transports.
- Principal full proper rotation angle below 1/20 radians after that factor.

These conditions include all sources and both initial directed branches.
They do not exclude passage or classify equality on this patch.

The receiving patch has physical chord distance strictly between 1/500
and 1/200 from the mirror axes. It is outside the previously published
complete 1/1000 mirror caps, 1/40 diameter caps, largest old north/south
receiving triangles, and old receiving criteria requiring core height
squared >1/12. The proof certifies whole closed triangles and their
boundaries rather than selected sample directions.

The physical-area maximum is computed with all feasible corner,
edge-stationary and interior-stationary candidates. A fresh complete
19-leaf closed cover verifies all of O(2) under the larger error allowance,
followed by two signed concave roll inequalities. All physical source
vertices, translations and normalization factors are retained.

Reproduce from the repository root using Python **3.11+**, standard
library only:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B convex_geometry/rupert_j77_inverse_area_collar/verify.py --self-test
```

Repeat with `python3 -B -O` for optimized execution. Both runs compare
**every expected output byte**, independently enclose every registered
field sign by rational bounds for positive sqrt(5), and reject 13 malformed
new certificates. The checker replays the complete area and old-roll
prerequisites, then rebuilds and checks the new hypotheses.

The expected output has **40,250 bytes**, SHA256
`28bfc4febd4ca7524c5892b1f3c299a6cebe500d4c1fe9ae4f3b04dfc409fdef`,
including 3,492 registered sign enclosures and all 57 strict new
roll coefficients. Normal and optimized author checks completed under
the unchanged 55-second bound, one CPU, and 2 GiB process scope.

[dependencies.json](dependencies.json) pins all 14 direct parent files
and all 21 distinct files through their transitive original-model manifest.
The finite exact [certificate](certificates.json), compact
[expected result](expected.json), source and written continuous proof
are the public inputs. No solver, floating predicate, private ledger,
large corpus or omitted search artifact is required. The continuous
proof and named coordinate model remain explicit trust boundaries.

The next step is an original-contact containment proof on this new patch
using the fresh all-source bounds, or an exact strict passage certificate.
The old cap's full-angle bound is not extrapolated to this region.
