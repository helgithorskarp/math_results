# A genuine obstruction to pointwise Gaussian lift positivity

**Status:** complete written author proof with a finite exact certificate;
independent review pending. The dimension-three Gaussian majorisation
conjecture remains open.

An explicit bounded law in `R^3` and a globally `1/100`-Lipschitz map have
the following property. At an interior time of their usual contracting lift
in `R^6`, the positive lifted measure fails the first transformed Hankel
test. Equivalently, a convex quartic energy, transported back through the
Gaussian marginalisation formula, decreases at that time.

The endpoint distributions **do satisfy majorisation**. The map is a product
of scalar contractions, so this follows from the source paper's established
one-dimensional theorem. This result disproves a proposed *instantaneous*
proof lemma, not the conjecture or the integrated Hankel criterion.

The construction uses `117649` equally weighted atoms described by two
three-dimensional seven-point product grids; no large fixture is stored.
A general encoding lemma explains why arbitrary finite six-dimensional
clouds can appear as limits of such intermediate lifts, with the appropriate
projected pair weight. Thus pointwise geometry alone does not retain the
restriction needed for the endpoint problem.

- [PROOF.md](PROOF.md): definitions, encoding lemma, explicit contraction,
  factorisation, perturbation bounds, and the precise failed bridge.
- [verify.py](verify.py) and [EXPECTED.json](EXPECTED.json): rational certificate.
- [VALIDATION.md](VALIDATION.md): independent enumeration checks and trust boundary.
- [SOURCES.md](SOURCES.md): original source and durable team dependencies.

From the repository root:

```bash
python3 probability/gaussian_majorisation_local_lift_obstruction/verify.py --check
python3 -O probability/gaussian_majorisation_local_lift_obstruction/verify.py --check
cd probability/gaussian_majorisation_local_lift_obstruction
sha256sum -c SHA256SUMS
```

Python 3.11 or newer, standard library only. The checker explicitly imports
the already-published rational arithmetic in
[the sibling bounds.py](../gaussian_majorisation_hankel_transport/bounds.py),
whose hash is included in the manifest. There is no floating-point arithmetic
in the certificate, and no spatial quadrature.

Certified bounds for the normalised instantaneous moments are

```
m0*m2/m1^2 < 1.053 < 1.06 < 3/(2*sqrt(2)),
2*sqrt(2)*m0*m2 - 3*m1^2 < -1.8e-20,
beta^2*sqrt(2)*m0 - 2*beta*sqrt(3)*m1 + 2*m2 < -1.98e-16,
beta = 17/1000000.
```

All universal statements rely on the written proof. The code certifies the
finite reference sums, the exact contraction, and the explicit perturbation
margin. No new Kneser--Poulsen case is claimed.
