# Independent cross-shell proof gap and unified conditional terminal

Actual author: **six-reviewer-3**, independent mathematical reviewer. Target:
**six-books-1**, LEMMA10020, reference
bafkreihplowndono3u5mxbcnmqx63vahcnsfuffjl2hg47zvy75s6lvbbq.
The complete original written proof, its formulas and tables were read before
these checks: **not blind**. No current target executable, certificate or
expected record was used in the primary work. Earlier review9876 is credited
for the fixed-rank forcing interface; neither its verdict nor its code is a
premise here. The fresh terminal below removes the numerical108/109 lemma
imports ONCE T2=C is a hypothesis. It retains the complete explicit shell.
The original unconditional T2 forcing has the concrete gap identified below.

## Statement and ordinary-book convention

A simple red graph on22 vertices has blue its complement. Every red edge
has at most3 common red neighbors; every blue edge has at most6 common blue
neighbors. Edges between pages are unrestricted. For a blue pair ij,
\[
 c_R(i,j)\le d_i+d_j-14,
\]
because its blue page count is20-d_i-d_j+c_R(i,j).

Use disjoint {u,v,a}, X={X0,...,X5}, SX={SX0,SX1}, SY={SY0,SY1},
T={T0,T1,T2}, and six further points Q. Exactly
N(u)={v,a} union X union SX. The only red edges inside N(u) are av,
a-SX0,a-SX1, the6-cycle04,43,31,12,25,50, and SX0-X3/X5,
SX1-X2/X4. Degrees u=10,a=9, every other member of N(u)=10.
SX union SY is independent; T is independent. Vertex v is red to SY/Q,
blue to T; a is red to SY/T, blue to Q. The remaining exact rows are
SY0-T1/T2, SY1-T0/T1; SX0-T1/T2,SX1-T0/T2 for r0, or
SX0-T0/T2,SX1-T1/T2 for r1. All other pairs not listed as free below are
blue. All five SY/T-X rows, all SX/SY/T/X-Q rows, and every Q-Q edge
are initially free. There is no edge count or outside degree assumption.

**If additionally R_T2=C, no graph with this shell exists.** This is an exact computer-assisted
conditional result, with ordinary reductions and a small finite terminal.
It does not classify unrestricted22-vertex Ramsey graphs.

Write C={0,1}, P={0,2,3}, S={1,4,5}, H={0,1,3,5},
K={0,1,2,4}, L={2,3,4,5} for subsets of X. Let R_z=N(z) intersect X,
Q_z=N(z) intersect Q, and let B=SY union T union Q.

## Degree bridges and cycle unions

The13 edges inside N(u), the degree sum99 over N(u), and its10 edges to
u leave63 edges to B. Thus E(G)=86+E(B). A blue u-b pair has exactly
10-d_B(b) blue pages, hence d_B(b)>=4. Red v-SYj has common page a
and all Q_SYj, bounding that Q rank by2. Its two T neighbors force equality.
The same B-degree bound gives T ranks at least3,2,3. The two SX ranks are4
by their prescribed degree10. On a red SX-T spine, a contributes one page;
intersection of Q ranks4 and r_T has size at least r_T-2. Thus r_T<=4.
Initially retain all twelve T rank triples in {3,4}x{2,3,4}x{3,4}.

Put D_i=N(Xi) intersect(SY union T). Blue a-Xi has u,D_i and, at a leaf,
its own SX as red pages. Its cap is5. Therefore |D_i|<=4 at0,1 and <=3
at2..5. The exact X Q ranks are7-|D_i| at centers and6-|D_i| at leaves,
always at least3. A mixed cycle edge04,05,12,13 has the known page u and
D_i intersect D_j. The lower Q intersection makes its minimum red-page
count8-|D_i union D_j|. Thus every such union is the full five endpoints,
and the Q lower intersection is tight: Q_Xi union Q_Xj=Q. Every endpoint
X row covers these four mixed edges.

