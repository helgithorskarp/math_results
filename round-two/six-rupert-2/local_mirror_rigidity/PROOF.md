# Local closed-fit rigidity at all six J74 minimum axes

**six-rupert-2, researcher; 2026-10-01.** Author-checked, unformalized
intermediate proof with exact finite hypotheses. No independent review of
this extension or historical priority is asserted. J74 remains globally
unresolved.

Let `K=conv(V)` be the unit-edge metabigyrate rhombicosidodecahedron in
[model.py](../model.py), with sixty originals of common squared radius
`R^2=(11+4sqrt(5))/4`. For unit `n`, put `P_n=I-nn^t`, `M_n=I-2nn^t`.
The six unit minimum normals `m_0,...,m_5` are `e_x,e_y` and
`(1,epsilon phi,delta phi^2)/(2phi)`, with mixed signs ordered
`(--),(-+),(+-),(++)` and `phi=(1+sqrt(5))/2`.
Let `B_j` be the original finite catalogue of proper base motions with
receiver `m_j`; its sizes are `2,4,4,4,4,4`.

**Theorem.** There exists a positive, **unquantified** `epsilon` such
that, for every unit receiver with
`min(||n-m_j||,||n+m_j||)<epsilon`, every original closed fit

\[
 \lambda P_n(QK)+t\subseteq P_nK,
 \qquad Q\in SO(3),\quad\lambda\ge1,\quad t\in n^\perp
\tag{1}
\]

holds if and only if

\[
 \lambda=1,\quad t=0,\qquad
 Q=Q_0\ \text{or}\ Q=M_nM_{m_j}Q_0
 \quad\text{for some }Q_0\in B_j.
\tag{2}
\]

These have exactly the receiver shadow. Thus strict projected passage is
excluded in an open receiving neighborhood of each minimum axis, with
**all sources, planar rolls and translations included**. No distinct
count of moving branches is claimed; they can coincide at the axis.
Unlike a differentiable-path restriction, the theorem decides arbitrary
higher-order and singular deviations locally.

No numerical exclusion radius is proved. The earlier **1/15** is a shadow
reduction domain; **1/100** below is a support-triangle length in
unnormalized tangent coordinates. Neither is this theorem's `epsilon`.

## 1. Literal closed contact cones and actual prototypes

The [boundary-prototype lemma](../boundary_prototypes/PROOF.md), graph
8775, supplies `C_j=conv(W_j)` with 28 actual boundary originals and

\[
 P_nK=P_nC_j\quad\text{if}\quad
 \operatorname{dist}(n,\{m_j,-m_j\})\le1/15.
\tag{3}
\]

It proves `M_(m_j)C_j=C_j`, and every base motion from `i` to `j` has
`Q_0C_i=C_j`, `Q_0m_i=+/-m_j`. Proper marked transports reduce the four
mixed prototypes to `C_2`, leaving representatives `C_0,C_1,C_2`.
The mixed reflections fail to preserve the full body: (3), rather than
full-body symmetry, permits their use here.

Fix a representative and set `m=m_j`, `E=m^perp`,

\[
 u=m+r,\quad r\in E,\qquad n=u/\|u\|.
\tag{4}
\]

[certificate.json](certificate.json) supplies cyclic physical tangent
wall rays, `l1`-normalized, with **18,12,16** closed cones for the three
representatives. The [checker](check.py) proves distinctness, one polar
ordering around the circle, adjacent widths strictly less than `pi`, and
one record for each closed adjacent interval including the wrap. Thus
these cones cover every tangent direction and all walls. Completeness of
a discovery enumeration or hull finder is not a premise.

For each cone with rays `d_0,d_1`, sixteen actual unit edges have ordered
endpoints `v_a,v_b` in `W`. Define

\[
 \Delta_i=v_b-v_a,\quad h_i=(\Delta_i\times m)\cdot v_a>0,
 \qquad m_i(u)=\frac{\Delta_i\times u}{h_i}.
\tag{5}
\]

