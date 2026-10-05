# A parent budget from a deepest-leaf path

Author: Atlas, agent ID `studio-researcher-1`, researcher. Version 1,
2026-10-05. This is the structural component of the global critical
tree-stacking multiplicity argument. Its universal inequalities are proved
below for weighted trees. The stacking classification used to apply them is
a separate inherited result; this component does not reprove that
classification or the final upper/lower asymptotic theorem.

## Exact tree and potential conventions

Let T be a finite simple tree of order n >= 3. Let L be its graph leaves,
I = V(T) minus L its nonleaves, and P the set of parents of graph leaves.
Thus every p in P is a nonleaf. All degrees below are degrees in the FULL
tree T. Set

\[
 F(v)=\sum_{u\in I}\deg_T(u)2^{\operatorname{dist}_T(v,u)},
 \qquad X_p=F(p),\qquad
 d_p=|N_T(p)\cap L|.
\]

For a graph leaf z with parent p, every path from z to a nonleaf passes
through p. Consequently F(z) = 2F(p). Write S(z) = F(z)/2 = X_p, and
define precisely

\[
 P^*=\{p\in P:F(p)=\max_{q\in P}F(q)\}.
\]

All ties are retained. The maximization is over leaf parents, rather than
over every vertex. For p in P* it is equivalent to

\[
 X_p\geq S(w)\quad\text{for every graph leaf }w.\tag{1}
\]

The graph-leaf eccentricity is H = max over v in V(T) of dist_T(p,v).
The core eccentricity is h = max over u in I of dist_T(p,u). These are
distances, not the directed structural deficits used in the inherited
stacking theorem. The induced nonleaf core is connected, so its distances
agree with dist_T on I.

For any p in P, a farthest vertex is a graph leaf: a nonleaf other than p
has a child further from p. A farthest nonleaf has a graph-leaf child for
the same reason. Hence

\[
 H=h+1.\tag{2}
\]

This includes a star, whose center has h = 0 and H = 1. In a nonstar tree,
H >= 2 and h >= 1 for every p in P. Indeed, H = 1 would say that every
other vertex is adjacent to p, making the tree a star.

## Potential normalization at the inherited interface

The directed structural deficit is denoted by alpha, to keep it distinct
from either eccentricity. For an oriented edge u -> v it is recursively
defined by

\[
 \alpha_{u\to v}=1\quad\text{if u has no neighbor other than v},
 \qquad
 \alpha_{u\to v}=3+2\sum_{x\sim u,\ x\ne v}\alpha_{x\to u}
 \quad\text{otherwise}.
\]

Let B_{u|v} be the component containing u after deleting uv. Direct
induction on this component gives the identity

\[
 \alpha_{u\to v}
 =1+2\sum_{x\in B_{u|v}\cap I}\deg_T(x)
       2^{\operatorname{dist}_T(u,x)}.\tag{3}
\]

For a terminal u the sum is empty. Otherwise let r be the number of
neighbors of u other than v, so deg_T(u) = r+1. Substituting the child
identities in the recursion yields 3+2r plus four times the child-rooted
sums. This is precisely the right side of (3): the contribution of u is
2(r+1), and each child-rooted sum is multiplied by four. This proves the
induction using full-tree degrees, including the edge to v.

For a leaf z with parent p, all nonleaves belong to B_{p|z}. Equation (3)
therefore says

\[
 \alpha_{p\to z}=1+2F(p)=1+2X_p.\tag{4}
\]

In the inherited score notation, the leaf score is
alpha_{p->z} + |L| = 1+2X_p+|L|. Thus the parents of globally maximum-score
leaves are exactly the P* defined above. This is the normalization bridge;
the assertion that the maximum leaf score equals the stacking threshold,
and the classification of equality configurations, remain inherited
stacking results.

## Strong budget for nonstars

**Lemma.** Let T be nonstar, n >= 3, p in P*, d = d_p >= 1, and
H = ecc_T(p) >= 2. Then

\[
 (d-1)(1-2^{1-H})
 \leq\frac54(n-1-d-H).\tag{5}
\]

**Proof.** Root T at p. Split each nonleaf's degree into its incident edge
ends. If an edge has parent at depth a and child at depth a+1, its total
contribution to F(p) is

\[
 3\,2^a\quad\text{if the child is a nonleaf},\qquad
 2^a\quad\text{if the child is a graph leaf}.\tag{6}
\]

In the first case both endpoints are nonleaves, giving 2^a+2^{a+1}.
In the second case only the parent is a nonleaf. The root's incident
edge ends are included in (6); no additional root term is needed.

Choose a farthest graph leaf w, and let Q be the p-to-w path of H edges.
It has H-1 nonleaf-child edges followed by one leaf-child edge. Since
H >= 2, Q shares no edge with the d leaf edges incident with p. Put
t = 2^{H-1}. The path contributes

\[
 3\sum_{a=0}^{H-2}2^a+2^{H-1}=4t-3,
\]

and the d root-leaf edges contribute d. Let R be the remaining edge set,
m = |R| = n-1-d-H, and let E be its total contribution divided by t.
Thus m >= 0 and

\[
 X_p=d+4t-3+tE.\tag{7}
\]

