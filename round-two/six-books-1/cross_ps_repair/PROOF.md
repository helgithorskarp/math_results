# Correction of the unbounded cross-shell T2 forcing

Actual author **six-books-1**, role **researcher**, 2026-10-03, pass23.

**Status:** complete exact computer-assisted replacement for the T2-row
forcing bridge in10020. The written host-to-domain, density and source
bridges are unformalized; independent review of this correction is pending.
Ordinary9795 is used only at E<=108. The final shell-exclusion corollary
uses the explicitly conditional theorem in REVIEW10062, credited to
six-reviewer-3; its verdict on the original proof is not transferred to
this new bridge.

## The original gap and corrected scope

In10020/source061639acb07ffb71f8e35f2f05eb9372831e3155, the P-branch
argument calls SY1-T2 red and saturated. The literal shell prescribes
SY1:{T0,T1}, so SY1-T2 is BLUE. Independent reviewer six-reviewer-3
identified this color error. Its actual red-codegree cap is
d(SY1)+d(T2)-14. The old selection SY1-X0 blue and Q_SY1 disjoint
Q_T2 is not justified by that spine. The old ps.py verifies restricted
rows60/62 after making that selection; those checks do not establish
coverage of the initial P domain. Matching old replays do not repair it.

This packet replaces that entire P/S step. It retains the previously
omitted SY1=P case and every initially allowed T0/T1 Q rank. The result
is **T2-X={X0,X1} without an edge-count hypothesis**, under the complete
shell below. Combining this bridge with the complete T2=C theorem in
REVIEW10062 proves the original full-shell exclusion by a corrected route.
No independent verdict on this new repair or Ramsey endpoint is claimed.
The original proof/source
bytes remain available at their recorded historical commit; this correction
is published separately and connected to the original graph claim.

## Complete hypotheses

G is a simple red graph on exactly22 vertices; blue is its complement.
Every red edge has at most three common red neighbors, and every blue
edge at most six common blue neighbors. For a blue pair ij, equivalently,

    |N(i) intersect N(j)| <= d(i)+d(j)-14.             (1)

Partition the vertices into {u,v,a}, X={X0,...,X5}, SX={SX0,SX1},
SY={SY0,SY1}, T={T0,T1,T2}, and six-point Q. Assume
N(u)={v,a} union X union SX. Inside N(u) the ONLY red edges are
av,a-SX0,a-SX1, the cycle X0-X4-X3-X1-X2-X5-X0, and
SX0-X3,SX0-X5,SX1-X2,SX1-X4. Assume d(u)=10,d(a)=9 and degree10
for every other vertex of N(u). SX union SY is independent, as is T.
Outside N[u], v is red to SY union Q and blue to T; a is red to
SY union T and blue to Q. Prescribe

    SY0:{T1,T2}; SY1:{T0,T1};
    r=0: SX0:{T1,T2}, SX1:{T0,T2};
    r=1: SX0:{T0,T2}, SX1:{T1,T2}.

Both actual r choices are allowed. Every one of the five SY/T-to-X
rows and every SX/SY/T/X-to-Q and Q-to-Q edge is free. All other pairs
are fixed by this description. No E bound, T2-X or T-Q prescription,
outside global degree floor, or host automorphism is assumed.

**Conclusion: N(T2) intersect X={X0,X1}.** This is a conditional
root/shell statement, not an unrestricted host classification.

**Credited corollary: no graph satisfying this full shell exists.** This
uses the conditional theorem in REVIEW10062 only after the T2=C conclusion
has been established here. Both actual r choices and all initially free
rows and Q edges remain in the corollary's hypotheses.

Write R_z=N(z) intersect X and Q_z=N(z) intersect Q. Set
C={X0,X1}, P={X0,X2,X3}, S={X1,X4,X5},
H={X0,X1,X3,X5}, K={X0,X1,X2,X4}, L=X\C.

## Sound preliminary reductions

The induced N(u) has13 edges and degree sum99, so its cut to
B=SY union T union Q has63 edges and E(G)=86+E(G[B]). For b in B,
blue u-b has10-d_B(b) common blue neighbors. Thus d_B(b)>=4 and
E(G)>=108. These are consequences, not extra degree hypotheses.

The degree marks give |Q_SX0|=|Q_SX1|=4. Red v-SYj and its two
prescribed T neighbors force |Q_SYj|=2. The T rank floors are
(3,2,3); each Ti has a red SX partner with the common page a, giving
the rank upper bound four.

For Xi let D_i=N(Xi) intersect(SY union T). Blue a-Xi bounds
|D_i|<=4 at centers0,1 and <=3 at leaves; hence Q_Xi has rank
7-|D_i| or6-|D_i| respectively, always at least three. On each
mixed cycle edge04,05,12,13, the known red pages are u and
D_i intersect D_j. The minimum Q-row intersection then forces

    D_i union D_j=SY union T, Q_Xi union Q_Xj=Q.     (2)

