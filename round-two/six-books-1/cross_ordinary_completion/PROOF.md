# An ordinary obstruction for the four terminal cross configurations

Actual author **six-books-1**, role **researcher**, 2026-10-02, pass18.
This is a new ordinary proof for a specified part of the earlier cross
computation. Independent review is pending; the written argument and code
correspondence are unformalized. The proof does not import a finite census.
The preceding step forcing these four configurations from arbitrary cross
cores remains computational; this does not replace that step or decide
the Ramsey number.

A valid graph is a simple red graph on 22 vertices with at most three
common red neighbors at a red edge and at most six common blue neighbors
at a blue pair. Blue is the complement on distinct vertices. Books are
ordinary subgraphs; edges between their pages are unrestricted.

## Exact conditional statement

Let a degree-ten root u have this induced labeled red neighborhood:

```text
0:1,8,9; 1:0; 2:6,7; 3:4,5; 4:3,7,9;
5:3,6,8; 6:2,5,9; 7:2,4,8; 8:0,5,7; 9:0,4,6.
```

The marked neighbor a=0 has global degree nine; the other nine members of
N(u) have global degree ten. Set v=1. The labeling comes from the ordinary
sole-page pair structure of
[9131](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/single_page_pairs/PROOF.md):
X=N(u)\{v,a} and Y=N(v)\{u,a} each have eight points, with two specials
SX and SY respectively, and three remaining points T. Write the ordinary
blocks as X0,...,X5 and Q=Y0,...,Y5. The sixteen known coordinates are
u=0,v=1,a=2, Xi=3+i, SX=9/10, SY=11/12 and T=13/14/15; Q has
coordinates16,...,21.
The old neighborhood labels map to (a,v,X0,...,X5,SX0,SX1).

The X cycle is 0--4--3--1--2--5--0 in local X indices. The SX own pairs
are {3,5} and {2,4}. The four specials form an independent set, and T is
independent. Each special is red to a and to its own root (SX to u, SY to
v), blue to the other root, and red to two T points. The vertex a is red
to u,v and all specials and T, and blue to every ordinary X/Q point.
The root u is blue to SY,T,Q; v is blue to X,SX,T and red to all Q.
These incidences and the table below specify every pair among the sixteen
known coordinates. Suppose the cross core
has the following fully specified incidences, retaining both actual r:

|r|SX0--T, SX1--T bit masks|T0--X, T1--X, T2--X bit masks|
|---|---|---|
|0|(6,5)|(43,23,3)|
|1|(5,6)|(23,43,3)|

SY0--T and SY1--T masks are (6,3). The ordered SY--X rows are either
(13,50) or (50,13). A mask has a bit at the corresponding local index;
13={0,2,3}, 50={1,4,5}, 43={0,1,3,5}, 23={0,1,2,4}.
All other known edges are exactly the ordinary pair shell and displayed
neighborhood; no unknown X--Q or internal-Q edge is prescribed.

**Lemma.** No valid graph with these hypotheses has e(G)<=108. No global
degree restriction on the eleven blue neighbors of u is an input. This
concerns exactly the four labeled terminal X16 configurations, not all
682 projected records per r or all cross cores.

The pair shell and four configurations below are explicit hypotheses;
the cited pair lemma is background for how this conditional subcase arises.
The edge equality used in
[9631](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/leaf_edge_only_candidate/PROOF.md) is
rederived here. The displayed neighborhood has 13 edges and neighbor-degree
sum 99. Its cut has 63 edges, so e(G)=86+e(G[B_u]). Every blue u--b spine
requires d_(G[B_u])(b)>=4. Hence e(G)<=108 forces e(G)=108 and B_u
four-regular. This gives Q row ranks

```text
X0,X1:3; X2,X3,X4,X5:4; SX0,SX1:4;
SY0,SY1:2; T0,T1,T2:3,2,3.
```

For q in Q, let s_j and t_k indicate its SY/T incidences. Its internal-Q
degree is h(q)=4-s0-s1-t0-t1-t2, and its actual global degree is
11+p0+p1-|M(q)|, where p_j indicates its SX incidence and M(q) is its
set of missing X neighbors. The derived SY degrees are 9,9 and T degrees
10,10,9; these are consequences, not additional outside degree hypotheses.
The red v--q cap gives t0+t1+t2>=1.

## Explicit transports

