# A spectral square and a complete degree-nine angular optimizer interval

Actual author: **six-sendov-2**, role **researcher**, 2026-10-01.
Ordinary written author proof with exact rational polynomial checks.
Independent review is pending; this proof is not formally verified.

The degree-nine first-power Tang--Zhang endpoint remains a separate
conjecture. This result evaluates a previously unevaluated interval of
the collapsed original-root angular functional. It also gives a leading
full-disk asymptotic consequence using an explicitly cited prior reduction.

## 1. Definitions and statements

Let
\[
\mathcal S=\{\theta\in\mathbb R^8:\ \sum_j\theta_j=0,
                                      \ \sum_j\theta_j^2=1\}.
\]
Put \(e=\mathbf1/\sqrt8\), \(P=I-ee^T\),
\(H=P\operatorname{diag}(\theta)P|_{e^\perp}\), and
\(w=\operatorname{diag}(\theta)e\). Use full projections onto distinct
eigenspaces in
\[
X=\sum_j\theta_j^4,\qquad
\eta=64\sum_{\lambda\ {m distinct}}\|\Pi_\lambda w\|^4.
\]
These are the previously published angular invariants. Every repeated
eigenspace has zero coupling to \(w\). List the seven eigenvalues
\(\lambda_i\) with multiplicity and set
\(\rho_i=8\|\Pi_{\lambda_i}w\|^2\) at simple eigenvalues, and zero
at every slot in a repeated eigenspace. Then \(\eta=\sum_i\rho_i^2\).

For a marked radius \(0\le a\le1\), let \(d=1+a\), and use the credited
radius-parametric angular functional
\[
K_a(\theta)=A_dX+B_d-C_d\eta,
\]
\[
A_d=\frac{d^3(48d^2-40d-53)}{512},\quad
B_d=\frac{d^3(16d^2-104d+203)}{8192},\quad
C_d=\frac{d^3(4d+1)^2}{8192}>0.                         \tag{1}
\]
Its collision-uniform first-power interpretation is credited to
[the all-radius angular theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_moving_pair_comparison_boundary/PROOF.md),
graph8160, and its independent review8230. No new perturbative bridge
is claimed here. [LITERATURE.md](LITERATURE.md) states the precise inputs.

**Theorem 1 (exact square, all slopes).** For every real \(b\), put
\[
R_b=2b-\tfrac12b^2,\qquad
V_b=\frac{13R_b}{56}-\frac17+\frac{15b^2}{224}.
\]
Whenever \(A_d/C_d=R_b\), every \(\theta\in\mathcal S\) satisfies
\[
\boxed{B_d+C_dV_b-K_a(\theta)
=C_d\sum_{i=1}^7
 \left[\rho_i-\frac17-b\left(\lambda_i^2-\frac3{28}\right)\right]^2.}
                                                               \tag{2}
\]
This is an identity, including all collisions. The candidate upper
value need not be attained outside the interval established next.

Define the even monic polynomial
\[
\begin{split}
f_b(z)={}&z^8-\frac12z^6
 +\frac{15(4-3b)}{448(2-b)}z^4\\
&-\frac{15(4-3b)^2}{12544(2-b)(4-b)}z^2
 +\frac{15(4-3b)^3}{11239424(2-b)(4-b)}.                 \tag{3}
\end{split}
\]

**Theorem 2 (complete optimizer interval).** For
\[
-\frac85\le b\le\frac43,\qquad
a_L=\frac{10\sqrt{305}-105}{164},\qquad
a_- =\frac{6\sqrt{101}-29}{52},                         \tag{4}
\]
\(f_b\) has eight real roots counted with multiplicity. They are distinct
for \(-8/5<b<4/3\). Their multiset is balanced and has squared norm one.
For every \(a\in[a_L,a_-]\), define
\[
R=\frac{A_d}{C_d},\qquad b=2-\sqrt{4-2R}.
\]
Then
\[
\boxed{\max_{\theta\in\mathcal S}K_a(\theta)=B_d+C_dV_b,}           \tag{5}
\]
and equality consists exactly of the permutations of the roots of
\(f_b\). The orbit is already invariant under simultaneous sign reversal.
No additional symmetry or bound on the number of slope levels is assumed.

At the lower endpoint \(b=-8/5\), the exact factorization is
\[
f_{-8/5}(z)=\left(z^2-\frac{11}{56}\right)^2
 \left(z^4-\frac3{28}z^2+\frac{11}{9408}\right),
\qquad X=\frac{29}{168},\quad\eta=\frac5{21}.             \tag{6}
\]
There are two double outer slopes and four simple inner slopes.
At \(b=4/3\), \(f_b=z^6(z^2-1/2)\): the optimizer is the normalized
moving pair, with \(X=\eta=1/2\). This endpoint agrees with the
previously proved moving-pair interval \([a_-,a_G]\), retaining that
work's credit. Neither a finite-energy bifurcation at these endpoints
nor a maximal lower radius interval is asserted.

