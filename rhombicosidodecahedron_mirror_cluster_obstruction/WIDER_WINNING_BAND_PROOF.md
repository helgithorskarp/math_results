# All-source rigidity on the wider winning RID receiving band

**six-rupert-3 — researcher — 2026-09-30.** Complete written,
unformalized intermediate proof with exact finite certificates. This
new receiving-domain theorem is independently unreviewed. Global
rhombicosidodecahedron Rupertness remains **OPEN**; historical priority
is unasserted.

## 1. Exact theorem and inherited interfaces

Use the standard edge-two RID model: V is the sixty original signed even
coordinate permutations of (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2),
where phi=(1+sqrt(5))/2. Put K=conv(V)=-K, R^2=7+8phi,
P_n=I-nn^t, f(n)=min_{v in V}|v.n|, beta=(19-8phi)/29.
Let G be its sixty proper body rotations and J_n=2nn^t-I.
Winning means one of the ten projective original signed regions of
maximum squared height 1/3 in the complete 436-region classification.

**Theorem.** For every unit receiving n in a winning signed region with

    f(n)^2>=beta-1/150,

every original Q in SO(3), every planar translation t and lambda>=1,

    lambda P_n(QK)+t subseteq P_nK
      iff lambda=1, t=0, Q in G union J_n G.                (1)

These are exactly 120 proper orientations in two disjoint LEFT cosets.
Every boundary of the height cutoff, all chart walls and ordering ties,
all source families, original spatial rotations and planar rolls are
quantified. In particular no strict passage uses this entire winning
band. Lower winning receivers and nonwinning receivers in the wider
band are not excluded by this theorem.

The [wide threshold-source proof](WIDE_THRESHOLD_SOURCE_PROOF.md) in this
same contribution proves the threshold branch, including closed
translations and scales. Its complete original-height/cone/preimage
geometry is regenerated in both the standalone source checker and
[wider_winning_band_certificate.py](wider_winning_band_certificate.py).
These native checks are not claimed independent of each other.

The substantive inherited proof interfaces are the complete
[source spectrum](GLOBAL_CAP_PROOF.md), source
9e9374854d153addb1d7697d05fd4b5d0180849f, graph7256;
the [balanced support and full-roll proof](BALANCED_SUPPORT_PROOF.md),
source a28d2c5b3ceeaee468843f42fef97d3a6efafad8, graph7468;
the [whole winning receiver proof](WINNING_RECEIVER_PROOF.md), source
a666fd496161000af9dcb9dd408f3ed3d2a00fcc, graph7498;
and the [original injection proof](GLOBAL_SLACK_PROOF.md), source
d68a00c27754ac1517aba99197334e5e19fabb8b, graph7703.
The [expanded 1/450 proof](EXPANDED_GLOBAL_SLACK_PROOF.md), source
6afb6b9e4585a35561752b3ef34eccabaa0d7e3e, graph7755, supplies the
preceding domain. All new bounds and the larger-domain torque certificate
are computed here rather than transferred from that smaller triangle.

The independently selected [global review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_global_slack_review2/REVIEW.md),
six-reviewer-2, independent mathematical reviewer, source
e9b77dc0a403bd7093e03bb271db39a7f33e6401, graph
bafkreiahuxldhobwg2dajs7eqmpvjbcijnjdmh7ehxgxxd6n4ms4sga7ta at7792,
confirms both preceding global gaps and proves the stronger global
gap 1/445. It also independently checks all 720 rank permutations and
the sharp third-height square. That review does not assess (1).

## 2. All-source exhaustion and the threshold branch

Central symmetry and convex midpoints remove the translation and scale
as necessary conditions, leaving S=P_n(QK) subseteq T=P_nK. The diameter
identity diam(P_nK)^2=4(R^2-f(n)^2) forces f(k)>=f(n), k=Q^t n.
Exact comparisons give

    beta-1/150 > (449/1000)^2 > 1/7.

The complete spectrum leaves only winning and threshold sources;
an original axial sign boundary has f=0 and cannot occur. The entire
threshold family is excluded by the wide threshold-source proof:
both actual source circles have eight distinct original preimages,
whereas its complete closed rank-cone argument leaves only four possible
actual receiver support originals. The new exact height margin is

    2436127/3645000000>0.

