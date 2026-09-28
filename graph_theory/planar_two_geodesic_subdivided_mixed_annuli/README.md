# Exact-half separators in subdivided mixed annuli

Arbitrary unit subdivisions of the inner cycle are now permitted in
mixed triangular/quadrilateral annuli, including the formerly excluded
`DAD` configuration. The first spoke is selected by aggregate sector
mass. At one exceptional transition, its vertices are repartitioned
between two new ambient geodesics. This gives the original quantitative
residual bound and, with local attachment treewidth at most three, exact
half balance for every nonnegative vertex weighting.

This combines the geometry of the
[subdivided no-DAD result](../planar_two_geodesic_quadrilateral_annuli/README.md)
with the selection rule of the
[unsubdivided mixed result](../planar_two_geodesic_selected_spoke_annuli/README.md).
The conclusion retains the selected spoke's **vertices**; the spoke
need not remain one of the two paths. Independent review is pending.

The result is a sufficient class for
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
The [official schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html)
announces a disproof of a Codsi planar balanced-separator conjecture,
without its exact statement or witness. A renewed primary-source search
on 28 September 2026 did not locate that account. No claim of continued
openness, unrestricted resolution or historical priority is made.

## Construction and statements

Take a cyclic word in A, C, D, with increments

    A=(1,0), C=(0,1), D=(1,1).

Let k=#A+#D and m=#C+#D. Assume k,m>=3, every cyclic pure A-run has
length at most k-2, and every cyclic pure C-run has length at most m-2.
There is no DAD restriction.

The core has outer cycle a_0,...,a_(k-1), inner branch cycle
c_0,...,c_(m-1), a root r adjacent to every outer vertex, and cross edge
a_i c_j at every visited staircase state. A and C describe triangles,
and D describes a quadrilateral with neither diagonal added. Replace
each inner edge by a path T_j from c_j to c_(j+1), with any positive
integer number of edges. Its internal vertices have degree two in the
core H. All edges of H have one common length lambda>0.

Let G be a finite connected simple graph with strictly positive edge
lengths, containing H isometrically, with no additional edges between
vertices of H. Every component K of G-V(H), even a zero-mass component,
has boundary N(K) contained in one of

    {r}, {r,a_i}, {r,a_i,a_(i+1)}.

No attachment meets an inner branch or subdivision vertex. Outside
edge lengths are arbitrary subject to isometry; lengths at least
lambda/2 suffice because each permitted boundary is a clique whose
edges have length lambda. Planarity of the full G is unnecessary under
these hypotheses. Its planar unit-edge members bear on Problem 31.

Give vertices nonnegative real masses w of total W. Write
Y(K)=N(K) intersect {a_i}, and let

    kappa_i=sum_{Y(K)={a_i,a_(i+1)}} w(K).

A DAD sector is a singleton A-step immediately preceded and followed
by D. If any exist, choose one maximizing kappa_i **among DAD sectors**
and start the cyclic word with that A-step. Call its outer endpoints
a_0,b_0=a_1 and its center c_0. Otherwise choose any cyclic seam that
does not split an A-run. Set P=(r,a_0,c_0). All maximum-sector ties
are allowed.

For a maximal A-run from a_l to a_t at c_j of length at least two, let F
contain its strictly internal outer vertices, all K with sole active
boundary at one of them, and all K whose two active boundary vertices
form an outer edge of the run. Set

    B=max_K w(K), Fmax=max_F w(F),         empty maxima are zero;
    D0=sum_{K: Y(K) empty or {a_0}} w(K);
    M=W-w(P)-D0.

**Quantitative theorem.** Two ambient G-geodesics have union containing
V(P), and their deletion leaves every component of mass at most

    h=max{M/2,B,Fmax}.

No treewidth assumption is needed for this statement. It does not say
that P itself can always be completed by one more geodesic.

**All-mass corollary.** If every induced torso G[K union N(K)] has
treewidth at most three, every nonnegative vertex weighting has a
separator equal to the union of at most two ambient geodesics, with
every residual component of mass at most W/2. Both paths may change
in a heavy-attachment or heavy-fan case. Singleton paths are allowed.

The unit subdivision hypothesis is substantive in the reused
quadrilateral midpoint identity. Arbitrary positive lengths on
individual subdivision edges are not asserted here.

## Sweep and the previously handled transitions