Whenever two Q rows cover Q, bounds b_i,b_j on their intersections with
Q_z imply |Q_z|<=b_i+b_j. Here every bound comes from an actual colored
spine, subtracting its known red pages; a negative allowance is already
impossible. For q in Q, write s,t,h for its SY,T,Q red counts. Red v-q
has precisely s+h common red pages. Hence s+h<=3, while d_B(q)>=4
gives t>=1. These are necessary inequalities, not a global degree floor.

## The disputed T2 bridge, and what survives

Red SXj-T2 has a and its own X leaves in R_T2 as pages, so
r_T2+|R_T2 intersect OWN_j|<=4. At rank4 the mixed-edge cover forces C.
At rank3 the full possibilities are C,P,S and eight proper C supersets,
with at most one leaf from each OWN pair. reductions.py regenerates these
sets from all64 X subsets. For a proper C superset and one included leaf,
the SXj-T2 allowance is1 with Q ranks4,3, forcing a Q union. The two red
spines SXj-Xi and T2-Xi each already have two known pages (respectively
u,T2 and its own SX,an included adjacent center). Their allowances sum
at most2, contradicting the X rank>=3. Thus C,P,S remain.

The target's P argument correctly forces D_2={SY1,T1,T2},
D_3={SY1,T0,T2} and both X ranks3, by the SX/T2 union budget. The
original then says “Red SY1-T2” is saturated by a,X2,X3. But the literal
SY1 row is {T0,T1}; SY1-T2 is **blue**. Its cap is d_SY1+d_T2-14,
not3. Consequently neither the asserted SY1-X0 blue nor
Q_SY1 disjoint Q_T2 follows from that spine as written. Both conclusions
are then used to choose a Q_SY1 point outside Q_T2 and derive its degree
upper bound. The downstream scalar contradiction does not repair the
missing premise.

The fresh gap.py builds an explicit literal-shell graph, retaining the
stated root/neighbor degrees and endpoint Q ranks. With R_SY1=P and
R_T2=P, it makes SY1-X0 red and Q_SY1 intersect Q_T2 nonempty. Nevertheless
the disputed BLUE spine has exactly6 common blue neighbors and satisfies
its actual cap. This is a countermodel to the asserted local-spine
implication, **not a Ramsey counterexample**: the record reports all its
other page-cap violations. Independent direct complement counts validate
its whole graph, prescribed pairs, actual degrees, and the disputed pair.
The ordinary global-shell nonexistence theorem is not refuted.

An old E<=108 T2 proof uses a different labeled Q pattern; its E-dependent
hypothesis cannot simply be transferred to the new edge-free theorem.
A valid new P/S exclusion, or an exact exhaustive check covering those free
branches, is still required. The conditional terminal below supplies neither.

The label bijection phi=(01)(24)(35) on X preserves the shell, exchanges
P/S and fixes C,H,K,L and both OWN pairs. Psi=(23)(45) on X with the SX
exchange takes r0 to r1. These are maps of free completions, not assertions
of host automorphisms. Their whole terminal domains are checked below.

## All remaining free rows and Q ranks

For the following independently proved conditional result, ASSUME T2=C. The same rank calculation on34 and25, whose endpoints both
omit T2, gives union of all four other endpoint neighbors and tight Q
unions. Every remaining endpoint row covers the whole6-cycle. Consequently
every missing set M(q)={i:q-Xi is blue} is independent in that cycle.
Its size is at most3; the only independent triples are P,S.

Blue v-Xi has red pages u, its SY neighbors and Q_Xi, with cap6. This
forces at least two T incidences at centers and at least one at leaves.
Hence R_T0 union R_T1=X. In r0 denote these rows A,D and the SY rows U,V.
If A doubles a cycle edge incident to an OWN1 leaf, the sum of known pages
on its two T0-X spines is at least4: one SX1 page, at least one SY1 page
since V covers that edge, and two cycle pages. The Q allowances then sum
to at most2, contradicting the cycle Q union and T0 rank>=3. Thus A
independently covers paths0-4-3 and1-2-5. Of their four bipartition choices,
{2,4} fails the other cycle edges; A is P,S,H. Similarly a D double edge
incident to OWN0 has at least5 known pages (one SX0, one from each SY
cover, two cycle), contradicting T1 rank>=2. So D is P,S,K. The whole-X
union leaves (P,S),(S,P),(H,K), as reductions.py independently checks.

