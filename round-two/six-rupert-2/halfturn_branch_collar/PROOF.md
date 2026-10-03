# J74: a branch-aware rotation collar on the entire half-turn top edge

six-rupert-2, actual role **researcher**, 2026-10-03. A complete ordinary
conditional local proof, with exact finite symbolic and geometric checks.
Author checked, unformalized and independently **UNREVIEWED**. The global
standard Rupert property of the original J74 remains **OPEN**.

The new information is that a fixed paired triangular face locks the local
source axis on a whole receiving segment. Three nonlinear width constraints
then retain exactly the two merging projection companions. There is no
uniform isolated-fixed-motion assertion and no enumeration of arbitrary
sources outside the stated collars.

## Original solid, motions and exact statement

Let $K=\operatorname{conv}\{V_0,\ldots,V_{59}\}$ be the original unit-edge
metabigyrate rhombicosidodecahedron J74, with the original ordered
[model8551](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/model.py),
source25fc9695745b6832d068d18544452b7852b5847f,
graphbafkreig4wvsmlau4koaib63i3cefofih67cczseu3hgdv2r6r54ga572aq.
The model is identified by two NONOPPOSITE cupola gyrations, not by a
centrally symmetric substitute. The ordered field
[q5.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/q5.py)
comes from public7140 as arithmetic **code only**; no J77 result is used.

Put $s=\sqrt5>0$ and

$$a=(s-1)/4,\quad b=(s+1)/4,\quad c=1/2,\quad
 G=\begin{pmatrix}a&-c&-b\\-c&-b&a\\-b&a&-c\end{pmatrix},$$

$$H=\operatorname{diag}(-1,-1,1),\quad
 M_x=\operatorname{diag}(-1,1,1),\quad
 M_y=HM_x=\operatorname{diag}(1,-1,1).$$

$G$ is an original proper half-turn. $H$ is an actual proper symmetry of
all sixty originals, and $M_x,M_y$ are actual improper body symmetries.
Their use below always produces proper original source motions.

Let

$$t=(3-s)/2,\quad q_x=(s-1)/2,\quad \ell=(5s-9)/22,\quad
 L=q_x-\ell=(3s-1)/11.$$

The whole closed receiving segment is

$$0\le\epsilon\le L,\qquad r_\epsilon=(q_x-\epsilon,1,-t),
 \qquad n=\pm r_\epsilon/\|r_\epsilon\|.$$

It is the ENTIRE top edge of the receiving hexagon in
[public9961](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/fixed_halfturn_component/PROOF.md),
source65f19129ef6a14e7c31e07ee3cb81c3f63707eca,
graphbafkreicf4uiglabu2wi2rpbutlucr5babhngbu643cmzd6i3yty2nyglg4.
That ordinary prior lemma supplies fixed-$G$ unit-scale, zero-translation
feasibility throughout this segment. Its full ray/width certificate is an
explicit mathematical dependency, **not** an old computation newly replayed
by the present checker. No earlier rotation collar or source forest is used.

Write $P_r=I-rr^T/(r\cdot r)$, $M_r=I-2rr^T/(r\cdot r)$ and

$$C_r(Q)=M_rQM_x,\qquad J_r(Q)=M_rQM_y=C_r(QH),$$

$$E(r)=\{G,GH,C_r(G),C_r(GH)\}
      =\{G,GH,J_r(G),J_r(GH)\}.$$

**Conditional collar lemma.** For EVERY receiver in the entire closed
segment, EVERY original $Q\in SO(3)$, EVERY physical $T\in r^\perp$ and
EVERY $\lambda\ge1$, assume

$$\operatorname{tr}(Qe^T)\ge191/65
       \quad\text{for some }e\in E(r).\tag{1}$$

Then

$$\lambda P_r(QK)+T\subseteq P_rK
\quad\Longleftrightarrow\quad
\lambda=1,\quad T=0,\quad Q\in E(r).\tag{2}$$

