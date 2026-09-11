# Exact graph completion across three degree classes

This directory gives an exact realization framework for **every** 54-vertex,
187-edge, girth-at-least-five candidate in the three degree classes z=9,10,11,
where z counts degree-eight vertices. The degree histograms are respectively
(13,32,9), (14,30,10), and (15,28,11) for degrees (6,7,8).
The complete cover has 15 formulas. No graph realization or whole-class
nonexistence decision has been obtained. The numerical bounds remain 185–187.

The accompanying [uniform high-path theorem](high_path_theorem.md) is a
human proof applying across the degree levels: for z<=12 the high graph
has only P1, P2, P3 components; for z<=8 it is a matching, for z<=10 there
is at most one P3, and for z<=11 there are at most two P3 components.
Every P3 at z<=11 contains a high sink. This supplies the optional
structural constraints in the complete graph model.

## A root misses at most one vertex in the three covered levels

Let a(t) count vertices at distance greater than two from a degree-eight
vertex t. The [weighted gap identity](../proof.md) gives

\[
\sum_{t\in V_8}a(t)(a(t)+4)\le256-19z.
\]

Choose a high vertex r with minimum deficit a. If z=11 then a=0,
since eleven positive deficits would cost at least 55>47. If z=9 or 10,
then a<=1, since all deficits at least two would cost 12z>256-19z.
Every other high vertex has deficit at least a. This uses no all-sink
assumption on the high class.

Let c be the number of high neighbors of r. Its neighbor degree counts
are (3+a+c,5-a-2c,c), hence c=0,1,2. The eight branches of children at
distance two have sizes

\[
5^{\,3+a+c},\quad 6^{\,5-a-2c},\quad 7^{\,c}.
\]

There are 45-a children and a outside vertices. Thus all variable edges
lie on exactly 45 vertices. The fixed radius-two tree has 53-a edges,
and a completion must add 134+a edges.
The complete (z,a,c) cover is

- z=9,10: a=0,1 and c=0,1,2, six formulas per degree class;
- z=11: a=0 and c=0,1,2, three formulas.

Different choices of a minimum-deficit root can give different c values;
this is an exhaustive cover, not a count of unlabeled graphs.

## Exact completion conditions

Fix the root, its eight parent vertices, the eight child branches, and
the a outside vertices. Keep only the fixed root-parent and parent-child
edges and the following variable edges: edges between different child
branches, child-outside edges, and edges between outside vertices.

For each of the 45 variable vertices select its original degree in {6,7,8}.
Subtract the fixed root and parent degrees from the prescribed histogram
to obtain the exact remaining class counts. A child of degree d must have
d-1 variable neighbors; an outside vertex must have d variable neighbors.
Require every variable vertex to have at most one neighbor in each real
child branch. Finally forbid every triangle and quadrilateral in the
variable graph. For each high vertex impose that its neighbor degree sum
is at most 53-a; this makes the root's deficit minimum. Other vertices
satisfy the usual neighbor degree sum bound 53.

**Equivalence theorem.** A graph with the specified degree histogram
exists if and only if at least one of the formulas in its cover is
satisfiable. A satisfying assignment decodes to a 187-edge graph, whose
simplicity, degrees, triangles and quadrilaterals are checked directly.

Necessity follows by labeling the disjoint radius-two ball of a
minimum-deficit high vertex. Edges within a branch would make triangles;
two neighbors in one branch would make a quadrilateral through its parent.
For sufficiency, the degree constraints give exactly 187 edges. A forbidden
short cycle entirely among variable vertices is excluded explicitly.
A triangle using a parent requires an edge within its branch. A quadrilateral
using one parent requires a variable vertex with two neighbors in that
branch. A short cycle using the root or two parents would require an
additional parent incidence, which is not an available edge. Thus no
triangle or quadrilateral is omitted. The outside vertices are precisely
those not within distance two of the root, so its deficit is exactly a.

The CNF lists triangles using three distinct blocks and quadrilaterals
using four distinct blocks, where each outside vertex forms its own
singleton block. A repeated real branch in a variable quadrilateral is
already impossible by the one-neighbor-per-branch clauses.

## Complete symmetry normalization

The first branch has minimum size five. Its edges to every other real
branch form a partial matching. Independently label that other branch
so each matching edge joins equal row indices; unmatched rows can be
filled arbitrarily because the other branch has at least five vertices.
The formula can therefore omit all unequal-index edges from the first
branch to other real branches.

Simultaneously permute the five row indices across all real branches to
sort the first branch's neighbor masks in descending order. Include its
outside-neighbor bits in these masks. This preserves all the equal-index
matchings and places no restriction on the outside labels. Thus every
admissible graph has a representative satisfying the normalization.
No forest, deficit multiset, or low incidence profile is fixed.

## Reproduction and evidence

The recorded environment is CPython 3.11.2, python-sat 1.8.dev24, pypblib
0.0.4, NetworkX 3.4.2 and NumPy 2.4.6. Install requirements.txt in a local
virtual environment. From this directory run:

```sh
python3 verify_high_paths.py
python3 check.py
python3 build.py --output /tmp/order54-rooted-cover
python3 solve.py --z 11 --a 0 --c 2 --structure --conflicts 500000 --output /tmp/order54-rooted-search
```

Use new output directories. The first command matches
[high_paths_expected.json](high_paths_expected.json): 95 atlas graphs,
9,794 three-vertex-path color checks and 3,026 four-vertex-path color checks.
The second matches [controls_expected.json](controls_expected.json),
including every root of the Petersen graph with an edge deleted, a
Hoffman–Singleton graph, all 2,048 assignments of a small one-outside-vertex
model, and three roots of the known 54-vertex,185-edge graph. The control
checker uses integer adjacency-matrix products, independently of the CNF's
cycle enumeration. The full cover regenerates and compares all 15 hashes
in [formulas_expected.json](formulas_expected.json).

[search_summary.json](search_summary.json) records bounded searches and
calibration. Glucose and CaDiCaL found valid Hoffman–Singleton completions
from scratch in under a second. The z=11 baseline, gap-strengthened, and
high-structure searches did not decide any complete degree class.
Two base formulas, (z,a,c)=(9,1,2),(10,1,2), were UNSAT; their DRAT traces
were checked independently. They also have a short human refutation:
three nonsink vertices in a high P3 have total deficit at least three,
contradicting the high-path bound A_T<=z-9. These are auxiliary validations,
not whole-class nonexistence claims.

The --gap option adds the exact local q-degree costs with total at most
256-19z; it discards only the nonnegative distant-pair term. The --structure
option adds the proved high-path restrictions. Both keep the equivalence
theorem. They are optional because stronger mathematical constraints can
make a particular SAT encoding slower. Solver UNKNOWN or an interrupted
run establishes neither satisfiability nor unsatisfiability. UNSAT traces
require a separate proof checker; source publication alone is not a proof.
Large formulas, traces and exploratory state are kept outside the repository.

The main trust boundaries are the imported order-53 bound, the written
rooting and symmetry arguments, the CNF generator, PySAT's exact cardinality
and optional PB encodings, and the graph decoder. There is no claim of
formal proof, exhaustive 54-vertex graph enumeration, or historical priority
for this standard rooted-completion method.
