# A repaired signed phase and exact torque cover close the two-thirds wedge

Author: **six-rupert-1**, role **researcher**, 2026-09-30. Author-checked
written intermediate proof with exact finite hypotheses; unformalized,
without asserted independent review or historical priority. **Global
Rupert property of the deltoidal hexecontahedron remains OPEN.**

Let K be the centered standard solid with the 62 original vertices in
[verify.py](verify.py), G its sixty proper body rotations and P_n the
orthogonal projection onto n-perp. Put s=sqrt(5) and

    M=((3s-5)/6,(s-1)/6,1), m=M/||M||,
    N8=((5-s)/10,(-5+3s)/10,1),
    N10=((3-s)/2,(7-3s)/2,1),
    W=(25/38-17s/114,7/114+5s/114,1),
    D_t=conv(M,M+t(W-M),M+t(N10-M)),
    J_n=2nn^T-I.

The exact weight W=(1-r)N8+r N10 has r=(17+4s)/57 in (0,1).
All D_t below use the raw unit-z chart; n=u/||u|| is the physical unit
receiver normal. The new receiver domain is the **entire closed D_(2/3)**
and all its actual proper-body and antipodal images.

**Claim.** For every receiver n in that domain, every original Q in
SO(3), every planar translation t and every scale lambda>=1,

    lambda P_n(QK)+t subseteq P_nK
       iff lambda=1, t=0, Q in G union J_nG.                 (1)

These are 120 proper equality orientations in two disjoint **left**
cosets. In particular no strict passage uses these receivers. All source
normals, full spatial angles, rolls, edges and corners are quantified.
This is an intermediate receiving-domain theorem, not a global
non-Rupert proof or a construction of a strict passage.

The direct receiving-domain parent is the
[selected ten-contact half-wedge proof](selected_torque_wedge_proof.md),
by six-rupert-1, researcher, source
**062fb4ce6d5d471c92fc72a5821806ae16d5e120**, graph
**bafkreidqodlngnuxspd5qsvsduvjplg4xit3ffcmgcvylkc65zsip2gmym**,
actually committed at 7771. Its checker and compact fixture are hash-pinned.
We replay its complete prerequisite block, which recursively pins and checks
the original-body, area-fan and signed-frame chain. We use those proved
geometric identities; every new source, signed-roll and torque inequality
below is checked afresh. No narrower-domain numerical gate is transferred.
The older [area-sublevel proof](area_sublevel_wedge_proof.md) supplies the
fixed source-cover checker and continuous convex-cone bridge. The new
[two_thirds_wedge_certificate.py](two_thirds_wedge_certificate.py) reconstructs
fixed source and facet witnesses, rather than trusting search success.

## Exact source localization and unrestricted-angle reduction

The parent's complete twelve-cell fan has physical projection area
A(u/||u||)=C.u/||u|| in each closed cell, including all boundary ties.
For D_(2/3) the complete corner/edge/interior algorithm gives

    max A(n)^2=(1208294350+539801050s)/11021769,
    A(n)<T=14803427/1000000,
    A(n)-a0<86753/1000000,
    ||n-m||<d=70567/1000000,                                 (2)

where a0^2=(3503950+1491850s)/31581 is the global minimum area squared.
The active maximum is corner 2; all positive-cone edge and interior
critical points are checked before this conclusion is drawn.

A new global conditional source lemma is

    A(k)<=T  implies  dist(k,Gm)<a=11/100                   (3)

for every unit original source k. Its fixed witnesses are in
[expected_two_thirds_wedge.json](expected_two_thirds_wedge.json).
Sixteen closed fan triangles cover all twelve source cells. The complete
prefix-free midpoint subdivision has **181 closed leaves**, **236 nodes**,
depth at most four: **72 cap leaves and 109 above-area leaves**. Each leaf
uses three positive-branch squared corner tests, 543 strict inequalities.
With c=1-a^2/2, a cap corner satisfies

    M.u>0, (M.u)^2>c^2||M||^2||u||^2;

