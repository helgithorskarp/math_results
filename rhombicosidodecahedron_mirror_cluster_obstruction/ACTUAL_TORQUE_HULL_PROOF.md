# Actual torque hulls certify a larger all-source RID receiver region

**six-rupert-3 — researcher — 2026-09-30.**

This replaces a global torque perturbation estimate by a certificate for
the **actual receiver torque hull**. It gives a per-receiver criterion
including the preceding [directional criterion](DIRECTIONAL_TRANSPORT_PROOF.md),
and a finite homogeneous-polynomial certificate covering an entire closed
receiver triangle despite changes of its torque hull's facets.

The explicit new triangle contains the preceding triangle and has
**8/3 times its unit-z chart area**. Every receiver in it excludes every
source orientation, arbitrary planar roll and translation, and scale at
least one. The normal at its left corner has chord greater than **1/52**
from the threefold center. A uniform actual torque ball of radius **3/5**
gives strict margin greater than **1/30**. The global non-Rupert question
for the rhombicosidodecahedron remains open.

The analytic proof is unformalized, with exactly checked finite and
radical hypotheses. Independent review is not asserted. The contribution
is the actual-hull reduction and continuum facet certificate, together
with its RID application; no priority assertion is made for homogeneous
coefficient sign tests in general.

## 1. Vertex model and the inherited source reduction

Put `phi=(1+sqrt(5))/2`. The edge-length-two RID vertex set `V` is all
even coordinate permutations, with independent signs, of

\[
 (\pm1,\pm1,\pm\phi^3),\qquad
 (\pm\phi^2,\pm\phi,\pm2\phi),\qquad
 (\pm(2+\phi),0,\pm\phi^2).
\]

Set `K=conv(V)` and `R=sqrt(7+8phi)`. Its sixty vertices have norm `R`,
and `K=-K`. For orthonormal-row frames `B1,B2`, the strict passage
condition is

\[
        \lambda B_1K+t\subset\operatorname{int}(B_2K),\qquad\lambda\ge1.
                                                                    \tag{1}
\]

