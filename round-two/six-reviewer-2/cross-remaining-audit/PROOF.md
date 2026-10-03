# Independent remaining-row derivation

Actual agent **six-reviewer-2**, role **independent mathematical reviewer**.
Target: LEMMA9847, authored explicitly by six-books-1 (researcher).
The target's complete written argument was exposed before this derivation;
its executable, mathematical record and native checker were not opened.
This is a separate literal graph reconstruction and proof audit, not a blind
discovery and not independence inferred from the shared signing identity.

## Exact conditional statement

Let G be a simple red graph on 22 points. Every red spine has at most three
common red neighbors; every blue spine has at most six common blue neighbors.
Books are ordinary subgraphs: their selected pages need not be independent
in G. For a blue pair xy the equivalent bound is
\[
 |N_G(x)\cap N_G(y)|\le d(x)+d(y)-14.
\]
These are the actual degrees, including all unknown Q incidences.

The disjoint parts are u,v,a; X0,...,X5; SX0,SX1; SY0,SY1;
T0,T1,T2; and a six-point Q. N(u) is exactly v,a,X,SX. Within this
neighborhood the only red edges are av, a-SX0, a-SX1, the six-cycle
04,43,31,12,25,50 on X, and SX0-3, SX0-5, SX1-2, SX1-4.
Degrees are d(u)=10, d(a)=9, and 10 at the other nine neighbors of u.
SX together with SY is independent, and T is independent. Outside N[u],
v is red to SY and Q and blue to T; a is red to SY and T and blue to Q.
SY0 has T neighbors T1,T2, and SY1 has T neighbors T0,T1.
In actual r=0, SX0 has T neighbors T1,T2 and SX1 has T0,T2;
in actual r=1 these two SX rows exchange. The five SY/T-X rows, all
SX/SY/T/X-Q edges, and QQ edges are free; the remaining pairs are fixed
by these literal declarations. Assume E(G)<=108. No degree bound on the
eleven points outside N[u] is added.

Use C={0,1}, P={0,2,3}, S={1,4,5}, H={0,1,3,5},
K={0,1,2,4}, L={2,3,4,5}. We import ordinary lemma9795 solely to get
R_T2=C, with its identical broader hypotheses. The new argument below
forces (R_T0,R_T1)=(H,K) in r0 and (K,H) in r1, and ordered
(R_SY0,R_SY1)=(P,S) or (S,P). These four literal inputs coincide with
ordinary lemma9685; importing that terminal theorem excludes all remaining
Q completions under the original E<=108 hypotheses. Neither peer review
9820 nor 9753 is a mathematical premise, and neither verdict transfers.

## Root cut, actual degrees and cycle coverage

There are 13 edges in N(u), whose degree sum is 99. Its cut to
B=SY union T union Q has 99-26-10=63 edges. Thus E(G)=86+e(B).
A blue u-b spine has exactly 10-d_B(b) common blue neighbors, so every
b in B has d_B(b)>=4. Since |B|=11, E<=108 forces equality and B
four-regularity. The five endpoint Q ranks in order SY0,SY1,T0,T1,T2
are (2,2,3,2,3). Each SX Q rank is 4; Q_v=Q and Q_u=Q_a=empty.

For Xi, put D_i=N(Xi) intersect (SY union T). Its Q rank is 7-|D_i|
at centers 0,1 and 6-|D_i| at leaves 2,3,4,5. Blue a-Xi has known
pages u, its own SX neighbor when Xi is a leaf, and D_i. Its red-codegree
cap is 5. Thus |D_i|<=4 at centers and <=3 at leaves, giving Q rank>=3.

On every cycle spine the known common red neighbors are exactly u and
D_i intersect D_j. The Q subset minimum and red cap give
|D_i union D_j|>=5 on 04,05,12,13 and >=4 on 34,25.
The first four unions exhaust SY union T. With T2=C, the two leaf edges
have no T2 endpoint, so their unions exhaust the other four endpoints.
Consequently every bound is tight and Q_Xi union Q_Xj=Q on all six
cycle edges. All four remaining endpoint X rows are cycle vertex covers;
every Q point misses an independent set in this cycle.

Blue v-Xi has known page u, red SY incidences and its entire Q row.
Substituting the above ranks yields at least two T incidences at centers
and at least one at leaves. Since T2=C, R_T0 union R_T1=X.
At the endpoints, actual degrees are 6 plus their X-row sizes for
SY0,SY1,T0,T1, and 9 for T2. The cycle-cover minimum now implies
degree>=9 for the first four; this is derived rather than assumed.

Whenever Q_i union Q_j=Q, intersection allowances b_i,b_j for a third
row Q_z imply |Q_z|<=b_i+b_j. Each allowance is computed from the
physical colored spine, subtracting its known sixteen-point page list
from cap 3 (red) or d(i)+d(j)-14 (blue). This is the elementary union
budget, not a claim of a new inequality. The stronger overlap-aware
version in review9820 is credited background and is not required here.

## Remaining T rows

Work in r0 and write A=R_T0, D=R_T1, U=R_SY0, V=R_SY1.
Suppose A doubles a cycle edge incident to 2 or 4, SX1's own X pair.
The sum of the two known page counts on T0-X endpoints is at least four:
one SX1 occurrence, one SY1 occurrence because V covers the edge,
and two cycle-neighbor occurrences because both endpoints lie in A.
The Q allowances sum to at most 2, less than |Q_T0|=3, contradicting
the covering Q pair. Thus A covers and is independent on paths 043
and 125. A connected three-point path has precisely two independent
vertex covers, its two bipartition classes. Combining the two paths gives
P,S,H,{2,4}; {2,4} fails cycle edges 05 and 13. Hence A=P,S,H.

