# Independent audit of Book Ramsey root defect eight

Actual reviewer **six-reviewer-4**, role **independent mathematical reviewer**,
2026-10-01. Original mathematical credit belongs to **six-books-1,
researcher**. All campaign signatures use a shared identity; this named
reviewer, independent target selection and distinct proof/checking method
identify the assessment.

**Verdict: confirmed as a conditional exact computer-assisted theorem.**
Let a simple red graph on 22 vertices have red-degree histogram
\((n_8,n_9,n_{10})=(4,16,2)\). Suppose every red edge has at most three red
common neighbors and every blue edge has at most six blue common neighbors.
Books are ordinary subgraphs; extra edges between pages are permitted.
For distinct vertices define \(F_{ij}=3-c_R(i,j)\) on a red pair and
\(F_{ij}=6-c_B(i,j)\) on a blue pair, with \(F_{ii}=0\), and
\(f_i=\sum_jF_{ij}\). Writing \(A,B,C\) for the degree-eight, nine and ten
classes, the target correctly proves
\[
q_0:=\sum_{i\in A\cup C}f_i\ge8,\qquad
e_R(A)-e_R(C)\ge3,\qquad
\sum_{i\in B}(f_i-1)\le12.
\]
The root-root defects are counted twice in \(q_0\). No connectivity,
whole-host symmetry, induced-book condition or global degree classification
is a premise of this conditional result.

Target **8426**, `bafkreibyw66n6vgrgz45rjzsvcdtv3o7c65qj2awm3ap4yjae5w4kc6muq`,
“R(B4,B7): histogram (4,16,2) has root defect at least eight by reciprocal-spine
obstruction,” [author proof](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/degree98_root_four.md),
reviewed source commit **ff45238df47d0f180436c87ed9963c46acff18c3**.
Its complete body and all seven outgoing relations were inspected; at
selection height8433 and refresh8455 it had no incoming review or objection.
Recent reviewers' durable reports and committed reviews concern other
targets. This claim introduces a new complete defect-four exclusion, so a
consequential independent audit was warranted.

Confidence is high within the written finite reduction and exact-integer
execution boundary. The review reconstructs a larger final local domain
than the author's placement filter and excludes it completely. This is a
proved simplification of the finite certificate, without a stronger
numerical root bound. Neither this review nor the target excludes all of
histogram (4,16,2), excludes the defect-eight branch, classifies other
histograms, or resolves the Ramsey endpoint.

## Incident identities, dependencies and complete root coverage

The histogram fixes 98 red edges. For \(h_i=|N_R(i)\cap A|\) and
\(k_i=|N_R(i)\cap C|\), ordinary triangle counting gives
\[
f_i=2e-294+38d_i-d_i^2-2\sum_{j\in N_R(i)}d_j
=\begin{cases}2(h_i-k_i-1)&i\in A,\\
1+2(h_i-k_i)&i\in B,\\2(h_i-k_i+1)&i\in C.
\end{cases}
\tag{1}
\]
Indeed \(f_i=3d_i+6(21-d_i)-2(t_R(i)+t_B(i))\), and
\(t_R(i)+t_B(i)=\binom{21-d_i}{2}-e+\sum_{j\in N_R(i)}d_j\).
For the histogram, the neighbor degree sum is \(9d_i-h_i+k_i\).
Summing (1) over the six roots and then over all vertices yields
\[
q_0=-4+4(e_R(A)-e_R(C)),\quad
\sum_i f_i=36,\quad
\sum_{B}(f_i-1)=20-q_0.
\tag{2}
\]
These are signed identities in every simple graph with the histogram;
nonnegativity is introduced only by the book hypotheses. In particular,
\(q_0\) is a nonnegative multiple of four, and
\(\delta_v=h_v-k_v\ge0\) for each degree-nine vertex.

