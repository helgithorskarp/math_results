# The full cross shell has no completion, without an edge-count bound

Actual author **six-books-1**, role **researcher**, 2026-10-03, pass22.

**Status:** exact computer-assisted conditional lemma. Ordinary arguments
force all five initially free X rows, the two possible T-Q rank triples,
and an edge cutoff110. The published108 and109 lemmas close those edge
counts; a new complete column computation closes110. The written reduction
and its correspondence with the source are unformalized. Independent review
of this new result is pending.

## Complete hypotheses

Let G be a simple red graph on22 vertices, with blue its complement.
Every red edge has at most three common red neighbors; every blue edge has
at most six common blue neighbors. A blue pair ij therefore satisfies

    |N(i) intersect N(j)| <= d(i)+d(j)-14.                 (1)

Partition the vertices into {u,v,a}, X={X0,...,X5}, SX={SX0,SX1},
SY={SY0,SY1}, T={T0,T1,T2}, and six-point Q. Assume
N(u)={v,a} union X union SX. Inside N(u) the ONLY red edges are
av,a-SX0,a-SX1, the cycle X0-X4-X3-X1-X2-X5-X0, and
SX0-X3,SX0-X5,SX1-X2,SX1-X4. Assume d(u)=10,d(a)=9 and degree10
for every other point of N(u). SX union SY is independent, as is T.
Prescribe v red to SY union Q and blue to T, a red to SY union T and
blue to Q, and these exact endpoint rows:

    SY0:{T1,T2}; SY1:{T0,T1};
    r=0: SX0:{T1,T2}, SX1:{T0,T2};
    r=1: SX0:{T0,T2}, SX1:{T1,T2}.

Both actual r choices are allowed. **All five SY/T-to-X rows and all
SX/SY/T/X-to-Q and Q-to-Q edges are free.** All other pairs are fixed by
the partition. There is **no edge-count assumption**, no prescribed T2-X
row, and no global degree floor outside N[u].

**Conclusion: no such G exists.** The explicit shell remains a hypothesis;
this is not a classification of every22-point Ramsey graph.

Write R_z=N(z) intersect X and Q_z=N(z) intersect Q, and put

    C={X0,X1}, P={X0,X2,X3}, S={X1,X4,X5},
    H={X0,X1,X3,X5}, K={X0,X1,X2,X4}, L={X2,X3,X4,X5}.

## Local degree and rank bounds

The root neighborhood has13 edges and degree sum99. Its cut to
B=SY union T union Q has99-26-10=63 edges. Thus

    E(G)=86+E(G[B]).                                      (2)

For b in B, blue u-b has10-d_B(b) common blue neighbors. Hence
d_B(b)>=4 and E(G)>=108. Write epsilon_b=d_B(b)-4>=0, without any
upper bound on the sum. Red v-SYj has a and Q_SYj as red pages, so
|Q_SYj|<=2. Its two prescribed T neighbors and d_B>=4 give equality.
The prescribed SY/T neighbors likewise give

    |Q_T0|>=3, |Q_T1|>=2, |Q_T2|>=3;
    |Q_SX0|=|Q_SX1|=4.                                  (3)

Each Ti has a red SX partner, with a as a common red page. Consequently
1+max(0,4+|Q_Ti|-6)<=3 and |Q_Ti|<=4. The only necessary rank triples
are {3,4} x {2,3,4} x {3,4}; no edge-count input is used.

For Xi let D_i=N(Xi) intersect(SY union T). Blue a-Xi has u, D_i and,
at a leaf, its own SX point as common red pages. Its cap(1) is five.
Therefore |D_i|<=4 at centers0,1 and <=3 at leaves2,3,4,5. The Q ranks
are7-|D_i| at centers and6-|D_i| at leaves, always at least three.

On mixed cycle edges04,05,12,13 the known red pages are u and
D_i intersect D_j. The minimum Q intersection is the rank sum minus6.
The red cap implies |D_i union D_j|>=5, hence it is the whole five-point
endpoint set. The rank bound is then tight:

    Q_Xi union Q_Xj=Q on04,05,12,13.                      (4)

