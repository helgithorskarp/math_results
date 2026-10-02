# Ordinary forcing of T2={X0,X1} in the broader cross shell

Actual author: **six-books-1**, role **researcher**, 2026-10-02, pass19.

**Status:** complete ordinary written proof with same-author exact corroboration.
Independent review pending; not formalized. This is a proof of
a specified conditional obstruction, not a new Ramsey endpoint or a new host
class beyond the previous specified-leaf exclusion9631/1.

## Statement and complete hypotheses

Let G be a simple graph on22 vertices. Every red edge (an edge of G) has at
most3 common red neighbors, and every blue edge has at most6 common blue
neighbors. Write d(x) for the red degree. For a blue pair xy these conditions
equivalently give

    |N_G(x) intersect N_G(y)| <= d(x)+d(y)-14.             (1)

Partition the labeled vertices as

    {u,v,a}, X={X0,...,X5}, SX={SX0,SX1},
    SY={SY0,SY1}, T={T0,T1,T2}, Q={six vertices}.

The root neighborhood is N(u)={v,a} union X union SX. Its induced graph has
the edge av, the six-cycle

    X0-X4-X3-X1-X2-X5-X0,

the two edges a-SX0,a-SX1, and the edges SX0-X3,SX0-X5,SX1-X2,SX1-X4.
There are no other edges inside N(u). Assume d(u)=10,d(a)=9, and degree10
for all the other nine members of N(u).

The other prescribed incidences are as follows. The four vertices of SX union
SY form an independent set, as do the three vertices of T. The vertex v is
red to both SY and all Q and blue to T. The vertex a is red to SY union T
and blue to Q. SY-to-T rows, with bits ordered T0,T1,T2, are

    SY0: {T1,T2}; SY1: {T0,T1}.

There are two actual SX-to-T choices:

    r=0: SX0:{T1,T2}, SX1:{T0,T2};
    r=1: SX0:{T0,T2}, SX1:{T1,T2}.

All SY/T-to-X, SX/SY/T-to-Q, X-to-Q and Q-to-Q edges are free.
All other pairs are determined by the above partition and neighborhood.
These are explicit shell hypotheses, not an assertion that every Ramsey
graph has this neighborhood or shell. Assume finally |E(G)|<=108.

**Conclusion:** the X-neighbor row of T2 is exactly **{X0,X1}**.
We use P={X0,X2,X3} and S={X1,X4,X5} for the two remaining alternatives
that will be excluded.

No global degree bound on the eleven vertices outside N[u] is assumed.
In particular, an intermediate SY degree8 is allowed throughout.

The broader cross shell was already computationally excluded as part of
9631/1. This argument replaces the entire T2-row forcing step with ordinary
mathematics. It does not prescribe the other SY/T endpoint rows or make
the entire parent proof ordinary. The previous ordinary
terminal result9685/0 has T2={X0,X1} and prescribed other endpoint rows;
its proof is not a premise here.

## Cut equality and the four tight cycle edges

Put B=SY union T union Q. The root-neighborhood edge count is13. The sum
of its ten prescribed global degrees is99, so the cut from N(u) to B has
99-26-10=63 edges. Consequently

    |E(G)|=86+|E(G[B])|.

For b in B, the blue u-b spine has 10-d_B(b) blue common neighbors inside
B. Its cap6 implies d_B(b)>=4. Hence |E(G[B])|>=22, and the edge bound
forces equality and **G[B]4-regular**.

For a known vertex z let Q_z=N_G(z) intersect Q. Its ranks therefore are

    |Q_v|=6; |Q_a|=|Q_u|=0; |Q_SX0|=|Q_SX1|=4;
    |Q_SY0|=|Q_SY1|=2; |Q_T0|=3, |Q_T1|=2, |Q_T2|=3.  (2)

For an endpoint z in SY union T write R_z=N_G(z) intersect X. For Xi
write D_i=N_G(Xi) intersect(SY union T). Then

    |Q_Xi|=7-|D_i| (i=0,1), 6-|D_i| (i=2,3,4,5).

The blue a-Xi bound(1) gives |D_i|<=4 for i0,1, and <=3 otherwise.
In particular |Q_Xi|>=3. On a red cycle pair Xi-Xj there are already
1+|D_i intersect D_j| common neighbors in the known sixteen vertices.
The six-point Q universe supplies at least |Q_Xi|+|Q_Xj|-6 additional
common red neighbors. For the four edges04,05,12,13 the red cap gives

    D_i union D_j = SY union T,
    Q_Xi union Q_Xj = Q.                                  (3)

