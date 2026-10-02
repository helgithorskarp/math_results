# Independent ordinary audit and fractional missing-set separation

Actual author **six-reviewer-4**, **independent mathematical reviewer**.
This proof was written from the complete committed statement of LEMMA9685
before reading the target's executable sources or expected record. The
defining proof, its counts and its six-cycle table were visible; this is
not a blind audit. No earlier executable or imported finite classification
is used. All statements below are ordinary, unformalized mathematics.

## Exact conditional host

The target is a simple red graph on 22 labelled vertices with red
codegree at most 3 on red pairs and blue codegree at most 6 on blue pairs.
The complement is off-diagonal and the forbidden books are subgraphs,
with no induced-page restriction. The root u has degree 10, with its
induced labelled neighborhood

```
0:1,8,9; 1:0; 2:6,7; 3:4,5; 4:3,7,9;
5:3,6,8; 6:2,5,9; 7:2,4,8; 8:0,5,7; 9:0,4,6.
```

Old label 0 is a with global degree 9; all other root neighbors have
global degree 10. In the literal coordinates used by `core.py`,
u=0, v=1, a=2, X_i=3+i, SX=9,10, SY=11,12, T=13,14,15,
Q=16,...,21. The old-label map is (a,v,X_0,...,X_5,SX_0,SX_1).
Both r choices and both ordered SY--X choices are prescribed exactly
as in the target statement. `frame` records every known edge among
the first 16 vertices; all other such pairs are blue. X--Q, special--Q,
T--Q and Q--Q are unknown, with v--Q red and u--Q,a--Q blue.
The edge bound e(G)<=108 is essential to the following deduction.
No outside global-degree restriction or host automorphism is assumed.

The root neighborhood has 13 edges and degree sum 99. Its cut is
99-10-2(13)=63, giving e(G)=10+13+63+e(B_u)=86+e(B_u).
For every blue u--b pair, its blue pages are the ten other vertices of
B_u not red to b, so d_(B_u)(b)>=4. Since |B_u|=11, e(B_u)>=22.
The edge bound therefore forces equality and four-regular B_u.

Subtracting known incidences gives Q ranks
(0,6,0,3,3,4,4,4,4,4,4,2,2,3,2,3) on the first 16 vertices.
In particular the SY degrees are 9,9 and the T degrees 10,10,9.
These are consequences of the equality, not extra outside hypotheses.
For q in Q put p_j=[q red to SX_j], s_j=[q red to SY_j],
t_j=[q red to T_j], and M={i:q blue to X_i}. Then

\[
h(q)=4-s_0-s_1-t_0-t_1-t_2,\qquad
d(q)=11+p_0+p_1-|M|.
\]

For every blue pair ij, inclusion-exclusion among the 20 other
vertices gives red codegree <=d(i)+d(j)-14. No degree-10 substitution
is permitted for a derived degree-9 SY vertex.

## Physical page inequalities and endpoints

On each X-cycle edge, the known pages plus its two Q ranks exhaust
the red cap 3 and the subset minimum. Thus the two Q rows cover Q.
Consequently M is independent in the cycle
0--4--3--1--2--5--0. Its 18 independent sets are the empty set,
six singletons, nine independent pairs and P={0,2,3}, S={1,4,5}.
The tight SX--own-X pairs imply

\[
M\cap\{3,5\}\ne\varnothing\Rightarrow p_0=1,\quad
M\cap\{2,4\}\ne\varnothing\Rightarrow p_1=1.
\]

The tight X_5--T_0 pair implies 5 in M => t_0=1. Red v--q gives
t_0+t_1+t_2>=1. The blue a--q and red SY--q pairs give

\[
|M|\le5-s_0-s_1-\sum t_j,\quad
s_0=1\Rightarrow |M\cap P|\ge1+t_1+t_2,\quad
s_1=1\Rightarrow |M\cap S|\ge1+t_0+t_1.
\]

If both s_j=1, these imply 2+t_0+2t_1+t_2 <=
3-t_0-t_1-t_2. This contradicts sum t_j>=1, including its boundary
t_1=0. Thus the two rank-2 SY Q sets are disjoint.

The three already saturated red SY_1--T_0, SY_1--T_1, SY_0--T_1
pairs have known page sets {a,X_1,X_5}, {a,X_1,X_4}, {a,X_0,X_2}
respectively. They forbid their Q intersections. The two SY_1 points
therefore belong to T_2 only; the two unmarked points form precisely
T_1's Q set. The blue T_1--T_2 red cap 5 is already exhausted by
{a,SX_0,SY_0,X_0,X_1}, so those Q sets are disjoint.
The third T_2 point is one SY_0 point, A1, and the other, A0, lies in
T_0. Rank(T_0)=3 leaves exactly these cases:

| case | A0 | A1 | two B points | other points |
|---|---|---|---|---|
| U | SY0,T0 | SY0,T2 | SY1,T2 | two C in T0,T1 |
| V | SY0,T0 | SY0,T0,T2 | SY1,T2 | C in T0,T1, D in T1 only |

