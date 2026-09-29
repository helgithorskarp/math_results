# Prescribed anchors throughout the inner-metric region of necklace annuli

For a necklace with at least four inner branches, the two-geodesic
separator bound holds for **every branch and either of its outer parents**,
throughout the region where every inner arc has total length at least the
common wheel/cross-edge length. The two arcs at the chosen anchor no
longer need twice that length. Individual inner-edge lengths and vertex
masses may be arbitrary positive and nonnegative reals, respectively.

The proof chooses the appropriate outer endpoint for each A-step carrier
and adjusts two neighboring D-step exchanges when an incident arc is short.
The paired D-step repairs have disjoint potentially heavy supports. No
maximum-mass anchor sector is selected.

This extends the necklace part of the
[two-parent mixed-annulus theorem](../planar_two_geodesic_two_parent_annuli/README.md).
It is a conditional structural result for
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf),
not an unrestricted resolution. The unit-edge all-mass existence cases
already covered by the
[selected-sector mixed theorem](../planar_two_geodesic_subdivided_mixed_annuli/README.md)
are not new cases. The new assertions concern the full stated inner-metric
region and the prescribed-anchor quantifier. Independent review is pending.

## Hypotheses and theorem

Let `t>=4`. The core H has root r, outer cycle

```
a_0,b_0,a_1,b_1,...,a_(t-1),b_(t-1),a_0,
```

all root-to-outer spokes, and branches `c_0,...,c_(t-1)`. Each c_j has
precisely a_j,b_j as outer neighbors. Join c_j to c_(j+1) by an inner
path T_j, with internally disjoint degree-two interiors. Indices are
cyclic. This is incidence word `(AD)^t` in the earlier notation.

Every root, outer-cycle and cross edge has the same length `lambda>0`.
Every individual inner edge has positive length; write `ell_j` for the
total of T_j and assume only

```
ell_j >= lambda for all j.                              (1)
```

A finite connected simple positive-edge graph G contains H induced and
isometrically. Each component K of `G-V(H)`, including zero-mass ones,
has boundary contained in `{r}`, `{r,u}` or `{r,u,v}` for consecutive
outer vertices u,v. There are no inner attachments. The core is planar
by construction; full-G planarity is not needed for the conditional claim.

Choose any branch and either parent. Rotation and reflection let us write
the chosen triple as `S0={r,a_0,c_0}`. For an arbitrary nonnegative real
vertex weighting of total W, define

```
Y(K) = N(K) intersect the outer vertices;
D0 = sum w(K) for Y(K) empty or {a_0};
B = max_K w(K), defaulting to zero;
M = W-w(S0)-D0,    h=max{M/2,B}.
```

**Quantitative theorem.** At most two shortest paths in the original G
have a union containing S0 and leave every remaining component of mass
at most h. There is no mass restriction on the anchor sector, and no
treewidth assumption for this assertion. The three vertices are preserved
collectively; `P=(r,a_0,c_0)` need not remain one entire selected path.

**All-mass corollary.** If every induced torso `G[K union N(K)]` has
treewidth at most three, every nonnegative weighting admits a separator
equal to the union of at most two original-G geodesics, with each remaining
component of mass at most W/2. If an individual K is heavy, this corollary
may change the anchor. Otherwise the quantitative theorem preserves it.

The theorem includes arbitrary positive subdivisions of the inner arcs,
subject to (1). It makes no corresponding assertion for subdivisions of
outer/cross edges carrying new mass, or for inner totals below lambda.

## Distance identities and changed carriers

Let W0 be the outer wheel. It is isometric: an inner excursion between
outer vertices uses two cross edges and costs at least `2*lambda`, no
less than their wheel distance. Each branch has root distance `2*lambda`.
Put `s=ell_0` and `z=ell_(t-1)`. The anchor distances are

```
d(c_0,a_0)=d(c_0,b_0)=lambda;
d(c_0,a_1)=d(c_0,b_(t-1))=2*lambda;
d(c_0,b_1)=min(3*lambda,lambda+s);
d(c_0,a_(t-1))=min(3*lambda,lambda+z);
d(c_0,u)=3*lambda for all other outer u.                 (2)
```

