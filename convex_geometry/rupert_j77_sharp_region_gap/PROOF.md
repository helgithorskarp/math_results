# Sharp signed-region source reduction and an enlarged J77 receiver domain

Author: **six-rupert-2**, role **researcher**, 2026-09-30.

Let K be the standard unit-edge paragyrate diminished rhombicosidodecahedron,
Johnson solid J77, in the pinned independently reconstructed 55-vertex model.
All vertices have squared norm r^2=(11+4s)/4, where s=sqrt(5). Exactly fifty
vertices form an antipodal core. Choose its twenty-five representatives a_i
using the published original vertex order and the smaller index of each pair.
For a unit normal n set

    f(n)=min_i |a_i.n|,
    B=(65+10s)/596, c0=sqrt(B),
    D=(0,-1,(7+s)/2), n0=D/||D||,
    A=(0,(1+s)/2,1).

R denotes the verified proper 72-degree body rotation about A,
X=diag(-1,1,1) the verified body mirror, and M_n=I-2nn^T.
These are the same normalizations as the
[directional receiver proof](../rupert_j77_directional_receiver_domains/PROOF.md),
source f7cfae81911e86c562b226a04f7966989812f94d.

**Sharp regional theorem.** The twenty-five axial wall great circles
have exactly 602 directed strict sign regions, paired into 301 projective
regions. Every region has a unique maximizing direction for f. The full
regional maximum spectrum has fourteen values, given below, and thirty-seven
projective orbits under the verified C5v body group. Exactly five projective
winning regions have maximum squared height B, at the rays R^kD.
Every other region has maximum squared height at most **1/12**.
Equality is attained at exactly the five projective body images of

    E=(1,-(3+s)/2,0).

This is a sharp statement about REGIONAL maxima of the symmetric-core
axial function. Away from a verified receiving domain it does not assert
that the asymmetric full body's diameter is determined only by the core.

**All-source closed receiver theorem.** Put

    L=(0,-8/7,(7+s)/2), C=(1/40,-25/24,(7+s)/2).

For every unit receiver normal on a ray through the ENTIRE CLOSED triangle
conv{D,L,C}, or any of its C5v body images or normal reversals, every
Q in SO(3), arbitrary planar translation t and every lambda>=1,

    lambda P_n(QK)+t subseteq P_n(K), P_n=I-nn^T,

holds if and only if

    lambda=1, t=0,
    Q=R^k or Q=M_n X R^k for some k=0,...,4.             (1)

Every displayed form gives equal shadows. Thus the full closed receiving
domain excludes every strict Rupert passage from all source orientations
and rolls. No initial source-normal or full relative-angle restriction
is imposed. The entire previous receiver triangle is contained; the fixed-z
chart area grows by **30/7**. The L ray has chord greater than **1/35**
from n0 and its actual squared core height lies below the old cutoff.
The preceding complete radius-1/200 caps remain valid.

The general criterion in the preceding directional proof also improves:
replace ONLY its prerequisite F^2>(5-s)/20 by **F^2>1/12**, retaining every
other actual diameter, source-chord, receiver-support, roll, half-turn and
torque hypothesis. This includes the entire preceding criterion, not just
its examples. The proof of that transfer is in Section 4.

Both results are complete unformalized analytic proofs with exact finite
hypotheses. The current extension has no independent review or proof-assistant
checking. J77's **global** Rupert question remains open.

## 1. Signed cells and nearest-point certificates

Fix a nonempty strict signed cell. Write b_i=sigma_i a_i, sigma_i in {+1,-1},
so b_i.n>0 throughout the cell. Let y be the unique point of least norm in
conv{b_i}. A strict cell normal separates all b_i from zero, so y is nonzero.
Set c=||y|| and n*=y/c. The nearest-point condition gives

    b_i.y>=||y||^2 for every i.                          (2)

Hence b_i.n*>=c>0, so n* belongs to this SAME strict cell. A convex
combination y=sum w_i b_i, w_i>=0, sum w_i=1 gives

    min_i b_i.n* <= sum w_i b_i.n* = y.n* = c.

Together with (2), this proves f(n*)=c. For every unit normal n in the cell,

    f(n)=min_i b_i.n <= y.n = c(n.n*) <= c.               (3)

