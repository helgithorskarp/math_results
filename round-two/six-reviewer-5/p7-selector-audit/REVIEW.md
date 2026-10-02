# Independent P7 selector review and sharp opposite-hub interface

Actual contributor: **six-reviewer-5**, role **independent mathematical
reviewer**, 2026-10-02. The common campaign signing identity does not
establish distinct authorship. This is a new independent audit of
six-code-1's claim, with explicitly credited reuse of this reviewer's own
earlier finite primitives and carrier theorem.

**Verdict: confirms the full stated restriction9215**, conditional on the
explicit previously reviewed finite inputs below. Every71-word packing
of profile(17,19,19,20^15) with total hub-pair multiplicity7 has E>=2;
if E2, its three-unsaturated-point triple is uncovered. The proof is an
ordinary combinatorial reduction with exact finite checks, not a
proof-assistant formalization. No defect was found in the original
center-reversal or reciprocal-leave argument.

Target: **bafkreid5crq5qfpshkaltx5vu5lwcwxyfls4fr65l44cwhhgymfsni23oe**,
committed lemma9215, “A(18,6,5): the17/19/19 P7 boundary forces row excess
at least2, with uncovered hub triple atE2”. Original researcher source
commit **1cf7217d385522501bd9547f6582718da154fd46**, direct
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/p7_small_excess_selector/PROOF.md).
The earlier [review9217](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/three-hub-budget-audit/REVIEW.md)
only confirmed9180 and excluded E0 at P7; it supplies no E1/E2 verdict.
The present target was independently selected after full-body and
neighborhood inspection at9228. Peer review scopes were checked to
avoid redundant sufficient assessment.

**Proved refinements in this review:** the relevant five-distinct-point
unit/unit interface cannot exist; the corresponding unit/mixed interface
has sharp maximum61 without the original covered-triangle premise. A
quantified selector needs no tau0 premise. Its application removes113 of
213 normalized necessary inventories in the still-open E2,t0 sector,
leaving100. These are necessary statistic inventories, not packings or
isomorphism classes of packings. The unrestricted campaign interval69--71
and the full17/19/19 profile remain unresolved.

## Definitions, budget and coverage

Let F be71 distinct five-subsets of an18-point set with pairwise
intersection at most2. Write r_p for replication, lambda_pq for pair
multiplicity, and say a triple is covered when it is contained in a word.
Let H={w,u,v}, r_w=17,r_u=r_v=19, and S the15 points of replication20.
Set a=lambda_wu,b=lambda_wv,c=lambda_uv, and t in {0,1} for coverage of H.
At each saturated center s, delta_sp=5-lambda_sp is nonnegative with
sum5. Let h_s count positive deficits, e_s=5-h_s, and q_s count uncovered
triples through s whose other two points are both deficient at s and
include at least one point of H. A high-leave edge touching two H points
is counted once. Put E=sum_s e_s,Q=sum_s q_s. Let X be total unordered
S-S excess sum(max(delta_xy-1,0)); let tau count uncovered all-S triples
whose three pairs have positive deficits.

Universal8323 and the exact deficit budget8368 give

\[
 D=(D_w,D_u,D_v)=(14-c,6-b,6-a),\qquad W_{SS}=28,
\]
\[
 E+Q+2\tau=6-t,\qquad E=19-\sum_{s\in S}k_s+2X,
\]

where k_s is the number of deficient H points in row s. A saturated
link has exactly h_s-1 uncovered high-high triples and no uncovered
low-low triple. Each low point has exactly one leave friend. An H-pair
tail covers exactly3lambda_ij-t distinct S points, so the number L_ij
of rows low to both hubs satisfies L_ij<=3lambda_ij-t. Also
L_ij>=15-D_i-D_j. These inequalities force a,b>=1,c>=3 and leave
exactly (1,1,5),(1,2,4),(1,3,3),(2,2,3), up to swapping the equal-replication
u,v roles. The source additionally runs both other ordered cases
(2,1,4),(3,1,3). No automorphism of F is assumed.

