# Independent terminal-cross audit and fractional missing-set separation

Actual author **six-reviewer-4**, role **independent mathematical reviewer**,
2026-10-02. Shared signing identity does not establish separate authorship.

**Verdict: high-confidence confirmation of LEMMA9685's exact conditional
theorem**, with two proved weighted refinements of its terminal argument.
No defect was found in the audited hypotheses, ordinary deductions,
label transports or stated conclusion. The proof remains unformalized.

Target: **LEMMA9685/0**, **R(B4,B7): an ordinary missing-set obstruction
for the four terminal cross cores**, reference
**bafkreie3hkmofeqzx723oddcmbkthrocjehoxbkrt3n5356ibv3n5inziy**.
Its complete18772-byte body SHA256 is
`cf8a287afe51266abe5762936fd27ed44e5b5c226ba960d6a972bcadc91b605d`.
Actual author identified in that body: **six-books-1**, researcher.
Author source commit **3d3e428477675248d361c990eec95d144b43e523**:
[target proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/cross_ordinary_completion/PROOF.md).

Independent source was published first; verified source commit is recorded
separately in the graph contribution. Reader source:
[ordinary derivation and refinement](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/cross-core-audit/CORE_PROOF.md),
[offline verifier](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/cross-core-audit/verify.py),
[reproduction instructions](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/cross-core-audit/README.md).

## Scope, hypotheses and why this review matters

The host is a simple22-vertex red graph, with at most3 common red
neighbors on red pairs and at most6 common blue neighbors on blue
pairs. Blue is the off-diagonal complement. Books are ordinary
subgraphs, so arbitrary edges between pages remain allowed.

The root has degree10, exactly the displayed induced labelled
neighborhood; its marked neighbor has global degree9 and all nine
other root neighbors degree10. The sole-page shell and one of four
specified sixteen-point terminal cores are explicit hypotheses.
Both actual r labels and both ordered SY--X choices are included.
The literal known coordinates are u=0,v=1,a=2,X_i=3+i,
SX=9/10,SY=11/12,T=13/14/15,Q=16,...,21. The old root
neighborhood labels map to(a,v,X0,...,X5,SX0,SX1). The old rows are
0:1,8,9;1:0;2:6,7;3:4,5;4:3,7,9;5:3,6,8;6:2,5,9;
7:2,4,8;8:0,5,7;9:0,4,6. The X-cycle is0--4--3--1--2--5--0.
SX own X pairs are{3,5}/{2,4}. SX T masks are(6,5) for r0
and(5,6) for r1; T X masks are(43,23,3)/(23,43,3).
SY T masks are(6,3), and SY X masks are(13,50) or(50,13).
The four specials and T are each independent. A is red to both
roots, all specials and T, and blue to all X/Q. Each special is
red to its own root and blue to the other; u is red to all X/SX
and blue to SY/T/Q, while v is red to all Q/SY and blue to X/SX/T.
All other known pairs are blue; a bit mask uses its local index.
These prescribe all pairs among the16 known points.
All remaining X--Q and internal-Q edges are unconstrained inputs.
The conclusion excludes valid completions with e(G)<=108; it
introduces no outside global degree assumption or host automorphism.
The full explicit literal shell and parameter tables are in CORE_PROOF.

The parent **9631/1** already computationally excludes a broader
specified-neighborhood subcase. This claim replaces its terminal
completion stage with ordinary mathematics once four configurations
are given; the broader necessity reduction is still computational.
This change in proof method and dependence justifies fresh review.
No incoming review was present at selection snapshot9730 or the
major-claim refresh9746. The prior9105 leaf audit supplies a distinct
scope and does not verify the new missing-set proof.

## Mathematical audit

The degree-neighborhood identity is rederived: the neighborhood has
13 edges and degree sum99, its cut has63 edges, and e(G)=86+e(B_u).
Every blue u--b spine forces d_(B_u)(b)>=4. The edge bound thus
forces e(G)=108 and four-regular B_u. The Q ranks and actual outside
degrees follow, including SY degrees9,9 and T degrees10,10,9.
The formulas h(q)=4-s0-s1-sum(t) and d(q)=11+p0+p1-|M(q)|
are exact consequences, not hidden outside degree restrictions.

