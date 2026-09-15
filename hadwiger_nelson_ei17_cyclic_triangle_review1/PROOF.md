# Independent proof architecture

## 1. Source realization

Vertices 10 and 16 are fixed at `(-1,0)` and `(0,0)`.  The other 30
coordinates and the 30 nonfixed unit-edge equations form a square polynomial
system `F(x)=0`.  From the pinned rational midpoint, the review recomputes the
exact midpoint Jacobian inverse `A`.

Every Jacobian entry is evaluated over the entire radius-`10^-18` rational
box.  Entrywise interval matrix arithmetic encloses

```text
I - A J(X).
```

Its infinity row norm is less than one, and

```text
||A F(m)||_infinity + q r < r.
```

Therefore `T(x)=x-AF(x)` is a contraction mapping the box into itself.  Since
`||I-AJ(m)||<1`, the square matrix `A` is invertible; the unique fixed point of
`T` is the unique root of `F` in the box.  Direct interval squared distances
prove all 17 points distinct and exclude unit distance for every declared
nonedge.

## 2. Frame completeness and geometry

For an ordered source edge `(i,j)`, its exact root displacement has norm one.
There are precisely two isometries sending it to the ordered segment from
`A=(0,0)` to `B=(1,0)`, according to orientation.  Choosing one of 31 edges,
one of two endpoint orders, and one of two orientations gives the 124 declared
frames.  This is completeness for the declared same-frame cyclic architecture,
not for independent choices on three copies.

The independent interval transformation encloses both isometries and the map

```text
T(z) = 1 + ((-1+i sqrt(3))/2) z.
```

Anchor images are replaced by their exact equilateral vertices, a consequence
of the source unit equation.  Every other pair of the 51 labels has disjoint
coordinate intervals unless it is one of the three declared anchor
identifications.  Thus there are exactly 48 physical points.

For every unordered physical pair, the review encloses squared distance for
all label representatives.  A pair is excluded only when all enclosures avoid
one; otherwise it enters the upper graph.  Hence no actual unit edge can be
omitted.  The independent physical groups and upper edges agree entry-by-entry
with the target stream.

## 3. Source-colouring completeness

A fixed-order exhaustive search proves the source non-three-colourable.  A
separate search enumerates all four-colour words satisfying

```text
c(10)=0, c(16)=1.
```

It finds 170,176.  Every proper source word uses four colours.  In each orbit
under the 24 global colour permutations, exactly two words give the specified
ordered colours to this fixed edge—the two remaining colours may be exchanged.
Thus there are exactly `170176/2 = 85088` source-colour orbits, and testing all
fixed-edge words covers every orbit twice.

As an independent control, proper colour orbits are also counted as partitions
of the vertex set into four nonempty independent sets.  This second method
finds 1,181 independent sets and 85,088 valid partitions.

## 4. Extension proof

For an upper graph with no cross-copy edge, let the ordered anchor colours in
copy zero be distinct values `(a,b)`, and choose a third colour `c`.  Apply a
colour permutation sending `(a,b)` to `(b,c)` on copy one and to `(c,a)` on
copy two.  The three copy words agree at all equilateral anchors, and every
within-copy edge remains proper.  The review checks this symbolic argument for
all 12 ordered pairs in all 116 plain frames.

For each of the eight 96-edge upper graphs and each fixed-edge source word, the
base colours delete forbidden colours from the 31 new-vertex domains.  Equal
domain vectors reuse a witness, but every one of 1,361,408 source/frame inputs
is explicitly mapped to its state.  A separate minimum-domain backtracker
finds a positive witness for every state; each witness is checked against its
domains and every new--new edge.  Source edges are proper by enumeration and
base--new edges are exactly the domain deletions, so these checks give a full
proper colouring.

Every actual strict unit graph is a subgraph of its coloured upper graph and
contains the exact four-chromatic source.  Its chromatic number is therefore
exactly four.

## 5. Structural result and trust boundary

Direct deletion tests find no articulation or bridge.  Deleting every vertex
pair finds exactly three cuts in each frame, precisely the three anchor pairs.
Minimum degree is three, so vertex connectivity is exactly two.

The proof trusts CPython integer and `Fraction` arithmetic, JSON parsing, and
the pinned midpoint and edge bytes.  It does not import the target interval
class, geometry builder, colouring enumerator, or solver.  No floating-point
incidence predicate, negative external solver answer, or formal proof system
is used.