Each of all five endpoint X rows covers this four-edge forest. We will use
the union budget: if Q_i union Q_j=Q and physical spines give Q-overlap
allowances b_i,b_j against z, then

    |Q_z|<=b_i+b_j.                                      (5)

Each allowance is cap3 or(1), minus known red common pages among the
sixteen points outside Q.

For q in Q let s,t,h count its red neighbors in SY,T,Q. Red v-q gives
s+h<=3; d_B(q)=s+t+h=4+epsilon_q then gives

    t(q)>=1+epsilon_q>=1.                                (6)

## The unprescribed T2 row: ordinary exclusion of P/S

Red SXj-T2 has a and the intersection of R_T2 with its own pair
{X3,X5} or {X2,X4} as known pages. Its rank inequality is

    |Q_T2|+|R_T2 intersect OWN_j|<=4.                    (7)

At rank four there are no leaves, so the mixed cover forces R_T2=C.
At rank three each own pair contributes at most one leaf. A mixed cover
with only X0 is P, with only X1 is S; with neither center it would need
all four leaves, violating(7). Both centers permit C plus at most one
point from each own pair: C and eight proper supersets.

For a proper C superset choose an included leaf Xi and its own SXj.
SXj-T2 has Q allowance one and ranks4,3, forcing a tight union. Red
SXj-Xi already has u,T2 as pages; red T2-Xi has SXj and Xi's adjacent
center as pages. Both allowances are at most one, contradicting(5) and
|Q_Xi|>=3. Only C,P,S remain.

The relabeling phi=(01)(24)(35) on X exchanges P,S, fixes C,H,K,L and
the two SX own pairs, preserving the full free shell. Psi=(23)(45) on X
with SX0<->SX1 takes r=0 to r=1 and exchanges H,K while fixing
P,S,C,L. These are bijections of free completions; no host automorphism
is assumed. It suffices to exclude r=0,R_T2=P. Equation(7) gives T2
rank3 and tight Q unions with both SX rows.

At X2 let u_i,v_i,alpha_i,beta_i be the SY0,SY1,T0,T1 incidences.
Its Q rank is5-u_i-v_i-alpha_i-beta_i. The SX1-X2 Q allowance is
1-alpha_i and T2-X2 allowance2-u_i. Their union budget forces
v_i+beta_i>=2, so both are one; blue a-X2 then gives u_i=alpha_i=0.
At X3 the same argument exchanges T0,T1. Therefore

    D_2={SY1,T1,T2}, D_3={SY1,T0,T2}, Q ranks3,3.       (8)

This calculation does not prescribe T0/T1 center membership. Red SY1-T2
is saturated by a,X2,X3: SY1-X0 is blue and Q_SY1 avoids Q_T2. The
mixed cover now gives R_SY1=L or L+{X1}. Both T0,T1 contain X1 by
their respective edges12,13 and(8). If one omitted X0, edges04,05
would force X4,X5 as well. Its forced P leaf then gives three points
in R_SY1 plus a on red SY1-Ti, impossible. Thus both contain C.

Choose q in rank-two Q_SY1, outside Q_T2. Both SX points are red to
q by the tight unions. Let c,ell be its center/leaf counts and beta
indicate R_SY1=L+{X1}. The actual degree is3+c+ell+s+t+h, with the
three fixed known neighbors v,SX0,SX1; here t counts T0,T1 and s>=1.
Equation(6) gives t>=1. Red SY1-q bounds
1+t+ell+beta*1(q-X1 red)<=3. Since s+h<=3,

    d(q)<=8+c-beta*1(q-X1 red)<=10.

Blue a-q has3+s+t common red pages and cap d(q)-5, so
d(q)>=8+s+t>=10. Equality forces c=2,s=t=1,ell=1,h=2,beta=0.
The unique Ti red to q then has four distinct common red pages
X0,X1,its SX partner,SY1. This contradiction excludes P and, by the
two explicit transports, all P/S branches, without an edge count.

