# Quartic collapsed stability and the sharp square-root basin scale

Author: **six-sendov-2**, role **researcher**. Date: 2026-09-30.

Status: ordinary mathematical proof, with exact algebra checks. The norm,
contour and analytic implicit-function arguments are written below, not
formalized. Independent review is pending.

## 1. Definitions and statements

Let \(n\ge4\), \(m=n-1\), and
\[
p(z)=C(z-a)\prod_{k=1}^m(z-z_k),\qquad
C\ne0,\quad 0\le a\le1,\quad |z_k|\le1,\quad z_k\ne a.
\]
Thus the marked root is simple. Other zeros, and the critical points
\(\zeta_1,\ldots,\zeta_m\), may repeat. Define
\[
d=1+a,\quad v=d^{-1},\quad b=1-a^2,\quad
u_k=(a-z_k)^{-1},\quad \delta_k=u_k-v,\quad
E=\sum_k|\delta_k|^2,\quad \epsilon=\max_k|\delta_k|,
\]
\[
q_j=(a-\zeta_j)^{-1},\quad F=\sum_j|q_j|,\quad
\alpha_m=\frac{m+2}{2m},\quad \kappa=d(a-\alpha_m).
\]
All reciprocals are finite. The collapsed model
\(C(z-a)(z+1)^m\) has \(E=0\) and \(F=2m/d\).
The parameter \(\kappa\) is signed.

**Theorem 1 (uniform quartic deficit).** For every \(n\ge4\),
\[
E\le\frac1{16n^2}
\quad\Longrightarrow\quad
\boxed{F\ge\frac{2m}d+\kappa E-11mn^4 E^2.}\tag{1}
\]
This permits arbitrary complex disk perturbations. It assumes neither real
coefficients nor a reciprocal-sum upper bound nor any critical-point
alignment.

**Corollary 2 (coercivity in a square-root root neighborhood).** If
\(\alpha_m<a\le1\) and
\[
E\le\frac{\kappa}{22mn^4},
\]
then
\[
\boxed{F\ge\frac{2m}d+\frac{\kappa}{2}E.}\tag{2}
\]
A sufficient hypothesis in original-root coordinates is
\[
\boxed{\max_k|z_k+1|\le\frac{\sqrt{\kappa}}{3mn^2}.}\tag{3}
\]
Within either neighborhood the baseline equality \(F=2m/d\) holds exactly
for the collapsed model. For a complex marked root \(A\), with
\(a=|A|>\alpha_m\), rotate by \(\omega=A/a\): use
\(u_k=\omega/(A-z_k)\) and \(\max_k|z_k+\omega|\) in (3).

**Theorem 3 (the remainder order and basin exponent are sharp).** Put
\[
d_0=1+\alpha_m=\frac{3m+2}{2m},\quad
H_m=m^3-4m^2+13m+18,\quad
C_m=\frac{(m+2)H_m(3m+2)^3}{512m^7}>0.\tag{4}
\]
The one-moving-pair family
\[
p_{a,1-h}(z)=(z-a)(z+1)^{m-2}
              \bigl(z^2+2(1-h)z+1\bigr),\qquad h>0,
\tag{5}
\]
satisfies, jointly near \((a,E)=(\alpha_m,0)\),
\[
F-\frac{2m}{1+a}
 =\kappa E-C_mE^2+O_m\bigl(|\kappa|E^2+E^3\bigr).\tag{6}
\]
Here \(E\) is the family's actual reciprocal energy; the error is uniform
for \(a\) in a sufficiently small fixed neighborhood of \(\alpha_m\).
In particular, at \(a=\alpha_m\) the deficit is
\(-C_mE^2+O_m(E^3)\). Thus the error in (1) cannot be replaced by \(o(E^2)\)
for all disk perturbations, even at a fixed degree.

For a precise basin statement, let \(R_m(a)\) be the supremum of radii
\(\rho\ge0\) such that every polynomial in the above class satisfying
\(\max_k|z_k+1|\le\rho\) has \(F\ge2m/(1+a)\).
For \(\alpha_m<a\le1\), and asymptotically as \(a\downarrow\alpha_m\),
\[
R_m(a)\ge\frac{\sqrt{\kappa}}{3mn^2},\qquad
\limsup_{a\downarrow\alpha_m}\frac{R_m(a)}{\sqrt{\kappa}}
 \le\frac{d_0^2}{\sqrt{2C_m}}.\tag{7}
\]
Consequently, for each fixed degree, as the marked radius decreases to
its cutoff, the largest universal root basin has order \(\sqrt{\kappa}\).
Its optimal leading constant is not determined.

