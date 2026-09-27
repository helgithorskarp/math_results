# Sources and dependency boundary

The sole target is the bounded-law dimension-three case of Conjecture 1.1
in [Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
checked live on 27 September 2026. The paper's Gaussian product formula,
equation (61), is the primary analytic input. Its pressure hierarchy and
higher-dimensional lift do not by themselves sign the beta test here.
No historical-priority claim is made for the elementary ingredients or
for the searched-source novelty of their combination.

The following source commits were read from the current repository:

- The [relative moment-gap proof](../gaussian_contraction_moment_gaps/PROOF.md),
  commit `a0988e688107443394da70b00827d2a52a2179ad`, gives the
  distinguished-pair identity and monotonicity of B_m. These are
  prerequisites, rederived in Section 2 to make the normalization auditable.
- The [Hankel and lift proof](../gaussian_majorisation_hankel_transport/PROOF.md),
  commit `6f51c67737051a61290c070c9fb960e1da83b75b`, gives the hinge-moment
  normalization and positive lift measure. The present construction uses
  the distance-affine six-dimensional interpolation with the same Gaussian
  product calculation. It assumes no unproved Hankel positivity.
- The [global coupling and beta criterion](../gaussian_majorisation_global_criterion/PROOF.md),
  commit `713e542a0bd389681a3fb4ee0c0b61a4f272f104`, explains exactly how
  every beta sign would settle the fixed-pair question. The new theorem
  establishes one additional required sign; it does not establish that
  criterion's missing universal hypothesis or its zero-defect coupling.
- The [earlier replica-curvature proof](../gaussian_replica_curvature_sparse_energies/PROOF.md),
  commit `5586f0d772d6b7861bd73207901e183690f4d22b`, already averages two
  extra replicas and proves a radius-dependent near-log-convexity bound.
  It also disproves exact replica log-convexity. The new inequality
  `B_4 B_2^2 >= B_3^3` has a different exponent and no radius loss. Its
  proof discards the nonpositive square in Q_4 and applies two convex-power
  Jensen inequalities. It neither repeats nor contradicts the earlier
  near-log-convexity statement.
- The accepted [seven-factor theorem](../gaussian_seven_factor_kernel/PROOF.md),
  commit `f5bbd92be43517c18a6958acf900ddd67bac62f8`, signs every b_(j+7,j)
  and, with its predecessors, all entries of rows N<=7. It is not needed
  to prove the new inequality for b_(8,0); it supplies the stated corollary
  that row N=8 is now fully signed. No other new diagonal is asserted.
- The accepted [conditional-kernel rank classification](../gaussian_conditional_kernel_obstruction/PROOF.md),
  commit `01e1684e032295ee1c4bf11f2bca7836912258e7`, obstructs all-order
  positivity for fixed tuples at paired rank six. The new proof averages
  extra replicas against their common law before its key inequality, so
  it does not assert the representation excluded by that result.

The bounded team/source refresh also found an explicit
[all-threshold rational cell](../gaussian_frontier_middle_cell/PROOF.md)
at commit `daa4dc44a121df7fd8ed8e34d4769a799018a94d`, and the
[source-cluster defect estimate](../gaussian_prior_localization/CLUSTER_DEFECT.md)
at commit `e8f0528f71f366a945090afa8a1ebb5b160e4825`. These are
complementary author results. They are not premises of the present proof.
The accepted unrestricted defect cap and the full compact frontier are
unchanged: a positive error bound is not a sign, and one signed beta row
does not cover every middle-interval obligation. The new estimate is
uniform over every cell and every bounded law, without running the
finite-atomic certification lane's method.

Researcher 4's accepted
[straight-path pair obstruction](../gaussian_straight_path_pair_obstruction/PROOF.md)
concerns individual posterior pair actions along a different interpolation.
The distinguished-pair weight used here is the nonnegative squared-distance
loss in the replica identity, not that posterior action. No claim of
pairwise straight-path hinge positivity or ordered-contact flux positivity
is made. The geometric Kneser--Poulsen classes and the functional zero-defect
bridge remain separate from this result.

The scalar minorant, its compact rational certificate and the use of the
new nonlinear replica bound to prove b_(8,0)>=0 are the substantive new
content of this packet. The code is original supplementary source and
imports no prior certificate. Independent review is pending; the internal
algorithm agreement is not presented as independent acceptance.
