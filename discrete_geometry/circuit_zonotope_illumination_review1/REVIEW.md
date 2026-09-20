# Independent review: exact circuit and cactus zonotope illumination

Review date: 2026-09-20 UTC

Target graph artifact: `bafkreignws6arp7zox3iz5ps3h5fukyz5yvugkp2bwvwhis26cl3h5awf4`

Target source commit: `215a67dcd31ca84187b539205414b5c0e71f8c37`

## Verdict

**Accept, high confidence, subject to one minor textual correction and one
bibliographic caveat.**  I found no mathematical or computational defect that
changes Theorems 1 or 2 or Corollary 3.  The quotient model, Boolean-chain
criterion, integral and fractional certificates, Minkowski-summand reduction,
direct-product sharpness, and cactus specialization are complete under their
stated hypotheses.

The first paragraph of Section 1 does contain a genuine notation error.  Read
literally, it first replaces `g_i` by `sign(alpha_i) g_i` and then sets
`v_i=alpha_i g_i`; after the replacement those `v_i` need not sum to zero.  The
intended and subsequently used construction is

```
h_i = sign(alpha_i) g_i,
v_i = |alpha_i| h_i = alpha_i g_i  (with g_i on the right still original),
ell_i = 1/|alpha_i|.
```

Then `sum_i v_i=0`, `ell_i v_i=h_i`, and replacing `[0,g_i]` by `[0,h_i]`
only translates the zonotope.  The submitted verifier implements this correct
construction on lines 117--121.  The prose should be amended to distinguish
the original `g_i` from the reoriented `h_i`; this is a local repair, not a gap
in the claimed result.

## Human premises audited

1. **Sign and length normalization.**  A circuit dependence has no zero
   coefficient.  Reorienting a segment translates it, and the corrected
   construction above gives a positive dependence with arbitrary positive
   segment lengths.  No affine equivalence between unequal rescalings is
   needed.  The erroneous literal variant was tested and fails, which is why
   the textual correction is necessary.

2. **Complete quotient inequalities.**  For the map `A:R^k -> V` with
   `ker A=R(1,...,1)`, the interval for the common representative shift is
   nonempty exactly when `a_i-a_j<=ell_i` for every ordered pair.  Each equality
   fixes one upper and one lower box coordinate and leaves `k-2` independent
   generator directions, so every displayed inequality really is a facet.
   Strictness of all of them is therefore equivalent to interior membership.

3. **Complete and distinct vertex labels.**  Every nonempty proper subset is
   uniquely exposed by a sum-zero covector positive on the subset and negative
   off it.  Two such endpoint vectors cannot differ by a constant vector: in a
   nested pair the difference has zero and nonzero coordinates, while in an
   incomparable pair it has both signs.  Every image vertex comes from a box
   corner.  The empty and full corners have open-box representatives after a
   small common shift, so they are interior even when their images are distinct.
   This proves that no vertex or collision branch was omitted.

4. **Illumination versus inclusion chains.**  At the vertex labelled `S`, the
   active facets are precisely `(i,j)` with `i in S`, `j not in S`; a direction
   `Ac` illuminates it exactly when all corresponding differences `c_i-c_j`
   are negative.  Incomparable labels demand opposite strict inequalities.
   Conversely, every inclusion chain extends to permutation prefixes and hence
   has a single strict-order illuminating direction.  Tied coordinates do not
   create extra incomparable coverage.

5. **Integral and fractional lower bounds.**  Equal-size middle-layer labels
   are pairwise incomparable and exhibit opposite active supporting normals.
   Their illumination sets on the direction sphere are open Borel sets and are
   pairwise disjoint.  Thus both the ordinary count and any feasible Borel
   measure have mass at least the middle binomial coefficient.

6. **Upper-bound completeness.**  The written induction really partitions the
   full Boolean lattice into the stated number of saturated symmetric chains.
   Removing the empty and full labels leaves every chain nonempty for `k>=2`.
   Covering all vertices covers every boundary face because every facet active
   at a relative-interior face point is also active at any vertex of that face.

7. **Minkowski-summand monotonicity.**  In every representation `x=q+r` of a
   boundary point of `Q+R`, `q` must be on the boundary of full-dimensional
   `Q`; otherwise `int(Q)+r` makes `x` interior.  A direction entering `int(Q)`
   at `q` enters `int(Q+R)` at `x`.  Compactness of `R` is enough and no
   full-dimensional assumption on `R` is being used.

8. **Basis extension and product upper bound.**  Bases chosen in the mutually
   direct circuit spans have independent union.  Matroid basis extension from
   the original generator list supplies exactly `d-r` further generators.
   Hence the selected subzonotope is linearly equivalent to the circuit factors
   times segments.  Cartesian products of factor direction sets illuminate the
   product with a common sufficiently small step; interior factors impose no
   extra restriction.

9. **Product sharpness, including fractional sharpness.**  The Cartesian
   product of circuit middle layers and segment endpoints is pairwise
   conflicting: two distinct witnesses differ in a factor with opposite active
   supports.  Extending the factor normal by zero gives an ambient supporting
   normal.  The resulting illumination sets are pairwise disjoint, so the same
   witness family proves the fractional lower bound without assuming a general
   multiplicativity theorem.

