# Attribution, dependencies, and the certification boundary

The current constructive continuation is [EFFECTIVE.md](EFFECTIVE.md).
The original compactness argument is preserved in PROOF.md. It received
independent acceptance at graph6422
`bafkreihagjha6hrnzivyd3iutnmtilrvx5dclurfrjcxf4q4ep5k56vpua`,
[review source](../gaussian_mean_loss_margin_review2/REVIEW.md)
`0babf1cceeae17179cc6975dc1d588ebb86b7e95`.
That review does not assess the new constructive argument or its constants.
The constructive continuation is a complete author proof awaiting its own
independent review. Neither theorem is proof-assistant formalized, and
historical priority is not claimed.

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
publication. It has [independent acceptance](../gaussian_loss_moment_middle_review_frontier/REVIEW.md)
at graph6420, review source `dc3c58a818f288df5cb024a1b0b8518073018f60`.
It is an effective test based on `Q/d` and preserves its guard
with ten extra paired cubature features. Our theorem does not assume
`Q/d` small. Section 8 gives an exact full-rank rare-fold family for which
`D->0` while `Q/D` stays positive, even after scaling into that guard's
radius and covariance range. EFFECTIVE.md now makes the mean-loss cutoff
explicit; the quartic guard retains its separate practical value.

The [loss-preserving paired cubature](../gaussian_prior_localization/LOSS_CUBATURE.md)
(graph6364, accepted6380; source
`afacddeb257993b31ee118ff92e7360a7870cbc6`) and
[positive Jackson reconstruction](../gaussian_jackson_certification/PROOF.md)
(graph6398; mathematical source
`052dc9a502f6e96f7899050d5a017c28f07ff4e2`) supply the existing finite-moment
interfaces. Neither is needed to prove the current theorem. This result
removes the full-rank zero-loss boundary with an explicit cutoff on bounded
volume ranges. Actual signs at positive loss above the cutoff are still
needed before those interfaces can yield a uniform cover.

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
[homogeneous ray and convex-normal-bundle theorems](../gaussian_angular_ray_contractions/NORMAL_BUNDLES.md),
graph6402/6418, belong to the all-variance geometric class landscape, with
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

Remaining obligations are covariance collapse, arbitrarily small density
thresholds, and general positive
loss outside this neighborhood. No claim of unrestricted majorisation,
a new Kneser--Poulsen case, an all-radius loss-relative modulus for the
entire hinge curve, or an improved universal numerical defect bound is made.

## Constructive continuation of graph6414

The prepublication refresh found R3's concurrent
[effective mean-loss theorem](../gaussian_effective_mean_loss/PROOF.md),
graph6426 `bafkreieyattiaogc4s7iosnunxfq3yi6sy2enhq23ftgtoua7fz22zb6ni`,
source `f171c499bc0ed272d1b6fd5f78d57968d1578b62`. It already makes the
same full parameter family effective through a quantitative comparison
on interval components of the actual source superlevel. Its worked
threshold cutoff is stronger. We therefore make no claim to a new signed
region or priority for effectiveness. The present independently developed
argument instead supplies the quantitative midpoint reflection and robust
polarization lemmas, and a compressed integer implementation of its own
sufficient guard. It is not a review of the concurrent theorem. Both
constructive arguments await independent assessment.

[EFFECTIVE.md](EFFECTIVE.md) and [effective.py](effective.py) replace the
non-effective constants of our preceding contribution6414,
`bafkreie5iago7b2rtbm5oyabb3fshfabujmwms37a3vsojzo7efsgfybey`,
source `888c64db59feccd280575061612804854b0f658c`. They retain its full
radius/covariance/volume parameter range. The new argument uses an explicit
midpoint derivative bound for a polarized set, stability of the actual
source top-set polarization under small exceptional mass, and an exact
repair of approximate one-point contractions. It uses the same credited
first variation and Procrustes estimate6180/6196, and recalls the bulk
conditional-alignment calculation from6414. No claim is made that the
classical reflection pairing or elementary interpolation identity is new.

The compact dyadic schedule is an explicit mathematical exclusion test,
not another approximation basis or a family of isolated Gaussian samples.
Its constants can be extremely small. The large-radius control emits an
exponent of order10^26 without constructing the corresponding denominator.
This makes the guard cheap to represent, not a practical solution of the
remaining positive-loss sign problem. The constructive analytic theorem
still awaits its own independent assessment; the preceding qualitative
theorem has acceptance6422.

The new [R2 logarithmic-noise polynomial theorem](../gaussian_logarithmic_noise_certificate/PROOF.md),
graph6412 `bafkreia6dvwc2yn44kb2vxsikmdtuvc4ypnoksq7tqqfzgnhtyfqj5gqye`,
provides a complementary finite-degree cone at high noise. Its exact
marginal moment producer is now public. The current guard instead uses
source radius, covariance and mean loss only; a paired cubature retaining
degree-two marginal moments and original support preserves these
hypotheses. The quartic guard6408 remains a distinct effective test.
No extra mixed fourth moments are required by this mean-loss guard.

For the entire hinge curve, an independently uniform low-threshold sign
must still meet the stated threshold interval. Removing the covariance
floor, signing the rest of the positive-loss compact region, and obtaining
an unrestricted or new Kneser--Poulsen consequence remain separate open
obligations. The earlier statement that the mean-loss cutoff was
non-effective describes PROOF.md's original argument; EFFECTIVE.md closes
that particular obligation.
