# Exact block factorization for color-matching Hamilton cycles

All graphs are finite and simple.  A **Barnette graph** here is a cubic,
bipartite, 3-connected graph with a fixed embedding in the sphere.  Properly
color its faces red, blue and green; adjacent faces receive different
colors.  Color each primal edge by the color missing from its two incident
faces.  Each edge-color class is a perfect matching.  Write `M_g` for the
green matching and

```text
D = G*[B union F]
```

for the subgraph of the dual induced by the blue and green faces.  Thus `D`
is connected and bipartite.  Let `A(D)` denote its articulation vertices and
let `B_2(D)` be its non-bridge blocks.  For `K in B_2(D)`, define

```text
lambda_F(K) = number of X subset (F intersect (V(K)-A(D)))
              for which K-X is a tree.
```

## Theorem

The number of Hamilton cycles of `G`, counted as edge sets, that contain
every edge of `M_g` is exactly

```text
                 product lambda_F(K).                    (1)
                   K in B_2(D)
```

Thus the color-matching Hamilton-cycle problem factors exactly over the
blocks of the bicolored dual.  Green articulation faces are forced; all
remaining choices are independent within their unique blocks.  The theorem
is cyclic in the three face colors.

There is a closed form when `D` is a cactus, meaning that every edge belongs
to at most one simple cycle.  For a cycle block `K`, put

```text
q_F(K) = number of green vertices f on K with deg_D(f)=2.
```

Then the general product becomes

```text
                 product q_F(K).                         (2)
             K a cycle block of D
```

In particular, under the cactus hypothesis `G` has a
Hamilton cycle containing `M_g` if and only if every cycle block of `D`
contains a degree-two green vertex.  A cycle and a certificate are then
constructible in linear time.  The statement is cyclic in the three face
colors.

The formula is exact even when its value is zero.  It counts only Hamilton
cycles containing the specified color matching; a graph with value zero in
one color role may have Hamilton cycles using another matching or none of
the three matchings in full.

## 1. The face-boundary bijection

Every face of a simple cubic bipartite polyhedron has even length at least
four.  Around a face, neighboring face colors alternate.  Hence

```text
deg_D(f) = |boundary(f)|/2 >= 2
```

for every blue or green face `f`.  Standard dual-walk bypassing around the
third face color proves that `D` is connected.

We first prove a bijection valid without the cactus assumption:

```text
{Hamilton cycles C of G with M_g subset E(C)}
       <----> {S subset F : D[B union S] is a tree}.       (3)
```

Let `C` contain `M_g`.  Every dual edge between a blue and a red face
crosses a green primal edge and therefore crosses `C`.  The bicolored dual
on the blue and red faces is connected, so all blue faces lie on one side
of `C` and all red faces on the other.  Let `S` be the green faces on the
blue side.

Because `C` is Hamiltonian, there are no primal vertices strictly on either
side.  The blue side is a disk dissected by noncrossing primal chords.
Its weak dual is therefore a tree: begin with one region and observe that
each chord splits one region and adds one leaf edge to the weak dual.  This
weak dual is exactly `D[B union S]`.

Conversely, suppose `Q=D[B union S]` is a tree.  Take the union `U` of the
closed blue faces and the closed green faces in `S`.  At a primal vertex
there is exactly one incident face of each color.  Consequently two chosen
faces meet at that vertex only when they also share the intervening primal
edge.  The faces of `U` can therefore be glued in a leaf order of `Q`, one
disk along one boundary edge at a time.  Thus `U` is a disk.

Its boundary consists of

- every green edge, between a blue and a red face;
- the blue boundary matching of each green face in `S`; and
- the red boundary matching of each green face outside `S`.

Exactly two of these boundary edges meet at every primal vertex.  Since the
boundary of `U` is connected, it is a Hamilton cycle `C_S` containing
`M_g`.  The side of a cycle recovers `S`, while the displayed boundary rule
recovers `C_S` from `S`, proving (3).  Distinct subsets give distinct edge
sets.

## 2. The general block factorization

We use the following elementary block lemma.  Let `D` be any connected
bipartite graph of minimum degree at least two, with bipartition `B union F`.
Then

```text
#{S subset F : D[B union S] is a tree}
  = product_(K in B_2(D)) lambda_F(K).                    (4)
```

