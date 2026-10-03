# The prescribed-center cross shell has no 109-edge completion

Actual author **six-books-1**, role **researcher**, 2026-10-03, pass21.

**Status:** exact computer-assisted conditional lemma. The reduction to nine
marked Q-role cases is an ordinary written argument; the final complete
necessary-column enumeration is supplied by the sealed standard-Python
source. The ordinary/source correspondence is unformalized, and independent
review of this new result is pending.

## Exact hypotheses

Let G be a simple graph on22 vertices. Every red edge has at most three
common red neighbors, and every blue edge has at most six common blue
neighbors. Thus a blue pair ij satisfies

    |N(i) intersect N(j)| <= d(i)+d(j)-14.          (1)

Partition the vertices into {u,v,a}, X={X0,...,X5}, SX={SX0,SX1},
SY={SY0,SY1}, T={T0,T1,T2}, and a six-point Q. Assume
N(u)={v,a} union X union SX. Inside this neighborhood the ONLY edges are
av, a-SX0, a-SX1, the cycle

    X0-X4-X3-X1-X2-X5-X0,

and SX0-X3,SX0-X5,SX1-X2,SX1-X4. Assume d(u)=10,d(a)=9 and degree10
for all other nine points of N(u). SX union SY is independent, and T is
independent. The remaining prescribed edges are: v is red to SY union Q
and blue to T; a is red to SY union T and blue to Q;

    SY0:{T1,T2}; SY1:{T0,T1};
    r=0: SX0:{T1,T2}, SX1:{T0,T2};
    r=1: SX0:{T0,T2}, SX1:{T1,T2}.

Both actual r labels are allowed. Prescribe additionally
N(T2) intersect X=C={X0,X1}. The other four SY/T-to-X rows and all
SX/SY/T/X-to-Q and Q-to-Q edges are initially free. The partition fixes
all other pairs. Assume **E(G)=109**. There is no global degree bound on
the eleven vertices outside N[u].

**Conclusion: no such G exists.** This excludes a new, precisely prescribed
109-edge host class. The earlier108-edge theorem9847 does not supply the
new variable-degree bridge. Its T2-forcing dependency9795 is NOT applied
at109; here C is an explicit hypothesis. Nothing here excludes every
unprescribed109-edge cross shell or resolves R(B4,B7).

Write R_z=N(z) intersect X, Q_z=N(z) intersect Q, and

    P={X0,X2,X3}, S={X1,X4,X5},
    H={X0,X1,X3,X5}, K={X0,X1,X2,X4},
    L={X2,X3,X4,X5}.

## Cut excess and variable ranks

The root neighborhood has13 edges and degree sum99. Its cut to
B=SY union T union Q has99-26-10=63 edges. Therefore

    E(G)=86+E(G[B]), so E(G[B])=23.

For b in B, blue u-b has10-d_B(b) common blue neighbors, giving
d_B(b)>=4. The eleven integer excesses epsilon_b=d_B(b)-4 sum to2:
one excess2, or two excesses1. This gives66 labelled distributions.

Red v-SYj has a and all Q_SYj as common pages, so |Q_SYj|<=2.
Its two prescribed T neighbors and d_B(SYj)>=4 give |Q_SYj|>=2.
Hence both SY Q ranks are exactly2 and both SY excesses are zero.
Put e_k=epsilon_Tk. Then

    |Q_T0|=3+e0, |Q_T1|=2+e1, |Q_T2|=3+e2;
    |Q_SX0|=|Q_SX1|=4.

All e_k are nonnegative, with sum at most2. This is not a four-regular
outside graph. Its actual degrees will retain the excesses throughout.

## Ordinary forcing of the other four X rows

For Xi set D_i=N(Xi) intersect(SY union T). Blue a-Xi gives
|D_i|<=4 at centers0,1 and <=3 at leaves2,3,4,5. Their Q ranks are
7-|D_i| at centers and6-|D_i| at leaves. On a red cycle edge Xi-Xj,
the known common red pages are u and D_i intersect D_j. The minimum
intersection of two Q rows is their rank sum minus6, or zero if negative.
Combining this with the red cap gives |D_i union D_j|>=5 on04,05,12,13,
and >=4 on34,25. T2 is absent at both ends of the last two edges, so
each union is maximal. The Q intersection minimum is consequently tight:

    Q_Xi union Q_Xj=Q on every one of the six cycle edges.             (2)

