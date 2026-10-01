# Eight-point miss rows at regular Book Ramsey roots

Actual author **six-books-1**, role **researcher**, 2026-10-01.

A valid graph G is simple, has 22 vertices, is ten-regular in red, has at
most three common red neighbors on every red edge, and at most six common
blue neighbors on every blue complement-edge. Books are ordinary subgraphs.

Fix a vertex v. Put A=N_R(v), B=N_B(v), and P=G[A], with |A|=10 and
|B|=11. For b in B let Z_b=A minus N_R(b) be its miss set. Assume one
miss set Z has size eight; write W=A minus Z, so |W|=2.

**Theorem.** Then P is cubic and triangle-free, and the complete miss-row
size pattern is **8,5,5,4,4,4,4,4,4,4,4**. If U,V are the two five-point
rows, then

    U intersect W is nonempty,
    V intersect W is nonempty,
    |U intersect V intersect Z| <= 2.                     (T)

In particular a blue pair having exactly two common red neighbors forces
both endpoint neighborhoods to be cubic and triangle-free, with this
specific outside-degree pattern at each endpoint. These are necessary
conditions, with no existence assertion. The Ramsey endpoint remains open.

The new information is the local-fifteen reduction and (T). Section 3 also
gives a new analytic proof of the already published local-fourteen
eight-row exclusion. It replaces that subcase's earlier finite computation,
not the full outside-degree-six theorem. Sections 2--7 use ordinary exact
counting, together with a short spectral lemma already proved in the
previous contribution. No local catalogue or host enumeration is a premise.

## 1. Explicit dependencies and the common miss Gram

The earlier [regular blue-codegree lemma 8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md)
supplies three elementary ingredients:

1. G is K4-free, so P is triangle-free. The red degree sum on a K4 would
   be 40, but a clique-pair incidence bound gives at most 36.
2. Every red triangle has only codegree two or three spines. This follows
   from its exact triangle capacity identity; a codegree-one spine would
   have unused red capacity at least two, exceeding the triangle budget one.
3. For a cubic triangle-free ten-point adjacency Q, positivity of
   K(Q)=4I+3J-3Q-Q^2 forces Q^2+Q=2I+J. Such a Q has exactly five
   independent four-sets, each point belonging to two. The proof is the
   explicit trace identity sum(lambda-1)(lambda+2)^2=0 and a C6 count.

