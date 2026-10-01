# A closed RID source-branch exclusion from stronger full-roll support gaps

**six-rupert-3, researcher; 2026-10-01.** Complete written, unformalized
computer-assisted intermediate proof. The finite hypotheses are checked by
[gamma_branch_certificate.py](gamma_branch_certificate.py). This new branch
proof is independently unreviewed. Historical priority is unasserted.
Global non-Rupertness of the rhombicosidodecahedron (RID) remains **open**.

## 1. Precise statement and dependency interface

Put \(\phi=(1+\sqrt5)/2\). The sixty original vertices \(V\) are the
distinct independent signs and even coordinate permutations of

\[
 (1,1,\phi^3),\qquad (\phi^2,\phi,2\phi),\qquad
 (2+\phi,0,\phi^2).
\]

They give the standard edge-two body
\[
 K=\operatorname{conv}V=-K,\quad R^2=7+8\phi,\quad
 P_n=I-nn^T,\quad f(n)=\min_{v\in V}|v\cdot n|,\quad
 \beta=(19-8\phi)/29.
\]
Here \(n\) is a unit vector. For any directed reference \(m\), its strict
signed region is
\[
 C(m)=\{u\in S^2:(v\cdot u)(v\cdot m)>0\text{ for every }v\in V\}.
\]
The proper body group \(G\) has sixty elements. Winning regions are the
proper images of the region with raw reference
\[
 B=(0,2-\phi,1).
\]
The two threshold classes have raw directed representatives
\[
 r_L=(0,(2-\phi)/3,-1),\qquad r_H=(0,1,(3\phi-1)/11).
\]
Directions are normalized when used as \(m\). These are the same actual
signed regions and proper classes as in the
[threshold classification](THRESHOLD_RECEIVER_PROOF.md), graph **7520**.
The alternative raw low reference \((0,1,-3-3\phi)\) is a positive
multiple of \(r_L\). The checker verifies the actual proper body group,
all original vertex permutations, twenty directed winning references,
sixty references in each directed threshold orbit, their antipodes, and
all 140 distinct directed original sign patterns. Thus signs and body
gauges below are actual geometric symmetries.

**Theorem.** Let the receiver \(n\) belong to any threshold signed region,
with
\[
 f(n)\ge83/200.
\]
For every original proper rotation \(Q\), if \(k=Q^Tn\) belongs to any
winning signed region, then for every planar translation \(t\in n^\perp\)
and scale \(\lambda\ge1\),
\[
 \lambda P_n(QK)+t\not\subseteq P_nK.
\]
Both proper threshold classes, all rolls, and the height-cutoff boundary
are included. Consequently the same source-branch exclusion holds under
\(f(n)^2\ge\beta-1/28\), since the checker proves
\(\beta-1/28>(83/200)^2\).

This does **not** enlarge the global receiving gap. The global necessary
condition remains the [weighted \(1/100\) theorem](WEIGHTED_GLOBAL_BAND_PROOF.md),
source **e8f808484cb7ad21bf95438833f5737355c5ff8a**, graph **8058**,
independently confirmed by
[six-reviewer-4](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_weighted_gap_review4/REVIEW.md),
source **0e8708ef1b27633bcdf0f89b717d93b949c68490**, graph **8108**.
That review applies to 8058, not to this new theorem.

The proof uses the following explicit inherited interfaces. They are
credited rather than asserted as new.

* [Original geometry and actual chart/body bridge](CELL_PROOF.md), graph **7178**;
  [complete signed-region spectrum](GLOBAL_CAP_PROOF.md), graph **7256**:
  436 projective strict regions, ten winning regions with maximum
  \(f^2=1/3\), sixty threshold regions with maximum \(\beta\), and every
  other maximum at most \(1/7\). The spectrum is needed only for the
  common-band corollary in Section 6, not for the conditional theorem.
* [Winning original tangent hexagon](WINNING_RECEIVER_PROOF.md), graph
  **7498**, and [threshold original tangent quadrilaterals](THRESHOLD_RECEIVER_PROOF.md),
  graph **7520**: the positive originals all have common height
  \(c_0=1/\sqrt3\) or \(c=\sqrt\beta\), respectively. Their tangent
  polygons contain centered disks of sharp squared radii
  \(\rho_W^2=8/3+4\phi\) and \(\rho_T^2=(39+37\phi)/29\).
* [Threshold review by six-reviewer-2](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md),
  source **52d7829380a548c66fe716ca8155c2c22e6cd23f**, graph **7576**, and
  [regional coercivity interface](BETA_CAP_PROOF.md), source
  **7dec5c34b27552eaf8cbc8b06c06ed5e09a245bc**, graph **7659**.
  The old full-roll constant \(1/16\) is credited to review 7576.
