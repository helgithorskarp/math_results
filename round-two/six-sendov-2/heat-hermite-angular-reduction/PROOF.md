# Heat regularization and four-/six-coefficient angular tests

Actual author **six-sendov-2**, role **researcher**, 2026-10-05.
Complete ordinary derivation; **unformalized and independently unreviewed**.
Source contains the complete ordinary reduction and finite exact arithmetic
corroboration. A finite sign decision, numerical gap, numerical collar, or
global complex FIRST proof is not supplied.

## 1. Definitions and exact reduction

Use the full angular convention7432. For a balanced unit vector
\(x\in\mathbb R^8\), let \(\mu_k=\sum_i x_i^k\),
\(P=I-\mathbf1\mathbf1^T/8\), and
\(H=(P\operatorname{diag}(x)P)|_{\mathbf1^\perp}\).
At each **distinct** compression eigenvalue let
\(m_\lambda=\|\Pi_\lambda x\|^2\), and set
\[
\eta=\sum_\lambda m_\lambda^2,\qquad
D=\mu_4-1/8,\qquad C=(1-\eta)/D\quad(D>0).
\]
The previously proved [full-sphere continuous extension8753](../angular-three-level-transition/PROOF.md),
independently audited in [8806](../../six-reviewer-1/three-level-angular-audit/REVIEW.md), is
\(\widetilde C=16\) at the uniform four-positive/four-negative profiles,
and \(\widetilde C=C\) elsewhere. That continuity is an explicit input
only for passing an angular bound to collision limits.

Put \(u=\mu_3,v=\mu_5\). Newton identities give the complete monic chart
\[
f(z)=z^8-\tfrac12z^6-\tfrac u3z^5+2Ez^4
       +(\tfrac u6-\tfrac v5)z^3+4Gz^2+8Jz+c.       \tag{1}
\]
Whenever this polynomial has eight real roots, their ordered vector is
balanced, has norm one, and has exactly the moments \(u,v\).
Conversely every balanced unit root vector gives exactly one such chart.
Here \(D=3/8-8E\). Let \(\mathcal H_f=(\mu_{i+j})_{0\le i,j\le7}\),
where all moments through14 are obtained by the Newton recurrence of(1).
Let \(L_k\) be its leading principal determinant of order \(k\),
\(1\le k\le8\).

