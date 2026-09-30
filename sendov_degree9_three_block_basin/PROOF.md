# A three-block obstruction for the degree-nine collapsed stability basin

Author **six-sendov-2**, role **researcher**, 2026-09-30.
Ordinary mathematical proof with exact author arithmetic; independent
review pending. No formalization or independent code audit is claimed.

The result is a sharper upper obstruction for the maximum-original-root
basin, together with an exact coefficient at a varying marked zero.
The proof below uses a residual cubic directly. It does not require the
earlier general-angular spectral theorem or a universal quartic bound.

## 1. Definitions and statement

For a degree-nine polynomial with a simple marked zero \(a\in(0,1)\),
write its other eight zeros as \(z_1,\ldots,z_8\), and define
\[
 F(p,a)=\sum_{p'(\zeta)=0}\frac1{|a-\zeta|},\qquad d=1+a.
\]
Critical points are counted with multiplicity. Simplicity of \(a\)
ensures that no denominator vanishes. Let \(R_8(a)\) be the supremum
of radii \(\rho\ge0\) such that **every** degree-nine polynomial with
all zeros in the closed unit disk, simple marked zero \(a\), and
\(\max_j|z_j+1|\le\rho\), satisfies \(F(p,a)\ge16/d\).
This is the definition used by the independent
[two-block basin review](https://github.com/helgithorskarp/math_results/blob/main/sendov_two_block_quartic_review1/REVIEW.md),
source 823da55eaa6088dfa0168f57da2157ca0b01fd11, graph
bafkreig7yesgssknqm3ot3egoa44fajqduxkumrlisjoawk2nqsg6i4xzy,
height 7446. The admissible radii form an initial interval; radius zero
is admissible since the collapsed polynomial has \(F=16/d\).

Put
\[
 a_0=5/8,\quad d_0=13/8,\quad \kappa(a)=d(a-a_0).
\]
For \(k\in\{2,4,6\}\), consider the actual disk-root family
\[
 p_{a,t,k}(z)=(z-a)(z+1)^{8-k}
                  (z^2+2\cos(t)z+1)^{k/2}.
\]
Its other roots are \(-1\) and \(-e^{\pm it}\), with the displayed
multiplicities. The marked zero is simple. Define
\[
 E=k\left|(a+e^{it})^{-1}-d^{-1}\right|^2,
 \qquad \rho^2=\max_j|z_j+1|^2=2(1-\cos t).
\]

**Theorem.** Uniformly for \(a\) in a sufficiently small fixed
neighborhood of \(a_0\), as \(E\downarrow0\) in this family,
\[
 \boxed{F(p_{a,t,k},a)-16/d
       =\kappa(a)E-K_k(a)E^2+O_k(E^3),}
\]
where the coefficient at the varying marked zero is explicitly
\[
 \boxed{K_k(a)=d^3\left\{
 \frac{48d^2-40d-53}{512k}
 +\frac{16d^2-216d+405}{16384}\right\}.}
\]
At the cutoff,
\[
 K_k(a_0)=\frac{76895(11k+32)}{33554432k}>0,
 \qquad F(p_{a_0,t,k},a_0)=128/13-L_kt^4+O_k(t^6),
\]
\[
 L_k=\frac{35k(11k+32)}{2\cdot13^5}.
\]
For each fixed \(k\), there is a unique small positive crossing energy
\(E_k^*(a)\) for \(a>a_0\) sufficiently close to \(a_0\), with
\[
 E_k^*(a)=\frac{\kappa(a)}{K_k(a_0)}+O_k(\kappa(a)^2).
\]
Within a fixed small neighborhood in this one-parameter family, the
gap is positive for \(0<E<E_k^*(a)\), zero at \(E_k^*(a)\), and
negative for \(E>E_k^*(a)\). Set
\[
 (\rho_k^*(a))^2=
 \frac{E_k^*(a)d^4}{k+ad^2E_k^*(a)}.
\]
Then \(R_8(a)\le\rho_k^*(a)\) for all such \(a\). In particular,
the \(3+3+2\) family, namely \(k=6\), proves
\[
 \boxed{\limsup_{a\downarrow5/8}
 \frac{R_8(a)}{\sqrt{(1+a)(a-5/8)}}
 \le\sqrt{\frac{53248}{1715}}.}
\]
With denominator \(\sqrt{a-5/8}\), the squared constant is
\(86528/1715\). The squared \(\kappa\)-constant is exactly
\(240/343\) of the reviewed two-block bound \(3328/75\).
This improves an upper obstruction; it supplies no larger sufficient
basin, optimal universal constant, or explicit numerical neighborhood.

## 2. The cubic and a formula without colliding root labels

Write \(h=8-k\), \(c=\cos t\), \(\delta=1-c\). Differentiation gives
\[
 p'=(z+1)^{h-1}(z^2+2cz+1)^{k/2-1}R(z,a,c),
\]
\[
 R=((h+1)z+1-ha)(z^2+2cz+1)
       +k(z-a)(z+1)(z+c).
\]
The repeated factors have total degree five, and the residual cubic
accounts for the remaining three critical points. The identity also
counts all eight at \(t=0\). Its more convenient form is
\[
 R=R_0(z)+\delta Q(z),\qquad
 R_0=(z+1)^2(9z+1-8a),
\]
\[
 Q(z)=-(18-k)z^2+\{(16-k)a-(k+2)\}z+ka.
\]
At collapse the separated root is
\(w_0=(8a-1)/9\), with
\[
 R_z(w_0,a,1)=9(w_0+1)^2=64d^2/9>0.
\]
The analytic implicit-function theorem gives a jointly real analytic
real root \(w=w(a,\delta)\) near \((a_0,0)\). Put \(W=a-w\).
Its base is \(W_0=d/9>0\), so \(W>0\) after shrinking the neighborhood.

The other two cubic roots have sum \(S\) and product \(P\). The
coefficients of \(z^2,z\) in \(R\) are respectively
\[
 C_2=19-8a-(18-k)\delta,\quad
 C_1=11-16a+\{(16-k)a-(k+2)\}\delta.
\]
Consequently \(S=-C_2/9-w\), \(P=C_1/9-wS\).
Substitution of the first root coefficient below yields
\[
 S^2-4P=-(8-k)\delta+O_k(\delta^2).
\]
The remainder is uniform for \(a\) near \(a_0\). Because \(8-k>0\),
these roots are a conjugate nonreal pair for positive sufficiently
small \(\delta\). Their distances from the real marked zero are equal.
Also \(R(a)=d(d^2-2a\delta)\), so their distance product is
\[
 M=(a-z_+)(a-z_-)=\frac{d(d^2-2a\delta)}{9W}>0.
\]
Thus, for physical \(\delta\ge0\) near collapse,
\[
 \boxed{F=\frac{7-k}{d}
       +\frac{k-2}{\sqrt{d^2-2a\delta}}
       +\frac1W
       +2\sqrt{\frac{9W}{d(d^2-2a\delta)}}.}
\]
All square roots use their positive bases. This expression extends
real analytically to an open rectangle around \((a_0,0)\), although
only \(\delta\ge0\) is needed for the actual unit-circle family.
The formula uses the one simple root and the conjugate-pair product;
it assumes no analytic labeling of the entire multiple critical
cluster. The pair-discriminant argument is essential: the formula
must not be extended to \(k=8\), where that pair is no longer nonreal.

## 3. Exact coefficients and the energy variable

Expand \(w=w_0+w_1\delta+w_2\delta^2+O(\delta^3)\). The implicit
recurrence is
\[
 w_1=-\frac{Q(w_0)}{R_0'(w_0)},\qquad
 w_2=-\frac{R_0''(w_0)w_1^2/2+Q'(w_0)w_1}{R_0'(w_0)}.
\]
In terms of \(d\), it gives
\[
 w_1=\frac{k}{72}-\frac{k}{32d},
\]
\[
 w_2=\frac{k(81-108d+32d^2)}{1024d^3}
       +\frac{k^2(-45+38d-8d^2)}{4096d^3}.
\]
Substituting into the positive-root formula for \(F\) gives
\[
 F-16/d=A_1\delta+A_2\delta^2+O_k(\delta^3),
 \qquad A_1=\frac{2k(a-5/8)}{d^3},
\]
\[
 A_2=\frac{k}{d^5}\left\{
 \frac{885}{128}-\frac{405k}{4096}
 +d\left(-\frac{163}{16}+\frac{27k}{512}\right)
 +d^2\left(\frac{29}{8}-\frac{k}{256}\right)\right\}.
\]
These are generic rational identities, checked in the Laurent ring
\(\mathbb Q[d,d^{-1},k,k^{-1}]\) by [verify.py](verify.py). The
root residuals, inverses, both modulus squares, Vieta distance product,
and discriminant coefficient are checked separately. No values from
the earlier angular theorem are imported.

The original-root energy has the exact expression and inverse
\[
 E=\frac{2k\delta}{d^2(d^2-2a\delta)},\qquad
 \delta=\frac{Ed^4}{2(k+ad^2E)}.
\]
Hence
\[
 E=e_1\delta+e_2\delta^2+O(\delta^3),\qquad
 e_1=2k/d^4>0,\quad e_2=4ka/d^6.
\]
The ratio \(A_1/e_1\) is exactly \(\kappa(a)\). The energy-quartic
coefficient satisfies
\[
 e_1^2K_k(a)=\kappa(a)e_2-A_2,
\]
which gives the displayed closed formula. Analytic substitution of
the exact inverse proves the uniform \(O_k(E^3)\) statement on a
fixed smaller rectangle. Truncated arithmetic alone would not prove
the remainder or its uniformity.

At \(d=d_0\), \(A_1=0\) and
\(A_2=-70k(11k+32)/13^5\). Since
\(\delta=t^2/2-t^4/24+O(t^6)\), this gives \(F_4=A_2/4=-L_k\).
Moreover \(E_2=k/d_0^4\), so \(K_k(a_0)=L_kd_0^8/k^2\), as claimed.

## 4. The first local crossing and the universal-basin consequence

Let \(\mathcal F_k(a,E)\) denote the analytic formula above after
the exact energy substitution. Since \(\mathcal F_k(a,0)=16/d\),
\[
 H_k(a,E)=\frac{\mathcal F_k(a,E)-16/d}{E}
\]
has an analytic extension at \(E=0\), with
\[
 H_k(a,0)=\kappa(a),\quad
 H_k(a,E)=\kappa(a)-K_k(a)E+O_k(E^2).
\]
At \((a_0,0)\), \(H_k=0\) and
\(\partial_EH_k=-K_k(a_0)<0\). The analytic implicit-function theorem
gives an analytic crossing energy \(E_k^*(a)\). Differentiation, or
substitution into the displayed expansion, gives
\(E_k^*(a)=\kappa(a)/K_k(a_0)+O_k(\kappa(a)^2)\).
After shrinking a fixed neighborhood, \(\partial_EH_k<0\) throughout
it. For \(a>a_0\) sufficiently close, the crossing energy is positive,
unique there, and the signs on either side are as stated.

Every positive sufficiently small energy corresponds to a real
\(t\) through the exact positive \(\delta\). For energies just above
\(E_k^*(a)\), these actual disk-root polynomials violate \(F\ge16/d\).
Their radius is
\[
 \rho^2=\frac{Ed^4}{k+ad^2E},
\]
an increasing function of \(E\) near zero. Each such witness forces
\(R_8(a)\le\rho\); taking its energy down to the crossing proves
\(R_8(a)\le\rho_k^*(a)\). Finally,
\[
 \frac{(\rho_k^*(a))^2}{\kappa(a)}
 \longrightarrow B_k=\frac{d_0^4}{kK_k(a_0)}
                   =\frac{106496}{35(11k+32)}.
\]
The three centered profiles have the following exact constants.

| Moving roots \(k\) | Multiplicities | \(L_k\) | \(K_k(a_0)\) | \(B_k\) |
|---|---|---|---|---|
| 2 | 1+1+6 | 1890/371293 | 2076165/33554432 | 53248/945 |
| 4 | 2+2+4 | 5320/371293 | 1461005/33554432 | 26624/665 |
| 6 | 3+3+2 | 10290/371293 | 3767855/100663296 | 53248/1715 |

Thus \(k=6\) is strongest among precisely these three centered
profiles. No optimization over arbitrary three independent phases
or arbitrary original-root directions is asserted.

## 5. Prior inputs, scope and independently checkable evidence

The \(k=2\) moving-pair cutoff and earlier basin obstruction are
credited to
[the uniform-radius source](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_threshold/PROOF.md),
source 4cade1368e2880d76fd98c32ec32135e37482083, graph
bafkreig6nbpaohth4dglfilv7nt34s5kzo3mmmbl26zfwxr2l4tygao2ly,
and
[the quartic stability source](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_quartic_stability/PROOF.md),
source fe5f093e012430f54554e83e9fe1eba39524f999, graph
bafkreihspazdbffjge3vs3zevwt5zvwpfukkyr5ih6hzrbst2pwrlfv5fm.
The table's first row is a reproduction control, not a new constant.
The independent review7446 improves that \(k=2\) obstruction with
balanced two blocks to \(B=3328/75\), and proves its optimization
within the two-block subclass. Our exact ratio is
\[
 \frac{53248/1715}{3328/75}=240/343<1.
\]
Also \(L_6=10290/371293\) exceeds the balanced two-block root quartic
\(9600/371293\). This establishes that balanced two blocks are not
optimal in the larger angular class. It does not contradict the
review's explicit two-block scope.

The author's
[general angular coefficient](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md),
source 57dd686588ddf1874ebb2e52f1a9aac898cc2df8, graph
bafkreicigqr4oirngnmaffpaf4eq2efg2qrgunoq77q6cdrcdkg2ulapne,
already predicts these cutoff coefficients; we credit that derivation.
The new result is the direct cubic proof, the explicit coefficient for
varying \(a\), and the sharper joint basin/crossing theorem. The
[energy optimizer](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_optimizer/PROOF.md),
source 71a2f9f201bc9fa7e32237bdd14feef5ff8c3f8f, graph
bafkreibyx62xasxzcqheejib64y3i4dr462rjc4bjoerumtthypw6rqcdi,
maximizes \(K\), rather than the basin objective \(L/(\mu_2M^2)\)
for balanced slopes, \(M=\max_j|\theta_j|\). Those are distinct
normalizations. Neither spectral source is a premise of this proof.

Reviewer **six-reviewer-3** proves the
[full nonlinear two-block phase constant](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_two_block_review3/PROOF.md),
source 4de653093173ec7ec24de738ea297f9f829e0c1a, graph
bafkreicye5w4llvutfwvsbe46hv7vhnbeukaejjevzpy6ldyxli5q3xqsq,
height7462. Its marked cutoff and two-block family stay fixed; it
does not settle the unrestricted root-basin problem. The complementary
[critical-reciprocal radial gap](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_phase_radial_gap/PROOF.md)
by **six-sendov-1**, source 9c9bd0a1e0d8e83d26254461586a82d9d21086c2,
graph bafkreic7rctxzow5pjncoiswptyrgloe5jdkk63n7p35yj55sduxgj3nna,
height7434, concerns a different phase family and supplies no premise.

The checker passes **39 generic identities** and **1261 exact checks**
in total. Its separate individual-root algorithm expands each critical
reciprocal and its positive modulus, in exact quadratic extensions
\(\mathbb Q(i\sqrt{(8-k)/8})\), for **15 profiles**, and compares
**150** coefficients of \(F,E\) through order four with the generic
pair-product formula. It checks every required cubic residual,
inverse multiplication and modulus square. Both routes are author
implementations, not independent reviewer computations. Six wrong
coefficient/constant candidates are rejected. The fixed
[manifest](expected.json) records the coefficient digest and exact table.
These finite controls audit implementation; the generic identities
and the written analytic, positivity and crossing arguments establish
the stated result. Python 3.11 standard library only, with no imported
campaign checker, floating-point input, solver or proof corpus.

The broader Sendov status, Tang–Zhang endpoint and precise prior-art
comparison are in [LITERATURE.md](LITERATURE.md). The collapsed value
\(128/13>8\), so the displayed small deficits stay above eight.
They do not refute the exponent-one endpoint or supply a new ordinary
Sendov theorem. The optimal universal basin still requires a reduction
of arbitrary angular directions, nonlinear approaches and inward disk
motion. This proof supplies explicit admissible witnesses and their
local first crossing, with no such optimality claim.
