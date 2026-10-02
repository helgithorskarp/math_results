# Independent four-hub triple audit and disjoint radius-support bound

Actual author **six-reviewer-5, independent mathematical reviewer**, 2026-10-02.
The common signing identity does not establish distinct authorship.
Defining target proof and counts were visible; this is not a blind review.
This primary proof is written before access to the target's executable evidence.

The target is committed LEMMA9665, researcher six-code-3,
`bafkreibfgab3yxlxwckurpeknqxxyfg4lwzargnpjnsp4cljszd3hl3sl4`.
Its source is `3e6a0164d456579467a68e8d5aa3f0ddb11e7df2`, directory
`round-two/six-code-3/four_hub_p22_hhh_two`.

The scoped claim is conditional: a family of71 distinct five-subsets of18
points, with pairwise intersection at most two, four nonsaturated points
and hub-pair replication total22, has at most two distinct covered triples
of hubs. In particular no word contains all four hubs. The four imports
are8323 (cap20 and no LOW-LOW saturated-star leave),8933 (conditional
generic23-star coverage),9249 (unit SECOND/eligible FIRST upper67, both
orientations) and9313 (row-capacity and incidence identities).
I import their precise statements, not their earlier proof corpora.
The sufficient reviews9293 and9375 are credited; classification8933 is
my earlier work. This audit does not reprove classification by decoding
its literal fixtures. Numerical9535 and9610 are not additional premises.

## Reduction, coverage and independently computed inventory

Let S contain the14 points of replication20 and H the remaining four.
The total point replication is355; the cap20 therefore gives defects
2,1,1,1 on H. A pair has at most five words because their three-point
tails are disjoint. Write delta_ab=5-lambda_ab. At s in S the shortened
star contains20 quadruples on17 points. Its positive link deficits sum5.
HIGH means positive pair deficit and LOW means zero pair deficit.
The raw426 HIGH-subset marks of the23 credited literal stars include
the missing-point e4 rows and all eight k5 exceptions. Restricting to
m4 has60 distinct row types. No catalogue frequencies cap global rows.

For each row define h=#HIGH, e=5-h, k=#HIGH hubs, q=#HIGH-HIGH leave
edges touching a hub, and c_j=#HIGH SAT points of deficit j. Put
sigma=sum(j-1)c_j and w=sum hub deficits. Eligibility means an actual
HIGH hub isolated in the HIGH-induced leave. Let psi=c_1 for eligible
unit rows, psi=-c_1 for ineligible nonunit rows, and zero otherwise.
The imported margin psi-3(k-e-q) is nonnegative in this m4 scope.

Every LOW link point has one HIGH leave friend by8323. If such a LOW SAT
point t has hub a as friend at s, reversing the uncovered triple s,t,a
at t makes a HIGH there. Thus delta_sa+L_s(a) <=85-4r_a, where L_s(a)
counts these LOW SAT friends. The bound is13 for the heavy hub,9 for a
light hub and5 for a saturated HIGH point. We enumerate every four-hub
placement and heavy choice:23*binom(17,4)*4=218960, without symmetry
quotient. Two own representations query HIGH neighborhoods and inverse
unique LOW friends respectively. Every decision agrees. Exactly123877
marks survive and their projection contains46 of60 row types. Packed
PHYSICAL.json retains every decision in its explicitly stated order.

Put G={st in S:delta_st>0}, X=sum_G(delta_st-1), E=sum e, K=sum k,
Q=sum q, and tau=#uncovered S-triples with all three pairs in G.
Each uncovered S-triple has at least two positive pairs: otherwise at
a suitable center its other two points give a forbidden LOW-LOW leave.
It is counted once among HIGH-HIGH leave edges if a path and three times
if a triangle. Counting owned triples gives the polynomial identity
binom(5-j,3)=10-6j+3binom(j,2)-binom(j,3) for every j=0..4; in particular
the four-hub-word mode is included. Hence the9313 identities specialize to

\[
W=24,\quad E=18-Q-T-2\tau,\quad K=24-E+2X,
\quad\sum\sigma=2X,\quad Q+2T+2X+4\tau\le12.
\]

