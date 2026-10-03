# Parity descent on the two-moment-zero original-root angular family

Actual author **six-sendov-2**, role **researcher**, 2026-10-03.
Complete ordinary author proof with exact arithmetic corroboration;
**unformalized and independently unreviewed**. Classical least squares,
Newton identities and Schur complements retain their credit. No historical
priority is claimed. These are real degree-eight original angular slopes
auxiliary to the complex degree-nine first-power Tang--Zhang problem.

## 1. Statements and actual domain

Let the eight original slopes be distinct real numbers, balanced and of
squared norm one. Write their power sums as \(\mu_k\), and suppose
\(\mu_3=\mu_5=0\). Newton identities give the entire coefficient chart

\[
 f(z)=z^8-\tfrac12z^6+2Ez^4+4Gz^2+8Jz+c,\qquad
 h=f'/8=z^7-\tfrac38z^5+Ez^3+Gz+J.                 \tag{1}
\]

The actual \(h\) has seven distinct real critical roots \(\lambda_j\).
Use the actual compression masses and angular quotient

\[
 m_j=-8f(\lambda_j)/h'(\lambda_j)>0,\quad
 \sum m_j=1,\quad \eta=\sum m_j^2,\quad
 D=\mu_4-\tfrac18=\tfrac38-8E>0,\quad C=(1-\eta)/D. \tag{2}
\]

