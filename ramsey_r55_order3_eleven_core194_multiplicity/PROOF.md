# A complete seven-case multiplicity split of Core194

Let G be a hypothetical Ramsey(5,5;43) graph with action `1^10 3^11`,
four internally red moving triangles C0,...,C3, seven internally blue
triangles, and canonical red core `100110110110110100` on pair order
01,02,03,12,13,23. A fixed vertex has signature S, the set of red moving
triangles joined red to it. Let z count empty signatures, x_i count
singletons {i}, and y_ij count pairs {i,j}.

The accepted forced-empty theorem gives z>=1. All four complementary
three-triangle anchors apply to Core194, so the accepted intrinsic anchor
theorem gives z+x_i>=2 for every i. The proved sharp pair bounds give
x_i+y_ij<=2 for all ordered distinct i,j. These constraints are already
in the complete inherited base; their earlier UNKNOWN outcomes play
no role as mathematical premises.

## Six necessary patterns when z=1

Each complementary nine-vertex core has a red K4. For omitted indices
0,1,2,3, respectively, literal witnesses are

```
{3,4,7,10}, {0,1,7,10}, {0,3,9,10}, {0,3,6,7}.
```

A fixed vertex red to any three red triangles would complete a red K5
with the corresponding witness. Therefore every fixed signature has
size at most two. This observation holds for all z, not just z=1.

Now assume z=1. The anchors give x_i>=1, while x_i+y_ij<=2 and
nonnegativity give x_i<=2 and y_ij<=1. Let k count singleton types
occurring twice. There are 4+k singleton vertices, so the remaining
5-k fixed vertices have pair signatures. A pair touching a doubled
singleton type has multiplicity zero, by the same sharp inequality.
Hence

```
5-k <= C(4-k,2).
```

For k=1,2,3,4, the left sides are 4,3,2,1 and the right sides 3,1,0,0,
contradictions. Thus k=0. Each of the four singleton types occurs once;
exactly five of the six pair types occur once. The missing pair is the
only choice: 01,02,03,12,13 or23. This classifies necessary signature
multisets; it does not assert that any multiset extends to a full graph.

The independent auditor checks all 48,620 weak compositions of nine
vertices into the four singleton and six pair types. Imposing the anchor
and sharp inequalities leaves exactly those six multisets. Literal
K4 witnesses justify omitting larger signature types from that count.

## Complete full-graph branches without a new normalizer

The accepted parent sorts fixed vertices 33,...,42 lexicographically by
their eleven red incidence bits, with the four red-core bits first.
Their four-bit prefixes are consequently ordered, and every empty
prefix precedes every nonempty prefix. For z=1, all ten prefixes in
each derived multiset are distinct, so their row locations are determined.

Masks below use bit i for membership of Ci. The sorted order compares
bits in the sequence i=0,1,2,3, rather than comparing mask integers.

| Missing pair | Prefix masks at fixed rows 33,...,42 |
|---|---|
| 01 | 0,8,4,12,2,10,6,1,9,5 |
| 02 | 0,8,4,12,2,10,6,1,9,3 |
| 03 | 0,8,4,12,2,10,6,1,5,3 |
| 12 | 0,8,4,12,2,10,1,9,5,3 |
| 13 | 0,8,4,12,2,6,1,9,5,3 |
| 23 | 0,8,4,2,10,6,1,9,5,3 |

Each of the six one-empty formulas assigns the four red-core links
at rows 34,...,42 accordingly, using exactly 36 primary units. Row33's
empty prefix is already in the base. No fixed edge or blue-cycle
attachment is specified. No missing pair is identified with another
by a stabilizer or selected arbitrarily; all six cases are retained.

The seventh case is z>=2. Since row33 is already empty and prefixes are
ordered, it is equivalent to row34 also having empty prefix. It adds
only the four units -222,-223,-224,-225. Other fixed signatures remain
free subject to the full inherited constraints.

The six one-empty cases and this multiple-empty case are disjoint and
exhaustive for hypothetical full Core194 extensions. The one-empty
classification, not mere Boolean splitting, justifies replacing the
nonzero second-prefix branch by these six precise multisets. There is
no imported three-versus-eight equality pattern, selected fixed graph,
degree profile or additional automorphism.

## Exact inherited full base and evidence

The base F is the entire [guarded full Core194 formula](../ramsey_r55_order3_eleven_core194_full),
whose 350 guarded attachment clauses follow from the independently
accepted [Core194 maximal-branch exclusion](../ramsey_r55_order3_eleven_core194_maximal_review1).
It contains all parent Ramsey, degree, auxiliary and normalization
clauses; eighteen core units; all four intrinsic anchor constraints;
the first empty prefix; 1,440 sharp pair cuts; and the ten guarded bounds.

Its identity is 24,968,396 bytes, SHA256
`f7f9eab7a28f32f56bebd54349db8a0e06010274bb16df9f90cbbb9b982216bf`,
with 34,320 variables and 617,932 clauses. Every body byte is retained.
Each one-empty child has 617,968 clauses, and the multiple-empty child
has 617,936 clauses. There are no new auxiliary variables or normalizers.
The guarded base's previous UNKNOWN is not a premise for these cuts.

The producer rebuilds the complete inherited preparation and guarded
base in an isolated namespace. A separate literal auditor reconstructs
320 primary meanings from physical edge orbits, checks all complementary
K4 witnesses, exhausts the count domain, verifies the exact seven-case
cover, and compares every base byte, child unit, header and EOF. It checks
all 2,048 full rows for the prefix-order implication and all sixteen
second prefixes for the zero/nonzero partition. Twenty-one malformed
certificates, cases or formulas must be rejected under normal and
optimized Python, whose reports agree.

Each case receives one bounded full solve. An UNSAT exit must pass full
DRAT replay including RAT steps. Fresh verification rebuilds the entire
base and all seven formulas and replays every refutation again. UNKNOWN
is inconclusive; its partial trace is neither a proof nor saved solver
state. A SAT target needs a compact edge list and literal inspection of
every five-set.

Only refuting all six one-empty cases implies z>=2. Only refuting the
multiple-empty case implies z=1. A whole-Core194 exclusion requires all
seven refutations. The six one-empty cases are subdivisions of the same
81-label core class; their label counts cannot be added as six distinct
whole classes. The other sixteen residual cores are not tested.

The new rigidity lemma, seven-case bridge and computational outcomes
await independent review. The parent, core cover, intrinsic anchors,
forced-empty theorem and maximal Core194 exclusion have accepted reviews
at their stated scopes; the guarded full encoding has author checking.
Cumulative counts retain older empty-signature-specific review boundaries.
Other trust comprises imported R(4,5)=25, unformalized reductions, exact
source/runtime/compiler/hardware, SHA256 and full DRAT checking. Internal
reconstruction is not peer review or proof-assistant formalization.
No new Ramsey lower bound is asserted.