Thus every endpoint row covers the two paths4-0-5 and2-1-3. For a Q point
q its missing set M(q)={i:q is blue to Xi} is independent in those paths.
In particular, missing X0 forces red X4,X5, and missing X1 forces red
X2,X3.

Two other useful scalar bounds follow directly from physical spines.
The blue v-Xi pair has u, its SY neighbors, and Q_Xi as common red
neighbors. Therefore the number of T neighbors of Xi is at least2 for
i0,1 and at least1 for i2,...,5. For a Q point put

    p_j=1(q-SXj red), s_j=1(q-SYj red), t_k=1(q-Tk red),
    h(q)=d_G[Q](q)=4-s0-s1-t0-t1-t2.

The red v-q cap forces t0+t1+t2>=1. Its actual global degree and the
blue a-q bound are

    d(q)=11+p0+p1-|M(q)|,
    |M(q)| <= 1+h(q).                                     (4)

These identities retain arbitrary actual Q degrees.

## First reduce T2 to the two-center row or P/S

For any three known vertices z,Xi,Xj with Q_Xi union Q_Xj=Q, the two
spine intersection bounds |Q_z intersect Q_Xi|<=L_i and
|Q_z intersect Q_Xj|<=L_j imply |Q_z|<=L_i+L_j. This ordinary union
budget keeps simultaneous row information that separate subset minima lose.

Suppose T2 is red to both endpoints of one of04,05,12,13. On the two
red T2-X spines, their total number of common red neighbors in the known
sixteen vertices is at least4: the one own SX neighbor of the noncenter
endpoint, at least one occurrence of SY0 because its row covers the edge,
and the two cycle occurrences contributed by the endpoints themselves.
The two red caps therefore give a sum of Q-intersection allowances at
most6-4=2. But(3) and |Q_T2|=3 give the opposite bound3. This is
impossible. Consequently R_T2 is independent in the two paths, and is
also a vertex cover of them.

In either three-point path an independent vertex cover must be one of its
two bipartition classes. Thus R_T2 is one of01,023,145,2345. Each red
SXj-T2 spine already has a and its own-pair intersection as common red
neighbors, and its Q subset minimum is1. Each own-pair intersection has
size at most1. This excludes2345. Only01,P,S remain, in both actual r
labels. It suffices now to exclude P/S.

## Force the labeled Q pattern when r=0 and T2=P

We first prove this actual branch. Both own-pair intersections of T2 with
SX are1. Each red SXj-T2 pair already has a and that own X point as common
neighbors. With Q ranks4 and3, its Q intersection minimum1 is forced.
Thus Q_SXj union Q_T2=Q for both j.

Put C=Q_T2 and O=Q minus C, both of size3. Both SX rows contain all O and
one C point. The blue SX0-SX1 pair already has u,a,T2 as common red
neighbors, so its Q intersection is at most3. Their C points must differ.
Label them c0,c1; let n be the third C point. Thus

    Q_SX0={c0} union O; Q_SX1={c1} union O.

The red SX0-X3 spine has u,T2 and possibly T1 as known common red
neighbors. Its Q minimum is4-|D_3|. Combining its cap3 with |D_3|<=3
forces |D_3|=3, X3-T1 blue, and Q_X3 union Q_SX0=Q. Therefore Q_X3
contains c1,n. On red T2-X3 these two Q points and SX0 exhaust the cap3.
It follows that X3-SY0 is blue, its third Q neighbor lies in O, and

    D_3={SY1,T0,T2}; Q_X3={c1,n,z3}, z3 in O.

Similarly red SX1-X2 and then T2-X2 give

    D_2={SY1,T1,T2}; Q_X2={c0,n,z2}, z2 in O.

The endpoint-union equalities(3) on12 and13 now force SY0,T0,T1 into
D_1. Since X1-T2 is blue, D_1 is this triple, possibly with SY1. The
missing Q row of X1 has size2 or3 and, by(3), lies in Q_X2 intersect
Q_X3={n} plus at most one point of O. Hence the size is2, X1-SY1 is
blue, and z2=z3=z. Write the other two O points w,w'. We have forced

|vertex|complete red Q row|
|---|---|
|X1|c0,c1,w,w'|
|X2|c0,n,z|
|X3|c1,n,z|
|SX0|c0,z,w,w'|
|SX1|c1,z,w,w'|
|T2|c0,c1,n|

The Q labels are chosen by actual incidences. This is not a host symmetry
assumption. In particular the two points w,w' are the only unordered pair
left, and the subsequent argument treats them alike.

## Reduce the endpoint rows to two shapes

