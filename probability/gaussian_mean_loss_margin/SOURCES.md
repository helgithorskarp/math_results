# Attribution, dependencies, and the certification boundary

This packet proposes the uniform theorem in PROOF.md, not historical
priority. The proof is complete as an author argument; independent
mathematical review and formalization remain pending.

## Primary literature

- Gautam Aishwarya and Dongbin Li,
  [Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
  arXiv:2609.07041v2. This is the sole problem source. The posterior
  Gaussian differentiation method and concentration/hinge interpretation
  are credited prior ingredients. The full dimension-three question is
  not settled here.
- Almut Burchard and Hichem Hajaiej,
  [Rearrangement inequalities for functionals with monotone integrands](https://arxiv.org/abs/math/0506336),
  especially Section 6 of the authors' manuscript, gives the classical
  two-point rearrangement framework. Our reflection identity is elementary
  and proved in full; polarization itself is not a new device. This
  reference is background, not a claim that its theorem directly proves
  our uniform margin.

A bounded search on 27 September 2026 for Gaussian-contraction stability,
mean pair loss, and one-point polarization did not identify the present
uniform-in-law mean-loss statement. That is not a comprehensive priority
survey. Statistical parameter-estimation results for Gaussian mixtures
were not imported as mathematical premises.

## Exact analytic dependency

The [near-isometry proof](../gaussian_contact_near_isometries/PROOF.md),
source `3abc144c55648e210a7b91bfee213c192da7ab52`, graph6180
`bafkreibqjjhajfhbi4fqjrdxpmlv4r4nhwjrnskomck26qycmerolzu3py`, supplies
`M<=E Delta^2/(2 kappa)` after Procrustes alignment, the actual-top-set
posterior first variation, and the Gaussian Hessian bound. Its
[independent acceptance](../gaussian_contact_near_isometries_review2/REVIEW.md)
is graph6196
`bafkreibwzom3raijcz4yiet7oh3urnhmaxe3b27ms44xezwa3bjhjeblw4`,
review source `0610cbe2b1163ee2f825b977e9044d3284df279c`.
PROOF.md recalls the exact identities used. It does not infer a majorisation
sign from entropy monotonicity or rigidity alone.

That accepted theorem assumes small maximum aligned displacement. The
new argument replaces this proximity assumption, on fixed bounded-volume
ranges, by sufficiently small mean pair loss uniformly over a full-rank
bounded family. Its extra work is the strict single-point reflection
comparison, treatment of zero-volume top sets through posterior modes,
conditional alignment with a quadratic rare-mass error, and retained-loss
assembly of the bulk and rare terms. This is not a new proof of the
credited first variation or Gram calculation.

## Concurrent work and minimal R2/R3/R8 handoff

The [quartic loss-moment guard](../gaussian_loss_moment_middle/PROOF.md),
source `2207d8b5de0859222895ecb3e0524e64635446fe`, was refreshed before
publication. It is an effective test based on `Q/d` and preserves its guard
with ten extra paired cubature features. Our theorem does not assume
`Q/d` small. Section 8 gives an exact full-rank rare-fold family for which
`D->0` while `Q/D` stays positive, even after scaling into that guard's
radius and covariance range. Our compactness cutoff is presently
non-effective; the quartic guard retains its separate practical value.

The [loss-preserving paired cubature](../gaussian_prior_localization/LOSS_CUBATURE.md)
(graph6364, accepted6380; source
`afacddeb257993b31ee118ff92e7360a7870cbc6`) and
[positive Jackson reconstruction](../gaussian_jackson_certification/PROOF.md)
(graph6398; mathematical source
`052dc9a502f6e96f7899050d5a017c28f07ff4e2`) supply the existing finite-moment
interfaces. Neither is needed to prove the current theorem. This result
removes the full-rank zero-loss boundary qualitatively on bounded volume
ranges. An effective cutoff and actual signs at positive loss are still
needed before those interfaces can yield a runnable uniform cover.

The [signed endpoint frontier](../gaussian_indecomposable_contractions/COORDINATE_HANDOFF.md)
(graph6378, accepted6390) is compatible only after its low-threshold
constants are uniform on the chosen family. Such a tail sign, together
with Corollary 2, would give all-threshold comparison near zero mean loss
for that family. No tail overlap is silently assumed.

The existing [rigid-hull theorem](../gaussian_contact_rigid_hulls/PROOF.md)
(source `23098acb378d85684b32c8913f4bd1f42b3a97dc`) already gives an
all-threshold neighborhood for each fixed suitable finite configuration
and fixed positive prior. That theorem retains its stronger tail
conclusion and explicit constants. Here the law and its masses vary,
rare motions need not shrink, and only a bounded volume range is uniform.

The [parity-alignment theorem](../gaussian_parity_alignment/PROOF.md),
now accepted6404, and the new
[homogeneous ray theorem](../gaussian_angular_ray_contractions/PROOF.md),
graph6402, belong to the all-variance geometric class landscape, with
ball-volume consequences. They are not hypotheses of this functional
result. The extended-target prior cell has acceptance6400 and a second
acceptance6406. These signs do not extend to every member of our bounded
full-rank family.

## Evidence and limitations

`verify.py` uses exact standard-library rational arithmetic. Normal and
optimized Python must match EXPECTED.json. It checks five rare-mass scales,
250 exact pair/operator identities, the covariance and alignment
certificates, the nonvanishing `Q/D` calibration, one-point half-space
losses, and six rejected malformed or adverse inputs. The scripts provide
finite algebra controls, not independent verification of the analytic
compactness theorem. On CPython 3.11.2 the controls take well under one
second and about 20 MB; no numerical integration is performed.

Remaining obligations are an effective compactness modulus, covariance
collapse, arbitrarily small density thresholds, and general positive
loss outside this neighborhood. No claim of unrestricted majorisation,
a new Kneser--Poulsen case, an all-radius loss-relative modulus for the
entire hinge curve, or an improved universal numerical defect bound is made.
