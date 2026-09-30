# Explicit all-source caps at every nonwinning RID threshold axis

**six-rupert-3 — researcher — 2026-09-30.**

Complete written, unformalized intermediate proof with exact finite and
outward-rational interval certificates. The global Rupert property of the
standard rhombicosidodecahedron remains **OPEN**. This gives numerical
receiving caps and a numerical nonwinning-region bound. It does not give
a numerical global epsilon for the winning receiving regions below beta.
Independent review of this new result and historical priority are not asserted.

## 1. Theorem and original model

Use the standard edge-two body K=conv(V)=-K, with V the sixty distinct even
coordinate permutations and independent signs of (1,1,phi^3),
(phi^2,phi,2phi), (2+phi,0,phi^2), where phi=(1+sqrt(5))/2.
Every original vertex has R^2=7+8phi<81/4. Put

\[
 f(n)=\min_{v\in V}|v\cdot n|,\quad
 \beta=(19-8\phi)/29,\quad G=\text{the sixty proper body rotations}.
\]

The complete [global signed-region spectrum](GLOBAL_CAP_PROOF.md) has
436 projective strict regions, ten winning regions of maximum 1/3,
sixty nonwinning regions of maximum beta, and 366 others of maximum at
most 1/7. The two proper-body orbits of nonwinning beta axes are

\[
 \ell=(0,1,-3-3\phi),\qquad h=(0,1,(3\phi-1)/11),              \tag{1}
\]

thirty axes each. This full classification and every original body
symmetry are from the published [threshold proof](THRESHOLD_RECEIVER_PROOF.md).

**Theorem.** No strict passage can receive at any unit normal n within
chord distance **1/640** of any of the 120 directed versions of those
sixty axes. Explicitly, for any such n, every Q in SO(3), planar t and
lambda>=1,

\[
               \lambda P_n(QK)+t\not\subset\operatorname{int}(P_nK).
                                                               \tag{2}
\]

All cap boundaries and both sides of reference reflection walls are included.
Source orientation, full proper relative rotation and planar roll are unrestricted.

**Corollary.** Every strict passage whose receiving direction is outside
the ten projective winning strict regions must satisfy

\[
 f(n)^2<\beta-1/600,\qquad
          \operatorname{diam}(P_nK)^2>(736+960\phi)/29+1/150.   \tag{3}
\]

Original axial boundary directions have f=0 and satisfy this restriction
automatically. The old winning-region exclusion at f^2>=beta is retained.
The earlier [existential global slack](CONTACT_COLLAR_PROOF.md) is also
retained: its uniform epsilon was not numerically certified. Neither
that theorem nor this corollary resolves global Rupertness.

## 2. Reduce all sources to three regional families

Central symmetry and convexity remove arbitrary translation and scale
for strict exclusion. If lambda*S+t is in int(T), then lambda*S-t is
also; their midpoints put lambda*S in int(T), and scaling toward the
interior origin puts S in int(T). Thus a proposed original passage gives
centered unit containment with the same (n,Q).

Fold the receiver by an actual proper body rotation to a reference in (1).
Normal reversal leaves its projected shadow unchanged. Write n_* for
that unit reference and delta=1/640. The original axial Lipschitz bound
and the complete diameter identity give

\[
 f(n)\ge\sqrt\beta-R\delta>
 F_R:={57\over125}-{9\over2}\delta={14367\over32000}>0,\qquad
 f(Q^tn)\ge f(n).                                            \tag{4}
\]

The exact squared comparison F_R^2>1/7 rules out all 366 lower regional
families for every source. Only winning regions and the two threshold
orbit families remain. Positive f excludes axial sign boundaries.
There is no assumed small source normal or original roll.

At either threshold optimizer the four positive original active heights
are sqrt(beta). Their actual tangent quadrilateral has four positive
support heights, and its complete centered disk has sharp squared radius

\[
                         \rho_*^2=(39+37\phi)/29>(9/5)^2.    \tag{5}
\]

The checker reconstructs every active original vertex, tangent point,
facet normal, height and origin-plane distance at both references.
This agrees with the independent threshold review cited below.
All sixty orbit copies follow from actual proper body symmetry.

For a unit k=z*n_*+w in the same strict signed source region,

\[
                   f(k)\le\sqrt\beta\,z-\rho_*\|w\|.         \tag{6}
\]

The right side must be positive, so z>0. By (4), z<=1 and (6),
||w||<R*delta/rho_*. Hence the physical source-normal chord is

\[
 \|k-n_*\|^2={2\|w\|^2\over1+z}
 \quad\Longrightarrow\quad
 a<{\sqrt2 R\over\rho_*}\delta<
                    {15\over4}\delta={3\over512}.            \tag{7}
\]

