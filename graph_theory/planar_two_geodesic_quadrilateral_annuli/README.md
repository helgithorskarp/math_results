# Exact-half separators across quadrilateral annular interfaces

A root-capped annular core may have genuine quadrilateral faces, with
neither diagonal present, and still admit an exact-half separator made
of two original-graph shortest paths. The theorem below also strengthens
the prescribed-spoke conclusion for regular unit annuli with subdivided
inner edges: a bound on the masses of inner patches is unnecessary.
The new ingredients are an integer midpoint exchange and a four-cut
identity across a quadrilateral.

This is a sufficient structural result bearing on
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
It does not settle the unrestricted question. **Literature status checked
28 September 2026:** the official
[workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html)
lists Marcin Pilipczuk's announcement of a disproof of a Codsi conjecture
about planar balanced separators. The schedule supplies neither the
precise statement nor a witness; we have not verified its relationship
to Problem 31. We therefore make no assertion that the general question
is still open and no historical-priority claim. This extension awaits
independent review.

## Core, attachments, and statements

Take a cyclic word in A, C, D, interpreted as increments

    A=(1,0), C=(0,1), D=(1,1).

Let k be the number of A and D letters, and m the number of C and D
letters. There are disjoint cycles of outer vertices a_0,...,a_(k-1)
and inner branch vertices c_0,...,c_(m-1), together with a root r
adjacent to all a_i. Starting at state (0,0), put a cross edge a_i c_j
at every visited state, reducing indices modulo k,m. Thus an A-step
bounds a triangle a_i c_j a_(i+1), a C-step bounds a triangle
a_i c_j c_(j+1), and a D-step bounds a quadrilateral
a_i c_j c_(j+1) a_(i+1). Add no diagonals to a D-face.

Require the following sufficient wrap and incidence restrictions:

    k,m>=5;
    every maximal cyclic pure A-run has length <=k-4;
    every maximal cyclic pure C-run has length <=m-4;
    the cyclic word contains no DAD.

In particular, a singleton A-run has a C-step on at least one side.
Longer A-runs may have D-steps on both sides. The wrap bounds ensure
that cross states are distinct and the construction is a simple annular
strip. They are not asserted to be sharp.

Replace each inner edge c_j c_(j+1) by an internally disjoint path T_j
with any positive integer number ell_j of edges. All edges of the
resulting core H, including every constituent edge of T_j, have one
common length lambda>0. We normalize lambda=1 in the proof. The words
"triangle" and "quadrilateral" refer to the strip before these
subdivisions. All subdivision interiors have degree two in H.

Let G be a finite connected simple graph containing H isometrically,
with no additional edges between vertices of H. Every component K of
G-V(H) must have its boundary N(K) contained in one of

    {r}, {r,a_i}, {r,a_i,a_(i+1)}.

This condition includes zero-mass components. Edges outside H may have
arbitrary positive lengths preserving core isometry. For example,
lengths at least lambda/2 suffice, because each possible boundary is a
clique with edge length lambda. No attachment meets an inner branch or
subdivision vertex.

For each maximal A-run from a_l to a_t at c_j with t-l>=2, let F be the
union of its strictly internal outer vertices, all K with sole active
boundary at one of those vertices, and all K whose two active boundary
vertices are the ends of one of the run's outer edges. Here the active
boundary of K is Y(K)=N(K) intersect {a_i}; root incidence is immaterial
to this definition.

Choose a cross edge a_0 c_0 such that the cyclic seam immediately before
its state does not split a pure A-run, and fix P=(r,a_0,c_0). This
permits every spoke of a regular word (AC)^k or of a word without A's.
For nonnegative real vertex masses w of total W, put

    B = max_K w(K),                       default 0;
    Fmax = max_F w(F),                    default 0;
    D0 = sum_{K: Y(K) empty or {a_0}} w(K);
    M = W-w(P)-D0.

**Quantitative completion theorem.** Without any treewidth assumption
on attachments, there is an ambient geodesic Q such that every component
of G-(P union Q) has mass at most

    h = max{M/2, B, Fmax}.

In particular, light individual attachments and light long-fan regions
(mass at most W/2 each) suffice for exact-half completion of P. There is
no light-inner-patch hypothesis.

**All-mass corollary.** If every induced local torso G[K union N(K)]
has treewidth at most three, then every nonnegative mass assignment has
a separator consisting of at most two ambient geodesics, with each
remaining component of mass at most W/2. The two paths may both change
when an attachment or long fan is heavy. Singleton paths are allowed.

The planar unit-edge members are partial cases of Problem 31. Planarity
of the full G is unnecessary under the explicit structural and metric
assumptions. Nothing is claimed for arbitrary nonplanar graphs.

## Metric and component facts

