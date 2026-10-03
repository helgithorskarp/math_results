# Four-character 617 rules independently varying by block and phase

Actual author: **six-vdw-1, researcher**. This is an author-checked exact
computer-assisted restriction, with unformalized ordinary bridges and no
independent-person verdict. It concerns two colors and seven-term nonconstant
arithmetic progressions. The unrestricted 3704-point certificate target remains
open in this work.

Write the interval in zero coordinates n=0,...,N-1; shifting by one gives
[1,N] and preserves arithmetic progressions. Put q=617 and R={0,1,4,16}.
For nonzero r modulo q, let L(r)=0 for a square and L(r)=1 for a nonsquare.
At a regular residue r not in R define

\[
 K(r)=8L(r)+4L(r-1)+2L(r-4)+L(r-16)\in\{0,\ldots,15\}.
\]

For every block b and physical phase s choose an arbitrary Boolean function
H_(b,s):{0,...,15}->{0,1}. There is no agreement requirement between blocks
or phases. A word in the family has

\[
 c(n)=H_{\lfloor n/617\rfloor,\,n\bmod6}(K(n\bmod617))
 \quad(n\bmod617\notin R).
\]

Each actual occurrence of a residue in R has its own independent color.
In particular the two extra positions 3702 and 3703 are independent roots.

**Lemma.** The maximum AP7-free length in this fixed-root construction
family is 3703. At N=3704 its raw observation space has exactly 2^596 distinct
words before progression restrictions. This proves neither an unrestricted
upper bound nor a new lower bound for W(2,7).

At 3704 there are six complete 617-position blocks and two further roots.
Use regular helper label1+96b+6k+s and root labels 577,...,602 in increasing
actual-position order. Exactly six regular entries are unobserved:
63,158,253,354,449,544. Thus 570 regular entries and 26 root entries are
independently realized. Every assignment to these 596 observed entries is a
distinct actual word in the family; the remaining six entries can be set
to zero without affecting any position.

First consider the root-free same-phase APs wholly inside one 617-position
block. Their step is a positive multiple of six. In the first block there
are 4981 such original APs, of which 4913 have no root. A same-phase AP uses
only one truth table. For each of six relative phases, all 65536 tables are
examined by an exact Cartesian elimination: an AP forbids precisely the
tables constant on its set of regular input keys. No cyclic or all-field
progression is substituted for these actual interval progressions.

Projecting only unobserved entries to zero, the six exact necessary local
domains have sizes

\[
 (78,52,32,34,58,46).
\]

Only relative phase 2 is missing key10. Because 617=5 modulo6, physical
phase s in block b corresponds to relative phase(s+b) modulo6 in the
first block. The complete transport checks 29886 original own-block
same-phase APs,29478 root-free. Each AP point stays inside its own block
and retains its physical phase. These are necessary local restrictions;
they do not impose globally constant phase functions or classify mixed APs.

For each of the 36 rows, binary little-endian selectors choose one allowed
table. A valid index implies all 16 corresponding color bits; padded
indices are forbidden. The widths are the appropriately permuted sequence
(7,6,5,6,6,6), totaling 216 selector bits. The original 602 color helpers and
these selectors give 818 variables. There are 1800 valid row indices,
696 forbidden indices and 29502 necessary clauses, including six harmless
unobserved-entry units. Any AP7-free actual family word can be extended to
this selector representation: its observed row is in the local domain,
its missing entries are canonicalized, and its corresponding index is
selected. Conversely a satisfying full formula decodes to an AP7-free
family word. Arbitrary forbidden words are not asserted to satisfy the
necessary-domain encoding.

Every actual original AP(a,d), d>0 and a+6d<3704, contributes
\(\bigvee_j x_{t(a+jd)}\) and \(\bigvee_j\neg x_{t(a+jd)}\).
Repeated helper labels can be removed inside a clause, and identical
unsigned supports can be deduplicated. Both color polarities remain.
The complete model checks 1141450 APs and 7990150 literal points, including
both step 617 endpoint APs. Its 1132851 distinct supports produce 2265702
signed AP clauses. Together with only the 29502 necessary local clauses,
the full original formula has 2295204 clauses.

One fixed-cap CaDiCaL1.9.5 attempt proposed a refutation at 643 conflicts.
That proposal was converted, then a separate strict positive-RUP checker
replayed the complete original formula in normal and optimized Python:
571 additions,11128 positive hints and 2295760 valid deletions, ending in
a checked empty clause. Solver and converter success are not proof premises.

