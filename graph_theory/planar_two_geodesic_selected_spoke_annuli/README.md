# Selecting the first spoke in mixed annuli

Choosing the first path according to the vertex masses removes the
`DAD` exclusion from the preceding
[quadrilateral-annulus theorem](../planar_two_geodesic_quadrilateral_annuli/README.md)
when the inner edges are not subdivided. Arbitrary triangular fans and
quadrilateral faces are allowed. A maximum aggregate sector determines
the first spoke; one additional ambient geodesic gives the same sharper
residual bound as before. Local attachment treewidth at most three then
gives an exact-half separator for every vertex weighting.

The choice of spoke matters. A 52-vertex unit planar control below has
three light attachments, all with local treewidth at most three, but a
specified spoke cannot be completed at half balance. Two freely chosen
paths do balance it. This is not a counterexample to
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

**Literature status, 28 September 2026.** The official
[workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html)
announces a Pilipczuk disproof of a Codsi conjecture about planar balanced
separators, without stating the exact claim or giving a witness. A narrow
primary-source check, including the linked
[workshop paper list](https://web.math.princeton.edu/~pds/barbadospub.pdf)
and [Codsi's author bibliography](https://arxiv.org/a/codsi_j_1.html), did
not locate an exact account. This does not establish continued openness
of Problem 31. We claim neither a resolution of that unrestricted question
nor historical priority. The extension below awaits independent review.

## Construction and result

Take a cyclic word in A, C, D with increments

    A=(1,0), C=(0,1), D=(1,1).

Let k=#A+#D and m=#C+#D. Require

    k,m>=3;
    every cyclic pure A-run has length <=k-2;
    every cyclic pure C-run has length <=m-2.

Use an outer cycle a_0,...,a_(k-1), an inner cycle c_0,...,c_(m-1), and
root r adjacent to all a_i. Each visited staircase state (i,j) gives a
cross edge a_i c_j, with indices modulo k,m. A- and C-steps describe
triangular faces and D-steps describe quadrilateral faces with neither
diagonal added. The wrap bounds prevent repeated cross states and the
exceptional incidences used below; they are sufficient, not asserted sharp.

Root, outer-cycle, and cross edges have common length lambda>0. Each
inner edge is a **single unsubdivided edge** of any length at least lambda.
There are no other edges in the core H. All unit-edge members are included.

Let G be a finite connected simple positive-edge-length graph containing
H isometrically, with no extra edges between vertices of H. Each component
K of G-V(H) has its boundary N(K) contained in one of

    {r}, {r,a_i}, {r,a_i,a_(i+1)}.

This includes zero-mass components. Define the active boundary
Y(K)=N(K) intersect {a_i}. Outside edge lengths are arbitrary subject to
core isometry; lengths at least lambda/2 suffice because the permitted
boundaries are cliques with edge length lambda.

Give the vertices nonnegative real masses of total W. Write

    kappa_i=sum_{Y(K)={a_i,a_(i+1)}} w(K).

An isolated A-step with a D-step immediately on both sides is called a
DAD sector. If there are any, choose a DAD sector maximizing kappa_i
**among DAD sectors**, and put its step first in the word. Relabel its
outer endpoints a_0,b_0=a_1 and its inner vertex c_0. Set

    P=(r,a_0,c_0).

If there is no DAD sector, choose any cyclic seam not splitting an A-run
and use its spoke as P. Ties among maximum sectors may be broken arbitrarily.
The selection uses aggregate sector mass, not the largest individual K.

For every maximal A-run from a_l to a_t at c_j with t-l>=2, let F contain
its strictly internal outer vertices, all K with sole active boundary at
one of these vertices, and all K with two active boundary vertices that
are the endpoints of an outer edge of this run. Put

    B=max_K w(K), Fmax=max_F w(F),       with empty maxima zero;
    D0=sum_{K: Y(K) empty or {a_0}} w(K);
    M=W-w(P)-D0.

**Quantitative completion theorem.** One ambient G-geodesic Q completes
the selected P so that each component of G-(P union Q) has mass at most

    h=max{M/2,B,Fmax}.

No treewidth assumption is needed for this assertion. In particular,
light individual attachments and light long fans suffice for half balance.

**All-mass corollary.** If every induced torso G[K union N(K)] has
treewidth at most three, every nonnegative vertex weighting admits a
separator consisting of at most two ambient geodesics, with every residual
component of mass at most W/2. Both paths may change in the heavy cases.
Singleton paths are allowed.

Planarity of the whole G is not required under these explicit assumptions.
Its planar unit-edge members give the claimed sufficient class for
Problem 31. No arbitrary nonplanar-graph claim follows.

## Geometry and accounting

Normalize lambda=1. Every core edge has length at least one, and every
c_j is at root distance two. Core isometry transfers all the following
shortestness statements to G.

An outer vertex's inner neighbors form a pure C-run interval, or a
singleton. The bound m-2 excludes an interval wrapping around from c_j
to c_(j+1) the long way. Hence a D-step (a,c) to (b,d) has no opposite
cross edges ad,bc; both (a,b,d) and (b,a,c) are geodesics of length two.
Likewise, if a singleton A-step a--b at c is followed by a C-step to d,
then ad is absent and (a,b,d) is geodesic; reflect for a preceding C-step.
A long A-run's endpoints are nonadjacent because 2<=t-l<=k-2, so
(a_l,c_j,a_t) is geodesic.

For a DAD sector, its two outer endpoints each have exactly one inner
neighbor, namely its center c_j, and c_j has exactly these two outer
neighbors. This follows from the immediately preceding and following D
steps. Suppose the selected sector is a_0--b_0 at c_0. For the center c_j
of any other DAD sector with j not in {0,1,m-1},

    d_G(b_0,c_j)=3.

Indeed there is a length-three route through r. There is no one- or
two-edge route in H: b_0's neighbors are r, a_0, the next outer vertex,
and c_0. The root is not adjacent to c_j, and a_0 has only inner neighbor
c_0. If the next outer vertex were incident with this DAD center, it
would be the first endpoint of that sector immediately after the D-step
from b_0, forcing j=1. Finally c_0's inner neighbors are only c_1,c_(m-1).
Thus no two-edge route exists; the edge lower bounds finish the distance
check. Notice that arbitrary C-fans elsewhere do not change this argument.

Discard the K's counted in D0: P has detached each of them individually,
and each has mass at most B. Partition the remaining vertices outside P as

    alpha_i=w(a_i)+sum_{Y(K)={a_i}} w(K) for i!=0;
    gamma_j=w(c_j) for j!=0;
    alpha_0=alpha_k=gamma_0=gamma_m=0;
    kappa_i=sum_{Y(K)={a_i,a_(i+1)}} w(K).

Their total is M=sum_i(alpha_i+kappa_i)+sum_j gamma_j. Expressions below
also denote their disjoint underlying vertex sets when inclusions are used.
At a cross state (i,j), deleting P and the spoke (r,a_i,c_j) leaves each
component meeting H within one formal side

    L(i,j)=sum_{s<i}(alpha_s+kappa_s)+sum_{q<j}gamma_q,
    R(i,j)=M-L(i,j)-alpha_i-gamma_j.

To check this, cut the two cycles at the deleted endpoints. Cross edges
come from states before or after (i,j) in the monotone word. A single-active
attachment or one consecutive outer sector cannot bridge the two surviving
intervals. Components disjoint from H are whole individual K's. The formal
bounds can overestimate actual components at deleted endpoints or seams.

A- and C-steps change the bounds by

    A: L'=L+alpha_i+kappa_i, R'=R-alpha_(i+1)-kappa_i;
    C: L'=L+gamma_j,         R'=R-gamma_(j+1).

D performs both changes. Thus L increases and R decreases, from (0,M)
to (M,0), and L+R<=M<=2h. If no spoke already completes P, some step goes
from a right-heavy state to a left-heavy state. Its old L and new R'
are light. A C-step cannot be that transition: its R+L'=M-alpha_i<=2h.
If h=0, all represented and detached masses are zero, so any spoke works.

## Exchanges except DAD

For a D-step abbreviate its two outer endpoint masses by alpha,beta,
its inner endpoint masses by gamma,delta, and its sector mass by kappa.
Let L be the old left side and R the new right side. Then

    M=L+R+alpha+beta+gamma+delta+kappa.

The old and new root spokes and the detours (a,b,d), (b,a,c) each retain
one light side. Their possibly heavy other bounds are

    R+beta+delta+kappa, L+alpha+gamma+kappa, L+gamma, R+delta.

Their sum is 2M-alpha-beta<=4h, so they cannot all exceed h. Sector
attachments detach individually when both outer endpoints are deleted.
This argument uses no added diagonals and no unit length assumption on
the unsubdivided inner edge.

For a transition inside a long A-run, take the entire run l,...,t at c_j.
Its initial left bound L and final right bound R are light by monotonicity.
The geodesic Q=(a_l,c_j,a_t) leaves core components within these two sides
or F. The strictly internal outer chain has only c_j as an inner neighbor;
its boundary is contained in {r,c_j,a_l,a_t}, and its attachments are exactly
those included in F. All three bounds are at most h.

For a singleton A-step with c_j=c_0, that inner vertex is already deleted.
The outer edge (a_i,a_(i+1)) leaves just the old-left and new-right sides,
plus individually detached K's. Otherwise, if a C-step follows, use
Q=(a_i,a_(i+1),c_(j+1)), with bounds (L+gamma_j,R'). The potentially heavy
left side is disjoint from the old heavy R within mass M, so it is light.
If only a preceding C-step is available, use the reflected detour
(a_(i+1),a_i,c_(j-1)), with bounds (L,R'+gamma_j); its potentially heavy
right side is disjoint from the new heavy L'. These inclusions follow
by cutting the same cyclic intervals, leaving the undeleted c_j on the
indicated side. This handles every singleton A-step except DAD.

## Repairing DAD by selecting the first spoke

There is a DAD sector only in the selection case, so P starts at a
maximum sector a_0--b_0 at c_0. Let a--b at c_j be the sector of the
heavy-side transition. Its aggregate kappa satisfies kappa<=kappa_0.
The j=0 case was already handled. Three cases remain.

**A nonadjacent inner center.** If j is neither 1 nor m-1, use

    Q=(b_0,r,b,c_j).

It is geodesic by d(b_0,c_j)=3. Compared with the new root spoke, it also
deletes b_0. Since a_0 was in P, every K in the anchor sector kappa_0 is
now detached individually. These K's belonged to L', so the core-side
bounds improve to

    L'-kappa_0, R'.

The old right-heavy inequality says

    L+alpha_a+gamma_j < M-h.

Consequently

    L'-kappa_0
      =L+alpha_a+kappa-kappa_0
      <M-h-gamma_j+kappa-kappa_0
      <=h.

The other side R' was already light. Detached K's have mass at most B.
This is the only case that uses maximality of the anchor sector.

**The next inner center.** If j=1, the two DAD sectors force four
consecutive outer vertices a_0,b_0,a,b: there can be no intervening C-step
or longer A-run. Write kappa_bridge for the sector b_0--a. Since the inner
edge c_0c_1 is unsubdivided, the new heavy left side is exactly

    L'=kappa_0+alpha_(b_0)+kappa_bridge+alpha_a+kappa > h.

Use Q=(b_0,a,b), a geodesic of length two. P union Q removes every active
vertex in this expression and both endpoints of all its sectors. Thus
every represented vertex of L' is deleted or lies in an individually
detached K. Every other represented component has mass at most M-L'<h.
The already discarded K's also remain separate and light.

**The preceding inner center.** If j=m-1, the local outer order is a,b,a_0.
The old heavy right side is exactly

    R=kappa+alpha_b+kappa_bridge > h,

where the bridge sector is b--a_0. Use Q=(a,b,a_0), again a geodesic of
length two. All groups in R are deleted or detached individually; the
remaining represented mass is M-R<h. The wrap bounds ensure the endpoints
of both three-outer-vertex paths are nonadjacent. In fact these cases
contain two distinct DAD sectors, so k>=5.

This exhausts the transitions and proves quantitative completion. It
also explains precisely where the lack of rim-interior vertices is used:
otherwise positive interior mass would occur in these near-center heavy
sides without being removed by the short outer path.

## Heavy attachments and fans

For completeness, the all-mass reduction is the one in the
[fan-annulus theorem](../planar_two_geodesic_fan_annuli/README.md).
A weighted centroid bag in a tree decomposition half-separates the graph:
assign every vertex's mass to one containing bag and take a centroid of
the resulting weighted decomposition tree. Covering that bag by geodesics
only deletes more vertices and preserves balance.

If an individual K has mass greater than W/2, take a width-three torso
decomposition. Its boundary is a clique of order at most three, contained
in a bag. Attach the outside bag V(G)-K as a leaf there. Assign K's mass
locally and all other mass to the outside leaf. A centroid cannot be that
leaf, whose branch has mass w(K)>W/2. The local centroid bag has at most
four vertices and is covered by two ambient geodesics by pairing vertices.
This is the [reviewed heavy-attachment argument](../planar_two_geodesic_prescribed_attachment_review1/REVIEW.md).

If a long fan F is heavy, it is one whole component after deleting
{r,c_j,a_l,a_t}. Use the path of bags

    {r,c_j,a_l,a_s,a_(s+1)}, s=l,...,t-1.

Glue every included attachment's width-three decomposition to a bag
containing its clique boundary, and attach V(G)-F as an outside leaf to
the last core bag. Edge coverage and the running-intersection property
are immediate from the consecutive outer chain and the clique gluing;
the last bag contains the whole fan boundary. Assign F's mass locally.
A centroid is local. Each core bag is covered by (r,a_s,c_j) and a geodesic
joining its at most two remaining vertices. Each guest bag has at most
four vertices and is covered by pairing. Hence a full-G half-separator
bag is covered by two ambient geodesics. This is a special decomposition,
not a statement about arbitrary treewidth-four graphs.

If neither heavy case occurs, h<=W/2 in the quantitative theorem, proving
the corollary. No planarity of attachments was used in this reasoning.

## Why arbitrary first spokes cannot be retained

The compact [control.json](control.json) specifies an instance with
word (AD)^5, all core edges unit, and twelve successive insertions into
triangular faces in each of three root sectors. Every inserted vertex
is adjacent to the three corners of its face. This proves planarity
inductively and gives width-three local torsos by reverse insertion.
The original core remains isometric because all attachment boundaries
are unit cliques. The graph has 52 vertices and 143 edges.

The listed nonnegative integer masses total 37 and vanish on the core.
The three outside components have masses 14,14,9; each is light. There
are no long fans. Nevertheless the prescribed spoke P=(0,1,11) has

    min_{ambient geodesics Q} max_{components K of G-(P union Q)} w(K)
      =19 > 37/2.

The path (10,9,8,34) attains 19. The unrestricted pair (0,10,15) and
(9,0,6,13) instead has largest residual mass 14. The selected-maximum
rule also passes for every tied maximum sector on this instance.
Thus this control disproves an arbitrary-spoke strengthening with light
attachments even under local width three. It does not say the maximum
rule is necessary for every successful spoke, and it is not a negative
instance of Problem 31 (which asks for freely chosen paths and vertex count).

This finite obstruction is checked exhaustively by two implementations.
The main checker uses the earlier Dijkstra and shortest-path DFS helpers.
The separate [audit.py](audit.py) imports none of those implementations:
it reconstructs the literal graph, checks face insertions and torso
elimination, computes distances by Floyd--Warshall, and builds all
geodesic vertex sets by dynamic programming on decreasing distance to
the destination. The recurrence includes every shortest first step, so
induction on distance proves completeness. Both enumerate 3,489 distinct
geodesic vertex sets, including singleton paths and every endpoint pair.
Merging paths with the same vertex set does not change deletion components.
The audit computes every residual component in the original graph and
checks the attaining and positive free-path witnesses.

## Reproduction and scope

Python 3.11+ and its standard library suffice; the run used Python 3.11.2.
From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_selected_spoke_annuli/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_selected_spoke_annuli/audit.py
```

The first output must match [expected.json](expected.json). Its 15 fixture
graphs include inner triangles and quadrilaterals, arbitrary C-fans,
long A-fans, many DAD sectors, unequal inner edge lengths, and core edges
of length two with outside edges of length one. All maximum-sector ties
are tested for each mass profile. The profiles include uniform masses,
individual vertices, strict-heavy and equality attachment cases, random
integer masses with seed 2026092815, long-fan concentration, and a forced
backward-neighbor exchange. Fifty additional bounded random words test
core geometry and component inclusions. The 52-vertex obstruction is a
separate additional fixture. Expected totals are 83 systems, 2,702
component cuts, 417 D identities, 278 C identities, 5,003 quantitative
checks, 2,585 heavy-attachment checks and 102 heavy-fan checks. All exchange
branches are exercised. The zero C-choice count is expected: such a
transition cannot have both required heavy sides.

The separate audit prints:

```text
vertices=52 edges=143 geodesic_sets=3489 total_mass=37 attachment_masses=9,14,14 fixed_optimum=19 free_largest=14 PASS
```

The universal theorem rests on the written metric, component and centroid
proof, not on finite mass sampling. The control obstruction is a finite
exhaustive computation with the stated completeness argument. The separate
audit is not independent peer review or formal verification.

The theorem covers DAD sectors and weaker wrap bounds but requires
unsubdivided inner edges. The preceding subdivision results retain their
own broader rim hypotheses; the two claims should not be combined without
a proof. Wider attachment boundaries and arbitrary annular incidence
beyond the stated staircase remain outside the result. The classical
[Diot--Gavoille paper](https://emilie-diot.eu/Article/DG10a) already supplies
other weighted exact-half two-path classes; no disjointness or priority
claim relative to all those classes is made here.
