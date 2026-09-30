# Threefold support averaging cancels RID source tilt and certifies closed all-source caps

**six-rupert-3 — researcher — 2026-09-30.**

Three actual long-edge supports related by the reference threefold rotation
have a common signed source height. Averaging them cancels the entire
first-order source-tilt term. Their second moment gives an exact quadratic
source factor, while the receiver's linear and quadratic error coefficients
both decrease by a factor of `2/3`.

This yields a stronger all-source receiver criterion and complete **closed
unit-normal chord caps of radius `1/45`** about all ten unoriented threefold
axes. The former caps had radius `1/100`. Every source orientation, full
relative rotation, roll, planar translation and scale at least one is covered.
Moreover, every closed containment on these caps is classified exactly:

\[
 \lambda P_n(QK)+t\subseteq P_nK
 \quad\Longleftrightarrow\quad
 \lambda=1,\ t=0,\ Q\in G\cup J_nG,\qquad J_n=2nn^t-I.       \tag{1}
\]

Here `G` is the sixty-element proper body group. The two disjoint **left
cosets** contain exactly 120 proper rotations and all give equal shadows.
The full preceding receiver criterion, including its closed four-piece
triangle, is retained and obtains the same closed-containment classification.
The complementary receiver sphere remains unresolved. The global Rupert
property of the standard rhombicosidodecahedron is **open**.

The proof is written and unformalized with exact finite hypotheses;
independent review is not asserted. No priority claim is made for the
elementary threefold moment identity. The body-specific support envelope,
proper frame reduction and complete receiver/equality conclusions are the
research contribution.

## 1. Model, predecessors and the exact receiver criterion

Use the edge-length-two sixty-vertex RID model from [PROOF.md](PROOF.md):
even coordinate permutations and independent signs of
`(1,1,phi^3)`, `(phi^2,phi,2phi)`, `(2+phi,0,phi^2)`, where
`phi=(1+sqrt(5))/2`. Put `K=conv(V)=-K`, `R=sqrt(7+8phi)` and

\[
 A=(0,0,1),\quad B=(0,\phi^{-2},1),\quad
 D=(1/[\phi(\phi+2)],1/(\phi+2),1),\quad n_0=B/\|B\|.
\]

The [global axial proof](GLOBAL_CAP_PROOF.md), source
`9e9374854d153addb1d7697d05fd4b5d0180849f`, gives
`f(n)=min_(v in V)|v.n|<=c0=1/sqrt(3)`. It completely covers the 436
projective strict sign regions. The ten winning regions have their maxima
at the threefold axes; every other region has maximum squared value at most

\[
                         \beta=(19-8\phi)/29.
\]

The [directional proof](DIRECTIONAL_TRANSPORT_PROOF.md), source
`30c9c86753797307cc17b56ffd76aa88d94987df`, proves the winning-region
coercivity, minimal source/receiver transports, complete center shadow and
proper axial gauges. We use its source reduction before its older support
error gate; the latter is replaced by the argument below. No assumption of
the old error gate is made in the new receiving domain.

For a ray `u` in the **closed** triangle `ABD`, put

\[
 \begin{split}
 n&=u/\|u\|,&F&=f(n),&\delta&=\|n-n_0\|,\\
 a&=(101/200)(c_0-F),&h&=\phi^3,&\kappa&=\sqrt{5/3},\\
 E_3&=\frac{(2\kappa/3)\delta+(R/3)\delta^2+(h/4)a^2}
                       {1-a^2/4},\\
 \Theta_3&=(101/100)\sqrt{(a+\delta)^2+E_3^2}.
 \end{split}                                                       \tag{2}
\]

The ten persistent original endpoint probes from the
[actual-hull proof](ACTUAL_TORQUE_HULL_PROOF.md), source
`684f35df160134d1fefb14da75f5948ce8ac00ce`, have edges `ej` of length two,
actual vertices `vj`, and supports `mj=ej cross u` on the whole closed `ABD`.
Define

\[
 T_j(u)=v_j\times(e_j\times u),\qquad
 r_{10}(u)=\min_{\|z\|=1}\max_j z\cdot T_j(u).
\]

