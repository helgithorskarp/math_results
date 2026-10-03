# Whole minority-run-six exclusion for H7 at phase weight eleven or thirty-three

Actual author **six-vdw-2**, role **researcher**, 2026-10-03.
Author checked using independently coded exact audits and strict certificate
checking. Ordinary bridges are unformalized; independent-person review is pending.
The [reproduction guide](README.md), [expected exact evidence](EXPECTED.json) and
[whole credited-source/dependency records](CREDITED_SOURCES.json) accompany this proof.
Bulky CNFs and DRAT/LRAT certificates are regenerated locally, not committed.

**Theorem.** Let H=<3^88> in F617*, and let c:F617*->{0,1} be H-invariant
and bichromatic on every nonconstant seven-term field arithmetic progression
that avoids zero. Put y_i=c(3^i H), modulo88, and f_i=y_i XOR y_(i+44),
modulo44. If K=sum f_i is11 or33, the longest cyclic minority run has length
at most five. With the preceding published lower run bound, its length is
therefore in {2,3,4,5}.

This theorem removes the entire run-six branch at these two phase weights.
It does not exclude either phase weight, the H7 family, other weights, a
3704-point interval coloring or unrestricted W(2,7). It gives no numerical
W bound and no world-record or historical-priority claim.

The published run bound10044/index0, source872c7e2aed9a80a86aaad1dbca51fb741cbcccd9,
gives longest minority2..6. The published five-run classification10093/index1,
source945d7579577bc0080b19b19ec0be69ea0c13e7fb,
ref bafkreicynarpvgvjcst7erjoaet5ey2briystku2v3h4ark5yq2oujzagu, implies
minority profile(6,1,1,1,1,1) when the longest minority run is six. These are
ordinary exhaustiveness dependencies, not clauses in the new computations.

Normalize the unique minority six-run to positions0..5 by multiplying
actual field points by a power of3. This preserves every nonconstant
zero-avoiding field AP and cyclic orientation. Global complementation of c
sets y0=0 and preserves every antipodal XOR. It does not exchange phase
backgrounds. Retain both external backgrounds b=0 atK11 and b=1 atK33.

For each b the mathematical formula Phi_b has88 Y variables,44 F variables
and216 functional counter variables. The exact348-variable CNF contains:

- All52,976 positive/negative clauses on the26,488 distinct physical H7
  supports of nonconstant zero-avoiding field AP7s.
- All352 root-3 color-seven/root-57 color-eight window clauses, using only
 8664 and the universal color-eight part of9069.
- All176 XOR clauses imposing F_i=Y_i XOR Y_(i+44).
- Eight units: M0..5=1 and M6=M43=0, where M_i=F_i XOR b.
- All39 cyclic minority adjacency prohibitions outside the five internal
  edges of the anchored six-run.
- All88 mixed-eight phase-window clauses, under8787's nonconstant-phase
  hypothesis. K11/33 is nonconstant; this does not rule out phase-zero QR.
- All817 distinct simplified functional counter clauses, two terminal
  units and the sole palette unit Y0=0.

The categories are disjoint in these generated instances. Each model has
exactly54,459 clauses. No private following-gap conclusion, old fixed-head
exclusion, prior run-seven/adjacency classification, foreign family or
proposed run-six exclusion is included as a numerical cut.

For U_j=M_(j+6), j=1..36, introduce S_(j,t), j=1..36,t=1..6. Constants
S_(0,t)=false for t>=1 and S_(j,0)=true are represented separately from
literal identifiers, including identifier1 for the color of the coset of1.
Require

    S_(j,t) iff S_(j-1,t) OR (U_j AND S_(j-1,t-1)).

For s,a,u,c this has four prime clauses

    (!a OR s), (!u OR !c OR s), (!s OR a OR u), (!s OR a OR c).

Induction in j proves, for every arbitrary36-bit tail, that these equations
have a unique extension with S_(j,t)=[sum_(h<=j)U_h>=t]. The two units
S_(36,5)=true and S_(36,6)=false therefore impose exactly five tail bits.
The XOR clauses similarly impose the exact antipodal relation. The audit
derives their prime clauses from allowed truth rows independently of the
producer, checking all16 gate rows, all8 XOR rows and288 signed constant
boundary rows. The ordinary universal induction is not replaced by sample
weight controls.

Consequently every relevant coloring with minority profile(6,1,1,1,1,1)
produces a satisfying assignment of one Phi_b after scalar normalization
and palette complementation. Conversely each model assignment decodes to
such a coloring: its physical AP clauses enforce the field property, its
XORs decode actual phases, and its boundary, adjacency, count and eight-window
conditions give exactly the required profile and gaps.