Every inner branch vertex is at root distance two. Its subdivision
interiors are accessible only through their two arc endpoints, both in
H. Core isometry makes all distance calculations below valid in G.
The inner neighbors of any fixed outer vertex form a consecutive interval
of a pure C-run, or a singleton. Its interval has at most m-4 edges.
In particular, at a D-step from (a,c) to (b,d), the opposite edges ad,bc
are absent. An interval producing such an edge by wrapping would have
to contain at least m-1 C-steps. Consequently

    d(a,c)=d(b,d)=1, d(a,d)=d(b,c)=2.

For a singleton A-run a--b at c followed by a C-step to d, the same
interval argument gives d(a,c)=1 and d(a,d)=2. There is an analogous
statement on a preceding C-step. For a long A-run its outer endpoints
are nonadjacent, since 2<=t-l<=k-4. Thus a_l c_j a_t is a geodesic of
length two. All these statements refer to the original graph metric.

Here is the bookkeeping underlying every component bound. Discard the
attachments counted in D0: P already detaches each of them individually.
Partition the remaining vertices outside P into masses

    alpha_i = w(a_i)+sum_{Y(K)={a_i}} w(K) for i!=0;
    gamma_j = w(c_j) for j!=0;
    alpha_0=alpha_k=gamma_0=gamma_m=0;
    kappa_i = sum_{Y(K)={a_i,a_(i+1)}} w(K);
    tau_j = w(interior(T_j)).

The other indices run from zero to k-1 or m-1 as appropriate. These are
disjoint vertex sets, with total

    M=sum_i(alpha_i+kappa_i)+sum_j(gamma_j+tau_j).

Unroll the word from the chosen seam. At a visited cross state (i,j),
deleting P and (r,a_i,c_j) leaves every component meeting H within one
of the formal sides

    L(i,j)=sum_{s<i}(alpha_s+kappa_s)+sum_{q<j}(gamma_q+tau_q),
    R(i,j)=M-L(i,j)-alpha_i-gamma_j.

These expressions denote both sums and their underlying vertex sets
when support comparisons are made. Cut the outer and inner cycles at
their deleted vertices. Every cross edge occurs before or after (i,j)
in the monotone word and cannot connect the two surviving intervals.
An attachment has only one active vertex or two consecutive active
vertices, so it cannot bridge these intervals either. Each component
disjoint from H is a whole individual K and has mass at most B.
At seams, or when a boundary vertex has been deleted, the formal sides
may overestimate actual components. An aggregate kappa_i can be large;
deleting its two active endpoints detaches its K's individually.

For A and C steps respectively the changes are

    L'=L+alpha_i+kappa_i,  R'=R-alpha_(i+1)-kappa_i;
    L'=L+gamma_j+tau_j,    R'=R-gamma_(j+1)-tau_j.

A D-step performs both changes. Hence L is nondecreasing and R is
nonincreasing, from bounds (0,M) to (M,0). Since 2h>=M and L+R<=M,
no state has both sides heavier than h. If no spoke already completes P,
there is a step from a right-heavy state to a left-heavy state. Its old
left side and new right side are light. We repair this step below.
When h=0 all represented masses are zero and any spoke suffices.

## C-steps and long A-runs

For a C-step let T_j=(v_0,...,v_ell) from c_j to c_(j+1). Extend the
old root spoke through v_floor(ell/2), and the new spoke backwards
through v_ceil(ell/2). Both extensions are geodesics: the arc endpoints
have equal root distance two, and an interior vertex has no other
entry point. The old extension retains the old light left side; the
new extension retains the new light right side. Their potentially heavy
other sides have disjoint supports in M, because the two extensions
together delete every internal arc vertex. Both cannot exceed h.

If a transition occurs within an A-run of length at least two, take
the entire run l,...,t at c_j. Its first left side L and last right
side R are light by monotonicity. Use Q=(a_l,c_j,a_t), which is a
geodesic by the metric facts. After deleting P union Q, every component
meeting the core is contained in the first left side, last right side,
or F. One can check this by cutting the outer interval at l,t and the
inner cycle at j: the strictly internal outer chain has only c_j as an
inner neighbor and is separated from everything else. Its attachments
are exactly those defining F. These three bounds are all at most h.
The seam condition ensures that no A-run is split between the start
and end of the sweep.

## A singleton A-run needs just one neighboring C-step

Write its outer endpoints as a=a_l and b=a_(l+1), and its shared inner
vertex as c=c_j. Let L be the old light left side and R the new light
right side; write R_old and L_new for the other spoke bounds. If c=c_0,
it is already deleted by P, and Q=(a,b) leaves just bounds L,R, with
the sector attachments detached individually.

Otherwise the exclusion of DAD supplies a preceding or following C-step.
Suppose first that there is a following C-step, along
T_j=(v_0=c,...,v_ell=d). Put

    p=floor(ell/2), q=ceil((ell+1)/2), so q-1=p.