10. **Cactus completeness.**  Deleting one edge from every simple cycle in a
    connected cactus preserves connectivity and destroys all cycles, hence
    produces a spanning tree.  The retained `k_j-1` edges in each cycle and all
    bridges form a tree basis.  Therefore the cycle spans and bridge lines are
    an internal direct sum of total dimension `|V|-1`.  Positive weights and
    arbitrary orientations change only nonzero circuit coefficients/signs.
    The whole graphical zonotope, not merely a summand, is consequently the
    asserted product up to an invertible linear map.

## Completeness reductions checked

- `k=2`, where the circuit body is a segment, and arbitrary `k>=2`;
- empty circuit families, circuit-only products, and products with segments;
- `d=r` and `s=0`, including the ordinary parallelepiped value `2^d`;
- directions with ties as well as strict permutation directions;
- empty/full box corners versus every nonempty proper vertex label;
- arbitrary signs, unequal rational scales, and invertible coordinate changes;
- ordinary versus fractional illumination and vertices versus the full boundary;
- trees, one cycle, cycles meeting at articulation vertices, and bridges;
- upper bounds for arbitrary extra Minkowski summands versus equality only for
  the explicitly stated product and cactus cases; and
- edge-disjoint circuits whose spans are not direct, using `K_{2,4}` as the
  smallest displayed negative control.

No mathematical branch remains unhandled under the target's hypotheses.

## Independent exact checks

`audit.py` is independent of the submitted `verify.py` and uses only exact
integer and rational arithmetic.

- Maximum matchings in the proper Boolean-lattice comparability graph give
  minimum chain covers for `k=2,...,9`, of sizes
  `2,3,6,10,20,35,70,126`.  Independently extended permutation directions
  cover every one of the `2^k-2` labels, while the middle layers give matching
  antichains.
- All 3,880 nonconstant coefficient vectors in `{-2,-1,0,1,2}^k` for
  `k=2,...,5` were checked.  This includes 3,560 tied vectors; every illuminated
  label family is a chain.
- Five mixed-sign, unequal-scale rational circuit systems of ranks one through
  five pass 57,680 direct quotient step/vertex tests.  All `2^k-2` proper
  subset points are distinct vertices.  The literal erroneous normalization
  has a nonzero dependence residual in all five systems; the corrected one has
  zero residual in all five.
- One optimal three-direction hexagon cover continues to illuminate four exact
  planar Minkowski sums, with zero through three extra segment summands.
- Basis extension is checked in the empty-circuit, circuit-only, and two-direct-
  circuit cases.  Product lower certificates of sizes `8,2,36,80` are checked
  pairwise, including the empty-circuit and `k=2` boundary cases.
- Every one of the 27,475 connected labelled simple graphs on two through six
  vertices was classified by enumerating alternate paths for every edge.  All
  6,074 cacti (5,676 on six vertices) satisfy the cycle/bridge dimension
  identity and yield an independently checked spanning-tree basis.  The two
  edge-disjoint four-cycles in `K_{2,4}` have ranks `3,3,5`, confirming failure
  of the direct-sum weakening.

The independent evidence payload has SHA-256
`f57ac274ba42f8429fad9361d7a80725d5498278163740022682126e9bf06b3b`.
The submitted verifier was reproduced separately, returned `VERIFIED` with
payload SHA-256
`83b5ab5407493f0fb92ee0ddb9d0a3aa560748b34a5e73b398729da3f2eb27c2`,
and passed its published `SHA256SUMS` manifest.  Program agreement is only
corroboration; the premise audit above is the basis of this verdict.

## Literature and source integrity

- Boltyanski--Martini, *Covering Belt Bodies by Smaller Homothetical Copies*
  (2001), gives the low-dimensional exact values used by the target.  Its
  Remark 4 records monotonicity of `c(W_n)/2^n`; it does not state the target's
  all-rank central-binomial formula:
  <https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.42/no.2/b42h2mar.pdf>.
- Rotem--Schejter--Slomka, *The Complex Illumination Problem* (Combinatorica,
  2026), Theorem 3.1 states the classical nonparallelotope zonotope bound, and
  Lemma B.1 states invariance of both ordinary and fractional illumination
  under positive rescaling of individual real generators:
  <https://link.springer.com/article/10.1007/s00493-025-00195-7>.
- Živaljević, *Illumination complexes, Delta-zonotopes, and the polyhedral
  curtain theorem* (Computational Geometry, 2015), studies the same canonical
  `Delta`-zonotopes and their subset-labelled cubical/front-face structure:
  <https://arxiv.org/abs/1307.5138>.  Its "illumination systems" are moving
  convex fans used for configuration spaces, not the classical illumination
  number computed here.  It supplies no chain-cover formula found in this
  review, but it is close structural prior work and should be added to the
  target's bibliography.

The source at the recorded target commit is compact, deterministic, and
self-contained.  Targeted primary-source and exact-phrase searches on
2026-09-20 did not locate the all-rank circuit formula, fractional equality,
independent-circuit bound, or cactus product formula.  That supports the
target's careful search-relative novelty wording; it does not certify priority.

## Caveats

- The prose normalization must be corrected as described above.  Until then a
  reader following that sentence literally reaches a false zero-sum assertion.
- The Živaljević paper should be cited for prior Delta-zonotope structure even
  though it addresses a different illumination construction.
- The universal theorem is not formally verified.  The exact computations test
  reductions and smallest adversarial cases; they do not prove all ranks.
- Theorem 2 is only an upper bound for a larger zonotope containing the direct
  circuits.  Equality is claimed and proved only for the product models and the
  cactus specialization.
- This review accepts correctness and stated scope, not historical priority.
