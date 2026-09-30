# All diameter-threshold receivers exclude strict Rupert passage

**six-rupert-3, researcher, 2026-09-30.** This is a complete, unformalized
argument with exact finite and interval certificates. It has not received
independent review. The global rhombicosidodecahedron Rupert question remains
**open**. The strict receiving region below the threshold is untreated.

Let `K=-K` be the standard edge-two rhombicosidodecahedron, with the sixty
original vertices `V` generated in [verify.py](verify.py). Put

\[
 \phi=(1+\sqrt5)/2,\quad R^2=7+8\phi,\quad
 f(n)=\min_{v\in V}|v\cdot n|\ (\|n\|=1),\quad
 \beta=(19-8\phi)/29.
\]

Let `G` be its verified sixty-element proper vertex rotation group,
`P_n` the orthogonal projection onto `n^perp`, and `J_n=2nn^T-I` the
proper half-turn about the unit normal `n`. Containment below always means
containment of the actual full projected convex bodies, with arbitrary
proper spatial rotation `Q`, planar translation `t`, and scale `lambda>=1`.

**Theorem.** For every unit receiver normal with `f(n)^2>=beta`,

\[
             \lambda P_n QK+t\not\subset\operatorname{int}(P_nK).
                                                        \tag{1}
\]

Consequently every strict Rupert passage must have

\[
 f(n)^2<\beta,\qquad
 \operatorname{diam}(P_nK)^2>(736+960\phi)/29.              \tag{2}
\]

The sixty isolated nonwinning threshold axes form **two proper-body
projective orbits of thirty**, represented by the rays

\[
 \ell=(0,1,-3-3\phi),\qquad
 h=(0,1,(3\phi-1)/11).                                    \tag{3}
\]

For a receiver on the `ell` orbit, every closed containment has `lambda=1`,
`t=0`, and exactly the 120 proper orientations `G union J_n G`, all giving
equal shadows. For the reference receiver `n=h/||h||`, the complete closed
classification instead comprises the following **four disjoint LEFT cosets**:

\[
              G\ \cup\ J_nG\ \cup\ CG\ \cup\ J_nCG.          \tag{4}
\]

Here `C` is the proper rotation by 36 degrees about `(0,phi,-1)` defined
exactly in Section 6. There are 240 orientations. The first two cosets give
equal shadows; the last two give unequal closed containment of the lower-area
threshold shadow. All eight maximum-circle points are shared, so these
containments are **not strict interior passage**. At `n=g h/||h||`, replace
`C` by `gC` in (4). Normal reversal changes no shadow or coset set.

## 1. Previously established inputs and scope

[GLOBAL_CAP_PROOF.md](GLOBAL_CAP_PROOF.md) establishes

\[
 \operatorname{diam}(P_nK)^2=4(R^2-f(n)^2)                 \tag{5}
\]

and the complete spectrum of 436 projective strict axial sign regions.
Ten winning regions have maximum squared height `1/3`; every other region
has maximum at most `beta`; exactly sixty nonwinning regions have maximum
`beta`. Its exact candidate enumeration uses 17,140 raw directions, 4,681
projective candidates and 140,430 candidate dot products. The pinned compact
output has SHA256
`69efa7e7cc4fbc359ce5481fc7eaa82c9779a51d56464597232e520663667fa8`.

[WINNING_RECEIVER_PROOF.md](WINNING_RECEIVER_PROOF.md) already excludes
strict passage for the entire closed winning superlevel components
`f(n)^2>=beta`, including every receiver with `f(n)^2>beta`. It gives their
closed classification `lambda=1,t=0,Q in G union J_nG`. The pinned output is
`f2796de9c7123917dbd845c651179216ca595545c30e6a7cdb48ea7bf6312ba3`.
This result does not cover the sixty nonwinning threshold axes; those are
the new receiving directions in the present proof.

The same winning proof supplies source coercivity. Choose its threefold
reference ray `B=(0,phi^(-2),1)`, set `n0=B/||B||`, and `c0=1/sqrt3`.
The six actual original vertices of positive height `c0` have tangent
projections whose convex hull contains the centered disk of squared radius
`8/3+4phi>9`. Hence, for a winning source unit normal `k=z n0+w`,

\[
 f(k)\le c_0z-\sqrt{8/3+4\phi}\,\|w\|.
\]

If `f(k)>=sqrt(beta)`, its winning signed region has `z>0`, and

\[
 a=\|k-n_0\|\le{101\over300}(c_0-\sqrt\beta)<1/24.        \tag{6}
\]

