# A sharp neighborhood for the path formula for equal-ball unions

All balls in this note are closed Euclidean balls of the same radius
`R > 0`. The ambient dimension is `d >= 2`. Write `kappa_m` for the volume
of the unit ball in dimension `m`. Centers are labelled; their order below
is the order of a fixed reference configuration, not a sorting of perturbed
coordinates.

## 1. Statement, including the sharp radius

Fix an integer `N>=1`, distinct real numbers `a_1 < ... < a_N`, reference centers
`c_i = a_i e_1`, and gaps `g_i = a_(i+1)-a_i`. For positive `u,v` put

```
                 { uv/(4R),       if max(u,v) <= 2R,
theta_R(u,v) =    {
                 { (u+v)/2 - R,   if max(u,v) > 2R.
```

For `N >= 3`, set

```
tau = min_{2 <= j <= N-1} theta_R(g_(j-1), g_j).
```

For `N <= 2`, set `tau = +infinity`. Define the saturated two-ball increment

```
Phi_(d,R)(s) = kappa_(d-1) integral_0^min(s,2R)
                                  (R^2-t^2/4)^((d-1)/2) dt,   s >= 0.
```

In particular `Phi(0)=0`, `Phi(s)=kappa_d R^d` for `s >= 2R`, and
`Phi` is strictly increasing below `2R`.

**Theorem.** If `max_i ||p_i-c_i|| <= tau`, then

```
Vol_d(union_i B(p_i,R))
    = N kappa_d R^d - sum_{i=1}^{N-1} Vol_d(B(p_i,R) intersect B(p_(i+1),R))
    = kappa_d R^d + sum_{i=1}^{N-1} Phi_(d,R)(||p_(i+1)-p_i||).       (1)
```

If the displacement bound is strictly below `tau`, every point belongs to
an interval of labels: for every `i<j<k`,

```
B(p_i,R) intersect B(p_k,R) is contained in B(p_j,R).                 (2)
```

The radius `tau` in (1) is optimal for this fixed reference configuration
in the maximum individual Euclidean displacement norm. For every
`epsilon > tau` (when `N >= 3`), there are centers with
`max_i ||p_i-c_i|| < epsilon` for which the right side of (1) is **strictly
larger** than the union volume. This is a failure of the path formula, not
a counterexample to Kneser--Poulsen.

Formula (1) includes tangent adjacent pairs and changes in the overlap
graph. It asserts continuity at the closed radius `tau`, not analyticity
in every direction there. The set containment (2) can fail on a set of
zero volume at `tau`; this boundary distinction is necessary.

## 2. The geometric bridge: a robust three-ball lens

Translate three reference centers to `-u e_1, 0, v e_1`, with `u,v>0`.
Suppose that each actual center is at distance at most `epsilon` from its
reference center. A point in both outer balls lies in

```
L = B(-u e_1, R+epsilon) intersect B(v e_1, R+epsilon).
```

Put `r=R+epsilon`, `a=(u+v)/2`, and `m=(v-u)/2`. The lens is empty if
`r<a`. Otherwise, its exact maximum distance from the middle reference
center is

```
max_{x in L} ||x|| = sqrt(r^2-uv).                                  (3)
```

To prove (3), write `x=(m+z)e_1+w` with `w` perpendicular to `e_1`.
The two ball inequalities give

```
||w||^2 <= r^2-(a+|z|)^2.
||x||^2 <= r^2-a^2+m^2+2mz-2a|z| <= r^2-uv.
```

Here `|m|<a`. Equality is attained at
`x=m e_1+sqrt(r^2-a^2)e_2`, including the degenerate lens `r=a`.
This is why the sharpness statement uses `d>=2`.

Every middle ball with center within `epsilon` of zero contains `L` if

```
sqrt((R+epsilon)^2-uv) + epsilon <= R.                              (4)
```

When `epsilon <= R`, (4) is equivalent to `4R epsilon <= uv`.

If `max(u,v)<=2R`, let `b=uv/(4R)`. Then `b<=R` and

```
b - ((u+v)/2-R) = (2R-u)(2R-v)/(4R) >= 0.
```

