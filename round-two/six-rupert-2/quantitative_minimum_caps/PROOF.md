# Explicit all-source caps at the six J74 minimum axes

**six-rupert-2, researcher; 2026-10-01.** Author-checked intermediate
proof with exact finite hypotheses. The continuum estimates below are
unformalized. No independent review of this extension or historical
priority is asserted. J74 remains globally unresolved.

Let `K=conv(V)` be the original unit-edge metabigyrate
rhombicosidodecahedron in [model.py](../model.py). For unit n write
`P_n=I-nn^t`, `M_n=I-2nn^t`. The originals have common
`R^2=(11+4sqrt(5))/4<5`, `R<9/4`. The minimum axes have representatives
`m_0=e_x,m_1=e_y` and `(1,epsilon phi,delta phi^2)/(2phi)`, ordered
`(--),(-+),(+-),(++)`, with `phi=(1+sqrt(5))/2`. Let `B_j` be the
complete catalogue of proper minimum-receiver motions in
[expected.json](../expected.json), with sizes `2,4,4,4,4,4`. Set

\[
 d_*={1\over5\,000\,000\,000}.
\]

**Theorem.** For any unit receiver n at projective chord distance
`d=dist(n,{m_j,-m_j})<=d_*`, an original closed fit

\[
 \lambda P_n(QK)+t\subseteq P_nK,
 \qquad Q\in SO(3),\quad\lambda\ge1,\quad t\in n^\perp
\tag{1}
\]

holds if and only if

\[
 \lambda=1,\quad t=0,\qquad
 Q=Q_0\quad\hbox{or}\quad Q=M_nM_{m_j}Q_0,
 \qquad Q_0\in B_j.
\tag{2}
\]

These give exactly the receiver shadow. All original source directions,
proper rolls, actual translations and singular deviations are included.
No distinct count of the moving branches is asserted; they may coincide.
Thus no strict Rupert passage receives in these six closed caps.

This makes the positive, unquantified collar of
[lemma8839](../local_mirror_rigidity/PROOF.md) effective. Its support
triangle `1/100` and the prototype reduction domain `1/15` retain their
original meanings. Neither is asserted to be an all-source exclusion
radius. The earlier larger `e_y` exclusion cap is compatible with this
uniform all-six result.

A separate quantitative bridge holds for every fit(1) with
`0<d<=10^-6`: some source minimum axis and `Q_0 in B_j` satisfy

\[
 \|Q^tn-(+/-m_i)\|<5d,\quad
 \|t\|\le300d^2,\quad\lambda-1\le25d^2,\quad
 \|Q-Q_0\|_{\rm op}\le40d.
\tag{3}
\]

The `10^-6` domain of(3) is a **pose-localization radius**; it alone
is not a passage exclusion.

## 1. Inputs and exact finite hypotheses

The [geometry proof](../PROOF.md), graph8551, gives `0 in int(K)`,
brightness minimum `a_0=(13+7sqrt(5))/2`, maximum
`sqrt(113+50sqrt(5))<15`, and the complete catalogue. Brightness
`A(n)=Area(P_nK)` is the support function of its projection zonotope,
so is globally 15-Lipschitz on unit normals. The
[receiving-cap proof](../RECEIVING_CAPS.md), graph8602, gives

\[
 A(k)\le a_0+\eta,\quad0<\eta\le1/80
 \ \Longrightarrow\ \operatorname{dist}(k,\{+/-m_i\})<\eta/3.
\tag{4}
\]

The [boundary-prototype proof](../boundary_prototypes/PROOF.md), graph8775,
gives `C_i=conv(W_i)` with 28 actual original vertices, and

\[
 P_kK=P_kC_i\quad\hbox{if}\quad
 \operatorname{dist}(k,\{+/-m_i\})\le1/15.
\tag{5}
\]

It proves `M_(m_i)C_i=C_i`, `Q_0C_i=C_j` for catalogue motions, and
proper marked transports to representatives0,1,2. Full-body reflection
symmetry at the mixed axes is not used.

The [checker](check.py) verifies afresh:

* The four actual equatorial originals q at each axis have positive
  literal weights from [contact8724](../tangent_contacts/PROOF.md),
  `sum beta=1`, `sum beta q=0`, and `M=sum beta q q^t>I_E/2` on
  `E=m_i^perp`. The last claim follows from positive physical planar
  trace and determinant of `M-I_E/2`.
* Every nonequatorial original of W has absolute height at least1/2;
  every equatorial pair distance is at least1. A specified pair a,b
  has Gram determinant greater than81/4 and trace `2R^2<10`.
