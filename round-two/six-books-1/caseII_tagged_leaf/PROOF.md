# Excluding the X-repeated leaf sector with actual four-low degree tags

Actual author **six-books-1**, role **researcher**, 2026-10-02.
All campaign agents share a signing identity; signatures do not identify authors.

A **valid graph** is a simple red graph on22 vertices with at most three
common red neighbors at every red edge and at most six common blue neighbors
at every blue pair. Blue is the complement on distinct vertices. The books
are ordinary subgraphs; edges between pages are unrestricted. All degrees below
are red degrees.

**Theorem.** Suppose a valid graph has degree multiset9^4,10^18. Let u be
a degree-ten vertex whose red neighborhood is exactly this labeled graph;
its mark0=a has global degree nine and its other nine points have global
degree ten:

```text
0:1,8,9; 1:0; 2:6,7; 3:4,5; 4:3,7,9;
5:3,6,8; 6:2,5,9; 7:2,4,8; 8:0,5,7; 9:0,4,6.
```

Let v=1, X=N_R(u) minus {v,a}, Y=N_R(v) minus {u,a}, and let T be the
three points outside {u,v,a} union X union Y. Set S_X=N_R(a) intersect X
and S_Y=N_R(a) intersect Y. Then the two S_X points **cannot omit the
same T point** in their red incidence to T.

This is the X-repeated sector, called Case II in
[lemma9197](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/degree9_cycle_saturation/PROOF.md)
and independent
[review9247](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/degree-nine-audit/REVIEW.md).
The new reduction retains all165 possible labeled placements of the three
additional degree-nine vertices. Two different exact enumerations recover
the same208 necessary X interfaces. An ordinary set argument closes every
interface, independently controlled on all18720 labeled SX endpoint frames.
No complete22-point graph enumeration or solver infeasibility is asserted.

The theorem concerns the displayed leaf and the stated global degree
multiset. Other neighborhoods, other multisets, cross-repeated cores,
arbitrary108-edge hosts and the Ramsey endpoint remain outside its scope.
The finite completeness and ordinary mathematics bridges below are explicit
and unformalized; the programs are independent implementations by the same
author, with no independent review verdict asserted here.

## 1. Normalized coordinates and inherited ordinary structure

Use coordinates u,v,a,X0..X5,SX0,SX1,SY0,SY1,T0,T1,T2,Y0..Y5, numbered0..21
in that order. Ordinary X means X0..X5 and ordinary Y means Y0..Y5.
The old neighborhood labels2..7 become X0..X5; labels8,9 become SX0,SX1.
The ordinary X graph is the cycle

```text
X0--X4--X3--X1--X2--X5--X0.
SX0 is red to {X3,X5}; SX1 is red to {X2,X4}.
```

The displayed graph gives d(u)=d(v)=10 and their sole common red page a.
The ordinary pair theorem
[9131](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/single_page_pairs/PROOF.md),
`bafkreiesfsfe44lvytykz4oczwidosjpdxf4g3imjfnw7pxdllkmqsfqwu`, implies
|X|=|Y|=8, |T|=3, |S_X|=|S_Y|=2, a red to all T, S_X union S_Y and
T each red-independent, and each special point red to two T points and
two ordinary points of its own block. The four omissions have multiplicities
2,1,1. These facts do not classify the red neighborhood of v.

For Case II label the common omission of both SX as T0. Label the distinct
SY omissions T1 for SY0 and T2 for SY1. Their red T masks are respectively

```text
SX0:6, SX1:6, SY0:5, SY1:3.
```

Bit t means red to Tt. This is a relabeling of the unnamed T and SY points
covering every Case-II core; no host symmetry assumption removes a case.

The global multiset gives108 edges. The ten degrees in N_R(u) sum to99,
and its local graph has13 edges. Its red cut has99-10-26=63 edges, so
the graph on the11 blue neighbors B_u has108-10-13-63=22 edges. For each
blue ub, its common blue count is10-d_(G[B_u])(b). Thus every B_u local
degree is at least4; its degree sum44 forces **four-regularity**. This
ordinary argument also appears in independent
[review9105](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/leaf-neighbor-audit/REVIEW.md).

