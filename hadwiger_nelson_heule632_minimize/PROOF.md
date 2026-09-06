# Certificate implications and exact claim scope

Let G be the 560-point graph specified by the retained labels in
`certificate.json`, with every Euclidean unit pair included as an edge.

## Exact five-chromaticity

The parent's two exact arithmetic implementations rebuild all 632 distinct
points in `Q(sqrt(3),sqrt(5),sqrt(11))^2`. After scaling coordinates by 96,
the squared distance is exactly one precisely when its radical coefficient
vector is `(9216,0,0,0,0,0,0,0)`. All unordered pairs are tested; restriction
to the published labels gives 560 vertices and 2,758 edges.

The direct CNF has four colour variables per vertex, exactly-one clauses,
and clauses forbidding equal colours on unit edges. Its triangle pins
preserve satisfiability by global colour permutation. Thus the CNF is
satisfiable exactly when G is four-colourable. The checked DRAT refutation
proves that it is not. A positive five-colouring, checked on all edges,
proves `chi(G) = 5`. Neither the exploratory selector encoding nor its
negative verdicts is a premise of this final lower bound.

## Positive certificates imply mandatory vertices

For every v in the published set M, a proper four-colouring of `G - v` is
provided by the original local witness table and separately regenerated from
public source. The checker validates each witness's exact support and every
edge. There are 492 distinct such vertices.

If a subgraph H of G omits any v in M, then H is a subgraph of `G - v`, so
that witness restricts to a proper four-colouring of H. Therefore every
non-four-colourable subgraph H contains M. Let `U = V(G) minus M`; it has
68 vertices.

Suppose G has a non-four-colourable subgraph H on at most 508 vertices.
Its vertex set contains M, so `V(H) = M union T0` for some subset T0 of U
of size at most 16. Enlarge T0 to a 16-element subset T of U. The induced
graph `G[M union T]` contains H and is still non-four-colourable.
Conversely, any non-four-colourable induced graph `G[M union T]`, with
`|T| = 16`, is a 508-vertex witness inside G. Its chromatic number is exactly
five, since the five-colouring of G restricts to it.

This proves the equivalence with the `binomial(68,16)` fixed target supports.
It does not prove that any of them is non-four-colourable, nor that all are
four-colourable. The numbers 492 and 68 concern verified witnesses and their
complement, not an assertion that U consists of dispensable vertices.

## Search and regeneration encodings

In the exploratory formula every host vertex has exactly one of four
colours, including an inactive vertex. An edge constraint is guarded by
both endpoint selectors, so it applies exactly when both vertices are
retained. Each triangle pin is guarded by its vertex selector. All selectors
are fixed by assumptions on every query. Any selected subset of the pinned
triangle is a clique, so a global palette permutation realizes the remaining
pins. Inactive vertices can be coloured arbitrarily. This proves both
directions of the selected-subgraph encoding.

The separate positive-witness regenerator instead enforces at least one
colour only when selected, at most one colour unconditionally, and forces
every colour variable false when its vertex is inactive. Edge clauses are
unconditional; an inactive endpoint makes them automatically true. This is
another complete encoding of the selected graph. Only directly checked
positive witnesses from this program are used in the family proof.

A negative exploratory query permits a provisional deletion. UNKNOWN
permits none. Positive witnesses persist under all later vertex deletions
by restriction. The optional degree-at-most-three removal rule is also
sound: any four-colouring of the remaining graph extends to that vertex
using a colour absent from its at most three neighbours. This rule was
available but never used in the recorded sweep.

The final proof and all positive checks stand independently of whether the
heuristic sweep reaches the same endpoint on another machine. The published
support and M/U partition define the theorem. The family reduction applies
only to G; it makes no statement about graphs using points deleted from the
earlier 630- or 632-point supports.
