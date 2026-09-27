# All-variance localization on affine components

This [author proof](PROOF.md) gives an atom-count-free sufficient criterion
for Gaussian majorisation on a finite union of compact, full-dimensional
affine components in R3. A single contracting motion certifies **every law
on the domain, every Gaussian variance, and every hinge threshold**, and
the arbitrary-radius union and intersection Kneser--Poulsen signs for every
finite selection of centers. Independent acceptance is pending; the full
dimension-three problem remains open.

Choose an auxiliary probability on the domain with component masses at
least `m`, conditional covariance at least `kappa I`, global covariance at
least `k I`, and domain diameter at most `d`. The actual input law has no
weight or covariance restrictions. For centered auxiliary pairs `(X,Y)`,
`Y=T(X)`, and an independent copy, set

```text
F = E[(X.X' - Y.Y')^2],
e = 2F/(km),               C = 4 + 78d^2/kappa.
```

The map must be affine and contractive on each component, and contractive
on the whole domain. If the minimum cross-component squared-distance loss
is at least `Ce` and `e<=kappa/4`, all comparisons above follow. In particular,
if cross losses are at least `rho` times the largest pair loss, the whole
auxiliary mean-loss sector

```text
D <= 2rho k m/(4+78d^2/kappa)
```

has the favorable sign at **all** scales, uniformly through `D=0`.

The key step converts mean alignment error into control of every point of
an affine component, using its auxiliary covariance. Polar interpolation
allows actual compression within each component. This extends the mechanism
of the [accepted rigid-block certificate](../gaussian_rigid_block_certificate/)
beyond finite rigid pieces; its lower-dimensional cases remain complementary.
It is not a claim that arbitrary cubature cells meet these hypotheses.

## Exact consumer

[`certificate.py`](certificate.py) accepts rational affine maps on solid
boxes. It proves whole-box contraction and the motion budget with exact
arithmetic, in `O(B^2)` fixed-size matrix operations for `B` boxes. Bit cost
depends on the input. Successful output signs every law on those boxes;
`UNRESOLVED` is a failed sufficient guard, not an adverse Gaussian hinge.

[`verify.py`](verify.py) has a supplied-record mode which imports no producer.
It uses exact product cubature to reconstruct the quadratic Gram error and
64-corner bounds for the multiaffine remainder of each cross loss. This is
not Gaussian quadrature or moment determination of hinges.

From this directory, with CPython 3.11 or later and the standard library:

```sh
python3 -B certificate.py INPUT.json > /tmp/affine-components-record.json
cmp /tmp/affine-components-record.json CERTIFICATE.json
python3 -B verify.py --input INPUT.json --certificate CERTIFICATE.json
python3 -B verify.py > /tmp/affine-components-audit.json
cmp /tmp/affine-components-audit.json EXPECTED.json
python3 -B -O verify.py > /tmp/affine-components-audit-opt.json
cmp /tmp/affine-components-audit-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

The full audit uses repository history for the seven byte pins in
[`INPUTS.json`](INPUTS.json); supplied-record verification needs no git history.
The expected audit status is `AFFINE_COMPONENT_LOCALIZATION_PASS`, with
canonical output SHA-256
`e70cbbc7c188fa651db00cc70fd55753f6fe8f023040ca9b2d78e81a2147f4eb`.
Normal and optimized CPython 3.11.2 runs matched, taking 3.304 and 5.272
seconds respectively on the author host. Both are finite author checks.

The calibration consists of three solid cubes with different rotations and
rank-one affine compressions. The proof covers the entire interval
`0<=t<=2^-36`; [`INPUT.json`](INPUT.json) is its upper endpoint. For positive
`t`, the map has no finite rigid-piece cover, no anchored norm-preserving
description, and no globally aligned contracting straight interpolation.
No exclusion from every historical motion class is claimed.

The proof, [consumer handoff](HANDOFF.md), and [attribution](SOURCES.md) state
the analytic dependencies and remaining limitations. General nonlinear
components, collapsing auxiliary covariance, uncontrolled component masses,
and tight cross-component contacts are not covered. The global `7/50`
adverse-defect cap is unchanged.