For clarity, `sqrt(beta)>57/125`, `c0<289/500` first give `||w||<1/20`
and `z>199/200`. The identity `a^2=2||w||^2/(1+z)` then gives (6).
These are signed-region estimates, not assumptions of local source rotation.
An actual proper body rotation gauges every winning source to this reference.
The new checker regenerates **every entry** of the predecessor's complete
six-point tangent hexagon and checks it against the pinned output.

The directional movement estimate from
[DIRECTIONAL_TRANSPORT_PROOF.md](DIRECTIONAL_TRANSPORT_PROOF.md), Section 2,
is rederived in Section 3 below. No previous small-roll gate, receiver torque
certificate, or C3 receiver averaging is required for the new threshold
receivers. The new circle argument covers all rolls directly.

## 2. The sixty nonwinning threshold axes, with uniqueness

The checker generates the actual proper vertex group and the two projective
orbits of (3). Each has thirty distinct axes, with sixty directed normals
including their reversals. Its directed stabilizer has order one and its
projective stabilizer order two. The orbits are disjoint. All sixty axes
belong to distinct strict signed regions and satisfy `f^2=beta`.

For **every** axis, not only the representatives, the checker finds a
strictly positive balance of three original positive active vertices:

\[
       \sum_{j=1}^3 w_jv_j=y=\sqrt\beta\,k,
       \qquad w_j>0,\quad\sum_jw_j=1.                     \tag{7}
\]

Here `k` is the directed unit optimizer and `y` is encoded over `Q(phi)`
without a new square root by using the original unnormalized ray. All four
positive active vertices are checked. For any other unit `u` in the same
strict signed region these fixed original vertex heights stay positive, so

\[
 f(u)\le\min_j v_j\cdot u\le\sum_jw_jv_j\cdot u
       =\sqrt\beta\,k\cdot u\le\sqrt\beta.                \tag{8}
\]

Equality at the regional maximum forces `u=k`. Thus these are sixty
distinct **unique** regional optimizers. The pinned global spectrum has
exactly sixty nonwinning beta-level regions; no further nonwinning
`f^2=beta` directions can exist. This uses the published complete spectrum,
with sixty new individually verified balances and strict sign keys. It does
not replace the global enumeration by an unsupported orbit count.

For each reference shadow the checker regenerates all sixty distinct
original projections, its sixteen convex hull corners, and all eight points
on the maximum-radius circle

\[
                        \rho_\beta^2=R^2-\beta.             \tag{9}
\]

Every one of the sixteen actual supports is tested against all sixty
original vertices: 960 comparisons per receiver, 1,920 altogether.
Consequently the later inequalities involve the actual receiving polygons.

## 3. Transporting twelve actual source corners

The full reference shadow `P_n0 K` has twelve hull corners on the circle
of squared radius `R^2-1/3`. Each corner `p` has exactly one original vertex
preimage `v` and `|v dot n0|=c0`. The checker verifies the full preimage
list and all 720 source edge/original-vertex support comparisons.

Let `A` be the minimal proper normal transport taking `n0` to a winning
source normal `k`, with chord `a` from (6). Resolve an original vertex in
the transport plane as `v=zeta n0+chi t+omega b`. If the transport angle is
`alpha`, direct rotation gives

\[
 P_{n_0}(A^T-I)v
   =\{(\cos\alpha-1)\chi-\sin\alpha\,\zeta\}t.
\]

Since `sin(alpha)<=a` and `1-cos(alpha)=a^2/2`, the twelve actual corner
preimages therefore satisfy

\[
 \|P_{n_0}A^Tv-p\|\le c_0a+Ra^2/2
   <{289\over500}{1\over24}+{9\over4}{1\over24^2}
   ={2687\over96000}=:\eta.                              \tag{10}
\]

For an arbitrary proper source rotation `Q`, first gauge its normal by a
body symmetry so that `k=Q^T n` is in the reference winning region. Then
`QA` takes `n0` to the receiver's directed normal. On the oriented tangent
planes it induces an arbitrary proper planar roll `W`. The actual source
contains the twelve points `QA(P_n0 A^T v)`, each within `eta` of `Wp`.
Indeed `P_n Qv=QA P_n0 A^T v`. Thus any unit receiving support separating
the rotated center dodecagon by more than `eta` also separates an actual
original source vertex. We make no approximation claim about the other
forty-eight original vertices; they can only increase source support.

## 4. A validated cover of the entire roll circle

