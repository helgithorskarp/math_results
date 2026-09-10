# The thirteen-degree-eight-vertex boundary is impossible

**Theorem.** Every finite simple graph of order 54, size 187 and girth at
least five has degree counts

    (n6,n7,n8) = (z+4,50-2z,z),             0 <= z <= 12.

In particular, **no such graph has thirteen degree-eight vertices**.
This closes the entire previous boundary, including every one of its
remaining high forests and all their incidence assignments. The unrestricted
existence question is still open: **185 <= ex(54,{C3,C4}) <= 187**.

The proof below is a human incidence argument using an existing exact
rational lower bound. It needs the original degree/weighted-gap theorem,
the all-sink theorem, and only the inequality m>=5 from the earlier
rational certificate. It does **not** use the previous SAT exclusions of
individual high forests, their remaining histograms, or their proof traces.
Those results and artifacts remain preserved.

## 1. Notation and prerequisites

Suppose for contradiction that z=13. The degree counts are (17,24,13).
Put T=V8, L=V6 union V7, H=G[T], m=e(H), and let k be the number of
vertices of degree two in H. All points of T are sinks, meaning that every
vertex is within distance two of each of them. Write

    C(v)=N(v) intersect T,       c(v)=|C(v)|,
    F(v)={u: dist(u,v)>2},
    s(v)=sum_(u adjacent v)(d(u)-6),
    epsilon(v)=s(v)-8 on V6,    epsilon(v)=s(v)-7 on V7.

The [degree and gap proof](proof.md) and [all-sink proof](boundary_sinks.md)
give s(t)=5 on T. Consequently h(t)=degree_H(t)<=2, and t has
3+h(t) six-neighbors and 5-2h(t) seven-neighbors. Unique short paths between
high points yield

    sum_V6 c=39+2m,             sum_V7 c=65-4m,
    sum_V6 binom(c,2)+sum_V7 binom(c,2)=78-m-k.

Subtracting 3c-6 on V6 and c-1 on V7 gives the nonnegative integer identity

    sum_V6 (c-3)(c-4)/2 + sum_V7 (c-1)(c-2)/2
      =22-3m-k.                                               (1)

Hence m<=7. Independently, the exact rational certificate in
[forest_reduction.md, Section 2](forest_reduction.md) gives

    m >= 4120933/1000000 > 4,                                  (2)

so m belongs to {5,6,7}. Only its first certificate is used. Its constraint
model is built with `edge_bounds=False`: neither m<=6, the later bound on
m+k, nor a prior forest exclusion is assumed. The new checker replays this
certificate with explicit exact rational comparisons, including under -O.

The epsilon identities, rederived here to fix their scope, are

    sum_L epsilon=7,                 sum_L c epsilon=2m.

Indeed, sum_v s(v)=24*7+13*16=376. Remove 13*5 and the low baselines
17*8+24*7, leaving seven. At a high t the local weighted identity gives
sum_(u adjacent t)s(u)=59; the baseline contribution of its neighbors is
5h+8(3+h)+7(5-2h)=59-h. Thus sum_(low u adjacent t)epsilon(u)=h(t).
Sum over t to obtain the second identity. In particular,

    sum_L (c-3)epsilon=2m-21.                                 (3)

## 2. Individual far-neighborhood covers

Let A be the adjacency matrix and let M be the distant-pair matrix on L.
All F(v) lie in L. With D=diag(8-d(v):v in L), unique short paths give

    A^2+A-7I=J-diag(0_T,D+M).

Commuting both sides with A at a high/low entry gives, for every t in T
and v in L,

    (8-d(v))[t in C(v)]
      +sum_(u in F(v))[t in C(u)]=8-d(v).                     (4)

For a seven-vertex y, C(y) and the sets C(u), u in F(y), therefore
**partition T**. For a six-vertex x, its far-neighbor high sets cover
T minus C(x) **exactly twice**, and avoid C(x). In particular,

    |{u in F(x): t in C(u)}|=2   if t not in C(x), d(x)=6.     (5)

The ball counts are

    |F(x)|=9-epsilon(x) on V6,
    |F(y)|=4-epsilon(y) on V7.                                (6)

