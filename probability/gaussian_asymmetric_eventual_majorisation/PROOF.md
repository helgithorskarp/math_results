# Every Gaussian hinge at high variance on the asymmetric square-cone family

Author proof with a validated finite numerical certificate, 26 September 2026.
Independent review of this new result is pending. The all-variance question
remains open; this result gives no new Kneser--Poulsen inequality.

## 1. Statement and role in the shared problem

In the indicated order, set

\[
 A=((1,0,1),(0,1,1),(-1,0,1),(0,-1,1)),\quad
 B=((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1)),
\]
\[
 X=(0,A,-B),\quad Y=(0,A,B),\qquad
 p=(8,12,7,15,44,21,11,23,43)/184.                 \tag{1}
\]

Write \(\mu_w=\sum_{i=0}^8w_i\delta_{X_i}\),
\(\nu_w=\sum_{i=0}^8w_i\delta_{Y_i}\), and let \(\gamma_s\)
have covariance \(sI_3\). For a density \(f\), put
\(H_f(a)=\int_{\mathbb R^3}(f-a)_+\).

**Theorem.** For every probability vector \(w\) satisfying
\(\|w-p\|_1\le1/25000\),

\[
 H_{\nu_w*\gamma_s}(a)\ge H_{\mu_w*\gamma_s}(a)
 \quad\hbox{for every }s\ge16896\hbox{ and every }a\ge0.       \tag{2}
\]

For the central vector \(w=p\), the variance bound improves to \(s\ge13200\).
The constants are sufficient bounds, not sharp transitions.

The map \(X_i\mapsto Y_i\) is a contraction: within clusters and from the
origin distances agree, while each cross squared-distance loss is
\(4a_i\cdot b_j\in\{0,8\}\). There are 28 zero and eight positive losses
among the 36 pairs. Kirszbraun extension places this finite map within the
source problem's global formulation. Both supports lie in \(B(0,\sqrt3)\).

This is the same configuration and central weight vector for which the
team's independently reviewed [bridge obstruction](../gaussian_atomic_bridge_obstruction/PROOF.md)
rules out position martingales after separate isometries, even after common
Gaussian smoothing, and exact common-output mixtures of deterministic maps
having contracting motions in \(\mathbb R^5\). Those exclusions hold on the
larger weight ball of radius \(1/4000\). They are not hypotheses of our
positive proof. Here a spherical comparison supplies a different sufficient
mechanism. The remaining possible counterexample regime for (1)--(2) has
\(0<s<16896\), or \(0<s<13200\) at the central weights. No claim about the
sign in those remaining regimes is made.

## 2. Spherical reduction and the finite certificate's exact obligation

With normalized sphere measure \(\sigma\), define

\[
 S_{\xi}(\lambda)=\int_{S^2}\log\mathbb E_{Z\sim\xi}
                   e^{\lambda\theta\cdot Z}\,d\sigma(\theta),\qquad
 J_w=S_{\mu_w}-S_{\nu_w}.                                  \tag{3}
\]

The team's independently reviewed [eventual-endpoint theorem](../gaussian_majorisation_eventual_endpoint/PROOF.md),
Theorem 1, states that laws supported in radius \(R\), related by a
contraction, obey every hinge inequality once

\[
 J(\lambda)\ge\kappa\quad(\lambda\ge1/(2R)),\qquad
 s\ge R^2\max\{8,44/\kappa\}.                              \tag{4}
\]

That theorem combines a uniform spherical-tail estimate with the signed
high-noise window. Its quantifiers include thresholds arbitrarily close to
zero. We retain all its assumptions and constants; we do not substitute
positivity at finitely many hinges or replica orders for (4).

We prove the concrete uniform estimate

\[
 J_p(\lambda)\ge1/100\quad\hbox{for every }\lambda\ge1/4.     \tag{5}
\]

A validated calculation handles \([1/4,24]\). An elementary analytic
support-function estimate handles the entire ray \([24,\infty)\).

## 3. Jensen cubature with an explicit error bound

For a law \(\xi\) in \(B(0,R)\), the function
\(F_\xi(v)=\log\mathbb E e^{\lambda v\cdot Z}\) satisfies

\[
 0\preceq D^2F_\xi(v)=\lambda^2\operatorname{Cov}_{v}(Z)
       \preceq\lambda^2R^2I.                               \tag{6}
\]

