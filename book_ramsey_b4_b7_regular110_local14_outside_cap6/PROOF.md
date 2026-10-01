# Outside degrees at a fourteen-edge regular Book Ramsey root

Actual author **six-books-3**, role **researcher**, 2026-10-01.

A simple red graph G on 22 vertices is valid if each red edge has at
most three common red neighbors and each blue complement-edge has at
most six common blue neighbors. Books are ordinary, noninduced.

**Conditional theorem.** Suppose G is ten-regular and, for a root v,
J=G[N_R(v)] has degree sequence **2^2,3^8**. The red graph on the eleven
blue neighbors B=N_B(v) has every degree between **four and six**.
Its degree sequence is necessarily one of

6,6,4^9; 6,5,5,4^8; 5^4,4^7.

No existence is asserted for these three patterns. The proof excludes
size-eight miss rows analytically and the size-seven-plus-five branch
by a complete exact finite computation with a new counting constraint.
It does not exclude the remaining patterns or the full regular host.

**Fourteen-edge corollary.** In a valid ten-regular G, every root whose
red neighborhood spans fourteen edges has the same outside-degree
conclusion. This uses the credited
[positive-codegree theorem](../book_ramsey_b4_b7_regular110_positive_codegrees/PROOF.md),
source7400e3949d93733d2050118e0557d94a8a8f1625, graph8120: all red-edge
codegrees are two or three. Their sum at a fourteen-edge root is28,
so precisely two are two and eight are three. For the application to
all valid110-red-edge hosts only, the credited
[degree-ten maximum](../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md),
sourcece3177a731086284ee89f18a8a3948b672b3c64e, graph8012, supplies
ten-regularity. Neither earlier computation is a premise of the
conditional local2^2,3^8 theorem.

The [fourteen/fifteen neighborhood theorem](../book_ramsey_b4_b7_regular110_neighborhood_floor14/PROOF.md),
source d00a13612475ea701786203b280200c11a105106, graph8218, motivates
this remaining frontier. It is refined in its local14 branch, not used
as a computational premise. The Ramsey endpoint stays unresolved.

## Incidence and pair capacities

Put A=N_R(v), |A|=10, |B|=11, h_i=d_J(i), H=sum h_i=28.
For b in B put Z_b=A minus N_R(b), z_b=|Z_b|, and let M be their
binary miss-incidence matrix. Ten-regularity gives

z_b=d_(G[B])(b), column miss counts h_i+2, and sum_b z_b=48.

The blue spine vb has10-z_b common blue pages, so z_b>=4. The surplus
above eleven rows of size four is four. Thus all possibilities are
one8; one7 and one5; two6; one6 and two5; four5, with remaining rows4.

For distinct i,j in A, define epsilon_ij as unused spine capacity:
three minus full red codegree on red pairs and six minus full blue
codegree on blue pairs. It is symmetric, nonnegative integral, with
zero diagonal. Let c_ij=|N_J(i) intersect N_J(j)|. Page counting gives
S=M^T M=S0-E, E=(epsilon_ij), where

(S0)_ii=h_i+2,

(S0)_ij=h_i+h_j-(5 if ij is red,2 if blue)-c_ij.

The two low points L={x,y} are independent: a red2--2 pair has a
negative S0 entry. A red2--3 pair has S0=-c_ij, forcing c_ij=epsilon_ij
and S_ij all zero. Therefore each low point chooses a nonedge neighbor
pair P_x,P_y among the eight cubic points C. In F=J[C], let
lambda_i=3-d_F(i), so sum lambda_i=4 and e(F)=10.
All S0 entries must be nonnegative. These are necessary local data;
no unknown-host extension is assumed.

## A--B row constraints and the analytic size-eight exclusion

For a red pair ab, a in A minus Z_b, let z=|Z_b| and
t=|N_J(a) intersect(A minus Z_b)|. In the ten-point set B minus{b},
a has8-h_a red neighbors and b has z. Their intersection has at least
z-h_a-2 points. Thus full red codegree is at least t+z-h_a-2 and

z <= h_a+5-t.                                                   (1)

For a blue pair ab, a in Z_b, their common blue neighbors in A alone
number z-1-|N_J(a) intersect Z_b|. Hence

|N_J(a) intersect Z_b| >= z-7.                                  (2)

Only necessary counting inequalities are used to filter candidate rows.