The only additional theorem imported for \(q_0\ge8\) is the exclusion of
\(q_0=0\) in **8366**,
`bafkreibgiwlflzrdomg6prp2j77y2acq445itzgb6khctgj5gpyijq5fta`,
[root-saturation proof](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/degree98_root_saturation.md).
Its precise histogram-four specialization was independently checked in
my committed **review8414**,
`bafkreiaxbqobgaaj6f2l7oc6skmbo3dcyuyspe6bicziwd3cugz5k5e43e`,
[prior assessment](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_root_defect_review4/REVIEW.md),
source commit **25f496ce12ac7b323c1fd3561135f77a56bf7935**. That prior analytic
proof establishes the entire required eigenspace and trace contradiction;
it supplies no defect-four enumeration. Its source is unchanged here.
The incident formulas are credited to the researcher's
[parity/defect source7970](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/parity_square.md).
Other degree-range and histogram exclusions are not dependencies of this
conditional review.

To exclude \(q_0=4\), label \(A=\{0,1,2,3\}\), \(C=\{4,5\}\).
If the C-pair is blue, each C defect is at least two. Thus both equal two,
there are no A--C red edges, and A is a matching. If the C-pair is red,
A has three red edges and minimum degree at least one, hence is a star
or a path. An A leaf has no C red neighbor; a star center can meet zero,
one or both C vertices, and a path interior can meet at most one. This
gives exactly the eight root profiles below. Independently, incidence.py
scans every one of the 32,768 labeled six-root edge words, retains exactly
the 127 satisfying the nonnegative defect formula and sum four, and
canonicalizes under all 48 permutations in \(S_4\times S_2\). The written
profiles are checked against the resulting complete orbit set.

| Profile | Root red edges | Nonzero root defects | Labeled copies |
|---|---|---|---:|
| 1 | 03,13,23,45 | \(f_3=4\) | 4 |
| 2 | 03,13,23,35,45 | \(f_3=f_5=2\) | 8 |
| 3 | 03,13,23,34,35,45 | \(f_4=f_5=2\) | 4 |
| 4 | 03,12 | \(f_4=f_5=2\) | 3 |
| 5 | 03,12,23,45 | \(f_2=f_3=2\) | 12 |
| 6 | 03,12,23,35,45 | \(f_2=f_5=2\) | 48 |
| 7 | 03,12,23,25,35,45 | \(f_5=4\) | 24 |
| 8 | 03,12,23,25,34,45 | \(f_4=f_5=2\) | 24 |

Profiles1--3 are excluded analytically. The three A leaves each have seven
red B-neighbors. A blue leaf pair has \(c_B=20-8-8+c_R\le6\), so its red
codegree is at most two; the common center consumes one of these two
places. Their B-neighbor sets have pairwise intersections at most one,
forcing union size at least \(21-3=18>16\). Relabeling the roots is not
an assumption that the whole host admits an automorphism.

## Independent exhaustive incidence reconstruction

Write \(R_0\) for red adjacency on the roots, \(M\) for the binary
16-by-6 B-to-root incidence matrix, and \(G=M^TM\). A root with
\(f_j=0\) has its entire F-row zero by nonnegativity. In a two-active-root
profile only \(F_{ab}=w\in\{0,1,2\}\) can be a nonzero root-root defect.
Profile7 has one active root and every root-root defect is zero.

The root Gram is determined by
\[
G_{ii}=d_i-d_{R_0}(i),\qquad
G_{ij}=d_i+d_j-14+(17-d_i-d_j)(R_0)_{ij}
-|N_{R_0}(i)\cap N_{R_0}(j)|-F_{ij}.
\tag{3}
\]
For a red pair the total red codegree is \(3-F_{ij}\); for a blue pair
\(c_B=20-d_i-d_j+c_R\), proving (3). Independent construction uses these
two cases directly rather than importing the author's matrices.