This is a set-theoretic exhaustive split, without symmetry breaking.
`endpoint_inventory` corroborates every actual six-point labelling:
180 case U and 360 case V endpoint assignments. The code does not
claim those endpoint assignments extend to graphs.

For a red known-i--q pair, the unknown Q pages have minimum
max(0,rank(i)+h(q)-6). For a blue pair q is absent from its known Q
row, so the sharper minimum is max(0,rank(i)+h(q)-5). These follow
from subset intersection on six, respectively five, actual Q vertices.
Our literal checker uses both. Dropping the latter blue minimum gives
exactly the same entire necessary column domain, not just its count.

Writing W0={0,1,3,5}, W1={0,1,2,4}, W2={0,1}, the red T--q
inequalities are

\[
t_0=1\Rightarrow |M\cap W0|\ge1+p_1+s_1,\quad
t_1=1\Rightarrow |M\cap W1|\ge1+p_0+s_0+s_1,\quad
t_2=1\Rightarrow |M\cap W2|\ge p_0+p_1+s_0-1.
\]

They and the point-spine caps give the target's complete necessary
table, independently recovered by checking all 8192 incidence words:

| role | missing sets |
|---|---|
| A0 | 01,03,35,P |
| A1 in U | 02,03 |
| A1 in V | 03 |
| B | 1,01,14,24 |
| C | 01,S |
| D | 01,24,P |

Here digit strings mean sets. Some missing sets have several SX
incidence possibilities; they are retained in the literal records.
For A1 the SY0 cap requires two P points; the T2/SX implications
remove 23 and P, leaving 02/03. Its additional T0 cap in V removes
02. For C the T0/T1 caps remove all pairs except 01; singletons 0/1
violate red X1--q/X0--q. P would force both p_j=1 and d(q)=10;
the blue SY1--q has six known red pages but cap 9+10-14=5.
Thus C is 01 or S. The degree-nine SY1 is essential to that step.
The other role classifications and their physical spine minima were
checked independently; the shorter proof below does not need them all.

## Proved strengthening: broader fractional domains

Let m_i be total missing mass at X_i. The Q ranks require
\(m=(3,3,2,2,2,2)\). The following two weighted inequalities exclude
that target even with broader role domains and arbitrary convex
mixtures separately at each role. Each role has total mass one.

For U use weight vector (0,0,1,1,-1,1). A0 may be ANY cycle
independent set and has score <=2. A1 retains 02/03 and has score <=1.
A B may be ANY independent set avoiding 5 and meeting S; its score
is <=0. Indeed 3 cannot occur, since then independence excludes
1,4 and 5 is absent; if 2 occurs, meeting S forces 4, cancelling its
score. A C remains 01/S and has score 0. Therefore

\[
m_2+m_3-m_4+m_5\le2+1+0+0+0+0=3,
\]

whereas the required target has score 4. This removes A0's full
classification and B's singleton-4 exclusion from the terminal proof.

For V use (0,1,1,0,0,1). A0 may be ANY independent set meeting P;
its score is <=1, since the only independent sets with score 2
are {1,5} and S, which miss P. A1 retains 03 and has score 0.
Each B and D may be ANY independent set avoiding 5, so score <=1
because 1--2 is a cycle edge. C may be ANY independent set, with
score <=2. Hence

\[
m_1+m_2+m_5\le1+0+1+1+2+1=6,
\]

whereas the target has score 7. This removes the D-specific
internal-Q subset-minimum classification and all C classification
from the V terminal argument. It does not remove the host equality,
the endpoint split, cycle independence or A1's point-spine bounds.

These maxima persist under convex combinations, so neither expanded
product of role convex hulls contains the required missing vector.
This is an exact rational separation; no LP solver or integrality
assumption is used. The unit gaps are actual certificate margins,
not claims of sharpness, minimum repair, physical realizability or
global Ramsey improvement. The supplied code checks every allowed
local set and all certificate coefficients with Python integers.

The original integer proof is also independently corroborated over
all 512 U and 384 V missing-set tuples, with no target sum. Computation
is supporting evidence for the ordinary deductions and two inequalities.

## Labels and trust boundaries

The SY-choice transport swaps X0/X1, X2/X4, X3/X5. The r transport
swaps X2/X3, X4/X5 and SX0/SX1. Every prescribed red/blue pair,
actual derived degree, Q rank and entire column domain transports;
these are bijections between hypotheses, not host automorphisms.
They carry the representative ordinary proof to all four actual cores.

The claim remains ONLY exclusion of the four prescribed terminal
configurations under e(G)<=108. It does not force those configurations
from all cross records or arbitrary hosts, review the parent9631
finite forcing stage, certify the upper23 flag proof, construct a
22-point host, or decide R(B4,B7). Background shell9131 and earlier
audit9105 are credited context rather than imported proof premises.
No graph classification, external solver, certificate import or
private data is a premise. Ordinary reasoning, faithful encoding and
CPython remain unformalized trust boundaries.
