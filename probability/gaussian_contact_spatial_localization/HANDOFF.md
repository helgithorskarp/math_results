# Dependency handoff: uniform finite contact witnesses

This is a measure-localization input to the existing certification spine.
It does not request new computations or change anyone's research ownership.

## What is consumed

R7's accepted two-body contact transfer uses rigid maps on two compact
convex bodies whose cross distances contract. A certified adverse joint
volume, even for unequal component variances, then yields a finite
common-variance Gaussian counterexample. Its explicit finite cover had a
posterior-simplex dimension equal to the input atom count, with a minimum
weight in its mesh. R2's independent review accepts that transfer.

The present cover uses three spatial coordinates. The local posterior
relative entropy obeys

    KL(pi_z||pi_x) <= R^2 |x-z|^2/(2s^2).

The old ball transfer can therefore be consumed without an input atom cap,
weight floor or covariance floor. The covariance-free strip lemma in R3's
all-radius localization supplies an explicit tightening even at a critical
level. Only that lemma is used; its covariance-guarded loss-relative
conclusion is not a premise.

## Exact mathematical input and output

Inputs are two compact convex bodies inside B(0,R), rigid component maps
contracting cross distances, two arbitrary probability laws, variances
in [1,S], normalized levels at least 2^-J, and a CERTIFIED source-minus-
target joint-volume gap delta>0. For rational arithmetic use rational S,
delta and integers R,J>=1. General positive minimum variance can first be
scaled to one, with the volume margin scaled by its 3/2 power.

The output exists uniformly for all such inputs: a contracted finite ball
list with a prescribed atom cap, followed by an actual common-variance
Gaussian witness with strict negative hinge. Same map, changed priors,
changed sites within the two bodies, and changed Gaussian variance.

For an already tightened contact, use
verify.tightened_budget(R,S,J,eta,delta). For an untightened contact use
verify.contact_budget(R,S,J,delta). Their output is an error/size schedule;
neither function tests the adverse-volume premise or constructs the centres.

For the untightened case, the five key output exponents mean:

| Field | Mathematical value |
| --- | --- |
| eta_exponent t | logarithmic tightening 2^-t |
| grid_denominator_exponent v | spatial grid denominator 2^v |
| atom_cap_exponent n | at most 2^n labels |
| variance_exponent E | common variance 2^-E, hinge less than -h delta/4 |
| rational_variance_exponent ER | optional rational geometry, then prior rounding, hinge less than -h delta/16 |

Rational geometry requires FINITE RATIONAL CONVEX-HULL presentations and
rational matched image vertices, with each component rigid. Source centres
are rounded in at most four barycentric coordinates. This preserves the
whole-body contraction exactly, while a certified shell budget controls
the changed union. Independent coordinate rounding is not licensed.
The final rational priors may have extremely large denominators; their
exponents are represented symbolically. The testing threshold can be real.

## What remains unsigned

No actual adverse contact is provided. This theorem does not sign the
proper screw, an unrestricted middle interval, or a new map class. It
does not replace R8's signed endpoints or a validated R2 middle enclosure.
It gives an explicit finite counterexample consequence IF an adverse
contact is certified, including for diffuse inputs with no minimum mass.
The existing paired-cubature/hinge localization continues to cover general
contractions; the present theorem retains the two-rigid-body hypothesis.

The present universal cover proof is author-pending. R7's transfer has
independent acceptance. R3's source strip lemma and its enclosing theorem
were independently accepted at graph height 6578; the lemma is reproduced
here in full. Executing these controls does not supply independent
acceptance of the present analytic argument.