Both endpoints supply source contact rows. At the three finite normals
`m,m+d_0/100,m+d_1/100`, every supplied edge is physically perpendicular
to `u`, has positive support value, and satisfies

\[
 m_i(u)\cdot(v_i-v)\ge0\qquad\text{for all }v\in V.
\tag{6}
\]

These comparisons are affine in `r`; they hold throughout the closed
triangle `r=gamma_0 d_0+gamma_1 d_1`, `gamma_k>=0`,
`gamma_0+gamma_1<=1/100`. Independent generators bound their coefficient
sum by a finite multiple of `||r||`. With finitely many cones, every
sufficiently small `r` lies in its cone's verified triangle. This gives
a uniform neighborhood including walls, without assigning a chord radius.

The finite check contains **132,480** supports against the original sixty
vertices: three corners times sixteen edges times sixty originals over
46 cones. Each cone has 32 persistent actual endpoint-contact rows.

## 2. Common balances and complete critical tilt cones

The four and only four actual equatorial originals `q_l` have positive
weights, credited to the [weighted-contact source](../tangent_contacts/PROOF.md),
with

\[
 \sum\beta_l=1,\quad\sum\beta_lq_l=0,\qquad
 M=\sum\beta_lq_lq_l^t,\quad\operatorname{tr}M=R^2.
\tag{7}
\]

Their span is `E`. At each singleton the two selected independent support
normals have the exact strictly positive decomposition

\[
 \theta_l m_{\rm left}(m)+(1-\theta_l)m_{\rm right}(m)=q_l/R^2,
 \qquad0<\theta_l<1.
\tag{8}
\]

Give the eight common rows weights `omega=beta_l theta_l` and
`beta_l(1-theta_l)`. With `g_i(m)=v_i cross m_i(m)`, exact physical checks give

\[
 \omega_i>0,\quad\sum\omega_i=1,\qquad
 \sum\omega_i m_i(m)=\sum\omega_i g_i(m)=0,
\]
\[
 S:=\sum\omega_i v_i m_i(m)^t=M/R^2,\qquad A=I_E-S.
\tag{9}
\]

Here common `v_i=q_l` lies in `E`. Both `S,A` are symmetric positive
definite on `E`, of trace one, with `0<A<I_E`: `S` has two positive
eigenvalues with sum one. The checker also verifies `A`'s positive physical
planar determinant. These stresses are checked data, not newly discovered
coefficients.

The common linear forms on `(rho,C) in R times E`,

\[
 L_i=g_i(m)\cdot(\rho m)+m_i(m)\cdot C,
\tag{10}
\]

have rank three; a nonzero three-row determinant is recorded per cone.
Equivalently their two normals at a singleton force
`rho(m cross q_l)+C=0`, and two distinct singletons force `rho=C=0`.
Positive balance and rank imply a positive constant `c` such that

\[
 \max_i L_i\ge c(|\rho|+\|C\|).
\tag{11}
\]

If all forms were nonpositive at a nonzero vector, their strictly positive
weighted zero sum would force each to vanish, contradicting rank.
Minimize the positive maximum on a compact unit sphere. Finitely many
cones supply a common `c>0`.

For all 32 rows let `c_i` be the tangent part of `g_i(m)`. Two supplied
independent critical rays `a_0,a_1`, also `l1`-normalized, satisfy every
`c_i dot a_k<=0`. Actual facet rows satisfy

\[
 c_{f_0}\cdot a_0<0,\quad c_{f_0}\cdot a_1=0,
 \qquad c_{f_1}\cdot a_0=0,\quad c_{f_1}\cdot a_1<0.
\tag{12}
\]

Therefore the exact common-zero tilt cone is
`{xi_0 a_0+xi_1 a_1:xi_k>=0}`: its two facet rows force nonnegative
coordinates and every other row permits them. This proves completeness
and pointedness. All four corners per cone satisfy

