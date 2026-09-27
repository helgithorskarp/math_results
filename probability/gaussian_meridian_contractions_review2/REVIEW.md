# Independent acceptance: meridian contractions

## Verdict

**Accept for correctness in the stated scope.** Let `n>=2`, let
`E` be a subset of the meridian half-plane, and suppose

```text
S(r,z)=(rho(r,z),zeta(r,z)),
|S(p)-S(q)|<=|p-q|,       0<=rho(r,z)<=r.
```

On the full rotational domain define
`T(ru,z)=(rho(r,z)u,zeta(r,z))`. The reviewed proof correctly constructs a
continuous contracting motion in `R^(n+2)`. Consequently, for arbitrary
bounded input laws, every Gaussian variance and every threshold, the target
Gaussian convolution majorises the source. For every finite selected center
list it also proves decreasing union volume and increasing intersection
volume for arbitrary individual nonnegative ball radii.

The exact target is Discovery Net artifact
`bafkreiabngjrclqthd36unxe7cjzyqw3uhmgbr5it62si6yjca6l6dnqf4` at source
commit `a1013f169d8dd6d32ae76cf9817a47dccd3f100f`. Seven target files are
content-pinned in `TARGET_INPUTS.json`. The author checker passes under
normal and optimized CPython 3.11.2 and reproduces record SHA-256
`bf93bccbca8662f73b7db0bd6aa31ac3250124ecc8909777b30960fce59145ae`.

This is a full theorem for the stated equivariant map class, not for an
arbitrary three-dimensional contraction. It does not cover azimuth changes,
signed transverse factors, or establish a classification or historical
priority. The unrestricted dimension-three Gaussian-majorisation problem
remains open.

## Exact geometric mechanism

Write

```text
A_t(p)=(1-t)r+t rho_p,
B_t(p)=(1-t)z+t zeta_p.
```

The proposed point path consists of `(A_t(p)u,B_t(p))` and the two auxiliary
coordinates `sqrt(t(1-t))(p-S(p))`. For two labels with `c=u.v`, direct
expansion gives

```text
|F_t(p,u)-F_t(q,v)|^2
 = (1-t)|p-q|^2+t|S(p)-S(q)|^2
   +2 A_t(p)A_t(q)(1-c).
```

The first part is the planar leapfrog expression. The second is
nonincreasing because both nonnegative factors `A_t` are nonincreasing.
Differentiation yields exactly

```text
|S(p)-S(q)|^2-|p-q|^2
-2(1-c)[(r-rho_p)A_t(q)+(s-rho_q)A_t(p)] <= 0.
```

Thus every pair distance decreases simultaneously; no sign of
`z-zeta` is used. Reparametrizing by `t=sin(theta)^2` makes all trajectories
analytic through both endpoints. Axis continuity follows from `A_t<=r`.
Distinct labels do not collide before the target endpoint: differing
meridians retain the positive `(1-t)|p-q|^2` term, and equal meridians with
different azimuths retain a positive angular term.

The characterization of the hypotheses is also correct on the full
rotational domain. Same-azimuth pairs force the meridian contraction, while
opposite points on one orbit force `rho<=r`; conversely the meridian and
angular summands in the physical squared distance both decrease. This also
covers `n=2`, where the azimuth sphere consists of its two antipodal points.

For a bounded law whose support closure is not contained in the initially
chosen Borel `E`, the Lipschitz map and the motion extend uniquely to the
closure, and `0<=rho<=r` survives the limit. This supplies the compact
support formulation used by the cited Gaussian theorem without adding a
closed-domain hypothesis.

## Gaussian and ball-volume transfers

Aishwarya--Li Theorem 1.4(i)(a) gives a coupling of the lifted endpoint
density samples with the source value at most the target value for a
continuous contraction. The endpoints here factor as the original
`n`-dimensional density times a two-dimensional Gaussian. If `Z` has that
Gaussian law, then

```text
gamma_2(Z)/(2 pi s)^(-1) = exp(-|Z|^2/(2s))
```

is uniform on `(0,1)`. Its sampled upper tail is therefore exactly
`integral(f-h)_+`, with the same formula for the target. This proves every
hinge comparison, including diffuse laws; equal total mass handles `h=0`.

The independently inspected Bezdek--Connelly Theorem 1 states precisely
that a piecewise-smooth expansion in `R^(n+2)` implies both the union and
intersection inequalities in `R^n`, for arbitrary radii. Reversing this
analytic contracting motion meets that hypothesis. If target centers
collide, the convex perturbation

```text
S_epsilon=(1-epsilon)S+epsilon I
```

remains contractive and satisfies `epsilon r<=rho_epsilon<=r`. For a finite
distinct source list, only finitely many positive epsilon values cause a
terminal collision. Applying the theorem along a collision-free sequence
and passing to the continuous volume limit is valid. Repeated source centers
are merged using the largest radius for a union and smallest for an
intersection; zero radii follow by continuity.

## Breadth and rank controls

The latitude-profile example is valid: `phi(0)=0` and one-Lipschitzness give
`0<=phi(theta)<=theta`, while the angle difference contracts inside the
hemisphere. The nonlinear global example has absolute Jacobian bounds
`3/4,1/4,1/4,1/4`, so its squared Frobenius bound is `3/4<1`; its transverse
radius is at most `3r/4`.

The conical fold is the identity on one side of `r=z/2` and the orthogonal
reflection on the other, folded into the fixed side. On the stated sector
its image radius lies in `[0,r]`. Independent exact computation reproduces
the seven-label benchmark’s 11 tight and 10 strict pairs, paired determinant
`-64/125`, and displacement determinant `-64/125`. Hence its paired affine
rank is six and its displacement rank is three. This benchmark excludes the
specified direct rank and scalar-defect criteria, but does not exclude all
finite compositions of prior classes.

## Independent exact evidence and trust boundary

`independent_check.py` imports no target module. It uses a univariate
coefficient expansion rather than the author’s ten-variable sparse
polynomial implementation. On a fresh global linear meridian contraction it
checks 378 physical pairs and 1,134 coefficient/monotonicity controls. It
recomputes the rank-six determinant by the permutation formula rather than
Gaussian elimination, and pins all seven reviewed files.

Reproduce with:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

The checker guarantees packet provenance, exact finite pair polynomials,
whole-time monotonicity of the fresh fixture, and the benchmark ranks. The
universal geometric argument, support-closure passage, sampled-density
coupling, Gaussian marginal cancellation, and ball-volume transfer remain
independently reviewed written mathematics and primary-source inputs, not
proof-assistant output. No Gaussian quadrature or sampled-sign inference is
used.