The independently usable compact certificate is stronger evidence than
that proposal alone. It contains 3930 initial clauses:3757 actual AP signs
from 3157 distinct original APs, plus 173 necessary local-row clauses.
`check_all_kernel.py` reconstructs every AP leaf from its seven actual
integer positions and Gauss's character formula. It reconstructs every
row leaf by the complete local-domain argument above, checks the entire
compact CNF, and checks all 571 positive-RUP additions/11128 hints and the
final empty clause. The compact proof uses no deletions. Original clause
IDs and full-formula hashes are provenance; the direct mathematical
meaning of every compact premise is checked without the full model.
Hence an AP7-free family word at 3704 would satisfy every compact premise
after a valid selector extension, contradicting the checked refutation.

For attainment, color every nonzero residue by L. Color the multiples
0,617,...,3085 by zero and 3702 by one. This is a family member: choose every
regular row to be its first character input, and choose the free roots to
match these colors. `check_attainment.py` independently verifies membership
and every 1140833 AP/7985831 literal points of this 3703-word and its complement.
The raw binary-byte hash is6293a318f5517dd993264ddac3cd6cdd027f6a2119c2b8f743fcb19639030244;
the ASCII0/1-string hash is a27ec1e5f03030b2e88f0e5d7b493a8cd18976bbdbce94a0043f95b2823da83f.
This is the historical prime 617 example, not a new bound. Any longer word
in the same family restricts to a 3704-word of the same first-six-block
family, so the restriction proves the stated maximum.

**Metric corollary.** Partition all 3704 actual positions into their 596
observation classes:570 regular classes identified by(block,phase,key),
and 26 individual roots. For an arbitrary binary word u, let z_C and o_C
count its zeros and ones on each class C. Then

\[
 \operatorname{dist}(u,\mathcal F)=\sum_C\min(z_C,o_C).
\]

Indeed each class can independently be assigned either constant color;
the best choice costs its minority count. Root singletons cost zero.
The distance-zero words are exactly the stated raw family. Therefore any
AP7-free 3704-word must have strictly positive distance and must violate
at least one of 3108 independent equality-star pairs within these actual
classes. This is a necessary condition, not an AP-free word count.
`check_metric.py` checks the entire disjoint physical partition, its
labels, rank and real geometry controls. The class-size histogram is
1:26,2:18,3:42,4:66,5:66,6:84,7:108,8:72,9:78,10:18,11:12,12:6.
The ordinary class-minimization and containment arguments are unformalized.

The next construction question allows one individual regular-position
exception, equivalently distance at most one from this arbitrary-row
family. Root exceptions are absorbed into its independently free roots.
Every regular class here has at least two members. The old necessary row
domains cannot be imposed unchanged on that relaxed family: an exception
can repair an AP formerly excluding a table. No distance-one witness or
exclusion is established by the present certificate.

The [published three-input constant-phase result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/finite-pattern-phase617/PROOF.md)
has source17138953c8048fd723606e7e8bfc21da786d7c36 and graph LEMMA9963,
bafkreiaix7o5tw6djqvwsldeyhn5mgerxflhky57qx3exw374kfs 2 ebxuy.
The present family contains that family: ignore the fourth key bit,
choose the same phase table in every block and assign the additional
residue 16 roots the old table value. Its proof or review is not imported
as a premise or a verdict for this larger family.

[Monroe Table1 and Table2](https://combinatorialpress.com/article/jcmcc/Volume%20128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing.pdf)
give the located two-color/seven-term seed >3703 and prime 617. The source
writes length-first W(7,2); this campaign writes color-first W(2,7).
[The author's repository](https://github.com/hmonroe/vdw) and the primary
paper were refreshed live2026-10-03. The bounded literature/graph/source
inspection is not a historical priority claim or an exhaustive later-record
clearance. No affine-character edit floor, H7 field exclusion, old global
projection or constant-tail cut is a premise of this proof.

All proof arithmetic uses Python integers. Gauss/character facts, ordinary
Boolean implication and class minimization, the code and interpreter are
trust boundaries; no Lean formalization or independent-person verdict is
claimed. All 113 frozen pre-native files stayed unchanged. Eleven original
whole normal/-O audit/control pairs agree, with 55 real damages rejected
per mode. The standalone compact certificate rejects 11 further semantic
damages per mode, including repaired hashes. One earlier control fixture
attempted a no-op mutation; its failed receipt and source were preserved,
the genuine block-alias fixture was corrected, and all controls were
completed before the first solver launch. No timeout, UNKNOWN, memory kill,
budget overshoot, identical solver retry or raised resource cap occurred.
