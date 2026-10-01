# Quantitative all-source control and a strict-exclusion tube around RID mirror arcs

**six-rupert-3, researcher; 2026-10-01.** Written geometric proof with exact
finite-hypothesis checks. Author-checked, unformalized; no independent review
or priority claim. The standard rhombicosidodecahedron's global Rupert
property remains unresolved.

## 1. Statement and motion conventions

Write \(\phi=(1+\sqrt5)/2\). Let \(V\) be all independent signs and even
coordinate permutations of
\[
 (1,1,\phi^3),\qquad(\phi^2,\phi,2\phi),\qquad(2+\phi,0,\phi^2),
\]
and \(K=\operatorname{conv}V=-K\), the standard edge-two RID. Every original
has squared radius \(R^2=7+8\phi<20\). Let \(G\subset SO(3)\) be its proper
body rotation group. A projection frame is an arbitrary real orthonormal-row
\(2\)-by-\(3\) matrix. Its **oriented** normal is the cross product of its
first and second rows. Completing those rows by this normal gives a proper
orthogonal matrix, so all relative spatial motions below are proper.
Planar rolls, physical planar translations, and scales are retained.

Put \(e=e_z\), \(a=\phi^2\), \(c=2+\phi\), \(b=\phi^3\), and define
\[
 \mathcal M=\bigcup_{g\in G}\bigcup_{0\le s\le1/12}
 \left\{g\frac{(s,0,1)}{\sqrt{1+s^2}},
        g\frac{(0,s,1)}{\sqrt{1+s^2}}\right\}.                 \tag{1}
\]
This compact set includes both endpoints of both reference arcs and their
proper body images. Since \(R_z=\operatorname{diag}(-1,-1,1)\in G\), both
signs of coordinate tilt are included. It is a union of curves, not a
spherical cap of radius \(1/12\). All normal distances are Euclidean chord
distances on the unit sphere; matrix norms are Euclidean operator norms.

**Quantitative theorem.** Suppose \(0<\delta\le10^{-6}\), the oriented
receiving normal \(n_2\) satisfies \(\operatorname{dist}(n_2,\mathcal M)
\le\delta\), and
\[
 \lambda B_1K+t\subseteq B_2K,\qquad \lambda\ge1,\quad t\in\mathbb R^2.\tag{2}
\]
There exist \(\sigma\in\{1,-1\}\) and \(g\in G\) such that
\[
 \|B_1-\sigma B_2g\|<40\sqrt\delta,\qquad
 \lambda-1<200\sqrt\delta,\qquad \|t\|<200\sqrt\delta.       \tag{3}
\]
There is no initial restriction on the source frame, planar roll, or
translation. At \(\delta=0\), the published arc theorem instead gives the
exact classification \(\lambda=1,t=0,B_1=\sigma B_2g\).

**Strict-exclusion corollary.** Every receiving frame with
\[
       \operatorname{dist}(n_2,\mathcal M)\le10^{-38}          \tag{4}
\]
excludes \(\lambda B_1K+t\subset\operatorname{int}(B_2K)\) for all frames
\(B_1\), scales \(\lambda\ge1\), and translations \(t\). Thus a closed,
explicit, positive receiving tube around the entire arc union excludes
standard Rupert passages. Closed fits inside this tube are only bounded
by (3); an exact classification off the arcs is not asserted.

Uniform rescaling leaves the frame, scale, chord and angle conclusions
unchanged. For the unit-edge body, the translation bound in (3) is
\(100\sqrt\delta\).

## 2. Published premises and what is checked

The [mirror-arc theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_mirror_arc_rigidity/PROOF.md)
(source `18e9736df5624f44a22d929699d585138f4b7483`, graph
`bafkreia32nj6ojbdmq2ndloqbxt57h5mzspoe6wko7gwi36dlp4fxfyc3m`) proves the exact closed
classification on (1). Its Sections 3 and 5–7 give the finite geometry,
actual-original matching, side/orientation exclusion and quadratic
transport used below. We explicitly check that their strict budgets
survive the perturbation; exact arc classification alone is not treated
as a quantitative stability theorem.