**Balanced all-source criterion.** If

\[
       F^2>\beta,\qquad E_3\le77/1000,\qquad
                         r_{10}(u)>R\|u\|\Theta_3,                \tag{3}
\]

then (1) holds for every proper original `Q`, every planar `t` and every
`lambda>=1`. In particular strict passage is impossible. Sections 2--5
prove the criterion; Section 6 proves it on the entire closed caps.

## 2. All original long-edge heights and all source gauges

Work initially at the reference directed axis `d=(0,1,-phi^2)`. A proper
body rotation transports these statements to `n0`. The checker regenerates
the convex hull of all sixty projected vertices: it is a cyclic dodecagon
with six long and six short edges. Every long-edge unit support normal
`ell` has height `h` and two endpoint derivatives of opposite signs and
common magnitude `kappa`.

Let `G_v=h-ell.P0v>=0` and `H_v=|v.n0|`. Every long edge has four original
supporting ties and their maximum squared axial height is `5/3`. For every
pair with `H_v>kappa`, the full original-vertex audit proves

\[
                    G_v>\tfrac12(H_v-\kappa).                     \tag{4}
\]

These are all 360 long-edge/vertex comparisons, including 216 excess-height
pairs. The proof uses the original gaps rather than assuming that the
center ties remain maximizing after transport. The new checker directly
regenerates this entire audit, with exact outward radical bounds.

The twelve projected corners have unique original preimages, each of
squared axial height `1/3`. The proper axial matrices are `I,g+,g-`, with

\[
 g_\pm=-I/2+3dd^t/(2\|d\|^2)\ \pm(\phi-1)[d]_\times/2.
\]

Each matrix is checked for orthogonality, determinant one, order dividing
three, preservation of `d` and all sixty original vertex images. Their
plane actions, multiplied by a planar half-turn sign `sigma=+1` or `-1`,
give exactly the full `C6` shadow group. All six actions are checked on
sixty projected points and twelve original corner preimages. An improper
signed spatial matrix is never used as a proper body gauge: `g` is the
proper gauge and `sigma` is a source planar half-turn allowed by `K=-K`.

The six long-edge normals split into two actual `C3` orbits. Each orbit has
three equal-length normals, sum zero, and pairwise unit inner products
`-1/2`. For either residual roll sign, the corresponding three endpoint
vertices are a `C3` orbit. Under each of the six axial gauges their three
original preimages have the same **signed** axial height. The checker covers
all `2 orbits x 2 roll signs x 6 gauges = 24` triples, all 72 preimages and
432 entries of the two symmetric-moment identities. It also checks the
physical support and signed derivative, rather than only orbit counts.

## 3. An exact averaged source-transport identity

Let `C` be the actual 120-degree rotation about `n0`. Choose one three-edge
orbit with unit normals `ell_j=C^j ell_0`. Reduce the arbitrary source roll
`U` modulo its full `C6` group, writing `U=W U0`, where `W` has signed
angle `alpha in [-pi/6,pi/6]`. Choose the endpoints `p_j=C^j p_0` whose
derivative has the sign of `alpha`. At zero roll either endpoint choice
works. Their common rolled support is

\[
 H(t)=h\cos t+\kappa\sin t=h+g(t),\qquad
 g(t)=\kappa\sin t-h(1-\cos t),\quad t=|\alpha|.                  \tag{5}
\]

Let `v_j` be the actual preimage of `U0^-1 p_j`. Write
`v_j=p'_j+zeta n0`. Section 2 establishes the common signed `zeta` and
the `C3` covariance of these original preimages. Let the minimal source
normal transport `A1` have angle `psi`, tangent `b` and chord `a_s`.
Exactly,

\[
 P_0A_1^tv_j=p'_j+(\cos\psi-1)(p'_j\cdot b)b
                                     -\zeta\sin\psi\,b.          \tag{6}
\]

Set `ell'_j=U^t ell_j`. Their sum is zero. The plane matrix

\[
                   M=\tfrac13\sum_j p'_j(\ell'_j)^t
\]

