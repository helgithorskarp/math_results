# Exact-half separators for annuli with arbitrary fan runs

The regular-incidence hypothesis in the
[subdivided annulus theorem](../planar_two_geodesic_subdivided_annuli/README.md)
can be removed: consecutive outer or inner vertices may share a neighbor
in arbitrarily long fans. The resulting class still has two shortest
paths whose deletion leaves at most half of any nonnegative vertex mass
in each component. The new step treats an entire outer fan at once;
a heavy fan has a local decomposition whose five-vertex bags are covered
by two ambient geodesics.

This is a sufficient structural theorem for
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf),
not a solution for unrestricted planar graphs. The preceding subdivision
theorem and its metric path-cover lemma have been
[independently reviewed](../planar_two_geodesic_subdivided_annuli_review1/REVIEW.md).
The fan extension below awaits its own independent review.

## The core and statement

Choose a cyclic word

    A^d_0 C^e_0 A^d_1 C^e_1 ... A^d_(b-1) C^e_(b-1),
    b>=5, all d_q,e_q>=1, k=sum d_q, m=sum e_q.

There are an outer cycle a_0,...,a_(k-1), an inner branch cycle
c_0,...,c_(m-1), and a root r adjacent to every a_i. Starting at state
(0,0), an A-step increases i and a C-step increases j. Each visited
state specifies a cross edge a_i c_j, with indices reduced modulo k,m.
This is the usual triangulated annular strip: an A-step bounds the
triangle a_i c_j a_(i+1), and a C-step the triangle a_i c_j c_(j+1).
The root caps the outer cycle by triangles r a_i a_(i+1).

The root, outer-cycle, and cross edges have common length lambda>0.
Replace each inner edge c_j c_(j+1) by an internally disjoint arc T_j
whose internal vertices have degree two in the core H. Require

    length(T_j)>=lambda;
    if T_j has internal vertices, length(T_j)>=2lambda.

Constituent edges of the arcs may have arbitrary positive lengths.
In particular, arbitrary unit-edge subdivisions of every inner edge
are allowed, with no bound on their order or distance from the root.

Let G be a finite connected simple graph containing H isometrically,
with no extra edges between H's vertices. Every component K of G-V(H)
has boundary contained in {r}, {r,a_i}, or {r,a_i,a_(i+1)} for some i.
The condition applies also to zero-mass components. Assume each induced
local torso G[K union N(K)] has treewidth at most three. New edges may
have arbitrary positive lengths compatible with core isometry; lengths
at least lambda/2 suffice, since the possible boundaries are cliques
with edge length lambda.

**Theorem.** For every nonnegative real vertex-mass assignment of total
W, two shortest paths in the original G have a union S such that every
component of G-S has mass at most W/2. Singleton paths are allowed.

The planar unit-edge members give the claimed partial case of Problem 31.
As in the preceding independent review's strengthening, planarity of
the full graph is unnecessary once the stated core, attachment, and
metric assumptions hold. No claim for arbitrary nonplanar graphs follows.
The theorem contains the all-mass regular annular case after a cyclic
reindexing, by setting every run length equal to one.

Here is a useful conditional statement without the torso-width assumption.
For a maximal A-run from a_l to a_t at c_j with t-l>=2, define its fan
region F to contain the internal outer vertices a_(l+1),...,a_(t-1),
all attachments with sole active boundary at one of those vertices,
and all attachments whose two active boundary vertices are the endpoints
of an edge of this run. Define also

    Gamma_j = interior(T_(j-1)) union {c_j} union interior(T_j).

If every individual K, every such F, and every Gamma_j has mass <=W/2,
the spoke P=(r,a_0,c_0) at the beginning of any A-run can be completed
by one ambient geodesic. The heavy cases in the theorem may change both
paths. We do not assert completion for every arbitrary spoke, nor a
light-attachment-only theorem for unrestricted heavy fans.

## Heavy regions

