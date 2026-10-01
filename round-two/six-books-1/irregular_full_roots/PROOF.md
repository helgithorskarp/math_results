# Petersen rigidity at full-degree roots of irregular Book Ramsey graphs

Actual author **six-books-1**, role **researcher**, 2026-10-01.

A valid graph is a simple red graph on 22 points with at most three common
red neighbors on each red edge and at most six common blue neighbors on
each blue nonedge. These are ordinary, noninduced book restrictions.

**Theorem.** Suppose G is valid, all its degrees belong to {8,9,10}, and
G is not ten-regular. Call v a *full-degree root* if v and all ten of its
red neighbors have degree ten. If such a root exists, then:

1. G has 107, 108 or 109 red edges.
2. The induced red graph P on the ten red neighbors of every full-degree
   root is Petersen or Petersen with one edge deleted. At 107 red edges
   it must be Petersen.
3. For B=N_B(v), write Z_b=N_R(v) minus N_R(b), k_b=|Z_b| and
   delta_b=10-d_G(b). Then d_(G[B])(b)=k_b-delta_b and
   k_b>=4+delta_b. Every k_b is at most eight in the Petersen case and
   at most seven in the edge-deleted Petersen case.

**109-edge consequence.** Every valid G with 109 red edges has such
roots. Its degree sequence is either 10^21,8 or 10^20,9^2. In the first
case exactly thirteen full-degree roots exist. In the second there are
at least two; if the two degree-nine points are red adjacent, at least
four exist. Every one has the local structure and row bounds above.

The degrees8..10 assumption in the theorem is explicit. For the
unconditional 109-edge consequence, it is supplied by the credited
[maximum-degree theorem 8012](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md),
artifact `bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi`.
No nonexistence claim is made for 109 edges or for an irregular graph.

## Credited mechanisms and the precise increment

The local pair-count and clique-degree identities originate in
[8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md),
artifact `bafkreieph2tyeefsbslbsfvs2jtv546shufx4ar3stjhca5c72lql37o4a`.
The packing proof for two degree-two points is credited to six-books-3's
[8559](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/local14-disjoint/PROOF.md),
artifact `bafkreihrw6fz7nozp5m5g2s5hnmeqkyte6taxfejvjk6gowwkepulvc4z4`.
The cubic four-column obstruction is credited to six-books-3's
[regular110 proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/regular110-exclusion/PROOF.md),
source commit 8f1d8fad8a130c3b01fced51959147dc79e6b28c.
The eight-row contraction is the analytic part of
[8621](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_eight_miss_rows/PROOF.md),
artifact `bafkreiahiz6epzvowfeqssgvekewr2bjre4ld5gt2caexsjecyu4rok4ju`.

The increment is their extension to irregular full-degree roots, the
ordinary elimination of both thirteen-edge profiles at those roots,
the edge-deleted Petersen identification, and the outside row bounds
with degree deficiencies. In particular, the packing proof works for
any number of local degree-two points. No earlier finite
positive-codegree, neighborhood-floor, nine-core or outside-star
enumeration is imported. Hall's classification is not a premise here.

## 1. Exact local identities with deficient outside points

Put A=N_R(v), B=N_B(v), with sizes ten and eleven, and P=G[A]. Write
h_i=d_P(i), H=sum_i h_i and Delta=sum_x(10-d_G(x)). Every deficient
point lies in B. Since v and all A points have degree ten, elementary
degree counting gives, with W_i=B minus N_R(i),

    |W_i|=h_i+2,
    d_(G[B])(b)=k_b-delta_b,
    k_b>=4+delta_b,
    sum_b k_b=H+20>=44+Delta.                         (1)

The last inequality follows from the blue spine vb: its common blue
neighbors number 10-k_b+delta_b, which is at most six. The red spine
vi gives h_i<=3. Therefore H<=30 and Delta<=6. Delta is the positive
even integer 220-2e(G), so Delta belongs to {2,4,6}. In particular
H>=26; if Delta=6, H=30.

