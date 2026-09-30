# A numerical global receiving-height gap for the rhombicosidodecahedron

**six-rupert-3 — researcher — 2026-09-30.**

Complete written, unformalized intermediate proof with exact finite
certificates. The global Rupert property remains **OPEN**. This gives
a numerical necessary condition for every strict passage, rather than
an exclusion of the entire receiving sphere. Independent review of this
new theorem and historical priority are not asserted.

## 1. Model, theorem and published inputs

Let phi=(1+sqrt5)/2 and let V consist of the sixty distinct signed even
coordinate permutations of (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).
Put K=conv(V)=-K, R^2=7+8phi, f(n)=min_v |v.n| for unit n and
beta=(19-8phi)/29. Every original vertex lies on the radius-R sphere.
The standard projection is P_n=I-nn^t.

**Theorem.** For every unit receiving normal n, every original proper
Q in SO(3), every planar translation t and every lambda>=1,

\[
 \lambda P_n(QK)+t\subset\operatorname{int}(P_nK)
 \quad\Longrightarrow\quad
 f(n)^2<\beta-\frac1{1200}.
 \tag{1}
\]

Equivalently, every strict passage requires

\[
 \operatorname{diam}(P_nK)^2>
              \frac{736+960\phi}{29}+\frac1{300}.
 \tag{2}
\]

The published [global spectrum](GLOBAL_CAP_PROOF.md) has 436 projective
strict signed regions: ten winning regions of maximum 1/3, sixty
threshold regions of maximum beta, and 366 others of maximum at most 1/7.
Its complete diameter identity is
diam(P_nK)^2=4(R^2-f(n)^2).
The [all-threshold proof](THRESHOLD_RECEIVER_PROOF.md) excludes every
strict receiver with f^2>=beta, including its complete closed boundary.
The [numerical beta-axis cap proof](BETA_CAP_PROOF.md), source
7dec5c34b27552eaf8cbc8b06c06ed5e09a245bc, graph
bafkreigcldw6lg5qliffah5wembwguuoawjyohyehdubadbt4xdsfia5xe at7659,
already excludes every nonwinning receiver with f^2>=beta-1/600.
The [contact-collar proof](CONTACT_COLLAR_PROOF.md) previously gave a
positive global epsilon by compactness without computing it.

These are explicit inherited mathematical conclusions. The new work
closes the winning receiving band by a uniform winning-source argument
and an original-point injection for threshold sources. It does not use
compactness or a floating passage search.

## 2. Center strict placements and reduce every source

For centrally symmetric source and receiving shadows, a strict inclusion
lambda*S+t in int(T) also holds with -t. Convex midpoints give
lambda*S in int(T); scaling toward the interior origin gives
S in int(T). Thus centered unit containment is a necessary condition.
All remaining exclusions use that condition with the original n,Q.

Assume f(n)^2>=beta-epsilon, epsilon=1/1200. The exact guards prove

\[
 \beta-\epsilon>q^2>1/7,\qquad q=57/125,\qquad
                 \sqrt{\beta-\epsilon}>9/20.
 \tag{3}
\]

Diameter monotonicity forces the source normal k=Q^t n to satisfy
f(k)>=f(n). The complete regional barrier therefore leaves only winning
and threshold source regions. Positive f excludes every original axial
boundary.

Nonwinning receivers are excluded by epsilon<1/600 and the published
nonwinning band. Receivers with f^2>=beta are already excluded.
We need only consider a winning receiver with

\[
                 \beta-\epsilon\le f(n)^2\le\beta.
 \tag{4}
\]

Actual proper body rotations and normal reversal give the standard
winning center n0=B/||B||, B=(0,phi^-2,1). Reversal leaves the shadow
unchanged; wall reflections are represented by their negatives as
proper body rotations and reversal. No improper matrix is allowed as Q.

## 3. Every winning-to-winning source pairing for f>q

The full positive original active hexagon at n0 has six tangents p_i
with centered disk squared radius 8/3+4phi>9. For any normal in its
winning signed region, write n=z*n0+w, w perpendicular n0. Then

\[
 f(n)\le c_0z-\rho_6\|w\|,\qquad c_0=1/\sqrt3,\quad \rho_6>3.
 \tag{5}
\]

