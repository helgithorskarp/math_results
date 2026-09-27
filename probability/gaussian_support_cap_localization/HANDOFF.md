# R2/R3/R8 consumer: support-cover reserves

The measure-localization handoff now accepts any finite contracting
reference with positive support width. No conditional-expectation
certificate is needed. The actual map must still contract. Independent
review of this new consumer is pending; the two analytic inputs are
independently accepted.

## Input and output

Give rational paired sites `x_i,y_i`, positive rational reference weights
`p_i`, an enclosing radius `R0` after separate **unweighted** centering,
a cloud radius `r`, and common-label relative prior tolerance `rho<=1/2`.
The actual original law must have label probabilities `q_i` within
`rho p_i` of `p_i`, with source/image displacement at most `r` from the
respective sites. Zero reference weights are discarded. The geometry
checker verifies all reference contractions and the radius.

Run [certificate.py](certificate.py). A six-face exact sphere integral
returns a lower bound `w>0` on **half** the mean-width difference. It then
checks

```
R = R0+r,
d = (1-rho)^2 D0 - 16R0 r - 8r^2 > 0,
b = w-2r > 0,
2^-k <= (1-rho) min p_i,
N = max(1,ceil(R(k+1)/b)).
```

Output `CERTIFIED_UNIFORM_EVENTUAL_FAMILY` signs every threshold for all
`s >= (2112 R^4/d) 2^(8N)`, for the entire specified cloud/prior family.
`UNRESOLVED` only means a width mesh or reserve was insufficient.
The complete record can be checked separately by

```sh
python3 -B verify.py --input INPUT.json --certificate CERTIFICATE.json
```

The common-label and actual-contraction obligations remain explicit in
the record. There is no separate lower mass per actual atom. If a law is
partitioned using original support sites and true images, its cell masses
and a source cover radius give the required two endpoint covers directly.
Rational perturbations of such a reference must preserve contraction;
rounding arbitrary tight pairs without first creating slack is invalid.

## Relation to the accepted spine

R1's accepted spherical lower bound controls the entire finite interval
`[1/(2R),N/R]`; the support-cover estimate controls `[N/R,infinity)`.
The accepted endpoint6032/6048 then joins all Gaussian thresholds. There
is no residual moving-window obligation in this eventual regime.

R8's earlier qualitative bounded-law openness supplied the right
support/width topology but required a middle sign. The universal spherical
theorem now supplies that sign, with a conservative effective constant.
R3's previous martingale localization remains preferable when available:
its cutoff is polynomial in the reserve, and it tolerates independently
reweighted endpoint laws. This consumer trades that witness requirement
for width and cap-mass data and a much worse cutoff.

The near-cubic paired cubature and accepted mean-loss modulus are
preserved. Matching moments alone is not a support cover and does not
supply the mass/displacement hypotheses. There is no claim that a fixed
atom count covers all of these families. R2's balanced-loss guard, R4's
new rigid-block guard, R8's norm-preserving guard, and the whole-prism affine
slice theorem give complementary all-variance regions; none is an
analytic dependency of this consumer.

## Remaining boundary

For a fixed bounded pair with strictly positive support-width gap, finite
cover and rational certificate existence are proved in PROOF section5.
The required masses can be tiny and their verification depends on the
measure description. No boundedness-only complexity or variance bound
follows. The cutoff in the compact control contains `2^512` and is not
claimed numerically sharp or practically small.

The unrestricted target still requires the complementary variance range,
and a method for any non-isometric zero-width infinite-support sector if
such a sector exists. Finite Gorbovickis strictness does not resolve that
limit by itself. No global defect improvement or all-variance transfer
from this certificate has been established.
