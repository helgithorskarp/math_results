# Nontrivial separators in Ramsey(5,5;43) graphs

Throughout, a **good** graph has neither a clique of order five nor an
independent set of order five. Edges are red and nonedges are blue. The
minimum degree and vertex connectivity refer to the red graph unless a
color is specified. All graphs are finite, simple and undirected.

**Theorem.** Let G be a good graph on 43 vertices and let
V(G) = A disjoint-union B disjoint-union S, where |A|, |B| >= 2 and
there are no edges between A and B.

1. |S| >= 20.
2. If |S| = 20, then, up to interchanging A and B, their orders are 10 and
   13, both have independence number two, and the minimum degree of G is
   at most 20.
3. Consequently, kappa(G) >= min(delta(G),21). In particular,
   kappa(G) = delta(G) when delta(G) <= 21.

The same statements hold in the complement. A separator of order at most
19, if present, has order 18 or 19 and separates one singleton component
from one connected component. The theorem does **not** exclude these
singleton separators or assert that the degree-18 vertex is unique.
The order-20 profile is a necessary residual possibility, not an existence
claim. This theorem does not construct a good43 graph or change R(5,5).

## 1. Ramsey inputs and degree bounds

We use the established bound **R(4,5) <= 25**. This is the sole imported
computational theorem. It was proved by McKay and Radziszowski,
[*R(4,5)=25* (1995)](https://onlinelibrary.wiley.com/doi/10.1002/jgt.3190190304)
and later formalized independently by Gauthier and Brown,
[*A Formal Proof of R(4,5)=25* (2024)](https://arxiv.org/abs/2404.01761).
Neither computation nor formal proof is rerun here.

For completeness, the other required upper bounds follow elementarily.
R(2,t)=t and R(1,t)=1. The usual neighborhood/nonneighborhood split gives
R(s,t) <= R(s-1,t)+R(s,t-1). Pigeonhole on the five contacts of a vertex
proves R(3,3)<=6. If a triangle-free graph on nine vertices had independence
number at most three, every vertex would have degree at most three. Its
nonneighbors induce a triangle-free graph with independence number at most
two, hence at most five vertices by R(3,3)<=6. Thus every degree is at least
three, giving a 3-regular graph on nine vertices, contrary to the handshaking
lemma. Therefore R(3,4)<=9 and the recurrence gives R(3,5)<=9+5=14.
Ramsey numbers are symmetric under complementation.

In a good43 graph, each neighborhood has no K4 and no independent five,
so has order at most 24. Applying this in the complement gives

    18 <= d_G(v) <= 24, for every vertex v.                  (1)

If C is an induced subgraph with independence number p, where p=1,2,3,
then its order is respectively at most 4,13,24. Since A and B are
anticomplete, alpha(A)+alpha(B) <= 4. In particular both independence
numbers are at most three.

## 2. Clique growth inside contact classes

Let C be an induced subgraph with alpha(C)<=2. Define a subset of S by

    T_C = {z in S : C minus N_G(z) is a clique}.

An empty set or a singleton counts as a clique. If U is a clique in T_C,
then alpha(G[C union U]) <= 2. Indeed an independent triple cannot lie
inside C; it cannot contain two vertices of the clique U; and one vertex
z in U cannot have two nonadjacent nonneighbors in C by the definition of
T_C. These cover all positions of a possible independent triple.

The induced graph on C union U is also K5-free. R(5,3)<=14 therefore gives

    |C| + |U| <= 13.                                      (2)

Writing c=|C|, the graph induced by T_C contains no clique of order 14-c
and no independent five. Thus for c=10,11,12,13 its order has the bounds

| c | Forbidden clique in T_C | Bound on class size |
|---|---|---|
| 10 | K4 | 24 |
| 11 | K3 | 13 |
| 12 | K2 | 4 |
| 13 | K1 | 0 |

These are bounds on an entire class of separator vertices, not bounds on
a single attachment. No triangle-count caps, degree-deficiency tables,
or catalog classification are used.

Suppose now neither A nor B is a clique. Then both independence numbers
equal two. Moreover,

    S = T_A union T_B.                                    (3)

For if z belonged to neither class, it would have a pair of nonadjacent
nonneighbors in A and another such pair in B. These four vertices together
with z would be an independent five, since A and B are anticomplete.
The two classes can overlap; only their union is used. Equations (2)-(3)
imply |S| <= cap(|A|)+cap(|B|), with the capacities in the table.

If |S|<=20, then |A|+|B|>=23 and each side has order at most 13. The complete
list of nonclique profiles, up to swapping A and B, is therefore:

| Separator order | First side order | Second side order | Sum of capacities | Consequence |
|---|---|---|---|---|
| 17 | 13 | 13 | 0 | Excluded |
| 18 | 12 | 13 | 4 | Excluded |
| 19 | 11 | 13 | 13 | Excluded |
| 19 | 12 | 12 | 8 | Excluded |
| 20 | 10 | 13 | 24 | Necessary residual only |
| 20 | 11 | 12 | 17 | Excluded |

There are no such profiles with |S|<=16.

## 3. Clique sides

It remains to handle a clique side of order k=2,3,4. Every vertex of that
side has at least delta-k+1 neighbors in S, where delta=delta(G)>=18.
Their common neighborhood in S consequently has size at least

    k(delta-k+1) - (k-1)|S|.                              (4)

It contains neither K_(5-k) nor an independent five, so its order is at
most 13 for k=2, at most 4 for k=3, and zero for k=4. For k=2, equation
(4) forces |S|>=2delta-15>=21. For k=3 it forces
2|S|>=3(delta-2)-4>=44, so |S|>=22.

For k=4 we use the attachment types to get the needed stronger inequality.
Each z in S has at least one blue contact to the K4, or it makes a red K5.
For each vertex i of the K4, let L_i consist of separator vertices whose
only blue contact to the K4 is i. Two red-adjacent vertices of L_i, together
with the other three clique vertices, would make a red K5. Hence L_i is
independent and |L_i|<=4. At most 16 separator vertices have exactly one
blue contact to the K4; all others have at least two. The total number of
blue contacts from S to the K4 is consequently at least 2|S|-16.
On the other hand, each clique vertex has at least delta-3 red contacts to
S, giving at most 4(|S|-delta+3) blue contacts in total. Therefore

    2|S|-16 <= 4(|S|-delta+3),
    |S| >= 2delta-14 >= 22.                               (5)

Thus no clique side is possible for |S|<=20. Combined with Section 2 this
proves the order-19 exclusion and the claimed orders at the boundary 20.

For a redundant arithmetic coverage check, the side order bounds 4,13,24
and alpha(A)+alpha(B)<=4 leave exactly 21 tuples
(|S|,|A|,|B|,alpha(A),alpha(B)) with 2<=|A|<=|B| and |S|<=20. Fifteen
have a clique side; the other six are listed above. All sixteen tuples
through order 19 are excluded. The program certificate records all 21.
Its checker separately enumerates integer populations n_j of separator
vertices with j blue contacts to a clique side, using

    sum n_j = |S|,
    sum j*n_j <= k(|S|-delta+k-1),
    n_0 <= 13,4,0 for k=2,3,4 respectively,
    n_1 <= 16 when k=4.

These population inequalities are weaker than full attachment feasibility;
their infeasibility is sufficient for exclusion. All 49,054 population
vectors in the relevant clique cases are checked. The numerical checker
is not a substitute for the graph-theoretic implications just proved.

## 4. The order-20 degree boundary

Let the 13-vertex side be C. Its complement H is triangle-free with
independence number at most four. Every neighborhood in H is independent,
so each H-degree is at most four. The nonneighbors of any vertex in H
have independence number at most three and are triangle-free; R(3,4)<=9
makes their order at most eight. Since this order is 12-d_H(v), every
H-degree is at least four. H is therefore 4-regular, and G[C] is 8-regular.

For each z in S, its red neighborhood within C contains no K4 and has
independence number at most two. R(4,3)<=9 bounds its order by eight.
There are no red edges from C to the other side, so

    13delta <= sum_(v in C) d_G(v)
             = 13*8 + e_G(C,S)
             <= 104 + 8*20 = 264.

Consequently delta<=floor(264/13)=20. No classification or uniqueness of
the triangle-free 13-vertex graph is required.

## 5. Vertex connectivity and the singleton exception

For a disconnected graph on at least four vertices, its components can
be grouped into two parts of order at least two unless it has exactly
two components, one of them a singleton. To see this when there are at
least three components, group two small components against a component
of order at least two, or split a set of singleton components into two
nontrivial groups. With exactly two components the assertion is immediate.

For a cut S of order at most 19, G-S has at least 24 vertices. The theorem
excludes a grouping into two nontrivial anticomplete parts. Thus G-S
consists of a singleton v and one connected component. All neighbors of
v lie in S, so delta<=d(v)<=|S|. In view of (1), |S| is 18 or 19.
This also proves G is connected by taking S empty.

If delta<=20, this already gives kappa(G)>=delta. If delta>=21, cuts of
order at most 19 are impossible. A cut of order 20 could not isolate a
singleton, and any nontrivial grouping would force delta<=20 by Section 4.
Thus kappa(G)>=21. Together these statements give kappa(G)>=min(delta,21).
The standard upper bound kappa(G)<=delta applies since G is noncomplete;
deleting the neighborhood of a minimum-degree vertex leaves that vertex
isolated and at least one other vertex. Equality follows when delta<=21.
Every step can be repeated after exchanging colors.

## 6. Complete branch decisions and cut clauses

Let x_uv=1 denote a red physical pair. For **any** disjoint A,B of orders
at least two with |A|+|B|>=24, every good43 graph satisfies both clauses

    OR_(a in A,b in B) x_ab,
    OR_(a in A,b in B) not x_ab.                           (6)

The first forbids an anticomplete red cut with at most 19 deleted vertices;
the second applies the theorem in the complement. These clauses do not
impose automorphisms, named small neighborhoods, degree profiles, fixed
cores, or a graph catalog. They are valid even for partial assignments that
have not yet decided any within-part edges. The standalone generator
`nogood.py` emits either clause in 903 lexicographic physical pair variables.

For an explicit target-facing application, use the earlier
[F27 pentagon normal form](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_pentagon_normal_form):
red edge 01 joined in red to the pentagon on 2..6, with further induced
red pentagons on 7..11, 12..16, 17..21 and 22..26. There are 61 fixed pairs
and 842 free pairs. Choose

    A = {2,...,11,27,28},
    B = {12,...,21,29,30},
    S = {0,1,22,...,26,31,...,42}.

All 144 pairs between A and B are free in F27. Fixing them all blue, or all
red, gives two disjoint complete labeled branches, each with 205 fixed
pairs and **all 698 other pairs arbitrary**. The theorem excludes every
one of the 2^698 assignments in each branch. This is a complete branch
decision, not a verdict on a smaller induced subsystem or a solver timeout.

The full substituted Ramsey CNFs have respectively 880,692 and 934,584
clauses. Independent inspection of all 2*C(43,5) physical monochromatic
events per branch agrees entry by entry, through a deterministic literal
stream digest, with compatible-clique enumeration. Neither branch has an
empty or a unit initial Ramsey clause. Thus ordinary unit propagation has
no initial step on these formulas; this is not a runtime comparison with
other inference methods. The two valid cut clauses are supplied in the
original 842 F27 variable numbering as well.

F27's **coverage of all target graphs up to relabeling and color exchange**
has its own published N5=21 computational premise, retained in that source.
The present separator proof, its two explicitly defined branch exclusions,
and the universal physical cut clauses do not require N5=21. No solve of
the unrestricted F27 family is claimed.

## 7. Prior results and scope of the improvement

Classical connectivity theorems concern extremal graphs on R(r,b)-1
vertices. For example, Beveridge and Pikhurko,
[*On the connectivity of extremal Ramsey graphs* (2008)](https://opikhurko.warwick.ac.uk/E/BeveridgePikhurko08ajc.pdf),
prove vertex connectivity at least r-1 in that setting. Our statement uses
the specified order 43 and does not assume it is the extremal order.

The earlier [global connectivity-18 result](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_global_connectivity18)
(Discovery Net h3381, accepted at h3393) proved kappa>=18 with the same
R(4,5) import. It already uses Ramsey side-size arguments and the obstruction
from a 13+13 anticomplete split. We do not claim those ingredients as new.

The separate [hard-cap separator-18 classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_hard_separator18)
(h3555) excluded nontrivial cuts through 18 under extra triangle-count caps,
using deficit and slack counts, and gave a more restrictive singleton
classification in that conditional setting. Here the contact-class
clique-growth argument removes those triangle-cap assumptions for
nontrivial cuts and reaches order 19; it also supplies the residual
order-20 profile and its degree restriction. The stronger singleton
uniqueness conclusions of the conditional result are not asserted here.

This is an unformalized combinatorial proof with exact arithmetic and
definition-level code checks, not external peer review or a machine-checked
formal theorem. No historical priority or optimality is claimed. It is a
global structural reduction; no target graph, degree-profile closure, or
measured construction-search speedup has been obtained.