* All `6*6*4!=864` equatorial bijections are examined. Exactly842 fail
  the Gram test, each with a discrepancy at least `3sqrt(5)/10>1/2`.
  The other22 have unique proper lifts matching exactly the22 original
  catalogue records, including source and receiver axes. There is no
  unclassified isometric correspondence.

The moment/translation method is credited to the independent
[contact audit8777](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/contact-path-audit/REVIEW.md).
That verdict audits8724, not this extension. The needed moments and
constants are freshly checked here.

The checker also replays all finite hypotheses of8839 and compares its
entire output to the pinned expected record:46 closed fans,132480
supports against all originals,184 bilinear corners greater than1/20,
positive common balances, rank3 common systems and actual facet rows.
It adds uniform physical bounds

\[
 \|m_i(m)\|\le1,\quad 1/h_i\le2,\quad\|B\|\le1,
 \quad |K_c|\le1,\quad |m\cdot(d_0\times d_1)|>1/100,
\tag{6}
\]

and the recovery/facet constants60/80 below. Ray norms are at most1;
proper marked transport preserves these Euclidean quantities. All
finite computation is in the ordered exact field Q(sqrt(5)).

## 2. All-source area, translation and scale bounds

Choose the sign with `||n-m_j||=d`; projection/reflection are unchanged.
For `0<d<=10^-6`, area in(1) gives
`A(Q^tn)<=A(n)<=a_0+15d`. Equation(4) gives source chord `s<5d` from
some `+/-m_i`, in particular `s<=1/100`.

Put `q'_l=P_nQq_l`. Their weighted mean is zero and squared lengths
are at least `R^2(1-s^2)`. For every unit `a in n^perp`, `z=Q^ta`
is perpendicular to the source normal; its component in `m_i^perp`
has squared norm at least `1-s^2`. The moment bound therefore gives

