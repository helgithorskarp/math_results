# The four-module obstruction

## Statement

Let `k<=4`. For each i, let Vi be a finite set of distinct plane points and
Ti a designated subset with at least two points. Assume:

1. Every two distinct points of Ti have Euclidean distance strictly greater
   than two.
2. Every assignment of four colours to Ti that is not monochromatic extends
   to a proper four-colouring of the strict unit-distance graph on Vi.
3. For i distinct from j, `Vi intersect Vj` is contained in `Ti intersect Tj`.
4. Every unit edge of the strict graph on `V=union Vi` that is not internal
   to any Vi has both endpoints in `T=union Ti`.

Then the strict unit-distance graph on V is four-colourable. There is no
vertex-count bound, restriction on the number of terminals in a module,
coordinate field, denominator, orientation, or translation. Terminals may
coincide between modules. No additional connector points occur in V.
The hypotheses exclude overlaps and additional edges involving private
interiors. Four-colourability of the individual modules alone does not
replace hypothesis 2.

## Auxiliary graph and its degree

Choose any pair of distinct terminals in each Ti. Let L be the set of these
unordered pairs, identifying repetitions, and U the strict unit graph on T.
A chosen pair has length greater than two, so L and U are disjoint. Form the
simple auxiliary graph H with edges U union L. Edges in L are colour
inequalities, not physical unit edges.

Fix x in T, and let r be the number of terminal sets containing x. There is
no unit neighbour of x in any such set. Each other terminal set contains
at most one unit neighbour: if it contained y and z, then
`|y-z|<=|y-x|+|x-z|=2`, contradicting hypothesis 1. Consequently

```
d_U(x) <= k-r <= 3.
```

This remains valid with overlapping terminal sets: counting a neighbour in
several sets only increases the upper bound. At most r selected pair edges
are incident with x, so

```
d_H(x) <= (k-r)+r = k <=4.
```

The first inequality, `d_U<=3`, supplies a compact alternative to invoking
Brooks' theorem in the next step.

## A geometric K5 needs at least six long edges

Consider five distinct plane points for which every pair has either distance
one or distance greater than two. Mark the corresponding complete graph U/L.
A triangle cannot have exactly two U edges: their endpoints are at distance
at most two, so its remaining edge cannot be L. Thus the U relation is
transitive after adjoining equality. Its components are complete graphs.

At most three distinct plane points can have all mutual distances one.
To see this, normalize two points to `(0,0),(1,0)`. Every further point must
be one of `(1/2,+sqrt(3)/2),(1/2,-sqrt(3)/2)`. Those two points are at distance
sqrt(3), not one. Hence every U component has size at most three.

Partitioning five points into blocks of size at most three gives at most
four U edges, attained by block sizes 3+2. Of the ten complete-graph edges,
at least six must therefore be L. In H there are at most four L edges in
all, so **H contains no K5**, even as a noninduced subgraph.

The bound six is sharp for this geometric statement: take a unit triangle
and a distant unit pair. Four pairs are unit and all six cross pairs are
long. Their augmented K5 is an auxiliary graph, not a physical unit graph.
The same exclusion of K5 also holds when at most five long edges are added;
this observation alone does not settle the five-module case.

## A finite four-colouring proof

Repeatedly remove a vertex of current degree at most three from H. If the
remaining graph R is nonempty, it is 4-regular, since H has maximum degree
four. Every vertex of R is incident with an L edge: its U degree is at most
three, including before removal. As L has at most four edges,

```
|V(R)| <= 2|L| <=8.
```

Any simple 4-regular graph has at least five vertices. The following finite
positive check covers all possible orders of R:

| Order | Labelled 4-regular graphs | Explicitly four-coloured | K5 exceptions |
|---:|---:|---:|---:|
| 5 | 1 | 0 | 1 |
| 6 | 15 | 15 | 0 |
| 7 | 465 | 465 | 0 |
| 8 | 19,355 | 19,355 | 0 |

`kernel.py` generates these graphs by selecting each vertex's later
neighbours with exact residual-degree constraints. Every labelled graph has
one such sequence, so there is no isomorphism or sampling assumption.
It finds a colouring by partitioning vertices into nonadjacent pairs, with
one singleton when necessary. Every resulting colour word is directly
checked. The only uncoloured graph is the geometrically excluded K5.

The independent `audit_kernel.py` proves coverage differently. It computes
the coefficient

```
[x_0^(n-5) ... x_(n-1)^(n-5)] product_(i<j)(1+x_i*x_j)
```

to count all labelled complements without enumerating those graphs. It
constructs a positive covering set separately: perfect matchings at n=6,
cycle covers at n=7, and edge-disjoint unions of a perfect matching and a
cycle cover at n=8. Each resulting complement has the required degree, and
its matching supplies the colour pairs in the original graph. The number
of distinct generated complements equals the independent polynomial count,
so none is omitted. Sorted graph-set hashes agree entry for entry with the
first enumeration. Neither checker imports the other.

The K5 marking lemma is also audited twice: all 1,024 ten-edge masks are
filtered by the no-two-U triangle condition and the unit K4 exclusion;
independently, all equivalence partitions into blocks of size at most three
are generated. Their 46 surviving masks agree exactly. Their long-edge
histogram is `{6:10,7:10,8:15,9:10,10:1}`.

Colour R using its checked finite witness. Reinsert removed vertices in
reverse order. Each has at most three already coloured neighbours and
therefore an available fourth colour. This constructs a proper
four-colouring of H. A short alternative is Brooks' classical theorem
(maximum degree four and no K5 component), but the finite proof above does
not assume that theorem or an external graph catalogue.

## Lifting and quantitative consequences

The H colouring is proper on every terminal unit edge. Since a selected
pair in each Ti has different colours, each Ti is non-monochromatic.
Hypothesis 2 extends the colouring through each Vi. The extensions agree
on shared points by hypothesis 3. Internal edges are proper in their own
module, and every additional edge is proper in H by hypothesis 4. This
proves the full strict physical graph is four-colourable.

Thus **every non-four-colourable assembly satisfying the other hypotheses
needs at least five modules**. This rules out the four-module architecture
even if each module is greatly reduced. In particular, deleting private
vertices from a module preserves its positive extension property by
restriction, so such reductions cannot defeat the four-module theorem.
No claim is made that the reduced module retains a negative forcing property.

For the archived Parts A159 and B214 modules, the exact source check gives:

| Module | Private vertices | Terminal geometry | Positive assignments checked |
|---|---:|---|---:|
| A159 | 156 | equilateral triangle of side sqrt(7) | all 60 nonmono assignments |
| B214 | 212 | pair at distance 3 | all 12 unequal assignments |

Interiors are disjoint by hypothesis 3. Any assembly with an A module and
at least five modules has at least `5*156+3=783` points. If all modules are B,
it instead has at least `5*212+2=1062` points. Consequently **every
non-four-colourable full-A159/B214 terminal-only assembly has at least 783
vertices**. This is an architecture-specific necessary bound, not a lower
bound for arbitrary unit-distance graphs or a claim of attainability.

For five modules, the sharper bounds by number of B copies are respectively
783, 840, 896, 952, 1008, and 1062. In a mixed assembly the terminal union has
at least four points, because a distance-three pair cannot be contained in
an equilateral sqrt(7) triple.

For arbitrary replacement modules within this architecture, a
non-four-colourable assembly on at most 508 vertices must contain **at least
five modules and some module with at most 101 private vertices**: otherwise
its private vertices alone number at least `5*102=510`. These conditions are
necessary only. They provide no positive candidate, sufficiency claim, or
lower bound outside the stated architecture.