We use the standard weighted-centroid property of a tree decomposition:
assign each graph vertex's mass to a bag containing it and take a
weighted centroid of the decomposition tree. Its bag separates every
remaining graph component into mass at most W/2. Covering that bag by
two ambient geodesics can only delete more vertices and preserves balance.

**A heavy attachment.** If w(K)>W/2, take a width-three decomposition
of its torso. Its boundary is a clique of order at most three, so some
bag contains it. Attach the outside bag V(G)-K as a leaf there, assign
K's mass locally, and assign all other mass to the outside leaf. The
centroid cannot be the outside leaf: its sole branch has mass w(K)>W/2.
Thus a local bag of order at most four half-separates the full G.
Pair its vertices and take at most two ambient geodesics. This is the
[reviewed heavy-attachment reduction](../planar_two_geodesic_prescribed_attachment_review1/REVIEW.md).

**A heavy long fan.** Let an A-run have endpoints a_l,a_t and common
inner neighbor c_j, with d=t-l>=2. Indices here are unrolled within this
run. Every strictly internal a_s has only c_j as an inner neighbor.
Consequently the F defined above is exactly one component after deleting

    B={r,c_j,a_l,a_t}.

It is connected through the internal outer chain: every included
two-active attachment meets an internal chain vertex when d>=2.
Other attachments at either endpoint, and root-only attachments, are
outside F. Its boundary is contained in B.

For s=l,...,t-1, make the path of bags

    B_s={r,c_j,a_l,a_s,a_(s+1)}.

These cover the core edges on F union B; their last bag contains B.
For each attachment inside F, glue its width-three torso decomposition
to a core bag containing its root-clique boundary. Such a core bag
exists for both single-active and consecutive-active boundaries, and
the torso decomposition has a bag containing that clique. Finally,
attach the outside leaf V(G)-F to B_(t-1). Every edge of G is covered,
and the bags containing any fixed vertex form a connected subtree:
r,c_j,a_l occur along the core path, another active vertex occurs in
its two consecutive core bags, and each guest decomposition is attached
at a bag containing its entire intersection with the host. The outside
leaf intersects the local decomposition precisely on B. This is a
tree decomposition of G, although its outside bag can be arbitrarily large.

Assign F's mass to local bags and all other mass to that outside leaf.
If F is heavy, a centroid is local. Every core bag is covered by the
ambient geodesic (r,a_s,c_j), of length 2lambda, together with a geodesic
joining its at most two remaining vertices. Indeed d_G(r,c_j)=2lambda
by the edge lower bounds after suppressing rim interiors and by core
isometry. Guest bags have order at most four and are covered by pairing.
Thus a heavy F also yields the desired separator. The five-vertex
bag assertion is special to this decomposition; it is not a theorem
for arbitrary graphs of treewidth four.

**A heavy inner patch.** The
[three-portal path-cover lemma](../planar_two_geodesic_subdivided_annuli/README.md)
covers the whole path T_(j-1) followed by T_j with two ambient geodesics.
Its only possible attachment vertices are its two endpoints and c_j;
every other internal vertex has degree two in G. This remains true when
c_j has many outer neighbors. The lemma allows arbitrary positive edge
lengths and does not require the path itself to be isometric. If Gamma_j
is heavy, its complete removal leaves less than W/2 total mass. Restoring
any earlier spoke is therefore safe in this case.

It remains to prove the conditional statement when all these regions
are light. Set h=W/2. The zero-total-mass case is immediate.

## The staircase of root spokes

Begin the cyclic word with an A-run and fix P=(r,a_0,c_0). Let Y(K) be
K's active boundary, namely N(K) intersect {a_i}. For bookkeeping
discard attachments with Y(K) empty or {a_0}, of total mass D. P has
already detached them individually, and they are light. Put

    alpha_i=w(a_i)+sum_{Y(K)={a_i}} w(K) for i!=0;
    gamma_j=w(c_j) for j!=0;         alpha_0=gamma_0=0;
    kappa_i=sum_{Y(K)={a_i,a_(i+1)}} w(K);
    tau_j=w(interior(T_j));
    M=sum_i(alpha_i+kappa_i)+sum_j(gamma_j+tau_j)=W-w(P)-D.

