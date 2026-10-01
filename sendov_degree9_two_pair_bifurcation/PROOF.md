# A true two-pair bifurcation at the lower moving-pair stability curve

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary written author proof with exact coefficient evidence;
independent review of this extension is pending. Earlier reviews retain
their precise scopes. The actual pair construction, lower split-stability
curve and complete leading angular split loss are credited inputs, not
new claims here; [LITERATURE.md](LITERATURE.md) records their authors and
source provenance.

The new steps are a jointly analytic actual two-pair modulus formula
through the collapsing groups, an exact fourth-order energy normal form,
entry of every minimizing member of the **whole** two-pair family into
that scale, and its resulting exact minimum and bifurcating branch.
That branch is stationary under every fixed-energy circle-root angular
motion. Its stability against other angular or inward motions and the
unrestricted full-disk minimizer remain separate questions.

## 1. Definitions and statements

Fix a simple marked real root `0<=a<=1` of
\[
p(z)=c(z-a)\prod_{j=1}^8(z-z_j),\quad c\ne0,\quad
|z_j|\le1,\quad z_j\ne a.
\]
Count all original and critical algebraic multiplicities. Set
\[
v=(1+a)^{-1},\quad b=1-a^2,\qquad
E=\sum_{j=1}^8|(a-z_j)^{-1}-v|^2,\quad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}.
\tag{1}
\]
All critical reciprocals here are finite because `p'(a)!=0`.
The actual moving pair retains **six-sendov-2, 7328** credit:
\[
x(a,s)={(1+a)^4s\over4+2a(1+a)^2s},\qquad
A_{a,s}(z)=z^2+2(1-x(a,s))z+1,
\]
\[
Q_{a,e}(z)=(z-a)(z+1)^6A_{a,e}(z).
\tag{2}
\]
For sufficiently small s>=0, A has roots `-exp(±it_s)`, where
`1-cos t_s=x(a,s)` and `t_s>=0`. Their exact E contribution is s,
and `t_s^2=s/(2v^4)+O(s^2)`.

The actual two-pair family was introduced in **8315**, six-sendov-3:
\[
R_{a;e,f}(z)=(z-a)(z+1)^4A_{a,e-f}(z)A_{a,f}(z),
\qquad0\le f\le e.
\tag{3}
\]
It has E=e exactly, four collapsed circle roots and two opposite circle
pairs. Its two endpoints give Q, and `R_(f)=R_(e-f)` exactly.
The family includes every f in its stated interval; no ordering of
critical-point distances is assumed.

Write
\[
a_-={6\sqrt{101}-29\over52},\quad
v_-={24\sqrt{101}-92\over239},\quad
C_d={d^3(4d+1)^2\over8192},\quad d=1+a,
\]
\[
\gamma(a)={64C_{1+a}\over81}={(4+v)^2\over10368v^5},\qquad
\gamma_-:=\gamma(a_-)>0.
\tag{4}
\]
The derivative and analytic curve retain **8315** credit:
\[
H(a,e)=\left.\partial_fF(R_{a;e,f})\right|_{f=0+}
      =h_1(a)e+h_2(a)e^2+O(e^3),
\]
\[
h_1={208-184v-239v^2\over2304v^5},\qquad
h_2={-245888+771984v-786792v^2+246931v^3\over4718592v^8},
\]
\[
a_Q(e)=a_-+c_Qe+O(e^2),\quad H(a_Q(e),e)=0,
\quad c_Q=-h_2(a_-)/\lambda_-,
\quad\lambda_-:=h_1'(a_-)={\sqrt{101}\over48v_-^3}>0.
\tag{5}
\]
In particular h2(a_-)<0 and `.112226<c_Q<.112227`.

**Theorem 1 (true rescaled normal form).** For each finite M>=0 there
are a radius neighborhood of a_- and a common e0>0 on which the actual
sum for f=e^2 rho, `0<=rho<=M,0<e<e0`, has an analytic extension in
`(a,e,rho)` and the exact identity
\[
F(R_{a;e,e^2\rho})-F(Q_{a,e})
  =e^2H(a,e)\rho+e^4\rho^2 B(a,e,\rho),
\tag{6}
\]
where B is jointly real analytic and
\[
B(a,0,\rho)=\gamma(a)-h_1(a).
\tag{7}
\]
All analytic neighborhoods and remainders may be chosen uniformly on
the stated compact rho interval. Signed parameters are used only for
analytic continuation; physical roots and modulus interpretation are
asserted at positive e and nonnegative rho.

