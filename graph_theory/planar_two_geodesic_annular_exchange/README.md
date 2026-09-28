# Completing every annular spoke across arbitrary light attachments

Let H_k, k>=3, have vertices r, a_0,...,a_(k-1), c_0,...,c_(k-1),
with indices modulo k and edges

    r a_i, a_i a_(i+1), a_i c_i, a_i c_(i+1), c_i c_(i+1).

The first four edge types have a common length lambda>0; inner-cycle
edges have length at least lambda. There are no subdivided rim edges
in the theorem below. Let G be a finite connected simple planar graph
obtained by adding vertices and incident edges to this core. Assume:

1. H_k is isometric in G.
2. Every component K of G-V(H_k) has its core boundary contained in
   {r}, {r,a_i}, or {r,a_i,a_(i+1)} for some i.

The boundary condition applies to zero-mass components too. Edge lengths
outside the core may be arbitrary positive numbers consistent with
isometry. A sufficient condition is that all new edges have length at
least lambda/2: excursions between distinct boundary vertices cost at
least their length-lambda clique edge. Vertex masses are arbitrary
nonnegative real numbers. Every geodesic is shortest in the full G.

**Light-attachment theorem.** If each outside component has mass at
most W/2, where W=w(G), then **every prescribed core spoke**

    P=(r,a_j,c_j) or P=(r,a_j,c_(j+1))

can be completed to an exact half separator by one additional ambient
geodesic. There is no restriction on the number of occupied attachment
sectors or on their vertex-cover number. Attachment order and internal
treewidth are unrestricted in this light version.

In fact Q can be selected from these 4k two-edge paths:

    (r,a_i,c_i), (r,a_i,c_(i+1)),
    (a_i,a_(i+1),c_(i+2)), (a_(i+1),a_i,c_i).

All are ambient geodesics: their endpoints are nonadjacent in H_k,
every core edge has length at least lambda, a displayed route has
length 2lambda, and core isometry preserves the distance.

**All-mass corollary.** If every outside torso G[K union N(K)] has
treewidth at most three, G has a two-geodesic half separator for every
nonnegative real mass assignment. The prescribed spoke can be retained
whenever all outside components are light; a heavy attachment uses a
different local separator.

This removes the two-vertex boundary-cover restriction from the
unsubdivided annular part of the
[previous rerooting theorem](../planar_two_geodesic_rerooted_attachments/README.md).
The proof below is an elementary cyclic mass argument and does not use
the earlier interval/facial sweep. It proves another all-order positive
class for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf),
not its unrestricted resolution.

## Mass reduction and a sharper bound

By rotation and reflection assume P=(r,a_0,c_0). Put
Y(K)=N(K) intersect {a_0,...,a_(k-1)}. Delete r conceptually, but keep P
in every final path union throughout the argument.

If Y(K) is empty or equals {a_0}, P already detaches K. Let D be the
total mass of these components. For i!=0 set

    alpha_i = w(a_i) + sum_{Y(K)={a_i}} w(K),
    gamma_i = w(c_i).

Set alpha_0=gamma_0=0. Let kappa_i be the total mass of components with
Y(K)={a_i,a_(i+1)}. Multiple components in a sector are grouped only for
bookkeeping; deleting both portals leaves them as separate components.
Their aggregate kappa_i is allowed to exceed W/2.

The represented mass is

    M = sum_i(alpha_i+gamma_i+kappa_i) = W-w(P)-D.

Let B be the largest individual outside-component mass, with B=0 if
there are none. We will prove that Q leaves every component with mass
at most

    h = max(M/2, B).

If an active vertex is removed, its original mass disappears and each
one-active-boundary attachment at it becomes a separate component of
mass at most B. If it survives, the mass assigned to alpha_i accounts
for all such attachments. Similarly, a sector's mass lies on a core
side when a portal survives; if both portals are removed, each original
component is individually bounded by B. No contraction or change to
the graph metric is performed.

## The cyclic exchange proof

For 0<=i<=k, use alpha_k=gamma_k=0 and define

    L_i = sum_{j=0}^{i-1}(alpha_j+gamma_j+kappa_j),
    R_i = M-L_i-alpha_i-gamma_i.

Thus (L_0,R_0)=(0,M) and (L_k,R_k)=(M,0). Consider the ordered spoke
sequence U_0,V_0,U_1,V_1,...,U_(k-1),V_(k-1),U_k, where

    U_i=(r,a_i,c_i),       V_i=(r,a_i,c_(i+1)),       U_0=U_k=P.

For G-(P union U_i), the two core-side mass bounds are L_i,R_i. For
G-(P union V_i), they are L_i+gamma_i, R_i-gamma_(i+1). Every remaining
component meeting the core lies on one such side; every component
disjoint from the core is an original outside K of mass at most B.
At the seam, a formal side can group several detached components;
this only overestimates their masses.

