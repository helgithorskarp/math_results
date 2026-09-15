# Native five-point double triangles cannot replace the six Parts stars

For the fixed 503-point host and published point pool below, **all 1,401
five-point double-triangle replacements are four-colourable**. Every complete
physical graph has 508 distinct points and between 2,439 and 2,452 unit edges.
This closes one capped positive-parent surgery architecture. It is not a
sub-509 five-chromatic construction or a theorem about arbitrary replacements.

The selector's strongest example has **508 points and 2,450 unit edges**.
It rejects 12 of 22 tested host colourings, including three rejections that
require private new–new contacts. Ten tested colourings still extend. That
nonempty intersection ends the operation; no larger pool, different deletion
set, phase, copy count or added-point-count continuation is justified here.

## Frozen geometry and cap

Let `G` be the strict graph on the exact Parts509 coordinate input. Delete its
six independent degree-four vertices

```text
D = (310,313,316,319,322,325),    H = G-D.
```

The host has 503 points and 2,418 unit edges. The original six stars block
all host four-colourings because the original graph is five-chromatic. Its
[degree-four obstruction](../hadwiger_nelson_parts509_degree4_signatures/README.md)
and [22-state list interface](../hadwiger_nelson_parts509_degree4_list_kernel/README.md)
were previously studied. No new complete receiver relation is enumerated here.

Let `Q` be exactly the ordered 1,158-point list in
`../hadwiger_nelson_parts509_swap_closure/completion_points.json`, with file
identity in `manifest.json`. These points are distinct and outside all 509
parent points. Consider every five-element subset `A` of this finite list
whose unit graph contains two equilateral unit triangles sharing exactly
one vertex. Include all other physical contacts too. The graph under test is
always `UD(H union A)`, with exactly `503+5=508` distinct points.

This is a prescribed coupled replacement of six independent stars by a
five-point graph with private internal constraints. It is not an arbitrary
five-addition search or a claim that the finite pool exhausts all possible
plane replacements. Every source coordinate lies in
`Q(sqrt(3),sqrt(5),sqrt(11))`, at common denominator 288 in the basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

## Complete finite check

The verifier reconstructs the complete strict graph on all 1,667 ambient
points, considering all 1,388,611 unordered pairs. A checked homomorphism of
the integer radical ring modulo 1,321 rejects only nonunits; every survivor is
tested by exact squarefree-radical/gcd multiplication. The resulting 11,074
edges agree entry-for-entry with the earlier ambient manifest. Thus every
host–new and new–new contact in every declared replacement is included.

Every eligible five-set is found by choosing its common triangle centre and
two disjoint unit edges among that centre's new-point neighbours. Duplicate
five-sets are merged. This yields precisely 1,401 supports.

For each of the 22 previously published explicit host colourings, compute
at each new vertex the colours absent from its actual host neighbours. A
five-variable finite list-colouring check decides extension over the complete
new-point graph. Every support has an extension of at least one fixture;
every returned word is checked directly against the host, contact and internal
constraints. In fact each support admits between 10 and 22 of these fixtures.
Their full histogram is in `expected.json`.

The 22 fixtures are actual colourings of all 503 host vertices. Although they
came from a complete list-interface classification, **they do not enumerate
all host colourings or all replacement boundary patterns**. Rejecting a fixture
does not prove that its whole list-interface class is excluded. Positive
extensions alone suffice for this finite family's four-colourability theorem.

## Selected physical obstruction test

Select the five-set minimizing the number of extending fixtures, then break
ties lexicographically by pool indices. It is

```text
A = Q[38], Q[54], Q[529], Q[561], Q[953].
```

Its triangles are `(38,529,561)` and `(54,529,953)`. There are six new–new
edges and 26 host–new edges, giving `2418+6+26=2450` complete edges. Its new
contacts meet only the small Parts side and the origin; none meets a neighbour
of the deleted stars. These are exact contact facts, not an assumed interface.

The extending fixture indices are

```text
3,5,8,9,12,13,14,16,17,18.
```

`certificate.json` supplies their local extensions and a full 508-symbol
proper four-word. The selected negative cases are also checked by a separate
exhaustion of all `4^5` assignments.

Nine of the twelve rejected fixtures already leave some new vertex with no
available colour. Fixtures 6, 10 and 11 instead leave every individual star
colourable, but fail after the private unit edges are included. For example,
fixture 6 gives the five available lists, in the displayed order,

```text
{0}, {1}, {1}, {1}, {0,3}.
```

The physical edge between `Q[54]` and `Q[529]` then joins two vertices forced
to colour 1. Thus the complete support strictly restricts the full host
colouring relation, and private contacts provide a demonstrable additional
restriction. The ten surviving fixtures prove that the restriction is still
insufficient. No full relation cardinality, individual-contact essentiality,
ordinary non-four signal or candidate is claimed.

## Reproduction and trust

From this directory in a full checkout of the repository:

```sh
python3 verify.py
python3 verify.py --emit /tmp/parts503-double-triangle
```

CPython 3.11 and its standard library suffice. The optional command writes the
selected coordinates and full edge list outside Git. Inputs are hash-pinned;
all four dependency files are already public. No SAT solver, proof log,
floating-point geometry or local scratch data is needed.

The original selector used the previously certified ambient contact list and
a dynamic list search. The public verifier reconstructs all ambient contacts
with different norm arithmetic and uses a static-order list search. Selected
geometry agrees entry-for-entry. The separate `4^5` check validates all 22
selected extension verdicts. These are author-side checks, not independent
review or formalization. Trust remains in the pinned source bytes, exact
field identities, the elementary finite enumeration, Python integer arithmetic
and the directly checked colour words. Imported parent chromaticity motivates
the construction but is unnecessary for the four-colour stopping proof.

The theorem is scoped only to this fixed
503-point host, the finite Q list and the five-point double-triangle shape.
It says nothing about other replacement graphs or points outside Q, and does
not license nearby widening after the stop. Both reviewed Parts receivers
remain banked inputs. No F29/bowtie coupler or other researcher's construction
was used as a premise.

The supported unrestricted record remains
[Parts's 509 points and 2,442 edges](https://arxiv.org/abs/2010.12665), also
identified as current by [Haugland v4](https://arxiv.org/html/2608.04542v4).
This finite negative and its partial physical relation gain do not improve it.