Equality at c forces n.n*=1 and therefore n=n*. This proves uniqueness.
It also supplies the quantitative necessary reduction

    f(n)>=F>0  implies  ||n-n*||^2<=2(1-F/c).            (4)

It works even if the active tangent convex hull has zero disk inradius.
The convex nearest-point lemma is standard; the contribution here is its
complete exact J77 classification and resulting sharp source reduction.

Every positive-weight b_i in a closest-point representation lies in the
supporting plane b_i.y=c^2. Caratheodory in that two-dimensional plane
therefore gives a representation using at most three active vectors.
With equal-radius data, one active vector gives its own direction; two
give the signed sum, because the closest point of an equal-radius segment
is its midpoint; three give the normal ray of their affine plane. These
are the 9,825 one/two/three candidate occurrences in the
[earlier active-set proof](../rupert_j77_all_source_diameter_caps/PROOF.md).

The new checker canonicalizes their projective rays and scores each against
all twenty-five representatives. It finds 3,306 distinct rays, 335 on axial
walls and 2,670 positive but nonstationary candidates. For each stationary
candidate d, put h=min_i|a_i.d| and

    y=(h/(d.d))d, c^2=h^2/(d.d).                        (5)

These quantities lie exactly in Q(s). The checker regenerates a balance of
at most three actual signed active vectors. It independently verifies its
nonnegative weights, sum one, ALL THREE balance coordinates, all twenty-five
inequalities (2) and the complete active tie set. There are **301 nearest-point
certificates and 7,525 support comparisons**. Each certificate proves an
actual cell maximum by (2)-(3), rather than merely labeling a candidate.

## 2. Complete region coverage, spectrum and sharp gap

All C(25,3)=**2,300** determinants of distinct core representatives are
nonzero. Pair cross products are nonzero as well. Thus the axial great
circles are distinct and no three meet at a common spherical point.
The first circle gives two regions. The jth circle has 2(j-1) distinct
intersection points with previous circles and adds 2(j-1) regions.
Therefore the total is

    2+25*24=602 directed regions, or 301 antipodal pairs. (6)

A strict sign set is a normalized convex cone inside one open hemisphere,
so it is connected. Each region has one sign vector; reversing its normal
complements all twenty-five signs. The checker uses the smaller integer
encoding of a sign vector and its complement as its projective cell key.
The 301 certificates have DISTINCT projective keys. Formula (6) consequently
proves complete coverage independently of candidate pruning. There is no
unexamined region. The active-set argument is a complementary completeness
route, with the orthogonal one/two/three controls checked explicitly.

The full spectrum, in decreasing order, is as follows. Counts are projective
regions; their sum is 301. Directed counts are twice these counts.

| Maximum squared height | Projective regions |
|---|---:|
| (65+10s)/596 | 5 |
| 1/12 | 5 |
| (371-20s)/4484 | 10 |
| (371+164s)/12644 | 10 |
| (15-4s)/116 | 35 |
| 1/28 | 20 |
| (5-2s)/20 | 6 |
| (11-4s)/164 | 30 |
| (7-2s)/348 | 15 |
| (26-11s)/284 | 40 |
| (51-4s)/10084 | 40 |
| (41-18s)/244 | 15 |
| (127-56s)/1796 | 30 |
| (299-132s)/9124 | 40 |

The checker compares these values exactly, regenerates the complete table,
and partitions all its axes into **37** orbits under the actual C5v
rotations and mirror. Every orbit has one height value, all images are
present, and the orbit union is the full table. Compact exact representatives
and counts are in expected.json. The winning axes are exactly the D orbit.
The next five are exactly the E orbit, with squared height 1/12. This
proves both the universal nonwinning upper bound and its sharpness.

The previous cutoff beta=(5-s)/20 was an upper bound obtained by scoring
ALL nonmaximizing active-set candidates, including nonstationary ones.
Its witness ['two',1,2,-1], in the twenty-five CORE indexing, has score beta
but belongs to the winning D sign region. Its ray differs from the regional
optimizer. This is checked by exact scoring and its canonical sign key.
The earlier upper bound remains correct; the sharp regional bound is smaller.

## 3. Necessary source elimination from the actual receiver diameter

At a receiver where the ACTUAL full-body diameter satisfies

    diam(P_nK)^2=4(r^2-F^2), F=f(n),                     (7)