For E<=2, every positive deficit partition has h=3,4 or5. For h3/4,
the audit admits every graph with h-1 edges and every ordered positive
partition of5. For h5, the four complete unit high-leave classes from
generic census8933 are used. All distinct ordered H marks, including
absent high marks, are tried. This is an enlarged necessary domain,
not an assertion that its rows can be simultaneously realized. A good
hub flag requires that hub isolated in the high leave and either a unit
row or a mixed2111 row heavy **at that hub**. A mixed row heavy elsewhere
does not acquire this flag merely from hub isolation.

The independent projection has117 six-coordinate types; retaining
three flags gives138 nine-coordinate types. At most six positive-cost
rows occur since each costs e+q>=1 and the total cost is at most6-t.
The remaining four zero-cost filler types are uniquely determined by
the three cross-weight deficits and the total row population15.
The producer checks excess conservation, SS evenness, tau parity, all
three pair-tail cuts and the shared-hub cohort cuts. It conservatively
uses the cohort cut only at X0; no X>0 budget-valid record occurs in the
claimed domains or the reported E2,t0 survivors. The original flagged
cut at X>0 is also legitimate, since each flagged row has unit S-S
deficits; no objection to that original step is asserted.

A separate cost-class occupancy algorithm enumerates124 occupancy
patterns and30589 exceptional multisets before hub filters, with no
monotone row recursion or hub-deficit pruning. It solves fillers through
the independent SS weighted-degree equation sum56, then compares the
entire actual budget-valid multiset sets in all36 ordered domains,
including six E2,t0 extension domains. This tests coverage before
the low-pair or independent-cohort cuts, rather than just final totals.

## A new sharp local interface with opposite isolated hubs

This statement has no global replication-profile or71-word assumption.
Let F be any packing of five-subsets on18 points with distinct
physical points x,y,U,w,V such that:

1. r_x=r_y=20; lambda_xy=4; lambda_xV=lambda_yV=5; xyV is uncovered.
2. x is unit: every lambda_xp is4 or5. Also lambda_xU=4,
   lambda_xw=5, and U is isolated in x's induced high leave.
3. lambda_yU=5; lambda_yw is3 or4; every other lambda_yp is4 or5;
   w is isolated in y's induced high leave.

**Then lambda_yw=3 and |F|<=61; the bound61 is attained.** In particular,
the branch where y is unit has no compatible complete two-star core.

Proof and computational boundary: import the complete actual-point
two-star carrier proved in [review9141](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/unfiltered-two-star-audit/REVIEW.md),
reference **bafkreiewiqmpeig4hs4vmz2qgdt3lsim6lk7y7ph5tlvbzovbtmrykc3lm**,
source **bde7ea936c220c567874957906688597da8387d7**. This carrier covers
every raw interface with a unit second center and a unit or isolated-heavy
first center at its marked hub, multiplicities4/5 to the other specified
center/low hub, and the specified uncovered center-center-low triple.
Its34 normalized36-word cores cover all raw cases through actual18-point
transports. The prior complete unquotiented enumeration and its transports
are mathematical premises here; the191-million-map raw census is not
rerun or newly claimed.

For the unit branch use old first=x, old second=y, old marked hub=U,
old low hub=V, and try **every** remaining physical point as w. For the
mixed branch use old first=y, old second=x, old marked hub=w, old low
hub=V, and try every remaining physical point as U. The extra-hub
condition is invariant under the imported actual point transports, so
checking every extra marking on every normalized representative covers
every raw case. [interface.py](interface.py) freshly decodes all34 cores
from the generic fixtures and literal point maps, checks every original
simultaneous role condition, every pair intersection, and each extra
mark. All eight unit-first roots fail the opposite-isolated-hub condition.
Exactly three mixed extra marks survive:

| Prior root | Physical (x,y,U,w,V) | Residual candidates | Graph edges | Exact residual maximum | Total |
|---|---|---:|---:|---:|---:|
|22|(11,17,16,13,2)|116|5576|23|59|
|23|(11,17,5,13,2)|122|6107|25|61|
|24|(11,17,8,13,2)|122|6117|20|56|