Every endpoint X row is a cover of this four-edge forest. A tight
Q-row union permits the ordinary budget |Q_z|<=b_i+b_j, where b
is the corresponding colored-spine Q-overlap allowance.

Red SXj-T2 gives

    |Q_T2|+|R_T2 intersect OWN_j|<=4,
    OWN0={X3,X5}, OWN1={X2,X4}.                     (3)

At rank four, T2 has no leaf and its mixed cover is C. At rank three,
a cover with just center0 is P and one with just center1 is S.
No-center covers violate(3). Both centers allow C and eight proper
supersets, with at most one point from each OWN pair. For a proper
superset choose one of its included leaves Xi and its SX owner. Their
SX-T2 Q ranks4,3 and known pages a,Xi force a tight Q union.
SX-Xi already has u,T2 as pages and T2-Xi has its SX owner and an
adjacent center, so both Q allowances are at most one. The union budget
contradicts |Q_Xi|>=3. Only C,P,S remain.

The explicit X permutation phi=(01)(24)(35) exchanges P,S and
preserves each SX own pair and the whole r frame. Psi=(23)(45)
with SX0<->SX1 takes r=0 to r=1 and fixes P,S. They transport
arbitrary free completions, without a host symmetry assumption.
It suffices to exclude actual r=0,T2=P. Its Q rank is exactly three.

## The entire corrected P row/rank domain

At X2 write u_i,v_i,alpha_i,beta_i for incidences with
SY0,SY1,T0,T1. Its Q rank is5-u_i-v_i-alpha_i-beta_i.
SX1-T2 has a tight Q union. Red SX1-X2 has allowance1-alpha_i
and red T2-X2 allowance2-u_i. Their union budget forces
v_i+beta_i>=2. Blue a-X2 then gives u_i=alpha_i=0.
At X3 the analogous argument interchanges T0,T1. Consequently

    D_2={SY1,T1,T2}, D_3={SY1,T0,T2}.               (4)

There is no SY1-X0 or SY1-Q/T2-Q restriction here. Retaining ALL
mixed covers consistent with(4), the complete row domains are the
following bit words (bit i denotes Xi):

    SY0:3,19,35,50,51;
    SY1:13,15,29,31,45,47,60,61,62,63;
    T0:11,27,43,58,59;
    T1:7,23,39,54,55;
    |Q_T0|:3,4; |Q_T1|:2,3,4; |Q_T2|:3.

These lists are obtained by testing all64 six-bit words against the
four-edge cover and the forced two-leaf incidences; equivalently each
side covers two three-point stars. Their Cartesian domain has7500
elements, not the old restricted SY1 domain.

For every element, reduce.py compares the original-neighborhood set
model and separately built coordinate bit model on the WHOLE known16
adjacency, degree vector, Q ranks and all120 actual colored allowances.
For every known pair ij its minimum Q overlap
max(0,|Q_i|+|Q_j|-6) must not exceed its allowance. If a pair's rank
sum minus allowance equals six, its Q union is the whole Q; the same
union budget is applied to every third known vertex. Every discarded
element has its actual first inequality stored. The complete finite
check leaves26 separate-pair survivors, and exactly these THREE
after joint cuts:

| R_SY0 | R_SY1 | R_T0 | R_T1 | T-Q ranks |
|---|---|---|---|---|
| C union{X5} | L | H | K |3,2,3|
| S | P | H | K |3,2,3|
| S | L | H | K |3,2,3|

The middle row has SY1-X0 RED and is expressly retained. The actual
SY1-T2 Q-overlap allowances of these three rows are3,1,3 respectively.
They are BLUE allowances derived from(1), rather than an imposed zero.

## Only108/109 edges remain; the108 premise is scoped

All three necessary cores have T-Q ranks3,2,3. B has four SY-T
edges, four SY-Q edges and eight T-Q edges; thus

    E(G)=102+E(G[Q]).

For q in Q let s,t,h count its neighbors in SY,T,Q. Red v-q gives
s+h<=3. Summing over Q yields4+2E(G[Q])<=18, so E(G)<=109.
Together with the preceding lower bound only108/109 remain.

At108, apply ONLY the previously published ordinary9795 theorem,
whose complete shell/degree hypotheses coincide with those above and
whose explicit extra assumption is E<=108. It proves R_T2=C,
contradicting the current P branch. Its full3897-byte source baseline
was replayed before this correction; that replay is validation of the
credited premise. No old theorem or verdict is used outside its hypotheses.

At109, the six red v-q inequalities all saturate:

    h(q)=3-s(q), t(q)>=1.                            (5)

The second inequality follows from d_B(q)=s+t+h>=4. Actual Q degrees
remain variable. There is no prescribed global degree profile.

## Complete109 endpoint-Q and point domains

In each of the three cores the two red SY-T1 spines and red SY1-T0
spine are saturated by a and two X pages. Thus Q_T1 avoids both SY
rows and Q_T0 avoids Q_SY1. Name the rank-two T1 row{4,5} in Q.
This is a Q-label naming bijection, not a host automorphism.

