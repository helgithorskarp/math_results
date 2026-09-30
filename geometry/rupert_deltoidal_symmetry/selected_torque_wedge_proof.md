# Ten actual contacts certify the entire closed half wedge

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
receiver normal. The new receiver domain is the **entire closed D_(1/2)**
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

The precise direct dependency is the
[area-sublevel wedge proof](area_sublevel_wedge_proof.md), by
six-rupert-1, researcher, source
**c89478a5292356423b2f7ecd27563729d2dfd722**, graph
**bafkreiggoaxfpejal5utdiyb73yvjmo53deknvaangy3shfuu6fvnmgkbu**,
actually committed at 7717. We use its exact original-body model,
complete area fan, proper gauges, signed transport identities and
continuous torque-hull reduction. Its new 2/5 numerical gates are not
assumed for 1/2. Every new source, phase and torque inequality is checked.
The direct checker and fixture hashes are pinned in the new
[selected_torque_wedge_certificate.py](selected_torque_wedge_certificate.py).

## Exact source localization and unrestricted-angle reduction

The parent's complete twelve-cell fan has physical projection area
A(u/||u||)=C.u/||u|| in each closed cell, including all boundary ties.
For D_(1/2) the complete corner/edge/interior algorithm gives

    max A(n)^2=(4894930+2178010s)/44649,
    A(n)<T=14788791/1000000,
    A(n)-a0<36059/500000,
    ||n-m||<d=1659/31250,                                 (2)

where a0^2=(3503950+1491850s)/31581 is the global minimum area squared.
The active maximum is corner 2; all positive-cone edge and interior
critical points are checked before this conclusion is drawn.

A new global conditional source lemma is

    A(k)<=T  implies  dist(k,Gm)<a=9/100                   (3)

for every unit original source k. Its fixed witnesses are in
[expected_selected_torque_wedge.json](expected_selected_torque_wedge.json).
Sixteen closed fan triangles cover all twelve source cells. The complete
prefix-free midpoint subdivision has **109 closed leaves**, **140 nodes**,
depth at most five: **57 cap leaves and 52 above-area leaves**. Each leaf
uses three positive-branch squared corner tests, 327 strict inequalities.
With c=1-a^2/2, a cap corner satisfies

    M.u>0, (M.u)^2>c^2||M||^2||u||^2;

an above-area corner satisfies

    C.u>0, (C.u)^2>T^2||u||^2.

For every nonnegative corner combination, linearity and the norm
triangle inequality extend the chosen strict bound to the entire closed
leaf. Hence a leaf either lies in the a-cap or has area strictly above T.
The complete leaf record SHA256 is

    4e61219975bb7413e75ec9a37a5f379a045b5dcecbd357eb08e91eb9be5dc9d8.

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

    E=509411203690689/39062500000000000,
    H=20/9, tau=26991/40000.

The upward near-zero quadratic

    (2H+E)x^2-2tau x+E>=0

is positive at zero and negative at 1/10. The first root is strictly
below 9993/1000000; the grid predecessor and proper small branch are
checked. Consequently the full surviving roll chord is below
9993/500000.

In (2), d exceeds the old 1/20 receiver guard. We do not invoke that
numerical guard outside its range. The transport and signed-envelope
identities above hold for these acute nonantipodal normal pairs; the
new checker instead tests a<=1/5 and d<=3/40, the actual positive
quaternion branch and all new interval inequalities. With

    X^2=(a+d)^2+(9993/500000)^2=1043680797/50000000000,
    P=(1-a^2/4)(1-d^2/4)(1-(9993/500000)^2/4),

the exact tests give P>(99/100)^2 and 99/100-ad/4>0. The perpendicular-
axis quaternion identity of the parent bounds the principal full angle
by 2asin(X/2). The derivative test
(1003/1000)^2(1-X^2/4)>1 then yields

    theta<Theta=144911/1000000.                           (6)

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

    113523/125000,468867/1000000,30063/62500,47651/40000,
    580603/500000,580603/500000,47651/40000,30063/62500,
    468867/1000000,113523/125000.

For each corner they strictly exceed ||V_source||||mu||/2. Norm convexity
extends the same bound throughout D_(1/2). The normalized torque points

    S_j(u)=(V_source cross mu(u))/B_j

are affine in the raw unit-z receiver u; no physical-normal denominator
has been omitted. The four retained original contact ids 1,3,8,10 have
40 strictly positive cubic cofactor coefficients and three identically
zero quartic vector balances. Their rank is three. Hence zero is in
the interior of the selected torque hull everywhere on the closed
receiver triangle.

