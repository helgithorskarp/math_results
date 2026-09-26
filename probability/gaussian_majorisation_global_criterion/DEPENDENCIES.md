# How the Team B mechanisms certify the same global criterion

All statements below refer to `Delta_s` in [PROOF.md](PROOF.md). A zero
is full majorisation for the stated law and variance. The table preserves
the hypotheses of the linked proofs; it does not enlarge their classes.
Source commits and primary attribution are in [SOURCES.md](SOURCES.md).

## Geometric and mixture certificates

| Durable mechanism | Why it gives `Delta_s=0` | Scope and boundary |
|---|---|---|
| [Paired affine rank at most five](../gaussian_majorisation_rank_abel/PROOF.md) | A contracting motion in at most five dimensions gives the coupling of Theorem 1. | Every bounded law on a domain satisfying the rank condition, every variance; in particular the established small-atom range. Paired rank six is outside this certificate. |
| [Scalar-defect budget](../gaussian_majorisation_scalar_defect/PROOF.md) | The inequality `|dy|^2 + |e.dx-f.dy|^2 <= |dx|^2` constructs an explicit `R^5` motion. | All laws and variances on the certified domain. The nine-point norm-preserving reflection and the new 37-point damped example are excluded from this sufficient mechanism. |
| [Simplicial dual-cone reflection](../gaussian_simplicial_cone_reflections/PROOF.md) | Its explicit `R^5` contraction supplies the same endpoint coupling. | Arbitrary bounded weights and all variances on its full cone domain. The full nonsimplicial dual-cone map need not have such a motion. |
| [Axial cone rotation](../gaussian_axial_cone_rotations/PROOF.md) | The planar product-hull perimeter budget at most four constructs an `R^4` motion, padded to five. | All laws and variances; circular cone slopes satisfy `p q <= 2/pi`. |
| [Damped cone reflection](../gaussian_damped_cone_reflections/PROOF.md) | Its product-support path integral at most two constructs an `R^4` motion, again padded to five. | Circular slopes satisfy `p q F(lambda^2)<=2`, with `F(eta)=sqrt(1-eta^2)+eta(pi-arccos eta)+eta-1`. At `lambda=1` it recovers the undamped axial condition. Every proper dual-cone pair admits a positive damping range. This new geometric input is incorporated without a separate analytic subclass. |
| [Ray relabelling](../gaussian_ray_relabelling/PROOF.md) and [fixed-core relabelling](../gaussian_majorisation_fixed_core/PROOF.md) | An alternate contraction has the same output law and a lower-dimensional motion. Equality of output laws makes the global criterion identical. | The exact whole-radial-measure balances in those sources are essential. These are statements about a law as well as its labelled map. |
| [Common-target gluing](../gaussian_majorisation_common_target/PROOF.md) | Convexity in the source gives `Delta(sum alpha_i f_i,g)<=sum alpha_i Delta(f_i,g)`. | Component constructions must have **one identical target law**. The fixed-core/ray result allows the published open range of weights and arbitrary permitted radial laws. General paired mixtures with varying targets do not follow from this argument. |
| [Finite density-orbit comparison](../gaussian_majorisation_square_cone_orbits/PROOF.md) | The 48-element orbit hinge inequality integrates to `Delta_s=0` by (17), and hence supplies the endpoint coupling (4). | Every variance on the full radius-`1/552` nine-point weight ball and the stated arbitrary bounded radial laws with directional weights in two explicit cones. The exact computer-assisted proof awaits independent review. It does not require a centre motion or cover arbitrary weights. |

The damped-cone source also proves that an undamped **full** proper
dual-cone reflection has an `R^5` motion exactly when the cone is
simplicial. Its obstruction is to a motion of centres, not to the endpoint
coupling in our Theorem 1. The positive-operator ingredient in that
classification is classical and credited in the geometric source.

The moment criterion is invariant under separate endpoint isometries.
It therefore accommodates the endpoint congruences used in the motion
proofs. It also explains why full-dimensional paired-rank examples can
be positive: the rank certificate is sufficient, not necessary.

## Analytic completion and incomplete tests