Consequently every T has four red neighbors in whole Y. The two SY have
two own ordinary-Y red neighbors each. Whole Y has10 internal edges,
of which four are SY--ordinary-Y edges; ordinary Y has six internal edges.
Each SX has four cross ordinary-Y red neighbors from its degree ten.
In Case II the ordinary-Y row ranks of T0,T1,T2 are **2,3,3**, since their
SY row ranks are2,1,1.

## 2. Actual low tags and exhaustive necessary budgets

The root and its displayed neighborhood already contain only one low
point, a. Three degree-nine points lie in B_u=SY union T union ordinary Y.
Preserve individual binary low flags

```text
l=(l_T0,l_T1,l_T2,l_SY0,l_SY1),  sum(l)<=3.
```

There are26 flag words. For each, choose3-sum(l) of the six ordinary Y
points to be low. The total count is
sum_l binomial(6,3-sum(l))=binomial(11,3)=**165**. The selected X tests
do not use the ordinary-Y low locations. Forgetting those locations is a
necessary overapproximation covering every labeled placement, rather than
an assumption that the locations are equivalent in a full graph.

Let c_i be the red T mask of Xi and put g_i=popcount(c_i). Inside X,
X0,X1 have degree2 and the other four ordinary points have degree3.
The exact blue vXi page count is10-d_(G[X])(Xi)-g_i. Hence

```text
g_i >= M_i,  M=(2,2,1,1,1,1);  k_i=g_i-M_i>=0.
```

The ordinary-X row ranks of T0,T1,T2 are

```text
(5-l_T0,3-l_T1,3-l_T2),  sum(k)=3-l_T0-l_T1-l_T2.
```

Indeed subtract each T's mark edge, its two/zero SX edges and its four
whole-Y edges from its actual degree. An SY cross row in ordinary X has
rank4-l_SY, after subtracting its root edge, mark edge, two T edges and
two own-Y edges.

Put m=sum(l). The nine red neighbors of a have degree sum90-m; their
local graph has13 edges, giving red outside cut55-m and31+m edges on
the twelve blue neighbors B_a=ordinary X union ordinary Y. Each ordinary
block has six internal edges, so the mutual red cut has19+m edges.
The exact blue aXi spine forces local degree at least5 in B_a. Write
beta_i=d_(G[B_a])(Xi)-5>=0. Since Xi has two internal ordinary-X edges,
its cross ordinary-Y row has3+beta_i red points. If s_i counts its SY
red incidences, the actual degree equation yields

```text
s_i+k_i+beta_i=2,  0<=beta_i<=2,  sum(beta)=1+sum(l).
```

All individual degree tags and all possible excess entries are retained.
The Case-I fixed T0 row and the older
[9281 all-full-neighbor reduction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/isolated_leaf_mark/PROOF.md)
are not premises of this calculation.

## 3. Exact X interface enumeration and completeness bridge

Let K be the16 points outside ordinary Y. Its ordinary-Y red row ranks are

```text
u:0, v:6, a:0, Xi:3+beta_i, SX:4, SY:2, T0:2, T1:3, T2:3.
```

All global K degrees are10 except a and the individually flagged SY/T
points, which are9. For a K pair ij, let c_K be its common red count
inside K and let q_i,q_j be its ordinary-Y row ranks. The necessary bound

```text
c_R(i,j) >= c_K+max(0,q_i+q_j-6)
```

is at most3 for a red pair and at most d(i)+d(j)-14 for a blue pair;
the latter follows from c_B=20-d(i)-d(j)+c_R. The producer checks all120
K pairs. The checker instead counts actual common blue and red points
inside K and uses their separate six-point outside minima.

[derive.py](derive.py) starts with all26 actual flag words and all T rows
of the three stated ranks:82425 row choices before lower bounds. It retains
both SX columns6, then enumerates both SY cross rows of their actual ranks
and computes beta. Its early necessary red-spine bounds are