These definitions are credited to the [angular framework7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and [constant-term reduction9271](../constant-term-angular-reduction/PROOF.md).
Let \(g_k=DC[z^k]\) be the original balanced, fixed-norm coefficient
derivatives. The four directions remaining in (1) are \(1,z,z^2,z^4\);
in particular \(\partial_J C=8g_1\), \(\partial_c C=g_0\).

Define \(\bar C(E,G,J)\) by maximizing the quadratic in \(c\) over
**all real constants**, without requiring its primitive to be real-rooted.
Sections2--3 give its exact finite matrix formula and its unique center
\(c_*(E,G,J)\). An actual primitive satisfies \(C\le\bar C\), with equality
exactly when \(g_0=0\), or equivalently \(c=c_*\).

**Theorem A (uniform direction at an actual center).** If \(g_0=0\)
and \(J\ne0\), then

\[
 \boxed{\ Jg_1<-14J^2,\qquad |g_1|>|\mu_7|/4,\qquad
         \operatorname{sign}g_1=\operatorname{sign}\mu_7.\ } \tag{3}
\]

Here \(\mu_7=-56J\). This has no root-gap, approximate stationarity,
large-value or small-variance hypothesis. Changing \(J\) locally toward
zero with \(E,G,c\) fixed is a legal improving direction in the actual
two-moment-zero family. No globally feasible centered path is asserted.

**Theorem B (every-profile algebraic penalty).** For every actual profile
as above with \(J\ne0\),

\[
 \boxed{\ C(f)\le\bar C(E,G,J)
          <\bar C(E,G,0)-56J^2
          =\bar C(E,G,0)-\mu_7^2/56.\ }               \tag{4}
\]

At \(J=0\), the valid comparison is \(C(f)\le\bar C(E,G,0)\).
The value at the right of (4) is explicitly **unconstrained**. It cannot
be replaced by the value or maximum of actual even profiles.

**Theorem C (constrained collision reduction).** No actual profile with
eight distinct original roots and \(\mu_3=\mu_5=0\) is stationary even
on this four-dimensional constrained coefficient chart. Consequently,
every maximum of the continuously extended angular \(C\) over the
balanced norm-one two-moment-zero locus has an original-root collision.
The even stationary exclusion in [9398](../even-angular-exclusion/PROOF.md)
is an explicit input for the last even branch, independently confirmed
by [REVIEW9416](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/even-angular-audit/REVIEW.md).
The compactness consequence uses the continuous extension \(C=16\) on
the uniform orbit from [8753](../angular-three-level-transition/PROOF.md),
confirmed in [REVIEW8806](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/three-level-angular-audit/REVIEW.md).
No claim is made about nonsymmetric collision maxima or a global angular
upper bound.

## 2. Entire moment matrix and constant elimination

Put \(\tau_k=\sum_{j=1}^7\lambda_j^k\), with \(\tau_0=7\). The complete
traces needed below, derived by Newton's recurrence for \(h\), are

\[
\begin{array}{c|l}
k&\tau_k\\\hline
1,3,5&0\\
2&3/4\\
4&9/32-4E\\
6&27/256-9E/4-6G\\
7&-7J\\
8&81/2048-9E/8+4E^2-3G\\
9&-27J/8\\
10&243/16384-135E/256+15E^2/4-45G/32+10EG\\
11&11EJ-99J/64.
\end{array}                                                \tag{5}
\]

The compression resolvent identity is

\[
 \sum_j\frac{m_j}{z-\lambda_j}
 =8\left(z-\frac{f(z)}{h(z)}\right)
 =\frac{z^6-8Ez^4-24Gz^2-56Jz-8c}{h(z)}.              \tag{6}
\]

Thus the six coupling moments \(\nu_k=\sum m_j\lambda_j^k\),
\(0\le k\le5\), and the next moment are

\[
 \nu=(1,0,\tfrac38-8E,0,\tfrac9{64}-4E-24G,-56J)^T,
\quad \nu_6=\tfrac{27}{512}-\tfrac{15}8E+8E^2-10G-8c. \tag{7}
\]

Let \(V_{kj}=\lambda_j^k\), \(0\le k\le5\), and
\(\mathcal M=VV^T=(\tau_{i+k})_{i,k=0}^5\). The seven real distinct
nodes give \(V\) row rank six, so \(\mathcal M\) is positive definite.
As \(c\) varies, the mass vector is affine with nonzero direction
\(\kappa_j=-8/h'(\lambda_j)\). Residue interpolation gives
\(V\kappa=0\). The affine fiber is therefore the entire one-dimensional
solution set of \(Vm=\nu\). Its unique Euclidean least-squares minimum is

\[
 \beta=\mathcal M^{-1}\nu,\quad m_*=V^T\beta,\quad
 R_6=\nu^T\mathcal M^{-1}\nu,
 \qquad \bar C=(1-R_6)/D.                              \tag{8}
\]

This is the credited six-moment fiber mechanism of9271, now specialized
to the entire pencil (1). Comparing its sixth moment with (7) gives

\[
 c_*={1\over8}\left(\tfrac{27}{512}-\tfrac{15}8E+8E^2-10G
                 -\sum_{i=0}^5\beta_i\tau_{i+6}\right). \tag{9}
\]

The actual \(\eta\) is \(R_6+\alpha(c-c_*)^2\),
\(\alpha=\sum\kappa_j^2>0\). Consequently \(g_0=0\) exactly at
the algebraic center. The formula for \(\bar C\) is smooth wherever
\(h\) has seven simple real roots and \(D>0\). For each
\(\theta\in\{E,G,J\}\), its entire reduced gradient is

\[
 (R_6)_\theta=2\beta^T\nu_\theta-\beta^T\mathcal M_\theta\beta,
\quad
 \bar C_E=(8\bar C-(R_6)_E)/D,\quad
 \bar C_G=-(R_6)_G/D,\quad \bar C_J=-(R_6)_J/D.         \tag{10}
\]

All moments and every matrix entry in (10) are specified in (5)--(7).
At an **actual** center, differentiating \(C(E,G,J,c_*(E,G,J))\) gives
these actual derivatives by the chain rule, because \(C_c=0\).
We never infer positivity of \(m_*\) from its least-squares definition.

## 3. A positive Schur derivative with a uniform budget

Order the six powers as \((0,2,4;1,3,5)\). Then

\[
 \mathcal M=\begin{pmatrix}A&JU\\JU^T&B\end{pmatrix},\quad
 \nu=\binom u{Jv},\qquad
 U=\begin{pmatrix}0&0&0\\0&0&-7\\0&-7&-27/8\end{pmatrix},
\]
\[
 A=\begin{pmatrix}7&\tau_2&\tau_4\\\tau_2&\tau_4&\tau_6\\
                         \tau_4&\tau_6&\tau_8\end{pmatrix},\quad
 B=\begin{pmatrix}\tau_2&\tau_4&\tau_6\\\tau_4&\tau_6&\tau_8\\
                         \tau_6&\tau_8&\tau_{10}\end{pmatrix},
\quad u=\begin{pmatrix}1\\3/8-8E\\9/64-4E-24G\end{pmatrix},
\quad v=\begin{pmatrix}0\\0\\-56\end{pmatrix}.           \tag{11}
\]

The displayed \(A,B,U,u,v\) are independent of \(J\). Put

\[
 y=A^{-1}u,\quad w=v-U^Ty,\quad Q=U^TA^{-1}U\succeq0,
\quad x=J^2,\quad S=B-xQ\succ0.
\]

Schur elimination in (8), without discarding any moment row, gives

\[
 R_6=u^TA^{-1}u+xw^TS^{-1}w,\qquad
 {dR_6\over dx}=w^TS^{-1}BS^{-1}w=:H.                 \tag{12}
\]

The derivative identity follows from \((S^{-1})_x=S^{-1}QS^{-1}\)
and \(B=S+xQ\). In particular
\(H\ge w^TS^{-1}w\ge w^TB^{-1}w\).
Nonvanishing already follows simply: \(w=0\) would imply
\(y_2=0,y_1=8,y_0=-5/7\) from (11) and the first normal equation.
The second normal equation would then force \(E=25/448\), giving
\(D=-1/14\), outside the stated domain.

For a quantitative bound write

\[
 a=3/4,\ b=\tau_4,\ t=\tau_6,\quad
 k=b-a^2/7>0,\quad \ell=t-ab/7,
\quad q_1=\ell/7-27k/392,\ q_2=k/7.
\]

Eliminate \(y_0\) from the first two equations \(Ay=u\). Since
\(w_1=7y_2\) and \(w_2=-56+7y_1+(27/8)y_2\), the entire mismatch is

\[
 \boxed{\ q_1w_1+q_2w_2=-3(D+1/14).\ }               \tag{13}
\]

The real traces with \(\tau_2=3/4\) imply
\(0\le b\le9/16\), \(0\le t\le27/64\), and hence

\[
 0<k\le27/56,\quad |\ell|\le27/56,\quad
 |q_1|\le2241/21952<3/28,\quad
 |q_2|\le27/392<1/14,
\]
\[
 q_1^2+q_2^2<13/784<1/49.                              \tag{14}
\]

Here \(k>0\) follows from a principal minor of the positive definite
matrix \(A\). Cauchy's inequality in (13)--(14) gives
\(\|w\|^2>441(D+1/14)^2\).
Also \(|\lambda_j|^2\le\tau_2<1\), so

\[
 \lambda_{\max}(B)\le\operatorname{tr}B
    =\tau_2+\tau_6+\tau_{10}\le3\tau_2=9/4.
\]

Combining this with (12) yields the strict universal bound

\[
 \boxed{\ H>196(D+1/14)^2.\ }                          \tag{15}
\]

Finally \(\bar C_J=-2JH/D\). At an actual center this gives

\[
 Jg_1=-J^2H/(4D)<-49J^2(D+1/14)^2/D\le-14J^2,
\]

where \((D+1/14)^2/D\ge4/14\) for every \(D>0\).
Newton's identity \(\mu_7=-56J\) now proves all of (3).
The strictness in (14)--(15) is retained even when the final scalar
inequality has equality at \(D=1/14\).

## 4. Horizontal-level continuation and integrated penalty

Fix \(E,G\) and write \(h_J=k_0+J\), where \(k_0\) is odd.
If \(h_J\) has seven simple real zeros, Rolle gives six simple real
derivative zeros, independent of \(J\), in three opposite pairs.
At every local maximum, \(h_J>0\); at every local minimum, \(h_J<0\).
The opposite critical value of the odd \(k_0\) reverses sign, and its
type reverses. Thus a local maximum of \(k_0\) exceeds \(|J|\), while
every local minimum is below \(-|J|\).
For every \(|J'|\le|J|\) the same strict critical-value signs hold for
\(h_{J'}\). Its seven monotone intervals, including both outer ones,
each contain one simple zero. This proves the entire closed segment
of simple real critical spectra, including \(J'=0\).

Consequently (15) holds along that segment, and for \(J'>0\),
\(\bar C_{J'}<-112J'\). Reflection, or directly (12), makes \(\bar C\)
even in \(J\). Integrating from zero to \(|J|\) proves
\(\bar C(E,G,0)-\bar C(E,G,J)>56J^2\). The actual inequality
\(C\le\bar C\) proves (4). This continues **critical spectra** and
the unconstrained algebraic formula, without asserting that
\(c_*(E,G,J')\) gives eight real originals anywhere along the path.

## 5. Constrained extrema and the feasibility obstruction

The root-to-coefficient Jacobian at eight distinct originals is a
nonzero Vandermonde. Fixing the leading coefficients to \(1,0,-1/2\)
fixes balance and squared norm; setting the \(z^5,z^3\) coefficients
to zero is exactly \(\mu_3=\mu_5=0\). Thus the four coefficients
\(E,G,J,c\) form an open local chart for this constrained family.
All sufficiently small two-sided coefficient variations retain eight
distinct real original roots. In particular the improving direction
in Theorem A is legal locally.

A stationary point on this chart must have \(g_0=0,g_1=0\).
Theorem A forces \(J=0\). Its primitive is then even, and the three
remaining derivatives in \(E,G,c\) would give stationarity in the
entire even chart. The credited no-even-stationarity theorem9398
excludes it. This proves the first assertion of Theorem C.

The balanced norm-one zero-moment locus is closed and compact. The
credited continuous extension8753 makes \(C\) attain a maximum there.
An all-distinct maximum would be stationary in the open chart just
described, which is impossible. At \(D=0\), the only balanced profile
is the uniform four-plus/four-minus orbit, which already has collisions.
Every maximizing profile therefore has an original collision. No
classification of these collision profiles follows from this argument.

The unconstrained even center can fail feasibility **within this exact
two-moment-zero family**. For example

\[
 f_0(z)=\prod_{r=1}^4(z^2-r/20)
 =z^8-\tfrac12z^6+\tfrac7{80}z^4-\tfrac1{160}z^2+\tfrac3{20000}
\]

has eight distinct real originals, \(E=7/160,G=-1/640,J=0,D=1/40\).
Formula (9) gives \(c_*=1/7040\). Its centered primitive has exactly
**four** real zeros. Indeed, putting \(x=z^2\), \(y=x-1/8\), its square
polynomial is

\[
 y^4-y^2/160+9/2560000-7/880000.
\]

The constant is negative, so the quadratic in \(y^2\) has one positive
and one negative root. The positive root is smaller than \(1/64\),
because the quadratic is positive at \(1/64\). Hence its two real
\(x\) roots lie strictly between zero and \(1/4\), yielding precisely
four real \(z\) roots. The other four are nonreal. This exact obstruction
prevents replacing \(\bar C(E,G,0)\) by an actual symmetric bound.

## 6. Reproduction, attribution and remaining frontier

[verify.py](verify.py) recomputes every coefficient of the twelve Newton
traces, seven coupling moments, whole six-by-six Gram and all four
coefficient derivative matrices. It checks every closed rational budget
in (14)--(15), the exceptional \(E,D\), and the seventh-moment conversion.
An independent dual-number calculation in \(\mathbb Q[\epsilon]/(\epsilon^2)[z]/h\)
computes the whole interpolant and square-mass trace. All four **moving-node**
derivatives agree with (10) at four exact centered controls; three have
eight real originals, and the fourth is the explicit infeasible center
above. Exact Sturm counts retain original feasibility and critical reality.
The nonzero signed controls have opposite full \(J\) gradients, and
frozen-node differentiation disagrees. All nine semantic damages and
the entire external [record](expected.json) are checked using explicit
exceptions, including under Python optimization. These finite controls
are corroboration, not an enumeration or independent peer review.

Run from the repository root using Python3.10+ standard library:

    python3 -I -B round-two/six-sendov-2/two-moment-parity-descent/verify.py
    python3 -I -B -O round-two/six-sendov-2/two-moment-parity-descent/verify.py

All six native numerical thread variables should be set to one.
The code uses no solver, floating predicates or large external certificate.
The ordinary proof boundaries are the real Gram/Schur positivity,
least-squares and derivative bridges, hyperbolicity interval, local chart,
and the expressly credited even/continuity results. No formalization is
claimed. Source and [literature/dependency provenance](LITERATURE.md) are
compact and reproducible; no historical priority or optimal constant is
claimed.

The new frontier is the **actual nonsymmetric original-collision boundary
on this two-moment-zero locus**, or a controlled perturbation away from
the locus and exact centering. This proof gives neither a separation-free
approximate full-gradient estimate nor a global angular value, physical
disk deformation, or unrestricted complex first-power theorem.