The two center stars are already complete, so any remaining word avoids
both centers. Every one of the4368 five-subsets of the other16 points
is tested against the36-word core. A second owned-triple oracle checks
the whole candidate universe and every adjacency. The independently
audited exact unweighted clique kernel gives the maxima above, taking
1034,246,7330 nodes respectively with unchanged guards. Each maximizing
completion is literally checked against all five-role hypotheses.
[WITNESS61.json](WITNESS61.json) attains61 in root23. The cap is thus a
complete carrier corollary with freshly rebuilt residual graphs and
exact maxima, conditional on prior9141 coverage. It is not a new raw
carrier census, new unrestricted69/70 construction or literature-priority claim.

## Quantified selector without tau0

Suppose X0, so the S-S positive-deficit support G is a simple graph
with28 edges. Let A consist of good singleton-w rows: unit rows, or
mixed2111 rows heavy at w, with w isolated in the high leave. Shared-hub
8356/8397/8438 imply A is independent. Write d=sum_{y in A}deg_G(y),
M=28-d. Exactly M edges lie wholly outside A.
Let B be the unit singleton-u or singleton-v rows with their own
deficient hub isolated. Put

\[
 \Gamma=|B|-[15-(3c-t)]-2M.
\]

At most15-(3c-t) points of B are absent from uv tails, and at most2M
points touch an edge wholly outside A. Thus at least Gamma points
x in B belong to a uv word and have every G neighbor in A. This
union-bound argument needs **no tau0 condition**.

For any such x let U be its deficient degree19 hub and V the other.
The low point V has one leave friend in x's link. That friend cannot
be U because xuv is covered, or w because xw and xV are both low and
there are no low-low leaves. Consequently the friend is y in A. The
triple xyV is uncovered, lambda_xy4, lambda_xV=lambda_yV5, lambda_yU5,
lambda_xw5, lambda_xU4 with U isolated, and y is unit or heavy only at
isolated w. All five **distinct physical marks** in the new local
theorem hold simultaneously. Unit y is impossible; mixed y gives
|F|<=61. Therefore **Gamma>0 excludes a71-word ambient realization**.

There is a further purely reciprocal capacity simplification. At each
mixed y in A both degree19 hubs are low, and each has one leave friend;
at most two eligible unit x points can use that y. If A has m mixed
rows, Gamma>2m already contradicts the unit-branch incompatibility and
leave-friend capacity, without computing a mixed residual maximum.

## Closing all claimed E0/E1/E2,t1 inventories

The original complete ordinary proof was read in full. Its support
inequalities and pair-tail cuts retain all hubs, and its reversed-center
use of9045 is sound: when the selected friend y is mixed, (y,x),w,V
has a heavy isolated first row and a unit second row low to both marked
hubs. The remaining unsaturated U is low at y and fails the additional
triangle antecedent; all saturated antecedents are covered by tau0.
Using (x,y) instead would violate the original unit-second-row premise.
The original E2,t1 argument also correctly retains reciprocal coverage
of wyz, rather than treating its two saturated centers independently.

The independent enlarged domain before researcher executable read
has11 coarse surviving statistics:1 at E0,9 at E1,1 at E2,t1. The
refined domain has50: six E0 at(1,1,5),43 E1 split32/11 at(1,1,5)/(1,2,4),
and one E2,t1 at(2,2,3). Every E0/E1 survivor has X=t=tau0. The actual
138 row tuples, all20 normalized domain summaries including state
counts, and all50 normalized original survivor records are compared
entrywise with [AUTHOR_EXPECTED.json](AUTHOR_EXPECTED.json). We do not
claim equality of the original whole-record hash, which includes the
old covered-triangle bridge rather than this new local proof.

For the49 E0/E1 survivors, A has degree27 or28, B consists of actual
unit singleton rows, and Gamma>0. The new bridge closes34 through
unit-friend core incompatibility, nine through Gamma>2m capacity, and
six through the sharp mixed61 theorem. All50 count certificates are
in [EXPECTED.json](EXPECTED.json). All additional reversed ordered
E1 survivors are also checked directly in the30 ordered claimed domains;
the ordered total is61, of which11 duplicate u/v-renamed normalized
E1 statistics. This is renaming of role labels, not quotienting by an
ambient automorphism.

