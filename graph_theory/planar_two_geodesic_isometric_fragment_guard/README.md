# Isometric fragments give an unbounded weighted two-geodesic guard rule

All graphs are finite and simple with unit edge lengths. A singleton is a
shortest path. Vertex masses are arbitrary nonnegative real numbers. A
path or cycle `C` is **isometric in `F`** when the distance in `F`
between any two vertices of `C` equals their distance along `C`.
The word *induced* below refers to the graph on the component's vertices.

The useful invariant is **complete coverage of the heavy residual
component**. Removing paths that cover only half its mass does not
work: vertices of the original paths can return and reconnect pieces.
That error occurred in the [withdrawn eight-residual claim](../planar_two_geodesic_eight_residual/README.md).

## Metric fragment lemma

**Lemma.** Let `F` be a unit-edge graph and let `C` induce an isometric
path or an isometric cycle in `F`, of any order. Let `H` be any spanning
edge subgraph of `F`, and let `D` be a connected vertex set in `H[C]`.
At most two shortest paths in `H` have union containing *every* vertex
of `D`.

**Proof.** If `C` is a path, the connected graph `H[D]` is a contiguous
subpath of `C`; its edges survive in `H`. This subpath is shortest in
`F` by isometry, hence also in `H`.

If `C` is a cycle of length `m`, then `H[D]` is a path or a cycle.
List the `t=|D|` vertices in the order of that path, or in cyclic
order if it is a cycle. Split the list into two consecutive blocks of
sizes at most `ceil(t/2)`. Every edge within a block survives in `H`.
Each block is a cycle arc of length at most `ceil(t/2)-1`, which is at
most `floor(m/2)`. Such an arc is shortest in `C`, and is shortest in
`F` by isometry. Deleting edges cannot shorten it, so it remains a
shortest path in `H`. The two blocks cover `D`. Empty blocks are
omitted. The two-vertex path and triangle cases are included. QED.

## Protected-edge descent

**Theorem 1.** Suppose `F` has two `F`-geodesics `P,Q` such that every
component `C` of `F-(V(P) union V(Q))` satisfies one of:

1. `|C| <= 4`;
2. `|C| = 5` and `F[C]` is not complete;
3. `F[C]` is an isometric path or isometric cycle in `F`, of any order.

For **every** spanning edge subgraph `H` of `F` retaining the edges of
`P,Q`, and **every** nonnegative vertex-mass assignment, `H` has a
half-balanced separator that is the union of at most two `H`-geodesics.

**Proof.** The protected paths remain `H`-geodesics: their lengths
cannot improve when edges are deleted. Put `X=V(P) union V(Q)` and let
the total mass be `W`. If `X` is not balanced, there is a unique
component `D` of `H-X` with mass greater than `W/2`. It lies within
one component `C` of `F-X`.

When `|D|<=4`, pair its vertices and join the pairs by shortest paths
in `H`, allowing a singleton. When `|D|=5` and `C` has order five,
`H[D]` is connected and noncomplete. Choose an induced three-vertex
path in `H[D]`; it is an ambient `H`-geodesic because its ends are
nonadjacent. Join the remaining two vertices by an `H`-geodesic.
If `C` is a metric fragment, apply the lemma to `D` instead; this
also handles larger `D`. In each case the replacement paths cover
**all** of `D`. Every component left after removing them has mass at
most `W-w(D)<W/2`, even if their paths pass through `X` or other
fragments. QED.

Thus this witness-edge template can terminate a deletion branch once
it finds such protected paths. It has no claim for edge deletions that
remove one of their edges.

## Dynamic guard without protected edges

**Theorem 2.** Let `G` be any unit-edge graph with a set `S` of at most
four vertices. Suppose each component `C` of `G-S` is either of order
at most four, of order five and noncomplete, or induces an isometric
path or isometric cycle in `G` (with no order bound). Then, for **every**
spanning edge subgraph `H` of `G` and **every** nonnegative vertex-mass
assignment, `H` has a half-balanced separator equal to at most two
`H`-geodesics.

