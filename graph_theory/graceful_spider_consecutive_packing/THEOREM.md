# A consecutive-multiplier packing theorem for graceful spiders

## Definitions and inputs

A graceful labeling of a tree with `m` edges bijectively labels its vertices
by `0,1,...,m` so that its edge differences are exactly `1,2,...,m`.

We use the self-matched-leg framework of Dumitru and Nacu.  With the hub
labeled `1`, set

```text
A_m = {0,2,3,...,m},
tau_m(0)=m,             tau_m(x)=x-1 for x>=2.
```

A rooted path `(1,x_1,...,x_s)` is *self-matched* if its edge-difference set
is `tau_m({x_1,...,x_s})`.  Pairwise label-disjoint self-matched paths, one
of which contains `0`, become the nontrivial arms of a graceful spider after
every unused label in `A_m` is attached to the hub as a leaf.  Indeed, the
nontrivial arms use `tau_m(X)` and the hub leaves use `tau_m(A_m-X)`.

Two explicit self-matched paths from that framework are needed here.

For `s>=2`, `q>=1`, and `m+1>=sq+2`, the multiplicative path `P_s(q)`
alternates through the arithmetic progression

```text
q+1, 2q+1, ..., sq+1
```

in high-low order.  Its label set is the displayed progression and its
difference set is `{q,2q,...,sq}`.

For a closure length `c>=2`, define

```text
C_2(m) = (1,m,0),
C_3(m) = (1,m-1,0,m),
C_c(m) = (1,2^(c-4)+1,2^(c-5)+1,...,2, m,0,m-1)  (c>=4).
```

This is a zero-containing self-matched path whenever

```text
M_c = 2                         if c=2,
      3                         if c=3,
      2^(c-4)+3                 if c>=4
```

satisfies `m>=M_c`.  Its low labels, other than the hub, are at most
`P_c+1`, where

```text
P_c = 0                         if c=2 or 3,
      2^(c-4)                   if c>=4.
```

These assertions can also be checked directly: the closure differences are
`{m-1,m}` for `c=2`, `{m-2,m-1,m}` for `c=3`, and

```text
{1,2,4,...,2^(c-4)} union {m-2,m-1,m}
```

for `c>=4`, exactly the `tau_m`-images of their non-hub labels.

## Consecutive-multiplier theorem

Fix `c>=2` and `r>=1`, and let

```text
L_1 >= L_2 >= ... >= L_r >= 2,       L=L_1,
S=c+L_1+...+L_r.
```

Define

```text
Q=max(1, P_c, (L-1)r-L+1),
q_i=Q+i                         (1<=i<=r),
K=max(M_c, 3 + max_i L_i q_i),
T=max(0,K-S).
```

Then, for every integer `t>=T`, the spider

```text
S(c,L_1,...,L_r,1^t)
```

has a graceful labeling with hub label `1`.

### Proof

Let `m=S+t`, so `m>=K`.  Put `C_c(m)` on the distinguished arm and put
`P_(L_i)(q_i)` on arm `i`.

First consider two multiplicative arms `i<j`.  If they shared a label, then
for some `1<=a<=L_i` and `1<=b<=L_j` we would have

```text
a q_i + 1 = b q_j + 1.
```

Because `q_i<q_j`, this forces `a>b`; hence, since `a,b<=L`,

```text
q_j/q_i = a/b >= L/(L-1).                         (1)
```

On the other hand,

```text
q_j/q_i <= (Q+r)/(Q+1) < L/(L-1),                 (2)
```

where the strict inequality in (2) is equivalent to
`Q>(L-1)r-L`, built into the definition of `Q`.  Thus (1) and (2)
contradict each other, and the multiplicative label sets are pairwise
disjoint.

Every multiplicative non-hub label is at least `q_1+1>P_c+1`, so none is a
low closure label.  Also

```text
L_i q_i+1 <= m-2,
```

by the definition of `K`; hence no multiplicative label is one of the high
closure labels `m-1,m` (and it is plainly not `0`).  The weaker ambient
requirement `m+1>=L_i q_i+2` also follows.  Therefore all selected paths are
valid, self-matched, and pairwise label-disjoint, while the closure path
contains `0`.

The paths use exactly `S` non-hub labels.  There are `m-S=t` unused labels
in `A_m`; attach those labels as hub leaves.  The self-matched packing
argument then gives every vertex label `0,...,m` and every edge difference
`1,...,m` exactly once.  This proves the theorem.

## Exchange-optimal assignment on the chosen interval

Among the fixed multipliers `Q+1<...<Q+r`, assigning the arm lengths in
decreasing order minimizes `max_i L_i q_i`.

Indeed, suppose `alpha>=beta` but `alpha` is assigned to `q'>q` and `beta`
to `q`.  Before swapping, the larger of the two products is at least
`alpha q'`.  After swapping, both `alpha q` and `beta q'` are at most
`alpha q'`.  Removing inversions one at a time proves the claim.  Thus the
formula for `T` uses the best assignment for this consecutive multiplier
set; it does not assert global optimality over all multiplier sets.

## Profile corollary and growth

Given any `k>=2` nontrivial arm lengths, the theorem may be applied with any
one of them as `c`; taking the smallest resulting `T` is valid.  In
particular, let `d` and `L` be the minimum and maximum lengths and choose an
arm of length `d` for the closure.  With `r=k-1`,

```text
Q <= 1 + 2^(max(d-4,0)) + Lr,
K <= 3 + L(Q+r).
```

Consequently a sufficient total edge count is

```text
O(L 2^d + L^2 k).
```

For bounded shortest nontrivial arm length, this is polynomial in the
longest length and number of arms.  This is a quantitative consequence of
the self-matched normal form, not a proof that this threshold is necessary.

## Trust boundary

The proof is elementary integer arithmetic plus the cited self-matched
packing framework, whose two path templates were rechecked above.  The
standard-library program reconstructs complete labelings for a broad finite
test grid and checks the defining bijections.  Those computations are an
audit of formulas and boundary conventions; the quantified theorem rests on
the proof.