* [Proper frame and whole-support transport arguments](WEIGHTED_GLOBAL_BAND_PROOF.md),
  graph **8058**, building on [closed dyadic roll certificates](COUPLED_NONWINNING_PROOF.md),
  source **fde90bccf928a5d369c50e491e1e323b1910fd28**, graph **7972**.
  The new computation regenerates the physical coefficients and whole
  support envelopes at the new constants. It does not invoke the old
  cutoff or an old small-angle source bound on the enlarged domain.

## 2. Necessary centering and honest whole-region normal chords

Suppose the stated containment holds. Central symmetry also gives
\(\lambda P_n(QK)-t\subseteq P_nK\). Taking convex midpoints and then
scaling toward the origin yields the necessary containment
\[
 P_n(QK)\subseteq P_nK.                                      \tag{1}
\]
This keeps the original physical \(n,Q,k\). All originals have squared
norm \(R^2\), and a farthest projected original and its antipode attain
the diameter. Therefore
\[
 \operatorname{diam}(P_nK)^2=4(R^2-f(n)^2),\qquad
 f(k)\ge f(n)\ge q:=83/200.                                 \tag{2}
\]

Apply actual proper receiving and independent right source body gauges
to choose the displayed threshold and winning references. For either
reference unit \(m\), write a unit vector in its signed region as
\(u=zm+w\), with \(w\perp m\). Positive original signs and the tangent
disk give
\[
 q\le f(u)\le c_m z-\rho_m\|w\|.                            \tag{3}
\]
Indeed, every positive original height is positive in this region, and
the minimum of those heights is at most
\(c_mz+\min_j P_j\cdot w\le c_mz-\rho_m\|w\|\).
Equation (3) implies \(z>0\).

The certificate regenerates positive outward \(10^{-12}\)-grid root
brackets. Use upper height endpoints and lower radius endpoints
\[
 C=456966311669/10^{12},\quad
 C_{0U}=57735026919/10^{11},\quad
 R_T=1846406179243/10^{12},\quad
 R_W=188940328519/62500000000.
\]
Define
\[
 s_T=(C-q)/R_T,\quad s_W=(C_{0U}-q)/R_W,\quad
 a_T=(1001/1000)s_T,\quad a_W=(1001/1000)s_W.                 \tag{4}
\]
The strict upper height endpoints imply the actual tangent norms are
strictly below \(s_T,s_W\). Let \(Z_T,Z_W\) be validated lower bounds for
\(\sqrt{1-s_T^2},\sqrt{1-s_W^2}\). The exact checks
\((1001/1000)^2(1+Z_T)>2\) and its winning counterpart, together with
\[
 \|u-m\|^2=2\|w\|^2/(1+z),
\]
prove the actual whole-region chord bounds
\[
 \|n-m\|<a_T=42008277980669/1846406179243000<23/1000,
\]
\[
 \|k-b\|<a_W=16251261945919/302304525630400<54/1000,           \tag{5}
\]
where \(b=B/\|B\|\). The older \(25\epsilon/27\) estimate is not used;
its separate denominator premise fails on this domain. There is no
initial small-angle hypothesis on \(Q\).

All tangent polygon facets and their sharp disk radii are regenerated
from the sixty originals. The exact finite comparison is inherited
geometric data checked anew, not an inference from a numerical drawing.

## 3. A reference support gap of 7/100 for every proper roll

The full reference winning source shadow has twelve corners. Every one
has a unique original preimage of squared axial height \(1/3\). The
checker reconstructs the full original hull and all **720** original
corner-edge support comparisons. No surrogate planar corner without an
original spatial preimage is used.

For each of the two threshold references, the receiver's full original
shadow has sixteen corners and sixteen outward facet normals. For unit
facet \(\mu_j\), let \(H_j=\max_{v\in V}\mu_j\cdot v>0\). In oriented
orthonormal charts of the source and receiving planes, every proper
planar roll is an angle \(\alpha\). For source original corner \(p_i\),
its support excess has the form
\[
 A_{ji}\cos\alpha+D_{ji}\sin\alpha-H_j.                     \tag{6}
\]
All **192** physical facet/original-corner triples per receiver are
regenerated with exact outward rational intervals for their coefficients.
The positive root branches and every denominator are checked explicitly.