For distinct i,j in A put c_ij=|N_P(i) intersect N_P(j)| and
s_ij=|W_i intersect W_j|. Their literal red or blue pages give

    s_ij<=h_i+h_j-5-c_ij  if ij is red,
    s_ij<=h_i+h_j-2-c_ij  if ij is blue.               (2)

These inequalities require only the full degrees of the A points;
the degrees of B points need not be ten. A red pair's common red
neighbors number 8-h_i-h_j+c_ij+s_ij. A blue pair has the same
expression for its common blue neighbors, counting A and B directly.

P is triangle-free. A triangle in P together with v would be a red K4
of four degree-ten points. For a red four-clique T, each of its six
spines already has two clique pages; hence
sum_(x outside T) binom(|N_R(x) intersect T|,2)<=6. The integer inequality
t<=1+binom(t,2), for 0<=t<=4, bounds the number of red edges from T to
its other eighteen points by 24. Thus sum_(a in T)d_G(a)<=12+24=36,
contrary to 40. This is the generic clique count of 8541.

All s_ij are nonnegative. A local degree-one point would have a red
neighbor of local degree at most three, making its red upper bound in
(2) negative. Two local isolated points would have a negative blue
upper bound. The even degree sum H>=26 consequently gives precisely
the following necessary profiles:

    3^10;  2^2,3^8;  2^4,3^6;  0,2,3^8.             (3)

## 2. Packing eliminates four degree-two points

Two local degree-two points x,y are blue: the red upper bound in (2)
would be negative. Every neighbor of such a point has local degree
three. Suppose x,y have r>=1 common local neighbors, and choose one p.
The red 2--3 upper bounds force W_p disjoint from both W_x and W_y.
The blue xy bound gives s_xy<=2-r. Hence

    11>=|W_x union W_y union W_p|
       =4+4+5-s_xy>=11+r>11,

a contradiction. All degree-two points therefore have pairwise
disjoint local neighbor sets. This is the ordinary 8559 mechanism,
with its original two-low-point hypothesis removed: every common
neighbor p is cubic because a red 2--2 pair is already impossible.

In the profile 2^4,3^6, four two-point neighbor sets would need eight
distinct cubic points, but only six exist. This profile is impossible.

## 3. Four columns eliminate every local four-cycle

For any four-set L in A put t_b=|Z_b intersect L| and
H_L=sum_(i in L) h_i. The column counts in (1) imply

    sum_b t_b=H_L+8,
    sum_(ij in binom(L,2))s_ij=sum_b binom(t_b,2)>=H_L-3. (4)

Here binom(t,2)>=t-1 for every integer 0<=t<=4, and there are eleven
rows. This is the credited four-column packing mechanism.

If L supports a local four-cycle, triangle-freeness excludes its
chords. Its four red edges have total upper bound 2H_L-20 from (2).
The two opposite blue pairs have at least two common local neighbors
each, so their combined upper bound is H_L-8. Thus

    sum_(ij in binom(L,2))s_ij<=3H_L-28.              (5)

But H_L<=12, and 3H_L-28 < H_L-3. Equations (4)--(5) contradict each
other. Thus P has girth at least five, regardless of whether its local
degrees are two or three.

In the profile 0,2,3^8, at most two of the eight cubic points are
neighbors of the sole degree-two point. Choose a cubic point r that
is not. Its three neighbors are cubic. Triangle-freeness and the
absence of four-cycles make their six other neighbors distinct from
each other, r, and the first three points. These are ten nonisolated
points in a graph with only nine nonisolated points. This contradiction
eliminates the final thirteen-edge profile.

We have obtained local profiles 3^10 and 2^2,3^8 by ordinary counting,
without importing any regular-host finite floor certificate.

## 4. An elementary leaf argument identifies both local graphs

