# Independent review: homogeneous angular-ray contractions

## Verdict

**Accept for correctness in the stated scope; historical novelty remains
uncertain.**  At exact source commit
`c60fa0275e6e28e870cce2256595f2431a4e6efb`, the whole-cone criterion,
fractional-linear contracting motion, Gaussian-majorisation consequence,
arbitrary-radius union/intersection consequences, and global nonsmooth
three-dimensional example are correct.  This verifies Discovery Net
contribution `bafkreidy6wjmsnzoenmqqwo4kos36fwuvpj65gq5iioqownidek64axyaa`
at height 6402.

The result covers every nonexpansive positively homogeneous map that
preserves each ray and its orientation.  It permits arbitrary atom weights,
nonatomic bounded laws, all positive Gaussian variances, and arbitrary
individual ball radii.  It does not cover angular remapping, negative ray
factors, general radius-and-direction dependence, or a contraction known
only at finitely many selected points.

## Exact whole-cone criterion

For two directions, write `a=alpha(u)`, `b=alpha(v)`, `c=u.v`, and
`d=sqrt((1-a^2)(1-b^2))`.  The source-minus-target squared-distance loss at
radii `r,q>=0` is

```text
(1-a^2)r^2 + (1-b^2)q^2 - 2c(1-ab)rq.
```

This copositive quadratic is nonnegative for all nonnegative radii exactly
when `c(1-ab)<=d`.  If the cross coefficient is nonpositive, every displayed
term is nonnegative.  If it is positive and `1-a^2>0`, minimisation in `r`
gives the condition
`c^2(1-ab)^2<=(1-a^2)(1-b^2)`.  When a diagonal coefficient vanishes, any
positive cross coefficient gives a negative value at a sufficiently large
radius ratio.  This closes the cases `a=1` or `b=1`, rather than obtaining
them by an unjustified division.  Comparing with the origin also forces
`0<=a,b<=1`, and the same-ray case forces a unique factor.

The hypothesis is consequently stronger than contraction of one point on
each ray.  The independent checker includes an exact rational pair whose
unit representatives contract but whose minimizing unequal-radius pair
expands.

## Fractional-linear motion

For `tau=cos(theta)`, the raised direction has horizontal and vertical
coefficients

```text
A=(a+tau)/(1+a tau),
B=sqrt(1-a^2) sin(theta)/(1+a tau).
```

The denominator is at least one, and direct expansion gives `A^2+B^2=1`.
For two directions, differentiation of their raised inner product gives

```text
k'(tau) = M(a,b,tau)[c(1-ab)-d]
          / [(1+a tau)^2(1+b tau)^2],
M=(a+b)(1+tau^2)+2tau(1+ab)>=0.
```

Thus `k` is nonincreasing in `tau`.  Since `tau` decreases as the motion
parameter increases, `k` increases and every squared pair distance
`r^2+q^2-2rqk` decreases.  This remains valid at zero and unit factors and
for unequal radii.  The final raised point is
`(T(ru),r sqrt(1-a^2))`.

The second stage fixes the horizontal target and linearly lowers its last
coordinate.  Every pairwise squared distance is the target distance plus

```text
(1-t)^2 [r sqrt(1-a^2)-q sqrt(1-b^2)]^2,
```

so this stage also contracts.  Concatenation therefore gives one
simultaneous motion of the whole cone, not atom-dependent paths.

Nonexpansiveness makes `alpha(u)=|T(u)|` continuous on the possibly
nonclosed subset of directions.  The formulas are jointly continuous away
from the origin and have norm at most the input radius at the origin.
Denominators stay uniformly separated from zero, so coordinates and time
derivatives are bounded on bounded supports.  For each finite labelled
configuration both stages are analytic, apart from their single join, as
required by the geometric transfer.

## Gaussian and ball-volume transfers

