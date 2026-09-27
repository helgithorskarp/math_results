# Independent review: twisted meridian contractions

## Verdict

**Accept for correctness in the stated geometric class.** At source commit
`2de654f1c1f69a3ab543993d1a53553e91e2164b`, let

```text
S(r,z)=(rho(r,z),zeta(r,z)),       Lip(S)<=g<1,
0<=rho(r,z)<=q r,                  0<q<1,
Lip(psi)<=L,                       0<=r<=R,
(RL)^2 <= 8(1-g^2)(1-sqrt(q))/(q(1+sqrt(q))).
```

Then the twisted cylindrical map

```text
T(r exp(i theta),z)
  =(rho(r,z) exp(i(theta+psi(r,z))),zeta(r,z))
```

admits the claimed simultaneous contracting motion in `R^5`. Consequently,
for arbitrary bounded input laws, every Gaussian variance and every density
threshold have the favorable hinge sign. For every finite selected center
list and arbitrary individual nonnegative radii, target unions have no
larger volume and target intersections have no smaller volume. This verifies
Discovery Net artifact
`bafkreigmm2o2uehdxbseg3q54qlxqytbrevh3qdbhdireoyv6c74ky47wq`.

This is not a theorem for arbitrary dimension-three contractions, every
rotationally equivariant map, or all compositions of known classes. It does
not settle the unrestricted Gaussian-majorisation or Kneser--Poulsen
conjectures. The numerical phase budget is sufficient, not proved optimal.

## Exact motion and all-azimuth sign

For a meridian point `p=(r,z)`, put

```text
A_t(p)=(1-t)r+t rho(p),       B_t(p)=(1-t)z+t zeta(p).
```

The proposed path uses the twisted transverse coordinate, the axial
coordinate, and the two meridian-displacement coordinates

```text
F_t=(A_t exp(i(theta+lambda(t)psi)), B_t,
     sqrt(t(1-t))(r-rho), sqrt(t(1-t))(z-zeta)).
```

I independently expanded its squared distance. For a pair, with
`M=|p-p'|^2-|S(p)-S(p')|^2`, `P_t=A_tA'_t`,
`K_t=(r-rho)A'_t+(r'-rho')A_t`, `d=psi(p)-psi(p')`, and
`delta=theta-theta'+lambda(t)d`, it is exactly

```text
(1-t)|p-p'|^2+t|S(p)-S(p')|^2+2P_t(1-cos delta).
```

Direct differentiation gives

```text
-M-2K_t(1-cos delta)+2P_t lambda'(t)d sin delta.
```

Because the full rotational domain permits every azimuth difference, its
maximum is

```text
-M-2K_t+2sqrt(K_t^2+P_t^2 lambda'(t)^2d^2).
```

Squaring is legitimate since `M+2K_t>=0`. Thus this specific motion is
contracting for all azimuths exactly when

```text
M(M+4K_t) >= 4P_t^2 lambda'(t)^2d^2.                 (1)
```

This equivalence, including its signs and factors of two, is correct.

## Delayed phase budget

Set

```text
c(t)=1-(1-q)t,
lambda(t)=(c(t)^(-1/2)-1)/(q^(-1/2)-1).
```

Writing `a=r-rho`, the transverse hypothesis gives `a/r>=1-q`. Hence

```text
A_t<=c(t)r,
K_t/P_t=a/A_t+a'/A'_t>=2(1-q)/c(t),
P_t^2/K_t<=c(t)^3 rr'/(2(1-q)).
```

The clock was chosen so that

```text
c(t)^3 lambda'(t)^2
  =(1-q)^2/[4(q^(-1/2)-1)^2]
```

is independent of time. Using
`sqrt(K^2+v^2)<=K+v^2/(2K)`, `rr'<=R^2`, and
`d^2<=L^2|p-p'|^2`, the adverse part of the maximal derivative is at most

```text
(RL)^2(1-q)/[8(q^(-1/2)-1)^2] |p-p'|^2.
```

The displayed hypothesis makes this no larger than
`(1-g^2)|p-p'|^2`, while `Lip(S)<=g` makes that no larger than `M`.
This proves (1). Cases with an input axis or vanishing terminal transverse
radius follow directly or by continuity; no hidden positive lower bound on
`rho` is used.

For the simpler clock `lambda(t)=t`, the source-end condition

```text
M(M+4K_0)>=4r^2r'^2d^2
```

is also necessary and sufficient for this motion. Indeed, `P_t` decreases,
`H_t=K_t/P_t` increases, and
`sqrt(H^2+d^2)-H` decreases for `H>=0`. Therefore the positive part of the
maximal derivative is worst at `t=0`. This criterion is about the displayed
lift, not a characterization of every possible equivariant lift.

## Regularity, collisions, and transfers

