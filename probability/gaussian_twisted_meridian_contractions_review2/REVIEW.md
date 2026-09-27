# Independent acceptance: twisted meridian contractions

## Verdict

**Accept for correctness in the stated scope.** In cylindrical coordinates,
let the meridian map `S=(rho,zeta)` have Lipschitz constant at most `g<1`,
let `0<=rho(r,z)<=q r` with `0<q<1`, and let a real phase lift `psi` have
Lipschitz constant at most `L` on meridians with `0<=r<=R`. If

```text
(RL)^2 <= 8(1-g^2)(1-sqrt(q))/(q(1+sqrt(q))),
```

then

```text
T(r exp(i theta),z)
  =(rho(r,z) exp(i(theta+psi(r,z))),zeta(r,z))
```

admits a simultaneous contracting motion in `R5`. Consequently, for every
bounded input law supported on the full rotational domain and every Gaussian
variance, the target convolution majorises the source. For every finite
selected center list and arbitrary individual ball radii, target union volume
does not increase and target intersection volume does not decrease.

The exact target is Discovery Net artifact
`bafkreigmm2o2uehdxbseg3q54qlxqytbrevh3qdbhdireoyv6c74ky47wq` at source
commit `2de654f1c1f69a3ab543993d1a53553e91e2164b`. Nine exact target and accepted
precursor files are content-pinned. This is a theorem for the displayed
twisted-meridian class, not for every three-dimensional contraction, every
rotationally equivariant map, or every possible five-dimensional lift.
Historical priority is not determined.

## Exact motion and pair criterion

For meridians `p=(r,z)`, `p'=(r',z')`, put

```text
a=r-rho(p),                   A_t=r-ta,
M=|p-p'|^2-|S(p)-S(p')|^2,
P_t=A_t A'_t,
K_t=a A'_t+a' A_t,
d=psi(p)-psi(p').
```

The target path uses transverse radius `A_t`, phase
`theta+lambda(t)psi(p)`, interpolated axial coordinate, and two auxiliary
coordinates `sqrt(t(1-t))(p-S(p))`. Direct expansion gives

```text
|F_t(x)-F_t(x')|^2
 =(1-t)|p-p'|^2+t|S(p)-S(p')|^2
   +2P_t(1-cos(delta)),
delta=theta-theta'+lambda(t)d.
```

Differentiating is sign-consistent because `P'_t=-K_t`:

```text
-M-2K_t(1-cos(delta))+2P_t lambda'(t)d sin(delta).
```

Maximization over the entire azimuth circle, not a sampled set of angles,
gives

```text
-M+2sqrt(K_t^2+P_t^2 lambda'(t)^2d^2)-2K_t.
```

Since `M+2K_t>=0`, squaring introduces no spurious branch. Thus this explicit
motion contracts exactly when

```text
M(M+4K_t) >= 4P_t^2 lambda'(t)^2d^2
```

for every pair and time. When a source radius is zero, `rho=0` and both
`P_t` and `K_t` vanish, so the axis case is included.

For the simple clock `lambda=t`, `P_t` decreases while
`H_t=K_t/P_t=a/A_t+a'/A'_t` increases. The nonnegative function
`sqrt(H^2+d^2)-H` decreases in `H`; hence the adverse term
`2P_t(sqrt(H_t^2+d^2)-H_t)` is maximal at time zero. This proves that the
endpoint-data condition

```text
M(M+4K_0) >= 4r^2r'^2d^2
```

is both necessary and sufficient for the specified full-rotational motion.
It recovers the accepted untwisted meridian class when `psi` is constant.

## Delayed phase and uniform budget

Write `x=sqrt(q)` and `u=sqrt(c(t))`, where
`c(t)=1-(1-q)t`. The delayed clock simplifies to

```text
lambda=x(1-u)/(u(1-x)),
lambda'=x(1+x)/(2u^3).
```

Therefore `c^3(lambda')^2=x^2(1+x)^2/4` is constant. From
`rho/r<=q`, both transverse factors satisfy `A_t<=c(t)r`, while

```text
K_t/P_t >= 2(1-q)/c(t),
P_t^2/K_t <= c(t)^3 rr'/(2(1-q)).
```

