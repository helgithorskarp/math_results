# Strict norm-preserving Gaussian comparison

The [author proof](PROOF.md) gives a loss-normalized strict margin for
**every bounded norm-preserving contraction in R3**, including diffuse laws.
If the support map is nonisometric, every hinge below the target Gaussian
peak is strictly positive. Equality at one such hinge forces isometry.

With anchors satisfying `|x-a|=|T(x)-b|<=R sqrt(s)`, let `D` be the ordered
mean squared-distance loss and `C_s=(2 pi s)^(-3/2)`. For integers
`R>=1`, `j,k>=0`, put

```text
W=2R+2^(j+1),                 N=2W²+W+8R+8k+33.
```

On `C_s 2^-j <= h <= max(g)-C_s 2^-k`, the hinge gap is at least
`(D/s)2^-N`. Its coefficient is independent of the loss, atom count,
minimum weight, and covariance. A radial crossing in the reviewed positive
kernel gives this bound even at critical thresholds.

Combining strictness with the accepted compact-width theorem and the
earlier bounded-law openness criterion makes every nonisometric member
an **ambient interior point at each fixed variance, without an additional
homothety**. Both endpoint laws may be perturbed independently, breaking
the anchor condition. One positive neighborhood works on any specified
compact positive variance interval. Section 5 gives the minimal finite-beta
interface for R2/R3.

This is an author proof awaiting independent review. The norm-preserving
non-strict comparison was already proved and reviewed; general openness
was also already proved. [SOURCES.md](SOURCES.md) credits both. No uniform
neighborhood as the variance or loss tends to zero, new Kneser--Poulsen
limit, unrestricted theorem, or fixed-variance sign for the canonical screw
is claimed.

## Reproduction and trust boundary

From this directory, using CPython 3.11 or later and its standard library:

```sh
python3 -B verify.py
python3 -B -O verify.py
python3 -B verify.py INPUT.json
sha256sum -c SHA256SUMS
```

The first two commands compare their complete output with [EXPECTED.json](EXPECTED.json).
Expected status: `STRICT_NORM_HINGE_CONTROLS_PASS`; record file SHA-256:
`fe45528d1fa47c19aa3adb40c805644930f9e5d54c3cc5525ff8cd8842b14f5d`.
The full audit uses five adjacent repository sources for byte pins; the
supplied-input mode only needs this packet. Runtime is under one second
on the author's CPython 3.11.2 host. No numerical library, quadrature,
solver, external dataset, or large certificate is used.

The rational seven-site coordinate-fold calibration has paired affine
rank six, 21 pairs, 15 tight pairs, and `D=129/392`. It certifies the bound
`(129/392)2^-723` on `1/8<=h/C<=1/4`. It is a familiar positive example,
not a new geometric class. A separate symbolic two-site family has `D=t`
on `0<=t<=1/16`, checking that the same coefficient persists through zero
loss. Additional exact controls cover 19 posterior laws, 192 kernel
configurations, 125 constant schedules, independent endpoint frames,
variance scaling, and 12 failed or malformed guards.

For another finite input use [INPUT.json](INPUT.json)'s schema: rational
3-vectors, strictly positive rational weights summing to one, independent
anchors, rational variance, and integer `R,j,k`. `UNRESOLVED` means a
sufficient hypothesis failed, not that majorisation is false. Malformed
data raise an error. The output distinguishes a band conditional on the
true target peak from an explicit band using its conservative lower bound.
It does not numerically estimate either peak.

The [checker](verify.py) verifies exact finite hypotheses and supporting
algebra. The radial crossing, smooth hinge limit, diffuse-law extension,
and ambient topology are written mathematical arguments, not consequences
of the finite tests or a proof-assistant formalization.