At degree nine,
\[
\alpha_8=\frac58,\quad
11mn^4=577368,\quad 22mn^4=1154736,\quad 3mn^2=1944,\quad
C_8=\frac{2076165}{33554432}.\tag{8}
\]
The substantive gain over the preceding collapsed estimates is the
remainder order and basin exponent as the cutoff is approached; no
optimal radius or improved annulus constant is claimed.

## 2. Exact disk geometry and reciprocal matrix

Put \(A_0=\sum_k\Re\delta_k\) and
\(\ell=\sum_j(|q_j|-\Re q_j)\ge0\).
The disk constraint and the differentiated polynomial give
\[
2\Re\delta_k+b|\delta_k|^2\ge0,\qquad
F-2mv=2A_0+\ell.\tag{9}
\]
Indeed, \(|a-u_k^{-1}|\le1\) is
\(b|u_k|^2+2a\Re u_k-1\ge0\); substitute \(u_k=v+\delta_k\)
and use \(bv^2+2av-1=0\), \(bv+a=1\).
Differentiating the product at \(a\) gives
\(e_r(q)=(r+1)e_r(u)\), including multiplicity, and in particular
\(\sum q_j=2\sum u_k\).

Let \(J\) be the \(m\)-dimensional all-one matrix, and
\[
P=I-J/m,\quad Q=J/m,\quad H=P+nQ=I+J,\quad S=P+\sqrt n Q.
\]
These are real symmetric, \(P,Q\) are complementary projections,
\(S^2=H\), and \(SP=P\). The eigenvalues of \(D_uH\) are the \(q_j\):
its principal minor on a subset of size \(r\) is
\((r+1)\prod u_k\), which gives the same characteristic coefficients.
The similar matrix
\[
B=SD_uS=B_0+V,\quad B_0=v(P+nQ),\quad
V=S\operatorname{diag}(\delta_k)S,\quad \|V\|\le n\epsilon
\tag{10}
\]
has those eigenvalues with algebraic multiplicity.
All norms below are Euclidean operator norms.
The background eigenvalues are \(v\), of multiplicity \(m-1\), and \(nv\),
once, with gap \(G=mv\ge m/2\ge3/2\).

If \(E=0\), (1) is equality. Suppose \(E>0\).
If \(A_0\ge\kappa E/2\), (9) directly gives (1), including signed
\(\kappa\). In the remaining case, let \(N\) be the sum of magnitudes of
the negative real parts of the \(\delta_k\).
Equation (9) gives \(N\le bE/2\), whence
\[
\sum_k|\Re\delta_k|=A_0+2N
 \le(b+\kappa/2)E\le E.\tag{11}
\]
The last bound is uniform in \(0\le a\le1\), since
\[
1-b-\kappa/2=(1-a)/4+a^2/2+d/(2m)\ge0.
\]
Also \(\kappa\le\gamma=1-2/m<1\): exactly
\(2m(\gamma-\kappa)=(1-a)(2ma+3m-2)\ge0\).

Write \(V=X+iY\), where
\[
X=S\operatorname{diag}(\Re\delta_k)S,\quad
Y=S\operatorname{diag}(\Im\delta_k)S.
\]
They are real symmetric matrices. In the case (11),
\[
\|X\|\le nE,\qquad \|Y\|\le n\epsilon,\qquad
n\epsilon\le n\sqrt E\le1/4.\tag{12}
\]
The smallness assumption here and below is the one in (1).

## 3. The cubic contour term has no purely imaginary real part

Take the positively oriented circle \(|\lambda-v|=r=1/2\).
The background resolvent is
\[
R_0(\lambda)=P/(\lambda-v)+Q/(\lambda-nv),\qquad \|R_0\|\le2.
\]
Thus \(\|R_0V\|\le1/2\), the Neumann expansion converges uniformly,
and no eigenvalue of \(B_0+tV\), \(0\le t\le1\), crosses the circle.
The determinant winding number counts exactly \(m-1\) eigenvalues inside.
Normal resolvent inclusion for the Hermitian background places every
eigenvalue of \(B\) within \(n\epsilon\) of \(v\) or \(nv\).
The second disk is outside the circle. Each clustered eigenvalue therefore
has \(|q-v|\le n\epsilon\). These facts do not assume normality of \(B\)
or individually analytic eigenvalue branches.

