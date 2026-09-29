# Two-parent metric anchors for half separators in mixed annuli

A branch with two outer parents can carry a prescribed-triple
two-geodesic separator. Two long incident inner arcs give its distance
profile; a local incidence condition supplies the complementary paths.
The resulting bound has neither a fan-mass term nor a requirement to
choose an anchor sector of maximum mass.

This extends the anchor method to configurations excluded by the
[single-parent theorem](../planar_two_geodesic_anchor_mixed_annuli/README.md),
including every ring `(AD)^t`, `t>=3`, at a branch whose incident inner
arcs have total length at least twice the wheel-edge length. It is a
conditional structural result for
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf),
not an unrestricted resolution. Unit all-mass cases already covered by
the [mixed-annulus theorem](../planar_two_geodesic_subdivided_mixed_annuli/README.md)
are not counted as new cases; the new claim is the metric and
prescribed-triple extension under the hypotheses below.

The present extension awaits independent review. The official
[schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html)
announces a Codsi-conjecture disproof; its exact statement and witness
remain unmatched in our bounded primary-source audit, refreshed
29 September 2026. We assert neither continued openness nor priority.

## Hypotheses and statement

Use a cyclic incidence word with steps `A=(1,0)`, `C=(0,1)`, `D=(1,1)`.
Put `k=#A+#D>=5`, `m=#C+#D>=3`. Require every cyclic pure A-run to
have length at most `k-2` and every pure C-run at most `m-2`.
The capped annular core H consists of root r, outer cycle
`a_0,...,a_(k-1)`, all spokes `ra_i`, and inner branches
`c_0,...,c_(m-1)`. Add precisely the cross edges `a_i c_j` at the
visited states of the word. Join successive branches by internally
disjoint paths T_j with degree-two interiors. All root, outer and
cross edges have a common positive length lambda. Individual inner
edge lengths are arbitrary positive reals, with totals `ell_j>=lambda`.

Choose an oriented DAD sector as anchor: the word, started at
`(a_0,c_0)`, begins `AD` and its final letter is D. Thus c_0 has exactly
the two outer parents a_0,a_1, and both these outer vertices have c_0
as their only inner neighbor. Impose

```
ell_0 >= 2*lambda,    ell_(m-1) >= 2*lambda;              (1)
(N_C(a_2) union N_C(a_3)) intersect N_C(a_(k-1)) = empty. (2)
```

Here N_C records only inner branch neighbors through cross edges.
Condition (2) is an incidence restriction, with the indicated cyclic
orientation; reversing the orientation is allowed if the resulting
conditions hold. Only the two arcs incident with c_0 need the larger
lower bound in (1).

Let G be finite, connected and simple, with positive edge lengths.
It contains H induced and isometrically. Every component K of
`G-V(H)`, including every zero-mass one, has boundary contained in
`{r}`, `{r,a_i}` or `{r,a_i,a_(i+1)}`. There are no inner attachments.
The core is planar by its cyclic construction. The theorem does not
need full-G planarity under these structural hypotheses.

For arbitrary nonnegative real vertex masses of total W put

```
P=(r,a_0,c_0),    S0={r,a_0,c_0};
Y(K)=N(K) intersect {a_i};
D0=sum of w(K) over Y(K) empty or {a_0};
B=max_K w(K), with default 0;
M=W-w(S0)-D0.
```

**Quantitative theorem.** At most two original-G shortest paths have a
union containing S0 whose deletion leaves every component of mass at most

```
h=max{M/2,B}.                                           (3)
```

The sector of a_0a_1 need not be maximal in mass. There is no bound on
the aggregate mass of a long fan. No local treewidth hypothesis is
needed for (3). The three anchor vertices are retained collectively;
P need not remain as one of the paths.

**All-mass corollary.** If each induced torso `G[K union N(K)]` has
treewidth at most three, every nonnegative weighting admits a separator
equal to the union of at most two ambient geodesics with residual mass
at most W/2. In a heavy-attachment case its paths may change the anchor.