Cover the whole circle by four closed quarters. On each quarter use
\(t\in[0,1]\),
\[
 \cos\alpha=(1-t^2)/(1+t^2),\qquad
 \sin\alpha=2t/(1+t^2),
\]
with the correct quarter transformation of \((A,D)\). On a closed leaf
\([l,h]\), the numerator of (6) minus \(\Gamma\), where
\(\Gamma=7/100\), has quadratic Bernstein coefficients with weight triples
\[
 (1-l^2,2l,1+l^2),\quad
 (1-lh,l+h,1+lh),\quad
 (1-h^2,2h,1+h^2).
\]
Each coefficient is bounded below by
\[
 A_{\rm lo}a+D_{\rm lo}d-(H_{\rm hi}+\Gamma)v.              \tag{7}
\]
The nonnegative Bernstein basis sums to one. Three strictly positive
bounds in (7) thus prove the strict support gap on the entire closed
leaf, including both endpoints.

The freshly generated complete covers have respectively **26** and
**58** closed leaves, **48** and **112** total tree nodes, and maximum
depths **4** and **6**. All four closed quarter roots are present. Every
internal midpoint node has both children. Every selected original
witness index is valid. All **252** selected exact coefficient bounds
are strictly positive, and the full selected-record hashes are recorded
in [gamma_branch_expected.json](gamma_branch_expected.json). Consequently,
for every proper planar roll, some actual reference receiving facet and
some actual original source corner satisfy
\[
 \mu_j\cdot\operatorname{roll}(p_i)>H_j+7/100.               \tag{8}
\]
This strengthens the credited reference bound \(1/16\). It is not a
claim of the optimal reference gap. A depth limit would mean an
incomplete certificate; the successful computation explicitly checks
complete closed coverage rather than treating a failure as exclusion.

## 4. Whole receiving support envelopes on the enlarged normal domain

For a minimal proper rotation \(S:m\to n\), its axis is perpendicular
to \(m\). Let \(\delta=\|n-m\|\). Rodrigues' formula gives, for every
original \(v\),
\[
 \|P_m(S^Tv-v)\|\le |v\cdot m|\delta+R\delta^2/2.           \tag{9}
\]
The linear term from the tangent component is parallel to \(m\) and
vanishes after projection; the quadratic term has norm at most
\(R(1-\cos\theta)=R\delta^2/2\). This identity also holds at zero
chord with \(S=I\). Our normal chords preclude antipodal ambiguity.
For a unit facet \(\mu\perp m\), the same estimate bounds
\(\mu\cdot S^Tv\) above by \(\mu\cdot v+|v\cdot m|\delta+R\delta^2/2\).

Keep the original reference slack
\(g_v=H-\mu\cdot v\ge0\), and put \(h_v=|v\cdot m|\).
At the new actual bound \(a_T\) in (5), the certificate proves for
**every original at every receiving reference facet**
\[
 g_v\ge\max(0,h_v-13/10)a_T.                               \tag{10}
\]
For every zero-gap original it verifies \(h_v\le13/10\). Each positive
gap comparison is strict using validated outward height and unit-normal
bounds. There are **960** comparisons per reference, **1,920** in total.
Their complete generated record hashes and the per-facet exact positive
slack minima are in the compact expected output.

Because \(R<9/2\), equations (9)--(10) give the support envelope
for the **whole original receiving body**
\[
 \max_{v\in V}\mu\cdot S^Tv\le H+\eta_T,\qquad
 \eta_T=(13/10)a_T+(9/4)a_T^2.                             \tag{11}
\]
Every tied noncorner original is included. No persistence of the
sixteen-corner hull's combinatorics is presumed.

Apply (9) in the independent minimal proper source frame \(T:b\to k\).
All twelve original reference source corners have \(|v\cdot b|=c_0\),
so their individual projection transport error is bounded by
\[
 \eta_W=C_{0U}a_W+(9/4)a_W^2.                              \tag{12}
\]
Their projections need not remain corners in the actual source hull;
they remain original points in the actual source, which suffices.

## 5. The actual containment contradiction

Set \(A=S^TQT\). Since \(Qk=n\), this proper orthogonal map sends
\(b\) to \(m\) and restricts to a proper planar isometry
\(b^\perp\to m^\perp\). It is therefore one of the arbitrary proper
rolls already covered by (8). The actual source point in the receiving
reference plane is
\[
 S^TP_nQv=A P_bT^Tv.
\]
By (8) and (12), some reference receiving facet and some actual original
source point have support strictly greater than
\(H+\Gamma-\eta_W\). By (11), every actual receiving original has
support at most \(H+\eta_T\). The exact rational check is
\[
 \Gamma-\eta_W-\eta_T
 =\frac{33475388346154508000108855144764898133548010189418430106209}
 {19472593810389064746169409123835905425719050830240000000000000}
 >1/600>0.                                                 \tag{13}
\]
This contradicts (1) and proves the theorem. The argument includes
the cutoff boundary, every original proper \(Q\), translation and
scale stated in Section 1. It uses small **normal** chords and covers
the full residual roll; it does not assume a small full spatial rotation.

