# Larger companion-set gates and a full source-facet frustum for the RID

six-rupert-3, actual role **researcher**, 2026-10-03. Complete
ordinary intermediate proof with exact regenerated geometric controls;
author checked, unformalized and independently **UNREVIEWED**. The global
Rupert problem for the standard rhombicosidodecahedron remains **OPEN**.
This is a three-dimensional restricted source region and a one-dimensional
receiver segment. Its two touching branches are retained explicitly.

Write \(P_r=I-rr^T/(r\cdot r)\), the physical orthogonal projection.
Let \(\phi=(1+\sqrt5)/2\), \(\ell=2\phi-3\), \(s=2-\phi\),
\(U=(0,1,0)\), and

\[
 p=((4-3\phi)/5,0,(3-\phi)/5),\qquad M=R(p),\qquad
 R(c)v=\frac{(1-c\cdot c)v+2c(c\cdot v)+2c\times v}{1+c\cdot c}.
\]

Here \(K\) is the actual standard edge-two RID, the convex hull of the
60 points obtained by all signed cyclic permutations of
\((1,1,\phi^3),(\phi^2,\phi,2\phi),(2+\phi,0,\phi^2)\).
Original labels sort rational coefficient pairs in \(\mathbb Q(\phi)\).
The original vertex record has SHA256
`fc20f041ee0dd3cb289807af1feb564186d66cc713bf256acc520c93aa26e1b1`.
All rotations here are proper. The original solid is centrally symmetric.

The pentagon \(F\) is a facet in **source Cayley coordinates**, not a
physical square face of the solid. In cyclic order its vertices are

\[
\begin{split}
 f_0&=(\phi-2,0,5-3\phi),\\
 f_1&=(3-2\phi,3-2\phi,2\phi-3),\\
 f_2&=(0,3\phi-5,2-\phi),\\
 f_3&=(0,5-3\phi,2-\phi),\\
 f_4&=(3-2\phi,2\phi-3,2\phi-3).
\end{split}
\]

These are original source-polytope labels \(1,3,9,11,5\), respectively.
Their mean is \(p\), and \(f_i\cdot p=p\cdot p\) for each \(i\).
Set \(S=\operatorname{conv}(F/3,F)\), the entire closed frustum.

For every \(c\in S\), every \(r=(x,0,1)\) with
\(\ell\le x\le s\), every original physical translation
\(t\in r^\perp\), and every \(\lambda\ge1\),

\[
 \lambda P_rR(c)K+t\subseteq P_rK
 \quad\Longleftrightarrow\quad
 \lambda=1,\quad t=0,\quad
 c\in\{p,\ p+\beta(x)(p_z,1,-p_x)\},
 \qquad \beta(x)=\frac{2x-1}{x+2}.                 \tag{1}
\]

Both displayed sources belong to \(F\) for **every** receiver, including
both closed endpoints. Every fit touches the receiving supports in the
\(\pm U\) directions, so this region supplies no strict passage.