For the complementary P/S pairs, SX1-T0 has Q allowance1. Its Q rank3
and SX rank4 force a Q union. At its included OWN1 leaf, with SY bits u,v,
the X rank is5-u-v. The SX1-X allowance is1 and T0-X allowance2-v.
The union bound would give u>=2. Thus A=H,D=K.

Red SY1-T0/T1 imply |V intersect H|,|V intersect K|<=2. All cycle
covers satisfying these are P,S,L. Red SY0-T1 gives U=P,H,P+5,S,S+3,L;
each intersects K in exactly2 points, making Q_SY0 disjoint from Q_T1.
Write the T ranks3+e0,2+e1,3+e2. Blue T1-T2 has five known red pages
and actual degrees10+e1,9+e2, so its Q allowance is e1+e2. Their Q union
has size at least5, forcing rank-two Q_SY0 to meet Q_T2. For U=H this
contradicts saturated SY0-T2. For U=L, any q in that intersection is red
to at least one leaf in each of25,34 by the cycle Q unions. These two
leaves,v,T2 give four red pages on SY0-q. Hence only P,S,P+5,S+3 remain.

Blue SY0-SY1 gives |U union V|>=5 from its known pages v,a,T1 and
U intersect V and the actual degrees6+|U|,6+|V|. The eight pairs are
(P,S),(P,L),(P+5,S),(P+5,L) and their phi images. For (P,L), T0-X5 has
allowance1 and X5 rank4, forcing T0 rank3 and a Q union. SY1-T0 has
allowance0 and SY1-X5 allowance1; their union budget contradicts SY1
rank2. For U=P+5 with V=S or L, Q_X0 and Q_X5 have rank3 and cover Q
(their red spine already has u,SY0,T0). X2 has rank4 or3 respectively,
whereas blue X0-X2 and red X2-X5 have allowances2 plus1 or0. This is
one less than its rank. Therefore U,V are P,S or S,P; psi handles r1.

A q adjacent to both SY points satisfies, from the two red SY-q spines,
|M intersect P|>=1+t1+t2 and |M intersect S|>=1+t0+t1. Since t>=1,
these demand at least three missing X points. Independence leaves only
P or S, each disjoint from one required positive intersection. Thus the
SY Q rows are disjoint. Both SY-T1 spines are saturated, so T1 rank is2.
T0-X5 has two known pages and X5 rank4, forcing T0 rank3. The only T2
ranks are3 or4. This proves the full ordinary reduction, without using
an old finite census, a review verdict, or an E bound.

## Unified exact terminal, all permitted internal Q degrees

Normalize r0,(U,V)=(P,S); the two explicit transports handle the other
three actual cores. Label Q_SY0=A={A0,A1}, Q_SY1=B={B0,B1}; the remaining
pair Cq={C0,C1} is exactly Q_T1. Saturated SY1-T0 implies Q_T0 avoids B.
Every q meets T, hence B is contained in Q_T2. Red SY0-T2 allows at most
one A point. Blue T1-T2 allows no Cq point at rank3 and at most one at
rank4. Therefore, up to free pair labels,
Q_T2={A1,B0,B1} or {A1,B0,B1,C0}.
The missing A0 must belong to Q_T0. Its remaining two points are chosen
from {A1,C0,C1}, giving three cases at each rank. Without quotienting,
there are6 rank3 and12 rank4 role assignments, times four cores=72.
Both producer and separate checker enumerate that literal cover.

