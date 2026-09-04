# Sparse-motion obstructions for involutions and order-three automorphisms

Let `G` be a graph on 43 vertices with neither a clique nor an independent
set of order five. Then:

- every involution in `Aut(G)` has at least five transpositions;
- every order-three element in `Aut(G)` has at least seven 3-cycles.

Equivalently, the following prime-order cycle types are impossible:

```text
order 2:  1^41 2,  1^39 2^2,  1^37 2^3,  1^35 2^4;
order 3:  1^40 3,  1^37 3^2,  1^34 3^3,
          1^31 3^4,  1^28 3^5,  1^25 3^6.
```

These are analytic structural exclusions, not a 43-vertex construction or
an improvement to the Ramsey bound.

## Three local facts

Use two colors for edges and nonedges.

1. Every degree in either color is at least 18. If a vertex has red degree
   `d`, its `42-d` blue neighbors contain neither a blue `K_4` nor a red
   `K_5`. The equality `R(4,5)=25` gives `42-d <= 24`.
2. The common red neighborhood of a red edge has at most 13 vertices. Its
   induced coloring has neither a red `K_3` nor a blue `K_5`, so this follows
   from `R(3,5)=14`. The same statement holds with the colors reversed.
3. The common red neighborhood of a red triangle has at most four vertices.
   It has no red edge, since that edge would complete a red `K_5`; five such
   vertices would therefore be a blue `K_5`. Again the statement is
   color-symmetric.

## Involutions

Suppose an involution has `k` transpositions. Choose one transposition
`C={x_0,x_1}` and call the color of its internal edge red. Let `W` be the
common red neighborhood of `C`, so `|W|<=13`.

Every fixed vertex has the same color to both vertices of `C`; if that color
is red, the vertex lies in `W`. Between `C` and another transposition there
are two two-edge orbits. If both are red, both vertices of the other
transposition lie in `W`; otherwise `x_0` has at most one red neighbor in
that transposition.

If `a` fixed vertices and `m` complete transposition blocks lie in `W`, then

```text
a + 2m <= 13,
red_degree(x_0) <= 1 + (a+2m) + (k-1-m) <= k+13.
```

The degree lower bound 18 forces `k>=5`.

## Order three

Suppose an order-three element has `k` 3-cycles. Choose one, `C`. Its three
internal edges form one orbit, so they have one color, say red. Let `W` be
the common red neighborhood of this red triangle; then `|W|<=4`.

A fixed vertex joined red to one vertex of `C` is joined red to all three
and lies in `W`. Between `C` and another 3-cycle there are three three-edge
orbits. If all three are red, that entire other cycle lies in `W`; otherwise
each vertex of `C` has at most two red neighbors in the other cycle.

If `a` fixed vertices and `m` complete 3-cycle blocks lie in `W`, then

```text
a + 3m <= 4,
red_degree(x) <= 2 + (a+3m) + 2(k-1-m) <= 2k+4.
```

The degree lower bound 18 forces `k>=7`.

## Reproduction

The dependency-free checker reconstructs the internal and cross pair-orbits
for orders two and three. It exhausts every cross-orbit coloring and every
relevant product of cross blocks, applies the exact common-neighborhood
caps, and independently recovers maximum possible color-degrees 14 through
17 for one through four transpositions and 6 through 16 for one through six
3-cycles.

```bash
./verify.sh
```

The regenerated output is byte-compared with `result.json`. The checker
audits the finite orbit optimization and arithmetic. The equalities
`R(3,5)=14` and `R(4,5)=25` remain mathematical inputs.

## Scope and provenance

The result only excludes the ten displayed sparse-motion types. Involutions
with at least five transpositions and order-three elements with at least
seven 3-cycles remain possible by this argument. Powers of composite-order
automorphisms may be screened against the theorem, but no assertion is made
from the cycle type of a generator alone.

The Ramsey inputs are Greenwood--Gleason,
[*Combinatorial Relations and Chromatic Graphs*](https://doi.org/10.4153/CJM-1955-001-4),
and McKay--Radziszowski,
[*R(4,5)=25*](https://doi.org/10.1002/jgt.3190190304). The inspected
structured-construction literature and refreshed Discovery Net graph did
not state these sparse-motion exclusions. Novelty is claimed only relative
to those searched sources, not as a universal priority claim.