Since f>q, this forces z>0, ||w||<(289/500-q)/3<1/20,
z>199/200 and the unit-normal chord<1/24. This applies separately
to the actual winning receiver and to every winning source.
The full six originals, tangents and sharp disk are regenerated.

Audit [WINNING_RECEIVER_PROOF.md](WINNING_RECEIVER_PROOF.md) Sections2--5
and [BALANCED_SUPPORT_PROOF.md](BALANCED_SUPPORT_PROOF.md) Sections2--5.
Their use of f^2>=beta before the geometric gates supplied winning
region membership and f>q. Both facts are established directly here.
All subsequent source transport, receiver folding, cut and torque
hypotheses use those facts and the chords<1/24.

In particular the entire receiving tail folds into the old closed
outer cut triangle U defined by the actual original v*=(-1,phi^3,-1)
and v*.u>=q. Its chart norm is<27/25. The complete published torque
certificate on U has raw centered ball at least1/2, with all840strata
covered. All original support inequalities on the three U corners
are regenerated here:1800comparisons. The840strata are inherited.

For arbitrary original proper Q, the actual six axial shadow gauges
reduce the entire roll, using proper body factors and the moving
receiving half-turn J_n=2nn^t-I. The C3 support average cancels the
first-order source tilt for every tangent and both roll signs.
The complete remote-roll gate and perpendicular-axis proper-frame
bound give, with d=1/24,

\[
 E<\frac{(13/15)d+(3/2)d^2+(17/16)d^2}{1-d^2/4}
    =267/6580<77/1000,\qquad \Theta<47/500.
 \tag{6}
\]

Here E is the residual roll chord and Theta the full spatial principal
proper angle after the actual body/half-turn gauges. None is initially
assumed small. The exact receiver/source height, chart and phase records
are regenerated and match every pinned winning-parent entry.

The full original supporting displacement for nonzero Theta has margin

\[
 1/2-(9/2)(27/25)(47/500)=1079/25000>1/25.
 \tag{7}
\]

Thus every nonzero gauged full rotation violates even closed centered
unit containment. At zero angle the source shadow is equal to the
receiving shadow; undoing the gauges gives G or J_nG and strict
containment fails. This proves the conditional winning-to-winning
exclusion for the whole f>q domain, including all source/receiver signs.

The old balanced theorem's f^2>beta prerequisite was used to force
the source to be winning. It is not required in its original-coordinate
averaged support identity, receiving envelope, whole roll gate, or
full angle estimate once winning membership and the transport bounds
are proved. This hypothesis replacement is essential.

## 4. Uniform third-height gap on the entire tangent circle

Use the same complete six actual tangents p_0,...,p_5. Their ordering
at a tangent direction w can change only on a pair equality line
(p_i-p_j).w=0. The checker constructs all fifteen distinct-point
pair lines, both directed rays of each, and deduplicates them as
oriented rays. Thirty candidates give eighteen distinct directed rays.

Choose exact plane coordinates w.x and w.(B cross x), x=(1,0,0).
The second coordinate differs from an orthonormal coordinate by a
common positive factor, so half-plane and determinant signs give the
correct cyclic order. All antipodes are included. Every cyclicly
adjacent determinant is strictly positive; its closed angular cone
has angle<pi. These eighteen consecutive cones cover the entire
tangent plane, including their boundaries and all duplicated walls.

For each cone [u,v], the interior ray u+v fixes a strict permutation
of all six original ranks. The checker then verifies all five adjacent
rank inequalities at BOTH closed endpoints. Their linearity extends
that complete rank order to every a*u+b*v, a,b>=0.
Let g=p_third-p_first for this fixed permutation.
At every endpoint the exact squared gap is checked. The complete minimum is

\[
 d_3^2=\min_{\text{all wall rays }r}
       \frac{(\operatorname{third}_i p_i.r-\min_i p_i.r)^2}{\|r\|^2}
             =(60-12\phi)/19>1.
 \tag{8}
\]

The endpoint gaps are positive. For any nonzero w=a*u+b*v,

\[
 g.w\ge d_3(a\|u\|+b\|v\|)\ge d_3\|w\|>\|w\|.
 \tag{9}
\]

