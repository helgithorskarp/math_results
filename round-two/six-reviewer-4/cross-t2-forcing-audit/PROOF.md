# Independent ordinary audit of the broader-shell T2 forcing

Actual author: **six-reviewer-4**, independent mathematical reviewer,
2026-10-02, PASS35. The graph's complete defining proof was visible.
This reconstruction and its literal set checker were sealed before opening
the target's executable or compact certificate. This is not a blind audit.
Prior reviewer source for terminal9685 supplied notation and colored-spine
methods; its prescribed endpoint rows and fixed X ranks are **not premises**.

The target is LEMMA9795 by six-books-1, conditional on its literal22-vertex
cross shell, marked root/neighborhood degrees10/9/10 and red edge count108
or less. All five endpoint-to-X rows initially are free and all eleven
outside global degrees are unrestricted. The hypotheses and exact local
edge lists appear in the companion REVIEW. Red edge codegrees are at most3;
blue edge red codegrees are at most \(d_i+d_j-14\).

## Cut, ranks and simultaneous unions

Write \(H=N(u)\) and \(B=V(G)\setminus N[u]\). The literal H has13 edges,
and its global degree sum is99. Its cut to B is \(99-26-10=63\).
Therefore \(e(G)=86+e(B)\). For every blue u-b pair there are
\(10-d_B(b)\) common blue neighbors, so each induced B degree is at least4.
The assumed bound forces \(e(B)=22\) and every degree in B equals4.

All Q row ranks now follow directly: v has6, a/u have0, SX have4 each,
SY have2 each, and T0/T1/T2 have3/2/3. Let \(D_i\) be the endpoints
among SY/T adjacent to Xi. The ranks of X0/X1 are \(7-|D_i|\), and those
of the four other X vertices are \(6-|D_i|\). The blue a-Xi cap bounds
\(|D_i|\le4\) for i0,1 and \(|D_i|\le3\) otherwise.

On any of04,05,12,13, one endpoint is a center and one a leaf. The
known common red count is \(1+|D_i\cap D_j|\); the Q intersection has
lower bound \(7-|D_i|-|D_j|\). Summing gives at least
\(8-|D_i\cup D_j|\ge3\). Equality is forced. Thus the endpoint union
is all5 and the Q union all6. In particular, every endpoint row covers
both paths4-0-5 and2-1-3. Every Q column's missing X set is independent
in these paths. Blue v-Xi also forces at least2 T neighbors at the two
centers and at least1 at each leaf.

For arbitrary Q subsets A,B,Z with \(A\cup B=Q\), there is an exact
simultaneous budget
\[
 |Z|=|Z\cap A|+|Z\cap B|-|Z\cap A\cap B|.
\]
Consequently upper allowances L1,L2 imply
\(|Z|+|Z\cap A\cap B|\le L1+L2\). The target uses its weaker
overlap-free consequence. This is a general elementary identity, not a
new Ramsey theorem; the overlap version is a useful optional tightening.

If T2 contains both ends of a tight edge, the two known T2-X common
counts sum to at least4: two cycle incidences, one own-SX incidence and
one SY0 incidence by the cover. Their two Q allowances sum to at most2,
contradicting the rank3 of T2 and the Q union. Thus T2 is an independent
cover of each path, hence one of01,023,145,2345. The red SXj-T2 cap,
known common a and Q intersection minimum1, limits its intersection
with each own pair35/24 to1. It removes2345.

This uses neither the old terminal lemma nor a global outside degree
floor. The checker enumerates all25 covers, the eleven masks passing
the own-pair test, all200 offending-mask/SY0-cover witnesses, and the
three final masks. These small enumerations corroborate the displayed
ordinary independent-cover classification; they are not its premises.

## P branch and complete endpoint classification

Take actual r0 and T2=023=P. Put C=Q_T2, O its complement. Both SX
Q rows are tight unions with C, so each consists of O plus one C point.
Blue SX0-SX1 has known common u,a,T2 and cap6, hence its Q intersection
is at most3. Their C points differ: name them c0,c1 and the third n.

Red SX0-X3 has known u,T2, possibly T1, and Q intersection minimum
\(4-|D_3|\). The cap and \(|D_3|\le3\) force \(|D_3|=3\), T1 absent
and a Q union. Red T2-X3 then has SX0 and c1,n, exhausting the cap:
SY0 is absent and the third Q point belongs to O. Thus D3={SY1,T0,T2}.
The SX1-X2/T2-X2 argument gives D2={SY1,T1,T2}. The two unions at X1
force D1 to contain SY0,T0,T1, possibly SY1. Its missing Q row has
size2 or3 and lies in Q_X2 intersect Q_X3, which has n and at most one
O point. Therefore its size is2, SY1 is absent at X1 and both third
O points coincide, call this point z. Name the remaining O points w,w'.

The forced Q rows are X1=c0,c1,w,w'; X2=c0,n,z; X3=c1,n,z;
SX0=c0,z,w,w'; SX1=c1,z,w,w'; T2=c0,c1,n. This is a choice of
actual labels, not an automorphism assumption about a host.

The four remaining endpoint rows have five cover choices each:
SY0:01,014,015,0145,145;
SY1:023,0234,0235,02345,2345;
T0:013,0134,0135,01345,1345;
T1:012,0124,0125,01245,1245.