Partition \(S^2\) into finitely many cells of masses \(q_C\), and let
\(c_C=\mathbb E[\Theta\mid\Theta\in C]\) be their vector centroids.
These centroids need not lie on the sphere. Jensen's inequality and Taylor's
formula with the Hessian bound give

\[
 \sum_Cq_CF_\xi(c_C)\le S_\xi(\lambda)
 \le\sum_Cq_CF_\xi(c_C)
      +\frac{\lambda^2R^2}{2}\sum_Cq_C(1-|c_C|^2).            \tag{7}
\]

The first-order Taylor term integrates to zero in each cell, and
\(\mathbb E[|\Theta-c_C|^2\mid C]=1-|c_C|^2\). Thus (7) is an integral
error bound, not an unvalidated quadrature rule.

Translations leave \(S_\xi\) unchanged. Translate the target by \(-e_3\):
its origin becomes \(-e_3\), and its other points become the cardinal and
diagonal planar vectors. The translated target is in \(B(0,\sqrt2)\).
Apply the lower half of (7) to the source and the upper half to this target.
For \(M=\sum_Cq_C(1-|c_C|^2)\), this yields

\[
 J_p(\lambda)\ge
 \sum_C q_C\log\frac{\sum_i p_i e^{\lambda c_C\cdot X_i}}
                        {\sum_i p_i e^{\lambda c_C\cdot(Y_i-e_3)}}
           -\lambda^2M.                                   \tag{8}
\]

### Exact cell geometry

Use 16 equal polar-angle intervals and 64 equal azimuth intervals. For a
cell \(\theta\in[\theta_0,\theta_1]\), \(\phi\in[\phi_0,\phi_1]\), put

\[
 d=\cos\theta_0-\cos\theta_1,\quad
 h=\frac{(\theta_1-\theta_0)/2
                 -(\sin2\theta_1-\sin2\theta_0)/4}{d}.
\]

Its normalized area is \(q=d/128\), and its centroid is

\[
 c=\left(h\frac{\sin\phi_1-\sin\phi_0}{\phi_1-\phi_0},
          h\frac{\cos\phi_0-\cos\phi_1}{\phi_1-\phi_0},
          \frac{\cos\theta_0+\cos\theta_1}{2}\right).        \tag{9}
\]

These follow by integrating \((\sin\theta\cos\phi,
\sin\theta\sin\phi,\cos\theta)\sin\theta\,d\theta\,d\phi\).
The cells cover the sphere, with boundary overlaps of zero area. All cell
weights are positive; their sum is one and their weighted centroids sum to
zero. The computed enclosure has \(M<1/269\); formula (8) uses the complete
ball enclosure rather than that rounded upper bound.

### Covering every spherical parameter between the certified knots

The source lies in \(B(0,\sqrt3)\), so differentiating (3) gives

\[
 J_p''(\lambda)=\int\operatorname{Var}_{\mu,\lambda\theta}
                         (\theta\cdot X)\,d\sigma
             -\int\operatorname{Var}_{\nu,\lambda\theta}
                         (\theta\cdot Y)\,d\sigma\le3.      \tag{10}
\]

In particular, if \(J(a)\ge L_a\), \(J(b)\ge L_b\), then concavity of
\(J(\lambda)-3\lambda^2/2\) implies, throughout \([a,b]\),

\[
 J(\lambda)\ge\frac{b-\lambda}{b-a}L_a+
               \frac{\lambda-a}{b-a}L_b
                   -\frac32(\lambda-a)(b-\lambda)
 \ge\min(L_a,L_b)-\frac38(b-a)^2.                           \tag{11}
\]

[EXPECTED.json](EXPECTED.json) gives 26 rational knots from \(1/4\) to 24
and a rational lower bound at each. [verify.py](verify.py) encloses the
right side of (8) with outward 128-bit Arb arithmetic and checks each
strict lower-bound claim. Exact rational evaluation of (11) over all 25
adjacent intervals has minimum

\[
 \frac{1290469}{128000000}>\frac1{100}.                       \tag{12}
\]

The file contains every knot, so coverage is explicit and complete.
This proves (5) on the compact interval. The exact geometry, Hessian
estimate, and interpolation inequality explain why the finite certificate
implies a continuum statement.

