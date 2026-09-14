# Proof and finite verification boundary

## Exact geometry

A field element is a rational four-tuple on

```text
1, sqrt(3), sqrt(11), sqrt(33).
```

Multiplication uses the XOR of the two square-root masks and multiplies by
`3` or `11` when the corresponding radical occurs twice.  A plane point is a
complex pair of such elements.  Squared Euclidean distance is
`z*conjugate(z)` and is compared exactly with one.

The Moser points and the eighteen-point set `D` are decoded at denominator
12 from the hash-pinned all-terminal-contact certificate.  The verifier tests
directly that every point of `D` is distinct and has exactly two unit
neighbours in the seven-point Moser set.  The completeness of `D` as the set
of all external double neighbours is the imported source theorem; its
certificate gives both circle-intersection witnesses for every pair of Moser
centres.

The ten Golomb points are reconstructed from the displayed integer rows in
the verifier.  Their complete graph has 18 unit edges.

## Placement completeness

For distinct Golomb points `x0,x1` and distinct docking points `y0,y1` of the
same separation, the direct isometry is

```text
u = (y1-y0)/(x1-x0),       t = y0-u*x0.
```

For the reflected case replace each `x` by its complex conjugate.  Exact norm
checking proves `|u|=1`.  Both orders of `y0,y1` are used.  Therefore every
isometry carrying two Golomb vertices to two docking points occurs in the
1,188 recipe list.  Conversely every recipe is such an isometry.  Exact tuple
deduplication leaves 972 transformations.

For each transformation the seventeen formal addresses are grouped by exact
coordinate equality.  Every unordered pair of resulting classes is then
tested for squared distance one, so incidental collisions and unit contacts
are included.  This produces the complete strict physical graph rather than
an abstract union of supplied edge lists.

## Colour relations

The first three vertices in each component form a unit triangle.  Fixing them
to `0,1,2` removes only global colour-name symmetry.  Literal enumeration of
the remaining source vertices gives 16 Moser and 95 Golomb patterns.  For
every placement and every such pattern, deterministic backtracking constructs
a full proper four-colouring.  This proves surjectivity of both restriction
maps from union colourings to component colourings.

For every physical nonedge `uv`, the same search constructs extensions of
the normalized prescriptions `(0,0)` and `(0,1)`.  Any equal named pair can
be globally permuted to `(0,0)`, and any unequal named pair to `(0,1)`.
Therefore every nonedge has both possible equality states.  Every unit edge
has only the unequal state in any proper colouring.  Hence all two-terminal
relations are exactly the bare graph relations.

Finally, exhaustive testing of all `3^7` assignments finds no proper
three-colouring of the Moser subgraph.  The component-extension witnesses
provide a proper four-colouring of every union.  All 972 graphs are therefore
exactly four-chromatic.

The conclusion is deliberately low-arity: surjective one-component
projections and neutral pair projections do not logically exclude a mixed
relation on three or more terminals.  No such stronger statement is claimed.
