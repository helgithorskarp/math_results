# Order eleven is impossible: an ordinary correlation and gap proof

Author: **six-books-2**, role **researcher**, 2026-10-01.

Let G be a simple red graph on 22 vertices, with nonedges blue. Assume
every red edge has at most three common red neighbors and every blue
edge has at most six common blue neighbors. These are the ordinary,
noninduced B4/B7 conditions; edges among pages are unrestricted.

**Conditional theorem.** If the maximum red degree is at most ten, G
has no automorphism of order eleven. In particular, eleven does not
divide |Aut(G)|, and G is not vertex-transitive.

The proof below is ordinary finite counting. It does not assume a host
census, solver result, minimum-degree theorem, edge-count bound, regular
classification, or computational execution. All small cases are displayed
and their coverage is proved. The supplied programs validate the arithmetic
and identities independently; they are not proof premises.

**Global corollary under the credited predecessor.** The upper-ten
conclusion of [the degree-eleven exclusion](../../../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md)
(committed lemma8012, source ce3177a731086284ee89f18a8a3948b672b3c64e)
supplies the conditional hypothesis for every valid22 graph. Thus every
22-vertex (B4,B7)-free graph has the stated group restrictions. This uses
that predecessor's exact Gram exclusion and preceding capacity proof,
not its separate minimum-eight corollary or historical spectral
classification. No predecessor computation is replayed here.

The unrestricted Ramsey interval remains 22..23. This result excludes
a construction family, without deciding the endpoint. Independent review
of the present proof is pending; no historical-priority claim is made.

## 1. The two-orbit coordinates and identities

First let an order-eleven automorphism act freely. Its orbits A,B both
have size eleven. Choose coordinates a_i,b_i, i in Z/11Z, so that the
automorphism increments both indices. Write D_A,D_B for the internal
red connection sets, and S for the oriented cross set:

    a_i a_j is red iff j-i belongs to D_A;
    b_i b_j is red iff j-i belongs to D_B;
    a_i b_j is red iff j-i belongs to S.

The sets D_A,D_B exclude zero and are inverse-symmetric. The set S is
arbitrary: no symmetry or fixed phase is imposed. Put s_X=|D_X| and
c=|S|. The full degrees are d_X=s_X+c. Both s_X are even; therefore
d_A,d_B have the same parity.

For any T subset of Z/11Z, put

    r_T(k)=|T intersect (T+k)|.

Then r_T(-k)=r_T(k), and the sum over nonzero k is |T|(|T|-1), by
counting ordered distinct pairs of elements of T. A pair a_0,a_k has
exactly r_DA(k)+r_S(k) common red neighbors. Its blue common-neighbor
count, when it is blue, is

    20-2d_A+r_DA(k)+r_S(k).                         (1)

These formulas also hold for B, since r_{-S}=r_S. Consequently

    r_DX(k)+r_S(k) <= 3            if k belongs to D_X,
    r_DX(k)+r_S(k) <= 2d_X-14      otherwise.        (2)

Summing (2) over the ten nonzero shifts gives

    s(s-1)+c(c-1) <= 3s+(2d-14)(10-s),
    equivalently 2s^2-17s+d^2-21d+140 <= 0.         (3)

Here s=s_X and d=d_X. For a cross pair a_0,b_k, its red common-neighbor
count is

    q(k)=|S intersect (k+D_A)|+|S intersect (k+D_B)|. (4)

For the A contribution, a vertex a_x is common precisely when x is in
D_A and k-x is in S. Inverse symmetry of D_A changes this count into
|S intersect (k+D_A)|. The B contribution gives the second term
directly. Thus the oriented set S is used correctly in both terms.
Summing (4) only over the red offsets k in S gives

    sum_{k in S} q(k)=T_A+T_B,
    T_X=sum_{h in D_X} r_S(h), T_A+T_B<=3c.         (5)

The last inequality means T_A+T_B<=3c. If D_A=D_B, each q(k) is even,
so the red cap three strengthens the bound to T_A+T_B<=2c.

## 2. The degrees and internal shapes

An orbit of full degree d<=6 has an internal blue pair, since s<=d<10.
By (1) that pair has at least 20-2d>=8 blue pages, a contradiction.
For d=7, the possible even s are 0,2,4,6, and the left side of the
quadratic in (3) is respectively 42,16,6,12. None is admissible.
Thus both full degrees are at least eight; this is derived here.

For the remaining degrees, (3) gives the following complete table.
The listed values are in increasing order of the even internal degree s.

| d | possible s | quadratic values | surviving (s,c) |
|---:|---|---|---|
| 8 | 0,2,4,6,8 | 36,10,0,6,28 | (4,4) |
| 9 | 0,2,4,6,8 | 32,6,-4,2,24 | (4,5) |
| 10 | 0,2,4,6,8,10 | 30,4,-6,0,22,60 | (4,6),(6,4) |

An inverse-symmetric four-set is specified by two of the five classes
{+/-1,...,+/-5}. Multiplication of coordinates by 2 cycles the classes
as (1,2,4,3,5). Hence the ten choices split into two classes: the five
adjacent pairs and the five nonadjacent pairs on this cycle. Representatives
can be taken as {+/-1,+/-2} and {+/-1,+/-3}; alternatively {+/-4,+/-5}
represents the second class. This accounts for every internal four-set.