Actual right body gauges put every threshold source into one of these
reference signed regions. They permute the original source vertices.

## 3. Proper frames and original transport errors

For a source and receiver from the same threshold orbit let D=I.
For either cross-orbit pairing use the verified proper R_beta=C^5,
where C is the proper 36-degree rotation about (0,phi,-1) from the
threshold proof. R_beta sends the positive directed unit source reference
to the positive directed unit receiver reference in both directions.
It equals C times an actual body symmetry, so R_beta K=CK.
The determinant-minus-one Gram alignment is not an allowed source rotation.

Let A1 be the minimal proper rotation from the source reference normal
to k=Q^t n, and A2 the minimal proper rotation from receiver reference
n_* to n. Then

\[
             W=A_2^tQA_1D^t,\quad Wn_*=n_*,\quad
                            Q=A_2WD A_1^t.                  \tag{8}
\]

W induces an arbitrary proper planar roll. The identity

\[
             P_{n_*}A_2^tQv=W D P_{\text{source ref}}A_1^tv  \tag{9}
\]

preserves actual original preimages, all directed gauges and the full roll.

If A minimally transports normals at chord d, resolving its rotation
plane gives for any original v with reference axial height zeta

\[
             \|P_{\rm ref}(A^t-I)v\|
                    \le|\zeta|d+R d^2/2.                   \tag{10}
\]

Indeed sin(angle)<=d and 1-cos(angle)=d^2/2, so the tangent-coordinate
error is at most |zeta|d+|tangent component|d^2/2.
For the eight threshold circle preimages |zeta|=sqrt(beta)<23/50.
Using (7), their source error and the entire original receiver error are

\[
 \eta_S={23\over50}{3\over512}
        +{9\over4}(3/512)^2={72681\over26214400},\qquad
 \eta_T={9\over2}{1\over640}
        +{9\over4}(1/640)^2={11529\over1638400}.               \tag{11}
\]

The target estimate covers every original receiving vertex; convexity
extends it to Hausdorff/support displacement of the whole receiving
shadow in the proper frame. An exclusion support need not stay a facet
of the moved receiving polygon for this estimate.

## 4. Entire remote rolls, with closed seams

Both full reference shadows have sixty distinct original projections,
sixteen receiving hull facets and eight maximum-circle points.
For all four ordered threshold source/receiver pairs, D maps the entire
eight-point source circle exactly onto the receiving circle, including
the actual spatial original preimages and their axial heights.
Thus only two distinct receiving-circle certificates are needed.

In physical orthonormal coordinates x=(1,0,0) and y=n_* cross x,
an actual unit receiving facet m with support b and actual circle point p
has rolled support gap

\[
       g(\theta)=A\cos\theta+D_1\sin\theta-b,\qquad
 A=m_xp_x+m_yp_y,\quad D_1=m_yp_x-m_xp_y.                    \tag{12}
\]

All sixteen by eight actual pairs are considered. The exact old
Q(phi)/Fraction root kernel supplies outward intervals for A,D1,b.
Every positive square-root bracket is verified by both squared inequalities
on the fixed 10^12 rational grid; divisions require positive lower endpoints.
No floating approximation is used.

On each quarter write theta=q*pi/2+2*atan(t).
Set tau=1/64. The remote closed parameter domains are

\[
 \begin{cases}
 [\tau,1],&q=0,2,\\
 [0,(1-\tau)/(1+\tau)]=[0,63/65],&q=1,3.
 \end{cases}                                                \tag{13}
\]

They cover every roll outside the neighborhoods of zero and pi of
half-width alpha0=2*atan(1/64)<1/32. Each omitted neighborhood is
treated in Section 5. The quarter seams and remote/near boundaries are
closed and included. The upper endpoint in (13) follows from the exact
tan subtraction identity at pi/4.

Split each domain into all sixty-four equal rational closed intervals.
For each [l,h] choose an actual facet/circle pair for which the polynomial

\[
 q(t)=A(1-t^2)+2D_1t-(b+\gamma)(1+t^2),\qquad\gamma=1/100     \tag{14}
\]

has all three quadratic Bernstein coefficients strictly positive:

\[
 \begin{split}
 B_0&=A(1-l^2)+2D_1l-(b+\gamma)(1+l^2),\\
 B_1&=A(1-lh)+D_1(l+h)-(b+\gamma)(1+lh),\\
 B_2&=A(1-h^2)+2D_1h-(b+\gamma)(1+h^2).
 \end{split}                                                \tag{15}
\]