## 6. A common-band reduction, and the remaining frontier

The [antipodal axial-majorization theorem](AXIAL_MAJORIZATION_PROOF.md),
source **28e16144212f714dd6959afd1d3e7ca13ea2171a**, graph **8110**,
excludes every threshold source into any winning receiver at
\(f(n)\ge21/50\). That theorem remains independently unreviewed.
Since \(21/50>83/200\), the theorem here excludes the opposite mixed
branch on the same band. By (2), the complete region spectrum and
\((21/50)^2>1/7\), any closed containment receiving at
\(f(n)\ge21/50\) can now only have a winning source with a winning
receiver, or a threshold source with a threshold receiver.

This is a reduction to the two same-type branches. It proves neither
branch rigid on that enlarged band. The two threshold proper classes
and their four ordered pairings remain included in the second open
branch. No global \(1/31\), global \(1/28\), or global non-Rupert
theorem follows.

The concrete next step is to keep the signed Cayley contact quadratics
for the larger winning region, with a proved full spatial-angle
prerequisite and a complete closed axis cover. The whole-D1
[deltoidal proof by six-rupert-1](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cayley_wedge_proof.md),
graph **8030**, and the
[J77 signed-contact reduction by six-rupert-2](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_receiving_balanced_stress/PROOF.md),
graph **8086**, give complementary method context. Their bodies,
constants and hypotheses are not imported. For threshold comparisons,
retain the weighted axis-sensitive energy and actual matched-original
hypothesis identified in review 8108 before deriving directional
remainder bounds. No reviewer verdict was requested or influenced.

## 7. Reproduction and trust boundary

From the repository root, Python **3.11+**, standard library only,
run sequentially with all numerical threads set to one:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/gamma_branch_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B -O rhombicosidodecahedron_mirror_cluster_obstruction/gamma_branch_certificate.py --self-test
```

Both regenerate and compare **every byte** of the 39,358-byte expected file,
SHA256 **03566958f78c39217fd109c297508534e8c8cf7ac5c0944be7c4136b2b8ca426**.
Ordinary and optimized author checks completed in 7.264110 and 7.381223
seconds, respectively, within separate 55-second limits; their maximum
child resident sizes were 26,096 and 27,880 KiB. These timings are
reproducibility metadata and have no mathematical role.
[gamma_branch_inputs.json](gamma_branch_inputs.json) pins all **47**
previously published mathematical Python/JSON inputs. They are preserved.
The new code freshly reconstructs both closed roll trees, all 384
physical facet/corner coefficient intervals, all 252 selected bounds,
all 1,920 enlarged receiving envelopes, all 720 source hull supports,
original tangent geometry, 140 directed reference regions, sixty proper
body matrices and permutations, six outward positive root enclosures,
and ten scalar gates. Twelve malformed controls reject missing inputs,
original points, facets, quarters and leaves, duplicated leaves, invalid
witness indices, false Gamma, unsafe tied-height intercept, reuse of
the old Gamma on the enlarged band, and a lower unsupported cutoff.
Explicit guards survive optimized Python.

The previous 436-region enumeration, weighted global theorem, old
torque covers and conditional C3 averages are not claimed rerun. Hash
pins establish source provenance, not independent proof of every
ancestor. The trust boundary is the original solid and region
identification, exact Python/Fraction and quadratic-field semantics,
validated positive root branches and complete finite checks, the
specified inherited interfaces, and the written unformalized
centering, diameter, regional coercivity, proper-frame, Bernstein and
original support-envelope arguments above. Native replay is author
validation, not independent review or formal verification. No sampled
continuum, floating search, solver outcome, timeout, memory kill,
UNKNOWN or incomplete enumeration is an exclusion premise.

The standard strict-shadow characterization is in
[Steininger–Yurkevich](https://arxiv.org/abs/2112.13754). Live bounded
primary checks on 2026-10-01 found
[Zeng](https://arxiv.org/html/2604.26531) still states the RID conjecture
as open; [Steininger–Yurkevich's non-Rupert construction](https://arxiv.org/abs/2508.18475)
concerns a different body. The named unresolved baseline in
[the passage study](https://arxiv.org/html/2509.08190) likewise retains
RID. These checks are not exhaustive novelty evidence.
