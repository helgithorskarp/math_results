# Low-noise degree barrier for Gaussian counterexamples

A finite contraction with distinct target sites and a strictly shortened
nearest target pair passes every curvature-square polynomial test of any
fixed degree once the Gaussian variance is sufficiently small. The
[proof](PROOF.md) gives an explicit cutoff and a factor-one-half lower bound
for the full diagonally normalized Hankel matrix.

This is uniform over arbitrary geometries and priors satisfying the stated
separation, nearest-pair loss and mass bounds. It is a counterexample-search
exclusion, **not full Gaussian majorisation or a new KP inequality**. Any
negative curvature-square witness in the certified domain must exceed the
certified degree. The nearest-pair hypothesis is essential to this proof.

For example, with every weight >=1/8, target separation squared >=1/4, and
loss >=1 at a nearest target pair, all stated globally convex polynomial
energies through degree twelve compare for variance <=1/422400. The
seven-site rational control has paired rank six and an oblique tetrahedral
core; the closed orthocentric flap assignment is not revisited.

Complete author proof; independent review and historical priority are
pending. The full dimension-three question remains open.

From this directory, standard-library Python 3.11 or later:

```sh
python3 -B verify.py --check
python3 -B -O verify.py --check
sha256sum -c SHA256SUMS
```

The expected marker is `LOW_NOISE_DEGREE_BARRIER_EXACT_PASS`. The checker
validates exact input/cutoff arithmetic and finite algebraic controls. The
universal conclusion rests on the written proof. No numerical integration
or unpublished search data is required.