There are 120 possible facet triples. For each, the checker considers
all seven nonempty relative simplex faces. The base **840** cases have
716 strict opposite-gap cases, 119 nonnegative plane-distance cases,
and five unresolved cases in just two original contact triples:
(3,4,6) and (5,7,8). Unresolved is not treated as proved. For each of
those two triples the fixed four closed midpoint children 0,1,2,3 are
checked, again with every one of the seven faces. Each child cover has
24 opposite-gap and four distance cases, with no unresolved or
degenerate leaf cases. Equivalently, replacing the two base triples by
their complete child covers gives **882 terminal cases**, 758 opposite
and 124 distance. Every receiver edge and corner is covered.

For a candidate triple let N be the actual cross-product normal and H
its signed height. A distance case proves, by the nonnegative
homogeneous coefficients on its relative face,

    H^2-rho^2||N||^2(lambda0+lambda1+lambda2)^2>=0,
    rho=Theta+1/100=154911/1000000.                        (7)

Strict opposite gaps rule out a supporting facet; a zero normal is
handled by degeneracy. Positive origin-interiority and all possible
supporting facets imply that the selected hull contains the centered
closed rho-ball. There are **6370 joint vector/scalar formula audits**:
6240 at the base corners and an interior barycentric point, plus 130
in the ten fixed refinement-tree nodes. The refinement count uses ten
actual gaps per sample, rather than the older twelve-contact audit
count. Complete base coefficient and case hashes are

    eeedbbcaf5ef5e200e9714e147c25b401ad4ae3fc6f648f172d148198bd9eff2,
    dc496e841d07286eacc3e6eb89c37f41b4c81dc0b6625e4335103de4ccdadb0b.

The refinement coefficient hash is

    e2d10893e838b8bfabc30eea144d258dac43fd6d2223763f52989e49e626e1c3.

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

D_(1/2) contains the entire D_(2/5), with unit-z chart area ratio **25/16**.
This is not a spherical area ratio. The new strict interior witness has
barycentric weights (1/10,1/15,5/6). For all sixty projective body images,
the checker verifies its mixed Cramer signs outside each of the five
previous triangular cones: the two D4 triangles, whole cell7, old D9
triangle and D_(2/5). These are **300 exact cone tests**. Thirty squared
axis comparisons put it at chord greater than 1/50 from every signed
minimum center, outside all old closed 1/64 caps. Thus this is a strict
addition to the entire previously retained explicit union. D4,D9,
cell7 and caps remain valid separately.

From the repository root, Python 3.11+ standard library only, run
sequentially with numerical threads one:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B geometry/rupert_deltoidal_symmetry/selected_torque_wedge_certificate.py --prerequisites
python3 -B geometry/rupert_deltoidal_symmetry/selected_torque_wedge_certificate.py --hull
```

Each command compares every expected field with the compact fixture.
Final public checks matched every expected field: prerequisites
24.588182 seconds / 24620 KiB, hull 16.444644 seconds / 23860 KiB,
under separate 55-second deadlines. Twelve new malformed controls reject.
The fixture SHA256 is
`13fd9a4153d6905f9daf83bc7d2b0b9fe1a5a1a951484186628e1d4ecacd5b7e`.
All private source-cover fields and full leaf records, all new phase
fields and 36 endpoint margins, every selected hull mathematical field,
all 120 case hashes and both fixed refinement records match production.
These are definition and regression checks, not independent review.

The prerequisite command pins and replays the direct parent's complete
prerequisite block, including its signed Rodrigues audits and ancestor
checks; it then checks the new source/phase, receiver geometry and
malformed controls. It does **not** rerun the old 2/5 torque hull or the
six older receiver-piece hull jobs. The hull command checks every new
selected facet and each supplied closed refinement leaf. Python -O is
explicitly refused. The original body model, Python Fraction arithmetic,
inspected Q(sqrt(5)) sign kernel, imported exact parent theorems and
written continuous bridges remain the trust boundary. This is not a
formal proof or independent review.

The next nonlocal frontier is the complement of the retained receiver
union. A 2/3 wedge trial fails the present fixed signed remote-roll
sufficient bounds before torque testing. That failure is not evidence
of passage or nonexistence. Sharper source-height directional envelopes
or additional actual original roll witnesses may improve the next
region; no resource setting was increased.

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

Current primary status was checked in
[Gosain--Grimmer Table 3](https://arxiv.org/html/2509.08190), which retains
the deltoidal and pentagonal hexecontahedra as unresolved Catalan cases.
[2604.26531](https://arxiv.org/html/2604.26531) retains the standard RID
conjecture; [2508.18475](https://arxiv.org/abs/2508.18475) proves a different
non-Rupert convex body. No primary resolution of our named solid was
located in the bounded refresh. The qualitative uniform local-gap
phase at graph 7322 remains closed. Neither it nor this larger explicit
receiving domain resolves global Rupertness.