The [area/width filter](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_low_area_width_filter/PROOF.md)
(source `2965d5f69373933b5a186976d11867a779b7cf89`, graph
`bafkreig3ksndxbobnpq2brpxglwkozqo54hz4ykibzp6lpw4cxcn32xwsi`)
uses \(A_0=12+28\phi\), \(A_1=\sqrt{940+1520\phi}\), and proves that
\[
 A(n_2)\le A_1+\tfrac14,\quad
 \mu(n_2)^2\le (20+32\phi)(1-10/(16\cdot729))               \tag{5}
\]
localize **every** source of a closed fit with scale at least one to a
proper twofold-axis image with normal chord \(<1/8\) and transverse norm
\(\sin\angle(n_1,Ge)<3/25\). Here \(\mu\) is minimum physical shadow width.
We use this all-source filter, not an assumed nearby source.

The [brightness certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md)
(source `58824907716016ff519f2aa5430fef92aa78c62c`, graph
`bafkreigejf2bp43sgs6vx5eaomipinr2ifhyvsgucjf6gsnedxlembvi6u`)
reconstructs the actual named body, proper group, facets and physical
Cauchy area vectors. The arc checker replays the full filter, fivefold
and brightness expected records and their pinned inputs. The
[twofold transport](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_quadratic_twofold_caps/PROOF.md)
and [fivefold matching](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_fivefold_rigidity/PROOF.md)
are credited antecedents; their implications needed here are written below.

For the strict corollary we use the distinct published
[uniform local theorem](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/LOCAL_PROOF.md),
source `b7246943cdd927f46af48c604d4562b9483f2c17`, graph
`bafkreih4ge2xplbtaali3mjaqccgklblzkpge7stgk5dfvkyjidx57node`:
\[
 \forall B\ \forall Q\in SO(3)\ \forall t:\quad
 \operatorname{angle}(Q)\le10^{-16}
 \ \Longrightarrow\ BQK+t\not\subset\operatorname{int}(BK). \tag{6}
\]
Its quantifiers allow both source and receiver to vary, and the angle is
the full relative rotation, including planar roll. This is a strict-fit
statement, not a classification of closed fits. We read its written
[local](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/LOCAL_PROOF.md),
[cell](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/CELL_PROOF.md),
[torque](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/TORQUE_PROOF.md)
and [mirror-class](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/PROOF.md)
arguments. `DEPENDENCIES.json` pins eleven required public files; the new
checker independently runs that complete local certificate and byte-matches
its whole 3851-byte expected record, including its inherited cell hash.
It also compares all sixty actual vertices from the two prerequisite
arithmetic kernels. No transfer between differently named bodies occurs.

## 3. A larger tube still meets the all-source filter

Fix a nearest \(m\in\mathcal M\) to \(n_2\), which exists by compactness.
Properly fold it to a reference arc, indexed by \(j=x\) or \(y\). Let
\(T\in SO(3)\) be shortest rotation sending the actual receiving normal
to \(m\). Then
\[
 \|T-I\|=\|n_2-m\|\le\delta.
\]
A common proper planar gauge makes the actual receiver
\(B_2=C_mT\), where \(C_m\) is shortest transport from the reference
frame \(P=(e_x^t;e_y^t)\). Therefore
\[
                  \|B_2-C_m\|\le\delta.                  \tag{7}
\]
These proper body folds and common planar gauges preserve (2), norms and
physical translation. They are undone at the end.