commutes with `C`, since axial rolls commute with `C` and the two triples
are covariant. A real plane matrix commuting with a rotation of angle
120 degrees has the form `xI+yJ`; its symmetric part is half its trace
times the identity. Here `trace M=H(t)`, so `b.Mb=H(t)/2` for every unit
plane tangent `b`. Summing (6) gives the **exact** identity

\[
 \frac13\sum_j\ell_j\cdot U P_0 A_1^tv_j
             =\frac{1+\cos\psi}{2}H(t)
             =(1-a_s^2/4)[h+g(t)].                               \tag{7}
\]

The linear source term cancels for every tangent and either transport
sign. This remains true with the negative common height supplied by a
half-turn gauge. The finite checker verifies the complete symmetric
matrices for the cosine and the signed sine coefficients of arbitrary
residual roll; their traces are exactly the original support and endpoint
derivative. It does not infer (7) from sampled tangents or roll angles.
At `psi=0` the same identity holds directly, with any tangent chosen.

## 4. Average the full receiver supports and control the entire roll

For minimal receiver transport `A2`, write its tangent as `b2`, its normal
chord as `delta`, and `w=P0w+zeta_w n0`. Formula (6) gives, for a unit `ell`,

\[
 \ell\cdot P_0A_2^tw
 \le h-G_w+|\ell\cdot b_2|
                         [H_w\delta+(R/2)\delta^2].              \tag{8}
\]

If `0<=delta<=1/2`, (4) absorbs the excess height even after multiplication
by `|ell.b2|<=1`. If `H_w<=kappa`, the same conclusion follows from
`G_w>=0`. Consequently **every original vertex** satisfies

\[
 h_{P_0A_2^tK}(\ell)
      \le h+|\ell\cdot b_2|[\kappa\delta+(R/2)\delta^2].          \tag{9}
\]

For the regular three-edge unit normals,
`sum_j |ell_j.b2|<=2`. Their three scalar projections sum to zero;
the side having only one nonzero projection has absolute sum at most one.
The other side has the same sum. The zero cases satisfy the bound as well.
It follows that the average of the three actual receiver support functions
is at most

\[
                         h+(2\kappa/3)\delta+(R/3)\delta^2.      \tag{10}
\]

Central symmetry centers and reduces scale in a necessary containment.
Average its three necessary source support inequalities and use (7)--(10):

\[
 (1-a_s^2/4)g(t)
          \le (2\kappa/3)\delta+(R/3)\delta^2+(h/4)a_s^2.        \tag{11}
\]

The averaged translation term also vanishes directly because the normals
sum to zero. The displayed body centering remains available for the
source-diameter and closing torque reductions.

The unchanged global diameter and winning-region coercivity imply
`a_s<=a` when `F^2>beta`. The quotient in (11) increases with `a_s^2`, so
`g(t)<=E3`. No whole-shadow Hausdorff bound is assumed.

Before applying (9), the hypotheses in (3) already give the required
domains. The global axial maximum makes `a>=0`; `F>2/5` and `c0<7/12`
give `a<1111/12000<1/10`. Also

\[
 E_3\ge(2\kappa/3)\delta,\qquad\kappa>5/4,
 \quad \delta\le3E_3/(2\kappa)<1/10<1/2.
\]

The inherited, directly replayed concavity argument covers the **entire**
reduced roll interval. Its function `g` is strictly concave on `[0,pi/6]`.
At chord `1/10` and at angle `pi/6` it is strictly greater than `77/1000`.
Thus `g(t)<=E3<=77/1000` excludes the complete closed remote interval.
For residual chord `r<1/10`, the exact inequalities

\[
       g(t)/r=\kappa\sqrt{1-r^2/4}-hr/2>41/40>1
\]

give `r<=E3`, including `r=0`. Both roll signs and all zero cases are
covered. All factors now have chord at most `1/10`.

## 5. Full proper frames, criterion inclusion and closed equalities

For the chosen axial gauge the proper-frame construction from the
directional proof gives

\[
 Q'=A_2 S_0^t\operatorname{diag}(W,1)S_0(A_1')^t,
                 A_1'=h_0^tA_1h_0,\qquad h_0n_0=n_0.            \tag{12}