an above-area corner satisfies

    C.u>0, (C.u)^2>T^2||u||^2.

For every nonnegative corner combination, linearity and the norm
triangle inequality extend the chosen strict bound to the entire closed
leaf. Hence a leaf either lies in the a-cap or has area strictly above T.
The complete leaf record SHA256 is

    a64369d8ef794dd79503aadc32919b4558bb6e93fdb96264114471afb363ee7c.

The checker reconstructs fixed leaf paths and validates the full closed
trees, independently of the exploratory pruning decisions. The parent's
actual determinant-minus-one body reflection in (-phi,-phi^2,1) fixes m.
Composing any improper chamber fold with that reflection supplies a
proper body gauge with the same source chord. Thus (3) has the directed
proper orbit Gm and does not permit an improper moving source.

Centrality K=-K removes translation and scale as necessary conditions:
from lambda S+t subseteq U also obtain lambda S-t subseteq U, then
lambda S subseteq U and S subseteq U. Therefore original containment
implies A(Q^T n)<=A(n)<T. Equation (3) derives an actual right body gauge
with source chord below a. Let R1:m->k and R2:m->n be the minimal proper
transports. Their axes are perpendicular to m. Since left multiplication
by J_n preserves the projected centrally symmetric source, the full
proper roll may be reduced modulo pi:

    Q'=J_n^epsilon Qh=R2 C_alpha R1^T,
    h in G, epsilon in {0,1}, -pi/2<=alpha<=pi/2.          (4)

No small angle or roll is an initial assumption.

The exact signed Rodrigues identities in the parent give, for each
actual reference probe (mu,H) and original or checked convex source
point p, the necessary inequality at x=tan(|alpha|/2):

    (gamma-H-E)+2 tau_sign x-(gamma+H+E)x^2<=0,
    gamma=mu.p,
    E=L_mu+eta[hp a+(R/2)(a^2+d^2)], R=23/10.            (5)

Here eta>=||mu||, hp>=|p.m|, tau_sign is an outward lower signed torque
and L_mu is the exact whole-receiver envelope from the original
vertices. Weighted linear-fractional corner envelopes and the signed
Rodrigues identity justify the whole closed receiver bounds; they are
not receiver sampling. The parent reconstructs all sixteen reference
facets, all 62 original source vertices and its twelve actual convex
zero-height source points. The new phase checks fresh envelopes and all
**18 consecutive closed signed remote intervals**, nine per sign, with
**36 strict endpoint inequalities**. Concavity in (5) excludes every
remote x in [1/10,1], with no omitted endpoint.

For probes 3 and 4 and V45, both new linear envelope costs are zero.
The common error, width and signed torque bound are

    E=204000996446406829/10000000000000000000,
    H=20/9, tau=26991/40000.

The upward near-zero quadratic

    (2H+E)x^2-2tau x+E>=0

is positive at zero and negative at 1/10. The first root is strictly
below 15959/1000000; the grid predecessor and proper small branch are
checked. Consequently the full surviving roll chord is below
15959/500000.

In (2), d exceeds the old 1/20 receiver guard. We do not invoke that
numerical guard outside its range. The transport and signed-envelope
identities above hold for these acute nonantipodal normal pairs; the
new checker instead tests a<=1/5 and d<=3/40, the actual positive
quaternion branch and all new interval inequalities. With

    X^2=(a+d)^2+(15959/500000)^2=33623200213/1000000000000,
    P=(1-a^2/4)(1-d^2/4)(1-(15959/500000)^2/4),

the exact tests give P>(99/100)^2 and 99/100-ad/4>0. The perpendicular-
axis quaternion identity of the parent bounds the principal full angle
by 2asin(X/2). The derivative test
(201/200)^2(1-X^2/4)>1 then yields

    theta<Theta=46071/250000.                           (6)

Thus the wider receiver range is checked through the actual algebra,
not assumed from an earlier numerical theorem.

## A smaller normalized hull is sufficient

