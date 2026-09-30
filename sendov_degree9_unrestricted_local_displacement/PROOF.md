# An explicit local displacement maximum with every slope free

Actual author **six-sendov-2**, role **researcher**, 2026-09-30.
Complete ordinary author proof with exact algebra controls. Independent
review of this extension is pending. No formalization is asserted.

## 1. Functional and precise result

For a nonzero balanced real eight-vector \(\theta\), put
\[
 \mu_k=\sum_j\theta_j^k,\quad e=\mathbf1/\sqrt8,\quad P=I-ee^*,
 \quad A=P\operatorname{diag}(\theta)P|_{e^\perp},\quad
 w=\operatorname{diag}(\theta)e,
\]
\[
 \Psi=\sum_{\lambda\in\operatorname{spec}(A)}\|\Pi_\lambda w\|^4,
 \qquad L(\theta)=122\mu_2+\frac{224\mu_4-5760\Psi}{\mu_2}.       \tag{1}
\]
The sum is over distinct eigenvalues with their full spectral projections.
Every algebraic multiplicity is retained; a collision eigenspace is not
split arbitrarily. The credited angular theorem gives
\(L=\mu_2K/p_8\), \(p_8=10985/33554432\), and continuity through
collisions. The displacement objective is \(L/\|\theta\|_\infty^2\).
We work on \(\|\theta\|_\infty=1\), and write this objective as \(J=L\).

Recall the credited scalar curve and optimizer
\[
 j(r)=\frac{2058+21912r-15876r^2+19224r^3+3402r^4}
                 {(3+r)(1+3r)^2},\qquad J_*=j(u_*),           \tag{2}
\]
where \(2/25<u_*<9/100\) is the unique global maximizing root on
\([0,1]\) of
\[
 T(r)=26634-231084r-907290r^2+376920r^3
                          +971190r^4+224532r^5+30618r^6.     \tag{3}
\]
The preceding four-block and scalar-face proofs establish this global
classification and \(J_*>5472/7>780\). They also establish
\[
                 J_*-j(r)\ge450(r-u_*)^2\quad(0\le r\le1/4). \tag{4}
\]
These scalar results are inputs, not new optimization claims here.

For a labelled balanced max-normalized vector set
\[
 \delta_i^+=1-\theta_i\ (i=1,2,3),\qquad
 \delta_i^-=1+\theta_{i+3}\ (i=1,2,3),
 \quad S=\sum_i(\delta_i^++\delta_i^-),
 \quad x=\frac{\theta_7-\theta_8}{2},\quad r=x^2.             \tag{5}
\]
Define the explicit local chart \(\mathcal N\) by
\[
 \sum_j\theta_j=0,\quad\|\theta\|_\infty=1,\quad
 0\le S\le\frac1{100000},\quad x\ge0,\quad
                       \frac2{25}\le r\le\frac9{100}.       \tag{6}
\]
Let \(\mathcal N^{\rm orb}\) be its permutations and sign reflections,
and let \(\mathcal O_*\) be the permutations of the unit-normalized
\(\theta_*=(1,1,1,-1,-1,-1,\sqrt{u_*},-\sqrt{u_*})\).
The opposite sign is already a permutation of this vector.

**Theorem 1 (all-balanced explicit local maximum).** Every vector in
\(\mathcal N\), with no equality or multiplicity conditions on its entries,
satisfies
\[
 \boxed{j(r)-J\ge200S,\qquad
        J_*-J\ge200S+450(r-u_*)^2.}                           \tag{7}
\]
Equality \(J=J_*\) occurs only at \(\theta=\theta_*\) in this chart.
Consequently \(\theta_*\) is a strict local maximum against **all** balanced
max-normalized eight-vectors, including arbitrary splitting of either
triple and profiles with eight distinct entries. Moreover
\[
 \boxed{\operatorname{dist}(\theta/\sqrt{\mu_2},\mathcal O_*)^2
                                \le\frac1{90}(J_*-J).}     \tag{8}
\]
The same conclusions hold in every relabelled chart. The exact first-order
normal-loss coefficient at the optimizer is \(J_*/3\), in the sense of
Section 6; the explicit coefficient 200 is conservative.

