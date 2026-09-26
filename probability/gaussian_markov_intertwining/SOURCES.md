# Sources, dependencies, and claim boundary

Checked 26 September 2026. The result is an author-proved obstruction to
one proposed method. Independent review is pending. No full R3
Gaussian-majorisation or new Kneser--Poulsen theorem is claimed.

## Primary literature

1. Gautam Aishwarya and Dongbin Li, *Gaussian Convolution, Internal Energies,
   and the Kneser--Poulsen Conjecture*,
   [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
   Conjecture 1.1 is the campaign's sole problem. Theorem 1.3 includes
   full majorisation in dimension one, used as the positive control for
   every law on the three test sites. Tensoring with a common Gaussian
   supplies the stated R3 control. The introductory anisotropic example
   already shows why arbitrary initial majorisation need not persist
   under heat flow; we do not republish that observation as new.

2. Giacomo De Palma, Andrea Mari, Vittorio Giovannetti and Alexander S.
   Holevo, *Normal form decomposition for Gaussian-to-Gaussian
   superoperators*, [arXiv:1502.01870](https://arxiv.org/abs/1502.01870),
   [primary manuscript](https://arxiv.org/pdf/1502.01870), Theorem III.2.
   It classifies Feller operators on finite measures that preserve all
   Gaussian measures. The hypotheses differ: our channel is already
   positive and normalized; only one input covariance and one common
   output covariance are tested, on an open set of means; there is no
   Feller hypothesis. The general affine-Gaussian classification theme
   is established prior work. This note provides a self-contained
   fixed-covariance proof and an explicit finite error certificate for
   the proposed majorisation method, not a priority claim.

Holder's inequality, uniqueness of Fourier transforms of finite
measures, and elementary uniqueness for real analytic functions are
standard analytic inputs. Their applications and the necessary
integrability are explicit in PROOF.md. The finite constant check uses
pi<4, Gaussian integration, and rational Taylor-tail estimates. No
unquoted numerical enclosure from the literature is required.

## Durable campaign inputs

* Researcher 1, [ordered heat-contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md),
  graph height 6140, `bafkreibrti7gur7ddhxqck2kq7lco2x6lmosmorbytzjfzb26qufiasy3m`;
  source commit `1d1f1c6e58ceb3010e05dcbe5fc477f4c7edde6f`.
  It supplies the still-open equivalent sign `J_f>=J_g` at ordered
  contacts. This note neither changes its hypotheses nor proves the sign.

* Researcher 5, [Hankel/transport proof, Section 4](../gaussian_majorisation_hankel_transport/PROOF.md),
  height 5962, `bafkreids462diitdof5ijilzcq2xqwftk2bzjr5t2gihnxk327uezbndbm`.
  The earlier obstruction is to the Lebesgue row bound for every fixed
  orthogonal common-noise coupling, even though that reverse posterior
  kernel may depend on the prior. The present result uses a different
  quantifier and does not purport to exclude arbitrary prior-dependent
  couplings.

* Researcher 5, [global density-value criterion](../gaussian_majorisation_global_criterion/PROOF.md)
  at height 6088, `bafkreihp3see622wt3h2fxowhnp6cj4jtz5t53dxp5bmerz7aj5tfo2eeq`,
  and [fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md)
  at height 6112, `bafkreievpgikszwz2kggan4dnfbbhvtvjohiycou6xuhlsqpxjvvxrhaai`.
  These permit dependence on the prior and retain arbitrary rare
  packets. They do not require a universal spatial Gaussian channel.

* Researcher 3, [common-set formulation](../gaussian_prior_localization/PROOF.md),
  height 6122, `bafkreiam5rzibygouwnzj7aokt23ld4twuarsvrpr4ffdxvokehvtl7gd4`.
  Its target test set may depend nonlinearly on the source test set.
  It does not supply or demand a linear operator on test functions.

* Researcher 5, [latest eight-lane interface](../gaussian_majorisation_global_criterion/INTERFACES.md),
  height 6144, `bafkreiacdj7cffmui6ee56u5p5tnk7kqninqt75gjrqa6u3eohnqdq3b54`;
  source commit `8b004c6a747883fcf96f895a052a292a62683f5f`.
  Its compact moment and fixed-atom bounds do not assume the channel
  ruled out here. The distinction between law-dependent endpoint
  criteria and universal linear constructions is essential.

* Researcher 4, [three disjoint cap reflections](../gaussian_disjoint_cap_reflections/PROOF.md),
  height 6146, `bafkreidc5kg5ekkk4drpdjpfgnr7frbhubsk77pncxp6vuizyvcedi6nay`;
  source commit `bd57aa06efc46fd737b962bbd6d96384c4efdf2c`.
  Its broad all-prior Gaussian and Kneser--Poulsen conclusions use an R5
  contracting motion. A nonaffine cap map on a full-dimensional convex
  domain cannot have the universal channel in Theorem 1; the geometric
  proof does not require it. This source was refreshed before submission;
  its independent correctness and priority review are still pending.

The pass also inspected the newest completed reports from researchers
2--8, and refreshed source and graph additions through height 6157.
Researcher 2's [exact common-set equality faces](../gaussian_majorisation_minimax_faces/PROOF.md)
at height 6142 are compatible: the selected reflection depends on the
source equality face, and its conclusion concerns a restricted family
of test sets. Researcher 3's [shift-averaging obstruction](../gaussian_prior_localization/SHIFT_AVERAGING_BOUNDARY.md)
at height 6148 closes a different proposed sign mechanism and preserves
the earlier localization. Researcher 8's [support-uniform modulus](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md)
at height 6150 improves an absolute approximation budget; it supplies
neither an exact sign nor a channel. Researcher 6's axial geometric work
and researcher 7's failed certified-counterexample searches also remain
separate routes. These are awareness inputs, not premises of Theorems 1--2.

## Reproduction and review scope

The self-contained analytic argument is in PROOF.md. The standard-library
program `audit.py` checks the three exact distance ratios, target
distinctness and midpoint defect, the likelihood-ratio slab exponents,
and the rational chain giving `1/648`. It does not verify the universal
analytic argument or certify a negative majorisation gap.

The expected JSON must match entry by entry. Normal and optimized Python
runs use explicit exceptions rather than removable assertions. The
manifest covers all public source and the expected record; no private
input, external certificate corpus, solver, or quadrature is needed.

A review should check the common-output-covariance cancellation in (8),
the extension from an open set of means, identification only almost
everywhere, the total-variation convention and denominator `1+C_0`, and
the difference between the positive-control majorisation statement and
the uniform-channel obstruction. The old contact proof and all other
lane sources are preserved.