Suppose z_b=8. A low point in Z_b must have both cubic neighbors
outside Z_b, since its joint-miss entry with a red neighbor is zero.
If exactly one low point is selected, the complement has only one
cubic point and cannot contain both neighbors. If both are selected,
their pairs must coincide with the two complementary cubic points;
then S0_xy=2-|P_x intersect P_y|=0, so a row missing both lows is
impossible. Thus Z_b=C. Now b is red adjacent to both low points,
has eight red B-neighbors, and a low point has six other red B-neighbors.
In B minus{b} these intersect in at least6+8-10=4 points, contradicting
the red cap three. Therefore size eight never occurs.

## A necessary double-low constraint for a size-seven row

Suppose z_b=7 and Z_b avoids both low points. Each low point has
seven red B-neighbors, including b; the other six intersect b's seven
red B-neighbors in at least three points. The full red cap is three,
so the intersection is exactly three and their union fills B minus{b}.
Every one of b's three blue B-neighbors is therefore red adjacent to
both lows. These three miss rows avoid both x and y.

Among the ten rows other than b, each low column has four misses.
By inclusion-exclusion the number missing neither low is

10-4-4+S_xy=2+S_xy.

It must be at least three, so S_xy>=1. With r=|P_x intersect P_y|,
S0_xy=2-r and S=S0-E give the additional necessary constraint

epsilon_xy <= 1-r.                                             (3)

This is an ordinary red-spine/column-count proof. It is applied only
when the selected seven-point row avoids both low points. It permits
discarding other host conditions and does not assume any symmetry.

This constraint matters: [gram_control.json](gram_control.json) is an
exact rank-five PSD residual Gram of nine binary four-point rows for
the uncut necessary system. Its two low miss columns are disjoint;
only two other rows miss neither low, and it violates(3). Thus Gram
positivity, rank and binary-row realization alone do not finish this
branch. The control is not a valid host or a Ramsey construction.

## Complete finite local-core and selected-row coverage

Up to relabeling C and possibly exchanging x,y, there are exactly three
pair alignments:01,01 (r=2);01,02 (r=1);01,23 (r=0). The corresponding
F degrees are(1,1,3^6),(1,2,2,3^5),(2^4,3^4). A relabeling normalizes
any two two-point subsets to one of these alignments; it assumes no
automorphism of G. The C-permutation stabilizers of the unordered pair
systems have sizes1440,240,192. For r=2, the low exchange is an additional
trivial symmetry of the pair system; for the other cases the low exchange
is determined by the C permutation.

[census.py](census.py) decides every forward-neighbor subset in a
prescribed-degree F, with the required pair nonedges, and retains every
nonnegative full S0. It finds1800,2765,3871 fixed-degree graphs before
the S0 filter, and1260,2400,3660 afterwards: **7320 labeled fixed-alignment
cores**. Enumerating all8! permutations identifies their complete
stabilizers and partitions them into3,15,34 orbits: **52 profiles**.
The full group action is checked to preserve the domain and cover it
without overlap. These fixed-alignment counts are not counts of hosts.

The independent [binary_audit.cpp](binary_audit.cpp) visits all **268435456**
free-edge binary words:2^27,2^26,2^26 for the three alignments.
A reflected Gray sequence flips exactly one free edge at each step;
the two endpoint degrees and adjacency rows are updated exactly.
Every free-edge word occurs once. The program checks the degrees and
literally reconstructs every ten-point S0 before retaining a graph.
Its complete retained sets equal the star generator's sets, not just
their cardinalities. No external catalogue is supplied.

The separate checker builds the stabilizer groups by closure under
explicit generating swaps, uses class-specific S0 formulas, and checks
every retained core under its normalization map. Complete comparison
additionally checks all **732000** core entries against full adjacency.

For each normalized profile, choose every seven-subset and every
five-subset of its ten points. Each candidate row must have all pair
entries in S0 at least one and satisfy(1)--(2). There are235 seven-rows
before the A--B filters and138 afterwards, containing0,1,2 low points
in99,34,5 cases respectively. Every five-row is similarly covered.
The checker selects rows instead from all1024 binary words of each
required weight and requires equality of the complete selected-pair sets.
There are **861** seven/five selected pairs after the nonnegative-entry
and incident-slack necessary filters below. The two sizes distinguish
the outside vertices; there is no ordering or distinct-row ambiguity.
Possible rows with repeated miss sets elsewhere are permitted.

## Every allowed weighted slack is indefinite

Let a,b be the indicators of the selected seven-row and five-row.
Removing them leaves nine binary rows of size four. Put

B0=S0-aa^T-bb^T, R=B0-E.

