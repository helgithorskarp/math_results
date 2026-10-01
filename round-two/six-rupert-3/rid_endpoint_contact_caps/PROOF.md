# All-source closed-rigidity caps at the RID mirror-arc endpoints

**six-rupert-3, researcher; 2026-10-01.** Written geometric proof with
exact finite hypotheses. Author-checked, unformalized and independently
unreviewed; historical priority is unasserted. The global standard
rhombicosidodecahedron (RID) Rupert question remains open.

## 1. Body, motions and the all-source conclusion

Let \(\phi=(1+\sqrt5)/2\), and let \(V\) be all independent signs and even
coordinate permutations of
\[
 (1,1,\phi^3),\quad(\phi^2,\phi,2\phi),\quad(2+\phi,0,\phi^2).
\]
Then \(K=\operatorname{conv}V=-K\) is the standard edge-two RID. The sixty
originals have \(R^2=7+8\phi<20\); \(G\subset SO(3)\) is its sixty-element
proper body group. Put
\[
 a=\phi^2,\quad c=2+\phi,\quad b=\phi^3,\quad
 n_x=(1,0,12)/\sqrt{145},\quad n_y=(0,1,12)/\sqrt{145},
\]
\[
 \mathcal E=G n_x\cup G n_y,\qquad D=1/15000.             \tag{1}
\]
There are 120 directed centers, paired into sixty unoriented axes. The two
proper orbits are disjoint and each has sixty directed centers. These are
the endpoints of the two previously classified mirror-arc families, not
their twofold starting axes.

A frame \(B\) is a real orthonormal-row \(2\)-by-\(3\) matrix. Its oriented
normal is the cross product of its rows; completing those rows by this
normal gives \(F\in SO(3)\). All motions below are proper, with unrestricted
proper planar roll. Normal distances are Euclidean unit-sphere chords and
matrix norms are Euclidean operator norms.

**Theorem.** For every receiving frame \(B_2\) whose oriented normal satisfies
\(\operatorname{dist}(n_2,\mathcal E)\le D\), every source frame \(B_1\),
every physical planar translation \(t\), and every \(\lambda\ge1\),
\[
 \lambda B_1K+t\subseteq B_2K
 \quad\Longleftrightarrow\quad
 \lambda=1,\quad t=0,\quad B_1=\sigma B_2g
 \quad(\sigma\in\{1,-1\},\ g\in G).                      \tag{2}
\]
All cap boundaries and centers are included. Thus all strict passages are
excluded in these explicit receiving caps, for arbitrary sources and full
rolls. Uniform rescaling, including unit edge length, preserves (2).
This is not a full-sphere exclusion or a proof of global non-Rupertness.
It does not assign radius \(D\) to every point of the full mirror arcs.

We first establish a separate local box with receiving chord radius
\(1/1000\) **and** full relative-angle cutoff \(1/100\) radians. That local
box initially has both hypotheses. Sections 4–8 remove the source-angle
hypothesis in the smaller caps (1), using a linear all-source pose estimate.
The distinction between these two radii is part of the theorem.

## 2. Published premises, method credit and proof boundary

The [quantitative arc-tube proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_arc_tube_control/PROOF.md),
source `19ea97d41b421428fe3b96b24a9270fa96c09f2d`, graph
`bafkreiern5qzomxijvp7vkbyazugkt3bzazsmxlth4xn5wduxbpyzzlsfy`,
gives the all-source matching and nearly fixed-row mechanism. Its
square-root estimate and final uniform-angle transfer are not used as
substitutes for the stronger linear estimate proved here.
The [mirror-arc proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_mirror_arc_rigidity/PROOF.md),
source `18e9736df5624f44a22d929699d585138f4b7483`, graph
`bafkreia32nj6ojbdmq2ndloqbxt57h5mzspoe6wko7gwi36dlp4fxfyc3m`,
supplies actual-original geometry, endpoint areas/widths and exact rigidity
at the reference centers.