The sole E2,t1 surviving inventory has one heavy three-hub row with
(delta_w,delta_u,delta_v,e,q,SSdegree)=(3,1,1,2,2,0), one unit singleton-w
row z with (1,0,0,0,1,4), and zero-cost counts(0,7,3,3). It has X=tau0,Q3.
Seven good unit-w rows form an independent A of degree28, so every one
of z's four G neighbors y lies in A. Isolation of w at each y says
wyz is covered. Therefore no high-leave edge at z can touch w; z has
no other deficient hub. This forces q_z0, contradicting its required1.
This final contradiction is ordinary reciprocal triple ownership, not
a numerical local completion bound.

All claimed sectors fail, proving E>=2 and E2=>t0 at the exact profile
and P7. The original author's result has full independent support at
the stated imported-premise boundary; no verdict is transferred to
the broader new-carrier claims9176 or9209.

## Strengthening and improvement opportunities

**Proved:** the five-role sharp61 corollary replaces the covered-triangle
local64 bridge in this selector, excludes the unit/unit case at core
level and removes tau0 from the reusable selector. Its fresh extension
to E2,t0 gives:

| (a,b,c), up to u/v renaming | Necessary inventories after original cuts | New Gamma>0 exclusions | Remaining |
|---|---:|---:|---:|
|(1,1,5)|69|68|1|
|(1,2,4)|83|45|38|
|(1,3,3)|9|0|9|
|(2,2,3)|52|0|52|
|Total|213|113|100|

Every reported extension survivor has X0. All113 newly excluded
inventories happen to have tau0; the stronger selector's general
statement removes that hypothesis, but no actual tau-positive excluded
example is claimed in this table. Running all six ordered cases gives
305 necessary inventories,158 excluded and147 remaining. These are
different bookkeeping conventions for the same equal-hub renaming.
Neither table counts codes or proves that a remaining inventory is realizable.

The sole residual(1,1,5) statistic has two exceptional singleton-w unit
q1 rows, one heavy three-hub row(1,2,2,2,2,0), filler counts(0,6,3,3),
Q4,tau0. Here A has six good unit rows, degree24, B six unit points,
four edges outside A and Gamma=-2. Closing this case requires an actual
reciprocal friend-routing or triple-ownership restriction on those four
edges; the count criterion alone supplies none. The other remaining
99 refined statistics are similarly exact next finite interfaces.

**Open improvements:** combine precise reciprocal edge-charge constraints
with these100 necessary statistics, then identify literal additional
hub marks before applying any broader local theorem. The researcher's
private33-inventory reciprocal reduction reported in chat1508 is credited
as a separate unpublished development; its evidence is not imported,
intersected with this table, or asserted independently verified here.
The newer [9176 local interfaces](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/additional_deficit_pair_interfaces/PROOF.md)
and [9209 second-v relaxation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/unit_second_v_four_interfaces/PROOF.md)
may help if every simultaneous ordinary mark is proved; they remain
unreviewed context in this audit. A complete exclusion of E2,t0 would
still leave E>=3 and larger P; no global endpoint is implied.

**Fresh context:** during this audit the three-point selector9249,
**bafkreibbbtgqmcd56rs55op2fl6gbo4oklwr5byq4eqkl5xkhswyn5iag4**,
was committed from source **f75822147714015beb30b690d4fbfbd52b6f01d0**;
its [full source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/unit_second_u_four_interfaces/PROOF.md)
and full signed body were read. It asserts upper67 from distinct x,y,U,
two saturated centers with pair4, a unit y row, and deficient U isolated
in x's induced high leave. Its new lambda_yU4 branch and inherited9209
branch remain separately unreviewed here. Reviewer4 independently
selected9249 (chat1553); its pending verdict is not assumed. The owners'
private unit-partner count and proposed larger P restrictions
(chats1549/1555) are also credited context only. They may replace the
remaining friend-routing question with existence of an isolated deficient
row, but their stronger global conclusions are neither imported nor
independently assessed in this review. The new sharp61 interface and
the independently verified9215 selector use only the earlier complete9141
carrier, with no dependence on this new three-point certificate.

Formalizing the short deficit identities, the actual extra-mark transport
argument and the opposite-hub selector would reduce the ordinary-proof
trust boundary. Formalizing only the generated inventory hashes would
leave those essential links open. Broadening the local theorem by
discarding lambda_xw5 or lambda_yU5 requires a genuinely broader carrier;
this complete three-root computation does not justify that relaxation.

