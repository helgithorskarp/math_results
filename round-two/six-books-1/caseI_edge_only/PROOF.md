# An ordinary edge-only exclusion of the Y-repeated specified leaf

Actual author **six-books-1**, role **researcher**, 2026-10-02.
This is an author-checked ordinary lemma. The proof below does not import
the six-interface census of9327 or a global outside degree profile. Complete
portable finite projections and a graph-free cycle audit corroborate it in
fresh normal and optimized Python. Ordinary and implementation bridges are
unformalized; new independent peer review is pending. The compact cold
reproduction and source/scope/semantic controls are complete.

All graphs are simple red graphs on22 points. On every red edge there are
at most three common red neighbors; on every blue pair, at most six common
blue neighbors. Blue is the complement on distinct points. These are
ordinary books, so colors between pages are unrestricted. Degrees are red.

**Lemma.** Suppose a degree-ten root u has this exact labeled
induced red neighborhood. Its mark0=a has global degree nine, and its other
nine points have global degree ten:

```text
0:1,8,9; 1:0; 2:6,7; 3:4,5; 4:3,7,9;
5:3,6,8; 6:2,5,9; 7:2,4,8; 8:0,5,7; 9:0,4,6.
```

If the repeated omission consists of both S_Y points in the ordinary
sole-page pair core, then e(G)>=109. No global degree assumption is made
on the eleven points outside {u} union N_R(u), and no rootlessness,
symmetry or root count is assumed. No existence or sharpness is claimed.

## Equality and normalized coordinates

Assume e(G)<=108 for a contradiction. Let v be old label1. The root
neighborhood has13 edges and global degree sum99. Its cut to B_u has
99-10-26=63 edges, so e(G)=86+e(G[B_u]). On a blue ub spine the blue
page count is10-d_(G[B_u])(b). Thus all eleven B_u degrees are at least
four. The edge assumption forces equality: e(G)=108 and G[B_u] is
four-regular. This rederives the credited equality in review9105 and9414.

The ordinary pair theorem9131 applies to the degree-ten pair u,v with
sole degree-nine common page a, without outside degree assumptions.
Let X=N_R(u) minus {v,a}, Y=N_R(v) minus {u,a}, and T the remaining
three points. Each block has eight points and two special points adjacent
to a. The special points and T are independent. Each special has exactly
two neighbors in its own block and two in T. All a--T edges are red and
the four special omissions have multiplicities2,1,1.

Write the ordinary six-point blocks as X_0..X_5 and Q=Y_0..Y_5, and the
specials as SX_0,SX_1,SY_0,SY_1. Their actual coordinates are u0,v1,a2,
X3..8,SX9/10,SY11/12,T13..15,Q16..21. The X cycle in local indices is

    X_0--X_4--X_3--X_1--X_2--X_5--X_0.

SX_0 has own pair {X_3,X_5}; SX_1 has own pair {X_2,X_4}.
Normalize T_0 as the point omitted by both SY, T_1 as that omitted by
SX_0, and T_2 as that omitted by SX_1. Then the special-to-T masks are
SX(5,3), SY(6,6). This covers all six labeled Y-repeated cores by
relabeling T and transporting every degree and edge; SX labels are kept.

Four-regularity in B_u gives SY--Q ranks2, T--Q ranks(4,2,2), and
SX--Q ranks4 from the actual SX degree ten. On red vq the page count is
4 minus q's T incidence, so the T rows cover Q. No internal-Q graph is
needed below.

## Bounds on the actual T and SY rows

Let T_t^X be the red X row of T_t, with rank R_t, and S_j the red X row
of SY_j, with rank s_j. Their actual global degrees are
d(T)=(7+R_0,6+R_1,6+R_2) and d(SY_j)=6+s_j.

For a blue pair on22 points, c_B=20-d_i-d_j+c_R. Every blue v--T
spine has exactly five common red neighbors. Hence each T degree is at
least nine, as a consequence of its actual spine, rather than an input.

Blue SY_0--SY_1 has common red neighbors v,a,T_1,T_2 plus its X and Q
intersections. Its red-codegree cap is s_0+s_1-2. Consequently

    |S_0 union S_1| >= 6 + |SY_0^Q intersect SY_1^Q|.

Thus the X union is all six points, and the two Q two-sets are disjoint.

On red SX_j--T_0, a is one common page and their Q four-sets intersect
at least twice. Therefore T_0^X avoids both SX own pairs. It is contained
in {X_0,X_1}; its degree at least nine forces exactly that pair, R_0=2.

On each red SY_j--T_t, t=1,2, the page a gives
|S_j intersect T_t^X|<=2. Because S_0 union S_1 is all X, this implies
R_t<=4. The T degree floor implies R_t>=3.

Both R_1,R_2 cannot be four. If they were, both SY intersections with
each T row would be exactly two, saturating their red caps together with a.
Each T--Q two-set must then avoid both disjoint SY--Q two-sets. Both T
Q rows equal their common two-point complement. Blue T_1--T_2 has at
least seven common red neighbors: a, both SY, at least two X points and
those two Q points. Both T degrees ten give cap six, a contradiction.
Thus (R_1,R_2) is (3,3), (3,4), or (4,3).

## Two incidence colors on the X cycle

For X_i, let c_i be its T-column rank, sigma_i its SX incidence
(zero for i=0,1, one otherwise), and C_i its nonempty subset of adjacent
SY points. The blue v--X_i bound gives c_i>=2-sigma_i. Put

    M=(2,2,1,1,1,1), k_i=c_i-M_i,
    beta_i=2-k_i-|C_i|.

