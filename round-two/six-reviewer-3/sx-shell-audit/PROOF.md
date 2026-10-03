# Four mixed degree sums suffice; every valid shell has weighted sum at most 79

Actual six-reviewer-3, independent mathematical reviewer, 2026-10-03.
Ordinary combinatorial proof, unformalized. The target's written proof and
prior scoped review9414 were exposed; this is not blind. No executable,
fixture, expected result, or certificate from the new target has been read.

Use EXACTLY the original22-vertex shell in LEMMA10144, with red page cap3
and blue page cap6. Keep all root, cycle, SX/SY independence, T independence,
and omission incidences. All previously free incidences remain free,
including all Q-Q pairs. Remove the six individual X degree marks.
Let E*={(0,4),(0,5),(1,2),(1,3)} be the four mixed cycle edges, and
write d_i for the actual full red degree of X_i.

**Strengthened exclusion.** No such graph satisfies d_i+d_j>=20 for ALL
(i,j) in E*. No SX degree, total edge bound, prescribed T0 row, outside
degree floor, or root-classification premise is added.

**Necessary cuts without ANY X degree assumption.** In every valid
completion of this same fixed shell, each d_i+d_j<=20 on E*, some such
sum is<=19, and

\[
2d_0+2d_1+d_2+d_3+d_4+d_5\le79.
\]

No realization, optimality of79, other shell, or Ramsey endpoint is claimed.

## Entire labelled shell

The vertices are u,v,a, X0..X5, SX0,SX1, SY0,SY1, T0,T1,T2, Q0..Q5.
N_R(u)={v,a,X0..X5,SX0,SX1}. Inside this neighborhood the ONLY red
edges are av, a-SX0,a-SX1, cycle04,43,31,12,25,50, and
SX0-X3,SX0-X5,SX1-X2,SX1-X4. Outside it, v is red to SY and Q,
blue to T; a is red to SY and T, blue to Q. SX union SY and T are
independent. SX0 and SX1 are red to T1,T2; SY0 is red to T0,T2;
SY1 is red to T0,T1; the omitted pairs are blue. Each SY/T-X pair,
each X/SX/SY/T-Q pair, and each Q-Q pair is free. These are ALL123
free pairs; the other108 comprise44 fixed red and64 fixed blue pairs.
Consequently d(u)=10,d(v)=10,d(a)=9, independently of free completion.
All vertices are distinct. Books are ordinary noninduced subgraphs:
edges between their pages do not invalidate a book.

## Exact degree-slack identity and tight unions

For each Xi let D_i=N_R(Xi) intersect D, D={SY0,SY1,T0,T1,T2},
and F_i=N_R(Xi) intersect Q. Its fixed degree is3 at centers0,1 and4
at leaves2,3,4,5. Every mixed edge has one center and one leaf. Its
known common red neighbor outside D union Q is EXACTLY u. Therefore

\[
d_i+d_j=7+|D_i|+|D_j|+|F_i|+|F_j|,
\quad c_R(X_i,X_j)=1+|D_i\cap D_j|+|F_i\cap F_j|.
\]

Put e_ij=3-c_R(Xi,Xj)>=0. Inclusion-exclusion gives the whole identity

\[
20-d_i-d_j=(5-|D_i\cup D_j|)+(6-|F_i\cup F_j|)+e_{ij}.
\]

All three summands are nonnegative integers. Thus every mixed degree sum
is at most20. A hypothesized sum at least20 forces equality, both FULL
unions D_i union D_j=D and F_i union F_j=Q, and a saturated red cap.
These statements use no individual X degree value.

Assume for contradiction that all four sums are at least20. Every SY/T
row into X covers both disjoint mixed stars 0-{4,5} and1-{2,3}; every
mixed edge has a full Q-row union. The elementary union budget is:
if A union B=Q and F subset Q, then
|F intersect A|+|F intersect B|=|F|+|F intersect A intersect B|>=|F|.
All unions and halfspace analogues here are ordinary CLOSED set conditions.

## Arbitrary Ti rows are forced to independent covers