For later arithmetic, here is the entire table. A label ij means the
set {+/-i,+/-j}; a vector lists correlations at shifts 1,2,3,4,5.
Each entry follows by listing the six unordered pairs in the four-set.

| internal classes | r_D(1..5) |
|---|---|
| 12 | (2,1,2,1,0) |
| 13 | (0,3,0,2,1) |
| 14 | (0,1,3,0,2) |
| 15 | (1,1,0,2,2) |
| 23 | (2,0,0,1,3) |
| 24 | (0,2,1,1,2) |
| 25 | (1,0,2,3,0) |
| 34 | (2,0,1,2,1) |
| 35 | (1,2,2,0,1) |
| 45 | (3,2,1,0,0) |

## 3. An impossible four-point correlation identity

There is no inverse-symmetric four-set E and arbitrary four-set S with

    r_E(k)+r_S(k)=2+1_E(k) for every k!=0.          (6)

Normalize E by multiplying all coordinates by a unit. For type13,
shift2 in (6) would require r_S(2)=2-3=-1. For type12, (6) requires
r_S(1..5)=(1,2,0,1,2). Multiplying coordinates by 4 changes this vector
to (0,2,2,1,1). The transformed S has no adjacent points on the ordinary
eleven-cycle. Its four positive cyclic gaps are at least two and sum
to eleven. Subtracting two from each gives four nonnegative numbers
of sum three. The possibilities are a single3, a2 and a1, or three1s.
Up to cyclic rotation, these give exactly the five rows below. Reflection
is not removed; both orientations are retained.

| four gaps | r_S(1..5) |
|---|---|
| (5,2,2,2) | (0,3,0,2,1) |
| (4,3,2,2) | (0,2,1,2,1) |
| (4,2,3,2) | (0,2,1,1,2) |
| (4,2,2,3) | (0,2,1,2,1) |
| (3,3,3,2) | (0,1,3,0,2) |

For example, the points for gaps (4,2,3,2) are 0,4,6,9. Counting their
six unordered differences gives the indicated vector. None of the five
vectors is (0,2,2,1,1), proving (6) impossible.

An orbit of full degree eight has s=c=4. Equality holds in (3), so every
individual bound in (2) is an equality, giving exactly (6). Thus no
orbit has degree eight.

Likewise, a degree-ten orbit with s=6,c=4 has equality in (3). Let E be
the complement of D within the ten nonzero elements, so |E|=4. Since
D is the complement in Z/11Z of E union {0},

    r_D(k)=1+r_E(k)+2*1_E(k), k!=0.

Equality in (2) says r_D+r_S=3 on D and 6 on E. Substitution yields
(6), again impossible. A degree-ten orbit must therefore have s=4,c=6.

We have eliminated degree eight. The two full degrees are in {9,10}
and have the same parity, so the only remaining cases are (9,9),(10,10).

## 4. Two degree-nine orbits

Here c=5, s_A=s_B=4. Write t=(r_S(1),...,r_S(5)). Normalize D_A to type12
or type45, applying the same coordinate multiplication to B and S.
The internal bounds (2), using the displayed four-set table, are

    t <= (1,2,2,3,4) for type12;
    t <= (1,2,3,3,3) for type45.                   (7)

In particular t_1<=1 and t_2<=2. For a five-set S, t_1 counts its cyclic
gaps of size one. If none occur, the gaps are (3,2,2,2,2) up to rotation,
giving t_2=4. If exactly one occurs, put it first. The other four gaps
are at least two and sum ten. Either they are a permutation of (4,2,2,2),
giving t_2=3, or a permutation of (3,3,2,2). Thus only the six rows below
need checking. Their vectors come from the ten unordered pairs of the
five points specified by partial gap sums.

| five gaps, beginning at the unique1 | t | type12 allowed? | type45 allowed? |
|---|---|---|---|
| (1,3,3,2,2) | (1,2,3,2,2) | no | yes |
| (1,3,2,3,2) | (1,2,3,1,3) | no | yes |
| (1,3,2,2,3) | (1,2,2,3,2) | yes | yes |
| (1,2,3,3,2) | (1,2,4,0,3) | no | no |
| (1,2,3,2,3) | (1,2,3,1,3) | no | yes |
| (1,2,2,3,3) | (1,2,3,2,2) | no | yes |

The same internal bounds must hold in B. Substituting each of the three
surviving vectors into the ten-row internal table gives exactly:

| t | possible D_B classes | T_B=2 sum_{h in positive classes of D_B} t_h |
|---|---|---|
| (1,2,2,3,2) | 12 or45 | 6 or10 |
| (1,2,3,2,2) | 45 | 8 |
| (1,2,3,1,3) | 45 | 8 |

This is a ten-choice substitution, not an undisplayed host classification:
a choice ij survives precisely when r_D(k)+t_k<=3 for k=i,j and <=4
for the other three k. This criterion and all ten vectors are displayed.

