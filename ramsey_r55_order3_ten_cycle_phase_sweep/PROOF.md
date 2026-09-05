# A unique minority core at ten moving 3-cycles

Let G be a graph on 43 vertices containing neither a clique nor an
independent set of order five. Suppose it has an automorphism of type
`1^13 3^10`. The preceding
[internal-color theorem](../ramsey_r55_order3_ten_cycle_obstruction/PROOF.md)
and [minority-matching theorem](../ramsey_r55_order3_ten_cycle_anchor_sweep/PROOF.md)
are dependencies. After complementation, four moving triangles are red
and six are blue. At each red triangle, the three red-to-red block weights
are 1,2,2, while the six red-to-blue weights are p ones and 6-p twos for
`1<=p<=4`. A block weight counts red neighbors per vertex across the
invariant three-by-three block.

## The additional conclusion

The twelve vertices in the red moving triangles induce the graph H below,
up to relabeling. Label these vertices `3i+s`, `0<=i<4`, `s in Z/3Z`.
All four internal triangles are red. For i<j, the edge from `3i+u` to
`3j+v` is red exactly when

```text
v-u = 0 mod 3,          if (i,j) is (0,1) or (2,3);
v-u in {0,1} mod 3,     for the other four pairs.
```

Thus the six normalized words are

```text
01:100   02:110   03:110   12:110   13:110   23:100.
```

The literal [42-edge list](minority_core.edges) has twelve vertices,
not 43. Its red graph is 7-regular and its blue graph is 4-regular and
triangle-free. The red clique counts at orders 3,4,5 are 52,18,0.
The blue triangle count is zero, so H has red independence number two.
These are exact inspections of the forced core, not graph-existence
claims at order 43.

Every vertex fixed by the automorphism is red to all or none of each
red moving triangle. It can be red to **at most two** of the four.
For every three of these triangles, H contains a red K4 supported on
their union; a fixed vertex red to all three would complete a red K5.
Conversely all eleven binary signatures of weight at most two extend
H by one fixed vertex without creating a monochromatic K5 in that
13-vertex graph. This converse is only a local fixture statement; it
does not assert compatibility with any further vertex or degree condition.
`inspect_core.py` independently checks all sixteen literal extensions.

The whole ten-cycle type remains open. The four unresolved anchor
profiles have the same indices 64,65,67,69 as before, now restricted
to this one core. The global lower bound of ten moving cycles is unchanged.

## Complete phase cover

Normalize the minority matching to 01 and 23. Independent cyclic shifts
of cycles 1,2,3 make the anchor words 01,02,03 respectively 100,110,110.
Each word of weight one or two has exactly three cyclic rotations, so
the remaining words on 12,13,23 leave exactly `3^3=27` phase choices.
For a phase tuple `(a,b,c)`, rotate 110 left by a on 12, rotate 110 left
by b on 13, and rotate 100 left by c on 23.

The eight permutations of the four cycles preserving the matching may
be applied, followed by rephasing against the new anchor. Also allow
the simultaneous replacement `s -> -s` on **all ten** moving cycles,
again followed by rephasing. Reflection conjugates the order-three
permutation to its inverse. It therefore preserves invariance, although
it need not commute with that permutation. It would be incorrect to
reflect only some moving cycles in the full graph.

These operations give six orbits of the normalized phase triples:

| representative | number of normalized triples | four anchor cases |
|---|---:|---|
| (0,0,0) | 1 | open |
| (0,0,1) | 4 | excluded |
| (0,1,0) | 8 | excluded |
| (0,1,2) | 8 | excluded |
| (1,1,1) | 4 | excluded |
| (1,2,2) | 2 | excluded |

The classes concern this action and normalization. We do not claim that
they are six distinct abstract graph-isomorphism classes. All 27 core
graphs alone contain no monochromatic K5; their exclusion needs the
full extension constraints.

`model.py` computes the induced action on three-bit words. The separate
`audit.py` applies the actual twelve-vertex permutations, compares every
one of the 66 edges, checks the normalizer identity, and compares all
432 transformed phase entries. It verifies orbit closure, disjointness
and full coverage, not just the six class sizes.

After choosing the core representative, phase-shift the six blue cycles
so their words to the new red anchor are 100 or 110. Sort those cycles
by weight. The anchor has some `p in {1,2,3,4}`; choosing the core
representative might change which red triangle is anchor, so all four p
values are retained in every core class. Finally sort the thirteen fixed
vertices by their ten-bit incidence signatures. Repeated signatures are
allowed. This ordering does not change the core or its phases.

Consequently the six core classes times the four anchor profiles cover
every hypothetical target of this cycle type. The cases need not cover
all raw assignments of the unnormalized parent CNF; the proof requires
coverage of graphs up to the stated valid relabelings. Prefix-counter
auxiliaries are extended afresh after relabeling. They are not assumed
to transform by a permutation of their variable names.

`controls.py` additionally checks 96 whole-graph normalizations on
deterministic invariant-graph fixtures, including all maps from the 27
phase states to their representatives, arbitrary majority orbit bits,
permuted majority cycles and permuted fixed vertices. It checks the
full 903-pair invariance, internal colors, resulting core, anchor words,
anchor-profile membership and final signature ordering. These fixtures
test the implementation; the relabeling argument supplies universal coverage.

## Exact full-extension formulas

The base is the complete published r=4 formula, with 28,950 variables
and 927,000 clauses, including fixed-vertex degree counters. Its SHA256 is

```text
f01c990a1dae17fb7bc1cd633d785cd819ba9f4d1a1eeacd69b4034663af104e
```