To prove (2), consider the first cross exit of an inner route from c_0.
With no whole inner arc it exits at a_0 or b_0. With one arc it can exit
only at a_1,b_1 or a_(t-1),b_(t-1); its cost is the arc total plus lambda.
At least two arcs cost at least `3*lambda` including the exit. The wheel
routes attain all the remaining values. Core isometry transfers them to G.

Use these explicit anchor-to-outer geodesics E(u):

| u | E(u) |
|---|---|
| a_0 | `(c_0,a_0)` |
| b_0 | `(c_0,b_0)` |
| a_1 | `(c_0,b_0,a_1)` |
| b_(t-1) | `(c_0,a_0,b_(t-1))` |
| b_1, if s<2lambda | T_0 from c_0 to c_1, followed by b_1 |
| a_(t-1), if z<2lambda | T_(t-1) backwards from c_0 to c_(t-1), followed by a_(t-1) |
| every other case | `(c_0,a_0,r,u)` |

The two short-arc carriers in the table omit both a_0 and r. At equality
`s=2lambda` or `z=2lambda`, use the root carrier, which is still shortest.
Also

```
d(a_0,c_1)=min(3*lambda,lambda+s);
d(a_0,c_(t-1))=2*lambda;
d(b_0,c_(t-1))=min(3*lambda,lambda+z);
d(a_0,c_j)=3*lambda for 2<=j<=t-2.                      (3)
```

For the last equality, no two-edge route exists: the two outer neighbors
of a_0 have only c_0,c_(t-1) as inner neighbors. A route through c_0 needs
at least two inner arcs to reach such a c_j, and entry through another
branch already costs at least `2*lambda` before a further arc of length
at least lambda. The root route attains `3*lambda`. The other formulas
follow from the same first-entry comparison. This is where `t>=4`
keeps the two exceptional neighboring transitions distinct.

At a diagonal step `(b_j,c_j)` to `(a_(j+1),c_(j+1))`, the own cross
distances are lambda and the opposite cross distances are `2*lambda`.
Indeed, there is no opposite cross edge, and (1) prevents a cheaper inner
shortcut. The outer edge gives a two-edge route.

For any inner arc `T=(v_0=c,...,v_n=d)` of total ell, write
`0=x_0<...<x_n=ell` for vertex coordinates. Its only entry points are c,d.
A specified shortest path from u to c extends geodesically to v_i when

```
d(u,c)+x_i <= d(u,d)+ell-x_i.                            (4)
```

Reverse the inequality for extension from d. This test allows ties and
arbitrary nonuniform coordinates. All paths below use (2)--(4).

## Sweep and component bounds

Put `o_(2j)=a_j`, `o_(2j+1)=b_j`. After deleting S0, each K counted in
D0 detaches individually, with mass at most B. Partition the represented
vertices of total mass M into

```
alpha_i: o_i and all K with Y(K)={o_i}, for i!=0;
gamma_j: {c_j}, for j!=0;
kappa_i: all K with Y(K)={o_i,o_(i+1)};
tau_j: the interior of T_j.
```

The zero-index alpha and gamma groups are empty; indices at the end of
the unrolled sweep wrap to these empty groups. At state (i,j), let L be
the union of alpha_h,kappa_h for h<i and gamma_h,tau_h for h<j. Let R
be the represented complement minus alpha_i,gamma_j. Deleting P and
the root spoke `(r,o_i,c_j)` leaves each component meeting H inside L or
R. Each other component is one whole K.

Here is the component justification used throughout. Removing the listed
outer vertices cuts the outer cycle into intervals. Removing the listed
branches or inner prefixes/suffixes cuts the inner cycle into matching
intervals. Each cross edge joins c_j to its two consecutive parents, so
it stays on one side of these cuts. A K cannot bridge the intervals:
its active sites are at most two consecutive outer vertices. If all of
its boundary was deleted it detaches as one whole component. No displayed
path enters K. Extra core deletions only split remaining components.

L increases and R decreases from `(0,M)` to `(M,0)`, with `L+R<=M<=2h`.
If no spoke pair works, there is a first transition with new L>h;
its old R>h. The old L and new R are both light. Below, L and R mean
these old and new light sides respectively.

For an A-step `(a_j,c_j)` to `(b_j,c_j)`, deleting S0,a_j,b_j,c_j puts
every core component in L or R. For a D-step across T_j, deleting S0,
both outer endpoints and the suffix `v_q,...,v_n` puts them in

