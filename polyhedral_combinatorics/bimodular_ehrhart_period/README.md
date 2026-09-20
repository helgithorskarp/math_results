# Simple bimodular polytopes have full Ehrhart period

Let `P={x in R^d:Ax<=b}` be bounded, full dimensional and simple, with
`A,b` integral. If every `d`-by-`d` row minor of `A` has absolute value at
most two, then **the minimal Ehrhart quasiperiod equals the vertex
denominator: one if P is integral, two otherwise**.

This is the full-minor convention for a bimodular matrix. Smaller minors
and entries may exceed two. Nonprimitive facet inequalities, such as
`2x<=1`, are allowed. Redundant input inequalities may be removed first.
The lattice is the fixed standard integer lattice.

The proof gives a more general local criterion. Suppose `2P` is a lattice
polytope. Among nonempty faces whose affine spans miss the lattice, let
`g` be the minimum codimension and `M` the faces of codimension `g`.
For each `F` in `M`, require exactly `g` containing facets and

    [Z^g : A_F Z^d] = 2,

where `A_F` contains those facet normals from a fixed integral description.
Then, for `L_P(n)=A_P(n)+(-1)^n B_P(n)`,

    deg B_P = d-g,
    [n^(d-g)] B_P = 2^(-g-1) sum_(F in M) vol_(d-g)(F) > 0.

Volume uses the face-direction lattice with unit lattice cube volume one.
The reduced Ehrhart denominator is exactly

    (1-t)^(d+1) (1+t)^(d-g+1).

The face directions need not be coordinate subspaces. Minimality forces
the index-two image to be the even-total-sum lattice; this supplies the
proper-face translations and positive local parity jump. Bimodularity
forces the needed image index by a quotient-group projection, while
simplicity supplies the facet count. [PROOF.md](PROOF.md) gives the full
argument and the numerator residual at `-1`.

The local criterion contains the preceding type-B theorem. The bimodular
corollary alone does not contain every type-B system: disjoint unbalanced
blocks can give a full minor of absolute value four. No recognition of a
signed-graph representation is needed for the new criterion.

Both restrictions matter. Stanley's known collapsing pyramid is itself
bimodular but fails the local facet count. The simple half-integral
McAllister--Woods collapsing triangle has active image index four. These
are credited prior examples, not new counterexamples. The theorem is a
sufficient criterion and does not classify all nonsimple systems.

## Reproduce

From this directory, using Python 3.11 or newer and its standard library:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

The Python commands print [expected.json](expected.json) and fail on any
mismatch. No files are generated. The manifest covers the five substantive
files in this directory.

The compact verifier checks:

- Thirteen named polytopes, including nonprimitive inequalities, rational
  simplices, an oblique prism with entries larger than two but full minors
  at most two, a case satisfying the local criterion with global minor
  four, a nonsimple valid case, and the two known collapsing controls.
- Exact rational vertices and actual facets, all face intersections, image
  indices from gcds of maximal minors, and affine integrality from the
  corresponding augmented matrix. Segment volumes use primitive direction
  vectors, including a direction with three nonzero coordinates.
- Direct integer counts, 52 unused interpolation values and 39 comparisons
  with unpruned Cartesian-product enumeration.
- Thirteen rectangular index-two systems: 471 right-side membership checks
  against independently enumerated residue images and 101 proper-subsystem
  checks, including partial-support characters exposing smaller obstructions.
- Five malformed inputs and an inconsistent dependent affine system.

Basic linear algebra and interpolation helpers were adapted from the
preceding checker and are credited in [SOURCES.md](SOURCES.md). The general
integer-image and direction-lattice checks replace its root-specific
assumptions. This is not an independent review. Boundedness is explicit in
the fixtures; the volume routine supports points and segments only.

The universal theorem rests on the written proof and the explicitly
imported Berline--Vergne local Euler--Maclaurin theorem. Finite checks do
not replace that input, prove the universal result by extrapolation, or
establish novelty. This extension is unformalized and not independently
reviewed. Novelty is relative to bounded primary-source searches.
