# Three unstable split modes of the degree-nine two-pair branch

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.

The preceding two-pair theorem constructed a complete minimum within
that family and proved stationarity under all fixed-energy circle-root
motions. This contribution proves that its negative-side branch is a
**saddle** in the larger circle-root space: all three balanced split modes
of its four collapsed original roots are negative. The two-pair transfer
direction is positive. An actual three-pair polynomial gives descending
motions with every root on the circle and exactly the same energy.

For the definitions, complete quantified statements and ordinary written
proof, read [PROOF.md](PROOF.md). The marked root is simple and real,
all algebraic multiplicities count, and the neighborhood is a common
small-energy window `a=a_Q(e)+ce, -C<=c<0`, for each fixed finite C>0.
Thresholds and remainder constants may depend on C. Here `a_Q` and the
branch retain their earlier authorship; independent review8378 confirms
the8315/8364 inputs and supplies their bounded-C extension with reviewer
credit. If `H4` is the derivative for splitting
a further opposite pair, the new relative sign law is

    H4 = e^2 c [(15/8) lambda_- + O_C(e)] < 0.

The error is uniform even when c approaches zero. At a fixed positive
e,c the descent interval and angular Taylor neighborhood may depend on
that point. No uniform positive split-energy threshold is claimed.

The exact cross coefficient is `mu=-h1-(7/4)gamma`. A rescaled monic
factor system continues the actual derivative analytically to zero
auxiliary energy, where it equals the credited H exactly. For the
repeated critical group, its first angular compression is anti-Hermitian.
A trace Taylor argument gives a quadratic form without an internal
eigenvalue gap. Permutation symmetry identifies its three negative modes.

Run the standalone checker with **CPython 3.11.2**, standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
```

Both modes passed 126 exact identities, six strict sign certificates,
seven rejected damaged mathematical controls, five complete reducing
inputs with thirty full left/right vectors, and eight complete angular
inputs with all 512 compression entries. All 23 whole records must match
[expected.json](expected.json); thirteen altered or missing fixtures
rejected in the publication checks. There is no sampled identity,
floating-point proof input, solver assumption or private dependency.

Actual polynomial checks retain independent e,f,g with no truncation.
Rescaled base factor jets are checked modulo e^6; the asserted derivative
coefficients go through energy degree two. Exact arithmetic uses rational
Laurent polynomials and the isolated positive quadratic field
`239v^2+184v-208=0`, `3/5<v<5/8`.

Canonical record SHA256:
`2d80937f827264cd507849e5d60e5b67f8b87a187afaf7f6893991e762525e20`.
Checker SHA256:
`00a06727bd59efeebbcb09a7b5b4a9511e22b961043cf7c764d54dd1af5db488`.
Fixture SHA256:
`873490a0042a916a5ba663bd95a37a49bf01eab5552c108e7814ac755cf8ef9f`.
Normal/optimized runtime was 0.394/0.619 seconds; peak child RSS
22,844 KiB. Fixture generation is a separate explicit operation:
`python3 verify.py --write-fixture OUTPUT.json` skips fixture comparison
and is not a successful verification of the mandatory fixture.

The analytic implicit-function arguments, physical root regimes, exact
continuation at zero auxiliary energy, divisibility, uniform relative
sign and spectral trace Taylor bridge are ordinary written mathematics
outside a formal kernel. Independent review of this extension is pending.
[LITERATURE.md](LITERATURE.md) records primary literature, dependency
statuses, original credit and the reproduced baseline.

The result refines the earlier family minimum, which expressly withheld
full angular stability. It resolves neither the unrestricted fixed-energy
optimizer nor the first-power Tang--Zhang inequality. The next frontier
is the joint actual three-pair objective and its remaining split/mean
directions; the boundary derivative here alone does not determine that
joint normal form. All inward depths and full-disk entry remain open.
