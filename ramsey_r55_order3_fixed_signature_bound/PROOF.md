# Ten-cycle symmetry forces three fixed vertices blue to the minority core

In a hypothetical Ramsey `(5,5;43)` graph with an automorphism of type
`1^13 3^10`, at least **three fixed vertices are blue to all twelve
minority vertices**, after naming the minority internal color red.
If exactly three have this property, each of the ten nonempty fixed
signatures occurs exactly once: the four singletons and the six pairs
of minority triangles. In that equality case, each minority triangle
has exactly four fixed red neighbors.

This follows from the standalone extension lemma below and the previously
certified [unique minority core](../ramsey_r55_order3_ten_cycle_phase_sweep).
The lemma does not impose a degree profile, an M=214 assumption, a
selected exceptional core, or any symmetry of the fixed-vertex graph.
The ten-cycle type and its four full-extension cases remain open.

## A standalone core extension lemma

Let G contain neither a red nor a blue K5. Suppose it contains the
following graph H on vertices `3i+s`, `i=0,1,2,3`, `s mod 3`:

* the four triangles `C_i={3i,3i+1,3i+2}` are red;
* red differences from C_i to C_j, i<j, are `{0}` for pairs 01,23
  and `{0,1}` for pairs 02,03,12,13.

Let F be any set outside H whose vertices are each complete or
anticomplete in red to every C_i. No automorphism is assumed here.
The red signature of f is

```text
S(f) = {i : f is red to all of C_i}.
```

**Lemma. At most ten vertices of F have a nonempty signature. If ten
do, every singleton and every two-element signature occurs exactly once.**

First, every signature has size at most two. Each union of three
minority triangles contains a red K4. Explicit witnesses, covering
supports 012,013,023,123 respectively, are

```text
{0,3,6,7}, {0,3,9,10}, {0,2,6,9}, {3,5,6,9}.
```

A vertex red to all three triangles would complete a red K5.

Write x_i for the number of vertices of signature `{i}`, y_ij=y_ji
for the number of signature `{i,j}`, and

```text
X = sum_i x_i,       Y = sum_{i<j} y_ij.
```

All vertices of F red to one triangle are pairwise blue: a red edge
between two of them would form a red K5 with that triangle. They therefore
number at most four, giving

```text
x_i + sum_{j != i} y_ij <= 4             for every i.       (1)
```

For every ordered pair i!=j there is also

```text
x_i + y_ij <= 2.                                          (2)
```

Indeed, any three vertices with signatures `{i}` or `{i,j}` are
pairwise blue by their common red adjacency to C_i. All three are
blue to the two minority triangles outside `{i,j}`. Those two triangles
have a blue edge between them. Its endpoints and the three vertices
of F would be a blue K5.

Sum (1) over the four indices, and (2) over the twelve ordered pairs:

```text
X + 2Y <= 16,          3X + 2Y <= 24.
```

Adding yields `4(X+Y)<=40`, hence `X+Y<=10`.

If X+Y=10, both summed inequalities are equalities. Every inequality
(2) is then tight. Comparing `x_i+y_ij=2` with `x_j+y_ij=2` shows
all x_i are equal. The two summed equalities give X=4 and Y=6, so
every x_i=1 and every y_ij=1. Equation (1) is also tight at every i.
This proves the lemma and its equality description without a solver
or exhaustive computation.

## Application to the order-three action

Every vertex fixed by the automorphism is uniform to each moving
triangle. The prior internal-color, matching and phase reductions force
the displayed H on the four minority triangles. Apply the lemma to
the thirteen fixed vertices. If z is the number with empty signature,

```text
z = 13-X-Y >= 3.
```

For z=3 the signatures are exactly three empty copies, four distinct
singletons and six distinct pairs. This does not require the fixed
vertices to be automorphic or any assumed ordering of their other edges.
Only their red adjacencies into H are described.

In the existing normalized full-extension formulas, fixed vertices are
sorted lexicographically by their ten incidence bits, with the four
minority bits first. All empty minority signatures therefore precede
the nonempty ones. Vertices 30,31,32 must consequently be blue to H.
This supplies twelve additional necessary unit assignments in that
normalization. It does not specify the mutual edge colors of those
three vertices. No new full-extension solver run is performed here.

## Complete census of the forced-blue multiplicity constraints

This is a separate necessary-condition census, not part of the hand
proof and not a classification of graph realizations.

Two vertices of F with intersecting nonempty signatures must be blue
to each other, since they are red to a common minority triangle.
Consider a nonempty family A of pairwise-intersecting nonempty
signatures. Copies of its signatures form a forced blue clique.
Let U be their union. Their common blue neighbors in H are precisely
the minority triangles outside U.