Cauchy's physical formula is \(A(n)=\sum_{q\in C}|q\cdot n|\), with
31 paired-facet vectors. The new checker finds exactly
\(\max_{q\in C}\|q\|^2=15+20\phi<49\); hence
\[
             |A(n)-A(n')|<250\|n-n'\|.                  \tag{8}
\]
The arc proof gives strictly increasing area and a strictly increasing
explicit directional width on each full interval \(0\le s\le1/12\).
Using its independently reconstructed endpoint values, the new exact
gates strengthen the endpoint margins to
\[
 A(m)<1171/20-1/1000<A_1+1/4-1/1000,
\]
\[
 w_j(s)<9,\qquad
 w_j(s)^2<(20+32\phi)(1-10/(16\cdot729))-1/1000.           \tag{9}
\]
These are entire-arc bounds because the published derivatives are positive.

In the corresponding unit planar width direction, (7) changes each
original support by at most \(R\delta<5\delta\). Thus actual target width
is at most \(w_j(s)+10\delta\). Its squared increase is less than
\(180\delta+100\delta^2\). For \(\delta\le10^{-6}\), the rational gates
\[
 250\delta<1/1000,\qquad180\delta+100\delta^2<1/1000       \tag{10}
\]
prove both parts of (5), including the weak endpoints.

Central symmetry of both shadows lets us negate and average (2), giving
\(\lambda B_1K\subseteq B_2K\). Since \(\lambda\ge1\) and the centered
source contains zero, also \(B_1K\subseteq B_2K\). This centered unit fit
is used for geometry, while the actual \(\lambda,t\) are retained. Fold
the source independently by a proper body symmetry. The filter now gives
\[
 n_1=z_1e+u_1,\quad z_1>0,\quad \|u_1\|<3/25,
 \quad\|n_1-e\|<1/8.                                    \tag{11}
\]
No small planar roll has yet been assumed.

## 4. Actual-original matches and full-frame control survive

The equatorial originals are exactly
\(E=\{(\pm a,\pm c,0)\}\); \(a^2+c^2=R^2\). Every other original has
\(|v_z|\ge1\), and each coordinate is at most \(b<9/2\) in magnitude.
At a reference receiver, its squared height is strictly greater than
\(45/116>(3/5)^2\). At the actual receiver the height therefore exceeds
\(3/5-5\delta>0\), using (7) or the normal chord bound. Our exact gates give
\[
 (3/5-5\delta)^2>1/3>36/125.                             \tag{12}
\]
Source equatorial projected squared radii exceed \(R^2-36/125\), by (11)
and \(R^2<20\).

For every source equatorial point \(x=B_1v\), support containment supplies
an actual receiving original projection \(y=B_2v'\) with
\(x\cdot y\ge\|x\|^2\). Cauchy–Schwarz gives \(\|y\|\ge\|x\|\).
Equation (12) excludes \(v'\notin E\). Moreover, using only
\(\|y\|^2\le R^2\),
\[
             \|x-y\|^2<36/125<(11/20)^2.                 \tag{13}
\]
At an off-arc receiver the four target radii need not coincide; we do
not assume that they do.

The source normal's positive \(e\) component exceeds \(24/25\). The
reference receiver's exceeds \(99/100\), since
\(144/145>(99/100)^2\); the actual receiver's exceeds
\(99/100-\delta>24/25\). Both projections of \(e^\perp\) therefore have
smallest singular value above \(24/25\).

The arc proof's matching argument uses just (13), these two singular
bounds, and the fixed actual rectangle. It consequently applies unchanged:
separation \(2a(24/25)>2(11/20)\) gives a unique antipodal bijection;
\(2c(24/25)-2a>2(11/20)\) forbids exchanging long and short sides;
and
\[
 2(11/20)\,2(a+c)+4(11/20)^2<4ac(24/25)
\]
prevents a determinant sign reversal. The only surviving label maps are
identity and simultaneous sign reversal. In the latter case replace the
source frame by \(-B_1\), a proper planar half-turn with the same shadow
and oriented normal. Now all four matches use identical original labels.

Write \(B_1=LC_{n_1}\), \(L\in SO(2)\), in the receiver's gauge.
For equatorial \(v\), shortest transport obeys
\[
 C_n|_{e^\perp}=I_2-uu^t/(1+z),\quad C_ne=-u,
 \quad\|C_n-P\|=\|n-e\|,
\]
\[
             \|C_nv-Pv\|\le R\|n-e\|^2/2.              \tag{14}
\]
Thus the source drift is below \(9/256\), the reference receiver drift
is at most \(1/64\), and the extra actual-receiver drift is below
\(5\delta\). One same-label match, \(R>22/5\), and the planar rotation
identity \(\|(L-I)Pv\|=R\|L-I\|\) yield
\[
 \|B_1-P\|<1473/5632+(25/22)\delta<4/15.                \tag{15}
\]
This bounds the entire initially arbitrary roll, not only normal tilt.

## 5. Correcting the nearly fixed row costs less than 16 delta

The reference arc's fixed row is \(e_k^t\), with \(k=y\) on the x arc
and \(k=x\) on the y arc. Let \(r^t\) be the corresponding source unit
row. By (15), \(r_k>9/10\) and its transverse norm
\(q=(\sum_{i\ne k}r_i^2)^{1/2}<4/15\).
The actual target support in this planar row direction is at most
\(b+5\delta\). The four actual source originals with coordinate \(b\)
in direction \(e_k\) and independent \(\pm1\) in the other two
coordinates force
\[
 b r_k+\sum_{i\ne k}|r_i|\le b+5\delta.
\]
Using \(1-r_k=q^2/(1+r_k)\) and \(q\le\sum_{i\ne k}|r_i|\) gives
\[
 q\le\frac{bq^2}{1+r_k}+5\delta
 <\frac{12}{19}q+5\delta,
 \quad q<\frac{95}{7}\delta<14\delta.                  \tag{16}
\]
For \(q=0\) the conclusion follows immediately; no division by \(q\)
is used. The chord of this unit row from \(e_k\) is
\(q\sqrt{2/(1+r_k)}<(11/10)q<16\delta\) when \(q>0\), and is zero
otherwise.

Let \(H\in SO(3)\) be shortest rotation sending \(e_k\) to the column
\(r\), and set \(B'_1=B_1H\). Then the fixed row is exactly
\(e_k^t\), and
\[
                      \|B'_1-B_1\|<16\delta.             \tag{17}
\]
The remaining row has positive reference coordinate because
\(\|B'_1-P\|<4/15+16\delta<1/3\). Orthonormality now implies
\(B'_1=C_{n'_1}\) on that same mirror plane, with
\[
 n'_1=z'e+u'e_j,\quad z'>24/25,
 \quad |u'|<3/25+16\delta<1/7,
 \quad \|n'_1-e\|<1/8+16\delta<1/4.                    \tag{18}
\]
The correction does not assert that the new source still fits; its
radial and area errors are tracked next.

## 6. Radial order and area give a square-root tilt estimate

Write \(u_0=s/\sqrt{1+s^2}\ge0\) for the reference arc's transverse
coordinate and \(\gamma=a\) on the x arc, \(\gamma=c\) on the y arc.
For every equatorial original, the corrected source radius is exactly
\(R^2-\gamma^2(u')^2\); the reference receiving radius is
\(R^2-\gamma^2u_0^2\).
For orthonormal-row frames \(D,F\) and an original \(v\),
\[
 |\|Dv\|^2-\|Fv\|^2|\le2R^2\|D-F\|.                   \tag{19}
\]
The original support match satisfies \(\|B_1v\|\le\|B_2v'\|\), with
both actual originals in \(E\). The source correction costs less than
\(640\delta\) in squared radius by (17),(19); receiver transport costs
less than \(40\delta\) by (7),(19). Hence
\[
 R^2-\gamma^2(u')^2
 \le R^2-\gamma^2u_0^2+680\delta.
\]
Since \(\gamma^2>6\) and \(680/6<11^2\), this implies
\[
                      |u'|>u_0-11\sqrt\delta.            \tag{20}
\]
If \(|u'|<u_0\), use
\((u_0-|u'|)^2\le u_0^2-(u')^2\); otherwise (20) is immediate.
This avoids division by the arc parameter, including at \(s=0\).

The 25 area vectors nonzero at \(e\) have
\(\min (q\cdot e)^2/\|q\|^2=(2-\phi)/4>1/16\).
Thus their signs remain unchanged in the entire chord domain (18).
The other six give the exact mirror-plane area
\[
 F_j(v)=A_0\sqrt{1-v^2}+H_jv,\quad v=|u'|,
 \quad H_x=4+8\phi>14,\ H_y=8+4\phi>14.                 \tag{21}
\]
For \(0\le v\le1/7\),
\[
              F'_j(v)>14-58(1/7)/(24/25)>5.             \tag{22}
\]
The corrected normal is \(H^tn_1\), so its change is at most
\(\|H-I\|<16\delta\).
The original centered fit has \(A(n_1)\le A(n_2)\); (8) consequently gives
\[
               F_j(|u'|)\le F_j(u_0)+4250\delta.         \tag{23}
\]
Indeed the source correction costs at most \(4000\delta\) and the target
at most \(250\delta\). Equations (22),(23) imply
\(|u'|<u_0+850\delta\). Since \(850^2\delta<1\) for our domain,
\[
                  \big||u'|-u_0\big|<11\sqrt\delta.     \tag{24}
\]

## 7. Recovering the original frame, scale and translation

Choose the sign of the reference mirror tilt to match \(u'\), choosing
either when \(u'=0\). On \(|v|\le1/7\) the normal's other coordinate
is \(z(v)=\sqrt{1-v^2}>24/25\), and
\[
 |z(v)-z(w)|\le\frac{2/7}{2(24/25)}|v-w|.
\]
In a fixed mirror plane the corresponding transported frames differ in
only one row; their operator distance equals this unit-normal chord.
The displayed coefficient gives a chord factor less than two. Thus (24)
puts \(B'_1\) within \(22\sqrt\delta\) of the matching reference frame.
For negative tilt the exact proper-body identity is
\[
                    C_{-\mathrm{tilt}(m)}=-C_mR_z.       \tag{25}
\]
The minus sign is a planar half-turn, not an improper spatial rotation.
Adding the source correction and actual-receiver transport gives
\[
  \|B_1-\sigma B_2g\|<22\sqrt\delta+17\delta
                                      <40\sqrt\delta
\]
in the folded gauge, and then in the original frames after undoing the
independent proper folds, optional source half-turn, and common gauge.
Here \(g\in G\), \(\sigma\in\{1,-1\}\).

Set \(A=B_1K\), \(C=B_2K\), and let \(h_A,h_C\) be their support
functions in unit planar direction \(\zeta\). Because
\(\sigma B_2gK=B_2K\), the frame bound yields
\[
                    |h_A(\zeta)-h_C(\zeta)|<200\sqrt\delta.\tag{26}
\]
Every support of \(A\) is at least one: the eight actual originals
\((\pm1,\pm1,\pm b)\), with independent signs and \(b>1\), enclose
\([-1,1]^3\) and its unit ball inside \(K\).
Applying the **actual** containment (2) in directions \(\pm\zeta\)
and using centrality gives
\[
              \lambda h_A(\zeta)+|\zeta\cdot t|
                                          \le h_C(\zeta).\tag{27}
\]
Equations (26),(27), \(h_A\ge1\), and \(\lambda\ge1\) give both remaining
bounds in (3). In particular \(t\) has not been silently set to zero.

## 8. A proper correction of both symmetry branches proves the tube

Let \(F_i\in SO(3)\) complete the rows of \(B_i\), and let
\(Q=F_2^tF_1\), so \(B_1=B_2Q\). If two projection frames differ in
operator norm by \(h\), each row differs by at most \(h\) and their
cross-product normals differ by at most \(2h\). Completing the frames
therefore changes the operator norm by at most
\(\sqrt{1+2^2}\,h<3h\).
For the positive branch of (3), completion puts \(Q\) within
\(120\sqrt\delta\) of \(g\). For the negative branch the proper reference
is \(J_{n_2}g\), where
\[
                       J_n=2nn^t-I\in SO(3).             \tag{28}
\]
This is a spatial half-turn around the **actual receiving normal**;
\(B_2J_{n_2}=-B_2\). Indeed it has eigenvalues \(1,-1,-1\), is a proper
involution, fixes \(n\), and negates every vector perpendicular to \(n\).
The completion of \(-B_2g\) is exactly \(F_2J_{n_2}g\), since negating
both first rows preserves their cross product. Treating the negative
frame as an improper rotation would leave a gap here.

Define a proper relative rotation
\[
 \widetilde Q=
 \begin{cases}Qg^{-1},&\sigma=1,\\
                J_{n_2}Qg^{-1},&\sigma=-1.
 \end{cases}                                            \tag{29}
\]
Then \(\|\widetilde Q-I\|<120\sqrt\delta\), and in both cases
\(B_2\widetilde QK=B_1K\) **exactly**. In the negative case this follows
from \(gK=K\) and \(-B_1K=B_1K\); it preserves the original \(\lambda,t\).
No new rotation symmetry of the solid is assumed for \(J_{n_2}\).

For a proper rotation of full angle \(0\le\theta\le\pi\),
\(\|\widetilde Q-I\|=2\sin(\theta/2)\).
Concavity of sine on \([0,\pi/2]\), and \(\pi<4\), imply
\(\theta\le2\|\widetilde Q-I\|\). Hence
\[
                  \operatorname{angle}(\widetilde Q)
                                             <240\sqrt\delta.\tag{30}
\]
The exact rational gate
\(240^2\cdot10^{-38}<10^{-32}\) puts the entire closed tube (4) strictly
inside the published full-angle threshold (6).
If a strict scaled fit existed, the origin in the centered source and
\(\lambda\ge1\) would give
\[
 B_2\widetilde QK+t\subseteq\lambda B_2\widetilde QK+t
                                     \subset\operatorname{int}(B_2K),
\]
contradicting (6) with this actual receiver and translation. This also
covers exact arc receivers: apply (3) with the positive radius
\(\delta=10^{-38}\), or use their exact published classification.
All normal and arc endpoints in (4) are included.

## 9. Reproduction, trust boundary and remaining problem

From the repository root, Python 3.11+ with only the standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-rupert-3/rid_arc_tube_control/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B round-two/six-rupert-3/rid_arc_tube_control/check.py
```

Each output must equal `expected.json` byte for byte. Every mathematical
guard is an explicit exception check. The local kernel runs in a fresh,
sequential child, preventing collision with the arc chain's hash-pinned
arithmetic module. Its timeout is an operational limit, never evidence
of a geometric obstruction. The checker reconstructs all physical area
vectors, verifies the new scalar margins and squared-root budgets using
exact ordered \(\mathbb Q(\phi)\) and rational arithmetic, and checks
proper half-turn identities on four exact rays. The universal identity
(28) and continuum arguments (7)–(30) are written proof; those four sanity
cases do not purport to enumerate the rotation space. Six damaged controls
must reject: larger filter radius, unsupported exclusion radius, insufficient
radial gap, insufficient completion factor, wrong half-turn formula, and
missing actual vertices. Full prerequisite outputs, not selected convenient
entries, are replayed before the new gates.

The proof is unformalized and depends on the stated published premises
and their written continuum arguments. It asserts no independent reviewer
verdict. No floating-point search, fitted formula, solver nonexistence
return, omitted corpus, or resource timeout supplies a proof step.

The earlier [global axial-height cutoff](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/GLOBAL_BAND_83_PROOF.md)
excludes receivers with \(f(n)=\min_{v\in V}|v\cdot n|\ge83/200\).
For either reference arc, an actual equatorial original gives
\(f(m)\le c/12<1/3<83/200\), since \(a<c=2+\phi<4\).
The same holds under proper body images. The present arc tube concerns
a different receiving domain from that axial cutoff. Earlier
[threefold caps](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/LINEAR_ROLL_PROOF.md)
and [contact collars](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/CONTACT_COLLAR_PROOF.md)
also remain prior art; their numerical radii are not transferred here.

Current primary seeds,
[Steininger–Yurkevich, arXiv:2508.18475](https://arxiv.org/abs/2508.18475)
and [Zeng, arXiv:2604.26531](https://arxiv.org/html/2604.26531), continue to
list the global RID question as unresolved. The positive tube (4) is
extremely thin because it transfers the conservative published uniform
angle; it is a rigorous intermediate obstruction, not a global conclusion
or a practical whole-sphere cover. A useful next frontier is to strengthen
the off-mirror contact inequalities or the uniform-angle bound enough to
exclude a macroscopic receiving region outside the earlier twofold and
fivefold caps. The explicit stability estimate (3) can be reused for
that purpose without relying on a nonconstructive compactness argument.