The new result is local and makes no structural reduction of the global
balanced polytope to the previously solved symmetric or 3+3+1+1 classes.

## 2. Three active eigenvalues and an analytic upper support

Consider the scalar leaf
\[
 \theta^0(x)=(1,1,1,-1,-1,-1,x,-x),\qquad 1/4\le x\le1/3.
\]
For \(H(t)=(t^2-1)^3(t^2-r)\), the classical compression determinant
identity gives \(\det(t-A)=H'(t)/8\). Indeed
\(e^*(t-D)^{-1}e=H'(t)/(8H(t))\), and the Schur determinant in the
decomposition \(\mathbb Re\oplus e^\perp\) gives the identity, extended
as a polynomial across repeated slope values. Direct differentiation yields
\[
 H'=2(t^2-1)^2[4t^3-(1+3r)t].                               \tag{9}
\]
Thus the compression has eigenvalues \(-1,1\), each twice, and the
three simple active values \(0,\pm\lambda\), where
\(\lambda=\sqrt{1+3r}/2\). The eigenspaces at \(\pm1\) consist of
zero-sum vectors supported inside their respective triples. They are
orthogonal to \(w\), so their weights vanish.

The secular residue \(-8H/H''\) gives the active weights
\[
 a_0=\frac{4r}{1+3r},\qquad
 a_+=a_- =\frac{3(1-r)^2}{8(1+3r)}.                         \tag{10}
\]
Substitution in (1) reproduces exactly (2). The checker verifies these
coefficient identities and checks the weights from full rational matrices.

Use the three fixed circles of radius \(1/8\) with centers
\(0,\pm9/16\) to select the active projections, and two circles of the
same radius centered at \(\pm1\) for the inactive clusters. Since
\[
 (43/80)^2<19/64\le\lambda^2\le1/3<(47/80)^2,
\]
the active eigenvalues lie within \(1/40\) of \(\pm9/16\).
Every active circle has distance at least \(1/10\) from the leaf spectrum;
each inactive circle has distance at least \(1/8\).

Let \(h\) be a balanced change, with \(\|h\|_\infty\le S\le1/40\),
such that every entry of the segment \(\theta^0+t h\), \(0\le t\le1\),
lies in \([-1,1]\). The compression perturbation has norm at most \(S\).
Eigenvalue perturbation for real symmetric matrices, or the resolvent
Neumann identity, keeps the active contour ranks one and the inactive
ranks two. The active resolvent norm is at most \(40/3\); the inactive
one is at most 10. This separation also holds in an open neighborhood
of each such segment. It makes the selected Riesz projections real
analytic functions of the entries, regardless of splitting inside the
inactive clusters.

Write \(a_i=\|\Pi_iw\|^2\) for the three active weights, and define
\[
 U(\theta)=122\mu_2+
          \frac{224\mu_4-5760\sum_{i=1}^3a_i^2}{\mu_2}.      \tag{11}
\]
On real balanced vectors \(L\le U\), because the discarded inactive
terms in \(\Psi\) are nonnegative. On the entire leaf \(U=L=j(r)\).
This is an **analytic upper support**, not an assumption that individual
projections inside a colliding cluster are analytic.

There is also uniform fourth-order contact. For each inactive cluster,
contour differentiation gives \(\|\Pi'\|\le(100/8)S\).
Since \(\|w\|\le1\), \(\|w'\|\le S\), and \(\Pi w=0\) at the leaf,
\(\|\Pi w\|\le14S\) throughout the segment. The sum of squared
weights of any subdivision of a cluster is at most its total weight
squared. Therefore, whenever \(\mu_2\ge5\),
\[
       0\le U-L\le\frac{5760}{5}\,2\,14^4 S^4
                                      <90000000 S^4.         \tag{12}
\]
This argument includes all inactive collisions and arbitrary splitting.

## 3. The full balanced gradient from symmetry and homogeneity

Extend the support locally off the balanced hyperplane by first centering
the vector. This extension is invariant under translation. At a leaf point,
permutations inside either triple preserve it; changing sign and swapping
the two triples and the singletons preserves it as well. The active
contours are exchanged under the sign change. Its ambient gradient is
therefore of the form
\[
                       (a,a,a,-a,-a,-a,d,-d).               \tag{13}
\]
Its entries sum to zero, agreeing with translation invariance.

Along the leaf, \(2d=\partial_xj(x^2)=2xj'(r)\).
The support is locally homogeneous of degree two: a scale sufficiently
close to one scales all corresponding spectral projectors without changing
which contours select them. Euler's identity gives
\(6a+2xd=2j(r)\). Consequently
\[
                  d=xj'(r),\qquad a(r)=\frac{j(r)-rj'(r)}3. \tag{14}
\]
The checker also derives every component on seven independent balanced
tangent axes using differentiated rational spectral projectors. This is a
different algebraic check of (14), without imposing equal changes inside
either triple. Finite controls supplement the symmetry proof, not replace it.

Let \(j_N,j_D\) be the numerator and denominator in (2). Then
\(T=j_N'j_D-j_Nj_D'\), and
\[
 3j_D^2(a-250)=j_Nj_D-rT-750j_D^2.                          \tag{15}
\]
All six rational Bernstein coefficients of this polynomial on
\([2/25,9/100]\) are strictly positive. They and the inverse conversion
are regenerated in verify.py and fully recorded in expected.json.
Since \(j_D>0\), this proves \(a(r)>250\) throughout this interval.
It is a continuous-domain certificate, not a grid of evaluations.

## 4. A conservative, explicit support Hessian bound

All derivatives here are along \(\theta(t)=\theta^0+t h\), and primes
refer to \(t\). The bounds use only \(\|h\|_\infty\le S\),
\(|\theta_j(t)|\le1\), and \(\mu_2\ge5\).
Resolvent differentiation on the active circles gives
\[
 \|\Pi_i'\|\le\frac{200}{9}S,\qquad
 \|\Pi_i''\|\le\frac{16000}{27}S^2.
\]
Thus
\[
 |a_i'|<25S,\qquad
 |a_i''|\le(2+800/9+16000/27)S^2<684S^2.
\]
The active projections are mutually orthogonal, so \(a_i\ge0\) and
\(\sum a_i\le\|w\|^2\le1\). For \(\tau=\sum a_i^2\),
\[
 \tau\le1,\quad |\tau'|\le50S,\quad
 |\tau''|\le2(3\cdot25^2+684)S^2<5200S^2.                 \tag{16}
\]
The moment bounds are
\[
 |\mu_2'|\le16S,\quad |\mu_2''|\le16S^2,\quad
 \mu_4\le8,\quad |\mu_4'|\le32S,\quad |\mu_4''|\le96S^2.
\]
With \(v=1/\mu_2\), \(v\le1/5\), \(|v'|<S\), and
\(|v''|\le(512/125+16/25)S^2<5S^2\). Product differentiation gives
\[
 |(\mu_4v)''|<124S^2,\qquad |(\tau v)''|\le1145S^2.
\]
In (11), these yield
\[
 |U''|\le(122\cdot16+224\cdot124+5760\cdot1145)S^2
                       =6624928S^2<6700000S^2.              \tag{17}
\]
Taylor's integral remainder is therefore at most \(3350000S^2\).
Every constant calculation is checked exactly. There is no floating
rounding premise or numerically estimated derivative in these estimates.

## 5. All coordinate changes, strictness and quantitative distance

For (5), let \(S_+=\sum\delta_i^+\), \(S_-=\sum\delta_i^-\).
Balance forces
\[
 y=\frac{\theta_7+\theta_8}{2}=\frac{S_+-S_-}{2},\quad
 \theta=\theta^0(x)+h,\quad
 h=(-\delta^+_1,-\delta^+_2,-\delta^+_3,
                    \delta^-_1,\delta^-_2,\delta^-_3,y,y).   \tag{18}
\]
Hence \(\|h\|_\infty\le S\), and the segment in Section 2 stays in
the box. Its squared norm is at least \(6-2S>5\). Both singleton
gradient terms cancel exactly; (14) gives \(DU[h]=-a(r)S\).
The support and Taylor bound imply
\[
 J\le U\le j(r)-250S+3350000S^2\le j(r)-200S               \tag{19}
\]
because \(S\le1/100000\). Combining with (4) proves (7).
If its right side vanishes, \(S=0\), balance gives \(y=0\), and
\(x=\sqrt{u_*}\); thus \(\theta=\theta_*\). Conditions (6) contain
a relative neighborhood of \(\theta_*\), since \(u_*\) is strictly
inside their scalar interval. This proves strict local maximality in
the whole balanced max-normalized domain.

For the distance bound, set \(b_*=\sqrt{u_*}\). The singleton common
shift is orthogonal to their difference shift, so
\[
 \|\theta-\theta_*\|^2
 =\sum(\delta_i^+)^2+\sum(\delta_i^-)^2+2y^2+2(x-b_*)^2
 \le\tfrac32S^2+\tfrac{25}{4}(r-u_*)^2.
\]
Here \((x+b_*)^2\ge8/25\), and \(S^2\le S\). Formula (7) gives
\(\|\theta-\theta_*\|^2\le(J_*-J)/72\). Adding and subtracting
\(\theta_*/\|\theta\|\), then using the reverse triangle inequality,
gives the normalization bound
\[
 \left\|\frac\theta{\|\theta\|}-
              \frac{\theta_*}{\|\theta_*\|}\right\|^2
 \le\frac4{\|\theta\|^2}\|\theta-\theta_*\|^2
 \le\frac1{90}(J_*-J).
\]
Minimizing over the orbit proves (8). In particular, within this explicit
neighborhood, a deficit \(D\) forces \(S\le D/200\), squared scalar
deviation at most \(D/450\), and singleton common shift at most \(D/400\).

## 6. Sharp normal coefficient and a broader local phase basin

At \(r=u_*\), (14) gives \(a=J_*/3\), \(d=0\). The balanced path
\[
 \theta(s)=(1-s,1,1,-1,-1,-1,b_*+s/2,-b_*+s/2),\qquad s\downarrow0,
\]
stays max-normalized, has \(S=s\), and keeps \(r=u_*\). Equations
(12), (14), and analytic Taylor expansion give
\[
                   J(\theta(s))=J_*-\frac{J_*}{3}s+O(s^2). \tag{20}
\]
Thus no larger uniform first-order coefficient multiplying \(S\) can
hold in every neighborhood at fixed \(r=u_*\). More generally every
\(c<J_*/3\), \(c>0\), can replace 200 on a sufficiently small
neighborhood, by continuity of \(a(r)\) and (17). The effective chart
(6) and coefficient 200 do not require such an unspecified shrinkage.

There is a polynomial corollary using the credited all-disk variational
reduction. Let \(p(z)=c(z-a)\prod_{j=1}^8(z-z_j)\), \(c\ne0\),
have a simple marked root \(0<a<1\) and all roots in the closed unit disk.
For \(\rho=\max|z_j+1|\le1/2\), write uniquely
\(z_j=-(1-\tau_j)e^{i\phi_j}\) with \(-\pi/2<\phi_j<\pi/2\).
Require that the nonzero centered phase vector, after max normalization,
lies in \(\mathcal N^{\rm orb}\). This imposes **no repeated-phase or
equal-inward-depth condition**. Define
\[
 G=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}-\frac{16}{1+a},\quad
 \kappa=(1+a)(a-5/8),
\]
and let \(R_{\mathcal N}(a)\) be the supremum of \(0\le q\le1/2\)
for which every polynomial in this direction class with \(\rho\le q\)
has \(G\ge0\). Count every critical multiplicity. The simple marked
root makes the sum finite. We do not assert endpoint admissibility.

**Theorem 2 (locally unrestricted complex phase basin).**
\[
 \boxed{\lim_{a\downarrow5/8}\frac{R_{\mathcal N}(a)^2}{\kappa}
     =B_*=\frac{106496}{5J_*},\quad
                          27.106707<B_*<27.106708.}          \tag{21}
\]
The coefficient and matching symmetric upper family are prior inputs;
the extension here removes every phase-multiplicity condition in the
specified explicit angular neighborhood.

For completeness, the cited reduction supplies the following uniform
statements on a negative-gap sequence tending to collapse. Write
\(T_0=\sum\tau_j\), \(M=\sum\phi_j\), \(L_0=\sum\phi_j^2\),
\(s=\|\phi-(M/8)\mathbf1\|\), and
\(\widehat\theta=(\phi-(M/8)\mathbf1)/s\). Its bootstrap gives
\(T_0=O(L_0^2)\), \(M^2=O(L_0^2)\), \(\kappa=O(L_0)\).
With \(E=\sum|(a-z_j)^{-1}-(1+a)^{-1}|^2\), \(d_0=13/8\), and
\(q=\|\widehat\theta\|_\infty^2\ge1/8\), its joint expansion is
\[
 G=\kappa E+\frac{128}{169}T_0+\frac{40}{2197}M^2
                              -K(\widehat\theta)E^2+o(E^2),
 \qquad \rho^2=s^2q+O(s^3),\quad E=d_0^{-4}s^2+O(s^4).     \tag{22}
\]
Theorem 1 gives \(K(\widehat\theta)/q\le p_8J_*\). Negativity and
(22) imply \(\kappa d_0^4/\rho^2\le p_8J_*+o(1)\), contradicting
any sequence of failures at \(\rho^2\le(B_*-\varepsilon)\kappa\),
\(0<\varepsilon<B_*\). Sequential contradiction proves uniform
sufficiency and the lower limit.

The credited actual family
\[
 (z-a)(z^2+2\cos t\,z+1)^3
                 (z^2+2\cos(\sqrt{u_*}t)\,z+1)
\]
has centered direction \(\theta_*\), and gives \(G<0\) at
\(\rho^2=\lambda B_*\kappa+O(\kappa^2)\) for every \(\lambda>1\).
These radii are below \(1/2\) eventually. This proves the upper limit
and (21), without deciding the sign at the crossing itself.

For a negative sequence in this class with \(\rho^2/\kappa\to B_*\),
divide (22) by \(E^2\). The nonnegative angular deficit, inward term
and mean term must all vanish. Formula (8) gives convergence of the
unit direction to \(\mathcal O_*\), with \(T_0/E^2,M^2/E^2\to0\)
and \(G/E^2\to0\). No numerical original-root energy threshold or
remainder rate is claimed by this corollary.

## 7. What is checked, what is cited, and what remains open

verify.py uses exact rational arithmetic only. It checks the full scalar
polynomial and secular-weight identities, the six new normal-gradient
Bernstein coefficients and inverse reconstruction, the credited scalar
curvature reproduction, every rational resolvent/Hessian constant, and
the full seven-dimensional tangent gradient at four rational leaf points.
The latter controls construct all spectral projectors from the actual
8 by 8 compression and differentiate them by reduced resolvents.
They supply an independent algebraic route within the author's code;
they are not independent peer review or a finite substitute for the
analytic continuum argument.

The Riesz projection calculus, symmetry, positivity of omitted weights,
contour separation, norm bounds and local coverage are ordinary written
mathematics. The angular interpretation, scalar global optimizer,
collision continuity, joint all-disk expansion, original-root metric
conversion and matching family are credited in LITERATURE.md.

The unrestricted **global** displacement optimizer, its full complex
basin, effective original-root neighborhoods and the global first-power
Tang--Zhang endpoint remain unresolved here. At \(a=5/8\) the comparison
\(16/(1+a)=128/13\) exceeds 8; a negative local comparison gap is not a
first-power counterexample. No historical-priority claim is made.
