# Seven positive diagonals of the Gaussian beta criterion

For every bounded probability law in R3, every contraction and every
positive Gaussian variance, the [author proof](PROOF.md) establishes

    b_(N,j) >= 0 whenever 0<=N-j<=6.

Here b is the team's normalized beta average of the target-minus-source
hinge gap. These signs are strict unless the support map is an isometry.
They include every weight face, repeated sites and diffuse laws, and hold
for every homogeneous weight coefficient before averaging the weights.
All rows N<=6 are completely signed. Seven entries of every later row
can be removed from a negative-certificate search.

Researcher 5's concurrent [projection proof](../gaussian_beta_projection/PROOF.md)
already signs N-j<=5. The additional affine-offset representation here
extends that coverage to N-j=6 and supplies a quantitative certificate.
After conditioning on the distinguished pair and the other base positions,
six remaining points have affine dimension at most five. A Poisson moment
identity retains their common offset and turns the alternating sum into an
integral of nonnegative factors. The full paired configuration may have
rank six; no global five-dimensional motion is assumed.

For the original compact frontier K_l, the following compressed rational
bound holds for **every** configuration Q in that set:

    b_(N,j)(Q) >= [(N+1) binom(N,j)/(1024*3^(N-j))]
                  * 2^[-2(j+2)(18l^2+8l+4)] * E(pair-distance loss).

The checker outputs all seven bounds at l=3, N=429981694. It stores only
rational mantissas and integer exponents, and computes no huge moment sum.
The constants are conservative; they do not replace stronger local margins
in researcher 8's [weight-cell certificate](../gaussian_beta_weight_certificate/PROOF.md).

**The full conjecture remains open.** In particular b_(7,0) is not decided.
Its first unpruned tuple patterns are exactly (2,2,1,1,1,1,1),
(2,1,1,1,1,1,1,1) and nine singletons, with distinguished pairs specified
in the proof. A rational seven-site contraction certifies a remaining
affine-rank-six case, not a negative coefficient. No optimal strip width,
new all-threshold map class or Kneser--Poulsen consequence is claimed.
Independent correctness and historical-priority review are pending.

## Reproduce

Standard-library CPython 3.11 or later. From this directory:

```sh
python3 verify.py
python3 check_controls.py
python3 -O verify.py
python3 -O check_controls.py
sha256sum -c SHA256SUMS
```

The first command reproduces [EXPECTED.json](EXPECTED.json), with status
`UNIVERSAL_BETA_DIAGONALS_EXACT_AUDIT_PASS` and canonical record SHA256

    6011d3623f6916cc7075b79ca1aa03392b52247064986553cf235b97a209b8d5

The control status is `BETA_CONDITIONING_DAMAGE_CONTROLS_PASS`, with six
rejections. Normal and optimized CPython 3.11.2 and 3.12.14 give identical
outputs. One audit takes less than one second on the author's host.

The exact audit covers 28 polynomial normalization identities in an
unbounded base index, 49 finite Gram identities (3528 matrix entries),
the affine-offset and exponent algebra, all 30 partitions of nine and
262 distinct-label pair cases, and the rank-six fixture. These checks
supplement the universal written proof; they do not formalize Gaussian
integration or the Poisson representation. No solver, Gaussian quadrature,
floating-point sign, imported checker, hidden input or large certificate
is required. [SOURCES.md](SOURCES.md) records the dependency boundaries.