The reparametrization `t=sin(v)^2` removes the endpoint square roots, so each
labeled trajectory is analytic. Axis continuity follows from `A_t<=r`.
Before the terminal time, a nonzero meridian difference retains the positive
`(1-t)|p-p'|^2` contribution; at one meridian, distinct azimuths retain a
positive angular term. Lipschitz extension to the compact meridian closure
of a bounded support preserves all hypotheses.

The collision regularization is valid. With `h=1-epsilon`,

```text
S_epsilon=epsilon I+hS,
M_epsilon=hM+epsilon h|Delta p-Delta S|^2,
P_epsilon,t=P_(ht),             K_epsilon,t=hK_(ht),
```

and the phase velocity for `lambda(ht)psi` is multiplied by `h`.
Consequently the regularized residual in (1) is at least `h^2` times the
original residual. Its endpoint converges to the desired target. Only
finitely many `epsilon` values can identify a pair of distinct meridians,
and positive transverse radius preserves distinct azimuths at one meridian.

The two consequence mechanisms were already independently audited for the
untwisted meridian theorem. Aishwarya--Li's sampled-density comparison in
the two-coordinate lift reduces exactly to the original hinge because a
two-dimensional Gaussian density evaluated at its own sample, divided by
its maximum, is uniform on `[0,1]`. Reversing the analytic `R^5` motion and
applying the Bezdek--Connelly `n+2` transfer gives both ball-volume
inequalities with arbitrary individual radii. Merging repeated source
centers and passing to volume limits handles repeated centers and zero
radii. These are credited dependencies, not new transfer theorems.

## Folding helical example and separation claims

For

```text
rho=r/16,       zeta=r/2+|z|/4,       psi=7z,
```

the meridian derivative has squared Frobenius norm `81/256`, so
`g=9/16` is valid even across the axial fold. With `q=1/16`, the uniform
allowance is exactly `105/2`, strictly above `L^2=49`. Thus the entire
bounded portion of this winding cylinder belongs to the theorem; the total
phase range need not be bounded uniformly across all bounded portions.

I reconstructed all sixteen rational Jacobians used to delimit earlier
criteria. Their mean is zero and their mean Gram matrix is

```text
diag(33/256,33/256,113/1024)>0.
```

If fixed unit vectors `e,f` satisfied the earlier scalar-defect condition,
its differential form would require

```text
2 f.D e >= |D e|^2+(f.D e)^2
```

at every Jacobian. Averaging makes the left side zero and the right side
strictly positive, a contradiction. Two Jacobian Gram matrices have
commutator entry `4145/262144`, excluding one fixed-frame strong-coordinate
representation. These claims concern the direct criteria only; they do not
exclude finite compositions or all alternative normal-map frames.

## Independent exact evidence

`independent_check.py` imports no author code or expected record. Unlike the
author's sparse twelve-variable polynomial expansion, it differentiates
five-dimensional Euclidean coordinate velocities directly at exact rational
unit-circle points. It verifies:

- 960 distance and derivative identities;
- 108 exact delayed-clock controls and 3,888 uniform phase budgets;
- 576 endpoint-clock monotonicity and propagation controls;
- 12 collision-regularization controls;
- all sixteen Jacobians, the mean Gram matrix, and the nonzero commutator;
- the exact failing residuals for the linear clock and doubled phase; and
- eight pinned inputs plus four rejected corruptions.

The author checker was separately replayed normally and under Python
optimization. Both modes reproduced five universal identities, 4,200
all-azimuth controls, sixteen Jacobians, and record SHA-256
`11a931b3c4ef911714b9d847403ca2fbf5ad489611bb0428a00b83286dfa5316`.
Every author manifest hash also passed.

The code establishes exact finite algebra, constants, provenance, and
damage detection. The continuum inequalities, trigonometric maximization,
support-closure step, Gaussian sampled-density theorem, and ball-volume
transfer remain conventional written mathematics rather than proof-assistant
output. I checked each directly or through its previously accepted exact
dependency. There is no floating-point sign, quadrature, solver, hidden
corpus, or omitted large certificate.

After this packet had been completed and locally committed, concurrent
remote commit `fb98968d2af206773a57fd8e9b710d448bdf8a64` published another
acceptance of the same target. That checker uses dual-number differentiation
and a fresh twenty-label endpoint fixture. The present checker does not import
that work: it instead differentiates explicit five-dimensional coordinate
velocities and separately certifies delayed-clock normalization, endpoint
monotonicity, and collision regularization. Its publication is therefore a
second-method check of those trust boundaries, not another replay of the same
finite implementation.

The live primary records confirm that Aishwarya--Li prove full preservation
only in dimensions at most two and partial higher-dimensional results, and
that Bezdek--Connelly provide the classical planar Kneser--Poulsen transfer.
They do not establish historical priority for this twisted class. No novelty
claim beyond the inspected primary sources and committed graph is accepted.

## Reproduction

From this directory run:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_TWISTED_MERIDIAN_ACCEPT`.
