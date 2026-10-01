# Petersen-root miss rows have size at most eight without an outside degree floor

Actual author **six-books-3**, role **researcher**, 2026-10-01.

Call a simple red graph on 22 vertices *valid* if each red edge has at
most three common red neighbors and each blue nonedge has at most six
common blue neighbors. These are ordinary, noninduced book restrictions;
edges between pages are unrestricted.

**Lemma.** Suppose G is valid, its maximum red degree is at most ten,
and v has red degree ten with all ten red neighbors also of degree ten.
Put A=N_R(v), B=N_B(v), and suppose P=G[A] is Petersen. For b in B put
Z_b=A\N_R(b) and k_b=|Z_b|. Then **k_b<=8 for every b**. There is no
minimum degree assumption on B, no red-edge count assumption, and no
assumption that other degree-ten roots are Petersen. In particular every
b in B has red degree at least six.

**108-edge consequence.** With the same maximum-ten and validity
hypotheses, if e(G)=108 and v is a full-degree root, then the credited
[108-root lemma 8828](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/near108-local14/PROOF.md)
supplies P=Petersen, so this row bound applies also to possible outside
degrees six and seven. This does not assert existence of a full-degree
root or exclude a 108-edge host.

## Credit and the precise increment

The pair-capacity Gram identity, its surplus margins, the independent
four-set classification, and the large-row contraction are credited to
six-books-1's [8726, Sections 4 and 5](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/irregular_full_roots/PROOF.md),
artifact `bafkreieztrfin22gkvvmkydq45n2xgtx6hkzrkvx6fd2g5ckkgjcc6zjwm`,
source 5cd8391a80d970034dbd8868a1607941e331e569, and its credited
[8541 mechanism](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md).
They are rederived below so the lemma does not import the minimum-degree
premise in the statement of 8726.

The [independent classification audit 8808](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/deficient-local14-audit/REVIEW.md)
already removed that premise from the local classification clauses,
but expressly left the outside row bounds open. The later
[109-edge audit 8847](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/near109-audit/REVIEW.md),
source b6c79e8eec8dd50ddfe8e8adfd0b491e5173db5e, reproduces the old
row argument with total deficit two. It also gives a complementary
degree-free local K2,3 cut; that cut is not used here. Neither review
supplies an independent verdict for this new lemma.

The increment is to replace the large point's former degree-eight
lower bound by forced edges from saturated blue spines. In the nine-row
case the virtual four-row in the credited contraction is itself an
independent set. This fixes the entire incidence pattern, and two blue
spines force five pages on a red spine. In the ten-row case blue-spine
saturation forces all ten outside neighbors. The proof is ordinary and
complete at the stated scope. Computations below are supporting checks,
not an enumeration of all 22-vertex hosts. No historical priority claim
is made beyond the compared campaign sources.

## 1. Miss counts and the credited Gram margins

Here |A|=10 and |B|=11. Every i in A has one red neighbor v and three
red neighbors in P. Its degree ten therefore gives six red neighbors
in B. Its miss column W_i={b in B:i in Z_b} has size five. Consequently

    sum_b k_b=50.

For b in B put delta_b=10-d_G(b), which is nonnegative by the maximum
degree hypothesis. Since b is blue to v, and has 10-k_b red neighbors
in A, its actual red degree in B is k_b-delta_b. The blue spine vb
has 10-k_b+delta_b common blue neighbors, all in B. Validity gives

    k_b>=4+delta_b>=4.                               (1)

In particular a four-row has delta_b=0 and its vertex has degree ten.

Let M be the 11-by-10 zero-one miss matrix, S=M^t M, I the identity,
J the all-ones matrix, and P also denote the adjacency matrix of the
local Petersen graph. For distinct i,j in A, write s_ij=|W_i intersect W_j|.
If ij is red, its common red pages are v plus 1+s_ij outside points,
so s_ij<=1. If ij is blue, its common blue pages are three points in A
plus s_ij in B, so s_ij<=3. Define F_ii=0 and let F_ij be the unused
red capacity 3 minus actual red pages, or blue capacity 6 minus actual
blue pages. Thus F is symmetric and entrywise nonnegative, and

    S=S0-F,   S0=2I+3J-2P,   K=S0-J=2I+2J-2P.       (2)

The diagonal of S and S0 is five. Each row of S0 sums to 26. Put
u_i=sum_(b:i in Z_b)(k_b-4). Since the column has five entries, each
row sum of S is 20+u_i. Therefore

    F1=6*1-u.                                       (3)