\[
 a_j^tAa_k>1/20\qquad(j,k=0,1).
\tag{13}
\]

All **184** comparisons are exact. For `p^+=sum xi_j^+ a_j` and
`P=sum xi_j^+`, (13) and `A<=I_E` imply `P<=5||p^+||`.

## 3. Actual translation, proper companion and bilinear identity

Analyze a unit prototype fit with proper `Q` near identity. Its Cayley
vector and the actual translation lift are

\[
 w=\rho m+p,\quad p\in E,\quad\eta=\|w\|,
 \quad Qv-v=\frac{2}{1+\eta^2}
 \{w\times v+w\times(w\times v)\},
\]
\[
 T=t-(t\cdot m)u\in E,\quad P_uT=t,\qquad C=(1+\eta^2)T/2.
\tag{14}
\]

Every original support (6) gives the exact necessary inequality

\[
 F_i=m_i(u)\cdot\{w\times v_i+w\times(w\times v_i)+C\}\le0.
\tag{15}
\]

No initial translation bound or centering is assumed. The proper motion
`Qtilde=M_n Q M_m` has the same source shadow and the same actual
translation by the prototype reflection and (3). Put `Jv=m cross v`,
`w_0=Jr`, `D=1+w_0 dot p`. Its Cayley vector is exactly

\[
 \widetilde\rho=(\rho+r\cdot p)/D,\qquad
 \widetilde p=(w_0-p+\rho r)/D.
\tag{16}
\]

Indeed `M_nM_m` has Cayley vector `w_0`; conjugation by `M_m` sends `w`
to `rho m-p`, and the proper Cayley product formula gives (16).
Denominators are positive near zero; both Cayley norms tend to zero as
`(r,w)->0`. The actual reflection map is involutive. In particular,

\[
 \rho=D(\widetilde\rho+r\cdot\widetilde p)/(1+\|r\|^2),
 \qquad w_0=p+D\widetilde p-\rho r.
\tag{17}
\]

The same inequalities hold for the companion with
`Ctilde=(1+etatilde^2)T/2`. This admits arbitrary input roll; the proper
companion changes the spatial motion.

For tangent vectors set `[a,b]=m dot (a cross b)`. For common rows define
`k_i=(Delta_i dot m)/h_i`, `B=sum omega_i k_i v_i`,
`K_c=sum omega_i k_i`, all reconstructed by the checker. Then

\[
 m_i(u)=m_i(m)-m(m_i(m)\cdot r)+k_iJr.
\tag{18}
\]

The common sum `F=sum omega_i F_i` obeys the exact identity

\[
 \begin{aligned}
 F={}&D\{p^tA\widetilde p-[p,\widetilde p][p,B]\}\\
 &+\rho\{B\cdot r-p\cdot r+[p,r][p,B]\}
 -\rho^2(1+w_0\cdot B)+K_cw_0\cdot C.
 \end{aligned}
\tag{19}
\]

The translated bilinear mechanism is credited to the
[J77 mirror proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_bilinear_mirror_cap/PROOF.md),
graph 7988; its different-body caps and constants are not transferred.
For completeness, expand (15) using (18),(9). Symmetric planar `S` of
trace one satisfies `JS=AJ`. Before substituting (16) the sum is

\[
 p^tA(w_0-p)+\rho B\cdot r-\rho p^tSr-\rho^2(1+w_0\cdot B)
 +(p\cdot B)(w_0\cdot p)-\|p\|^2(w_0\cdot B)+K_cw_0\cdot C.
\]

Use `(p dot B)(w_0 dot p)-||p||^2(w_0 dot B)=-[p,w_0][p,B]`,
`A+S=I_E` and (17). This proves (19) for arbitrary variables, rather
than from finite sample motions.

## 4. Uniform perturbation bounds and the local contradiction

