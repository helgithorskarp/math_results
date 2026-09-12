# Exact scope and conditional join

This document establishes an equisatisfiable normalization of one complete
122-task family. It is not a refutation of that family. The terminal run status
is recorded separately; input auditing alone retires no original ID.

## The literal original family

Let `F_c` be the full `triangles=False` formula produced by
`ramsey_r55_maximal_block_order/ordered.py` for `bo1-q7-r5-c{c:06d}`.
The index set `I` is exactly `retained_core_indices` in
`ramsey_r55_q7r5_tail_decisions/TASKS.json`, whose SHA256 is
`3d6e4497ea449f3831a66e1e2832976ca35ec61128c4cc36468e7a7ee5558544`.
It contains 122 distinct indices. Every literal ID and its complete original
DIMACS hash is listed in `ORIGINAL_INPUTS.json`.

The physical graph has vertices 0 through 42. Blocks 0 through 4 are the
prescribed red K4s on consecutive four-sets beginning at 0,4,8,12,16.
Blocks 5 and 6 are the blue K4s beginning at 20 and 24. The literal core
on vertices 28 through 42 is record `c` in the pinned 640-record R(4,4;15)
catalogue. All red and blue K5s are forbidden, as are all red K4s in the
23-vertex residual 20 through 42.

The original root-column inequalities order the columns in each of the six
matrices between block 0 and another block. The original whole-block
inequalities compare the root matrices of block pairs (1,2),(2,3),(3,4),(5,6).
These inequalities involve only edges between prescribed blocks, never an
edge joining block 0 to the core. No further isomorphism reduction is assumed.

## Finite descent inside each literal original task

Put `E = {{0,c}:28 <= c <= 42}`. Suppose `G` satisfies `F_c` physically,
with its original ordering auxiliary variables. Process the fifteen edges
of `E` in increasing order of their core endpoint. If the current edge is
blue, leave it blue. If it is red, change it to blue exactly when that change
does not create a blue K5. Call the resulting graph `G*`.

Every intermediate graph still satisfies the same original task:

1. Deleting red edges cannot create a red K5.
2. The deletion is expressly allowed only when it preserves blue-K5-freeness.
3. The literal core, all prescribed block internals, and all block-to-block
   edges are fixed throughout. In particular, the root-column constraints,
   whole-block comparators, and their original auxiliary values are unchanged.
4. The red-exhausted residual excludes vertex 0, so none of its edges changes.

Now take an edge `e={0,c}` which remains red. When it was processed, deleting
it would have created a blue K5. This new K5 must contain `e`, since all other
edges were unchanged by that deletion. Its other three vertices form a set
`S` such that all nine edges of `K5[{0,c} union S]` other than `e` are blue.
Any later change deletes another red edge and preserves these nine blue
edges. Therefore this same witness still works in `G*`.

This proves the one-pass normalization theorem: every model of each literal
`F_c` has a model of that *same* `F_c` in which every remaining red edge of
`E` has a physical blue K5-minus-that-edge witness. There are at most fifteen
deletions. This is an existence-preserving map, not an assertion that every
old model satisfies criticality. No cross-core or cross-stratum redirect is
used. In particular, the witness clauses are not claimed to be implicates
of a single original formula.

The one-pass output is minimal under further red deletion on E. It need not
minimize the red-edge count among arbitrary recolorings of E; that stronger
optimization claim is neither used nor encoded.

## The whole-family formula H

Variable 1 is true. Variables 2 through 862 are the physical unfixed edges,
in increasing lexicographic pair order, with only the 42 block-internal
edges omitted. Core edges are exactly variables 758 through 862. Variables
863 through 922 are the four original 15-variable equality-prefix chains.

The physical base contains all original constraints with the core still
unfixed. It has 1,543,935 clauses. For each `c in I` introduce a selector
`s_c`, require the disjunction of all 122 selectors, and require
`s_c -> (core equals the literal catalogue word c)` by 105 binary clauses.
An at-most-one selector constraint is unnecessary: the physical core words
are distinct. The base plus selectors expresses precisely the disjunction
of the original family, up to the explicitly described auxiliary variables.

