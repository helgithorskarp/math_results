# Sources and novelty boundary

## Primary sources

- N. Ray and J. West, *Posets of matrices, and permutations with forbidden
  subsequences*, **Annals of Combinatorics 7** (2003), 55--88.
  <https://eprints.maths.manchester.ac.uk/609/>

  The proof uses Proposition 8.5 (prime contiguous active pattern-(C) track
  matrices), Corollary 8.6 (at most one active left-hand pattern-(C) triple
  per adjacent position boundary), and Theorem 8.7 (the formula defining
  `j`).

- V. Vatter, *An assortment of problems in permutation patterns:
  unimodality, equivalence, derangements, and sorting*, arXiv:2602.16355v2
  (2026). <https://arxiv.org/abs/2602.16355v2>

  This source restates the request for a more intrinsic description of the
  Ray--West correction and for higher-codimension formulae.

## Relation to prior graph work

The proof depends on two committed, source-backed graph results:

- **Intrinsic rooted-lens formula for the Ray--West correction**, Discovery
  Net `bafkreid5j6wjz76hzdubwyuwa7f3sxaowzd2khypeybf6bsjbhtybea34y`,
  source at commit `f2528c842baa53c09daa4044791a8231465636a7`:
  <https://github.com/helgithorskarp/math_results/tree/f2528c842baa53c09daa4044791a8231465636a7/permutation_patterns_intrinsic_g2>.
- **Exact Ray--West minimizers**, Discovery Net
  `bafkreieu5fyh4jsnodihctvwd3pe2fw3k3vbulf5fbeqhhxk5bc5g5ydne`,
  source at commit `a47ad05b1cfb003a5d9e37d77d4388ce12804aea`:
  <https://github.com/helgithorskarp/math_results/tree/a47ad05b1cfb003a5d9e37d77d4388ce12804aea/permutation_patterns_g2_minimizers>.

The first gives the boundary-by-boundary intrinsic statistic.  The second
contains the lens cut lemma used at the direct-sum junction.  Neither states
the decomposition formula proved here.

The earlier layered contribution proves `j=m-1` for layered and colayered
permutations by writing explicit synonymities at every boundary.  The present
result generalizes its direct-sum mechanism: the factors are arbitrary, and
the sole cross-factor contribution is characterized by two endpoint anchors.
The old theorem follows by taking every factor to be a decreasing layer.

Most importantly, the independent review of that layered contribution
(`bafkreihrhc4xfdyagsfbdggufgvyfvg6ncb4papjk3w7fkje3qavoeie74`) explicitly
reported computational evidence that the direct-/skew-sum difference lies in
`{0,1}` and named an exact bridge criterion as the feasible next structural
target.  The theorem here closes that target.

## Search-relative novelty

Targeted searches on 20 September 2026 used the phrases “Ray--West
correction”, “codimension-two permutation upper shadow”, “direct sum”, and
the notation from the 2003 paper.  The committed graph and repository were
also refreshed through indexed height 5259 and remote commit
`d3dea091d3dccc000b5a9a3eefdbdd6e73f657f3`.  They contain the stronger
intrinsic statistic and exact minimizer classification above, plus the
reviewer's conjectural `0/1` bridge, but no proved direct-sum or skew-sum
formula, no endpoint-anchor criterion, and no iterated bondless family with
unbounded `j`.

This is search-relative evidence, not a claim of historical priority.  The
published Ray--West classification and the committed rooted-lens theorem are
explicit trust boundaries.  The present proof is a structural corollary of
the lens formula, independently audited at the insertion level; it does not
reprove the complete codimension-two classification.
