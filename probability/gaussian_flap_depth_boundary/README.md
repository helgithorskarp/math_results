# Gaussian majorisation for shallow asymmetric simplex flaps

Author proof; independent review pending. The full R3 conjecture is open.

The strongest conclusion is [RELATIVE_TAIL.md](RELATIVE_TAIL.md),
Theorem 6 and Section 8: an open geometric class of asymmetric tetrahedral
flaps satisfies **every Gaussian hinge inequality**, for arbitrary
positive atom weights and each fixed variance, at sufficiently small
depth. An explicit rational example has six distinct core edge lengths.
The full maps have no R5 contracting motion. The depth bound depends on
the variance; no common depth for all variances, and no new
Kneser--Poulsen consequence, is proved.

For any nondegenerate tetrahedron v_i, choose inward face-normal vectors
d_i of arbitrary positive lengths. The classical flap contraction fixes
the vertices and sends v_j-t d_i to v_j+t d_i for i!=j. All sixteen label
weights may be asymmetric or zero.

[PROOF.md](PROOF.md) establishes two functional statements:

* The derivative at depth zero of every nontrivial Gaussian hinge gap is
  strictly positive unless the weighted map is an isometry. A positive
  explicit numerator gives the complete equality criterion.
* Uniformly over a compact positive variance interval and weights bounded
  away from that isometry boundary, sufficiently shallow flaps satisfy
  every hinge whose threshold is at least any prescribed a_0>0. This
  includes thresholds near or above the density maximum and critical levels.

Thus a shallow negative sequence in these parameter ranges must have its
threshold tending to zero. The depth bound depends on a_0.

[TAIL_BLOWUP.md](TAIL_BLOWUP.md) now controls a joint limit in that tail.
At fixed variance s, take a=(2 pi s)^(-3/2) exp(-s tau^2/(2t^2)). As depth
t tends to zero, the hinge gap divided by a s^2 tau/t converges to an
explicit spherical logarithmic coefficient. That coefficient is strictly
positive exactly for nonisometric weighted maps, with a quantitative lower
bound. Convergence is uniform on compact positive tau intervals. Hence
every such scaling window has strictly positive actual hinge gaps for
sufficiently small depth, including fully asymmetric configurations.

The sign proof isolates each tetrahedron tip and uses the established
simplicial-cone motion. Its leading coefficients add, even though the
original finite-depth hinges do not decompose into packet hinges. No
additional symmetry assumption or numerical tail quadrature is used.

[RELATIVE_TAIL.md](RELATIVE_TAIL.md) strengthens this to an explicit
relative error, valid down to tau=0. It supplies an effective positive
window 0<tau<=log R/(12D), where R=sqrt(2 log(C_3/a)) at variance one
and D bounds the normal lengths. More generally every fixed multiple
b log R with b<1/(6D) is eventually positive. Any shallow failure at
fixed geometry and weights must therefore have
liminf tR/log R>=1/(6D). Combining this with the threshold-floor theorem
proves all hinges above C_3 exp(-c log^2(1/t)/t^2) for sufficiently small
depth, for every 0<c<1/(72D^2). General fixed variance follows by scaling.

The same proof records why the full geometric configuration has only its
two endpoint distance states even in R5, so it admits no R5 contracting
motion. This uses tight Gram constraints, including for the asymmetric
control. A positive large-parameter support coefficient, verified on
an open asymmetric geometric class in RELATIVE_TAIL.md, closes the
remaining tail and yields the all-threshold theorem above.

From this directory run:

```
python3 verify.py --check
python3 -O verify.py --check
python3 verify_tail.py --check
python3 -O verify_tail.py --check
python3 verify_relative.py --check
python3 -O verify_relative.py --check
sha256sum -c SHA256SUMS
```

The checker uses Python integers and Fraction only. Tested with CPython
3.11.2 and 3.12.14. It checks 240 full depth polynomials, 96 individual
divergence coefficients, both quadratic weight identities, and five weight
controls for each of two geometries. It evaluates no Gaussian integral.
The new tail checker adds three universal polynomial identities, 128
normal/edge identities, twelve angular-band controls, an exact positive
coefficient, a spherical-normalization algebra check, and an isometry
control. See [TAIL_EXPECTED.json](TAIL_EXPECTED.json) and
[verify_tail.py](verify_tail.py). The universal analytic, integration,
and compactness arguments remain a written-proof trust boundary.
See also [EXPECTED.json](EXPECTED.json), [verify.py](verify.py), and
[SOURCES.md](SOURCES.md).

The relative-error controls in [RELATIVE_EXPECTED.json](RELATIVE_EXPECTED.json)
and [verify_relative.py](verify_relative.py) verify the coefficient
arithmetic, a deliberately conservative effective-radius example, the
regular support-sign calculation, and an exact fully asymmetric
perturbation with a positive support coefficient.
The large radius is stored symbolically; no tiny Gaussian value is
computed. Each checker takes well under a second on the author's host.

For arbitrary tetrahedral geometry and label support, strict positivity
of the support coefficient remains undecided. Uniformity as occupied
weights vanish or variances and geometry degenerate is not asserted.
The final depth cutoff in the all-threshold theorem is not made
effective; its far-tail part has an explicit test. The unrestricted
problem and the new Kneser--Poulsen consequence remain open.