If c0/c1 belongs to Q_SY0, the red T2 spine forces X0 blue, hence
X4,X5 red. The red SY0 spine has v,X1,T2 already, forcing its row01.
If n belongs to Q_SY0, the analogous spine forces missing set {0,1}
and its row contains at most one of4/5. Thus0145 excludes all C points
from Q_SY0. A possible w/w' neighbor has h<=2 by the T cover and
\(|M|\le1+h\), leaving at most one row point missing since2/3 are
already missing and1 is red. But the red SY0 spine requires at least
\(|R_{SY0}|-2+t1\ge2\) row points missing. Only z remains, insufficient
for rank2. Row145 also excludes C, while blue SY0-SX0 has four known
common neighbors and actual degrees9/10. It permits only one Q common
neighbor, although both SY0 Q points would lie in O, contained in SX0.

For SY0=01/014/015, red SX1-X4/SX0-X5 give
\[
 s_{04}+s_{14}+t_{14}\ge2,\qquad
 s_{05}+s_{15}+t_{05}\ge2.
\]
Red SY1-T0/SY1-T1/SY0-T1 give the three corresponding endpoint
intersections at most2. T0 union T1 must contain0,4,5.
For row01 the first inequalities force SY1=2345,T0=0135,T1=0124.
For row014, the possible (SY1,T0) pairs are (2345,0135)/(0235,1345):
the first forces T1=1245, intersecting SY1 three times; the second
forces T1 to contain0/1/4, intersecting SY0 three times. Row015 gives
(SY1,T1)=(2345,0124)/(0234,1245) and T0=0135. The second alternative
has X5 rank3, while red X2-X5 and blue X1-X5 each allow only one Q
common point. Since Q_X1 union Q_X2=Q, this is impossible.

Exactly two shapes remain, with SY0=01 or015 and the other three
rows SY1=2345,T0=0135,T1=0124. The literal checker independently
enumerates all625 cover quadruples and both actual orientations, checks
all2500 full adjacency/rank/degree transports and obtains the three
scalar shapes and two after this additional union cut. It retains the
actual degree8 of SY0 in the01 branch.

## Ordinary terminal contradiction

Tight red X3-X4 and SX1-X4 force Q_X4=c0,n,w,w'. The red SY1-T0/T1
caps prohibit any Q intersection. Every Q point meets a T row (red v-q
cap), hence Q_SY1 lies in C. The point n would make red SY1-n have
v,X2,X3,X4 as four common neighbors. Thus Q_SY1={c0,c1}.

Red SY1-c0, with v,X2,X4 already, forces X5 blue, and consequently X0
red. Red T2-c0 has SX0,X0,X2 already and red X2-c0 has X1,SY1,T2
already. These prohibit SY0 and internal Q neighbors in C or Q_X2,
respectively. Its internal degree2 therefore forces exactly w,w'.
For c1, missing X4 forces X0 red; red T2-c1 and X3-c1 give the same
conclusion, again with internal degree2.

For b=w/w', red X1-b now has both c0,c1 as Q common neighbors. Its
other common neighbors are its adjacent SY0,T0,T1. The cap and the T
cover force SY0 blue and exactly one of T0/T1 red; hence h(b)=3.
Now Q_SY0={n,z}. Red T2-n has X2,X3,SY0 already, forcing X0 blue and
no internal neighbor in C. Missing X0 forces X4,X5 red; M(n)={0,1},
so the blue a-n cap implies h(n)>=1. Here h(n)=2-t0-t1.

Blue SY0-T0 permits only one Q common point in both shapes: the known
count is3/4 and the actual degree-dependent cap4/5. If n met T0, z
could not. Rank3 would force w,w' into Q_T0. Red SX1-b then has
X4,T0,c1 already, prohibiting its third internal Q neighbor in O;
it must be n. Both b meet n, contradicting h(n)<=1.
Therefore n omits T0, and all O meets T0. The same SX1 argument makes
w,w' meet n, so h(n)=2 and n omits T1. Both c0,c1 already omit T1,
and w,w' omit it since they meet T0 and exactly one of T0/T1. Only z
remains, contradicting the rank2 of T1.

Every use of an induced internal Q degree is derived from B4-regularity;
no outside global degree floor has entered. The blue-spine caps above
use each actual endpoint degree, including8.

As distinct corroboration, the checker builds all16 known vertices and
enumerates Q subsets by prescribed rank with exact pair intersection
caps. It then checks every known-vertex/Q-point spine with the necessary
internal-Q subset lower bound. Both shapes have zero surviving prefixes.
No Q-Q graph is assumed, generated or needed for this computation.
This finite necessity check is supplemental; the ordinary collision
argument above proves the terminal step.

## Transport and scope

X permutation(01)(24)(35) fixes each own SX pair, the cycle, all marks
and r, and exchanges P/S. X permutation(23)(45) with SX exchange changes
actual r0/r1 and preserves P/S. Both are bijections of all free incidence
choices, not symmetry restrictions on a host. Thus all four branches
are covered and T2=01 is necessary. There is no existence or sharpness
assertion. The larger shell was already excluded computationally in9631;
this ordinary replacement closes one reduction step, not R(B4,B7).

Written proof, program correspondence and the finite-case bridges are
unformalized. The defining shell is conditional; no assertion that every
22-vertex Ramsey graph has it is made.
