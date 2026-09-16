# Straight-chain unitization does not carry the odd21 obstruction

This package closes one predeclared auxiliary-point unitization of the exact
21-point odd-distance spindle of Ardal--Maňuch--Rosenfeld--Shelah--Stacho.
For every source pair at distance `d` in `{1,3,5,7}`, take the straight segment
between it and insert points at unit intervals.  No second source, reciprocal
copy, affine deformation, or relation-only surrogate is used.

The cap equation fixed before enumeration was

```text
21 + 26*(3-1) + 14*(5-1) + 8*(7-1) = 177 <= 508.
```

Exact collision merging leaves **115 points**.  Complete all-pairs
reconstruction gives **219 unit edges**: 141 distinct chain segments and 78
additional incidental contacts.  The resulting strict unit-distance graph is
only **three-chromatic**.  More importantly, for each of the 48 nonunit source
constraints, the certificate supplies a proper three-colouring of the whole
219-edge graph in which that constraint's source endpoints receive the same
colour.  Thus none of the length-3, length-5, or length-7 chains supports the
intended source inequality.  Only the seven constraints already at unit
distance are represented.

This is an exact stopping result for this one economical straight-geodesic
unitization.  It is not a five-chromatic construction, not a sub-509 record,
and not an exclusion of other auxiliary-point gadgets.  In particular, an
odd number of unit edges in a path does not force its endpoints different in
a colouring with three or four available colours.

## Exact geometry

Write a point as

```text
(a + b*sqrt(85)) + i*(c*sqrt(3) + d*sqrt(255)),  a,b,c,d in Q.
```

The eleven unrotated source points are
`h(n,m)=(n+m/2, sqrt(3)*m/2)` at the published integer pairs.  The other ten
are their images under multiplication by
`rho=(127+i*sqrt(255))/128`; the origin is shared.  Linear interpolation by
`k/d` therefore remains in the displayed exact field.  For a difference row
`(a,b,c,d)`, squared distance is

```text
(a^2 + 85*b^2 + 3*c^2 + 255*d^2)
  + (2*a*b + 6*c*d)*sqrt(85).
```

The checker uses this identity on every unordered point pair.  It separately
reconstructs the source, all chain occurrences, collisions, intended segments,
and incidental contacts.  The physical triangle on source vertices I1, I2,
I3 proves the lower bound of three; the saved proper three-colouring proves
the upper bound.

## Reproduce

Python 3.11 or later and only the standard library are required:

```sh
python3 -B hadwiger_nelson_odd21_geodesic_unitization_stop/produce.py \
  --output /tmp/odd21-geodesic.json
cmp /tmp/odd21-geodesic.json \
  hadwiger_nelson_odd21_geodesic_unitization_stop/certificate.json
python3 -B hadwiger_nelson_odd21_geodesic_unitization_stop/verify.py \
  --check-expected
python3 -O -B hadwiger_nelson_odd21_geodesic_unitization_stop/verify.py \
  --check-expected
python3 -B hadwiger_nelson_odd21_geodesic_unitization_stop/controls.py
sha256sum -c hadwiger_nelson_odd21_geodesic_unitization_stop/SHA256SUMS
```

The producer uses canonical DSATUR search to find the colour words.  The
checker does not trust search verdicts: it rebuilds the complete exact graph
and checks all 49 supplied colourings edge by edge.  Its only negative
chromatic statement is the elementary unit-triangle lower bound.  File hashes
protect reproducibility rather than replacing the mathematical checks.

## Scope and provenance

The fixed source is the 21-point spindle in Ardal, Maňuch, Rosenfeld, Shelah
and Stacho, [*The Odd-Distance Plane
Graph*](https://shelah.logic.at/files/95939/923.pdf) (2009).  The accepted
source audit and affine no-go are in the sibling package
[`hadwiger_nelson_odd21_affine`](../hadwiger_nelson_odd21_affine/README.md).
That source's full 55-edge `{1,3,5,7}` graph is five-chromatic; the present
package shows exactly why replacing its long edges by bare unit chains does
not transfer the obstruction.

At the evidence refresh for this pass, the campaign's committed Discovery
index remained stale and later accepted broadcasts remained pending; this
package makes no commitment claim.  The published unrestricted comparison
remains Parts' 509-point strict unit-distance construction.  Historical and
teammate evidence was preserved, and no adjacent odd21 design was opened.

The mathematical source was published in commit
`f86de68966eb6be461b0cfc1f0bf8d574c0b989e`.  The corresponding Discovery
finding was accepted for broadcast once with CheckTx code zero.  It was absent
from the committed index at height 4363 when checked on 2026-09-16, so its
receipt is **pending and uncommitted** and must not be resubmitted solely for
that absence.  See [DISCOVERY_RECEIPT.json](DISCOVERY_RECEIPT.json).