Use oriented orthonormal charts `(e1,n cross e1)` for the unit normal at
each reference, where `e1=(1,0,0)` and all reference rays have first
coordinate zero. For every unit outward receiver facet normal `m` with
support `b`, and every reference source corner `p`, write

\[
 m\cdot W_\theta p-b=A\cos\theta+D\sin\theta-b,
 \quad A=m_xp_x+m_yp_y,\quad D=m_yp_x-m_xp_y.              \tag{11}
\]

These are physical unit supports and physical source coordinates. The
checker encloses all square roots and field values with closed outward
`Fraction` intervals. For `q in Q(phi)`, the pinned exact root kernel uses
a fixed denominator `10^12`, verifies `0<=lo<=hi` and `lo^2<=q<=hi^2`
with exact field comparisons, and takes the positive branch. It encloses
`phi=(1+sqrt5)/2`, all positive normal/facet lengths, and reciprocals only
of intervals with strictly positive lower endpoint. Addition, multiplication,
division and sign-sensitive scaling preserve containment by elementary
interval arithmetic. No floating-point or solver output enters these bounds.

On each of the four **closed** circle quarters take all 129 parameters
`t=j/128`, `j=0,...,128`, and use the exact unit-circle coordinates

\[
             c={1-t^2\over1+t^2},\qquad s={2t\over1+t^2}, \tag{12}
\]

rotated by that quarter's multiple of 90 degrees. At every parameter, at
least one actual receiver facet and one actual source corner have interval
lower support gap greater than `3/40`. Every one of the `16*12` possibilities
is evaluated at all 516 cases: **99,072 evaluations per receiver**, or
198,144 for the two representatives. Exact witness records are regenerated;
their digests are

* `ell`: `aa2cbe4f5e9bf41156aeef17614e1c0fc6e08353c16bc3bfb6681e0728f7de95`;
* `h`: `5b134a20b52b53f3e7365d9fa9768b92e31a999e802da790cf849ee35261098d`.

This is a continuum cover, rather than a sampled premise. On a quarter
`theta=2 arctan(t)`, so `|dtheta/dt|<=2`. Every `t in [0,1]` lies within
`1/256` of a grid parameter. Hence every roll is within angular distance
`1/128` of one covered case; endpoints of adjacent closed quarters are
included. For a fixed actual source corner and unit facet, the gap in (11)
is Lipschitz in angle with constant at most `||p||<R<9/2`. Its loss from the
selected case is therefore less than `9/256`.

After both this whole-circle loss and the actual source-corner movement,
the chosen actual source support exceeds the receiving support by

\[
       {3\over40}-{9\over256}-{2687\over96000}
         ={569\over48000}>{1\over100}.                    \tag{13}
\]

The gap is in unit physical support, independent of the arbitrary original
roll. Therefore no winning source with `f^2>=beta` has even centered
unit-scale **closed** containment in either threshold receiver. Proper
body transport and directed normal reversal cover all sixty receiving axes.

## 5. Exhaustive closed comparisons between threshold source orbits

A closed containment in a threshold receiver forces `f(source)^2>=beta`
by (5) after the central-symmetry reduction in Section 7. Winning sources
are excluded by (13). By Section 2 every remaining source is a member of
one of the two nonwinning threshold orbits.

The source and target then have the same maximum radius `rho_beta` and
eight distinct maximum-circle points each. Every source circle point in a
closed receiving polygon must be one of its eight circle points: equality
in the Euclidean norm bound on a convex hull is possible only at an original
maximum-radius point, by strict convexity of that norm. Containment therefore
forces a bijection of the complete eight-point sets.

The exact proper alignment in Section 6 identifies their directed planes
and circles. Fix one aligned source circle point. A proper planar roll is
uniquely determined by its image, and there are exactly eight candidate
images. The checker tests all eight for **each of the four ordered
source/receiver orbit pairs**, without angular sampling. Only the zero and
180-degree rolls preserve the complete circle. For both surviving rolls it
tests all sixty original projected source points against all sixteen full
target facets: 960 inequalities per roll, **7,680 total**.

The results are:

| Source orbit | Receiver orbit | Surviving circle rolls | Full containment |
|---|---|---|---|
| `ell` | `ell` | zero, half-turn | equal shadows |
| `ell` | `h` | zero, half-turn after proper alignment | unequal closed containment |
| `h` | `ell` | zero, half-turn after proper alignment | neither is contained |
| `h` | `h` | zero, half-turn | equal shadows |

For the failed `h` to `ell` cases the exact minimum original support gap
is `4-4phi<0`. For the successful cross-orbit cases it is zero. The complete
physical areas satisfy

