# The saturated blue neighborhood of an empty fixed vertex

Let G be a hypothetical Ramsey(5,5;43) graph with an order-three action
`1^10 3^11`, in the four-red/seven-blue internal moving-triangle split.
The existing complete normalization places four internally red triangles
at C0,...,C3 and seven internally blue triangles at C4,...,C10.

The accepted forced-empty theorem and fixed-row order make the first fixed
vertex e blue to every vertex of C0,...,C3 for the current residual cores.
Let b count blue moving triangles blue to e, and h its red neighbors among
the other nine fixed vertices. Uniformity gives

```
d_red(e) = 3(7-b)+h,  d_blue(e) = 21+3b-h.
```

The inherited degree window 18..24 implies b<=4. If b=4, necessarily h=9:
e has exactly 24 blue neighbors, all moving, and all other fixed vertices
are red to e. N_blue(e) therefore consists of the four red triangles and
four selected blue triangles.

Its induced graph H has no red K5 by heredity and no blue K4, since a blue
K4 together with e would be a blue K5. The order-three action restricts to
eight moving cycles on H, with four internally red and four internally
blue. Its red core is the same twelve-vertex core as in G.

This pass examines this necessary local condition for precisely the six
maximal-attachment branches still unresolved by the preceding full test:

| Core | Red cross words concatenated in pair order 01,02,03,12,13,23 |
|---|---|
| 124 | 000110110011101110 |
| 155 | 100100110001101110 |
| 159 | 100100110011001110 |
| 168 | 100100110011110110 |
| 180 | 100100110101100110 |
| 194 | 100110110110110100 |

These are five two-anchor classes and one four-anchor class, representing
2,349 labeled red cores. They are part of the 18 still-open full classes;
the other twelve full classes already have a proved b<=3 bound and are
not tested here.

## Why one local formula covers all selected blue triangles

Keep the red core labeled exactly as in its full representative. Relabel
the four chosen blue moving triangles as local C4,...,C7, preserving the
direction of the order-three generator on each. Local phases are unrestricted.
No other moving triangle, fixed vertex, incidence count, degree bound or
full-parent ordering constraint is imported into H.

Every selection of four out of the seven full blue triangles restricts to
one assignment of this same local formula: their original names disappear
when the omitted vertices and all external incidences are forgotten.
Conversely, every model of the local formula is precisely an invariant
24-vertex graph with the stated core, internal colors and clique conditions.
There is no claim that it extends to the omitted nineteen vertices.

In particular, no arbitrary first-four selection is imposed in G. This
is a forgetting map to a local graph with four freely labeled blue cycles,
not a reordering under the full parent's normalization. No symmetry-breaking
clause is needed. A local refutation thus rules out the whole b=4 branch for
that core, including all 35 choices of selected blue triangles. It does
not rule out its b<=3 full extensions.

A local witness establishes that this exact neighborhood condition alone
cannot refute the corresponding maximal branch. The omitted nineteen
vertices and their incidences still require a full extension.

## Exact local encoding

Use vertices 0,...,23, with C_i={3i,3i+1,3i+2}. Positive Boolean variables
mean red edges. For i<j and d in Z/3, a single variable x_(i,j,d) controls
all edges (3i+s,3j+t) with t-s=d modulo 3. There are
`3*C(8,2)=84` variables, in increasing (i,j,d) order. Internal edges are
constant red for i<4 and blue for i>=4.

For every five-set, forbid all its pairs being red; for every four-set,
forbid all its pairs being blue. Constant opposite-color pairs make a
prohibition automatically true, so those clauses are omitted. Repeated
variables within a clause and identical clauses are removed. Exactly
26,712 five-sets and 8,076 four-sets survive constant simplification;
together they yield 11,566 distinct clauses. Append the 18 signed units
for the chosen red core, yielding 84 variables and 11,584 clauses.

The local core variable IDs are

```
1,2,3,4,5,6,7,8,9,22,23,24,25,26,27,40,41,42.
```

They differ from the 43-vertex parent's IDs. The independent checker
recovers them by literal edge-orbit enumeration on 24 vertices. There are
no auxiliary variables, degree constraints, or normalization clauses.

A model decodes to an invariant graph because each edge orbit has one
color. Each generated clause rules out exactly its monochromatic subset,
and every forbidden subset either supplies a clause or already contains
an opposite-color constant. Thus the formula is equivalent to the stated
local graph problem in both directions. This equivalence is stronger than
the one-way restriction from a full 43-vertex graph to H.

## Verification and scope

The generator uses coordinates and phase differences. The independent
auditor imports no producer and enumerates physical pair orbits under the
literal 24-vertex permutation. It reconstructs every clause from physical
four- and five-sets, retains all 18 core units, and checks header, exact
clause order and EOF. Its independent representation has 276 physical
pairs and 84 variable orbits. Fresh verification repeats all six formulas.

For one, two and three moving triangles, for each prefix internal red
count, the controls examine every invariant cross-coloring: 2,074 small
graphs in all. Direct monochromatic-subset tests agree with satisfaction
of the corresponding generated formula. Nine malformed case records or
formulas are rejected. Normal and optimized Python reports must agree.

An UNSAT result requires full DRAT replay including RAT steps, followed by
a second replay against the freshly reconstructed formula. A SAT result
requires a compact red-edge list and a standalone literal checker. That
checker verifies the exact order, absence of red K5 and blue K4, all internal
colors, order-three invariance, and the literal red-core word. Five malformed
witnesses must be rejected. The checker uses no SAT solver or formula to
establish a witness's validity. UNKNOWN is inconclusive.

The inherited full-core cover, forced-empty theorem and degree theorem
are used only to identify the six branches and justify a possible transfer
of local obstructions. A local witness or local formula refutation can be
checked directly for its explicit core without importing any full-core
exclusion chain. Any cumulative full-core counts retain their existing
review boundaries. New code and local outcomes await independent review.
Ordinary unformalized reductions, exact source, interpreter/hardware and
hash identity remain trusted; a refutation additionally trusts the full
DRAT checker. Internal independent checking is not peer review or formalization.
No full-core exclusion, complete eleven-cycle exclusion or new Ramsey lower
bound follows merely from this local test.