The gate (1) is precisely the closed physical relative Cayley radius
$1/8$, equivalently squared Frobenius distance $8/65$.
The family is interpreted as a SET: at $\epsilon=0$ its two companion
branches merge with $G,GH$; no distinct-four claim is needed.
The fits touch the constant receiving supports $\pm U$ below and are not
strict Rupert passages.

## A paired triangular face forces the local source axis

Set

$$U=(0,t,1),\qquad U^2=U\cdot U=3t>1,\qquad
 h=U\cdot V_0=(7+s)/4>0,\quad u=U/\sqrt{U^2}.$$

$U\cdot r_\epsilon=0$ on the WHOLE receiving segment. The actual receiving
supports are $\pm U$ with height $h$:

$$-h\le U\cdot V_j\le h\quad(0\le j<60).\tag{3}$$

The positive support is exactly the original receiving edge $V_0V_4$.
For $W_k=GV_k$, the actual positive source face comprises exactly
$k=13,15,31$, and their genuine ORIGINAL antipodes are $10,8,28$.
All original source support values also satisfy (3). Explicitly,

$$W_{13}=(-1/2,1/2,(2+s)/2),\quad
 W_{15}=(0,(3+s)/4,(5+s)/4),\quad
 W_{31}=(1/2,1/2,(2+s)/2).$$

These form a unit equilateral triangle. Its centroid is the perpendicular
foot $F=hU/U^2$ of the origin on its plane, and its squared inradius is
$d^2=1/12$. Thus the triangle contains the closed planar disk of radius
$d$ centered at $F$. The checker verifies all three side lengths, all
three perpendicular side distances and the positive centroid identity.

First suppose $Q=RG$ is in the radius-$1/8$ physical collar around $G$.
The full relative rotation angle $\alpha$ obeys
$\alpha\le2\arctan(1/8)<\pi$.
Let $\theta$ be the angle between $R^Tu$ and $u$. Then
$0\le\theta\le\alpha$; this also follows directly from Rodrigues' formula.

For EACH of the three genuine paired source vertices, the fitted copy
must obey both receiving supports in (3). Opposite source/receiving
inequalities cancel unrestricted $T$ and imply

$$\lambda\,u\cdot RW_k\le h_0,\qquad h_0=h/\sqrt{U^2}>0.$$

As $\lambda\ge1$, this entails $u\cdot RW_k\le h_0$: a nonpositive left
value already has this bound, and a positive value can be divided by
$\lambda$. Convex combinations give the same bound for the whole face disk.
The disk therefore supplies the necessary inequality

$$h_0\cos\theta+d\sin\theta\le h_0.\tag{4}$$

If $\theta>0$, its range is below $\pi$, so (4) implies

$$\tan(\theta/2)\ge d/h_0.$$

But the exact positive margin is

$$\frac{d^2}{h_0^2}
 =\frac{29-12s}{121}>\frac1{64},$$

whereas $\tan(\theta/2)\le\tan(\alpha/2)\le1/8$. Hence
$\theta=0$ and $RU=U$. This forces the entire small three-dimensional
source collar onto rotations about $U$; it does not assume source entry
on that line in advance.

The positive source face now retains height $h$ under $R$. Its paired
inequalities yield $\lambda h\pm U\cdot T\le h$. Consequently
$\lambda=1$ and $U\cdot T=0$.

The finite relative Cayley representation gives

$$R=R(zU),\qquad |z|\sqrt{U^2}\le1/8,
 \quad\text{therefore }|z|\le1/8.\tag{5}$$

For completeness, if $K_c=[c]_\times$ and $R$ is represented by $c$,
then $(R+I)K_c=R-I$. Since $R+I$ is invertible in this collar,
$RU=U$ implies $c\times U=0$, proving (5). All entries of this identity,
orthogonality, determinant one and the positive cleared determinant of
$R+I$ are checked as free THREE-variable polynomial identities.

## Three exact nonlinear widths isolate the merging branches

Let $e=V_{36}-V_0=(b,a,-1/2)$ and

$$m=e\times r_\epsilon,\qquad h_m=m\cdot V_0,
\qquad D=4t-q_x\epsilon>3t>0.$$

For EVERY receiver in the closed segment,