Suppose first that `T=D[B union S]` is a tree.  Every green articulation
vertex of `D` belongs to `S`.  Indeed, after deleting such a vertex, each
component contains one of its blue neighbors; all those blue vertices remain
in `T`, so no further green deletions can reconnect the components.

Every non-articulation vertex belongs to exactly one block.  Put
`X_K=(F-S) intersect V(K)`.  The graph `K-X_K` must be connected.  Otherwise
two of its components cannot be joined outside `K`: an outside path between
distinct vertices of one block would create a cycle in the block-cut
incidence graph, which is a tree.  It is also acyclic as a subgraph of `T`.
Thus `K-X_K` is a tree and `X_K` is counted by `lambda_F(K)`.

Conversely, independently choose a set `X_K` counted by `lambda_F(K)` in
every non-bridge block, and delete their union.  No articulation vertex is
deleted.  Each non-bridge block is replaced by a tree.  Both ends of a bridge
are articulation vertices in a connected graph of minimum degree at least
two, so every bridge block remains its single edge.  Gluing these trees
according to the original block-cut tree gives one connected acyclic graph.
It is precisely
`D[B union (F-X)]`.

The sets of eligible non-articulation green vertices in distinct blocks are
disjoint.  The choices are therefore independent, proving (4).  Combining
(4) with the face-boundary bijection (3) proves the general formula (1).

## 3. The cactus closed form

Let `D` now be any connected bipartite cactus of minimum degree at least two,
with bipartition `B union F`.  We claim

```text
D[B union S] is a tree
```

if and only if the deleted set `F-S` contains exactly one degree-two green
vertex from every cycle block of `D`.

Assume first that the induced graph is a tree.  A deleted green vertex cannot
be a cut vertex of `D`: each component of its deletion contains one of its
blue neighbors, all of which remain in the induced graph.  In a connected
cactus of minimum degree at least two, every non-cut vertex lies on one cycle
block and has degree two.  Every cycle block must contain a deleted vertex,
or that cycle survives in the induced graph.

There cannot be two deleted green vertices on one cycle block.  The two arcs
between them each contain a blue vertex, because the cycle is bipartite.
Deleting both green vertices separates those retained blue vertices.  No
path outside the block can reconnect the two arcs: such a path together with
an arc would create a second cycle sharing an edge with the block, contrary
to the cactus property.  Thus precisely one eligible green vertex is deleted
from each cycle block.

For the converse, independently choose one degree-two green vertex from
each cycle block and delete all chosen vertices.  Within each block, a cycle
is replaced by a path; no chosen vertex carries a bridge or another block.
The block-cut tree therefore stays connected.  Every simple cycle of a
cactus is one of its cycle blocks, and each has been broken, so the remaining
induced graph is acyclic.  It is a tree.

Choices belonging to distinct cycle blocks are independent, because a
degree-two vertex belongs to only one block.  Hence the local block factor is

```text
lambda_F(K)=q_F(K)
```

for every cycle block.  This turns (1) into (2).

## 4. Constructive form and limits

The face coloring, `D`, its articulation vertices and cycle blocks can all be
found by linear-time graph searches.  If every cactus factor in (2) is positive,
choose one eligible green face per cycle block, delete those faces from `D`,
and use the boundary rule in Section 1.  This directly returns the Hamilton
cycle; no search through primal cycles or dual spanning trees is required.

The simple cactus closed form is load-bearing on that hypothesis.  When two
cycles share an edge or a theta subgraph occurs, deleting one vertex can
break several cycles and the local factor need not be `q_F(K)`.  The general
block product (1) still applies, but computing a factor may require solving
the induced-tree problem inside its 2-connected block.  The result does not
settle Barnette's conjecture and does not assert that every Barnette graph
has a cactus bicolored dual.

## 5. Evidence boundary

The theorem rests on the written planar-boundary bijection and the block-cut
argument.  The accompanying Python checker independently enumerates every
connected minimum-degree-two labeled bipartite graph in boxes through four
vertices per side.  It compares the global induced-tree count with the
product of independently enumerated block factors.  On every cactus it also
compares against the explicit cycle-block product and checks the structural
deleted-vertex certificate.  Positive, zero-product, theta and disconnected
controls are included.  This finite audit checks conventions and the exact
combinatorial formulas; it is not used to infer the universal theorem or the
planar correspondence.
