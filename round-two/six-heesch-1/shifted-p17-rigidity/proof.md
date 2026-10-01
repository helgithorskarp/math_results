# Rigidity of the doubled P17 inner network with unit placement shifts

Actual author **six-heesch-1**, role **researcher**, 2026-10-01. This is an
author-checked finite computational lemma with a written encoding argument.
It is unformalized and has no independent-review verdict. It supplies a
specific obstruction to prototype deformation, not a new Heesch record.

## Precise finite family

Let P be the seventeen-cell square polyomino specified in `input.json`.
This is the P17 example from zero-based entry 43 of
[Kaplan's primary table](https://cs.uwaterloo.ca/~csk/heesch/omino/17omino_2up.txt).
The table reports Hc=Hh=3 on the square grid. Our earlier
[all-motion exact-value proof](../p17-exact-three/proof.md) establishes that
same value for arbitrary Euclidean rigid motions and reflections.

The attributed three-corona construction has cumulative copy counts
1, 7, 19, 36. Each physical map is written

    g_j(x)=A_j x+t_j,

where A_j is an orthogonal signed permutation matrix. The input lists all
36 maps. These were recovered from the literal normalized orientations of
the earlier witness, including the unit-cell offset for negative axes.
The root map is the identity. Only the first 19 designated maps, at levels
0, 1, 2, are used in the rigidity test.

Define the prototype-cell pool and anchor by

    D={(x,y) in Z^2: 0<=x<12 and 0<=y<10},   a=(2,0).

Let M be any cell mask contained in D and containing a. Regard it as the
union of its closed unit squares. Keep the root map the identity. For each
other designated copy choose independently

    delta_j in {-1,0,1}^2,   f_j(x)=A_j x+2t_j+delta_j.

Thus there are nine pose options per nonroot copy and 163 options in total.
Orientations and designated levels stay fixed. Let P_k be the union of the
designated copies through level k, for k=0,1,2.

**Claim.** Suppose M and all three P_k are closed topological discs, the
19 whole-copy interiors are pairwise disjoint, and

    P_0 subset int(P_1),   P_1 subset int(P_2).

Then M is exactly the 68-cell mask representing the homothetic tile 2P.
There is no area hypothesis. The conclusion also holds if the usual
requirement that every new copy touch the preceding prefix is added.

The rectangle and anchor are explicit hypotheses. They are not universal
bounds for unknown prototypes. Other masks, orientations, placements,
additional copies and corona networks are outside this statement.
In particular, allowing holes or pinches in P_2 is not covered. For the
finite-five target, the inner prefixes must be discs anyway.

## Necessary Boolean encoding

Use one variable x_p for each p in D, and fix x_a true. For each designated
copy choose exactly one option y_o. The root's only option is true. Define
z_(o,p) equivalent to x_p AND y_o. At each world cell impose at most one
potential z occupant. Different options of the same copy cannot both be
selected, so including them in the same group is harmless. Each selected
option maps cells bijectively; hence these clauses express whole-copy
interior disjointness without allowing clipping.

For every prefix k and potential world cell q define u_(k,q) equivalent to
the OR of its occupants with designated level at most k. A missing cell
has constant false occupancy. For k=0,1 and every occupied q require
u_(k+1,q+d) for the eight nonzero vectors d in {-1,0,1}^2. For integral
unit-square unions this collar condition is equivalent to strict inclusion
in the next prefix's interior. It is also necessary directly: the closure
of a predecessor cell includes its four sides and vertices, so every
neighboring unit cell must be present in any integral strict surround.

At each grid vertex prohibit either pattern of exactly two occupied
diagonal quadrants and two empty quadrants. Writing the four occupancy
literals as a,b,c,d in a two-by-two square, the clauses are

    (-a,b,c,-d),   (a,-b,-c,d).

A closed disc cannot have this pinch. Full connectedness and hole-freeness
of the prefixes are omitted; the test is a necessary relaxation.

Finally every selected prototype cell must have a selected edge neighbor.
This is necessary for an edge-connected mask of at least two cells. A
singleton cannot satisfy the first collar condition: its eight neighbors
would need covering by only six other singleton copies. Thus the
non-isolation clauses discard no admissible connected prototype.

Add one clause excluding the complete control mask 2P:
negative x_p literals for its 68 cells, positive x_p literals for D minus
those cells. The desired theorem is that this necessary formula is
unsatisfiable.

AND and OR gates are exact equivalences. At-most-one is encoded by a
running prefix OR: for x_1,...,x_r, start s=x_1, then add (-s,-x_i) and
replace s by the exactly defined OR(s,x_i). This accepts every group with
at most one true member and excludes every group with two true members.
Every admissible geometry therefore extends to all auxiliary variables.
Conversely, no converse to the omitted topology conditions is needed.

## Complete finite reconstruction and certificate

`model.py` constructs all incidences from forward cell images

    A_j p + (min(a,b,0),min(c,d,0)) + 2t_j+delta_j

for A_j=(a,b;c,d). Independently, `inverse_incidence` enumerates world-cell
centers in doubled coordinates, applies A_j transposed to the center minus
the physical translation, and recovers its prototype-cell corner. It
does not call the forward cell-image function. `check.py` compares every
one of the 19,560 option/cell incidences, then constructs a fresh complete
formula from those inverse incidences. Both formulas are identical.
The Boolean compiler is shared; this is an explicit trust boundary.

The formula has 40,141 variables and 170,689 clauses. Its complete DIMACS
SHA-256 is

`ca4c01f8120cca3eb43b84a4b9a08ec8767cd61558790669d15769bf6a4b043f`.

The source includes `mask.rup`, a 70,313-byte trace with 510 additions.
The independent reader accepts an added clause only if the existing
formula plus the negations of that clause's literals unit-propagates to
a contradiction. This reverse-unit-propagation rule proves each clause
from its predecessors. Induction and the final empty clause establish
unsatisfiability. No SAT solver is required for the published reader.

Discovery used PySAT 1.8.dev24 / Glucose4. Its deletion-free trace had 602
additions and 84,436 bytes; all additions passed the exact Python reader.
The retained dependency trace is checked afresh on the inverse formula.
Deleted clauses were retained during checking: retaining proved
consequences preserves each unit-propagation contradiction. The solver's
native UNSAT result itself is not a premise.

The five byte-pinned source dependencies are listed in
`dependencies.json`. They include the physical-source fixture, exact
isometry helper, Boolean gates, closed-disc cell checker and RUP reader.
The elementary geometric bridges above, those programs and CPython are
the trust boundary; no proof-assistant certification is claimed.

## Positive control and implications

The reader checks all 36 zero-shift copies of 2P, not only the inner 19.
Each physical footprint agrees with a literal scaled source footprint.
Copies do not overlap, every prefix is a disc, every collar is complete,
and every designated new copy touches the prior prefix. The cumulative
cell counts are 68, 476, 1292, 2448. The corresponding mask and zero-shift
options satisfy every necessary clause before the control-exclusion
clause. Four false or malformed controls are rejected.

Euclidean homothety preserves corona existence and nonexistence: conjugating
a rigid motion by x -> 2x is still a rigid motion, and strict nesting,
contacts and disc topology are preserved. Thus 2P has all-motion
Hc=Hh=3 by the earlier exact-value theorem. The only prototype permitted
by this finite network family cannot achieve the finite-five target.
This does not bound Heesch numbers of prototypes outside the family.

The result rules out repairing this network by changing the prototype
inside the stated rectangle while independently moving the inner copies
by zero or one cell in each coordinate. A different network or a change
outside the listed hypotheses is needed. It does not prescribe how much
such a change must be or claim that a nearby successful prototype exists.

## Credit and scope

[Kaplan's paper](https://arxiv.org/abs/2105.09438) supplies the prior-art
shape, census and corona conventions; its grid restriction is not silently
replaced by a global claim about this finite family. The lower witness is
attributed through the byte-pinned [P17 source](../p17-exact-three/input.json).
The earlier [exact-three proof](../p17-exact-three/proof.md) motivated the
new search and supplies only the homothety corollary's exact Heesch value.
It is not a premise of the finite rigidity refutation.

The complementary [six-heesch-2 shifted-polyhex lemma](../../six-heesch-2/shifted-inner/proof.md)
uses an unknown mask with independent placement options in a different
199-cell hexagonal pool. Its committed graph reference is
`bafkreighl7grmik3pduzwoi5dwuqnakprthmqt3rqbz55d7c57nqrsxgoq`
(height 8849), source `fbc0b1936e334dcda2b41d1b627a0c16d661e989`.
It is complementary precedent, not a mathematical premise or an
independent audit of this square-cell theorem. No historical-priority
claim is made for the Boolean encodings or the RUP rule.
