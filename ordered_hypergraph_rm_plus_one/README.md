# The first overfull case of the ordered pattern-clique extremal conjecture

## Result

Let `P` be an `r`-partite `r`-pattern, let `P^(m)` be its ordered
`P`-clique of size `m`, and let `ex_<(n,P^(m))` be the maximum number of
edges in an ordered `r`-graph on `[n]` containing no ordered copy of
`P^(m)`.  Then, for every `r,m >= 1`,

```text
ex_<(rm+1,P^(m)) = binom(rm+1,r) - (r+1).                 (1)
```

Together with the immediate cases `n < rm` and `n = rm`, this verifies
Anastos--Jin--Kwan--Sudakov Conjecture 1.20 throughout the initial range
`n <= rm+1`.  The published conjecture predicts

```text
ex_<(n,P^(m))
  = binom(n,r) - binom((n-r(m-1))_+,r)
```

for every `n`; (1) is its first nontrivial overfull boundary case.

## Canonical copies on `rm+1` vertices

Normalize the two edges of `P` so that its first block is `AB`.  Encode its
`r` consecutive two-vertex blocks by signs

```text
epsilon_1 = +1,
epsilon_i in {+1,-1}.
```

For `1 <= i <= r` and `1 <= j <= m`, put

```text
p_i(j) = j              if epsilon_i = +1,
         m+1-j          if epsilon_i = -1,
b_i(j) = (i-1)m+p_i(j).
```

The canonical `P`-clique on `[rm]` has edges

```text
B_j = {b_i(j): 1 <= i <= r},       1 <= j <= m.
```

Set `N=rm+1`.  For each `x in [N]`, let

```text
phi_x(t) = t              if t < x,
           t+1            if t >= x.
```

The unique `P`-clique `C_x` on `[N] minus {x}` has the `m` edges
`phi_x(B_j)`.  If an ordered `r`-graph `G` is `P^(m)`-free and `D` is the
set of its missing edges, then

```text
D meets E(C_x) for every x in [N].                         (2)
```

We prove that (2) forces `|D| >= r+1`.

## Upper bound: a nonconstant orientation vector

First suppose that the signs `epsilon_i` are not all equal.  For
`q=0,...,r`, consider the `r+1` canonical copies with omitted vertices

```text
x_q = qm+1.
```

Their `j`th edges are

```text
E_(j,q) = {b_i(j) + 1[i>q] : 1 <= i <= r}.                (3)
```

These `r+1` matchings have pairwise disjoint edge sets.  Indeed, suppose
`q<q'` and `E_(j,q)=E_(k,q')`.  Equality of the increasingly ordered
coordinates in (3) gives

```text
p_i(j) = p_i(k)       for i <= q or i > q',
p_i(j)+1 = p_i(k)     for q < i <= q'.                    (4)
```

The second line forces `k=j+1` in a `+1` block and `k=j-1` in a `-1`
block.  If there is an index outside `(q,q']`, the first line instead
forces `k=j`, a contradiction.  The only remaining possibility is
`q=0, q'=r`; then the second line of (4) requires all block signs to be
equal, again a contradiction.

Thus a missing edge can meet at most one of these `r+1` canonical copies.
Condition (2) therefore needs at least `r+1` missing edges.

## Upper bound: the all-forward pattern

It remains to consider `epsilon_i=+1` for every `i`.  Here

```text
b_i(j)=(i-1)m+j.
```

For `q=0,...,r`, define

```text
E_(j,q) = {b_i(j)+1[i>q] : 1 <= i <= r},
b_0(j)=0,  b_(r+1)(j)=N.
```

The `j`th edge of `C_x` equals `E_(j,q)` precisely when

```text
b_q(j) < x <= b_(q+1)(j).                                 (5)
```

For `0<q<r`, the interval in (5) has length `m`.  The only duplicated
representations with different `q` are

```text
E_(j,0)=E_(j+1,r),       1 <= j < m.
```

The two corresponding endpoint intervals have total length

```text
j + (m-j) = m.
```

The two unpaired endpoint representations also have intervals of length
`m`.  Consequently every missing edge belongs to at most `m` of the
`N=rm+1` canonical copies.  Any `r` missing edges meet at most `rm<N`
copies, so (2) again implies `|D|>=r+1`.

## Matching construction

For completeness, the lower-bound construction can be described directly.
Let the two edges of `P` be `A,B`, with `A[1]<B[1]`.  For `i<r`, let `s_i`
be the number of vertices of `B` strictly between `A[i]` and `A[i+1]`, and
let `s_r` be the number after `A[r]`.  Thus

```text
s_1+...+s_r=r.
```

Include an `r`-set `e={e[1]<...<e[r]}` in `G_0` if

```text
e[i+1]-e[i] <= s_i(m-1)        for some i<r,
```

or if

```text
e[r] >= N-s_r(m-1)+1.
```

In a hypothetical `P`-clique with edges ordered by their first vertices,
all the other `m-1` edges force the first edge to violate every displayed
membership condition.  Hence `G_0` is `P^(m)`-free.

Its nonedges satisfy the reverse strict gap conditions.  The shift

```text
y_i=e[i]-(m-1)(s_1+...+s_(i-1))
```

is a bijection from those nonedges to the `r`-subsets of
`[N-r(m-1)]=[r+1]`.  Therefore `G_0` has exactly `r+1` missing edges.  This
matches the upper bound and proves (1).

## Exact verification

`verify.py` independently constructs the canonical copies from their vertex
sets, derives the lower-bound parameters from the two-edge pattern, and uses
exact finite enumeration to check:

- every canonical object is a matching with the required vertex set;
- the construction has exactly `r+1` nonedges and avoids every canonical
  copy;
- the selected `r+1` matchings have pairwise disjoint edge sets for every
  nonconstant orientation vector; and
- every edge occurs in at most `m` canonical copies in the all-forward case.

It checks all normalized block patterns for `1 <= r,m <= 5` using only the
Python standard library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ordered_hypergraph_rm_plus_one/verify.py
```

Expected final lines:

```text
checked_parameter_pairs=25
checked_normalized_patterns=155
max_r=5 max_m=5
record_sha256=85271763769e03fb770543bd4080010e969aa725f0903a6c600ead9fcd7ff3da
status=VERIFIED
```

The computation is corroborative.  The theorem is the ordinary argument
above and does not depend on Python, a solver, randomized testing, or
floating-point arithmetic.

## Literature and scope

The problem and lower-bound construction are from Michael Anastos, Zhihan
Jin, Matthew Kwan, and Benny Sudakov, *Extremal, enumerative and
probabilistic results on ordered hypergraph matchings*, Forum of Mathematics,
Sigma 13 (2025), e55:

- https://doi.org/10.1017/fms.2024.144
- https://arxiv.org/abs/2308.12268

The final paper states the exact formula as Conjecture 1.20 and proves the
matching general lower bound in Theorem 1.18(1).  Targeted searches of the
paper's citations and later literature on ordered hypergraph matchings found
no treatment of the `n=rm+1` boundary.  Thus the result is apparently new to
the searched sources, not a historical priority claim.  It does not settle
the conjecture for `n>=rm+2`.