It suffices to write the ordinary argument for r0 and SY--X=(13,50).
Swapping X0/X1, X2/X4 and X3/X5 preserves the cycle, both SX own pairs
and all T rows, and interchanges the SY X classes. It transports the other
SY row choice. Swapping X2/X3 and X4/X5 while also exchanging SX0/SX1
preserves the displayed neighborhood and sends r0 to r1, leaving the SY
classes fixed. These are explicit relabelings of every prescribed edge
and unknown completion, not assumptions of host automorphisms.

Put P={0,2,3}, S={1,4,5}, W0={0,1,3,5}, W1={0,1,2,4}, W2={0,1}.
The required missing-row totals across the six Q-points are

    (3,3,2,2,2,2).                                      (1)

## Missing sets and the endpoint partition

On each red X-cycle edge ij the common known pages and the two Q row
sizes force the Q intersection to its minimum |Q_i|+|Q_j|-6. Therefore
Q_i union Q_j=Q, and M(q) is an independent set of the six-cycle for
every q. Its only size-three possibilities are P and S; every M has
size at most three. For clarity, the counts on the six cycle spines are:

|X spine|known common red pages|Q ranks|maximum/minimum Q intersection|
|---|---|---|---|
|X0--X4|u,T1|3,4|1|
|X4--X3|u|4,4|2|
|X3--X1|u,T0|4,3|1|
|X1--X2|u,T1|3,4|1|
|X2--X5|u|4,4|2|
|X5--X0|u,T0|4,3|1|

Each red SX own spine has just u as a known common red page and Q
ranks4,4, so its intersection maximum/minimum is2. This gives

    M meets {3,5} => p0=1;  M meets {2,4} => p1=1.        (2)

The red X5--T0 spine has two known pages, X0 and SY1, and Q ranks4/3.
Its Q intersection is at most1 and at least1, so their Q union is all Q:

    5 in M => t0=1.                                     (3)

The blue a--q cap is |M|<=5-s0-s1-t0-t1-t2=1+h. Red SY--q spines give

    s0=1 => |M intersect P|>=1+t1+t2;
    s1=1 => |M intersect S|>=1+t0+t1.                   (4)

If both s_j were one, (4) would give |M|>=2+t0+2t1+t2,
while the blue cap gives |M|<=3-t0-t1-t2. Since the T rows cover Q,
this is impossible. Thus the two SY Q two-sets are disjoint.

Red SY1--T0, SY1--T1 and SY0--T1 spines are already saturated by
{a,X1,X5}, {a,X1,X4} and {a,X0,X2}, respectively. Their Q intersections
are empty. Hence the two points
of SY1^Q lie only in T2, and the two remaining unmarked points are
exactly T1^Q. The blue T1--T2 spine already has common known red neighbors
{a,SX0,SY0,X0,X1} and red-codegree cap five, so its Q intersection is empty.
The third T2 point is one of SY0's two Q points; call it A1. Call the
other A0. The latter must belong to T0. Label the two SY1 points B0,B1.
There are just two possibilities:

|case|A0|A1|B0,B1|unmarked points|
|---|---|---|---|---|
|U|SY0,T0|SY0,T2|SY1,T2|C0,C1 both T0,T1|
|V|SY0,T0|SY0,T0,T2|SY1,T2|C in T0,T1; D in T1 only|

This uses the actual T0 rank three, not a symmetry quotient of endpoints.

## Small ordinary classification of missing sets

The following table contains every possibility needed in the proof.
Notation such as 01 means {0,1}; entries are labeled sets.

|point role|possible M|
|---|---|
|A0|01,03,35,P|
|A1 in U|02,03|
|A1 in V|03|
|B0 or B1|1,01,14,24|
|C (in T0,T1)|01,S|
|D (in T1 only)|01,24,P|

Here is a direct derivation, rather than an imported computed table.
For a red T--q spine, its X and special pages give

    t0=1 => |M intersect W0|>=1+p1+s1;
    t1=1 => |M intersect W1|>=1+p0+s0+s1;
    t2=1 => |M intersect W2|>=p0+p1+s0-1.              (5)

Every M is one of the eighteen independent sets of the six-cycle: the
empty set, six singletons, nine independent pairs, or P/S. Conditions
(2)--(5) already make A1 in U either02 or03, and in V only03: (4)
requires two P points, and (5) rules out23 or P; the T0 inequality
also rules out02 in V.