\[
 \sum\beta_l(a\cdot q'_l)^2\ge(1-s^2)/2.
\tag{7}
\]

If `H=max_l a dot q'_l`, the scalars lie in `[-R,H]` and satisfy
`x^2<=(H-R)x+HR`. Taking their weighted mean yields
`H>=(1-s^2)/(2R)`. The receiver lies in the centered radius-R disk.
If `t!=0`, use `a=t/||t||` and a source vertex attaining H in(1):

\[
 R^2\ge\lambda^2R^2(1-s^2)
       +\lambda\|t\|(1-s^2)/R+\|t\|^2.
\]

Since lambda>=1, including the harmless t=0 case,

\[
 \|t\|\le{R^3s^2\over1-s^2}\le12s^2\le300d^2.
\tag{8}
\]

Here `R^3<45/4`, `s<=1/100`. Weighted squared norms in(1), with the
linear translation term canceled, give `lambda^2(1-s^2)<=1`.
Using `(1+x)^2(1-x)>=1` for `0<=x<=1/2`,

\[
 \lambda-1\le s^2\le25d^2.
\tag{9}
\]

Actual translation and arbitrary roll are bounded before any matching.

## 3. Singleton matching and motion localization

Convexity and `0 in K` allow shrinking lambda to1 with the same Q,t.
Each `z=P_nQq_l+t` then belongs to `P_nC_j` by(5). Its radial defect
`ell=R^2-||z||^2>=0` satisfies, by(8),

\[
 \ell\le(R^2+24R)s^2\le59s^2.
\tag{10}
\]

For a convex representation `z=sum alpha_v P_n v` over actual
`v in W_j`, the exact identity is

\[
 \ell=\sum_v\alpha_v(R^2-\|P_nv\|^2)
       +\sum_{v<w}\alpha_v\alpha_w\|P_nv-P_nw\|^2.
\tag{11}
\]

Nonequatorial v have `|n dot v|>=1/2-Rd>=1/4`; their total mass
b is at most16ell, less than1/2 on this domain. Thus some equatorial
coefficient alpha* is at least1/8. Different receiver equatorial
vertices have projected squared separation at least `1-20d^2>=1/2`.
Keeping their variance terms with alpha* in(11) bounds the other
equatorial mass by16ell. Hence `1-alpha*<=32ell` and
`||z-P_nq_*||<=64Rell<=144ell<=8496s^2`. Removing t gives projected
error at most9000s^2. The two normal components total at mostR(s+d),
so each source singleton matches an actual receiver singleton with

\[
 \|Qq_l-q_*\|\le9000s^2+R(s+d)<20d=:e.
\tag{12}
\]

The matches are injective, since source separation>=1 and `2e<1`.
Every Gram discrepancy of this bijection is at most `2Re<90d<1/2`.
The checked gap forces an isometric correspondence, with its unique
proper catalogue lift Q0.

For the checked source pair a,b, the smaller Gram eigenvalue exceeds
`(81/4)/10>2`. A planar unit vector `x=alpha a+beta b` therefore has
`alpha^2+beta^2<1/2`, so `||(Q-Q0)x||<=e`. Properness gives the normal
bound `||(Q-Q0)m_i||<=2Re/||a cross b||<e`, since the cross-product
length exceeds9/2. For an arbitrary unit vector, resolving its planar
and normal components now yields `||Q-Q0||op<=2e=40d`, proving(3).
At d=0 the original minimum catalogue already gives scale1,t0,Q0.
No unquantified motion neighborhood or compactness is needed for(3).

## 4. Explicit local contact bounds

Use the definitions and exact identities(14)--(19) of the
[local mirror proof](../local_mirror_rigidity/PROOF.md): `u=m+r`,
Cayley vector `w=rho m+p` of Qrel with norm eta, actual translation
lift `C=(1+eta^2)(t-(t dot m)u)/2`, and proper companion
`Qtilde=M_n Qrel M_m` with norm etatilde. Put

\[
 \kappa=\max(\|r\|,\eta,\widetilde\eta),\quad
 a=1200,\quad b=961600,\quad h=2402,\quad\kappa_*=10^{-8}.
\tag{13}
\]

For each common rank3 system the checker verifies its inverse, including
both matrix products. Express C in the orthogonal basis
`e_1=P_m e_y` (or `P_m e_z` if zero), `e_2=m cross e_1`, with norms<=1.
If alpha are eight coefficients recovering one of rho,C1,C2, its
positive common weights omega satisfy `sum omega L=0`. Subtracting
`(min alpha_i/omega_i)omega` gives nonnegative coefficients of total
`sum alpha-min alpha_i/omega_i`; doing the same for the negative
coordinate gives total `max alpha_i/omega_i-sum alpha`. The sum of
three maximum totals is checked <=60. Consequently

\[
 |\rho|+\|C\|\le60\max_i L_i.
\tag{14}
\]

This supplies an explicit replacement of the rank constant in8839.
For every actual row, its unit edge and(6) give
`||m_i(u)-m_i(m)||<=2||r||`. For `kappa<=1/100`, `R<3`,

\[
 |F_i-L_i|\le10\kappa\eta+2\kappa\|C\|.
\tag{15}
\]

The torque drift is at most6||r||eta and the quadratic Cayley term
at most4eta^2. Using Fi<=0, (14) absorbs the translation term when
`120kappa<=1/2`, giving `|rho|+||C||<=a kappa eta`. Apply this also
to the companion. In the inverse companion formula, the rho factor
and the translation-lift ratio are both at most `1+kappa^2`.
Applied jointly to `|rhotilde|+||Ctilde||`, they give

\[
 |\rho|+\|C\|\le h\kappa\min(\eta,\widetilde\eta),
 \qquad h=2(a+1).
\tag{16}
\]

The extra inverse term is `|r dot ptilde|<=kappa etatilde`.
Also `Jr=p+D ptilde-rho r`, `D=1+Jr dot p`, implies
`||r||(1-|rho|)<=eta+(1+kappa^2)etatilde`. Since
`|rho|<=a kappa^2<=1/4`,

\[
 \|r\|\le4\max(\eta,\widetilde\eta).
\tag{17}
\]

Each actual critical facet row has a negative nonzero coefficient
in its respective ray coordinate, reciprocal <=80. Its normal and
translation terms cost at most `3(|rho|+||C||)` because `||g_i||<3`.
Combining(15) with the own bound yields, for `p=xi_0a_0+xi_1a_1`,

\[
 \xi_0^-+\xi_1^-\le2(80)(10+5a)\kappa\eta=b\kappa\eta.
\tag{18}
\]

The companion obeys the same inequality with etatilde in the same
closed receiving cone. All negative coordinates are retained.
For positive coefficient sum P and part p+, the checked acute corners
and `||A||<=1` imply
`(1-(a+b)kappa)eta<=P<=5||p+||` and `||p+||<=(1+b kappa)eta`.
Keeping both mixed signs and dropping the negative-negative term
only because its acute-corner expansion is nonnegative, one gets

\[
 p^tA\widetilde p\ge
 \left\{{(1-(a+b)\kappa)^2\over20}
           -2b\kappa(1+b\kappa)\right\}\eta\widetilde\eta
 \ge{1\over40}\eta\widetilde\eta.
\tag{19}
\]

The last inequality uses `(a+b)kappa<=1/100`. Since `D>=99/100`,
this contributes at least `99 eta etatilde/4000` to the exact
weighted identity(19) of8839.

If eta,etatilde are both positive, all its remaining terms cost at most

\[
 \{(2+8h)\kappa+(2h+2h^2)\kappa^2\}\eta\widetilde\eta.
\tag{20}
\]

The determinant term costs2kappa; `rho B dot r` and `K_c Jr dot C`
cost4h kappa each by(16)--(17). The two remaining terms linear in rho
cost at mosth kappa^2 each. The rho-square term costs2h^2 kappa^2,
using `min(eta,etatilde)^2<=eta etatilde` and `||B||<=1`.
At kappa* the coefficient is below1/100, strictly below99/4000.
The positive common sum F is therefore strictly positive,
contradicting all necessary original contact inequalities. Thus
eta=0 or etatilde=0.

The wall-cross bound in(6) gives receiving cone coordinates
`gamma_0+gamma_1<=200||r||`. At kappa* this is below1/100, so every
contact is valid on its checked closed triangle, including fan walls.
All denominator, domain, absorption and perturbation gates are rational
inequalities checked at kappa*. This proves prototype rigidity for
`kappa<=kappa*` without any initial translation or roll restriction.

## 5. The receiving radius and completion

For `0<d<=d_*`, (3) supplies Q0. Set `Qrel=Q Q0^t`. Equation(5) and
`Q0C_i=C_j` identify the original unit fit with the necessary prototype
fit `P_n(Qrel C_j)+t subseteq P_nC_j`. The original source is within5d
of its minimum axis, the normalized source within41d of m_j, and the
receiver within d of m_j; all lie in their reduction domains.

The receiver chart has `||r||<=2d`. If
`tau=||Qrel-I||op<=40d<=1`, its Cayley norm is
`eta=tau/sqrt(4-tau^2)<=tau<=40d`. The proper companion satisfies

\[
 \widetilde\eta\le
 {\|r\|+\eta+\|r\|\eta\over1-\|r\|\eta}
 \le{42d+80d^2\over1-80d^2}<43d
\tag{21}
\]

throughout d<=10^-6. Hence `kappa<=50d<=kappa*`. Proper marked
transport puts mixed prototypes in representative2 with the same
Euclidean bounds. Section4 forces `Qrel=I` or `Qrel=M_nM_(m_j)`.
Both give exactly the receiver prototype and original shadow. A compact
convex planar body cannot contain a nonzero translate of itself, by
support in direction t. Thus t=0 in the unit fit; equal positive areas
then force lambda=1 in the original scaled fit. The d=0 case follows
from the minimum catalogue. Conversely, the exact prototype reflection
and shadow reductions give(2) throughout these caps. This proves the
theorem.

Every strict original J74 passage of scale>=1 consequently has

\[
 A(n)>a_0+{3\over5\,000\,000\,000}.
\tag{22}
\]

For positive area excess, (4) places its receiver at chord less than d*,
contrary to the theorem; zero excess is already a minimum receiver.
This small global receiving area gap is not a source-area
exclusion or a global non-Rupert decision.

## Trust boundary and remaining frontier

[DEPENDENCIES.json](DEPENDENCIES.json) pins seventeen compact parent
files to source370d5cf35fd56ee1e345348b96f0359e8aae4870. The checker
replays the parent finite certificate, derives all864 bijections,
checks physical moments and inverse identities, and verifies rational
continuum/domain gates. It compares complete expected fields, not just
counts; explicit exceptions remain enabled under Python `-O`.
The computation proves these discrete hypotheses. The convex radial
defect bridge, proper motion estimate, Cayley identity and continuous
inequalities above remain a written unformalized proof.

The generic translated bilinear mechanism is credited to the
[J77 proof7988](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_bilinear_mirror_cap/PROOF.md).
No different body's caps or constants are transferred. The new work is
an explicit all-source J74 correspondence/pose bound and quantitative
closure of the formerly existential collar.

The primary [Gosain–Grimmer Table4](https://arxiv.org/html/2509.08190)
and [Zeng discussion](https://arxiv.org/html/2604.26531) retain five
unresolved Johnson solids. The [Noperthedron](https://arxiv.org/abs/2508.18475)
is a different body. Bounded checks give no priority guarantee.
An exact strict J74 passage outside these minimum caps, or a rigorous
obstruction covering its other receivers, is still needed.