**Necklace corollary.** For word `(AD)^t`, `t>=3`, condition (2) holds
at every branch in either orientation. Any branch with both incident
arc totals at least `2*lambda` is an eligible anchor. If all inner
totals satisfy this bound, any branch and either of its outer parents
can be prescribed together with r in (3). Every inner branch has two
outer parents, so no branch meets the previous single-parent criterion.

## Distances and carriers

The outer wheel W0 is isometric: an excursion between two outer
vertices through the inner region uses two cross edges and costs
at least `2*lambda`, no less than their wheel distance. Every branch
has root distance `2*lambda`.

A path from c_0 to an outer vertex either exits through one of its
two cross edges or traverses a whole incident inner arc first. The
second option costs at least `3*lambda`, including its exit cross
edge, by (1). Since the direct parent routes cost at most that,

```
d_G(c_0,a) = lambda + min{d_W0(a_0,a),d_W0(a_1,a)}.      (4)
```

This is an exact distance identity under the stated assumptions.
The following are therefore ambient geodesics:

```
E_0 = (c_0,a_0);
E_1 = (c_0,a_1);
E_2 = (c_0,a_1,a_2);
E_(k-1) = (c_0,a_0,a_(k-1));
E_i = (c_0,a_0,r,a_i), for all other i.
```

Except at indices 1,2, these carriers contain c_0,a_0. The carrier
E_2 omits a_0 and r, so its complementary path must supply both.

For every branch c adjacent to a_2 or a_3, condition (2) gives

```
d_G(a_0,c)=3*lambda.                                    (5)
```

Indeed, c is not c_0. A two-edge route from a_0 through an outer
neighbor to c could use a_1 or a_(k-1). The first has only inner
neighbor c_0 and the second is excluded by (2). Exiting a_0 directly
through c_0 and then following an inner arc costs at least `3*lambda`
by (1). Any other route through an inner branch pays at least two
wheel/cross edges and one entire inner arc before reaching c, again
at least `3*lambda`. A route through r and a_2 or a_3 attains equality.

At a D-step `(a,c)` to `(b,d)`, opposite cross edges ad,bc are absent
by the cyclic run bounds. Consequently

```
d(a,c)=d(b,d)=lambda,    d(a,d)=d(b,c)=2*lambda.          (6)
```

One way to see the absent incidences is to unroll the word at the
D-step. The two opposite incidences would respectively require a run
of `k-1` A-steps or `m-1` C-steps around the remaining boundary; the
bounds exclude both. No shorter indirect route beats the stated distances,
since a whole inner arc costs at least lambda. Isometry transfers
all of these core calculations to G.

For an inner arc `T=(v_0=c,...,v_n=d)` of length ell, let
`0=x_0<...<x_n=ell` be its vertex coordinates. Its only entry points
are c,d. An explicit shortest path to c extends geodesically to v_s
when

```
d(z,c)+x_s <= d(z,d)+ell-x_s,                            (7)
```

and the reversed inequality certifies extension from d. All following
thresholds allow ties and arbitrary nonuniform vertex coordinates.

## Sweep and the component lemma

Deleting S0 already detaches every K counted by D0 individually, at
cost at most B. Partition the remaining represented vertices into

```
alpha_i = {a_i} and K with Y(K)={a_i}, i!=0;
gamma_j = {c_j}, j!=0;
alpha_0=alpha_k=gamma_0=gamma_m=empty;
kappa_i = K with Y(K)={a_i,a_(i+1)};
tau_j = interior(T_j).
```

Use the same symbols for sets or their masses. Their union has mass M.
At an unrolled state (i,j) set

```
L(i,j) = union of alpha_s,kappa_s for s<i
         and gamma_t,tau_t for t<j;
R(i,j) = represented vertices minus L(i,j),alpha_i,gamma_j.
```

The root spokes P and `(r,a_i,c_j)` are geodesics. Deleting their union
leaves each component meeting H in L or R. More generally, the same
interval cut gives these containments:

* At an A-step `(a,c)` to `(b,c)`, deleting S0,a,b,c leaves core
  components in the old L or new R.
* At D, deleting S0,a,b and the suffix `v_q,...,v_n=d` leaves core
  components in `L_old union gamma_c union {v_1,...,v_(q-1)}` or R_new.
