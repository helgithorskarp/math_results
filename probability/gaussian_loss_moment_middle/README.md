# Uniform middle signs from a quartic loss guard

Author proof; independent review pending. The full dimension-three
Gaussian-majorisation problem remains open.

At variance s, use favorable hinge gap H, normalized mean pair loss d and
second loss moment Q. For every bounded law satisfying

```
centered radius <= sqrt(s)/2,
Cov(X)/s >= 2^-15 I,
Q <= 2^-48 d,
```

the [proof](PROOF.md) gives `H(u)>=2^-40 d` on the ENTIRE interval
`[1/64,1/2]`, and `H(u)>=0` for `u>=1/64`. It permits diffuse laws and
loss tending to zero. It does not sign `0<u<1/64` or prove a new KP case.

The analytic mechanism retains the second loss moment in R1's accepted
first-variation estimate. Ten additional features preserve this guard under
R3's paired cubature: **79 pairs suffice at degree four**, and the existing
loss-relative error schedules remain available with only ten extra atoms.
The [consumer handoff](HANDOFF.md) is an exact polynomial guard before any
threshold mesh, with UNRESOLVED as the result when the guard fails.

A complete rational parameter family allows `0<t<=2^-40`, rare mass
`alpha<=2^-65 t`, and independently varying priors within the two four-site
groups of R6's motion-obstruction geometry. The parameter proof is uniform;
it does not enumerate priors or infer signs from samples. The balanced member
already has a stronger parity-alignment proof, credited in the source.

Run with standard-library CPython 3.11 or later, from this directory:

```
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

Expected marker: `LOSS_MOMENT_MIDDLE_PASS`. About three seconds and 20 MB.
The compact [record](EXPECTED.json) includes 225 finite family controls,
72 independent pair-sum versus moment checks, and an exact 31-to-22 pair
cubature matching all 79 features. Equal marginals with different Q show
why the extra features matter. Six invalid-input or altered-data controls
are rejected. The continuum proof and general cubature existence remain
written mathematics; these checks are not independent review.

[INPUTS.json](INPUTS.json) pins the accepted analytic dependencies and the
geometric template. [SOURCES.md](SOURCES.md) records attribution and the
newer team context. No solver, floating sign, large certificate, or private
input is required. Rational bit complexity and effective diffuse-law input
oracles are not bounded. Ordinary rounding is not part of the theorem.