Thus the other four endpoint rows cover the entire C6. For each q,
M(q)={i:q-Xi is blue} is an independent set of C6. Its maximum size
is3, with only P and S as size-three independent sets. Blue v-Xi also
forces R_T0 union R_T1=X. Finally, red v-q gives

    s(q)+h(q)<=3, and d_B(q)=s(q)+t(q)+h(q)=4+epsilon_q,
    so t(q)>=1+epsilon_q,                          (3)

where s,t count red SY,T neighbors and h counts red neighbors within Q.

We use the following elementary union budget. If Q_i union Q_j=Q and
physical spines bound |Q_z intersect Q_i|<=b_i and
|Q_z intersect Q_j|<=b_j, then |Q_z|<=b_i+b_j. Each b is the red cap3,
or (1), minus the known sixteen-point common red neighbors.

Work in r=0 and put A=R_T0,D=R_T1,U=R_SY0,V=R_SY1. If A doubles a
cycle edge incident with X2 or X4, its two red T0-X spines have at least
four known pages in total: one SX1 occurrence, one SY1 occurrence since
V covers the edge, and two cycle occurrences. Their Q allowances total
at most2, contradicting (2) and |Q_T0|>=3. Hence A independently covers
the paths0-4-3 and1-2-5. Their bipartition choices, together with the
remaining cycle edges, give A=P,S,H. The same argument for D on
0-5-2 and1-3-4 has five known pages, using SX0 and both SY covers.
Its Q allowances total at most1, contradicting |Q_T1|>=2. Thus D=P,S,K.
Their union must be X, leaving (P,S),(S,P),(H,K).

For either complementary P/S pair, red SX1-T0 has a and exactly one
own X point as known pages. Its allowance is1; the SX1 Q rank4 forces
the T0 Q rank to be exactly3 and the union Q_SX1 union Q_T0=Q.
Take that own point Xi, namely X2 or X4. Write u_i,v_i for its SY
incidences. Its Q rank is5-u_i-v_i. Red SX1-Xi has known pages u,T0
and allowance1. Red T0-Xi has SX1 and possibly SY1 as known pages,
and allowance2-v_i. The union budget would give

    5-u_i-v_i <= 1+2-v_i, forcing u_i>=2.

Therefore A=H and D=K, even with variable outside degrees.

Red SY1-T0 and SY1-T1 give |V intersect H|,|V intersect K|<=2.
A cycle cover then has V=P,S,L: one center gives a minimum cover;
no center forces all four leaves; two centers cannot fit the allowances.
Red SY0-T1 similarly leaves U=P,H,P+{X5},S,S+{X3},L. Each meets K
in exactly two points, so Q_SY0 intersect Q_T1 is empty.

Blue T1-T2 has five known common red neighbors a,SX0,SY0,X0,X1.
Its ACTUAL degrees are10+e1 and9+e2, so its Q allowance is e1+e2.
Consequently |Q_T1 union Q_T2|>=5, even though the Q rows need not
be disjoint. The rank-two SY0 row avoiding Q_T1 must meet Q_T2.
For U=H, red SY0-T2 is already saturated by a,X0,X1, a contradiction.
For U=L, take q in that intersection. Equation(2) makes q red to a
point of25 and a point of34. On SY0-q these two leaves, v and T2
are four distinct red pages. Thus U=P,S,P+{X5},S+{X3}.

Blue SY0-SY1 has known pages v,a,T1 and U intersect V. Its actual
degrees are6+|U|,6+|V|, yielding |U union V|>=5. The entire remaining
list is

    (P,S),(P,L),(P+5,S),(P+5,L),
    (S,P),(S,L),(S+3,P),(S+3,L).

The X relabeling phi=(01)(24)(35) fixes H,K,C,L and the SX own pairs,
and exchanges the two halves of this list. For U=P,V=L, red T0-X5
has allowance1 and X5 Q rank4. It first forces T0 Q rank3, then a
tight union with Q_X5. Red SY1-T0 has allowance0 and red SY1-X5
allowance1, contradicting the SY1 rank2. For U=P+5 and V=S or L,
X0 and X5 each have Q rank3 and their red cycle spine has saturated
known pages u,SY0,T0, so their Q rows cover Q. X2 has Q rank4 or3.
Blue X0-X2 has allowance2, and red X2-X5 allowance1 or0. Their sum
is one smaller than X2's rank. These union budgets exclude six cases.
Thus (U,V)=(P,S) or(S,P).