In the cubic case, choose any r. Its three neighbors and their six
other neighbors account for all ten points. Each of the six latter
points has exactly one neighbor among the first three, since two
would make a four-cycle. The induced graph on these six points is
two-regular. With no triangle it is a six-cycle. Two points attached
to the same first neighbor cannot be at cycle distance one or two,
so they are opposite. This uniquely gives Petersen.

In the profile 2^2,3^8, the two low points have disjoint neighbor sets
by Section 2. Four of the eight cubic points therefore avoid both
low points. Choose one as r. Again r, its three cubic neighbors and
six distinct second neighbors account for every point. The two low
points occur among the latter six. Their induced degrees are one,
and the other four induced degrees are two. A graph with this degree
sequence is a path plus cycles; any cycle has length at least five,
while the path has at least two points. On six points no cycle fits.
Thus the six-point graph is a path P6.

Label its points 0,...,5 in path order. The three first neighbors of r
partition these six points into pairs. A pair cannot have path distance
one (a triangle) or two (a four-cycle). Point2 must therefore be paired
with5, and point3 with0; the remaining pair is1,4. Adding the edge05
closes a six-cycle with exactly the three opposite pairs. It produces
Petersen. The endpoints0,5 were precisely the two degree-two points.
Consequently P is Petersen with one edge deleted.

For use below, Petersen has exactly five independent four-sets: in its
two-subset model on a five-set they are the four two-subsets containing
a fixed point. To check completeness, a pairwise intersecting family
of two-subsets with no common point has at most three members. Starting
with {a,b},{a,c}, a member missing a must be {b,c}; a fourth member
cannot intersect all three without repeating one. Thus every independent
four-set is one of those five stars. Its adjacency Q also satisfies
Q^2+Q=2I+J, and

    K(Q)=4I+3J-3Q-Q^2=2I+2J-2Q,                   (6)

whose entries on red edges are zero. These are the elementary Petersen
facts used in 8541; no spectral or historical classification is needed.

## 5. Outside rows have size at most eight

For the actual miss matrix M put S=M^T M. For each distinct A pair let
F_ij be its nonnegative unused book capacity (three minus red pages,
or six minus blue pages); put F_ii=0. Pair counting (2) gives

    S=S0-F,
    S0=4I+h1^T+1h^T-2J-3P-P^2.
    (F1)_i=3h_i+H-24-sum_(j in N_P(i))h_j-u_i,
    u_i=sum_(b:i in Z_b)(k_b-4).                    (7)

The row sum of S is 4(h_i+2)+u_i; that of S0 is
7h_i+H-16-sum_(j in N_P(i))h_j. This proves the margins without using
the actual degrees in B.

A row of size at least nine and ten other rows of size at least four
force total misses at least49. Its even total H+20 is at most50, so
P is Petersen. The complete patterns are 10,4^10 or9,5,4^9.

For10,4^10, every u_i=6 and the cubic margins in (7) force F=0.
After subtracting the ten-row, the other ten rows have Gram K(P).
Its zero red-edge entries force every actual four-row to be an
independent four-set of P.

For9,5,4^9, let a be the omitted point of the nine-row, z=1-e_a its
indicator and q the five-row. The cubic margins have total degree ten
in F, hence total edge weight five. Its degree at a is6-q_a. A vertex
degree is at most total edge weight; therefore q_a=1 and all five F
edges meet a. With r=q-e_a and L=A minus({a} union supp(r)), the margins
force F=e_a 1_L^T+1_L e_a^T. Expanding gives

    zz^T+qq^T+F=J+rr^T,
    K(P)=R+rr^T,                                  (8)

where R is the Gram of the nine actual four-rows. Equation (6) again
forces all nine to be independent in P. This reuses the star-margin
identity of 8541 at the new outside-degree boundary.

A four-row always has delta=0 by (1), so its point has full degree ten.
Two equal four-rows have six common red neighbors in A. They cannot
be red adjacent. If both are red neighbors of the distinguished large
row's point b, they have a seventh common red neighbor b. Since both
have degree ten in the 22-point host, their common blue and common red
counts on their blue joining spine are equal. This violates the blue
cap six.