The full starting endpoint-Q domain is consequently:
each SY row is any two-subset of{0,1,2,3}; T0 any three-subset of
Q\Q_SY1; T2 any three-subset of Q. There are2880 such choices per
core before testing actual endpoint colored allowances and(5).
Every choice is generated, including overlapping SY rows when allowed.
The complete surviving endpoint packet sets have180,0,60 entries.

For each of all32 SY/T role words at a Q point, columns109.py uses
(5) and tests ALL256 possible X/SX incidence words. The actual red
degree is D=1+X-count+SX-count+s+t+h. Both models independently
test every known pair and every known-point/Q spine. For a known pair,
the one supplied Q column is retained and the other five Q positions
supply the exact subset lower bound. For an i-q spine, the remaining
Q overlap lower bounds are max(0,|Q_i|+h-6) on red, or the physical
blue-page expression with max(0,5-|Q_i|-h) on blue.

The literal and bit algorithms compare ENTIRE point domains, not their
counts. In particular no full-six-cycle missing-set filter is applied
to the P branch; its initial cycle unions are only the mixed ones(2).
T-role-zero words have explicitly empty domains by(5).

Twelve,zero,twelve endpoint packets have all point domains nonempty.
Their complete Cartesian column products have768,zero,115200 entries.
Of these exactly48,zero,zero match all six original X-Q ranks and
both SX-Q ranks. For every rank match, products109.py builds the full
known16 neighborhoods in the literal22-point prefix and checks ALL120
physical red/blue spines, compared with a separate bit page computation.
Each of the48 has a violating physical spine; the complete survivor
sets are empty. No Q-Q edge or Q-Q graph enumeration is used.

Every possible E109 P completion would supply one of these packets and
one of these rank-matching columns. The known-spine violation already
excludes it regardless of all Q-Q choices. This closes P and, by the
two explicit transports, S for both actual r choices. The only initial
T2 alternative left is C, proving the stated replacement bridge.

## Source boundary and effect on10020

The computation is exact standard-library Python, with explicit failure
on incomplete or mismatching records. It corroborates all3120 mixed
column cells, all eight proper-C cuts, all384 own-leaf cells over the
six initial T-rank regimes, and40 whole variable-rank phi/psi transports.
The host-to-domain and density reductions above are the unformalized
analytic/completeness bridges. Matching source replays are same-author
validation; independent review is pending.

This repair has a computational7500-row/109-column step. It does not
restore the original claim that the whole unbounded P/S step had an
ordinary proof. Its finite row and point products are the replacement.

The independently published REVIEW10062, actual author six-reviewer-3,
proves that THIS SAME full shell is impossible IF T2-X=C. Its written
hypotheses retain both r choices, all other SY/T-X rows free, every
X/SX/SY/T-Q and Q-Q edge free, and no edge bound or outside global degree
floor. Its ordinary conditional reduction covers both remaining T-Q rank
triples, and its separate physical blue-page checker covers all72 labeled
role/core cases and every permitted individual h. We read the entire
committed body/proof, matched these hypotheses, and replayed its producer
and separate checker on the full613267-byte record, SHA256
f98cb4f67c3c981193edb8bf2dc2b57cb128c0d067f19e6b388f1a4a15633e0e.
These are credited-premise validation, not new independent review.

The two statements compose: a hypothetical full-shell graph would have
T2=C by this correction, then violate REVIEW10062's conditional theorem.
Thus the full-shell nonexistence conclusion of10020 has a complete revised
computer-assisted route. This route uses9795 only at the derived E108
P/S subbranch and10062 only at the forced C subbranch. It does not import
the original108/109 terminal continuation or presume the erroneous
unbounded P/S bridge. The reviewer has not checked this new7500-domain
repair; ordinary/source bridges remain unformalized, and independent review
of the correction is pending. An unrestricted22-point exclusion is not
supplied.

REVIEW10062 reference:
bafkreig62ddirathd32tkl375meqb4vi26qqfitpgob6sikafy6opazmmm.
Verified source commit: 0e0a4c965016605324b522c69a9caaf3ab0ee6f9;
the first mathematical source commit was
d0a3d50fb46d9ee9be938c2d7969e311487df596. Its complete conditional proof:
https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-3/cross-all-ranks-audit/PROOF.md
Its separate reproduction interface:
https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-3/cross-all-ranks-audit/README.md

The source kernels are credited adaptations of10020's original-label
and coordinate models. The old9795 proof uses a different, E108-specific
Q-pattern argument; the erroneous unbounded blue-spine selection is not
its premise. Source links and exact references are recorded in README
and CLAIM. Current primary Table1 was rechecked2026-10-03 and retains
22..23. The authors'21-point fixture is reproduced separately,93 red/
117 blue pairs, maxima3/6, as prior-art validation. No global upper23
flag certificate or reviewer verdict is replayed as new mathematics.
