# Degree feasibility and the free50 covering certificate

Let G be the exact 560-point unit-distance graph specified by the parent
certificate. Its vertices are partitioned as M union U, where `|M|=492` and
`|U|=68`. Each v in M has a verified proper four-colouring of `G-v`.

## Necessary conditions for a target obstruction

Any non-four-colourable subgraph of G must contain M: otherwise it is a
subgraph of one of the positively coloured `G-v`. If such a graph has at
most 508 vertices, choose a vertex-minimal non-four-colourable subgraph K.
It still contains M and is five-chromatic because G is five-colourable.
Every vertex of K has degree at least four. Indeed, after deleting a vertex
of degree at most three, minimality gives a four-colouring; one of the four
colours is absent from its neighbours and restores that vertex, a contradiction.

Thus K has vertex set `M union T` for `T subset U`, `|T|<=16`, and the
induced graph on that vertex set has minimum degree at least four. This is
a necessary condition for the existence of a target obstruction. Minimum
degree four is not asserted for every non-four-colourable supergraph.

## Exact selector form and its feasible subfamily

Write `b(v)=|N_G(v) intersect M|` and `r(v)=max(0,4-b(v))`. A selection T
has the required minimum degree exactly when

```text
|N_G(v) intersect T| >= r(v)             for every v in M,
v in T implies |N_G(v) intersect T| >= r(v)  for every v in U.
```

These equations simply partition each selected vertex's neighbours into
mandatory and selected optional neighbours. Add the constraint `|T|<=16`.

The exact coordinate/edge computation gives `r(v)=0` for all v in M.
Let `F={v in U : r(v)=0}` and `D=U minus F`. The certificate checks
`|F|=50`, `|D|=18`, with 11 requirements of one, six of two, and one of three
on D. All D vertices are fresh completion centres.

For every `T subset F`, all selected vertices already have at least four
neighbours in M, so the degree conditions hold. In particular the empty
selection is feasible, as are selections of every cardinality from zero
through 16. The degree/cardinality system is satisfiable; a global
infeasibility certificate for it cannot exist. This observation does not
decide colourability.

## One positive graph closes the subfamily

Set `A=G[M union F]=G-D`. Its 542 exact distinct points induce exactly
2,672 unit edges. The public 632-position colour string uses colours
0 through 3 at precisely these points. The verifier checks the exact
support, alphabet and all 2,672 edge inequalities. Hence A is four-colourable.

Every subgraph of A inherits that colouring. In particular all `2^50`
choices `M union T`, `T subset F`, are four-colourable. Exactly

```text
binomial(50,16) = 4923689695575
```

of these have 508 vertices, and

```text
sum_{k=0}^{16} binomial(50,k) = 8639411571051
```

have at most 508 vertices while containing M. These counts describe labelled
subsets of a fixed graph. Their colourability follows by restriction, not
by enumerating them or quotienting by automorphisms.

Conversely, any non-four-colourable subgraph of G must contain a vertex of D;
otherwise it is a subgraph of A. Together with the parent mandatory-vertex
lemma, the exact remaining target family can be restricted to `M union T`
with `|T|=16` and `T intersect D` nonempty. The usual enlargement argument
from a smaller non-four-colourable subgraph to size 508 remains valid and
preserves this intersection. No assertion of colourability or
non-four-colourability is made for the remaining members.

## Exactness and certificate trust

All host coordinates are coefficient vectors in the basis of
`Q(sqrt(3),sqrt(5),sqrt(11))`. Multiplying coordinates by 96 gives integer
coefficients; a squared distance is one exactly when the scaled square has
coefficient vector `(9216,0,0,0,0,0,0,0)`. Basis independence justifies this
coefficient comparison and distinctness test. Every host point pair is
tested before restriction to A.

Kissat only discovered the positive colour string. Its verdict is not needed
once the certificate is checked against the independently reconstructed
graph. The actual proof therefore has no SAT infeasibility trust boundary
and requires no DRAT trace. The unused conditional negative branch in the
frozen plan cannot create a claim about an unqueried graph.