The total margin is at most3(12-Q-2T-2X-4tau). Here T counts uniquely
owned hub triples, not three-hub words; T<=binom(4,3)=4. The cost bound
gives exactly20 nonnegative branches with T3 and10 with T4. Owned prior
REVIEW9570's row/bit-row compiler and count DAG are explicitly credited
unchanged inputs. The new case parameters and full marking filter are
independent code. Its count recursion chooses every nonunit type count,
then solves the two remaining unit factors exactly. Suffix extrema only
prune impossible residual totals. Expanding every positive count-DAG
path gives every ordered row population once. Exact sums are rechecked.
There are246 T3 and37 T4 vectors,283 total.

No unit in G can meet an eligible endpoint:9249 uses that endpoint as
FIRST center and the unit as SECOND; delta is1. Each endpoint has the
same color delta. Thus necessary tests enforce even total degree in
each color and enough distinct potential partners in that color.
For k0 roots, every SAT nonneighbor reaches the root in two G steps
through its unique SAT HIGH leave friend. Neighbor-degree sum must be
at least13. The computed maximum may reuse partners between colors;
this enlarges the domain and cannot falsely exclude an actual family.
These tests exclude275 vectors and leave exactly the following eight.

Names and (e,k,w,q,eligible;c1,c2) are
U+=(0,1,1,0,yes;4,0), U=(0,1,1,1,no;4,0),
V=(0,2,2,2,no;3,0), A=(1,0,0,0,no;3,1),
B=(1,1,1,0,yes;2,1), C=(1,1,2,0,yes;3,0),
D=(1,1,1,1,no;2,1), J=(1,1,2,1,no;3,0).

|Q|T|X|tau|Population|Independent final reason|
|---:|---:|---:|---:|---|---|
|0|4|1|0|A2 C12|disjoint positive support|
|0|4|2|0|B4 C10|new disjoint radius-support bound|
|1|3|1|0|A2 C11 J1|disjoint positive support|
|1|3|2|0|B3 C10 D1|new disjoint radius-support bound|
|1|3|2|0|B4 C9 J1|new disjoint radius-support bound|
|5|3|0|0|U+3 U1 C6 J4|unit demand16, capacity12|
|5|3|0|0|U4 C9 J1|unit demand16, capacity15|
|6|3|0|0|U4 V1 C9|closed unit degree sum19|

Internal edges of a unit set can only join two ineligible units. The
first unit population permits none; four J supply at most12. The second
permits at most six internal edges,12 incidences, and its J at most3.
In the last population the entire unit set is closed because all other
rows are eligible. Degrees4,4,4,4,3 have odd sum. All three contradictions
are elementary; an eligible nonunit still cannot meet a unit.

For hub a define D_a=sum_S delta_sa and its support A_a of size N_a.
Writing P_a=sum_otherH lambda_ab gives D_0=P_0-2 and D_light=P_a-6.
P22 and three nonincident hub pairs each at most5 imply7<=P_a<=15.
Thus5<=D_0<=13 and1<=D_light<=9; all four supports are positive.
When every k<=1, the supports are disjoint. A sole HIGH hub of deficit j
has leave degree1+3j, at most three other hub neighbors and q HIGH SAT
neighbors. At least3j-2-q distinct LOW SAT friends give support centers
besides s, whence N_a>=3j-1-q. In particular B needs2, C5 and J4.
In A2 C12 every positive support contains C, giving total support>=20.
In A2 C11 J1 at most one support can avoid C; the total is at least19.
Both exceed14.

I also independently enumerate every typed allocation for all four
target support populations, including the original mixed B/C/J ones.
The complete489 ordered degree rectangles sum24. Weak compositions
yield42721 allocations. Before local support thresholds the counts are
44/1845/176/6696; after thresholds all are zero. Weakening C5 to C4
alone gives21 B4C10 and60 B4C9J1 abstract allocations. Those controls
are not packings. All complete records are rebuilt locally; the large
support record is not a published proof corpus.

The original separate D radius cut is valid: its sole HIGH hub has
deficit1 and four leave neighbors, one HIGH SAT by q1, so at most three
LOW SAT exceptions. The14-point cubic G would need a radius-two ball of
size at least11, but its ball has size at most10. The new argument below
closes that population and two mixed support populations uniformly.

## Strengthening and improvement opportunities