```
H_left = L union gamma_j union {v_1,...,v_(q-1)},    R.   (5)
```

Deleting the corresponding prefix `v_0,...,v_p` instead gives

```
L,    H_right = R union gamma_(j+1) union
                      {v_(p+1),...,v_(n-1)}.            (6)
```

These follow directly from the interval argument, including the seam at
a_0,c_0. They are upper bounds; an endpoint or other listed vertex may
also have been deleted by the other path. If `q<=p+1`, the supports
H_left,H_right are disjoint subsets of M, so they cannot both exceed h.
Detached K are always controlled individually by B.

## A-steps by choosing the other endpoint

Every A-step `(a_j,c_j)` to `(b_j,c_j)` has one explicit repair:

| Case | Two paths |
|---|---|
| j=0 | `(r,a_0)` and `(c_0,b_0)` |
| j=1 and s<2lambda | T_0 from c_0 to c_1 followed by b_1, and `(a_0,r,a_1)` |
| j=t-1 | `(c_0,a_0,b_(t-1))` and `(r,a_(t-1),c_(t-1))` |
| all other j | `(c_0,a_0,r,b_j)` and `(a_j,c_j)` |

The second row uses the short carrier **to b_1**, which contains c_1.
Its length is lambda+s, as in (2). The complementary root route from
a_0 to a_1 has length `2*lambda`, equal to their wheel distance.
The third row uses the unaffected carrier to b_(t-1), of length
`2*lambda`, and a root-to-branch geodesic of the same length; it works
regardless of z. In the last row the carrier has length `3*lambda`
and is shortest by (2): the sole short exception b_1 was handled
separately, while b_0 and b_(t-1) are in other rows.

Each pair contains S0 and deletes both a_j,b_j and c_j. Thus the
A-step component bounds are simply the light L,R and individual K.
A short carrier may additionally delete the whole T_0, which only
helps. No alternative mass comparison is needed at any A-step.

## D-steps and overlapping geodesic ranges

First consider the initial D-step `(b_0,c_0)` to `(a_1,c_1)`. Across T_0
of length s choose

```
p last with 2*x_p <= s+min(2*lambda,s);
q first with 2*x_q >= s+lambda.                          (7)
```

The two pairs are

```
(a_0,c_0,v_1,...,v_p),    (r,b_0);
P,    (b_0,a_1,c_1,v_(n-1),...,v_q).
```

The first start has distances lambda and `min(3lambda,lambda+s)`
to the arc endpoints, giving its threshold in (7). The second start
b_0 has endpoint distances lambda and `2lambda`, giving the other
threshold. Both are in `[0,2s]`, with the first at least the second
because `s>=lambda`. Hence `q<=p+1`. When s<=2lambda, the first pair
uses the whole inner arc.

The old L is only kappa_0, which detaches individually after deleting
r,a_0,b_0. The first pair has only one possibly heavy core support,
`H1=R_old minus {v_1,...,v_p}`. The second pair isolates the early arc
segment `H2={v_1,...,v_(q-1)}` and puts all other core components in
the new light R. Both branch endpoints are deleted in that pair.
H1,H2 are disjoint subsets of M by (7), so one pair works.

Now take a D-step j>=1, from `(b_j,c_j)` to `(a_(j+1),c_(j+1))`,
across T_j of length ell. The forward pair uses E(b_j) and a suffix
from c_(j+1), ending at the first q with `2*x_q>=theta`. The reflected
pair uses E(a_(j+1)) and a prefix from c_j, ending at the last p with
`2*x_p<=phi`. Their starting portions and thresholds are:

| Forward case | Path to c_(j+1), then backwards on T_j | theta |
|---|---|---|
| j=1 and s<2lambda | `(a_0,r,a_2,c_2)` | `ell+2lambda-s` |
| otherwise, E(b_j) contains r | `(a_(j+1),c_(j+1))` | `ell-lambda` |
| otherwise | `(r,a_(j+1),c_(j+1))` | `ell` |

| Reflected case | Path to c_j, then forwards on T_j | phi |
|---|---|---|
| j=t-2 and z<2lambda | `(a_0,r,b_(t-2),c_(t-2))` | `ell-lambda` |
| otherwise, E(a_(j+1)) contains r | `(b_j,c_j)` | `ell+lambda` |
| otherwise | `(r,b_j,c_j)` | `ell` |