There is no assumption f(n)^2<=beta for the winning branch. For the
threshold branch that inequality follows automatically from source
diameter dominance and the threshold maximum beta.

## 3. Fresh winning source and receiver localization

It remains to consider a winning source. Both actual source and receiver
have height strictly above q=449/1000. For their own actual winning
centers n0, the six positive original active tangents have disk squared
radius 8/3+4phi>9. Writing n=z n0+w gives

    f(n)<=c0 z-rho6||w||, c0=1/sqrt(3), rho6>3.

The same holds for k. Positivity gives z>0; with c0<289/500,

    ||w||<43/1000, z>499/500,
    ||n-n0||<(101/300)(289/500-q)<d=1/23.                  (2)

The rational cosine and acute-chord checks are fresh. In particular
d=1/23 replaces the older 1/24 factor chord. Bounding these chords only
by 1/20 would lose the closing rotation margin; the sharper (2) matters.

Proper body rotations and normal reversal fold the receiver into the
icosahedral chamber. The new chamber checks explicitly test all twenty
directed winning centers and all nineteen other-center wall defects.
Their complete minimum squared negative unit-wall defect is

    (2-phi)/3 > (1/23)^2.

Consequently the folded center must be B=(0,phi^-2,1), not another
directed orbit representative. The three chamber wall reflections are
actual signed body symmetries. Their negatives are proper; normal
reversal leaves P_n unchanged. No improper Q is introduced.

At B/||B|| the physical third coordinate exceeds 9/10. At chord less
than d the receiving third coordinate exceeds 9/10-d=197/230.
For the raw unit-z chart u=n/n_z, the cross-product estimate gives

    ||u-B|| < d/[(9/10)(9/10-d)]=100/1773<1/10.

Every chamber cell other than closed ABD has chart y<=D_y, while
B_y-D_y=7/5-4phi/5>1/10. Thus the whole folded receiving band lies in
closed ABD, with A=(0,0,1), D=(1/[phi(phi+2)],1/(phi+2),1).
This is a fresh 1/23 whole-chamber argument, not reuse of a 1/24 cap.

The actual original v_*=(-1,phi^3,-1) has the positive winning sign.
Since ||u||>=1, v_*.u>=f(n)||u||>q. Hence the receiver lies in
the ENTIRE closed triangle

    U=conv(B,(1-s)B+sA,(1-t)B+tD),
    s=(phi-1-q)/phi, t=(phi-1-q)/(phi-1).                  (3)

This strictly contains the predecessor's q=909/2000 triangle. Fresh
corner checks and norm convexity give

    ||u||<27/25, ||u-B||<11/200.                           (4)

The preceding 27/500 raw drift bound fails on the new triangle and is
not used. The larger 11/200 bound is sufficient below.

## 4. The entire larger torque triangle, with all facets and boundaries

Use the same ten persistent actual endpoint probes (v_j,e_j), where
each v_j is an original vertex and each e_j is an original length-two
edge. Their supports m_j=e_j cross u satisfy

    m_j.(v_j-v)>=0 for every actual v in V

at all three new corners: 1,800 exact comparisons. Linearity extends
these inequalities throughout closed U. Set T_j=v_j cross m_j.
Their center hull is regenerated, equals the complete center torque
hull, and has sharp centered ball radius phi-1>3/5.

Each torque changes by at most 2R||u-B||<9(11/200). Support functions
therefore retain an origin-interior ball strictly larger than

    3/5-9(11/200)=21/200>0.                               (5)

This establishes origin interiority separately from plane distances.
For all 120 possible triples and all seven nonempty relative simplex
faces, including the three edges and three corners, the new exact
homogeneous coefficient certificate establishes:

* 726 strata have strict opposite vertex-gap signs, so cannot be facets;
* 114 strata have supporting-plane distance at least 1/2;
* zero strata are degenerate or unresolved.

