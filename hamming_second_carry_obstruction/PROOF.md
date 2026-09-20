# Proof: the exact second carry cannot be repaired inside the minor box

## 1. Definitions

For a finite graph `H` and an integer `s >= 2`, call a nonempty vertex set
`C` **s-legal** when the induced graph `H[C]` has minimum degree at least
`s-1`.  Let `pi_s(H)` be the largest number of parts in a partition of
`V(H)` into s-legal sets.

Let

```text
B = K_m square K_n square K_p,
```

and assume throughout the thin second-carry hypotheses

```text
s >= 7,                  m,n >= s,                  1 <= p < s,
r = m mod s,             u = n mod s,
1 <= r,u < s,            ru < s,                   rup = 2s.       (H)
```

Set

```text
Q = p floor(mn/s).
```

Since `mn mod s = ru`, hypothesis (H) gives

```text
mnp = sQ + rup = s(Q+2).                                  (1)
```

Also `p<s` and `rup=2s` imply `ru>2`, hence

```text
3 <= ru < s.                                               (2)
```

The relation `p=s-1` would imply `s-1` divides `2s`, hence divides `2`,
which is impossible for `s>=7`.  Therefore

```text
3 <= p <= s-2.                                             (3)
```

## 2. Three inherited structural inputs

We use the following established Hamming-core facts with `h=s-1`.

1. Every nonlinear s-legal set has at least `2s-2` vertices.  At equality
   it is `K_(s-1) square K_2`, hence is the union of two coordinate lines.
2. Every nonlinear s-legal set of order `2s-1` is either two nested parallel
   lines of sizes `s` and `s-1`, two perpendicular s-point lines sharing one
   point, or (only when `s=5`) a `3 by 3` grid.  Our assumption `s>=7`
   excludes the grid.
3. Every s-legal set of order `2s` is in one of the corrected maximum-line
   forms: a single line; two disjoint s-point lines; or an `(s+1)`-point line
   together with an `(s-1)`-point line.  In particular it is the union of at
   most two coordinate lines.  This is the order-`2s` normal form that closes
   the boundary left open by the first two inputs.

In each of the three orders, every constituent line has at least `s-1`
points.  By (3), no such line can run in the `p` direction.  Consequently
each of these cores meets at most two of the `p` layers

```text
K_m square K_n square {z},  z in [p].                      (4)
```

We also use the sharp thin-coordinate theorem: the maximum number of
coordinate-line subsets of size at least `s` that can be pairwise disjoint
in `B` is `Q`.  Its balanced-rectangle construction partitions all of `B`
into exactly `Q` such line sets.

## 3. Exact minor-box partition theorem

**Theorem 1.** Under (H),

```text
pi_s(B) = Q.                                                (5)
```

**Proof.**  The balanced-rectangle partition in each of the `p` layers gives
`Q` coordinate-line parts of size at least `s`, so `pi_s(B)>=Q`.

Legality is preserved when two parts are merged: vertices retain all of
their old same-part neighbours.  Hence any partition with more than `Q+1`
parts could be merged down to one with exactly `Q+1` parts.  Suppose for a
contradiction that such a partition exists.  Every part has at least `s`
vertices.  At most `Q` of the parts can
be coordinate-line parts, so at least one part is nonlinear.  Each nonlinear
part has at least `2s-2` vertices and therefore consumes excess at least
`s-2` above the baseline size `s`.  By (1), the total excess of all `Q+1`
parts is exactly

```text
s(Q+2) - s(Q+1) = s.                                       (6)
```

Two nonlinear parts would consume at least `2s-4>s`, since `s>=7`.
There is consequently exactly one nonlinear part `C`, and the other `Q`
parts are line parts.  Their sizes are at least `s`, so (1) gives

```text
2s-2 <= |C| <= 2s.                                         (7)
```

Thus `|C|` is one of `2s-2`, `2s-1`, and `2s`.  The three inherited normal
forms and (4) show that `C` meets at most two `p`-layers.  Since `p>=3`, fix
a layer `L` disjoint from `C`.

Every remaining part is a coordinate-line set of size at least `s`.  It
cannot run in the `p` direction because `p<s`, so it lies wholly in one
layer.  The parts lying in `L` therefore partition its `mn` vertices.

Write every line-part size as `s+e_i`, with `e_i>=0`.  Across all `Q` line
parts, (1) and (7) give