Normalize lambda=1. All inner branch vertices have root distance two.
An outer vertex's inner neighbors form a C-run interval, or a singleton.
The bound m-2 excludes the long wrap that could supply an opposite
cross edge across D. The bound k-2 makes the endpoints of a long A-run
nonadjacent. These are the only wrap facts needed below, so the stronger
k-4,m-4 bounds in the preceding subdivided result are unnecessary here.

After deleting P, discard the K counted by D0: each is detached
individually and has mass at most B. Partition the remaining mass into

    alpha_i=w(a_i)+sum_{Y(K)={a_i}} w(K), i!=0;
    gamma_j=w(c_j), j!=0;
    alpha_0=alpha_k=gamma_0=gamma_m=0;
    kappa_i as above;
    tau_j=w(interior(T_j)).

At a cross state (i,j), deleting P and the root spoke (r,a_i,c_j)
leaves each component meeting H within one formal side

    L(i,j)=sum_(s<i)(alpha_s+kappa_s)+sum_(q<j)(gamma_q+tau_q);
    R(i,j)=M-L(i,j)-alpha_i-gamma_j.

Indeed, cut the outer and inner cycles at their deleted endpoints.
Every cross edge lies before or after the state in the monotone word,
and attachments meet at most two consecutive outer vertices. Hence
neither can join the two surviving intervals. A component disjoint
from H is a whole individual K. Formal bounds may overestimate at
deleted endpoints or seams. The formulas also denote their underlying
vertex sets in the set comparisons below.

L increases and R decreases from (0,M) to (M,0), with L+R<=M<=2h.
Unless a spoke already works, some transition has old R>h and new L'>h,
while old L and new R' are light. If h=0, all represented and detached
mass is zero and no exchange is needed.

Here are the repairs other than DAD; their component proofs are the
cyclic-interval cuts in the
[preceding proof](../planar_two_geodesic_quadrilateral_annuli/README.md).
They use the weaker wrap facts just verified.

* At a C-step along T=(v_0,...,v_n), extend the old root spoke to
  v_floor(n/2), or the new spoke backwards to v_ceil(n/2).
  Root distances to both ends are two, so both paths are geodesic.
  Each retains one light side, and the two potentially heavy sides
  are disjoint subsets of represented mass M.
* For a transition within a long A-run l,...,t at c_j, use
  a_l--c_j--a_t. Its length two is shortest. The first left side,
  last right side and F bound the core components; all are light.
* For a singleton A-step at c_0, its outer edge suffices, since P
  already deletes the inner center.
* A singleton A adjoining C has an offset-midpoint exchange. For a
  following C-arc T=(v_0=c,...,v_n=d), use the old root extension
  (r,a,v_0,...,v_floor(n/2)) or the detour
  (a,b,v_n,...,v_ceil((n+1)/2)). Distances from a to c,d are one,two.
  Thus both are geodesic, and their potentially heavy side supports
  are disjoint. Reflect the construction for a preceding C-step.
* At a D-step (a,c) to (b,d), write T=(v_0=c,...,v_n=d) and
  p=floor(n/2), q=ceil(n/2), u=floor((n-1)/2), v=ceil((n+1)/2).
  The four geodesics are
  (r,a,v_0,...,v_p), (r,b,v_n,...,v_q),
  (a,b,v_n,...,v_v), (b,a,v_0,...,v_u).
  Root distances and opposite endpoint distances one,two give
  shortestness. Each retains a light side. If alpha,beta are the
  two outer atoms, their four other side bounds sum to
  2M-alpha-beta<=4h: each internal arc vertex occurs exactly twice.
  Thus one candidate works.

These operations retain P as one path. Only a singleton A between
two D-steps remains.

## The new DAD exchange

A DAD sector has exactly two outer neighbors at its inner center,
and both outer endpoints have that center as their unique inner
neighbor. This follows directly from its entering and leaving D-steps.

The selected sector is a_0--b_0 at c_0, with maximum aggregate kappa_0.
Write a--b at c_j for the failed DAD transition, with sector mass kappa.
Then kappa<=kappa_0. The c_j=c_0 case was already handled.

### Distant centers and the preceding center

For j not in {0,1,m-1}, the complementary anchor vertex satisfies
d(b_0,c_j)=3. Its neighbors in H are r,a_0,the next outer vertex,c_0.
The root is not adjacent to c_j; a_0 has only inner neighbor c_0.
If that next outer vertex were incident with this DAD center, it
would force the center to be c_1. Finally c_0 is not adjacent to
the nonneighbor c_j, including after subdivision. A length-three
route through r supplies equality.

