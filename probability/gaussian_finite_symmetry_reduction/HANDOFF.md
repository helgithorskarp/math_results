# Counterexample and positive-bound interface

The unrestricted bounded-law R3 Gaussian question is equivalent to the
same assertion for full signed-permutation-invariant laws and globally
equivariant short maps, at variance one. More strongly, the supremal
absolute hinge defect is exactly unchanged. Both covariances may be
taken scalar and positive. They are not equal to each other in the
construction, and this is not simultaneous covariance normalization.

There is also a complete compact test class: common rescaling gives source
Cov=I and support in B(0,2), target Cov=alpha I with 0<alpha<1 and support
in B(0,2sqrt(alpha)). All positive variances must be allowed. The full
supremal defect is again retained. Thus a possible failure does not require
an ill-conditioned or degenerate source covariance. This assertion does
not retain rational coordinates after the scalar normalization.

For an input radius bound R>=1, certified positive adverse margin delta,
and variance s, select k>=1, L>=16R satisfying

    47*2^-k <= delta/2,       (L-4R)^2 >= 32*s*k.

Make the 48 source copies w(L(1,2,3)+p_i) and target copies
w((L/2)(1,2,3)+q_i), dividing each weight by 48. A violation at h becomes
a violation at h/48 with margin at least delta/2. The map on those
labels contracts every pair. The proof supplies an equivariant global
extension without changing their endpoint values.

An adverse margin is a required input, not an output of the exact
geometry checker. The supplied fixture is only an asymmetric rank-six
algebra control. Its Gaussian sign is not evaluated here.

This reduction applies to the full defect, not only a motion class or
a two-body family. Improving a universal defect bound on the restricted
class improves the unrestricted bound by the identical amount. A proof
of zero defect for that class would solve the headline. Existing finite
Coxeter alignment positivity does not cover arbitrary changes of orbit
representatives: both alternating components here vanish, while the
invariant components can differ.

Scope safeguards:

* Finite symmetry is not radial/spherical invariance or norm preservation.
* The variance stays fixed; support radius and atom count are not bounded
  uniformly in that version. The compact isotropic version instead allows
  variance approaching zero. The construction increases atom count by 48.
* The absolute defect is retained; distance-loss-normalized margins and
  efficient certificate complexity are not retained.
* Separation controls the error. It does not sign the original component
  comparison or remove its free geometry and priors.
* No negative Gaussian hinge, new positive class or KP sign was obtained.

The [all-radius loss-localization result](../gaussian_all_radius_loss_localization/HANDOFF.md)
requires an actual covariance floor. These constructed laws have the
stronger guard radius^2/covariance_scalar<4. Its unsigned error estimate
can therefore consume those guards; no positive sample margin or signed
endpoint follows from this reduction. No competing cubature or oracle
implementation is supplied.

The earlier [two-body contact transfer](../gaussian_two_body_contact_transfer/HANDOFF.md)
remains an independent conditional route to an adverse input. This packet
does not extend that interface, enumerate its contacts or claim a sign for
the proper screw. Completed low-noise, radial and motion-obstruction
checkpoints remain unchanged.
