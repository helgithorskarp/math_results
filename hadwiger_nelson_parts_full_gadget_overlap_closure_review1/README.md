# Independent review of the capped full-Parts-gadget closure

Verdict: **ACCEPT**, at high confidence, for this exact restricted-family
theorem. Let `L` be the first 374 points of the archived Parts graph and let
`S+` be its last 135 points together with the origin. For every Euclidean
isometry `g`, if `L` and `g(S+)` share at least two distinct points, the
complete strict unit-distance graph on their union is four-colourable.
Consequently every placement of these two complete gadgets with at most 508
distinct points is four-colourable.

The reviewed source is
[`hadwiger_nelson_parts_full_gadget_overlap_closure`](../hadwiger_nelson_parts_full_gadget_overlap_closure/README.md)
at commit `7757f7fc0629bc1a2565ce94eb1702f7647c6e79`.

## Scope of acceptance

This closes one whole physical construction family, including the 2,772
previously archived 508-point residual placements. It is **not** a global
lower bound for plane unit-distance graphs, a five-chromatic construction, or
a statement about incomplete gadgets, added points, different gadget sources,
or zero- and one-overlap placements. The original Parts placement has one
cross-gadget overlap, 509 distinct points and 2,442 unit edges, so it lies
exactly outside the hypothesis.

The unrestricted order record therefore remains Parts's 509-vertex,
2,442-edge graph ([arXiv:2010.12665](https://arxiv.org/abs/2010.12665)).
Haugland's August 2026 paper also identifies 509 as the current unrestricted
record; its 2,131-point construction advances the separate Moser-spindle-free
restriction ([arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4)).

## Re-derived universal argument

Identify the plane with the complex numbers and put

```text
E = Q(i*sqrt(3), i*sqrt(11)),
rho = (7+i*sqrt(15))/8.
```

The previously reviewed field theorem proves that every strict unit-distance
graph on a subset of `E` is four-colourable. Only this upper bound is needed
here. Its source at commit `825d763c59e6e299f2c7df4b8c93b13dece6d511`
and independent acceptance at commit
`0d54b52f753674be64f78b6aa57754d873464347` both replay unchanged.

Exact coordinate inspection gives

```text
L is a subset of E,
B = conjugate(rho)*S+ is a subset of E,
S+ = rho*B,
abs(rho) = 1.
```

For an arbitrary isometry `g`, define `h(z)=g(rho*z)`. Then `h(B)=g(S+)`.
If two distinct overlaps are `h(b_j)=a_j`, with `a_j` in `L`, write either
`h(z)=u*z+t` or `h(z)=u*conjugate(z)+t`. Subtracting the two overlap equations
gives

```text
u = (a_1-a_0)/(b_1-b_0),
```

with a conjugated denominator in the reversing case. The denominator is
nonzero because the overlaps are distinct. Since `E` is a field closed under
complex conjugation, both `u` and `t` lie in `E`; hence the entire union lies
in `E` and inherits the reviewed four-colouring, including every extra unit
edge created by the placement.

Finally, the gadgets contain `374+136=510` points before cross-collision
merging. A union of order at most 508 therefore has at least two distinct
overlaps. This proves the capped conclusion for all isometries, without a
finite placement enumeration or solver assumption.

## Independent exact checks

[`independent_check.py`](independent_check.py) imports no target or field-
colouring implementation. It pins the source and dependencies by SHA-256 and
uses generic subset-mask multiplication in
`Q(sqrt(3),sqrt(5),sqrt(11))`, rather than the source's sparse radical
adapter. All 64 basis products, 128 precisions of the chosen 2-adic square
root, the unit norm of `rho`, and all 136 inverse-rotation roundtrips pass.

The checker independently finds 374 points and 1,860 complete internal unit
edges in `L`, and 136 points and 564 edges in the normalized `B`. Every point
lies in the required four-dimensional complex field. The normalized integer
coordinate hash is
`cccc21127b01ccf2febd4326779fcb05fe5e71c29d7c348a03f9e89782ff0145`,
matching the source. A separately implemented 2-adic field colouring checks
every internal edge. The original unnormalized Parts support is independently
reconstructed as 509 distinct points and all 2,442 unit edges.

As a stronger archive audit, the checker reconstructs every one of the 2,772
residual isometries from its two segment correspondences. It finds 1,372
orientation-preserving and 1,400 orientation-reversing placements. Every
placement has exactly the two declared cross-gadget coincidences, exactly 508
merged points, and field-valued isometry parameters and image points. The
deterministic parameter, placed-point, and colour-word stream hashes are
recorded in [`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt).

All four complete sample graphs from the source match edge-for-edge and
colour-for-colour. Nine additional independently selected residuals were also
completed from the distance definition. Across the 13 samples, 1,674,114
unordered pairs yield 32,557 unit edges, and every field colour is checked on
every edge. Five malformed-field, collision, division, precision, and colour
controls are rejected. Normal and optimized Python runs are byte-identical.

The finite archive reconstruction confirms that every listed residual is a
valid instance of the theorem. It does not rerun the older 22-minute census
that originally proved those 2,772 seeds were the complete library-failure
list. That completeness remains covered by its prior qualified independent
review. More importantly, the new universal theorem does not depend on the
archive being complete: it directly covers every capped isometry, listed or
not.

## Reproduce

From a complete repository checkout with Python 3.11 or later:

```sh
(cd hadwiger_nelson_parts_full_gadget_overlap_closure && \
  sha256sum -c SHA256SUMS && \
  python3 -B verify.py | diff -u EXPECTED.json - && \
  python3 -O -B verify.py | diff -u EXPECTED.json - && \
  python3 -B controls.py | diff -u CONTROLS.json -)

PYTHONDONTWRITEBYTECODE=1 python3 -B \
  hadwiger_nelson_nonmono_field_obstruction_review3/independent_check.py \
  hadwiger_nelson_nonmono159_214_lowden2/points159.tsv \
  hadwiger_nelson_nonmono159_214_lowden2/points214.tsv \
  | diff -u \
      hadwiger_nelson_nonmono_field_obstruction_review3/EXPECTED_OUTPUT.txt -

PYTHONDONTWRITEBYTECODE=1 python3 -B \
  hadwiger_nelson_parts_full_gadget_overlap_closure_review1/independent_check.py \
  | diff -u \
      hadwiger_nelson_parts_full_gadget_overlap_closure_review1/EXPECTED_OUTPUT.txt -

(cd hadwiger_nelson_parts_full_gadget_overlap_closure_review1 && \
  sha256sum -c SHA256SUMS)
```

The clean-room all-residual run takes about two minutes on the recorded host.
No SAT solver, native binary, or large generated artifact is required.

## Limits and trust boundary

The universal conclusion rests on the written two-overlap field argument and
the accepted, unformalized 2-adic colouring theorem—not on the 13 finite graph
samples. Executable checks trust the pinned coordinate and seed bytes, CPython
exact integers and fractions, SHA-256, and ordinary hardware. No proof-
assistant formalization or independent derivation of Parts's original
coordinate corpus is supplied.

Within those limits, I found no normalization error, field-membership gap,
unhandled reflection, collision-count error, invalid archived residual,
monochromatic unit edge, or scope-changing hidden assumption. Acceptance is
warranted only for the two complete gadgets under arbitrary Euclidean
isometry at the two-overlap/capped boundary.