Use the parent's twelve original contacts, numbered 0 through 11, but
retain only **1,2,3,4,5,6,7,8,9,10**. Explicitly the retained triples
(edge start, edge end, source vertex) are

    (59,55,55),(55,58,55),(55,58,58),(58,45,58),
    (58,45,45),(45,34,45),(45,34,34),(34,36,34),
    (34,36,36),(36,20,36).

For each contact define mu(u)=(V_end-V_start) cross u. All three receiver
corners and all 62 original vertices give **1860** exact weak support
tests mu.(V_source-V)>=0. Linearity extends these to the whole closed
triangle. The fixed positive denominators, in the displayed order, are

    113523/125000,246707/500000,50619/100000,47651/40000,
    580603/500000,580603/500000,47651/40000,50619/100000,
    246707/500000,113523/125000.

For each corner they strictly exceed ||V_source||||mu||/2. Norm convexity
extends the same bound throughout D_(2/3). The normalized torque points

    S_j(u)=(V_source cross mu(u))/B_j

are affine in the raw unit-z receiver u; no physical-normal denominator
has been omitted. The four retained original contact ids 1,3,8,10 have
40 strictly positive cubic cofactor coefficients and three identically
zero quartic vector balances. Their rank is three. Hence zero is in
the interior of the selected torque hull everywhere on the closed
receiver triangle.

There are 120 possible facet triples. For each, the checker considers
all seven nonempty relative simplex faces. The base **840** cases have
716 strict opposite-gap cases, 118 nonnegative plane-distance cases,
and six unresolved cases in just two original contact triples:
(3,4,6) and (5,7,8), each on relative faces (0,1,2), (0,2), (1,2).
These unresolved cases are not proof. They are replaced by the following
complete closed midpoint covers; paths use the standard four children.

* Original triple (3,4,6), selected indices (2,3,5):
  `0, 1, 20, 210, 211, 212, 213, 220, 221, 222, 223, 230, 231, 232, 233, 3`.
  All 21 tree nodes and 16 closed leaves are checked, with maximum depth
  three. The terminal 112 strata are 88 opposite and 24 distance.
* Original triple (5,7,8), selected indices (4,6,7):
  `0, 1, 20, 21, 220, 221, 222, 223, 23, 3`.
  All 13 tree nodes and 10 closed leaves are checked, maximum depth three.
  The terminal 70 strata are 56 opposite and 14 distance.

Each prefix-free cover has total normalized area one and all four
children of every internal node. All seven relative faces are checked
on every closed leaf; no endpoint, corner or tie wall is omitted.
Replacing both base triples gives **1008 terminal cases**, 854 opposite
and 154 distance, with no unresolved or degenerate terminal case.

For a candidate triple let N be its actual cross-product normal and H
its signed height. A distance case proves, by nonnegative homogeneous
coefficients on its relative face,

    H^2-rho^2||N||^2(lambda0+lambda1+lambda2)^2>=0,
    rho=Theta+1/100=48571/250000.                        (7)

A strict opposite-gap pair excludes the candidate supporting plane.
A zero normal is handled by degeneracy; no such terminal case is needed
here. A genuine facet contains a noncollinear triple of selected vertices.
Positive origin-interiority and the bounds on every possible supporting
facet therefore imply a centered closed rho-ball in the selected hull.

There are **6682 joint vector/scalar formula audits**: 6240 at the base
corners and an interior barycentric point, plus 442 in the 34 refinement
nodes. The count is ten actual gaps plus the joint vector normal, scalar
height and scalar distance tests per sample. These formula audits check
implementation identities; the homogeneous coefficient signs and full
closed covers prove the continuous assertion. Complete base coefficient
and case hashes are

    218c8e45d6a4d333635732ac93fca687780dbbb4213dd678a9e4f82f8bd22221,
    1db8a765e3d0d147a4f295290438fc6f9647cb9622d3ec0629d541461f92a686.

The refinement coefficient hash is

    2c190e99b14667d4fb2a3189a6914836f070de2b930f2f25a75917215e306800.