In the radius window `a=a_Q(e)+ce`, `|c|<=1/5`, define the gap divided
by e^4 as W. It extends analytically and
\[
W(e,c,\rho)=c\Lambda(e,c)\rho+\rho^2\mathcal B(e,c,\rho),
\quad\Lambda(0,c)=\lambda_-,\quad\mathcal B(0,c,\rho)=\gamma_-.
\tag{8}
\]
For each finite M there is a constant C_M such that, uniformly,
\[
|W-\lambda_-c\rho-\gamma_-\rho^2|
 \le C_M e(|c|\rho+\rho^2).
\tag{9}
\]
Its first two rho derivatives also converge uniformly to those of the
displayed quadratic. In particular, at `a=a_Q(e)`, Q is strictly lower
than each nonzero scaled auxiliary split in this family; its true
single-direction quartic coefficient is positive.

**Theorem 2 (minimum of the whole two-pair family and angular stationarity).**
There is one e0>0 such that, for every `0<e<e0, |c|<=1/5` and
`a=a_Q(e)+ce`, the complete family (3), with every `0<=f<=e`, has
precisely the following minimizing polynomial, modulo scalar and root
permutation:

- if c>=0, Q alone, including c=0;
- if c<0, `R_(a;e,e^2 rho_*(e,c))`, with the parameter value
  `e-e^2 rho_*` giving the identical polynomial.

Here rho_* is uniquely determined in `(0,6)` on the negative side,
extends jointly real analytically to c=0, and
\[
\rho_*(e,c)=-{\lambda_-\over2\gamma_-}c+O(e|c|).
\tag{10}
\]
The entire family minimum obeys the relative law
\[
F_{\rm pair,min}-F(Q)=
-e^4c^2\left\{{\lambda_-^2\over4\gamma_-}+O(e)\right\}\quad(c\le0),
\tag{11}
\]
and is exactly F(Q) for c>=0. Uniformity includes c=0; its zero gap is
not replaced by an absolute error. For c<0 the new branch is stationary
under all seven fixed-energy circle-root angular directions, including
the collapsed-block directions. This statement does not assert that it
is a local minimum against all those directions or inward motions.

**Corollary 3 (quantified endpoint construction).** At a=a_- the family
minimum has auxiliary energy and gap
\[
f_*(e)=\beta e^2+O(e^3),\quad
\beta=-{h_2(a_-)\over2\gamma_-},\qquad
F_{\rm pair,min}=F(Q)-\nu e^4+O(e^5),\quad
\nu={h_2(a_-)^2\over4\gamma_-}>0,
\tag{12}
\]
\[
2.219843<\beta<2.219844,\qquad .107206<\nu<.107207.
\tag{13}
\]
Even the completely explicit rational transfer `f=(11/5)e^2` gives
\[
F(R_{a_-;e,(11/5)e^2})-F(Q_{a_-,e})
 =-\nu_0e^4+O(e^5),\quad
\nu_0=-{11\over5}h_2(a_-)-{121\over25}\gamma_-,
\]
\[
.107198<\nu_0<.107199.
\tag{14}
\]
Every root of these polynomials is in the closed unit disk. Thus they
give an admissible order-e^4 improvement for the full-disk infimum as
well. They are not claimed to attain that unrestricted infimum.

## 2. Complete actual reciprocal polynomial and characteristic

For the actual opposite pair, direct substitution `z=a-1/q` in A and
clearing its x denominator gives
\[
u_+u_-=v^2+as/2,\qquad u_++u_-=2v-bs/2.
\]
Its energy is `2u_+u_--2v(u_++u_-)+2v^2=s`, since `bv+a=1`.
With xi=q-v and `k(xi)=(1+bxi)/2`, its monic reciprocal polynomial is
`xi^2+s k(xi)`. This is an actual original-root transform, not a proposed
critical tuple.

