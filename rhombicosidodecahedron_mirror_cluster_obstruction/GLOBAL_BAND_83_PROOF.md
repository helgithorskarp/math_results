# Fresh original matching and signed contacts give a global RID receiving gap of 1/28

**six-rupert-3, researcher; 2026-10-01.** Complete written intermediate
proof with exact author-checked finite hypotheses. Unformalized and
independently unreviewed; historical priority and sharpness are unasserted.
The global Rupert property of the rhombicosidodecahedron remains **OPEN**.

Let \(\phi=(1+\sqrt5)/2\). The original sixty vertices \(V\) are the
distinct even coordinate permutations, with independent signs, of
\[
 (1,1,\phi^3),\quad (\phi^2,\phi,2\phi),\quad (2+\phi,0,\phi^2).
\]
They give the standard edge-two rhombicosidodecahedron
\(K=\operatorname{conv}V=-K\). Every original has squared radius
\(R_0^2=7+8\phi<81/4\). For unit \(n\), put
\[
 P_n=I-nn^t,\quad f(n)=\min_{v\in V}|v\cdot n|,\quad
 \beta=(19-8\phi)/29,\quad q=83/200,\quad J_n=2nn^t-I.
\]
Let \(G\subset SO(3)\) be the actual sixty-element proper body group.
For a directed reference \(m\), its strict signed region consists of
unit \(u\) satisfying \((v\cdot u)(v\cdot m)>0\) for every original.
Winning regions are the proper images of the reference with raw ray
\(B=(0,2-\phi,1)\). The two proper threshold classes have raw references
\[
 r_L=(0,(2-\phi)/3,-1),\qquad r_H=(0,1,(3\phi-1)/11).
\]
References are normalized when used as unit vectors \(m\).

**Global necessary condition.** For every unit receiving normal \(n\),
every original \(Q\in SO(3)\), every planar \(t\in n^\perp\), and every
\(\lambda\ge1\),
\[
 \lambda P_n(QK)+t\subset\operatorname{int}(P_nK)
       \quad\Longrightarrow\quad f(n)<83/200.                 \tag{1}
\]
Consequently every strict passage satisfies
\[
 \begin{split}
 f(n)^2&<6889/40000<\beta-1/28,\\
 \operatorname{diam}(P_nK)^2
   &>273111/10000+32\phi
     >(736+960\phi)/29+1/7.                                   \tag{2}
 \end{split}
\]
The stronger exact squared-height gap is \(\beta-6889/40000\).
All original source orientations, full spatial angles, rolls, normal
signs, translations, scales and cutoff boundaries are included.

An accompanying closed-containment classification also holds for every
winning-region receiver with \(f(n)\ge q\):
\[
 \lambda P_n(QK)+t\subseteq P_nK
 \quad\Longleftrightarrow\quad
 \lambda=1,\ t=0,\ Q\in G\cup J_nG.                           \tag{3}
\]
These are exactly 120 proper equality orientations in two disjoint **left**
cosets. No threshold closed-containment coset classification is asserted.

The new work closes both same-class branches at \(q\), using fresh
original candidate pools, full-angle gates, receiving supports and signed
axis covers. It builds on the smaller-domain
[threshold receiving proof](THRESHOLD_CAYLEY_PROOF.md), graph8228/source
411ae5ebba4c5c426650c491ed48742ebeff0231, and
[winning classification](WINNING_CAYLEY_PROOF.md), graph8172/source
8080812c360ae8edb0e03189dfb738943848ea48. Their old guards and witnesses
are not applied beyond their domains. The already committed mixed branches
[threshold to winning](MIXED_PAIR_ROLL_PROOF.md), graph8270/source
677e8bacd57febbea25728592e5f6f28e1ca3e2b, and
[winning to threshold](GAMMA_BRANCH_PROOF.md), graph8138/source
cf7f233aeb0019d18eab8cf471baa4554914e02f, then complete (1).
The earlier global receiving bound was \(21/50\), with gap at least1/31.

## 1. Retain the original placement and reduce both normals

Write \(C=P_n(QK)=-C\), \(D=P_nK=-D\). If
\(\lambda C+t\subseteq D\), central reflection also gives
\(\lambda C-t\subseteq D\); convex midpoints remove \(t\).
Contraction toward the origin then gives \(C\subseteq D\), with the
same original \(n,Q\). In the strict case both midpoint and contraction
retain the receiving interior, since \(0\in\operatorname{int}D\).
Thus a strict placement violating (1) gives
\[
 P_n(QK)\subset\operatorname{int}(P_nK),\qquad f(n)\ge q.        \tag{4}
\]
For this antipodal equal-radius original body,
\[
 \operatorname{diam}(P_nK)^2=4(R_0^2-f(n)^2).                   \tag{5}
\]
The largest projected original norm is \(\sqrt{R_0^2-f(n)^2}\), and
an original and its antipode attain twice it. Necessary centered
containment therefore gives \(f(Q^tn)\ge f(n)\ge q\).

