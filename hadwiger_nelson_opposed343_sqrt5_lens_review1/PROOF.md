# Proof and computation boundary

## 1. Independent exact arithmetic

Put `E=Q(r,s)` with `r^2=3`, `s^2=11`, and basis `(1,r,s,rs)`. The checker
implements multiplication in this basis by direct expansion. It then writes
the full coordinate field as `E + sqrt(5) E` and uses

```text
(u+v sqrt(5))(x+y sqrt(5)) = ux + 5vy + (uy+vx)sqrt(5).
```

All coordinates are integer coefficient pairs at common denominator 144.
This quadratic-tower representation is algebraically equivalent to, but
implemented independently of, the target basis
`(1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165)`.

The B214 input is hash-pinned, checked to lie in the old subfield, shifted and
reflected exactly, then merged with the ten Golomb points by exact equality.
This gives 343 distinct source points and 1,782 unit edges. No tolerance or
floating-point predicate occurs.

## 2. Complete lens construction

For an old pair `p,q` with squared distance `16/9`, let `v=q-p` and let `R`
be quarter-turn. The two proposed points are

```text
x_plus/minus = (p+q)/2 plus/minus (sqrt(5)/4) R(v).
```

The summands are perpendicular and `|R(v)|=|v|`, so

```text
|x-p|^2 = |v|^2(1/4+5/16) = (16/9)(9/16) = 1.
```

Conversely, two unit circles whose centers are `4/3` apart have exactly these
two intersections: their common chord lies on the perpendicular bisector and
its half-height is `sqrt(1-(2/3)^2)=sqrt(5)/3`, equal to
`(sqrt(5)/4)|v|`. Thus both orientation branches, and no others, are included
for the declared center class.

The checker exhausts all `C(343,2)` old pairs and finds 54 qualifying pairs.
They use 108 distinct old vertices, so the center-pair graph is a matching.
Exact construction yields 108 distinct points, none equal to an old point;
each has a nonzero `sqrt(5)E` coefficient. Scanning all `C(451,2)=101475`
pairs gives 2,170 unit edges, partitioned as 1,782 old--old, 216 old--new,
and 172 new--new. Each new point's two old neighbours are exactly its defining
centers. This proves a complete physical realization, not an abstract graph
with a selected edge list.

## 3. Projected relation

The first 343 vertices induce exactly the independently reviewed S343 graph.
That imported theorem says its normalized complete Golomb relation consists
of 66 patterns; therefore the final graph, as a supergraph, can project to no
other pattern.

The target certificate has exactly one 451-character word for each of those
66 patterns. The checker tests its ten-character prefix and all 2,170 edge
inequalities. Hence every source pattern extends and the final relation is
exactly the same 66-element set. Positive words need no trust in the PySAT
program that produced them.

The new layer itself contains Moser spindles, and is therefore not
three-colorable; the checked positive words show that it and the full graph
are four-colorable. Thus the ordinary chromatic number is four independently
of the relation upper-bound argument.

## 4. New-layer decomposition

Connected-component search on the 108 new vertices and 172 new--new edges
gives eight components with `(vertices,edges)=(6,7)` and four with
`(15,29)`. Exact backtracking graph isomorphism finds one isomorphism type at
each order. The eight small components pass direct bipartiteness tests. Each
large component fails exhaustive three-coloring and admits four colors.

For structural identification, the checker scans all seven-vertex subsets of
each large component. Exactly one induced subset per component is isomorphic
to the canonical eleven-edge Moser spindle. The four global vertex sets are

```text
343 370 401 415 426 429 435
346 362 373 374 382 423 432
347 361 372 375 381 397 424
369 378 400 416 427 428 436
```

The canonical spindle is independently tested non-three-colorable and
four-colorable. The four subsets are vertex-disjoint because they lie in
distinct components.

Each new component has an old-neighbour attachment set. Exactly six distinct
sets occur, each for two components: four attachment sets have order 12 and
two have order 30. This is descriptive structure, not a claim that the full
graph decomposes across those old vertices.

## 5. Exact vertex connectivity

Tarjan low-link search finds the graph connected with no articulation. For
every unordered pair `{a,b}`, the checker deletes the pair and reruns the
low-link search. A disconnected result would exhibit a two-cut. If a triple
`{a,b,c}` separated the graph, the pair-deleted graph—already verified
connected—would have articulation `c`. Thus requiring every one of the
101,475 pair-deleted graphs to be connected and articulation-free covers all
15,187,425 triples. No separator of order at most three exists.

Vertex 349 has degree four and neighbours `[15,139,386,413]`; deleting those
four vertices isolates it. Therefore the full graph's vertex connectivity is
exactly four. This strictly strengthens the target's no-articulation and
no-bridge statement.

## 6. Scope

No search over other old-pair distances, one intersection per pair, subsets
of the 54 pairs, iterative lens completion, placements, or receivers is part
of this theorem. Relation equality imports the prior exact S343 exclusion of
29 patterns. The result supplies no five-chromatic graph and makes no global
claim about the Hadwiger--Nelson frontier.
