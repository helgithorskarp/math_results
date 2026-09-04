# Analytic obstruction for order-five type `1^38 5`

Let `G` be a graph on 43 vertices with neither a clique nor an independent
set of order five. No automorphism of `G` has cycle type

```text
1^38 5^1.
```

This is a short structural theorem. It needs no SAT solver and is not a
43-vertex construction or an improvement to the Ramsey bound.

## Proof

Regard edges and nonedges as two colors. Suppose that `g` is an order-five
automorphism fixing a set `F` of 38 vertices and cycling the remaining set
`C={c_0,...,c_4}`.

The action of `g` on the ten pairs inside `C` has exactly two orbits: the
five pairs at cyclic distance one and the five at cyclic distance two. Each
orbit is monochromatic. They cannot have the same color, since then `C`
would itself be a monochromatic `K_5`. Consequently, in either color the
subgraph on `C` is a five-cycle, and every `c_i` has exactly two neighbors
of that color inside `C`.

Fix either color, call it red, and let

```text
Y = {v in F : every edge from v to C is red}.
```

This is well-defined because `g` fixes `v` and acts transitively on `C`, so
all five edges from `v` to `C` have one color. For every `c_i`,

```text
red_degree(c_i) = 2 + |Y|.
```

Every color-degree in a Ramsey `(5,5;43)` coloring is at least 18. Indeed,
if a vertex has red degree `d`, its 42 minus `d` blue neighbors contain
neither a blue `K_4` nor a red `K_5`; the equality `R(4,5)=25` therefore
gives `42-d <= 24`. Hence `|Y| >= 16`.

On the other hand, `G[Y]` contains no red triangle: such a triangle,
together with any red edge inside `C`, would form a red `K_5`. It contains
no blue `K_5` because `G` contains none. The equality `R(3,5)=14` therefore
gives `|Y| <= 13`, a contradiction.

The argument works identically after interchanging the colors. Thus the
claimed cycle type is impossible.

## Reproduction

The standard-library checker reconstructs the pair orbits under a 5-cycle,
exhausts their four two-color assignments, and verifies that the only two
nonmonochromatic assignments give degree two in each color. It also records
the exact numerical implication of the two Ramsey constants.

```bash
./verify.sh
```

The output manifest is rebuilt and byte-compared with `result.json`. The
checker is an audit of the finite orbit and arithmetic steps; the two known
Ramsey equalities remain mathematical inputs.

## Scope and provenance

Together with the sibling degree-network and middle-stratum obstructions,
this leaves only `1^3 5^8` and `1^8 5^7` among the eight possible
order-five cycle types. It does not exclude all order-five automorphisms and
does not constrain asymmetric colorings.

The exact values used above are due to Greenwood--Gleason,
[*Combinatorial Relations and Chromatic Graphs*](https://doi.org/10.4153/CJM-1955-001-4),
for `R(3,5)=14`, and McKay--Radziszowski,
[*R(4,5)=25*](https://doi.org/10.1002/jgt.3190190304), for `R(4,5)=25`.
The inspected structured-construction literature and refreshed Discovery
Net graph did not state this cycle-type obstruction. Novelty is claimed
only relative to those searched sources, not as a universal priority claim.
