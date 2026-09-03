# Gallai-block forcing for the Albertson `r=27` order-53 frontier

This note combines the rooted Kempe normal form with Gallai's theorem on
low vertices of a critical graph.  It gives new degree-support restrictions
and exact boundary normal forms for the three order-53 cases left by the
September 2026 Albertson reduction.  It does **not** prove Albertson's
conjecture for chromatic number 27.

A two-scale crossing argument committed while this work was in progress
eliminates the former order-54 branch without using criticality.  The same
Gallai-block calculation for that now-closed branch is retained below as a
structural corollary, but it is not part of the remaining frontier.

## Result

Let `G` be a hypothetical 27-critical counterexample in the frontier of
Sadhu, and put

```text
L = {v : d_G(v)=26},       Q = V(G)-L,
l = |L|,                  h = |Q|.
```

Thus the vertices in `Q` have degree at least 27.  Then:

| order and size | total excess `sum_v(d(v)-26)` | conclusion |
|---|---:|---:|
| `(53,713)` | 48 | `h >= 8`, hence `l <= 45` |
| `(53,714)` | 50 | `h >= 8`, hence `l <= 45` |
| `(53,715)` | 52 | `h >= 9`, hence `l <= 44` |
| `(54,726)` (now closed independently) | 48 | `h >= 10`, hence `l <= 44` |

At the minimum allowed value of `h`, considerably more is forced.  All
unions below are vertex-disjoint; a "bridge" is a single edge joining the
two displayed low cliques.  There are no other edges inside `L`.

* At `(53,713)` with `h=8`, either

  ```text
  G[L] = K22 disjoint-union K23,       G[Q] = K8 minus one edge,
  ```

  or

  ```text
  G[L] = K22 and K23 plus one bridge,  G[Q] = K8.
  ```
* At `(53,714)` with `h=8`,

  ```text
  G[L] = K22 disjoint-union K23,       G[Q] = K8.
  ```
* At `(53,715)` with `h=9`, the two large low blocks have orders either
  `22,22` or `21,23`.  If `t` is the number of bridges (necessarily 0 or
  1) and `r` is the number of missing edges in `G[Q]`, then respectively

  ```text
  (22,22): t+r=3;          (21,23): t+r=2.
  ```
* In the former `(54,726)` branch, `h=10` would force exactly one of:

  ```text
  G[L] = K21 disjoint-union K23,       G[Q] = K10;
  G[L] = K22 disjoint-union K22,       G[Q] = K10 minus one edge;
  G[L] = K22 and K22 plus one bridge,  G[Q] = K10.
  ```

The low-to-high incidences are then fixed in row sum.  A low vertex in a
clique block of order `a` has `27-a` neighbours in `Q`, except that an
endpoint of the possible bridge has `26-a`.

These normal forms are necessary conditions, not existence claims.  In
particular, criticality, connectedness of the complement, and exclusion of
a topological `K27` still have to be imposed on the remaining incidence
matrices.

## Rooted Gallai-block lemma

We use two classical facts.  First, Gallai proved that every block of the
subgraph induced by the degree-`k-1` vertices of a `k`-critical graph is a
clique or an odd cycle.  Second, Stehlik proved that, when the complement is
connected, for every vertex `v` there is a `(k-1)`-colouring of `G-v` in
which every colour class has at least two vertices.

Fix a low vertex `v`, that is, `d_G(v)=k-1`.  In a Stehlik colouring, every
colour has a unique vertex `y_i` adjacent to `v`: `v` must see every colour,
and it has exactly `k-1` neighbours.  Call a two-vertex colour class
`{y_i,x_i}` **fully low** when both its vertices belong to `L`.

For any two pair classes `i,j`, the distinguished vertices `y_i,y_j` lie in
the same component of the bichromatic graph.  Otherwise a Kempe swap on the
component containing `y_i` frees a colour at `v`.  Consequently:

* if `y_i y_j` is present, `v,y_i,y_j` form a triangle;
* if `y_i y_j` is absent, the four-vertex bichromatic graph must contain
  the path

  ```text
  y_i - x_j - x_i - y_j.
  ```

Now assume both classes are fully low.  In the first case, the two edges
`v y_i` and `v y_j` lie in one clique block of `G[L]`.  In the second case,
the displayed path together with these two edges is a 5-cycle in `G[L]`.
It lies in one block; that block cannot be a clique because `y_i y_j` is
absent, so Gallai's theorem makes it precisely this odd-cycle block `C5`.

Every edge lies in a unique block.  Hence fully-low pair classes cannot use
two different blocks through `v`: classes from different blocks have
nonadjacent distinguished vertices, and the forced 5-cycle would put their
two incident edges into the same block.  It follows that all fully-low pair
classes use one block through `v`.  If there are at least three of them,
that block is a clique and contains `v` and all their distinguished
vertices.

