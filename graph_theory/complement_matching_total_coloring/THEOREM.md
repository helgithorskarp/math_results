# A complement-matching total-colouring theorem

All graphs are finite and simple.  A total colouring assigns colours to all
vertices and edges so that adjacent vertices, adjacent edges, and incident
vertex-edge pairs receive different colours.  Its minimum number of colours
is `chi''(G)`.

## Theorem

Let `G` have even order `2r`, where `r>=3`.  If the complement of `G`
contains a perfect matching, then

```text
chi''(G) <= 2r-1.                                      (1)
```

Consequently, if `Delta(G)=2r-2`, then

```text
chi''(G)=Delta(G)+1=2r-1.                              (2)
```

The order-four analogue of (1) is false: `C_4` has a perfect matching in
its complement but has total chromatic number four.

## Transfer lemma

Suppose a proper edge colouring `phi` of `K_(2r)` with `2r-1` colours has a
perfect matching `M` whose `r` edges have pairwise different colours.  Let
`H` be any spanning subgraph of `K_(2r)-M`.  Keep `phi` on the edges of `H`.
For a vertex `v`, let `m(v)` be its edge of `M` and set

```text
c(v)=phi(m(v)).
```

This is a total colouring of `H`.  Indeed:

- retained adjacent edges have different colours because `phi` is proper;
- an edge incident with `v` has colour different from `phi(m(v))`, since it
  and `m(v)` are adjacent in `K_(2r)`;
- adjacent vertices of `H` lie in different edges of `M`, and the matching
  is rainbow, so their vertex colours differ.

Thus it remains only to exhibit such a rainbow matching in one
one-factorization of every `K_(2r)`, `r>=3`.

## Cyclic one-factorization

Put `q=2r-1` and use the vertex set

```text
{infinity} union Z_q.
```

Colour `infinity--a` by `a`.  For distinct `u,v` in `Z_q`, colour `uv` by

```text
(u+v)/2 mod q,                                         (3)
```

where division by two is valid because `q` is odd.  At a finite vertex `u`,
the finite-edge colours are all residues except `u`, and the edge to
`infinity` has colour `u`.  At `infinity`, all colours occur once.
Therefore (3) is a proper `(2r-1)`-edge colouring of `K_(2r)`, equivalently
a one-factorization.

We next give a rainbow perfect matching in this factorization.

### Odd `r`

Write `r=2m+1`.  Take

```text
{infinity,0}, {1,2}, {3,4}, ..., {4m-1,4m}.             (4)
```

The non-infinite edge indexed by `k=1,...,2m` has doubled colour
`4k-1` modulo `q=4m+1`.  These colours are distinct because four is
invertible modulo `q`.  None is zero: in the relevant range the only
possible positive multiple of `q` is `q` itself, but
`4k-1=4m+1` has no integer solution.  Hence (4) is rainbow.

### The case `r=4`

For `q=7`, take

```text
{infinity,0}, {1,3}, {2,6}, {4,5}.
```

Their colours are respectively `0,2,4,1`.

### Even `r>=6`

Write `r=2m`, where `m>=3`, so `q=4m-1`.  Take the following edges:

```text
{infinity,0};
{2k-1,2k}                         for 1<=k<=m-1;
{2m-1,2m+1};
{2m+2t,2m+3+2t}                   for 0<=t<=m-4;
{4m-6,4m-2};
{4m-4,4m-3}.                                          (5)
```

The middle range is empty when `m=3`.  The displayed pairs partition all
vertices.  Their colours, in the same order, form the disjoint sets

```text
{0},
{2m+1,2m+3,...,4m-3},
{2m},
{2,4,...,2m-6},
{4m-4},
{2m-3}.                                                (6)
```

To verify (6), double every claimed colour and compare it with the sum of
the corresponding endpoints modulo `4m-1`.  The sets in (6) are visibly
disjoint, so (5) is rainbow.  This completes the construction for every
`r>=3`.

Now let `M` be a perfect matching in the complement of `G`.  Relabel the
vertices so that `M` is the rainbow matching just constructed and apply the
transfer lemma, proving (1).  If `Delta(G)=2r-2`, a maximum-degree vertex
together with its incident edges is a set of `Delta(G)+1` pairwise
conflicting elements in every total colouring.  This proves the lower bound
in (2), and hence equality.

## Thick-spider corollary

For `r>=2`, let `S_r` have clique

```text
X={x_0,...,x_(r-1)}
```

and stable set

```text
Y={y_0,...,y_(r-1)},
```

where `x_i y_j` is an edge if and only if `i!=j`.  Its complement contains
the perfect matching `{x_i y_i}`, and every `x_i` has degree `2r-2`.
Thus the theorem gives

```text
chi''(S_r)=2r-1                                       (7)
```

for `r>=3`.  For `r=2`, the graph is the path with edge order
`x_0y_1, x_0x_1, x_1y_0`.  One three-total-colouring gives vertex colours

```text
c(x_0)=0, c(x_1)=1, c(y_0)=c(y_1)=2
```

and edge colours `1,2,0` in that order.  Since its maximum degree is two,
the usual `Delta+1` lower bound proves (7) also for `r=2`.

When `r>=3`, `S_r` has no pendant vertex and no universal vertex.  The
known stretch-index characterization of split graphs therefore puts it in
the `sigma=3` class, rather than the already classified `sigma=2` class.

## Trust boundary

The theorem is the elementary construction and transfer proof above.  The
standard-library checker directly verifies all incidence constraints,
matching formulas, and boundary conventions, but finite checks do not prove
the quantified statement.  No solver, random sampling, floating point,
external dataset, or omitted certificate is used.