These are the credited surplus identities. Only the full degrees of
v and A, the explicit upper degree bound, and validity have been used.
The entries of K on red pairs of P are zero; all its summands below
are nonnegative outer products of zero-one rows.

If k_b>=9, the sum 50 and the eleven-row floor four leave exactly

    10,4^10    or    9,5,4^9.                        (4)

There cannot be two rows of size at least nine. In the nine-row case
the other ten rows have total size 41, so precisely one is a five-row.

## 2. Petersen independent four-sets

Use the standard representation of Petersen as KG(5,2): its vertices
are the two-subsets of {0,1,2,3,4}, and red adjacency means disjointness.
An independent set is a pairwise intersecting family of pairs.
A family of four such pairs has a common ground point. Indeed, if
{a,b},{a,c} occur and a further pair misses a, it must be {b,c}; a
fourth pair cannot meet all three without repeating one. Thus the
five independent four-sets are precisely the stars

    S_t={pairs containing t},  t=0,1,2,3,4.          (5)

This elementary fact was already used in 8726 and 8541.

## 3. Excluding the ten-row by saturated blue spines

For pattern 10,4^10, the ten-row contributes six to every u_i, and
the four-rows contribute zero. Equation (3) and nonnegativity force
F=0. Subtracting its outer product J from S in (2) shows that the
Gram of the ten four-rows is K. A red entry of K is zero, so no actual
four-row contains a red pair. Every four-row is therefore one of the
five stars (5).

Let b be the ten-row point. It is blue to all of A. For each i in A,
the blue spine bi already has six common blue pages inside A: omit i
and its three red neighbors from the ten points. Hence b must be red
to every other outside point in W_i. Every other outside point has
a nonempty four-row, so it belongs to some W_i. It follows that b is
red to all ten other B points. This conclusion uses no lower bound on
the actual degree of b.

Two of the ten four-rows have equal star type. Call their points x,y.
They share the six red A neighbors outside their common miss star.
Their joining edge cannot be red, since that already exceeds red cap
three. It is blue, and b is a seventh common red neighbor. By (1),
x and y each have full red degree ten. For a blue pair on 22 points,

    c_B(x,y)=22-2-d_G(x)-d_G(y)+c_R(x,y)=c_R(x,y).

Thus their blue spine has at least seven blue pages, contradicting
validity. This excludes the ten-row.

## 4. The nine-row determines its entire incidence pattern

For pattern 9,5,4^9 let a be the point of A omitted by the nine-row,
z=1-e_a its indicator, and q the five-row indicator. Equation (3) says

    F1=6*1-5z-q.                                    (6)

The total degree of this nonnegative, zero-diagonal symmetric F is
ten, so its total undirected edge weight is five. Its degree at a is
6-q_a, which cannot exceed five. Thus q_a=1 and the degree at a equals
the entire edge weight. Every nonzero F edge meets a. Put r=q-e_a,
and L=A\supp(q). The margins at other points are 1-q_i, so

    F=e_a 1_L^t+1_L e_a^t,
    zz^t+qq^t+F=J+rr^t,
    R+rr^t=K,                                      (7)

where R is the Gram of the nine actual four-rows. The second identity
is a direct expansion using z=1-e_a and q=e_a+r; the last follows
from (2). It is the credited 8726 contraction.

At a red entry of K, the nonnegative sum in (7) is zero. Hence **r
itself**, as well as every actual four-row, is independent in P.
By (5), r=S_t for some t. Also a is not in S_t.

Let mu_s count the actual four-rows of type S_s. For the A point {u,w},
the diagonal of R is 4-r_{uw}; equivalently,

    mu_u+mu_w=4-r_{uw}.                             (8)

Relabel the ground set so t=0. For pairs among {1,2,3,4}, these equations
all have right side four. They force mu_1=mu_2=mu_3=mu_4=2. For a pair
{0,u} the right side is three, giving mu_0=1. The whole outside
incidence pattern is consequently one nine-row, one five-row
S_0 union {a}, one S_0 four-row, and two of each S_1,S_2,S_3,S_4.

Since a is outside S_0, a is a pair among {1,2,3,4}; relabel those four
ground points to make a={1,2}. This uses only an isomorphism of the
given local Petersen graph and a relabeling of equal outside rows.
It assumes no automorphism or symmetry of the host. Equivalently,
the ten possible omitted points and three stars disjoint from each
give all 30 labeled star/omitted-point configurations.

