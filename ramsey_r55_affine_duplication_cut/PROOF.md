# Complete affine-duplication cut exclusion

All ranks and vector coordinates are over F2. Red adjacency is1; blue is0.
A good graph contains neither a red nor a blue complete graph of orderfive.

**Declared family.** Partition43 vertices into A of size20 and B of size23.
Every nonzero type in F2^4 appears once on each side. Five distinct A types
are doubled. On B, precisely the eight types in an affine hyperplane
H_w={y:w dot y=1}, w nonzero, are doubled. Cross edges are dot products.
All443 internal edges are arbitrary. Include every vertex relabeling and
both choices of the color being factored. No full graph automorphism or
full-adjacency-rank condition is imposed.

**Theorem (computer-assisted).** This complete43-vertex family contains no
good graph. Its32 canonical global branches have necessary23-side CNFs
with physically checked DRAT refutations. The public replay regenerates
all32 proofs and checks their bytes. No saved status substitutes for a proof.

Both factors span dimensionfour, so the red cut rank isfour. There are no
zero rows or columns. The all-one vector belongs to neither factor column
space: a linear functional cannot equalone at all nonzero types, since its
values at x,z,x+z would contradict linearity. Appending independent all-one
columns to both factors gives rankfive for the complementary cross matrix.
Thus these cuts pass the prior necessary boundfour in both colors and the
zero-pair filter. Other cuts of these graphs are not constrained here.
The remaining rank-four families and good43 existence stay open.

## Complete type and pair-color coverage

A factor basis change sends x to Lx and y to (L^-1)^T y. It preserves all
cross colors. Choose Lw=e1=1, making the doubled B types precisely the odd
integers1..15. The stabilizer of e1 in GL(4,2) has14*12*8=1344 elements:
choose successive images of the other basis vectors outside the prior span.
It acts on the3003 five-subsets of nonzero A types. Complete enumeration
gives these16 representatives and orbit sizes:

    1 2 3 4 5     21       2 3 4 5 6     42
    1 2 3 4 6     84       2 3 4 5 8    168
    1 2 3 4 8    336       2 3 4 6 8    672
    1 2 4 6 8    224       2 3 4 8 12   112
    1 2 4 7 8    224       2 3 4 8 13   112
    1 2 4 8 14    56       2 3 4 8 14   224
    1 2 4 8 15    56       2 4 6 8 10   168
    2 4 6 8 11   336       2 4 7 8 11   168

`geometry.py` enumerates full-rank basis images. The independent auditor
instead computes orbit closure under e_j -> e_j+e_i, with j=2,3,4 and i!=j.
These transvections generate the stabilizer: GL(3,2) on the quotient and
the eight translations along e1. The orbit lists agree entry by entry and
cover every five-subset. All302400 type contacts under all1344 transformations
and their dual maps are checked directly. Identical type multiplicities
allow these maps to extend to physical vertex bijections. Internal edges
are transported arbitrarily; no graph automorphism is asserted.

Let c_x be the internal color of a doubled A pair. If x=w, the pair has16
common red contacts on B and is forced blue by R(3,5)<=14. For distinct
doubled types x,z with c_x=red and c_z=blue, consider the actual B vertices
in C(x,z)={y:x dot y=1,z dot y=0}. A red triangle there extends with the x
pair; a blue triangle extends with the z pair. Thus |C|<=5 by R(3,3)<=6.

The underlying nonzero types contributefour to C. The doubled hyperplane
contributeszero if w=z, four if w=x or w=x+z, andtwo if w is independent
of x,z. Hence C has sizefour only when the blue pair's type is w; all
other cases have sizesix or eight and are forbidden. All doubled types
other than w must consequently have the same color. Exactly two assignments
remain for each doubled set D:

    mode0: all five pair edges blue;
    mode1: all pair edges red except w, if present, stays blue.

The audit exhausts all96096 pair-color assignments for3003 sets, retaining
exactly6006, these two for each set. There are32 canonical branches. The
other438 internal bits are still arbitrary after fixing the five pair bits.

For completeness, R(3,3)<=6 is the usual three same-color contacts argument.
A triangle-free graph on nine vertices with no independentfour has degree
at mostthree, and degree at leastthree because each nonneighborhood is a
(3,3) graph of size at mostfive. Its degree sum27 is impossible. This proves
R(3,4)<=9. The standard recurrence with R(2,5)<=5 gives R(3,5)<=14. No small
graph catalog is used in the pair-color reduction.