Consequently the full degree-eight original reciprocal polynomial for
(3) is
\[
\mathcal R=\xi^8+e k(\xi)\xi^6+f(e-f)k(\xi)^2\xi^4.
\]
Differentiating `p(a-1/q)=-c prod_j(a-z_j) q^-9 R(q)` gives the
complete critical characteristic `9R-qRprime`. In full,
\[
9\mathcal R-q\mathcal R'=\xi^3C_5(\xi),\quad
C_5=\xi^2C_3+f(e-f)J,
\tag{15}
\]
\[
C_3=\xi^3+A\xi^2+B_0\xi+C_0,\quad
A=-8v+be,\quad B_0=k_1e,\quad C_0=-3ve,\quad k_1=(7a-4)/2,
\]
\[
J=J_3\xi^3+J_2\xi^2+J_1\xi+J_0,
\quad(J_3,J_2,J_1,J_0)=
(3b^2/4,b(3a+1)/2,5(2a-1)/4,-v).
\tag{16}
\]
The leading characteristic coefficient is one, and its q=0 constant
is nonzero. It counts all eight critical reciprocals. For f>0 small,
three remain fixed at v; at f=0 two more coalesce there. The source
checker verifies every coefficient of the complete characteristic.

## 3. Analytic group factorization on the small energy-transfer scale

Set f=e^2 rho and `D=e^3rho-e^4rho^2`. Seek monic factors
\[
C_5=(\xi^2-e^2 S\xi+e^2P)
           (\xi^3+A_c\xi^2+B_c\xi+C_c).
\tag{17}
\]
The leading three coefficient equations give exactly
\[
A_c=A+e^2S,\quad
B_c=B_0+DJ_3+e^2SA_c-e^2P,
\]
\[
C_c=C_0+DJ_2+e^2SB_c-e^2PA_c.
\tag{18}
\]
The two remaining equations, after removing e^3, are
\[
P(C_c/e)=(\rho-e\rho^2)J_0,
\quad -S(C_c/e)+P(B_c/e)=(\rho-e\rho^2)J_1.
\tag{19}
\]
The divided coefficients are polynomials analytic at e=0; their values
there are -3v and k1. Thus the unique limiting solution is
\[
P_0=\rho/3,\quad S_0=\rho(16a-7)/(36v).
\tag{20}
\]
The Jacobian of the left residuals, in variables (P,S), is triangular
at e=0, with diagonal -3v,3v and determinant -9v^2!=0.
It is nonsingular independently of rho. The analytic IFT gives a
jointly analytic solution on a neighborhood of every compact
`(a,rho)` set considered here. Compactness gives one common small energy
threshold; local solutions glue by their uniqueness near (20).

At rho=0 the exact solution is P=S=0 for every small e. Therefore
`P=rho p` and `S=rho s` analytically, with `p(a,0,rho)=1/3`.
For rho>0 small positive e the auxiliary discriminant is
\[
e^4S^2-4e^2P=e^2\rho(e^2\rho s^2-4p)<0
\]
uniformly on `0<rho<=M`. Its q-product and total modulus are
\[
v^2+ve^2S+e^2P,\qquad 2\sqrt{v^2+ve^2S+e^2P}.
\tag{21}
\]
At rho=0 the same formula counts two copies of v.

The external cubic has a simple far root q_f, with q_f(0)=9v and
q derivative 64v^2 at zero. Its two near roots have
`xi=±i sqrt(3e/8)+O(e)` and stay conjugate. The external q-product is
\[
P_c=-[(-v)^3+A_cv^2-B_cv+C_c],
\]
so the actual sum, for positive e and nonnegative rho, is exactly
\[
\mathcal F(a,e,\rho)=3v+2\sqrt{v^2+ve^2S+e^2P}
                   +q_f+2\sqrt{P_c/q_f}.
\tag{22}
\]
Both square roots have positive constant v. Formula (22) consequently
defines a jointly analytic extension through e=0 and rho=0. There is no
requirement that individual colliding critical labels be analytic.

## 4. Exact coefficients and whole-box divisibility

The exact checker recursively solves (19) through energy degree two.
Its first corrections, for example, are
\[
P=\rho/3-e\rho^2/27+O(e^2),\quad
S=\rho(16a-7)/(36v)+e\rho^2/(12v)+O(e^2).
\]
It verifies all six coefficients of (17) through energy degree five.
The far cubic and both positive squared-modulus identities are then
checked through degree four. The **entire** rho-polynomial gap is
\[
\mathcal F(a,e,\rho)-\mathcal F(a,e,0)
=e^3h_1(a)\rho+e^4\{h_2(a)\rho+q_2(a)\rho^2\}+O(e^5),
\tag{23}
\]
\[
q_2(a)={-1840+1672v+2153v^2\over20736v^5}
       =\gamma(a)-h_1(a).
\tag{24}
\]
These are identities in v and rho, with all lower coefficients zero.
No finite radius or direction interpolation is used. Uniform analytic
remainders and their rho derivatives follow from (22) on the whole compact
box, not from the older o(e^2) leading angular error.