Deleting contacts makes a smaller convex hull. A ball certified in
this smaller hull also lies in the original full hull. **No redundancy
of either deleted torque point is asserted or required.** This is the
useful certificate mechanism: irrelevant potential triples can make
coefficient covers difficult, while a selected subhull may already
supply the entire support bound needed for the proof.

For a nonzero proper Q' of axis z and angle theta, the centered ball
supplies a retained contact with z.S_j>=rho. The proper rotation Taylor
remainder has norm at most ||V_source|| theta^2/2. Dividing its signed
support displacement by B_j bounds the remainder by theta^2, giving

    theta rho-theta^2>=theta(rho-Theta)>0.

This contradicts the necessary receiving support inequality. Thus Q'=I.
Undoing (4) gives exactly the two left cosets in (1). Equal-shadow area
forces lambda=1, and boundedness forces t=0. The parent gives squared
Frobenius separation (106-36s)/29 between J_m and G; the checker verifies
that it exceeds 8d^2. Since ||J_n-J_m||_F^2<=8||n-m||^2, J_n is not a
body symmetry. The two cosets are disjoint, completing (1).

## Exact enlargement, reproduction and remaining frontier

D_(2/3) contains the entire D_(1/2), with unit-z chart area ratio
**16/9**. This is not a spherical area ratio. The new strict interior
witness has barycentric weights (1/10,1/15,5/6). For all sixty projective
body images, the checker verifies mixed Cramer signs outside each of
six earlier triangular cones: the two D4 triangles, whole cell7, old D9
triangle, D_(2/5) and D_(1/2). These are **360 exact cone tests**. Thirty
squared axis comparisons put it at chord greater than 1/50 from every
signed minimum center, outside the old closed 1/64 caps. Thus the actual
retained receiving union strictly grows. The older domains remain
valid separately.

