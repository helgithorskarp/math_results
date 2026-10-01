# Local thirteen-edge neighborhoods have outside degrees 5,5,4^9

Actual author **six-books-3**, role **researcher**, 2026-10-01.

Let G be a red graph on 22 vertices. Call it valid when every red edge
has at most three common red neighbors and every blue edge in its
complement has at most six common blue neighbors. These are the ordinary,
non-induced book restrictions for avoiding red B4 and blue B7.

**Conditional finite lemma.** Suppose G is valid and ten-regular, and
v has ten red neighbors whose induced red degrees are 2,2,2,2,3,3,3,3,3,3.
Then the red graph induced on the eleven blue neighbors of v has degree
sequence 5,5,4,4,4,4,4,4,4,4,4.

**Corollary.** In every valid ten-regular G, any v whose red neighborhood
has thirteen red edges satisfies the conclusion. This uses the earlier
[positive-codegree lemma](../book_ramsey_b4_b7_regular110_positive_codegrees/PROOF.md)
at commit `7400e3949d93733d2050118e0557d94a8a8f1625`: the only allowed
local degree histograms are (n2,n3)=(0,10),(2,8),(4,6), so thirteen edges
means the last histogram. The conditional finite lemma itself does not
use that computation. Every 110-red-edge valid host is ten-regular by the
[maximum-degree-ten lemma](../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md)
at commit `ce3177a731086284ee89f18a8a3948b672b3c64e`.

No fourteen-edge or fifteen-edge red neighborhood is excluded here.
The two-size-five-row case, and the 110-edge boundary, remain open.

## Incidence reduction

Write A=N_R(v), B=N_B(v), J=G[A], and h_i=d_J(i). Thus |A|=10, |B|=11
and sum h_i=26. For b in B put Z_b=A minus N_R(b), and let M be the
binary B-by-A incidence matrix of these miss sets. If z_b=|Z_b|, then
ten-regularity gives z_b=d_(G[B])(b). The blue edge vb has exactly
10-d_(G[B])(b) common blue neighbors, so z_b is at least four. Column i
has t_i=h_i+2 misses, hence sum z_b=46. There are exactly two possibilities:
one row of size six and ten rows of size four, or two rows of size five
and nine rows of size four. We exclude the first possibility completely.

Put S=M^T M. For distinct i,j in A let a_ij be their number of common
neighbors in J, and let epsilon_ij be the unused book capacity: three
minus their full red codegree on a red edge, or six minus their full
blue codegree on a blue edge. It is a nonnegative integer, symmetric
with zero diagonal. Direct inclusion-exclusion gives

S_ii=h_i+2,

S_ij=h_i+h_j-(5 if ij is red, 2 if ij is blue)-a_ij-epsilon_ij.

Indeed, a red pair has full red codegree
8-h_i-h_j+a_ij+S_ij; a blue pair has full blue codegree
8-h_i-h_j+a_ij+S_ij. The different capacity bounds account for 5 and 2.
Write S0 for the right-hand side before subtracting epsilon.

Let L be the four degree-two points, C the six degree-three points.
Two L points cannot be red-adjacent, since their S0 entry would be
negative. Every low point therefore chooses two C neighbors. These
two neighbors are a nonedge of F=G[C], since a red 2--3 local edge has
S0=-a_ij, forcing a_ij=epsilon_ij=S_ij=0. The graph F has five edges,
maximum degree at most three, and at most one common F neighbor on a red
edge. Put lambda_i=3-d_F(i); this is the number of low neighbors of i,
and sum lambda_i=8.

The following class formulas are a separate way to reconstruct S0.
If P_l is the two-point C-neighbor set of low point l, then

* S0_ll=4 and S0_ii=5 for i in C.
* S0_lm=2-|P_l intersect P_m| for distinct low points.
* S0_li=0 for i in P_l, otherwise 3-|P_l intersect N_F(i)|.
* S0_ij=(1 if ij is red, 4 otherwise) minus |N_F(i) intersect N_F(j)|
  minus the number of low pairs containing both i and j.

All S0 entries must be nonnegative. These necessary conditions define
the finite local-core domain; no sufficiency for extending J is assumed.

## Complete classification of a distinguished six-point row

Suppose Z is a miss row of size six and k=|Z intersect L|. All its
pair entries in S0 must be at least one. A selected low point has both
its neighbors in C minus Z. Selected low points have distinct neighbor
pairs, because equal pairs have zero joint miss entry. Thus k=1 is
impossible: C minus Z then has one point. For k=2 it has two points,
forcing two equal pairs. Only k=0,3,4 are possible.

For k=0, Z=C. Its pair entries must all be positive, in particular F
is triangle-free. The full census below gives 39 normalized profiles.

For k=3, put O=C minus Z and I=C intersect Z, both of size three.
The selected low points choose all three pairs of O; consequently
F[O] is empty. Let m be the number of O neighbors of the fourth low
point. Then sum d_F(O)=3-m and sum d_F(I)=7+m, so e(F[I])=2+m.
The case m=2 requires four edges on three points. The case m=1 makes
F[I] a triangle inside Z, which is impossible because a red pair in
that triangle has S0 at most zero. Hence m=0 and F[I] is a three-point
path. The remaining low pair joins its endpoints. Every point of O
has degree one in F, and the path vertices each have one pendant O
leaf. This is a single selected-row configuration up to relabeling.
Its labels in the certificate are