The forced incidences imply that R_SY0 contains X1 but excludes X2,X3,
R_SY1 contains X2,X3 but excludes X1, R_T0 contains X1,X3 but excludes
X2, and R_T1 contains X1,X2 but excludes X3. Each still covers4-0-5.

If c0 or c1 is red to SY0, red T2-q forces X0 blue. The missing-set rule
then makes X4,X5 red. Red SY0-q already has v,X1,T2 as three common red
neighbors, so neither X4 nor X5 can lie in R_SY0. The cover condition
forces **R_SY0={X0,X1}**. Thus for every other SY0 row c0,c1 are blue
to SY0. If n is red to SY0, red T2-n forces X0 blue, and hence
M(n)={0,1}; red SY0-n implies R_SY0 contains at most one of X4,X5.

The only five cover rows initially available for SY0 are

    01, 014, 015, 0145, 145,

where concatenated indices denote a set. Row0145 is impossible: c0,c1,n
cannot be SY0 neighbors by the preceding paragraph. If w or w' were red
to SY0, then h<=2 by the T cover, and(4) bounds |M|<=3. The missing
X2,X3 use two places; since X1 is red, at most one member of R_SY0 is
missing. Red SY0-q, however, requires at least |R_SY0|-2+t1=2+t1
missing members of this row. Only z could be a SY0 neighbor, contrary
to its rank2.

Row145 is also impossible. The preceding c0/c1/n conditions make Q_SY0
a subset of O. The blue SY0-SX0 pair has the four known common red
neighbors a,T1,T2,X5. Its actual degrees9 and10 give a cap5 in(1).
It permits at most one Q common neighbor, but O is contained in Q_SX0
and |Q_SY0|=2.

For the remaining three rows use the following ordinary inequalities.
Red SX1-X4 and SX0-X5, their Q subset minima, and |D_4|,|D_5|<=3 give

    1(X4 in R_SY0)+1(X4 in R_SY1)+1(X4 in R_T1) >=2;
    1(X5 in R_SY0)+1(X5 in R_SY1)+1(X5 in R_T0) >=2.     (5)

The red SY1-T0,SY1-T1,SY0-T1 spines give respectively

    |R_SY1 intersect R_T0|<=2,
    |R_SY1 intersect R_T1|<=2,
    |R_SY0 intersect R_T1|<=2.                           (6)

Finally X0,X4,X5 each lie in R_T0 union R_T1, by their T-neighbor lower
bounds and the assumption R_T2=P. These conditions have the following
short case analysis; no projection census is used.

* **SY0=01.** Equation(5) forces X4 into both SY1,T1 and X5 into both
  SY1,T0. The SY1-T1 intersection already contains X2,X4, so T1
  omits X5 and is0124; SY1 must omit X0 and is2345. The SY1-T0
  intersection contains X3,X5, so T0 omits X4 and is0135.
* **SY0=014.** Equation(5) forces X5 into SY1,T0. Their intersection
  already contains X3,X5. The cover rows leave just
  (SY1,T0)=(2345,0135) or(0235,1345): having either extra X0 or X4
  in both rows is forbidden. In the first case T1 must contain X4
  to cover it, and(6) with SY0 forces it to omit X0. The cover row is
  then1245, which meets SY1 in X2,X4,X5. In the second case T1
  must contain X0 to cover it and X4 by(5), meeting SY0 in three
  points. Both cases contradict(6).
* **SY0=015.** Equation(5) forces X4 into SY1,T1. Their intersection
  already contains X2,X4, leaving(SY1,T1)=(2345,0124) or(0234,1245).
  In both cases the cover and(5)-(6) force T0=0135. The second case
  is impossible as follows. X5 has Q rank3. On red X2-X5 there are
  already u,T1, so |Q_X5 intersect Q_X2|<=1. On blue X1-X5 there
  are already u,X2,SY0,T0,T1, so(1) gives |Q_X5 intersect Q_X1|<=1.
  But Q_X1 union Q_X2=Q, contradicting |Q_X5|=3.

It remains only to exclude

    R_T0=0135, R_T1=0124, R_SY1=2345,
    R_SY0=01 or015.                                     (7)

For completeness, each claimed two-pair alternative above can be checked
directly from the cover description: SY1 rows are023,0234,0235,02345,2345;
T0 rows are013,0134,0135,01345,1345; T1 rows are012,0124,0125,01245,1245.
The named two already common points exclude every extra common0/4 or0/5.
This elementary cover argument supplies the classification bridge.

## A forced Q-neighbor collision excludes both remaining shapes

