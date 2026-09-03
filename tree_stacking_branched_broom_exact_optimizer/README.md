# Eventual exact optimizer in the branched-broom family

This directory sharpens the asymptotic optimization of the branched-broom
trees `R(d,e,t)` used in the Discovery Net tree-stacking project.  It proves
an eventual exact optimizer and evaluates the logarithm of its critical
configuration count through the periodic constant and first inverse-order
term.

The result uses the already established sibling-leaf classification of
critical tree-stacking obstructions.  It does not reprove that classification
and does not claim that a branched broom is globally extremal among all trees.

## Definitions

Start with a path of `t` edges from `p` to `q`, attach `d` leaves to `p`, and
attach `e` disjoint two-edge arms `q-a_i-b_i` to `q`.  The resulting tree is
`R(d,e,t)` and has

```text
n = d + 2e + t + 1
```

vertices.  The two possible leaf-parent potentials are

```text
X_p = d - 3 + (5e+3) 2^t,
X_a = (d+3) 2^(t+1) + 10e - 12.
```

If the `p`-leaf class is uniquely maximizing, the sibling-leaf theorem gives

```text
N(R(d,e,t)) = binom((5e+3)2^t + 2d - 4, d-1).       (1)
```

Let `M_R(n)` be the maximum of `N(R(d,e,t))` over positive integer parameters
of order `n`.

## Theorem

Fix `s` in `{0,...,17}` and write

```text
n = 18m + 1 + s.
```

For all sufficiently large `m`, the unique parameter triple attaining
`M_R(n)` is

```text
d = 5m+3,       e = 2m+2,       t = 9m-7+s.         (2)
```

Put `r=5m+2`.  At (2), `X_p-X_a=2^t-15m-8`, so the maximizing class is the
`p`-leaf class and

```text
M_R(n) = binom((10m+13)2^t + 10m+2, 5m+2).          (3)
```

Uniformly over the eighteen choices of `s`, as `m` tends to infinity,

```text
log_2 M_R(18m+1+s)
 = 45m^2 + (5s-12+5/ln 2)m - (1/2)log_2 m
   + 2s-12 + 13/(2 ln 2) - (1/2)log_2(10 pi)
   - 269/(120 m ln 2) + O(m^(-2)).                  (4)
```

In particular,

```text
log_2 M_R(n)
 = (5/36)n^2 + ((5/ln 2)-17)n/18
   - (1/2)log_2 n + O(1).                           (5)
```

This identifies the linear and logarithmic terms left open by the earlier
`(5/36)n^2+O(n)` theorem.  Formula (4) also gives the bounded periodic
constant after translating between `m` and `n`.

## Proof of the optimizer

Set `r=d-1`.  Subtracting the potentials gives

```text
X_p-X_a = (5e-2d-3)2^t + d-10e+9.                  (6)
```

Suppose `d>=2` and the `p` class is maximizing.  Then

```text
e >= e_0(r) := ceil((2r+6)/5).                      (7)
```

Indeed, if `5e-2d-3<=0`, then at `t=1` the right side of (6) is
`3-3d<0`.  At `t>=2`, the coefficient of `e` in

```text
d(1-2^(t+1)) + e(5*2^t-10) + 9-3*2^t
```

is positive.  Substituting `e<=(2d+3)/5` again bounds (6) by `3-3d<0`, a
contradiction.

For fixed `n` and `r`, the exponential part of the upper argument in (1)
strictly decreases with `e`, because

```text
((5(e+1)+3)2^(-2(e+1))) / ((5e+3)2^(-2e))
 = (5e+8)/(4(5e+3)) < 1.                            (8)
```

Consequently the formal row obtained by putting `e=e_0(r)` is an upper bound
for every contributing row with that `r`, whether or not the formal row
itself satisfies (6).

Write `r=5k+j`, `0<=j<=4`.  At `e=e_0(r)`, the main factor and the formal
value of `t` can be written as

```text
j    0       1       2       3       4
a_j  13      11      9       12      10
q_j  -6      -26/5   -22/5   -28/5   -24/5

5e_0+3 = 2r+a_j,        t_0 = n-(9/5)r+q_j.         (9)
```

Let `lambda=1+1/ln 2`.  In the only range capable of maximizing the count,
`r/n` tends to `5/18`, hence `t_0` is linear in `n`.  Stirling's formula and
`binom(Y,r)=Y^r/r! * (1+O(r^2/Y))` therefore give, uniformly in that range,