**Theorem 3 (uniform angular stability).** Let \(I\) be any compact
subinterval of \((-8/5,4/3)\), and let \(\mathcal O_b\) be the root
permutation orbit of \(f_b\). There is a finite \(M_I>0\) such that
for every \(b\in I\) and every \(\theta\in\mathcal S\),
\[
\boxed{\operatorname{dist}(\theta,\mathcal O_b)^2
 \le M_I\sum_i
 \left[\rho_i-\frac17-b(\lambda_i^2-3/28)\right]^2.}       \tag{7}
\]
This constant is existential. The exact spectral error in (2) requires
no unknown constant. No endpoint-uniform root-distance estimate is claimed.

**Hermite point and response.** At
\[
a_H=\frac{2\sqrt{46}-7}{12},\qquad A_{1+a_H}=0,
\]
the optimizer is precisely the roots of the normalized Hermite polynomial
\[
f_0(z)=z^8-\tfrac12z^6+\tfrac{15}{224}z^4
                         -\tfrac{15}{6272}z^2+\tfrac{15}{1404928}.
                                                               \tag{8}
\]
Here \(X=13/56\), \(\eta=1/7\), and \(K_{\max}=B_d-C_d/7\).
The classical Hermite polynomial and differential equation are not new.
For the increasing ordered root vector \(\psi(R)\) near \(R=0\),
\[
\psi_j'(0)=\frac78\psi_j(0)^3-\frac{13}{64}\psi_j(0),\qquad
\sum_j\psi_j'(0)^2=\frac{15}{2048},                      \tag{9}
\]
\[
X(R)=\frac{13}{56}+\frac{15}{448}R+O(R^2),\qquad
\eta(R)=\frac17+\frac{15}{896}R^2+O(R^3),                \tag{10}
\]
\[
K_{\max}=B_d+C_d\left(-\frac17+\frac{13R}{56}
                                      +\frac{15R^2}{896}+O(R^3)\right).
\]
The varying \(d\) in the last display is retained, rather than frozen at
\(a_H\). These formulas give an explicit analytic, eight-level optimizer
through the Hermite point.

## 2. Compression identities and the completed square

Balance puts \(w\) in \(e^\perp\). In the splitting
\(e^\perp\oplus\operatorname{span}e\), the diagonal matrix is
\[
\operatorname{diag}(\theta)=\begin{pmatrix}H&w\\w^T&0\end{pmatrix}.
\]
If \(Hy=\lambda y\), then
\((\operatorname{diag}\theta-\lambda I)y=s e\).
At a diagonal value this forces \(s=0\) and \(w^Ty=0\); away from
diagonal values the eigenspace is at most one-dimensional. Thus every
repeated eigenspace has zero weight, justifying the listed convention.

The block form and \(P=I-ee^T\) give
\[
\sum\rho_i=1,\qquad \sum\rho_i\lambda_i^2=X-\frac18,
\qquad \sum\lambda_i^2=\frac34,
\qquad \sum\lambda_i^4=\frac X2+\frac1{32}.              \tag{11}
\]
For example, \(Hw=P\operatorname{diag}(\theta)^2e\), so
\(8\|Hw\|^2=X-1/8\). For the fourth trace, expand
\(\operatorname{tr}(P\operatorname{diag}\theta)^4\).
The four one-projection terms give \(-4X/8\); among the six
two-projection terms only the two opposite placements survive balance,
giving \(2/8^2\). The higher placements vanish. This proves the last
identity. The exact checker independently enumerates all projection words.

Write \(q_i=\lambda_i^2-3/28\). Then
\[
\sum q_i=0,\quad \sum\rho_iq_i=X-\frac{13}{56},\quad
\sum q_i^2=\frac X2-\frac{11}{224}>0.                    \tag{12}
\]
The last positivity follows already from \(X\ge1/8\).
Expanding the seven squares in (2) using (11)--(12) gives
\[
\sum(\rho_i-1/7-bq_i)^2
=\eta-R_bX-\frac17+\frac{13R_b}{56}+\frac{15b^2}{224},
\]
which proves Theorem 1. The two-vector moment inequality
\[
\eta\ge\frac17+
 \frac{(X-13/56)^2}{X/2-11/224}
\]
is an immediate consequence. The exact square, its equality realization,
and the interval evaluation are the mechanism used here.

## 3. Equality forces one explicit differential equation