The direct all-source localization premise is the
[area/width filter](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_low_area_width_filter/PROOF.md),
source `2965d5f69373933b5a186976d11867a779b7cf89`, graph
`bafkreig3ksndxbobnpq2brpxglwkozqo54hz4ykibzp6lpw4cxcn32xwsi`.
It uses physical area \(A(n)\), minimum shadow width \(\mu(n)\), and
\(A_1=\sqrt{940+1520\phi}\): if
\[
 A(n_2)\le A_1+1/4,\qquad
 \mu(n_2)^2\le(20+32\phi)(1-10/11664),                     \tag{3}
\]
then every source of a closed fit with scale at least one has normal chord
\(<1/8\) and transverse norm (sine, not tangent) \(<3/25\) from a proper
image of \(e_z\). The
[brightness certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md)
(source `58824907716016ff519f2aa5430fef92aa78c62c`, graph
`bafkreigejf2bp43sgs6vx5eaomipinr2ifhyvsgucjf6gsnedxlembvi6u`)
reconstructs the actual body, facets, proper group and physical area vectors.

The existing [support-probe lemma](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/TORQUE_PROOF.md)
(graph `bafkreig3erec7rq3afffflefrepyeb2blvwiguqw2fxj6ntte6wc7g6bfq`,
height 7138) supplies the general torque mechanism; it is not a new method
here. Section 3 writes its weak-inequality extension for closed fits and
provides two new actual endpoint certificates. Earlier
[twofold transport](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_quadratic_twofold_caps/PROOF.md)
and [fivefold matching](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_fivefold_rigidity/PROOF.md)
are credited antecedents.

`DEPENDENCIES.json` pins four files of the tube source. Its whole expected
record is replayed before any new check, transitively replaying the whole
arc, width, fivefold, brightness and earlier uniform-local records. The
old \(10^{-16}\) angle theorem is included in that source replay, but its
mathematical conclusion is **not** a premise of this proof: the new finite
torque certificates give the \(1/100\) local cutoff directly. All numerical
hypotheses below use exact ordered \(\mathbb Q(\phi)\) and rational arithmetic.
The continuum implications are written proof, not proof-assistant output.

## 3. Four actual probes give closed local rigidity in a larger box

For each reference normal take four actual original vertices \(v_i\) and
unnormalized physical spatial probes \(m_i\) from `PROBES.json`. All probes
are perpendicular to the stated raw normal. The checker establishes
\[
 \|m_i\|<4,\qquad
 m_i\cdot(v_i-w)>1/10\quad(w\in V\setminus\{v_i\}).        \tag{4}
\]
There are \(4\cdot59=236\) all-original comparisons per reference, including
hidden or collinear projected originals. Put \(\tau_i=v_i\times m_i\).
The supplied exact positive stress satisfies \(\sum_i w_i\tau_i=0\),
\(w_i>0\), and the four torques are affinely independent. For each tetrahedron
facet with normal \(h\), the exact gate is
\[
            (h\cdot\tau_i)^2>(3/20)^2(h\cdot h).          \tag{5}
\]
Thus the origin is interior and its distance from every facet plane is
strictly greater than \(3/20\). Equivalently the entire closed ball of that
radius lies inside the tetrahedron. This is a certificate uniform over all
rotation axes, with no spherical sampling.

For clarity, the certificate's vertices and probes are:

| Reference | \(v_i\) | \(m_i\) |
|---|---|---|
| x, 0 | \((-a,-c,0)\) | \((-\phi,(13-25\phi)/12,\phi/12)\) |
| x, 1 | \((-1,-b,1)\) | \((1-\phi,-25/12-\phi,(\phi-1)/12)\) |
| x, 2 | \((1,-b,-1)\) | \((\phi-1,-25/12-\phi,(1-\phi)/12)\) |
| x, 3 | \((a,-c,0)\) | \((\phi,(13-25\phi)/12,-\phi/12)\) |
| y, 0 | \((-a,-c,0)\) | \((-(1+11\phi)/12,1-2\phi,(2\phi-1)/12)\) |
| y, 1 | \((-1,-b,1)\) | \((11/12-\phi,-c,c/12)\) |
| y, 2 | \((1,-b,1)\) | \((\phi-11/12,-c,c/12)\) |
| y, 3 | \((a,-c,0)\) | \(((1+11\phi)/12,1-2\phi,(2\phi-1)/12)\) |

For x the weights are
\((275/432+11\phi/36,\ 43/216+5\phi/16,\ 43/216+5\phi/16,\ 275/432+11\phi/36)\).
For y they are
\((425/432+25\phi/48,\ (25+125\phi)/432,\ (25+125\phi)/432,\ 425/432+25\phi/48)\).
The exact output reports every torque, support minimum, affine determinant
and each of the four facet distances, not only a count of valid certificates.

