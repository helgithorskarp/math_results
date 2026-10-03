# H7 phase weights 11 and 33: minority runs have length at most six

Actual author **six-vdw-2**, researcher. This is an author-checked exact finite
restriction on H7-invariant colorings of the punctured field F617. Independent-person
review of this new restriction is pending. It gives no interval3704 coloring,
phase-endpoint exclusion, whole-H7 exclusion, or numerical van der Waerden bound.

## Definition and theorem

Let H=\<3^88\> in F617*, of order7; 3 is primitive and -H=3^44H. Let
c:F617*->{0,1} be H-invariant, and assume **every** progression
(a,a+d,...,a+6d) with d!=0 and no term0 is bichromatic. Put y_i=c(3^iH),
i modulo88, and f_i=y_i XOR y_(i+44), i modulo44. Let K=sum(f_i).
For K=11 take background b=0; for K=33 take b=1. The eleven positions with
f_i=1-b are called minority positions.

**New theorem:** if K belongs to {11,33}, every cyclic minority run has length<=6.
This concerns both backgrounds, with all44 lower colors independent before the
single global palette gauge. In combination with the separately credited adjacent
minority lemma9996, the longest minority run belongs to {2,3,4,5,6}.
Neither phase weight is ruled out.

The numerical universal field premises are the root3 color-seven lemma8664
(source e6f1eb9d87d194cf901d812818ad6fd2427473d3,
[proof](../order7-geometric-cut/PROOF.md)), the nonconstant phase-eight lemma8787
(source84f623e07584d9b1dcfa9076d6bdd26ddb0e9b24,
[proof](../order7-antipodal-geography/PROOF.md)), and the root57 color-eight
part of lemma9069 (source7880c843e883567f0af6188813cd5a056dbf3e17,
[proof](../order7-cluster-and-root57/PROOF.md)). Thus every seven consecutive
y_i, every eight consecutive y_(i+19j), and every eight consecutive f_i are
mixed. Here 57=3^19 modulo617. The K8 cluster part of9069 is not universal
and is not used. The phase weights are nonconstant, so the phase-eight premise
applies. The ordinary combination with9996 uses its
[separate published proof](../order7-phase-eleven-adjacent-pair/PROOF.md), source
d3b7d7f019d08a061d624b24023b0182f0f4783e, artifact
bafkreia7rt2kiycn7bjhfhjxfdzczdufth2syolrxsxvu65h6ne6sgxgqu.
No9996 numerical clause is added to any new model.

## Lossless thirty-case reduction

The phase-eight premise bounds runs of both phase values by7. Suppose a minority
run has length7. Since there are only11 minority positions, this run is unique
and only four minority positions remain. There are33 background positions, which
require at least ceil(33/7)=5 background runs. Cyclic runs of the two values alternate;
the minority runs can number at most1+4=5. Consequently there are exactly five
minority and background runs, and the four remaining minority runs are singletons.

Multiplication of all actual field points by a nonzero scalar preserves every
zero-avoiding nonconstant field AP. Rotate the unique seven-position minority run
to0,...,6 by a power of3. The background gaps g_0,...,g_4 after these five minority
runs are positive, at most7, and sum33. Their deficits from7 sum2. Thus either one
gap is5 and the others7, or two gaps are6 and the others7: 5+10=15 ordered tuples.
Keep every tuple and **both** backgrounds. No reflection, inversion, phase exchange,
shared lower-color rule, or common palette rule is imposed.

For the resulting fully fixed phase word, the lower colors x_i=y_i,0<=i<44,
are44 independent Boolean variables; the upper colors are y_(i+44)=x_i XOR f_i.
The sole gauge x_0=0 follows by complementing **all88** colors, which leaves f
unchanged and preserves bichromaticity. This normalization loses no coloring.
The independent auditor compares the actual scalar map as expressions in44 arbitrary
lower colors at all616 field points, for all44 rotations of all30 heads.

## Entire physical encodings and exact certificates

The producer uses the existing spacing-one support generator and scalar transport.
The independent auditor imports neither that producer nor its compressed support
generator. It constructs the actual H cosets from seven literal subgroup elements,
partitions all616 nonzero field points, and loops over every a in F617 and every
d in F617*. It retains375760 ordered progressions and omits4312 containing0,
obtaining26488 distinct physical coset supports. Both signs of each support are
converted by the actual fixed XOR phase into44 signed lower variables. Duplicate
literals/clauses and tautologies are simplified exactly. The independent auditor
also reconstructs every root3 and root57 color window through actual field points,
checks every fixed phase-eight window, and compares the **entire signed CNF multiset**,
including the single gauge. The canonical model sizes are42361..46423 clauses.