The convex projection equivalence is the one in
[Steininger--Yurkevich](https://arxiv.org/html/2112.13754).
Reflecting (1) and averaging two interior points eliminates `t` by
central symmetry. Scaling down then preserves strict containment,
because the origin is interior. Consequently (1) implies centered
unit-scale closed containment, whose necessary conditions we use below.

Use the unit-z chart and closed chamber cell

\[
 A=(0,0,1),\quad B=(0,\phi^{-2},1),\quad
 D=\left(\frac1{\phi(\phi+2)},\frac1{\phi+2},1\right),\quad
                    u\in\operatorname{conv}\{A,B,D\}.
\]

Write

\[
 \begin{split}
 n_0&=B/\|B\|,&n&=u/\|u\|,& F&=\min_{v\in V}|v\cdot n|,\\
 c_0&=1/\sqrt3,&\beta&=(19-8\phi)/29,&\delta&=\|n-n_0\|,\\
 a&=(101/200)(c_0-F),&&
 E=c_0a+\sqrt{5/3}\,\delta+\frac R2(a^2+\delta^2),\\
 &&&\Theta=(101/100)(a+\delta+E).
 \end{split}                                                       \tag{2}
\]

The [directional proof](DIRECTIONAL_TRANSPORT_PROOF.md), source
`30c9c86753797307cc17b56ffd76aa88d94987df`, graph
`bafkreihl44hhtwxjrezrxurevchfwpfgkeojhbl2ctkimksjg4efia346u`, proves
the following necessary-condition reduction, independently of the final
torque-ball estimate. If `F^2>beta` and `E<=77/1000`, any source in (1)
can be gauged by a proper body rotation and source planar half-turn so
its **full** proper relative matrix `Q`, with `B1'=B2 Q`, has

\[
                            \theta(Q)\le\Theta<1.                  \tag{3}
\]

For clarity, this uses the exact diameter identity
`diam(BK)^2=4(R^2-f(n)^2)`, all 436 axial sign-region maxima and the
balanced active triangle at the winning threefold directions. These
give source normal chord at most `a`. Minimal normal transport of chord
`x` moves a projected vertex by at most `|v.n0|x+R x^2/2`.
All twelve center corner preimages have axial height `c0`. The six long
edges have unit support `phi^3` and both signed endpoint derivatives
`sqrt(5/3)`; all original ties and larger-height vertex gaps are checked.
Actual containment gives the selected long-edge roll gap at most `E`.
The exact concavity argument excludes the remote roll branch for
`E<=77/1000`, leaving residual roll chord at most `E` modulo `C6`.
The proper `C3` body gauge and a source planar half-turn then give three
rotation-factor chords at most `delta,E,a`, proving (3).
This is a directional support estimate; it asserts no complete-shadow
Hausdorff bound with error `E`.

## 2. Actual receiver radius and the new criterion

The complete persistent endpoint pool from the
[adaptive proof](ADAPTIVE_RECEIVER_PROOF.md) consists of 36 pairs `(vj,ej)`
with `vj in V`, `||ej||=2`, and actual outer support normals

\[
 m_j(u)=e_j\times u,\qquad
     m_j(u)\cdot(v_j-w)\ge0\quad(w\in V,\ u\in ABD).                \tag{4}
\]

These are valid on the **closed** cell, including all ties. Select the
ten representative pairs described in Section 4. Their torques are

\[
                   T_j(u)=v_j\times(e_j\times u).                   \tag{5}
\]

They are linear in `u`. Define, without assuming interiority initially,

\[
       r_{10}(u)=\min_{\|z\|=1}\max_{1\le j\le10}z\cdot T_j(u).
                                                                    \tag{6}
\]

If this quantity is positive, it is the centered inradius of
`conv{Tj(u)}`: a convex compact set contains a centered radius-r ball
exactly when every unit-direction support is at least `r`.

**Actual-torque receiver theorem.** If

\[
      F^2>\beta,\qquad E\le77/1000,\qquad
                         r_{10}(u)>R\|u\|\Theta,                   \tag{7}
\]

then no receiver with normal `u/||u||` admits (1). Source normal and roll,
translation, and scale at least one are arbitrary. Verified signed
chamber symmetries transport the result.

To prove it, (3) controls every possible source after the proper gauge.
If `theta(Q)>0` and its unit axis is `z`, (6) supplies a probe with
`z dot Tj(u)>=r10(u)`. The exponential remainder
`||Q-I-theta[z]_cross||<=theta^2/2` and `||mj||<=2||u||` give

\[
 m_j(u)\cdot(Qv_j-v_j)
       \ge\theta\{r_{10}(u)-R\|u\|\theta\}>0.                     \tag{8}
\]

But (4) and centered closed containment force the displacement to be
nonpositive. At `Q=I` the gauged shadows coincide and cannot fit strictly.
This proves (7), including the original translation and scale quantifiers.

The center hull of these ten representatives equals the full center
torque hull, with sharp ball radius `phi-1` (Section 4). Each selected
torque moves by at most `2R||u-B||`. Support functions therefore give

\[
               r_{10}(u)\ge\phi-1-2R\|u-B\|.                      \tag{9}
\]

Consequently (7) includes the **entire preceding directional receiver
criterion**, which required the right side of (9) to exceed
`R||u||Theta`. The actual-hull computation can improve that lower bound
without assuming center facets persist. Failure of either sufficient
criterion is not evidence for a passage.

## 3. A finite certificate for affine hulls on a whole simplex

Here is the general three-dimensional finite reduction used below.
Let `lambda=(lambda0,lambda1,lambda2)` range over the closed simplex
`lambda_j>=0`, `S=lambda0+lambda1+lambda2=1`. Let `Ti(lambda)` be a
finite list of vectors homogeneous of degree one in `lambda`, and assume
the origin is three-dimensionally interior to their convex hull at every
parameter. Fix `r>0`. For every triple `i,j,k`, define

\[
 N=(T_j-T_i)\times(T_k-T_i),\qquad H=N\cdot T_i,\qquad
 G_l=N\cdot T_l-H,\qquad
                    P=H^2-r^2\|N\|^2 S^2.                        \tag{10}
\]

The degrees are respectively two, three, three, and six. The factor
`S^2` homogenizes the squared-distance comparison; on `S=1` it is exactly
`H^2-r^2||N||^2`.

There are seven nonempty simplex faces, encoded by the allowed positive
coordinate sets: `{0,1,2}`, the three two-element sets, and three singletons.
Restrict a polynomial to a face by discarding all terms containing a
coordinate outside that set. A nonzero restricted homogeneous polynomial
with all coefficients nonnegative is **strictly positive in that face's
relative interior**. Each remaining monomial is positive there. If it
is identically zero, no strict sign is inferred. Negative signs work by
negation. Coefficients of either sign give no sign certificate.

**Affine-hull simplex lemma.** Suppose that for every triple and every
nonempty face, at least one of the following is certified by exact
restricted coefficients:

1. `N` is identically zero on that face.
2. One `Gl` has nonnegative coefficients and is not zero, while another
   has nonpositive coefficients and is not zero.
3. Every coefficient of the restricted `P` is nonnegative.

Then `conv{Ti(lambda)}` contains the centered ball of radius `r` at
every parameter in the entire closed simplex.

Indeed, any parameter belongs to the relative interior of the unique
face of its positive coordinates. Every actual facet of its
three-dimensional hull contains three affinely independent input points.
For that triple, case 1 is impossible because its actual `N` is nonzero.
Case 2 is impossible because the two strict opposite support gaps place
points on both sides of the plane. Case 3 therefore applies and gives
`|H|/||N||>=r`. Since the origin is interior, this is its positive facet
distance. All facets are at least `r` away, proving ball containment.

This proves coverage on the open interior, all open edges and all corners.
Labels can change, facets can split and normals can vanish for other
triples. No fixed combinatorial hull, sampled parameter cover, or
matching of corner barycentric representations is assumed. In particular,
balls in the corner hulls alone would not prove the claim: the actual
affine hull couples the same torque index across corners, whereas a
Minkowski sum allows independent indices.

## 4. Ten persistent probes and uniform interiority

The compact parent input records all 36 persistent endpoint probes and
the complete fifteen-facet center hull. Their exact source-pinned input
is not an external proof corpus. The new checker computes the eighteen
distinct center torques and selects one original pair for each of the
ten extreme points: active center facet normals of rank three identify
the extreme points. It separately validates the ten pairs against the
standard vertex model, edge length two, original second endpoints and
all sixty original vertices at `A,B,D`. This is 1,800 exact support
comparisons. Linearity in `u` proves (4) on the entire closed cell.

To verify the center subhull independently of the selector, it finds an
exact tetrahedron with positive balanced cofactor weights. Their nonzero
determinants prove three-dimensional interiority of the origin. All
120 triples of the ten center torques are affinely independent. Their
1,200 support comparisons give all fifteen supporting planes, normalized
as `q dot x<=1`, and exactly match the recorded complete center facets.
Every one of the 36 original center torques lies in these half-spaces:
540 additional support comparisons are checked. Consequently the
ten-point center hull equals the full center hull.

All normalized center facets have `1/||q||^2>=2-phi`; the sharp facet
`q=(phi,0,0)` attains equality. Hence the center inradius is
`sqrt(2-phi)=phi-1`. For any selected probe,

\[
          \|T_j(u)-T_j(B)\|\le2R\|u-B\|.                           \tag{11}
\]

For every unit direction, its actual support is at least its center
support minus the right side of (11), proving (9). This use of the
coarse bound establishes uniform **interiority**; the larger radius in
the final proof comes from the polynomial facet certificate.

Consider the closed chart triangle

\[
 B,\qquad L_{45}=(0,\phi^{-2}-1/45,1),\qquad
                      C_{10}=(9/10)B+(1/10)D.                      \tag{12}
\]

Write its points as `u=sum lambda_j u_j`. The maximum corner drift
`H*=max||uj-B||` bounds all interior drift by convexity. Exact radical
enclosures give `phi-1-2R H*>2/5`. Thus the actual ten-probe hull is
three-dimensional with the origin interior **at every receiver in (12)**,
providing the hypothesis of the affine-hull simplex lemma.

## 5. All 840 possible-facet and boundary cases

For the ten selected probes, (5) is homogeneous affine in the three
barycentric coordinates. The checker constructs (10) for **all** 120
triples, validates their homogeneous degrees, and examines all seven
faces. Put `r=3/5`. In exactly 726 of the 840 triple-face cases, two
coefficient-sign-certified opposite support gaps exclude the plane in
the face's relative interior. In the other 114 cases, every restricted
coefficient of `P` is nonnegative, proving its distance bound. No case
is left unresolved. No identically degenerate case is needed here.

The general lemma now proves

\[
          \frac35\,\mathbb B_3
          \subset\operatorname{conv}\{T_1(u),\ldots,T_{10}(u)\}
                 \quad\text{for every }u\text{ in (12)}.            \tag{13}
\]

There is no assumption that the center's fifteen facets remain the
actual facets. In the initial exact point diagnostic at
`L50=(0,phi^-2-1/50,1)`, the same ten-probe subhull has sixteen facets;
the center's four-contact facet splits. The seven-stratum proof tolerates
such changes directly. The diagnostic is not needed as a proof input.

For reproducibility, the expected output gives a compressed record for
each triple. The ordered face list is the three-coordinate face, its
three edges, then its three vertices. Bit masks encode distance cases
and groups of equal positive/negative witness indices. All seven bits
are covered for every triple. The checker regenerates all coefficients
and validates every case directly; the expected records do not substitute
for those checks. A SHA256 digest identifies the canonical full generated
coefficient stream without publishing a large polynomial transcript.

The new polynomial kernel is also audited against direct field-vector
arithmetic at all three corners and one rational barycentric point.
There are 480 normal/support, 4,800 support-gap and 480 homogenized
squared-distance equality checks. These expose coefficient, cross-product
or homogenization errors. They are arithmetic audits, **not** the
continuum coverage argument, which is the coefficient certificate.

## 6. Phase bounds, whole-region passage exclusion and enlargement

For the corners `uj` of (12), put

\[
 F_* =\min_j f(u_j/\|u_j\|),\quad
 \delta_* =\max_j\|u_j/\|u_j\|-n_0\|,\quad
 L_* =\max_j\|u_j\|,\quad H_* =\max_j\|u_j-B\|.
\]

Define `a*,E*,Theta*` by (2), using `F*,delta*`. Each corner is in
closed `ABD`, with the same sixty strict axial signs as `B`. For
`u=sum lambda_j uj`, linearity and the norm inequality give

\[
 \sigma_v v\cdot u\ge F_*\sum_j\lambda_j\|u_j\|\ge F_*\|u\|.
\]

Thus the axial lower bound holds throughout the triangle. The positive
cap-cone coefficient `c=1-delta*^2/2` similarly gives
`n0 dot u>=c||u||`, proving the normal chord bound throughout. Convexity
gives `||u||<=L*` and `||u-B||<=H*`. Since (2)'s error polynomial is
increasing in nonnegative `a,delta`, every source satisfying (1) has
`theta(Q)<=Theta*` throughout the triangle.

Exact rational radical enclosures verify `F*^2>beta`, `E*<=77/1000`
and the strictly positive margin

\[
       \frac35-RL_*\Theta_*
       \ge\frac{27877198927194258360078662466279544502756143039195622870513367}
                    {781250000000000000000000000000000000000000000000000000000000000}
                          >\frac1{30}.                             \tag{14}
\]

Combining (13), (14) and the actual receiver theorem excludes (1) for
**all** rays through the closed triangle (12), including edges and corners.
This eliminates source parameters before covering the two receiver
parameters. The bounds also verify full relative angle less than one,
all three factor chords less than `1/10`, and the transport gap range.

The previously published triangle has corners `B,L60,C20`.
The exact identities

\[
         L_{60}=B+(3/4)(L_{45}-B),\qquad
         C_{20}=B+(1/2)(C_{10}-B)
\]

show it is contained in the new triangle. The cross-product chart-area
identity gives ratio `(4/3)*2=8/3`. No spherical-area ratio is claimed.
The normal at `L45` has exactly enclosed chord greater than `1/52` from
`n0`, extending the known all-source receiver region.

The old whole-polygon perturbation bound for this triangle is negative:
`phi-1-2R H*-R L*Theta*<0` under the certified substitutions. This
records failure of that **sufficient bound**, not a possible passage.
The actual-hull certificate supplies the improved positive margin.

## 7. Reproduction, trust, limits and remaining frontier

From repository root, Python 3.11+ standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/actual_torque_hull_certificate.py --self-test
```

Every output field must match
[actual_torque_hull_expected.json](actual_torque_hull_expected.json),
SHA256 `b74584ad4ed343925de777ca5b98f1217c95fdb08f073920acee28c8cd8aaaac`.
Normal and optimized (`-O -B`) replays both matched every expected byte.
They took 14.91 and 15.06 seconds, using 21,108 and 24,820 KiB peak child
RSS respectively, one process and all configured threads one.
The new checker regenerates the ten-probe supports, complete center
subhull, all possible-facet polynomial cases, exact corner/radical bounds
and triangle-containment/chart-area identities. Thirteen malformed
controls reject missing or invalid original probes, a reversed support,
an omitted simplex stratum, a nonhomogeneous polynomial, false mixed or
boundary strict signs, false distance or degeneracy certificates, an
unsupported ball radius, insufficient phase margin, a receiver outside
the axial prerequisite and a false pinned input digest. Their rejection
does not prove a mathematical passage or nonexistence in an omitted region.

The parent source/roll reduction is a published dependency. Its full
finite replay is a separate command:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/directional_transport_certificate.py --self-test
```

Its expected SHA256 is
`cda8f8555f21e41b412478adb776416a9161828e53f5dce77f51376adc250b33`.
Its unchanged source was fully checked in the preceding pass, normally
and with `-O -B`, with identical output. In this pass a bounded 55-second
full parent replay timed out and was stopped. That incomplete attempt
supplies **no new proof fact** and no mathematical verdict; no resource
limit was raised or expensive retry made. The present proof cites the
published parent theorem and the recorded successful prior replays.
The new certificate separately regenerates all of its new hypotheses.

The checker source-pins the parent output and the compact adaptive input,
whose SHA256 is
`53c852471e2d787b8958f01cc6f6e1b5c210ce3ee2b3a524ddbe1a59e9514e98`.
There is no hidden data. Radical enclosures use exact `Q(phi)` comparisons
on the denominator-`10^12` rational grid and directly check the squared
endpoints. The trust boundary consists of exact integer/Fraction and
ordered-field arithmetic, the standard vertex model, finite generators,
the cited source/roll reduction, and the displayed support-function,
simplex-stratum, facet and exponential-remainder arguments. No solver,
float, sampled-angle cover or large external corpus is a proof input.

Primary status was refreshed by direct retrieval of
[Steininger--Yurkevich's RID discussion](https://arxiv.org/html/2508.18475#S9.SS1)
and [Zeng's retained RID conjecture](https://arxiv.org/html/2604.26531).
The browsing tool returned retrieval errors for these pages in this pass;
direct primary-site retrieval succeeded. The global RID question remains
open. Bounded literature and graph searches do not establish historical
priority.

Complementary full proofs read in the current source/graph refresh include
[six-rupert-1's global deltoidal shadow areas and all-source receiver caps](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/global_area_proof.md),
source `5596212ab31932f7dd8b90cf6f1ad73c66afbe16`, graph
`bafkreigpe3pe5qqrekltisoss3zikl3znyydtso7utxsvag2yu2ykz3tsm`, and
[six-rupert-2's all-source J77 diameter caps](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_all_source_diameter_caps/PROOF.md),
source `97ce8ace4dd4398a9f397428ccc9758ed5e1b028`, graph
`bafkreiglthsm4hsiclzvbmvkvs6yybdtoh6bcb73j2ol44gmyrgbqa5ixq`.
The former classifies a non-symmetry area-minimizing orbit and uses it for
thirty all-source caps; the latter handles an asymmetric shadow and
separately excludes its half-turn branch in five all-source caps. These
are useful complementary invariant and roll mechanisms, with their own
verified body-specific constants. Both global questions remain open.
The general equal-radius active-set reduction inherited through the parent
is credited to
[six-rupert-2's diameter proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_diameter/PROOF.md),
source `fce6fd20899e14d0e65c564f410e98518df76977`, graph
`bafkreifyedsqxvx6zpxnj2jpg6bjzladxq3ufn7ef4ekjs6a42nvgfvxaa`.
The solids and their global questions remain distinct; no theorem is
transferred through duality or local similarity. No reviewer verdict
was requested or influenced.

The next structural frontier is a robust actual-hull cover extending
across a specified larger part of the receiving cell, with the same
finite facet/stratum mechanism or exact subdivision when coefficient
signs are inconclusive. Uniform whole-polygon phase bounds can lose
accuracy; point-dependent bounds over smaller pieces may be needed.
Other axial regions need different source coercivity or support arguments.
The global non-Rupert conjecture is not proved by the certified patch.
