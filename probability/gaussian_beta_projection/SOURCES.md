# Attribution and dependency boundary

The sole research target is the full dimension-three question in
[Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
The paper was checked live on 26 September 2026. Its Gaussian product
and lifting mechanisms are prior work. The finite-difference sign proved
here uses the Gaussian product identity directly; it does not assume
the desired majorisation or a five-dimensional contraction of the labels.
No general novelty or historical-priority claim is made.

The following exact source commits were inspected in this pass. Reader
links use the repository's main branch; hashes are recorded separately.

- Researcher 8's [beta weight-cell proof](../gaussian_beta_weight_certificate/PROOF.md),
  commit `a006501b012a7084676d632df4d73af1fdd92a58`, supplies the
  polarization formula, its combinatorial normalization and the positive
  product when the full paired affine rank is at most five. Its numerical
  theorem signs row five on a particular metric cell at variance one.
  The present projection removes that cell restriction for the qualitative
  sign and proves six columns at every degree. It does not reproduce or
  replace the cell's quantitative margins. This is researcher 8's source,
  interfacing with researcher 2's finite-atomic work.
- The existing [Hankel/replica source](../gaussian_majorisation_hankel_transport/PROOF.md),
  commit `6f51c67737051a61290c070c9fb960e1da83b75b`, gives the moment
  normalization, Gaussian replica identity and distinguished-pair
  differentiation. These are rederived for clarity and credited, not
  presented as new ingredients.
- The existing [global criterion](../gaussian_majorisation_global_criterion/PROOF.md),
  commit `713e542a0bd389681a3fb4ee0c0b61a4f272f104`, identifies all beta
  signs with the full question. The present proof establishes signs on
  an infinite strip of that criterion, rather than another equivalence.
- Researcher 3's [rational interface](../gaussian_prior_localization/RATIONAL_INTERFACE.md),
  commit `92c30828d980c4e556a25a49035ab0e39b6541ce`, and researcher 8's
  [uniform moment frontier](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md),
  commit `88bc098a0f98080f8762ddae9b11cc4e63669e95`, are downstream
  consumers: the six columns need no geometric or weight subdivision.
  Their remaining degrees, rounding, error budgets and unsigned compact
  maxima are unchanged. These reductions are not premises of the sign proof.
- The [paired-rank source](../gaussian_majorisation_rank_abel/PROOF.md),
  commit `f7c122d6a5ade217930d63da27e67f9a9e55a539`, retains the full
  comparison for at most six atoms and the seven-atom necessary boundary.
  The new row/column result does not raise that atom boundary: repetitions
  are permitted in higher-degree replicas. Its distinction between an
  actual five-dimensional realization and a six-dimensional lift is kept.

The new ingredient is the centroid projection identity (9)--(10) in
PROOF.md and its use separately in each positive Gaussian block. The
omitted squared energy is independent of the subset of remaining labels;
this supplies the sign instead of an absolute-error estimate. The
identity itself is an elementary consequence of the classical Gaussian
product formula. Source publication and the exact algebra audit do not
constitute independent acceptance.

The accompanying audit is original, self-contained supplementary code.
It imports no prior certificate, exact-bounds module, dataset or solver.
The proof has no unreported computational premise or omitted large artifact.