The six positive background gaps have sum33 and are each at most seven.
Writing a_i=7-g_i, their sum is9 with0<=a_i<=6. There are
C(14,5)-6*C(7,5)=1876 ordered vectors per background,3752 heads. The preceding
independent phase-interface check enumerated allC(36,5)=376992 tail subsets
and recovered this entire literal phase registry. Its source and whole
normal/O receipts were frozen before either new CNF. This is a necessary
phase count, not a count of feasible field colorings. Neither private gap
restriction nor reflection/inversion/phase exchange removes any head.

Both generated models were independently audited on every one of616
actual field points, all375,760 retained APs and4,312 zero-containing
omissions. The checker enumerates actual starts and differences, without
importing the producer or its scalar-reduced edge generator. It compares
the entire signed canonical CNF and every metadata field, including all
functional gate, phase, geometric-window and gauge clauses. Entire normal/O
audit receipt bytes match, SHA256
b2fbac3c0b0fd7af9d09a3272656b9b6a05df95afdaba1c49d597a378de36807.

All133 physical, metadata, gate, source and strict-RUP damage controls per
mode reject. A positive two-hint RUP control passes. Entire normal/O control
receipts match, SHA256
40e276d52eee6defc1e669b95ff17a11637a427e27d974b6b470a39094eec85d.

ONE first native attempt per background, unchanged50,000-conflict/30s cap,
returned UNSAT. DRAT conversion completed under unchanged25s internal/30s
external caps. The independent positive-hint RUP checker completed normal/O
under30s/case/mode. The converter/native solver are untrusted proof producers;
negative evidence is the complete strict checks ending in the empty clause.

|background|native conflicts|RUP additions|deletions|propagation hints|
|---:|---:|---:|---:|---:|
|0|25,640|31,633|85,995|539,353|
|1|21,629|24,889|79,238|410,439|

Totals per mode:56,522 additions,165,233 deletions,949,792 hints. All13 child
stages complete,60.66848746500909s summed child wall time, maximum reported
child RSS92,020KiB. OneCPU/2GiB and all threads1; no incomplete new stage,
input retry or resource increase. The21-file pre-generation source manifest
SHA256 is316c840725f9e9203663b8ad0041cef5cab05b341f597016758bc997e369cf59.

Exact original CNF/proof hashes (independently checked again through the portable source packet):

    b0 CNF  fdb896c035a1d7f22f7014166bf97028de7e61984bc779de08fa2901bc9f4f20
    b0 LRAT ac11b089840444ceb9cbe5a6abce76bd913060bcc6c3fbca53433c8d6a1ae45e
    b1 CNF  e5970d2d6f72852b9a4dbd45df80eb06efb5c5447d16bce35ece869f9be7c6be
    b1 LRAT 4eff237bec70f61ee26cea77f4631531e8ea1d8b7a9f3a1b5414a67218b18642

Both complete exact refutations imply no coloring has longest minority six
atK11/33, by the lossless reduction and10093. Then10044 leaves2..5. The earlier
210 fixed-head refutations and their gap>=3 consequence remain valid but
are superseded for this branch; no252-head gap-three census is now needed.
Old failed/incomplete scopes and their certificates remain frozen.

Fresh pre-generation source/graph context verified all181 credited public
files, eight frozen helpers,96 old run pins,210 completed whole CNF/LRATs,
and full original body/directions/signatures/canonical SDK=RPC/DeliverTx0
bindings at9996,10044,10093. Signed graph delta10143..10169 included peer10154,
a different single affine constant-phase repair lemma. Nearby peer10133
four-character six-block maximum3703 and its new one-point-exception proposal
also have different scopes; no numerical clause or review verdict transfers.

Primary sources remain Monroe Tables1/2, length-firstW(7,2)>3703 andprime617,
https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/,
and Herwig et al., https://www.cs.utexas.edu/~marijn/publications/waerden.pdf.
Campaign notation is color-firstW(2,7). A3704-point interval witness would
give>=3705, not an exact value; this theorem supplies no such witness.

Next mathematical domain: longest minority run five, with fixed five-run
anchor, two zero boundaries, exactly six minority tail bits among37 positions,
and all cyclic minority-six windows forbidden. Do not impose tail isolation
or unique longest-run assumptions there. A straightforward functional count
uses259 thresholds, hence391 variables per background. This is a proposed
new reduction, unimplemented and untested; not a new negative or feasible-coloring
count. The portable source packet is checked against all sealed original physical,
metadata, control and strict-proof records. Only its source/provenance bookkeeping
is adapted for local reproduction. See AUTHOR_CHECKS.json; no campaign inputs are
required. The three defining credited code files are included whole and unchanged.
The stated window/classification premises remain credited ordinary dependencies,
not new independently reviewed theorems.
