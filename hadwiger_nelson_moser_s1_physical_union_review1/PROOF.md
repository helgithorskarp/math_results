# Proof and review analysis

## 1. Independent reconstruction of `S1`

The only geometric input is the 25-point set `C` from
`hadwiger_nelson_moser_all_terminal_contacts/certificate.json`, pinned by
SHA-256. A coordinate is represented by four rational coefficients in the
basis

```text
(1, sqrt(3), sqrt(11), sqrt(33)).
```

This is a basis of `Q(sqrt(3),sqrt(11))`, so equality of coefficient vectors
is equality of real coordinates. The checker builds the complete unit graph
on `C`. For each vertex and each unordered pair of its unit neighbours it
adds the reflected fourth vertex of the unit rhombus. Collision merging gives
115 points. Complete all-pairs reconstruction gives 447 unit edges.

No function or intermediate graph is imported from the reviewed package.

## 2. The source terminal claims

Let

```text
T = (0,10,11,17,18).
```

The first three points are noncollinear. The checker constructs the complete
ten-entry distance signature of `T` and independently intersects exact
distance neighborhoods inside `S1`. This gives exactly 70 ordered tuples.
Their entrywise list agrees with the reviewed certificate.

For pattern `00112`, vertex 29 sees terminal colours 0, 1, and 2 at vertices
0, 11, and 18, so it is forced to colour 3. Vertex 93 then sees all four
colours at vertices 10, 17, 18, and 29. The checker verifies all seven unit
contacts used in this argument.

The reviewed certificate supplies a proper `S1` word restricting to `00001`
on `T`, and one proper host word with the same restriction for every ordered
embedding. This review checks all 71 words directly on the independently
rebuilt 447-edge graph. Hence the original isolated-relation conclusion is
accepted.

## 3. From a metric tuple to a physical copy

Fix one enumerated tuple `(a,b,c,d,e)`. The first three points are
noncollinear and have the same three mutual squared distances as the first
three target points. There is therefore a unique affine map taking
`(a,b,c)` to the corresponding target triangle, and equality of the two Gram
matrices makes its linear part orthogonal. It is a genuine Euclidean isometry,
possibly orientation-reversing.

The checker computes this affine map by exact two-by-two frame inversion in
the number field. It then verifies that the remaining two tuple points map
exactly to their target roles. Applying the map to all 115 host points gives
the physical second copy.

## 4. Complete physical unions

For each frame, the checker takes the union of the original and mapped point
sets and merges exact coordinate coincidences. It tests every unordered pair
of distinct physical points for squared distance one. Thus all inherited and
incidental unit contacts are present; no terminal-only abstraction remains.

For each resulting graph, `certificate.json` contains a four-colour word.
Direct edge-by-edge checking proves the upper bound four. Each graph contains
the original `S1`, which contains the seven input Moser points. Their complete
unit graph has 11 edges. Exhaustion of all `3^7` colour assignments proves
that this subgraph is not three-colourable. Thus every one of the 70 physical
unions has chromatic number exactly four.

## 5. Completeness and limitations

The finite family is complete because all ordered five-tuples satisfying all
ten target distances are enumerated, and a noncollinear congruent triangle
determines the only possible isometry for each tuple. Completeness applies
only to this fixed five-role self-host architecture.

The result cannot be promoted to a global lower bound or a general exclusion
of Moser-reflection constructions. It says nothing about hosts or terminal
sets outside the four conditions in the README. In particular, it produces
no five-chromatic plane graph and no construction smaller than 509 vertices.

## 6. Trust boundary

- Exact arithmetic uses Python integers and `fractions.Fraction` only.
- Field inversion is checked by multiplication back to one.
- Point equality and unit distance never use floating point or tolerance.
- Every physical edge set is reconstructed from all unordered pairs.
- SAT is used only in `generate.py` to produce positive colour words.
- `verify.py` trusts neither solver code nor a negative solver result.
- The remaining executable trust base is CPython plus this compact checker.