## From the rooted lemma to two large low blocks

Suppose first that `|G|=2k-1`.  The colouring of `G-v` consists of `k-1`
pairs.  Since there are only `h` high vertices, at least

```text
(k-1)-h
```

pairs are fully low.  When this is at least three, the rooted lemma puts
every low vertex `v` in a clique block of `G[L]` of order at least

```text
s = k-h.
```

If `|G|=2k`, the colouring has `k-2` pair classes and one triple.  Even if
all three vertices of the triple are low, at least `k-h-2` of the pair
classes are fully low.  Thus every low vertex lies in a clique block of
order at least

```text
s = k-h-1.
```

A counterexample has no `TK_k`, so every clique block has order at most
`k-1`.  In each small-`h` range used below,

```text
2(s-1) > k-1.
```

Therefore a low vertex cannot belong to two of the large clique blocks,
since its degree inside their union would already exceed `k-1`.  The large
blocks consequently partition `L`.  The same ranges satisfy `l>k-1` and
`3s>l`; hence there are exactly two such blocks.  Write their orders as
`a,b`, so `a+b=l`.

Because every remaining block of the Gallai forest can meet a large block
in at most one vertex, and the large blocks already cover `L`, the only
possible additional edge in `G[L]` is one bridge between the two cliques.
In particular there is at most one.

## Excess calculation

Put `e_L=|E(G[L])|` and `e_Q=|E(G[Q])|`.  Summing the fixed degree `k-1`
over `L` gives

```text
e(L,Q) = (k-1)l - 2e_L.
```

All excess is supported on `Q`, and therefore

```text
E := sum_v(d(v)-(k-1))
   = e(L,Q) + 2e_Q - (k-1)h.
```

The two-block structure and simplicity give

```text
e_L >= C(a,2)+C(b,2),        e_Q <= C(h,2),
```

so

```text
E <= (k-1)l - a(a-1)-b(b-1) + h(h-1) - (k-1)h.       (1)
```

For fixed `a+b=l`, the right side is maximised by the two most balanced
allowed block orders.  At `k=27`, exhaustive exact evaluation of (1) gives:

| `h` | max `E`, order 53 | max `E`, order 54 |
|---:|---:|---:|
| 2 | 26 | 2 |
| 3 | 28 | 4 |
| 4 | 30 | 8 |
| 5 | 34 | 12 |
| 6 | 38 | 18 |
| 7 | 44 | 24 |
| 8 | 50 | 32 |
| 9 | 58 | 40 |

For order 53 the `h=1` maximum is also 26.  Comparing with the required
excesses `48,50,52` proves the four lower bounds on `h`.  Keeping track of
the even deficit from (1) gives the boundary normal forms stated above.

## Reproduction

Run with CPython 3.9 or later:

```sh
python3 verify.py
```

The dependency-free verifier checks the full integer range of candidate
block orders, independently checks the balanced-pair maximizer, proves the
small-`h` block-count inequalities used in every excluded row, and derives
all boundary profiles from exact edge deficits.  It uses no solver,
randomness, floating point, generated data, or external project code.

The script verifies only the finite arithmetic after the displayed
structural proof.  The mathematical trust boundary is Gallai's block
theorem, Stehlik's colouring theorem, and Sadhu's four-case frontier.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the four surviving order/size
  regimes and exclusion of a `TK_27` from a counterexample.
* The subsequent [two-scale sampling
  lemma](../albertson_r27_order54_two_scale_sampling/README.md), for the
  independent closure of the order-54 row.
* M. Stehlik, [*Critical graphs with connected
  complements*](https://doi.org/10.1016/S0095-8956(03)00069-8), JCTB 89
  (2003), 189--194, for the all-classes-size-at-least-two colouring.
* T. Gallai, *Kritische Graphen I*, Publ. Math. Inst. Hungar. Acad. Sci. 8
  (1963), 165--192, for the low-vertex block theorem.  The exact statement
  is also reproduced as Theorem 8 in A. Kostochka's
  [survey](https://kostochk.web.illinois.edu/docs/2008/book06.pdf).
* The preceding [rooted Kempe-state
  note](../albertson_r27_kempe_states/README.md), whose local pair-pair mask
  is reproved above in the form needed here.

The Gallai and Stehlik ingredients are classical.  The contribution is their
combination through fully-low Kempe pairs, the resulting two-large-block
forcing, and its exact specialization to the three remaining order-53
regimes (together with the recorded structural corollary for the closed
order-54 row).  Targeted searches of the current Albertson and
sparse-critical literature and of the committed Discovery Net found no prior
statement of these degree-support bounds or boundary normal forms.  This is
a search-relative assessment, not a claim of historical priority.
