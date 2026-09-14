# All capped isometric placements of the two full Parts gadgets are four-colourable

Let `L` be the first 374 points of the archived Parts graph, and let `S+`
be its last 135 points with the origin adjoined. For **every Euclidean
isometry g**, if `L` and `g(S+)` share at least two distinct points, their
complete strict unit-distance graph is four-colourable.

Since the two full gadgets have 510 points before merging, **every placement
of both full gadgets with at most 508 distinct points is four-colourable**.
This closes the previously archived **2,772 physical 508-point residuals**,
and also covers placements with more than two overlaps. It is a restricted
construction-family exclusion, not a record improvement.

The proof is a short application of an already reviewed field theorem.
The new link is the exact normalization of the full 136-point small gadget;
the earlier published application concerned the separate 159- and 214-point
nonmono gadgets. No new field-colouring theorem or method is claimed.

## Proof

Identify the plane with the complex numbers and set

\[
E=\mathbb Q(i\sqrt3,i\sqrt{11}),\qquad
\rho=(7+i\sqrt{15})/8.
\]

The reviewed [field theorem](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
proves that the strict unit-distance graph on all of `E` is four-colourable,
including nonintegral coordinates. Its
[independent acceptance](../hadwiger_nelson_nonmono_field_obstruction_review3/README.md)
also accepts the two-overlap isometry corollary.

Exact inspection of all coordinates gives

\[
L\subset E,\qquad B=\overline\rho S^+\subset E,
\qquad |\rho|^2=(49+15)/64=1.
\]

Thus `S+=rho B`. For an arbitrary isometry `g`, define `h(z)=g(rho z)`.
This is again an isometry and `h(B)=g(S+)`. If two distinct points satisfy
`h(b_j)=a_j` with `a_j` in `L`, write either `h(z)=u z+t` or
`h(z)=u conjugate(z)+t`. Subtraction gives

\[
u=(a_1-a_0)/(b_1-b_0)
\]

in the preserving case, with a conjugated denominator in the reversing
case. The denominator is nonzero. As `E` is a field closed under conjugation,
`u,t` belong to `E`, and hence the entire union belongs to `E`. The imported
four-colouring colours every physical unit edge, including any extra edges
created by the placement. Collision merging changes no part of this argument.

Finally, `|L union g(S+)|=374+136-|L intersection g(S+)|`; order at most 508
forces at least two overlaps. This proves the capped full-gadget assertion.

## Exact coordinate bridge and checks

The hash-pinned [509-point table](../hadwiger_nelson_parts509_completion_census_degree9/points.tsv)
uses denominator 96 and the real basis
`1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165` separately for `x,y`.
Membership in `E` means only positions `1,sqrt33` may be nonzero in `x`,
and only `sqrt3,sqrt11` in `y`. This is a restricted complex field, not the
larger Cartesian coordinate set `Q(sqrt3,sqrt11)^2`.

For a small-gadget point `(x,y)`, multiplication by `conjugate(rho)` gives

\[
((7x+\sqrt{15}y)/8,\ (7y-\sqrt{15}x)/8).
\]

The checker tests field membership for all 374 large and all 136 normalized
small points, verifies all 136 inverse-rotation roundtrips, and reconstructs
the complete internal graphs: 1,860 and 564 edges. It also checks literal
four-colourings using the imported field algorithm.

The [reviewed residual archive](../hadwiger_nelson_parts509_two_overlap_library_review1/README.md)
contains 2,772 distinct seeds. Their hash, count and determining segment
equalities are checked here. The earlier library failures remain valid:
failure of those fixed libraries was never a non-four-colourability proof.
The universal argument above empties their chromatic residual without
re-enumerating placements or calling a solver.

As concrete bridge checks, the first and last residual of each orientation
parity are reconstructed directly from their overlap pairs. Exact collision
merging gives 508 points in each case. All 515,112 unordered pairs are tested,
recovering respectively **2,515, 2,468, 2,492 and 2,468** unit edges. All 9,943
edge inequalities pass explicit four-colourings in [EXPECTED.json](EXPECTED.json).
These are four samples, not a complete geometry replay of all residuals.
The infinite theorem, not sampling, establishes the closure.

The same fixed field colouring on `L` extends in all four samples; indeed
the proof gives this extension for every two-overlap placement. Sample point
order is `L` in archive order followed by previously unseen images of `S+`
in archive order. Edge hashes use compact JSON of sorted index pairs.

## Reproduce and scope

From this directory in a full repository checkout, Python 3.11+ standard library:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py
python3 -B -O verify.py
python3 -B controls.py
```

Verification takes about one second on the recorded host. Normal and optimized
runs agree. Controls check both rotation signs, eight radical basis products,
25 separate norm identities, malformed colours, unmerged collisions, and the
hypothesis boundary: the original Parts placement has **one** overlap,
509 points and 2,442 complete unit edges. Its non-four proof is not replayed.

Trust rests on the imported reviewed field theorem and its colouring code,
the pinned coordinate identification, exact integer/Fraction arithmetic and
the ordinary isometry argument. The new adapter uses sparse radical products
and a separate two-coefficient norm formula; it is an author check, not an
independent review or formal proof. No floating-point unit test or SAT verdict
is a premise. Input hashes and [VALIDATION.json](VALIDATION.json) record provenance.

This class is retired. The conclusion also colours every subgraph of a union
with two overlaps. It **does not** decide capped subsets of a zero- or
one-overlap union, incomplete gadgets with a different budget, added points,
or other sources. It provides no reason to start such variants. The record
remains 509, as reported by [Parts](https://arxiv.org/abs/2010.12665) and
[Haugland](https://arxiv.org/html/2608.04542v4).