every contained unit-scale source has f(source)>=F: its antipodal core
diameter is 2sqrt(r^2-f(source)^2) and is a lower bound for its full diameter.
If **F^2>1/12**, (3) and the complete spectrum force its signed cell into
one of the ten directed winning D regions. It cannot lie on an axial wall,
where f=0. This conclusion is for every source orientation, not a sampled
or initially aligned source.

The inherited winning tangent hull has disk radius
rho, rho^2=(233-10s)/596, and in its winning cell

    f(source)<=c0(source.n*)-rho||P_n*source||.

Therefore, exactly as in the preceding proof, every possible source can
be gauged to normal chord at most

    a=(101/100)(c0-F)/rho, provided a<=1/10.             (8)

The proof first establishes a positive optimizer dot product, bounds the
tangent sine, and uses its checked sine/chord conversion. Its proper and
improper body/frame gauges remain unchanged. An improper source symmetry
S transforms the row-frame cross normal by det(S)S^T; completing by this
normal gives a proper frame. No improper matrix is treated as a proper
relative rotation. Translation remains present.

The weaker but all-cell estimate (4) is available for future source classes
below 1/12. It is not needed for the present receiving triangle.

## 4. Transfer of the directional criterion, retaining translations

The complete [directional proof](../rupert_j77_directional_receiver_domains/PROOF.md)
is a dependency. After it forces the source into a winning region, no later
step uses the old beta. Thus the sharp gap replaces ONLY that prerequisite.
For clarity, the other hypotheses and implications remain explicit here.

Put delta=||n-n0|| and epsilon=1/25. The reference minimal transports obey

    ||B0(A^T-I)v||<=|v.n0|x+||v||x^2/2

for normal chord x. Require delta<=1/20 and a,delta<=1/10. The inherited
three remote-roll receiver probes m_j and their actual width-support tie
heights kappa_j have full original-pair gap envelopes. All 9,075 difference
pairs and 5,166 excess-height comparisons are replayed. For every actual
chosen source difference w_j the necessary support-gap error is

    E_j=||m_j||[|w_j.n0|a+kappa_j delta+r(a^2+delta^2)].

For all twelve signed closed pieces [l_j,b_j] of x=tan(|alpha|/2) in
[1/50,1], require gamma_j>(1+b_j^2)E_j, where gamma_j is the inherited
exact lower quadratic Bernstein gap. These pieces cover every remote roll.
Only the difference body is quotiented by a half-turn at this stage.

The full J77 shadow is asymmetric. Its separate near-half-turn stress
has positive weights on cycle probes 2,5,12 with sum one and normal sum
zero in all three coordinates. Their opposite support excess is
g_pi=(-151+74s)/241. With actual minimum-support preimage heights xi_i and
maximum-support tie heights kappa_i^+, require

    g_pi > sum w_i||m_i||[
            xi_i a+kappa_i^+delta+(r/2)(a^2+delta^2)+r epsilon].

All 165 original single-vertex and 120 excess-height comparisons are
replayed. Summing its necessary inequalities cancels the arbitrary
translation and rejects the full-shadow half-turn branch.

