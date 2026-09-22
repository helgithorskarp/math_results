# Sources and status boundary

## Primary mathematical sources

- N. Ray and J. West, *Posets of matrices, and permutations with forbidden
  subsequences*, Annals of Combinatorics 7 (2003), 55--88.
  <https://eprints.maths.manchester.ac.uk/609/>

  This is the source of the codimension-two active-insertion framework and the
  correction `j`.

- V. Vatter, *An assortment of problems in permutation patterns: unimodality,
  equivalence, derangements, and sorting*, arXiv:2602.16355v2 (2026).
  <https://arxiv.org/abs/2602.16355>

  This restates the intrinsic-statistic problem that motivated the graph
  program around `j`.

- F. Bassino, M. Bouvel, V. Feray, L. Gerin, and A. Pierrot, *The Brownian
  limit of separable permutations*, Annals of Probability 46 (2018),
  2134--2189; arXiv:1602.04960.
  <https://arxiv.org/abs/1602.04960>

  Proposition 2.13 records the size-preserving bijection between separable
  permutations and signed Schroeder trees with alternating signs.

- J. B. Gil, O. A. Lopez, and M. D. Weiner, *On separable permutations and
  three other pairs in the Schroeder class*, arXiv:2603.25528 (2026).
  <https://arxiv.org/abs/2603.25528>

  This is a current primary reference for multivariate enumeration of other
  positional statistics on separable permutations and for the large-Schroeder
  normalization.

## Direct dependency

The signed-tree marking lemma uses the previously proved exact direct- and
skew-sum locality law for `j`:

<https://github.com/helgithorskarp/math_results/tree/main/permutation_patterns_direct_sum_g2>

That result in turn depends on the intrinsic rooted-lens formula committed in
Discovery Net.

## Novelty boundary

Targeted searches on 2026-09-22 combined the terms Ray--West correction,
codimension two, separable permutations, signed Schroeder trees, and generating
functions.  They located the sources above and work on other statistics, but no
distribution formula for `j` on separable permutations.  Accordingly, the
claimed increment is search-relative: the local marked-tree statistic, its
bivariate quadratic equation, the exact first-moment series, and the resulting
mean asymptotic.

No novelty is claimed for the Ray--West definition, the canonical signed-tree
encoding, the univariate large-Schroeder series, or standard square-root
singularity transfer.
