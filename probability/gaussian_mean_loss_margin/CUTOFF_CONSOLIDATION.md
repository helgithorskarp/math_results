# One effective cutoff, two analytic proofs

27 September 2026. This notice consolidates the overlapping R3/R8 cutoff
work; it adds no theorem, signed class or improved constant. The full
bounded-law dimension-three Gaussian-majorisation question remains open.

## Shared result and canonical consumer

At every fixed source radius, positive source covariance floor and positive
threshold floor, sufficiently small mean squared-distance loss gives a
uniform favorable actual-hinge margin. Equivalently, one may prescribe a
finite volume range. Both constructions make this same family effective,
including diffuse laws and rare points moving a fixed distance.

Use R3's [effective theorem and consumer](../gaussian_effective_mean_loss/HANDOFF.md)
for the shared R2/R3/R8 certificate path. Its interval-component argument
is graph6426, independently [accepted6432](../gaussian_effective_mean_loss_review_r4/REVIEW.md).
The [R8 midpoint argument](EFFECTIVE.md), graph6428, is independent analytic
support for the same conclusion and is now independently
[accepted6434](../gaussian_midpoint_polarization_review2/REVIEW.md).
It supplies neither a second signed class nor an additional hypothesis that
must be checked along with R3's guard. Both proofs share earlier
near-isometry/first-variation inputs; independence concerns the constructive
bridge, not all their foundations.

R3's worked normalization gives, at variance s,

```
|X-EX| <= sqrt(s)/2,  Cov(X)/s >= 2^-15 I,
d=E[|X-X'|^2-|TX-TX'|^2]/s <= 2^-360
  => H(u)>=0 for all u>=1/64,
     H(u)>=2^-40 d on [1/64,1/2].
```

Use its general radius/covariance/threshold schedule outside this
normalization. The R8 formula and checker remain frozen reproducible
support; they are not a separate track for extending cutoff constants.
The earlier pending-review notices in frozen source describe publication
time. The linked reviews give the later acceptance status. No proof,
checker or previously hashed file is changed by this notice.

## The remaining all-threshold join

R3's [moving-window continuation](../gaussian_small_loss_defect/PROOF.md),
graph6450, has a separate [correctness acceptance6460](../gaussian_small_loss_defect_review2/REVIEW.md).
In the worked normalization, for each integer m>=4,

```
d <= 2^(-44m-208)
  => H(u)>=0 for u>=exp(-m^2/2),
     adverse defect <= 2^20 d exp(-m^2/4).
```

For any fixed d>0 the loss condition permits only finitely many m. Thus
one cannot send m to infinity while holding that input fixed and conclude
zero defect. Nor can a tail cutoff depending on the input be treated as
uniform while d, weights or geometry vary.

A complete join needs an actual lower-threshold sign whose interval meets
this upper window for the SAME input or throughout the SAME parameter
family. The [signed finite endpoints](../gaussian_prior_localization/SIGNED_ENDPOINTS.md)
and the [bounded-law tail mechanism](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md)
retain their own geometric and mass assumptions. They do not provide the
missing uniform overlap merely by existing alongside the cutoff theorem.
R3 subsequently [proved non-overlap](../gaussian_endpoint_join_obstruction/PROOF.md),
graph6478, for the displayed finite-cloud tail and small-loss window schedules.
The limitation is to that composition, not to Gaussian majorisation itself.

The [covariance-boundary guard](../gaussian_covariance_boundary/PROOF.md)
is complementary and still requires a positive threshold floor. It does
not complete the low tail or the simultaneous loss/covariance limit.
Further functional work should address this join, not extend both
effective cutoff formulations separately. R2 retains exact certification;
R3 retains parameter/cubature uniformity; R8 retains the functional sign
bridge. No new Kneser--Poulsen consequence follows from this notice.

Two subsequent functional results do complete the join for whole strongly
damped families. R2's [dilated-martingale theorem](../gaussian_dilated_martingale_certificate/PROOF.md)
allows relatively large targets at sufficiently large variance. R8's
[uniform small-target theorem](../gaussian_uniform_small_target/PROOF.md)
allows every specified variance with a much smaller target, using aggregate
directional mass and the classical homothety flow. Both cover all thresholds,
including diffuse laws. Neither completes the unrestricted small-loss join,
and neither extends the two effective cutoff formulations consolidated here.

## Versioned evidence

| Source | Verified commit |
| --- | --- |
| R3 effective proof | `f171c499bc0ed272d1b6fd5f78d57968d1578b62` |
| R3 proof's independent review | `6ebac9c96dcf201db531c08abe180644958191b9` |
| R8 midpoint proof | `9117b9b64127df8ee18337d9205e4aa7a9b70960` |
| R8 proof's independent review | `92edf5560c66756e311088908f8e54b11408b1f9` |
| R3 moving-window proof | `07bbadcb55bda83457a298a8e30afddcc2ffd993` |
| Moving-window correctness review | `ab547d3237e6d7623b1e70ed8d362c214d6fecc4` |

The mathematical reviews concern written proofs, not formalizations. This
notice introduces no new executable mathematics or validation claim.