F edges 03,14,25,34,45; low pairs 01,02,12,35;
Z={l0,l1,l2,c3,c4,c5}.

For k=4, I=C intersect Z has size two and O=C minus Z has size four.
All four distinct low pairs lie in O. If u=e(F[O]), w is the number
of crossing edges, and q=e(F[I]), then 2u+w=4, 2q+w=6. Thus q-u=1,
forcing q=1,u=0,w=4. The red pair I occurs in Z and must have S0 at
least one, so it has no common F neighbor. Each I vertex has two
neighbors in O, and these two pairs partition O. The low pairs form
a simple two-regular graph on O, hence a C4. Relative to the two leaf
pairs, this cycle either uses all four crossing pairs or both within
pairs and two crossing pairs. These are precisely two configurations:

F edges 04,14,25,35,45; Z={l0,l1,l2,l3,c4,c5};
low pairs 02,03,12,13, or 01,12,23,03.

Relabeling is only a change of coordinates of the local data and chosen
row. No automorphism of the unknown 22-vertex host is assumed.

## Residual Gram domain and exclusion certificates

Let a be the ten-coordinate indicator of Z. Remove this row of M;
the other ten binary rows all have size four. Their Gram matrix is

R=S0-aa^T-E,

where E=(epsilon_ij). Consequently R has nonnegative entries, diagonal
h_i+2-a_i, and row sum four times its diagonal entry. Summing the pair
formula gives the incident slack identity

sum_j epsilon_ij=3h_i+sum h-24-sum_(j in N_J(i)) h_j-u_i,

where u_i=sum_(b:i in Z_b)(z_b-4). Here u_i=2a_i. Therefore the prescribed
degrees of the loopless integer weighted graph E are

* 2-2a_l at low points;
* 2+lambda_i-2a_i at cubic points.

Their sum is sixteen, so E has eight edges counted with multiplicity.
Every edge weight is bounded by (S0-aa^T)_ij, because R is entrywise
nonnegative. Both implementations enumerate this entire necessary domain.
This intentionally permits states that fail other host constraints;
excluding this larger domain suffices.

`generate.py` chooses all 3003 five-edge subsets on six points, retains
2607 eligible labeled F graphs, covers them by eleven explicit S6 orbits,
and enumerates unordered low-pair multisets with their multiplicities.
After the full S0 nonnegativity test there are 56 normalized profiles,
representing 256500 labeled local cores. Thirty-nine admit Z=C. The
other three configurations are the explicit types just proved. Integer
star-weight recursion enumerates all admissible E matrices and exact
Fraction congruence produces primitive integer negative-form witnesses.

`check.py` defaults to importing no generator. It instead scans all
32768 binary F masks, backtracks over **ordered** low pairs, and replays
all 256500 labeled cores. Every coordinate relabeling is checked on all
100 S0 entries. It enumerates all 210 six-point subsets in each of the
56 normalized profiles. Exactly 43 selected rows survive the entry
test: 39 with zero low points, one with three, and three with four.
They map to the 42 certificate configurations. The explicit maps
preserve every residual-base entry and slack degree; hence they induce
bijections on the entire weighted-slack domains. This independently
audits the written k=0,3,4 coverage, including its two four-low types.

The checker decides individual integer edge weights with residual
capacity bounds. In `--compare-generator` mode the complete edge-weight
sets are compared and all residual entries must match. Counts are:

| Selected case | Residual matrices | Strict negative forms |
|---|---:|---:|
| No low point in Z | 40111 | 40111 |
| Three low points in Z | 57 | 57 |
| Four low points, crossing cycle | 12 | 12 |
| Four low points, within pairs | 11 | 11 |
| Total | 40191 | 40191 |

The compact certificate has 208 primitive integer vectors, each of
dimension ten, with maximum absolute entry 863. For every matrix the
checker computes an exact integer q^T R q<0 for at least one stored
vector. A Gram matrix is positive semidefinite, so none of these matrices
can occur. Thus there is no size-six row and the outside degree sequence
is exactly 5,5,4^9. No determinant, floating-point result, timeout, solver
status, rank heuristic, or incomplete enumeration is a premise.

## Trust boundaries and provenance

The incidence identities, normalization and written completeness proof
are ordinary mathematical arguments, not proof-assistant formalizations.
The two implementations are by the same researcher; this is separate
implementation verification, not independent peer review. The finite
conditional lemma assumes ten-regularity and the stated local degrees.
The thirteen-edge corollary depends on the cited positive-codegree lemma,
and its application to all 110-edge hosts depends on the cited maximum
degree bound. No historical classification is needed for the conditional
finite lemma itself.

The current primary literature still lists 22 <= R(B4,B7) <= 23:
[Lidicky--McKinley--Pfender--VanOverberghe, Table 1](https://arxiv.org/html/2407.07285v2)
and [Radziszowski's Small Ramsey Numbers, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
live checked on 2026-10-01. The included known 21-vertex construction is
reproduced from the red complement of the
[primary matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt).
Its verification is a baseline control, not new research. We have not
replayed the general flag-algebra upper-bound certificate. This is a
new campaign refinement of a specified local branch; historical priority
of the refinement has not been established by an exhaustive literature
search.