H has no blue triangle, and every two minority triangles have a blue
edge between them. Thus the size of this forced blue clique is bounded by

```text
2, if |U| is 1 or 2;
3, if |U| is 3;
4, if |U| is 4.                                          (3)
```

There are 58 pairwise-intersecting families on the ten nonempty
signatures. These 58 inequalities describe **exactly** the absence of
a blue K5 whose edges are already forced by H and the signatures:
a blue K5 can use at most two vertices of H, since H is blue-triangle-free.
With three, four or five fixed vertices, (3) supplies exactly the relevant
capacity. Empty-signature vertices have no forced blue edges to other
fixed vertices, so they cannot be in such a clique. Edges not forced blue
remain undetermined in this argument.

In particular every nonempty signature has multiplicity at most two.
The complete domain is therefore `3^10=59049` ten-tuples, with empty
multiplicity `z=13-sum(counts)` when nonnegative. Exactly 1,868 survive
the 58 inequalities:

| empty-signature multiplicity z | surviving count vectors |
|---:|---:|
| 3 | 1 |
| 4 | 10 |
| 5 | 50 |
| 6 | 178 |
| 7 | 424 |
| 8 | 548 |
| 9 | 405 |
| 10 | 186 |
| 11 | 55 |
| 12 | 10 |
| 13 | 1 |

The order of the ten masks is `[1,2,3,4,5,6,8,9,10,12]`, where bit i
means red adjacency to C_i. The complete survivor stream is regenerated,
not stored as a large list. Its format and SHA256 are recorded by the
verifier and [report.json](report.json).

Two algorithms compare every input decision. The first tests the 58
family inequalities. The second builds the literal forced-blue graph
on H plus thirteen labeled fixed vertices and searches for an actual
blue K5 using bitset clique recursion. It does not use signature-union
capacities. All 59,049 decisions agree. Cases with negative z are
rejected before graph construction. The recursion is additionally checked
against direct subset enumeration for every graph on five vertices and
every clique size 1 through 5.

These 1,868 vectors need not extend to a fixed-vertex coloring, six majority
triangles, the full degree bounds or a 43-vertex Ramsey graph. They do
not change the separate hard-branch profile/split counts maintained by
the structural researcher.

## Sharp local witness

The literal [sharp25.edges](sharp25.edges) has 25 vertices and 132 red
edges. Vertices 0..11 induce H. Vertices 12,13,14 have empty signature;
vertices 15..24 have the ten nonempty signatures above, in that order.
Its order-three automorphism rotates the four triangles and fixes the
other thirteen vertices, so it has type `1^13 3^4` on these 25 vertices.

Direct enumeration of all `C(25,5)=53130` five-sets finds no monochromatic
K5. All 300 pairs are checked for action invariance and all fixed
incidences are checked literally. The witness attains the lemma's
ten nonempty signatures and the campaign corollary's z=3 within this
core-plus-fixed-vertices relaxation.

It is **not** a 43-vertex target or an extension by six majority triangles.
The minority vertices have red degree eleven in this 25-vertex fixture,
not the full target's degree window. No complete ten-cycle equality
branch is asserted feasible. The witness shows that the local Ramsey
conditions on H plus thirteen fixed vertices alone cannot strengthen
the conclusion to z>=4.

The witness was found by a small SAT search on the 78 fixed-to-fixed
edge variables, projecting all five-sets of the 25-vertex template.
That discovery formula, solver log and model are not proof dependencies:
the complete edge list and direct standard-library checker suffice.

## Evidence and trust

The main lemma and equality case have the displayed hand proof. The
application imports the previously certified unique-core theorem. That
theorem now has an [accepted independent review](../ramsey_r55_order3_ten_cycle_phase_sweep_review1),
conditional on the older four-versus-six internal-color split. The prior
matching refinement has the same explicit conditional review boundary.
This result does not independently rerun or review the older split.

The new count-vector census and literal fixture checks use Python 3.11.2
standard-library exact integers. No LP, MILP, SAT status, graph catalog
or omitted certificate is needed for verification. Unformalized reasoning,
the published source, Python runtime, hardware and SHA256 remain trust
boundaries; the new lemma and its checker have not yet received
independent peer review. Internal agreement is not peer review.

Exploratory majority-triangle tables and triangle-common-neighborhood
relaxations supplied no exclusion in this pass. They are preserved
privately as discovery state, not used as theorem evidence. This
completed fixed-signature milestone leaves actual compatibility with
the six majority triangles for the next pass.