For A0, (4) requires a P point. Conditions(2),(5) eliminate the singleton2
and pairs02,23,24. Singleton0 is impossible on the red X3--q spine
(cycle neighbors, SY0 and T0); singleton3 is impossible on red X0--q.
The remaining independent sets are precisely01,03,35,P.

For B, (3) forbids5 and (4) requires an S point. The only candidate
sets are1,4,01,14,24. Singleton4 has red X1--q pages X2,X3,SY1,T2,
so is impossible. This gives the B row of the table.

For C, (2),(5) rule out every independent pair except01. Singletons
0 and1 violate red X1--q or X0--q respectively, with both T0,T1 pages.
The size-three set P would force both p_j=1, actual d(q)=10, and the
blue SY1--q spine would have six common red neighbors v,X1,X4,X5,T0,T1.
Its red-codegree cap is9+10-14=5. Hence only01 or S remains.

For D, h=3. Red SX0--q, when p0=1, has a T1 page and at least one
internal-Q page, because the SX Q rank is4 and h=3. Thus it requires
M to meet {3,5}; by(3), 5 is forbidden. On a red own X--q spine the
same Q minimum contributes one page. In particular, if X2 is red to q,
its page cap forces 1 in M and p1=0, since 5 is not in M. With p1=0,
(2) leaves both X2,X4 red, and the X4 cap then forces0 in M. Independence
gives M=01. With p1=1, X2 must be missing. If X4 is also missing,
independence gives24. Otherwise its red-spine bound forces both0,3
missing, giving P. This proves the last row of the table.

All uses of an internal-Q minimum are the ordinary subset bound: on a
red i--q spine the unknown Q contribution is at least
max(0, |Q_i|+h(q)-6). No particular internal-Q graph is selected.
For a blue pair ij, the equivalent red-codegree cap is
d(i)+d(j)-14, by inclusion-exclusion in the twenty other vertices.

## Case U: missing multiplicities contradict the row totals

Each of the six missing sets normally has size two. Let c be the number
of the two C points with M=S, a indicate A0 having M=P, and b count
the B points with singleton M=1. The total in(1) is14, so

    c+a-b=2,  0<=c<=2, a in {0,1}, 0<=b<=2.            (6)

If c=2, coordinate4 already has its required two missing occurrences.
Both B sets must avoid4 and therefore contain1. The two C sets also
contain1, exceeding its target three. Thus c<=1. Equation(6) now forces
c=a=1 and b=0.

The C sets are S and01 and A0 is P. Coordinate1 needs precisely one
occurrence among the B sets, so one B set is24. Coordinate4's target
is now exhausted by S and24, forcing the other B set to be01. Coordinate2
is exhausted by P and24, forcing A1=03 rather than02. But coordinate0
then occurs in P,01 at C,01 at B and03 at A1: four times, contrary to(1).

## Case V: the remaining integer possibilities are impossible

Let a indicate A0=P, c indicate C=S, d indicate D=P, and b count the
singleton B sets. The missing total is again14, giving

    a+c+d-b=2.                                        (7)

If a=d=1, coordinate3 occurs in A0, D and the fixed A1=03, exceeding
its target two. Thus a+d<=1, and(7) forces c=1, b=0 and a+d=1.

If d=1, coordinate3 is exhausted by D and A1, so A0 must be01. Then
coordinate0 is exhausted by D,A1,A0. Both B sets must avoid0, hence
both contain4, which already occurs in C=S: three occurrences, impossible.

If a=1, D is01 or24. With D=01, coordinate0 is exhausted by A0,A1,D
and again both B sets add4 to C=S, impossible. With D=24, coordinate4
is exhausted by C and D, so both B sets are01. Coordinate0 then occurs
in A0,A1 and both B sets, four times. This is the final contradiction.

The four specified terminal configurations therefore have no valid
completion, by ordinary page bounds, six-cycle independence and integer
missing-neighbor counts alone. Explicit transports cover every actual label
choice. There is no computer-generated premise in this argument.

## Scope and remaining bridge

The preceding full cross lemma9631 uses exact computation to force the
four terminal configurations from the broader necessary domain and then
checks360 physical books. This proof replaces that terminal completion
stage once the four configurations are obtained. It does not assert that
the four patterns follow from ordinary inequalities, weaken the specified
neighborhood, remove the edge bound, or provide a new Ramsey endpoint.
Independent corroboration and meaningful literal-label/page controls are
reported separately; they do not turn same-author checks into peer review.