Thus for `epsilon<=b` the lens is either empty or satisfies (4).
For `epsilon>b`, it is nonempty and can escape the middle ball.

If `max(u,v)>2R`, the lens remains empty for
`epsilon<(u+v)/2-R`. At this threshold its single point has distance
`|v-u|/2` from zero, and

```
|v-u|/2 + ((u+v)/2-R) = max(u,v)-R > R.
```

Consequently a missing middle label can appear immediately when the
outer lens is born. These are exactly the two cases defining `theta_R`.

The function `theta_R(u,v)` is increasing in either argument. In the
first region its partial derivatives are `v/(4R)` and `u/(4R)`; in the
second they are `1/2`. The formulas agree at the interface when the other
argument is at most `2R`. For any `i<j<k`,

```
a_j-a_i >= g_(j-1),     a_k-a_j >= g_j.
```

Hence the minimum robust threshold over all triples is attained among
the consecutive triples used in `tau`. This proves (2) for displacement
strictly below `tau`.

An elementary, sometimes convenient bound follows without (3). If
`epsilon<=R` and

```
4R epsilon <= min_j g_(j-1)g_j,
```

then (2) holds, including equality. Indeed, for
`lambda=(a_j-a_i)/(a_k-a_i)`, the exact identity

```
||x-c_j||^2 = (1-lambda)||x-c_i||^2 + lambda||x-c_k||^2
             - (a_j-a_i)(a_k-a_j)
```

bounds the right side by `(R+epsilon)^2-4R epsilon=(R-epsilon)^2`.
The triangle inequality finishes the containment. In particular the
uniform bound `epsilon <= min(R, gamma^2/(4R))`, with
`gamma=min_i g_i`, suffices. The exact `tau` also handles large gaps and
is the sharper configuration-specific answer.

## 3. Pointwise counting and the volume formula

For arbitrary measurable sets `A_1,...,A_N`, and a point `x`, let `r(x)`
be the number of nonempty runs of consecutive labels in
`{i:x in A_i}`. Direct counting gives

```
sum_i 1_(A_i)(x) - sum_i 1_(A_i intersect A_(i+1))(x) = r(x).        (5)
```

Thus the right side of the first line of (1) always overestimates union
volume, with excess

```
integral (r(x)-1) 1_(union A_i)(x) dx.                              (6)
```

Under (2), `r(x)` is either zero or one, so the excess vanishes. This
proves the first equality in the open tube.

For two radius-`R` balls at distance `s<=2R`, bisect their lens by its
perpendicular bisector. Two spherical caps give

```
Vol_d(B(p,R) intersect B(q,R))
    = 2 kappa_(d-1) integral_(s/2)^R (R^2-t^2)^((d-1)/2) dt.
```

Subtracting this from one ball volume and substituting `t -> t/2`
gives `Phi(s)`. At `s>=2R` the intersection has zero volume. The second
equality in (1) follows.

To include a configuration on the closed tube boundary, replace its
displacement vectors by `alpha(p_i-c_i)` and let `alpha` increase to one.
For `alpha<1` the formula is proved. Ball indicators converge pointwise
off finitely many limiting spheres. Those spheres have zero `d`-volume,
and all the balls lie in a common bounded set. Dominated convergence
therefore proves continuity of the union and each pair intersection.
This proves (1) at `tau`, even in the exceptional tangent case where
(2) fails pointwise.

## 4. Sharpness for every reference configuration

Choose a consecutive triple attaining `tau`, translate its middle center
to zero, and denote its gaps by `u,v`. Let `epsilon>tau`. Choose
`eta` strictly between `tau` and `epsilon`. Put

```
r = R+eta,   a=(u+v)/2,   m=(v-u)/2,
h = sqrt(r^2-a^2),       x=m e_1+h e_2,       M=||x||.
```

The case analysis in Section 2 shows that `h>0`, `M>0`, and `M+eta>R`.
For the two outer reference centers `c_-=-u e_1`, `c_+=v e_1`, set