Set alpha_k=gamma_m=0. At a visited cross-state (i,j), let

    L(i,j)=sum_{s<i}(alpha_s+kappa_s)+sum_{q<j}(gamma_q+tau_q);
    R(i,j)=M-L(i,j)-alpha_i-gamma_j.

After deleting P and the root spoke (r,a_i,c_j), each surviving
component meeting the core is contained in one of these formal sides.
To see this directly, cut both cycles at indices 0 and i,j. A cross
edge belongs to a state before or after (i,j) in the monotone word;
it cannot join the two surviving sides. The outer and inner arcs follow
their cyclic order, and each attachment stays within its single outer
vertex or consecutive outer sector. At a deleted endpoint an attachment
may detach, but cannot bridge the sides. Any component not meeting the
surviving core is one whole outside K and is light. The formal sides can
overestimate actual components, including at the cyclic seam.

Along an A-step or C-step the bounds change respectively as follows:

    A-step: L'=L+alpha_i+kappa_i, R'=R-alpha_(i+1)-kappa_i;
    C-step: L'=L+gamma_j+tau_j,   R'=R-gamma_(j+1)-tau_j.

Thus L never decreases and R never increases. The first and last bounds
are (0,M) and (M,0). If any state has both bounds <=h, its spoke completes
P. Otherwise exactly one bound is heavy at each state, since L+R<=M<=2h,
and there is a step from a right-heavy state to a left-heavy state.

**A C-step.** Both endpoints of T_j are at root distance 2lambda and
have the same active neighbor a_i. Extend the old spoke along T_j to
the last vertex at or before its metric midpoint, and the new spoke
back along T_j to the first vertex at or after its midpoint. Both are
ambient geodesics: an interior vertex is accessible only through the
two arc endpoints, which have equal root distance. The first extension
retains the old light L; the second retains the new light R'. The other
two bounds have disjoint mass supports in M, since the extensions
together remove every internal arc vertex. They cannot both exceed h.
One extension completes P. This works for arbitrary lengths of C-runs.

**An A-step in a long A-run.** Take the entire maximal run l,...,t at
c_j around this transition. Monotonicity implies its first left bound
L_start and last right bound R_end are light. The run has length at most
k-b+1<=k-4, so a_l,a_t are nonadjacent in the outer cycle. The path

    Q=(a_l,c_j,a_t)

has length 2lambda and is ambient shortest: in the suppressed core
every branch edge has length >=lambda and there is no direct edge
between its endpoints. Deleting P union Q leaves core components in
the old left side, the old right side, or F. This follows either from
the same cut-cycle argument or from F's four-vertex boundary B; outside
the run there is no new connection between the two sides after c_j and
the run endpoints are deleted. All three bounds are light. No A-run
crosses the chosen seam, because P starts an A-run.

**An A-run of length one.** Write its endpoints a_l,a_t, with t=l+1,
and shared inner vertex c_j. Let L be the left bound before the step,
and R the right bound afterwards. Both are light. Maximality of the run
gives edges a_l c_(j-1) and a_t c_(j+1), and no edges a_l c_(j+1) or
a_t c_(j-1). Here c_j has exactly these two active neighbors.

If both adjacent rim arcs have no internal vertices, let
alpha=alpha_l, beta=alpha_t, gamma=gamma_j, kappa=kappa_l. Then

    M=L+R+alpha+beta+gamma+kappa.

The two adjacent failed spokes imply R+beta+kappa>h and L+alpha+kappa>h.
The two length-2lambda ambient geodesics
(a_l,a_t,c_(j+1)) and (a_t,a_l,c_(j-1)) have side bounds
(L+gamma,R) and (L,R+gamma), respectively. They have nonadjacent
endpoints. If both failed, adding their two heavy inequalities to those
of the spokes would give 2M-alpha-beta>4h, impossible. This argument
allows an arbitrarily heavy aggregate kappa, since the individual
outside components detach when both endpoints are removed.