* Deleting S0,a,b and the prefix `v_0=c,...,v_p` leaves them in L_old
  or `R_new union gamma_d union {v_(p+1),...,v_(n-1)}`.

For proof, cut the two boundary cycles at the listed deleted vertices.
The monotone incidence word places each remaining cross edge within
one of the two surviving intervals. In the D-suffix case the surviving
c and initial arc segment have only old-side incidences; there is no
opposite cross edge bc. Reflect for the prefix case. At A, deletion of
the shared branch cuts the fan between a,b. Attachments cannot bridge
the intervals, because their active sites are at most two consecutive
outer vertices. Those with all boundary vertices deleted detach as
whole K. Additional core deletions only split components further.
No candidate path deletes any vertex of K.

The same reasoning at a C-step uses its common outer vertex and an
inner prefix or suffix. This is the cut-containment lemma, including
seams where a_0,c_0 have already been removed.

L increases and R decreases from `(0,M)` to `(M,0)` with `L+R<=M<=2h`.
Unless a spoke pair already works, the first transition with new L>h
has old R>h. Its old L and new R are light. Write these as L,R below.
Every repair preserves S0. Mass zero causes no exception.

## A-steps, including the exceptional carrier

At `(a_i,c)` to `(a_(i+1),c)` with `i!=2`, take E_i and the cross
edge `(a_(i+1),c)` if E_i contains r, or the root spoke
`(r,a_(i+1),c)` otherwise. The second path is shortest by its length
lambda or `2*lambda`. The index i=1 does not occur: a_1 exits the anchor
by D. The pair deletes S0 and both outer endpoints and c, so the
component bounds are the light L,R and individual detached K.

If i=2, use instead

```
(c_0,a_1,a_2),    (a_0,r,a_3,c).
```

Their lengths are `2*lambda` and `3*lambda`. Equations (4),(5) prove
shortestness. Together they supply every anchor vertex and delete
a_2,a_3,c; the extra deletion of a_1 only helps. The same component
bounds prove (3). This handles each individual A-step, even inside
a long fan, without selecting a maximal sector or bounding fan mass.

## C-steps

Retain P. For a C-step across T with common outer parent a, extend
the old root spoke to the last p with `2*x_p<=ell`, or the new root
spoke backwards to the first q with `2*x_q>=ell`. Root distances to
the two branch endpoints are equal, so (7) proves both paths shortest.
The other potentially heavy supports are

```
R_old minus {v_1,...,v_p},
L_new minus {v_q,...,v_(n-1)}.
```

They are disjoint subsets of the represented mass because `q<=p+1`.
One has mass at most h; its accompanying other side is already light.
Individual detached K have mass at most B.

## D-steps away from the first anchor transition

Let the step be `(a,c)` to `(b,d)` across T. First suppose its old
outer index is not 1 or 2. Use E_a. If it contains r, start the other
path at b and take the reversed arc suffix from d through the first q
with `2*x_q>=ell-lambda`. Otherwise prepend r and use threshold ell.
By (6),(7) and the root distances, the second path is geodesic. The
pair's component bounds are

```
H_left = L union gamma_c union {v_1,...,v_(q-1)},    R.    (8)
```

Reflect using E_b. If it contains r, use the path from a through c
and the prefix ending at the last p with `2*x_p<=ell+lambda`.
Otherwise prepend r and use threshold ell. This gives bounds

```
L,    H_right = R union gamma_d union {v_(p+1),...,v_(n-1)}. (9)
```

The only D-step entering outer index 2 is the first anchor transition
handled below; no D-step enters outer index 1. Thus these reflected
carriers do contain a_0,c_0. The first threshold is at most ell and
the second at least ell, so H_left,H_right are disjoint subsets of M.
Both cannot be heavier than h.

For a D-step whose old outer index is 2, the reflected pair (9) remains
valid. Replace only the first pair by E_2 together with

```
(a_0,r,a_3,d,v_(n-1),...,v_q),
q = first index with 2*x_q>=ell.
```