\[
 \operatorname{area}(P_\ell K)^2={137984+223232\phi\over145}
 <{29056+45888\phi\over29}=\operatorname{area}(P_hK)^2.     \tag{14}
\]

Thus the successful cross-orbit shadows are genuinely unequal. All eight
circle contacts remain on the target boundary, so (14) does not give a
strict Rupert passage.

## 6. Proper spatial alignment and the exact 36-degree turn

The complete four-original-active-vertex Gram alignment can be written

\[
 M=\begin{pmatrix}1&0&0\\0&a&-2a\\0&-2a&-a\end{pmatrix},
 \qquad a=(2\phi-1)/5=1/\sqrt5.
\]

It is orthogonal with determinant **minus one**. It is therefore not used
alone as an allowed proper source rotation. Put `H=-M` and
`L=diag(1,-1,-1) in G`. Then `H` and `R_beta=HL` are proper, and `R_beta` maps the
positive directed unit normals of `ell` and `h` to one another in both
directions. This is checked by applying `R_beta` to their nearest-point vectors
from (7), which have the same norm `sqrt(beta)`. Since `LK=K` and `K=-K`,
`R_beta K=HK=MK` as sets. Hence the proper alignment has exactly the shadow
comparison used above, with no improper orientation assumption.

An equivalent coset representative is the Rodrigues rotation about
`u=(0,phi,-1)`:

\[
 C=cI+(1-c){uu^T\over\phi+2}+s[u]_\times,
 \qquad c=\phi/2,\quad s=(\phi-1)/2>0.                  \tag{15}
\]

Here `[u]_cross v=u cross v`; `c^2+(phi+2)s^2=1`. Thus the actual positive
sine of the rotation angle is `s||u||`, and `c=cos(pi/5)` identifies a
36-degree proper rotation. All matrix entries lie in `Q(phi)`. The checker
verifies orthogonality, determinant one, `C notin G`, `C^2 in G`, `C^4 in G`,
and `C^5=R_beta`. In particular `CG=R_beta G=HG`, and the exact source construction is

\[
                     P_h(CK)\subsetneq P_hK.              \tag{16}
\]

The positive unit source normal of `R_beta` is the `ell` reference; that of `C`
is an actual body transform of it, because `C` and `R_beta` differ by a verified
body symmetry. This explains how the same unequal shadow containment is
realized by a 36-degree turn rather than the 180-degree representative `R_beta`.

For each fixed threshold receiver, proper source gauges and the two complete
circle-preserving rolls now give exactly the cosets stated in (4) and the
120-orientation lower-orbit case. The checker constructs all matrices in
these cosets and verifies every pair of cosets disjoint and each of size
sixty. At a body-transformed receiving normal, left multiplication by that
body rotation transports the complete orientation set, yielding `gCG` and
`J_n gCG`. This also shows independence from the chosen representative `g`.

## 7. Translation, scale, strictness, and the global conclusion

For centrally symmetric convex shadows `S=-S`, `T=-T`, a containment
`lambda S+t subset T` also gives `lambda S-t subset T`. Taking midpoints
gives `lambda S subset T`, and `S subset T` follows for `lambda>=1`.
The same midpoint argument preserves strict interior containment. Therefore
the winning-source exclusion (13) applies to arbitrary translation and scale.

For a surviving nonwinning threshold source, equal source and receiver
diameters force `lambda=1`. The receiver lies in the closed disk of radius
`rho_beta`. Let `p,-p` be any source maximum-circle pair. Containment implies
`||p+t||<=rho_beta` and `||-p+t||<=rho_beta`. Adding their squared inequalities
gives `2rho_beta^2+2||t||^2<=2rho_beta^2`, hence `t=0`. This completes the
closed classification including translation and scale.

Strict containment between compact planar bodies gives strict diameter
inequality. By (5), any strict source in a threshold receiver must satisfy
`f(source)^2>beta`, so it is winning and contradicts (13). Equivalently,
the complete closed classification contains only equal or boundary-touching
shadows. Combining this exclusion of all sixty nonwinning axes with the
previous closed winning receiver theorem proves (1). Equation (5) then gives
the strict global necessary condition (2). No conclusion is drawn for
receiving normals with `f(n)^2<beta`.

## 8. Reproduction, trust boundary and primary literature

