# Gaussian majorisation for three disjoint cap reflections

Reflect up to three pairwise disjoint caps of a convex body in their boundary
planes and keep the remainder fixed. [PROOF.md](PROOF.md) constructs a
five-dimensional contracting motion. It implies full dimension-three Gaussian
majorisation for every measure and variance, and both Kneser--Poulsen union
and intersection inequalities for arbitrary individual ball radii.

**Status:** author proof; independent correctness and priority review pending.
The unrestricted dimension-three problem remains open.

The [seven-site control](EXPECTED.json) has paired affine rank six, 15 tight
and six strict pairs. A reduction to eight reflection states proves that
no finite chain of coordinatewise strong contractions in dimension three,
even in changing orthonormal frames, produces its endpoint map. An
intentionally wrong lift increases three pair distances near its endpoint.
These obstructions leave the explicit five-dimensional motion available.

Run from the repository root with Python 3.11 or later, standard library only:

```sh
python3 probability/gaussian_disjoint_cap_reflections/verify.py
python3 -O probability/gaussian_disjoint_cap_reflections/verify.py
```

To regenerate the compact expected data, use `verify.py --emit`. The verifier
checks exact rational pair polynomials for the whole time interval, cap
separation on the source convex hull, endpoint and paired ranks, the complete
eight-state transition graph, and the two negative controls. It does not
compute Gaussian integrals or prove the
all-measures theorem by finite testing. That theorem depends on the analytic
proof and the primary sources identified in [SOURCES.md](SOURCES.md).

Reproduction was checked with CPython 3.11.2 and 3.12.14. [SHA256SUMS](SHA256SUMS)
records the compact packet's file hashes. No external data or large artifact
is required.