Use just p and the interior vertices of Q to lower-bound S(w)=F(w)/2.
We have deg_T(p) >= d+1, and every interior vertex of Q has degree at
least two. All omitted contributions are nonnegative. Hence

\[
 S(w)\geq(d+1)t+
       \sum_{a=1}^{H-1}2^{H-a}
       =(d+3)t-2.\tag{8}
\]

Combining (1), (7), and (8) gives

\[
 E\geq(d-1)(1-1/t).\tag{9}
\]

It remains to upper-bound E by 5m/4. A leaf-child edge in R has parent
depth at most H-1, so its normalized weight is at most one. A
nonleaf-child edge has parent depth at most H-2, since its child has a
descendant leaf. If its parent depth is at most H-3, its normalized
weight from (6) is at most 3/4. The only heavier case has parent depth
H-2 and normalized weight 3/2.

For each such heavy edge u->v in R, the child v is a nonleaf at depth
H-1. It has at least one child, and every child is a graph leaf at depth
H. Select one edge v->z. Its normalized weight is exactly one. The
vertex v is off Q: if it belonged to Q, its unique parent edge u->v
would also belong to Q. Therefore v->z is off Q and, since v has
positive depth, is not a root-leaf edge. It belongs to R.

Distinct heavy edges have distinct child vertices v, and their selected
leaf-child edges are distinct. A selected leaf-child edge cannot itself
be heavy. Thus these pairs are disjoint. If there are b pairs, they
have total normalized weight (5/2)b on 2b edges. Every unpaired edge
has normalized weight at most one, so

\[
 E\leq\frac52b+(m-2b)=m+\frac12b\leq\frac54m.\tag{10}
\]

Equations (9) and (10) prove (5). The argument includes d = 1 and all
ties in (1). No core-endpoint reduction or enumeration is needed. QED.

Using H = h+1, rearrangement of (5) gives the stronger form

\[
 n\geq h+\frac65+\frac95d
            -\frac45(d-1)2^{-h}.\tag{11}
\]

Subtracting the right side of the following weaker budget from that of
(11) leaves 1/5+(4/5)2^{-h} > 0. Therefore, for every nonstar p in P*,

\[
 n\geq h+1+\frac95d-\frac45d\,2^{-h}.\tag{12}
\]

## Stars, one-leaf classes, and K2

For a star with n >= 3, its sole leaf parent is its center, d = n-1,
h = 0, and X_p = d. Budget (12) is equality: its right side is d+1.
Budget (11) was proved only for nonstars and would be false for a star.
Thus (12) holds for every tree of order at least three and every p in P*.

When d = 1, the structural proof still holds; the inherited binomial
count for that class is binom(X_p,0) = 1. Keeping tied parents is
essential, since different parents can contribute separate such classes.
For all n >= 3, X_p > 0 because the tree has a nonleaf with positive
degree. This also prevents overlap between the inherited sibling families
for distinct parents.

K2 has empty nonleaf core and is handled separately. The only
nonstackable configuration of mass two is (1,1); neither vertex permits
a move. Every configuration of mass three is either already supported
at one vertex, or is (2,1) or (1,2), which becomes a singleton after
one move. Hence stack(K2)=3 and N(K2)=1 under the least-k>=2 and
nonempty-singleton convention. No core formula is used for K2.

For later analytic use, another immediate potential bound is

\[
 0<X_p\leq 2(n-1)2^h\quad(n\geq3),\tag{13}
\]

because every nonleaf lies within distance h and the sum of their
full-tree degrees is at most the full degree sum 2(n-1).

## The separate stacking input and scope

The inherited sibling-classification theorem, with stack(T) defined as
the least integer k >= 2 for which every configuration of exactly k
pebbles can reach nonempty singleton support, states for n >= 3 that

\[
 N(T)=\sum_{p\in P^*}\binom{X_p+d_p-1}{d_p-1}.\tag{14}
\]

Here N counts individual functions on the vertex set. There is no
quotient by tree automorphisms. The family for p has positive odd leaf
piles 1+2x_z for z adjacent to p, sum x_z = X_p, one pebble at every
other leaf, and zero at every nonleaf. The equality rigidity establishing
that these are ALL critical configurations belongs to the inherited
classification and its separate source audit. Equations (3)--(4) verify
the potential normalization; they do not replace that equality audit.

Immutable inherited sources are the
[sibling-classification source](https://github.com/helgithorskarp/math_results/blob/d4c0ebbc94ca2855f4fdc547549eed41d63d704c/tree_stacking_extremal_classification/README.md)
and the
[full-degree potential and core source](https://github.com/helgithorskarp/math_results/blob/80b058418b869fcee4762ae8d4ec930acc33e7a2/tree_stacking_global_growth/README.md).
The estimator and directed deficit calculus are prior work; the primary
papers are Csernak--Soukup,
[arXiv:2604.22341](https://arxiv.org/abs/2604.22341), and Fairfax-Ball,
[arXiv:2609.31811v1](https://arxiv.org/abs/2609.31811v1).

The contribution here is the universal path/edge-charge budget (5), its
all-tree form (12), and explicit interfaces. Finite exact controls in
`check_structural.py` test the source implementation and conventions;
they are not a proof of a universal tree statement. The final global
asymptotic, explicit uniform analytic constants, and all-order lower
construction are separate components. This source does not assert
historical priority or external peer review.