```text
popcount(c_i intersect c_j)<=min(2,k_i+k_j) on each X cycle edge;
popcount(6 intersect c_i)<=min(2,1+k_i) on each SX--own-X edge.
```

For the first, the whole-Y X rows have sizes5-k_i,5-k_j and therefore
common red count at least max(0,2-k_i-k_j); root u is a further common
red page. For the second, the SX whole-Y rank4 gives outside contribution
at least max(0,1-k_i), again with common root u. Ignoring other common
pages weakens each test and cannot lose a valid graph.

[verify.py](verify.py) shares no imported producer code. It starts with
all38416 T column words having the proved minimum ranks, infers the
individual T low flags from their row sizes, and tests literal spines
in the fourteen points excluding SY and ordinary Y, with outside size8.
It independently scans all4096 two-bit SY column words, retains all1225
whose two row ranks are3 or4, and infers both actual SY low flags. It
then imposes sum(l)<=3, computes all outside budgets from literal global
degrees and tests the sixteen-point frame with outside size6. The
fourteen-point pruning is the direct colored intersection bound, independent
of the producer's scalar early cuts. It cannot be stronger than the
corresponding fully specified sixteen-point bound: specifying the two SY
members can only improve each outside lower bound.

Every valid graph maps into each enumerated domain: the coordinate
normalization covers every core; the rank equations cover every actual
tag; and each rejection violates a proved necessary book bound. The two
complete freshly generated sorted domains agree, not merely their counts.
Their common **208** interfaces and all26 flag counts appear in the
14173-byte [EXPECTED.json](EXPECTED.json). The domain SHA256 is
`9da2e8de3b0b2ac4aaca38fab36341f97984f7004afc26fae7eebe4c90062121`.

Every interface has l_T0=1, a stronger actual-tag reduction than the
earlier Case-II cut that at least one of T0,SY0,SY1 is below ten. This
finite strengthening is scoped to the hypotheses here; it is not a
global low-degree theorem.

## 4. Closing112 interfaces by a six-point union obstruction

Let Q be the six ordinary Y points, and let A,B be the cross red rows
of SX0,SX1 in Q. Each has size4. The blue SX0SX1 pair has global
degrees10,10 and already has the four common red pages u,a,T1,T2.
Thus |A intersect B|<=2, while the six-point intersection bound gives
|A intersect B|>=2. Consequently their intersection has size2 and
A union B=Q. Their complements P=Q minus A and R=Q minus B are
disjoint two-sets.

For t=T1 or T2 let W_t be its ordinary-X red row, Z_t its ordinary-Y
red row of size3, and let p_(t,s)=|W_t intersect N_R(SXs) intersect
ordinary X|. The red SXs--t spine already has the common mark a and
these p_(t,s) ordinary-X pages. Hence

```text
|Z_t intersect A|<=2-p_(t,0),
|Z_t intersect B|<=2-p_(t,1).
```

If both p_(t,0),p_(t,1) are positive, the three-set Z_t intersects each
four-set in at most one point. It must contain both disjoint two-set
complements P and R, which requires four points. This is impossible.
Exactly112 of the208 interfaces have this obstruction for at least
one T endpoint. This argument allows either endpoint degree9 or10.

## 5. Closing the remaining96 by the blue T1T2 spine

The other96 interfaces satisfy the following literal facts, independently
checked for every entry rather than assumed from a symmetry class:

```text
l_T1=l_T2=0;
each W_t has size3 and contains {X0,X1};
each overlap pair (p_(t,0),p_(t,1)) is (1,0) or (0,1).
```

Since the four other ordinary X points are partitioned by the two SX
own red pairs, each W_t is {X0,X1} together with one point from one of
those own pairs. Its red-spine inequalities have a precise consequence.
If the overlap is(1,0), then Z_t contains P and its third point lies in
R: it has at most one point in A and at most two in B. If the overlap
is(0,1), then Z_t contains R and its third point lies in P. Thus every
Z_t is one of the forms

```text
P union {r}, r in R;  or  R union {p}, p in P.
```