In(7), X4 has Q rank4. Red X3-X4 has u,SY1 as common neighbors, so
Q_X4 union Q_X3=Q. Red SX1-X4 has only u among the known common
neighbors, so Q_X4 union Q_SX1=Q as well. The two complement sets
force all four points c0,n,w,w' into Q_X4. Hence

    Q_X4={c0,n,w,w'}.

Both red SY1-T0 and SY1-T1 already have a and two X points as common
neighbors. Thus Q_SY1 is disjoint from both T rows. The T cover gives
Q_SY1 subset C. The point n cannot belong: red SY1-n would have the
four common red neighbors v,X2,X3,X4. Therefore

    Q_SY1={c0,c1}.

Red SY1-c0 has v,X2,X4 as common neighbors and forces X5 blue to c0.
Missing X5 forces red X0. Red T2-c0 then already has SX0,X0,X2;
it forces SY0 blue and no internal Q neighbor in C. Red X2-c0 has
X1,SY1,T2, forcing no internal Q neighbor in Q_X2. Consequently the
two internal Q neighbors of c0 are exactly w,w'.

The point c1 is blue to X2,X4, so missing X4 forces red X0. Red T2-c1
already has SX1,X0,X3, forcing SY0 blue and no internal Q neighbor in
C. Red X3-c1 already has X1,SY1,T2, forcing no internal neighbor in
Q_X3. Since c1 is red to SY1,T2 and blue to SY0,T0,T1, its internal
degree is2. Its neighbors too are exactly w,w'.

For either b=w,w', the red X1-b spine now has c0,c1 as common Q
neighbors. Its other known common neighbors are exactly its red
neighbors among SY0,T0,T1. The cap3 and T cover give

    b-SY0 blue, exactly one of b-T0,b-T1 red.

Thus both b have internal degree3. Since c0,c1,w,w' are all blue to
SY0, its rank2 forces Q_SY0={n,z}. Red T2-n has X2,X3,SY0 as three
common neighbors, forcing X0 blue and no internal Q neighbor in C.
Missing X0 forces X4,X5 red. Equation(4) with M(n)={0,1} implies
its internal degree is at least1. Its exact degree in G[Q] is

    h(n)=2-1(n-T0 red)-1(n-T1 red).

The blue SY0-T0 pair has a,X0,X1, and also X5 if SY0=015, as known
common red neighbors. Its derived-degree cap exceeds this count by1
in either case, so |Q_SY0 intersect Q_T0|<=1.

If n-T0 were red, z-T0 would be blue. The T0 rank3 would then force
both w,w' red to T0. For each such b, red SX1-b already has X4,T0
and its Q neighbor c1 as common neighbors. Its third internal Q
neighbor cannot be in O, which is red to SX1, and must therefore be n.
Both w,w' would meet n, although h(n)<=1. Hence n-T0 is blue.

Now T0 rank3 forces all O={z,w,w'} red to T0. The same SX1 argument
forces w,w' adjacent to n. Since h(n)=2-1(n-T1 red), it follows that
n-T1 is blue. But c0,c1 were already blue to T1, and both w,w' are
blue to T1 because they are red to T0 and meet exactly one T row.
Only z could be red to T1, contradicting its required Q rank2.

This excludes(7), and finishes the r=0,T2=P branch.

## Explicit transports, not symmetry restrictions

The permutation of X indices(0 1)(2 4)(3 5), fixing u,v,a,SX,SY,T and
each Q vertex, preserves the literal neighborhood, the six-cycle and
each own pair. It exchanges P and S and transports every free endpoint
row and completion. It therefore excludes T2=S for r=0 as well.

The permutation(2 3)(4 5) on X, accompanied by SX0<->SX1, fixes all
other known vertices and sends the actual r=0 SX-T incidences to r=1.
It preserves P and S, the cycle, all prescribed degrees and every shell
incidence. Transporting Q labels c0<->c1 preserves the named proof
pattern. Combining these two relabelings covers both P/S choices in
both actual r labels. No automorphism of a hypothetical host is assumed.

## Reproducibility and remaining obligations

The proof above uses ordinary spine counts, subset unions, row ranks and
the displayed finite cover descriptions. It imports no candidate census,
solver result or peer verdict as a premise. The accompanying source
corroborates the literal root/coordinate bridge, all scalar counts, the
endpoint cover, the two terminal forced-Q patterns and all four transports.
Written proof/source correspondence remains unformalized, and same-author
distinct checks do not constitute independent review.

The remaining ordinary forcing problem is the other SY/T-to-X rows once
T2=01. No 22-vertex witness or unrestricted22-vertex exclusion is supplied.
