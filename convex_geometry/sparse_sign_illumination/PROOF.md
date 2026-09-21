# Exact fractional illumination and covering arrays

For integers `1 <= k <= n`, put

\[
 P_{n,k}=\{x\in\mathbb R^n: |x_i|\le1\ (i\in[n]),\quad
                         \sum_i|x_i|\le k\}.
\]

Write `I(P)` for ordinary illumination by directions, and `I_f(P)` for
fractional illumination: nonnegative weights on finitely many nonzero
directions, with total weight at least one illuminating each boundary
point. Directions can be normalized without changing illumination.
The fractional number is the infimum of the total weights. All fractional
optima below have explicit finite rational certificates, so are attained.

Let `CAN(k,n,2)` be the least number of rows of a binary array with `n`
columns such that every restriction to `k` columns contains all `2^k`
binary patterns. Repeated rows do not help. Our argument uses no unknown
covering-array values.

## Theorem

1. The maximum number of vertices of `P_{n,k}` illuminated by one direction is

   \[
   M(n,k)=
   \begin{cases}
   \binom{n-1}{k-1},&2k\le n,\\
   \binom nk,&2k>n.
   \end{cases}
   \]

   Consequently

   \[
   \boxed{I_f(P_{n,k})=\begin{cases}
   (n/k)2^k,&2k\le n,\\
   2^k,&2k>n.
   \end{cases}}
   \]

2. If `2k>n`, then

   \[
   \boxed{I(P_{n,k})=\operatorname{CAN}(k,n,2).}
   \]

   Every illuminating direction can be replaced by a vector in
   `{−1,1}^n` which illuminates all vertices illuminated by the original
   direction. This gives a conversion of every feasible solution, in
   both directions, preserving or decreasing its cardinality.

3. In the range `2k>n`, the equality `I(P_{n,k})=I_f(P_{n,k})` holds
   exactly when `k=n` or `k=n−1` (the latter requires `n>=2`). Thus
   `n/2<k<=n−2` forces strict inequality. For `k>=2` and `2k>n`,

   \[
   \frac{I(P_{n,k})}{I_f(P_{n,k})}
   \ge \frac{1+\lceil\log_2(n-k+2)\rceil}{4}.
   \]

   In particular the ratio is unbounded on `P_{2k−1,k}` as `k` tends
   to infinity. This identifies a rounding obstruction in this polytope
   family; unbounded illumination gaps for general convex bodies were
   already known, for example from smooth bodies.

The Hadwiger inequality for this family is already a consequence of
Sun–Vritsiou's theorem for all 1-symmetric convex bodies. Our subject is
the exact fractional value and the exact optimization reduction, not a
new proof of that conjectured inequality. The combinatorial ingredients
are classical Erdős–Ko–Rado and elementary covering-array facts.

## 1. Vertices and the exact entering condition

The body is full dimensional, since the origin satisfies every defining
inequality strictly. Its vertices are precisely

\[
 v(F,\sigma)_i=\begin{cases}\sigma_i,&i\in F,\\0,&i\notin F,
 \end{cases}
 \qquad |F|=k,\quad \sigma\in\{-1,1\}^F.
\]

To prove completeness, a point with `sum |x_i|<k` has a coordinate with
`|x_i|<1`, and sufficiently small positive and negative perturbations of
that coordinate are feasible. Such a point is not a vertex. At a point
with `sum |x_i|=k`, if some absolute coordinate lies strictly between zero
and one, at least two do, because `k` is an integer. One can transfer a
small amount between those two absolute coordinates, keeping their signs
and the sum fixed. This again gives a feasible segment. The remaining
possibilities are exactly the displayed points. Conversely, maximizing
`sum_{i in F} sigma_i x_i` uniquely selects `v(F,sigma)`: equality at `k`
forces all coordinates in `F`, and the absolute-sum constraint forces all
others to zero. There are `V=2^k binom(n,k)` vertices.

For a nonzero direction `d`, the necessary and sufficient condition for
illuminating `v(F,sigma)` is

