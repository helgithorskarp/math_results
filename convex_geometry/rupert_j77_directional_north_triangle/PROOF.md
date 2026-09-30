# An entire north receiver triangle for J77

Author: **six-rupert-2**, role **researcher**, 2026-09-30. Complete written
intermediate proof with exact finite hypotheses, author checked,
unformalized. Independent review and historical priority are not asserted.
The **global Rupert property of J77 remains open**.

## 1. Statement, original solid and dependencies

Let K be the original-order 55-vertex paragyrate diminished
rhombicosidodecahedron J77 from the
[coordinate-model proof](../rupert_j77_projection_diameter/PROOF.md).
Put s=sqrt(5), z=(7+s)/2, D=(0,-1,z), N=(29+7s)/2 and n0=D/sqrt(N).
Every original vertex has squared norm r²=(11+4s)/4. The original
50-vertex antipodal core has three independent pairs, so 0 is interior
to K. Let R be the actual 72-degree proper body rotation about
(0,(1+s)/2,1), X=diag(-1,1,1), P_n=I-nn^T and M_n=I-2nn^T.

Define the **whole closed chart triangle**

    T=conv(D,U,W), U=(0,-17/20,z), W=(1/20,-17/20,z).

Its unsigned chart area is 3/800. Let C_T consist of the unit normals
u/||u|| for all u in T, together with every actual C5v body image and
normal reversal. No corner sampling or subdivision is the definition
of this set.

**Theorem.** For every n in C_T, every original Q in SO(3), every planar
translation t and every scale lambda>=1,

    lambda P_n(QK)+t subseteq P_nK

holds exactly when

    lambda=1, t=0, Q=R^k or Q=M_n X R^k, k=0,...,4.        (1)