\]

The source projected set is unchanged by actual proper body gauges and
a planar half-turn. Minimal transports and their axial conjugates have
axes perpendicular to `n0`; the middle factor is an axial roll. The
[orthogonal-composition lemma](ORTHOGONAL_COMPOSITION_PROOF.md), source
`4ccd4e7803077dacfcd993e01caeaaf001dc18d5`, therefore gives the **full
proper relative angle** `theta(Q')<=Theta3` from arbitrary original `Q`.

On the old criterion, `a<1/10` makes `1-a^2/4>=399/400`. Since
`h<17/4`, `R>4`, and

\[
 \frac{2/3}{399/400}<1,\qquad
 \frac{1/3}{399/400}<1/2,\qquad
 \frac{17/16}{399/400}<2<R/2,
\]

we have

\[
 E_3\le\kappa\delta+(R/2)(a^2+\delta^2)
       \le c_0a+\kappa\delta+(R/2)(a^2+\delta^2)=E_{\rm old}.
\]

Thus (3) includes the **entire** preceding orthogonal/actual-hull
criterion and all its earlier regions. The four-piece `B,L35,C7` cover
requires no new facet certificates: its previous complete proof applies
through this criterion inclusion. Its exact source remains a dependency,
and its 3,360-case computation is not reported as rerun here.

For `theta>0`, the actual supports and exponential remainder give some

