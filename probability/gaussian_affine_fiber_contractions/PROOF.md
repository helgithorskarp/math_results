# Parallel affine fibers: a five-dimensional contracting motion

27 September 2026. Complete author proof; independent review and historical
priority are pending. The unrestricted dimension-three Gaussian-majorisation
question remains open.

## 1. The class and theorem

Use independent fixed orthonormal frames at the two endpoints. Let
`K` be a nonempty closed subset of `R2`; it need not be convex. Suppose

```text
T(u,z)=(H(u), a(u) z+b(u)),       u in K, z in R,            (1)
```

is 1-Lipschitz. Thus complete parallel source lines are mapped affinely
into parallel target lines, possibly to points. No affinity, injectivity,
differentiability or symmetry is assumed for the base functions `H` and `b`.

**Theorem 1.** Every map (1) has one simultaneous continuous contracting
motion in `R5`, with the two endpoints in copies of `R3`. The motion can
have `C1` trajectories, smooth phase interiors, and speed bounded on every
bounded set of source labels. Consequently:

1. For every bounded probability law `mu` on `K x R`, every `s>0` and every
   `h>=0`, writing `f=mu*gamma_s^(3)` and `g=T#mu*gamma_s^(3)`,

   ```text
   integral (f-h)_+ <= integral (g-h)_+.                    (2)
   ```

   Equivalently all defined convex internal energies with `U(0)=0` compare
   in the favorable direction, with the usual extended-integral convention.
2. For every finite selection `p_i` from the domain, `q_i=T(p_i)`, and every
   choice of individual radii `r_i>=0`,

   ```text
   Vol3(union B(q_i,r_i)) <= Vol3(union B(p_i,r_i)),
   Vol3(intersection B(q_i,r_i)) >= Vol3(intersection B(p_i,r_i)).  (3)
   ```

The new ingredient is the motion below, not the Gaussian or ball-volume
transfer theorems. The complete-line assumption in (1) is used to identify
the exact allowable class. Alternatively, the normalized short-profile
condition (5) below can be assumed directly for a restriction of this map.

## 2. Exact characterization by a short planar profile

For `u,v in K`, compare `(u,z)` and `(v,z)` as `|z|` tends to infinity.
The input distance stays `|u-v|`, so (1) forces `a(u)=a(v)`. Write the
common value as `a`. On each individual line, shortness gives `|a|<=1`.

When `|a|<1`, put `c=sqrt(1-a^2)` and `g(u)=b(u)/c`. For any pair of
base points and any real vertical difference `q=z-w`, endpoint shortness is

```text
|Delta H|^2+(a q+Delta b)^2 <= |Delta u|^2+q^2.             (4)
```

The maximum over `q` of `(a q+Delta b)^2-q^2` is
`(Delta b)^2/(1-a^2)`, including `a=0`. Hence (4) for all `q` is equivalent
to

```text
G(u)=(H(u),g(u)): K -> R3 is 1-Lipschitz.                 (5)
```

In particular **every** short planar-to-spatial profile `G` and every
`|a|<1` yield a member

```text
T(u,z)=(H(u), a z+c g(u)).                                (6)
```

When `|a|=1`, the coefficient of `q` in (4) forces `b` to be constant;
then (1) is exactly a planar contraction `H` times a line isometry, followed
by a translation. This also covers a one-point base.

The elementary identity behind the characterization is

```text
|Delta u|^2+q^2-|Delta H|^2-(a q+c Delta g)^2
 = L+(c q-a Delta g)^2,
L=|Delta u|^2-|Delta H|^2-(Delta g)^2 >= 0.                (7)
```

Thus the full endpoint loss separates into the short-profile loss and one
square. The construction retains those two losses with different clocks.

## 3. The motion for 0<a<1

Negative `a` is reduced to positive `a` by reversing the source line
coordinate, an endpoint isometry. In `R2 x R2 x R`, put

```text
d_t=a^2+t c^2,             r_t=t/d_t,
Phi_t(u,z)=(sqrt(1-t)u, sqrt(t)H(u),
                         (a z+t c g(u))/sqrt(d_t)),
0<=t<=1.                                                   (8)
```

Here `d_t>=a^2>0`, `Phi_0=(u,0,z)` and
`Phi_1=(0,H(u),a z+c g(u))`. An ambient quarter-turn in the two transverse
planes places the final configuration in the initial copy of `R3`.

For a fixed pair of labels let `q=Delta z`, `v=Delta g` and `L` be as in
(7). Direct expansion gives the exact identity

```text
|Delta Phi_t|^2
 = |Delta u|^2+q^2 - t L - r_t(c q-a v)^2.                 (9)
```

Both subtracted quantities are nonnegative. Moreover

```text
r'_t = a^2/d_t^2 > 0,
d/dt |Delta Phi_t|^2 = -L-a^2(c q-a v)^2/d_t^2 <= 0.     (10)
```

This proves simultaneous contraction for all labels, without choosing a
finite support or differentiating `H` or `g`. At `t=1`, (9) reduces to (7).
This is not the ordinary linear interpolation of squared endpoint distances:
the coefficient of the square in (9) is the rational clock `r_t`.