For D, use SX0's own pair 3,5 and paths 052,134. On a doubled restricted
edge the two T1-X spines have at least five known-page occurrences: one
SX0, one each SY0,SY1 and two cycle occurrences. The Q allowances sum
to at most 1, less than |Q_T1|=2. This leaves D=P,S,K. The already
proved A union D=X leaves exactly (P,S),(S,P),(H,K).

For (A,D)=(P,S) or (S,P), the red SX1-T0 spine has exactly a and
one own X point as known pages. Q ranks 4 and 3 force their intersection
to be exactly 1, so their union is Q. The own point Xi is 2 for A=P
and 4 for A=S. Write ui,vi for its SY0,SY1 adjacency indicators.
It is red to T0 and blue to T1,T2, giving |Q_Xi|=5-ui-vi.
Red SX1-Xi has known pages u,T0, allowance 1; red T0-Xi has SX1
and, when vi=1, SY1 as pages, allowance 2-vi. The union budget would
require 5-ui-vi<=3-vi, or ui>=2. Both alternatives are excluded.
Therefore A=H,D=K.

## Remaining SY rows

Red SY1-T0 and SY1-T1 have a as a page, hence |V intersect H|,
|V intersect K|<=2. Since H union K=X and their intersection is C,
|V|+|V intersect C|<=4. A cycle cover with no center is L; one with
one center and at most three points is P or S; two centers violate this
bound. Thus V=P,S,L.

Red SY0-T1 similarly gives |U intersect K|<=2. With no centers U=L;
both centers force U=H; center0 alone forces P and allows optional5;
center1 alone forces S and allows optional3. The exact six U rows are
L,H,P,P union{5},S,S union{3}, each intersecting K in exactly two points.
SY0-T1 is saturated by a and these two X pages, so Q_SY0 avoids Q_T1.
The blue T1-T2 known pages are exactly a,SX0,SY0,X0,X1, with actual
degrees 10 and 9, cap 5. Thus Q_T1 avoids Q_T2 as well.
Their respective Q ranks are 2,2,3, forcing |Q_SY0 intersect Q_T2|>=1.
For U=H, red SY0-T2 has a,X0,X1 as pages, which forces that intersection
empty: contradiction. For U=L choose q in this intersection. The covering
Q pairs on cycle edges 25 and 34 supply two distinct leaf pages on the
red SY0-q spine. Together with v and T2 they make four distinct pages:
contradiction. This step assumes no QQ incidence or degree at q.

The four surviving U rows and three V rows must also satisfy the blue
SY0-SY1 spine. It has known pages v,a,T1 and U intersect V; its actual
cap is |U|+|V|-2. Therefore |U union V|>=5, leaving exactly eight:

| U | V |
|---|---|
| P | S or L |
| S | P or L |
| P union{5} | S or L |
| S union{3} | P or L |

Phi=(01)(24)(35) on X fixes C,H,K,L and both SX own pairs and
preserves every fixed shell incidence. It exchanges the two table halves.
For U=P,V=L, red T0-X5 has pages X0,SY1 and Q ranks 3,4, forcing
Q_T0 union Q_X5=Q. Red SY1-T0 has a,X3,X5 as pages, allowance 0;
red SY1-X5 has X2,T0 as pages, allowance 1. Their union budget is 1,
less than |Q_SY1|=2.

For U=P union{5}, V=S or L, the red 05 spine is saturated by u,SY0,T0.
Its two Q ranks are 3,3, hence those Q rows cover Q and are disjoint.
The target row Q_X2 has rank 4 for V=S and 3 for V=L. Blue 02 has
exact pages u,X5,SY0,T1, allowance 2. Red 25 has u,SY0, and SY1
only for V=L, giving allowance 1 or 0. Again the summed allowance is
exactly one smaller than the target rank. Phi excludes the other three
nonterminal cases. Precisely (U,V)=(P,S),(S,P) remain.

## Exact transports, terminal dependency and strengthening

Psi=(23)(45) on X together with SX0/SX1 exchange transports the full
r0 shell to r1, exchanges H,K and fixes P,S,C,L. Both maps fix the
unlabeled Q points; free QQ and all free endpoint-Q incidences transport
bijectively. These are isomorphisms between hypothesis classes, not
automorphisms imposed on each hypothetical G. The code compares fixed
adjacency, all thirty independent endpoint-X edge positions, actual-degree
functions and Q ranks on a complete affine basis. It also compares all
120 colored spine page lists and allowances on 710 complete core records.

The four forced endpoint patterns are exactly ordinary9685's r0/r1
terminal inputs. The root-neighborhood map and all original free Q
incidences coincide; no extra degree assumption or symmetry is introduced.
Ordinary9795 and9685 are the two imported theorems. Their sufficient
existing audits are context, not subjects of a duplicate review.

**Proved interface refinement:** the remaining-four-row forcing statement
also holds with no upper bound on E(G), if R_T2=C and the five endpoint
Q ranks (2,2,3,2,3) are explicitly assumed, with every other literal shell,
root/neighbor degree and ordinary book-cap hypothesis retained. Indeed
the root cut and B four-regularity are used here only to provide those
ranks. Each subsequent global endpoint degree follows from the fixed
sixteen-point graph plus its Q rank. Every subsequent inequality and
transport above is unchanged. No degree at a Q point or QQ incidence is
used in the remaining-row argument. This refinement proves forcing only:
it does not import the E<=108 terminal nonexistence theorem beyond its
scope, force T2 at higher edge count, or assert that higher-edge terminal
completions exist. The exact-rank assumptions need a separate necessity
proof in any broader host class.

All steps remain ordinary mathematics with exact finite corroboration,
not proof-assistant formalization or a standalone finite Ramsey census.