The first 343 variables describe red unordered-pair orbits. All
`C(43,5)=962598` five-sets are projected in both colors; internal
triangles have their prescribed constant colors. The base also retains
the previously proved moving-row deficit, common-neighborhood, degree,
phase-order and fixed-signature constraints. The parent Python generator
and separate C++ checker reconstruct every primary and auxiliary clause.
The checker derives the pair orbits from the actual action. Neither
the fixed degree bounds nor their repeated edge multiplicities are omitted.

The new formula appends exactly 334 clauses and 24 fresh variables:

1. Thirty clauses force the six minority-block weights to the perfect
   matching pattern. For each three-bit block, they exclude the five
   assignments of the wrong weight.
2. Forty-eight clauses force each of the 24 mixed blocks to have weight
   one or two, excluding its all-zero and all-one words.
3. For each mixed block a new Boolean z is equivalent to weight one.
   Its eight truth-table implications give 192 clauses in total.
   The new variables are 28951 through 28974, in minority-row-major order.
4. At each minority row, one positive six-literal clause forces at least
   one z, and six negative five-subset clauses force at most four.
   This gives another 28 clauses. The first four items total 298.
5. Twenty-seven units specify one of the four normalized anchor profiles.
6. Nine units specify the three remaining minority-block phases.

Every case therefore has **28,974 variables and 927,334 clauses**.
Items 1--4 use the already proved simultaneous minority-matching theorem
at all four minority triangles. They do not presume additional symmetries,
M=214, a degree profile or a selected exceptional core.

The appended-clause audit independently recovers the variable meanings
from actual unordered-pair orbits. It exhausts the local assignments for
exact weights, each mixed-block gate and each six-bit row bound: 688
truth assignments per case. It then compares the entire 334-clause
multiset with the generator. Each generated case must have the unchanged
parent byte stream, correct header, exact audited tail and no trailing
data. All 24 case meanings are checked.

## Checked finite exclusions

The deterministic case index is `4*class_index + anchor_index`, with the
classes in the table's order and anchors `[64,65,67,69]`. Those anchor
profiles, in that order, have p values `[4,3,2,1]` and weights

```text
64: (1,2,2; 1,1,1,1,2,2)
65: (1,2,2; 1,1,1,2,2,2)
67: (1,2,2; 1,1,2,2,2,2)
69: (1,2,2; 1,2,2,2,2,2).
```

All 24 cases were run with two workers and a native 30-second Kissat
limit per case. Cases 4 through 23 have checked UNSAT proofs. Cases 0
through 3 reached the limit and remain open. They are not feasible
witnesses, and their incomplete traces are not certificates. The bounded
sweep finished in 155.037 seconds; the largest child peak RSS was
495,708 KiB. All generated formulas and original traces remain outside Git.

The used input clauses and proof lemmas were then extracted for each
of the twenty exclusions, and each extracted pair was replayed.
The twenty pairs total **310,309 bytes**, and every file is at most
25,354 bytes. All forty small certificate files are included under
`certificates/`. The original twenty traces totaled 214,430,938 bytes
and are unnecessary for replay of these published certificates.

A fresh final verifier reconstructed the entire parent again, checked
4,992 core-clause occurrences, and checked 992 distinct obligations
against the parent after removing each core's own audited tail clauses.
It replayed every extracted proof in 31.134 seconds including parent
regeneration and checking. Case 20 uses three RAT core lemmas; the
other nineteen extracted traces use no RAT core lemmas. These remain
general DRAT files with checker-supported deletion/RAT semantics.
The verifier does not replace DRAT checking with a hash or solver verdict.

Negative controls reject a flipped phase unit, a missing unit, a removed
mixed-block constraint, an incorrect variable header and an altered parent
clause. A core containing an unjustified new-auxiliary unit is rejected by
clause membership even when its recorded file hash is updated to match
the corruption. Normal and optimized-Python audit, whole-graph control
and literal-core outputs agree.

Twenty exclusions eliminate every normalized phase tuple outside the
singleton class (0,0,0), proving the stated unique-core theorem.
No extension of that remaining core is decided here.

## Trust boundary and pass boundary

The proof imports the prior internal-color and minority-matching results,
and through them the established R(4,5)=25 degree window and earlier
symmetry reductions. The minimum-ten theorem and the global order-five
exclusion have accepted independent reviews. Before publication,
[reviewer-1 accepted the 94-anchor minority-matching refinement](../ramsey_r55_order3_ten_cycle_anchor_sweep_review1),
conditional on the preceding four-versus-six internal-color theorem.
That review rebuilt the r=4 parent and reran all 94 new exclusions, but
did not rerun the five older internal-color exclusions. The latter remain
an explicit imported dependency without a recorded independent review.
This new phase result is internally checked, not independently peer
reviewed or formalized.

The unformalized mathematical reduction, exact Python semantics, C++
compiler/runtime, source correctness, hardware, SHA256 and external
DRAT checker remain boundaries. The new twenty exclusion certificates
are fully included, but earlier imported reductions retain their own
published reproduction requirements and omitted-large-trace boundaries.
No catalog completeness, numerical optimizer or solver status is trusted.

This completes one bounded phase milestone. The four anchor extensions
of H are the next symmetry frontier. The teammate's ten-edge-cell
obstruction and subsequent common-root squeeze belong to M=217 and were
inspected without duplicating that lane. The latter leaves one central
cell-size pattern and two W types, without excluding the whole profile.
The earlier whole-M=214 reproduction/decision checkpoint remains
in force. No eleven-cycle stratum, further extension sweep, or catalog
radius is started as part of this pass.