Put \(t=(1,1,1,1,-1,-1)^T\) and for a row word x set \(\delta(x)=xt\).
Every incidence row has nonnegative surplus. Equations (1)--(3) imply
\[
\sum_v\delta_v=8,\qquad M^T\delta=Gt.
\tag{4}
\]
The reviewer enumerates all positive-surplus row multisets in increasing
numeric word order, permitting repetitions by recurring at the same
word index. It tracks the 21 ordinary integer Gram quotas and all six
weighted quotas \(Gt\). A chosen word subtracts one from its Gram
features and \(\delta\) from its supported weighted coordinates.
Only necessary completion conditions prune: all quotas are nonnegative,
no weighted coordinate exceeds the remaining surplus mass m, and the
remaining second moment lies in \([m,4m]\) with its difference from m
even. These follow from \(1\le\delta\le4\) on positive words and
\(\delta^2-\delta\) being even. A valid multiset has one unique ordered
recursion path and cannot be removed by these conditions. At most eight
positive rows are needed. This method uses no lane packing, author
moment-profile list, supplied incidence list, or author's grouped join.

After the positive rows are exhausted, the zero-surplus rows are uniquely
recovered. They are the empty word, eight words \(\{i,c\}\), and six
words \(\{i,j,4,5\}\), with \(i,j\in A,c\in C\). If H is the residual
Gram, their counts are
\[
n_{\{i,j,4,5\}}=H_{ij},\qquad
n_{\{i,c\}}=H_{ic}-\sum_{j\in A\setminus\{i\}}H_{ij}.
\tag{5}
\]
The empty word fills the row count to sixteen. Nonnegative integral counts
and all 21 reconstructed Gram entries, including the diagonal, are checked.
Thus each valid incidence multiset is recovered, and invalid residual
solutions are rejected. Sorting B rows is a relabeling, not host symmetry.

All 13 root-profile/weight cases are covered below. In particular, the
four weight-two cases are reconstructed rather than rejected by the
author's active-column correlation lemma. Recursion visits 161,014 states,
with at most 65,193 in one case. The state guard is 2,000,000 per case;
none is reached. The independent proof recovers the original 143 forms
and 56 further weight-two forms, for 199 complete incidence forms.

## Literal local stars and complete reciprocal contradiction

For each incidence form, a degree-nine B vertex v with root word x has
exactly \(9-|x|\) red B-neighbors. Enumerate every subset of this size
excluding v. Attach the fixed root neighbors x and compute its ordinary
red and blue pages at every root--B pair by intersections in the literal
22-point universe. Retain the row precisely when all six page caps hold
and every saturated-root defect is zero. The active defects only have to
be nonnegative. There is no active column allocation, root-column sum,
correlation, parity, per-B-point defect budget or upper bound inherited
from an active root's total defect budget imposed in this filter.

The second decoder independently scans all 65,536 binary neighbor masks
for every labeled B vertex. It computes
\[
F_{vj}=\ell_j-2x_j\mathbf1_{j\in C}
-|x\cap N_{R_0}(j)|-|N_P(v)\cap M_j|,
\qquad \ell=(3,3,3,3,5,5).
\tag{6}
\]
This follows from \(d_v=9\): for an A root either color gives total red
codegree \(3-F_{vj}\); for a C root it is
\(5-2x_j-F_{vj}\). Thus the formula is the same necessary condition as
the literal page intersections. All labeled mask/active-defect tuples
agree entry by entry. The first generator uses equal-word transpositions
only to avoid repeating local enumeration; the second enumerates each
labeled vertex separately and does not trust that transposition bridge.

For the resulting domains \(\mathcal D_i\), every simple symmetric P
must choose one row per vertex with matching reciprocal edge truth values.
In one synchronous round delete a row at i if some current domain at j
has no row agreeing on edge ij. Equivalently, intersections and unions
of the domains identify forced and forbidden edges. Any actual solution
supplies support at j and is preserved in every round. An empty domain
therefore proves nonexistence. A fixed point with every domain nonempty
would not prove nonexistence and would stop the theorem checker with an
error.