The elementary bound
`sqrt(K^2+v^2)<=K+v^2/(2K)` makes the adverse phase contribution at most

```text
(RL)^2(1-q)/(8(q^(-1/2)-1)^2) |p-p'|^2.
```

The stated phase budget makes this no larger than
`(1-g^2)|p-p'|^2`, and meridian contraction supplies
`M>=(1-g^2)|p-p'|^2`. This proves the whole-time pair condition. The
algebraic identity

```text
(q^(-1/2)-1)^2/(1-q)
  =(1-sqrt(q))/(q(1+sqrt(q)))
```

confirms the exact constant in the theorem.

## Regularity and transfers

Reparametrizing by `t=sin(v)^2` makes the auxiliary coordinates
`sin(v)cos(v)(p-S(p))`, so each trajectory is analytic through both
endpoints. Before the terminal time, a nonzero meridian difference retains
the positive `(1-t)|p-p'|^2` contribution. At a common meridian, distinct
azimuths retain a positive angular term. Axis continuity follows from
`A_t<=r`. Lipschitz extension to the compact support closure preserves every
hypothesis.

The accepted Aishwarya--Li continuous-contraction theorem in `R5` gives the
sampled-density comparison. At each endpoint the two auxiliary Gaussian
coordinates factor. If `Z` has the two-dimensional Gaussian law, then its
normalized density value is uniform on `[0,1]`; conditioning therefore turns
the sampled-density inequality exactly into each three-dimensional hinge
comparison. No symmetry or atomic approximation of the input law is used.

Reversing the analytic motion meets the Bezdek--Connelly expansion hypothesis
and yields both ball-volume inequalities in dimension three for arbitrary
individual radii. Terminal collisions are handled correctly: for
`h=1-epsilon`, the regularized meridian map
`S_epsilon=epsilon I+hS` has

```text
M_epsilon=hM+epsilon h|Delta p-Delta S|^2,
P_epsilon,t=P_(ht),
K_epsilon,t=hK_(ht),
```

and the compressed phase has velocity `h lambda'(ht)`. Hence the pair
condition persists. Only finitely many positive `epsilon` can create a
terminal coincidence for a finite list; avoiding them and passing to the
continuous volume limit proves the claimed endpoint statement. Repeated
source centers and zero radii are covered by the stated merging and limit
arguments.

## Breadth example and scope controls

For

```text
rho=r/16,  zeta=r/2+|z|/4,  psi=7z,
```

the meridian derivative has squared Frobenius norm `81/256`, so `g=9/16`;
with `q=1/16`, the exact allowed value is `(RL)^2<=105/2`, which includes
`L^2=49`. Thus the folding helical example is genuinely within the theorem.

The sixteen rational Jacobians used for scope separation have zero mean and

```text
mean(D^T D)=diag(33/256,33/256,113/1024),
det(mean(D^T D))=123057/67108864>0.
```

Averaging the necessary local scalar-defect inequality would give zero on
its left side and a strictly positive right side, so no single fixed
all-frame scalar certificate exists. Two Jacobian Gram matrices have
commutator entry `4145/262144`, excluding one fixed strong-coordinate
representation. These are limited representation-separation statements;
they do not exclude finite compositions of older classes.

## Independent exact evidence and trust boundary

`independent_check.py` imports no target module. It differentiates pair
distances with exact dual numbers rather than the author's twelve-variable
sparse-polynomial engine. It checks 324 exact value/derivative controls, 18
clock controls, 360 radial budget controls, and a fresh 20-label endpoint
fixture at all 2,090 pair/time positions. It independently reconstructs the
sixteen Jacobians, positive mean Gram matrix, and noncommuting pair. Four
deliberately invalid clocks, budgets, or pair certificates are rejected.

Reproduce with:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

The checker guarantees source provenance, exact finite algebra, clock
normalization, budget constants, the fresh endpoint fixture, and the scope
controls. Trigonometric maximization, continuum inequalities, regularity,
support-closure passage, Gaussian cancellation, and ball-volume transfer
remain independently reviewed written mathematics, not proof-assistant
output. The primary sources support the transfer mechanisms and the fact
that unrestricted dimension-three majorisation remains open; they do not
establish historical novelty of this twisted class.