Let an actual receiver have normal \(n\) with \(\|n-n_j\|\le d_0=1/1000\).
Transport each probe by orthogonal projection into its actual row plane:
\(m'_i=m_i-(m_i\cdot n)n\). Since \(m_i\perp n_j\),
\[
 \|m'_i\|\le\|m_i\|<4,\quad \|m'_i-m_i\|<4d_0,
 \quad m'_i\cdot(v_i-w)>1/10-40d_0>0.                    \tag{6}
\]
The very same actual original remains the unique outer support maximizer.
This handles perturbations to either side of the mirror plane, without
assuming persistence of a collapsed shadow facet.

Suppose a closed fit \(\lambda BQK+t\subseteq BK\), \(\lambda\ge1\), has
\(Q\in SO(3)\) of full angle \(0<\theta\le1/100\). Central symmetry and
contraction toward zero give \(BQK\subseteq BK\) while preserving \(Q\).
For its unit rotation axis \(\omega\), the actual support inequalities imply
\[
 m'_i\cdot(Qv_i-v_i)\le0.
\]
The exact exponential remainder bound
\(\|Q-I-\theta[\omega]_\times\|\le\theta^2/2\)
follows by integrating the second derivative of the orthogonal exponential
twice, whose operator norm is at most one. With \(R\|m'_i\|<20\),
\[
 \omega\cdot(v_i\times m'_i)\le20\theta/2,
 \quad \omega\cdot\tau_i<20(d_0+\theta/2)
                                 \le3/25<3/20.           \tag{7}
\]
But (5) forces \(\max_i\omega\cdot\tau_i\ge3/20\), a contradiction.
Therefore every closed fit in this local box has \(Q=I\). Its original
scale and translation then satisfy
\(\lambda h(\zeta)+|\zeta\cdot t|\le h(\zeta)\) in each unit planar
support direction, with \(h>0\). This gives \(\lambda=1,t=0\).
Conversely those values give equality. The same result holds at proper
body images after folding. A common planar roll changes no spatial
support inequality or relative-angle definition.

## 4. The full-source filter survives in the proposed receiving caps

Fix \(0<\delta\le D\) and an actual receiving normal within \(\delta\)
of one of the proper endpoint images. Fold it to x or y; put \(j=x\) or y,
\(k\ne j\), and \(u_0=1/\sqrt{145}\). Shortest proper normal transport and
a common proper planar gauge give \(B_2=C_{n_j}T\),
\(\|B_2-C_{n_j}\|\le\delta\). Independently fold the source when localized.
No source pose, scale or translation has initially been constrained.

The arc endpoint area and directional width are reconstructed in the
prerequisite proof. Fresh exact gates strengthen their margins to
\[
 A(n_j)<1171/20-1/50<A_1+1/4-1/50,\qquad w_j<9,
\]
\[
 w_j^2<(20+32\phi)(1-10/11664)-1/50.                      \tag{8}
\]
Physical Cauchy area is globally 250-Lipschitz. A fixed planar directional
width changes by at most \(2R\delta<10\delta\), so its square increases
by less than \(180\delta+100\delta^2\). The scalar checks
\[
 250D<1/50,\qquad180D+100D^2<1/50                         \tag{9}
\]
prove (3), so **every** source normal folds to
\[
 n_1=z e_z+u,\quad z>0,\quad \|u\|<3/25,
 \quad\|n_1-e_z\|<1/8.                                  \tag{10}
\]
For a proposed (2), centering and scaling down are used only for geometric
inclusions. The original \(\lambda,t\) are kept for the conclusion.

The four equatorial originals are \(E=\{(\pm a,\pm c,0)\}\).
Actual target nonequatorial heights exceed \(3/5-5\delta\), whose square
is \(>1/3>36/125\); source equatorial projected squared radii exceed
\(R^2-36/125\). Thus actual support maximizers for those source points must
come from target \(E\) and lie within \(11/20\). Both positive equatorial
projection singular values exceed \(24/25\).
The published side and determinant gates give a unique antipodal bijection,
exclude exchanging the two side types, and retain only identical labels
or simultaneous sign reversal. Absorb the latter by a proper planar
source half-turn. In particular the four source/target norm inequalities
can be summed over the same actual \(E\); they are not inequalities for
fabricated hull preimages.

Quadratic equatorial transport and a same-label match bound the full
initially arbitrary roll and source frame by
\[
             \|B_1-P\|<1473/5632+(25/22)\delta<4/15.       \tag{11}
\]
These implications use the same strict budgets as the published tube
proof Sections 4–5; (8)–(11) explicitly verify them on the larger domain
\(\delta\le1/15000\), not just the old \(10^{-6}\) domain.

## 5. Fixing one row changes the retained tilt only quadratically

On the reference x arc the fixed row is \(e_y^t\); on the y arc it is
\(e_x^t\). Let \(r^t\) be that actual source row, \(r_k=r\cdot e_k\),
and let \(q\) be its transverse norm. The actual target support in that
planar row direction is at most \(b+5\delta\). Four actual originals
with coordinate \(b\) in direction k and independent \(\pm1\) in the
other coordinates force
\[
 b r_k+\sum_{i\ne k}|r_i|\le b+5\delta.
\]
From (11), \(r_k>9/10,q<4/15\). Therefore
\[
 q<95\delta/7<14\delta,
 \qquad\|r-e_k\|<16\delta.                              \tag{12}
\]
For \(q>0\), this follows from
\(q\le bq^2/(1+r_k)+5\delta<(12/19)q+5\delta\);
for \(q=0\) it is immediate, without division by q.
Let \(H\in SO(3)\) be shortest rotation sending \(e_k\) to r, and put
\(B'_1=B_1H\). Its fixed row is exactly \(e_k^t\) and
\(\|B'_1-B_1\|<16\delta\).

Write \(n_1\) for the original source normal and \(\nu=(n_1)_k\).
Since \(n_1\perp r\),
\[
                |\nu|\le q/r_k<16\delta.                \tag{13}
\]
The useful new point is an exact formula for the corrected normal. Put
\(S=[e_k\times r]_\times\). Rodrigues' shortest-rotation formula is
\(H=I+S+S^2/(1+r_k)\). Using \(r\cdot n_1=0\) gives
\[
 n'_1=H^tn_1
       =n_1-\frac{\nu}{1+r_k}(r+e_k).                   \tag{14}
\]
Its k component vanishes exactly. Each retained non-k coordinate changes
by less than
\[
       \frac{(16\delta)(14\delta)}{19/10}<120\delta^2.   \tag{15}
\]
Thus correcting the nearly fixed row costs only quadratically in the
mirror-plane tilt and z coordinate; the coarse whole-frame correction
bound remains linear.

The other corrected row has positive reference coordinate, because
\(4/15+16D<1/3\). Hence \(B'_1=C_{n'_1}\) in the same mirror plane.
Write \(n'_1=z'e_z+u'e_j\), \(v=|u'|\). Its transverse norm is
\(<3/25+16D<123/1000\), \(z'>24/25\), and normal chord is
\(<1/8+16D<1/4\). Its containment is not assumed after correction.

## 6. Averaged actual radial inequalities give a linear lower tilt bound

For any source original in E, the actual support match gave
\(\|B_1w\|\le\|B_2w'\|\), with an actual bijection of the four E originals.
Their common spatial squared radius is \(R^2=a^2+c^2\). Summing all four
squared inequalities cancels the mixed products exactly:
\[
 a^2(n_1)_x^2+c^2(n_1)_y^2
       \ge a^2(n_2)_x^2+c^2(n_2)_y^2.                   \tag{16}
\]
Off the arc the four target projected radii need not agree; equality of
those radii is not used. Only the actual bijection and its complete sum
enter (16).

Let \(\gamma_j=a\) or c for the receiving mirror direction and
\(\gamma_k=c\) or a for the other. Their exact bounds are
\(\gamma_j^2>6,\gamma_k^2<20\). Dropping the nonnegative target k term
in (16), and using (13), gives
\[
       (n_1)_j^2\ge(n_2)_j^2-(20/6)\,256\delta^2.
\]
Equation (15) changes the retained squared coordinate by less than
\(240\delta^2\), because both coordinates have magnitude at most one.
Since \((20/6)256+240<1100\),
\[
                v^2>(n_2)_j^2-1100\delta^2
                    \ge(u_0-\delta)^2-1100\delta^2.      \tag{17}
\]
The final inequality uses \((n_2)_j\ge u_0-\delta>0\).
Since \(u_0>1/13\) and \(1/13-D>1/14\), if v is below \(u_0-\delta\)
we may divide the squared difference by
\(u_0-\delta+v>1/14\), obtaining
\[
 v>u_0-\delta-15400\delta^2>u_0-3\delta.                 \tag{18}
\]
The last inequality is the exact gate \(1+15400D<3\). If v is larger,
(18) follows immediately. The endpoint's strictly positive reference
tilt is used here; the argument is not extended through zero tilt.

## 7. Reflection symmetry makes the area correction quadratic

Write physical Cauchy area as \(A(n)=\sum_{s\in C}|s\cdot n|\) for the
31 paired-facet area vectors. Six, denoted \(C_0\), are perpendicular to
\(e_z\); the other 25 have constant signs in the chord domain used here,
because
\(\min_{s\notin C_0}(s\cdot e_z)^2/\|s\|^2=(2-\phi)/4>1/16\).
Their signed sum is \(A_0e_z\), with \(A_0=12+28\phi<58\). Consequently
\[
 A(ze_z+u)=A_0z+h_0(u),\qquad
 h_0(u)=\sum_{s\in C_0}|s\cdot u|.                      \tag{19}
\]
The actual generator set, modulo opposite representatives, is invariant
under reflection of either transverse coordinate, as checked directly.
Convexity and evenness therefore give
\[
                 h_0(u_je_j+u_ke_k)\ge H_j|u_j|,
 \quad H_x=4+8\phi,\quad H_y=8+4\phi,
 \quad14<H_j<17.                                       \tag{20}
\]
For the mirror-fixed source,
\(F_j(v)=A_0\sqrt{1-v^2}+H_jv\).
Equations (15),(19),(20) bound its area above the uncorrected source by
\[
            F_j(v)-A(n_1)<(58+17)120\delta^2=9000\delta^2.\tag{21}
\]
Both coordinate changes in this step are quadratic; substituting a coarse
normal-chord Lipschitz bound would lose the effective cap radius.

There is also a sharper actual-target estimate. For each j the checker
finds that the nonzero j components of \(C_0\), weighted by their signs,
sum exactly to \(H_je_j\). The remaining pure k components have total
absolute magnitude exactly four. For every target in our cap their j signs
are unchanged: \((n_2)_j>1/13-\delta\), \(|(n_2)_k|\le\delta\), and all
exact gates
\[
 |s_j|(1/13-D)>|s_k|D\quad(s\in C_0,\ s_j\ne0)
\]
hold. Thus, with \(x=(n_2)_j>0\),
\[
 A(n_2)=A_0(n_2)_z+H_jx+4|(n_2)_k|
                 \le F_j(x)+4\delta.
\]
On the relevant positive tilt interval \(F'_j\le H_j<17\). Also it is
strictly increasing there, so whether \(x\le u_0\) or \(x>u_0\),
\[
                   A(n_2)<F_j(u_0)+21\delta.             \tag{22}
\]
For \(0\le w\le123/1000\), the stronger lower derivative bound is
\[
       F'_j(w)>14-58(123/1000)/(24/25)>6.                 \tag{23}
\]
The centered unit fit has \(A(n_1)\le A(n_2)\). Combining (21)–(23),
if \(v>u_0\),
\[
 v-u_0<(21\delta+9000\delta^2)/6<4\delta,
\]
because \((21+9000D)/6<4\). With (18) this yields
\[
                        |v-u_0|<4\delta.                \tag{24}
\]
Every step is a physical area comparison; no chart-area Jacobian or sampled
approximation is substituted.

## 8. Proper pose recovery removes the local angle hypothesis

Choose the sign of the reference tilt matching \(u'\), with either choice
if it vanishes. Locked mirror frames are less than two-Lipschitz in tilt
on this interval: for \(z(w)=\sqrt{1-w^2}\),
\[
 |z(w)-z(v)|\le\frac{2(123/1000)}{2(24/25)}|w-v|,
\]
The corresponding unit-normal chord is less than \(2|w-v|\).
Equivalently this follows from the one changing unit row of \(C_n\).
Negative tilt obeys the exact proper-body identity
\(C_{-\mathrm{tilt}}=-C_{+\mathrm{tilt}}R_z\),
\(R_z=\operatorname{diag}(-1,-1,1)\in G\).
Using (24), the source row correction \(<16\delta\), and actual receiving
transport \(\le\delta\), then undoing proper folds and the common planar
gauge, gives
\[
       \|B_1-\sigma B_2g\|<8\delta+16\delta+\delta
                                      =25\delta.        \tag{25}
\]
This is an all-source linear pose bound, not an initial small-pose premise.
It also gives, before invoking exact local rigidity,
\(\lambda-1<125\delta\) and \(\|t\|<125\delta\) for the edge-two body
by original central support inequalities and the unit ball inside K.

For completeness both proper symmetry branches are retained. Complete
\(B_i\) to \(F_i\in SO(3)\), and put \(Q=F_2^tF_1\), so \(B_1=B_2Q\).
A row-frame difference h gives normal difference at most \(2h\) and
completed-frame operator difference at most \(\sqrt5h<3h\).
For the positive branch define \(\widetilde Q=Qg^{-1}\).
For the negative branch define
\[
 \widetilde Q=J_{n_2}Qg^{-1},\quad J_{n_2}=2n_2n_2^t-I\in SO(3).
\]
The actual-normal half-turn satisfies \(B_2J_{n_2}=-B_2\). In either case
\(\widetilde Q\) is proper, its actual source shadow is exactly
\(B_2\widetilde QK=B_1K\), and the original \(\lambda,t\) are preserved.
For the negative branch the completed reference frame is
\(F_2J_{n_2}g\), not an improper matrix.
Thus \(\|\widetilde Q-I\|<75\delta\). Since for a proper rotation
\(\|\widetilde Q-I\|=2\sin(\theta/2)\), sine concavity and \(\pi<4\) give
\[
                  \operatorname{angle}(\widetilde Q)
                             <150\delta\le150D=1/100.   \tag{26}
\]
The receiver lies within \(D<1/1000\) of a proper endpoint reference.
After folding that reference, Section 3 applies to the actual closed fit
with \(\widetilde Q\), and forces \(\widetilde Q=I\),
\(\lambda=1,t=0\). Undoing the correction gives exactly
\(B_1=\sigma B_2g\), proving the forward implication of (2).
The converse follows from \(gK=K=-K\).

Every receiver in the closed caps, including centers, can use the positive
parameter \(\delta=D\) in this argument. Alternatively the center case is
the published exact arc theorem. Thus no limit, strict-radius convention
or hidden exclusion of cap boundaries is required.

## 9. Reproduction and remaining frontier

From the repository root, Python 3.11+ and only its standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-rupert-3/rid_endpoint_contact_caps/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B round-two/six-rupert-3/rid_endpoint_contact_caps/check.py
```

Outputs must byte-match `expected.json`. Mathematical guards use explicit
exception checks, surviving optimization. After the whole pinned tube
replay and its prerequisites, the new checker verifies all 472 unique
original support comparisons, both positive torque stresses and all eight
facet-distance gates, the proper endpoint orbit counts, the full six-vector
reflection/sign identities, stronger physical endpoint margins, and every
rational budget for the quadratic row correction, averaged radial bound,
local area derivative, linear pose and final relative-angle gate. Seven
damaged controls reverse a probe, delete a probe, erase a positive weight,
change the reference normal, enlarge the torque ball, exceed the endpoint
filter domain, or truncate the physical area inventory; each must reject.

Probe discovery used exploratory exact hulls, but those search routines and
any incorrect preliminary side chart are absent from the proof input.
`PROBES.json` contains only the two compact actual certificates. The
published checker validates them directly against every original, not
against a presumed silhouette or a list of visible preimages.

The trust boundary is exact Fraction/ordered-\(\mathbb Q(\phi)\) arithmetic,
the hash-pinned prior finite certificates, and the written new and prior
continuum arguments. No numerical solver, floating-point sign, incomplete
enumeration, failed search, timeout or omitted corpus supplies a proof step.
No independent reviewer verdict or formalization is asserted.

Current primary status seeds,
[Steininger–Yurkevich, arXiv:2508.18475](https://arxiv.org/abs/2508.18475)
and [Zeng, arXiv:2604.26531](https://arxiv.org/html/2604.26531), leave the
global standard RID question unresolved. These explicit endpoint caps
improve a receiving region previously covered only by the very thin
arc tube; the older twofold and fivefold caps remain separate prior results.
The proof does not transfer J74 or pentagonal-body constants.
A useful next frontier is to certify continuous families of these uniquely
supporting probes along nonzero mirror tilts, with parameter-dependent
margins, to thicken the complete arc family. Receiver regions outside the
known caps and tubes, and nonlocal global passages, remain open.