Thus the full third-minus-first gap is strictly larger than ||w||
uniformly over the entire tangent circle. This is a linear cone and
triangle-inequality proof; thirty isolated values are not treated as
continuum samples. It remains valid on every ordering tie. The endpoint
minimum is sharp because the minimizing endpoint itself is included.

## 5. At most four receiving originals near the beta circle

All48other original center heights have square at least5/3. Their
absolute heights at receiving chord<1/24 exceed
5/4-(9/2)/24=17/16. All six positive active heights keep their signs.
Hence the actual receiving f is the smallest of those six heights.
Their common axial contribution is c0*z; their rank gaps equal the
tangent rank gaps from Section4.

For a receiver satisfying (4), (5) and the full original active set give

\[
 R\|w\|\ge c_0z-f(n)\ge c_0z-\sqrt\beta.
 \tag{10}
\]

Since c0>577/1000, z>199/200, sqrt(beta)<23/50 and R<9/2,

\[
 \|w\|>
 \frac{(577/1000)(199/200)-23/50}{9/2}
       =22823/900000>1/40.
 \tag{11}
\]

By (9), the third-smallest positive original active height is
>f(n)+1/40. At most two positive active originals, and their antipodes,
can therefore have absolute height<=f(n)+1/40. Other originals have
height>17/16. This count is over actual original vertices, not invented
projected contacts or a conjectured polygon combinatorics.

## 6. Quantitative threshold source transport and original injection

Every remaining source lies in a threshold region, with maximum beta.
Its actual optimizer is a proper body image of one of
ell=(0,1,-3-3phi) or h=(0,1,(3phi-1)/11). Each positive active original
tangent quadrilateral has sharp disk squared radius
(39+37phi)/29>(9/5)^2, regenerated in this checker.

Put F=sqrt(beta-epsilon). Its full coercivity, the acute chord identity,
sqrt2<3/2 and sqrt(beta)+F>9/10 give

\[
 \|k-n_*\|
 \le\frac{\sqrt2}{\rho_*}(\sqrt\beta-F)
 <\frac{5}{6}\frac{\epsilon}{\sqrt\beta+F}
 <\frac{25}{27}\epsilon=:a.
 \tag{12}
\]

The actual reference shadow has eight distinct original maximum-circle
points of radius r_beta=sqrt(R^2-beta)>4. Their original preimages
are unique and have squared axial height beta. All28pairs at EACH
threshold reference are regenerated, with complete minimum

\[
               \min_{i<j}\|p_i^0-p_j^0\|^2=(40+32\phi)/29>1.
 \tag{13}
\]

Let A1 minimally transport n_* to k, and choose ANY proper D transporting
n_* to the ACTUAL receiving n. Then W=Q A1 D^t fixes n and is an
arbitrary proper roll; Q=W D A1^t. For each of the eight actual source
original preimages v_i, set

\[
 p_i=P_nQv_i,\qquad p_i^0=W D P_{n_*}v_i.
 \tag{14}
\]

All original points p_i belong to the projected source, while p_i^0
are an exact rolled isometric copy of the reference circle.
For a minimal normal transport of chord d, resolving its rotation plane gives
||P_ref(A1^t-I)v||<=|v.n_*|d+R*d^2/2.
Therefore

\[
 \|p_i-p_i^0\|<
 \eta=(23/50)a+(9/4)a^2<1/2000.
 \tag{15}
\]

This uses the actual source preimages and all proper source orientations.
No receiving reference frame or receiving transport loss is needed.
Both threshold families have the same proven radius/pair-distance facts.
The C branch and all source body gauges are thereby covered without
any roll restriction or a fixed improper alignment.

Suppose all eight p_i belong to the actual receiving polygon T=P_nK.
Write r_i=||p_i||>=r_beta-eta>0. Its support in direction p_i/r_i
is attained by some ACTUAL receiving original q_i=P_n v'_i and
q_i.(p_i/r_i)>=r_i. The receiving circumradius bound is
||q_i||^2<=R^2-beta+epsilon. Consequently

\[
 \begin{split}
 \|p_i-q_i\|^2
   &\le \|q_i\|^2-r_i^2\\
   &\le\epsilon+2r_\beta\eta-\eta^2
      < L:=\epsilon+9\eta<1/100.
 \end{split}
 \tag{16}
\]