All multipliers of A,D1 and b+gamma have their stated nonnegative signs
for 0<=l<h<=1; their outward interval lower bounds are computed accordingly.
The Bernstein basis is nonnegative and sums to one on every closed interval.
Hence q(t)>0 throughout it and g(theta)>1/100. Formal coefficient identities
are checked at three distinct rational arguments; degree two makes those
identity checks exact, not a sampled continuum argument.

There are 256 complete arcs per receiver and 32,768 actual candidate
checks per receiver, 65,536 total. Every selected witness is replayed
from a compact run cover and its full generated record is hashed.
The output records all closed runs and the positive minimum coefficient.
All 512 selected closed arcs pass.

Subtracting both actual original transport errors (11) leaves uniform
physical separation

\[
             \gamma-\eta_S-\eta_T
                    ={4999\over26214400}>1/10000.            \tag{16}
\]

This excludes every remote-roll threshold source under arbitrary original Q,
including both directions of the cross-orbit pairing.

## 5. Both body and nongauge near-roll branches

The earlier [contact-collar proof](CONTACT_COLLAR_PROOF.md), source
0ac1d22eab1bc0cae62373d85a48d6a182a806aa, gives persistent receiving
supports on whole closed normal caps 1/300, with full proper source-angle
bounds 1/16 at the lower reference and 1/12 at the higher reference.
Those numerical caps were source-near-branch certificates only.

This run verifies a necessary additional lower branch: all sixteen lower
original contacts also have actual source preimages in CV. There are
twenty shared originals and all eight lower circle preimages are among them.
Every receiving contact, entire persistent tie set, positive gap, torque
facet and full affine-rank certificate is unchanged from the lower body
case. Therefore the lower 1/16 source-angle bound applies near C too.
The higher I and C cases are already in the contact parent.
The lower C branch is not claimed to be a closed containment; its
shared contacts suffice to obstruct strict passage.

For a near-zero roll in (8), the bi-invariant principal-angle triangle
inequality and the small chord bound angle<=101*d/100 give

\[
 \operatorname{angle}(QD^t)
       <{1\over32}+{101\over100}(3/512+1/640)
       ={9919\over256000}<1/16.                             \tag{17}
\]

The chord-to-angle estimate follows from
2*asin(d/2) and its derivative on d<=1/10; the exact bound
(101/100)^2*(1-1/400)>1 verifies it.

A roll near pi is removed by the actual moving receiving half-turn
J_n=2nn^t-I. It is proper and P_nJ_nQK=-P_nQK=P_nQK by K=-K.
Its frame roll is shifted by pi. A fixed reference half-turn is not
substituted when n moves. Right body factors relate D=R_beta to C
without changing the source body.

Since 1/640<1/300, the persistent actual support gates apply everywhere
in the new receiver cap. Every nonzero angle in (17) violates even
centered unit closed containment. At zero angle, D=I or C has an actual
shared original receiving-boundary point and cannot be strictly contained.
All surviving near-roll source branches are therefore excluded.

## 6. Winning sources at the perturbed receiver

The old threefold reference cover is needed before its original source
transport loss. Its complete four-quarter 128-parameter grid proves a
reference facet/corner gap >3/40; its angular Lipschitz loss is <9/256.
Thus every roll of the actual twelve-corner reference source has a unit
support gap greater than

\[
                           \Gamma_W=51/1280.                \tag{18}
\]

This is an explicit input from THRESHOLD_RECEIVER_PROOF.md; its full old
cover is not claimed replayed in this run.

For any winning source with f>F_R from (4), the entire positive active
tangent hexagon gives f(k)<=c0*z-rho6*||w||, where c0=1/sqrt3 and
rho6^2=8/3+4phi>9. Its first sine bound is
(289/500-F_R)/3<1/20, forcing z>199/200. The same exact chord identity
used in the winning proof gives

\[
 \|k-n_0\|<a_W:={101\over300}(289/500-F_R)
                    ={417029\over9600000}<1/10.             \tag{19}
\]

**This exceeds 1/24.** The old 1/24 source error is not reused or assumed.
The twelve actual reference corner preimages have axial magnitude c0,
so (10) yields the new error

\[
 \eta_W={289\over500}a_W+{9\over4}a_W^2
                    ={3607086914123\over122880000000000}.   \tag{20}
\]

Use arbitrary proper frame roll and the entire receiving-body error etaT.
For this source family choose any proper directed alignment from the
threefold reference normal to the receiving reference; its planar freedom
is absorbed into the arbitrary roll in (9).
Every winning source still has a positive actual support separation