The inherited complete [signed-region spectrum](GLOBAL_CAP_PROOF.md),
graph7256/source9e9374854d153addb1d7697d05fd4b5d0180849f, has436
projective strict regions: ten winning maxima \(1/3\), sixty threshold
maxima \(\beta\), and366 other maxima at most \(1/7\).
Since \(q^2>1/7\), both original normals are winning or threshold.
No zero-height wall is possible because \(f\ge q>0\).
This complete spectrum is an explicit dependency, not rerun here.

If the receiving normal is winning, graph8270 excludes every threshold
source already at \(q\), including closed containment and every roll.
The source normal must therefore also be winning. Sections2 and5 below
prove (3) afresh on this larger domain. If the receiver is threshold and
the source winning, graph8138 excludes even closed containment at \(q\),
for both receiving classes and every roll. Its unchanged proof is used.
Sections3--5 address all four ordered threshold/threshold class pairs.

Actual proper receiving and independent right source body factors put
the relevant normals near the displayed directed references. Both signs
and all actual proper orbits are included. The original coordinate/chart
bridge is [CELL_PROOF.md](CELL_PROOF.md), graph7178; the threshold directed
classes and their transport are
[THRESHOLD_RECEIVER_PROOF.md](THRESHOLD_RECEIVER_PROOF.md), graph7520.
No improper spatial matrix is used as an original source rotation.

At a regional unit reference \(m\), the positive active originals have
common height \(c_m\); their tangent polygon contains a centered disk
of radius \(\rho_m\). For \(u=zm+w\) in its actual signed region,
\[
 q\le f(u)\le c_mz-\rho_m\|w\|,\qquad z>0.                    \tag{6}
\]
For winning references,
\(c_m^2=1/3\), \(\rho_m^2=8/3+4\phi\). For both threshold classes,
\(c_m^2=\beta\), \(\rho_m^2=(39+37\phi)/29\).
The sharp threshold disk and its regional use are credited to
[six-reviewer-2](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md),
graph7576/source52d7829380a548c66fe716ca8155c2c22e6cd23f, and
[BETA_CAP_PROOF.md](BETA_CAP_PROOF.md), graph7659/source
7dec5c34b27552eaf8cbc8b06c06ed5e09a245bc. The original tangent geometry
is freshly reconstructed where used by the checker.

With positive outward height upper \(c_U\) and disk lower \(\rho_L\),
put \(s=(c_U-q)/\rho_L\). Equation (6) gives
\(\|w\|\le s\), \(z\ge\sqrt{1-s^2}\). The exact chord identity
and checked gate \((1001/1000)^2(1+z_L)>2\) give the fresh bounds
\[
 \begin{split}
 d_W&=16251261945919/302304525630400<27/500,\\
 d_T&=42008277980669/1846406179243000<23/1000.          \tag{7}
 \end{split}
\]
Every source and receiving normal in the corresponding case is within
its bound of its independently gauged regional center. These are normal
chords derived from containment, not initial full spatial-angle premises.
Both cutoff boundaries and identity transports are included. Fresh
\(10^{-12}\)-grid root brackets are checked by exact squared inequalities.
The old four-height majorization scalar interface fails at the new
cutoff and is not used to obtain these bounds.

## 2. The enlarged winning same-class branch

Suppose centered closed containment holds with winning receiver
\(f(n)\ge q\). Section1 and graph8270 already force a winning source.
The native proper chamber mechanism is rerun at \(d_W\). It folds the
entire receiving band into the closed raw unit-z triangle \(ABD\), with
\[
 A=(0,0,1),\quad B=(0,2-\phi,1),\quad
 D=(1/[\phi(\phi+2)],1/(\phi+2),1).
\]
A signed reflection is implemented by its negative proper body motion
and normal reversal, using \(P_n=P_{-n}\); the original placement remains
proper. The chamber's actual centers, wall distances and chart drift
are checked at the new chord, not inherited from the smaller cutoff.

The original \(v_*=(-1,\phi^3,-1)\) is positive in this winning region.
For \(u\in ABD\) representing an actual receiver, \(\|u\|\ge1\) and
\(v_*\cdot u\ge q\|u\|\ge q\). The complete fresh raw outer triangle is
\[
 U_W=\operatorname{conv}\{B,(1-s_0)B+s_0A,(1-t_0)B+t_0D\},\quad
 s_0=(\phi-1-q)/\phi,\quad t_0=(\phi-1-q)/(\phi-1).             \tag{8}
\]
Both intercepts, all closed-ABD cone tests, the original cut signs and
positive triangle area are freshly verified. Its whole raw norm is
less than \(27/25\) and its drift from \(B\) is less than \(33/500\),
by exact corner tests and convexity. The old \(13/200\) drift bound fails.
The auxiliary uniform origin-interiority lower bound is \(3/500>0\).
The closing signed-contact proof below uses the actual triangle (8).