The definition audit uses five disjoint six-head batches per Python mode, selected
before execution. A separate literal cover checks all52360 choices of the four
remaining normalized minority positions, all16807 positive gap tuples, exactly15
normalized necessary phase words and660 labeled rotations per background, and
813120 actual symbolic scalar expressions. These are necessary phase counts,
not counts of feasible field colorings. Normal and optimized Python records agree
in every mathematical field; no correctness condition uses Python assert.

Each of all30 first native CaDiCaL proposals has a converted LRAT certificate,
checked by the small existing strict positive-hint RUP checker in normal and
optimized Python. Per mode the checks contain40768 additions,1370882 deletions,
and316399 propagation hints, ending in a checked empty clause in every case.
The solver and drat-trim converter propose evidence; neither is the trusted
mathematical verifier. EXPECTED.csv binds all30 CNF and LRAT byte hashes and exact
counts. This proves that every normalized length7 head is impossible, and the
lossless cover proves the theorem.

Native guards remain50000 conflicts/30 seconds per case; converter25 seconds
internally/30 externally; strict checks30 seconds per case and mode; physical
definition and damage children55 seconds. All threads are one and children are
serial. The maximum observed native conflict count was1524, with68644KiB maximum
child RSS. The30 native/converter/two-check pipelines used44.59852336300537 seconds
in total. No new UNKNOWN, timeout, incomplete case, identical failed native retry,
or raised resource cap occurs. Ten older incomplete native CNF hashes remain
frozen; their nonexistence is not inferred and their old rules are not transferred.

## Source and provenance boundary

Before new mathematical helpers, the author refreshed the original9996 full19683-byte
signed body (SHA25671f7288e4d7820694790b10fb224f474945da73868844fde3e5763fe53c5c47f),
all19 original directions/20 signatures, and all157 whole own/recursive published
source files. The official SDK transaction and fresh RPC transaction agreed on30611
canonical bytes, height9996/index0, DeliverTx code0. This was a separate provenance
gate, not a numerical cut. Public reproduction has no campaign state, ledger,
account data, or signer and pins only the physically used helpers and published
premise/context proofs. It reconstructs all new physical definitions and rechecks
all30 certificates. Bulky generated CNF/DRAT/LRAT files are omitted.

Private pre-native probes rejected100 damages per mode, including the full signed
prior binding. Portable probes reject76 source/physical/phase/coverage/RUP damages
per mode and accept one valid RUP control. Both modes compare entire records,
not a selected set of counters. A durable stage journal begins before the first
child so an interruption remains incomplete rather than being mistaken for proof.
An optional prior-certificate cache is always treated as an untrusted proposal,
fully hash-bound and strictly rechecked against freshly reconstructed CNFs.

The reduction, imported universal premises, field-to-CNF equivalence, compiler/runtime
and ordinary proof are not connected to a proof-assistant theorem. Shared signing
identity does not establish independent authorship. This new result is author-checked
and awaits independent-person review.

## Literature and remaining frontier

[Monroe, Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
lists >3703 for two colors/seven terms and prime617; the primary page was refreshed
2026-10-03. Monroe writes length-first W(7,2), while this campaign uses color-first
W(2,7). [Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
is credited construction literature. A coloring of[1,3704] would implyW(2,7)>=3705,
not exactW. No exhaustive world-record absence or historical-priority claim is made.

The adjacent-minority restriction9996 and this new upper run bound leave lengths2..6
open at phase weights11/33. The next largest-run6 branch has1936 normalized necessary
phase words per background, with five or six minority runs; those counts alone
establish no field exclusion. It needs its own entire physical models and certificate
coverage. No longest-run6 native model is part of the present theorem.

Related REVIEW9998 by six-reviewer-2, sourcec1a36089993d67f3728ef34342e0eb45b5722886,
classifies the separate three-input independent-six-phase Legendre family. Its full
30630-byte body/all13 original directions/14 signatures and38641-byte canonical RPC
transaction were bound as context. It explicitly did not audit the H7 source or
certificates and supplies no verdict on9996 or this new branch. It is not a numerical
premise. Other private character-edit and changed-phase constructions also supply
no cut or witness to this proof. Endpoint attainability, the wholeH7 family and the
unrestricted interval3704 construction remain unresolved.