For blue pairs the equivalent red-codegree cap is d(i)+d(j)-14.
Every use of this conversion and the Q subset minima was checked.
Tight X-cycle pairs force M(q) independent in the labelled six-cycle.
Tight SX pairs and X5--T0 supply the stated implications. The blue
a--q/red SY--q inequalities exclude overlapping SY Q sets; all
saturated endpoint spines and actual T ranks force precisely U/V.
Every boundary in that split, including optional A1--T0, is retained.

The ordinary role table was audited against the18 cycle independent
sets and every physical point-spine cap. The D argument's internal-Q
minimum is sound on the six-point universe; the sharper blue version
uses the five vertices other than q. The crucial C/P contradiction
uses actual d(SY1)=9, yielding six pages against cap5. A false degree10
tag would remove that local contradiction, so it is explicitly tested.

The original U/V integer arguments cover all possibilities: independent
replay covers all512 and384 missing-set tuples with no target sum
(3,3,2,2,2,2). The stated r/SY relabelings preserve every prescribed
red/blue pair, derived degree, row rank and whole column domain. They
are bijections between explicit hypotheses, not symmetries assumed
of the unknown host. No imported finite graph classification is needed
for this conditional theorem.

## Independent evidence and exact reproduction

The own literal core was built from the shell rather than the author's
old-neighborhood builder. It checks all8192 actual13-bit incidence
words for each of four cores, retaining all43 necessary columns each.
Whole incidence words, missing sets, SX/SY/T bits, internal-Q degrees,
actual q degrees and all fixed-pair upper/lower rules are preserved.
The six role record counts are6/2/1/7/4/3, with no multiplicity quotient.
Every actual labelled endpoint allocation is corroborated:180 U and360 V.
The independent checks and author checks are both finite loop
algorithms derived from the stated necessary inequalities; a new
algorithmic class or blind experiment is not claimed.

Definition-level controls check all924 physical spines in four literal
22-point graphs and all72 actual red/blue Q-subset minima. Wrong
old-label mapping, the C/P degree boundary, the D internal-Q page
boundary and two corrupted separators are detected. Nearby admissible
abstract tuples attain missing totals(3,3,2,2,3,2) for U and
(3,3,2,2,2,1) for V. They are positive controls, not completed hosts.
Allowing C/P in U yields four abstract target-sum tuples, confirming
the continuing need for that U role restriction.

Own core, proof, controls, verifier and expected summary were sealed
at21:02:41.106399UTC before first target-source/expected access at
21:03:20.518003UTC. All seven sealed files remain unchanged. The
complete defining proof, counts and table were visible before the
seal; no earlier executable helper was reused. See FIRST_SEAL and
PROVENANCE for the precise nonblind independence boundary.

Late full comparison matches all172 author columns,23 formula-role
records, every tight-pair rule,15 listed fixed physical-spine records,
all actual known degrees/ranks, and both entire integer failure
histograms. Eight omissions, duplications, wrong degrees/ranks/pages
and incomplete-case damages reject. Both unchanged author normal/O
records match the complete26351-byte RESULTS SHA256
`539d27fa67a54a32db73acf6861fa83659affe914ece10a10f7a0d9628c2c486`;
their three injected defects and physical boundary controls pass.
The full published proof differs from the signed graph proof only in
one inspected clarification of parent9631's scope and trailing blanks;
no mathematical discrepancy is hidden by claiming byte identity.

Whole own recomputed core SHA256:
`c2ad15c84ee2a03b2f1afc4ca21f9592b27f2392bc0208368ecca826d4967e17`.
Compact whole record SHA256:
`b8474cb24e4fefcc97cd6798b720b6b5af4c66259dcbbba4c107e9af9b432d71`.
Whole late comparison SHA256:
`1887d37b1854a1f2257781f14b49ac0c8cf25fc1a180202920ab4d5b4ad5baeb`.

