# Independent review: convex normal-ray contractions

## Verdict

**Accept for correctness in the stated scope; novelty remains uncertain.**  At
source commit `15808c71e5da96669aefdc8736bc721f8e5c6521`, let `C` be a nonempty
closed convex subset of `R^n`, let `rho:[0,infinity)->[0,infinity)` be
1-Lipschitz with `rho(0)=0`, and set

```text
T(p+r u)=p+rho(r)u,  p=P_C(x),  r=dist(x,C),
```

with `T=I` on `C`.  The review accepts the claimed full Gaussian hinge
majorisation at every variance, the arbitrary-radius union and intersection
ball-volume inequalities, the parallel-body collar reflection, and the
closure under restriction, isometric conjugacy, and finite composition.
This verifies Discovery Net contribution
`bafkreifktf3exjltqmj5gnt5wvhpqe2za3cbb7rkdnlt3ha774is52k2j4` at height
6331.

The result is a substantial positive class but does **not** settle unrestricted
dimension-three Gaussian-convolution majorisation.  Nor does this review
establish historical priority for the convex-core extension.

## Convex projection and the lift

For `x=p+ru` and `y=q+sv`, the metric-projection variational inequality gives

```text
alpha=(p-q).u >= 0,  beta=-(p-q).v >= 0,  c=u.v <= 1.
```

These signs remain correct when either point lies in `C` after taking its
radius and normal to be zero.  They require neither a smooth boundary nor a
full-dimensional core.  Projection is unique and 1-Lipschitz for every
nonempty closed convex set in finite-dimensional Euclidean space.

Writing `R=rho(r)`, `S=rho(s)` and
`A_t(r)=(1-t)r+tR`, direct expansion of

```text
F_t(x)=(p+A_t(r)u, sqrt(t(1-t))(r-R))
```

reproduces exactly

```text
|F_t(x)-F_t(y)|^2
 = |p-q|^2 + 2A_t(r)alpha + 2A_t(s)beta
   +(1-t)(r-s)^2 + t(R-S)^2
   +2A_t(r)A_t(s)(1-c).
```

Its derivative is a sum of nonpositive terms because `0<=R<=r`,
`0<=S<=s`, `|R-S|<=|r-s|`, and the three geometric coefficients above are
nonnegative.  Thus every pairwise distance is nonincreasing.  At `t=0` and
`t=1` the endpoints are `(x,0)` and `(Tx,0)`, respectively, so `T` is also
1-Lipschitz.

After `t=sin(theta)^2`, every fixed labeled trajectory is analytic in
`theta`.  Joint continuity in the label also holds at `C`: the horizontal
displacement from `x` is at most `r`, the extra coordinate is at most `r/2`,
and `r=dist(x,C)` tends to zero.  This closes the regularity boundary needed
by both transfer theorems.

## Gaussian transfer

Pad the lift by one zero coordinate.  It is then a continuous contraction in
`R^(n+2)` whose endpoints lie in the original copy of `R^n`.  Theorem
1.4(i)(a) of
[Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2)
supplies a coupling under which the sampled source density is no larger than
the sampled target density.  The theorem is stated for an arbitrary
probability measure on the contraction domain and assumes only continuity of
the contracting homotopy for this part.

If the endpoint densities are `f(x) gamma_(2,s)(z)` and
`g(x) gamma_(2,s)(z)`, then with `X` of density `f`, independent
`Z~N(0,sI_2)`, and `c_s=(2 pi s)^(-1)`,

```text
P[f(X) gamma_(2,s)(Z)>h c_s]
 = integral (f-h)_+.
```

Indeed `exp(-|Z|^2/(2s))` is uniform on `[0,1]`; conditioning on `X=x`
gives `(1-h/f(x))_+`.  Applying the sampled-density order at threshold
`h c_s` therefore has exactly the direction claimed in the source.  This is
the essential two-auxiliary-coordinate cancellation; it is not a consequence
of 1-Lipschitzness alone.

## Ball-volume transfer and collisions

Reverse the analytic lift.  It is an expansion from the target centers to
the source centers in `R^(n+2)`.  Theorem 1 of
[Bezdek--Connelly, arXiv:math/0108098](https://arxiv.org/pdf/math/0108098)
then gives, in the endpoint `R^n`, increasing union volume and decreasing
intersection volume along that expansion, with arbitrary individual radii.
This is precisely the source theorem's required orientation.

Coincident labels cause no hidden gap.  Repeated source centers can first be
merged using the largest radius for a union and the smallest for an
intersection.  For the remaining finite set, replace `rho` by
`rho_e=(1-e)rho+e r`.  When `e>0`, every noncore target stays strictly on its
normal ray, so targets on different projection fibres cannot coincide;
different directions on one fibre cannot coincide either.  On the same ray,
the collision equation is the nonzero affine equation

```text
(rho(r)-rho(s)) + e[(r-s)-(rho(r)-rho(s))] = 0,
```

and excludes at most one `e` per pair.  A generic sequence `e` tending to
zero avoids all collisions.  Finite ball volumes are continuous in their
centers and radii, so the limit proves the original statement, including
zero radii.  In fact the published theorem's proof also explicitly
piecewise-handles coincident trajectories; the perturbation gives a clean
independent route through that boundary.

## Parallel-body collar

Let `K=C+aB`.  If `x=p+ru` with `r>a`, then `p+au` lies in `K`, while the
1-Lipschitz property of `dist(.,C)` gives

```text
|x-k| >= dist(x,C)-dist(k,C) >= r-a   for every k in K.
```

Hence `P_K(x)=p+au`.  The triangular profile in the source fixes `r<=a`,
maps `a<=r<=2a` to `2a-r`, and maps larger radii to zero.  Therefore on
`C+2aB=K+aB` it is exactly `2P_K-I`, including both boundary levels.  The
argument works unchanged for unbounded, lower-dimensional, and nonsmooth
convex cores.

## Independent executable evidence

The target checker was replayed under normal and optimized Python, its output
matched `convex_core_expected.json`, and all source manifest hashes passed.
The independent checker imports none of the target code.  It pins the three
material target files, uses exact rational arithmetic on a box, segment,
affine plane, and singleton, and checks the lifted coordinates directly for
five profiles and six times.  It separately checks the collar formula, the
Gaussian cancellation, and the affine collision equation, and rejects a
mutation of the angular coefficient.

Reproduce from this directory with Python 3.10 or later:

```sh
python3 independent_check.py
python3 -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `CONVEX_NORMAL_RAY_INDEPENDENT_ACCEPT`.

## Trust and scope

The executable evidence guarantees the pinned source bytes and its stated
finite exact controls.  The universal projection argument, continuity at the
core, stochastic-order transfer, limiting argument for colliding labels, and
parallel-body projection identity remain written mathematics and were
checked directly above.  The Aishwarya--Li coupling theorem and the
Bezdek--Connelly volume theorem remain external published dependencies, not
reproved results.

The contribution's novelty claim is appropriately provisional.  The review
confirms that the cited older lift does not by itself state the convex
normal-bundle class, but it does not certify an exhaustive literature search.
No claim is made here for signed profiles, base- or direction-dependent
profiles, nonconvex cores, arbitrary reflected projections, or the full
unrestricted dimension-three frontier.
