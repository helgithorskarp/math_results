# Validation and reproduction

Run from the repository root with Python 3.11 or newer:

```bash
python3 probability/gaussian_majorisation_local_lift_obstruction/verify.py --check
python3 -O probability/gaussian_majorisation_local_lift_obstruction/verify.py --check
```

Both commands were run with CPython 3.11.2. They compare the entire result,
including all enclosures, with `EXPECTED.json`. The checker does not rely on
`assert`, so optimized mode performs the same checks. Each run takes about
one second on the development host; runtime is not part of the certificate.

The expected JSON SHA256 is

```
8d08b10a4f8e00128a306e538e651c86a40d96e6537b0fcd0d1f3ff1139b2cab
```

The exact checks cover:

- all `1176` pairs of the `49` scalar encoded input points, with contraction
  constant `1/100`, and all `48` adjacent interpolation slopes;
- all `2793` ordered one-dimensional replica tuples for powers `2,3,4`;
- an independent count-vector enumeration with `322` multinomial states,
  comparing each exponential-histogram entry, including the pair weights;
- probability normalization and the exact unweighted pair variance `81/2`;
- the three perturbation enclosures in equation (14), and strict negative
  determinant and rational-vector quadratic-form margins in equation (15).

No full six-dimensional atom list is generated. Its `117649` atoms have an
exact product definition; the factorisation in the written proof replaces
enumeration. The perturbation estimate applies to all tuples uniformly.

Exponentials are enclosed at `70` decimal digits by
[bounds.py](../gaussian_majorisation_hankel_transport/bounds.py), a shared,
previously published standard-library module. It uses rational range reduction,
Taylor expansion with an explicit geometric bound for the omitted tail,
outward rounding, squaring, and reciprocation. Square roots are bounded with
integer square roots. There are no machine-float evaluations in the checker.
The shared module's exact file hash is included in `SHA256SUMS`.

The ordered/count-vector check is independent at the enumeration level, but
uses the same rational interval arithmetic. This is not an independent
mathematical review or a proof-assistant formalisation. The trust boundary is
the written Gaussian reduction, product factorisation, and perturbation proof,
plus the Python interpreter and the stated rational arithmetic implementation.
Exploratory float searches and their scratch logs are not evidence and are
not included in this publication.

Passing this checker certifies only the instantaneous obstruction. Endpoint
majorisation for this example follows analytically from the source theorem
and tensorisation; the checker does not numerically integrate endpoint hinge
energies. The general dimension-three conjecture remains unresolved.