## Independence, reproduction, literature and limits

The independent coarse and refined mathematical records were sealed
before reading any target9215 executable. [FIRST_SEAL.json](FIRST_SEAL.json)
preserves their original hashes: coarse compact canonical JSON
`63d2dfb7e502c57b12895f17c8a3f5a4023c9c9acc0c7a6a3d9e2b56b9f676ec`,
refined actual default-spaced file bytes
`9ed9e5357636a52fbef2d2197e9c53854448275c9e575f1c47d3bc52c92be766`.
Both original records regenerate exactly. The target's executable source
was later read as text to audit its steps; no researcher engine is
imported or executed. Seven unchanged pure row/fixture functions reuse
this same reviewer's source5da38609ee3a674dc37f262fe334a28ab548d8a8,
and the independently audited clique kernel reuses prior9141 source.
[PROVENANCE.json](PROVENANCE.json) gives exact file/function hashes.
This is continuing independent methodology, not an additional reviewer.

The generic23 fixtures originated with8720, source
69f2312bb468eb59b8ab3d8978fe19b3d86cf58a. Generic completeness8933,
universal8323, deficit budget8368 and shared-isolated-hub8356/8397/8438
are imported mathematical premises, with precise review8989 for the
shared-hub mechanisms. Direct source:
[universal review](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md),
[generic census review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twenty-star-classification-audit/REVIEW.md),
[deficit budget](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/DEFICIT_CUT_71.md),
[common mixed](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/COMMON_MIXED.md),
[common unit](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/COMMON_UNIT.md),
[common mixed/unit](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/COMMON_MIXED_UNIT.md),
[shared-hub review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/multiplicity-four-audit/REVIEW.md).
No involution or arbitrary-code symmetry premise is imported from8720.
The old covered-triangle9045/9076 and unfiltered9098/9141 retain credit;
only9141 completeness is needed for the new local computation. The
two-unsaturated9073 result is prior context, not a premise of this
three-hub transfer. The earlier P>=7 restriction9180 remains prior work.

Run the two commands in [README.md](README.md). Standard-library
CPython3.12.14 normal and optimized runs compare the entire frozen
mathematical record, SHA256
**e810a32faf8b064be44293c10c6b65f27b45325fe2a425f698dc865f9e87f3ad**.
Both reject14 semantic damages and nine changed external inputs, and
verify1100 simple graphs against complete subset clique maxima. Literal
attaining completions verify the opposite isolation, orientation and
five distinct physical marks. The full50 selector certificates,
all34 extra-mark records, all three rebuilt graphs and all36 coverage
records are compared, not only aggregate totals. Full generated inventories
stay in scratch. Reproduction details are in [VALIDATION.json](VALIDATION.json).

Fixed200000-state/20second producer and occupancy guards,
3000000-node/30second clique guards and60second whole-audit guard are
unchanged throughout validation. Peak producer states30331, peak clique
nodes7330; no guard was hit. All native threads1, serial jobs,
unchanged1CPU/2GiB. Timeout, incomplete computation, memory kill or
UNKNOWN establishes no absence. The reduction, inherited finite
completeness, clique algorithm and Python interpreter remain explicit
trust boundaries; there is no independent search trace or proof-assistant
certificate. That limitation is compatible with the stated conditional
computer-assisted verdict, not a claim of formal proof.

Candidate-specific primary literature was refreshed2026-10-02, including
queries for the exact A(18,6,5),71/61 and profile constants. The
[maintained table](https://aeb.win.tue.nl/codes/Andw.html) still gives69--72;
[Aw--Chee--Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf), Theorem1
and AppendixA, supplies the established69 construction; [Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf)
supplies the saturated point cap20. Those facts are prior art, and no new
baseline reproduction or priority is claimed. This campaign's reviewed
upper71 is separate prior progress. The local sharp61 and113-inventory
cut are proved graph-level refinements relative to the inspected sources;
absence from a bounded search does not establish historical novelty.
The compact artifact is ready for scoped source/graph publication, while
global resolution and journal-level priority remain unestablished.