Neither (4) nor any later argument assumes the absence of distant
seven-seven pairs. The sets C(u) in these covers may be empty.

## 3. A local sign rule and the only negative contributions

If a low vertex has a six-neighbors, b seven-neighbors and c high
neighbors, then s=b+2c. For d=6,

    2c-8 <= epsilon <= c-2.

Thus `(c-3)epsilon>=0` at **every degree-six vertex**: for c<=2 both
factors are nonpositive; for c>=4 both are nonnegative; c=3 contributes
zero. If c=5 on V6, then epsilon>=2 and

    (c-3)epsilon>=4,             |F(v)|<=7.                   (7)

For d=7, `2c-7<=epsilon<=c`. Its contribution is nonnegative when c=0,
c=3, or c>=4. The only potentially negative types are

    (c,epsilon)=(1,1), (2,1), (2,2).

We will shortly prove c<=5 on all low vertices. This rules out (2,2):
its far set would have two vertices by (6), whose c values would sum to
13-2=11 by the partition (4), exceeding 5+5.

Let A1 be the seven-vertices with (c,epsilon)=(1,1), and A2 those with
(c,epsilon)=(2,1); write a1=|A1|, a2=|A2|. These contribute -2 and -1,
respectively. All other contributions to (3) are nonnegative. Hence

    2a1+a2 >= 21-2m.                                         (8)

If a six-vertex of c=5 exists, its positive contribution strengthens this to

    2a1+a2 >= 25-2m.                                         (9)

## 4. The complete inventory of large high neighborhoods

Call a low vertex large when c>=4. Put r=c-3 on V6. For every integer r,

    r(r-1)/2 + r >= binom(max(r,0)+1,2).

For r<0 the left side r(r+1)/2 is nonnegative; for r>=0 equality holds.
Since sum_V6 r=2m-12, equation (1) implies

    sum_V6 binom(max(c-3,0)+1,2)
      +sum_(v in V7, c(v)>=4) (c(v)-1)(c(v)-2)/2
      <=10-m-k<=5.                                          (10)

A six-vertex with c>=6 or a seven-vertex with c>=5 costs at least six
in (10), and is impossible. This proves c<=5 on L, as used above. A
six-vertex with c=4 costs one; one with c=5 costs three; a seven-vertex
with c=4 costs three. Therefore the following two cases cover everything:

* No c=5 vertex: there are at most five c=4 vertices, at most one of
  which has degree seven.
* A c=5 vertex exists: it is a unique six-vertex x. All other large
  vertices are six-vertices of c=4, in number t satisfying
  `t<=7-m-k<=7-m`, hence t<=2.

No histogram or assumed high-forest shape is omitted by this inventory.

## 5. Two packing facts from individual partitions

Distinct low vertices have at most one common high neighbor, since two
would give a four-cycle. We use this repeatedly.

**Fact I: a fixed pair of c=4 vertices occurs in at most two A2 far sets
of the form {u,v,z}, c(z)=3.** Such a partition leaves five high points
outside C(u) union C(v), and C(z) is the complement of the two-set C(y)
there. Distinct y have distinct z, since equal z would give two distinct
y vertices the same two high neighbors. For distinct z,z',

    |C(z) intersect C(z')|=1+|C(y) intersect C(y')|<=1.

Thus the two-sets C(y) are pairwise disjoint on five points, allowing at
most two. The degrees of u,v,z may be six or seven.

**Fact II: a fixed c=5 six-vertex x and c=4 vertex u occur in at most two
A1 far sets of the form {x,u,z}, c(z)=3.** Outside C(x) union C(u) there
are four high points. C(z) is the complementary triple to the singleton
C(y). If two such singletons differed, the two distinct triples would
intersect in two points, a four-cycle. Hence every such y has the same
singleton {p}. They all lie in F(x), so the double-cover equation (5)
at (x,p) allows at most two. The vertex z may have either low degree.

## 6. No c=5 vertex

Let C1,...,Cr be the high neighborhoods of the large vertices, so r<=5
and each has size four. Each pair intersects in at most one point.
There are at most three disjoint pairs among these blocks. This is
immediate for r<=3; for r=4,5 use

    13 >= |union_i Ci| >= 4r-sum_(i<j)|Ci intersect Cj|.