\[
 \sigma_i d_i<0\quad(i\in F),\qquad
 \sum_{i\in F}|d_i|>\sum_{i\notin F}|d_i|. \tag{1}
\]

Indeed, the active coordinate inequalities require the first condition.
For a sufficiently small positive `t`, the signs on `F` do not change and

\[
 \sum_i|v(F,\sigma)_i+td_i|
 =k+t\left(\sum_{i\in F}\sigma_i d_i+
                   \sum_{i\notin F}|d_i|\right).
\]

The absolute-sum inequality becomes strict exactly when the second
condition in (1) holds. The other coordinate inequalities are strict
for sufficiently small `t`. Necessity also follows directly from the
active supporting inequalities. All inequalities in (1) are strict;
zero coordinates of `d` in `F` are forbidden.

For completeness, illuminating all vertices, ordinarily or fractionally,
suffices for the entire boundary of a polytope. Given a boundary point
`x`, take a vertex `v` of its minimal face. Every defining inequality
active at `x` is also active at `v`. Thus every direction illuminating
`v` illuminates `x`. The weight reaching `x` is at least that reaching
this one fixed vertex. This argument applies to the full displayed
inequality description even when some inequalities are redundant.

## 2. Exact one-direction capacity

Fix `d`, set `w_i=|d_i|>=0` and `W=sum_i w_i>0`. For each support `F`
there is at most one sign assignment illuminated by `d`. The eligible
supports satisfy `sum_F w_i>W/2`, and cannot contain a zero coordinate.
Any two eligible supports intersect: disjoint ones would have combined
weight greater than `W`.

When `2k<=n`, the Erdős–Ko–Rado theorem bounds every intersecting family
of `k`-subsets of `[n]` by `binom(n−1,k−1)`. This proves the upper bound
for the capacity. To attain it, use a direction with one absolute
coordinate equal to `n` and all others equal to one. Exactly the
`k`-subsets containing the heavy coordinate are eligible. This also
handles `2k=n`, where equality of the two sides in (1) would otherwise
matter.

When `2k>n`, the number of supports is the upper bound `binom(n,k)`.
The direction with all absolute coordinates one makes every support
eligible and attains the bound. These arguments include `k=1`, `k=n`,
and `n=1` in their respective ranges.

## 3. Matching finite fractional certificates

Give each vertex dual weight `1/M(n,k)`. Section 2 says that the total
dual weight illuminated by any direction is at most one. Summing the
fractional covering constraints over vertices therefore gives

\[
 I_f(P_{n,k})\ge V/M(n,k).
\]

This is elementary weak duality and requires no infinite-dimensional
linear-programming duality theorem.

For `2k<=n`, use all `n 2^n` directions

\[
 d^{j,\epsilon}_i=
 \begin{cases}n\epsilon_i,&i=j,\\\epsilon_i,&i\ne j,
 \end{cases}
 \quad j\in[n],\quad\epsilon\in\{-1,1\}^n.
\]

Assign each the weight `1/(k 2^(n−k))`. A vertex `v(F,sigma)` is
illuminated exactly when `j in F` and `epsilon_i=−sigma_i` on `F`.
There are exactly `k 2^(n−k)` such directions. Every vertex receives
weight exactly one, and the total weight is `n 2^k/k=V/M`.

For `2k>n`, use all `2^n` sign directions, each with weight
`1/2^(n−k)`. Each vertex is illuminated by exactly `2^(n−k)` of them.
The mass is `2^k=V/M`. By the boundary argument in Section 1 these are
fractional illuminations of the whole body. This proves part 1.

## 4. Reduction to a binary covering array

Assume `2k>n`. Replace each nonzero direction `d` by a sign vector `s`,
where `s_i=sign(d_i)` for nonzero coordinates, and arbitrary signs are
assigned at zeros. If `d` illuminates `v(F,sigma)`, then `d_i` is nonzero
and `s_i=−sigma_i` on `F`. For `s`, the two sides of the second inequality
in (1) are `k` and `n−k`. Thus `s` illuminates this vertex too.