| Durable input | Exact implication in the global criterion | What it leaves open |
|---|---|---|
| [Complete endpoint Hankel reduction](../gaussian_majorisation_hankel_transport/PROOF.md) | All endpoint Hankel matrices positive semidefinite iff all beta tests nonnegative iff `Delta_s=0`. The present proof adds monotone finite lower bounds and an explicit global error. | Nonnegative entries, individual replica gaps, and finitely many positive matrices do not establish the full hierarchy. |
| [Sparse finite Hankel hierarchy](../gaussian_sparse_hankel_hierarchy/PROOF.md) | The specified finite blocks are positive when their order-dependent high-variance condition holds. | Its variance threshold grows with the block order. It cannot prove the infinite hierarchy at one fixed variance by exchanging quantifiers. |
| [High-noise hinge window](../gaussian_majorisation_high_noise_window/PROOF.md), [spherical tail](../gaussian_majorisation_spherical_tail/PROOF.md), and [eventual completion](../gaussian_majorisation_eventual_endpoint/PROOF.md) | A uniform positive spherical gap on the stated range, together with the two controlled threshold regimes, proves `Delta_s=0` for all sufficiently large `s`. | The spherical sign hypothesis is not known universally. A window or finite asymptotic calculation alone leaves part of (1) uncontrolled. The endpoint proof and its premises have an [independent acceptance](../gaussian_majorisation_eventual_endpoint_review2/README.md). |
| [Asymmetric nine-point high-variance certificate](../gaussian_asymmetric_eventual_majorisation/PROOF.md) | `Delta_s=0` for `s>=13200` at weights `(8,12,7,15,44,21,11,23,43)/184`; throughout its `L1` weight ball of radius `1/25000`, for `s>=16896`. | Preserved valid prior work. The new density-orbit theorem removes its variance restriction and contains both weight classes; further optimization of these cutoffs is unnecessary. |
| [Covariance-free entropy rigidity](../gaussian_contraction_covariance_free/PROOF.md) and its [bridge audit](../gaussian_majorisation_bridge_barrier/PROOF.md) | Closeness modulo isometries gives unsigned hinge control through total variation. | A small upper bound for `Delta_s` does not establish `Delta_s=0`. It cannot decide the sign at the hardest thresholds. |
| [Tail-deficit obstruction](../gaussian_tail_deficit_obstruction/PROOF.md) | It rules out the proposed uniform deficit-only bound for the **normalized** tail error. Its signed next coefficient can refine eventual completion under its separate hypotheses. | It does not obstruct the absolute all-threshold continuity bound (11), and its extra signed hypothesis is not added to the global criterion. |

At the pass-start checkpoint researcher 7 also had private finite
degree-32 positive matrix computations at five variances. Those are
finite evidence only and are not a dependency of any theorem here.
The prepublication refresh then found researcher 8's complete density-orbit
source, read its universal analytic transfer and replayed both exact
finite checkers. It is now included above; this replay is not independent
review. The earlier exploratory spherewise calculations are not premises.

## What the transport obstructions actually say

The [atomic bridge obstruction](../gaussian_atomic_bridge_obstruction/PROOF.md)
has an [independent acceptance](../gaussian_atomic_bridge_obstruction_review1/REVIEW.md).
It excludes a position martingale, even after separate isometries and
the stipulated common smoothing, for the asymmetric nine-point family.
The same source excludes exact deterministic common-output mixtures of
the proposed motion components on its stated open weight neighbourhood.
The earlier simplicial-cone source proves the absence of an `R^5`
contracting motion for the nine labelled square-cone centres.

The new all-variance density-orbit theorem covers that entire obstruction
ball. Thus the endpoint density-value coupling in (4) **exists at every
variance** there even though those more restrictive constructions do not. This is the
concrete positive obligation for transport work: allow couplings of
density values that are not induced by a labelled centre motion or the
excluded position martingale. Existence here follows from the credited
orbit proof. The unrestricted input and contraction remain the target.

The [local-lift obstruction](../gaussian_majorisation_local_lift_obstruction/PROOF.md)
shows that positivity of every instantaneous lifted Hankel matrix is
too strong even for an endpoint pair with full majorisation. In the
six-dimensional path representation, the endpoint moments are obtained
only **after integration over time**. A positive proof must preserve
that integration or construct the endpoint coupling directly. The
global beta tests do not turn the false instantaneous assertion into
a valid lemma.

## The shared obligation and Kneser--Poulsen boundary

The single remaining analytic task is `Delta_s=0` for arbitrary bounded
three-dimensional input, arbitrary contraction, and each `s>0`.
Theorem 1 gives a primal construction target; Theorem 2 gives an exact
dual hierarchy with certified finite error. The geometric lane supplies
zero-failure certificates for its classes, and the adversarial lane can
settle a failure with a single negative finite test. The integrated
hinge sign is still missing for the unrestricted problem.

For a geometric consequence from internal energies, preserve all input
laws and all variances as required by the cited Aishwarya--Li theorem.
The existing motion sources separately establish their arbitrary-radius
ball comparisons. The density-orbit source explicitly claims no new
Kneser--Poulsen case from its weight family. Neither does this consolidation.
Finite moment checks and unsigned entropy bounds supply no such claim.
