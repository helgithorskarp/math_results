# Independent acceptance: arbitrary nonlinear parallel slices

## Target and verdict

- Discovery Net artifact:
  `bafkreia6xrsq7zfvdx3m6mlvi53u5vmha6fmggrwh3ndl5bed2bv6l7zlq`
- Exact reviewed source commit:
  `43c807f9ffe40fb40b7c2a44b8441cfd55324e84`
- Reviewed source:
  [`../gaussian_parallel_slice_contractions`](../gaussian_parallel_slice_contractions/)

**Accept with high confidence in the stated scope.**  Let `K` be a closed
convex subset of `R2`, let `I` be an interval, and let

```text
T(u,z)=(f(u,z),h(z)): K x I -> R2 x R
```

be 1-Lipschitz.  The proof correctly constructs a simultaneous continuous
contracting motion in `R5`, with both endpoints in the original `R3`.  It
follows that every bounded law on the prism has the Gaussian hinge comparison
at every positive variance and every nonnegative threshold.  Finite center
selections also have both arbitrary-individual-radius ball-volume signs.

The transverse map `f` may be genuinely nonlinear and nonsmooth.  The
whole-prism hypothesis, convexity of `K`, and the requirement that the last
target coordinate depend only on the source height are essential.  This is
not an acceptance of the unrestricted dimension-three problem or of a
finite-endpoint-only extension.  Historical priority remains uncertain.

## The partition lemma

Since `T` is short, `h` is 1-Lipschitz and hence absolutely continuous on
compact intervals.  Put

```text
omega(z)=sqrt(1-h'(z)^2),
A(z)=integral omega.
```

The new claim is the support-wide estimate

```text
|f(u,z)-f(v,w)|^2 <= |u-v|^2+|A(z)-A(w)|^2.       (1)
```

For a partition `w=z_0<...<z_N=z`, define

```text
ell_i=sqrt((Delta z_i)^2-(Delta h_i)^2),
L=sum ell_i.
```

When `L>0`, allocate the horizontal displacement along the segment from
`v` to `u` in the fractions `ell_i/L`.  Convexity of `K` keeps every
allocated point in the domain.  Applying the endpoint contraction to the
`i`th space-height step gives

```text
|Delta f_i|^2
 <= (ell_i/L)^2 |u-v|^2 + ell_i^2
 =  (ell_i/L)^2 (|u-v|^2+L^2).
```

The triangle inequality and `sum ell_i/L=1` therefore give the same bound
with `L` in place of `|A(z)-A(w)|`.  If `L=0`, every vertical step has zero
transverse change; one horizontal step and those zero-cost vertical steps
give the required estimate without division.

On equal dyadic partitions, `Delta h_i/Delta z_i` is the cell average of
`h'`.  These averages converge almost everywhere to `h'`, while the
integrands `sqrt(1-b_i^2)` lie in `[0,1]`.  Dominated convergence yields
`L -> integral omega`, proving (1).  This argument differentiates only the
scalar `h`; it assumes neither a derivative of `f` nor an affine completion.
The full prism and horizontal convexity are used exactly where claimed.

## Exact factorization and finite data

Estimate (1) implies that `A(z)=A(w)` forces `f(u,z)=f(u,w)` for each `u`.
Thus

```text
f(u,z)=G(u,A(z))
```

for a well-defined 1-Lipschitz map `G` on `K x A(I)`.  Conversely, the
absolutely continuous curve `z -> (A(z),h(z))` has unit speed almost
everywhere.  Its chord satisfies

```text
|Delta A|^2+|Delta h|^2 <= |Delta z|^2,
```

so every short `G` produces a short `T`.  The equivalence includes flat
`A` fibers and folds of `h`.

The prescribed-frame finite extension criterion also has the right
quantifiers and direction.  For consecutive source levels, Jensen's
inequality bounds the actual unused length by

```text
sqrt((Delta z)^2-(Delta t)^2).
```

Summing and applying (1) proves necessity of the pairwise transverse
budgets.  For sufficiency, piecewise-linear interpolation of the scalar
heights realizes those budgets exactly.  Kirszbraun--Valentine extends the
resulting finite short map `(u_i,a_i)->v_i` from `R3` to `R2`; composing it
with `(u,A(z))` supplies a whole-prism map.  This is a criterion in supplied
frames, not an all-frame classifier or a claim that arbitrary radicals are
decided by the rational checker.

## The `R5` motion

In `R2 x R x R2`, the first phase is

```text
Phi_t(u,z)=(sqrt(1-t)u, H_t(z), sqrt(t)f(u,z)),
H_t(z)=(1-t)z0+t h(z0)+integral q_t,
q_t=sqrt(1-t+t h'^2).
```

For a pair with different heights, write

```text
L_t=integral q_t,
C_t=integral omega^2/q_t,
Q=|Delta f|^2-|Delta u|^2.
```

For `t<1`, differentiation under the integral is justified because `q_t`
is bounded away from zero on compact time intervals.  The pair-square
derivative is exactly

```text
Q-L_t C_t.
```

Estimate (1) gives `Q<=(integral omega)^2`, and Cauchy--Schwarz gives
`(integral omega)^2<=L_t C_t`.  Hence every pair distance is nonincreasing.
Equal heights reduce directly to shortness of `f`, and continuity covers
`t=1`, including zero sets of `h'`.

At the first endpoint,

```text
H_1(z)=h(z0)+integral |h'|.
```