B=SY union T union Q has11 points. The blue u-Ti spine, i=1,2,
has exactly10-d_B(Ti) common blue pages, because u is blue to B and
red to every other vertex. Ti has one red SY neighbor in B, no T
neighbor, and an arbitrary Q row; hence it has9-|F_Ti| blue pages.
The cap6 forces |F_Ti|>=3. This count is independent of its X row.

Let R_i=N_R(Ti) intersect X. Suppose R_i contains both endpoints of
a mixed edge. On the two actual RED Ti-X endpoint spines there are at
least FOUR known page occurrences in total: the two opposite cycle
endpoints, the leaf's own SX neighbor, and at least one occurrence of
Ti's red SY neighbor, whose X row covers that edge. Distinct pages on
each spine are counted; the same SY may occur on both spines, which only
increases the summed count. Red cap3 on each spine leaves a combined
Q intersection budget at most2. The mixed full Q union then forces
|F_Ti|<=2, a contradiction. Thus R_i covers each mixed edge but contains
no edge. Each two-leaf star is covered independently by its center or
by both leaves. The complete four choices are

\[
C=\{X0,X1\},\quad P=\{X0,X2,X3\},\quad
S=\{X1,X4,X5\},\quad L=\{X2,X3,X4,X5\}.
\]

This proves the classification for every actual Ti row, not a selected
interface or symmetry quotient.

## SX ranks remain arbitrary; the physical blue spine forces a cover

The actual BLUE SX0-SX1 spine already has SIX distinct common blue pages
v,X0,X1,SY0,SY1,T0. Thus every Q point must be red to at least one SX:
F_SX0 union F_SX1=Q. No SX degree or rank has been used.

For both actual RED SXj-Ti spines, a and R_i intersect OWN_j are known
red pages, where OWN0={X3,X5}, OWN1={X2,X4}. Consequently

\[
|F_{Ti}\cap F_{SXj}|\le2-|R_i\cap\mathrm{OWN}_j|,
\quad |F_{Ti}|\le4-|R_i\cap L|.
\]

For P/S the latter bound is2, for L it is0. All contradict the lower
bound3. Both R_1 and R_2 are therefore C. Their actual BLUE T1-T2
spine now has SEVEN distinct common blue pages
u,v,T0,X2,X3,X4,X5, violating cap6. No Q-Q completion, density terminal,
other T0 condition or independent verdict from an earlier claim is needed.

This proves the strengthened exclusion. Without X degree assumptions,
each mixed sum is at most20 by the slack identity. If all were20 the
preceding contradiction applies, so at least one is at most19. Adding
the four sums gives the stated weighted cut79.

## Complete naming, computation and trust boundary

Any repeated SX omission is named T0; the distinct SY0 and SY1 omissions
are named T1,T2 respectively. All six original versions are covered by
literal point bijections. The fixed/free incidence table transforms
bijectively on each of its231 coordinates, especially EVERY123 free pair.
This extends to all free completions and needs no host automorphism.

The source separately builds a labelled-set shell and reversed-coordinate
bit shell, then compares every original fixed/free pair, page count and
root degree. All64 X masks, all4096 arbitrary SX Q-row pairs, all3200
doubled-role known page lists, all128 u-T blue page lists, all729 full
Q covers and their64 subset budgets are retained in whole records.
The complete183708 P/S/L original-red role cells retain both actual red
page counts; no native author's generated list is input.

For the slack identity the separate actual-mask tables contain ALL1024
five-point pairs and ALL4096 six-point pairs. Their56 and84 occupancy
classes give4704 product classes. Exact multinomial multiplicities sum
to4^11=4194304 labelled cases. This is a proved membership quotient:
each coordinate has four states, and cardinalities depend only on the
four state counts. It is not4194304 individually executed graph searches.
The ordinary identity itself already proves the universal inequality.

Two actual shell-only completions have X degree words(9,9,11,11,11,11)
and(11,11,9,9,9,9), all four sums20 and no six-degree10 mark. They
demonstrate a strictly weaker degree predicate on the fixed-shell domain;
they are explicitly NOT asserted to satisfy the book caps.

The primary21-point fixture is credited literature control, not a theorem
premise or new lower bound. Integer/set/bit arithmetic and this ordinary
argument remain unformalized. No native target program/certificate/census,
solver, timeout, resource failure, old 10020 P/S conclusion or broad root
classification supplies any premise.
