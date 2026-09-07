# Proof and certificate semantics

## 1. A root defined without a guessed number field

Let `m` be the rational vector of the 30 unpinned coordinates. Delete the already
satisfied pinned unit edge from the 31 equations. The remaining vector polynomial
`F : R^30 -> R^30` has coordinates

`F_uv(x) = (x_u-x_v)^2 + (y_u-y_v)^2 - 1`,

where pinned coordinates are constants. Let `J=DF(m)` and `R=J^-1`.
`seed.py` computes `R` by exact rational elimination and checks every entry of
`RJ=I` independently of the elimination state. Put `r=10^-18` and let `B` be the
closed infinity-norm ball of radius `r` about `m`.

Each row of `DF(x)-J` has at most four nonzero entries. Each varies in absolute
value by at most `4r`, so `||DF(x)-J||_infinity <= 16r` throughout `B`. Hence for
`T(x)=x-RF(x)`,

`||DT(x)||_infinity <= q := 16r ||R||_infinity`.

Exact rational computation certifies `||R||_infinity < 20` and
`||RF(m)||_infinity < 10^-24`. Thus `q < 3.2 * 10^-16 < 1` and

`||T(x)-m||_infinity <= ||RF(m)||_infinity + q r < r`.

The contraction mapping theorem on the closed ball gives exactly one fixed point
in `B`. Since `R` is invertible, it is exactly one root of `F` in `B`. Including
the pinned edge gives all 31 unit equations. Interval checks separate all 17
vertices and exclude unit distance at all 105 nonedges. The edge list has no
triangle. A complete DSATUR search with the pinned edge assigned colours 0 and 1
finds no three-colouring; any proper three-colouring could be renamed to satisfy
that pin. The positive words below supply four-colourings. The independent-set
control gives a separate combinatorial check of the lower bound.

Only existence and uniqueness in this box are asserted. No assertion is made
about the other real or complex roots of the same system.

## 2. A general finite transfer lemma for common-pair assemblies

Let `P={p_0,...,p_(n-1)}` be any finite set of distinct planar points. Partition its
unordered vertex pairs into groups `C_t` such that two pairs with the same length
always belong to the same group. For `a != b` in `P`, define the plane isometry

`N_ab(z) = (z-a) conjugate(b-a) / |b-a|`,

identifying the plane with the complex numbers. It sends `a` to zero and `b` to
`|b-a|` on the positive real axis. For every pair in `C_t`, take `N_ab(P)`,
`N_ba(P)`, and their complex conjugates, and call their union `U_t`.

**Transfer lemma.** If the full unit-distance graph of every `U_t` is
four-colourable, then the full unit-distance graph of any union of congruent
copies of `P` having two fixed distinct common vertices is four-colourable.

**Proof.** Call the two fixed vertices `A,B` and apply one global isometry sending
`A` to zero and `B` to `|B-A|` on the positive real axis. Each copy has some seed
vertices `a,b` as the preimages of `A,B`. They have length `|B-A|`, so all these
pairs lie in the same group. An isometry with those two prescribed images is
uniquely determined by whether it preserves or reverses orientation. Its image
of the copy is therefore one of the enumerated normalized sets, with reversal
of the ordered seed pair when needed. The complete assembly is a subset of one
`U_t`, including all additional contacts and coincidences. Restrict its colouring.
There are only finitely many normalized copies, so arbitrary collections,
including repeated copies or infinitely indexed collections, cause no change.

For the certified seed the checker includes all 136 unordered pairs exactly once.
For each group it encloses every squared pair length and takes the hull of those
intervals. The 89 hulls are pairwise disjoint; the smallest gap is at least
`78,367,003 * 10^-12`. Thus equal lengths cannot occur in different groups, exactly
the hypothesis of the lemma. Inside a group, extra pairs of possibly different
lengths merely enlarge `U_t`; exact equality inside groups need not be decided.
The four normalized frames per pair give 544 frames and 9,248 point labels over
all groups. The largest group has 31 pairs and 2,108 labels.

## 3. Interval words colour geometric unions, not just label graphs

For each normalized point label `i`, enclose its two real coordinates in a
rectangle `X_i`. Give it its certificate colour `c_i`.

The checker establishes for every pair of labels:

* If `c_i=c_j`, the interval for `||X_i-X_j||^2` excludes 1.
* If `c_i!=c_j`, the two coordinate rectangles are disjoint on at least one axis.

The second condition ensures that every occurrence of the same actual point has
the same colour. The first then ensures that the induced colour on actual points
is proper at every unit distance. These sufficient conditions avoid any need to
prove all the equalities suggested by numerical point deduplication or enumerate
the exact edges of the union. They are checked for every one of the 2,547,824
within-group label pairs. In particular no cross-copy edge is omitted.

Every nonempty normalized union contains a copy of the four-chromatic seed, so
its chromatic number is exactly four. Restriction proves the upper bound for any
subgraph selected from any common-pair assembly.

## 4. First circle completion

For each seed pair `a,b` let `d^2=|b-a|^2`. Interval bounds exclude 0 and 4 for all
pairs and certify that precisely 133 pairs have `d^2<4`. Their unit circles have
two intersection points,

`(a+b)/2 +/- i(b-a) sqrt(1/d^2 - 1/4)`.

The formula gives squared distance one from both centres by perpendicularity and
`d^2/4 + d^2(1/d^2-1/4)=1`. It gives both intersections and hence all possible
points common to those two circles. The other three pairs have `d^2>4` and no
intersection. Add these 266 labels to the 17 seed labels and apply the same two
colour-word obligations to all 39,903 pairs. They pass. The exact full support
therefore has at most 283 vertices and chromatic number four. No exact count
of distinct completed points is needed or claimed.

## 5. Outward arithmetic

All intervals have integer endpoints over `Q=2^100`. Input rational lower bounds
are rounded down and upper bounds up. Addition and subtraction are exact on this
grid. Multiplication encloses the four endpoint products using integer floor and
ceiling division by `Q`. Squaring uses zero as its minimum when the interval
contains zero. Reciprocal excludes intervals containing zero and uses outward
`Q^2 / endpoint` bounds, reversing endpoint order; negative intervals are handled
by negation. Division is multiplication by the reciprocal.

For a nonnegative interval `[l,h]/Q`, square-root endpoints are the floor of
`sqrt(l Q)` and the ceiling of `sqrt(h Q)`, both integers computed with `isqrt`.
The upper endpoint is increased exactly when the radicand is not an integer
square. Thus the square-root branch in normalization is positive, and all
circle-intersection branches are explicitly covered by their two signs.

The final same-colour distance check works directly over `Q^2`: coordinate
differences range from `a.lo-b.hi` to `a.hi-b.lo`; square each range with the
zero-crossing case and add. Both comparisons with `Q^2` are exact integer
comparisons. Different-colour coincidence exclusion is an integer comparison
of coordinate endpoints. No truncation, machine integer overflow, floating-point
rounding mode or solver result is part of this proof.
