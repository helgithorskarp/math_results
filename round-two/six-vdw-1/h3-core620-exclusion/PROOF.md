# No H3-invariant antipodal regular cyclic620 core

Author: **six-vdw-1**, role: **researcher**. Status: exact computer-assisted
lemma with an ordinary, unformalized reduction. Another researcher's review
is not asserted.

Identify Z/620Z with F31 × Z/20Z by CRT. A regular point has nonzero field
coordinate. An antipodal regular core is a binary function c(r,s) on
F31* × Z/20Z with c(r,s+10)=1-c(r,s). Put H3={1,5,25} in F31*.
H3 invariance means c(hr,s)=c(r,s) for every h in H3. AP7-free means that,
for every a in Z/620Z and every nonzero step d in Z/620Z, the seven terms
a+j d, 0<=j<=6, are not monochromatic whenever all terms are regular.
Modular repetitions are included.

**Lemma. No AP7-free H3-invariant antipodal regular core exists.**

This excludes a specified construction family. It makes no claim that arbitrary
3704-point colorings must satisfy these hypotheses, and changes no numerical
van der Waerden bound.

## Imported premise and absolute inputs

The previously published [orbit16 lemma](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-vdw-1/h3-orbit16-exclusion620/PROOF.md)
at ACTUAL9576/0, CID
`bafkreig4gyqfrxg7brwukbp7jbrfbj2bkzv6sctzy2ba6lgbt55qkbykme`,
source commit `99b8f2cf222afd483784a41cdfbb94221158acae`, proves that every
such core avoids the entire160-member phase-affine orbit of mask16 on every
field coset. This is a genuine premise of the present proof. Its source
inventory SHA256 is
`100c117c166bd00e1d78b1815744c6c334289cf50542a17b25ef82186c100381`.
`support.py` verifies that inventory and every listed source file before
loading its generic generator or separately written physical auditor. The
prior certificate is not silently replaced by a solver's status. Its
independent exact reproduction command is in the linked prior README.

There are ten H3 cosets, in the increasing least-residue order given by
`cover.py`. The 100 ORIGINAL Boolean inputs B(g,j), 0<=g<10 and 0<=j<10,
are absolute lower-phase colors. A regular CRT point (r,s) has color
B(g,s mod10) XOR floor(s/10), where r belongs to coset g. Each input describes
three positive and three negative physical positions. Other than a specified
first row, all rows remain arbitrary antipodal words. No palette, relative
base mask, phase-power transport law, affine-row membership, extra anchor,
weight restriction or pole assignment is introduced.

If m is a forbidden mask, its exact exclusion at row g is the clause
OR over j of [B(g,j) != bit_j(m)]. Its signed literal is -(10g+j+1) for
bit1, and +(10g+j+1) for bit0. There are1600 such width10 clauses.
The separate auditor checks all1,638,400 original row-input/cut truth cases
for EACH of the six formulas, rather than checking only promised local rows.

## Complete six-case reduction

The antipodal phase word defined by a ten-bit mask m is
b_m(s)=bit_(s mod10)(m) XOR floor(s/10). Regular progressions with fixed
nonzero field coordinate imply that each row avoids every cyclic seven-term
phase progression. The full1024-mask,380-progression local census yields580
admissible masks. Its seven phase-affine orbits under s -> v s+z, with v a
unit modulo20, have representatives and sizes:

| Representative | 8 | 10 | 12 | 16 | 20 | 34 | 72 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Size |160|40|80|160|40|80|20|

This classification is prior work, independently rebuilt here, not a new
local-census claim. The imported orbit16 exclusion leaves420 first-row masks.
`cover.py` checks EVERY one of them has a phase normalizer to one of
**8,10,12,20,34,72**, and that the chosen normalizer preserves ALL160 imported
forbidden masks. It performs67,200 such mask-transport checks.

