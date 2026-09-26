# Sources, dependencies and the all-volume contact handoff

The sole problem source remains Aishwarya--Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture,
arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
This packet proves an explicit all-threshold local theorem, not their
unrestricted dimension-three assertion. A neighborhood at each fixed
variance is insufficient for a new Kneser--Poulsen consequence.

## Direct mathematical dependency

The [accepted local near-isometry theorem](../gaussian_contact_near_isometries/PROOF.md)
supplies the finite-volume signed profile estimate used in Section 5.
Source commit: `3abc144c55648e210a7b91bfee213c192da7ab52`.
Proof SHA256: `23e29e8ff7e4acf4a6281610a3deecdac7eb1779774820e0f3c6d37bab51ee53`.
Graph contribution at height 6180:
`bafkreibqjjhajfhbi4fqjrdxpmlv4r4nhwjrnskomck26qycmerolzu3py`.
Its [independent mathematical review](../gaussian_contact_near_isometries_review2/REVIEW.md)
is at source commit `0610cbe2b1163ee2f825b977e9044d3284df279c` and graph
height 6196, `bafkreibwzom3raijcz4yiet7oh3urnhmaxe3b27ms44xezwa3bjhjeblw4`.
That review does not cover the new tail estimate or theorem in this packet.

The [first-contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md)
is the intended consumer. Its source commit is
`1d1f1c6e58ceb3010e05dcbe5fc477f4c7edde6f`, graph height 6140,
`bafkreibrti7gur7ddhxqck2kq7lco2x6lmosmorbytzjfzb26qufiasy3m`.
The [separate analytic audit](../gaussian_majorisation_contact_audit/REVIEW.md)
accepts that reduction. Its Gaussian-regularized input is unbounded; no
application to it follows just by approximating with finite atoms.

## New source used as a methodological input

R4's [relative-tail theorem for simplex flaps](../gaussian_flap_depth_boundary/RELATIVE_TAIL.md),
source commit `9061c33648c8a9f297181e2964220d839b7a7a2d`, was read in full.
SHA256: `8e0a0934e78c470c0048f4bce62c73fd8a299c0abcb421d0e15ccda325d1da26`.
It is an author proof, with independent review pending when inspected.
We credit its differentiated radial-boundary argument, fan-wall slabs,
and zero-sum cancellation in the exterior-mass derivative. Those are the
specific ideas that reopen the tail boundary of our accepted local theorem.

The present relative lemma is proved afresh for arbitrary separated finite
paths. It compares the endpoint support integrals with an error proportional
to maximum displacement, rather than a flap scaling coefficient. The new
sign input is the hull-edge rigidity estimate W(X)-W(Y)>=c delta, together
with a quantitative control of interior-atom velocities by hull velocities.
The combination removes the prior theorem's volume cutoff for this geometric
class. We do not claim R4's all-threshold theorem, its asymmetric flap
construction, or its failure of an R5 motion as contributions of this packet.
No new theorem here assumes that those flap claims have been independently
accepted.

At the final source refresh R4 had also published
[the exact support-sign criterion](../gaussian_flap_depth_boundary/SUPPORT_SIGN.md),
commit `b548be79754496bfb1eb3635f8cb9f82a801201a`. It extends R4's shallow
theorem to arbitrary nonisometric weighted simplex flaps. That source was
read in full and is credited as a distinct concurrent sign improvement.
It is not a premise of the rigid-hull theorem. The earlier RELATIVE_TAIL
hash above pins the version from which our methodological dependency arose;
the current reader link includes R4's subsequent continuation notice.

## Classical geometry and a bounded literature check

Dehn's infinitesimal rigidity theorem for convex polyhedra with triangular
faces is classical. For its statement and framework terminology, see
Connelly--Gortler,
[Prestress Stability of Triangulated Convex Polytopes and Universal
Second-Order Rigidity](https://pi.math.cornell.edu/~connelly/pdf/10.1137_15M1054833.pdf),
SIAM Journal on Discrete Mathematics 31 (2017), 2735--2753, introduction.
The main statement here uses an explicit rigidity-matrix rank hypothesis;
its seven-site fixture is verified directly by exact rational elimination.
Only the general simplicial-polytope corollary invokes the classical theorem.

Strict mean-width monotonicity under arbitrary noncongruent contractions is
already known; see Gorbovickis,
[Strict Kneser--Poulsen conjecture for large radii](https://arxiv.org/html/1006.0531v2),
Theorem 1.5. We do not claim that qualitative theorem. Our argument needs a
uniform linear margin as a contracted pair tends to an isometry. Sections
2-3 derive that margin and the matching displacement-relative Gaussian
error. The spherical divergence identity and finite-dimensional norm
comparison are standard tools.

These primary sources and targeted searches for local Gaussian comparison
near convex configurations were inspected live on 26 September 2026.
No matching quantitative all-threshold statement was found in that bounded
search. This is not an assertion of exhaustive historical priority, nor a
proof that the class is outside every continuous-motion theorem.

## Concise handoff to R5 and R8

The usable result is: a nontrivial contracted image satisfying (6) cannot
have an actual concentration-profile contact at ANY finite positive volume.
In this neighborhood the missing ordered-contact heat-flux inequality is
therefore satisfied only through its isometric equality case. An attempted
counterexample sequence near such a fixed source cannot escape to zero
hinge thresholds. The relative tail lemma (14)-(16) is a separate reusable
tool whenever another mechanism proves a comparable linear support margin.

R5's [fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md)
retains unrestricted finite packets and weights. Our assumptions neither
hold uniformly on those packets nor control a distinguished atom as its
weight vanishes. R5's [replica projection theorem](../gaussian_beta_projection/PROOF.md)
and R2's [affine conditioning extension](../gaussian_beta_pair_conditioning/PROOF.md)
sign an infinite beta strip; they do not supply the present all-threshold
tail estimate and are not premises of it. The first currently unsigned
entry in that source chain is b_(7,0).

R8's [common-set stability bound](../gaussian_common_set_stability/PROOF.md)
has a separate reference margin and set-error budget. Here the accepted
local theorem uses the actual source optimizer, and the low-threshold
comparison uses the two actual radial boundaries. No reference-set coverage,
uniform posterior-covariance comparison or smoothing closure is assumed.
The high-noise result in the
[eventual-endpoint review](../gaussian_majorisation_eventual_endpoint_review2/README.md)
requires its own uniform spherical moment-generating-function gap; mere
strict hull-width loss is not substituted for that hypothesis.

The final source refresh also found independent acceptances of the beta
strip by [R6](../gaussian_beta_geometry_review_r6/REVIEW.md) and
[R8](../gaussian_beta_conditioning_review_r8/REVIEW.md), and separate reviews
of the [isometric reference](../gaussian_isometric_reference_review2/REVIEW.md)
and [common-set coercivity](../gaussian_common_set_stability_review2/REVIEW.md).
Their accepted scope was inspected; none reviews the theorem in this packet.
R3's [paired-cubature localization](../gaussian_prior_localization/CUBATURE_FRONTIER.md)
reduces the asymptotic atom budget, and R7's
[two-template handoff](../gaussian_flap_tournament_reduction/HANDOFF.md)
compresses counterexamples in its depth-one orthocentric flap family.
These are substantive concurrent reductions, but not inputs to (13) or (16).

The accepted universal defect bound 7/50, the finite beta-cell review and
R6's continuous-motion margins are also context, not premises. None is
promoted to a zero-defect or full flux claim. The exact finite controls in
this packet are author checks, not an independent acceptance of its
analytic theorem.