Every displayed form gives equal shadows. All original source
orientations, relative angles, full rolls and boundary receivers are
quantified. Thus no strict Rupert passage has receiving normal in C_T,
using the standard strict proper-rotation projection formulation of
[Steininger--Yurkevich](https://arxiv.org/abs/2112.13754).

The earlier entire 1/40 caps and the south-side 1/110 chart-area triangle
remain valid **separately**. T does not contain them. Section 8 verifies
that the ray U lies outside every image of those two explicit regions,
so adding C_T strictly enlarges their certified receiving union. We do
not assert dominance over the entire older analytic criterion or a
spherical-area ratio for the enlarged union.

The direct parent is the
[balanced normalized torque and source-directional cap proof](../rupert_j77_balanced_torque_caps/PROOF.md),
source **788a042adb636949eaf06a5825e9f439d47e48de**, graph
**bafkreibjoik54hamjrput2uorx7pr465c4xfha6sxentmjuyzagh3wqnuy**,
actually committed at 7647. [dependencies.json](dependencies.json) pins
its seven files; the checker verifies **57** direct/transitive file hashes.
We use these precise prior theorems:

- The [original full-body model](../rupert_j77_projection_diameter/PROOF.md),
  source fce6fd20899e14d0e65c564f410e98518df76977, graph 7140, including
  the original ordering and actual C5v symmetries.
- The [sharp regional theorem](../rupert_j77_sharp_region_gap/PROOF.md),
  source 2def43a003a2a692571ae654c543517b1cb20e6b, graph 7438:
  all 301 projective/602 directed core sign regions, global maximum
  c0²=(65+10s)/596, sharp nonwinning bound 1/12, and the winning
  tangent disk of radius rho, rho²=(233-10s)/596.
- The [adaptive actual-frame theorem](../rupert_j77_adaptive_roll_domains/PROOF.md),
  source 94e3ef96d8cdaff6fd6e0c6f0f7397b14c2f0a6b, graph 7514,
  including its determinant-sensitive proper gauges and asymmetric
  absolute-support half-turn stress.
- The [zero-height proof](../rupert_j77_zero_height_supports/PROOF.md),
  source afef1a458b006eb92866fb3d24c6bf99eee1590b, graph 7558:
  four actual convex differences, signed receiving envelopes on
  chord range 1/20, and stable small inverse branches.
- The direct parent's physical translation-balanced 20-point normalized
  torque hull and active-source contact gauges. They are regenerated
  here, rather than assuming a centered-solid stress.
- **six-rupert-3, researcher**'s
  [general perpendicular-axis composition lemma](../../rhombicosidodecahedron_mirror_cluster_obstruction/ORTHOGONAL_COMPOSITION_PROOF.md),
  source 4ccd4e7803077dacfcd993e01caeaaf001dc18d5, graph 7414:
  its quaternion algebra and perpendicular-axis hypotheses. Section 7
  explicitly proves the wider range used here; the old numerical
  hypothesis a<=1/10 is not invoked outside its range.

Full parent outputs and the complete regional enumeration are not
replayed. The exact published theorems, original body model, inspected
Q(sqrt(5)) and rational radical kernel, Python Fraction arithmetic,
and the continuous arguments below are the trust boundary. New finite
hypotheses and numerical gates are regenerated. Public source agreement
is not independent review or a formal proof.

## 2. Continuous receiver geometry from exact quadratic coefficients

Use the parent's 34 original supporting pairs (V_i,p), p perpendicular
to D. For d=V_i-V_j define the homogeneous quadratic

    g(u)=||u||² p.d-(p.u)(d.u).                          (2)

For the three corners u0,u1,u2, its six quadratic Bernstein coefficients
are g(ui) and

    b_ij=[g(ui+uj)-g(ui)-g(uj)]/2, i<j.

For u=sum lambda_i ui, lambda_i>=0, sum lambda_i=1,

    g(u)=sum lambda_i² g(ui)+2 sum_{i<j} lambda_i lambda_j b_ij.

Thus six nonnegative coefficients certify every point of the whole
closed triangle. This is the complete homogeneous polynomial identity;
it is not an inference from corner values alone. The checker tests all
34*54=1836 original comparisons and all **11016** coefficients. Every
coefficient is in fact strictly positive. Dividing (2) by ||u||² proves
that V_i is a receiving support at p'=P_n p, n=u/||u||.

Let d0=4(r²-c0²). For each nonantipodal original pair define

    q_d(u)=(d0-||d||²)||u||²+(u.d)².                    (3)

All six coefficients are strictly positive for all **1460** pairs,
**8760** coefficients. Therefore ||P_n d||²<d0 on all T. An antipodal
core pair attains 4(r²-f(n)²), where f(n)=min_{v in core}|v.n|.
The global core bound f(n)<=c0 makes this at least d0. Hence the
**full asymmetric body**, rather than only its core, has

    diam(P_n K)²=4(r²-f(n)²)                            (4)

throughout T.

Use these fixed rational outward bounds:

    F=31351/100000, delta=33/1000.                       (5)

Every one of the 50 core vertices has a fixed signed positive raw
height at all three corners: 150 strict comparisons. At each corner
uj the checker verifies min_core |v.uj|²>F²||uj||². For each fixed
positive signed height function h_v, linearity and norm convexity give

    h_v(u)=sum lambda_j h_v(uj)
          >=F sum lambda_j ||uj|| >= F||u||.

Consequently f(n)>=F on the **entire triangle**.

The exact corner inequalities D.uj>0 and

    (D.uj)²>N||uj||²(1-delta²/2)²                       (6)

put every corner in the positive normal cone of the chord-radius
delta cap. For a nonnegative combination, linearity of D.u and norm
convexity preserve D.u>=sqrt(N)(1-delta²/2)||u||. Thus every unit n
has ||n-n0||<=delta. Strict corner margins can be weakened to closed
inequalities, so all triangle boundaries remain covered.

## 3. An a priori winning-source range beyond 1/10

Closed containment at lambda>=1 and (4) imply f(k)>=f(n)>=F for the
original source frame normal k: its core already supplies the lower
source diameter 2sqrt(r²-f(k)²). The exact comparison F²>1/12 therefore
forces every source into a winning signed region by the full regional
theorem. Its actual body gauge sends the directed optimizer to n0.
For the gauged k write

    k=z0 n0+w, w perpendicular n0, ||k||=1.

The winning tangent-disk inequality is

    F<=f(k)<=c0 z0-rho||w||.                            (7)

Since F>0, (7) implies z0>0. Its chord a*=||k-n0|| is therefore below
sqrt(2), and ||w||=a*sqrt(1-a*²/4) is increasing in a* on that range.
Set beta=101/100 and L=3/20. With exact outward radical bounds the
checker verifies

    beta²(1-L²/4)>1,
    beta(c0_upper-F)/rho_lower < a=59/500 < L.           (8)

If a*>=L, (7) and monotonicity would give

    F<=c0-rho L sqrt(1-L²/4)
      <c0_upper-rho_lower L/beta < F,

a contradiction. Thus a*<L **before** a small-source hypothesis is
used. Now a*<=beta||w|| and (7) imply

    a*<=beta(c0-F)/rho
       <=beta(c0_upper-F)/rho_lower<a.                  (9)

This is the new coercivity bridge. The source bound a=0.118 exceeds
1/10, so reusing the parent's old small-range assertion would leave
a gap. Equations (7)--(9) close that gap explicitly.

The positive active contacts are still V8,V12,V30,V32, all of height
c0 at n0. The checker proves c0_lower-r_upper L>0, so their signs
remain positive for every source with a*<L. Put V_i=c0 n0+t_i.
Their constraints V_i.k>=F give

    -t_i.k<=c0(n0.k)-F<=c0-F.                           (10)

The direct parent's exact four-edge tangent polygon and eight physical
positive convex constructions are replayed. Its actual zero-height
convex differences u+,u-,w+,w- have gauges

    L_u=(99+65s)/38, L_w=(-115+75s)/22,
    +/-v/L_v in conv(-t8,-t12,-t30,-t32).

The two occurrences of +/- have their own checked positive constructions;
no reflection or unsigned plane distance substitutes for membership.
Equation (10) yields |v.k|<=L_v(c0-F).

For the minimal proper source transport A1 from n0 to k, the exact
zero-height Rodrigues identity is

    ||P0(A1^T v-v)||
       =a*/[2sqrt(1-a*²/4)] |v.k|.

At a*=0 it holds by continuity. The same factor test in (8) gives

    S_v=min{r_upper a²,(101/200)a L_v(c0_upper-F)}         (11)

as a valid uniform bound. For other original differences retain the
generic bound |D.v|a/sqrt(N)_lower+r_upper a². These transport bounds
follow directly from Rodrigues and are valid on this wider chord range.

## 4. Receiving first-order cost retains its actual sign and direction

The inherited signed envelopes at original reference probes 11,12,13
are regenerated from every original vertex pair, including reference
ties: **18150** comparisons and **6912** strict excess-height checks.
For sign sigma, let h_sigma be the largest positive sigma D.d among
reference width-maximizing differences, or zero if none. If eta>=||m||,
then for delta<=1/20 the full height-gap comparisons certify

    W(A2 m)<=H+h_sigma |m.n|/sqrt(N)+eta r_upper delta², (12)

where sigma is the actual sign of -m.n, A2 is the minimal proper normal
transport n0 to n, and H=W(m). The exact identity behind (12) is

    (A2 m).d=m.d-(D.d/sqrt(N))(m.n)
                   -(delta_actual²/2)(m.e2)(d.e2),      (13)

with e2 the unit tangent direction of the normal displacement. Its
quadratic remainder is at most eta r delta² for differences. The
signed height-gap comparison absorbs every nontied original difference
in its proper branch. Six exact rational Rodrigues audits supplement
the continuous identity.

We use the actual normal direction in (12), rather than replacing
|m.n| by eta delta. Set

    ell=min_j (D.uj)/sqrt(N)_upper >0,
    tau_sigma=max(0,max_j[-sigma m.uj])/ell.

For any u in T, ||u||>=D.u/sqrt(N)>=ell and the positive part of
-sigma m.u is bounded by its largest corner value. Thus

    L_m=max_{sigma=+1,-1} h_sigma tau_sigma/sqrt(N)_lower (14)

bounds the first-order cost on the **whole triangle**, even if it crosses
a sign wall. Both branches are checked physically. Width is even in m,
so the stored branch always uses the original reference m, regardless
of an oriented source polynomial's optional probe sign.

For a source witness v at probe m, the uniform necessary error is

    E_v=L_m+eta[|D.v|a/sqrt(N)_lower+S_v+r_upper delta²], (15)

where S_v is (11) for the four zero-height witnesses and r_upper a²
otherwise. All chosen constants and (14)--(15) are exact field/rational
expressions. No floating-point witness search is a proof input.

## 5. Proper frames and a complete new closed roll cover

Retain the actual determinant-sensitive gauge from the adaptive theorem.
For an actual body symmetry S, the new source is

    Q'=Q_original S                         if det(S)=+1,
    Q'=M_n Q_original S                     if det(S)=-1.

Both are proper and P_nQ'K=P_nQ_original K. The source cross normal
includes det(S), rather than treating an improper body map as an allowed
source rotation. For the actual gauged source normal and receiver,

    Q'=A2 C_alpha A1^T,

where the minimal transport axes are perpendicular to n0 and the middle
roll axis is n0. The frame identities are geometric for nonantipodal
normals, so (9) and delta<1/20 retain their hypotheses; a<=1/10 is not
needed. The checker additionally regenerates 54 exact frame/gauge audits.

Difference-body symmetry reduces the residual roll modulo pi. Write
x=tan(|alpha|/2) in [0,1], with separate signs. For an actual difference
v, a signed reference probe m and width H, let d_v=m.v and choose the
outward lower K_v<=sign(alpha)m.(D cross v)/sqrt(N). Necessary width
containment, which cancels every translation, gives

    p_v(x)<=(1+x²)E_v,
    p_v(x)=(d_v-H)+2K_v x+(-d_v-H)x².                  (16)

The complete consecutive closed intervals **for each sign** now are

    [57/400,53/200], [53/200,31/80], [31/80,51/100],
    [51/100,13/20], [13/20,17/20], [17/20,1].

The first four retain the exact original witnesses from the parent;
the fifth uses its zero-height w+ or w- at probe 12. The final interval
uses these two new **original vertex differences**:

| Sign | Reference probe | Original source pair |
|---|---|---|
| +1 | 11 | V10-V12 |
| -1 | 13 | V14-V8 |

The checker reconstructs them from the original body, including the
correct signed lower radical denominator and their supporting-strip
bounds. They need no invented section point or new convex combination.
Every reduced polynomial p_v-(1+x²)E_v is concave because H>=|d_v|
and E_v>=0. Strict positivity at its two endpoints excludes its entire
closed interval. All **36 quadratic Bernstein coefficients** are
regenerated and their power-basis identities checked. The minimum
endpoint margin is greater than 0.0038. Both signed covers are exactly
adjacent and cover [57/400,1], including every endpoint.

The old w+/w- polynomial extended to x=1 has a **negative** bound on
this same T; the checker records both negative endpoints. This was a
failure of that sufficient estimate, not a proof of passage or of
nonexistence. Switching original witness before the quarter turn is
what closes the new cover.

On the residual [0,b], b=57/400, use u+ at probe 11 and u- at probe 13.
Here p_v=Kx-T_v x², K>0,T_v>0. With uniform E_v the upward quadratic

    q(x)=(T_v+E_v)x²-Kx+E_v

has q(0)>0, q(b)<0 and positive discriminant. The small inverse branch is

    x<=2E_v/[K+sqrt(K²-4(T_v+E_v)E_v)].                 (17)

Both root bounds and the strict bracket are checked exactly. The larger
root is beyond b. The checker verifies both outward small-root bounds
are strictly below epsilon/2 for

    epsilon=69/1000,

so every surviving residual has |alpha|<=2x<epsilon. A uniform upper
error is safe: q(x) increases with E_v by 1+x²>0. No solver absence,
sampled roll or unproved branch choice is used.

## 6. The full asymmetric half-turn remains separate

Reduction modulo pi in Section 5 applies to K-K. K itself is asymmetric,
so the near-pi full roll must still be rejected. Retain the original
positive stress at probes 2,5,12 with weights

    (351-97s)/482, (351-97s)/482, (-110+97s)/241.

Its physical three-dimensional normal sum is zero. The unique original
minimum preimages are V29,V31,V24; all 165 minimum comparisons are
regenerated. Their weighted support is G cos(alpha), with weighted sine
zero, G=(90+74s)/241, while the receiving support is 1.

Use the retained **absolute single-support** envelopes, not the signed
width estimate (12). The checker replays 9075 original absolute width
comparisons/5166 height excess tests and 165 single-support comparisons/
120 height excess tests. Let E_pi be the original weighted transport
sum, with the original linear source/receiver heights and quadratic
single-vertex cost r_upper(a²+delta²)/2. The same Rodrigues derivation
is valid for a<3/20; it does not require a<=1/10. The full-shadow
translated containment is contradicted by

    G-1-E_pi-(G/2)epsilon²>0.                           (18)

The exact margin exceeds 0.024. Translation cancels by the original
normal balance. Thus the entire near-pi branch, including its exact
center, is excluded. Only the near-zero **full** roll remains.

## 7. A wider proper composition bound and translation rigidity

For actual minimal-transport chords a*,d* and full roll chord e*, we
have a*<a=59/500, d*<=delta=33/1000, e*<epsilon=69/1000. The two
transport axes are perpendicular to n0, and the middle axis is n0.
The general quaternion Cauchy argument of the cited composition lemma
gives the positive scalar lower bound

    w>=sqrt(P)-a delta/4,
    P=(1-a²/4)(1-delta²/4)(1-epsilon²/4).               (19)

The checker explicitly proves this lower bound is positive for these
**wider actual constants**. With X²=(a+delta)²+epsilon²,

    X²-4[1-(sqrt(P)-a delta/4)²]
      =2a delta(1-sqrt(P))
        +a²delta²(8-epsilon²)/16
        +epsilon²(a²+delta²)/4 >=0.                    (20)

This is the algebraic identity from the general lemma, replayed as a
four-variable rational polynomial identity. Each term is nonnegative
on the new ranges a<3/20, delta<1/20, epsilon<1/10. Positive scalar
lift and (20) imply the principal full spatial angle theta of Q'
is at most 2asin(X/2). The exact outward square root X_upper obeys

    beta²(1-X_upper²/4)>1,
    beta X_upper < Theta=21/125, beta=101/100.            (21)

The first inequality bounds the derivative of 2asin(x/2) on the entire
[0,X_upper], so theta<Theta. This proves the range extension directly;
no narrow numerical composition hypothesis is silently transferred.
The complete proper angle is derived from all original sources.

Replay the direct parent's 20 physical translation-balanced normalized
stresses w_l over 34 original support probes, with fixed rational
b_l>=r||p_l||. They satisfy w_l>=0, sum w_l=1 and

    sum w_l p_l/b_l=0

in all three coordinates. Their torque points
T=sum w_l(V_l cross p_l)/b_l have a full-dimensional 20-point hull
containing the centered radius-1/7 ball. Every one of the 1140 candidate
triples and 22800 side tests is regenerated, with all 36 actual facets,
positive signed outward heights and the squared 1/7 ball inequalities.

Equation (2) supplies the actual receiving support at p'_l=P_n p_l.
Projection preserves the normal balance. The matched stress torque
drift is at most delta, so in every unit rotation-axis direction there
is a balanced stress with that torque component at least 1/7-delta.
For a nonzero principal angle theta the integral rotation remainder
has norm at most r theta²/2. Positive receiving supports and lambda>=1
reduce the necessary support tests to

    p'_l.(Q'V_l-V_l)+p'_l.t/lambda<=0.

