# The sharp raw stability coefficient has an unattained endpoint

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Status: author-checked ordinary analytic lemma with a finite exact arithmetic
certificate. This new endpoint exclusion has not been independently reviewed
or formalized. Its analytic minimizer and chart are attributed reviewed inputs.

## Statement and normalization

Let p be monic of degree9 with all original roots in the closed unit disk
and marked root a=1-eta, where eta>0 is sufficiently small. Its eight critical
points count with multiplicity; write

\[
F(p)=\sum_{j=1}^8|a-\zeta_j|^{-1},\qquad
\zeta_j=\eta u_j+i\sqrt\eta h_j.
\]

A zero denominator means infinity. Let m(eta) be the **exact** all-complex
radiuswise minimum and p_eta its unique monic minimizer from
[8921](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/analytic-boundary/PROOF.md),
independently confirmed in
[8955](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/analytic-minimizer-audit/REVIEW.md).
The two large imaginary criticals have labels1,2; the raw free coordinates are
z=(h3,...,h8,u3,...,u8). Its minimum has
z_eta=(0^6,x_min(eta)^6), with x_min analytic and x_min(0)=u_z.
This is the literal twelve-coordinate Euclidean norm, not the norm of all
sixteen normalized critical coordinates. For the four active original roots
near exp(plus/minus2pi i k/9), k=3,4, let their half-radials be
a_k^s=(|r_k^s|^2-1)/2, s=plus/minus.

**Endpoint exclusion.** Fix any real q>=3 and A>0. For every sufficiently
small eta>0 there is a real-coefficient disk-rooted polynomial p=p(eta)
with all nine original roots simple, all four active half-radials exactly zero,
and

\[
0<F(p)-m(\eta)<A\eta^q,
\qquad
F(p)-m(\eta)<\frac12\eta^2\|z-z_\eta\|^2.                 \tag{1}
\]

Consequently coefficient1/2 cannot hold uniformly on any positive exact
excess-budget class F<=m+Aeta^q, including with any additional fixed radial
weights: the witness has zero radial slack. Together with8955's theorem for
every fixed0<kappa<1/2, the supremum of uniform raw quadratic coefficients
on such collars is1/2 and is not attained. Each smaller coefficient may have
its own collar. No explicit collar width, interior-radius classification,
or resolution of the full first-power conjecture is asserted.

## Attributed constants and limiting cost

Put c=cos(pi/9), the unique root of8c^3-6c-1 in(3/4,1), and define

\[
\begin{gathered}
d=2c^2-1,\quad v=2d^2-1,\quad y_0={1\over3(1+c)},\quad
H_0=14y_0,\quad U_0=-8(2/3-y_0),\quad \rho=(c-5)/3,\\
u_z=(U_0+\rho H_0)/8,\quad u_p=(U_0-6u_z)/2,\quad
B_*={2311\over108}+{4934\over27}c-{1976\over9}c^2,\quad C=8/3+y_0,\\
w_4=(c+d)^{-1},\quad w_3={2\over3}[7-(1-d)w_4],\\
K_0=-2609/405-(2000/81)c+(12964/405)c^2,\quad
\sigma=3/8-[(3/2)w_3+(1-v)w_4]/20.
\end{gathered}
\]

The reviewed zero-slack chart is jointly real analytic on a fixed parameter
neighborhood including eta=0. It retains z literally; its four normal variables
are determined by the four actual original-root radials. On zero slack,

\[
\mathcal F(\eta,0,0,z)=8+C\eta+\eta^2G(\eta,z),\quad
G(0,z)=K_0+\tfrac12\|u\|^2+\rho\sum h_j^2u_j+\sigma\sum h_j^4. \tag{2}
\]

The concentration, global comparison and uniform all-complex coverage are
inherited from8921/8955, within their explicitly reviewed7190/8619/8684
premises. They are not re-proved by this finite certificate. Their conclusion
that m is the exact minimum, and their literal zero-slack chart, are essential.
The centered-real split and limiting coefficient1/2 already occur in
[8883](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/fourth-boundary-audit/REVIEW.md)
and8955. The new result is the negative first curvature correction and
nonattainment of the uniform endpoint left open in8955.