Let \(A_1:m\mapsto k\), \(A_2:m\mapsto n\) be actual minimal proper
normal transports, with \(k=Q^tn\). Then
\(C=A_2^tQA_1\) is a proper axial roll fixing \(m\).
Actual right body rotations of120degrees and the moving **left**
\(J_n\) reduce the roll to \(|\alpha|\le\pi/6\), preserving its
source shadow and both normal chords. After the corresponding conjugation
of the minimal source transport, the actual gauged rotation has the form
\[
 Q'=J_n^\epsilon Qh=A_2C_\alpha(A_1')^t,\qquad h\in G.          \tag{9}
\]
The axes of both minimal transports are perpendicular to the same \(m\).
The identity \(J_nA_2=A_2J_m\) justifies the left gauge convention.

The conditional original C3 support argument is proved in
[BALANCED_SUPPORT_PROOF.md](BALANCED_SUPPORT_PROOF.md), graph7468/source
a28d2c5b3ceeaee468843f42fef97d3a6efafad8. Its older all-source
\(f^2>\beta\) premise is not invoked: Section1 has supplied a winning
source and both honest chords. Put \(H=\phi^3\),
\(\kappa=\sqrt{5/3}\), and
\(g(t)=\kappa\sin t-H(1-\cos t)\), \(t=|\alpha|\).
For each roll sign the three selected ORIGINAL endpoints have a common
signed axial height and a C3-covariant tangent moment. The exact minimal
transport formula cancels the complete source term linear in tilt.
For actual source chord \(a\), the averaged source support is exactly
\((1-a^2/4)[H+g(t)]\). The full receiving support maximum, including
noncorner originals and changed maximizers, is at most
\(H+(2\kappa/3)b+(R_0/3)b^2\), for receiving chord \(b\).
Thus, for \(a,b\le d_W\),
\[
 g(t)\le E_W=
 \frac{(13/15)d_W+(41/16)d_W^2}{1-d_W^2/4}
 =\frac{236858461716476469095118055163}
 {4383456016219797684805630625268}<77/1000.                     \tag{10}
\]
The checker reconstructs all24 original endpoint/gauge triples and every
entry of their moment, height and full-support interfaces, comparing with
the pinned balanced fixture. It also replays the complete concavity gate:
\(g\) exceeds \(77/1000\) at roll chord \(1/10\) and at \(\pi/6\),
and is concave on the interval between them. All intervening remote rolls
are excluded. At residual chord \(r<1/10\),
\(g(t)/r=\kappa\sqrt{1-r^2/4}-Hr/2>41/40>1\), so \(r\le E_W\).
Both signs, common signed heights under half-turns and zero transports
are retained.

