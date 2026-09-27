# Sources, dependencies and trust boundaries

The sole problem source is Gautam Aishwarya and Dongbin Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
arXiv:2609.07041v2, reread 27 September 2026. The full dimension-three
question is not resolved here. Its Theorem 1.4 and the two-coordinate
Gaussian marginalization are prior ingredients behind the comparison
used below; neither is claimed new.

Classical Euclidean Kirszbraun extension permits a map specified on a
finite or bounded support to be evaluated on its plane projection. If T
is already global, no extension is needed. The theorem never assumes that
orthogonally projecting the source while keeping the original target
labels preserves contraction. It uses `T(PX)`, and proves a coupling bound
to `T(X)`. The certificate requires no algorithm for constructing that map.

## Mathematical inputs

- R2's concurrent [marginal covariance guard](../gaussian_covariance_collapse_guard/PROOF.md),
  graph6442 `bafkreibu6ndtzdch7bpiqxfolh7fcs4oykqd5ep2btts4fyrkptao736ki`,
  source `b3ecb0d0d611bd4bee0c83f26c648716176c9626`, already proves
  signs for all `u>=1/64` at normalized source radius at most `1/2`,
  when either marginal covariance has a direction at most `2^-86 D^2`.
  Source and target plane projections, loss retention and the resulting
  boundary exclusion are shared mechanisms and are credited to that
  publication. Its full proof and exact certificate were read after the
  concurrent refresh. This packet is scoped to arbitrary bounded radius,
  any positive threshold floor, and a margin through the source peak.
  Its more conservative `D^10` cutoff does not imply R2's sharper `D^2`
  cutoff. Neither packet independently accepts the other. R2's existing
  exact completion-of-squares producer can supply a direction for a
  rational covariance ceiling; this packet checks a supplied direction
  and does not duplicate that spectral producer.
- R6's [target-peak quantitative motion margin, Theorem H2](../gaussian_axial_cone_rotations/HINGE_MARGIN.md),
  graph6264 `bafkreigm6usjhweqdxfahzlusvbe4x2vhhn27dyqqkq5wlkcb6nnechbbm`,
  source `32f04f8f67c0dae00eda7443912cb5b3a0ca2f02`, supplies exactly
  (15) in PROOF.md. Its full source- and target-peak arguments were read,
  including the terminal-loss and two-coordinate steps. This is an
  explicit author theorem; no independent acceptance of this quantitative
  annex was found in the refreshed neighborhood. The present packet is
  a new consequence, not a review or independent acceptance of H2.
- The [paired affine-rank comparison](../gaussian_majorisation_rank_abel/PROOF.md),
  graph5964 `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu`,
  source `f7c122d6a5ade217930d63da27e67f9a9e55a539`, already includes
  every planar source or target. We explicitly construct its elementary
  R2-plus-R3 and R3-plus-R2 lifts. Exact planarity
  is an existing full comparison, not the contribution of this packet.
- The [earlier posterior peak theorem C](../gaussian_contraction_rigidity/PROOF.md),
  graph `bafkreiheirbfdiqq4igulat36rylgtda5zd2jc2ksdrif3qildy7ulnvy4`,
  is credited for (11). Our proof recalls the Jensen argument and derives
  the bounded-radius coefficient in (12) so this normalization is visible.
  Entropy monotonicity by itself is not used to infer a hinge sign.

Gaussian translation bounds, orthogonal projection and centered-L2
triangle inequalities are elementary prior tools. The contribution is
their quantitative assembly with the target-peak margin, yielding a
uniform signed neighborhood of either covariance boundary for every fixed
positive-loss/threshold slab. The explicit scalar constants are sufficient
and deliberately conservative. No historical priority certification is
made; a bounded primary-literature search found no additional theorem
imported as a premise.

## Minimal R2/R3/R8 handoff

The [effective small-loss theorem](../gaussian_effective_mean_loss/PROOF.md),
graph6426 `bafkreieyattiaogc4s7iosnunxfq3yi6sy2enhq23ftgtoua7fz22zb6ni`,
source `f171c499bc0ed272d1b6fd5f78d57968d1578b62`, is now independently
[accepted at6432](../gaussian_effective_mean_loss_review_r4/REVIEW.md),
review source `6ebac9c96dcf201db531c08abe180644958191b9`.
R8's alternative [midpoint proof](../gaussian_mean_loss_margin/EFFECTIVE.md),
source `9117b9b64127df8ee18337d9205e4aa7a9b70960`, also received
[acceptance6434](../gaussian_midpoint_polarization_review2/REVIEW.md),
review source `92edf5560c66756e311088908f8e54b11408b1f9`.
Those effective-cutoff obligations are closed; this packet does not
repeat them. It instead removes covariance collapse on a slab where
loss is bounded below. The simultaneous zero-loss/covariance corner
remains outside their demonstrated combined coverage.

The accepted [paired cubature](../gaussian_prior_localization/LOSS_CUBATURE.md),
graph6364/6380, mathematical source
`afacddeb257993b31ee118ff92e7360a7870cbc6`, preserves this guard when
it retains marginal means and second moments on original paired sites.
The marginal means, radius bound, both covariances and mean pair loss all survive.
No extra mixed features are needed. R2 can evaluate the guard before a
moment or hinge oracle. No uniform diffuse-law integration oracle,
rational rounding guarantee, or complete finite cover is asserted.

The prepublication refresh also inspected R5's
[averaged replica rank gap](../gaussian_averaged_replica_rank_gap/README.md),
source `5a2b55eca217a7fd7a0d035757eb29124bd5a204`, and R1's
[regularized-contact margin](../gaussian_regularized_contact_margin/README.md),
source `7e8165706d3dac6827e766b9a7359de4d180110e`.
Their averaged-replica and unbounded-contact routes are separate. Neither
is used to prove this bounded-law projection theorem. The geometric
motion classes retain their stronger all-variance and ball-volume claims;
the current finite-noise/threshold guard adds no such conclusion.

The statement and handoff of R3's concurrent
[small-loss defect theorem](../gaussian_small_loss_defect/README.md),
source `07bbadcb55bda83457a298a8e30afddcc2ffd993`, were also inspected.
It moves a signed threshold toward zero as loss decreases under a fixed
positive source covariance floor. That is a different hypothesis from
the positive-loss covariance boundary here. It is not a premise, and
combining the two does not close the simultaneous loss/covariance limit.

## Reproducibility and remaining obligations

`verify.py` uses exact rational arithmetic and standard-library integers.
It compares sixty parameter schedules against 660 expanded sufficient
budgets, checks 2209 logarithm controls, all 91 pairs of explicit original
and projected source labels, 21 target-projection pairs, and two nonzero
paired affine-rank-six determinants. It checks independent translations, coordinate rotation,
direction rescaling, Gaussian variance normalization, zero-weight labels,
known planar/isometric branches, equality at both sufficient cutoffs,
unresolved guards and thirteen damaged
inputs. A huge-radius schedule stays compressed.

The expected record is fixed and read only in ordinary verification.
These checks establish finite algebra and software behavior, not the
universal analytic estimates or independent mathematical acceptance.
There is no Gaussian quadrature, floating-point sign, solver, private
input or omitted large certificate. The two seven-label fixtures
calibrate the guard; they are not claimed outside every existing positive
class, and do not themselves prove the uniform theorem.

Remaining obligations are the positive-covariance interior at positive
loss, the joint zero-loss/covariance corner, and low thresholds. The new
counterexample covariance floor is explicit on each prescribed slab;
it does not by itself settle those remaining signs or improve the
unrestricted numerical defect bound. Both this argument and any novel
historical claim await independent assessment.
