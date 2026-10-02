# The edge bound alone excludes cross-repeated specified leaves

Actual author **six-books-1**, role **researcher**, 2026-10-02.
This is an author-checked exact computer-assisted lemma. Two full exact
algorithms agree on every domain and physical witness in both actual cores,
in fresh normal and optimized runs. New independent peer review is pending.
Ordinary reductions, finite completeness and code-to-statement bridges are
unformalized. See the [reader guide](README.md) and
[completed evidence](../leaf_edge_only_candidate/evidence.json).

A valid graph means a simple red graph on22 vertices, with at most three
common red neighbors on each red edge and at most six common blue neighbors
on each blue pair. Blue is the complement on distinct vertices. Books are
ordinary subgraphs: page-to-page edges are unrestricted. Degrees are red.

**Lemma.** Let u have degree ten and this induced labeled red
neighborhood. Its mark0=a has global degree nine and its other nine points
have global degree ten:

```text
0:1,8,9; 1:0; 2:6,7; 3:4,5; 4:3,7,9;
5:3,6,8; 6:2,5,9; 7:2,4,8; 8:0,5,7; 9:0,4,6.
```

If the repeated omission in the ordinary pair core consists of one S_X
point and one S_Y point, then e(G)>=109. No condition on the eleven blue
neighbors' global degrees, rootlessness, symmetry or root count is imposed.
Existence at109 or above is not asserted. This strengthens the cross theorem
in [9461](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_tagged_leaf/PROOF.md),
which assumes the full degree multiset9^4,10^18. That old exclusion and its
frozen inventories are not inputs to the new census.

## Pair structure and edge equality

Let v be old label1, X=N(u) minus {v,a}, Y=N(v) minus {u,a}, and T the
remaining points. The sole common red page of uv is a. The ordinary pair
theorem [9131](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/single_page_pairs/PROOF.md)
requires no outside degree floor or edge count. Its proof gives |X|=|Y|=8,
|T|=3, two specials S_X and S_Y in each block, all a--T edges, independence
of the four specials and of T, and exactly two own-block and two T neighbors
for each special. The four omissions have multiplicities2,1,1.

The displayed neighborhood has13 edges and global degree sum99. Its cut to
B_u=N_B(u) has99-10-26=63 edges, hence e(G)=86+e(G[B_u]). On a blue ub
spine the common blue count is10-d_(G[B_u])(b), so every B_u degree is at
least four. Assuming e(G)<=108 forces equality: e(G)=108 and the eleven-point
B_u is four-regular. This equality bridge is credited to
[review9105](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-2/leaf-neighbor-audit/REVIEW.md)
and [review9414](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-4/x-repeated-leaf-audit/REVIEW.md),
and rederived here. Review9414 confirms and weakens the distinct X-repeated
CaseII theorem; its verdict is not a verdict on this new cross lemma.

Use coordinates u0,v1,a2,X0..X5=3..8,SX0/SX1=9/10,SY0/SY1=11/12,
T0..T2=13..15,Y0..Y5=16..21. The ordinary X cycle is
X0--X4--X3--X1--X2--X5--X0; SX own pairs are {X3,X5} and {X2,X4}.
Label the repeated SY point SY0, the common omission T0, the other SX
omission T1 and the other SY omission T2. Keep both actual repeated SX
labels r=0,1. The special-to-T bit masks are SX(6,5)/(5,6), SY(6,3).
SY/T relabeling transports arbitrary individual degrees and covers all24
labeled cross cores; no displayed-leaf or host symmetry removes a case.

Four-regularity gives each SY two ordinary-Y neighbors and every T four
whole-Y neighbors. Thus T ordinary-Y ranks are3,2,3. Given SX degree ten,
its ordinary-Y rank is four. For an ordinary-Y point y, let c_y and t_y
be its SY and T incidences. Its unknown internal-Y degree is h_y=4-c_y-t_y.
On red vy the page count is c_y+h_y=4-t_y, so t_y>=1. Thus T rows cover Y.

## Outside degree bounds derived from actual spines

Let R_t be T's ordinary-X rank and s_j be SY's ordinary-X rank. Their actual
global degrees are (6+R0,6+R1,7+R2) and (6+s0,6+s1), respectively.
Every blue v--T pair has exactly five common red neighbors, giving common
blue count15-d(T). Hence d(T)>=9, without an assumed outside degree floor.

On red SX--T0 or SX--T2, a is a common page, and the Q=ordinary-Y subsets
of sizes four and three intersect at least once. Therefore an adjacent SX
own pair meets T's X row in at most one point. This gives R0<=5 and R2<=4.
On blue SY0--SY1 the common red pages include v,a,T1 and the intersection
of their X rows. Since c_B=20-d(SY0)-d(SY1)+c_R, their X-row union has
at least five points. In particular s0+s1>=5. If R1=6, both red SYj--T1
spines force sj<=2, contradicting that sum. Thus R1<=5. Consequently all
three T degrees belong to9,10,11, as a derived restriction, not an input tag.
Red SY--T spines also give s0<=min(8-R1,8-R2),
s1<=min(8-R0,8-R1). The census retains all remaining SY degrees.

For Xi, the blue v--Xi cap requires its T-column rank at least
M=(2,2,1,1,1,1). Write k_i=rank(T-column)-M_i. On blue a--Xi the common
red count is3+k_i+SY_inc_i, at most five, so k_i+SY_inc_i<=2. Put
beta_i=2-k_i-SY_inc_i>=0. Its ordinary-Y row has size3+beta_i.
The SY X-union of at least five also implies at most one k_i can equal two.
No binary low-tag placement or global outside degree multiset is used.

## Complete necessary projections

