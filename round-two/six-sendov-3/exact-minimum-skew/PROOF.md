# Exact skew optimizers above the true degree-nine boundary minimum

Actual author **six-sendov-3**, role **researcher**, 2026-10-05.
Complete ordinary author proof, unformalized and independently unreviewed.
The finite algebra certificate establishes only the explicitly identified
coefficient, matrix and sign identities. All collars below are existential.

## 1. Statement, normalization and credited premises

Let \(\mathcal P_\eta\) be the class of all complex monic polynomials of
exact degree nine, with all nine original roots in the closed unit disk and
with marked root \(a=1-\eta>0\). For their eight critical points, counted
with algebraic multiplicity, define

\[
 F(p)=\sum_{j=1}^8|a-\zeta_j|^{-1},\qquad
 \lambda(p)=\eta^{-2}\sum_{j=1}^8(\Im\zeta_j)^3.                 \tag{1}
\]

A zero reciprocal denominator means infinity. No separation hypothesis is
imposed on a competitor's original or critical roots. Write \(m(\eta)\)
for the attained minimum of \(F\) over the entire class, and \(p_\eta\)
for its unique minimizer in the sufficiently small boundary collar.
These exact global objects are credited inputs, not reconstructed from
a finite Taylor polynomial in this proof.

Put

\[
\begin{gathered}
 c=\cos(\pi/9),\quad H=\frac{14}{3(1+c)},\quad b^2=H/2,\\
 a_T=-\frac{11564}{405}-\frac{20482}{81}c+\frac{123284}{405}c^2,
 \quad b_T=\frac{49}{180}-\frac{105889}{486}c+\frac{305123}{1215}c^2,\\
 \gamma=\frac{4(a_T+6b_T)}{27H^3}>0.                           \tag{2}
\end{gathered}
\]

**Theorem.** There are real analytic functions \(\mathcal R,U,V\),
defined on a neighborhood of \((0,0)\), independent of the budget constant,
with

\[
 \mathcal R(0,0)=1,\qquad U(0,0)=-\frac1{9H},                 \tag{3}
\]

such that the following holds. For every finite \(D\ge0\) there is
\(\eta_D>0\) so that, simultaneously for all \(0<\eta<\eta_D\)
and all \(0\le g\le D\eta^3\), both the exact level
\(F=m(\eta)+g\) and the cap \(F\le m(\eta)+g\) are nonempty and
have the same attained maximum of \(|\lambda|\), namely

\[
 S(\eta,g)=\sqrt{\frac{g}{\gamma\eta^3}}
       \mathcal R\!\left(\eta,\frac{g}{\gamma\eta^2}\right).   \tag{4}
\]

The value at \(g=0\) is exactly zero. For \(g>0\), the positive
\(\lambda\) maximizer is a unique monic polynomial, and the negative
maximizer is its complex conjugate. They are distinct and are exactly
the two maximizers of \(|\lambda|\). Every maximizer spends the full
budget and has exactly the four original roots near
\(e^{\pm2\pi i/3}\) and \(e^{\pm8\pi i/9}\) on the unit circle.
The other five original roots, including the marked root, are strictly
inside, and all nine originals of these maximizers are simple.

Each maximizer has exactly one critical point of multiplicity six and
two other distinct simple critical points. To specify the common small
critical point, set

\[
 r=\sqrt{\frac{g}{\gamma\eta^2}},\quad \sigma=r^2,
 \qquad \zeta_j=\eta u_j+i\sqrt\eta h_j.
\]

For the positive \(\lambda\) maximizer its six small coordinates satisfy
exactly

\[
 h_3=\cdots=h_8=rU(\eta,\sigma),\qquad
 u_3=\cdots=u_8=u_0(\eta)+\sigma V(\eta,\sigma).              \tag{5}
\]

Here \(u_0\) is the exact analytic small-real critical coordinate of the
credited global minimizer. The negative maximizer negates the imaginary
coordinates and keeps the real ones. At \(g=0\) the single optimizer is
\(p_\eta\), with its credited real six-fold critical point and nonreal
conjugate pair. For \(g>0\) this proof does not assert that the two large
critical points are a conjugate pair.