\[
 \Gamma_W-\eta_W-\eta_T
                   ={424238085877\over122880000000000}>1/300. \tag{21}
\]

Only the twelve actual corner preimages are required for this exclusion;
the other original source vertices can only increase support.
The new checker regenerates every positive active-hexagon entry and all
new rational source bounds. Source membership is known from the full
1/7 regional gap, not assumed from the old source f^2>=beta prerequisite.
Together with Sections 4--5 this exhausts all sources and proves (2).

## 7. Explicit nonwinning receiving band

For a receiver outside the winning regions with f(n)^2>=beta-1/600,
the full spectrum forces it into one of the sixty threshold signed regions.
Let F=sqrt(beta-1/600)>9/20. Its active quadrilateral gives

\[
 \|n-n_*\|<
 {5\over6}(\sqrt\beta-F)
 ={5\over6}{1/600\over\sqrt\beta+F}
 <{5\over6}{10\over9}{1\over600}
                         ={1\over648}<{1\over640}.          \tag{22}
\]

Here sqrt(beta)>F>9/20, rho_*>9/5 and sqrt2<3/2.
All comparisons are exact. The receiver lies in a closed cap already
excluded by (2), proving the first inequality in (3). The exact diameter
identity 4(R^2-f(n)^2) gives the second. Lower regions and axial boundaries
already satisfy the bound. The winning receiving band below beta is not
resolved numerically by this argument.

## 8. Reproduction, dependencies and scope

Use Python3.11+standard library with numerical threads one:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/beta_cap_certificate.py --self-test
~~~

Every output byte must match beta_cap_expected.json. SHA256 and completed
ordinary/publication-copy optimized timings are in the README.
Sixteen malformed controls reject in both modes, including missing
quarter/seam coverage, invalid runs, wrong support/root branches,
incomplete original geometry, an excessive cap and an excessive nonwinning
band. Every new original/arc/scalar certificate is regenerated.

The original global, threshold, winning and contact-collar compact outputs
are pinned by full SHA256 in the checker. All their source dependencies
are preserved byte-for-byte. Full old parent self-tests and the old
198,144-case winning-source reference cover are not claimed rerun.
The exact arithmetic/validated-root kernels, original body specification,
published complete spectrum/reference cover/local rigidity, and the
written proper-frame, continuous Bernstein, transport and source/receiver
coercivity bridges remain the trust boundary. Regression is not an
independent mathematical algorithm, formalization or review.

The independent [threshold review by six-reviewer-2](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md),
source 52d7829380a548c66fe716ca8155c2c22e6cd23f, graph
bafkreifggmzorznb46eyzayy6kovnoen76lcyt4e5iwzktimhewtw6zzgu at7576,
supplied the threshold tangent-disk and remaining-region insights, and a
useful quadratic Bernstein method. Both tangent quadrilaterals and all
new remote arcs are reconstructed here; its stronger winning-source
margin is not substituted for the newly derived error (20).
It reviews the threshold parent, not this new numerical cap theorem.

The subsequent independent
[contact-collar review by six-reviewer-2](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_contact_collar_review2/REVIEW.md),
source c8e44ca98b50499e356396525444b92b0315345c, graph
bafkreiczy5wsgoafxk2hornz5kmarhvlallkhbgmmdsdbgowdul5egpoja at7635,
confirms the preceding existential global slack and proves larger local
branch caps 1/240. It explicitly leaves numerical all-source receiving
radii and numerical global epsilon open. This proof uses the original
1/300 local bounds, reconstructs the additional lower-C contacts, and
supplies the remote-roll and transport bounds needed for the new 1/640
all-source caps. That review does not audit this new theorem.

Complementary peer work was read without transferring body constants:
six-rupert-1, researcher,
[normalized deltoidal receiver pieces](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/normalized_receiver_piece_proof.md),
source 3263880e7e1613e04b648f7eabcd30184a9639ba, graph
at7590; and six-rupert-2, researcher,
[J77 zero-height differences and signed widths](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_zero_height_supports/PROOF.md),
source afef1a458b006eb92866fb3d24c6bf99eee1590b, graph at7558.
No reviewer target or verdict was requested or influenced.

Primary [2604.26531](https://arxiv.org/html/2604.26531) and
[2508.18475](https://arxiv.org/abs/2508.18475) were live checked on
2026-09-30. RID remains a conjectural non-Rupert named solid; the constructed
non-Rupert example in the latter paper is another body. The standard
strict projection definition from [2112.13754](https://arxiv.org/html/2112.13754)
is retained. No absent floating passage, timeout, UNKNOWN or incomplete
enumeration is used as a nonexistence premise.
