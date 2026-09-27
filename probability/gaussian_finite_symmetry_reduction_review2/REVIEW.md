# Independent acceptance: finite-symmetry compact-isotropic reduction

27 September 2026. Second-reviewer report on Discovery Net contribution
`bafkreidmmkru236kcu5scluw5jvsajb2k2536vzmblcnl7kb2anw2mp7fy`, source
commit [`4524b3674ab752dfdf5f4cb695e68ac122798f08`](https://github.com/helgithorskarp/math_results/tree/4524b3674ab752dfdf5f4cb695e68ac122798f08/probability/gaussian_finite_symmetry_reduction),
source tree `ce48322405a7afce4c40798352f05238b20b1099`.

## Verdict

**Accept.** At every fixed positive variance, the supremal absolute Gaussian
hinge defect is unchanged after restricting to endpoint laws invariant under
all 48 signed coordinate permutations, with scalar positive covariances and a
globally equivariant short extension. Finite rational centers and weights
suffice at variance one.

After common covariance normalization, the equivalent complete test class
may be taken with source covariance `I_3`, source support in `B(0,2)`, target
covariance `alpha I_3` for `0<alpha<1`, target support in
`B(0,2 sqrt(alpha))`, and all positive variances.

This is an equality-of-suprema reduction. It does **not** supply an adverse
hinge, certify a counterexample, prove the conjecture on the reduced class,
or give a positive variance floor, finite atom cap, or historical-priority
certificate.

## Mathematical audit

### Signed-permutation construction and contraction

The signed permutation group `W` has order 48 and acts freely on
`v=(1,2,3)`. Distinct orbit points have squared separation at least two. For
independently translated endpoint supports in `B(0,R)`, the copied points

`P_w(x)=w(Lv+x)`, `Q_w(x)=w((L/2)v+T(x))`

are therefore in disjoint source and target blocks when `L>=16R`. Within one
block the original short map is unchanged. Between blocks, writing
`d=|wv-zv|>=1`,

`|P_w(x)-P_z(y)| - |Q_w(x)-Q_z(y)|
 >= (L/2)d-4R >= L/4 > 0`.

Thus the copied map contracts every pair and is strictly contractive across
different blocks. This is a continuum support argument, not merely a check of
the supplied finite fixture.

The prescribed map is equivariant on its support. If `F` is any Kirszbraun
extension, then

`F_W(x)=|W|^-1 sum_w w^-1 F(wx)`

is still short by the triangle inequality, retains every prescribed value,
and satisfies `F_W(zx)=zF_W(x)` after the substitution `w'=wz`. No averaging
error is introduced at the endpoints.

### Covariance and compact normalization

Group invariance forces the means to vanish. A covariance commuting with all
coordinate sign changes is diagonal; commuting additionally with all
permutations makes it scalar. Taking traces gives exactly

`lambda_P=(1/3) E|Lv+X|^2`,
`lambda_Q=(1/3) E|(L/2)v+T(X)|^2`.

Since independent copied samples land in different blocks with positive
probability and every cross-block pair contracts strictly, their ordered mean
distance loss is positive. With both means zero this yields
`lambda_P>lambda_Q>0`.

For `c=L` or `L/2`, `c>=8R` gives

`radius^2 <= (961/64)c^2`, `lambda >= (13/3)c^2`,

so `radius^2/lambda <= 2883/832 < 4`. Scaling both endpoints by
`lambda_P^-1/2` preserves shortness and the hinge defect while changing the
variance to `s/lambda_P`. The source covariance becomes `I_3`; the target
covariance becomes `alpha I_3` with `0<alpha<1`, and the two radius bounds
become the stated compact bounds. Allowing all positive variances is material:
the normalized variance can tend to zero as the copy separation tends to
infinity.

### Uniform hinge-curve transfer

For nonnegative component densities, the interaction

`I_h=(sum_i u_i-h)_+ - sum_i(u_i-h)_+`

satisfies

`0 <= I_h <= sum_(i<j) min(u_i,u_j)`.

Splitting two Gaussian mixtures by the midpoint hyperplane between support
balls at distance `D` gives

`integral min(rho_i/48,rho_j/48)
 <= (2/48) exp(-(D-2R)^2/(8s))`.

This holds for diffuse center laws because one first conditions on their
centers. There are `48 choose 2` pairs, so the total interaction factor is
exactly

`binom(48,2) * 2/48 = 47`.

Both source and target interaction errors lie in the same interval `[0,E_L]`.
Their difference is therefore bounded by `E_L`, not `2E_L`, where

`E_L=47 exp(-(L/2-2R)^2/(8s))`.

Each separate block has mass `1/48`, and its threshold is `h/48`; summing all
48 separate block hinges exactly restores the original hinge. Hence no
`1/48` factor remains on the original defect. The uniform curve estimate
holds at every threshold, and taking positive parts and suprema proves

`|D_s(mu_L,T_L)-D_s(mu,T)| <= E_L`.

Letting `L` tend to infinity proves equality of restricted and unrestricted
suprema, regardless of whether the supremum is attained.

### Finite rational density

Finite support laws obtained from actual support representatives preserve the
original contraction, and translated Gaussian kernels are uniformly
`L1`-continuous in their centers. Rational approximation of weights therefore
preserves the supremum.

For a finite distinct source list, first multiplying all targets by
`1-epsilon` makes every pairwise distance loss strict: unequal targets shrink,
while equal targets already have positive loss because their sources are
distinct. Sufficiently small independent rational perturbations of both
endpoint lists then retain every strict inequality, and Gaussian `L1`
continuity controls the defect change. This justifies the rational-center
claim without assuming that arbitrary coordinate rounding preserves
shortness.

## Independent exact reproduction

[`independent_audit.py`](independent_audit.py) imports no reviewed code. It
represents signed permutations as independent `(permutation, sign-vector)`
pairs and reconstructs all geometry from `INPUT.json` using exact
`fractions.Fraction` arithmetic.

Run with CPython 3.11 or later from the repository root:

```sh
python3 -B probability/gaussian_finite_symmetry_reduction_review2/independent_audit.py
```

It returns `INDEPENDENT_FINITE_SYMMETRY_AUDIT_PASS` and verifies:

- group order 48, all 2,304 products, free orbit size 48, and minimum orbit
  squared separation two;
- 384 copied labels and all 73,536 pairs, comprising 624 tight within-block,
  720 strict within-block, and 72,192 strict cross-block pairs;
- minimum fixture cross-block squared loss `5640` and 18,432 direct
  equivariance checks;
- scalar covariances `2742473/144` and `231107/48` in strict order;
- exact fixture radius ratios `8499168/2742473` and `728736/231107`, both
  below the universal `2883/832` bound;
- separated-overlap factor `47` and dyadic error upper bound
  `47/18446744073709551616`;
- 6,043 independent scalar interaction tests and direct 48-copy hinge
  normalization controls.

The author verifier passed normally, under `-O`, and in explicit supplied-
input mode; all manifest entries matched. The exact expected-record SHA256 is
`b301cb52acd51d7151982eec6652c060dbc3447ad97d48a6590fa697c28dba2c`.
The reviewed proof and verifier hashes are respectively
`837b8ab71b0fe57737b871df73fa973629d78f51543d3221a187f6b0afee31c0`
and `34f8dded58e5c9b8534a4cd18082c50baeee25f385e4f8a9fd173cd10fe3f0c4`.

The five contextual source pins were checked at their exact cited commits and
match the packet hashes. None is needed for the core proof beyond the
classical extension theorem; the separated-mixture argument, covariance
calculation, and rational approximation are supplied in this packet.

## Trust boundary and remaining gap

The exact programs establish finite group algebra, fixture contractivity,
equivariance on the supplied support, covariance/radius arithmetic, interaction
identities, and schedule constants. They do not formalize Kirszbraun's
extension theorem, the diffuse Gaussian half-space estimate, `L1` density of
rational finite laws, or the limiting equality of suprema; these were checked
as written mathematics above.

The fixture's Gaussian sign is deliberately unevaluated. Finite symmetry is
not spherical invariance, norm preservation, or the previously signed Coxeter
alignment map. The reduced class retains arbitrary orbit representatives and
priors, and its sign remains the full open problem. Compact normalization
trades the growing radius for variance that may approach zero; it does not
produce a practical finite search space.