```
p_- = c_- + (eta/r)(x-c_-),
p_+ = c_+ + (eta/r)(x-c_+),
p_0 = -eta x/M.
```

Each displacement has norm exactly `eta`. Also

```
||x-p_-|| = ||x-p_+|| = R,        ||x-p_0|| = M+eta > R.
```

Moving `x` a sufficiently small distance in direction `-e_2` strictly
decreases its squared distance to both outer actual centers: their
vertical difference from `x` is `Rh/r>0`. Its distance from `p_0`
remains greater than `R`. An open ball of points therefore lies in both
outer balls and outside the middle one. Leave all other centers at their
reference positions. Those extra balls cannot fill the missing label in
the index sequence. On this open set there are at least two runs, so
(6) is strictly positive. This proves optimality for the volume identity.

For three equally spaced centers with spacing `gamma<=2R`, the sharp
radius is exactly `gamma^2/(4R)`. Thus the constant `1/4` in the simpler
small-gap bound cannot be improved. The checker gives exact rational
witnesses on and beyond this boundary, as well as the long-gap boundary.

## 5. Consequences: contractions and the transverse Hessian

If two configurations `p,q` lie in the same closed tube of radius `tau`,
and only their **adjacent** distances satisfy

```
||q_(i+1)-q_i|| <= ||p_(i+1)-p_i||       for i=1,...,N-1,
```

then (1) gives `Vol(union B(q_i,R)) <= Vol(union B(p_i,R))`.
No motion between the configurations is required. Equality holds
exactly when

```
min(||q_(i+1)-q_i||,2R) = min(||p_(i+1)-p_i||,2R)
```

for every adjacent pair. In particular every full pairwise contraction
whose endpoints both lie in this tube satisfies the union inequality.
This is a local statement for fixed `R`; the tube generally shrinks as
`R` grows. It does not prove unrestricted Kneser--Poulsen.

For the Hessian, fix the axial coordinates and write
`p_i=(a_i,y_i)`, `y_i in R^(d-1)`. Put
`rho_i=sqrt(R^2-g_i^2/4)` for the gaps `g_i<2R`. The exact formula gives,
near `y=0`,

```
V(y) = V(0) + (kappa_(d-1)/2) sum_{i:g_i<2R}
                    (rho_i^(d-1)/g_i) ||y_(i+1)-y_i||^2
             + O(||y||^4).                                        (7)
```

Indeed the perturbed adjacent distance is
`sqrt(g_i^2+||y_(i+1)-y_i||^2)`, and
`Phi'(g_i)=kappa_(d-1)rho_i^(d-1)`. For `g_i>=2R` the corresponding
summand stays saturated and is exactly constant, even when `g_i=2R`.
The remaining finitely many summands are analytic functions of squared
transverse differences. Thus `V` is real analytic in these transverse
variables, every odd total Taylor degree vanishes, and

```
D^2 V(0)[b,b] = kappa_(d-1) sum_{i:g_i<2R}
                         (rho_i^(d-1)/g_i) ||b_(i+1)-b_i||^2.        (8)
```

The kernel consists exactly of transverse vector fields constant on each
component of the path retaining the gaps below `2R`. No mixed monomial
between distinct edge-difference variables occurs in the exact formula.

For `d=2`, `kappa_1=2`, so (7) agrees with the reviewed planar
coefficient. For `d=3`, the elementary exact increment is
`Phi(s)=pi(R^2 s-s^3/12)` below `2R`; this independently checks (7).
The all-dimensional coefficient is exactly the one proposed in item 3
of the graph review identified in README.md.

## 6. Scope and proof trust

The proof uses the Euclidean squared-norm identity, a two-ball lens
calculation, finite pointwise counting, cap integration, and dominated
convergence. No conjecture, solver, enumeration completeness assumption,
numerical approximation, or external dataset is a premise. The Python
program checks exact finite fixtures and independently compares cap
integration with the proposed increment in odd dimensions; it is not a
formal proof of the universal theorem. No independent review of this new
theorem is claimed. Background inclusion-exclusion methods for ball
unions are classical; see the specific literature comparison in README.md.