In particular, uniformly for all positive gaps in the stated range,

\[
 S(\eta,g)=\sqrt{\frac{g}{\gamma\eta^3}}\,[1+O_D(\eta)].     \tag{6}
\]

No positive lower bound on \(g/\eta^q\), for any \(q\), is required.
Thus (4)--(6) cover gaps that vanish faster than every power, as well as
the exact zero-gap case. They compare with the true minimum, not a
truncated surrogate. They do not decide which side of \(m\) an unpaid
next Taylor endpoint lies on, give an effective collar, or settle the
first-power inequality at interior radii.

The direct substantive premises are:

* [Committed lemma8921, analytic-boundary, source ac6099018ea9e0e8e3092122db6ff24d549ebf32](https://github.com/helgithorskarp/math_results/blob/ac6099018ea9e0e8e3092122db6ff24d549ebf32/round-two/six-sendov-3/analytic-boundary/PROOF.md),
  by six-sendov-3: the exact global minimum, full analytic four-normal
  inverse chart, all-original-root feasibility, uniform all-competitor
  entry for every fixed cubic budget, and the error-free gap inequality.
* [Committed independent review8955, source af8744b970f35769564fba7cb7c53377281661ca](https://github.com/helgithorskarp/math_results/blob/af8744b970f35769564fba7cb7c53377281661ca/round-two/six-reviewer-1/analytic-minimizer-audit/REVIEW.md),
  by six-reviewer-1: confirms that theorem relative to its explicitly
  inherited concentration7190 and second-optimum8619/review8684 inputs,
  and independently reconstructs the entire tangent matrix used here.

Those inherited hypotheses remain premises. Their global concentration
and uniform inverse-map bridges are not newly proved by this finite
checker. Fourth coefficient8841/review8883 retain prior credit for the
tangent coefficients and limiting real-splitting constant, already
carried by8921/8955. Neither the later author fifth/sixth coefficient
sources, the private seventh coefficient, nor a constructed-family-only
calculation is a premise of this theorem. An ancestor review supplies
no independent verdict on this new optimizer theorem.

## 2. The full chart and the exact centered functions

Here is the part of the credited chart required for the argument.
The six free small critical coordinates are
\(z=(h_3,\ldots,h_8,u_3,\ldots,u_8)\in\mathbb R^{12}\).
The other two criticals are specified by the normal coordinates
\(U,H',V',M\) through

\[
\begin{gathered}
 m_h=(\eta V'-\textstyle\sum_{3}^8h_j)/2,
 \quad s_h=\sqrt{(H'-\sum_{3}^8h_j^2)/2-m_h^2}>0,\\
 h_1=m_h+s_h,\quad h_2=m_h-s_h,\qquad
 m_u=(U-\textstyle\sum_{3}^8u_j)/2,\\
 d_u=(M-2m_hm_u-\sum_{3}^8h_ju_j)/(2s_h),\qquad
 u_1=m_u+d_u,\quad u_2=m_u-d_u.                              \tag{7}
\end{gathered}
\]

The normal inverse is real analytic in \((\eta,E_3,E_4,O_3,O_4,z)\)
near the reference \((0,0,0,0,0,z_*)\), where
\(z_*=(0^6,u_z^6)\), \(s_h=b\). Its four coordinates refer to the
four *actual*, independently variable original-root half-normals
\(a_k^\pm=(|Z_k^\pm|^2-1)/2\):

\[
 a_k^\pm=\eta E_k\pm\eta^{3/2}\sin(2\pi k/9)O_k,
 \qquad k=3,4.                                              \tag{8}
\]

For each small positive \(\eta\), (7), the normal inverse and the full
anchored integral \(p(z)=\int_{1-\eta}^z9\prod_j(w-\zeta_j)\,dw\)
determine an actual monic polynomial. Throughout one fixed small chart
neighborhood, nonpositivity of the four half-normals implies all nine
originals are in the disk. The four other unmarked originals have
uniformly negative leading radial slopes and the marked original is
exactly \(1-\eta\). These roots are the nine disjoint simple root maps
near the ninth roots of unity. This feasibility statement holds for
arbitrary complex free coordinates, including collisions among the
six small criticals. No analytic critical labeling for a competitor
is assumed.

Let \(\mathcal F\) denote the exact objective in this inverse chart,
and \(J=\sum_{j=1}^8 h_j^3\). Both are real analytic in the chart
variables, including \(\eta=0\). The exact identity (1) is
\(\lambda=\eta^{-1/2}J\). The credited objective decomposition is

\[
 \mathcal F=8+\eta(C-W_3E_3-W_4E_4)+\eta^2\widetilde G,
 \quad W_4=\frac1{c+2c^2-1},\quad
 W_3=\frac23[7-(2-2c^2)W_4]>0.                              \tag{9}
\]

All required derivatives of \(\widetilde G,J\) are bounded on a
smaller fixed product neighborhood. Holding \(z\) fixed, (8),(9) give
uniformly

\[
 \mathcal F_{a_k^\pm}=-W_k/2+O(\sqrt\eta),\qquad
 |J_{a_k^\pm}|\le K\eta^{-3/2}.                            \tag{10}
\]

In particular each objective derivative is bounded above by a fixed
negative constant. The second bound follows by the chain rule from
the bounded \(E,O\) derivatives and (8); it need not be sharp.

On the exact boundary stratum \(E=O=0\), write

\[
 F_0(\eta,z)=8+C\eta+\eta^2G(\eta,z),\qquad J_0(\eta,z)=J(\eta,0,0,z).
\]

The exact minimizer is at the analytic point
\(z_\eta=(0^6,u_0(\eta)^6)\), with
\(\nabla_zG(\eta,z_\eta)=0\), \(J_0(\eta,z_\eta)=0\), and
\(m(\eta)=F_0(\eta,z_\eta)\). For every fixed cubic budget the
credited all-competitor gap, with fixed \(\delta,c_0>0\), is

\[
 F-m(\eta)\ge\delta\sum_{k,\pm}(-a_k^\pm)
                    +c_0\eta^2\|z-z_\eta\|^2.              \tag{11}
\]

Its uniform chart inclusion and labeling hold over every competitor
in that budget. Since \(m=8+C\eta+B_*\eta^2+O(\eta^3)\), the entire
cap \(F\le m+D\eta^3\) is one such fixed cubic budget. A single
common collar can therefore be chosen for each finite \(D\).

## 3. The full sharp quadratic form and cubic derivative

For raw free displacement \(d=(x,y)\in\mathbb R^6\oplus\mathbb R^6\),
the credited full tangent cost and the literal cubic derivative are

\[
\begin{aligned}
 Q(d)&=\frac{a_T}{b^2}\sum x_i^2+
       \frac{b_T}{b^2}(\sum x_i)^2+
       \frac12\sum y_i^2+\frac14(\sum y_i)^2,\\
 L(d)&=-\frac{3H}{2}\sum x_i.                              \tag{12}
\end{aligned}
\]

Thus, uniformly near the exact minimum,

\[
 \frac{F_0(\eta,z_\eta+d)-m(\eta)}{\eta^2}
   =Q(d)+O(\eta\|d\|^2+\|d\|^3),\quad
 J_0(\eta,z_\eta+d)=L(d)+O(\eta\|d\|+\|d\|^2).             \tag{13}
\]

For the new second identity, at \(\eta=0,E=O=0\), the chart imposes
\(\sum h_j=0\), \(\sum h_j^2=H\). Put
\(S=\sum_3^8h_j\), \(T=\sum_3^8h_j^2\). Then
\(m_h=-S/2\), \(s_h^2=(H-T)/2-S^2/4\), and the whole all-eight
cubic, including the two large points and all six small multiplicities,
is exactly

\[
 J_0(0,z)=2m_h^3+6m_hs_h^2+\sum_3^8h_j^3
       =-\frac{3H}{2}S+\frac32ST+\frac12S^3+\sum_3^8h_j^3.   \tag{14}
\]

This proves the derivative \(L\), with no construction-family
restriction. The whole coefficient identity is separately checked.

Write \(Q(d)=d^TAd\), \(L(d)=l^Td\), and put
\(e=(-(9H)^{-1}\mathbf1_6,0^6)\). Direct exact identities give

\[
 l^Te=1,\quad Ae=\gamma l,\quad e^TAe=\gamma,
\]
\[
 Q(x,y)=\gamma L(x,y)^2+
        \frac{a_T}{b^2}\sum(x_i-\overline x)^2+
        \frac12\sum y_i^2+\frac14(\sum y_i)^2.              \tag{15}
\]

Here \(a_T>0\), \(a_T+6b_T>0\). The real block is positive
definite, so \(A\) is positive definite. Consequently the unique
maximizer of \(L\) under \(Q\le\gamma\) is exactly \(e\), with
maximum one. Equality exhausts all cost and annihilates the entire
variance and real blocks. This is an all-twelve-variable conclusion.

The finite certificate freshly reconstructs the known tangent matrix
from the literal finite chart cost in all twelve axes and all sixty-six
pair sums, rather than assuming the displayed invariant matrix. Its
entries and those of (15) are compared in full. Exact arithmetic in
\(\mathbb Q[c]/(8c^3-6c-1)\), with the physical root isolated in
\(15/16<c<47/50\), verifies every stated matrix identity and sign.
Reproducing the known matrix is validation, not new research.

## 4. Uniform entry of every maximizing competitor, even for flat gaps

Fix finite \(D\) and initially \(g>0\). Set
\(r=\sqrt{g/(\gamma\eta^2)}\); then
\(0<r\le\sqrt{D/\gamma}\sqrt\eta\). For every competitor in the
cap, (11) permits the definitions

\[
 z-z_\eta=rw,\qquad a_k^\pm=-\eta^2r^2\ell_k^\pm,
 \qquad \ell_k^\pm\ge0,                                   \tag{16}
\]

with \(w\) and all four \(\ell\)'s uniformly bounded. These bounds
do not divide an uncontrolled Taylor remainder by a small \(g\):
they follow from the exact, error-free inequality (11).
Equation (8) then gives \(E=O(\eta r^2)\) and
\(O=O(\sqrt\eta r^2)\). Integrating (10) at fixed \(z\), and using
(13) and bounded analytic derivatives for \(J\), gives uniformly

\[
 \frac{F-m}{\eta^2r^2}
     =Q(w)+\sum_{k,\pm}\frac{W_k}{2}\ell_k^\pm+o(1)
     \le\gamma,
 \qquad \frac{J}{r}=L(w)+o(1).                              \tag{17}
\]

For example the cost errors are bounded by a fixed multiple of
\(\eta+r+\sqrt\eta\) on these bounded sets, and the additional
normal contribution to \(J/r\) is \(O(\sqrt\eta r+\eta r)\).
They tend to zero uniformly over every positive gap in the cap range,
however flat its dependence on \(\eta\).

There is an actual, exactly level-feasible lower witness for each gap.
Define the following analytic functions, extended at \(r=0\):

\[
 A_*(\eta,r,w)=\frac{G(\eta,z_\eta+rw)-G(\eta,z_\eta)}{r^2},
 \quad B_*(\eta,r,w)=\frac{J_0(\eta,z_\eta+rw)}r.             \tag{18}
\]

The constant and linear terms in the first numerator vanish by exact
stationarity; the constant term in the second vanishes by symmetry of
the exact minimizer. Taylor's integral formula proves convergent real
analytic divisibility, with
\(A_*(0,0,w)=Q(w)\), \(B_*(0,0,w)=L(w)\).
Applying the scalar analytic implicit function theorem to
\(A_*(\eta,r,te)=\gamma\) at \((0,0,1)\) is valid since its
\(t\) derivative there is \(2\gamma\). It yields an analytic
\(t=1+o(1)\), giving an actual zero-slack polynomial at
\(F=m+g\) and with \(J/r=1+o(1)>0\).

The maximum exists. For fixed \(\eta\), the class \(\mathcal P_\eta\)
is a compact coefficient set, being the continuous image of the
compact eight-unmarked-root disk product with the marked factor
anchored. Critical multisets depend continuously on coefficients.
The objective, extended by infinity at a zero denominator, is lower
semicontinuous. Hence the finite cap is closed and compact; it is
nonempty by the witness. The cubic sum is a continuous symmetric
function of that multiset, so has an attained maximum on the cap.
No differentiable labeling at critical collisions is needed.

Every positive \(J\) maximizing competitor satisfies, uniformly,

\[
 w\longrightarrow e,\qquad \ell\longrightarrow0.             \tag{19}
\]

Indeed otherwise choose a sequence \(\eta\downarrow0\) and positive
gaps in the range, and extract bounded limits in (16). The witness
forces \(L(w)\ge1\), while (17) and (15) force
\(\gamma L(w)^2\le Q(w)\le\gamma\). Thus \(L(w)=1\),
all terms in the remainder of (15) vanish, every positively weighted
slack vanishes, and \(w=e\), a contradiction. This compactness
argument establishes common uniform entry, not only entry along a
prescribed fixed-power path.

## 5. Exact budget exhaustion and exact removal of all four radials

Near the maximizing profiles (19), analyticity, (9),(12),(13) give
the following derivative estimates at fixed physical half-normals:

\[
 \mathcal F_z[e]=2\gamma\eta^2r[1+o(1)]>0,
 \qquad J_z[e]=1+o(1)>0.                                   \tag{20}
\]

To justify the first when the radials are nonzero, its boundary value
is \(\eta^2[2(A(z-z_\eta))\cdot e+
O(\eta\|z-z_\eta\|+\|z-z_\eta\|^2)]\).
The difference of \(\widetilde G_z\) between nonzero and zero normals
is \(O(\|E\|+\|O\|)=O(\sqrt\eta r^2+\eta r^2)\).
Divide by \(r\) and use (19) and \(Ae=\gamma l\) to obtain (20).
The second estimate follows from the bounded derivatives of \(J\).
All these errors are uniform in the stated range, including flat gaps.

If a cap maximizer has \(F<m+g\), a sufficiently small free change
\(z\mapsto z+te\), keeping the four physical radials fixed,
increases \(J\) and remains below the cap by (20). The chart still
gives actual disk-contained originals, a contradiction. Thus every
maximizer has \(F=m+g\).

Now suppose some individual physical half-normal \(a_j<0\).
Increase just that coordinate to \(a_j+s\) for a sufficiently small
positive \(s\), keep the other three fixed, and adjust the free
coordinates to \(z+t(s)e\). The ordinary implicit function theorem
using (20) uniquely keeps \(F=m+g\). At \(s=0\),

\[
 t'(0)=-\frac{\mathcal F_{a_j}}{\mathcal F_z[e]}
      \ge \frac{k_1}{\eta^2r},\qquad
 \frac{dJ}{ds}=J_{a_j}+J_z[e]t'(0)
      \ge-K\eta^{-3/2}+\frac{k_2}{\eta^2r}>0.                \tag{21}
\]

The constants are fixed positive numbers in a sufficiently small
collar. The last strict inequality follows from
\(\sqrt\eta r\le\sqrt{D/\gamma}\eta\to0\). Choose
\(s<-a_j\) and small enough that the local adjustment stays in the
fixed chart; such a positive \(s\) exists even when the radial slack
is arbitrarily tiny. All active roots stay in the disk and all five
inactive originals remain strictly inside. This produces an actual
polynomial at the same exact objective level with larger \(J\), a
contradiction. Thus every maximizing competitor has

\[
 a_3^+=a_3^-=a_4^+=a_4^-=0.                                \tag{22}
\]

This exhaustion is exact at each permitted positive gap. It is not
an inference of zero slack from the asymptotic limit (19), and does
not assume conjugate symmetry or an active-constraint multiplier
qualification.

## 6. The analytic maximum and its uniqueness in all twelve variables

By (22), all maximizers lie on the boundary stratum, where the
normalized problem is to maximize \(B_*\) subject to
\(A_*=\gamma\). By (19), its free coordinate \(w\) is near \(e\).
The constraint gradient is nonzero there, so a maximizer satisfies

\[
 \nabla_w B_*-\tau\nabla_w A_*=0,\qquad A_*=\gamma.          \tag{23}
\]

At \((\eta,r,w,\tau)=(0,0,e,1/(2\gamma))\), these equations
hold by (15). Their full thirteen-variable Jacobian with respect to
\((w,\tau)\) is

\[
 \mathcal J=
 \begin{pmatrix}-A/\gamma&-2Ae\\2e^TA&0\end{pmatrix},
 \qquad \det\mathcal J=-\frac{4\det A}{\gamma^{10}}<0.       \tag{24}
\]

For clarity, the Schur complement of the upper block is
\(-4\gamma^2\), since \(e^TAe=\gamma\), and the upper-block
determinant is \(\det A/\gamma^{12}\). The finite checker retains
every entry of this bordered matrix and compares its Gaussian
determinant to (24), rather than checking an assumed two-coordinate
restriction. The determinant of the full cost matrix is

\[
 \det A=(a_T/b^2)^5((a_T+6b_T)/b^2)/16>0.                   \tag{25}
\]

The analytic implicit function theorem therefore yields a unique
analytic branch \((w(\eta,r),\tau(\eta,r))\) near \((e,1/(2\gamma))\).
This is the unique global positive maximum throughout the required
common collar. To see the global assertion, every attained cap
maximizer has already entered an arbitrarily small neighborhood of
\(e\) uniformly by (19). Its multiplier is close to \(1/(2\gamma)\):
take the inner product of (23) with \(e\), whose denominator
\(\nabla A_*\cdot e\) tends to \(2\gamma\), while its numerator
tends to one. Thus every maximizer enters the uniqueness neighborhood
of the full implicit branch. Existence was proved separately in
Section4, so this step does not mistake a local stationary point for
a global maximum. The branch reconstructs an actual polynomial
uniquely through the normal inverse and anchored monic integral.

The same exact-level witness and the global budget exhaustion show
that the level and cap maxima agree. Conjugation preserves the disk
class and \(F\), and negates \(J\); it supplies the unique negative
maximizer. Positive \(J\) is nonzero by the witness, so these two
polynomials are distinct. The zero-gap case is the credited unique
global minimizer and requires no division by \(g\) or \(r\).

## 7. Symmetry, the even analytic peak and exact critical coalescence

All six-small-critical permutations preserve the exact chart,
\(F_0,J_0\), the point \(z_\eta\), and the axis \(e\). Uniqueness
in (23) forces the analytic branch to be fixed by every such
permutation. Hence its six imaginary coordinates coincide exactly,
and its six real coordinates coincide exactly. For positive \(\eta\)
this means an actual complex critical point of multiplicity six;
the two large criticals are separate from it and from one another
because \(h_1\to b\), \(h_2\to-b\).

On the boundary stratum conjugation, with the two large labels
exchanged, acts on free coordinates as
\(T(h,u)=(-h,u)\). Thus
\(F_0(\eta,Tz)=F_0(\eta,z)\),
\(J_0(\eta,Tz)=-J_0(\eta,z)\), and \(Tz_\eta=z_\eta\).
Set \(R(h,u)=(h,-u)\) on free *displacements*, so \(T=-R\).
The exact analytic functions (18), including their divided extensions,
satisfy

\[
 A_*(\eta,-r,Rw)=A_*(\eta,r,w),\qquad
 B_*(\eta,-r,Rw)=B_*(\eta,r,w).                             \tag{26}
\]

These equalities preserve (23), its multiplier and its base point.
Uniqueness therefore gives \(w(\eta,-r)=Rw(\eta,r)\).
The imaginary part of \(w\) is even in \(r\); its real part is odd.
Their common components can consequently be written as
\(U(\eta,r^2)\), \(rV(\eta,r^2)\), respectively, with convergent
real analytic functions on a neighborhood of \((0,0)\).
This follows by taking the even/odd terms of the convergent local
power series; it is not a formal series conclusion.

The peak
\(B_*(\eta,r,w(\eta,r))\) is likewise even in \(r\), so equals
\(\mathcal R(\eta,r^2)\), analytic with value one at zero.
Together with \(\lambda=\eta^{-1/2}J\) and (18), this proves the
exact formula (4) and the coordinate description (5). Analyticity
gives \(\mathcal R(\eta,\sigma)=1+O(|\eta|+|\sigma|)\).
Since \(0\le\sigma\le(D/\gamma)\eta\), the error is
\(O_D(\eta)\), uniformly including arbitrarily flat positive gaps.
The expression itself extends to \(g=0\) with the exact value zero.

For a marked root with arbitrary nonzero phase, rotate the polynomial
so the marked root is positive real and use (1) in that frame.
Nonzero scalar multiplication has no effect on roots or objectives.
Transporting the monic equality classification by these operations
gives the corresponding classification for arbitrary leading scalar
and phase. No extra critical ordering is part of that classification.

## 8. Evidence, prior art and remaining obligations

The finite certificate uses only exact Python standard-library rational
arithmetic. Its characteristic-zero coefficient field is
\(\mathbb Q[c]/(8c^3-6c-1)\), normal form \((1,c,c^2)\); the
polynomial is irreducible by the rational-root criterion. Root isolation
uses the strictly increasing cubic on the stated positive bracket.
The known finite tangent is reconstructed in 78 literal directions,
which determine all 144 entries by quadratic polarization. The new
rank-one remainder, maximizing axis, entire 169-entry bordered
Jacobian, whole all-eight cubic and ten strict signs are checked in
full. Determinant signs use the checked factorizations (24),(25) and
positive rational interval factors, avoiding cancellation in expanded
inverse powers. Exact field identity with the previously used
\(\gamma=\kappa/H\) is a compatibility check only; no later
Taylor-coefficient theorem is imported.

The ordinary compactness, root-map feasibility, global chart entry,
analytic divisions, derivative estimates, exact slack exhaustion,
global-to-local uniqueness and convergent symmetry descent are outside
a formal proof kernel. They are written above and rely precisely on
8921/8955 and their disclosed inherited premises. Validation of a
finite record is not independent mathematical review of this theorem.
No floating-point search, solver, unknown result, interrupted job or
incomplete enumeration is a premise.

[The current first-power paper](https://arxiv.org/html/2609.19126),
Conjecture1.2, formulates the reciprocal-power family; its strongest
first-power endpoint remains distinct from the proved quadratic and
higher-power cases. [Tao's exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
gives the stronger-family context. Both were rechecked live on
2026-10-05. [Miller, Theorem1](https://arxiv.org/pdf/math/0505424v3),
already uses a repeated degree-six real critical factor plus a quadratic
factor in degree nine for a different nearest-critical objective.
That derivative template has prior credit. The extension here is the
exact all-complex cubic-skew optimizer classification above the true
global first-power minimum, with uniform coverage of every shrinking
gap in a cubic-budget collar, exact radial exhaustion and an analytic
even peak. A bounded literature search did not find this precise
statement; it is not a claim of established literature priority.

The previously sealed private seventh-minimum result is preserved
separately. This proof neither computes the eighth minimum coefficient
nor pays the truncated next endpoint \(v=J_7\). One useful next step
is to derive the first coefficients of \(\mathcal R,U,V\) directly
from this full nondegenerate system, rather than generating higher
minimum Taylor coefficients solely to handle ever flatter gaps.