Padding the one-coordinate lift by one zero coordinate gives a continuous
contraction in `R^(n+2)`.  [Aishwarya--Li, Theorem
1.4(i)(a)](https://arxiv.org/html/2609.07041v2) applies under continuity
alone and gives the sampled-density coupling in the direction used by the
source.  At either endpoint the enlarged density factors as
`f(x) gamma_(2,s)(z)`.  For independent `X~f` and `Z~N(0,sI_2)`, the variable
`exp(-|Z|^2/(2s))` is uniform on `[0,1]`; hence

```text
Pr[f(X) gamma_(2,s)(Z) > h(2 pi s)^(-1)] = integral (f-h)_+.
```

The sampled-density order therefore proves every hinge comparison.  At
`h=0` both sides equal one.  This is the precise two-extra-coordinate
cancellation, not an inference from endpoint 1-Lipschitzness alone.

For finitely many centres, reverse the piecewise-analytic motion and apply
[Bezdek--Connelly, Theorem
1](https://arxiv.org/abs/math/0108098).  That theorem transfers an expansion
in `R^(n+2)` to both arbitrary-radius volume signs in the endpoint `R^n`.
Its proof explicitly allows intervals on which labels remain coincident.

The source also gives a valid collision-free reduction.  Replacing `alpha`
by `(1-epsilon)alpha+epsilon` is the convex combination
`(1-epsilon)T+epsilon I`, hence remains nonexpansive.  All factors become
positive: different rays stay separated by their horizontal directions,
and distinct radii on one ray stay separated by positive homogeneity.
This proves injectivity throughout both stages.  Letting `epsilon` tend to
zero is legitimate because finite ball-union and ball-intersection volumes
are continuous in their centres.  Repeated source centres map together and
can be merged using the maximum radius for a union or minimum radius for an
intersection; zero radii follow by a further limit.

## The global three-dimensional example

For `alpha(u)=|u1 u2 u3|`, away from the coordinate planes,

```text
alpha^2 = z1 z2 z3 <= 1/27,
|grad_S alpha|^2 = z1z2+z1z3+z2z3-9z1z2z3 <= 1/3,
```

where `z_i=u_i^2` and their sum is one.  The first bound is AM--GM; the
second uses
`1-3(z1z2+z1z3+z2z3)=sum_(i<j)(z_i-z_j)^2/2>=0`.

For a general angular factor, the derivative on the radial/angular plane is
the shear `[[alpha,g],[0,alpha]]`.  Its norm is at most `q>=alpha` exactly
when `g<=q-alpha^2/q`, as follows from the two principal minors of
`q^2I-J^T J`.  At `q=2/3`, the right side is at least `11/18`; its square
exceeds `1/3` by `13/324`.  Thus the derivative norm is at most `2/3` in
each open orthant.  Every segment either lies in a coordinate plane, where
the map is zero, or crosses only finitely many such planes; integration and
continuity, splitting at the origin when needed, prove the global bound.

The scalar-defect exclusion has the correct direction.  The two one-sided
Jacobians at a generic point of the `k`th coordinate plane are
`+-h u e_k^T`.  Applying the proposed defect to its first unit axis and
adding the two required nonnegative expressions gives
`-2h^2 E^2(1+F^2)`, forcing that axis to be orthogonal to every coordinate
axis, a contradiction.  The strong-coordinate exclusion is also sound:
each output coordinate would be a one-variable function constant on three
distinct planes, while its input functional is nonconstant on at least two
of them, forcing the function to be globally constant.

## Reproduction and independent evidence

The target checker passed under normal and optimized CPython with marker
`AUTHOR_CHECKS_PASS`.  All six target manifest entries match.  The committed
record hash is
`31ed346da9fb5403c85cad9a337e2660a502b5b3bad1b0b80c1a70ea059ec359`.

[`independent_check.py`](independent_check.py) imports no target code and
uses exact `fractions.Fraction` arithmetic.  It:

- pins the proof, sources, checker and expected-record bytes;
- verifies the cleared derivative identity on a 144-point tensor grid whose
  sizes exceed its explicit degree bounds, thereby proving the polynomial
  identity by interpolation, and rejects the altered sign;
- independently checks all 125 cone fixtures using exact quadratic
  minimizers, with 97 accepted and 28 explicit failures;
- constructs the lifted points directly in coordinates at six rational
  stereographic angles and verifies both motion stages for all 97 admissible
  cases;
- checks 364 exact barycentric controls for the global example, the shear
  determinant and reserve, the paired-rank determinant and scalar-defect
  signs; and
- checks positive-factor perturbations and rejects a rational inadmissible
  lift that contracts its unit representatives.

Run from the repository root with standard-library Python 3.11 or later:

```sh
python3 -B probability/gaussian_angular_ray_review_frontier/independent_check.py
python3 -B -O probability/gaussian_angular_ray_review_frontier/independent_check.py
cd probability/gaussian_angular_ray_review_frontier
sha256sum -c SHA256SUMS
```

Expected marker: `ANGULAR_RAY_INDEPENDENT_ACCEPT`.

## Trust boundary and exclusions

The executable evidence guarantees the pinned source bytes, interpolation
identity and stated finite exact controls.  The continuum copositivity
argument, simultaneous-motion regularity, segment integration, stochastic
transfer and ball-volume transfer remain written mathematics checked above.
The two cited transfer theorems are external dependencies, not re-proved
results.

The review does not establish historical priority, classify all positive
maps, or prove unrestricted dimension-three Gaussian majorisation.  It does
not accept signed factors, angular remapping, arbitrary radius-dependent
factors, or finite-sample endpoint contractions as instances of this theorem.
