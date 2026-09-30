# Exact two-block quartic deficit at the collapsed cutoff

Author: **six-sendov-2**, role **researcher**.
Status: complete ordinary proof with exact symbolic checks; independent
review of this extension is pending. There is no proof-assistant claim.

## 1. Statement and normalization

Fix integers \(m\ge3\), \(1\le r\le m-1\), and set
\[
n=m+1,\quad s=m-r,\quad a=\alpha_m=\frac{m+2}{2m},\quad
d=1+a,\quad v=\frac1d,\quad D=3m+2,\quad M=m+2.
\]
For real \(t\) consider the explicit disk-root polynomial
\[
p_t(z)=(z-a)(z+e^{ist})^r(z+e^{-irt})^s.                 \tag{1}
\]
Its marked root is simple, since \(0<a<1\) and all its other roots
have modulus one. Count critical points \(\zeta_j(t)\) with multiplicity
and define
\[
F(t)=\sum_{j=1}^m|a-\zeta_j(t)|^{-1},\qquad
E(t)=r\left|\frac1{a+e^{ist}}-v\right|^2+
     s\left|\frac1{a+e^{-irt}}-v\right|^2.                \tag{2}
\]
All critical reciprocals are finite because \(p'_t(a)\ne0\).
The first angular moment vanishes: \(rs+s(-r)=0\).

**Theorem.** As \(t\to0\),
\[
F(t)=\frac{2m}{d}-K_m(r)E(t)^2+O_{m,r}(E(t)^3),         \tag{3}
\]
where
\[
\boxed{K_m(r)=\frac{(m+2)(3m+2)^3}{256m^7}
 \left[\frac{m^2(m^2-4m-4)}{r(m-r)}
                    -(m-6)(3m+2)\right].}             \tag{4}
\]
Every coefficient \(K_m(r)\) is strictly positive. Its maximum over the
integer two-block multiplicities is attained as follows:

- \(m=3\): both \(r=1,2\), maximum \(6655/373248\);
- \(m=4\): only \(r=2\), maximum \(3087/65536\);
- \(m\ge5\): only \(r=1,m-1\).

The same ratio limit covers any nonzero balanced constant-slope two-block
angular direction: if \(r\theta_x+s\theta_y=0\), then
\((\theta_x,\theta_y)=\lambda(s,-r)\), and a nonzero rescaling of \(t\)
does not change (3). This scope does not include arbitrary nonlinear
two-block paths, general angular multisets or interior disk perturbations.

For degree nine (\(m=8,a=5/8\)),
\[
K_8(r)=\frac{10985}{8388608}
          \left[\frac{448}{r(8-r)}-13\right],\qquad
\max_rK_8(r)=K_8(1)=K_8(7)=\frac{560235}{8388608}.       \tag{5}
\]
The preceding moving-pair curve has coefficient
\[
C_m^{\rm pair}=
\frac{(m+2)(m^3-4m^2+13m+18)(3m+2)^3}{512m^7}.          \tag{6}
\]
The maximum in (4) is strictly larger than (6) exactly for \(m\ge8\),
or \(n\ge9\). In degree nine the exact excess is
\[
\frac{560235}{8388608}-\frac{2076165}{33554432}
        =\frac{164775}{33554432}>0.                     \tag{7}
\]
Formula (6) is a cited dependency for this comparison; neither (1)--(4)
nor their proof depend on a spectral perturbation theorem.

## 2. Product-rule reduction and the exact modulus-sum identity

Write \(x=e^{ist},y=e^{-irt}\). Product differentiation gives
\[
p'_t(z)=(z+x)^{r-1}(z+y)^{s-1}R(z),\qquad
R(z)=(z+x)(z+y)+(z-a)\{r(z+y)+s(z+x)\}.                \tag{8}
\]
This is a degree-\(m\) factorization: the displayed repeated factors
have degree \(m-2\) and \(R\) has degree two. It remains valid at \(t=0\)
and counts collisions with multiplicity. The leading coefficient of
\(R\) is \(n\). Under \(q=(a-z)^{-1}\), direct substitution yields
\[
q^2R(a-1/q)=Aq^2-Bq+n,\qquad
A=(a+x)(a+y),\quad B=(m+2)a+(s+1)x+(r+1)y.             \tag{9}
\]
The two remaining critical reciprocals are exactly the roots
\(q_+,q_-\) of this quadratic. There is no root at \(q=0\), since
its constant coefficient is \(n>0\). With \(u_x=(a+x)^{-1}\) and
\(u_y=(a+y)^{-1}\),
\[
F=(r-1)|u_x|+(s-1)|u_y|+|q_+|+|q_-|.                \tag{10}
\]

Put \(\Delta=B^2-4nA\). Choose either square root \(w^2=\Delta\).
The quadratic formula and the parallelogram identity give
\[
|q_+|^2+|q_-|^2=\frac{|B|^2+|w|^2}{2|A|^2}
              =\frac{|B|^2+|\Delta|}{2|A|^2}.
\]
Also \(q_+q_-=n/A\), so
\[
\boxed{|q_+|+|q_-|=
 \frac{\sqrt{(|B|^2+|\Delta|+4n|A|)/2}}{|A|}.}         \tag{11}
\]
The square root in (11) is positive. The identity is insensitive to
the ordering or choice of the two quadratic roots.

At \(t=0\), \(A=d^2,B=(m+2)d,\Delta=m^2d^2>0\), and the
quadratic roots are \(v,nv\). Hence all the scalar norms and square roots
in (10)--(11) have strictly positive bases. They are real analytic for
real \(t\) in some neighborhood of zero. In particular this argument
does not assume analytic labels for the critical multiset at a repeated
critical point. Conjugation sends the data at \(t\) to the data at
\(-t\); (10)--(11) and (2) therefore show that both \(F,E\) are even
real-analytic functions.

## 3. Symbolic coefficient calculation

Let \(k=rs\). The positive reciprocal modulus expansion is
\[
\left|(a+e^{i\theta t})^{-1}\right|
 =v+\frac{a}{2d^3}\theta^2t^2+
 \left(-\frac{a}{24d^3}+\frac{3a^2}{8d^5}\right)
                 \theta^4t^4+O(t^6).                 \tag{12}
\]
This follows by expanding
\((d^2-2a(1-\cos(\theta t)))^{-1/2}\).
At the cutoff define
\[
K_2=\frac{2m^2M}{D^3},\qquad
L=9m^2+24m-4,\qquad K_4=\frac{m^2ML}{6D^5}.            \tag{13}
\]
The two coefficients in (12) are \(K_2,K_4\), respectively.
The repeated-critical multiplicity sums are
\[
R_2=(r-1)s^2+(s-1)r^2=Mk-m^2,\qquad
R_4=(r-1)s^4+(s-1)r^4=-m^4+(m^3+4m^2)k-Dk^2.        \tag{14}
\]

Here is a compact reproducible calculation of the two-root sum \(Q\)
in (11). Clear denominators with
\[
A_N=4m^2A=(M+2mx)(M+2my),\quad
B_N=2mB=M^2+2m\{(s+1)x+(r+1)y\},\quad
\Delta_N=B_N^2-4nA_N.
\]
Its positive bases are
\[
A_N(0)=D^2,\quad B_N(0)=MD,\quad
\Delta_N(0)=m^2D^2.
\]
Consequently the exact same sum can be expanded as
\[
Q=\frac{2m}{|A_N|}
   \sqrt{\frac{|B_N|^2+|\Delta_N|+4n|A_N|}{2}}.         \tag{15}
\]
Substitute
\(x=\sum_{j=0}^4(is)^jt^j/j!+O(t^5)\) and
\(y=\sum_{j=0}^4(-ir)^jt^j/j!+O(t^5)\).
To make the coefficient calculation explicit, for any real series
\(T=\sum T_jt^j\) with positive square-root base \(c\), recursively use
\[
b_0=c,\qquad
b_j=\frac{T_j-\sum_{i=1}^{j-1}b_ib_{j-i}}{2c}
\quad(1\le j\le4).
\]
For a reciprocal series use
\(b_0=T_0^{-1}\) and
\(b_j=-T_0^{-1}\sum_{i=1}^jT_i b_{j-i}\).
Apply these rules to \(|A_N|=\sqrt{A_N\overline{A_N}}\),
\(|\Delta_N|=\sqrt{\Delta_N\overline{\Delta_N}}\), the outer square
root, and the reciprocal in (15).
Only factors \(m,D,M\) are divided by. Exact coefficient collection gives
\[
Q=Mv+K_2(m^2-Mk)t^2+Q_4t^4+O(t^6),                  \tag{16}
\]
where
\[
Q_4=\frac{m^2M}{6D^5}
 \{m^4L-m^2(15m^3+36m^2+68m-16)k
                  +D(15m^2-12m-4)k^2\}.             \tag{17}
\]
The included checker verifies these identities with \(m,r\) as
indeterminates, not by fitting finitely many degrees. It substitutes
every reciprocal and square-root series back into its defining identity.
Equations (15), the recurrences and (17) also specify the calculation
without requiring an external computer algebra package.

Combining (10), (12), (14) and (16) cancels the second-order term.
The constant is \(Mv+(m-2)v=2mv\). The fourth-order coefficient is
\[
f_4=Q_4+K_4R_4
 =\frac{m^3Mk}{D^5}
      \{-m^2(m^2-4m-4)+(m-6)Dk\}.                    \tag{18}
\]
Even analyticity from section 2 upgrades the truncated coefficient
calculation to
\[
F(t)=2mv+f_4t^4+O_{m,r}(t^6).                        \tag{19}
\]
This analytic step is essential to interpreting the formal series.

For the energy, exactly
\[
\left|(a+e^{i\theta t})^{-1}-v\right|^2
 =\frac{2(1-\cos(\theta t))}
        {d^2\{d^2-2a(1-\cos(\theta t))\}}.
\]
Thus
\[
E(t)=e_2t^2+O_{m,r}(t^4),\qquad
e_2=\frac{rs^2+sr^2}{d^4}
   =\frac{mk}{d^4}=\frac{16m^5k}{D^4}>0.             \tag{20}
\]
In particular \(E(t)\) is comparable to \(t^2\) for small nonzero \(t\).
Since \(E^2=e_2^2t^4+O(t^6)\), (19) equals
\(2mv+(f_4/e_2^2)E^2+O(E^3)\).
Substitution of (18)--(20) gives \(-f_4/e_2^2=K_m(r)\),
proving (3)--(4).

## 4. Positivity and the exact multiplicity extremizers

Put \(T=m^2-4m-4\). Formula (4) has the form
\[
K_m(r)=\frac{A_m}{k}-B_m,\quad
A_m=\frac{MD^3T}{256m^5},\quad
B_m=\frac{M(m-6)D^4}{256m^7}.                         \tag{21}
\]
For \(m\ge5\), \(T>0\): writing \(m=5+u\) gives
\(T=u^2+6u+1\). Also
\[
m-1\le k\le m^2/4,\quad
k-(m-1)=(r-1)(m-r-1),\quad m^2-4k=(m-2r)^2.
\]
Since \(A_m>0\), (21) decreases strictly with \(k\). Its maximum
therefore occurs exactly at \(r=1,m-1\). Its bracket in (4) is bounded
below by
\[
4T-(m-6)D=m^2-4>0,
\]
proving positivity for all these multiplicities.

For \(m=3\) there are only \(r=1,2\), both with \(k=2\), and
substitution gives \(6655/373248>0\). For \(m=4\), \(A_m<0\),
so the coefficient increases with \(k\). The values are
\[
K_4(1)=K_4(3)=\frac{1715}{65536},\qquad
K_4(2)=\frac{3087}{65536}.
\]
They are positive and give the stated unique middle multiplicity.
This proves all the sign and optimization assertions.

## 5. Comparison with the moving pair and the degree-nine obstruction

The moving-pair coefficient (6) was proved in the preceding source
[uniform collapsed radius threshold, section 5](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_threshold/PROOF.md),
source commit \(4cade1368e2880d76fd98c32ec32135e37482083\),
graph bafkreig6nbpaohth4dglfilv7nt34s5kzo3mmmbl26zfwxr2l4tygao2ly,
height 7328. Its fixed-cutoff coefficient is independently confirmed in
[review2](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_review2/REVIEW.md),
source commit \(c153e27a7bd3da634bd652fc804387e94c8ab71b\),
graph bafkreic7fofp3cfqbgvh2iltof4vbjpamuar7shl4bokael3ohwmies2vq,
height 7362. That review covers the predecessor and its refinement;
it does not review this theorem or the general quartic theorem.

For \(m\ge5\) the two-block maximum is \(K_m(1)\), and subtracting (6)
gives exactly
\[
K_m(1)-C_m^{\rm pair}
 =\frac{MD^3}{512m^7(m-1)}P(m),\quad
P(m)=m^4-9m^3+13m^2-13m-6.                            \tag{22}
\]
For \(m=8+u\),
\[
P(8+u)=u^4+23u^3+181u^2+515u+210>0
\quad(u\ge0).
\]
The remaining three values are \(P(5)=-246,P(6)=-264,P(7)=-146\).
The maxima in degrees four and five are smaller as well:
\[
\frac{6655}{373248}<\frac{6655}{23328},\qquad
\frac{3087}{65536}<\frac{36015}{262144}.
\]
This proves the exact degree threshold for improvement.

Specializing (4) gives (5)--(7). In particular for \(r=1,s=7\),
\[
p_t=(z-\tfrac58)(z+e^{7it})(z+e^{-it})^7,\qquad
F(t)=\frac{128}{13}-\frac{1599360}{371293}t^4+O(t^6),
\quad E(t)=\frac{229376}{28561}t^2+O(t^4).             \tag{23}
\]
For all sufficiently small nonzero \(t\), this explicit disk polynomial
violates the radial baseline \(F\ge128/13\) at the cutoff.
The preceding moving pair already showed failure of that baseline;
the new information is the stronger quartic **energy** coefficient and
its uniform exact optimization within two-block directions.

## 6. What this adds to the stability frontier

For a fixed degree and cutoff, allow arbitrary disk-root polynomials
with simple marked root \(a=\alpha_m\), and define \(E=\sum|u_j-v|^2\),
\(u_j=(a-z_j)^{-1}\), and \(F=\sum|a-\zeta_j|^{-1}\).
The prior
[quartic stability theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_quartic_stability/PROOF.md),
source commit \(fe5f093e012430f54554e83e9fe1eba39524f999\),
graph bafkreihspazdbffjge3vs3zevwt5zvwpfukkyr5ih6hzrbst2pwrlfv5fm,
height 7348, proves
\[
E\le\frac1{16n^2}\quad\Longrightarrow\quad
F\ge2m/d-11mn^4E^2.
\]
It supplies finiteness for the extremal question
\[
C_m^*=\lim_{\rho\downarrow0}
  \sup_{0<E\le\rho}\frac{2m/d-F}{E^2}.                 \tag{24}
\]
The suprema decrease with the shrinking sets and the present curves
bound them below by positive constants, so the limit exists and is finite.
From (3),
\[
\boxed{C_m^*\ge\max_rK_m(r),\qquad C_m^*\le11mn^4.}
\]
The moving-pair lower bound \(C_m^*\ge C_m^{\rm pair}\) remains an
additional valid bound. In degree nine the new lower bound is
\(560235/8388608\), larger by (7). This is a refinement of the
published obstruction, not a claim of global optimality.

The leading constant for a basin stated using maximum original-root
displacement is a separate optimization: the curve in (23) has maximum
angular speed seven and squared angular norm56; the moving pair has
maximum speed one and squared norm2. A larger energy-normalized deficit
therefore gives no automatic improvement in that basin constant.

At a distinguished unit root, the team's existing
[boundary equality classification, section 7](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md)
gives, for \(n\ge4\), the two first-power equality families
\(C(z^n-\omega^n)\) and \(C(z-\omega)(z+\omega)^m\), \(|\omega|=1\).
The present theorem studies angular splitting of the collapsed family
at the interior marked cutoff \(\alpha_m\). It adds neither an equality
family nor a statement about the regular family. Both regular and
collapsed quantitative boundary families were already covered by
[two-family stability](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_family_boundary_stability/PROOF.md),
source commit \(437a2d57e99a6c3b61c514b2fee2e5121062f3cc\),
graph bafkreiehp3axlj3xcmilyh75rvowmdjz7rzsxhdovz3qcwako6kibr4ppa,
height 7220.

Zhang's [quadratic theorem](https://arxiv.org/html/2609.19126),
Theorem 1.3, concerns \(\sum|a-\zeta|^{-2}\ge m\) and regular-binomial
equality. Its first-power statement remains Conjecture 1.2.
Our baseline \(128/13\) is strictly above8; by continuity (23) still has
\(F>8\) for small \(t\). It refutes neither the first-power endpoint nor
the quadratic theorem. The original degree-nine Sendov target is covered
by the newer all-degree primary proof report cited in LITERATURE.md.

Reusable input for the complementary analytic lane is the branch-free
identity (11) and the exact two-block data (18)--(20). Their proof does
not assume real coefficients or conjugate critical pairing. The largest
energy-deficit example in degree nine is generally a complex polynomial.
The remaining mathematical questions are the optimal fourth-order
functional for arbitrary balanced angular vectors, effects of repeated
compression eigenvalues and nonlinear paths, and possible interior-disk
directions. A two-block optimizer is not yet a global optimizer in (24).

## 7. Reproducibility and trust boundary

From the repository root:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B sendov_collapsed_two_block_quartic/verify.py
~~~

Python 3.11.2 standard library: PASS, **60 exact checks**, **five rejected
coefficient mutations**. Coefficients are rational functions in symbolic
\(m,r\), with Gaussian extension \(i^2=-1\), truncated at \(t^5\).
The quadratic transform is checked in a separate free polynomial ring.
Every square-root and reciprocal recurrence is verified by substitution,
and the coefficient, energy conversion, positivity certificates,
optimization identities and degree threshold are checked exactly.
The output states the degree-nine maximum and exact excess. There are
no numerical root solves, floating-point operations or external inputs.
The explicit invariant checks also run under optimized Python.

Written mathematics establishes the critical-multiset interpretation,
positive analytic square-root branches, evenness, remainders and the
integer inequalities. Those steps are not formalized by the checker.
The arithmetic adapts this author's previous exact checkers and is not
independent peer validation. As a private additional control a different
mechanism, recursive simple quadratic-root series followed by individual
moduli, agreed in all 65 profiles with \(3\le m\le12\); those finite controls
are not the basis for the all-degree theorem and are not a published
exhaustive search certificate. No reviewer verdict has been requested.
