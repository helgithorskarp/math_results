# Kempe perturbations of the heptagon difference graph

Let H be the 21-point motif defined in the
[parent proof](../hadwiger_nelson_heptagon_difference_lifts/PROOF.md), and
let D=H-H, with all unit-distance edges included. Its exact sorted table
has 421 points and 1848 edges, with origin label 210. All labels below
refer to that table, whose byte identity is pinned in expected.json.
The parent gives 42 normalized potential rows p on H and the colouring
C(0)=0, C(h_a-h_b)=p_a XOR p_b. Nonzero ordered differences are unique.

**Result.** From these 42 rows, the complete census of single Kempe
component swaps gives 1260 distinct four-colourings modulo colour
permutation. Exactly 1218 are outside the potential class; 1008 of those
are not antipodally symmetric and 210 are antipodally symmetric.
There are 756 swaps making at least one designated sqrt(3) pair
monochromatic. Their union covers 84 of the 126 such pairs, in six
rotation orbits of size 14. Consequently none of these 84 pairs is
forced to receive different colours in every proper four-colouring of D.

The remaining 42 pairs are unresolved. Their failure in this search is
not a proof of a forced colour relation. No five-chromatic graph is
constructed, and the necessity of potential form is explicitly false.

## A singleton witness for the previous UNKNOWN query

Take the following potential row, with indices 0 through 20:

```
[0,1,3,0,2,1,2, 1,3,0,2,3,0,0, 2,2,2,3,0,3,1].
```

This is row 8 of the parent's lexicographically sorted certificate.
Vertex 0 is h_14-h_5 and has colour 3. Vertex 332 is h_18-h_6 and
has colour 2. Its complete unit-neighbour list, with colours, is

```
120:0, 121:1, 150:0, 237:1, 315:0, 333:0, 359:1, 394:0.
```

Changing only vertex 332 from colour 2 to colour 3 is therefore proper.
The exact squared distance between vertices 0 and 332 is 3. This gives
a monochromatic sqrt(3) pair. The opposite of 332 is vertex 88, whose
colour stays 2, so this colouring is not potential under any global
colour relabelling: all potential colourings give opposite points the
same colour, and relabelling preserves equality.

The old two native queries for [0,332] had returned UNKNOWN, not UNSAT.
Apply the colour permutation 3->0, 0->1, 1->2, 2->3 to this new witness.
It has colours 0,0,1,2 at labels 0,332,15,22 respectively. The audit
regenerates both old CNFs and checks this explicit one-hot assignment
on every clause. In particular it satisfies the exact old 7817-clause
ALO input. No native solver, incomplete DRAT trace or negative proof is
used to establish this positive answer.

## Kempe swaps and completeness of the finite test

Given a proper colouring c and two distinct colours a,b, consider the
subgraph induced by vertices of those two colours. Swapping a and b on
one connected component preserves properness. Every edge within that
component still has different endpoint colours. A boundary edge cannot
have its other endpoint coloured a or b, since then that endpoint would
be in the same component. Edges outside it do not change.

This argument also permits swapping any union of components for a fixed
colour pair. Suppose c(u)!=c(v). Such a union swap can make u,v equal
exactly when their two original colours are a,b and u,v lie in different
components of that induced graph. If they are in the same component,
they change together; if one original colour is outside {a,b}, no swap
can equate them. If they are in different components, swapping the
component of u alone suffices. Thus arbitrary unions do not enlarge the
set of monochromatizable pairs obtainable in one fixed-colour-pair step
from a seed. This does not cover sequences of swaps using different
colour pairs, or unrestricted colourings.

The producer considers every one of six colour pairs for each of the
42 seeds. Its breadth-first traversal visits every component, including
singletons. All 1260 resulting rows are tested on every unit edge and
every designated pair. The component-size histogram is

| Size | Components |
|---|---:|
| 1 | 336 |
| 2 | 420 |
| 3 | 84 |
| 4 | 168 |
| 185, 193, 197, 208, 214, 216 | 42 of each |

The unit triangle with labels 210,172,123 normalizes graph colours to
0,1,2; the remaining colour becomes 3. Every proper row has distinct
colours at these anchors, so this is a unique representative modulo all
24 colour permutations. It agrees with the normalized potential lifts.
The 1260 normalized rows are distinct. Comparing against the 42 seed
rows identifies 42 potential and 1218 nonpotential outcomes.

The independent checker does not rely on the completeness of that
potential list for the last distinction. Every permutation of four
colours is an affine transformation of F_2^2. Subtract the origin colour
by XOR, and put p_a=C(h_a-h_0) XOR C(0). A colouring has potential form,
up to colour permutation, if and only if for every ordered pair a,b,

```
C(h_a-h_b) XOR C(0) = p_a XOR p_b.
```

Necessity follows because the affine translation cancels and the linear
part commutes with XOR. Sufficiency follows by this displayed formula
on every point of D. The checker evaluates this test directly for every
outcome, including the 210 antipodal nonpotential cases.

## Six compact witnesses and the residual set

Rotation by t^3, where t=exp(pi*i/21), has order 14 and preserves D and
all its edges. For each covered orbit, witnesses.json gives one seed
potential row and a one- or two-vertex component to swap:

| Representative pair | Seed row | Swap colours | Component |
|---|---:|---|---|
| [0,332] | 8 | 2,3 | [332] |
| [4,9] | 30 | 1,3 | [9] |
| [12,163] | 7 | 2,3 | [12] |
| [14,306] | 7 | 2,3 | [14,114] |
| [14,343] | 2 | 1,2 | [14,77] |
| [76,323] | 1 | 1,3 | [76,97] |

Rotating each proper witness gives witnesses for all 14 pairs in its
orbit. These 84 pairs are exactly those reached by the full census;
this is a union of existence statements, not one colouring making all
84 pairs monochromatic simultaneously.

The uncovered representatives are [24,218], [24,395], [25,202], each
with an orbit of size 14. The residual pair graph is 14 vertex-disjoint
triangles, on 42 vertices of D. Each triangle is geometrically equilateral
of side sqrt(3), centred at the origin, with its vertices on the unit
circle. Exact norms and coordinate sums check this description. This
structural description makes no claim about ordinary colour forcing.

## Verification and trust boundary

The parent graph was rebuilt in Q(t) and independently checked in
Q(zeta_7,omega_6) in this pass. All 88410 distances were rescanned, and
both complete potential enumerations were replayed. Those exact graph
and seed data, with their published provenance, are inputs to this result.

The new audit uses disjoint-set unions over the entire edge list, without
importing the producer's component traversal. Every component, resulting
colour-row hash, potential verdict, antipodal verdict and monochromatic
pair list agrees entrywise with the producer. It separately checks the
component-union criterion for all designated pairs and all seed/colour
pair choices. Both implementations test properness directly.

Small controls exhaust every graph on three vertices and every proper
four-colouring, comparing the criterion with all unions of components.
They cover 5184 different-colour pair cases and 5508 union-swap colourings.
Three malformed or improper 421-colour rows are rejected. All new
checks were run by the author; external review is pending.

The trust boundary includes the parent's exact geometry/seed construction,
the stated normalization and Kempe arguments, finite enumeration, exact
Python integers, and ordinary runtime/code correctness. No floating-point
distance or SAT status is a premise. Colour-row hashes identify compared
streams; properness and coverage are checked, not inferred from hashes.