For each positive e the chain rule at rho=0 gives
`partial_rho F=e^2 H(a,e)`. This equality extends analytically. The
gap minus that exact linear term therefore vanishes to second order
in rho. Its energy coefficients through degree three vanish identically
by (23); analytic division gives `e^4 rho^2 B`. Equation (24) gives
its value (7). This proves (6) with both zero-coordinate factors intact.

Put `K(a,e)=H(a,e)/e`. Integrating its a derivative along the segment
from a_Q(e) to a_Q(e)+ce gives
\[
H(a_Q(e)+ce,e)=e^2c\Lambda(e,c),\quad
\Lambda(e,c)=\int_0^1K_a(a_Q(e)+tce,e)\,dt>0.
\tag{25}
\]
Its limiting value is lambda_-. Combining (6) and (25) gives (8).
Analyticity on bounded c,rho sets gives (9), with
`Lambda-lambda_-=O(e)`, `Bcal-gamma_-=O(e)` and
`Bcal_rho,Bcal_rhorho=O(e)`. This also proves the derivative uniformity.
The single-split true quartic at the curve follows from (6): if the
auxiliary pair phases are ±delta, then
`f=2v^4delta^2+O(delta^4)`, so at fixed positive e
\[
F-F(Q)=4v^8B(a_Q(e),e,0)\delta^4+o_e(\delta^4)>0
\]
for every sufficiently small nonzero delta. This is one actual slice,
not a conclusion for all zero-sum six-root directions.

## 5. Uniform analyticity for every energy fraction in the two-pair family

To justify whole-family entry, restrict by the exact symmetry in (3) to
`u=f/e in[0,1/2]`. Repeat the coefficient factorization at its natural
whole-family scale:
\[
C_5=(\xi^2-eS\xi+eP)(\xi^3+A_c\xi^2+B_c\xi+C_c),
\]
\[
D=e^2u(1-u),\quad A_c=A+eS,
\quad B_c=B_0+DJ_3+eSA_c-eP,
\quad C_c=C_0+DJ_2+eSB_c-ePA_c.
\tag{26}
\]
The low coefficient equations, divided by e^2, are
\[
P(C_c/e)=u(1-u)J_0,\quad
-S(C_c/e)+P(B_c/e)=u(1-u)J_1.
\tag{27}
\]
At e=0 they give
\[
8P_0^2-3P_0+u(1-u)=0,\quad
\Delta(u)=9-32u+32u^2=1+32(u-1/2)^2\ge1,
\]
\[
P_0={3-\sqrt\Delta\over16}\in[0,1/8],\qquad
S_0={u(1-u)J_1-P_0(k_1-P_0)\over v\sqrt\Delta}.
\tag{28}
\]
The low-equation Jacobian is again triangular: its diagonal is
`-v sqrtDelta, v sqrtDelta`, with determinant `-v^2 Delta`, uniformly
nonzero. Indeed `(3-16P0)^2=Delta` follows directly from the first
equation. The limiting branch (28), uniform analytic IFT and uniqueness
give jointly analytic P,S on a common neighborhood of the entire
compact interval `[0,1/2]` and small e, near a_-.

At u=0, P=S=0 identically, so both are analytically divisible by u.
Moreover `P0/u=2(1-u)/(3+sqrtDelta)>0`, including its limit at zero.
Thus the auxiliary pair is nonreal for u>0 small positive e, with
discriminant `e^2S^2-4eP<0` uniformly away from its trivial u factor.
For the external cubic `C_c/e` tends to `-3v+8vP0`; the two near
roots have squared leading xi coordinate
\[
\xi^2/e\longrightarrow -(3/8-P_0),\qquad3/8-P_0\ge1/4.
\]
They are a separated conjugate pair. The far root remains positive
and simple. Consequently the full actual sum has the same positive
square-root formula as (22), now with auxiliary product `v^2+veS+eP`.
It defines a jointly analytic function `Fhat(a,e,u)` on this whole
compact parameter set. At u=0 it gives Q; at u=1/2 it counts every
multiplicity of the two equal original pairs. No gap inside a collapsed
critical group is assumed.