## An exact centered-real disk-root family

For common real coordinate x near u_z and small real delta, set

\[
h_3=\cdots=h_8=0,\qquad
(u_3,\ldots,u_8)=(x+\delta,x-\delta,x,x,x,x).                \tag{3}
\]

Apply the reviewed zero-slack inverse with all four actual radials zero.
Conjugation followed by swapping the two large critical labels fixes the
free coordinates in(3). Uniqueness of that inverse forces the large pair
to have opposite imaginary coordinates and equal real coordinates. Thus
for jointly analytic Y(eta,x,delta)>0 and y(eta,x,delta), the exact polynomial is

\[
\begin{aligned}
p'(z)&=9\prod_{j=3}^8(z-\eta u_j)[(z-\eta y)^2+\eta Y],\\
p(z)&=\int_{1-\eta}^zp'(w)\,dw.                            \tag{4}
\end{aligned}
\]

Here Y is the **squared** normalized imaginary opening. At eta=0,
y=(U0-6x)/2 and Y=H0/2; these values do not depend on delta. The exact
polynomial is real and its coefficients are analytic in eta,x,delta although
its large critical points contain sqrt(eta). All four active original roots
are exactly on the unit circle. The other four unmarked original roots have
strictly negative first radial slopes on a fixed neighborhood, and the marked
root is exactly1-eta. Uniform continuity of the reviewed root maps puts all
five of these roots strictly inside for small positive eta. All nine original
roots remain simple and exhaust the degree9 polynomial. Critical multiplicity
is allowed: four of the small criticals in(3) still coincide.

For clarity, the computation's two unit-circle equations describe exactly this
family. If p=sum p_j z^j, let T_j,U_j be the Chebyshev polynomials and define

\[
I(t)=\sum_{j=1}^9p_jU_{j-1}(t),\qquad R(t)=\sum_{j=0}^9p_jT_j(t).
\]

At t3=-1/2,t4=-c, I_t=-9/(1-t_k^2) is nonzero. Hence the phase equation
I(t_k)=0 solves an analytic t_k(eta,x,y,Y,delta). Along that phase, R vanishes
at eta=0 and -R/(9eta) is analytic. Its leading derivative in(y,Y) has rows
(-A_k/4,B_k/7), with

\[
(A_3,B_3)=(3/2,3/2),\quad (A_4,B_4)=(1+c,1-d),\quad
\det={3(c+d)\over56}>0.                                   \tag{5}
\]

The analytic implicit function theorem therefore solves the two remaining
unit-root constraints uniquely. Because sin(theta_k) is nonzero and t_k stays
inside(-1,1), I=R=0 makes exp(plus/minus i arccos t_k) actual roots of p.
The resulting family has the same free coordinates and zero radials as the
reviewed chart, so uniqueness identifies the two constructions. Formula(5)
is also the normal system reproduced in
[8991](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/reduced-continuation/PROOF.md);
its C5 is not a premise here.

## Exact first weak-curvature correction

Write Psi(eta,x,delta) for the reciprocal objective of(4). Every real critical
denominator1-eta(1+u_j) is positive near eta=0, and the pair has distance
square (1-eta(1+y))^2+etaY near1. Thus Psi is jointly real analytic.
Swapping the first two small criticals sends delta to-delta without changing
p, so Psi is even in delta. In(2), h1=-h2, h1^2=h2^2=H0/2, all other h=0,
and the two large u values are(U0-6x)/2. Substitution gives the **complete**
second coefficient, for every nearby x and delta,

\[
[\eta^0]\Psi=8,\quad [\eta^1]\Psi=C,\quad
[\eta^2]\Psi=B_*+12(x-u_z)^2+\delta^2.                    \tag{6}
\]

In particular the centered-split coefficient is1 for every common x;
there are no higher delta terms in this second coefficient.

The exact joint computation in Q[c]/(8c^3-6c-1), with eta through degree3
and delta through degree2, yields

\[
\ell=[\eta^3\delta^2]\Psi(\eta,u_z,\delta)
=-{4441\over540}+{7046\over135}c-{2288\over45}c^2<0.        \tag{7}
\]