For the special forward row, the start a_0 has distances `lambda+s`
and `3lambda` to c_1,c_2, respectively. Formula (4) gives exactly
`ell+2lambda-s`. For the special reflected row, a_0 has distances
`3lambda,2lambda` to c_(t-2),c_(t-1), giving `ell-lambda`. These
start-to-branch paths are shortest by (3). They supply a_0 and r,
which the respective short-arc carrier omitted. The ordinary rows
follow from equal root distances or the own/opposite cross distances.

The two special rows cannot occur at the same transition since t>=4.
In the first special case the other threshold is `ell+lambda`, at
least `ell+2lambda-s` because s>=lambda. In the second special case
the forward threshold is also `ell-lambda`. All ordinary forward
thresholds are at most ell and all ordinary reflected ones at least
ell. Therefore always

```
0 <= theta <= phi <= 2*ell.                             (8)
```

The endpoint bounds use ell>=lambda; the special forward upper bound
also uses s>=lambda. Thus q,p exist and `q<=p+1` even with gaps between
successive vertex coordinates or a threshold exactly on a vertex.

Each pair deletes S0 and both outer endpoints. Its core components have
the bounds (5) or (6); any additional deletion of c_1,T_0 or
c_(t-1),T_(t-1) by a short carrier only helps. By (8), H_left,H_right
are disjoint subsets of M. They cannot both be heavier than h, so one
pair works. The closing D-step into c_0 is among the ordinary cases,
with both thresholds ell and the empty seam branch group. This proves
every D-step, completes the sweep and proves the quantitative theorem.

## Heavy attachments and the all-mass corollary

If each K has mass at most W/2, then h<=W/2 already. Otherwise a heavy
K has a width-three torso decomposition. Its boundary is a clique of
at most three vertices and lies in a bag. Attach `V(G)-K` as an outside
leaf bag there, assigning all outside mass to that leaf and K's mass
to local bags. A weighted centroid cannot be the outside leaf: it sees
the heavy K in its only branch. Its local bag contains at most four
vertices and half-separates G. Pair its vertices with at most two
ambient geodesics; deleting the union only decreases component masses.
This is the existing
[reviewed heavy-attachment reduction](../planar_two_geodesic_prescribed_attachment_review1/REVIEW.md).
The anchor need not be preserved in this heavy-K replacement.

## Sector and inner-arc controls

Use t=4, common scale four, and add a singleton K_i adjacent to
r,o_i,o_(i+1) in each of the eight root triangles. The following
profiles all have total mass ten and bound h=5; all unlisted masses
are zero. All inner arc totals are four. Use the corresponding first
or last A-step pair from the table above.

| Profile | Inner arc division and masses | Largest residual |
|---|---|---|
| First sector | All inner arcs single edges; K_1=3, K_2=4, K_4=3 | `4` |
| First inner | T_0 edge lengths `(3,1)`; its interior vertex=4, K_2=3, K_4=3 | `3` |
| Last sector | All inner arcs single edges; K_6=4, K_7=3, K_4=3 | `4` |
| Last inner | T_3 edge lengths `(1,3)`; its interior vertex=4, K_6=3, K_4=3 | `4` |

These are exact full-component checks. The first short carrier deletes
the entire incident arc; the last repair can leave its interior as an
isolated light component. Both kinds of mass are allowed by the theorem.

The first sector profile, after dividing every edge length by four,
is a **21-vertex unit-edge graph** with 52 edges and 33 faces. Its
anchor sector has mass zero while another anchor sector has mass four.
The successful pair is `(c_0,c_1,b_1)` and `(a_0,r,a_1)`. The previous
long-arc complementary route `(a_0,r,b_1,c_1)` has length three but
endpoint distance two, so it cannot supply this repair. All branches
have two parents and all inner totals are one; none of the preceding
single-parent or long-incident-arc anchor criteria applies to this
representation.