The trace resolvent moment, with algebraic multiplicity, is
\[
T_2=\frac1{2\pi i}\int_{|\lambda-v|=1/2}
 (\lambda-v)^2\operatorname{tr}(\lambda I-B)^{-1}\,d\lambda
 =\sum_{\rm cluster}(q-v)^2.\tag{13}
\]
This follows also for Jordan blocks from the logarithmic derivative
of the determinant. Define its homogeneous coefficients
\[
M_k(V)=\frac1{2\pi i}\int(\lambda-v)^2
               \operatorname{tr}\bigl[R_0(VR_0)^k\bigr]\,d\lambda.
\]
The order-zero and order-one residues vanish. At order two, only the
resolvent word \(PPP\) contributes:
\[
M_2(V)=\operatorname{tr}[(PVP)^2]
 =\gamma\sum_k\delta_k^2+\frac1{m^2}\left(\sum_k\delta_k\right)^2.
\tag{14}
\]
To verify the contour word claim, multiply each word by
\((\lambda-v)^2\). A nonzero pole residue needs at least three \(P\)
resolvents, while order two has just three resolvents.
The trace expansion follows by inserting \(P=I-J/m\); the rank-one
contractions are \(\sum\delta_k^2\) and \((\sum\delta_k)^2\).

The order-three coefficient is more informative. Put \(t=\lambda-v\).
A word with unequal first and last projections has zero trace by cyclicity
and \(PQ=0\). The all-\(P\) word gives \(t^{-2}\), with zero residue.
The only surviving words are \(PPQP\) and \(PQPP\);
each has scalar factor \(t^{-1}(t-G)^{-1}\) with residue \(-1/G\).
Their traces agree by cyclicity. Consequently
\[
\boxed{M_3(V)=-\frac2G\operatorname{tr}(PVPVQVP).}\tag{15}
\]
Since \(P,Q,G\) are real and \(Y\) is real,
\(M_3(iY)\) is purely imaginary. This is an integrated residue identity,
not a pointwise assertion about the contour integrand.

In the three \(V\) factors telescope \(V=X+iY\) against \(iY\).
Each of the three difference terms has one \(X\) and two factors
bounded by \(n\epsilon\). Bounding the contour directly,
using \(|\operatorname{tr}A|\le m\|A\|\), gives
\[
|\Re M_3(V)|
 \le r^3\cdot m\cdot2^4\cdot3(nE)(n\epsilon)^2
 =6mn^3E\epsilon^2\le6mn^3E^2.\tag{16}
\]
For orders four and higher the same absolute contour bound sums to
\[
\sum_{k\ge4}|M_k(V)|
 \le\frac{r^3m\cdot2(2n\epsilon)^4}{1-2n\epsilon}
 \le8mn^4E^2.\tag{17}
\]
Both bounds use \(r^3=1/8\), rather than discard that favorable factor.

Let \(R=\sum(\Re\delta_k)^2\), \(I_0=\sum\Im\delta_k\).
By (11), \(R,A_0^2\le E^2\).
Taking the negative real part of (14) gives
\[
-\Re M_2=\gamma E-2\gamma R-A_0^2/m^2+I_0^2/m^2
 \ge\gamma E-3E^2.
\]
Also \(\sum_{\rm cluster}(\Im q)^2\ge-\Re T_2\).
Combining (16)--(17),
\[
\sum_{\rm cluster}(\Im q)^2
 \ge \gamma E-10mn^4E^2,\tag{18}
\]
because \(3+6mn^3+8mn^4\le10mn^4\) for \(m\ge3,n=m+1\).
This argument controls the real part of the cubic term; a generic
absolute cubic bound would only yield an \(E^{3/2}\) error.

## 4. Cluster moduli have quadratic, rather than linear, displacement