```text
log_2 binom((2r+a_j)2^t_0+2r-2,r)
 = rn-(9/5)r^2+(q_j+lambda)r
   + a_j/(2 ln 2) - (1/2)log_2(2 pi r) + O(1/r).   (10)
```

For completeness, the restriction to this range follows first from the
coarser upper bound

```text
log_2 binom(Y,r) <= rt + r log_2(3 e n/r).
```

Together with the existing construction, its quadratic part forces every
maximizer to satisfy `r/n -> 5/18`.

The largest entry in the `q_j` row of (9) is uniquely `q_2=-22/5`.
Maximizing the quadratic in (10) shows that every other residue class loses
a positive multiple of `n`; hence eventually `r=2 (mod 5)` and (7) is an
equality.  On this lattice the quadratic vertex is

```text
rho_n = (5/18)(n+lambda-22/5).
```

For `n=18m+1+s`, the proposed lattice point `r_*=5m+2` satisfies

```text
rho_n-r_* = (5s+5lambda-53)/18.                    (11)
```

As `s` ranges from 0 to 17, (11) lies strictly between `-5/2` and `5/2`.
The endpoint inequalities reduce to `8/5<lambda<13/5`, which follow, for
example, from `5/8<ln 2<1`.  Thus `r_*` is the unique closest point to the
quadratic vertex in the lattice `2+5 Z`.  Its smallest quadratic advantage
over a neighboring lattice point occurs at `s=17` and is
`13-5lambda>0`.  The logarithmic term and the `O(1/r)` remainder in (10)
change neighboring comparisons by `o(1)`, so they cannot reverse this fixed
strict advantage.  This proves the eventual uniqueness in (2).  The possible
arm-class contribution at a tie is only `O(n)` and is negligible compared
with the same strict binomial gaps.

## Proof of the expansion

At (2), equation (3) has

```text
Y=(2r+9)2^t+2r-2.
```

Since `t` is linear in `m`, replacing `log_2 Y` by
`t+log_2(2r+9)` has exponentially small total error.  The two standard
expansions

```text
r log_2(2+9/r)
 = r + 9/(2 ln 2) - 81/(8r ln 2)
   + 243/(8r^2 ln 2) + O(r^(-3)),

log_2(r!)
 = r log_2 r-r/ln 2+(1/2)log_2(2 pi r)
   +1/(12r ln 2)+O(r^(-3))
```

give

```text
log_2 M_R(n)
 = rt+(1+1/ln 2)r+9/(2 ln 2)
   -(1/2)log_2(2 pi r)-245/(24r ln 2)+O(r^(-2)).   (12)
```

Substituting `r=5m+2`, `t=9m-7+s`, and expanding the logarithm and reciprocal
in (12) gives (4), including

```text
-1/(5m ln 2)-49/(24m ln 2) = -269/(120m ln 2).
```

Equation (5) follows by replacing `m` with `(n-1-s)/18`.

## Exact finite checks

The standard-library checker performs two finite tasks that are separate from
the asymptotic proof.

1. It directly enumerates every positive `(d,e,t)` below order 91 and records
   that order 90 is the last exception there to the pattern (2).
2. At every order from 91 through 500, it checks every `d` using the formal
   upper row (7), includes an additive upper bound for a possible tie, and
   proves that (2) is the unique optimizer.  A second implementation directly
   enumerates every positive triple through order 120.

These computations show that 91 is the exact onset through the checked range.
They are not used to assert that 91 is the universal onset; the ordinary proof
above establishes the pattern only for all sufficiently large orders.

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -I verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -I test_verify.py
sha256sum -c SHA256SUMS
```

Expected markers are `EXACT ORDERS 91..500 VERIFIED`, `last_exception=90`,
and `INDEPENDENT DIRECT ENUMERATION THROUGH 120 PASSED`.

The finite checks use exact arbitrary-precision integer arithmetic only.  No
floating point, randomness, solver, external data, proof log, or generated
large certificate enters either the theorem or the finite result.

## Prior-work and scope note

The source paper by Tamás Csernák and Lajos Soukup,
[Stacking and clearing in graph pebbling](https://arxiv.org/abs/2604.22341),
introduces the stacking number and gives a conjectural tree formula, but does
not study the multiplicity of critical obstructions or the family `R(d,e,t)`.
The earlier Discovery Net findings establish the sibling-leaf count formula,
the branched-broom exponent `5/36`, and its `O(n)` remainder.  Targeted
primary-source, web, repository, and committed-graph searches found no prior
exact optimizer or expansion (4).  Any novelty description is therefore
relative to the searched sources, not a priority claim.