For one fixed labeled20+23 cut the initial class has exactly

    15 * binom(15,5) * 20! * 23! / (2^13 * 20160)
    =17154780486757774613743095705600000000

cross matrices. Choose w and D and order both type multisets; their repeated
types contribute factors2^5 and2^8. Each physical rank-four matrix has
exactly20160 full-rank factor bases, whose action is free. Multiplying by
2^443 counts the complete physical graphs. No quotient by graph isomorphism
or sum over all cuts and colors is claimed.

## A necessary projection closes the entire global family

Fix D and a mode. B labels, in physical order, are
1,2,...,15,1,3,5,7,9,11,13,15. Its253 internal red-edge variables are the
first CNF variables. The formula imposes:

1. No monochromatic five-set in B.
2. No monochromatic four-set in B with a same-color contact to an A type.
   Such a four-set would extend with one A vertex.
3. No monochromatic triple in B with same-color contacts to a doubled A
   pair of that color. It would extend with both vertices of the pair.
4. Global red degrees18..24 at each B vertex. Cross contacts into A are
   known exactly from D, leaving explicit bounds on its22 internal contacts.

Condition4 imports [McKay and Radziszowski, R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
In a good43, a vertex has at most24 same-color contacts, so its opposite
degree is at least18. That computation is not rerun. The written reduction
and public formula use this premise even if some extracted proof cores
happen not to need the degree clauses.

The physical clauses have lengths10,6,3. Duplicate clauses are discarded.
Degree bounds are encoded by exact threshold gates

    s(i,j) <=> s(i-1,j) OR (edge_i AND s(i-1,j-1)),

with s(i,0)=true and s(i,j)=false for j>i. Four implications give the CNF
equivalence, simplified when an input is constant. Units assert the lower
threshold and negate the first threshold above the upper bound. The
auxiliaries are uniquely determined by the physical edge assignment.

`audit_formula.py` imports no generator. It builds dense coordinate/contact
tables, enumerates all physical subsets again, and compares the entire
physical clause set. Every actual auxiliary gate is tested on all assignments
to its inputs and output; every final degree unit and variable domain is
checked. No omitted or extra clause is permitted. All32 formulas pass in
ordinary and assertion-disabled Python with identical audit bytes.

Every good43 in the branch would give a satisfying assignment of its actual
B edges and their threshold prefixes. Each projected formula instead has a
checked DRAT refutation. Thus every completion of the A internal graph is
excluded in that branch. Complete orbit and pair-color coverage then excludes
the entire initial43-vertex family. A projected SAT witness would not have
closed a global branch; all32 projections here are UNSAT.

## Physical evidence and trust

The first run used pinned Debian amd64 CaDiCaL1.5.3-2 (`sc2021`) and
drat-trim0.0~git20240428.effa1dc-2. All32 solves finished UNSAT under the
fixed500000-conflict and600-second per-branch limits, and all32 physical
proof checks returned `s VERIFIED`. Solver time totaled159.111 seconds,
checker time121.681 seconds; the longest solve took31.284 seconds. The
188371117 proof bytes are retained privately. `expected_cases.json` records
all input and proof hashes and sizes as identities, not substitutes for
verification. `VALIDATION.json` records the fresh public replay.

Large CNFs and traces are omitted from GitHub under the standing large-file
boundary. The public replay regenerates every required proof in a fresh
external directory and checks all of them. No omitted private proof is an
input dependency. `verify.py` derives the full mathematical branch list,
reconstructs and independently audits all formulas, and actually executes
drat-trim on all physical proofs. It ignores saved solver statuses and old
checker logs. Adverse controls reject a fabricated family of32 UNSAT status
records, empty and truncated proofs, a stale success log, and omitted
physical or auxiliary clauses. No missing proof can close the family.

Trust consists of the written reductions, imported R(4,5)<=25, exact Python
semantics, standard DRAT soundness and the pinned C checker, hashing and
ordinary hardware. The solver's verdict alone is insufficient. There is
no proof-assistant formalization or claimed independent review of this
new package.

The motivating rank-width and zero-pair theorems were accepted together at
Discovery Net h3751, `bafkreihwelfcwkwvc5po2ho4u7n54rexswefzesxxzdtixx5u2qdzy7b34`,
review source `2b005912e60d5a5f79ce17be89872994fa527bce`. They are contextual,
not premises of this exclusion. The invalidated h3687 automorphism verifier,
fixed-neighborhood gluing, capped F27 solve and saved-parent repair are not
used. No historical priority, good43, or improved Ramsey bound is claimed.
Changing the affine-hyperplane or multiplicity hypotheses begins a different,
currently open family.