Blue a--X_i has common red count3+k_i+|C_i| and cap five. Thus beta_i>=0.
Its Q rank is3+beta_i. Since C_i is nonempty, k_i<=1, and
sum_i k_i=R_1+R_2-6 is zero or one. The fixed T_0 row is {X_0,X_1}.
The minimum columns show T_1^X union T_2^X is all X, with no overlap
when the sum is zero and one overlap point otherwise.

First omit both SY and Q, leaving fourteen known points and eight outside.
Each X_i outside rank is5-k_i. On a red X-cycle edge ij, its fixed common
red page is u, together with common T points. The outside subsets have
intersection at least2-k_i-k_j. Thus the common T rank is at most
k_i+k_j. T_0 never meets both ends of a cycle edge. Therefore away from
an overlap point, adjacent X vertices have opposite T_1/T_2 labels.

If there is no overlap, these are the two labeled proper colorings of the
six-cycle, with rows(13,50) or(50,13), where a bit at i denotes X_i:
13={X_0,X_2,X_3} and50={X_1,X_4,X_5}. If there is one overlap o, deleting
o leaves a five-vertex path with either proper coloring. Both T rows
contain o; the larger row contains the first, third and fifth path points.
There are six choices of o and two colorings, making twelve such patterns.
This is lossless ordinary coverage, not an assumption that a pattern has
a host, or a quotient by an SX automorphism.

Now reveal SY. On every red cycle edge ij the common T rank is precisely
k_i+k_j. Its known red pages are u, those T points and C_i intersect C_j.
The omitted Q rows have ranks3+beta_i and3+beta_j, so their intersection
is at least beta_i+beta_j. The red cap therefore gives

    k_i+k_j+|C_i intersect C_j|+beta_i+beta_j <=2,
    |C_i union C_j| >=2.

The latter follows by substitution. There are only two SY points, so
every cycle edge has both SY labels at its ends. Equivalently each S_j
is a vertex cover of the six-cycle. The red SY--T bounds remain
|S_j intersect T_t^X|<=2 for t=1,2.

## An overlap point is impossible

If o is the unique overlap, the larger T X row has four points. Each
has a nonempty C_i and its two SY intersections have total at most four.
Thus all four columns on that row are singletons, with two of each label.
Call the label at o A. The first and fifth path points are adjacent to o,
so both have the other label B. The third path point must then have label A
to retain two labels of each type on the larger row.

The second path point is adjacent to the first (B) and third (A).
The cycle-edge union rule forces its C_i to contain both labels.
The fourth point is likewise double. The smaller T row consists of o
and these two double points, hence has three neighbors of SY_A. This
violates |S_A intersect T_small^X|<=2. Both actual larger-T choices and
all six o locations are covered by this argument.

## The disjoint three-plus-three case is impossible

Now T_1^X,T_2^X are the two alternating three-sets. Every S_j is a
vertex cover, so it has at least three points. A size-three vertex cover
of a six-cycle must be one of its two alternating sets; that would meet
one T row three times, violating the red SY--T bound. On the other hand,
the two T intersection caps give s_j<=4. Therefore s_0=s_1=4, each
meeting each T row in two points.

Each SY blue X pair is one point from each T class and is nonadjacent,
because its complementary S_j is a vertex cover. The only nonadjacent
opposite-class pairs in a six-cycle are the three opposite pairs.
The two SY blue pairs are disjoint since S_0 union S_1 is all X.
Their remaining X pair, the two double columns C_i={SY_0,SY_1}, is
therefore the third opposite pair.

But the actual SX rows force two adjacent double columns. On a red
SX_j--X_i own edge sharing a T point, u and that T point are common
red pages. Its Q rows of ranks4 and3+beta_i intersect at least1+beta_i.
The red cap gives beta_i=0. With k_i=0, this forces |C_i|=2.
For T_1^X=13 and T_2^X=50, this applies at X_2 with SX_1 and at X_5
with SX_0; X_2--X_5 is a cycle edge. For the other proper coloring,
it applies at X_4 with SX_1 and X_3 with SX_0; X_4--X_3 is a cycle edge.
Both colorings force adjacent double points, contradicting their being
an opposite pair.

All derived T rank possibilities are now absent. This proves the
Y-repeated exclusion by ordinary counting and cycle structure alone.

## Exact corroboration and boundaries

The standalone projection code rebuilds the literal neighborhood from its
old adjacency list separately from a row/bit construction. It examines all
1000 rank-filtered T row pairs, compares the complete14-point survivor list
with the independently generated fourteen cycle patterns, and tests all
91 pairs. Both whole lists are the fourteen patterns. The column producer
tests every7290 permitted SY assignment and all120 actual16-point pair
bounds; the separate literal checker starts with all57344 SY row pairs.
Both16-point domains are empty in normal and optimized Python. No unknown
Q edge, prescribed SY rank, global9/10 tag or old six-interface list is input.

The mathematical proof does not depend on this census, a checksum or a
timeout. The 30-second phase/90-second child guards and1CPU/2GiB/one-thread
limits were unchanged. Earlier private corroborations took1.200/1.282 seconds,
maximum reported cumulative child19652KiB. Final portable cold measurements
are recorded separately in the whole-leaf evidence. Receipts and generated records
remain in scratch. Normal/O counts and complete domain records agree;
the portable cold reader-facing packet and16 damage controls in both modes
are complete. See the [reader guide](README.md) and
[whole mathematical result](../leaf_edge_only_candidate/RESULTS.json).

This theorem is distinct from the older9^4,10^18 statement9327 and its
imported six-interface finite premise. Review9537's confirmation concerns
9461's old cross theorem; it does not review this new argument. The
edge-only CaseII theorem in review9414 is another sector, and is not used
to prove this CaseI theorem. New independent review is pending. No
arbitrary leaf classification, global108-edge exclusion or Ramsey endpoint
is asserted. The live primary Table1 retains22<=R(B4,B7)<=23.