The remaining full roll is less than epsilon. Minimal transport angles
and the proper rotation-angle triangle inequality give

    theta(Q')<Theta=epsilon+(101/100)(a+delta).

The inherited 34 probes p_l and six strictly positive signed-coordinate
combinations have sum a_l p_l=0, sum a_l(v_l cross p_l)=sigma e_k,
sum a_l<C0=61/10 and r||p_l||<M0=9/8. Require ACTUAL receiver supports
P_n p_l at the designated original vertices and

    3[C0 M0(delta+Theta/2)]^2<1.                        (9)

Projection preserves translation balance. Its torque perturbation and
the exponential remainder give a strictly positive weighted displacement
for any nonzero Q', contradicting closed containment. Thus Q'=I and the
translation vanishes. These are actual receiver supports, not an invocation
of the old fixed cap at a larger receiver drift.

For scale lambda>=1, divide a purported inclusion by lambda. Convexity
and zero in the interior give a unit-scale inclusion with translation
t/lambda. Its classification gives equality of shadows and zero original
translation; their positive diameter then forces lambda=1. Undoing the
body gauges gives exactly (1), including boundary containments. Conversely
R^kK=K, XR^kK=K and P_nM_n=P_n prove all displayed equalities.

This proves the receiver criterion for F^2>1/12, with all other hypotheses
unchanged. It includes the entire previous criterion because 1/12<beta.

## 5. The entire enlarged triangle and the genuine cutoff crossing

All fifty core vertices have a common strict axial sign at D,L,C. Their
signed linear heights and the norm triangle inequality give a normalized
lower bound F_* from the minimum corner height throughout the entire
triangle. A positive cap-cone argument gives delta<=delta_*, the maximum
corner chord. The error expressions in Section 4 increase in nonnegative
a,delta, so uniform outward corner bounds suffice for every phase condition.

For each of the 34*54 original probe/vertex differences z, the ACTUAL
receiver support has homogeneous quadratic numerator

    (p_l.z)(u.u)-(p_l.u)(u.z).

Every one of its six triangular quadratic Bernstein coefficients is
strictly positive: **11,016 checks**. For each of the 1,460 nonantipodal
differences z, the comparison with the V11 antipodal pair has numerator

    (4r^2-z.z)(u.u)+(z.u)^2-4(V11.u)^2.

All six coefficients are strictly positive: **8,760 checks**. The maximum
core antipodal diameter dominates this one antipodal pair, which in turn
dominates every nonantipodal difference. This proves (7) for the full
asymmetric body throughout the CLOSED triangle. V11 need not remain the
sole axial minimizer. All 3,296 quadratic identities are independently
replayed at the barycenter using actual physical projections. Those points
audit the algebra; the coefficient signs prove continuum coverage.

The exact outward bounds give source chord below 0.029923, full relative
angle below 0.099867 radians, and positive minimum remote-roll, half-turn
and torque margins of approximately 0.002918, 0.002864 and 0.111887.
These decimals describe the exact rational-field inequalities in expected.json.
The full original source orientation and roll remain unrestricted.

The actual far-corner height, computed without a square-root approximation,
is

    f(L/||L||)^2=(142913+26600s)/1517156.

Its value is strictly between 1/12 and beta. Thus the old prerequisite
REALLY fails at a receiver in the new domain; this is not merely a loose
uniform lower enclosure crossing the old threshold. An outward LOWER
chord enclosure proves ||L/||L||-n0||>1/35.

Write the old triangle as D,L_old,C_old. The exact identities

    L_old=(5/12)D+(7/12)L,
    C_old=(17/40)D+(7/40)L+(2/5)C

prove containment of its entire convex hull in the new one. The new exact
area in the fixed-z affine chart is 1/560, versus the previous 1/2400,
giving ratio 30/7. No spherical-area ratio is asserted. Actual body
symmetries and normal reversal transport the entire theorem and its
closed-equality classification to all stated images.

## 6. Reproduction, trust, credit and the next obstruction

From repository root, Python 3.11+ standard library:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    python3 -B convex_geometry/rupert_j77_sharp_region_gap/verify.py --self-test

Keep the directional receiver directory and its all-source diameter-cap,
diameter model and translated-local siblings. Seven direct files are pinned,
with twenty-one more pinned transitively. The full directional parent checker
is replayed and compared with its complete published expected output.
Normal and optimized Python produce identical complete output. All 301
full nearest-point certificates also match the private development prototype
entry for entry; this is regression evidence, not independent review.

The compact output gives the complete fourteen-level/37-orbit classification
and hashes the regenerated 301 nearest-point records. It does not require
a hidden record corpus. Every nearest-point and arrangement hypothesis is
checked directly. Three orthogonal controls exercise one/two/three active
cases. Eight new malformed controls and twenty inherited controls are
rejected, including incomplete/duplicate cells, false points or weights,
a false gap, nongeneric walls and an unsupported larger receiver triangle.
Rejection of a sufficient criterion supplies no passage or nonexistence
conclusion for that receiver. There is no solver or floating-point premise.

Exact integer/Fraction and the pinned ordered Q(s) kernel supply finite
arithmetic. New signs are also audited against an independent rational
enclosure of sqrt(5). Radical quantities use the fixed denominator-10^12
outward grid intervals, checked by exact squaring. Written nearest-point,
great-circle, winning-region, frame, transport, translation-balanced
roll/stress, full-angle, torque and normalized Bernstein arguments are
the continuous trust boundary. The current proof is unformalized/unreviewed.

The direct mathematical source is
[six-rupert-2's preceding directional proof](../rupert_j77_directional_receiver_domains/PROOF.md).
Its source-height transport is derived there with precise credit to
**six-rupert-3**'s
[RID directional proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/DIRECTIONAL_TRANSPORT_PROOF.md),
source 30c9c86753797307cc17b56ffd76aa88d94987df. J77's translations and
asymmetric half-turn are retained; RID's centering does not transfer.

**six-reviewer-1** independently confirmed the earlier all-source cap
theorem and improved its radius to 1/1400 in the
[committed review](../rupert_j77_all_source_review1/README.md),
source e78fafefba916f04dc61ec7e2f9556e1469776a1, graph
bafkreialgb2n4e3yjo77r7gkgmaclia4evw2zkww7rgrzsw3ywznxopfum.
That review's independent active-set and local-stress audit supports the
parent geometry; it does not review the current spectrum or extension.
No reviewer verdict was requested or influenced.

The [uniform J77 local phase](../rupert_j77_uniform_local_exclusion/PROOF.md),
source d23b45ee6e2d2704087e42b6a4faef698c53b14d, remains closed and
complementary. **six-rupert-1**'s
[deltoidal uniform phase](../../geometry/rupert_deltoidal_symmetry/twofold_area_proof.md),
source 58ec651cdd077243b556287369b6f56132735f6d, concerns another solid.
Neither existential angle is a numerical sphere-cover cutoff.
The same researcher's
[deltoidal area theorem](../../geometry/rupert_deltoidal_symmetry/global_area_proof.md),
source 5596212ab31932f7dd8b90cf6f1ad73c66afbe16, and **six-rupert-3**'s
[actual torque-hull simplex proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/ACTUAL_TORQUE_HULL_PROOF.md),
source 684f35df160134d1fefb14da75f5948ce8ac00ce, offer further invariant
and continuous-facet methods. Their constants and central symmetry are
not premises of this J77 result.

The final refresh also read **six-rupert-1 (researcher)**'s
[adaptive deltoidal area and roll proof](../../geometry/rupert_deltoidal_symmetry/adaptive_area_proof.md),
source 2a0eb5428787e69876ac4652f7d8c192c07fa9e2, graph
bafkreiejtc4l7y4ubwokktltjem2nb2rviz3ds3jld4yavourzxaacwc4m,
and **six-rupert-3 (researcher)**'s
[orthogonal transport-composition proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/ORTHOGONAL_COMPOSITION_PROOF.md),
source 4ccd4e7803077dacfcd993e01caeaaf001dc18d5, graph
bafkreigmk5cetignwl2kdcdsks5mbnwajuamd4znhr5iorjgol7wzmf26y.
The first derives a complete reduced-roll chord bound 2 eta for its
reference shadow when eta<=1/28, using that shadow's actual maximal
radii and two signed support edges. The second proves a general
composition bound sqrt((a+delta)^2+e^2) for two transports with axes
perpendicular to the reference normal and an intervening axial roll,
when all three factor chords are at most 1/10. These are precise leads
for reducing the next J77 rotation bounds. Neither is an input to the
present certificate; J77's actual signed support edges, asymmetric
half-turn branch and translation balances must still be proved.

Current primary status refreshed 2026-09-30:
[Gosain–Grimmer Table4](https://arxiv.org/html/2509.08190) retains
J72,J73,J74,J75,J77 without a known passage;
[Zeng](https://arxiv.org/html/2604.26531) states 87 of 92 Johnson solids
known Rupert; the required
[Nopert construction](https://arxiv.org/abs/2508.18475) concerns another
body. Standard projection and local definitions are in
[Steininger–Yurkevich](https://arxiv.org/abs/2112.13754) and
[Scott](https://arxiv.org/html/2208.12912). Bounded current searches found
no later J77 resolution and establish no historical priority.

The former beta source threshold is now a closed obstruction with a
sharper exact substitute. On the enlarged triangle the actual sharp-gap
margin is substantial; remote-roll and translated half-turn errors are
closer to binding. The next step is receiver-dependent residual roll
control, followed by the perpendicular-axis composition bound after
checking J77's actual proper frame decomposition. Actual balanced-torque
estimates over further whole receiver pieces are another concrete route.
Other source classes can be treated by (4) when the receiver height
reaches 1/12. The complementary receiver sphere, an exact strict passage,
or a full global non-Rupert proof remain open. Failed searches, timeouts
and incomplete enumeration prove no mathematical nonexistence.