The same argument gives d(b_0,c_(m-1))=3 when T_(m-1) is subdivided:
there is then no direct edge c_0 c_(m-1). These facts are about H;
isometry transfers them to G.

Use Q=(b_0,r,b,c_j), together with P. It detaches every individual
K in kappa_0, since both anchor outer vertices are deleted. The
formal component bounds improve from L',R' to L'-kappa_0,R'.
The old heavy inequality gives

    L+alpha_a+gamma_j < M-h.

Since L'=L+alpha_a+kappa,

    L'-kappa_0
      < M-h-gamma_j+kappa-kappa_0 <= h.

All detached K are bounded by B.

If j=m-1 and T_(m-1) has just one edge, the old heavy right side
is exactly kappa+alpha_b+kappa_bridge, where the bridge is b--a_0.
The length-two outer path (a,b,a_0), together with P, deletes or
individually detaches every group in this side. Remaining represented
mass is less than M-h<=h. Two distinct DAD sectors require k>=5,
so its endpoints are nonadjacent.

### The next center: repartition the spoke's vertices

If j=1, the two DAD sectors force four consecutive outer vertices

    a_0,b_0,a,b.

There are no intervening C-steps or longer A-runs. Let eta denote
the aggregate sector mass on b_0--a, and beta the outer atom at b_0.

If T_0 has one edge, the new heavy left side is exactly
kappa_0+beta+eta+alpha_a+kappa. The outer geodesic (b_0,a,b), together
with P, deletes or individually detaches all its groups, and works
as in the preceding case.

Now let T_0=(v_0=c_0,...,v_n=c_1), n>=2. Define S to consist of a,
its sole-active attachments, and the two-active attachments on
b_0--a and a--b. Thus

    w(S)=alpha_a+eta+kappa.

S is a whole component after deleting {r,c_1,b_0,b}. Crucially, it
is already light. The old right bound satisfies the exact identity

    R_old+w(S)
      = M-kappa_0-beta-tau_0-gamma_1+kappa
      <= M,

using kappa<=kappa_0. Since R_old>h, w(S)<M-h<=h.
This is the mass comparison that pays for the formerly troublesome
subdivision interiors; no additional light-patch assumption is needed.
Here maximality is used for an adjacent center as well. The weaker
spoke-selection rule in the
[unsubdivided review](../planar_two_geodesic_selected_spoke_annuli_review1/REVIEW.md)
is not asserted for these subdivided arcs.

We have

    d(a_0,c_0)=d(b_0,c_0)=1,
    d(b_0,c_1)=2, d(a_0,c_1)=3.

For the last equality, there is no one- or two-edge route. The only
outer neighbors of c_1 are a,b, neither a neighbor of a_0 because
the displayed vertices are consecutive and k>=5. The edge c_0c_1
is absent because n>=2. A root route of length three exists.

Set p=floor((n+1)/2) and q=ceil((n+2)/2), so q=p+1. Replace the old
path pair by

    U=(a_0,r,b,c_1,v_(n-1),...,v_q),
    V=(b_0,c_0,v_1,...,v_p).

They are geodesics. Every entry into the interior of T_0 comes through
one of its ends. For U, 3+n-q<=1+q; for V, 1+p<=2+n-p.
The endpoint distances above therefore certify shortestness in H,
and hence in G.

Together U,V cover all vertices of T_0, since q=p+1. They contain
r,a_0,c_0, the vertices of P, and also delete b_0,b,c_1.
Every remaining component meeting H is contained in S or the new
right side R'. The short surviving outer interval is precisely a
with its included attachments. The inner arc is entirely removed,
and every other cross edge belongs to the right interval.
Other detached components are whole K. Since w(S),R',B<=h, the
new pair has the required balance.

This exhausts the sweep and proves the quantitative theorem.

## Heavy attachments and long fans

The all-mass reduction is unchanged from the
[fan-annulus theorem](../planar_two_geodesic_fan_annuli/README.md).
Here is the full-graph justification.

Every vertex-mass tree decomposition has a centroid bag whose deletion
half-separates: assign each vertex to a containing bag and take a
weighted centroid of the bag tree. Covering that bag by geodesics
deletes only more vertices.

If K is heavier than W/2, take a width-three decomposition of its
induced torso. Its clique boundary lies in a bag. Attach V(G)-K as
an outside leaf there, assign K's mass locally and all other mass
to the leaf. A centroid is local, since the outside leaf has a
branch of mass greater than half. Its at most four vertices can
be paired and covered by two ambient geodesics.