Set
\[
h=f'/8,
\quad r=8zh-8f
=z^6+uz^5-8Ez^4+(v-5u/6)z^3-24Gz^2-56Jz-8c.    \tag{2}
\]
For polynomials \(a,b\) of degrees at most7, define the fixed7-by7
Bezout matrix by
\[
\frac{a(X)b(Y)-a(Y)b(X)}{X-Y}
 =\sum_{i,j=0}^6 B(a,b)_{ij}X^iY^j.
\]
Write
\[
B_0=B(h,h'),\quad B_r=B(h,r),\quad
\Delta=\det B_0,\quad N=[t^2]\det(B_0+tB_r).       \tag{3}
\]
The letter \(t\) in(3) is a **formal coefficient-extraction variable**,
not another unknown in a real-existential test. For a fully explicit
division-free construction, \(N\) is the sum of21 determinants: replace
exactly two columns of \(B_0\) by the corresponding columns of \(B_r\),
and sum over the21 unordered pairs. Equations(1)--(3) and the Newton
recurrence therefore specify rational polynomials in the six coefficients;
they do not require numerical roots or an expanded discriminant table.

**Reduction theorem.** For every rational \(T\ge16\) and
\(\varepsilon\ge0\), the following assertions are equivalent:

1. Every balanced unit original vector with
   \(\mu_3^2+\mu_5^2\le\varepsilon\), including every original and
   compression multiplicity, has \(\widetilde C\le T\).
2. There is **no** real tuple \((E,G,J,c,u,v)\) satisfying
   \[
   L_1>0,\ldots,L_8>0,\quad D>0,\quad\Delta>0,
   \quad u^2+v^2\le\varepsilon,
   \quad TD\Delta-2N<0.                             \tag{4}
   \]

For the exact locus \(\mu_3=\mu_5=0\), substitute \(u=v=0\) in
every coefficient of(4). The resulting test has **four real unknowns**
\((E,G,J,c)\); the collar test has **six**. In particular a rational
\(0<q\le1/2\) is a valid entire exact-locus gap \(q\) precisely when
the four-variable strict counterexample test
\[
(47-2q)D\Delta-4N<0                              \tag{5}
\]
with the same positive guards has no real solution. A collar for the
threshold \(47/2-q/2\) uses the six-variable test
\((47-q)D\Delta-4N<0\), together with \(u^2+v^2\le\varepsilon\).
These are necessary-and-sufficient tests on **actual real originals**,
not independent critical-root or nonnegative-weight relaxations.

## 2. Backward heat preserves and strictly separates real roots

The following heat-preserver fact is classical; its use here is not a
priority claim. We include an elementary proof of the needed strict form.
For a monic real-rooted polynomial \(p\) of fixed degree \(n\), define
\[
p_t=e^{-t\partial_z^2}p
=\sum_{j=0}^{\lfloor n/2\rfloor}\frac{(-t)^j}{j!}p^{(2j)},
\quad t\ge0.                                      \tag{6}
\]

First, \(p+a p'\) is real-rooted for every real \(a\). For simple roots,
\(p'/p=\sum_i1/(z-x_i)\) decreases strictly in each gap. The equation
\(1+a p'/p=0\) has one root in each gap and one in an exterior interval,
accounting for the full degree. For \(a=0\) the assertion is immediate.
Approximate a multiple real root multiset by distinct real roots to obtain
the general assertion; monic fixed-degree real-rooted polynomials are
closed under coefficient limits.

For positive integers \(m\),
\[
(1-t\partial_z^2/m)^m
=[(1-\sqrt{t/m}\,\partial_z)(1+\sqrt{t/m}\,\partial_z)]^m.
\]
Both factors preserve real-rootedness. As \(m\to\infty\), the resulting
monic polynomials converge coefficientwise to(6), because derivatives
above the fixed degree vanish. Thus \(p_t\) is real-rooted for all \(t\ge0\).

It is in fact **simple** for every \(t>0\). Suppose \(p_{t_0}\) has a root
\(\alpha\) of multiplicity \(m\ge2\), and expand
\(p_{t_0}(\alpha+w)=\sum_{k=m}^n a_kw^k\), \(a_m\ne0\).
For \(0<s<t_0\), the semigroup identity gives
\(p_{t_0-s}=e^{s\partial_z^2}p_{t_0}\), still real-rooted. After setting
\(w=\sqrt{s}\,y\) and dividing by \(a_m s^{m/2}\), it converges uniformly
on compact complex sets to
\[
Q_m(y)=e^{\partial_y^2}y^m
=\sum_{j=0}^{\lfloor m/2\rfloor}
  \frac{m!}{j!(m-2j)!}y^{m-2j}.                    \tag{7}
\]
Indeed the other terms are
\((a_k/a_m)s^{(k-m)/2}e^{\partial_y^2}y^k\), which tend to zero.
The monic \(Q_m\) has zero coefficient of \(y^{m-1}\) and positive
coefficient \(m(m-1)\) of \(y^{m-2}\). Hence its root square sum is
\(-2m(m-1)<0\), so at least one root is nonreal. Choose a small disk about
such a root, disjoint from the real line and with a zero-free boundary.
Uniform convergence and Rouché's theorem force a nonreal root of the
scaled \(p_{t_0-s}\) for small \(s\), a contradiction. This argument pays
the possible degree drop in the scaled limit and applies to every
initial root multiplicity.

## 3. Normalization preserves the exact locus and improves residuals

Apply(6) to(1). The complete coefficient identity is
\[
\begin{aligned}
f_t(z)={}&z^8-(1/2+56t)z^6-(u/3)z^5
 +(2E+15t+840t^2)z^4\\
&+(u/6-v/5+20ut/3)z^3
 +(4G-24Et-90t^2-3360t^3)z^2\\
&+(8J-ut+6vt/5-20ut^2)z
 +c-8Gt+24Et^2+60t^3+1680t^4.                  \tag{8}
\end{aligned}
\]
Let \(A=1+112t\), and use the normalized polynomial
\(\widehat f_t(z)=A^{-4}f_t(\sqrt A\,z)\).
Its roots remain real and, for \(t>0\), simple. Their square sum is one
because the unnormalized square sum is \(A\); their mean remains zero.
Its chart coordinates are
\[
\begin{aligned}
E_t&=(E+15t/2+420t^2)/A^2,\\
G_t&=(G-6Et-45t^2/2-840t^3)/A^3,\\
J_t&=(J-ut/8+3vt/20-5ut^2/2)/A^{7/2},\\
c_t&=(c-8Gt+24Et^2+60t^3+1680t^4)/A^4,\\
u_t&=u/A^{3/2},\qquad v_t=(v+60tu)/A^{5/2}.       \tag{9}
\end{aligned}
\]
The last two identities also follow directly from Newton identities:
the unnormalized moments are \(\mu_3(t)=u\) and \(\mu_5(t)=v+60tu\).
Consequently every normalized exact-locus profile is a limit of
simple real originals **within that same exact locus**.

There is a stronger collar statement. Put \(w=v+60tu\). Direct
differentiation gives
\[
\frac{d}{dt}(u_t^2+v_t^2)
=-\frac{336A^2u^2-120Auw+560w^2}{A^6}
=-\frac{60(Au-w)^2+276A^2u^2+500w^2}{A^6}.      \tag{10}
\]
It vanishes identically if \(u=v=0\), and is strictly negative at every
\(t\ge0\) otherwise. Thus each **closed** residual collar is preserved
by the normalized flow. This includes its residual-equality boundary:
no interior-only density assumption is used in(4).

The ordered normalized roots tend to the ordered original roots as
\(t\downarrow0\). For example, disjoint small disks about the distinct
limiting original levels and fixed-degree coefficient convergence give
exactly the appropriate number of roots near each level; all are real.
Thus all collision patterns and the uniform endpoints are approached
by legal simple-root vectors within each collar.

## 4. The Hermite matrix licenses the original polynomial

We prove
\[
L_1>0,\ldots,L_8>0
\quad\Longleftrightarrow\quad
f\text{ has eight distinct real roots}.             \tag{11}
\]
For real roots, the quadratic form of \(\mathcal H_f\) at the coefficient
vector of \(a(z)\), \(\deg a\le7\), is \(\sum_i a(x_i)^2\).
For distinct real roots this is positive for every nonzero \(a\), by
Vandermonde invertibility. Conversely a repeated root makes the complex
Vandermonde factorization have rank less than8, so positive definiteness
is impossible. If the eight roots are distinct but some conjugate pair
is nonreal, prescribe the values \(i,-i\) on that pair and zero on all
other roots. Unique degree-at-most7 interpolation has real coefficients:
the assigned values respect conjugation. Its quadratic form is \(-2\),
contradicting positive definiteness. Finally Sylvester's criterion for
the real symmetric \(\mathcal H_f\) identifies positive definiteness
with the eight strict leading determinant inequalities.

Only **positive definite** leading-minor tests are used. Nonnegative
leading minors alone would not license positive semidefiniteness. A
positive discriminant of \(h\), or even seven simple real critical roots,
does not license eight real original roots; shifting \(c\) leaves \(h\)
unchanged and can destroy original real-rootedness. Equation(11) is the
original-root feasibility constraint in(4).

## 5. Full masses and the division-free angular numerator

For simple real originals, \(h=f'/8\) has seven simple strictly
interlacing real roots, the actual compression eigenvalues. The
cofactor identity for \(e=\mathbf1/\sqrt8\) gives
\(\det(zI-H)=f'(z)/8\): the \(e,e\) inverse entry of
\(zI-\operatorname{diag}(x)\) is \(f'/(8f)\).
The Schur complement in the decomposition \(e\oplus e^\perp\), with
coupling \(x/\sqrt8\), gives the rational identity
\[
x^T(zI-H)^{-1}x=8z-8f/h=r/h.                     \tag{12}
\]
It first holds away from the roots and then as a rational identity.
Taking its residues at the seven simple compression eigenvalues yields
\(m_i=r(\lambda_i)/h'(\lambda_i)\). These are actual nonnegative
spectral projection masses with \(\sum_i m_i=1\); no unrelated mass
variables are chosen.

Let \(V_{ij}=\lambda_i^j\), \(0\le j\le6\). Evaluation of the Bezout
kernel at the roots of \(h\) gives
\[
V B(h,g)V^T=\operatorname{diag}(h'(\lambda_i)g(\lambda_i)).
\]
For \(g=h'\), the diagonal entries are positive squares and
\(\Delta=\det B_0=\prod_{i<j}(\lambda_i-\lambda_j)^2>0\).
Applying the same identity to \(g=h'+tr\) gives
\[
\det(B_0+tB_r)=\Delta\prod_{i=1}^7(1+t m_i).
\]
Hence
\[
N=\Delta\sum_{i<j}m_i m_j
=\tfrac\Delta2(1-\eta),\qquad C=2N/(D\Delta).     \tag{13}
\]
Simple originals imply \(D>0\): its zero set on the balanced unit sphere
consists exactly of the uniform repeated profiles. The explicit guards
\(D>0,\Delta>0\) nevertheless remain in(4), making every denominator
clearing legal. Relations(11)--(13) prove(4) exactly on the simple locus.

## 6. Collision completion and finite-algorithm scope

If(4) has a solution, (11) supplies an actual simple real original
vector, (12)--(13) supply its actual angular value, and it violates the
proposed bound. In the other direction, suppose any collar vector has
\(\widetilde C>T\). Since \(T\ge16\), it is not uniform. By(9)--(10)
the normalized heat roots remain in the same closed collar and are
simple for every positive time. By imported continuity8753/8806 their
values converge to that strict violating value, so sufficiently small
positive heat time gives a solution of(4). This establishes both
directions through every original and compression collision.

No formula for a collision quotient is inferred by cancelling a zero
discriminant. Collisions are handled by legal density plus continuity;
the separate uniform value16 is why the threshold guard matters.

Conditional on the source-published, independently unreviewed global
exact-locus theorem at source5e8b7f46665b6cbaa9e794b9197bb5a78181a67c,
some dyadic \(q=2^{-k}\), \(k\ge1\), makes(5) infeasible. After one
such gap is **actually certified**, some dyadic \(\varepsilon>0\) makes
the six-variable collar test infeasible. Real-closed-field decision
provides a terminating-in-principle procedure; no decision program,
infeasibility certificate, numerical value, or feasible runtime here is
asserted. The mathematical equivalence(4) itself does not depend on
that global theorem or its still-pending graph transaction.

The [earlier published four-coefficient chart and resolvent10105](../two-moment-parity-descent/PROOF.md)
are credited prior work. The previous private23-variable spectral-moment representation remains
a valid broader encoding, but its spectral and weight variables and
64 ordered spectral partitions are unnecessary for these threshold
tests. The present mechanism replaces them with original-root Hermite
feasibility and simple-locus density.

## 7. Additional structure and limits of the heat path

The normalized polynomials tend, as \(t\to\infty\), to
\[
f_*(z)=e^{-\partial_z^2/112}z^8.
\]
This polynomial has eight simple real roots and is normalized. It is
fixed by(9): \((1/112+t)/(1+112t)=1/112\). The convergence is uniform
on each compact coefficient set, directly from(8)--(9). Reparameterize
\(t=s/(112(1-s))\), \(0\le s<1\), and assign \(f_*\) at \(s=1\).
This gives a strong deformation contraction of the compact actual
coefficient locus, and of each closed residual collar, to \(f_*\).
The same holds for the **ordered** root locus, by root continuity. It
does not identify the different labelled permutations of a vector.

There is **no angular monotonicity assertion**. At the exact-locus
profile \((1/\sqrt2,-1/\sqrt2,0,0,0,0,0,0)\), (12) gives two active
masses1/2, \(D=3/8\), and \(C=4/3\). At the fixed Hermite profile,
the recurrence \(f_*=zh-14(1/112)H_6\), \(h'=7H_6\), gives seven
masses1/7, \(D=3/28\), and \(C=8\). The uniform exact-locus endpoint
has the imported value16 and also flows toward8. Thus the angular
value is neither globally nonincreasing nor globally nondecreasing
along this exact-locus flow. In particular contractibility does not
give a numerical maximum or stability gap.

All vector profiles here are real angular profiles. The heat path is
not a claimed physical deformation of the complex degree-nine original
polynomial in the closed unit disk. The unrestricted complex first-power
Tang--Zhang endpoint remains a separate frontier.

## 8. Exact arithmetic corroboration and trust boundary

[check.py](check.py) independently specializes the entire six-coefficient
Newton and Hermite matrices to actual rational original vectors, and checks
their direct moment sums through14. It verifies every coefficient of(8),
the unnormalized odd moments, the complete residual square identity(10),
and every entry of the two Bezout matrices via their defining kernels.
At five rational coefficient fixtures, all eight coefficients of the
determinant polynomial agree with the characteristic polynomial of exact
residue multiplication in \(\mathbb Q[z]/h\). Original feasibility is
retained by all eight strict Hermite determinants. Two negative controls
exclude an infeasible constant shift with unchanged real critical roots,
and the singular uniform original polynomial; its normalized heat
regularization is a separate positive fixture.

These finite exact checks corroborate identities and interpretations;
they are not an enumeration, a real-feasibility decision, an independent
review, or a formalization of the ordinary heat/root-density/continuity
bridges. An unrestricted multivariate determinant expansion was interrupted
at the existing45-second local limit and is **not evidence of any sign
claim**. It is unnecessary for the division-free determinant specification
(3). [README.md](README.md) gives reproduction and the whole-record hash;
[LITERATURE.md](LITERATURE.md) and [DEPENDENCIES.json](DEPENDENCIES.json)
record credited primary and graph sources. No private ledger, ancestor
certificate corpus, or reviewer executable is an arithmetic input.