The P/S source corroborates every local mixed pair, all eight proper-C
cuts, all64 leaf incidence cells, the entire6144-cell scalar box with its
eight four-page contradictions, and40 variable-rank whole-frame transports.
These are local necessary projections, not actual-host enumeration.

## Ordinary remaining-row forcing for all twelve rank triples

Now T2=C. The cycle-union calculation on34 and25 gives the whole other
four endpoints and tight Q unions there too. Thus all six cycle Q-row
unions equal Q; each remaining endpoint X row covers the whole cycle.
Every M(q)={i:q-Xi blue} is independent in that cycle. It has size at
most three, with only P,S at size three. Physical blue v-Xi has pages
1+s_i+|Q_Xi|, with s_i its SY count. Cap6 requires two T incidences
at each center and one at every leaf, so

    R_T0 union R_T1=X.                                  (9)

Work in r=0, writing A=R_T0,D=R_T1,U=R_SY0,V=R_SY1. If A
doubles a cycle edge incident to own SX1 points X2 or X4, its two
red T0-X spines have at least four known pages in total: one SX1,
one SY1 since V covers the edge, and two cycle occurrences. Their
Q allowances total at most two, contradicting the tight union and
T0 rank>=3. Thus A independently covers paths0-4-3 and1-2-5. Their
bipartition choices are P,S,H,{X2,X4}, the last failing05,13. Similarly
D independently covers0-5-2 and1-3-4: a doubled edge gives five known
pages using SX0,both SY covers and the cycle, contrary to T1 rank>=2.
Its choices are P,S,K. Equation(9) leaves(P,S),(S,P),(H,K).

For a complementary P/S pair red SX1-T0 has allowance one, which
forces T0 rank3 and a tight Q union with rank-four SX1. At its own
point Xi=X2 or X4, write u_i,v_i for its SY incidences. Its Q rank
is5-u_i-v_i, whereas red SX1-Xi allowance one and red T0-Xi allowance
2-v_i force u_i>=2 by(5). Hence A=H,D=K.

Red SY1-T0 and SY1-T1 give |V intersect H|,|V intersect K|<=2.
A full cycle cover has V=P,S,L: no center forces L; a single center
forces a minimum cover P or S; two centers exceed the allowances.
Red SY0-T1 gives U=P,H,P+{X5},S,S+{X3},L. Explicitly, no center
forces L; both centers use the K allowance and force X3,X5; only X0
forces X2,X3, prohibits X4 and allows X5 optionally; only X1 gives
the other two rows. Each U meets K in exactly two points. Thus SY0
and T1 have disjoint Q rows.

Put the T ranks3+e0,2+e1,3+e2, retaining all twelve initial triples.
Blue T1-T2 has five known red pages and ACTUAL degrees10+e1,9+e2,
so its Q allowance is e1+e2. Its Q union has size at least five.
The rank-two SY0 row avoiding T1 must meet T2. For U=H this contradicts
saturated red SY0-T2. For U=L, take q in that intersection: cycle
unions give a red leaf in25 and one in34. The two leaves,v,T2 are
four distinct red pages on SY0-q. Hence U=P,S,P+{X5},S+{X3}.

Blue SY0-SY1 has known pages v,a,T1 and U intersect V, and ACTUAL
degrees6+|U|,6+|V|. Its necessary inequality is |U union V|>=5,
leaving exactly(P,S),(P,L),(P+5,S),(P+5,L) and their phi images.
For U=P,V=L, red T0-X5 has allowance one and X5 rank4, forcing T0
rank3 and a tight Q union. Red SY1-T0 allowance zero and red SY1-X5
allowance one then contradict rank-two SY1. For U=P+5,V=S or L,
X0 and X5 both have rank3 and their cycle spine already has u,SY0,T0
as pages, tightly covering Q. X2 has rank4 or3; blue X0-X2 allowance
two plus red X2-X5 allowance one or zero is one below that rank.
Union budget(5) and phi exclude all six nonterminal choices. Only
(U,V)=(P,S) or(S,P) remain; psi covers both actual r=1 cores.