## 6. Entry of every minimizing member into the rescaled chart

The credited collision-uniform original-root quartic from 8212/8258,
reconstructed in independent review 8305, applies to the actual zero-mean
circle phases in (3), on all marked radii and all u in the present compact
interval. It implies
\[
\widehat F(a,e,u)-F(Q_{a,e})=e^2U(a,u)+o(e^2),
\quad U(a,u)=K_Q(a)-K_a(\theta(u)),
\]
\[
\theta(u)=(\sqrt{1-u},-\sqrt{1-u},\sqrt u,-\sqrt u,0^4).
\tag{29}
\]
K is scale invariant. Exact pair energy fixes the overall scale; all
mean and inward terms in that reviewed quartic are zero here. Its
uniformity includes u=0 and critical collisions. These inputs are used
within their original domains, without any full-disk exact-minimum
assumption at a_-.

By the new joint analyticity from Section 5, (29) identifies the exact
energy coefficient. Because the gap vanishes at u=0, its analytic
remainder is divisible by u. Thus on one common box
\[
\widehat F-F(Q)=e^2U(a,u)+e^3u V(a,e,u),
\tag{30}
\]
where U,V are analytic and bounded with the needed derivatives.
This strengthens the older little-oh only on the present actual family;
the strengthening follows from its newly proved analytic factorization.

Independent review **8305**, actual six-reviewer-3, already proved the
complete leading angular single-curve identity at a_-:
\[
K_Q-K_{a_-}(1,-1,s,-s,0^4)
={64C_{1+a_-}z^2\over9(1+z)^2(9-14z+9z^2)},\quad z=s^2.
\]
Substitute `z=u/(1-u)` to obtain its credited consequence
\[
U(a_-,u)={64C_{1+a_-}u^2(1-u)^2\over9\Delta(u)}
\ge\gamma_-u^2\qquad(0\le u\le1/2).
\tag{31}
\]
For completeness the entire cleared inequality residual is
\[
{64C_d\over9}u^2(1-u)^2-\gamma u^2\Delta(u)
=\gamma u^3(14-23u)\ge0;
\tag{32}
\]
`14-23u>=5/2` on the closed interval. The source checks the full
polynomial identity. The angular formula and barrier retain the
reviewer's credit; the entry using the actual analytic sum is new here.

Since U(a,0)=0, its radius derivative is bounded by C u on a common
compact box. In the window `a=a_Q(e)+ce, |c|<=1/5`, one has
`|a-a_-|<=C'e`. Equations (30)--(31) therefore give
\[
\widehat F-F(Q)\ge e^2(\gamma_-u^2-C''e u).
\tag{33}
\]
Every member with value at most F(Q) satisfies `u<=M_0e`, for a fixed
finite M0 independent of e,c. The complete family has an attained
minimum by continuity on `[0,e]`, and that minimum is at most F(Q).
Thus every minimizing member, after f/e is reflected to `[0,1/2]`,
has `f=e^2rho` with bounded rho. This is a complete entry proof for
this family; it does not assert entry of arbitrary eight-root configurations.

## 7. Strict convexity, exact family minima and the bifurcating branch

Apply Theorem 1 on a compact rho interval containing `[0,max(M0,6)]`.
In the c window its normalized second derivative is
`W_rhorho=2gamma_-+O(e)`, uniformly, and is at least gamma_->0 after
shrinking the common threshold. At rho=0, `W_rho=c Lambda`.
The exact endpoint field certificate verifies
\[
12\gamma_--\lambda_-/5>0.
\tag{34}
\]
Therefore `W_rho(e,c,6)>0` uniformly for `|c|<=1/5` at small e.
For c>=0, W increases strictly at all rho>0 and its unique minimum is
zero at rho=0. For c<0, its negative derivative at zero and positive
derivative at six give exactly one interior stationary point, with
strict positive second derivative. It is the unique minimum throughout
the entire entry interval. This proves all minimizing-family cases in
Theorem 2, including c=0. Exact symmetry in f identifies the apparent
two parameter values as the same polynomial.

