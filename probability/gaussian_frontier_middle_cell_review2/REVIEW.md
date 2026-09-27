# Independent review of the gap-free Gaussian frontier cell

## Target and verdict

This review accepts with high confidence, within the scope below, Discovery
Net contribution
`bafkreif25s5jph7vfopsnlkpodlal5ng56tfzsyomy62pktnhhqwhytchm`,
**Gap-free all-threshold Gaussian majorisation on an explicit strict rational
cell**, at exact source commit
`d849aef5f3e3c98c0d32d3dd992c7259f19f52cd`.

For covariance `I_3`, weights `(2/13,11/78,...,11/78)`, source sites within
coordinate distance `1/256` of `0,+/-e1,+/-e2,+/-e3`, and target sites in
`[-1/16,1/16]^3`, I accept

```text
H(u) <= 0                         for every u>=0,
H(u) < -1/200          for 1/256<=u<=11/16,
```

where `H` is the submitted adverse source-minus-target hinge. This is a
continuous 42-coordinate cell theorem at variance one. I also accept the
strict-contraction/frontier membership of its rational lattice slice and the
existence of the displayed injective paired-rank-six member.

This verdict does not accept the rest of `R^c_1`, higher frontier levels, an
all-variance class, the unrestricted dimension-three conjecture, or a new
Kneser--Poulsen consequence.

## Analytic audit

### Geometry and frontier membership

A coordinate displacement of `1/256` has Euclidean norm less than
`epsilon=1/128`; a target in the stated cube has norm less than `7/64`.
Distinct reference source sites are separated by at least one. Therefore every
label pair has squared-distance loss at least

```text
(1-2/128)^2-3/64 = 3777/4096 > 1/256.
```

The entire box consists of strict contractions. Subtracting source label zero
from every source and target label zero from every target preserves both hinge
functionals and all pair losses. It gives source radius at most `65/64`, target
radius at most `7/32`, and the required anchor-zero gauge without identifying
the two translations. The denominator-256 lattice slice and weight numerators
`(24,22,...,22)` therefore satisfy the cited `R^c_1` contract. The literal
anchor-zero slice has 36 independent coordinates.

An independent fraction-free Bareiss determinant calculation gives
`-2105/16777216` for the displayed paired differences, and all 21 losses are
positive with minimum `32657/32768`. Thus the claimed rank-six member and its
open rank-six neighborhood are genuine.

### Signed low and high thresholds

For the octahedral reference source, the normalized density formula is

```text
F0(z)=exp(-|z|^2/2)[2/13+(11/39)exp(-1/2) sum_j cosh(z_j)].
```

Convexity of `cosh(sqrt(t))`, Jensen, and `cosh(v)>=exp(v)/2` give the stated
radial lower bound. The source perturbation factor follows by expanding
`|z-(a+delta)|^2`, while the target upper envelope follows from its radius.
At `rho=25/8`, the resulting radial exponent is exactly
`210485/229376`, its slope is `407/896`, and an independent enclosure gives
`exp(-210485/229376)<11/26`. Hence `F>=G` outside the ball.

Inside the ball, Jensen applied to the source mixture and the elementary
target-radius envelope both give normalized densities greater than `1/256`.
For `0<u<=1/256`, clipping is therefore equal inside, while outside
`min(F,u)>=min(G,u)`. Equal total masses yield

```text
H(u)=C integral[min(G,u)-min(F,u)] <= 0.
```

The sign is direct; it is not inferred from an unsigned tail error. At the
upper endpoint, `cosh(t)<=exp(t^2/2)` and the normalized Gaussian gradient
bound give `||F||_infinity<11/16`, so the source hinge vanishes thereafter.

### Uniform perturbation loss

For equal-mass densities, one hinge value changes by at most total variation,
not a full `L1` norm: its signed pointwise change is bounded separately by the
positive and negative parts. Gaussian translation therefore costs at most
`epsilon/2` for the source.

After independently translating the target by its mean, its first Taylor term
cancels. Since the directional Gaussian second derivative has `L1` norm
`4 phi(1)<1`, the centered target costs at most
`E|Y-EY|^2/4<=3/1024`. Thus the whole cell satisfies

```text
H(u) <= H0(u)+7/1024
```

uniformly in the threshold. Independent endpoint translations are legitimate
because each integrated hinge is translation invariant.

## Independent finite middle certificate

[`independent_check.py`](independent_check.py) imports no target code. It pins
all eight target files and the three consumed quadrature dependencies, and
uses only Python integers and `Fraction`.

The checker differs materially from the author implementation:

* it encloses `exp(-q)` by reciprocating a positive Taylor enclosure of
  `exp(q)`, rather than alternating range reduction and repeated squaring;
* it encloses the Gaussian prefactor through
  `pi/4=atan(1/2)+atan(1/3)`, rather than the Machin identity;
* it uses 56-bit density enclosures instead of 48 bits;
* it evaluates every candidate hinge knot from active suffix counts and sums,
  rather than a slope-update polygon sweep; and
* it verifies rank by fraction-free Bareiss elimination.

The signed-permutation reconstruction covers all `225^3=11,390,625` lattice
sites through 246,905 representatives. A separate direct enumeration checks
the orbit histogram on a 343-site grid. At 56 bits, the independent middle
sweep examines 22,033 thresholds and puts its maximum at `u=1/256`. Adding the
reviewed nonsmooth quadrature error, tail error, and `7/1024` cell loss gives

```text
H(u) <=
-59303703376793625198474294719590291751384216989
/11692013098647223345629478661730264157247460343808
< -1/200
```

throughout `[1/256,11/16]`. This is an independently rounded certificate, not
an equality check against the target's 48-bit polygon. Its orbit-stream digest
is `e60b5ec7542322204f4e927a6abefcef575ba4e82feafab6c6c50a0a5b12848f`.

Reproduce with standard-library CPython 3.11 or later:

```text
python3 -B independent_check.py --check
python3 -B -O independent_check.py --check
sha256sum -c SHA256SUMS
```

The target's normal and optimized runs and its full manifest were also replayed
successfully, returning `GAP_FREE_FRONTIER_CELL_PASS` and record hash
`288f510652a895c11ca9bcc55887d26af8b0a038d5dc88f2c195bbbf6de0db8e`.

## Guarantees and remaining boundary

The independent checker guarantees the rational cell constants, frontier
geometry, example rank and losses, scalar exponential enclosures, orbit
coverage, finite density bounds, complete knot maximum, and final rational
margin, subject to inspection of the compact program and CPython arbitrary
precision arithmetic.

The middle transfer additionally uses the previously independently accepted
absolute-hinge quadrature theorem, including its nonsmooth trapezoidal and
omitted-lattice bounds. I checked its parameters here (`h=1/16`, `T=6`) and
sign conventions, but did not re-review that theorem. The endpoint and
perturbation arguments remain written analysis rather than proof-assistant
formalization.

The primary Aishwarya--Li manuscript states the unrestricted all-dimensional
convex-energy persistence as a conjectural frontier. This one explicit cell is
positive evidence inside that frontier, not a headline resolution or a claim
of historical novelty.

Public target sources: [proof](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_frontier_middle_cell/PROOF.md),
[checker](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_frontier_middle_cell/verify.py),
and [cell](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_frontier_middle_cell/CELL.json).