Let `etatilde=||wtilde||`, `kappa=max(||r||,eta,etatilde)`.
The constants `H` below are finite positive constants from fixed verified
coefficients, enlarged uniformly over all 46 cones when necessary.
They depend on neither motion nor translation. All conclusions hold for
sufficiently small `kappa`, without assigning a numerical threshold.

For every row put `L_i=g_i(m) dot w+m_i(m) dot C`. Directly from the
fixed linear `m_i(u)` and (15),

\[
 |F_i-L_i|\le H\kappa\eta+H\kappa\|C\|.
\tag{20}
\]

The three errors are torque drift `O(||r|| eta)`, the quadratic Cayley
term `O(eta^2)`, and translation drift `O(||r|| ||C||)`. On common rows,
(11),(15),(20) give
`|rho|+||C||<=H kappa eta+H kappa||C||`.
Absorb its last term. Apply the same proof to the companion and use
the inverse in (17) and the bounded ratio
`||C||/||Ctilde||=(1+eta^2)/(1+etatilde^2)` when `T!=0`. Then

\[
 |\rho|+\|C\|\le H\kappa\min(\eta,\widetilde\eta).
\tag{21}
\]

For `T=0` translation is immediate. The additional inverse term
`|r dot ptilde|<=kappa etatilde` obeys the same estimate. Also (17) gives

\[
 \|r\|(1-|\rho|)\le\eta+(1+\kappa^2)\widetilde\eta,
 \qquad\|r\|\le4\max(\eta,\widetilde\eta).
\tag{22}
\]

Write `p=xi_0 a_0+xi_1 a_1`. The actual facet rows (12), the perturbation
bound (20), and the absorbed own bound `|rho|+||C||<=H kappa eta` imply

\[
 \xi_j^-:=\max(0,-\xi_j)\le H\kappa\eta.
\tag{23}
\]

Each facet's tangent part is a fixed strictly negative multiple of
`xi_j`, with the other coordinate zero. Normal/translation terms have
the established bounds. This proves (23); the companion obeys it with
`etatilde`, in the same receiving cone.

Keeping these negative coordinates, put `p^+=sum xi_j^+ a_j`,
`p^-=sum xi_j^- a_j`, `P=sum xi_j^+`. Since `||a_j||<=1`,

\[
 (1-H\kappa)\eta\le P\le5\|p^+\|\le5(1+H\kappa)\eta.
\tag{24}
\]

Use `||p||>=eta-|rho|`, `||p^-||<=H kappa eta` and (13).
The corresponding inequalities hold for the companion. Therefore

\[
 p^tA\widetilde p\ge(1/20-H\kappa)\eta\widetilde\eta.
\tag{25}
\]

The positive-positive term is at least `P Ptilde/20`; the two mixed
terms cost `H kappa eta etatilde`, by (23),(24), `||A||<=1`.
The negative-negative term is nonnegative because its two factors
are nonnegative combinations of the same rays and every corner in
(13) is positive. It is dropped only after establishing this sign.

Suppose both Cayley norms are positive. In (19) every other term is
bounded in absolute value by `H kappa eta etatilde`. The determinant
term uses `eta^2 etatilde<=kappa eta etatilde`; `rho B dot r` and
the translation term use (21),(22); `rho p dot r` uses
`eta min(eta,etatilde)<=eta etatilde`; and `rho^2` uses
`min(eta,etatilde)^2<=eta etatilde`. The remaining cubic term is
smaller. Since `D=1+O(kappa^2)`, (25) gives

\[
 F\ge(1/20-H\kappa)\eta\widetilde\eta>0
\tag{26}
\]

for sufficiently small `kappa`, contradicting (15) and the positive
common weights. Thus `Q=I` or `Q=M_nM_m`. These give exactly the target
shadow. Support in every planar direction excludes a nonzero translate
of a compact convex set into itself, forcing `t=0`; equal positive
areas then force `lambda=1`.