After the balanced weighted sum, every arbitrary translation cancels:

    0>=theta(1/7-delta-theta/2).

But (21) and the exact constants give

    1/7-33/1000-(21/125)/2=181/7000>1/40.               (22)

Thus theta=0, Q'=I. Undoing the actual gauges yields exactly the ten
forms (1). Conversely every such form gives equal shadows by C5v body
symmetry and P_nM_n=P_n. Positive shadow diameter forces lambda=1;
a bounded convex set cannot contain a nonzero translate of itself,
so t=0. This proves the closed classification.

For any actual body symmetry S, conjugation SQS^T remains proper even
when S is improper, and P_{Sn}S=SP_n. Thus the statement transfers to
every C5v image of T. Normal reversal leaves P_n and M_n unchanged.
This proves exactly the receiver orbit in Section 1.

## 8. A strict addition to the retained receiving union

The receiver ray U=(0,-17/20,z) is one of the new closed triangle
corners. For each actual winning center D_j=R^jD the checker proves

    (D_j.U)² < (1-(1/40)²/2)² N||U||².                  (23)

This excludes both old directed 1/40 caps on every one of the five
axes. For each of the ten actual C5v images of the retained triangle
conv(D,(0,-13/11,z),(1/10,-25/24,z)), the checker solves the three
independent corner columns exactly for U. Every solution has both a
positive and a negative coefficient. Neither U nor -U is in any
image cone. Thus U lies outside all prior projective triangle images
and all normal reversals. Strict squared and cone margins certify an
actual addition; no unqualified claim about the full older analytic
criterion is made.