## 4. The infinite parameter ray needs no quadrature

Let \(h_X,h_Y\) be the support functions of the point hulls in (1), and
\(\delta=\int(h_X-h_Y)\,d\sigma\). For a direction with
\(u=|\theta_1|\), \(v=|\theta_2|\), \(q=|\theta_3|\), write
\(m=\max(u,v)\), \(n=u+v\), \(\ell=\min(u,v)\).
Averaging the two signs of the third coordinate gives exactly

\[
 \frac12\left[\max(q+m,n-q)-\max(0,n-q)\right].            \tag{13}
\]

The bracket is nonnegative for all directions. When \(q\ge\ell\),
it equals \(2q-\ell\) if \(q\le n\), or \(q+m\) if \(q\ge n\);
in both cases it is at least \(q\). Moreover
\(\ell^2\le(1-q^2)/2\), so \(q\ge1/\sqrt3\) suffices.
The variable \(|\Theta_3|\) is uniform on \([0,1]\) under normalized
area on \(S^2\). Therefore

\[
 \delta\ge\frac12\int_{1/\sqrt3}^1q\,dq=\frac16.           \tag{14}
\]

The maximum bounds for a weighted exponential sum and \(p_{\min}=7/184\)
now give

\[
 J_p(\lambda)\ge\lambda\delta+\log p_{\min}
     \ge\lambda/6+\log(7/184)>1/100\quad(\lambda\ge24).      \tag{15}
\]

The checker proves the last elementary logarithmic inequality by the exact
rational certificate \(e^{399/100}>184/7\), using the first five nonnegative Taylor terms of the exponential. Thus the infinite ray is controlled without a
numerical cutoff assumption. Equations (12) and (15) prove (5).

## 5. An open weight class and completion of every hinge

Suppose \(\|w-p\|_1\le\epsilon=1/25000\). Componentwise,

\[
 (1-\eta)p_i\le w_i\le(1+\eta)p_i,
 \qquad \eta=\epsilon/p_{\min}=23/21875<1.
\]

For either support, the same inequalities hold for its moment generating
function. Consequently, uniformly over all \(\lambda>0\),

\[
 J_w(\lambda)\ge J_p(\lambda)
                  -\log\frac{1+\eta}{1-\eta}
 \ge J_p(\lambda)-\frac{2\eta}{1-\eta}.
\]

Here \(\log(1+\eta)\le\eta\) and
\(-\log(1-\eta)\le\eta/(1-\eta)\). Rational arithmetic gives

\[
 \frac1{100}-\frac{2\eta}{1-\eta}
       =\frac1{100}-\frac{23}{10926}>\frac1{128}.             \tag{16}
\]

In particular all weights remain positive. Since \(R=\sqrt3\) and
\(1/(2\sqrt3)>1/4\), (5), (16), and (4) apply. They give
\(3\cdot44\cdot100=13200\) for \(p\), and
\(3\cdot44\cdot128=16896\) throughout the stated weight ball.
This proves (2), including \(a=0\) by normalization.

## 6. Scope and trust boundary

The finite numerical obligations use Python integers/Fraction and
python-flint 0.8.0, whose Arb balls provide outward enclosures of all
transcendental expressions. The implementation fails on an inconclusive
comparison; displayed decimal approximations are not used as certificates.
The rational knot bounds in EXPECTED.json are validated, not assumed.
The mathematical proof of sphere coverage and errors is (6)--(11), and the
unbounded parameter tail is (13)--(15). The final transfer depends on the
published eventual-endpoint theorem and its analytic inputs.

The same rational certificate was also checked at 192 bits with a distinct
32-by-128 equal-height sphere partition. Its centroids use the primitive
\((z\sqrt{1-z^2}+\arcsin z)/2\) for the horizontal component. This changes
the integration cells and error bound, but still trusts Arb and the same
analytic cubature principle. It is supplementary verification, not an
independent mathematical review or formalization.

This establishes a positive high-variance region for a concrete open family
beyond the previously sufficient coupling constructions. It does not close
the smaller-variance regime, prove an all-weight cone theorem, or imply a
new ball-volume comparison. The constants should not become a separate
optimization project: the remaining task is an all-variance analytic hinge
mechanism or a rigorous counterexample within the unresolved region.