Run with Python 3.11+ and the standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/threshold_receiver_certificate.py --self-test
```

Every output byte must match
[threshold_receiver_expected.json](threshold_receiver_expected.json), SHA256
`5516794048036b35ce73b63b0fdf5eb1c01620b260b11f87dfc401e0e5ccfeac`.
The checker regenerates all new finite hypotheses, all complete-circle
interval witnesses, all sixty balances and every circle correspondence.
It rejects fifteen malformed controls, including an improper alignment,
missing or reversed hulls, an omitted circle point, missing quarters/endpoints,
a duplicate parameter, reversed intervals, an invalid positive denominator,
false square-root bounds, a coarse cover with insufficient margin, and a
false excessive sample-gap threshold. Explicit `require` checks remain
active under `python -O`.

The all-sixty-axis/balance record digest is
`ad2b17f5b8c916c3b714a76909164a68769c0735d124d6c74e8b340cbfc80573`.
These records and the two complete-circle witness arrays are regenerated,
not external inputs or bulk proof corpora. The compact output records their
hashes, all sixty sign keys and directions, representative balances, the
complete hulls and circles, every surviving circle-roll result, and all
comparison counts. Floating exploratory roll samples are not proof inputs.

The ordinary final source replay completed in **12.256843 seconds**, peak
child RSS **22,872 KiB**, within a 55-second single-thread deadline. Its
complete output matched every relevant private exact prototype entry,
including all sixty full balances and both whole-circle witness outputs.
The root and field kernels, the two written predecessor theorems, and
inspection of this source remain trust dependencies. Neither this replay
nor its optimized replay is an independent algorithm or formal verification.
The full old global, directional and winning self-tests are not claimed
rerun by this entry point; their pinned published conclusions are explicit
dependencies. A historical full directional-parent 55-second timeout occurred
four passes earlier and is not a negative mathematical result. The initial
private threshold diagnostic's unsupported field `abs` call was corrected;
the complete exact diagnostic then finished and matched the published
candidate-evaluation digest. No current resource-limited run proves absence.

The final **publication-copy optimized replay** (`python3 -O -B`) completed
in **12.311304 seconds**, peak child RSS **25,776 KiB**, and matched every
expected byte. Its fifteen explicit malformed-input checks remained active.

The standard projection characterization and diameter monotonicity are
documented in [Steininger--Yurkevich](https://arxiv.org/html/2112.13754).
Their generic equal-radius active-set mechanism was explicitly credited in
the global parent to
[six-rupert-2's J77 proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_diameter/PROOF.md),
graph `bafkreifyedsqxvx6zpxnj2jpg6bjzladxq3ufn7ef4ekjs6a42nvgfvxaa`.
The sharpened J77 result, graph
`bafkreieoes3bbhpwp53w22xek5ky7mrwmhcdxnb37fex5c2gox4zalouua`,
is context for regional nearest-point uniqueness, not a transferred RID
certificate; see its
[source](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_sharp_region_gap/PROOF.md).
The complementary full deltoidal cell7 receiver result, graph
`bafkreiadruucamsuv7k3pwtvy42mkpzfaed5qclp445z5jxjeaj3aft73i`,
uses its own contact geometry; see
[the deltoidal proof](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/closed_cell7_proof.md).
Neither body's constants are imported here, and no teammate review verdict
is asserted.

The preclaim refresh at committed graph index **7518** also read
six-rupert-2's newer adaptive J77 criterion, graph
`bafkreigxs2bozl4ddvvryzxhvtbng3lf5daw3eh7uxzngo3t7b3q2hs4am`,
source `94e3ef96d8cdaff6fd6e0c6f0f7397b14c2f0a6b`,
[adaptive J77 proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_adaptive_roll_domains/PROOF.md).
Its exact inverse-roll branches and even translated half-turn stress are
useful next-frontier context; no J77 constants are premises of this theorem.
Six-rupert-1's newer individually normalized deltoidal supports,
source `0b8097a272e4b134b88869e6bf1a395b898da6c3`,
[normalized cap proof](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/normalized_cap_proof.md),
give another potential local remainder method. Its own durable report still
recorded graph acceptance as pending; this proof relies only on its published
source for context and does not assert its graph commitment. Bounded relevant
reports, actual graph feedback and pertinent repository commits since the
previous checkpoint were inspected; no incoming objection, correction,
retraction or independent review of this RID chain was found.

Primary current-status sources are
[arXiv:2604.26531](https://arxiv.org/html/2604.26531) and
[arXiv:2508.18475](https://arxiv.org/abs/2508.18475).
They still leave the standard RID question unresolved. This result is a
threshold-receiver theorem and a closed shadow classification, not a new
claim of global non-Rupertness or a resolved named-solid status. Priority
against all prior projection classifications is not asserted.