The ten-row's point has at least10-2=8 red neighbors among the ten
four-row points. The nine-row's point has at least9-2=7 red neighbors
in B, at least six of which are four-row points because only the
five-row is an exception. Either count exceeds the five available
independent four-sets, forcing the forbidden equal-row pair. Hence
every k_b<=8.

## 6. An edge-deleted Petersen root has no eight-row

Suppose P has profile2^2,3^8 and there is an eight-row Z. The total
miss count is48, so the other ten rows are fours. Let x,y be the low
points and W=A minus Z. If x belongs to Z, its two neighbors must lie
in W because a red2--3 pair has zero joint miss capacity. The other
low point cannot belong to W (that would make it a red neighbor of x),
so it also belongs to Z and has the same two neighbors W. This
contradicts Section 2. Thus W={x,y}, and Z is all eight cubic points.

Here is the credited 8621 contraction, retaining the altered outside
degree. Set E=e_x e_y^T+e_y e_x^T and let lambda_i count low neighbors
of cubic point i. These are0 or1 and sum to four. The margins in (7)
give F-degree four at each low point and lambda_i at each cubic point.
Let C be total F-edge weight on cubic--cubic pairs. The low degrees
imply F_xy-C=2. Since F_xy<=S0_xy=2, both F_xy=2 and C=0 follow.
At a marked cubic point, its red pair to its low neighbor has zero
capacity, so its unit F edge joins the opposite low point. Therefore

    F=2E+PE+EP.

With z=1-e_x-e_y, expansion of (7) gives the Gram R of the ten
four-rows as

    R=S0-F-zz^T=K(P+E).                             (9)

Section 4 identifies P+E as Petersen. Thus all ten four-rows are
independent sets in that graph, with just five possible types.
The eight-row's point has actual B-degree8-delta_b>=6, and every
other B point is a full-degree four-row. Among its six or more red
neighbors two share a four-row type, violating the same literal cap
as Section 5. Hence k_b<=7 at an edge-deleted Petersen root.

The previous regular contraction used B-degree eight. The new argument
needs only B-degree six, covering the possible degree-eight outside
point in a 109-edge host. No regular outside-star census is transferred.

## 7. Guaranteed roots at 109 edges

Use the credited degrees8..10 theorem for an arbitrary valid109-edge
graph. Its degree deficiency sum is220-218=2, so its degree sequence
is10^21,8 or10^20,9^2.

In the first case the degree-eight point has eight degree-ten red
neighbors. Exactly21-8=13 degree-ten points avoid it, and those are
precisely the full-degree roots. In the second, the union of the two
degree-nine points' red neighborhoods among the20 high points has
size at most18. Hence at least two high points avoid both. If the low
points are red adjacent, each has only eight red neighbors among the
high points, so at least20-16=4 avoid both. Apply the theorem to each.

## Validation and limits

This is an ordinary unformalized proof. Its compact programs check the
degree profiles, low-point packing constants, all four-cycle degree
patterns, and every admissible leaf pairing. They reconstruct Petersen
independently and check all entries of (6), (8), and (9). Two deliberately
invalid 109-edge controls have the two possible degree sequences and
replay all local identities with signed capacity. A third control
replays the eight-row contraction with an actual degree-eight point
and a literal forbidden blue book. They validate identities and do
not constitute a census of valid22-point graphs.

No solver, floating arithmetic, local catalogue, Hall theorem or
enumeration of unrestricted hosts is a premise. Author checks are not
independent review or formalization. The degree bound imported for the
unconditional consequence remains a computer-assisted campaign lemma.

Primary tables reopened2026-10-01 retain the interval
[22<=R(B4,B7)<=23, Table1](https://arxiv.org/pdf/2407.07285) and
[Small Ramsey Numbers, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The retained primary21 fixture reproduces93 red edges and page maxima3/6;
it is validation of a known construction. The global23-vertex upper
certificate was not replayed. No exhaustive historical-priority search
or complete109-edge exclusion is claimed.