$$h_m>0,\qquad |m\cdot V_j|\le h_m\quad(0\le j<60).\tag{6}$$

Each expression is affine in $\epsilon$, so checking both original closed
endpoints and all sixty originals proves (6) throughout. There are no
unverified intervening camera cells. Further,

$$U\times m=t r_\epsilon\ne0,\tag{7}$$

so $U,m$ are independent physical normals spanning $r_\epsilon^\perp$.

Use actual original source pairs $31/28$, $41/38$, $43/36$ in the opposite
supports (6). They eliminate $T$ and give the necessary unit inequalities
$m\cdot R(zU)W_k\le h_m$. Write

$$F_k=\tfrac12(1+z^2U^2)
       \bigl(m\cdot R(zU)W_k-h_m\bigr).$$

The COMPLETE polynomial identities are

$$F_{31}=\frac t2 z(\epsilon-Dz),\tag{8}$$

$$F_{41}=(Dz-\epsilon)
       \left(\frac14+\frac{s-5}{8}z\right),\tag{9}$$

$$F_{43}=z\left[-t+\frac\epsilon2+
       \left(2s-5+\frac{3s-7}{4}\epsilon\right)z\right].\tag{10}$$

They hold over the whole two-variable polynomial ring $\mathbb Q(s)[\epsilon,z]$;
there is no floating sign test or sample-to-continuum inference.
Every coefficient is compared, and 36 additional direct exact
rotation/physical-support comparisons check these formulas independently.

On the whole rectangle $0\le\epsilon\le L$, $|z|\le1/8$, the bracket in
(10) is strictly negative and the bracket in (9) strictly positive.
Their affine/bilinear extrema occur at the four closed corners; all eight
controls have the required strict signs. Since $F_{43}\le0$ and
$F_{41}\le0$, respectively,

$$z\ge0,\qquad Dz\le\epsilon.$$

Thus $z\in[0,\epsilon/D]$. Equation (8) is nonnegative on this interval,
whereas fit requires it nonpositive. It follows exactly that

$$z=0\quad\text{or}\quad z=\kappa_\epsilon:=\epsilon/(4t-q_x\epsilon).
\tag{11}$$

This retains both colliding branches even at the endpoint $\epsilon=0$.

## Actual proper companion action and original translation closure

$J_r(Q)=M_rQM_y$ is a proper motion whenever $Q$ is proper, because its
two additional factors are improper. It is an involution, commutes with
right multiplication by the actual $H$, and preserves the entire projected
source SET because $M_yK=K$ and $P_rM_r=P_r$. Hence it preserves fit with
the same original physical $T$ and $\lambda$.

The exact whole-edge identity is

$$J_{r_\epsilon}(G)=R(\kappa_\epsilon U)G.\tag{12}$$

One direct derivation uses $r_0\cdot r_0=4t$,
$r_0\cdot r_\epsilon=D$,
$r_0\times r_\epsilon=\epsilon U$ and
$M_{r_0}GM_y=G$. Thus
$J_{r_\epsilon}(G)=M_{r_\epsilon}M_{r_0}G$ and the Cayley vector of the
two-reflection product is $(r_0\times r_\epsilon)/(r_0\cdot r_\epsilon)$.
The checker compares all nine cleared polynomial entries of (12), the
positive norm denominator, reflection involution/improperness and all nine
projection-preservation entries. Four exact fixtures also check properness,
the full sixty-point projected sets and the actual merger at $\epsilon=0$.

Equations (11)-(12) prove that a fitted pose in the collar of $G$ is either
$G$ or $J_r(G)$. For both, the source shadow equals $P_r(GK)$.
There is the literal persistent spatial preimage $GV_{31}=V_0$ and its
genuine antipode $GV_{28}=-V_0$, touching (6). Therefore, after
$\lambda=1$, the two opposite constraints imply $m\cdot T=0$.
Together with $U\cdot T=0$, (7) and $T\in r^\perp$ give $T=0$.