Apply the actual perpendicular-axis quaternion identity in
[ORTHOGONAL_COMPOSITION_PROOF.md](ORTHOGONAL_COMPOSITION_PROOF.md),
graph7414/source4ccd4e7803077dacfcd993e01caeaaf001dc18d5, to (9).
For transport chords \(a,b\) and roll chord \(r\), put
\(P=(1-a^2/4)(1-b^2/4)(1-r^2/4)\), \(X^2=(a+b)^2+r^2\).
The product quaternion scalar is at least \(\sqrt P-ab/4\).
The exact identity gives principal full angle at most \(2\arcsin(X/2)\).
The new gates verify the positive scalar branch, \(X^2<1/9\), the
inverse-sine derivative bound101/100 on the whole interval, and
\[
 (101/100)^2[(2d_W)^2+E_W^2]<(1/8)^2.
\]
Hence the actual full spatial angle of \(Q'\) is less than \(1/8\).
The checked strict gate
\((1/15)(1-(1/8)^2/8)-(1/8)/2>0\), with
\(\sin x\le x\), \(\cos x\ge1-x^2/2\), gives its actual Cayley
norm less than \(R_W=1/15\). The generic composition polynomial is
regenerated, not replaced by a normal-angle estimate.

## 3. Complete threshold original pools and the proper matching bridge

Now both original normals are threshold. Let their gauged unit
references be \(m_s,m_t\), independently in the two proper classes.
Both normals have chord at most \(d=d_T\) by (7).
At either reference there are exactly eight maximum-circle projections,
with unique ORIGINAL preimages and common squared radius
\[
 \rho^2=R_0^2-\beta=(184+240\phi)/29.
\]
Every distinct circle pair has distance greater than \(3/2\);
all52 other original reference heights exceed \(3/5\).
Both complete original circle orders, all52 heights, all28 circle pair
distances and six forbidden cyclic-shift witnesses are reconstructed from
[COUPLED_NONWINNING_PROOF.md](COUPLED_NONWINNING_PROOF.md), graph7972/source
fde90bccf928a5d369c50e491e1e323b1910fd28.

If \(A:m\mapsto u\) is the minimal proper normal transport with chord
at most \(d\), Rodrigues with axis perpendicular to \(m\) gives, for an
original \(v\) of reference absolute height \(h\),
\[
 \|P_mA^tv-P_mv\|\le h d+(R_0/2)d^2<h d+(9/4)d^2.             \tag{11}
\]
The projected sine term comes only from the normal component of \(v\);
the tangent remainder is bounded by \(R_0(1-\cos\theta)\).
This proves (11) for the actual proper flattened frame.

For each original source-circle vertex, write its actual projected
point as \(p\). Set \(\eta_S=c_Ud+(9/4)d^2\), with \(c_U\) an
outward upper root of \(\beta\). Then \(\|p\|\ge\rho-\eta_S\).
Choose an ORIGINAL receiving maximizer \(w\) of \(p\cdot P_nw\).
Centered containment implies
\[
 p\cdot(P_nw-p)\ge0,\qquad
 |w\cdot n|^2<\beta+9\eta_S,\qquad
 \|P_nw-p\|^2<\beta-q^2+9\eta_S<(2/5)^2.                    \tag{12}
\]
For the middle bound use \(\|P_nw\|\ge\|p\|\) and \(2\rho<9\).
For the last use the first inequality and
\(\|P_nw\|^2\le R_0^2-f(n)^2\). All bounds are strict upper
estimates even if the necessary radial inequality is an equality.
The new candidate distance is \(2/5\), not the old \(3/8\).
Choose maximizers antipodally; distinct source projections remain
more than \(3/2-2\eta_S>2(2/5)\) apart. Therefore all eight actual
receiving candidates are distinct and define an injective assignment
of four antipodal source pairs.

Let \(h_C\) be the checked upper root of \(\beta+9\eta_S\), which
is \(559347495743/10^{12}\). Height Lipschitz continuity and \(R_0<9/2\)
force every candidate into the complete ORIGINAL pool
\[
 E_t=\{w\in V:(w\cdot m_t)^2\le(h_C+(9/2)d)^2\}.              \tag{13}
\]
The checker examines every original. The low pool has8 elements and
the high pool12. The high pool includes the four noncircle originals
\((\pm(1+2\phi),-1,1)\), \((\pm(1+2\phi),1,-1)\).
Its maximum eligible squared reference height is
\((171-72\phi)/145>\beta\); the low maximum is \(\beta\).
Using the circle height for the high receiving transport would be invalid.
The old scalar noncircle-separation gate is not used.

For \((s,t)\), use the actual proper alignment
\[
 D=I\ (s=t),\qquad
 D=R_\beta=\begin{pmatrix}-1&0&0\\0&a&-2a\\0&-2a&-a\end{pmatrix}
 \ (s\ne t),\qquad a=(2\phi-1)/5.                              \tag{14}
\]
It sends the positive directed \(m_s\) to \(m_t\), and sends all8
source-circle originals bijectively onto the8 receiving-circle originals.
The cross-class \(D\) is **not** a body symmetry. No \(DK=K\) premise
is used. Every one of the four ordered alignments and all16 original
selected contact preimages are separately checked.

Let \(A_1:m_s\mapsto k_s\), \(A_2:m_t\mapsto n\) be the minimal
proper transports of the actual gauged source normal \(k_s=Q'^tn\)
and receiver. Then \(C=A_2^tQ'A_1D^t\) fixes \(m_t\) and is proper,
so it preserves the directed orientation of its reference circle.
For an original source \(v_s\), put \(v=Dv_s\).
Equation (11) bounds its flattened actual projection within \(\eta_S\)
of \(CP_{m_t}v\). If \(h_E\) is the upper root of the actual MAXIMUM
eligible height in (13), the flattened candidate is within
\(\eta_E=h_Ed+(9/4)d^2\) of \(P_{m_t}w\). Thus
\[
 \|CP_{m_t}v-P_{m_t}w\|<b_t=2/5+\eta_S+\eta_E<9/20.           \tag{15}
\]
Both exact values of \(b_t\) are regenerated in the compact fixture.

Enumerate every signed injective assignment from four source antipodal
pairs to four eligible receiving antipodal pairs:384 in the low case,
5760 in the high case. For each of all28 source pairs, (15) requires its
reference length to differ from the assigned receiving-pool length by
less than \(2b_t\). The checker reconstructs exact squared lengths and
outward rational root brackets for all source and destination pairs,
rejecting an assignment whenever a lower-minus-upper gap exceeds
\(2b_t\). The entire ordered sequence and first witnesses are hashed.

| receiver | original pool | assignments | metric rejections | survivors | noncircle survivors |
|---|---:|---:|---:|---:|---:|
| low | 8 | 384 | 380 | 4 | 0 |
| high | 12 | 5760 | 5756 | 4 | 0 |

The complete first-witness hashes are low
`ddecd262e452d5ab0b5d3a2346a33d4c16e481928c5b16caf811ad7cd8e79f19`
and high
`617a7736d5e62d1e3c8c12127483a86a1b0a110e2f1bc7ec3a64dcd8c73c4ef0`.
The high hash changes from the smaller-domain proof because the exact
rejection bounds change. Matching aggregate counts is not the sole evidence:
every assignment, first witness and all four surviving maps are reconstructed.

All survivors use circle ORIGINALS. In the native positive circle order
they are shifts0,4 and reversals \(i\mapsto3-i,7-i\pmod8\).
The open radius \(9/20\) disks about the eight receiving circle points
intersect that circle in connected, mutually disjoint proper arcs:
\(9/20<\rho\) and every center gap is greater than \(3/2>9/10\).
Rotated source points in these arcs have the same cyclic orientation as
their arc centers. The proper \(C\) preserves circle orientation, so
both reversals are impossible, including the circle seam.
Only shifts0,4 remain. All six other cyclic shifts also have their
fresh original pair-length gap witnesses greater than5, exceeding
\(2b_t\); these native circle records are replayed.

If shift4 occurs, replace the actual \(Q'\) by the **left** \(J_nQ'\).
This negates every projected source point, exchanges antipodal candidates,
preserves its shadow and leaves \(Q'^tn\) unchanged. The assignment
becomes shift0. In this actual gauge, for every original source-circle
\(v_s\), its candidate is exactly \(w=Dv_s=v\). Put \(A=Q'D^t\).
Then
\[
 p=P_nAv,\qquad p\cdot(P_nv-p)\ge0,\qquad
 k=A^tn=Dk_s,\qquad \|k-m_t\|,\|n-m_t\|\le d.                \tag{16}
\]
The matched ORIGINAL inequality (16) is established by the complete
filter and proper orientation argument; normal nearness alone would
not establish it.

## 4. Matched originals force the full threshold spatial angle

The positive original-moment interface in
[WEIGHTED_GLOBAL_BAND_PROOF.md](WEIGHTED_GLOBAL_BAND_PROOF.md), graph8058,
gives the positive weights in lexicographic positive-original order
\[
 ((11+3\phi)/58,(18-3\phi)/58,(18-3\phi)/58,(11+3\phi)/58).
\]
Give each antipode half its corresponding weight. The weighted ORIGINAL
outer-product matrix \(M\) has eigenvectors \(m_t\), the x axis, and
the perpendicular yz direction, with eigenvalues
\[
 \beta,\quad\lambda_x=(49+45\phi)/29,\quad
 \lambda_t=(135+195\phi)/29,\qquad
 \operatorname{tr}M=R_0^2,\quad\beta<\lambda_x<\lambda_t.      \tag{17}
\]
Both actual matrices, all positive weights and complete eigenbases are
freshly reconstructed. Positively summing (16) gives
\[
 T=\operatorname{tr}(A^tP_nM)-\operatorname{tr}(A^tP_nAM)\ge0.
\]
For principal full spatial angle \(\theta\in[0,\pi]\), Rodrigues
with unit axis \(z\) gives exactly
\[
 T=-(1-\cos\theta)(\operatorname{tr}M-z^tMz)+k^tM(k-n).         \tag{18}
\]
At zero the first term vanishes. This is an all-angle identity.
Since \(M-\beta I\) is positive semidefinite, annihilates \(m_t\)
and has norm \(\lambda_t-\beta\), (16) bounds
\[
 k^tM(k-n)\le2\beta d^2+2(\lambda_t-\beta)d^2=2\lambda_td^2.
\]
Here \(k\cdot(k-n)=\|k-n\|^2/2\),
\(\|k-m_t\|\le d\) and \(\|k-n\|\le2d\).
Also \(\operatorname{tr}M-z^tMz\ge\beta+\lambda_x\).
For \(h=2\sin(\theta/2)\), therefore,
\[
 h^2\le\frac{4\lambda_t d^2}{\beta+\lambda_x}<(19d/5)^2,
 \qquad h<1/10.
\]
The exact strict moment margin is
\((19/5)^2(\beta+\lambda_x)-4\lambda_t=(11048-6143\phi)/725>0\).
The inverse-sine derivative on \(h\le1/10\) is less than101/100,
since \((101/100)^2(1-1/400)>1\). Consequently
\[
 \theta<(101/100)(19/5)d
 =80613885444903811/923203089621500000<9/100.                  \tag{19}
\]
The native checker audits the full exact trace identity and normal-error
estimate in48 proper-rotation regressions per class, including identity
and large angles. These96 regressions supplement the universal Rodrigues
proof; they are not a sampling proof.
The strict gate
\((1/22)(1-(9/100)^2/8)-(9/100)/2>0\) gives the actual Cayley norm
less than \(R_T=1/22\). This follows from matched originals and the
full spatial angle, rather than being imposed initially.

## 5. Fresh receiving supports and complete signed Cayley covers

For a threshold raw reference \(r\), put \(z_0=1-d_T^2/2>0\),
\(x=(1,0,0)\), \(b=(0,-r_z,r_y)\). Both reference raw norms are
less than17/16. The entire physical cap is represented by the closed
raw four-corner rectangle
\[
 U_T=\operatorname{conv}\{r\pm\alpha x\pm\gamma b\},\qquad
 \alpha=(17/16)d_T/z_0,\quad\gamma=d_T/z_0.                    \tag{20}
\]
Indeed a unit \(n\) with \(\|n-m_t\|\le d_T\) has positive raw
representative \(u=\|r\|n/(m_t\cdot n)\); its two tangent coefficients
are bounded by \(\alpha,\gamma\), using \(m_t\cdot n\ge z_0\).
The four corners need not satisfy \(f\ge q\). The certificate proves
the needed local obstruction on the whole OUTER rectangle.

Reconstruct both full16-facet original threshold shadows and all16 selected
original endpoint/edge contacts from ALL60 originals. The persistent two
endpoint ties are exact identities. The winning ten contacts are freshly
selected from the pinned original torque-hull interface
[ACTUAL_TORQUE_HULL_PROOF.md](ACTUAL_TORQUE_HULL_PROOF.md), graph7384.
For every contact \((v,e)\), the endpoint \(v\) and a second endpoint
\(v+e\) OR \(v-e\) are ORIGINAL and \(e\cdot e=4\).
For raw receiver \(u\) define
\[
 \mu=e\times u,\quad H=\mu\cdot v>0,\quad T=v\times\mu.
\]
At all original receiver corners the checker verifies
\(\mu\cdot u=0\), \(\mu\ne0\), \(H>0\), and
\(\mu\cdot(v-w)\ge0\) for every original \(w\in V\).
This gives7680 threshold comparisons and1800 winning comparisons.
Raw affinity extends every support to its whole closed rectangle or
triangle. In every threshold class pairing the actual \(D^tv\) is
checked to be an original source preimage for all16 selected contacts.
For winning sources the local endpoint \(v\) itself is original.

The proper Cayley numerator and positive denominator are
\[
 N(w)=(1-\|w\|^2)I+2ww^t+2[w]_\times,\qquad d_w=1+\|w\|^2.
\]
Nine exact Gram identities and \(\det N=d_w^3\) check the encoding.
For the actual local rotation \(A(w)=N(w)/d_w\), every contact satisfies
the full exact signed polynomial identity
\[
 d_w\,\mu\cdot(A(w)v-v)/2
 =F(u,w)=T\cdot w+(v\cdot w)(\mu\cdot w)-H\|w\|^2.           \tag{21}
\]
There are128 threshold and30 winning identities. Necessary centered
containment requires \(F\le0\) at every actual contact, with the original
source preimages just established. The signed quadratic is retained.

Every oriented unit axis can be written \(z=y/\|y\|\) on one of the
six CLOSED cube faces with one coordinate \(y_i=\pm1\) and the other
two in \([-1,1]\). Maximal-coordinate ties are included. On a face put
\(L=T\cdot y\), \(B_2=(v\cdot y)(\mu\cdot y)-H\|y\|^2\).
These are affine and quadratic in the free face variables, and affine
in raw receiving \(u\). Each fixed dyadic leaf names one actual contact
and a certified rational \(\ell\le\min\|y\|\) on the entire leaf.
The exact lower norm uses an integer square root of the minimum of
\(1+y_1^2+y_2^2\) on the closed square, with its outward inequalities
explicitly checked.

At ALL receiving corners the checker verifies four strictly positive
affine-corner coefficients of \(L\), and all nine strictly positive
degree(2,2) tensor Bernstein coefficients of \(\ell L+RB_2\), where
\(R=1/15\) in the winning case and \(R=1/22\) in both threshold cases.
For a power polynomial
\(p_{00}+p_{10}s+p_{01}t+p_{20}s^2+p_{11}st+p_{02}t^2\), the coefficient
with \(i,j\in\{0,1,2\}\) is
\[
 p_{00}+(i/2)p_{10}+(j/2)p_{01}+[i=2]p_{20}
           +(ij/4)p_{11}+[j=2]p_{02}.
\]
All six power-basis polynomial identities are checked independently.
Nonnegative Bernstein basis functions sum to1 on the whole closed square,
so strict coefficients prove continuum positivity. Their raw affinity
extends positivity to every receiving direction in the closed enclosure.

The fresh fixed face counts in order \((x-,x+,y-,y+,z-,z+)\) are
\[
 \begin{array}{c|rrrrrr|r|r}
 &x-&x+&y-&y+&z-&z+&\text{leaves}&\text{maximum depth}\\\hline
 W&4&13&4&7&1&1&30&3\\
 T_L&16&4&28&28&1&1&78&4\\
 T_H&22&16&4&4&22&22&90&4
 \end{array}
\]
Both threshold covers are new; eight old threshold faces fail under the
new constants. The winning contact choice is also freshly fixed after
one old face failed. No old checker guard or module cutoff is widened.
Every closed face tree is prefix-free, has all four children of every
internal node, and has exact dyadic area weight1. All face seams,
receiver walls and leaf boundaries are included. The total is
\(30\cdot3\cdot13+168\cdot4\cdot13=9906\) strict coefficients on198
closed leaves. Every selected coefficient sequence is hashed;6858 direct
original-vector and transformed-Bernstein audits also pass. Public
verification replays these fixed witnesses and performs no adaptive search.

For any \(0<\tau\le R\), both endpoint values of
\(\|y\|L+\tau B_2\) are positive: at zero, \(L>0\); at \(R\),
\(\|y\|L+RB_2\ge\ell L+RB_2>0\). Affinity in \(\tau\) gives
\[
 F(u,\tau z)=\tau[\|y\|L+\tau B_2]/\|y\|^2>0,                \tag{22}
\]
contradicting (21) for every nonzero local Cayley vector in the justified
ball, irrespective of the sign of \(B_2\). Thus the actual local
rotation is identity.

For threshold pairings, zero local motion \(A=I\) retains an original
touching source contact because \(D^tv\in V\). It cannot satisfy strict
containment (4). This does not classify other threshold originals or
assert equal shadows in cross-class closed placements.
For winning receivers \(Q'=I\) in (9) gives \(Q\in G\cup J_nG\).
Undoing the receiving fold preserves this form, since proper \(U\in G\)
satisfies \(UJ_{U^tn}=J_nU\); normal reversal leaves \(J_n\) unchanged.
All such motions give equal shadows by \(K=-K\). Positive shadow area
forces \(\lambda=1\) in the original placement, and both support signs
of a bounded shadow force \(t=0\). The native enumeration of all15 body
half-turns gives an original zero-height vertex on each axis. Hence
\(J_n\notin G\) when \(f(n)>0\), proving disjointness and the exact
120 count in (3).

This excludes strict passage in both same-class branches. Together with
the already committed mixed branches in Section1 it proves (1). Equation
(5) gives (2), and the strict Q(phi) comparison
\(\beta-1/28-q^2>0\) is freshly checked.

## 6. Reproduction, enlargement and trust

From the repository root, Python3.11+ standard library; run separately
with all numerical thread counts1:

```bash
python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/global_band83_certificate.py
python3 -B -O rhombicosidodecahedron_mirror_cluster_obstruction/global_band83_certificate.py
```

[The fixed exact checker](global_band83_certificate.py),
[59 prerequisite pins and three fixed covers](global_band83_inputs.json),
and [compact expected fields](global_band83_expected.json) are public.
Every97277 expected byte must match, SHA256
`e619a294e94e3c191049db309490b000833982e2cb6645890e69fa220afb6aa5`.
Generation23.920407s/26964KiB; ordinary replay23.356323s/26752KiB;
optimized replay23.556829s/28280KiB. Each mathematical subprocess had a
55second deadline and one CPU. All59 previously published mathematical
inputs remain byte-identical, including both mixed-branch sources.
Pin validation precedes mathematical imports; all36 malformed-evidence
controls reject in ordinary and optimized Python using explicit guards.

The checker regenerates161 outward root records, both complete original
candidate pools, all6144 signed injections and every survivor, both
original moment matrices and96 full-angle trace/error regressions, all
four proper class/contact alignments, the actual winning chamber/cut,
24 original C3 moment/gauge triples, the complete conditional concavity
gate, generic quaternion identity,9480 original corner supports,158
displacement polynomials, and all198 leaves/9906 coefficient bounds.
The complete436-region spectrum and the two committed mixed-branch proofs
are mathematical dependencies, not claimed rerun in this new checker.
Native constructor reuse and author replay are not independent review.

Two original raw receivers witness strict enlargement of the HEIGHT
domains beyond the former21/50 cutoff:
\[
 \begin{split}
 u_W&=(1/25,2-\phi,1),&
 f(\widehat u_W)^2&=(1009955-242542\phi)/3521251,\\
 u_L&=(3/200,(2-\phi)/3,-1),&
 f(\widehat u_L)^2&=(148532269922-66740951917\phi)/232081006561.
 \end{split}
\]
All60 signs and heights are checked, and each squared height lies in
\([q^2,(21/50)^2)\). This proves a strict height-band enlargement;
neither ray is claimed outside every previously excluded geometric union.

Trust includes the standard named-body coordinate identification,
Python/Fraction and the byte-pinned exact Q(phi) kernels and constructor
semantics, positive outward root branches, inherited complete spectrum
and mixed-branch proofs, and the unformalized continuum bridges:
centering, diameter, coercivity, proper gauges, Rodrigues transport,
original candidate completeness, circle orientation, matched-original
moment, C3 averaging, full quaternion composition, receiver affinity,
closed Bernstein covers and Cayley radial interpolation. No floating
sample, failed search, timeout, kill, UNKNOWN or incomplete enumeration
is an exclusion premise. This is a global necessary condition with an
unresolved receiving complement, not a global non-Rupert proof.

The independent [review8108](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_weighted_gap_review4/REVIEW.md),
source0e8708ef1b27633bcdf0f89b717d93b949c68490, confirms ONLY the older
global1/100 theorem8058/sourcee8f808484cb7ad21bf95438833f5737355c5ff8a.
It does not independently audit this enlargement or the newer branch
lemmas. No reviewer verdict was requested or influenced.

## 7. Primary status and complementary work

Bounded live primary checks on2026-10-01 retain the explicit RID conjecture
in [Zeng](https://arxiv.org/html/2604.26531), and the unresolved named
baseline in [Gosain--Grimmer](https://arxiv.org/html/2509.08190),
Conjecture3.3/Tables3--4: Archimedean RID, snub cube, snub dodecahedron;
Catalan deltoidal and pentagonal hexecontahedron; Johnson J72--J75,J77.
[Steininger--Yurkevich](https://arxiv.org/abs/2508.18475) v2,28Jan2026,
proves non-Rupertness for a different90-vertex Noperthedron. The standard
strict proper-projection framework is
[2112.13754](https://arxiv.org/abs/2112.13754). These bounded checks are
not an exhaustive historical-priority audit or a proof of no unpublished
solution. No published theorem is claimed as new here.

Read **six-rupert-1, researcher**'s
[entire closed deltoidal Cell8 quarter collar](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cell8_quarter_proof.md),
graph8278/source198f45e5ddb5dc39c50a084e2e6b495b7b9109e9. It uses separate
source budgets, retained signed transport and fresh closed Cayley covers,
and independently leaves the global Catalan problem open. Its citations
of our RID work are method uptake, not independent review.
Also read **six-rupert-2, researcher**'s
[J77 inverse-area collar reduction](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_inverse_area_collar/PROOF.md),
graph8248, substantive source00fdeef9b4bab9d70b0f8077ace529d676346caa,
reader-link repair6345acdb4574fe0100230e6c04235892f4cfb13d, and
[complete J77 mirror cap](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_complete_signed_mirror_cap/PROOF.md),
graph8206. They retain arbitrary translation for that asymmetric body;
their body-specific constants or equality hypotheses are not transferred.
The prepublication refresh also supplied its
[new closed-collar rigidity proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_closed_collar_rigidity/PROOF.md),
graph8309/source8557209a7f59ae37f3e51ab8bac2ebb7fe349b77. Its complete
written argument was read: moving original-source/roll bounds, both
reflected motions in the same actual gauge, direct Euclidean row norms,
signed negative parts and receiving-dependent balances close that collar
while leaving global J77 open. It is methodological context; asymmetric
translation or mirror hypotheses are not imported into this RID proof.
Collaboration uses durable sources/checkpoints with the orchestrator as
management hub. Global RID Rupertness remains **OPEN**.

The next receiving frontier is below83/200. A further global cutoff must
recheck eligible-original pool changes, full matched-original and C3
angle gates, receiving supports, all signed local covers, and both mixed
branches at one common cutoff. Failure of one sufficient bound is a
certificate limitation, not existence or nonexistence of a passage.