For an actual facet at a parameter, choose an affinely independent
triple of its vertices. Its parameter is in one of the seven relative
faces. A polynomial with coefficients of one strict sign has that sign
on the relative interior; the distance polynomial's nonnegative
coefficients prove the squared-distance bound on the whole face.
Zero polynomials are not accepted as strict opposite-gap witnesses.
This covers every possible facet, including changes and contact splits.
With (5), it proves

    (1/2) B_3 subseteq conv{T_j(u)} for every u in closed U. (6)

The direct exact polynomial construction is checked at the three
corners and a strict interior barycentric point: 480 normal/support,
4,800 gap and 480 squared-distance identities. The four nodes verify
the arithmetic construction; whole-face coefficient signs establish
the continuous statement. No sampled parameter assumption is used.
The checker compares the entire 840-case, center-hull, cut and outer
geometry output with the previously saved exact prototype; this is
native regression evidence rather than independent peer review.

## 5. Actual balanced C3 supports control every original roll

The inherited balanced proof establishes the exact original-coordinate
support identities. Its old f^2>=beta hypothesis forced winning
membership and bounded normal transport; those hypotheses now follow
directly from the source classification and (2). The identities need
no f^2>=beta once those facts are available.

Actual proper C3 body rotations, together with the MOVING proper half-turn
J_n, reduce every roll to |alpha|<=pi/6. For the three original source
preimages in an endpoint orbit, the signed reference axial height is
common. The three support normals sum to zero and their symmetric
second moment is scalar in the reference plane. Minimal source
transport of chord a_s consequently gives the exact average

    (1-a_s^2/4)[h+g(t)],
    g(t)=kappa sin(t)-h(1-cos(t)), t=|alpha|.

The term linear in source tilt cancels for every tangent, both signs,
all body gauges and zero source tilt. The full actual receiver
height-gap envelope, valid at receiver chord delta<=1/2, bounds its
three-support average by h+(2kappa/3)delta+(R/3)delta^2.
Thus any containment requires

    g(t) <= E=[(13/15)d+(3/2)d^2+(17/16)d^2]/(1-d^2/4)
               =5399/126900<77/1000, d=1/23.              (7)

Here kappa<13/10, h<17/4 and R<9/2 are inherited exact original
support/height bounds. Both normal chords are below d<1/10, so all
domains of the source averaging and receiver envelope hold.

The complete inherited concavity argument excludes the whole remote
roll interval: g is strictly concave on [0,pi/6], and its values at
roll chord 1/10 and at angle pi/6 exceed 77/1000. For residual roll
chord r<1/10, g(t)/r>41/40>1, giving r<=E, also at r=0.
No small-roll assumption is made initially.

The [proper perpendicular-axis composition identity](ORTHOGONAL_COMPOSITION_PROOF.md)
controls the full proper spatial rotation after the actual gauges.
Its chord is at most sqrt((2d)^2+E^2). Exact rational conversion gives

    (101/100)^2[(2/23)^2+(5399/126900)^2]<(99/1000)^2,
    Theta<99/1000.                                        (8)

The minimal transports have axes perpendicular to the reference
normal and the middle factor is an axial roll, exactly as required.
All body factors are proper; J_n is used at the ACTUAL receiver, not
at the fixed reference. Zero angles and both signs are retained.

For every nonzero full principal angle, (4), (6) and the orthogonal
exponential remainder give some actual supporting displacement at least

    Theta[1/2-R||u||Theta]
      > Theta[1/2-(9/2)(27/25)(99/1000)]
      =Theta(943/50000)>0.                                (9)

This contradicts even closed centered unit containment. Thus the
gauged full rotation is zero. Undoing the actual proper body factors
and receiving half-turn gives Q in G union J_n G. The precise row-frame
completion argument in BALANCED_SUPPORT_PROOF.md Section 5 remains
valid for these new numerical bounds; a fixed reference half-turn
would not suffice.

## 6. All translations, scales and exact equality orientations

Every Q in those two left cosets has equal projected sets: gK=K,
P_n J_n=-P_n and K=-K. Returning to the original translated/scaled
containment, its positive diameter forces lambda=1. The equal support
functions then force t=0 (in direction t, a nonzero translation would
add ||t||^2 to the support). Conversely lambda=1, t=0 and either coset
obviously give closed equality.

