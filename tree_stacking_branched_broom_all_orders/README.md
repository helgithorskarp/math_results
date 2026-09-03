# Branched brooms beat symmetric double brooms at every order from 23 onward

## Results

For a finite tree `T`, let `N(T)` be the number of non-stackable pebbling
configurations of maximum possible mass `stack(T)-1`.  The established
sibling-leaf classification gives

```text
N(T) = sum over maximizing leaf-parents p of
       binom(X_p + d_p - 1, d_p - 1),
```

where `d_p` is the number of graph leaves adjacent to `p` and

```text
X_p = sum over nonleaf vertices u of deg_T(u) * 2^dist_C(p,u).
```

Here `C` is the nonleaf core of `T`.

Define `R(d,e,t)` from a path of `t` edges

```text
p = v_0 - v_1 - ... - v_t = q
```

by attaching `d` leaves directly to `p` and `e` pairwise disjoint two-edge
arms `q-a_i-b_i` to `q`.  Thus

```text
|V(R(d,e,t))| = d + 2e + t + 1.
```

This directory proves two theorems.

**Every-order separation.**  For every integer `n >= 23`, there are positive
`d,e,t` with `d+2e+t+1=n` such that `R(d,e,t)` has strictly more critical
configurations than every symmetric double broom on `n` vertices.  The
order-23 counterexample is therefore the first member of an all-orders
phenomenon, not an isolated exception.

**Sharp exponent inside the branched-broom class.**  If

```text
M_R(n) = max N(R(d,e,t)),
```

where the maximum is over positive parameters of order `n`, then

```text
log_2 M_R(n) = (5/36)n^2 + O(n log n).
```

The previously established maximum over all `n`-vertex caterpillars has
logarithm `n^2/8+O(n log n)`.  Since `5/36-1/8=1/72`, the present family is
larger by a factor

```text
2^(n^2/72 - O(n log n)).
```

In particular, sufficiently large global multiplicity-maximizing trees are
not caterpillars.

## Exact potentials

The two possible leaf-parent potentials of `R(d,e,t)` are

```text
X_p = d - 3 + (5e+3)2^t,
X_a = (d+3)2^(t+1) + 10e - 12.
```

The first is attained by the `d` leaves at `p`; the second is attained by the
single leaf below each arm parent.  Direct subtraction gives the decisive
identity

```text
X_p - X_a = (5e-2d-3)2^t + d-10e+9.                 (1)
```

For a symmetric double broom `B(a,a,ell)`, the same classification gives

```text
N(B(a,a,ell))
  = 2 binom(2^ell(a+3)+2a-4, a-1),                 (2)
```

with order `2a+ell+1`.

## Witnesses at every order

The finite witnesses begin with

```text
23 <= n <= 32:  R(8,4,n-17),
33 <= n <= 36:  R(10,5,n-21).
```

For every `n >= 37`, write uniquely

```text
n = 18m + 1 + s,       0 <= s <= 17,
```

and take

```text
d = 5m+3,      e = 2m+2,      t = 9m-7+s.          (3)
```

These parameters have the required order.  In (1), their potential
difference becomes

```text
X_p-X_a = 2^t-(15m+8).
```

It is positive for every `m >= 2`: at `m=2`, the left exponential is at
least `2^11>38`, and increasing `m` multiplies that exponential by 512 while
the linear term increases by 15.  Thus `p` is the unique maximizing parent,
and

```text
N(R(d,e,t)) = binom(Y,5m+2),
Y = (10m+13)2^t + 10m+2.                            (4)
```

The two independent finite verifiers use (2)--(4) and enumerate every
integer `a` with `ell=n-2a-1>=1`.  They prove strict separation at all 554
orders `23 <= n <= 576`.  The smallest absolute margin occurs at `n=23` and
is

```text
1,988,979,420,313,950,568.
```

## Uniform proof for the infinite tail

Suppose `n >= 577`, so the `m` in (3) satisfies `m >= 32`.  In (4), put
`r=5m+2`.  Since `(10m+13)/r>2` and
`binom(Y,r)>=(Y/r)^r`,

```text
log_2 N(R(d,e,t)) > (t+1)(5m+2)
                 >= (9m-6)(5m+2)
                  = 45m^2-12m-12.                  (5)
```

Now consider any symmetric double broom of order `n`, and put `x=a-1`.
The upper argument in (2) satisfies

```text
2^ell(a+3)+2a-4 <= 3(a+1)2^ell.
```

Writing `c=log_2(3(a+1))` and using
`ell=n-2x-3` therefore gives