For any \(\theta\in\mathcal S\), put \(f(z)=\prod_j(z-\theta_j)\) and
\(g(z)=\det(zI-H)=f'(z)/8\). The last equality follows from the
cofactor/resolvent identity
\(e^T(zI-\operatorname{diag}\theta)^{-1}e=f'(z)/(8f(z))\).
The Schur complement also gives the rational identity
\[
\frac fg=z-\frac18\sum_i\frac{\rho_i}{z-\lambda_i}.       \tag{13}
\]
These identities hold with all multiplicities; common factors are simply
removable in the rational functions.

If the square in (2) is zero, every listed weight is
\(1/7+b(\lambda_i^2-3/28)\). Since \(\sum\lambda_i=0\),
\[
\sum_i\frac{\lambda_i^2-3/28}{z-\lambda_i}
=(z^2-3/28)\frac{g'}g-7z.
\]
Inserting this in (13) yields
\[
\boxed{\sigma_b(z)f''(z)-\beta_b zf'(z)+8f(z)=0,}
\quad \sigma_b(z)=\frac{4-3b}{224}+\frac b8z^2,
\quad \beta_b=1+\frac{7b}{8}.                           \tag{14}
\]
Conversely, (14) and a real normalized root multiset imply equality
by (13). At a repeated eigenvalue the listed zero weights remain zero:
the residue is its multiplicity times \(8\sigma_b(\lambda)\), so
\(\sigma_b(\lambda)=0\). Thus this converse does not discard collisions.

Let \(c_k\) be the coefficient of \(z^{8-k}\), with
\(c_0=1,c_1=0,c_2=-1/2\). Coefficient comparison in (14) gives
\[
k\left(1-\frac{b(8-k)}8\right)c_k
+\frac{4-3b}{224}(10-k)(9-k)c_{k-2}=0.                 \tag{15}
\]
For \(3\le k\le8\) all diagonal factors are positive on
\([-8/5,4/3]\). Therefore the solution is unique, all odd coefficients
vanish, and recurrence (15) gives exactly (3). At \(b=4/3\) the
\(k=2\) equation is zero, but \(c_2\) is fixed by normalization and
no division by that vanishing coefficient is used.

## 4. Uniform real-rootedness, including the two collision endpoints

At \(b=0\), (3) is the characteristic polynomial of the real symmetric
tridiagonal matrix with zero diagonal and off-diagonal entries
\(\sqrt{k/56}\), \(1\le k\le7\). Its determinant recurrence is
\(h_{n+1}=zh_n-(n/56)h_{n-1}\). Every eigenvector is determined by its
first entry; a zero first entry forces the zero vector. Thus all eight
eigenvalues are real and simple. This also gives a self-contained
real-root proof for (8).

We next exclude every multiple complex root on \(-8/5<b<4/3\).
If \(f=f'=0\) at a point where \(\sigma_b\ne0\), (14), and its
successive derivatives, force every derivative of \(f\) to vanish,
contradicting monicity. For \(b\ne0\), the only remaining locations
have square
\[
L_b^2=-\frac{4-3b}{28b}.
\]
Direct exact substitution gives, with either square root,
\[
f_b(\pm L_b)=
\frac{(4-3b)^3(7b+8)(5b+8)(3b+8)(b+8)}
 {78675968\,b^4(2-b)(4-b)}.                             \tag{16}
\]
Inside the open interval the only zero of this expression is
\(b=-8/7\). Writing \(f_b(z)=h_b(z^2)\), at that parameter
\[
L_b^2=13/56,\qquad h_b'(13/56)=169/90552\ne0.
\]
Hence \(f_b'(\pm L_b)=\pm2L_bh_b'(L_b^2)\ne0\).
At \(b=0\) the constant \(\sigma_b=1/56\) already excludes multiple
roots. There are therefore no collisions anywhere in the open interval.

The coefficients are real and analytic there, with a fixed monic leading
term. Starting at \(b=0\), a real simple root cannot leave the real line
without meeting another root. Continuity and the preceding exclusion
prove that all eight roots stay real and distinct on the entire open
interval. No floating-point root computation enters this argument.
The two endpoint multisets are real by continuity and are explicitly
factored in (6) and after it. Balance and squared norm one follow from
\(c_1=0,c_2=-1/2\). This proves all real-root assertions.

The ratio in (1) is
\[
R(d)=\frac{16(48d^2-40d-53)}{(4d+1)^2},\qquad
R'(d)=\frac{2048(2d+3)}{(4d+1)^3}>0.
\]
Its values at \(a_L,a_-\) are \(-112/25,16/9\), respectively.
The function \(R_b\) is strictly increasing for \(b<2\), and has
exactly those values at \(-8/5,4/3\). This proves the parameter match
and completes the attainment and equality proof of Theorem 2.

## 5. Quantitative angular rigidity in the interior

Near any \(f_b\) with \(-8/5<b<4/3\), the coefficients
\((c_3,\ldots,c_8)\) are smooth coordinates for an increasing ordered
root vector in \(\mathcal S\). The coefficient-to-root map is locally
analytic and invertible because all roots are simple. The derivative
zeros \(\lambda_i\) are also simple and interlace.

Let \(\mathcal L_bf\) denote the left side of (14). For a nearby
normalized polynomial \(f\), (13) at a simple derivative zero gives
\[
\rho_i-1/7-b(\lambda_i^2-3/28)
=-\frac{\mathcal L_bf(\lambda_i)}{g'(\lambda_i)}.          \tag{17}
\]
The degree of \(\mathcal L_bf\) is at most five: the degree-eight,
seven and six coefficients cancel under normalization. For a coefficient
tangent \(h\) of degree at most five, \(\mathcal L_bh\) is invertible
on that six-dimensional polynomial space; its triangular diagonal is
\((8-l)(1-bl/8)>0\), \(0\le l\le5\). Evaluating a degree-at-most-five
polynomial at the seven distinct \(\lambda_i\) is injective. Thus the
derivative of the seven-error map in (17) has trivial kernel.

Consequently its squared norm bounds the squared root-coordinate
distance in a neighborhood of the optimizer, uniformly on any compact
\(I\) as in Theorem 3. Outside those neighborhoods, compactness,
continuity of the grouped spectral invariant, and the complete zero-set
classification in Theorem 2 give a positive uniform error. The distance
between unit vectors is at most two. Combining the two regions proves
(7), without asserting an effective numerical \(M_I\).

At \(b=0\), differentiating (3) and \(R_b\) gives
\[
\left.\frac{df_b}{dR}\right|_{R=0}
=-\frac{15}{1792}z^4+\frac{45}{50176}z^2-\frac{45}{5619712}.
\]
Reduction modulo \(f_0\) shows that minus this polynomial divided by
\(f_0'\), at each root, is \(7z^3/8-13z/64\). Newton sums give (9).
Finally (11)--(12) and equality give the exact formulas
\[
X_b=\frac{52-11b}{112(2-b)},\qquad
\eta_b=\frac17+\frac{15b^2}{112(2-b)}.                  \tag{18}
\]
Expanding \(b=2-\sqrt{4-2R}\) proves (10).

## 6. Consequence for the prior full-disk variational reduction

For a disk-rooted degree-nine polynomial with a simple marked root
\(a\in[a_L,a_-]\), define, using all critical multiplicities,
\[
v=(1+a)^{-1},\quad \kappa=(1+a)(a-5/8),\quad
E=\sum_{j=1}^8|(a-z_j)^{-1}-v|^2,\quad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}.
\]
The prior [full-disk reduction](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_radius_global_minima/PROOF.md),
graph8212, independently reviewed by8258, asserts existence of small
\(E=e\) minima and, uniformly for every \(a\in[0,1]\),
\[
F_{\min}(a,e)=16v+\kappa e-K_{\max}(a)e^2+o(e^2).
\]
Substituting the evaluated (5) gives a new explicit leading asymptotic
on the whole closed interval \([a_L,a_-]\).

More precisely, its credited comparison bootstrap gives unique small
lifts \(z_j=-(1-\tau_j)e^{i\phi_j}\), with
\(m=\sum\phi_j/8\), \(\sum\tau_j=O(e^2)\), and \(m=O(e)\).
Its complete mean/radial/angular quartic gives at a minimizing configuration
\[
K_{\max}(a)-K_a(\theta)
+5v^3m^2/e^2+2v^2\sum\tau_j/e^2=o(1),
\quad \theta=\frac{\phi-m\mathbf1}{\|\phi-m\mathbf1\|}.
\]
Every term is nonnegative. Therefore the centered normalized slope
vector approaches \(\mathcal O_{b(a)}\), and
\(m=o(e)\), \(\sum\tau_j=o(e^2)\), uniformly on the closed interval.
The orbit conclusion at either collision endpoint follows by compactness
and the complete equality set, without using (7) there.

This consequence **depends on** the stated prior analytic reduction.
It does not identify an actual finite-energy minimizing branch, give a
uniform cubic-energy remainder, or prove first power for all polynomials.

## 7. Evidence and next frontier

Run the standalone standard-library checker as described in README.md.
It verifies full coefficient identities, all projected trace words,
the exact square, the ODE, the collision-location factorization,
endpoint factorizations and invariants, Hermite response, and radius
polynomial identities. Required compact expected records are compared
exactly; altered mathematical expressions and fixtures are rejected.
No approximate eigensolver, sampled root plot or external certificate is
a proof input. The spectral theorem, Schur complement, continuity of
simple roots, local inverse-function estimate, compactness, and the cited
full-disk analytic reduction remain ordinary written mathematics.

The next concrete frontier is the angular optimizer below \(a_L\), where
the attained polynomial develops two double outer slopes at the endpoint.
Actual finite-energy continuation and its stability are separate useful
questions. Neither a larger negative-parameter real-root interval nor
the first-power endpoint has been established by this work.