For time regularity set `t=sin(theta)^2`, `0<=theta<=pi/2`.
All trajectory coordinates are smooth in `theta`, including its endpoints,
because `d_t>=a^2`. On a bounded set of source labels, `H,g,z` are bounded,
so their time derivatives are uniformly bounded for the fixed `a>0`.
Parameterize the transverse quarter-turn smoothly. Composing each phase
with a smooth increasing clock whose derivative vanishes at both ends makes
the concatenated motion `C1`, with smooth phase interiors. There is no
uniform speed claim as `a` tends to zero; that value has a separate motion.
Reflections and translations required by the endpoint frames can be joined
by ambient isometries in `R5`. A reflection of the occupied `R3` can be
extended with a reflection of an unused axis, hence lies in an ambient
orientation-preserving isometry connected to the identity.

## 4. Zero and saturated slopes

If `a=0`, (6) is independent of `z`. First contract `z` to zero, leaving
`u` fixed. Then use the classical planar-to-spatial leapfrog

```text
(sqrt(1-t)u, sqrt(t)G(u)) in R2 x R3.                     (11)
```

Its squared pair distances are `(1-t)|Delta u|^2+t|Delta G|^2` and decrease
by (5). Append an endpoint isometry. The first phase and sine-square clock
for (11) meet the same regularity requirements. This branch is an already
known planar-source comparison, not the new geometric case.

If `a=1`, drop the common translation temporarily. The motion

```text
(sqrt(1-t)u, sqrt(t)H(u),z) in R2 x R2 x R                (12)
```

contracts, again followed by an isometry and translation. The case `a=-1`
adds a line reflection. These are the familiar planar-product cases.
Together the three branches prove the motion assertion of Theorem 1.

## 5. The credited Gaussian and volume transfers

[Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
Theorem 1.4(i)(a), provides an increasing coupling of sampled Gaussian
density values under a continuous contraction in `R5`. At the two endpoints
the densities are, up to isometries, `f(x)gamma_s^(2)(y)` and
`g(x)gamma_s^(2)(y)`.

For `Y` with density `gamma=gamma_s^(2)`, the ratio
`gamma(Y)/gamma(0)` is uniform on `[0,1]`. If independently `X` has density
`f`, then

```text
Pr{ f(X) gamma(Y) > h gamma(0) }
 = integral f(x) (1-h/f(x))_+ dx
 = integral (f-h)_+ dx.                                  (13)
```

The sampled-density comparison therefore proves (2). Hinge representation
of convex energies gives the internal-energy formulation. This two-coordinate
transfer is stated explicitly after Theorem 1.5 in the named paper and was
already used in the team's accepted parallel-slice theorem; it is not new.

Reverse the piecewise-smooth `R5` motion and apply
[Bezdek--Connelly, *Pushing disks apart*](https://arxiv.org/pdf/math/0108098v1),
Theorem 1, with `n=3`, to obtain both inequalities (3). Their definition of
piecewise smooth requires smooth phase interiors, which the construction
has. It imposes no equal-radius restriction.

For completeness, finite collisions can be removed without leaving the
class. On the original domain set `T_epsilon=(1-epsilon)T+epsilon Id`.
It is short and still of form (1), with common slope
`(1-epsilon)a+epsilon`. For finitely many distinct source labels, their target
differences are nonzero except at finitely many positive `epsilon` values.
Use a sequence avoiding those values and let `epsilon` tend to zero.
Lebesgue volume of each finite union or intersection is continuous in its
centers and radii, by almost-everywhere convergence away from the finite
collection of sphere boundaries and bounded convergence on a containing
ball. Repeated source centers can be merged using the largest radius for
unions and the smallest for intersections. Zero radii follow by a radius
limit. No positive separation, minimum atom mass, or positive loss is needed.

## 6. Exact extension criterion for supplied finite data

Fix the two coordinate frames and a scalar `a` with `|a|<1`. Given finitely
many pairs

```text
p_i=(u_i,z_i), q_i=(v_i,w_i),
D_ij=|p_i-p_j|^2-|q_i-q_j|^2,
```

there is a global map of form (6), with this `a`, interpolating all pairs
if and only if for every pair

```text
(1-a^2)(|Delta u|^2-|Delta v|^2)
                  >= (Delta w-a Delta z)^2.              (14)
```

**Necessity** follows by evaluating the short profile (5) at
`G(u_i)=(v_i,(w_i-a z_i)/sqrt(1-a^2))`.
**Sufficiency:** (14) makes this finite profile well defined and short;
in particular coincident `u_i` force equal profile values. The classical
Kirszbraun--Valentine extension theorem extends it from a subset of `R2`
to all of `R2`, with values in `R3`. Formula (6) supplies the required global
map. A version with arbitrary Hilbert source and target is also obtained by
zero-padding and orthogonal projection from the Hilbert-space theorem.

Equivalently, (14) is

```text
(Delta z-a Delta w)^2 <= (1-a^2)D_ij,                    (15)
```

or the scalar quadratic constraint

```text
[(Delta w)^2+D_ij]a^2 - 2 Delta z Delta w a
                              +(Delta z)^2-D_ij <= 0.    (16)
```

Thus when the data are a contraction, allowable nonsaturated slopes are
the intersection of the finitely many closed quadratic sublevel intervals
with `(-1,1)`. Degenerate constant/linear polynomials are read literally.
This is a mathematical interval characterization, not an implemented
algebraic-root or all-frame search.

For `a=1` or `a=-1`, the exact conditions are that all `w_i-a z_i` be the
same constant and that `u_i -> v_i` be a well-defined short planar map.
Kirszbraun then gives the global extension.

The supplied checker tests (14) at any supplied rational `a`, including
`a=0`, and handles the saturated slopes separately. It never needs a square
root for this decision. Failed membership at the supplied frames and slope
does not refute Gaussian majorisation or rule out another motion. R4 retains
sharp all-frame/extremal-motion ownership; this is a positive-class consumer.

## 7. Breadth beyond the accepted parallel-slice representation

On `K=[-1,1]^2`, with `u=(x,y)`, set

```text
H(u)=((x^2-y^2)/8, xy/4),    g(u)=(x^2+y^2)/8,
a=3/5, c=4/5,
T(x,y,z)=((x^2-y^2)/8, xy/4, 3z/5+(x^2+y^2)/10).        (17)
```

For the profile `G=(H,g)`, `||DG||_F^2=3(x^2+y^2)/16<=3/8`.
The convex square and the derivative bound imply that `G` is short. Also
`||DT||_F^2<=69/100<1` on `K x R`. These are whole-domain estimates;
the selected rational labels only corroborate them.

**No fixed parallel-slice representation.** Suppose a nonzero target linear
functional of (17) were a function of one source affine coordinate on an
open subset. Such a scalar function would have the form

```text
F=alpha (x^2-y^2)/8+beta xy/4
                         +gamma[3z/5+(x^2+y^2)/10].       (18)
```

If `gamma!=0`, `partial_z F=3 gamma/5` is a nonzero constant. Dependence
on one affine coordinate then forces that coordinate to have nonzero
z-component and its univariate function to be affine locally. But the
three quadratic forms `x^2-y^2`, `2xy`, `x^2+y^2` are linearly independent,
so the Hessian in (18) cannot vanish when `gamma!=0`.

If `gamma=0`, its `x,y` Hessian is

```text
(1/4) [[alpha,beta],[beta,-alpha]],
```

with determinant `-(alpha^2+beta^2)/16<0` for nonzero `(alpha,beta)`.
It has rank two, whereas a smooth function of one affine coordinate has
Hessian rank at most one. The same conclusion holds if the univariate
function is initially only assumed Lipschitz, since restricting the smooth
polynomial along a transverse line supplies a smooth local representative.

Therefore the map does not belong to the accepted parallel-slice class
`T(u,z)=(f(u,z),h(z))` in **any** independent fixed endpoint frames, even
locally on an open subset. In particular it is not a direct coordinatewise
strong contraction in any such frames. This separates direct full-map
representations, not arbitrary compositions, all historical positive
classes, or every finite restriction of (17).

The seven labels `0, +/-e1, +/-e2, e1+e2, e3` have paired affine rank six:
the functions `x,y,z,x^2-y^2,xy,x^2+y^2` are independent on those labels
after subtraction of the zero row. The checker computes the exact nonzero
determinant. Hence the entire class is not contained in the older paired
affine-rank-at-most-five sufficient condition. The strict Jacobian bound
also gives strict contraction of every distinct pair in this calibration.
Neither finite rank six nor failure of a direct representation certifies
historical priority or absence of another older continuous motion.

## 8. Scope and evidence

The new positive class is the full affine-parallel-fiber class, not a
particular polynomial example or a new angular/twist schedule. It allows
nonlinear base geometry on arbitrary transverse sets, arbitrary bounded
laws and all variances and radii. It complements the reviewed nonlinear
parallel-slice class; no containment in the reverse direction is claimed.

The proof uses complete fibers to obtain the common slope and short profile.
Contraction verified only at finitely many spatial samples does not imply
that premise; the exact finite criterion (14) is what supplies an extension.
Nonlinear dependence on the fiber coordinate, variable target line directions,
arbitrary frame optimization and unrestricted R3 maps remain outside the
claim. There is no assertion that an arbitrary planar-to-spatial contraction
has an R4 motion. Formula (8) handles the fiber coordinate jointly, avoiding
the extra dimension that a simple independent product of motions would use.

The exact program verifies polynomial identities (9), (10), (14)--(16),
rational-profile pair controls, endpoint and clock identities, the finite
consumer, degeneracies, and the calibration rank and derivative bounds.
It does not prove the universal analytic transfers by sampling and is not a
proof-assistant formalization or an independent review. Primary literature,
team dependencies and the unresolved priority question are in [SOURCES.md](SOURCES.md).