```text
sum_i e_i = 2s-|C| <= 2.                                   (8)
```

If the line parts in `L` number `k`, then

```text
mn = sk + sum_(i in L) e_i.
```

The last sum is between zero and two by (8), while `mn mod s=ru` lies
between three and `s-1` by (2).  This is impossible.  Hence no `Q+1`-part
partition exists, proving (5).  Notice that this excludes arbitrary mixing
with stripped blocks; it is not merely a pure residual-box obstruction.  ∎

## 4. Consequence for four-dimensional majority C-colouring

Let

```text
G = K_n1 square K_m square K_n square K_p,
N1 = n1-1,
h = ceil(((n1-1)+(m-1)+(n-1)+(p-1))/2),
s = h-N1+1.
```

Assume the factors are ordered with

```text
n1 > m >= n >= p                                             (9)
```

and that the derived `s,m,n,p` satisfy (H).  The known class-size inequality
says that every colour class in a majority C-colouring of `G` has at least
`n1*s` vertices.  We record the equality case needed below.

**Lemma 2 (strict-major equality).** If a majority colour class has exactly
`n1*s` vertices, it is

```text
[n1] times S,
```

where `S` is an s-point subset of one minor coordinate line.

**Proof.**  At a vertex of the class let `a_i` be its same-coloured
directional degrees and `A=sum a_i`.  The first/second-shell inequality is

```text
|C| >= 1+A+(1/2) sum_i a_i(h-a_i).                         (10)
```

The cap-majorization proof of the class-size bound minimizes (10) at

```text
A=h,     (a_1,a_j,a_k,a_l)=(N1,s-1,0,0)                   (11)
```

up to the choice of minor direction `j`.  Equality at any larger `A` has
strictly positive excess.  Because `n1>m`, the largest cap `N1` is unique,
so equality in the class-size bound forces `a_1=N1` at every class vertex.
Thus the class is a union of complete first-coordinate fibres.  Its order
`n1*s` says that it is `[n1] times S` with `|S|=s`.

Every point of `S` has at least `s-1` neighbours within `S`; hence the
induced minor graph on `S` is complete.  Every clique in a Hamming graph is
contained in one coordinate line, proving the assertion.  ∎

**Theorem 3.** Under (H) and (9), if `Q=p floor(mn/s)`, then

```text
Q <= chi_bar_>=(G) <= Q+1.                                 (12)
```

Moreover, the maximum number of colours among colourings whose classes are
full first-coordinate cylinders is exactly `Q`.

**Proof.**  Lifting the `Q`-part balanced line partition of `B` through the
first coordinate gives `Q` majority colour classes: every vertex has at
least `N1+s-1=h` same-coloured neighbours.  This proves the lower bound and,
together with Theorem 1, the exact cylinder-lift statement.  Conversely, a
full first-coordinate cylinder is a majority colour class exactly when its
minor base is s-legal, so no cylinder colouring is omitted by this reduction.

The class-size bound and (1) give the prior upper bound `Q+2`.  If equality
held, all `Q+2` classes would have the minimum size `n1*s`.  Lemma 2 would
turn them into a partition of `B` by `Q+2` coordinate-line subsets of size
`s`, contradicting the sharp line maximum `Q`.  Thus at most `Q+1` colours
are possible.  ∎

The remaining one-colour gap in (12) is genuine scope, not suppressed
evidence: a `Q+1`-colouring, if it exists, must split the strict major
coordinate and cannot arise from any minor-core packing.

## 5. An explicit infinite family

Let `s>=8` be even and `A>=2`, and put

```text
n1 = 2As-s/2+5,
m  = (A+1)s+1,
n  = As+4,
p  = s/2.                                                   (13)
```

Then `n1>m>=n>=p`, the majority threshold is

```text
h = 2As+s/2+3,
```

and `h-(n1-1)+1=s`.  The relevant residues are `r=1`, `u=4`, so
`rup=2s` and `ru=4<s`.  Finally

```text
Q = (s/2)(A(A+1)s+5A+4).                                   (14)
```

Equations (12)--(14) give an infinite two-parameter family on which the
general volume upper bound drops from `Q+2` to `Q+1`, while every
first-coordinate-cylinder construction has at most `Q` colours.

For `(s,A)=(8,2)` this is

```text
G = K_33 square K_25 square K_20 square K_4,
248 <= chi_bar_>=(G) <= 249.
```