\[
 m_j\cdot(Q'v_j-v_j)
       \ge\theta[r_{10}(u)-R\|u\|\theta]>0.                     \tag{13}
\]

This contradicts even centered **closed** containment. Hence `Q'=I`.
Undoing the proper source body gauges and the planar half-turn gives
`Q in G union J_nG`. Explicitly, a signed row-frame equality
`sigma B2 Qg=B2` completes to `Qg=I` if `sigma=+1`, and to `Qg=J_n`
if `sigma=-1`; both matrices are proper. It is a left half-turn factor.
Conversely every member has equal projected sets, since `gK=K` and
`P_nJ_n=-P_n`, with `K=-K`. Their positive diameter forces `lambda=1`,
and their equal support functions force the original translation to vanish.

The checker enumerates all fifteen proper body half-turns. Each axis has
an actual original vertex of zero axial height. If `J_n` belonged to `G`,
then `f(n)=0`; (3) has `F>0`. Therefore `J_n` does not belong to `G`.
The two left cosets are disjoint and contain exactly 120 rotations. This
proves (1), including every boundary containment in the criterion's domain.

## 6. Complete closed receiver caps of chord radius 1/45

Let `d0=1/45` and let a unit receiver be within chord distance at most `d0`
of any directed threefold optimizer. There are twenty directed centers,
paired into ten unoriented axes. Fold the receiver into the closed
three-wall chamber using a proper body rotation and normal reversal, as
in [CELL_PROOF.md](CELL_PROOF.md). Those operations preserve the entire
containment problem and its original proper relative rotation.

The checker regenerates the sixty proper rotations and their 3,600
original vertex images. It checks the three chamber-wall reflections in
the signed body group. Every other signed threefold center has a negative
unit inward-wall component with square at least

\[
                          (2-\phi)/3>d_0^2.
\]

Consequently the folded closed cap is centered at `n0`. With
`n0_z>4/5` and `||B||<5/4`,

\[
 n_z>4/5-d_0=7/9,\qquad
 \|u-B\|\le(1+\|B\|)d_0/n_z<3d_0<1/10.
\]

Every other chamber cell has chart `y<=D_y`, while `B_y-D_y>1/10`.
Hence the entire folded cap is in closed `ABD`. All inequalities retain
their strict separation at the closed cap boundary.

The `R`-Lipschitz property of `f`, with `c0>4/7` and `R<9/2`, gives
`F>4/7-(9/2)d0=33/70`. The checker proves `(33/70)^2>beta` exactly.
The source-normal chord is at most

\[
                         a_*=(23/10)d_0=23/450.
\]

Using `kappa<13/10`, `h<17/4` and `R<9/2`, the monotonic expression (2)
is bounded by

\[
 E_* =\frac{(13/15)d_0+(3/2)d_0^2+(17/16)a_*^2}{1-a_*^2/4}
                  =73793/3237884<77/1000,
\]

and an exact outward root enclosure gives

\[
       \Theta_3\le\Theta_*=
                   7756106076773/100000000000000.                 \tag{14}
\]

It remains to bound the actual torque hull at **every** receiver. Normalize
the persistent torques to the unit normal: `Tj(n)=vj cross(ej cross n)`.
The complete center hull has sharp chart radius `phi-1`. The exact identity

\[
 \|B\|^2=3(2-\phi)
 \quad\Longrightarrow\quad
            r_{10}(n_0)=(\phi-1)/\|B\|=c_0>4/7                  \tag{15}
\]

is checked directly. Since `||vj||=R` and `||ej||=2`,
`||Tj(n)-Tj(n0)||<=2R||n-n0||`. Taking maximum supports and then the
minimum over all unit torque directions gives the continuous bound

\[
            r_{10}(n)\ge c_0-2Rd_0>4/7-9d_0=13/35.             \tag{16}
\]

This is a support-function argument on the entire cap, with no assumed
facet persistence or sampled receiver cover. It yields the exact margin

\[
 r_{10}(n)-R\Theta_3>
 \frac{13}{35}-\frac92\Theta_*
   =\frac{31365317163301}{1400000000000000}>1/50.                  \tag{17}
\]

Criterion (3) is homogeneous in `u`, so (17) verifies its final inequality.
This proves (1) on the entire closed cap. Undoing the body fold and normal
reversal transports both left cosets and the original unrestricted source
parameters. The caps of radius `1/100` and the preceding four-piece
triangle remain valid; the full complementary receiving sphere is open.

## 7. Reproduction, trust, operational history and literature

From repository root, Python 3.11+ standard library, with all numerical
threads one, run

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/balanced_receiver_certificate.py --self-test
```

Every output byte must match
[balanced_receiver_expected.json](balanced_receiver_expected.json), SHA256
`65561ab22beb5addc09e3f62d60eaa064d8d431ea90377365161d89e2b0fb86b`.
The normal replay took 5.376 seconds and 21,304 KiB peak child RSS. The
optimized publication-copy replay took 5.923 seconds and 24,572 KiB; every
output byte matched. Explicit checks remain active under `-O -B`.

The checker regenerates the complete center polygon and 720 original
support checks, all 360 long-edge height/gap comparisons and 216 excess-height
enclosures; the three proper axial gauges, all six signed plane actions;
24 signed endpoint/gauge triples, 72 actual preimages and 432 complete
symmetric tensor entries. Canonical regenerated moment-record SHA256 is
`711511d6aec8aa3f7e57c6dc1e2552ce4653d6ce74008c7dd079d3ed6d54c3e2`.
It verifies the full proper body group, nineteen other-center wall tests,
the fifteen half-turn zero-height witnesses, 1,800 persistent actual
probe/vertex/corner supports, 120 possible center triples/1,200 support
tests, all fifteen center facets, positive stress and 540 full-pool center
supports. The orthogonal composition identity, its 81 quaternion/matrix
arithmetic audits, all ten concavity/roll comparisons and every radical
cap bound are directly checked. The audits do not replace the continuous
averaging, full-roll, frame or support-function proofs.

Nine malformed controls reject unequal signed source heights, missing
preimages, repeated normals, a false symmetric moment, incomplete or
improper axial gauges, an unsupported `1/40` cap under these sufficient
bounds, an incorrect normalized center radius and a false dependency digest.
Failure of sufficient bounds does not decide the modified mathematical case.
The complete moment/witness records are regenerated and checked; hashes
avoid a large published corpus, which is not a hidden proof input.

The checker pins the preceding orthogonal expected SHA256
`6eaaf32e88a8b46e1732c159fd062f2b6fadbe12c8925e9475ce130a20cee366`,
actual-hull `b74584ad4ed343925de777ca5b98f1217c95fdb08f073920acee28c8cd8aaaac`,
directional `cda8f8555f21e41b412478adb776416a9161828e53f5dce77f51376adc250b33`,
and adaptive `53c852471e2d787b8958f01cc6f6e1b5c210ce3ee2b3a524ddbe1a59e9514e98`.
These source-backed predecessors are explicit dependencies. Their complete
old computations are not claimed rerun here; all new hypotheses are
directly regenerated. A full directional-parent attempt two passes earlier
timed out at 55 seconds and remains incomplete. Its unchanged published
source has prior completed normal and optimized replays. No expensive
retry or raised resource limit is made, and the incomplete attempt supplies
no mathematical verdict.

Trust includes the standard model and exact `Q(phi)`/Fraction kernel,
the cited complete global source-region/coercivity reduction, actual proper
gauges, and the continuous moment, transport, full-roll, frame, exponential
remainder, closed-equality, chamber and support-function arguments above.
All radical grid endpoints are checked by squaring. No floating-point
passage search, solver verdict or incomplete cover is a theorem premise.

Current primary status was checked on 2026-09-30 against
[Steininger--Yurkevich's RID discussion](https://arxiv.org/html/2508.18475#S9.SS1),
[Zeng's retained conjecture](https://arxiv.org/html/2604.26531), and
[Gosain--Grimmer's named-solid tables](https://arxiv.org/html/2509.08190).
They retain the global RID question; the last tables also retain the
other unresolved named solids. The projection formulation is
[Steininger--Yurkevich](https://arxiv.org/html/2112.13754).
Bounded primary checks do not establish historical priority.

Complementary full proofs/checkpoints read include **six-rupert-1,
researcher**'s [adaptive deltoidal area and full-roll theorem](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/adaptive_area_proof.md),
source `2a0eb5428787e69876ac4652f7d8c192c07fa9e2`, graph
`bafkreiejtc4l7y4ubwokktltjem2nb2rviz3ds3jld4yavourzxaacwc4m`, and
**six-rupert-2, researcher**'s
[J77 directional receiver theorem](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_directional_receiver_domains/PROOF.md),
source `f7cfae81911e86c562b226a04f7966989812f94d`, graph
`bafkreihbeoxtt3rmagrfbwqkn47u3oqm6jt55v7ffayh5yqnxt72fo6eym`, and
new [sharp J77 regional spectrum](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_sharp_region_gap/PROOF.md),
source `2def43a003a2a692571ae654c543517b1cb20e6b`.
Its committed graph reference is
`bafkreieoes3bbhpwp53w22xek5ky7mrwmhcdxnb37fex5c2gox4zalouua`
at height 7438.
The latter sharpens its winning-source gap by actual signed-cell maxima;
RID's existing proof already scores maxima separately by its complete
436-region classification. No J77 threshold transfers to RID.
The final refresh also read six-rupert-1's
[tangential area and directional transport proof](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/directional_area_proof.md),
source `7d6c787f4760e4038e23256c6a6e396ec73b38ec`, graph
`bafkreihb55kg5d5tclfow7alxh6zseg7hpjyhanejzjatmlt6vn2cxztau`
at height 7454. It uses the preceding RID orthogonal-composition lemma
with a separately derived proper deltoidal frame and certifies a whole
closed half-cell by positive torque-facet polynomials. Its area coercivity,
support constants and receiver domain are derived for that body and are
not premises here. This directed use of the earlier RID lemma is context
for future whole-domain certificates, not review of the present result.

All three named global questions remain open. Their full-roll and
translation-balanced methods are complementary context, not premises of
the new RID moment identity. **six-reviewer-1**'s
[earlier J77 review](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_all_source_review1/README.md),
source `e78fafefba916f04dc61ec7e2f9556e1469776a1`, graph
`bafkreialgb2n4e3yjo77r7gkgmaclia4evw2zkww7rgrzsw3ywznxopfum`,
does not review this RID result or the newer J77 extensions. No reviewer
was directed or asked for a verdict. The orchestrator remains the hub.

The next frontier is a substantially larger receiver cover under (3),
using exact winning-region geometry and actual torque hulls, or new
source-class comparison below `beta`. The complete winning-region sphere,
global non-Rupert theorem and an exact strict passage remain unresolved.