The reviewer replays each complete round with literal matching-row scans,
independently of the forced/possible-bit implementation. All 20,264
candidate deletions are checked. Exactly 115 of the 199 forms already
have an empty local domain; the remaining 84 empty after at most five
batch rounds, with 142 rounds in total. No B--B page inequality is used
in this final finite filter.

| Profile | w | Incidence forms | Initial labeled candidate masks | Forms needing rounds | Batch rounds |
|---|---:|---:|---:|---:|---:|
| 4 | 0,1,2 | 0,0,0 | 0 | 0 | 0 |
| 5 | 0 | 36 | 16,516 | 14 | 14 |
| 5 | 1 | 105 | 40,746 | 28 | 56 |
| 5 | 2 | 56 | 18,088 | 42 | 72 |
| 6 | 0,1,2 | 0,0,0 | 0 | 0 | 0 |
| 7 | 0 | 2 | 480 | 0 | 0 |
| 8 | 0,1,2 | 0,0,0 | 0 | 0 | 0 |

The 75,830 masks count all sixteen labeled vertex domains per incidence
form; they are not comparable to the author's representative-only mask
count. The star proof and the complete relaxed finite obstruction exclude
\(q_0=4\). Importing the credited zero-defect exclusion and using (2)
proves all three asserted inequalities.

## Strengthening and improvement opportunities

**Proved certificate simplification.** The entire defect-four contradiction
works with unrestricted nonnegative active-root defects in the final
local domains. The original 475 active-defect placements, their column
sums, correlations and parity, and the separate weight-two correlation
contradictions are unnecessary for this proof. All 199 relaxed incidence
forms fail by local root spines and reciprocal consistency alone. This
reduces the dependency and enumeration burden of the certificate.
Some omitted budget constraints follow automatically once an actual
symmetric P with the prescribed degrees and Gram exists. Accordingly,
this is a proved simplification of the finite method and larger local
domains, not a claim that the original ordinary-book hypotheses have
been weakened or that a stronger global host theorem was established.
The initial root classification and surplus restriction still use the
original nonnegative book defects.

**Next frontier, not excluded.** At root defect eight, (2) gives
\(e_R(A)-e_R(C)=3\) and total B surplus \(\sum_B\delta=6\).
This makes another finite incidence reduction plausible, but a proof
would require a complete new root-shape classification, all possible
root-root defect allocations, new Gram cases, and a demonstrated
contradiction in every case. The root shapes and thirteen cases here
apply only to defect four; they cannot be reused as coverage for eight.
Independent local domains may survive there, so active budgets, B--B
pages or another analytic invariant may become necessary. None of these
additional obligations has been discharged in this review.

**Shorter analytic certificates.** Profile7 has an already published
direct local-star explanation, which was checked against the two rebuilt
forms. Profile5 accounts for all reciprocal rounds. An analytic description
of the forced/forbidden edges across its 197 forms could replace part of
the computation; it would need to explain the full multiplicity domain
and each class of reciprocal contradiction, including all weight-two
forms. A few illustrative cases would not prove complete coverage.

**Formalization.** The recursion completeness, zero-row reconstruction and
support-preservation lemmas are small exact objects suited to formal
verification. The bridge from ordinary book pages to the finite Gram and
row-domain conditions must be included. Merely checking the compact
expected hashes would leave that bridge and completeness unproved.

## Independent controls, author replay and trust boundaries

The main incidence control exhausts all 1,653 unordered two-row multisets
in the entire 57-word nonnegative-surplus domain, groups them by exact
Gram, and recovers all multiplicity vectors by the new recursion. Four
16-row repeated-word positive controls cover all positive surplus types.
The reciprocal control exhausts all 3,375 nonempty three-vertex domain
systems, explicitly tests every row tuple, and preserves all 2,397 systems
having a symmetric graph. It independently replays every pruning round.
An intentionally incomplete state-limit-one incidence run raises
INCOMPLETE under normal and optimized execution.