From the repository root, Python 3.11+ standard library only, run
sequentially with numerical threads one:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B geometry/rupert_deltoidal_symmetry/two_thirds_wedge_certificate.py --prerequisites
python3 -B geometry/rupert_deltoidal_symmetry/two_thirds_wedge_certificate.py --hull
```

Each command compares every field against
[expected_two_thirds_wedge.json](expected_two_thirds_wedge.json). Both final
commands matched every expected field under separate 55-second deadlines:
prerequisites 27.749931 seconds / 24996 KiB, hull 19.573301 seconds /
24684 KiB. The compact fixture SHA256 is
`2697a7a5cca11d0dc137f6135439ecc95e313b7791567ce67883514c7d36f0c6`.
Sixteen new malformed controls must reject, including all four obsolete
signed witnesses. Python -O is refused before computation. Every private
source-cover field and full leaf-record hash, every new signed phase
field and endpoint margin, every selected-hull mathematical field and
both full fixed refinement records match production. These are author
checks, not independent review or proof-assistant formalization.

The prerequisite command hash-pins and replays the direct half-wedge
parent's complete prerequisites, including the older signed Rodrigues
and ancestor checks. It then checks the new source/phase, geometry,
proper folds, coset separation and malformed controls. It does not rerun
the parent half-wedge torque hull, the older 2/5 hull or the six old
receiver-piece hull jobs. The hull command checks every new selected
facet and all supplied fixed closed refinement paths. Exact original
body coordinates, Python Fraction and Q(sqrt(5)) semantics, the published
prerequisite chain, and the written continuous frame, convex-cone,
roll, facet and rotation bridges are the trust boundary. No floating
search, incomplete cover, solver output or resource failure proves a
continuous assertion here.

The remote-roll policy initially had four failing endpoint tests on this
larger domain. Each is repaired by an existing actual source witness:

| Roll sign and closed x interval | Old probe, point | New probe, point |
| --- | --- | --- |
| -1, [181/640,13/40] | 7,65 | 4,72 |
| -1, [167/320,343/640] | 7,67 | 5,4 |
| +1, [181/640,13/40] | 0,62 | 3,66 |
| +1, [167/320,343/640] | 0,73 | 2,57 |

Points 4 and 57 are original vertices; points 66 and 72 are among the
parent's twelve exactly checked convex source points. All source-height,
signed torque and whole-receiver envelopes for the replacements are
regenerated, including both endpoints and concavity. No new interval
is inserted or old interval omitted. Each obsolete witness is rejected
under the fresh a,d bounds by a separate exact negative control.
The new torque cover closes the former D_(2/3) gap. The complement of the
retained receiving union remains the nonlocal frontier; a future wider
domain needs new area/source, roll and torque bounds rather than an
assumption that these numerical guards continue to hold.

Complementary **six-rupert-2, researcher**'s
[J77 north-triangle proof](../../convex_geometry/rupert_j77_directional_north_triangle/PROOF.md),
source a2c00c148381a36cb840571ca5b82d98e274fc35, graph7735, develops a wider source
range with fresh signed widths and additional original quarter-turn
witnesses. Its asymmetric translation-balanced stresses are not the
centrality premise used here. **six-rupert-3, researcher**'s
[RID global-gap proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/GLOBAL_SLACK_PROOF.md),
source d68a00c27754ac1517aba99197334e5e19fabb8b, graph 7703, proves only a
necessary RID receiving-height cutoff using a common original-vertex
circumsphere and an eight-to-four injection. Those hypotheses have not
been established for this deltoidal solid, so no RID constant transfers.
The prepublication refresh also read the complete
[expanded RID global-gap proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/EXPANDED_GLOBAL_SLACK_PROOF.md),
by six-rupert-3, researcher, source
6afb6b9e4585a35561752b3ef34eccabaa0d7e3e, graph
bafkreihbc5jiplrfxcfepw4sf7xexzr6eob4ugaw36bpmukbhf4vkzakjm at7755.
It strengthens that body's global necessary height gap to1/450 using
an enlarged ten-point torque triangle, the independent nonwinning
review and fresh eight-into-four error gates. Its source-circle and
spectrum hypotheses still do not transfer to the deltoidal body.
The [independent RID beta-cap review](../../rhombicosidodecahedron_beta_cap_review2/REVIEW.md),
by six-reviewer-2, reviewer, source 943fd6675ef2fce4f338ded9756ebb16b0d5ca9a,
strengthens different RID caps. It does not review this claim or the RID
global gap. Reviewer selection remains independent.

The new [independent global RID review](../../rhombicosidodecahedron_global_slack_review2/REVIEW.md),
by six-reviewer-2, reviewer, source
e9b77dc0a403bd7093e03bb271db39a7f33e6401, confirms the RID 1/1200 and
1/450 gaps and proves a refined 1/445 gap. Its different exact field and
all-permutation order-cone audit are useful methodological context.
Its common-radius, threshold-circle and height-spectrum premises still
do not transfer. It supplies no review verdict on this deltoidal claim.

The newly published [J77 projection-area proof](../../convex_geometry/rupert_j77_projection_area/PROOF.md),
by six-rupert-2, researcher, source
cd0088c8aa1e308657b17d759bc5600c7b8b2b34, develops a finite polar-vertex
area budget followed by tangent-zonotope coercivity. It gives a global
source-normal bound without assuming source nearness or centrality.
That geometric mechanism suggests checking the complete area-zonotope
facet gap and tangent disk around M for the next deltoidal source bound.
Its J77 minimum axes and constants are not imported; no such sharper
deltoidal polar bound is asserted here. The full new proof was read at
the prepublication source refresh; no corresponding new committed J77
lemma appeared in the bounded lemma query at index 7797.

Current primary status was checked in
[Gosain--Grimmer Table 3](https://arxiv.org/html/2509.08190), which retains
the deltoidal and pentagonal hexecontahedra as unresolved Catalan cases.
[2604.26531](https://arxiv.org/html/2604.26531) retains the standard RID
conjecture; [2508.18475](https://arxiv.org/abs/2508.18475) proves a different
non-Rupert convex body. No primary resolution of our named solid was
located in the bounded refresh. The qualitative uniform local-gap
phase at graph 7322 remains closed. Neither it nor this larger explicit
receiving domain resolves global Rupertness.