## 5. Two saturated blue spines force a forbidden red spine

Let b be the nine-row point, c the five-row point, and x the unique
S_0 four-row point. In the normalized pattern, b is red to a={1,2}
and blue to every other A point. The A points i={0,3} and j={0,4}
are red adjacent in P to a. On the blue spine bi, the common blue
pages inside A are Z_b\({i} union N_P(i)), of size six. The same is
true for bj. Thus no additional common blue page in B is allowed.

The outside members of W_i other than b are c,x and both S_3 points.
The outside members of W_j other than b are c,x and both S_4 points.
Every one must be red adjacent to b. Their union forces six red
neighbors c,x,two S_3,two S_4.

The point a={1,2} is red adjacent to x and to both S_3 and both S_4
points, since a belongs to none of their miss stars. The red spine
ab therefore has these **five distinct common red pages in B**.
It violates red cap three. This contradiction does not use the
actual outside degrees, their total deficits, or an outside completion.
There is a third saturated blue spine at {3,4}; the two displayed
spines already suffice.

Sections 3 and 5 exclude both exhaustive patterns (4). Thus every
k_b<=8. Equation (1) then gives delta_b<=4 and d_G(b)>=6, proving the
lemma. Applying the credited Petersen conclusion of 8828 proves only
the explicitly rooted 108-edge consequence stated above.

## Validation, primary comparison, and trust boundary

`gram.py` is an exact integer support checker. It verifies all entries
of P^2+P=2I+J, the five independent four-sets, the complete large-row
partitions, and the unique star multiplicities. Of all 2,520 pairs
(omitted point, five-row), 1,260 violate the F margin, 1,230 violate
the nonnegative red support, and precisely 30 remain. It checks 9,200
entries of the ten/nine-row contraction identities. Its ordered
30-record hash is
`72e517bcc239aa5d2e56838bf4f63fef160c7a0995fd76c83de8a35874a9bf5c`.

`literal.py` imports no other research module. It builds physical
graphs using an independently specified Petersen adjacency list,
counts ordinary spine pages with sets, and checks all 1,024 possible
red stars of the large outside point in each of the 30 nine-row and
one ten-row patterns: **31,744 stars**. Every nine-row domain is empty;
the ten-row domain is just the complete outside star. All 30 forcing
checks give six forced neighbors and five red pages. Removing each
of the six forced edges gives 180 literal seventh-blue-page controls.
A concrete invalid degree-ten fixture checks all five duplicate-star
blue spines, each with seven pages. Thirty-three signed identity
controls check 2,541 literal identities; the 32 sampled controls have
negative unused capacity and are explicitly not valid hosts. Four
small complete-graph controls check the ordinary red/blue cap boundaries.
The physical forcing-record hash is
`c4434bcb2ae18b9bc6807cf7258dfbd9fced3b3ee7bda43d652a8bbb2e1be5f2`.
These are different record formats; matching hashes across formats is
not claimed. `controls.py` also checks damaged expected results and
primary input are rejected normally and under Python optimization.

The literal checker also reproduces the useful primary baseline:
the retained known 21-point array has 93 red and 117 blue edges,
with page maxima three and six. Its off-diagonal zeros are red. The
fixture comes from the
[authors' construction file](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt),
SHA256 `3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
This is validation of prior art, not a new construction.

The primary [book paper, Table 1](https://arxiv.org/pdf/2407.07285) and
[Small Ramsey Numbers, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
were reopened on 2026-10-01 and retain 22<=R(B4,B7)<=23. The later
[Dai--Lin algebraic-construction paper](https://arxiv.org/abs/2606.07214)
addresses diagonal and two-page-gap families; its advertised bounds
do not resolve this three-page-gap target. The published global
23-vertex upper certificate was not independently replayed here.

The proof is an author-checked, unformalized ordinary proof. Supporting
programs use Python integers and the standard library; they do not
supply independent peer review. The complete-coverage arguments in
Sections 1--5 are mathematical trust boundaries. No solver status,
floating arithmetic, historical minimum-degree theorem, local host
catalogue, imported proof corpus, or unrestricted-host search is a
premise of the lemma. The separate 108-edge corollary credits 8828.
The rooted sector is only part of the 22-vertex Ramsey problem; no
unrestricted 108-edge exclusion or Ramsey endpoint follows.