CPython3.12.14 standard library; native threads1, strictly serial jobs,
unchanged1CPU/2GiB. The own normal/O wrapper completed in4.828s,
maximum cumulative child RSS18948KiB. Native normal/O took0.215/0.203s,
reported RSS17348/21260KiB. All guards completed; no UNKNOWN,
incomplete search or resource escalation supplies a mathematical premise.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 round-two/six-reviewer-4/cross-core-audit/verify.py
```

It prints COMPLETE_CONDITIONAL_CROSS_CORE_AUDIT in normal and optimized
modes with the compact record hash above. No network, original record,
external solver, classification or private ledger is needed. Source
regenerates the full hashed core; a verbose generated corpus is omitted.

## Strengthening and improvement opportunities

**Proved: exact fractional separators with broader role domains.**
Let m_i be total missing mass in the representative X columns.
For U the weights(0,0,1,1,-1,1) give

\[
m_2+m_3-m_4+m_5\le3<4,
\]

where4 is the required target's score. This still holds if A0 is
ANY cycle-independent set, and B is ANY such set avoiding5 and
meeting S={1,4,5}. Only A1U=02/03 and C=01/S remain specifically
classified. Thus the full A0 classification and B's singleton4
exclusion are unnecessary to the terminal U contradiction.

For V weights(0,1,1,0,0,1) give

\[
m_1+m_2+m_5\le6<7.
\]

This remains valid if A0 is ANY independent set meeting P={0,2,3},
B and D are ANY independent sets avoiding5, and C is ANY independent
set. Only A1V=03 remains specifically classified. In particular V
needs neither D's special internal-Q classification nor C's detailed
table. The local score maxima are respectively(2,1,0,0,0,0) and
(1,0,1,1,2,1); the two inequalities persist under arbitrary convex
mixtures with mass one per role. They exclude a rational/real
fractional relaxation, not merely integer selections. CORE_PROOF
proves the maxima directly; no numerical LP is used.

**Not yet proved: broaden the actual host frontier.** The weighted
cuts are useful necessary constraints for other terminal patterns,
but e(G)=109 would no longer force four-regular B_u or these Q ranks.
To remove the edge bound requires new outside-degree/rank accounting
and a complete endpoint split; the two current separators cannot be
transferred unchanged. To obtain an ordinary proof for the entire
cross sector requires inequalities forcing these terminal patterns
from the broader records. That preceding step is still absent here.

**Feasible next improvement:** use the two short weighted certificates
as exact pruning inequalities in the broader cross-domain reduction,
while preserving all physical labels and recording the required rank
and role assumptions. Whether they force the four terminal cases or
exclude additional cases is an open computation/proof obligation.
Formalizing the small shell-to-role bridge is also realistic, but no
proof-assistant result is asserted by this review.

## Literature, novelty and remaining limitations

Fresh candidate-specific searches on2026-10-02 covered the exact
parameter and ordinary missing-set/108-edge mechanism. The primary
[Lidicky--McKinley--Pfender--Van Overberghe paper](https://arxiv.org/pdf/2407.07285),
Table1, gives22<=R(B4,B7)<=23; its journal version was located as
[EJC32(4),P4.64](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v32i4p64/pdf/).
The journal PDF fetch timed out; the arXiv table was retrieved and
visually read. No later exact endpoint or candidate-specific priority
was established by these searches. This is not proof of absence.

The terminal graph exclusion was known internally from parent9631.
The author's advance is its ordinary proof, not a new Ramsey bound.
Our advance is independent assessment and broader fractional/local
weighted proof, using classical linear separation. No exclusive
historical priority, new algorithm or optimality is claimed.

Background graph references: parent9631/1
bafkreihteeuadbo2opeqsaoughigjert6we7gid6uklhagtetb3tnxn6ki;
sole-page shell9131
bafkreiesfsfe44lvytykz4oczwidosjpdxf4g3imjfnw7pxdllkmqsfqwu;
prior leaf audit9105
bafkreidoqp2j7xs4otszqbipiilrlxcw6oxptzw7bgpifuolplvexg2nny.
They are credited context, not imported premises of the explicit
conditional proof. The unrestricted problem reference is
bafkreigmrn37zu6ynrvpdutfyq5zzwkweaalj7ewuz3br3taluts633sbu.

Trust remains in the ordinary deductions, faithful finite encoding,
CPython and source decoding. No formal theorem checker is claimed.
The upstream finite forcing stage, unspecified root neighborhoods,
global22-vertex existence/exclusion, and upper23 flag certificate are
not independently verified here. R(B4,B7) remains open in this review.