The relabeling psi=(23)(45) together with SX0<->SX1 transports the
complete r=0 hypotheses to r=1. It exchanges H,K and fixes P,S,C,L.
Both relabelings are explicit bijections of free completions. They assume
no automorphism of a hypothetical graph and retain all outside excesses.

## Force the excess locations and nine marked Q-role cases

Take the representative r=0,U=P,V=S. If q lies in both SY Q rows,
red SY0-q and SY1-q respectively give

    |M(q) intersect P|>=1+t1+t2;
    |M(q) intersect S|>=1+t0+t1.

By (3), t0+t1+t2>=1, so |M(q)|>=3. Independence in C6 forces M=P
or S, but each misses one of the two positive intersections. Hence the
two rank-two SY Q rows are disjoint.

Both red SY-T1 spines are saturated, so Q_T1 avoids those four points.
Its rank is at most2, forcing e1=0. Red T0-X5 has two known pages and
X5 Q rank4, forcing its rank at most3 and e0=0. Red SXj-T2 has the
known page a and SX rank4; its allowance2 forces T2 rank at most4.
Thus e2=0 or1. The two alternatives are:

| Type | T Q ranks | Sum of Q excesses | Internal Q edges |
|---|---|---:|---:|
| I |3,2,3|2|7|
| II |3,2,4|1|6|

The internal edge count is derived, not an enumeration premise: B has
four SY-T edges, four SY-Q edges and8 or9 T-Q edges, totaling23.

Label Q as A0,A1,B0,B1,C0,C1, with SY0={A0,A1},SY1={B0,B1},
T1={C0,C1}. The saturated red SY1-T0 spine prohibits both B points
from T0. Equation(3) then puts both in T2. Red SY0-T2 allows at most
one A point; blue T1-T2 allows at most0 or1 C point.

In typeI, relabel so T2={A1,B0,B1}. Equation(3) puts A0 in T0, which
contains two of A1,C0,C1. Free C labels give two patterns. No Q point
has all three T neighbors, so an excess2 is impossible by(3); the two
excess1 points must be the two roles having at least two T neighbors.

In typeII, relabel so T2={A1,B0,B1,C0}. Again A0 belongs to T0.
There are three choices for its other two points, and its unique Q
excess1 is at a role with at least two T neighbors. This gives exactly:

| Case | T0 Q row | T2 Q row | Q excess1 locations |
|---|---|---|---|
| I-U |A0,C0,C1|A1,B0,B1|C0,C1|
| I-V |A0,A1,C0|A1,B0,B1|A1,C0|
| II-a4 |A0,C0,C1|A1,B0,B1,C0|C0|
| II-a5 |A0,C0,C1|A1,B0,B1,C0|C1|
| II-b1 |A0,A1,C0|A1,B0,B1,C0|A1|
| II-b4 |A0,A1,C0|A1,B0,B1,C0|C0|
| II-c1 |A0,A1,C1|A1,B0,B1,C0|A1|
| II-c4 |A0,A1,C1|A1,B0,B1,C0|C0|
| II-c5 |A0,A1,C1|A1,B0,B1,C0|C1|

These are free-point labels, not a host-symmetry restriction. The source
also generates every34 labelled role/excess assignment with the three
marked pairs fixed, and compares all their column sets under explicit
pair relabelings with this nine-case catalog. The other two actual r/SY
choices are covered by phi and psi as above.

## Exact terminal prefix computation and completeness bridge

Coordinates are u=0,v=1,a=2,Xi=3+i,SX=9,10,SY=11,12,T=13,14,15,
Q=16,...,21 in the A0,A1,B0,B1,C0,C1 order. For a Q point q its known
SY/T incidences and excess determine

    h(q)=4+epsilon_q-s(q)-t(q);
    d(q)=its red degree into the known16 points + h(q).               (4)

Enumerate all64 missing X sets and all four SX incidences. The ordinary
reduction permits discarding nonindependent M. For a known pair i,j,
put b_i=1(i-q red), b_j=1(j-q red). The minimum Q intersection consistent
with this one column and the two row ranks is

    b_i*b_j + max(0,|Q_i|-b_i+|Q_j|-b_j-5).        (5)

Compare this with the known pair's physical Q allowance. For a known-q
pair, the minimum additional red intersection inside Q is

    max(0,|Q_i|+h(q)-6) on a red i-q;
    max(0,|Q_i|+h(q)-5) on a blue i-q.             (6)

Add the known16-point common red pages and use cap3 or d(i)+d(q)-14.
These are necessary lower bounds on ANY completion, with actual degree(4).
Discarding a column that violates them therefore cannot discard a host.

