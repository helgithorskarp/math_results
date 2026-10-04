# Balanced critical real means improve the fourth boundary coefficient

Author: **six-sendov-3 / researcher**. This is a complete ordinary author
argument with exact finite coefficient checks. The implicit-function and
uniform remainder arguments are **unformalized**. The new statement has no
independent review. Earlier reviews retain their original scopes.

## 1. Statement and domain

Put \(a=1-\eta\), \(0<\eta\), and let

\[
 F(p,a)=\sum_{p'(\zeta)=0}\frac1{|a-\zeta|},
\]

counting all eight critical multiplicities of a monic polynomial of degree
nine. A collision contributes infinity. In this note an actual polynomial
has all nine original roots in the closed unit disk and has the marked
root \(a\). Let \(\mathcal I(\eta)\) be the infimum of \(F\) over that
domain. The constructed polynomials below have no critical collision.

Define \(c=\cos(\pi/9)\), and the already credited third comparison

\[
 M_3(\eta)=8+C\eta+B_*\eta^2+T_*\eta^3,
\]

where

\[
 C=\frac83+\frac1{3(1+c)},\qquad
 B_*=\frac{2311}{108}+\frac{4934}{27}c-\frac{1976}{9}c^2,
\]

\[
 T_*=-\frac{60800959}{17496}
      -\frac{307083769}{17496}c+\frac{10980067}{486}c^2.
\]

The prior constructed fourth coefficient in
[10212](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/optimal-cap-construction/PROOF.md)
is

\[
 G_* = \frac{183619658945}{2519424}
       +\frac{444829186913}{1259712}c
       -\frac{288729410449}{629856}c^2 <0.
\]

**Lemma.** Set

\[
 L=-\frac{101920}{243}-\frac{1218245}{486}c
                       +\frac{251888}{81}c^2,
 \qquad \mu_*=-\frac38L.
\]

Then \(L<0\), \(8<\mu_*<16\), and

\[
 G_{\rm mean}=G_*-\frac3{16}L^2
 =\frac{340367352475}{839808}
  +\frac{808137564635}{419904}c
  -\frac{1052841914857}{419904}c^2
 <G_*<0.
\]

For every compact real parameter set \(K\), there is \(\eta_K>0\)
and an explicit polynomial family \(p_{\eta,\mu}\), for
\(\mu\in K\) and \(0<\eta<\eta_K\), having all nine original roots
simple and strictly inside the disk, with marked root \(1-\eta\), and

\[
 F(p_{\eta,\mu},1-\eta)
 =M_3(\eta)
  +\left(G_*+L\mu+\frac43\mu^2\right)\eta^4
  +8\eta^{9/2}+O_K(\eta^5).                 \tag{1}
\]

Consequently

\[
 \limsup_{\eta\downarrow0}
 \frac{\mathcal I(\eta)-M_3(\eta)}{\eta^4}
 \le G_{\rm mean}<G_* .                    \tag{2}
\]

The fourth coefficient \(G_{\rm mean}\) is sharp **within the coupled
real six-plus-two repair class defined in Section 5**. No sharp universal
fourth lower bound or existence of a universal fourth limit is proved.
In particular, (2) prevents promoting the old constructed \(G_*\) to a
universal sharp fourth lower coefficient. It does not contradict 10212 or
10254: both stated restricted constructed classes. None of these boundary
comparisons resolves the unrestricted first-power conjecture.

## 2. Explicit family, including the displaced means

Put

\[
 y=\frac1{3(1+c)},\quad x=\frac23-y,\quad H=14y,
 \quad U_0=-8x,\quad \rho=\frac{c-5}{3},
\]

\[
 u_z=\frac{U_0+\rho H}{8},\qquad
 u_p=u_z-\frac{\rho H}{2},\qquad
 W_* =\frac{2512}{27}+\frac{5840}{9}c-\frac{21392}{27}c^2,
 \quad w_2=W_*/8,
\]

\[
 \Gamma=\frac{13}{36}+\frac{1253}{72}c-\frac{50}{3}c^2,
\]

\[
 m_0=-\frac{17403419}{34992}-\frac{45702565}{17496}c
                                 +\frac{180635}{54}c^2,
\]

\[
 b_0=-\frac{1162307}{23328}-\frac{5484833}{11664}c
                                 +\frac{52426519}{93312}c^2,
\]

\[
 M_* =\frac{8148040331}{629856}
       +\frac{78878749667}{1259712}c-\frac{51194418673}{629856}c^2,
\]

\[
 \beta_* =\frac{27821775167}{17915904}
       +\frac{80418819893}{8957952}c-\frac{12650091319}{1119744}c^2.
\]

These zero-mean constants come from the same-author 10152/10212 actual
comparison construction. They are prior work; reproducing them is a
validation step, not the new lemma. The new functions are

\[
 m(\mu)=m_0+\frac{56}{9}(c-c^2)\mu,
 \qquad b(\mu)=b_0+\left(\frac12+2c\right)\mu,
                                                               \tag{3}
\]

\[
 \widehat M(\mu)=M_*+
       \left(-\frac{51583}{972}-\frac{175385}{486}c+448c^2\right)\mu,
                                                               \tag{4}
\]

\[
 \widehat\beta(\mu)=\beta_*+
       \left(\frac{1771}{324}-\frac{94039}{1296}c
                             +\frac{12347}{162}c^2\right)\mu
       +\frac27(1+c)\mu^2.                                    \tag{5}
\]

Define the real centers and imaginary pair scale by

\[
 A=u_z\eta+(w_2-\mu/3)\eta^2+m(\mu)\eta^3
                         +\widehat M(\mu)\eta^4+\eta^{9/2},
\]

\[
 B=u_p\eta+(w_2+\mu)\eta^2+m(\mu)\eta^3
                         +\widehat M(\mu)\eta^4+\eta^{9/2},
\]

\[
 K_\eta=i\left[1+\Gamma\eta+b(\mu)\eta^2
                              +\widehat\beta(\mu)\eta^3\right],
\]

\[
 p'_{\eta,\mu}(z)=9(z-A)^6
       \left[(z-B)^2-\frac H2\eta K_\eta^2\right],
 \qquad
 p_{\eta,\mu}(z)=\int_{1-\eta}^{z}p'_{\eta,\mu}(w)\,dw.      \tag{6}
\]

The integral is the polynomial primitive with the displayed anchor, so
the polynomial is monic of degree nine and has marked root \(1-\eta\).
Its critical slots are six at \(A\) and the conjugate pair
\(B\pm\sqrt{H/2}\sqrt\eta K_\eta\). For sufficiently small \(\eta\),
the pair scale is nonzero and the critical distances from the anchor
are bounded away from zero, uniformly on compact \(\mu\) sets.

The eight order-\(\eta^2\) real displacements are the balanced vector
\((\mu,\mu,-\mu/3,\ldots,-\mu/3)\). They have zero sum and zero
dot product with the leading opposite imaginary pair. Thus the leading
sum and mixed constraints do not remove this direction. Equations
(3)--(5) pay the changes in the higher actual normal budgets. Keeping
the old third repairs fixed would incorrectly exclude the useful mode.

## 3. Exact coefficients and all original roots

Here is a finite derivation that also specifies how the checkable
coefficient identities establish the claimed expansions. Use
\(\omega=\exp(2\pi i/9)\), \(\theta_j=2\pi j/9\), and
\(\epsilon=\sqrt\eta\). All polynomial coefficients in (6) are
polynomials in \(\epsilon\) and \(\mu\), over
\(\mathbb Q(\omega,i)\). Reduce powers of \(\omega\) with
\(\omega^6+\omega^3+1=0\). The real constants are in
\(\mathbb Q(c)\), with \(8c^3-6c-1=0\) and
\(c=-(\omega^4+\omega^5)/2\). Complex conjugation sends
\(\omega\) to \(\omega^{-1}\) and \(i\) to \(-i\).

The literal primitive of (6) and a second primitive obtained by all
eight power sums and Newton's elementary-symmetric recursion agree
coefficient by coefficient. For each \(j=0,\ldots,8\), write
\(Z_j=\omega^j+\sum_{e=1}^9 d_{j,e}\epsilon^e\). If all lower
coefficients are already known, the order-\(e\) equation has coefficient
\(9\omega^{8j}d_{j,e}\). Hence

\[
 d_{j,e}=-\frac{\omega^j}{9}
 [\epsilon^e]p_{\epsilon^2,\mu}
       \left(\omega^j+\sum_{k<e}d_{j,k}\epsilon^k\right).     \tag{7}
\]

This determines every original root coefficient, not just active
normals. Let \(N_j=(|Z_j|^2-1)/2\). Each of the nine full root equations
and half-normal vectors through \(\epsilon^9\) is stored and compared
in [EXPECTED.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/real-mean-fourth-repair/EXPECTED.json).
This is a whole polynomial coefficient comparison, not a check at finitely
many real values of \(\mu\).

For clarity, the two actual repair columns have a short derivation.
Adding \(t\eta^q\) to both centers, with \(q=3\) or \(4\), changes
the order-\(\eta^q\) primitive by \(9t(1-z^8)\).
Adding \(s\eta^{q-1}\) to the imaginary scale bracket changes that
primitive by \((9H/7)s(z^7-1)\). Their half-normal changes at label
\(j\) are therefore

\[
 -A_jt+\frac H7 B_js,
 \qquad A_j=1-\cos\theta_j,\quad B_j=1-\cos2\theta_j.       \tag{8}
\]

At \(j=3\), \((A_3,B_3)=(3/2,3/2)\); at \(j=4\),
\((A_4,B_4)=(1+c,2-2c^2)\). The determinant of the two columns
\((-A_j,HB_j/7)\) is \(2c-1>0\). Complex-conjugate symmetry
pays labels 5 and 6 individually as well. Solving first the order-three
and then the order-four row equations gives exactly (3) and (4)--(5).
The full calculation verifies all four active normals vanish through
order four in \(\eta\), and the lower first-power coefficients remain
\(8,C,B_*,T_*\) for every real \(\mu\).

For every label the first half-normal coefficient is

\[
 \nu_j=-\left(\frac13+x\cos\theta_j+y\cos2\theta_j\right).
                                                               \tag{9}
\]

It vanishes at labels \(3,4,5,6\) and is strictly negative at
\(0,1,2,7,8\). The strictly positive signs of the negatives are checked
with rational bounds on the physical cubic root. The additional common
center term \(\epsilon^9\) in (6) gives the primitive response
\(9(1-z^8)\epsilon^9\) and the root response
\((1-\omega^j)\epsilon^9\). Thus, at each active label separately,

\[
 N_j=-(1-\cos\theta_j)\epsilon^9+O_K(\epsilon^{10}),
 \qquad j=3,4,5,6.                                           \tag{10}
\]

At each inactive label,
\(N_j=\nu_j\epsilon^2+O_K(\epsilon^4)\). All nine equations and
these half-normal responses are checked in the finite record; no root
is omitted. In particular, label zero is the prescribed anchor.

## 4. Analytic containment, scalar cost and optimization

The primitive (6) is a polynomial in \(\epsilon\) whose coefficients
depend polynomially on \(\mu\). At \(\epsilon=0\) it is \(z^9-1\),
and the derivative is nonzero at every \(\omega^j\). The complex
implicit-function theorem supplies all nine analytic root branches.
Distinct disjoint neighborhoods of these nine roots can be fixed in
advance. Compactness of any fixed \(K\subset\mathbb R\) gives a common
small \(\epsilon\) collar and uniform Taylor remainders there. Equation
(7) is their unique Taylor recursion. The branches remain simple and
distinct; their number exhausts degree nine. The fixed negative
coefficients in (9) and (10), with the uniform remainders, make **every
original root strictly interior** when \(0<\eta<\eta_K\). This
argument supplies an existence collar; it does not compute a numerical
\(\eta_K\).

The scalar sum for the critical multiset in (6) is exactly

\[
 \frac6{a-A}+\frac2{\sqrt{(a-B)^2+(H/2)\eta |K_\eta|^2}},   \tag{11}
\]

where \(a-A>0\) on a sufficiently small common collar. Taylor expansion
of the first denominator and of \((1+t)^{-1/2}\) through its fourth
coefficient gives (1). Before the inward center term, its entire
fourth coefficient is

\[
 G(\mu)=G_*+L\mu+\frac43\mu^2.                            \tag{12}
\]

The coefficient at \(\epsilon^9\) from the common inward motion is
\(8\). The scalar expression (11) is analytic in \(\epsilon\) near
zero with its positive branch, uniformly on compact \(\mu\) sets.
Thus the first omitted term is \(O_K(\epsilon^{10})=O_K(\eta^5)\).
All coefficients, including the inward response, are verified by the
direct scalar formula independently of original-root recursion.

For exact signs, \(8c^3-6c-1\) has exactly one positive root by
Descartes' rule; its signs at \(15/16\) and \(47/50\) identify this
root. The derivative is positive throughout that bracket. For example,
elementary rational interval evaluation already gives

\[
 -\frac{826987}{19440}\ \le L\ \le
 -\frac{105352667}{4860000}<0.
\]

The accompanying bounds on \(-3L/8\) give \(8<\mu_*<16\).
The exact checker narrows the same bracket by 24 rational bisections
and verifies the signs of \(-G_*\), \(3L^2/16\), and
\(-G_{\rm mean}\) as well. No floating-point sign test is used.
Completing the square gives the entire identity

\[
 G(\mu)=G_{\rm mean}+\frac43(\mu-\mu_*)^2.                 \tag{13}
\]

Choosing the fixed value \(\mu_*\) in the actual interior family
proves (2). The strict improvement is \(3L^2/16>0\). Cubic reduction
of this square gives exactly the displayed formula for \(G_{\rm mean}\).

## 5. Sharpness in the stated coupled real repair class

Define this class explicitly; it is not asserted to contain all actual
competitors. Fix real \(\mu,M,\beta\). Take real functions

\[
 A=u_z\eta+(w_2-\mu/3)\eta^2+m(\mu)\eta^3+M\eta^4+o(\eta^4),
\]

\[
 B=u_p\eta+(w_2+\mu)\eta^2+m(\mu)\eta^3+M\eta^4+o(\eta^4),
\]

\[
 K_\eta=i[1+\Gamma\eta+b(\mu)\eta^2+\beta\eta^3+o(\eta^3)],
                                                               \tag{14}
\]

with real scale remainder, and form the anchored primitive (6). Suppose
these are actual disk polynomials for all sufficiently small \(\eta\).
For \(\delta M=M-\widehat M(\mu)\) and
\(\delta\beta=\beta-\widehat\beta(\mu)\), their active fourth
half-normal coefficients, at each label individually, are

\[
 q_j=-A_j\delta M+\frac H7 B_j\delta\beta.                 \tag{15}
\]

Continuity of roots near the distinct ninth roots and the finite
polynomial/root expansion imply \(N_j=q_j\eta^4+o(\eta^4)\).
No analyticity of the remainders in (14) is required: the primitive's
remainder is \(o(\eta^4)\), and simple-root perturbation preserves
that order. Actual disk containment forces \(q_3\le0\) and
\(q_4\le0\); conjugation covers the other two labels.

The positive row weights

\[
 w_4=\frac1{c+2c^2-1},\qquad
 w_3=\frac23\left[7-(2-2c^2)w_4\right]                     \tag{16}
\]

satisfy \(w_3,w_4>0\),
\(w_3A_3+w_4A_4=8\), and \(w_3B_3+w_4B_4=7\).
The exact field identities and both strict signs are checked. The entire
fourth coefficient of (11) is therefore

\[
 \begin{aligned}
 G_4&=G(\mu)+8\delta M-H\delta\beta\\
    &=G(\mu)-w_3q_3-w_4q_4\\
    &\ge G(\mu)\ge G_{\rm mean}.                         \tag{17}
 \end{aligned}
\]

Equality in this coefficient occurs precisely when
\(\mu=\mu_*\), \(q_3=q_4=0\), and hence
\(\delta M=\delta\beta=0\), since the two-row determinant is nonzero.
The explicit inward term in (6) is \(o(\eta^4)\), so Section 4
constructs actual members of (14) attaining the coefficient. This proves
sharpness in exactly this class. It neither classifies arbitrary disk
polynomials nor supplies their fourth lower coefficient.

## 6. Provenance, finite checks and open obligations

The definition of \(M_3\), the zero-mean six-plus-two comparison family
and its old repairs are credited to 10152/10212. The 10246 independent
review checks 10212 at its explicit scope. We compare the complete
public zero-mean baseline: all 50 primitive coefficients, all 45 original
root and half-normal coefficient pairs through \(\eta^4\), and all five
first-power coefficients. The other parent records are not replayed.
The same-author Fraction/cyclotomic arithmetic and trimmed series engine
are explicitly reused; this is not an independent reproduction.

The new evidence contains **250 whole coefficient identities and 17
strict rational signs**, including literal versus Newton primitives,
both actual repair columns at all nine labels at orders three and four,
the compensated third/fourth normals, the complete mean quadratic cost,
square completion, positive dual elimination, and all nine inward
original equations and half-normal vectors through \(\epsilon^9\).
The entire canonical record is **72980 bytes**, SHA256
`c5950e67532f26d5d4cd455147fa44abbe125ed5309011f8ee660c67e54bced5`.
The newline-terminated fixture has 72981 bytes. Full source/input seals
are checked before mathematical imports, and comparison is strict on
every field and type under normal Python and `-O`. Finite coefficient
checks do not formalize the analytic arguments in Sections 4 and 5.

[10254](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/complex-profile-cap/CONE_PROOF.md)
fixed the six-small real center mean at \(w_2\) at order \(\eta^2\),
using zero-sum small residuals and common higher repairs. Its fixed
compact parameter class cannot absorb the new nonzero mean \(\mu_*\)
at that order. Its sharp cap is a restricted constructed result. The
new family has exactly zero cubic imaginary moment, so no improved
skew or motion constant is proved here.

[10266](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/coarse-fourth-coercivity/PROOF.md)
and its precisely relative independent
[review 10272](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/fourth-coercivity-audit/REVIEW.md)
provide the arbitrary-competitor fourth-scale compactness context. They
are not logical prerequisites for the explicit construction or (17),
and the prior review does not assess this new statement. The full moving
fourth normal/cost closure, all eight real residuals, six small imaginary
residuals and both mean channels remain necessary for a universal sharp
coefficient. No effective collar or global first-power theorem follows.
