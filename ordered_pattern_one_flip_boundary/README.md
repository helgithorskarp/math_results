# The one-flip `rm+2` boundary for ordered pattern cliques

## Result

Let `r,m >= 2`, let `P` be an `r`-partite `r`-pattern, and normalize its
block-orientation word so that its first sign is positive.  Suppose that the
word has exactly one sign change, after block `t`:

```text
epsilon_1 = ... = epsilon_t = +1,
epsilon_(t+1) = ... = epsilon_r = -1,
```

where `1 <= t < r`.  Then

```text
ex_<(rm+2, P^(m)) = C(rm+2,r) - C(r+2,r).
```

Thus Conjecture 1.20 of Anastos--Jin--Kwan--Sudakov is exact at the
`rm+2` boundary for every one-flip pattern.  Together with the earlier
edge-disjoint packing argument for words with at least two flips, this gives
the conjectured value at `rm+2` for every nonconstant block-orientation word.
The only orientation type not covered by those two arguments at this
boundary is the constant (all-forward) word.

The cases `r=2` and `m=2` were already consequences of results in the
primary paper.  The new range of the theorem is `r,m >= 3`.

## Definitions and blocker reformulation

On `[rm]`, the rank-`j` edge of `P^(m)` is

```text
b_i(j) = (i-1)m + j             for i <= t,
b_i(j) = (i-1)m + (m+1-j)       for i > t.
```

At `N=rm+2`, an order-preserving copy is uniquely determined by the two
vertices omitted from `[N]`: apply the increasing bijection from `[rm]` to
the remaining vertices to all `m` base edges.

A set `D` of `r`-edges is a *blocker* if it meets every such copy.  The
complement of a `P^(m)`-free ordered hypergraph is a blocker and conversely,
so the claimed extremal equality is equivalent to saying that the minimum
blocker size is

```text
B = C(r+2,r) = C(r+2,2).
```

The lower-bound construction from Theorem 9.1 of the primary paper supplies
a blocker of size `B`.  In the present one-flip normalization it is the set
of increasing `r`-tuples `e` satisfying

```text
e[i+1]-e[i] > (m-1)(1 + 1_(i=t))    for 1 <= i < r.
```

Indeed, put

```text
y_i = e_i - (m-1)((i-1) + 1_(i>t)).
```

This is a bijection from those edges to the `r`-subsets of `[r+2]`.  The
first-by-first-coordinate edge of every copy lies in this blocker.  Indeed,
each of the other `m-1` copy edges puts one vertex in every successive gap
of that first edge, except that it puts two vertices in the flip gap and no
vertex after the last coordinate.  Thus those gaps contain respectively
`m-1` and `2(m-1)` intervening vertices.  This is the specialized gap-count
argument of Theorem 9.1.  It remains to prove that no blocker has size at
most `B-1`.

## Selected copies and their only collisions

Index weak compositions `mu=(mu_0,...,mu_r)` of 2 by their weakly
increasing two-term form `q_1 <= q_2`.  Select the copy `C_mu` whose omitted
vertices are

```text
q_1 m + 1,  q_2 m + 2.
```

There are exactly `B` selected copies.  If `E_(j,mu)` is the rank-`j` edge
of `C_mu`, then

```text
E_(j,mu)[i] = b_i(j) + sum_(h<i) mu_h.
```

Let `e_h` denote the unit vector in composition coordinate `h`, and set

```text
delta = e_0 + e_r - 2e_t.
```

Taking successive differences of the insertion counts gives the exact
collision criterion

```text
E_(j,mu) = E_(k,nu)  iff  nu-mu = (j-k) delta.          (1)
```

Both compositions have mass 2.  Therefore (1) permits only the following
collisions between distinct selected labels:

```text
alpha = e_0 + e_r,
beta  = 2e_t,
z_b = E_(b,alpha) = E_(b+1,beta),    1 <= b < m.       (2)
```

All other edges of all selected copies are private to their selected copy.

Suppose that a blocker `D` has size at most `B-1`.  It must hit the `B`
selected copies.  The only way to do that is:

- `|D|=B-1`;
- `D` contains exactly one bridge `z_b` from (2); and
- for every `mu` other than `alpha,beta`, `D` contains exactly one edge
  `E_(a_mu,mu)` of `C_mu`.

This is just the equality case of counting covered selected copies: one
bridge covers `C_alpha,C_beta`, while every other available edge covers at
most one selected copy.

## The bridge-chain contradiction

Fix the bridge index `b` forced above.  Define a path of compositions

```text
nu_q = e_q + e_r                  for 0 <= q <= t,
nu_q = e_t + e_(r+t-q)            for t <= q <= r.
```

Thus `nu_0=alpha` and `nu_r=beta`.  For `1 <= q < r`, write `a_q` for the
unique rank selected by `D` in `C_(nu_q)`.

For `1 <= q <= r`, define a further canonical copy `K_q` by its omitted
pair:

```text
{(q-1)m+b+1, N}                    if 1 <= q <= t,
{tm+1, N-(q-t-1)m-b}               if t < q <= r.       (3)
```

The increasing-complement map in (3) gives the following identity for
every rank `j`:

```text
rank-j edge of K_q = E_(j,nu_q)       if j <= b,
rank-j edge of K_q = E_(j,nu_(q-1))   if j > b.          (4)
```

For completeness, when `q<=t` the first omitted vertex lies in positive
block `q`; it shifts that block exactly when `j>b`, and the omission at `N`
never shifts a base vertex.  When `q>t`, the first omission shifts every
block after `t`, while the source threshold for the second omission lies in
negative block `r+t-q+1`; it shifts that block exactly when `j<=b`.  These
two insertion-count statements are precisely (4).

No `K_q` contains `z_b`: `K_1` uses `alpha` only at ranks above `b`, and
`K_r` uses `beta` only through rank `b`.  Hence hitting `K_1` forces
`a_1<=b`.  For `1<q<r`, hitting `K_q` forces

```text
a_q <= b  or  a_(q-1) > b.
```

Induction yields `a_q<=b` for all `q<r`.  But hitting `K_r` requires
`a_(r-1)>b`, a contradiction.  Thus every blocker has size at least `B`.
Together with the explicit blocker above, this proves the theorem.

## Scope and literature status

The primary source is Michael Anastos, Zhihan Jin, Matthew Kwan, and Benny
Sudakov, *Extremal, enumerative and probabilistic results on ordered
hypergraph matchings*, Forum of Mathematics, Sigma 13 (2025), e55
([DOI](https://doi.org/10.1017/fms.2024.144),
[open manuscript](https://arxiv.org/abs/2308.12268)).  Its Theorem 1.18(1)
gives the construction used above, and its Conjecture 1.20 proposes the
formula for all `r`-partite patterns and all parameters.

A targeted primary-literature and web search through 2026-09-20 found no
later proof of this one-flip `rm+2` boundary.  That is a search-relative
status statement, not a claim of priority.  This note does not settle the
constant-orientation case at `rm+2`, or the conjecture at larger excess.

## Reproduction

Requires only Python 3.11 or later and uses exact integer and set operations.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
sha256sum -c SHA256SUMS
```

The checker reconstructs canonical copies directly from every omitted pair
for all `2 <= r,m <= 7` and every flip location.  It independently verifies
the paper's blocker, the selected-copy encoding, the complete collision
criterion, the bridge classification, and all bridge-chain identities.  It
then compares a deterministic summary with `EXPECTED.json`.

The finite audit corroborates the definitions and identities; the
parameter-uniform proof above establishes the theorem.