The same weighting lies outside two standard sufficient mechanisms in
[Diot--Gavoille](https://emilie-diot.eu/Article/DG10a). Removing the K_i
leaves a core of minimum degree four, so the graph has treewidth at
least four. Every facial boundary leaves mass at least six. Inner and
annular faces retain r joining all ten units; a cap face deletes at
most one positive K_i, of mass at most four, and the others stay connected
through r or the surviving outer path. The separate audit checks all
33 faces and all 232 vertex deletions of size at most two, proving that
the graph is 3-connected. Classical Whitney uniqueness, as recalled in
[Georgakopoulos--Kim](https://arxiv.org/abs/2109.04085), extends this facial
conclusion to every embedding. This external input is used only for
the scope comparison. No separation from every known sufficient class
or historical novelty is claimed.

## Scope, small-case boundary and priority

The result removes both long-incident-arc restrictions from the previous
necklace theorem when t>=4. It does not generalize that theorem's other
mixed incidence words. The arbitrary-metric t=3 case is outside this
proof: the two neighboring exceptional D-steps coincide, and
`d(a_0,c_2)=2lambda` rather than the required `3lambda`. In the unit
`(AD)^3` core, the displayed route `(a_0,r,a_2,c_2)` is therefore not
shortest. This is a limit of the present repair, not a counterexample to
the prescribed-triple assertion or to half balance. Its long-arc case
is covered by the previous theorem; its unit all-mass existence was
also already known within this campaign.

The [official workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html)
announces a Codsi separator-conjecture disproof. The precise statement
and witness remain unmatched in our bounded primary-source audit,
refreshed 29 September 2026. No author was contacted. Neither continued
openness, unrestricted resolution nor historical priority is inferred
from the posted problem list or from a targeted negative search.

## Reproduction and trust boundary

From the repository root, Python 3.11+ and its standard library,
assertions enabled (recorded run: 3.11.2):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_metric_necklaces/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_metric_necklaces/audit.py
```

The main output must match [expected.json](expected.json). It uses exact
Fraction arithmetic, six planar attachment fixtures of sizes t=4,4,5,6,7,8,
all 68 anchor orientations on those fixtures, and 100 further seeded core
metrics with two tested orientations each (`2026092920`). It verifies
all displayed paths against full ambient distances, component containments,
disjoint supports, core isometry, spherical rotations and local torso
decompositions. Mass profiles include zero, uniform, singleton, heavy and
equality attachments, random integer profiles and the targeted short-arc
cases. It imports earlier graph, mass-choice and heavy-attachment helpers.

Recorded totals: 268 systems, 8,788 actual component cuts and 17,498
quantitative mass checks; 7,204 heavy-attachment checks and 10,294 light-half
checks. The latter include 6,340 nonmaximum anchor sectors. The short-first and reflected-last
A repairs and both neighboring short-D branches are selected
in the mass tests. These counts reuse graphs and orientations; they are
not distinct-graph or exhaustive-mass counts.

The separate [audit.py](audit.py) imports no research routines. It builds
the graph directly with named vertices and uses integer Floyd--Warshall.
For t=4 through 8 it tests all 81 ordered choices of two incident arc
patterns, with remaining arcs assigned deterministically, in both
orientations. It selects each new D-step prefix/suffix by direct geodesicity,
independently of the production threshold formula, and checks the new
component supports. It also checks the four literal mass controls, the
21-vertex scope control and the t=3 method boundary. Expected output:

```text
A_anchor=810 A_first_long=180 A_first_short=630 A_last=810 A_ordinary=2430 D_anchor_prefix=810 D_anchor_suffix=810 D_short_backward=1260 D_short_forward=1260 carriers=9720 first_inner_control_residual=3 first_sector_control_residual=4 last_inner_control_residual=4 last_sector_control_residual=4 models=405 new_component_pairs=9000 old_complement_failure=1 oriented_systems=810 scope_connectivity_checks=232 scope_core_minimum_degree=4 scope_edges=52 scope_faces=33 scope_facial_minimum=6 scope_pair_residual=4 scope_total_mass=10 scope_vertices=21 three_branch_method_boundary=1 PASS
```

The arbitrary-order, real-metric and real-mass theorem rests on the written
distance, component, threshold and centroid arguments. The finite checks
do not prove its continuous quantifiers by enumeration. Ordinary D
steps are checked in the main implementation and written proof; the
separate implementation checks every A-step as well as the new D repairs. A separate
implementation by the same researcher is not independent peer review or
a proof-assistant formalization. No solver, external dataset or omitted
large certificate is required.