The residual Gram must be PSD, with diagonal h_i+2-a_i-b_i, row sum
four times that diagonal, and rank at most nine. The rank condition
is not used to exclude the final domain; all its matrices are indefinite.

Summing the pair formula gives, with
u_i=sum_(z:i in Z_z)(|Z_z|-4)=3a_i+b_i,

sum_j epsilon_ij=3h_i+H-24-sum_(j in N_J(i))h_j-u_i.

Thus the loopless integer weighted graph E has degrees

4-3a_l-b_l at low points,

4+lambda_i-3a_i-b_i at cubic points.

Their sum is18, or nine weighted edges with multiplicity. Each weight
is between zero and the corresponding off-diagonal B0 entry, because
R is entrywise nonnegative. When the seven-row has no low point,
the low-low capacity is additionally bounded by(3). Other constraints
on the unknown host are discarded, enlarging the necessary domain.

The generator assigns a complete weighted star before moving to the
next vertex. The separate checker assigns one edge weight at a time;
all pruning is by necessary remaining-capacity bounds. It derives
incident degrees from sum_j(B0)_ij-4(B0)_ii, not from the displayed
h/lambda formulas. In full comparison the complete weighted state
sets agree for each selected pair and all **18406600** residual entries
agree. There are **184066** matrices. Every one has a literal strictly
negative integer form q^T R q, checked by the separate implementation.

The compact certificate has **259** distinct primitive ten-coordinate
integer vectors,268 profile references, maximum absolute entry884.
The checker validates integer type, primitive normalization, profile
coverage and references; then it computes every strict negative form.
A Gram cannot have a negative form. Hence the entire seven-plus-five
branch is impossible. Combined with the analytic size-eight exclusion
and the exhaustive surplus-four partition, the three degree patterns
in the conditional theorem follow.

## Credit, literature and trust boundaries

The local Gram and incident-slack identities continue the credited
regular-root framework at [graph8170](../book_ramsey_b4_b7_regular110_local13_outside_degrees/PROOF.md)
and [graph8218](../book_ramsey_b4_b7_regular110_neighborhood_floor14/PROOF.md).
Weighted-star and exact form-recovery functions, and the separately
implemented individual-edge recursion, are copied with provenance from
our source d00a13612475ea701786203b280200c11a105106; that source credited
their earlier implementation at5ac6c693382a19253fa867f91d74f112e015a3a1.
The new census is on eight cubic points, with two low points, the new
A--B filters, the proved double-low cut and the seven-plus-five exclusion.
Reproducing older tools and the known baseline is validation, not novelty.

The [independent positive-codegree audit](../book_ramsey_regular110_review4/REVIEW.md)
by six-reviewer-4, source2188810844c37533ed2cea41b55a0838993459ab, graph8190,
confirms that corollary premise. The newer
[independent local13 audit](../book_ramsey_local13_outside_review4/REVIEW.md),
source e291f436e56c9eaf89befd162d2b911f12e40353, graph8226, confirms
the earlier one6 exclusion and supplies universal real-slack
simplifications there. It does not review this local14 computation;
the one6 computation is not a premise of the conditional theorem here.
The independent degree-eleven audit at8060 confirms the110-edge premise.
The [independent fourteen-edge-floor audit](../book_ramsey_floor14_review2/REVIEW.md)
by six-reviewer-2, source653b98c3992de1cfe47ef27226c40207b17de471,
graph8244, confirms all1,747,161 matrices of the earlier two5 exclusion
and the resulting fourteen/fifteen theorem. That audit also derives
blue-deficit constraints. It is context and confirmation of graph8218,
not a review or a premise of the new conditional local14 theorem.

Both present implementations are by six-books-3; they are not independent
peer review. Incidence, row constraints, relabeling, complete coverage
and the new counting cut are written mathematics, not proof-assistant
formalizations. The binary-word completeness relies on the small C++
program and its compiler; weighted exclusions use exact Python integers.
No floating arithmetic, solver status, incomplete prefix, timeout,
UNKNOWN, memory kill, hidden corpus or historical graph classification
supports an exclusion. No actual22-vertex witness is asserted.

Located primary literature still gives22<=R(B4,B7)<=23:
[Lidicky--McKinley--Pfender--VanOverberghe, Table1](https://arxiv.org/html/2407.07285v2)
and [Small Ramsey Numbers, DS1.18 TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
reopened live2026-10-01. The included red21 fixture is the complemented
[known primary matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt),
reproduced exactly as validation. The general flag-algebra upper
certificate was not replayed. Historical priority of these local
refinements is not established by a bounded literature refresh.
