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
threshold tending to zero. The depth bound depends on a_0. There is no
all-threshold positive-depth theorem, effective depth bound, counterexample,
or new Kneser--Poulsen volume conclusion here.

The same proof records why the full geometric configuration has only its
two endpoint distance states even in R5, so it admits no R5 contracting
motion. This uses tight Gram constraints, including for the asymmetric
control. It does not determine the missing Gaussian sign.

From this directory run:

```
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

The checker uses Python integers and Fraction only. Tested with CPython
3.11.2 and 3.12.14. It checks 240 full depth polynomials, 96 individual
divergence coefficients, both quadratic weight identities, and five weight
controls for each of two geometries. It evaluates no Gaussian integral.
The universal analytic and compactness arguments remain a written-proof
trust boundary. See [EXPECTED.json](EXPECTED.json), [verify.py](verify.py),
and [SOURCES.md](SOURCES.md).

Continue at the coupled limit of depth and threshold tending to zero;
ordinary compactness or pointwise first-order positivity cannot close it.