## 5. Original sources, all-source localization and completion

For any original scaled fit, `0 in int(K)` and convexity imply
`QK subset lambda QK` for `lambda>=1`. Hence it implies unit containment
with the same motion and actual translation. Near a catalogue motion
`Q_0:i->j`, set `Qrel=Q Q_0^t`. When `n` is near `m_j` and `Qrel` near
identity, both shadows reduce by (3) to those of `C_j`: the normalized
source normal is near `m_j`, and the original source normal is near
the corresponding `m_i`. The actual spatial boundary map retains all
contact preimages. Apply the preceding unit argument. Returning to the
original scaled containment forces (2). Proper marked congruence transfers
the mixed representative result to every mixed receiver. No translation,
source roll or path regularity is omitted in this local argument.

Suppose no all-source receiving neighborhood existed for `m_j`. Take
closed fits with receivers tending to `m_j` but source motions escaping
the union of the established local motion neighborhoods. Compactness
of `SO(3)` gives a convergent source subsequence. Projection area bounds
give a uniform scale bound (`lambda<2` suffices from the original
maximum/minimum ratio). Since the source contains zero, each actual
translation belongs to the receiving shadow, hence `||t||<=R`.
Extract these variables too. Continuity of the finitely generated
projected convex hulls makes the limit a closed fit at `m_j`.

The [complete original minimum catalogue](../PROOF.md), graph 8551,
forces `lambda=1,t=0` and some `Q_0 in B_j`. The subsequence therefore
eventually enters its local motion neighborhood, contradicting its
choice. Thus a positive all-source receiving radius exists. Take the
minimum over the six finite axes, decreasing it below `1/15` and their
half-separation if needed. Negative signed normals obey `P_n=P_-n`,
`M_n=M_-n`. Conversely (2) gives equal shadows throughout the earlier
reduction domain by 8775. This proves the theorem.

## Scope, dependencies and remaining frontier

The new result proves completeness of the two local reference families.
[Lemma 8724](../tangent_contacts/PROOF.md) excluded scale gain through
quadratic order on C1 paths but left higher-order and singular approaches
undecided. The present finite-neighborhood argument needs no path
regularity. The [independent contact audit 8777](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/contact-path-audit/REVIEW.md)
verifies 8724 and sharpens its translation/regularity bounds; its verdict
does **not** audit this extension. Its numerical constants are not inputs.

The named geometry and catalogue are dependencies from 8551; actual
prototype equality and proper marked transports are dependencies from
8775. The generic translated bilinear mechanism and Cayley identities
are credited to 7988. The new finite work is the original-J74 closed
contact cones, positive common balances, complete critical cones and
acute bilinear corners. No different body's symmetry or numerical
exclusion radius is transferred.

[DEPENDENCIES.json](DEPENDENCIES.json) pins eight small parent inputs
to verified source commit `4288f5c57e8af1c73b30e2fdb3ab2fcca190723f`.
The checker reads literal closed cones and verifies all original supports,
importing only the pinned model and ordered Q(sqrt(5)) arithmetic. It has
no hull finder, solver, external dataset or private discovery input.
Four malformed controls reject a missing cone, negative weight, reversed
critical generator and false edge. Guards remain active under Python `-O`.
The exact program proves the finite hypotheses; the algebra, uniform
perturbation estimates and compactness proof above remain unformalized.

The primary [Gosain–Grimmer Table 4](https://arxiv.org/html/2509.08190)
and [Zeng discussion](https://arxiv.org/html/2604.26531) retain the five
unresolved Johnson solids. The [Noperthedron](https://arxiv.org/abs/2508.18475)
is a different body. Bounded checks give no historical priority guarantee,
and this local theorem does not settle J74 globally.
The next construction frontier is outside these minimum-axis receiving
neighborhoods. A quantitative source-localization bound could make the
existential collar effective. A strict passage elsewhere still requires
a compact exact certificate against all original polygon supports.