The map `H_1(z)->h(z)` is well defined and 1-Lipschitz: a flat `H_1` interval
has `h'=0` almost everywhere, while in general `|Delta h|<=|Delta H_1|`.
After an ambient quarter-turn exchanges the two transverse planes, the
standard one-dimensional leapfrog has squared pair distance

```text
(1-s)(Delta H_1)^2+s(Delta h)^2,
```

so the final fold is also contracting.  The quarter-turn itself is an
isometric phase.  These phases start at the source copy of `R3` and end at
the target copy of `R3`.

The time-regularity discussion is sufficient.  With `t=sin(theta)^2`,
`|partial_theta q|<=1`; dominated convergence supplies one-sided endpoint
derivatives even where `h'=0`.  Smooth clocks with zero endpoint derivative
join the phases into `C1` trajectories, with bounded speed on bounded source
sets and smooth interiors.  No regularity of `f` in its spatial variables is
needed for trajectory regularity.

## Gaussian and ball-volume transfers

Aishwarya--Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*](https://arxiv.org/html/2609.07041v2), Theorem 1.4(i)(a), applies
to the continuous contraction in `R5`.  Convolution of the endpoint measures
with the five-dimensional Gaussian gives densities
`f_j(x) gamma_s^(2)(y)`.  If `Y` has the two-dimensional Gaussian density
`gamma`, then `gamma(Y)/gamma(0)` is uniform on `[0,1]`.  Therefore

```text
Pr{f_j(X) gamma(Y) > gamma(0) a}
  = integral (f_j-a)_+.
```

The theorem's increasing coupling of sampled density values yields the
claimed three-dimensional hinge comparison.  This calculation is specific
to the two auxiliary Gaussian coordinates and has the correct direction.
Standard hinge representation then gives every defined convex internal
energy with `U(0)=0`.

Reversing the piecewise-smooth `R5` motion meets Bezdek--Connelly,
[*Pushing disks apart*](https://arxiv.org/pdf/math/0108098v1), Theorem 1,
and gives both union and intersection signs for arbitrary individual radii.
The perturbation `T_epsilon=(1-epsilon)T+epsilon Id` remains short and retains
the parallel-slice form.  It separates finitely many coincident target
centers except at finitely many parameter values, after which continuity
handles the limit.  Repeated source centers and zero radii are treated by
the stated merge and radius-limit arguments.

## Genuine nonlinear breadth

The displayed polynomial control is valid on the whole cube.  The squared
Frobenius norm of its `G` Jacobian is at most `3/8`, hence its operator norm
is below one.  Adding the scalar-height derivative yields the stated
`147/200<1` whole-map bound.  On each open height half, the first output
component has positive-definite Hessian, so the vector map cannot be affine
on any two-dimensional source plane, even after independent fixed endpoint
isometries.

The Hessian-rank argument against direct coordinatewise strong contraction
is also correct.  A scalar combination `alpha f_1+beta f_2+delta h` has
rank at most one only in the coefficient plane `beta=2alpha`.  Three
independent target coordinate functionals cannot all lie in that plane.
This separates direct representations, not arbitrary compositions or
historical provenance.

## Independent exact evidence

The author checker was replayed normally and under optimized Python.  Both
runs reproduce `NONLINEAR_PARALLEL_SLICE_EXACT_CONTROLS_PASS`, record digest
`6fd418efb87967baee6ee343e234e5ba04dc5a1999175626dd5d836937cc1945`,
and the full byte manifest.

[`independent_check.py`](independent_check.py) imports no target code and
pins three target files at the exact reviewed commit.  It uses the new
three-slope profile

```text
h' = 7/25, -20/29, 9/41,
omega = 24/25, 21/29, 40/41,
```

and the different nonlinear map

```text
G(x,y,a)=((x^2+y^2+a^2)/32, xy/32).
```

Its exact whole-domain Frobenius bound is
`507825299851/8143032960000<1`; the first scalar Hessian is positive definite
on every profile cell.  Across 63 rational sites the checker verifies 1,953
endpoint and transverse pairs, 2,997 allocated segments, 3,402 phase
derivative inequalities at the two exact regular boundary clocks, 9,765
fold controls, all 1,953 finite extension pairs, and 12 algebraic instances
of the two-Gaussian tail cancellation.  Normal and optimized runs match
[`EXPECTED.json`](EXPECTED.json), with exact-state digest
`d700a02638da84b751a63c49b634790359ed15e3fe6755c35c2f27002e2c5b57`.

## Trust boundary and limitations

The exact checkers guarantee their rational profiles, finite pair and
partition algebra, polynomial Lipschitz bounds, finite extension budgets,
phase/fold identities, rejection controls, and source provenance.  They do
not prove the continuum theorem by sampling.  The dyadic convergence,
Kirszbraun extension, time regularity, Gaussian coupling transfer, and
Bezdek--Connelly theorem are the hand-reviewed mathematical bridges above.

Acceptance removes transverse affinity for the parallel-slice class.  It
does not factor arbitrary `R3` contractions, remove the scalar-coordinate or
whole-prism premise, show that every finite contraction extends to this
class, optimize the motion dimension, or settle the full dimension-three
Gaussian-majorisation frontier.

## Reproduction

From this directory:

```sh
python3 -B independent_check.py > /tmp/parallel-slice-review2.json
cmp /tmp/parallel-slice-review2.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/parallel-slice-review2-opt.json
cmp /tmp/parallel-slice-review2-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_NONLINEAR_PARALLEL_SLICE_REVIEW_PASS`.