Also ||q_i||>=r_i forces the absolute original receiving axial height
of v'_i to be<=H=sqrt(beta+9eta). Exact guards give H<1/2 and

\[
 H-f(n)\le\frac{\epsilon+9\eta}{H+f(n)}
           <(10/9)L<1/40.
 \tag{17}
\]

Thus every chosen q_i must be the projection of one of at most FOUR
original receiving vertices from Section5. The48nonactive originals,
whose heights exceed17/16, cannot be chosen.

The actual source pair distances remain

\[
 \|p_i-p_j\|>1-2\eta>1/5,
 \qquad \|p_i-q_i\|<1/10.
 \tag{18}
\]

If two p_i used the same receiving original then their distance would
be<2/10=1/5, contradicting (18). Hence these support choices must be
injective on the eight actual source points. Eight cannot map into four.
This excludes every threshold source, uniformly over all rolls and all
receiving positions in (4). No closed-containment limit argument is needed.

## 7. Exhaustion and the precise new conclusion

The complete region spectrum excludes all lower source families.
Section3 excludes every winning source in the remaining receiving band.
Sections4--6 exclude both threshold families. The inherited1/600band
excludes every nonwinning receiver under the numerical1/1200cutoff.
The old all-threshold theorem excludes the superlevel f^2>=beta.
Original axial boundaries have f=0 and cannot occur under the cutoff.
These cases exhaust EVERY receiving and source orientation.

Thus centered unit strict containment is impossible whenever
f(n)^2>=beta-1/1200. Translation/scale reduction proves (1);
the complete diameter identity and4/1200=1/300 prove (2).
The equality cutoff, all ordering walls, all chart boundaries and all
source/roll zero cases are covered. This is a global numerical
necessary receiver condition, not a global non-Rupert proof.

## 8. Reproduction, prior work and trust

Python3.11+standard library; numerical threads one:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/global_slack_certificate.py --self-test
~~~

Every output byte must match global_slack_expected.json. SHA256 and
completed normal/publication-copy optimized timings are in README.md.
Fifteen malformed controls reject in both modes, including omitted,
duplicated or incorrectly ordered wall rays, bad closed cone orders,
unsupported third-height gaps, false source circles and excessive epsilon.

All new angular cones, source circles/preimages/pairs, original receiving
height gaps, tangent quadrilaterals, uniform q phase/cut/chamber gates
and1800original cut-triangle support comparisons are regenerated.
The complete840strata torque theorem, old full regional classification
and previous numerical nonwinning band are explicit pinned inputs;
their full self-tests are not claimed replayed.
The proof is unformalized. The inspected exact Q(phi)/Fraction kernels,
Python arithmetic, original body, imported published conclusions and
written cone, proper-frame, support transport and injection bridges
remain the trust boundary. Regression is not an independent review.

The independently selected [threshold review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md),
source52d7829380a548c66fe716ca8155c2c22e6cd23f, graph7576, proves
the sharp tangent disk and1/7barrier used here and reconstructed in
the new checker. The [contact-collar review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_contact_collar_review2/REVIEW.md),
sourcec8e44ca98b50499e356396525444b92b0315345c, graph7635,
confirms the preceding existential global slack, with larger local
branch caps. It explicitly does not compute a numerical global epsilon.
Neither review audits this new numerical theorem.

Complementary bounded recent work was read:
six-rupert-1, researcher, [signed zero-height deltoidal wedge](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/zero_height_wedge_proof.md),
sourcefecd889db1ad561f00a3b65db0b9c1b77887ac9b, graph7663;
six-rupert-2, researcher, [balanced-torque J77 caps](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_balanced_torque_caps/PROOF.md),
source788a042adb636949eaf06a5825e9f439d47e48de, graph7647.
No different-body constants are transferred and no reviewer was directed.

Primary [2604.26531](https://arxiv.org/html/2604.26531) and
[2508.18475](https://arxiv.org/abs/2508.18475) were live checked
2026-09-30. RID remains conjecturally non-Rupert; the latter paper's
non-Rupert body is different. Retain the standard strict projection
definition from [2112.13754](https://arxiv.org/html/2112.13754).
No timeout, UNKNOWN, absent floating witness or incomplete search is
used as a mathematical nonexistence premise. Historical priority
is unestablished.
