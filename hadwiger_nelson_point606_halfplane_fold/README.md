# A capped reflection fold of the point606 critical graph

The selected whole-plane fold produces **508 distinct exact points and 2,215
strict unit edges**, with a checked proper four-colouring. It does not improve
the Hadwiger–Nelson record. This package closes one physical construction gate;
it does not classify other axes, pointwise reflection choices, multiple folds,
or the other geometrically eligible folds considered at intake.

## Construction and physical cap

Let P be the 530-point, 2,648-edge critical graph reconstructed from
[`hadwiger_nelson_point606_criticality_gate`](../hadwiger_nelson_point606_criticality_gate/README.md).
Its exact five-chromaticity and vertex-criticality have an
[independent accepted review](../hadwiger_nelson_point606_criticality_gate_review1/README.md).
The present upper-colouring certificate does not depend on that non-four
proof and does not replay it.

Use positive square roots and put

```
c = -(sqrt(3)+sqrt(11))/6,
F(x,y) = (x, c + |y-c|),
Q = {F(p) : p in P}.
```

Thus the negative side of the horizontal line y=c reflects into the positive
side. Exactly106 source points move, nine lie on the axis, and22 disjoint
source pairs merge. The resulting508 points include84 positions outside P.
No source vertex was deleted. The operation changes the obstruction's
physical support, so the vertex-criticality of P alone does not decide Q.

Coordinates use denominator288 in the basis
`1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165`. The reflection formula
on the moving side is `y' = -(sqrt3+sqrt11)/3 - y`, which stays in this field
without introducing new denominators. Rational enclosures of the positive
radicals determine each side exactly; coefficient equality handles points on
the axis. Distinct coefficient vectors represent distinct real points.

Before the ordinary chromatic query, exact geometric accounting over normals
(1,0), (0,1), (1,1), (1,-1) found32 folds of this source within the cap. The
selection rule was largest capped order, then fewest lost source edges,
then lexicographic axis. Only the selected fold was tested for colourability.
Those intake counts are historical selection evidence, not a positive signal
or a complete chromatic classification of32 graphs.

## Complete unit graph and certificate

All128,778 unordered pairs in Q are reconstructed and tested exactly. The
image retains2,151 source unit edges when counted with source multiplicity;
497 source edges lose unit length. There are104 image unit edges that do not
come from a source edge. Thus the source's chromatic lower bound does not
transfer by a unit-edge-preserving map. The new graph has2,215 distinct edges.

`certificate.json` supplies508 colour digits, in lexicographic order of the
integer coordinate tuples. The verifier checks their domain and all2,215
edge inequalities. This proves `chi(UD(Q)) <= 4` and the same upper bound
for every subgraph of this one complete image graph. No SAT answer or
negative proof trace is required for this conclusion. Exact chromatic
number four is not claimed.

The scratch discovery query used ordinary four-colouring clauses: one
at-least-one-colour clause per vertex and one inequality clause per unit edge
and colour. Adjacent selected-colour sets are disjoint, so choosing one
selected colour per vertex is sound. Kissat4.0.4 returned SAT in approximately
0.062 seconds; its decoded literal word was checked. No other fold received
a SAT query and no solver remains running.

Exact containment checks against the existing P25/P44/L2, D7, U553, H574,
pure644 switching and H560 hosts found points outside every one. The minimum
outside count was78. These checks occurred after the fast SAT query, before
publication; they were not a premise of the decision. No general separation
from every previously studied host is claimed.

## Reproduction and validation

Keep a complete checkout of the repository so that the three hash-bound
sibling inputs in `inputs.json` are available. CPython3.11+ and its standard
library suffice. From the repository root:

```sh
python3 -B hadwiger_nelson_point606_halfplane_fold/verify.py
python3 -B -O hadwiger_nelson_point606_halfplane_fold/verify.py
python3 -B hadwiger_nelson_point606_halfplane_fold/audit.py
python3 -B hadwiger_nelson_point606_halfplane_fold/controls.py
```

Expected: `vertices=508`, `unit_edges=2215`,
`proper_four_colouring_checked=true`, `record_candidate=false`.

The separate distance audit first excludes nonunit pairs modulo1321 using
checked square roots, then tests survivors with generic square-free-radical
multiplication. It compares the entire edge list with the primary checker.
It shares coordinate parsing, side certification and collision merging with
the primary code; it is same-author validation, not independent peer review.
Controls cover exact side signs, a merging pair plus an axis point, and
malformed/monochromatic colour words. Normal and optimized outputs agree.
Input interpretation, exact Python arithmetic, the elementary reflection
formula and the literal colouring are the trust boundary; no formalization
is claimed.

The source package is compact; exploratory axis accounting, source-to-image
labels, solver CNF/logs and expanded coordinates remain outside Git. The
public fixed-support checker regenerates everything needed for its stated
four-colour claim. `VALIDATION.json` records the executed checks.

## Construction boundary

Retire this selected fold. Reaching508 physical points did not preserve the
five-colour obstruction. The nearby-axis, other-half-plane, second-fold and
subset variants are not opened by this result. The unresolved selection
problem is to change a certified positive parent's core while supplying a
trustworthy obstruction that survives at the physical cap. A coordinate
budget or inherited positive parent alone does not supply that signal.

This is a negative construction checkpoint, not an improvement to the
published509-vertex record ([Parts](https://arxiv.org/abs/2010.12665)).
No novelty or priority claim is made for folding or for this isolated
four-colourable graph. No Discovery contribution is being added for this
small negative gate; historical pending receipts remain unchanged.