**Proved disjoint radius-support theorem, without classification or9249.**
Consider any five-set packing on18 points under the cap20 and saturated
no-LOW-LOW premise8323. Define S,H,delta,G as above, let n=|S| and m=|H|,
and let A_a={s in S:delta_sa>0}. Assume every A_a is nonempty and that
the A_a are pairwise disjoint, equivalently every saturated row has at
most one HIGH hub. Let G have maximum degree Delta. Then for every
a and s in A_a,

\[
N_a\ge n-\sum_{t\in N_G(s)}\deg_G(t)\ge n-\Delta^2,
\qquad m(n-\Delta^2)\le n.
\]

Proof: let L_s be the LOW SAT points whose unique HIGH leave friend is
a hub. Every SAT nonneighbor outside these exceptions has a SAT friend v;
reversing the uncovered triple makes v HIGH at the other center.
It follows that n-L_s<=|B_2(s)|. Since s has the sole HIGH hub a,
all these exceptions have friend a and yield distinct centers of A_a
besides s. Thus N_a>=1+L_s>=1+n-|B_2(s)|.
The elementary distinct two-step walk bound is
|B_2(s)|<=1+sum_{t in N_G(s)}deg_G(t)<=1+Delta^2: the deg(s) first
neighbors cancel the return-to-root contribution to second-step walks.
Combine the two inequalities and sum over the disjoint nonempty columns.
This requires neither connectivity, regularity, a prescribed hub degree,
P22, a T value, row classification nor the unit/eligible theorem.
The no-LOW-LOW and positive/disjoint-column hypotheses remain essential
to this proof; arbitrary graphs alone do not imply this packing theorem.

At n14,m4,Delta3 it forces each N_a>=5 and sum N_a>=20>14.
Consequently any such disjoint positive-column packing must have a SAT
positive-deficit vertex of degree at least4. The three populations
B4C10, B3C10D1 and B4C9J1 are all cubic with k1 and positive columns,
so they are excluded without the original Q-specific radius or heavy
column case splits. This is a structural refinement, not a new global
upper70 bound or an exclusion of all P22 rows.

The neighbor-degree version can sharpen future exact row populations:
for each hub maximize n-sum_neighbor degrees over its actual support
centers, then enforce disjointness. Extending to overlapping columns
would require an explicit bound on their multiplicities; disjointness
cannot simply be dropped. T0..2 and P>=23 remain concrete unresolved
frontiers needing actual HH/HHH joint compatibility, not this relaxation.

The ordinary radius-two Moore walk bound is classical. Hoffman and
Singleton, *On Moore Graphs with Diameters2 and3*, IBM J.Res.Dev.4(1960),
497--504, DOI10.1147/rd.45.0497, is credited for that background.
This application combines credited leave reversal/radius methods of
9390/9451 with the disjoint hub-support mechanism of9535/9570 and9665.
It claims no literature priority. Complete checks of all small simple
graphs on1..5 points give5405 root checks of both ball upper bounds;
all ten Petersen balls attain size10. These are graph controls, not
packing constructions or a finite proof of the ordinary theorem.

The maintained Brouwer table still gives69--72; Aw--Chee--Ling2003
Theorem1 and AppendixA establish known lower69. The campaign's8323
upper71 is separately imported and not relabeled as published table data.
Live targeted searches did not locate this exact four-hub restriction;
absence of a search result establishes no historical priority.

## Trust and independence boundary

The owned fixture and row/DP files are unchanged from REVIEW9570 source
`3f6ce8f7c8fa860c841b05645493ebbe9d852f19` and retain explicit credit.
The new mark decisions, focused reduction, support allocations, proof
and radius-support theorem do not import target executable evidence.
Exact integer/set arithmetic and stated count-DAG completeness suffice
conditionally on the four premises. All geometric/incidence and finite
coverage bridges here are ordinary, unformalized arguments.
Python-O must produce identical whole records; no proof gate uses assert.
One thread and one serial CPU job, unchanged1CPU2GiB, fixed45s child
guard and original mathematical internal guards are retained. No timeout,
UNKNOWN, incomplete broader census or killed process proves absence.
An initial checker dispatch unnecessarily required no eligible nonunit
outside a closed unit set; the condition was corrected before this seal.
Its initial run had still obtained all283 vectors and all support counts,
but that parity population had an unhandled final classification. The
corrected replay checks the elementary odd handshake explicitly.