[verify.py](verify.py) multiplies and integrates all eight derivative factors,
anchors the marked root, and solves the two phase and two real equations
coefficient by coefficient. Every joint equation coefficient is checked.
The first two objective coefficients and the known cubic value at delta0 are
reproduced as validation. A separate actual complex residual-root expansion,
without Chebyshev equations, verifies the solved phase abscissas and every
actual half-radial coefficient through eta3/delta2 for both active pairs.
Their nonzero phase/normal Jacobians justify uniqueness of these finite jets.
The negative sign follows from rational bisection of the unique root in(3/4,1):

\[
-4.075854243<\ell<-4.075854241.
\]

These displayed decimals stand for exact rational endpoints with denominator
10^9. They are not floating-point proof inputs. The full rational bracket
and coefficients are frozen in[expected.json](expected.json).

## Analytic division and transport to the exact minimum

Evenness implies Psi(eta,x,delta)-Psi(eta,x,0) is divisible by delta squared
in the ring of convergent real power series, with quotient analytic in
eta,x,delta squared. The constant and first eta coefficients in(6) vanish
in the difference; divide by eta squared. Its coefficient at eta0 is
identically1, again by(6). Convergent Taylor expansion therefore gives

\[
\Psi(\eta,x,\delta)-\Psi(\eta,x,0)
=\eta^2\delta^2[1+\eta L(x,\delta^2)+\eta^2Q(\eta,x,\delta^2)],\tag{8}
\]

where L and Q are analytic and bounded on a smaller fixed product
neighborhood, and L(u_z,0)=ell. This analytic division is an ordinary proof,
not a conclusion drawn from the truncated computation alone.

At x=x_min(eta), the delta0 family is exactly p_eta by chart uniqueness.
Consequently Psi(eta,x_min,0)=m(eta), with **no truncated-minimum error**.
Analyticity gives x_min-u_z=O(eta) and
L(x_min,delta squared)=ell+O(eta)+O(delta squared), uniformly on that
neighborhood. Thus the exact split objective satisfies

\[
F(p)-m(\eta)=\eta^2\delta^2
             [1+\ell\eta+O(\eta^2)+O(\eta\delta^2)].       \tag{9}
\]

The literal free-coordinate distance in(3) at x=x_min is exactly2delta squared.
Fix q>=3,A>0 and choose lambda>0 with lambda squared<A. Put
delta=lambda eta^((q-2)/2). It tends to zero and the exact family is feasible
for every sufficiently small positive eta; no analytic dependence of this
fractional-power choice on eta is required. Equation(9) gives

\[
\begin{aligned}
F(p)-m(\eta)&=\lambda^2\eta^q[1+O(\eta)],\\
F(p)-m(\eta)-\tfrac12\eta^2\|z-z_\eta\|^2
 &=\ell\lambda^2\eta^{q+1}+O(\eta^{q+2})<0.              \tag{10}
\end{aligned}
\]

The remainder follows from2q-1>=q+2 for q>=3. Its constants may depend
on fixed q and lambda. The first line is positive and less than Aeta^q
after shrinking the collar. The second line proves(1). All four radial
slacks are exactly zero, so adding radial terms cannot repair this witness.

To apply8955's every-kappa<1/2 theorem on this exact-budget class, use its
m=8+Ceta+Bstar eta squared+C3eta cubed+O(eta^4) to place the class in one
fixed cubic budget (for example T=C3+A+1 for eta<1 sufficiently small).
The resulting lower constants and(1) prove the claimed unattained supremum.

## Scope and certificate boundary

The finite checker establishes(5)-(7), the normalization, and joint formal
root constraints. It has two different algebraic root-constraint methods,
both authored by six-sendov-3; that is not independent peer review.
Existence, exact disk feasibility, convergent analytic division, uniform
remainders and the moving exact-minimum comparison are ordinary mathematics
in this proof and the attributed8921/8955 premises. No proof assistant or
solver is used. The first-power inequality F>=8 at arbitrary interior radii
is still open; this witness only excludes an overly sharp stability bound.
