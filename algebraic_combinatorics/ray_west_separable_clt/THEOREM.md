# Gaussian Ray--West correction on separable permutations

Let `Sep_n=Av_n(2413,3142)`, and let `j(pi)` be the Ray--West
codimension-two correction.  Thus, for a permutation of length `n`,

```text
g_2(pi)=(n^4+2n^3+n^2+4n+4-2j(pi))/2.
```

For a uniformly random `Pi_n` in `Sep_n`, set `X_n=j(Pi_n)`.

## Theorem

Put

```text
sigma^2 = sqrt(2)-5/4.
```

Then `sigma^2>0`, and

```text
E[X_n]   = n/2 + O(1),
Var(X_n) = sigma^2 n + O(1).                         (1)
```

Moreover,

```text
(X_n-n/2)/sqrt(sigma^2 n)  ->  Normal(0,1)           (2)
```

in distribution.  In fact, the Kolmogorov distance in (2) is
`O(n^(-1/2))`.

## Algebraic starting point

The preceding distribution theorem proved that

```text
J(z,u)=sum_(n>=1) sum_(pi in Sep_n) z^n u^j(pi)
```

is the unique formal solution in `z Z[u][[z]]` of

```text
H J^2 + B J + E = 0,                                 (3)
H=(1-uz)(1+z-2uz),
C=(1-u)z^2,
B=(z-1)H-2C,
E=zH-2C.
```

Let

```text
R(z,u)=B(z,u)^2-4H(z,u)E(z,u)                       (4)
```

be its discriminant.  The branch selected by `J(0,u)=0` is

```text
J(z,u)=(-B(z,u)-sqrt(R(z,u)))/(2H(z,u)).             (5)
```

At `u=1`, direct factorization gives

```text
R(z,1)=(1-z)^4(1-6z+z^2).                           (6)
```

Write

```text
rho=3-2sqrt(2).
```

This is the unique zero of `R(z,1)` in a closed disk `|z|<=r` whenever
`rho<r<1`, and it is simple.  The zeros of `H(z,1)=(1-z)^2` lie outside
such a disk.

## Uniform singularity perturbation

Choose and fix `r` with `rho<r<1`.  Since `R_z(rho,1)` is nonzero, the
analytic implicit-function theorem gives a unique analytic function `rho(u)`
near `u=1` such that

```text
R(rho(u),u)=0,       rho(1)=rho.                     (7)
```

Shrinking the neighbourhood of `u=1` if necessary, continuity of polynomial
zeros and (6) show that this is the only zero of `R(.,u)` in `|z|<=r`;
`H` has no zero there.  Equation (5) consequently has, uniformly for complex
`u` near `1`, the expansion

```text
J(z,u)=A(z,u)+D(z,u)(1-z/rho(u))^(1/2),              (8)
```

where `A,D` are analytic near `(rho,1)` and `D(rho,1)` is nonzero.  Indeed,
the square-root coefficient is obtained from

```text
R(z,u)=-rho(u)R_z(rho(u),u)(1-z/rho(u)) + higher terms,
```

and neither `R_z` nor `H` vanishes there.

Uniform square-root transfer applied to (8) yields an analytic nonzero
function `K(u)` such that

```text
[z^n]J(z,u)
 = K(u) rho(u)^(-n) n^(-3/2)(1+O(n^(-1)))           (9)
```

uniformly for complex `u` in a neighbourhood of `1`.  Thus the moment
generating function of `X_n` has the quasi-power form

```text
E[exp(t X_n)]
 = K(exp(t))/K(1)
   * (rho(1)/rho(exp(t)))^n * (1+O(n^(-1))).         (10)
```

The error in (10) is uniform for complex `t` near zero.

## Exact mean and variance rates

All partial derivatives below are evaluated at `(rho,1)`.  Reducing powers
of `rho` by `rho^2-6rho+1=0` gives

```text
R_z  =  -96+544rho,
R_u  = -272+1584rho,
R_zz = -160+1088rho,
R_zu = -976+5696rho,
R_uu = -2248+13104rho.                               (11)
```

Implicit differentiation of (7) gives

```text
rho'(1)  = -R_u/R_z = -rho/2,

rho''(1) = -(R_zz rho'(1)^2+2R_zu rho'(1)+R_uu)/R_z
          = (-1+7rho)/2.                             (12)
```

Let

```text
lambda(t)=log(rho(1)/rho(exp(t))).
```

Then (12) gives

```text
lambda'(0)  = -rho'(1)/rho = 1/2,

lambda''(0) = -rho''(1)/rho-rho'(1)/rho
              +(rho'(1)/rho)^2
            = 1/4-rho/2
            = sqrt(2)-5/4.                           (13)
```

This is positive because `sqrt(2)>5/4`.  The quasi-powers theorem applied to
(10) now proves (1), (2), and the stated `O(n^(-1/2))` convergence rate.

## Evidence and scope

The exact standard-library checker reconstructs (4), verifies (6), computes
the five derivatives in (11) in the quadratic field `Q(rho)`, and checks every
identity in (12)--(13).  The combinatorial interpretation and the algebraic
equation (3) are audited separately in the dependency directory, including a
definition-level check against all 2,321 separable permutations through length
seven.

The theorem concerns only the Ray--West correction on uniformly random
separable permutations.  It does not assert a limit law for arbitrary
permutations, for other pattern classes, or for the codimension-three
correction.