For representative U=P,V=S, a q red to both SY vertices would satisfy
from the two red SY-q spines

    |M(q) intersect P|>=1+t1+t2;
    |M(q) intersect S|>=1+t0+t1.

Equation(6) makes their sum at least three. Independence forces M=P
or S, each missing a positive intersection: contradiction. The two SY
Q rows are disjoint. Both red SY-T1 spines are saturated, so T1 avoids
their four points and has rank<=2. Red T0-X5 has two known pages and
X5 rank4, forcing T0 rank<=3. Red SX-T2 has its page a and SX rank4,
forcing T2 rank<=4. With(3), the only possible ranks are

    SY ranks2,2; T ranks(3,2,3) or(3,2,4).                (10)

This extends the remaining-row argument in
[lemma9890](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_109_prescribed/PROOF.md).
Its former excess-sum bound was not used in those inequalities; the new
source checks all twelve rank triples, all7776 whole-frame transports and
all120 known allowances per model. No old census or review supplies this
input-necessity bridge.

## Ordinary density cutoff and the108/109 dependencies

Sum s(q)+h(q)<=3 over Q. The two rank-two SY rows give total s=4,
while total h=2E(G[Q]). Thus

    4+2E(G[Q])<=18, so E(G[Q])<=7.                      (11)

B has four prescribed SY-T edges, four SY-Q edges, eight or nine T-Q
edges and the internal Q edges. Consequently its edge count is16+E(Q)
or17+E(Q). Equations(2),(11) give E(G)<=109 in the first rank type
and <=110 in the second. Since E(G)>=108, only108,109,110 are possible.

At108 this is exactly the input of
[ordinary lemma9847](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_remaining_ordinary/PROOF.md),
which excludes the unprescribed shell. At109 the now forced T2=C
gives exactly the input of
[computer-assisted lemma9890](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_109_prescribed/PROOF.md).
Both permit free T-Q/Q-Q edges and no global outside degree floor.
These are explicit theorem dependencies, used only at proven edge counts.

## Complete110 role cover

At110 the second rank type is necessary and E(G[Q])=7. Equality in(11)
forces s(q)+h(q)=3 for every q, so

    epsilon_q=t(q)-1, h(q)=3-s(q).                       (12)

The two disjoint SY Q rows and rank-two T1 row partition Q. Label them
A={A0,A1},Bq={B0,B1},Cq={C0,C1}, respectively. Cq is a Q pair,
distinct from the X set C. A/Bq points have h=2 and Cq points h=3.
T0 has rank3 and T2 rank4. Saturated red SY1-T0 makes T0 avoid Bq;
equation(6) puts both Bq points into T2. Red SY0-T2 has a,X0 as known
pages, allowing at most one A point in T2. Blue T1-T2 has five known
red pages and cap six, allowing at most one Cq point. Rank four gives
exactly both Bq, one A and one Cq. Free pair labels normalize
T2={A1,B0,B1,C0}. The remaining A0 belongs to T0 by(6); its other
two points give exactly these cases:

| Case | T0 Q row | Q excesses at A0,A1,B0,B1,C0,C1 |
|---|---|---|
| a |A0,C0,C1|0,0,0,0,2,1|
| b |A0,A1,C0|0,1,0,0,2,0|
| c |A0,A1,C1|0,1,0,0,1,1|

The excesses are derived by(12), summing to three. The source generates
all12 labelled role assignments with the three marked pairs fixed. It
compares their entire catalogue against all4096 pairs of six-bit T0/T2
words, using the physical red SY1-T0,red SY0-T2,blue T1-T2 spines and
the t>=1 requirement. All eight within-pair permutations verify the
three-case cover. All four actual r/ordered-SY cores are retained, giving
48 configurations, without any host-symmetry hypothesis.

## Necessary columns, complete products and finite contradiction

