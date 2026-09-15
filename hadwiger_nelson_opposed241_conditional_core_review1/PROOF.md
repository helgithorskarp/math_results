# Proof and independent computation boundary

## 1. Exact physical graph

Let the eight basis elements be indexed by masks for the squarefree products
of `3`, `5`, and `11`. If basis masks `i,j` share prime factors, multiplying
them contributes the product of those common primes and leaves mask `i xor j`.
This gives exact integer multiplication in
`Q(sqrt(3),sqrt(5),sqrt(11))`. A point is represented by separate eight-term
real and imaginary coordinate vectors at common denominator 36.

The review reads the hash-pinned B214 fixture, independently checks that only
the coefficients of `1`, `sqrt(33)`, `sqrt(3)`, and `sqrt(11)` occur, and
forms

```text
G,  L(B) = B-(1/2,0),  R(B) = reflection_x(B)+(1/2,0).
```

Exact equality merging in first-occurrence order gives the reviewed 343-point
parent with 1,782 complete unit edges. Selecting the target's 241 sorted
source labels and testing all `C(241,2)=28,920` pairs gives 991 edges. A pair
is included exactly when generic multiplication gives squared distance
`(1296,0,...,0)` before division by `36^2`. Therefore the result is an actual
plane unit-distance realization, not merely an abstract graph.

The generic calculation specializes to

```text
a^2 + 33b^2 + 3c^2 + 11d^2 + 2(ab+cd)sqrt(33),
```

but the production geometry code does not use that specialization. The
controls compare both expressions over all 625 tuples in `[-2,2]^4` and test
associativity on all 512 basis triples.

## 2. Conditional nonextension

Fix colors `0121212203` on the ten Golomb vertices. The direct-assignment
search stores one color or “unassigned” at each remaining vertex. At every
node it chooses an unassigned vertex, computes the colors already used by
its assigned neighbours, and branches over every remaining color. Empty
availability closes the node. The DSATUR score changes only the vertex order;
the color order `(3,1,0,2)` changes only branch order. Thus each branch is a
complete disjunction, recursion assigns one new vertex, and exhaustive
failure proves nonextension. All independent branches close after 82,989
nodes.

This differs from the source's propagation search: there are no maintained
domains and no forced singleton propagation. The small-instance control
compares the implementation with literal `4^5` brute force on every labelled
five-vertex graph under three pin regimes, for 3,072 exact comparisons.

The target's `proper4` word is independently checked on all 991 edges and
restricts to `0121212023`, so the graph is four-colorable. The ten-vertex
Golomb subgraph has 18 physical edges. Fixing its unit triangle to `0,1,2`
and enumerating the remaining seven vertices gives 95 four-color patterns
and no three-color pattern. Hence the core's ordinary chromatic number is
exactly four. The rejected pattern is one complete fixed input, not an
ordinary non-four-colorability certificate.

## 3. Relative vertex minimality and projection loss

For each vertex `v=10,...,240`, the target certificate contains a length-241
word with `-` at `v`, the fixed Golomb prefix, and proper colors on every edge
not incident with `v`. The independent checker validates all 231 words. If
`T` is any proper induced subgraph of this core containing vertices 0 through
9, choose `v` outside `T`; restricting the word for `C-v` to `T` colors `T`
with the forbidden prefix. This proves exactly the claimed relative vertex
minimality.

It does not compare other subsets of the 343-point source, other deletion
orders, other prescribed inputs, or unrelated geometries.

Intersecting the core with the two B214 copies gives induced pieces of orders
121 and 176 with 56 common points. There are 47 remaining unit edges, each
between a left-private and a right-private point. The supplied contact-deleted
word satisfies every edge internal to either piece while retaining the
forbidden prefix. Its restriction to the entire 121-point left piece is
therefore a proper full input that cannot extend to the core. Restricting the
surviving core word gives a full left input that does extend. This establishes
strict input projection loss for the stated piece.

## 4. New contact-edge classification

For every one of the 47 private contacts, the independent DSATUR search is
rerun after deleting exactly that edge. Forty-three runs return a full proper
word with prefix `0121212203`; each word is checked directly, and its deleted
edge endpoints have the same color. The deterministic stream of these 43
witnesses has SHA-256
`d2f311a5cc67c298af0bc56517c83568fc3f4da3c10d6742416564b27d05b713`.

The searches for four edges exhaust without a word:

```text
(66,191), (74,186), (97,186), (97,226).
```

Together with the base run, the 47 deletion runs visit 1,167,961 nodes. It
follows that 43 contacts are individually critical for this conditional
property and four are individually redundant. This does not classify the
other 944 unit edges and does not assert monotonic behaviour under deleting
multiple contacts.

## 5. Vertex connectivity

Tarjan low-link search first finds one component and no articulation. For
each of the 28,920 unordered vertex pairs, the checker deletes the pair and
runs the same search. A disconnected result would be a two-cut; none occurs.
If a triple `{x,y,z}` were a cut, then after deleting `x,y` the remaining
graph—already known connected—would have articulation `z`. Recording all
articulations after every pair therefore covers all 2,303,960 triples; none
occurs. Hence vertex connectivity is at least four.

Vertex 37 has exactly the neighbours `[17,43,59,95]`. Deleting them isolates
37, giving a four-cut, so vertex connectivity is exactly four. This is
stronger than the source's no-articulation/no-bridge statement.

## 6. Native Parts373 role

The checker reads only the hash-pinned 509-row Parts coordinate fixture,
forms the archived 373-point host as rows 0 through 373 with row 310 omitted,
and compares coordinates at common denominator 288. It finds 137 equal
points, including the stated ten Golomb roles, so the union has
`373+241-137=477` points. Every nonzero coordinate remains in
`E=Q(i sqrt(3),i sqrt(11))`.

The deduction that the complete physical union is four-colorable imports the
separately reviewed theorem that the strict unit-distance graph on all of E
has chromatic number four. The present finite checker establishes the
coordinate-membership premise and size arithmetic only. It does not read a
receiver pattern relation, run a receiver solve, or produce a five-chromatic
construction.