The checker enumerates all fifteen trace-minus-one proper body
rotations, verifies they are involutions, extracts each axis and
finds an ACTUAL original vertex of zero height on that axis. If J_n
belonged to G, it would be one of those half-turns and f(n)=0.
The receiving band has f(n)>q>0, so J_n is not in G. The two left
cosets are disjoint and contain exactly 120 proper rotations.
This proves (1), including the closed equality cutoff.

The domain is not vacuous: the actual ray u=(0,349/1000,1) has all sixty
original signs of the canonical winning region and

    f(u/||u||)^2=(911005-421592phi)/1121801.

Exact field comparisons put it above beta-1/150, below the reviewed
global beta-1/445 cutoff, and below the old conditional winning height
(909/2000)^2. This is an explicit new-band receiver, not a passage
certificate or a claim that it avoids every earlier exclusion piece.

## 7. Reproduction and honest remaining frontier

From a complete public repository checkout, Python 3.11+ standard library,
one process and all numerical threads one:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/wider_winning_band_certificate.py --self-test
~~~

Every output byte must match
[wider_winning_band_expected.json](wider_winning_band_expected.json).
The complete original injection parent is replayed byte for byte,
including all fifteen malformed controls. The new checker rejects
26 additional controls: unsupported phase and injection bounds,
missing originals or walls, wrong ranks, omitted simplex faces, an
incorrectly smaller raw drift, incomplete half-turn coverage and a
receiver outside the new band. It computes the full NEW 840-stratum
torque certificate. Large old region, balanced and independent-review
enumerations are inherited where cited and are not claimed rerun.

Inherited geometry already present in the public parent fixtures is
compared entry by entry during generation and represented by compact
manifests in the new output. New original receiving-height records,
all half-turn witnesses and the full compressed 840-stratum certificate
are retained. Matching native output is not independent validation.

Trust: original coordinates, inspected Q(phi)/Fraction and Python
semantics, hash-pinned complete prerequisites, and the written centering,
coercivity, whole-cone, chamber, proper-frame, full-roll, facet and
support-injection bridges. No solver, floating predicate, sampled
continuum, timeout, memory failure or incomplete enumeration proves
nonexistence. This is unformalized and independently unreviewed.

The new necessary condition for a strict passage is piecewise:

    winning receiver:    f(n)^2 < beta-1/150;
    nonwinning receiver: f(n)^2 < beta-1/445 (inherited review).

To prove a GLOBAL 1/150 gap it would remain to exclude the nonwinning
receiving band beta-1/150<=f(n)^2<beta-1/445. Its regional coercivity
puts receivers within chord less than 1/162 of actual threshold axes,
but the largest currently cited all-source closed beta-axis cap is
only 1/480. Extending that cap or obtaining a different original-support
criterion is a concrete next frontier. The lower receiving sphere
still remains even after such a hypothetical enlargement.

Current primary [2604.26531](https://arxiv.org/html/2604.26531) retains
RID non-Rupertness as a conjecture; [2508.18475](https://arxiv.org/abs/2508.18475)
proves non-Rupertness for a different constructed polyhedron.
The standard strict definition is in [2112.13754](https://arxiv.org/html/2112.13754).
The named-solid list and complementary teammate source links are
recorded in WIDE_THRESHOLD_SOURCE_PROOF.md. No different-body constant
is imported. The orchestrator is the management hub; independent
reviewers choose their own targets and verdicts.

Latest complementary source inspected before publication: six-rupert-1,
researcher, [deltoidal two-thirds wedge](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/two_thirds_wedge_proof.md),
source 3276bf5919f10ad27d159578b6c17175cc078485, graph
bafkreicl6wlxycuxhyvmpsmj4qf4mz4t3jg5hun3ccsecopv3ytoffigyy at7805;
and six-rupert-2, researcher, [J77 projection-area source localization](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_area/PROOF.md),
source cd0088c8aa1e308657b17d759bc5600c7b8b2b34, graph
bafkreibdvhqnug46ccnk4fwx3czbz4y7moj44qqimnjge6w6idkms5j4au at7801.
These supply current structural context, with no imported body constants.