At least 4r-13 pairs intersect, leaving at most
binom(r,2)-(4r-13)=3 disjoint pairs.

If A1 is empty, every y in A2 has three far vertices with c sum eleven.
Their sizes must be 4+4+3. Assign y to its unique pair of c=4 far vertices.
Fact I and the three-pair bound give a2<=6, contradicting (8), whose right
side is at least seven.

Suppose instead that A1 is nonempty. Its three far vertices have c sum
twelve, so their three four-sets are disjoint and cover twelve points of T.
Let p be the remaining point. Any further four-set must meet each of those
three sets exactly once and contain p: it has at most one point in each
and only the point p outside their union. Thus every further four-set
intersects all the original three and all other further four-sets. The
original triple is the only disjoint triple, and its three pairs are the
only disjoint pairs.

No A2 vertex can exist. Its assigned pair would belong to that triple;
its c=3 far vertex z would have C(z) contained in the third four-set
union {p}. But C(z) can meet the third four-set in at most one point,
and has at most one point outside it, giving |C(z)|<=2 instead of three.

Every A1 vertex has high set {p} and is distant from each vertex of the
fixed triple. At most one large vertex has degree seven, so choose a
six-vertex of this triple. Equation (5) gives a1<=2. Therefore
2a1+a2<=4, again contradicting (8).

## 7. One c=5 vertex

Let x be that six-vertex and let t<=7-m be the number of c=4 vertices.
For y in A1, the three far sizes must be 5+4+3: there is only one five
and at most two fours. Thus x is far from every A1 vertex, and Fact II,
applied to each four, gives a1<=2t.

Split A2 into A2' containing vertices distant from x and A2'' containing
the rest. A vertex in A2'' has far sizes 4+4+3, so Fact I gives

    |A2''|<=2 binom(t,2).

Since A1 and A2' are disjoint subsets of F(x), (7) gives
`a1+|A2'|<=7`. Consequently

    2a1+a2 <= 7+2t+2 binom(t,2)=7+t(t+1).                   (11)

For m=5,6,7 respectively, the maximum allowed t is 2,1,0. The upper
bounds in (11) are 13,9,7, whereas the lower bounds in (9) are 15,13,11.
Each case is impossible. This exhausts the inventory (10), completing
the contradiction to z=13 and proving the theorem.

## 8. Reproduction and trust boundary

Run with CPython 3.11.2 and the standard library only:

    python3 verify_boundary_exclusion.py
    python3 -O verify_boundary_exclusion.py

The checker reconstructs and exactly replays the m>4 rational certificate
without adding an upper bound on m. It verifies the local sign rule and
charge inequalities over their complete finite domains. It independently
enumerates all point-incidence patterns of up to five four-subsets of a
thirteen-point set with pair intersections at most one; counts by number
of blocks are 1,1,2,9,71,546. This checks the disjoint-pair bound and the
absence of an A2 triple whenever an A1 triple exists. It also checks the
small complement-packing facts, the inventory and final inequalities,
and the partition/double-cover identities on actual graph controls.

The point-incidence enumeration labels the large blocks and normalizes
only the high-point labels by their block membership. Every point in at
least two blocks consumes a distinct clique of block pairs; those cliques
are disjoint because intersections have size at most one. Remaining block
points are singletons, and unused points fill the ground set to thirteen.
This supplies a complete control enumeration, not an enumeration of
54-vertex graphs. The written proof uses the elementary union inequality
and does not depend on this enumeration for completeness.

The m>4 certificate retains the original sparse constraint generator,
exact rational multipliers and rigorous error payment of428 times the
maximum coefficient excess. Its mathematical rows and proof are documented
in forest_reduction.md. The other imported results are the degree/weighted
gap and all-sink lemmas; published ex(53,{C3,C4})=181 remains external.
The new argument has internal exact checks, not formalization or a new
independent external review. No SAT/MILP status, prior forest census,
heuristic search, or floating-point approximation is a premise.

The individual distant-neighborhood mechanism was developed in the
preceding [distant-partition proof](distant_partition_exclusion.md). The
new sign and charge restrictions close the entire boundary without that
proof's four-profile/SAT prerequisite. Historical priority is not claimed.
All earlier source, partial searches and certificates are preserved.