At e=0 the stationary equation is `lambda_- c+2gamma_-rho=0`.
The analytic IFT at every point of its compact c segment gives
rho_*(e,c) jointly analytic, with limit (10). Uniqueness glues these
solutions. At c=0, the solution is exactly zero for all small e, so
rho_* is divisible by c, which gives the relative O(e|c|) error.
Substitution in the stationary equation and in W gives (11), with
an analytic positive coefficient after removing c^2.

At a=a_-, the parameter
`c(e)=(a_--a_Q(e))/e=-c_Q+O(e)` is analytic, lies in `[-1/5,0)`
for small e, and gives (12) by substitution. The rational transfer
rho=11/5 follows directly from (23) at h1=0. Bounds (13)--(14)
are certified in the exact positive field
`Q[v]/(239v^2+184v-208)`, with v in `(3/5,5/8)` and
`sqrt101=(239v+92)/24>0`. All inverses and reduced coefficients are
exact, and linear field expressions are bounded at rational isolating
endpoints. No decimal square root or floating sign enters the proof.

## 8. Stationarity under all circle-root angular motions

Fix a point on the new branch with c<0 and positive e. Both opposite
pairs are nontrivial; their five nonfixed critical reciprocals are
simple and separated. The three fixed reciprocals q=v are semisimple.
To check the last fact and the first derivative through the collision,
use `N=diag(u_j)(I+11^T)`, whose determinant lemma gives exactly
`det(qI-N)=9R-qRprime`. For the four equal original reciprocals v,
the supported zero-sum four-space is both a left and right reducing
space, and N on it is vI. The source independently checks all left
and right vector entries on three spanning differences and five
complete linear inputs (four external reciprocals plus the common v).

At this fixed positive e and f the three-group is separated from
every other critical root. Analytic invariant subspace compression
therefore makes its perturbation `vI+O(||delta u||)`. Its eigenvalues
shift by O(||delta u||), and their modulus sum is
\[
3v+\operatorname{Re}\operatorname{tr}(N_3-vI)+O(\|\delta u\|^2).
\]
The other simple moduli are differentiable. Hence F has a genuine
first angular differential at this collided point. No uniform internal
three-group gap or arbitrary individual critical labeling is needed.

Use the two pair amplitudes, their two common phase means, and four
independent collapsed-root phases as eight local circle coordinates.
Conjugation and pair interchange negate both means and all collapsed
phases while fixing the amplitudes. Invariance of F and E consequently
makes all those odd-coordinate derivatives zero at the real branch.
Each positive pair amplitude has strictly positive energy derivative,
as follows from its exact formula in (2). The two remaining amplitude
directions, at fixed total E, have just the one energy-transfer coordinate
f. At rho_* its F derivative is zero by the scalar stationary equation.
Thus the first differential vanishes on every fixed-energy angular
direction. This proves the stationarity claim while leaving the full
angular Hessian and all inward variations unclassified.

## 9. Evidence boundaries and next frontier

The self-contained CPython 3.11.2 checker uses exact fractions over
`Q[v,v^-1,rho]`, energy jets modulo e^6 for factor evidence and degree
four for the objective, plus an exactly isolated positive quadratic field.
It verifies 78 identities, eleven strict signs, ten damaged expressions,
and all thirty complete reducing-space vectors. All 32 complete records
must match the mandatory compact fixture in normal and optimized modes.
The complete eight-root/critical polynomial has actual energy degree at
most four, so its jet check retains every coefficient. The approximate
S,P series are checked only to their claimed degree, and no fifth-order
objective coefficient is claimed from them.

Analytic group factorization on both scales, the physical conjugate-root
regime, positive square-root interpretation, whole-box divisibility,
uniform remainder, reviewed quartic transfer, minimizing-family entry,
implicit branch and angular derivative at collisions are ordinary written
proof outside a formal kernel. Full fixture equality, hashes and source
publication do not prove these bridges. Earlier reviewed premises and
their original authors remain precisely credited. Independent review of
the new normal form, entry and branch is pending.

The next frontier is the complete constrained Hessian and true quartic
law in all five former six-block split directions, particularly the
three remaining four-root split modes on the new branch, together with
mean coupling and all independent inward depths. This exact family
minimum and angular stationary branch supply candidates and a quantified
upper comparison for that problem. They do not establish unrestricted
full-disk local or global minimality, or the first-power endpoint.