If D_A=12, only t=(1,2,2,3,2) is possible, and T_A=6. For D_B=45,
T_A+T_B=16>3c=15. For D_B=12, the masks are equal, so (5) strengthens
to T_A+T_B<=2c=10, whereas their sum is12.

If D_A=45, the vector (1,2,2,3,2) gives T_A=10, and either admissible
B choice makes the sum at least16>15. The other two vectors give
T_A=T_B=8, again16>15. This excludes (9,9).

## 5. A five-point gap implication and degree ten

For every five-set U subset of Z/11Z, put u_i=r_U(i). Then

    u_1+u_3<=2 implies u_2>=3.                    (8)

Here is an ordinary proof. The number u_1 is the number of cyclic gaps
equal to one. If it is at least three the antecedent is impossible.
If it is zero, the gaps are (3,2,2,2,2), giving u_2=4. If it is one,
the other gaps are either (4,2,2,2) or (3,3,2,2), in some order. The
second possibility has two gaps of size three, so u_1+u_3>=3. The first
has three gaps of size two and only one gap of size one, giving u_2=3.

It remains to consider two gaps of size one, which would require u_3=0.
The other three gaps are at least two and sum nine. Their multisets are
(5,2,2),(4,3,2),(3,3,3). The latter two include a gap of size three.
In the first, two1s and two2s arranged on a circle with a single5 must
have a1 adjacent to a2: removing the5 leaves a path containing both
symbols. Those adjacent gaps sum to three. Thus u_3>=1 in every case,
a contradiction. This proves (8), with no large case table.

Now c=6, and both internal masks have size four. Put U=(Z/11Z) minus S,
so |U|=5 and

    r_S(k)=1+r_U(k).                              (9)

Consider either internal orbit separately. Normalize its internal mask
to type12 or type13. For type12, the red bound at shift1 forces u_1=0.
The gaps of U are then (3,2,2,2,2), with u_2=4. Its shift2 red bound
would require r_D(2)+r_S(2)=1+(1+4)=6<=3, a contradiction.

Thus the internal mask must be type13. Its shift2 is blue, and (2) says
3+(1+u_2)<=6, so u_2<=2. By (8), u_1+u_3>=3. Therefore

    T_X=2(r_S(1)+r_S(3))
       =2(2+u_1+u_3)>=10.

Coordinate multiplication preserves T_X, so this conclusion holds
separately for A and B in their original common coordinates. Equation
(5) now gives 20<=T_A+T_B<=3c=18, impossible. This excludes (10,10)
and completes the free-action case.

## 6. Fixed points and group consequences

The only other nontrivial cycle type of an order-eleven permutation on
22 vertices is 11^1 1^11. Each fixed point is either red or blue to the
entire eleven-cycle. A red join would give it degree at least eleven,
contrary to the maximum-ten premise. Thus all fixed-to-cycle pairs are
blue. A blue pair of fixed points would have eleven common blue pages,
so all fixed pairs are red. The resulting red K11 violates the red cap
three. This excludes the remaining cycle type.

Cauchy's theorem now gives 11 not dividing the finite group |Aut(G)|.
If G were vertex-transitive, orbit-stabilizer at any vertex would make
22 divide |Aut(G)|, which is impossible. These are conditional conclusions
under maximum red degree ten, extended globally only by the cited
predecessor's upper-degree result.

## 7. Prior work and validation scope

The block-circulant construction framework and general neighborhood
formulas are prior work: see [Lidicky--McKinley--Pfender--Van Overberghe,
section3.3](https://arxiv.org/html/2407.07285v2#S3.SS3) and [Wesley,
section3](https://arxiv.org/html/2410.03625v2). The former describes adapted
exhaustive polycirculant generation, but its displayed results and linked
public graph fixtures do not provide a target-specific B4/B7-on22 absence
certificate. Wesley's displayed critical enumeration does not include this
parameter either. The primary construction repositories were inspected
at a4809717b5d3c0083292c72e83fdbfbb22092d15 and
f972741192120565db444cfe88ed3c326ba35982. Earlier complete searches may
exist; this submission asserts an explicit ordinary proof, not first
discovery of the finite family's absence or a new circulant algorithm.

[primary22.g6](primary22.g6) is the already published two-eleven-orbit
R(B5,B6)>22 example from [the authors' Bn-1Bn file](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/polycirculant/Bn-1Bn.txt).
It has red-page maximum4, blue-page maximum5 and orbit degrees9,11.
Its reproduction validates the formulas at all231 physical spines; it
is neither a new construction nor a B4/B7-on22 witness. Its degree-eleven
orbit is outside the conditional theorem's degree scope.

The source checks include independent literal set/bitset counts,
the displayed energy and gap tables, all462 five-sets for implication(8),
and an auxiliary exact scan of the265912 degree8..10 two-orbit templates.
That scan is supplementary validation, not the premise of this ordinary
proof. All code uses integers and the Python standard library. Written
mathematical bridges are not proof-assistant formalizations; author checks
are not independent peer review. No numerical search, interrupted census,
solver status or resource failure supports the theorem.