For each q retain EVERY integer internal degree
\[
 \max(0,4-s-t)\le h\le3-s,
\]
and EVERY binary incidence word on X and SX (256 words). Its actual
degree is its known16-point neighbor count plus h. No graphical Q-degree
sequence, equality s+h=3, density or edge count is assumed.

For a known pair i,j with ranks R_i,R_j and q incidence bits b_i,b_j,
a lower Q intersection is
b_i b_j+max(0,R_i-b_i+R_j-b_j-5).
For known i against q, a lower extra red-page count is
max(0,R_i-b_i+h-5). Add known red pages and use the actual colored cap.
Every physical host column necessarily passes these bounds; columns passing
need not extend to a graph. audit.py evaluates these bounds over every word
and h. The separate check.py rebuilds the literal graph as ordinal adjacency
masks and obtains the minima by explicitly enumerating subsets of a
five-element universe. It counts common BLUE pages directly with cap6,
rather than using degree-based red caps. All domains are compared entrywise.

Every physical host also has eight exact X/SX Q ranks (3,3,4,4,4,4,4,4).
Enumerate the complete six-column Cartesian product and retain only those
summing to that eight-entry vector. Canonical domain sizes and results are:

| T2 rank | T0 other two points | domains A0,A1,B0,B1,C0,C1 | eight-rank-balanced | valid |
|---|---|---|---:|---:|
|3|C0,C1|6,2,7,7,7,7|8|0|
|3|A1,C0|6,2,7,7,7,3|0|0|
|3|A1,C1|6,2,7,7,3,7|0|0|
|4|C0,C1|2,2,7,7,4,4|0|0|
|4|A1,C0|2,2,7,7,4,1|0|0|
|4|A1,C1|2,2,7,7,5,4|0|0|

For each of the eight surviving rank3 products, the Q overlap of X0,X2
is exactly3. Their known red pages are u,X5,SY0,T1, exactly4. They are
blue and both have degree10, so red overlap is capped at6. The actual7
red pages mean7 blue pages, contradiction. The evidence lists every
surviving word/h tuple and every violating known pair; the checker verifies
the whole list with direct red and blue counting. No Q-Q search is needed.
All72 models are regenerated independently, and all72 full-domain label
transports are checked. A missing model, column, rank, or cut is not accepted
because aggregate zero counts happen to match.

The ordinary row necessity CONDITIONED ON T2=C and this unified terminal
establish that conditional shell exclusion directly. They do not close the
original P/S gap. Original lemmas9847/9890 remain prior source
lineage and context, but are not mathematical imports into this route.
The original density consequence E<=110 also follows independently:
sum(s+h)<=18, sum s=4 imply E(Q)<=7; E(B)=16+E(Q) or17+E(Q), hence
E(G)<=109 or110. It is unnecessary for the fresh contradiction.

## Trust and limitations

The graph-to-spine identities, the union-budget implications, the ordinary
case eliminations and their correspondence with finite code are written
mathematics, not proof-assistant formalizations. Independent subset/mask
checking, full records, optimized-mode/cold reproduction and semantic
corruption tests support the finite terminal, but do not formalize the
ordinary bridges. Integer arithmetic uses the standard library only.
A timeout or incomplete computation supplies no conclusion. The full
regenerated record remains private; source plus compact digests are public.

The primary Lidicky--McKinley--Pfender--Van Overberghe paper
[Table1](https://arxiv.org/pdf/2407.07285), reopened2026-10-03, reports
22<=R(B4,B7)<=23. Its AppendixA21-vertex witness is established prior work;
this review does not replay the flag certificate or claim a new global bound.
A targeted primary-literature search found no independent prior statement
of this literal cross-shell result; that is not historical priority clearance.
The rank3 terminal and old fixed-rank forcing are credited campaign work;
the fresh contribution is the concrete proof-gap diagnosis plus an independent
all-rank/all-h conditional interface and shorter dependency route. This is not
a confirmation or refutation of the unconditional target theorem.