Any two such three-sets intersect in at least two points. They share
the same two-set if their forms agree; if their forms differ, the two
selected third points belong to the intersection. T1,T2 therefore have
at least seven common red neighbors: a, SX0,SX1, X0,X1, and at least
two ordinary Y points. Both endpoints have global degree ten and are
blue to one another, so

```text
c_B(T1,T2)=20-10-10+c_R(T1,T2)>=7,
```

contradicting the blue cap6. Equivalently u,v,T0 are common blue pages,
along with at least two ordinary X and at least two ordinary Y pages.
No ordinary X--Y or ordinary-Y internal edge can change either T endpoint
row. This closes all96 interfaces and proves the theorem.

## 6. Exhaustive finish controls and trust boundary

There are90 ordered four-set pairs A,B on Q with intersection size2.
For each of208 X interfaces, the producer checks all90 pairs and every
pair of three-set choices Z_T1,Z_T2 satisfying the four selected red
spine caps. None satisfies the blue T1T2 cap. The independent checker
instead builds the actual complete22-point endpoint neighborhoods of
both SX and T1,T2, scans all225 initial four-set pairs and accepts exactly
90 by the literal blue SX0SX1 page count. It checks every possible pair
of compatible T three-sets by literal red intersections and common blue
pages. All**18720** accepted SX endpoint frames have zero compatible T
row pairs. Only these endpoint neighborhoods are completed; the frames
are necessary domains, not valid host graphs.

Both normal and optimized Python modes generate the same entire canonical
record, whose SHA256 including its final newline is
`6272bd2638d39457faf9e685c2f4d5c94f2c3da7eaacd9b224d6d5542a313612`.
The independent checker's self-test also checks4096 six-point subset
pairs against both colored outside minima, verifies the frozen certificate,
and rejects14 altered scope/coverage/domain/finish/JSON controls. Deleted,
duplicated or changed domain rows are tested with their hash repaired.

The ordinary pair theorem9131 is an inherited mathematical premise. The
four-regularity, actual degree budgets, finite-domain completeness, omitted
ordinary-Y tag coverage and final set argument are written ordinary bridges.
None is machine-formalized. No solver, floating point, external generated
corpus or graph-search timeout establishes the conclusion. Exact commands,
versions and measurements are in [README.md](README.md) and
[provenance.json](provenance.json); independent review remains pending.

## 7. Relation to the complementary leaf sector and primary baseline

The complementary Y-repeated exclusion is
[lemma9327](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/caseI_tagged_leaf/PROOF.md),
`bafkreihma2u2sz5wqvg5h6k43gn6v7jiy2266kox56mvvwzn7m5nzpjitm`.
It is not a premise of the present theorem. Combining the two stated
theorems in the same degree model forces the repeated omission to involve
one SX and one SY. Of the36 labeled omission cores from9131, this leaves
the24 cross-repeated cores. This corollary depends on9327 in addition to
the present theorem and preserves its stated mathematical trust boundary.

Concurrent
[Book3 low-edge and equality-three work](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/three-root-incidence108/PROOF.md)
forces at least four one-nine roots when the low set has an edge, under
the additional hypothesis that every degree-ten vertex has a low red
neighbor. Its ordinary theorem and15-profile necessary incidence census
are a complementary frontier. The complete source was read; neither it
nor its executable is a premise here, and its new claims have no independent
verdict asserted by this contribution.

The best located primary published interval remains22<=R(B4,B7)<=23 in
Table1 of
[Lidicky--McKinley--Pfender--VanOverberghe](https://arxiv.org/pdf/2407.07285).
This contribution is a scoped structural exclusion, not a Ramsey endpoint
resolution or an assertion that no other unpublished result exists.
The primary
[21-point witness](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was fetched again and exactly reproduced:93 red edges,117 blue pairs,
maximum red/blue page counts3/6. Its raw SHA256 is
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
That replay validates the incumbent and definitions; it is not new research.
[baseline.py](baseline.py) supplies the standalone literal replay and
does not supply any input to the two new interface algorithms. The published
upper23 flag certificate was not replayed.
