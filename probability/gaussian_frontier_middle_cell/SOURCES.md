# Sources and exact dependency boundary

The named problem is Gautam Aishwarya and Dongbin Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/abs/2609.07041),
arXiv:2609.07041v2. This package concerns its dimension-three full
majorisation question. It settles only the stated cell at variance one.

The computation consumes the R3
[absolute hinge quadrature](../gaussian_prior_localization/DIRECT_HINGE.md)
and [exact scalar implementation](../gaussian_prior_localization/direct_hinge.py).
Original source 2e0d74152db80935259c25142da0e42d37ff0399, graph 6228,
has [independent acceptance](../gaussian_direct_hinge_review_frontier/REVIEW.md)
at source 90f0acbbba998f8b46829656cce23fe40184d6f3, graph 6271. The consumed
file hashes are checked before import and recorded in EXPECTED.json.
Its trapezoidal error for nonsmooth hinges and omitted-lattice bound are
written theorem premises. We do not repeat the reviewer's audit.

The cell is interpreted using the R3
[paired-cubature frontier](../gaussian_prior_localization/CUBATURE_FRONTIER.md),
in its unchanged variance-one convention: A_1=39, L=256, W=156,
support radius 3, anchored first labels X_1=Y_1=0, and squared pair-loss
floor 1/256. Independent endpoint translations put every certified lattice
pair in that gauge; the anchor-zero slice is a 36-coordinate cell already
in the family. The definition is pinned.
The accepted generic [signed endpoints](../gaussian_prior_localization/SIGNED_ENDPOINTS.md),
source 7bec0b3ac781fcc74a3d003a1e4d9fca2335c2b1, graph 6287, explain the
remaining middle obligation. Its independent review is graph 6297, source
badd3c11367dd39655205eddb7208115b8c511f2. Its extremely small uniform cutoff
is not used in this cell proof: a direct clipped-density comparison supplies
the practical low endpoint. No claim about improving the general cutoff is made.

The hinge-level transfer is the perturbation principle used by R8's
[finite certificate and bounded-law interface](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md)
and its [stability theorem](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md).
Here the relevant total-variation estimates are proved directly, including
a centered second-order target estimate. The qualitative existence of
positive neighborhoods around a point-target comparison is credited to
that prior stability work. Only this explicit cell and finite uniform
margin are asserted as new campaign evidence.

The [paired-rank conditional-kernel classification](../gaussian_conditional_kernel_obstruction/PROOF.md),
source 01e1684e032295ee1c4bf11f2bca7836912258e7, original 6267, is independently
accepted at 6289 and 6293. It is a design constraint and a cited distinction,
not a positivity premise. This proof preserves actual endpoint hinges and
uses no individual conditional-kernel positivity. Nor does it require
termwise straight-path pair positivity, whose failure is separately recorded
in [the recent pair obstruction](../gaussian_straight_path_pair_obstruction/PROOF.md).

Gaussian multiplication, total variation, Taylor's formula, Jensen's
inequality, signed-permutation symmetry and finite piecewise-linear maxima
are standard ingredients. No historical priority claim is made. This author
package is not itself an independent review of any cited work. Its own
independent mathematical review remains pending.