The separate [controls.py](controls.py) checks signed identities on
16 simple 22-point graphs, 15 distinct, with the exact histogram. Their
defects may be negative and none is a valid Ramsey construction. Literal
pair/triangle counts validate 3,696 off-diagonal pairs, 352 incident rows,
576 Gram entries, 1,536 root--B equations, 576 symmetric MTPM equations
and sixteen root budgets. A fabricated deletion at a reciprocal edge
with support is rejected. These are identity and boundary controls,
not exhaustive host proofs.

The known [primary 21-point construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was fetched live and its leading JSON matrix complemented off the
diagonal, then compared with [baseline21.rows](baseline21.rows) in all
441 entries. It has 93 red edges and red/blue page maxima 3/6. Its hash,
normalization and provenance appear in [INPUT.json](INPUT.json). It
validates established prior work and is not a new lower bound.

Both author commands were replayed sequentially on frozen source and
passed. Their separate audit reconstructs all 143 incidence forms, 475
defect placements and 12,693 permitted representative masks, then replays
all 102 original exclusion traces and 4,354 candidate-pair checks. Those
two programs are separate algorithms by the same researcher. They remain
author checks even when replayed by this reviewer.

After the standalone reviewer proof, [compare_author.py](compare_author.py)
compared all 9,152 original multiplicity entries and checked that every
original representative mask/defect pair belongs to the newly generated
relaxed literal domain. These private author records neither select nor
complete the independent domain. The placement counts were passively
counted; their full reconstruction is credited to the author program,
not misreported as a third independent placement algorithm.

Both standalone main runs, normal and `-O`, produce identical compact
output SHA256
`1132c2dc6d5b6e7b51b2765961d0ee8328929e7a9cca4d989dc94d23cdaf9b94`.
They took 49.272/50.504 seconds with peak RSS35,968/35,760 KiB.
The author primary/separate replays took 47.659/57.059 seconds with
RSS40,832/45,408 KiB. All jobs ran sequentially with thread limits one,
unchanged memory limits, and no resource guard reached. The separate
normal/optimized controls passed with identical output. Exact commands
are in [README.md](README.md), detailed evidence in
[VALIDATION.json](VALIDATION.json), and checksums in [SHA256SUMS](SHA256SUMS).
Full generated incidence and star corpora are omitted and rebuilt from
the compact public source when desired.

Trust includes the ordinary mathematical reduction, completeness and
support-preservation arguments, the credited root-zero proof, CPython
3.11.2 exact integers and execution, the independent source, and fixture
normalization for the positive control. There is no floating-point
decision, solver, supplied large proof corpus or proof-assistant
formalization. Hash agreement records provenance, not proof. Timeout,
guard exhaustion or resource failure cannot be interpreted as
nonexistence. Source publication and shared signing identity do not
themselves establish mathematical validity or independent authorship.

## Literature, credit and publication readiness

Reopened live on 2026-10-01, the
[primary paper, Table1](https://arxiv.org/html/2407.07285v2) and
[Small Ramsey Numbers, DS1.18, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
retain the located interval \(22\le R(B_4,B_7)\le23\); the latter table
was also inspected as a PDF image. The primary lower construction was
checked as above; the general upper-bound certificate was not replayed.
This conditional review does not change the located Ramsey interval.

Bounded candidate-specific searches covered the exact book parameter,
histogram (4,16,2), root defect eight/four and reciprocal-spine obstruction.
No matching earlier application was located; these are not an exhaustive
priority audit. The counting, binary Gram, Möbius reconstruction and
reciprocal support-pruning mechanisms are elementary or standard.
Researcher credit concerns the graph-specific defect-four exclusion;
the review contributes independent confirmation, a different ordinary
integer incidence recursion and a proved removal of active-placement
constraints from the finite certificate. Historical novelty, correctness
and graph-level verification remain separate assessments.

The target is ready as a documented conditional computer-assisted lemma
with compact source and the imported zero-defect premise explicitly
identified. Full endpoint publication would require exclusion of all
remaining positive-defect cases and other allowed histograms, or an
actual 22-point construction. No such resolution is certified here.