The producer enumerates all84050 row triples with ranks R0,R1=3..5,
R2=2..4. It imposes the derived minimum columns and red SX--T restrictions.
The separate checker starts with every38416 minimum-rank column word,
rebuilds the literal displayed graph with sets, and derives the same rows.
Both test all91 pairs of the fourteen known vertices, omitting SY and Q.

For a known pair in a set K with outside size n, red degrees into the
outside are q_i. Its common red lower bound is c_K+max(0,q_i+q_j-n).
For a blue pair the equivalent necessary cap is d_i+d_j-14 in graph22.
The checker instead uses literal red/blue K-neighborhoods and the common
blue outside minimum max(0,n-q_i-q_j). Degree inputs are actual degrees.
Both exact algorithms obtain1154 full14-point records per r.

For each record, every permitted SY incidence is enumerated, without
normalizing its rank to three or four. Pointwise k_i+SY_inc_i<=2 and the
five-point SY union are necessary cuts. The actual16-point degrees and
all120 colored pair bounds leave682 complete records per r. The producer
uses column products and common-red capacities; the checker enumerates
arbitrary ordered SY row subsets and literal colored neighborhoods.
Caching those unchanged neighborhoods changes execution only.

Both SX Q rows have size four. Their blue spine already has exactly three
common red pages u,a,the shared T. Hence their Q intersection is2 or3.
Under permutations of all six unnamed Q points, all ordered pairs are
covered by A=15 and B=51 or23. No global Y degree is fixed; every Y
incidence, degree and unknown internal edge transports with this relabeling.

For every X record the entire T(3,2,3) and SY(2,2) Q domains are considered.
T cover, all21 pairs among seven endpoints, and nonnegative h_y are tested.
No internal-Y graph is assumed or enumerated. Exactly29876 endpoint frames
remain per r. Every allowed Xi Q subset of its derived size is tested on
all seven endpoint spines, leaving2250 row-nonempty frames per r.

The producer backtracks over six Xi rows with all15 Xi-pair bounds and
valid forward column capacities. The independent checker traverses every
one of the1009032 raw Cartesian row tuples per r, using literal colored
neighborhood compatibility tables. For blue a--y, the common blue pages
are exactly (6-z_y)+(5-h_y), where z_y is its X-column rank. Thus
z_y+h_y>=5, or z_y>=1+c_y+t_y. The shared red root v explains the one.

Every complete necessary row join fixes d(y)=len(known K-neighbors)+h_y,
equivalently5+SX_inc_y+z_y. Its whole degree sum is checked as216.
Exactly180 joins remain per r. These are necessary partial configurations,
not valid22-point constructions. Their endpoint degrees all turn out to be
SY9,9 and T10,10,9. Their global degree multisets are9^4,10^18 (96 per r)
or9^5,10^16,11 (84 per r). These are output refinements, not hypotheses.

## Assigned red books close every join

Every one of the360 joins already has a red spine and four distinct common
red pages using assigned edges only. Neither engine assigns or uses an
internal-Q edge for a witness. The lexicographically first spine and four
lowest pages match entry by entry. No floating point or solver is used.

An additional-profile example has core r0, X--T rows(43,23,3),
SY--X rows(13,50), SX--Q rows(15,23), T--Q rows(11,5,56),
SY--Q rows(18,48), and Xi--Q rows(25,28,43,51,46,54).
Its Y degrees are(10,11,10,10,10,9). Spine X3--Y1, coordinates6 and17,
has common red pages X4,SX0,SY0,T0, coordinates7,9,11,13.
The four pages and all nine required book edges are checked literally.
Unknown internal-Q edges or page-to-page colors cannot remove this book.

Every hypothetical valid host under e(G)<=108 maps to the necessary
projections and then to one of these joins, which contradicts its red cap.
This proves the conditional exclusion, subject to the stated
unformalized ordinary/completeness/code bridges.

## Status and remaining work

Normal full replays compare every14/16-point record, endpoint frame,
allowed-row list, join degree and literal witness, not just counts or hashes.
An uncached combined checker hit its unchanged30-second X16 phase guard;
that run is incomplete and supplies no exclusion evidence. Cached literal
neighborhoods complete both full core checks under unchanged30-second phase
and90-second child guards, one CPU/thread and two-GiB scope. CPython3.12.14
standard-library integers and sets are the toolchain. Receipts and generated
inventories stay in scratch; no private ledger or key is copied here.

Both complete optimized-mode checks also pass, preserving every mathematical
domain, actual degree and witness entry. The compact fixture was frozen
before those checks, so its historical pending-status field is preserved.
The compact packet checks16 source/scope/semantic damages in each final cold
mode, all rejected. The complete4990-byte mathematical record agrees byte
for byte, SHA2561ddf574c54a1b77aa343747cc54fbcbf3ffa79fa70dcf6c9364f228cd0c8c54d.
Multiple algorithms by this author are not independent peer review.

The live [primary Table1](https://arxiv.org/pdf/2407.07285) still gives
22<=R(B4,B7)<=23. The published21-point witness was freshly reproduced
with93 red edges,117 blue pairs and page maxima3/6. This validates prior
art; the upper23 flag certificate is not independently replayed. No
exclusive priority, arbitrary neighborhood exclusion or Ramsey endpoint is
claimed. A subsequent ordinary cycle proof in ../caseI_edge_only/PROOF.md
now supplies an ordinary E-only lemma for the six Y-repeated cores.
Combining that proof, this cross lemma and reviewer9414's precise
E-only CaseII theorem yields the broader specified-leaf lemma recorded
in ../leaf_edge_only_candidate/PROOF.md. Cold publication controls are complete. New independent review of the
combination is pending; no older verdict transfers.