Coordinates are u=0,v=1,a=2,Xi=3+i,SX=9,10,SY=11,12,T=13,14,15,
Q=16,...,21 in A0,A1,B0,B1,C0,C1 order. For q its known SY/T roles
and(12) determine h. Enumerate every missing-X set and all four SX
incidence pairs. The actual degree is its known red-neighbor count plus h.
For a known pair ij and column incidences b_i,b_j, the necessary minimum
Q intersection is

    b_i*b_j+max(0,|Q_i|-b_i+|Q_j|-b_j-5).               (13)

For a known-q pair the minimum extra red pages in Q are
max(0,|Q_i|+h-6) if red and max(0,|Q_i|+h-5) if blue. Add known
common red pages, compare with cap3 or(1) at the ACTUAL degrees, and
reject only necessary violations. Every host's column must survive.

The literal old-label set model uses independent missing sets. A separate
coordinate-bit model scans all256 X/SX incidence words WITHOUT that
prefilter and bounds common BLUE pages directly. Entire column sets,
all120 known allowances and every known adjacency, degree and rank agree.
The two models share assumptions and an author; this is not independent
review or a formal proof.

For each of all12 labelled cases and all four actual cores take the
COMPLETE Cartesian product of its six column domains. Actual X Q ranks
are(3,3,4,4,4,4), or missing totals(3,3,2,2,2,2). One model enforces
missing totals; the other reconstructs each actual red X-Q row and its
rank. Both ENTIRE solution lists are empty in every configuration.
For r=0,SY=(P,S), the canonical compact table is

| Case | Column counts at A0,A1,B0,B1,C0,C1 | Complete product | X-rank solutions |
|---|---|---:|---:|
| a |2,2,7,7,1,2|392|0|
| b |2,1,7,7,1,1|98|0|
| c |2,1,7,7,1,2|196|0|

The source regenerates all48 full column/product records and checks all96
canonical-case/pair-label/core column transports. Twelve semantic data
damages are rejected against the entire physical reference, including
lost roles/cores, altered actual point degrees, lost valid columns,
inserted invalid columns and a fabricated balanced solution. A host would
give a six-column product with the correct X ranks; none exists. No Q-graph
search is needed. No timeout, floating arithmetic, solver result, imported
census or reviewer verdict supplies this contradiction.

This closes110; the exact108/109 dependencies and the ordinary density
cutoff prove the stated shell exclusion for every total edge count.

## Prior work, validation and remaining scope

The dependencies9847 and9890 above are replayed against their entire
original expected records as prior-result validation. Their replays add no
new coverage. Earlier [T2 lemma9795](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_t2_ordinary/PROOF.md)
and [terminal lemma9685](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_ordinary_completion/PROOF.md)
are the prior108 dependencies. Their edge restrictions are not transferred
to the new P/S or variable-rank arguments.
[Review9876](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-2/cross-remaining-audit/REVIEW.md)
checks9847; its verdict covers neither this new lemma nor9890. Its
[fixed-rank refinement](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-2/cross-remaining-audit/PROOF.md)
assumes endpoint Q ranks(2,2,3,2,3), whereas the new proof derives ranks
and retains the additional T2-rank-four case.

The primary [Lidicky--McKinley--Pfender--Van Overberghe paper](https://arxiv.org/pdf/2407.07285),
Table1, was reopened live on2026-10-03 and gives22<=R(B4,B7)<=23.
The authors' [21-point construction](https://raw.githubusercontent.com/gwen-mckinley/ramsey-books-wheels/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is included verbatim as primary21.txt, with zero the B4 red color. The
baseline checks all210 physical spines, reproducing93 red/117 blue edges
and maximum pages3/6. This is known-result validation; the global upper23
flag certificate is not replayed.

The new coverage is the full explicit shell with all five endpoint X rows,
all T-Q and all Q-Q edges initially free, with any total edge count and no
outside global degree floor. The Ramsey endpoint remains22..23. No global
22-point exclusion or exclusive historical priority is claimed. Replacing
the finite109/110 terminals by ordinary arguments would improve proof type,
not close a missing step of this explicitly computer-assisted lemma.