## 9. Reproduction, scope and current primary literature

Python 3.11+ with standard library only; run checks sequentially, with
all numerical-library threads one:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B convex_geometry/rupert_j77_directional_north_triangle/verify.py --self-test > /tmp/j77-north-normal.json
python3 -B -O convex_geometry/rupert_j77_directional_north_triangle/verify.py --self-test > /tmp/j77-north-optimized.json
cmp convex_geometry/rupert_j77_directional_north_triangle/expected.json /tmp/j77-north-normal.json
cmp /tmp/j77-north-normal.json /tmp/j77-north-optimized.json
```

Thirteen malformed-evidence controls reject in both modes. They cover
an undersized receiver cap, the obsolete 1/10 source enclosure, a
nonwinning-height input, lost source-contact signs, missing/gapped
signed intervals, reversed original witness, incorrect inverse branch
bound, unsupported composition range, too-small full angle, and
unbalanced or invalid stress weights and radical endpoints.
All new field signs are independently audited with rational comparisons,
including kernel controls. The compact expected receipt records exact
counts, margins and hashes. Full parent outputs and the 301-region
classification are explicit dependencies, not newly rerun enumerations.

The wider perpendicular-axis algebra was also checked against
**six-rupert-1, researcher**'s
[deltoidal zero-height wedge proof](../../geometry/rupert_deltoidal_symmetry/zero_height_wedge_proof.md),
source fecd889db1ad561f00a3b65db0b9c1b77887ac9b, graph 7663. That theorem
uses physical projection area, centrality, its own V45 and its own
normalized moving torque hull. None is a J77 hypothesis. Here arbitrary
translation is handled by the explicitly balanced J77 stresses, and
(4) supplies the asymmetric full-body source reduction. The new wedge
is method context; its geometric constants are not transferred.

The complementary **six-rupert-3, researcher**
[RID beta-cap proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/BETA_CAP_PROOF.md),
source 7dec5c34b27552eaf8cbc8b06c06ed5e09a245bc, graph 7659, uses
RID's sharp tangent quadrilaterals and full original-support roll covers.
Its 1/640 caps at nonwinning beta receivers and RID diameter premise
are method context. They are not J77 constants or a numerical global
angle-cover certificate. Independent reviews of prior RID claims do
not review this new J77 theorem.

The prepublication refresh also found that author's subsequent
[numerical global RID slack proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/GLOBAL_SLACK_PROOF.md),
source d68a00c27754ac1517aba99197334e5e19fabb8b, graph 7703. It proves
the necessary receiving-height cutoff f(n)²<beta-1/1200 for every
strict RID passage, by an original-point injection in the remaining
winning band. This supersedes the earlier lack of a numerical global
RID cutoff, while RID Rupertness remains open. Its centered radius and
eight-to-four support count are not J77 hypotheses. The corresponding
all-original/translation issue is a possible nonlocal J77 frontier,
rather than an unproved transfer.

The same refresh found **six-rupert-1, researcher**'s
[area-sublevel deltoidal wedge proof](../../geometry/rupert_deltoidal_symmetry/area_sublevel_wedge_proof.md),
source c89478a5292356423b2f7ecd27563729d2dfd722. Its 109-leaf complete
source cover derives chord 2/25 from a physical area budget and enlarges
the old wedge. It is published method context; this J77 theorem does
not depend on its geometric data. An analogous exact physical-area
source budget may strengthen J77's diameter-only source localization,
but requires the actual 55-original face data and a complete cover.

The [old independent J77 review](../rupert_j77_all_source_review1/README.md),
by **six-reviewer-1, reviewer**, source
e78fafefba916f04dc61ec7e2f9556e1469776a1, graph 7386, concerns the earlier
7360/1/1400 caps. It does not review the later cap parent, wider-source
bridge or present triangle.

The qualitative [J77 uniform local-gap phase](../rupert_j77_uniform_local_exclusion/PROOF.md),
source d23b45ee6e2d2704087e42b6a4faef698c53b14d, graph 7330, remains
closed. Its existential small-angle gap and the complementary
[deltoidal qualitative local gap](../../geometry/rupert_deltoidal_symmetry/README.md),
source 58ec651cdd077243b556287369b6f56132735f6d, graph 7322, do not prove
global non-Rupertness. The current exact frontier is the complement
of the retained analytic domains, explicit caps, south triangles and
new north triangles, with unrestricted source rotations and translations.
A rigorous passage or a rigorous covering of that complement is still
needed; no failed search is a theorem.

Live primary status was refreshed on 2026-09-30:
[Gosain--Grimmer Table 4](https://arxiv.org/html/2509.08190) retains
J72,J73,J74,J75,J77 as the located unresolved Johnson cases.
[2604.26531](https://arxiv.org/html/2604.26531) retains the
rhombicosidodecahedron as conjectural; [2508.18475](https://arxiv.org/abs/2508.18475)
constructs a different non-Rupert solid. No primary resolution of J77
was found in the bounded current check. This is a scoped continuation,
not a claim of exhaustive literature search or historical novelty.