**Proof.** Let `W` be the total mass. If no component of `H` has mass
greater than `W/2`, use the empty separator. Otherwise take its unique
heavy component `K`. Pair the vertices of `S intersect K`, and cover
them with at most two `H`-geodesics (a singleton handles an odd final
vertex). If this primary pair is unbalanced, its unique heavy residual
component `D` lies within a component `C` of `G-S`. Apply the same
complete-coverage argument as in Theorem 1, using the metric fragment
lemma when appropriate. Removing the replacement pair leaves total
mass at most `W-w(D)<W/2`. QED.

For planar `G`, an order-five component is automatically noncomplete.
The theorem is an all-spanning terminal rule for [witness-edge
descent](../planar_two_geodesic_edge_deletion16/README.md). It extends
the [four-vertex, five-fragment rule](../planar_two_geodesic_four_guard/README.md)
by allowing unbounded metric fragments. It is separate from the
[robust six-fragment classification](../planar_two_geodesic_six_fragment_guard/README.md):
that result also permits some six-vertex graphs that are not metric
paths or cycles.

## Biconnected planar graphs with arbitrarily large fragments

Start with the octahedron: equatorial cycle `0-1-2-3-0`, and
nonadjacent poles `4,5` joined to all four equator vertices. Inside a
face incident with edge `01`, add vertex-disjoint cycles
`C_{m_1},...,C_{m_r}`, with each `m_i>=3`. Label the vertices of each
cycle in cyclic order `a,...,f`, where `a,f` are adjacent, and add
attachment edges `0a,1f`. Place each gadget in the remaining face
incident with `01` before inserting the next. Call the graph
`G(m_1,...,m_r)`.

It has `6+sum(m_i)` vertices, `12+sum(m_i+2)` edges, and `8+2r`
faces. This insertion is planar. It is biconnected: deleting a core
vertex leaves the core connected and each gadget attached through at
least one of `0,1`; deleting a gadget vertex leaves the remaining
cycle path attached to the core through at least one of `a,f`.

Each gadget cycle is isometric in the whole graph. Any route that
leaves it must exit and reenter at `a` or `f`. An excursion between
the same endpoint can be removed; one between different endpoints
has length at least three via `a-0-1-f`, while the cycle has edge
`af` of length one. Thus no shortest route needs to leave the cycle.

The guard `S={0,1,2,3}` leaves the two poles as singletons and all
the isometric cycles as components. Theorem 2 applies for any number
and any lengths of gadgets. For `r>=5` with every `m_i>=7`, **no**
four-vertex set can leave only components of order at most six: four
deleted vertices meet at most four vertex-disjoint gadget cycles, so
one full cycle remains in a component of order at least seven. Thus
this family lies strictly beyond both earlier bounded-fragment guard
criteria. The graphs still contain the octahedron, so their treewidth
is at least four.

## Reproduce and scope

From the repository root, with Python 3.11 or later and no packages:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_isometric_fragment_guard/verify.py
```

The checker audits all connected edge/vertex restrictions of cycles
of orders 3 through 9 against the two-arc construction. It also checks
an explicit spherical rotation system, the formulas, biconnectivity,
guard components, and all-pairs isometry for several finite tuples,
including `(7,8,9,10,11)` and `(3,7,12,20,50)`.
Expected summary:

```text
connected restrictions by cycle order: [(3, 40), (4, 117), (5, 306), (6, 751), (7, 1772), (8, 4073), (9, 9190)]
lengths=(3,) vertices=9 edges=17 faces=10 planar=yes biconnected=yes isometric=yes
lengths=(6,) vertices=12 edges=20 faces=10 planar=yes biconnected=yes isometric=yes
lengths=(7,) vertices=13 edges=21 faces=10 planar=yes biconnected=yes isometric=yes
lengths=(7, 8, 9, 10, 11) vertices=51 edges=67 faces=18 planar=yes biconnected=yes isometric=yes
lengths=(3, 7, 12, 20, 50) vertices=98 edges=114 faces=18 planar=yes biconnected=yes isometric=yes
lengths=(7, 7, 7, 7, 7) vertices=41 edges=57 faces=18 planar=yes biconnected=yes isometric=yes
PASS
```

These finite audits catch construction mistakes; the universal
weighted statements and arbitrary-order family follow from the
written proofs. No result here settles
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf),
and no claim is made for arbitrary positive edge lengths.