These bounds follow directly from the cyclic vertex order. Under U_i,
the left side uses active and inner indices 1,...,i-1 and sectors
0,...,i-1. The right side uses active and inner indices i+1,...,k-1
and sectors i,...,k-1. V_i moves c_i to the left and removes c_(i+1)
from the right. The attachment boundaries cannot connect those sides
after the displayed core vertices are deleted.

If any spoke has both bounds at most h, it completes P. Otherwise each
spoke has exactly one bound greater than h, since their sum is at most
M<=2h. The first spoke is right-heavy and the last is left-heavy, so
there is a transition from right-heavy to left-heavy.

It cannot occur from U_i to V_i: the old right and new left bounds
sum to M-alpha_i<=2h. Thus it occurs from V_i to U_(i+1). Write

    L=L_i+gamma_i, R=R_(i+1),
    alpha=alpha_i, beta=alpha_(i+1),
    gamma=gamma_(i+1), kappa=kappa_i.

Then M=L+R+alpha+beta+gamma+kappa. The two failed spoke bounds give

    R+beta+kappa > h,       L+alpha+kappa > h,

while L<=h and R<=h.

Now consider the two local geodesics

    Q+=(a_i,a_(i+1),c_(i+2)),
    Q-=(a_(i+1),a_i,c_i).

Both remove the portals of sector i, so all its components are detached
and individually bounded by B. The remaining core-side mass bounds
are respectively (L+gamma,R) and (L,R+gamma). Removing the additional
inner vertex only decreases those bounds. These inclusions also hold
at i=0 and i=k-1; vertices already in P have mass zero in the sums.

If neither local choice balanced those sides, we would also have

    L+gamma > h,            R+gamma > h.

Adding all four strict inequalities gives

    2M-alpha-beta > 4h,

contradicting alpha,beta>=0 and 2M<=4h. One local geodesic therefore
completes P with maximum residual mass at most h. When B<=W/2, also
M<=W, so h<=W/2. Zero masses and equality cases are included.

This is the precise role of the exchange: the potentially shared sector
mass is detached by changing the second path's endpoints. Requiring Q
to remain rooted at r would forbid both local choices.

## Heavy attachments

For the all-mass corollary, only a component K with w(K)>W/2 remains
to handle. Its boundary is a clique of at most three core vertices.
Join a width-three decomposition of its torso to one outside bag
V(G)-K at a bag containing this boundary clique. Give outside masses
to the outside bag and inside masses to local bags. A weighted centroid
cannot be the outside leaf because its other side contains all of K's
heavy mass. A local centroid bag of at most four vertices is a half
separator in the full graph. Pair its vertices and take two ambient
geodesics covering the bag; deleting additional vertices preserves
balance. This is the
[reviewed local centroid reduction](../planar_two_geodesic_prescribed_attachment_review1/REVIEW.md).

For unit peripheral cones with universal r, the local torso has
treewidth at most three, since removing r leaves an outerplanar graph.
The core itself need not have treewidth three.

## Exact checks and a rooted-path obstruction

The [checker](verify.py) verifies the component-containment formulas
symbolically on abstract annuli, the four-term coefficient identity,
and the selected paths and exact residual masses on attached fixtures.
Its full-graph fixtures import construction utilities from the previous
transfer artifact; these are regression checks, not independent review
or a formal proof. The universal real-mass claim rests on the written
inequalities and component inclusions. No solver or graph census is a
premise. Compact results are in [expected.json](expected.json).

A 43-vertex unit fixture uses k=6 and three disjoint occupied sectors
0,2,4, each with a ten-vertex peripheral component. All three components
are strictly below half the uniform total. An exhaustive check of all
rooted geodesic pairs gives an optimal largest residual of 23>43/2.
The prescribed spoke P=(r,a_0,c_0) is nevertheless completed by
Q=(a_2,a_3,c_4), whose largest residual has only 14 vertices. Thus the
unrooted local exchange is necessary for this fixture, and the former
two-vertex sector-cover hypothesis fails. This is a different graph
from the earlier single-heavy-pocket 43-vertex prescribed-path
obstruction; it is not a counterexample to Problem 31.

Run from the repository root with Python 3.11 or later:

    PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_annular_exchange/verify.py --check

The class has arbitrary attachment order and number, and the all-mass
corollary covers every occupied-sector pattern. It does not include
arbitrary cyclic neighborhoods, arbitrary metrics that shorten the
core, or positive-mass subdivisions of inner-rim edges. The last case
changes the side-mass formulas and needs another argument; it is not
silently inferred from subdividing this weighted theorem. The earlier
rerooting theorem still covers such subdivisions under its stated
boundary-cover condition. No historical priority claim is made.