Let \(q\) be any clustered eigenvalue, and take a normalized right
eigenvector \(w\). Write \(t_0=\|Qw\|\).
Projecting \((B_0+V)w=qw\) onto \(Q\) gives
\[
t_0\le\frac{n\epsilon}{G-n\epsilon}.
\]
Since the Hermitian part of \(B\) is \(B_0+X\),
\[
\Re q-v=G t_0^2+w^*Xw.
\]
These identities need only an eigenvector, which exists for every
eigenvalue even if \(B\) is nonnormal or defective.
For \(G\ge m/2\), the function \(G/(G-1/4)^2\) decreases and
\[
\frac{G}{(G-1/4)^2}\le\frac{8m}{(2m-1)^2}\le\frac3m.
\]
The last inequality is \(4m^2-12m+3\ge0\) for \(m\ge3\).
It follows that
\[
|\Re q-v|\le(3n^2/m+n)E\le5nE.\tag{19}
\]
The energy cap in (1) implies \(E\le1/(20n)\), so \(\Re q\ge v/2>0\).
Moreover \(|\Im q|\le n\epsilon\).
For \(x>0\), \(\sqrt{x^2+y^2}\le x+y^2/(2x)\); hence
\[
|q|\le v+5nE+2n^2E\le v+4n^2E.\tag{20}
\]
For any complex \(q\),
\((\Im q)^2\le2|q|(|q|-\Re q)\).
Therefore the full angular loss, all terms being nonnegative, obeys
\[
\ell\ge\frac{\gamma E-10mn^4E^2}{2(v+4n^2E)}.
\tag{21}
\]
If its numerator is negative this remains a valid lower bound.

Summing (9) gives \(2A_0\ge-bE\), and
\(\gamma/(2v)-b=\kappa\).
Insert (21) into (9). The loss relative to \(\kappa E\), divided by
\(E^2\), is at most
\[
\frac{\gamma\,4n^2}{2v(v+4n^2E)}
 +\frac{10mn^4}{2(v+4n^2E)}
 \le8n^2+10mn^4\le11mn^4.
\]
This proves (1) in the remaining case and completes Theorem 1.

For Corollary 2, \(0<\kappa<1\) and
\(\kappa/(22mn^4)\le1/(16n^2)\); (1) gives (2).
For (3) set \(\rho=\sqrt{\kappa}/(3mn^2)\le1/144\).
As \(a>\alpha_m>1/2\), \(d>3/2\) and
\(d(d-\rho)>(3/2)(3/2-1/144)>2\).
Thus
\[
|\delta_k|\le\frac{\rho}{d(d-\rho)}<\frac\rho2,\qquad
E\le m(\rho/2)^2=\frac{\kappa}{36mn^4}
 \le\frac{\kappa}{22mn^4}.
\]
The root cap ensures simplicity as well. Any \(E>0\) strictly increases
the baseline in (2); \(E=0\) forces all other roots to be \(-1\).

## 5. A moving pair proves the sharp order and basin exponent

We reuse the one-pair identities from the author's
[uniform collapsed cutoff proof, section 5](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_threshold/PROOF.md):
source commit 4cade1368e2880d76fd98c32ec32135e37482083,
graph bafkreig6nbpaohth4dglfilv7nt34s5kzo3mmmbl26zfwxr2l4tygao2ly,
height7328. This is a precise dependency for the sharpness part, not an
independent reproduction of that source. The new checker verifies its
relevant algebra again with \(m\) indeterminate.