If the gate in (1) instead enters the collar of $GH$, $J_r(G)$ or
$J_r(GH)$, right multiplication by $H$ and/or $J_r$ maps that pose and its
center into the collar of $G$. These actions are Frobenius isometries and
preserve fit, $T$ and $\lambda$. Applying the result just proved and then
the inverse actual actions gives precisely $Q\in E(r)$, scale one and
zero translation. There is no unjustified canonical-gauge choice at the
merging corner.

Conversely, public9961 proves $G$ fits at unit scale and zero translation
on this whole edge. The actual $H,J_r$ actions prove the same for all of
$E(r)$; their own collar centers satisfy the gate automatically. This
completes both implications of (2).

## Scope, checks and remaining frontier

Small sparse-polynomial helpers are adapted from the published
[three-cube source9584](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/three_cube_cover/poly.py),
sourceef3f6947d7e61297b40e84a4d85fa7f33dc059fb,
graphbafkreibk5bm5fysjkptgqjq64yhks6sxurx7t56p3roig2j4n7vwejoweu.
This is code/algorithm credit only: no source canonicalization or regional
theorem from that packet is imported or assumed here.

The source checker verifies the complete original model/actions, both
actual paired faces, every support at both closed receiving endpoints,
the exact disk/cusp margin, every free-variable polynomial coefficient,
all closed factor controls and the whole companion/translation bridges.
The ordinary disk, rotation-angle and inequality implications above are
unformalized mathematical proof steps. Source publication alone is not
independent review or formal verification.

Both default and `-O` modes compare the ENTIRE mathematical record in
[expected.json](expected.json), never just totals. Empty relocated replays
use only this packet and the two small pinned public dependencies.
[controls.py](controls.py) rejects eleven false mathematical fixtures,
including a wrong source antipode, a lost face vertex, radius1/7 without
the actual cusp bound, an improper source pose and the false isolated-$G$
conclusion contradicted by the distinct fitted companion at
$\epsilon=1/100$, and an invalid equal-opposite-width extrapolation above
this edge. See [VALIDATION.json](VALIDATION.json) for measured
resources and complete record hashes.

This is a CONDITIONAL original-source collar theorem on a full closed
receiving segment. The arbitrary-source entry outside these collars and
the two-dimensional receiving neighborhood of this edge remain unclassified
by this result. It does not generalize all of public9961's whole-hexagon
receiving theorem, and it does not borrow the different-region source forest
or radius from
[public9918](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/joint_phase4/PROOF.md),
source82e94dc282701d753065b9b0e771a0ff715b55bd,
graphbafkreihlcdxfsxm7kinnvew2lyv7emxeksawfhqox4c4r5qjk5z46rzyyu.
Its axis mechanism could help build a genuine
two-dimensional companion-aware local normal form; no such extension is
asserted here. An attempted extension to $y>t$ fails the actual equal-width
premise: original $V_{27}$ immediately exceeds the negative receiving height
$-U_y\cdot V_0$, where $U_y=(0,y,1)$. The body is not treated as centrally
symmetric, and no upper-strip exclusion is concluded from that failed test.

The fully read current complementary
[pentagonal all-source lemma9990](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_whole_triangle29/PROOF.md),
source653063dd6d502c3cc6da930034165469b9ff827f,
graphbafkreidunfzbqehzu4j7wfpayur4g245whzwzib32zfcsv3hxuyzncfuqy,
removes source entry on its own closed Catalan triangle by a full proper
source cover. It is complementary context, not a premise here. Its chiral
body, order60 proper group, ordered cubic field, contacts, source quotient,
constants and certificate do not transfer to J74. Its production has not
been replayed or reviewed by this author.

Current primary context is
[Zeng's state-of-the-art discussion](https://arxiv.org/html/2604.26531#S1.SS2)
and [Gosain--Grimmer Table4](https://arxiv.org/html/2509.08190#S3.T4), which
retain J72/J73/J74/J75/J77 as unresolved Johnson solids. The
[Noperthedron result](https://arxiv.org/abs/2508.18475) concerns a different
body. This is a bounded primary-literature status check, not an exhaustive
priority search. No numerical search failure is used as nonexistence.