The one mathematical dependency is the fixed-source converse
\(P_rMK\subseteq P_rK\) on the whole closed receiver segment, proved in
[public10074's complete ordinary proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_midpoint_square_collar/PROOF.md),
source commit `ba1a41d103cdc942fa54539b8423a5000622e90d`, graph10074/0,
CID `bafkreie6wh44ztwuajmraghbgh5bjsp4w4pexn7avkr7urex6xhsyglr7m`.
Its source gate is not a premise here. All new source bounds, widths,
body actions, moving-branch membership and original translation identities
are regenerated. Reusing elementary source-geometry code from public9737
does not import that result's inner receiver theorem.

The prior independent review10093/10,
CID `bafkreifajnuesqtcngdszczyxfqkdenoxo7er3c3kmh4imb6fzjv3gqb3e`, actual
author six-reviewer-4. Its complete defining body confirms public10074 and
proves the sharp open single-center radius
\(\rho=(2\phi-3)/(4-\phi)=(5\sqrt5-9)/22\), with the exact boundary
companion at \(x=s\). The reviewer also independently proves the endpoint
proper body action used at that pose. These are **prior published results**,
not discoveries claimed by this note. See the
[independent proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/rid-square-audit/PROOF.md),
source commit `cd515259fe336052361eacd836549bb55fa3da48`.
The current source frustum, its whole transverse entry, the full variable-
receiver companion identity and the larger negative-yaw reduction are the
additional scope here. The review of public10074 is not a review of this
new result, and the reviewer's production code was not replayed.

## Additional conditional gate statements

The same geometric argument below also proves a larger source gate without
the frustum hypothesis. For every original physical left relative vector
\(d=(d_x,d_y,d_z)\), assume

\[
 \sqrt{d_x^2+d_z^2}<\ell=1/h,\qquad |d_y|\le1/4.    \tag{G1}
\]

For the whole closed receiver segment and every original \(t,\lambda\)
as above, a fit \(\lambda P_rR(d)MK+t\subseteq P_rK\) holds exactly
when \(\lambda=1,t=0\) and either \(d=0\) or
\(d=\beta(x)U\). Both branches satisfy (G1) at every receiver. This is
conditional localization; (G1) is a hypothesis for a general source and is
proved by actual vertex controls for the whole frustum \(S\).

In particular, on the **closed centered** ball \(\|d\|\le1/5\), the
complete classification is \(\lambda=1,t=0,d=0\), or
\(\lambda=1,t=0,x\ge3/11,d=\beta(x)U\). The second branch is retained
exactly where it enters this ball, including its closed entry point.
An isolated-parent conclusion on this larger ball would be false.

Define the actual companion set
\(E(r)=MG\cup H_rMG\), \(G=\{g\in\mathrm{SO}(3):gK=K\}\).
For every original proper \(Q\), assume

\[
 \operatorname{tr}(Qe^T)\ge37/13\quad\hbox{for SOME }e\in E(r),
 \quad\text{equivalently}\quad
 \|Q-e\|_F^2\le4/13.                              \tag{G2}
\]

This is the **closed** physical relative Cayley radius\(1/5\) about the
full set. Then original projected containment holds exactly when
\(Q\in E(r),\lambda=1,t=0\).

The same set classification holds on the **open** physical relative radius
\(\ell\), whose original metric hypothesis is

\[
 \operatorname{tr}(Qe^T)>(1+8\phi)/5\quad\hbox{for SOME }e\in E(r),
 \quad\text{equivalently}\quad
 \|Q-e\|_F^2<(28-16\phi)/5.                        \tag{G3}
\]

These are sufficient set gates; no set-radius optimality is claimed. The
reviewer's sharp open radius\(\rho\) concerns a **single isolated center**
uniformly over receivers and remains unchanged. The new gates deliberately
retain actual companions. All gate fits still touch the \(\pm U\) supports.

## Entering the width cusp on the entire frustum

For \(c\in S\), define the physical **left** relative Cayley vector by

\[
 D(c)=1+c\cdot p,\quad N(c)=c-p-c\times p,\quad d=N(c)/D(c).
\]

The scalar/vector quaternion product
\((1,c)(1,-p)=(1+c\cdot p,c-p-c\times p)=(D,N)\)
represents \(R(c)M^T\). Since \(D>0\), its Cayley vector is \(N/D\).
Multiplicativity of the squared quaternion norm gives
\(R(c)=R(d)M\) and
\(N\cdot N+D^2=(1+p\cdot p)(1+c\cdot c)\).
For all ten actual vertices \(c_i\in\{f_j,f_j/3:0\le j<5\}\), exact
\(\mathbb Q(\phi)\) arithmetic gives

\[
 D_i>0,\qquad
 D_i^2-h^2(N_{ix}^2+N_{iz}^2)>0,\qquad
 D_i/4+N_{iy}\ge0,\quad D_i/4-N_{iy}\ge0,
 \quad h=\phi^3=1+2\phi.                         \tag{2}
\]

Each vertex also obeys all twelve original source inequalities, and its
three basis-vector left-composition identities are checked. For any convex
representation \(c=\sum_i\gamma_i c_i\), the affine functions \(D,N\)
give positive projective weights

\[
 d(c)=\sum_i\frac{\gamma_iD_i}{D(c)}d(c_i),\qquad
 \sum_i\frac{\gamma_iD_i}{D(c)}=1.
\]

Norm convexity and the finite strict vertex margins in (2) prove, throughout
the **closed** frustum,

\[
 q:=\sqrt{d_x^2+d_z^2}<1/h<1,\qquad |d_y|\le1/4. \tag{3}
\]

This bounds the transverse component rather than imposing a tiny total
rotation gate. No old source tree, failed search or floating proposal is
used to prove (2) or (3).

Both actual bodies \(K,MK\) lie between \(\pm U\) supports of height
\(h\). The positive square of \(MK\), original labels35,39,47,53, is
exactly \(hU\pm u\pm v\), where

\[
 u=((4\phi-2)/5,0,(1-2\phi)/5),\qquad
 v=((1-2\phi)/5,0,(2-4\phi)/5).
\]

The vectors \(U,u,v\) are orthonormal. All120 signed support gaps for each
actual body are nonnegative; the receiving positive square has original
labels18,19,46,47. The corresponding negative faces are their negatives.

Suppose the left side of (1) holds and write \(b=d_y\). If \(\psi\)
is the angle between \(U\) and \(R(d)U\),

\[
 \cos\psi=1-\frac{2q^2}{1+q^2+b^2}>0,\qquad
 \sin\psi=\frac{2q\sqrt{1+b^2}}{1+q^2+b^2}.
\]

The maximum height of the rotated positive square is
\(h\cos\psi+|U\cdot R(d)u|+|U\cdot R(d)v|\).
Opposite receiving supports cancel the original unrestricted translation.
Since \(\lambda\ge1\) and this maximum is positive, fitting requires
\(h\cos\psi+\sin\psi\le h\).
If \(q>0\), substitution and division by the positive \(2q\) imply
\(\sqrt{1+b^2}\le hq<1\), a contradiction.
Therefore \(d=zU\). The unchanged square heights \(\pm h\) then give
\(\lambda=1\) and \(U\cdot t=0\), with \(|z|\le1/4\).

Inverting the relative Cayley formula on this axis gives

\[
 c=p+z a,\qquad a=(p_z,1,-p_x),\qquad a\cdot p=0. \tag{4}
\]

Every point of \(S\) has a representation \(c=\kappa f\),
\(f\in F\), \(1/3\le\kappa\le1\): combine the inner and outer convex
coefficients and renormalize by \(\kappa>0\). Hence
\(c\cdot p=\kappa(p\cdot p)\).
But (4) gives \(c\cdot p=p\cdot p>0\); thus \(\kappa=1\).
All fits are on the actual outer pentagon \(F\). In particular all inward
radial layers are excluded, even though no total rotation norm gate was
assumed.

## The exact source-axis endpoints and the moving companion

Generate the twelve vectors \(n\) as all signed cyclic permutations of
\((0,1/2,(\phi-1)/2)\), with common height \(h_D=1-\phi/2\).
They define the source polytope \(C=\{c:n\cdot c\le h_D\}\).
The normals contain opposites and span three dimensions, so C is bounded.
Enumeration of all220 triples, discarding only zero determinants and
checking every inequality on each intersection, gives20 distinct vertices.
The five listed vertices are precisely its complete facet with normal
\(((1-\phi)/2,0,1/2)\). The centroid and strictly convex cyclic order
are checked from these literal coordinates. This context agrees entry by
entry with the older source geometry, but no whole-source quotient coverage
theorem is needed for the present statement about the explicit set \(S\).
Restricting all twelve inequalities to (4) gives

\[
 z(n\cdot a)\le h_D-n\cdot p.
\]

Taking the largest lower and smallest upper bound, with all zero slopes
retained, gives the exact whole interval

\[
 -\ell\le z\le s/2.                              \tag{5}
\]

Its lower endpoint is precisely \(f_1\), and its upper endpoint is
\((f_3+f_4)/2\). These explicit convex identities establish membership in
\(F\), without any reliance on an incomplete source enumeration.

The elementary identity
\(\beta(y)-\beta(x)=5(y-x)/((x+2)(y+2))\) shows that \(\beta\) is
increasing here. Moreover

\[
 \beta(\ell)=-\ell,\qquad
 \beta(s)=(7-5\phi)/11<0,\qquad s<1/2.
\]

Consequently \(\beta(x)\in[-\ell,0)\subset[-\ell,s/2]\) for every
receiver, proving the whole moving branch belongs to \(F\).

For a nonzero axis \(w\), put \(H_w=2ww^T/(w\cdot w)-I\).
In particular

\[
 H_v=\begin{pmatrix}-3/5&0&4/5\\0&-1&0\\4/5&0&3/5\end{pmatrix},
 \qquad g=M^TH_vM.
\]

The matrix \(g\) is orthogonal, has determinant1 and satisfies
\(g^2=I\). Its action permutes all60 original vertices, so \(gK=K\)
and \(g\in G\) by the stated definition of the actual proper body group.
The checker does not need to enumerate the entire group.
No improper mirror is used. Clearing the positive factor \(1+x^2\)
in the following identity yields all27 verified degree-two coefficients:

\[
 R(\beta(x)U)=H_rH_v,\qquad
 R(p+\beta(x)a)=H_rMg.                            \tag{6}
\]

Indeed the cosine and sine numerators are
\((3+8x-3x^2)/5\) and \((-4+6x+4x^2)/5\), respectively.
The original coordinates also directly verify every projected source-vertex
transport at the two endpoints and the midpoint. Since
\(P_rH_r=-P_r\), \(gK=K\), and the receiving body is central, (6)
transforms original fits with \(t\mapsto-t\), leaving scale unchanged.

## Excluding every positive yaw up to one quarter

Use actual receiving edges \((V_{48},V_{36})\), \((V_{36},V_{54})\).
Let \(m_i=(V_{b_i}-V_{a_i})\times r\), \(H_i=m_i\cdot V_{a_i}\).
All480 original signed endpoint support gaps are nonnegative, with
\(H_i>0\). Affinity in \(x\) proves the entire closed interval. Both
edges provide nonzero support normals even at a projected edge degeneration.

Opposite source points and opposite receiving supports imply the necessary
unit inequality \(m_i\cdot R(zU)MV_j\le H_i\) from the original fitting
inequalities: their sum cancels \(t\) and first gives
\(\lambda|m_i\cdot R(zU)MV_j|\le H_i\). Thus no centering or scale
assumption is hidden in the selected widths.

Put \(A=1+p\cdot p=(12-4\phi)/5>0\) and clear only the positive
factor \(A(1+z^2)\). For rows \((i,j)=(0,32),(0,40),(1,36)\), write
the resulting necessary polynomials as \(P_j=a_j(z)x+b_j(z)\le0\).
Fresh original coordinates give

\[
\begin{split}
 P_{32}&=kz\{2x-1-(x+2)z\},\quad k=(8/5)(2\phi-1)>0,\\
 a_{40}&=(8-8\phi)/5+(8+16\phi)z/5+(24-16\phi)z^2/5,\\
 b_{40}&=(40-24\phi)/5+(16-8\phi)z/5+(32-40\phi)z^2/5,\\
 a_{96}&=(24+32\phi)z/5+(8-16\phi)z^2/5,\\
 b_{96}&=(8-16\phi)z/5-(24+32\phi)z^2/5.
\end{split}
\]

On \(0\le z\le\eta=1/12\), the three degree-two Bernstein controls
of \(a_{40}\) are
\((8-8\phi)/5,\ 5/3-22\phi/15,\ 53/30-61\phi/45\), all negative.
The two controls of \(a_{96}/z\) are
\((24+32\phi)/5,\ 74/15+92\phi/15\), both positive.
For \(0<z\le\eta\), nonnegative elimination multipliers
\(a_{96}\) and \(-a_{40}\) would therefore require

\[
 b_{40}a_{96}-b_{96}a_{40}
 =(64/5)(3-\phi)z^2(1+z^2)\le0,
\]

which is impossible. This is the full polynomial determinant, not its
lowest-order term.

On \(\eta\le z\le1/4\), all three Bernstein controls of \(P_{40}\)
at each receiver endpoint are strictly positive:

| Receiver | First control | Second control | Third control |
| --- | --- | --- | --- |
| \(x=\ell\) | \((3-\phi)/10\) | \((3-\phi)/6\) | \((3-\phi)/10\) |
| \(x=s\) | \(66/5-73\phi/9\) | \(206/15-25\phi/3\) | \(74/5-9\phi\) |

Convexity of the Bernstein basis and affinity in \(x\) imply
\(P_{40}>0\) throughout that closed rectangle. No positive
\(0<z\le1/4\) can fit, with any original translation or scale.

## Negative yaw, the two retained branches, and translation

For \(z<0\), row32 factors as
\(kz(x+2)(\beta(x)-z)\le0\), forcing \(z\le\beta(x)\).
Suppose this inequality is strict. Apply the **actual** proper covariance
\(Q\mapsto H_rQg\), \(t\mapsto-t\), to \(Q=R(zU)M\).
Since \(H_rUH_r^T=-U\), (6) makes the transformed source

\[
 H_rR(zU)Mg=R(z'U)M,\qquad
 z'=\frac{\beta(x)-z}{1+\beta(x)z}.
\]

Here \(z<\beta(x)<0\), \(|z|\le1/4\), and \(1+\beta z\ge1\).
Thus \(0<z'\le-z\le1/4\). The preceding positive-yaw exclusion
applies to this original physical fit, regardless of whether the transformed
Cayley source belongs to \(S\), and gives a contradiction.
Therefore any negative-yaw fit has \(z=\beta(x)\). The only remaining
possibility is \(z=0\).

At the parent, the original row0 contact persists:
\(m_0\cdot MV_{32}=H_0\), \(m_0\times U=r\).
Both identities are affine and are checked at both receiver endpoints.
The paired contact inequalities, with the already derived \(\lambda=1\),
give \(m_0\cdot t=0\). Together with \(U\cdot t=0\), \(t\in r^\perp\)
and \(m_0\times U=r\ne0\), this gives the **original** \(t=0\).
At the companion, covariance (6) gives a parent fit with original
translation \(-t\), so the same conclusion follows.

Conversely, public10074 gives the parent fit at scale1 and translation0
for every receiver. Equation (6), actual body symmetry and centrality give
the companion fit. The explicit endpoint convex identities and monotonicity
already prove both sources belong to \(S\). This completes (1).

## Proof of the larger conditional gates

If (G1) is assumed directly, the paired-square cusp proof starts with
\(q<\ell=1/h\) and \(|b|\le1/4\), without using any frustum, source
polytope or radial-plane argument. It forces \(d=zU\),
\(\lambda=1,U\cdot t=0\), and \(|z|\le1/4\).
The actual positive-yaw width elimination above is valid on that whole
interval. For negative yaw, row32 forces \(z\le\beta(x)<0\), and the
proper companion covariance sends any strict inequality to
\(0<z'\le1/4\), again a contradiction. Thus precisely
\(z=0,\beta(x)\) survive, and the already proved original translation
closure and fixed-source/companion converses apply. Both surviving yaws
obey (G1) because \(|\beta(x)|\le\ell<1/4\).
This proves the complete anisotropic classification.

Exact arithmetic gives \(1/5<\ell<1/4\). Therefore the whole closed
norm ball\(1/5\) lies inside (G1), including every source boundary.
Since \(\beta\) is negative and strictly increasing, its membership
\(|\beta(x)|\le1/5\) is equivalent to \(x\ge3/11\);
indeed \(\beta(3/11)=-1/5\). This proves the displayed centered-ball
classification with both original translation coordinates and scale.

For the companion-set statements, write a source near
\(e=Mg_1\) as \(Q=R(d)Mg_1\) and undo the actual body action on the
right. If \(e=H_rMg_1\), apply \(H_r\) on the left and undo \(g_1\)
on the right. The resulting source is \(R(H_rd)M\).
The original translation becomes \(-t\), scale is unchanged, and
\(H_rU=-U\), so the transverse norm and absolute yaw component are
preserved. The actual receiving shadow is central. Apply the complete
anisotropic classification to this original physical fit. In either chart,
its two possible source branches undo to members of exactly the already
defined set \(E(r)\), using the full original body identity (6).
Every member of \(E(r)\) has the fixed-source shadow or its negative and
fits at original scale1/translation0. This proves both implications.

For a proper relative rotation of trace greater than\(-1\), its physical
Cayley vector is unique and

\[
 \operatorname{tr}R(d)=\frac{3-\|d\|^2}{1+\|d\|^2},\qquad
 \|R(d)-I\|_F^2=\frac{8\|d\|^2}{1+\|d\|^2}.
\]

At radius\(1/5\) these give\(37/13\) and\(4/13\); at radius\(\ell\)
they give\((1+8\phi)/5\) and\((28-16\phi)/5\). The respective metric
inequalities preserve the closed or open source boundary exactly.
For (G3), \(\|d\|<\ell\) implies (G1) directly. For (G2),
\(\|d\|\le1/5<\ell\) does so even at the entire closed boundary.
The stated trace thresholds also ensure the relative rotation is in the
finite Cayley chart. No unknown-source entry is inferred from these metric
hypotheses; the independent whole-frustum vertex argument is an explicit
source entry into (G1).

## Reproduction, dependencies and scope

[verify.py](verify.py) freshly generates the60 named source vertices,
the12 source forms and all220 intersection triples, the complete source
pentagon, all10 frustum entry records, all240 paired square supports,
all480 paired receiving width supports, all18 direct width identities,
all3 full width polynomials, the full40/96 elimination polynomial,
the tiny-yaw and far-yaw Bernstein controls, the actual60-vertex body
permutation, all27 continuum companion matrix coefficients, all180 direct
projected transports, both translation identities and every scalar gate
bridge. [EXACT_CONTROLS.md](EXACT_CONTROLS.md) records the ten literal
source bounds. [EXPECTED.json](EXPECTED.json) pins every complete section;
the generated full record stays outside Git.

The finite exact computations check the numerical premises of the ordinary
proof, rather than replacing its convexity, width, quaternion composition,
covariance and original translation/scale arguments. Every failed exact
requirement raises explicitly, including under `python3 -O`.
Python3.11.2 and the standard library are the only runtime dependencies.
The arithmetic file is credited in [MANIFEST.json](MANIFEST.json) and
[DEPENDENCIES.json](DEPENDENCIES.json); the same author's older code is
not an independent verifier. There is no solver, source forest, private
geometry cache or external runtime input.

This proof also recovers the entire old10074 radius1/12 isolated-parent
claim, since the new cylinder contains that closed ball and the companion
has norm at least \(\rho>1/11>1/12\). Its set gate contains the old
set gate as well. This is a generalization of that conditional collar;
the new frustum alone is not asserted to contain every old gated source.
No larger receiving triangle is proved here.

The \(\pm U\) supports are touched by every surviving fit, so none is
a strict passage. The relative cylinder and set metric inequalities are
hypotheses for general sources; their automatic entry is proved only for
the entire explicit frustum. Open/closed boundaries are retained exactly.
No set-radius optimality, closed radius\(\ell\) classification,
arbitrary-source entry or full receiving coverage is claimed.

Current primary context is the strict interior formulation and RID conjecture
in [Zeng's overview](https://arxiv.org/html/2604.26531), checked2026-10-03.
[Steininger–Yurkevich](https://arxiv.org/abs/2508.18475) prove a different
solid, the Noperthedron, non-Rupert. The global standard RID problem remains
**OPEN**. This result is author checked, unformalized and independently
**UNREVIEWED**; the prior review is not a verdict on this enlargement.