A separate coordinate-bit checker enumerates all256 X/SX incidence words
WITHOUT the independent-set prefilter, and uses physical blue pages and
their complement-union lower bounds directly. It compares the entire
admissible column sets, not merely counts. The literal known16-point
adjacency, degree and rank data also agree entry by entry.

For each of the nine cases, take the complete Cartesian product of its
six necessary column domains. Enforce missing-X totals(3,3,2,2,2,2),
equivalent to the six actual X Q ranks, and SX row totals(4,4). The exact
result is:

| Case | Column counts in A0,A1,B0,B1,C0,C1 order | Cartesian | X ranks | X/SX ranks |
|---|---|---:|---:|---:|
| I-U |6,2,7,7,3,3|5292|32|4|
| I-V |6,1,7,7,3,3|2646|0|0|
| II-a4 |2,2,7,7,3,2|1176|8|0|
| II-a5 |2,2,7,7,0,2|0|0|0|
| II-b1 |2,1,7,7,0,1|0|0|0|
| II-b4 |2,1,7,7,3,1|294|0|0|
| II-c1 |2,1,7,7,4,2|784|0|0|
| II-c4 |2,1,7,7,1,2|196|0|0|
| II-c5 |2,1,7,7,4,2|784|0|0|

The four I-U prefixes have, up to the independently checked B/C label
swaps, the following missing sets and SX incidences:

    A0: M=35, SX=(1,0); A1: M=02, SX=(0,1);
    B0: M=01, SX=(1,0); B1: M=14, SX=(0,1);
    C0: M=P,  SX=(1,1); C1: M=S,  SX=(1,1).

For these rows Q_X0={A0,B1,C1} and Q_X2={A0,B0,B1,C1}, so their
intersection has3 points. The blue X0-X2 spine already has four known
common RED pages u,X5,SY0,T1, giving total red codegree7. Both actual
degrees are10, so (1) permits only6. Equivalently there are seven actual
common BLUE pages. This contradiction is independent of every Q-to-Q
edge. Swapping the B or C labels gives the same seven-page violation.

The source regenerates all four prefixes, counts all120 known-pair
physical spines, and records every direct seven-blue-page witness. The
complete domains and prefixes are in [RESULTS.json](RESULTS.json). No
Q graph search, solver certificate, imported census, reviewer verdict or
timeout inference is used. This closes every one of the nine cases and,
by the explicit ordinary reductions and transports, the claimed shell.

## Prior work and remaining scope

The108-edge [ordinary broader-shell result9847](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_remaining_ordinary/PROOF.md)
motivated the path-cover and union arguments. The earlier
[prescribed-core ordinary completion9685](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_ordinary_completion/PROOF.md)
introduced the missing-column formulation, and
[T2 forcing9795](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_t2_ordinary/PROOF.md)
explains the previously proved108-edge C branch. All109-edge bridges are
rederived here; neither108-edge theorem is transferred outside its scope.
Fresh [independent REVIEW9876](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-2/cross-remaining-audit/REVIEW.md)
and its [exact-rank refinement](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-2/cross-remaining-audit/PROOF.md)
confirm9847 and remove the edge bound from remaining-row forcing ONLY
with endpoint Q ranks(2,2,3,2,3) explicitly prescribed. That interface
matches typeI after the present rank-necessity proof. TypeII instead has
T2 Q rank4, and the initial109-edge domain can have excess at T0/T1.
It supplies no input-necessity or109-edge terminal verdict. This new
variable-rank proof and completion do not use its verdict or diagnostics.
The parent [specified-leaf result9631](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/leaf_edge_only_candidate/PROOF.md)
was already computer-assisted coverage at E<=108. The exact shell remains
an input, rather than a claimed unrestricted neighborhood classification.

The primary [Lidicky--McKinley--Pfender--Van Overberghe paper](https://arxiv.org/pdf/2407.07285),
Table1, was reopened live on2026-10-02 and still gives22<=R(B4,B7)<=23.
Its [published21-point construction](https://raw.githubusercontent.com/gwen-mckinley/ramsey-books-wheels/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is included verbatim as the compact positive fixture primary21.txt;
the authors use zero for the B4 color. All210 physical spines reproduce
93 red/117 blue edges and maximum pages3/6. This is prior-art validation.
The upper23 flag certificate is not replayed. No exclusive historical
priority, unrestricted22-point exclusion or new Ramsey endpoint is claimed.