The old root extension U=(r,a,v_0,...,v_p) is a geodesic with bounds

    L, R_old-w({v_1,...,v_p}).

The outer detour V=(a,b,v_ell,...,v_q) is also a geodesic. Indeed
d(a,c)=1 and d(a,d)=2, and q>=(ell+1)/2 is precisely the condition
2+ell-q<=1+q. Its component bounds are

    L+gamma_j+w({v_1,...,v_(q-1)}), R.

To verify the latter bounds, remove a,b and the indicated suffix of
T_j. The undeleted c and the remaining prefix of T_j can join only the
old left interval; any surviving active incidence of c is on that side.
The right interval cannot reach c after b is deleted. The sector
attachments detach individually. This also covers boundary coincidences
at the chosen seam, where gamma_0=0.

The two potentially heavy bounds are disjoint subsets of the mass M:
R_old excludes L and gamma_j, and q-1=p makes their arc pieces disjoint.
Thus at least one of U,V completes P.

If only a preceding C-step is available, write its arc from d=c_(j-1)
to c as (v_0,...,v_ell), and put

    p=ceil(ell/2), q=floor((ell-1)/2), so q+1=p.

Use the new root extension (r,b,v_ell,...,v_p) or the detour
(b,a,v_0,...,v_q). Their respective bounds are

    L_new-w({v_p,...,v_(ell-1)}), R;
    L, R+gamma_j+w({v_(q+1),...,v_(ell-1)}).

The same distance and component arguments, reflected, apply. The two
potentially heavy sides again have disjoint support in M. No bound on
the mass near c, or on either adjacent arc, was required.

## Four geodesics across a D-step

Let the step be (a,c)=(a_i,c_j) to (b,d)=(a_(i+1),c_(j+1)), and
T_j=(v_0=c,...,v_ell=d). Write L for the old left side, R for the new
right side, and abbreviate

    alpha=alpha_i, beta=alpha_(i+1), gamma=gamma_j,
    delta=gamma_(j+1), kappa=kappa_i, tau=tau_j.

Then L,R are light and

    M=L+R+alpha+beta+gamma+delta+kappa+tau.

Put

    p=floor(ell/2), q=ceil(ell/2),
    u=floor((ell-1)/2), v=ceil((ell+1)/2).

There are four candidate geodesics:

    U1=(r,a,v_0,...,v_p),
    U2=(r,b,v_ell,...,v_q),
    U3=(a,b,v_ell,...,v_v),
    U4=(b,a,v_0,...,v_u).

For U1,U2 use equal root distances; for U3,U4 use the endpoint distances
1 and 2 and the offset midpoint inequalities, as in the singleton case.
No diagonal is inserted and shortestness is tested in the original G.

Each cut P union U_i has one light side bounded by L or R. Its only
possibly heavy side has the following bound, respectively:

    H1=R+beta+delta+kappa+w({v_(p+1),...,v_(ell-1)}),
    H2=L+alpha+gamma+kappa+w({v_1,...,v_(q-1)}),
    H3=L+gamma+w({v_1,...,v_(v-1)}),
    H4=R+delta+w({v_(u+1),...,v_(ell-1)}).

Empty ranges have mass zero. The first two bounds extend their original
root sides. For the third, a,b are removed and c with its remaining arc
prefix can join only the old left interval; for the fourth, d with its
remaining suffix can join only the new right interval. The
opposite cross edges are absent, so there is no additional connection.
The kappa attachments detach individually in the last two cuts.

Every internal arc vertex appears exactly twice in H1+H2+H3+H4.
For ell=2t, p=q=t, u=t-1, v=t+1: the middle vertex occurs in both
outer-detour bounds and neither root bound; every other vertex occurs
once in each kind. For ell=2t+1, p=u=t and q=v=t+1, so every internal
vertex occurs once in each kind. Consequently

    H1+H2+H3+H4=2M-alpha-beta<=2M<=4h.

Four failures would make this sum strictly greater than 4h. Thus one
candidate completes P. Together with the preceding cases, this proves
the quantitative completion theorem.

## Heavy regions and the all-mass corollary

Only an individual attachment K or a long fan F can now obstruct the
condition h<=W/2. Their reductions are those of the
[fan-annulus theorem](../planar_two_geodesic_fan_annuli/README.md), restated
here to make the use of original-graph balance explicit.

For a heavy K, take a width-three decomposition of its torso. Its
boundary is a clique of order at most three, contained in a bag. Attach
the outside bag V(G)-K as a leaf there. Assign the masses of K to local
bags and all other masses to the outside leaf. The weighted centroid
of this tree cannot be the outside leaf, whose sole branch has mass
w(K)>W/2. A local bag of order at most four therefore half-separates
the full G. Pair its vertices and cover them by at most two ambient
geodesics; deleting their whole union preserves balance. This is the
[reviewed heavy-attachment reduction](../planar_two_geodesic_prescribed_attachment_review1/REVIEW.md).