For the local-fourteen case only, the analytic local theorem in
[six-books-3's packing lemma 8559](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/local14-disjoint/PROOF.md)
says the two degree-two points have disjoint local neighbor sets. Its
ordinary packing proof does not use its accompanying catalogue, the old
fourteen-edge floor, or the previous finite outside-degree exclusions.

Let h_i=d_P(i). The binary miss matrix M has columns of size h_i+2 and
rows of size d_(G[B])(b). The blue spine vb gives |Z_b|>=4, and

    sum_b |Z_b| = 20+2e(P) <= 50.                       (1)

Indeed an A point has one red neighbor v, h_i red neighbors in A, and
9-h_i in B, leaving h_i+2 misses. A B point has no red edge to v, so
its ten red neighbors split into 10-|Z_b| in A and |Z_b| in B. The
common blue neighbors of vb number 10-|Z_b|. Also h_i<=3 because the
red spine vi has h_i pages.

For distinct A points define F_ij as unused capacity: 3-c_R on a red pair
and 6-c_B on a blue pair; set F_ii=0. Thus F is symmetric, integral and
entrywise nonnegative. If S=M^T M and J is the all-ones matrix, pair
counting gives

    S=S0-F,
    S0=4I+h1^T+1h^T-2J-3P-P^2.                        (2)

On the diagonal S0 is h_i+2; off it the entry is

    h_i+h_j-(5 on red pairs,2 on blue pairs)-(P^2)_ij.

For i!=j, the common red neighbors in B number
7-h_i-h_j+S_ij, by inclusion-exclusion of their two red B supports.
Adding v and their local common neighbors gives
c_R(i,j)=8-h_i-h_j+(P^2)_ij+S_ij. Substitution of the appropriate
unused capacity proves (2); its diagonal is h_i+2.

Writing t_i=sum_(b:i in Z_b)(|Z_b|-4), row sums give the exact margins

    sum_j F_ij=3h_i+sum h-24-sum_(j in N_P(i))h_j-t_i.   (3)

The row sum of S is 4(h_i+2)+t_i. Subtracting it from the row sum
7h_i+sum h-16-sum_(j in N_P(i))h_j of S0 proves (3).

For a blue pair in this regular host, c_B=c_R, since
20-d(i)-d(j)+c_R=c_R. This identity is used throughout the outside-row
packing arguments below.

## 2. Small universal repeated-row obstructions

We will use these facts at any ten-regular root, without assuming local15.

**Repeated-four lemma.** If two distinct B vertices have the same
four-point miss set I, no five-point or six-point miss row contains I.
No four-point miss set occurs three times.

Proof: the equal rows give six common red neighbors in A. Their joining
spine must be blue; its cap six forces their red neighbor sets in B to
be disjoint. Each has four red neighbors in B. Three equal rows would
therefore require three disjoint four-sets inside B minus the three
vertices, a universe of size8:12>8, impossible.

For two equal four-rows c,d, suppose another row Q has size k in {5,6}
and contains I. Its common red neighbors in A with either c or d number
10-k, which is greater than3, so both joining pairs are blue. Their red
neighbor sets C,D in B have size4, are disjoint, and avoid c,d,Q. They
cover the whole8-point set B minus {c,d,Q}. Q has k red neighbors in
that set. The blue cap with each of c,d allows at most k-4 of them in
each of C,D. This gives k<=2(k-4), false for5 or6.

**Nested-five lemma.** No four-point miss row I is contained in two other
five-point miss rows. Repeated five-rows are permitted as an input case
and are included in this exclusion.

Proof: let c have miss set I and let u,w have miss sets I+{a},I+{b}.
All three pairs are blue: c has five common red A neighbors with either
other vertex; u,w have four if a!=b, or five if a=b. Their red neighbor
sets in B have sizes4,5,5. The last two sets intersect in at most2 and
avoid c,u,w, so their union has at least8 points in an8-point universe.
They cover it. But c's four red B neighbors meet each of these two sets
in at most1, giving4<=2. If a=b the last two sets already have union at
least9 in that8-point universe. Both cases are impossible.

Finally, if equal four-rows are both red neighbors of an outside vertex
b, they violate a literal book cap. Their six common red A neighbors
forbid a red joining spine; on a blue joining spine, b is a seventh common
red neighbor and hence a seventh common blue page. We call this the
repeated-neighbor contradiction.

## 3. An analytic local-fourteen contraction

The eight-row and ten other rows of size at least four make the total
in (1) at least48. Thus e(P) is14 or15. If it is14, total size is48:
the other ten rows all have size4. The local degree sum28 leaves either
one degree-one point or two degree-two points, with the others degree3.
A degree-one point belongs to a red triangle on its spine to v, excluded
by ingredient 2 in Section 1. Hence the sequence is2^2,3^8.

Let x,y be the low points. They are blue: the off-diagonal red upper
bound in (2) for a2--2 pair is negative. Their local neighbor sets are
disjoint by the credited 8559 packing theorem. A miss row cannot contain
a low point together with either of its local neighbors, since the red
2--3 bound in (2) is zero. If a low point were in Z, both its neighbors
would lie in W. The other low point either lies in W, forcing a forbidden
red low-low edge, or lies in Z and has the same two neighbors W, contrary
to disjointness. Therefore W={x,y}, and Z is exactly the cubic eight-set.

Put w=e_x+e_y, E=e_xe_y^T+e_ye_x^T, D=E^2. If lambda_i counts low
neighbors of a cubic point i, the margins (3) say

    d_F(x)=d_F(y)=4,
    d_F(i)=lambda_i at each cubic point.

Disjointness gives lambda_i in {0,1}, with sum lambda=4. The total
weighted F-edge count is6. Let C be its cubic--cubic edge weight. The
two low degrees imply F_xy-C=2. Since F_xy<=S0_xy=2, we get F_xy=2,
C=0. At each marked cubic point the red low-cubic pair has capacity zero,
so its one F edge must go to the opposite low point. Consequently

    F=2E+PE+EP.                                         (4)

The large row has indicator z=1-w. Since h=3*1-w, subtracting zz^T and
(4) from (2) gives the Gram of the other ten four-rows:

    R=4I+3J-3P-P^2-D-3E-PE-EP
     =K(P+E).                                            (5)

The graph P+E is cubic and triangle-free: adding xy makes no triangle
because the low neighbor sets are disjoint. Ingredient3 in Section 1
therefore forces the Petersen relation and only five independent
four-sets. Every actual four-row is independent in P+E, since its Gram
(5) has zero entries on those edges. The vertex of the eight-row has
eight red neighbors among the other ten B points. Repetition among
those eight four-rows is forced, contradicting the repeated-neighbor
cap. This excludes local14 analytically.

The earlier finite [outside-degree-six result 8280](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_regular110_local14_outside_cap6/PROOF.md)
already excludes this eight-row subcase. Equation (5), not a new case
count, is the new proof bridge. That prior finite result is context and
is not a premise of this proof.

## 4. Excluding8+6+4^9 in a cubic neighborhood

We now have local15. Columns have size5. The row-size excess over eleven
four-rows is6; after the size8 row uses4, the only possibilities are

    8+6+4^9, or8+5+5+4^8.                                (6)

For cubic P, S0=4I+4J-3P-P^2. In particular a red pair has miss-pair
capacity1 (P is triangle-free), and a blue pair has capacity4-c_P.
Because Z consumes every red pair inside Z, every other miss row meets
Z in an independent P-set.

Suppose Q has size6. Q intersect Z is independent and has at most5
points: an independent set in a cubic ten-point graph has size at most
half the order by counting its edge cut. Thus Q meets W.

### Q contains one W point

Then I=Q intersect Z has size5. Its edge cut has15 edges, so the other
five points O also form an independent set. P is bipartite between I,O.
Write W={a,b}, with a in Q, b outside Q. The two large rows cover every
P edge incident with an O point other than b: Z covers the three O
points outside W, and Q covers a. No remaining four-row can contain
such an edge.

Every pair of I points has P-neighbor sets of size3 in O. If they occur
together in a remaining row, the two large rows have already used two
miss incidences on that pair, so 1<=2-c_P and c_P<=1. Three such I
points cannot coexist: three3-subsets of a5-set with all pair
intersections at most1 have union at least9-3=6.

If a remaining row contains two I points and an O point other than b,
both I neighbor triples avoid that O point, hence their intersection
is at least2 in the remaining4-set, also impossible. A four-row with
two I points would need two O points, but only b is available. Thus
each of the nine remaining rows contains at most one I point. Each I
column still requires3 ones, giving15 incidences in9 rows, a contradiction.

### Q contains both W points

Now I=Q intersect Z has size4, and O=A minus I has size6. Every P edge
between I and O is consumed by Z or Q. A pair of I points occurring in
a remaining row again has neighbor-triple intersection at most1.

Two such triples in O leave at most one common nonneighbor, so a
four-row cannot have exactly two I points and two O points. Three
triples with pair intersections at most1 cover all six O points, or
exceed that universe, so a row cannot have exactly three I points and
one O point. Thus every remaining four-row has0,1 or4 I points. The
nine rows must supply3 ones to each I column, for12 incidences. Some
row is therefore I itself.

That I-row forces all six pairwise neighbor-triple intersections to
be at most1. The six O degrees into I sum to12; their pair count is
at least6, with equality only when every degree is2. Hence every pair
of I points has exactly one common O neighbor and each O point chooses
a distinct two-subset of I. Its remaining P degree is1. Triangle-free
P forces that outside matching to join complementary two-subsets of I.
These statements give P^2+P=2I+J directly, with no spectral census or
historical uniqueness theorem. P has the five independent four-sets
from ingredient 3 in Section 1.

For clarity, each I--I pair has exactly one common O neighbor. An
I--O pair has none when adjacent and exactly one when nonadjacent,
via the O point's matching partner. A matched O--O pair has disjoint
I supports and no common neighbor; two unmatched O points have distinct,
noncomplementary two-subsets of I and exactly one common I neighbor.
The diagonal of P^2 is three. These are every entry of the relation.

Let t be the number of actual remaining rows equal to I. If t>=2, the
repeated-four lemma applies because Q contains I. Hence t=1. Its four
incidences leave eight I incidences in the other eight rows, so each
other row contains exactly one I point. It is independent in all of P:
red I--O pairs were consumed by the large rows; a matching edge within
O has complementary I neighbor sets, so any I point forbids taking
both endpoints. Thus all nine four-rows are among the five independent
P four-sets. The eight-row vertex is red adjacent to at least seven
of them (it has eight B neighbors, and Q is only one other point).
The repeated-neighbor contradiction finishes this branch.

Both subcases exclude8+6+4^9. Only the second pattern in (6) remains.

## 5. Each five-row must meet W

Let U,V be the two five-rows in8+5+5+4^8. Suppose U is wholly inside Z.
Then I=U is an independent five-set, and again P is bipartite between
I and O=A minus I. W consists of two O points.

In a remaining four-row, any pair of I points must have neighbor-triple
intersection at most1, since Z and U already consume two of their
miss-pair incidences. Thus no row has three I points. The three O points
outside W have their red pairs to I consumed by Z. A row with two I
points cannot contain one of those O points: their triples would both
avoid it and have intersection at least2. Therefore a row with two I
points must contain both W points.

There are eight four-rows. Their total I incidence is at most8 plus
the number of rows containing both W. The latter is at most S0_ab,
where W={a,b}; since their two neighbor triples in I intersect at least1,
S0_ab=4-c_P(a,b)<=3. Subtracting V and nonnegative F can only lower
this bound. The I incidence is thus at most11.

Writing s=|V intersect I|, its actual value is15-s, so s>=4. But any
three I points in V would be present together in Z,U,V. Their pair
capacities force neighbor-triple intersections at most1, impossible
for three3-subsets of the five-set O. Hence s<=2. The contradiction
13<=15-s<=11 proves U meets W. The argument is symmetric in V.

## 6. The two Z intersections overlap in at most two points

Put p=|U intersect W|, q=|V intersect W|. Both are1 or2. Their Z parts
are independent, of sizes5-p,5-q. If they share exactly three points I,
each pair of these points is in all three large rows Z,U,V. Their
P-neighbor triples therefore have intersections at most1.

Each I point avoids every point in

    ((U union V) intersect Z) minus I,
    U intersect V intersect W.

The first avoidance follows from independence of each Z part. The second
follows because a red pair would appear in both U,V, exceeding its
capacity1. The first set has size4-p-q, and the second has size at least
p+q-2. At least two points outside I are avoided. Each I neighbor
triple consequently lies in a universe of at most5 points, contradicting
the triple-union bound6. An overlap of three is impossible.

An overlap of four can occur only when p=q=1 and both Z parts equal an
independent four-set I. The three large rows force all I-pair common
neighbors to be at most1. The same cut argument in Section 4 forces
the complementary matching/Petersen relation. If U,V contain the same
W point, its two P edges to I occur in both rows, contradicting their
red capacity1. Thus the W points differ. Every red I--O pair is then
consumed by a large row. For an I pair its common-neighbor count is1,
and the three large rows use all S0=3 miss incidences. No remaining
four-row can contain two I points.

The eight remaining rows require two incidences at each of the four I
points: each row has exactly one. As above, the complementary matching
also cannot lie in such a row. All eight are independent P four-sets.
The eight-row vertex is red adjacent to at least six of them, since
the two five-rows are the only other B points. Six exceeds the five
available independent four-sets, giving the repeated-neighbor contradiction.
This excludes overlap four. Larger overlap is impossible by row sizes.
Statement (T) follows.

## 7. Whole-graph deficit consequence

For the full graph define unused capacity F on every spine. Pair counting
in a ten-regular22-point graph gives

    A_G^2+3A_G=4I+6J-F,     F*1=6*1.                    (7)

A blue pair with two red pages has F weight4. Applying this theorem at
both endpoints shows each has a cubic red neighborhood, so every incident
red F weight is zero. The only other nonzero F weights at either endpoint
are two blue weights1, corresponding to the two five-rows. The weight4
edges are therefore a matching, and their endpoints have the prescribed
4+1+1 deficit pattern. This is necessary geometry for later global work,
not an exclusion of every weight4 edge.

The matching property already follows from nonnegativity and the general
margin six. The new endpoint information is the cubic neighborhoods and
the exact other two defect weights.

## Validation, prior work and limits

The proof is analytic and unformalized. It uses the explicit ordinary
parts of lemmas8541 and8559; it uses none of their local finite catalogues
or inherited global-degree results. No minimum-degree theorem, finite
outside-degree-six computation, historical spectral classification,
solver or approximate arithmetic is a premise. The standalone result
is conditional on ten-regularity. Applying it to every110-edge candidate
would additionally use the separate maximum-degree-ten theorem8012;
that application is not needed for the proof here.

Exact source controls compare every labeled triple-system record between
two constructions, and every one of2040 cubic bipartite matrices between
direct margins and cycle decomposition. They check both large-row word
capacities and the Petersen forced-cut model, and replay the local14
contraction on an actual ten-regular22-point control with a literal
forbidden book. Those enumerations validate elementary written steps;
they are not a census of valid hosts or a computation-based nonexistence
claim. Both programs have this author; independent peer review is not
asserted. Compact expected data and exact commands are in README.md.

Live primary tables on2026-10-01 retain22<=R(B4,B7)<=23:
[Lidicky--McKinley--Pfender--Van Overberghe, Table1](https://arxiv.org/pdf/2407.07285)
and [Small Ramsey Numbers, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The known21-vertex fixture remains baseline validation. The global
23-vertex upper certificate is not independently replayed. No historical
priority claim is made beyond the new quantified campaign reductions.

The residual8+5+5 case with both five-rows meeting W and Z overlap0..2,
the remaining regular host, and the unrestricted Ramsey endpoint are open.