The replacement works simultaneously for all vertices illuminated by
`d`. Deleting repeated sign directions cannot hurt an ordinary cover.
Conversely, a collection of sign directions illuminates all vertices
exactly when its restrictions to each `k` coordinates contain every
sign pattern. Replacing signs by bits is precisely a binary covering
array. This proves both inequalities in part 2.

No such equivalence is claimed when `2k<=n`. In particular, when
`2k=n`, a sign vector illuminates no vertices at all: (1) is then an
equality, not a strict inequality.

## 5. Exact equality obstruction and a growing gap

Every strength-`k` binary covering array needs at least `2^k` rows, by
looking at any fixed `k` columns. Suppose it has exactly `2^k` rows.
Its first `k` columns consist of every binary vector `x` exactly once.
Any additional column is therefore a function `f(x)`.

Replace the `i`th of these first `k` columns by `f`. For each assignment
to the remaining `k−1` columns, the two rows must have different `f`
values. Consequently `f(x+e_i)=1−f(x)` for every `x,i`, with addition
in `F_2`. Connectivity of the cube gives

\[
 f(x)=x_1+\cdots+x_k+c\pmod2.
\]

If `k>=2`, two additional columns would be equal or complementary.
Choosing those two and any `k−2` of the first columns would miss binary
patterns. Thus there is at most one additional column. This proves
`CAN(k,n,2)>2^k` for `2<=k<=n−2`. When `n=k`, all binary rows work;
when `n=k+1`, the array `x -> (x, parity(x))` works with `2^k` rows.
In the regime `2k>n`, the only case with `k=1` is `n=k=1`, already
covered. This proves the equality classification.

For the quantitative bound, fix any `k−2` columns of a strength-`k`
array. For each of their `2^(k−2)` patterns, the corresponding rows,
restricted to the remaining `m=n−k+2` columns, form a strength-two
binary covering array. In an `r`-row strength-two array the columns are
distinct even after identifying each binary column with its complement:
equal or complementary columns miss two patterns. There are only
`2^(r−1)` complementary pairs of binary columns. Hence

\[
 r\ge1+\lceil\log_2 m\rceil.
\]

Summing over the disjoint row classes gives

\[
 \operatorname{CAN}(k,n,2)\ge
 2^{k-2}\bigl(1+\lceil\log_2(n-k+2)\rceil\bigr).
\]

Divide by the exact fractional value `2^k`. For `n=2k−1` the logarithm
has argument `k+1`, proving the claimed unbounded ratio. This elementary
bound is not asserted to be a new covering-array bound or to be sharp.

## 6. One compact integral-gap witness

The classical covering-array value `CAN(3,5,2)=10` gives
`I(P_{5,3})=10`, while `I_f(P_{5,3})=8`. Here is a self-contained
certificate, included as a check of the geometric conversion rather
than as a new covering-array result:

```text
00000  11111
00011  11100
00101  11010
01001  10110
01110  10001
```

These ten rows contain all eight patterns on every three columns.
For the lower bound, partition the rows by any one column. Each part
must be a strength-two covering array on the other four columns.
The parity obstruction just proved, with `k=2,n=4`, requires at least
five rows in each part. Thus at least ten are needed.

The rational fractional certificate here consists of the 32 sign
directions, each of weight `1/4`. Uniform vertex dual weight `1/10`
has the same total mass, eight. The checker evaluates the active
supporting inequalities separately for every vertex and direction.

## Status and trust boundary

This is a written proof for all indicated integers. The only external
theorem used in the proof is classical Erdős–Ko–Rado; all covering-array
facts needed here have been proved above. Finite exact checks validate
the geometry, certificate construction, and small illustrative witnesses;
they do not prove the all-parameter statements or certify priority.
No general ordinary value is asserted for `2k<=n`, and no new numerical
covering-array bounds or solution of general illumination is claimed.
See [SOURCES.md](SOURCES.md) for the primary-source and novelty audit.