If a long F is heavy, its boundary is contained in
{r,c_j,a_l,a_t}. Use the path of core bags

    {r,c_j,a_l,a_s,a_(s+1)}, s=l,...,t-1.

Glue each included K's width-three decomposition at its clique
boundary, and attach V(G)-F as an outside leaf to the last core bag,
which contains the whole boundary. This is a full-G decomposition:
the internal outer chain has only c_j as inner neighbor, and all
attachments respect the indicated cliques. Assign F's mass locally,
so a centroid is local. A core bag is covered by r--a_s--c_j and
a geodesic joining its at most two remaining vertices; a guest bag
has at most four vertices. Thus two ambient geodesics cover a
full-G half-separator bag. This does not assert the analogous fact
for arbitrary treewidth-four graphs.

If neither heavy case occurs, h<=W/2. The quantitative theorem
then proves the corollary.

## Comparison with two established sufficient mechanisms

[Diot--Gavoille](https://emilie-diot.eu/Article/DG10a), Proposition 1,
gives ceil((treewidth+1)/2) ambient paths; their Theorem 1 gives two
from a half-separating face. Their strong notion uses original-graph
geodesics, as required here. These results are prior art.

An included weighted example avoids both of these sufficient
mechanisms. Reuse the
[52-vertex control](../planar_two_geodesic_selected_spoke_annuli/control.json),
with core (AD)^5, unit edges, and the three stacked attachments
of masses 14,14,9, total 37. The core has minimum degree four, so
it is not 3-degenerate; consequently the whole graph has treewidth
at least four.

The separate audit checks a spherical rotation with 93 faces and
connectivity after all 1,379 deletions of at most two vertices.
Thus the graph is 3-connected. Deleting the boundary of any face
leaves a component of mass at least 29, greater than 37/2.
By uniqueness of the plane embedding of a 3-connected planar graph
(Whitney's theorem, recalled in
[Georgakopoulos--Kim](https://arxiv.org/abs/2109.04085)),
this rules out a facial half-separator in any
embedding for this weighting. The theorem here nevertheless applies.

This comparison does not establish disjointness from all known
positive classes or historical novelty. The fixed-spoke obstruction
on the same graph was established in the earlier source; it is
reused here, not counted as a new counterexample. It is not a
negative instance of Problem 31.

## Reproduction and trust boundary

Use Python 3.11+ and its standard library (run used 3.11.2), with
assertions enabled, from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_subdivided_mixed_annuli/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_subdivided_mixed_annuli/audit.py
```

The first output must match [expected.json](expected.json).
Its totals are 84 systems, 3,948 component cuts, 4,404 quantitative
checks, 1,994 heavy-attachment cases and 99 heavy-fan cases. The new
pair is selected in 112 half-balance and 131 quantitative checks;
its overlap identity is checked in 15 coordinate systems.
It builds 12 attachment fixtures and 60 additional bounded random
core words, including inner triangles, C-fans, long A-fans, DAD
sectors, both arc parities, and scale-two core edges with length-one
attachment edges. It tests every tied maximum sector per mass profile.
Profiles include zero, uniform, individual-vertex, strict-heavy and
equality attachment cases, random integer masses with seed 2026092816,
and mass concentrated on inner arcs and outer regions.

The checks validate actual full-graph components, shortestness,
mass-set identities, local decompositions and their bag covers.
They import prior regression helpers from this repository. They
are not a graph census or a proof for all weights by finite sampling.
The two unsubdivided adjacent-center cuts are checked geometrically;
the mass profiles need not select every geometrically valid cut.

The separate [audit.py](audit.py) imports no research implementation.
It constructs (AD)^t rings directly for t=3,4,5,7, first-arc lengths
2 through 12, and scales one and two. Floyd--Warshall distances
independently check 88 instances of the new pair, core isometry,
component inclusions and the exact mass-overlap identity.
It separately reconstructs the literal 52-vertex control and checks
its rotation, connectivity and every facial residual. Expected output:

```text
geometries=88 three_connectivity_checks=1379 faces=93 minimum_facial_residual=29 total_mass=37 core_minimum_degree=4 PASS
```

The universal result rests on the written metric, component and
centroid proofs. The finite scope comparison also uses the standard
embedding-uniqueness theorem explicitly stated above. Separate
implementation by the same researcher is not independent peer review
or proof-assistant verification. No solver or large external artifact
is needed; the literal control and imported helpers are in the same
repository.