This is a whole-core transport, not an assertion of additional color
invariance. For a chosen (v,z), take CRT A=(1,v) and B=(0,z). Then
T(x)=Ax+B is a bijection of Z/620Z since A is a unit. It retains each field
coordinate and the pole set, sends (r,s) to (r,vs+z), and induces a signed
permutation of all100 original inputs. All160 maps,100-input signed
permutations and96,000 actual regular-point identities are checked. Since
v is odd, antipodality is retained; retaining the field coordinate preserves
H3 invariance. A nonzero progression step remains nonzero after multiplication
by A, so AP7-freeness, including modular repetitions, is preserved. Orbit16
is closed under these phase-affine actions at every row.

Consequently, an AP7-free H3 core would yield a core satisfying one of the
six formulas: the complete original AP constraints, all1600 proved row cuts,
and TEN absolute first-row units for the corresponding representative.
Each formula has100 variables and90 raw free inputs before AP/cut constraints.
The formulas do not restrict the other nine rows to affine orbits beyond the
proved orbit16 ban.

## Six exact refutations

For EACH formula, the physical auditor reconstructs ALL383,780 ordered
nonconstant cyclic progression pairs:299,400 regular pairs and84,380
pole-touching pairs. It checks the full physical point table,614,400 original
row-point truth cases,600 antipodal and1800 subgroup identities, and every
ordered clause and the whole DIMACS bytes. There are36,600 regular antipodal
tautologies and43,240 distinct AP clauses. Ten first-row units plus1600 proved
row cuts give44,850 clauses. Whole audit objects agree normally and under
Python-O for every case.

| First row | Native conflicts | RUP additions | Positive propagation hints |
|---|---:|---:|---:|
|8|15499|13660|169745|
|10|16815|15094|179336|
|12|19450|18092|223971|
|20|13248|13349|166308|
|34|15440|13746|173253|
|72|18636|16963|210659|

The complete canonical model/CNF/native-trace/LRAT hashes and all deleted-clause
counts are in `EXPECTED.json`. Each native trace was captured after exit and
converted to positive-hint LRAT. The credited strict RUP kernel checks every
addition by negating its literals and propagating the stated LIVE original or
previously derived clauses to contradiction. IDs are fresh/increasing,
out-of-domain literals and nonpositive/RAT hints are rejected, deletions must
refer to live clauses, and a checked empty clause is required. Each exact
refutation passes normally and under Python-O with identical full proof
records. Native/converter acceptance is not the proof.

All six formulas are therefore unsatisfiable. The complete preserving
six-case cover and imported orbit16 lemma prove the displayed lemma.
The prior orbit16 theorem concerns the full H3 family; it cannot be imported
as a universal cut after H3 is relaxed.

## Construction implication and limits

A coloring of zero-based[0,3703] whose nonpole values follow such a period620
antipodal H3 core would imply AP7-freeness of that regular core. Indeed any
monochromatic regular cyclic progression can be reversed to have step
1<=d<=310. Choose its start in[0,619] and lift it to an integer progression;
its last term is at most619+6*310=2479. All terms remain nonpoles because620
is divisible by31. Such a coloring would contain a forbidden integer AP.
Thus this family cannot be repaired merely by assigning its120 DISTINCT
finite poles0,31,...,3689. A useful next construction must relax H3 invariance
or change the chosen period/phase framework.

No arbitrary regular-core exclusion, exact W(2,7), W(2,7)>=3705 certificate,
finite pole witness or asymmetric w(3,k) claim follows. A future3704-point
witness still needs an independent exact check of all1,141,450 nonconstant
integer seven-term progressions.

Primary context: Monroe's [Table1 and paper](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give the two-color seven-term seed>3703, with prime617 in Table2; see the
author's [source repository](https://github.com/hmonroe/vdw). Monroe uses
length-first W(7,2), equal to color-first W(2,7) here. Live sources were checked
2026-10-02; this is no comprehensive current-record or historical-priority claim.

The ordinary CRT, local-census necessity, normalization and interval-lift
bridges are unformalized. Generator and physical auditor are distinct
algorithms by the same author, not independent peer review. Imported9576,
Python/execution, exact integer arithmetic and the credited strict RUP kernel
are explicit trust boundaries. Old UNKNOWN runs, restricted phase-power
results and complementary teammates' H7/XOR results are not new proof premises.
