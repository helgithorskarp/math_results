# Gaussian hinge comparison near a collapsed simplex-flap map

Author proof; independent review pending. The full R3 conjecture is open.

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

The same proof records why the full geometric configuration has only its
two endpoint distance states even in R5, so it admits no R5 contracting
motion. This uses tight Gram constraints, including for the asymmetric
control. The new coefficient sign does not yield full Gaussian comparison.

From this directory run:

```
python3 verify.py --check
python3 -O verify.py --check
python3 verify_tail.py --check
python3 -O verify_tail.py --check
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

Uniform approximation as tau tends to zero or infinity, varying weights
approach zero, or variance escapes a compact range remains unproved.
There is no all-threshold positive-depth theorem, effective depth bound,
counterexample, or new Kneser--Poulsen volume conclusion here.