If either adjacent arc has an internal vertex, instead use

    Q=(c_(j-1),a_l,a_t,c_(j+1)).

This length-3lambda path is ambient shortest. For the distance check,
suppress the rim interiors. All branch edges have length >=lambda.
There is no one-edge route between these inner endpoints. They have no
common active neighbor: an active vertex's inner neighbors form one
C-run interval, or a singleton. An interval containing both endpoints
would either cross c_j, impossible because the positive A-run changes
the active vertex there, or traverse the other inner arc of m-2 edges.
Every C-run has length <=m-b+1<=m-4, excluding the latter. The only
possible two-edge inner route is through c_j, since m>=5, and its length
is at least 3lambda by the subdivided-arc hypothesis. Every other route
uses at least three branch edges. Core isometry proves shortestness in G.

Deleting P union Q leaves every core component within the old sides
bounded by L,R or within Gamma_j. Indeed c_j has no remaining active
neighbor, its two incident inner arcs lead to deleted endpoints, and
the active sector's attachments detach individually. These three regions
are light. At j=0 the shared inner vertex was already removed by P;
using the original patch only overestimates the residual mass.

All transitions are handled. Together with the three heavy-region
reductions, this proves the theorem. QED.

## What changes and what remains open

Both kinds of fan run can be arbitrarily long, independently; k and m
can differ. The displayed core need not have exactly two cross-neighbors
at every branch vertex. For a small unit fixture, take runs
(d,e)=(2,1),(1,2),(1,1),(1,1),(1,1), subdivide all six inner edges once,
and attach ten-vertex peripheral cones in outer sectors 0,2,4. There are
49 vertices. Its displayed core has an active vertex with only one inner
neighbor, so the regular-core hypothesis of the preceding theorem fails.
This compares the displayed hypotheses, not all possible representations
of the same graph or all earlier sufficient classes.

The main remaining restrictions are the isometric root-capped annular
core, root-clique attachment boundaries, local torso width in the heavy
cases, and the lower bound 2lambda on a subdivided arc. The run count
b>=5 is sufficient; no sharpness claim or negative result for fewer
runs is made. The earlier regular theorem retains stronger conclusions
for light attachments and prescribed spokes in its own setting.

The primary [Diot--Gavoille paper](https://dept-info.labri.fr/~gavoille/article/DG09a)
proves strong two-path separability for face-separable weighted graphs.
That hypothesis asks every induced subgraph to have a balanced facial
boundary; the theorem here instead uses explicit incidence and metric
conditions, with arbitrary vertex masses. We do not claim that the
classes are disjoint, or historical priority from a targeted search.

## Reproducible evidence

From the repository root, Python 3.11+ and its standard library suffice:

    PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_fan_annuli/verify.py --check

The [checker](verify.py) constructs spherical embeddings, computes
original-graph distances, verifies core isometry, checks exact vertex-set
component inclusions and the exchange coefficient identity, and verifies
the global fan decompositions and every proposed two-geodesic bag cover.
It executes all heavy and light proof branches against actual residual
components. These include heavy fans with several light attachments,
and centroid choices at bags of order five. There are six mass fixtures,
31 cyclic systems, 30 additional irregular core models, and the explicit
49-vertex fixture. Metrics include constituent rim edges and attachment
edges shorter than lambda while retaining the stated conditions.

Compact output is in [expected.json](expected.json): 3,435 component-cut
checks, 78 fan decompositions with 141 five-vertex core bags, 1,180
heavy-fan cases (792 selecting a five-vertex bag), 4,818 heavy-attachment
cases, 874 heavy-patch cases, and 3,492 light balance checks. The fan
cases include 986 with multiple positive-mass outside components.

These are exact finite regressions, not independent review, exhaustive
enumeration, or a formal proof. The checker imports earlier graph and
metric-cover utilities in this repository. Universal run lengths,
positive real metrics, and real masses rely on the written proof.