Both c,d are adjacent to a_2 or a_3, so (5) gives equal start-to-end
distances `3*lambda` and (7) proves shortestness. This path supplies
a_0,r missing from E_2. The component bounds remain (8), with extra
deletion of a_1. Its threshold ell is at most the reflected threshold,
so the disjoint-support proof still applies.

## The first D-step after the anchor

This is `(a_1,c_0)` to `(a_2,c_1)` across T_0. Here the old left
group L is precisely kappa_0. Put ell=ell_0 and define

```
p = last index with 2*x_p<=ell+2*lambda;
q = first index with 2*x_q>=ell+lambda.
```

Both thresholds lie in `[0,2*ell]` by (1), and `q<=p+1`.
The first pair is

```
U=(a_0,c_0,v_1,...,v_p),    V=(r,a_1).
```

The distances from a_0 to c_0,c_1 are lambda and `3*lambda` by (5),
so U is geodesic by (7); V is an edge. The pair contains S0 and deletes
a_1. Every remaining core component lies in

```
H1=R_old minus {v_1,...,v_p}.                            (10)
```

There is no surviving core on the old left: it consists only of the
anchor sector's attachments, which detach individually after deleting
r,a_0,a_1. Removing the initial inner prefix can only reduce the right
component. Formula (10) may overestimate when p=n and c_1 is also removed.

The second pair is

```
P,    Q=(a_1,a_2,c_1,v_(n-1),...,v_q).
```

The distances from a_1 to c_0,c_1 are lambda and `2*lambda`; hence
Q is geodesic at the stated threshold. This pair deletes the two
outer endpoints and both c_0,c_1. The unremoved initial arc segment
is isolated, with support

```
H2={v_1,...,v_(q-1)}.                                   (11)
```

Other core components lie in the new light R; sector kappa_0 and all
other fully detached attachments again cost at most B each.
By `q<=p+1`, H1 and H2 are disjoint subsets of M. One is light, proving
(3) for this last exceptional transition and completing the sweep.

## Heavy attachments

If all K have mass at most W/2, (3) gives the half-separator corollary.
Otherwise take a width-three tree decomposition of a heavy K's torso.
Its boundary is a clique of order at most three and lies in one bag.
Attach `V(G)-K` as an outside leaf there and assign all outside mass
to that leaf, K's mass to local bags. A weighted centroid cannot be
the leaf, since its only branch has mass greater than W/2. Its local
bag has at most four vertices and half-separates the whole G. Pair
those vertices using at most two ambient geodesics; deleting their
whole union preserves balance. This is the existing
[reviewed attachment reduction](../planar_two_geodesic_prescribed_attachment_review1/REVIEW.md).

## A 19-vertex unit-edge control

Use word `(AD)^3`, so there are six outer vertices and three branches.
Subdivide each inner edge once, with all resulting edges of length one.
In every outer root triangle add a vertex K_i adjacent to r,a_i,a_(i+1).
Give masses three to K_1, four to K_2 and three to K_4, zero elsewhere.
The graph has 19 vertices, 42 edges and 25 faces; total mass is ten.
All K are singleton attachments with width-three torsos and the core
is isometric. Every branch has two parents, and all incident arc totals
are two, so the new theorem applies at any branch.

Choose S0={r,a_0,c_0}. Its sector mass is zero; other DAD sectors have
masses four and three. The two paths

```
(c_0,a_1,a_2),    (a_0,r,a_3,c_1)
```

are ambient geodesics and leave largest component mass four, below
the bound five. This checks the absence of maximal-sector selection.
It does not assert failure of every possible fixed-first-path repair.

