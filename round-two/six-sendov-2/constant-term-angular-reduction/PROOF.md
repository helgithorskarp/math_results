# Exact feasible constant-term reduction of the original-root angular quotient

Actual author **six-sendov-2**, role **researcher**, 2026-10-02.
Complete ordinary author proof with finite exact arithmetic certificates;
unformalized and independently unreviewed.

Fixing the derivative and varying a polynomial's constant term is a
classical reverse approach, explicitly described by
[Bl. Sendov](https://www.math.miami.edu/data/seminars/abstract_sendov.pdf).
The contribution here is its exact realization and optimization for the
specific angular mass-square quotient: the nonnegative six-moment relaxation
is precisely the real-rooted fiber, including blocked and collision endpoints.
Neither constant-term deformation nor ordinary least squares is claimed new.
The bounded literature intake does not establish historical priority.

This polynomial has **degree eight** and its roots are real angular slopes.
It is auxiliary to the assigned **complex degree-nine first-power** problem.
Varying this auxiliary constant does not give a legal deformation of the
actual disk-rooted degree-nine polynomial or prove the physical bridge.

## 1. Definition and statement

Let \(u=(u_1,\ldots,u_8)\in\mathbb R^8\) be nonzero and balanced:
\(\sum u_i=0\). Write
\[
e=\mathbf1/\sqrt8,\quad P=I-ee^T,\quad
H=P\operatorname{diag}(u)P|_{e^\perp},\quad
N=\sum u_i^2,\quad D=\sum u_i^4-N^2/8.
\]
For the **whole** eigenspace projection \(\Pi_\lambda\) of \(H\), put
\[
m_\lambda=\|\Pi_\lambda u\|^2,\qquad
\eta=\sum_{\lambda\ {\rm distinct}}m_\lambda^2,\qquad
C(u)=\frac{N^2-\eta}{D}\quad(D>0).                         \tag{1}
\]
This is the quotient of the preceding
[angular framework](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and
[global variational formulation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/angular-three-level-transition/PROOF.md).
It is invariant under nonzero raw scaling, signs and permutations.
Normalization \(u/\sqrt N\) gives its balanced unit-sphere definition.

Set \(f(z)=\prod_{i=1}^8(z-u_i)\), \(h=f'/8\), and
\(f_\delta=f+\delta\). Suppose first that \(h\) is squarefree.
Its seven roots are real and distinct; order them as
\(\lambda_1<\cdots<\lambda_7\).
In the following formulas \(m_j=m_{\lambda_j}\), with zero masses included.
Define
\[
m_j=-\frac{8f(\lambda_j)}{h'(\lambda_j)},\qquad
\kappa_j=-\frac8{h'(\lambda_j)},\quad
a=\sum_{j=1}^7\kappa_j^2>0,\quad
b=2\sum_{j=1}^7m_j\kappa_j,\quad
\delta_*=-\frac b{2a}.                                  \tag{2}
\]
The raw mass normalization is \(\sum m_j=N\), not \(8N\).
Let
\[
\ell=-\min_{j\in\{2,4,6\}} f(\lambda_j),\qquad
r=-\max_{j\in\{1,3,5,7\}} f(\lambda_j),\qquad I=[\ell,r].
                                                               \tag{3}
\]

**Theorem (complete feasible fiber and its exact optimum).**

1. \(I\) is a nonempty compact interval, possibly a singleton.
   \(f_\delta\) has eight real roots counted with multiplicity exactly when
   \(\delta\in I\), equivalently when \(m+\delta\kappa\ge0\)
   coordinatewise. Its roots then remain balanced with the same \(N,D\).
   Its seven compression masses are exactly \(m+\delta\kappa\).

2. The six coupling moments
   \[
   \mu_k=\sum_{j=1}^7m_j\lambda_j^k,\quad 0\le k\le5,
   \]
   are constant along the fiber. Define
   \[
   V_{kj}=\lambda_j^k\quad(0\le k\le5,\ 1\le j\le7),\quad
   G_6=VV^T=\left(\sum_{j=1}^7\lambda_j^{p+q}\right)_{p,q=0}^5,
   \quad R_6=\mu^TG_6^{-1}\mu.                            \tag{4}
   \]
   \(G_6\) is positive definite. Every vector \(v\in\mathbb R^7\)
   with \(Vv=\mu\) is \(m+\delta\kappa\) for a unique real \(\delta\).
   **Every such nonnegative vector is realized by the original-root
   polynomial \(f_\delta\)**, with its full eigenspace masses equal to \(v\).

3. Set \(\widehat\delta=\operatorname{clamp}(\delta_*,[\ell,r])\).
   The unique optimal constant, and the exact fiber maximum, are
   \[
   \boxed{\ \eta_{\rm feasible}
      =R_6+a\,\operatorname{dist}(\delta_*,I)^2,\qquad
   \max_{\delta\in I} C(f_\delta)
      =\frac{N^2-R_6-a\,\operatorname{dist}(\delta_*,I)^2}{D}.\ } \tag{5}
   \]
   Here \(C(f_\delta)\) means (1) applied to its eight real roots.
   Equivalently,
   \[
   \eta(\delta)=\eta(0)+b\delta+a\delta^2
              =R_6+a(\delta-\delta_*)^2.                  \tag{6}
   \]
   \(R_6\) is the exact *unconstrained* mass-square minimum; discarding
   the feasibility penalty is justified precisely when
   \(m+\delta_*\kappa\ge0\).

4. If \(\ell<\widehat\delta<r\), the maximizing original roots are
   all distinct, every mass is positive, and
   \[
   \sum_{j=1}^7\frac{f_{\widehat\delta}(\lambda_j)}
                         {h'(\lambda_j)^2}=0.            \tag{7}
   \]
   The seven optimal masses are evaluations at the \(\lambda_j\)
   of a polynomial of degree at most five. If
   \(\widehat\delta\in\{\ell,r\}\), at least one original double
   root occurs, including the case \(\ell=r\).

**Degenerate case.** For real-rooted \(f\), \(h\) fails to be squarefree
exactly when an original root has multiplicity at least three.
Then the entire real-rooted constant-term fiber is \(\{\delta=0\}\).
The seven-distinct-node inverse in (4) is inapplicable.
If \(h\) is squarefree, \(D>0\) automatically: \(D=0\) and balance
would give four copies each of two opposite equal-magnitude roots,
so \(h\) would have repeated roots.

**Global variational consequence.** For every real threshold \(T\), if
some nonuniform balanced profile has \(C>T\), there exists another
such profile with \(C>T\) which either has an original-root collision,
or has all eight roots distinct and satisfies (7) and the degree-five
mass-interpolation condition. A global maximizing profile with all
eight roots distinct must itself satisfy these conditions.
This is a one-parameter global reduction; it does not bound the
number of levels of a centered profile or control the collision strata.

In particular, the known three-level threshold \(c_3\) and local
[full-sphere stability](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/full-sphere-effective-neighborhood/PROOF.md)
retain their original domains. Equation (5) does not prove
\(C_*=c_3\). Constant-term optimization can move outside a stated
local neighborhood. There is no transfer to a physical first-power theorem.

## 2. Compression, resolvent and residues

In the orthogonal decomposition \(\mathbb R^8=\mathbb Re\oplus e^\perp\),
the diagonal matrix \(\operatorname{diag}(u)\) has blocks
\[
\begin{pmatrix}0&u^T/\sqrt8\\u/\sqrt8&H\end{pmatrix}.
                                                               \tag{8}
\]
The zero in the first block uses balance. A cofactor or Schur identity gives
\[
\det(zI-H)
=f(z)e^T(zI-\operatorname{diag}(u))^{-1}e
=f(z)\frac18\sum_i\frac1{z-u_i}
=\frac{f'(z)}8=h(z).                                      \tag{9}
\]
These are rational identities, extended across apparent poles by
polynomial equality, including repeated original roots.
The scalar Schur complement gives
\[
\left(z-\frac18u^T(zI-H)^{-1}u\right)^{-1}=\frac{h(z)}{f(z)},
\]
hence
\[
\boxed{\ u^T(zI-H)^{-1}u=8\left(z-\frac{f(z)}{h(z)}\right).\ }   \tag{10}
\]
By the spectral theorem the left side is
\(\sum_{\lambda}m_\lambda/(z-\lambda)\).
If \(h\) is squarefree, its residue at \(\lambda_j\) proves (2).
If \(f(\lambda_j)=0\), the residue is zero; no division by an
original-root pole was used. Such a shared root is double because
\(f''(\lambda_j)=8h'(\lambda_j)\ne0\). Its block-sum-zero
compression eigenvector is orthogonal to \(u\).

Replacing \(f\) by \(f+\delta\) in the right side of (10) changes each
residue by \(-8\delta/h'(\lambda_j)\). Once real-rootedness has been
established, (10) identifies these algebraic residues with the actual
nonnegative masses of the new compression. Before that, they are signed
algebraic residues and cannot be treated as spectral masses.

## 3. Exactly which primitives are real-rooted

For monic squarefree \(h\) of degree seven,
\(\operatorname{sign} h'(\lambda_j)=(-1)^{7-j}\).
Thus odd-index criticals of \(f_\delta\) are strict local minima;
even-index criticals are strict local maxima.
The inequalities \(m_j+\delta\kappa_j\ge0\) say exactly
\[
f_\delta(\lambda_j)\le0\quad(j\ {\rm odd}),\qquad
f_\delta(\lambda_j)\ge0\quad(j\ {\rm even}).                \tag{11}
\]
They are precisely \(\ell\le\delta\le r\).

Necessity follows from real-root interlacing with multiplicities.
More explicitly, for distinct original levels \(t_i\) of multiplicities
\(n_i\), away from these levels
\[
\frac{f_\delta'}{f_\delta}=\sum_i\frac{n_i}{z-t_i}.
\]
This sum is strictly decreasing in every gap and has exactly one
simple zero there. At an original level the derivative multiplicity
is \(n_i-1\). This gives the usual ordered weak interlacing and the
alternating weak signs in (11).

For sufficiency, divide the real line into the eight monotonic arcs
separated by \(\lambda_1,\ldots,\lambda_7\). The polynomial tends to
positive infinity at both ends, and (11) supplies alternating weak signs.
Each closed monotonic arc therefore contains a zero. An interior zero
counts once. A zero at \(\lambda_j\) is exactly double, since the
second derivative is nonzero, and belongs to its two adjacent arcs.
Consecutive criticals cannot both be zeros: their value difference
is \(8\int_{\lambda_j}^{\lambda_{j+1}}h(x)\,dx\ne0\).
Consequently this argument counts at least eight real zeros with
multiplicity, and degree eight forces all roots to be real.
It covers singleton feasible intervals as well as ordinary endpoints.

The original primitive is real-rooted, so \(0\in I\), and both endpoints
in (3) are finite. An interior constant makes all inequalities strict;
there can then be no shared derivative/original root, so all eight
roots are distinct. At a finite endpoint one inequality is equality,
giving an original double root. No triple root is possible while
the derivative is squarefree.

The coefficients of \(z^7,\ldots,z\) of \(f_\delta\) are independent of
\(\delta\). Newton identities fix the first seven original power sums.
In particular balance, \(N\), the fourth power sum and \(D\) remain fixed.
This is why maximizing (1) is exactly minimizing the mass-square sum.

If \(h\) has a repeated root \(\lambda\), the gap argument above implies
that \(\lambda\) is an original root of multiplicity at least three.
Every other real-rooted primitive with the same derivative must also
have \(\lambda\) as an original root: a derivative zero in a strict gap
is simple. Hence \(f_\delta(\lambda)=f(\lambda)+\delta=\delta=0\).
This proves the degenerate fiber statement without inverting \(h'\).

## 4. Six moments, complete realization and constrained least squares

Lagrange interpolation on the seven distinct nodes gives
\[
\sum_{j=1}^7\frac{\lambda_j^k}{h'(\lambda_j)}
=\begin{cases}0&0\le k\le5,\\1&k=6.\end{cases}             \tag{12}
\]
Indeed compare the coefficient of \(z^6\) in the interpolation of
\(z^k\) by \(h(z)/[(z-\lambda_j)h'(\lambda_j)]\).
Thus \(V\kappa=0\), and the next moment's slope is exactly \(-8\).
The six-row Vandermonde matrix \(V\) has rank six, so
\(\ker V=\mathbb R\kappa\). Since \(Vm=\mu\), its entire solution
space is \(m+\mathbb R\kappa\), with a unique constant parameter.
By Section3, its intersection with the nonnegative orthant is exactly
the set of mass vectors of real-rooted \(f_\delta\), \(\delta\in I\).
This proves the realization assertion, not only a necessary moment bound.

The unique vector of least Euclidean norm in this affine line is
\[
v_*=V^TG_6^{-1}\mu=m+\delta_*\kappa,\qquad
\|v_*\|^2=R_6.                                           \tag{13}
\]
For completeness, \(VV^T\) is positive definite by rank six;
\(Vv_*=\mu\), and \(v_*\) is perpendicular to \(\ker V\).
Therefore it is the orthogonal projection of zero onto the affine line.
Expanding \(\|m+\delta\kappa\|^2\) and completing the square proves (6).
Restricting a strictly convex quadratic to the nonempty compact interval
\(I\) gives the unique clamped optimizer and (5), also when \(I\) is a singleton.

Equation (13) expresses \(v_{*,j}\) as a polynomial of degree at most five
evaluated at \(\lambda_j\). Equivalently, the unique degree-at-most-six
interpolation polynomial for the seven residues loses its degree-six
coefficient at the unconstrained optimum. The identity
\(\sum_j(m_j+\delta_*\kappa_j)\kappa_j=0\), after substituting (2),
is exactly (7). If this vector has a negative entry, it is outside
the nonnegative orthant and outside the real-rooted fiber.

## 5. Global consequence and remaining obligation

Start with any \(C(u)>T\). If the original roots already collide,
the collision alternative holds. Otherwise \(h\) is squarefree and
\(\ell<0<r\). Choose the clamped optimum in (5).
Its eight real roots have the same balance, norm and denominator, so
their \(C\) is at least the starting value. An endpoint gives a
collision; an interior optimum gives the strictly positive centered
profile described in (7),(13). Normalizing by the unchanged \(\sqrt N\)
preserves the unit-sphere domain. If the starting profile is itself a
global maximizer with distinct roots, strict convexity and \(0\in I^\circ\)
force \(\delta_*=0\); it already obeys the centered condition.

The exact fiber test for exceeding \(T\) is
\[
R_6+a\,\operatorname{dist}(\delta_*,I)^2<N^2-TD.            \tag{14}
\]
One can now work on the collision strata and the positive centered
eight-root stratum instead of all constant parameters. Neither stratum
is classified here. Positivity alone does not bound \(R_6\) sharply enough
to prove the global angular conjecture, and no completeness claim for
the remaining higher-level strata is hidden in this reduction.

### Explicit remaining eight-root stationarity equations

The centered condition is just one necessary direction. At a profile with
all eight original roots distinct, the following six equations are
**equivalent to first-order stationarity of \(C\)** on the balanced
fixed-\(N\) root sphere. They are not sufficient for a maximum.
For each \(q\in\{1,z,z^2,z^3,z^4,z^5\}\), with \(q_4=[z^4]q\), require
\[
\boxed{\ -16\sum_j\frac{m_jq(\lambda_j)}{h'(\lambda_j)}
-\frac14\sum_j\frac{m_j^2q''(\lambda_j)}{h'(\lambda_j)}
+\frac14\sum_j\frac{m_j^2h''(\lambda_j)q'(\lambda_j)}
                         {h'(\lambda_j)^2}
-4Cq_4=0.\ }                                             \tag{15}
\]
For \(q=1\) this reduces to constant-term centering.

To prove the statement, perturb \(f\) to \(f+tq\).
All sufficiently small positive and negative \(t\) preserve eight simple
real roots. Its \(z^7,z^6\) coefficients and thus balance and \(N\) are fixed.
The root-to-coefficient Jacobian is a nonzero Vandermonde, so these six
coefficient variations span the complete six-dimensional constrained
root tangent space. Writing
\(\dot\lambda_j=-q'(\lambda_j)/(8h'(\lambda_j))\), differentiating (2) gives
\[
\dot m_j=-\frac{8q(\lambda_j)}{h'(\lambda_j)}
 -\frac{m_jq''(\lambda_j)}{8h'(\lambda_j)}
 +\frac{m_jh''(\lambda_j)q'(\lambda_j)}{8h'(\lambda_j)^2}.
\]
Newton identities give \(D=3N^2/8-4[z^4]f\), hence
\(\dot D=-4q_4\), while
\(\dot\eta=2\sum_jm_j\dot m_j\).
Finally \(\dot C=-(\dot\eta+C\dot D)/D\), proving (15) and the equivalence.
The collision strata require their own feasible variations; an unrestricted
coefficient derivative there must not be mistaken for a legal two-sided
root variation.

## 6. Exact controls and a feasibility obstruction at high angular value

The standalone checker uses rational arithmetic in \(\mathbb Q[z]/h\).
It computes the entire polynomial inverse of \(h'\), and the polynomials
\(-8f/h'\) and \(-8/h'\) modulo \(h\).
Quotient-ring traces give \(\eta,a,b,\delta_*,R_6\).
It independently constructs the full seven-dimensional Gram compression
in the basis \(e_i-e_8\), with metric \(I+J\), and recovers:
the whole degree-seven characteristic polynomial, thirteen trace powers,
and seven coupling moments. Separate seven- and six-moment Gram solves
match the whole residue and centered interpolation polynomials, and have
positive exact elimination pivots. The complete quadratic coefficient
identity, six zero slopes and seventh slope \(-8\) are checked.
For each profile all six coefficient first derivatives of \(\eta\) are
computed twice: directly from the critical-root motion in (15), and
by exact arithmetic in the independent first-order algebra
\(\mathbb Q[\epsilon]/(\epsilon^2)\), using the moving polynomial quotient,
its entire inverse and Newton traces. All 36 derivatives agree exactly.
The \(C\) derivatives include the literal denominator term
\(-4[z^4]q\). At collision controls these are explicitly formal
coefficient derivatives, without an asserted two-sided legal deformation.

Every critical root is isolated both by the monotone scalar secular
equation and Sturm counts, with the inactive criticals at original doubles
inserted exactly. Direct masses \(64/\sum_i(u_i-\lambda)^{-2}\) at gap
criticals, and zero masses at original doubles, enclose the independently
computed residue masses and their entire square sum. Exact outward
160-bit dyadic bounds keep fixtures compact. All mathematical decisions
are rational comparisons, including sign classification and real-root counts.

The finite controls include:

* \(u=(-7,-5,-3,-1,1,3,5,7)\):
  \[
  \delta_*=-1294848/280993\in I^\circ,\quad
  C(0)=2901071152/323219671,\quad
  \max_I C=2522064/280993.
  \]
  All centered masses are strictly positive; the shifted polynomial has
  eight distinct real roots. A raw scaling by \(-3\) verifies the exact
  degree-eight constant scaling and all metric factors.
* \(u=(-856,-854,-852,-850,412,998,1000,1002)\):
  \[
  24.53<C(0)<(N^2-R_6)/D<24.532.
  \]
  Here \(\delta_*<\ell\), the centered mass at the second critical is
  strictly negative, and the unconstrained primitive has exactly six
  real roots and one nonreal conjugate pair. Thus even at high angular
  value unconstrained centering is not a legal original-root deformation.
  Both values remain below the previously known \(c_3>24.53389668\);
  this is no counterexample to \(C_*=c_3\) or to \(R_6\)-based bounds.
* \(u=(-86,-85,-85,-83,40,98,99,102)\):
  \(\ell=0<r\), \(\delta_*<0\), and the unique fiber optimum is
  \(\widehat\delta=0\). The original double at \(-85\) is the second
  critical, a local maximum. The feasibility penalty is strictly positive.
  Its actual optimum is \(C(0)\), descriptively \(24.37423559\ldots\).
  A certified positive step gives eight simple real roots, so one
  original double does not by itself imply a singleton fiber.
* \(u=(-86,-85,-85,-83,40,40,128,131)\):
  the double at \(-85\) is an even critical and that at \(40\) is an
  odd critical. Consequently \(\ell=r=0\), despite squarefree \(h\).
* \(u=(-5,-5,-5,1,2,3,4,5)\):
  \(\gcd(h,h')=z+5\). The repeated-derivative theorem gives \(I=\{0\}\);
  shifts \(\pm1/1000\) each have exactly six distinct real roots.
  The forbidden quotient inverse is rejected.

An additional distinct eight-root control and the signed/scaled control
bring the simple-critical checks to six profiles. Six internal damages
reject a wrong residue normalization, unconstrained positivity, ignored
clipping, an incorrect universal singleton claim for doubles, and
inversion at a repeated derivative, and omission of critical-root motion
from a coefficient derivative. Every external fixture field is
compared under normal and optimized Python. These controls corroborate
the ordinary proof; they do not formalize it or enumerate a global domain.

Reproduction and whole-record hash are in [README.md](README.md).
The compact exact fractions and every critical/mass enclosure are in
[expected.json](expected.json). There is no solver, floating predicate,
external certificate, large omitted corpus, or resource escalation.