```text
log_2 N(B(a,a,ell))
 <= 1+x(n-3+c-2x)
 <= 1+(n-3+c)^2/8.                                  (6)
```

Since `a+1<=n/2`, `n<=18m+18`, and

```text
log_2(27m+27) <= m/3      for m >= 32,               (7)
```

equation (6) is at most

```text
1+(55m/3+15)^2/8.
```

For completeness, (7) starts from `891^3<2^32`; the ratio
`2^(m/3)/(27(m+1))` increases because
`34^3<2*33^3`.  Finally, the lower exponent in (5) minus the last upper bound
is

```text
(215/72)m^2 - (323/4)m - 329/8.                     (8)
```

It is positive at `m=32` (value `31151/72`) and strictly increasing from
there.  This proves the every-order theorem beyond the finite checked range.

## Sharp asymptotic optimization

For the lower bound, construction (3) and (5) give

```text
log_2 M_R(n) >= (5m+2)(9m-6+s)
             = (5/36)n^2-O(n).
```

For the upper bound, first suppose `d>=2` and the `p` class contributes to
`N(R(d,e,t))`, so `X_p>=X_a`.  If `5e-2d-3<=0`, then (1), `t>=1`, and
multiplication of a nonpositive integer by `2^t>=2` would force `d<=1`, a
contradiction.  Hence

```text
5e >= 2d+4,
t <= n-(9/5)d-13/5.                                  (9)
```

Also, with `Y=X_p+d-1`,

```text
Y = (5e+3)2^t+2d-4 <= 3n 2^t.
```

If the arm class wins instead, its total contribution is only `e<=n`, which
already satisfies the desired upper bound.  If `p` wins or the classes tie,
then, with `x=d-1`,

```text
N(R(d,e,t))
 <= (n+1)(3n)^x 2^(tx),

tx <= x(n-22/5-(9/5)x)
   <= (5/36)(n-22/5)^2.
```

Consequently

```text
log_2 M_R(n)
 <= (5/36)n^2 + n log_2(3n) + log_2(n+1),
```

which, together with the construction, proves the claimed sharp quadratic
coefficient `5/36`.

## Reproduction

The programs require CPython 3.11 or later and only the standard library.
Run from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_finite.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_direct.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_analytic.py
```

`verify_finite.py` uses the closed potentials and `math.comb`.
`verify_direct.py` independently reconstructs each potential as a weighted
sum over the nonleaf core and counts weak compositions by an exact numerator
product divided by a factorial.  Both hash every full exact comparison
record and return

```text
finite_orders_checked=554
minimum_margin_order=23
minimum_margin=1988979420313950568
record_sha256=090c104743620b18f6223b602104462a1f06355dfd7509d9a5b400912e604741
status=VERIFIED
```

On CPython 3.11.2, the closed-form and independent runs took about 17 and 30
seconds, respectively, on the research host.  `verify_analytic.py` checks
the integer and rational inequalities behind (7)--(8), without floating
point.  `expected_summary.json` is a compact persisted certificate of both
finite computations.

## Scope, trust boundary, and literature

The asymptotic theorem and the infinite-tail comparison are ordinary
inequality proofs.  The orders 23 through 576 are an exact computer-assisted
finite theorem.  Both finite implementations use arbitrary-precision Python
integers and have different potential and weak-composition implementations;
they agree entry-for-entry through the canonical record hash.  There is no
solver, floating point, randomness, timeout, external dataset, or proof log.
The remaining computational trust boundary is CPython, the two programs,
the runtime, and ordinary hardware behavior.

The sibling-leaf count formula is imported from Discovery Net contribution
`bafkreigrlfot45gncrzuggfqitcuxbwmxdwto2kav4srp47b6zbmslfl5u`, which has
an independent reproduction.  This contribution does not re-prove the
underlying tree-stacking transfer theorem.  It does not identify the global
maximizing tree at any fixed order.  Its universal exact claim is the strict
comparison with every symmetric double broom; its asymptotic consequence is
that the global maximizer is eventually non-caterpillar.

The original parameter and tree formula problem are due to Tamás Csernák and
Lajos Soukup, *Stacking and clearing in graph pebbling*, arXiv:2604.22341
(2026): <https://arxiv.org/abs/2604.22341>.  Their paper and public computation
repository <https://github.com/lajossoukup/pebbling> study stacking numbers
and finite non-stackability sets, but not critical-obstruction multiplicity,
double-broom extremality, or this branched-broom family.  The exact order-23
counterexample and the caterpillar exponent are prior Discovery Net results.
Targeted source and graph searches found no prior all-orders separation or
`5/36` exponent.  This is a search-relative novelty statement, not a
historical-priority claim.