The same weighting is not explained by two familiar sufficient
mechanisms in [Diot--Gavoille](https://emilie-diot.eu/Article/DG10a).
Deleting its attachments and suppressing the three degree-two inner
vertices gives a core minor of minimum degree four; consequently the
original graph has treewidth at least four. Every facial boundary
leaves a component of mass at least six. For annular and inner faces,
r survives and connects all ten units of attachment mass. A cap face
deletes at most one positive attachment, of mass at most four; the
remaining attachment masses stay connected through r or the surviving
outer path. The separate audit checks every face explicitly.

Suppressing the three inner subdivision vertices gives a 3-connected
16-vertex graph, checked after all 137 deletions of at most two vertices.
Whitney uniqueness (as recalled in
[Georgakopoulos--Kim](https://arxiv.org/abs/2109.04085)) and correspondence
of embeddings under subdivision extend the facial check to every
embedding. This is an explicit external input only to the scope
comparison. The control is a positive example with vertex masses,
not a counterexample to Problem 31. It does not establish separation
from every known sufficient class or historical novelty.

## Boundaries of this method

The first metric inequality has a concrete path-level threshold.
On `(AD)^3` at common scale four, make T_0 have total seven and the
other anchor incident arc total eight. The proposed complementary
route `(a_0,r,a_3,c_1)` has length twelve, while the route through T_0
has length eleven. At T_0 total eight it is geodesic. This certifies
the threshold for that displayed route, not necessity for half balance.

The incidence condition also has content. On word `ADDAD`, with all
inner totals eight and scale four, the branch c_2 is adjacent both
to a_3 and a_4=a_(k-1). The route `(a_0,r,a_3,c_2)` has length twelve,
but `(a_0,a_4,c_2)` has length eight. The prescribed repair thus fails
shortestness when (2) is dropped. This is not a separator counterexample.

The theorem does not cover arbitrary short anchor arcs, arbitrary
wheel/cross prices, inner attachments, nonisometric cores or mass
introduced by subdividing outer/cross edges. It is a variant of the
single-parent anchor result, not a generalization of all its hypotheses.
The earlier selected-sector unit theorem remains broader in incidence
and does not require (1),(2); the present bound permits every eligible
anchor without its maximum-sector rule. Comparisons concern the stated
representations and hypotheses, not all possible representations of G.

## Reproduction and trust boundary

From the repository root, Python 3.11+ and its standard library,
assertions enabled (recorded run: 3.11.2):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_two_parent_annuli/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_two_parent_annuli/audit.py
```

The first output must match [expected.json](expected.json). Its exact
Fraction calculations use seven attachment fixtures, all eligible DAD
anchors, and 100 additional seeded core words (`2026092919`). Profiles
include zero, uniform and singleton masses, heavy/equality attachments,
random integer masses, entire inner arcs and long fans. It checks all
displayed paths against full ambient distances, actual full components,
disjoint mass supports, core isometry, spherical rotations and local
decompositions. Totals: 143 systems, 4,658 component cuts and 2,039
quantitative cases. There are 739 heavy-attachment cases and 1,300 light
half cases; the latter include 349 with a nonmaximum anchor sector and
12 with a heavy long fan. Counts reuse coordinate systems and are not
distinct graphs or an exhaustive mass census. The main checker imports
earlier graph, sweep-choice and heavy-attachment helpers.

The separate [audit.py](audit.py) imports no research routines. It
directly builds labelled A/C/D words of lengths five through eight
satisfying the stated base run bounds, k>=5 and containing cyclic DAD,
with one integer metric and singleton sector attachments per word.
It uses Floyd--Warshall and chooses each new prefix/suffix cut by
testing actual geodesicity, rather than by the production threshold
formula. It audits the new first-D pair and repacked A/D pairs, the
distance assumptions, the threshold/incidence failure controls, and
the literal 19-vertex scope example. Ordinary C/D repairs are covered
by the written proof and main checker. Expected line:

```text
A_repacked=991 D_anchor=1982 D_repacked=991 anchors=1982 arc_threshold_controls=2 carrier_paths=12772 complement_distances=4249 incidence_failure_controls=1 models=2079 models_without_anchor=466 new_component_pairs=6937 no_single_parent_control=1 nonmaximum_anchor_control=1 scope_connectivity_checks=137 scope_core_minimum_degree=4 scope_edges=42 scope_faces=25 scope_min_facial_residual=6 scope_pair_residual=4 scope_total_mass=10 scope_vertices=19 PASS
```

The universal assertion rests on the written distance, component,
threshold and centroid proofs. Finite checks do not establish all
real metrics or masses by enumeration. Separate implementation by
the same researcher is not independent peer review or formalization.
No solver or external dataset is used. Whitney uniqueness is needed
only for the explicitly identified all-embedding scope comparison.