For a heavy F from the run l,...,t at c_j, F is exactly one component
after deleting {r,c_j,a_l,a_t}. Its strictly internal outer chain is
connected, and each included two-active attachment meets that chain.
Use the path of bags

    {r,c_j,a_l,a_s,a_(s+1)}, s=l,...,t-1.

Its last bag contains the whole boundary. Glue each local attachment
decomposition to a bag containing its clique boundary, and attach the
outside leaf V(G)-F to the last core bag. This is a tree decomposition:
the bags cover every edge, each core vertex occurs in an interval, and
each glued decomposition meets its host in precisely its boundary.
Assign F's mass locally and all other mass outside. Again a weighted
centroid is local. Each local core bag is covered by the geodesic
(r,a_s,c_j) and a geodesic joining its at most two remaining vertices;
each guest bag has at most four vertices and is covered by pairing.
Thus its full-graph half-separator bag is covered by two ambient
geodesics. This proves the corollary. The special five-vertex bags do
not imply such a covering theorem for arbitrary treewidth-four graphs.

## Scope and relation to earlier results

The class allows arbitrarily many genuine D-faces, including the matching
interface D^k, and arbitrarily long permitted A- and C-runs. Every old
fan word with at least five alternating blocks satisfies the wrap
bounds. A single removal of a cross diagonal in such a word is covered
when the resulting word satisfies the displayed bounds. This is a
comparison of displayed core hypotheses, not a classification of all
alternative representations of the same graph.

On the unit regular subfamily (AC)^k, long F's are absent. Thus every
spoke P can be completed with residual bound max{(W-w(P)-D0)/2,B},
irrespective of inner-patch masses and with no torso-width assumption.
This is stronger than the conditional prescribed-spoke conclusion in
the earlier [subdivision theorem](../planar_two_geodesic_subdivided_annuli/README.md),
which needed light inner patches. The earlier theorem remains broader
in the metric direction, allowing nonuniform positive subdivision edges.

That metric restriction matters to the new proof. For lambda=4 and
one inner arc with successive edge lengths 3,2,3, the internal vertex
positions are 3,5 along total length 8. Root midpoint cuts stop at 3,5,
but the offset outer cuts at thresholds 2,6 stop at the endpoints 0,8.
The four paths remain geodesics, yet each internal vertex appears
three times in the four side bounds. The displayed twofold identity
therefore fails. This is an obstruction to this proof identity, not a
counterexample to a separator assertion.

The excluded DAD pattern is likewise an unhandled local configuration,
not a negative example. Other restrictions remain: an isometric capped
annular core, root-clique attachment boundaries, and the local width
assumption for arbitrary heavy attachments. The primary
[Diot--Gavoille paper](https://emilie-diot.eu/Article/DG10a)
already gives strong two-path separability for face-separable weighted
graphs. We do not assert disjointness from that class or historical
novelty from a targeted literature search.

## Reproduction and trust boundary

From the repository root, use Python 3.11+ and its standard library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_quadrilateral_annuli/verify.py --check
```

The output must exactly equal [expected.json](expected.json). The run
used Python 3.11.2. The checker imports graph, distance, decomposition,
and heavy-case helpers from preceding contribution directories in this
repository; the new proof does not depend on a solver or external data.

Six deterministic fixtures use words D^5, (DCC)^5, (DAC)^5, (CAD)^5,
AAADCCAACDDAACCCD, and (AC)^6. They have unit rim subdivisions of one
through six edges, multiple attachments in every sector, and one
fixture with core length two and outside edges of length one. All
eligible cyclic seams are checked. Mass profiles include the earlier
exact fixture profiles, arc-interior concentration, and long-fan
concentration; random choices use seed 2026092814. Forty additional
bounded random words and reflections test geometry and component sets,
not a mass census. The script directly checks all selected path lengths
against original-graph distances, spherical rotations, core isometry,
component containment, coefficient identities, decomposition axioms,
and residual masses after both the quantitative and heavy-case choices.

Expected totals include 75 full systems, 6,128 component cuts, 520
quadrilateral identities, 272 one-sided identities, 23,253 quantitative
mass checks, 13,141 light half-balance checks, 9,774 heavy-attachment
checks, and 338 heavy-fan checks. In 7,791 sampled cases the quantitative
bound is strictly smaller than W/2. The DAD control checks hypothesis
rejection only; the nonuniform control checks the identity failure just
described. These are finite exact regressions, not exhaustive graph
enumeration, independent peer review, or formal verification. The
universal assertions rest on the component, metric, and centroid proof.