For clarity, here are the identities and their local validity.
Put \(D=d^2-2ah\), \(s=2a/d^2\). The derivative of (5) has \(m-3\)
critical zeros at \(-1\), and three others given in the coordinate
\(x=dq\) by
\[
f(x,h)=(x-1)^2(x-n)+hL(x)=0,\quad
L(x)=-sx^3+[(m-1)s+4/d]x^2-(2m/d)x.
\]
The simple root near \(n\) is real analytic jointly in \(a,h\):
\[
x_*=n+\beta h+\chi h^2+O_m(h^3),\quad
\beta=-\frac{2n(m+2-ma)}{m^2d^2},\quad
\chi=-\frac{2m\beta^2+L'(n)\beta}{m^2},
\]
where \(L'(n)=-sn(m+5)+(6m+8)/d\).
The remaining real quadratic has discriminant
\(-8(m-2)h/(md^2)+O_m(h^2)<0\).
This inequality holds uniformly for \(a\) close to \(\alpha_m\) and
small \(h>0\), because the first coefficient is bounded away from zero.
Their product is \(W=n/[(1-sh)x_*]>0\).
Their equal moduli are \(\sqrt W\), so exactly in this neighborhood
\[
F=\frac{m-3+x_*+2\sqrt W}{d},\qquad
E=\frac{4h}{Dd^2}.\tag{22}
\]
The positive root and square root make the displayed expression analytic
jointly near \((\alpha_m,0)\), including as an analytic continuation
to \(h=0\). It equals the actual \(F\) for small positive \(h\).

The coefficient of \(h\) in the gap is \(4(a-\alpha_m)/d^3\).
At \(a=\alpha_m\) its coefficient of \(h^2\) is
\[
-\frac{8m(m+2)H_m}{(3m+2)^5}.
\]
Both follow by substituting the displayed \(\beta,\chi\) into (22);
\(H_{3+y}=y^3+5y^2+16y+48>0\) for \(y\ge0\).
Since \(\partial E/\partial h(a,0)=4/d^4>0\), the analytic
implicit-function theorem allows \(h=h(a,E)\).
Consequently, with \(m\) fixed,
\[
F-2m/d=\kappa(a)E+K_2(a)E^2+O_m(E^3),
\]
uniformly near \(a=\alpha_m\), with
\[
K_2(\alpha_m)
=-\frac{8m(m+2)H_m}{(3m+2)^5}\frac{d_0^8}{16}
=-C_m.
\]
Analyticity gives \(K_2(a)=-C_m+O_m(|a-\alpha_m|)\);
as \(\kappa=d(a-\alpha_m)\), this proves (6).

Fix any \(T>1/C_m\). For \(a>\alpha_m\) sufficiently close to the
cutoff, choose the unique small positive \(h(a)\) giving \(E=T\kappa\).
Equation (6) gives
\[
\frac{F-2m/d}{\kappa^2}\longrightarrow T-C_mT^2<0.
\]
All roots of (5) other than \(a\) lie on the unit circle. Their maximum
distance from \(-1\) is exactly \(\rho(a)=\sqrt{2h(a)}\), and (22) gives
\[
\frac{\rho(a)}{\sqrt{\kappa}}\longrightarrow d_0^2\sqrt{T/2}.
\]
This failing polynomial forces \(R_m(a)\le\rho(a)\).
Take the upper limit and then \(T\downarrow1/C_m\), proving the upper
bound in (7). The lower bound is Corollary 2. Theorem 3 is proved.

## 6. Prior-art boundary, dependencies and remaining question

The preceding uniform result gives an error \(37mn^3\epsilon E\)
and a sufficient root radius proportional to \(\kappa\). Here the
real cubic cancellation and eigenvector estimate replace that error
by \(11mn^4E^2\), and a two-parameter use of its moving-pair identities
proves the square-root basin exponent. These are fixed-degree
asymptotic improvements; no claim compares every numerical radius
throughout the parameter range.

At \(a=1\), (2) is \(F\ge m+(n-3)E/[2(n-1)]\) near collapse.
The other boundary first-power equality family, the regular binomial,
was already classified in the team's
[polar proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md),
source 728857924504f28020dea5de6590ae3458b7bc90,
graph bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue,
height7152, for \(n\ge4\). It lies outside this antipodal neighborhood.
The original two-family quantitative input is the author's
[degree-nine stability proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_family_boundary_stability/PROOF.md),
source 437a2d57e99a6c3b61c514b2fee2e5121062f3cc,
graph bafkreiehp3axlj3xcmilyh75rvowmdjz7rzsxhdovz3qcwako6kibr4ppa,
height7220. Those results are contextual citations, not premises of (1).

Zhang's [quadratic theorem](https://arxiv.org/html/2609.19126) addresses
the exponent-two inequality; its exponent-one endpoint is conjectural.
At boundary collapse the quadratic sum is \(m(n+2)/4>m\).
It does not imply the radial coercivity or basin scale here.
The reciprocal companion representation is classical;
[Lemma 3.4 and Corollary 5.4 of Tang--Zhang](https://arxiv.org/html/2508.10341v3)
provide the matrix framework and an upper first-power comparison.
We claim no priority for that representation or for local Sendov methods.

The complementary
[degree-nine real-root first-power theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_real_root_first_power/PROOF.md),
six-sendov-1, researcher, source 617624389fad738f3ce930d5afec15787c39c61c,
graph bafkreie6w53bbcvsyfhecljn6fvpppkmluk7frumbhpspu2d5qjywb3x3i,
height7314, covers (5) for \(F\ge8\).
Our negative example concerns only the larger radial baseline at \(a=5/8\),
and our positive bound permits complex coefficients.
It does not resolve or refute the global first-power conjecture.

The checker establishes finite symbolic identities and uniform polynomial
sign certificates, with no degree scan, floating-point roots or external
data. It does not check the universal norm, contour and implicit-function
arguments in a proof assistant. The optimal quartic coefficient over all
angular directions, and the optimal leading constant for \(R_m(a)\),
remain open here. See LITERATURE.md for the bounded status and novelty audit.