For each selected edge `e={0,c}` and each three-set `S` disjoint from `e`,
omit `S` only when one of the other nine K5 edges is a prescribed red block
edge. Otherwise introduce `z_{e,S}` and the implications

`z_{e,S} -> (each unfixed edge of K5[e union S] other than e is blue)`.

Prescribed blue edges need no implication. Finally impose

`edge e is blue OR (OR over all z_{e,S})`.

These implications are one-way on purpose. A normalized physical graph
extends to a satisfying assignment by selecting one actual witness for
each remaining red edge and setting other witness variables false. Conversely,
a satisfying assignment with `e` red has a true witness variable, whose
implications certify all nine required blue edges physically. Reverse AND
definitions would not be needed for either direction.

There are 7,604 allowed three-sets per selected edge. The three root-mates
of vertex 0 are forbidden. From each of the other four red blocks one can
choose at most one vertex, while the other 22 available vertices have no
prescribed red pair. Thus the number is

`[x^3] (1+4x)^4 (1+x)^22 = 7604`.

There are 12 fixed blue pairs in the two blue blocks; after choosing such
a pair there are 36 allowed third vertices. Hence the number of nonconstant
witness implications per selected edge is `9*7604 - 12*36 = 68004`.
The entire witness layer has 114,060 variables, 1,020,060 binary implications,
and fifteen disjunction clauses. H has 115,104 variables and 2,576,821 clauses.

## Exact original input projection

The first 1,543,935 clauses of H are the common physical base. Substitute a
literal catalogue core `c`, remove every satisfied clause, and remove each
false core literal from surviving clauses. The physical non-core variables
2 through 757 remain unchanged. Shift each prefix auxiliary 863 through
922 down by 105, to become the original auxiliaries 758 through 817.

This produces exactly the ordered original stream, including its order:
the true constant, root inequalities, lexicographic five-sets in red-then-blue
order, residual four-sets, and the four comparator streams. A five- or
four-set clause is dropped under substitution exactly when the original
producer sees a fixed edge of the opposite color. The comparator formulas
coincide term by term after the auxiliary shift. Thus specialization is an
identity of literal streams, not a claimed inference from matching counts.

`project.cpp` emits the specialized DIMACS bytes, `parent_inputs.py` hashes
them and verifies all catalogue core bits against the pinned original
producer. Each original count is also checked against `ordered.build`.
The manifest records all 122 full input identities. The core-4 identity
additionally agrees with the independently retained original physical input.

## Admissible conclusions

We have the exact equivalence

`H is satisfiable  <=>  some F_c, c in I, is satisfiable`.

The right-to-left direction is finite descent followed by selector and
witness assignment. The left-to-right direction decodes the core selector,
forgets the new witness variables, and uses the original input projection.

A *checked complete refutation of H* would therefore exclude every one of
the 122 IDs, by this same-ID normalization join. It would not directly exclude
any q7,r6, q7,r7, q8, q9, or q10 task. Together with the 518 previously checked
q7,r5 exclusions, it would close the entire q7,r5 stratum. A solver UNKNOWN,
an unfinished trace, a closed internal search branch, or an input audit
provides no such exclusion.

A satisfying assignment must instead be decoded into all 903 physical edges
and checked against every monochromatic five-set. The selected original
parent must also be accepted by the pinned original checker. Only such a
checked physical graph would count as a good43.

## Trust boundary

The finite-descent and literal-stream arguments above are ordinary mathematical
proofs, not proof-assistant formalizations or independently peer-reviewed
results. `audit.py` independently reconstructs the input from physical sets
without importing the producer or using a solver. It checks each forbidden
five-set exactly once, every residual four-set, comparator truth tables,
literal selector words, and the complete physical witness collection.
This separates input validation from solver correctness, but does not itself
establish UNSAT. The external R(4,4;15) catalogue and original carrier
completeness remain the inherited catalogue and carrier trust boundaries.

R1's within-task monotone-chain package supplies related context. No chain
restriction, chain-count multiplier, conditional RUP clause, or complete-cover
redirect from that package is inserted into H. This is a bounded attempt to
consume the retained original family, not a novelty claim for monotone
normalization or SAT gluing in general.
