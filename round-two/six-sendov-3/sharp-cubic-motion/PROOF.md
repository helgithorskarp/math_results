# Sharp universal cubic original-root motion at the degree-nine boundary

Actual **six-sendov-3**, role **researcher**, 2026-10-03.
Complete ordinary author proof, **unformalized and independently unreviewed**.
Finite exact algebra corroborates the identities below. It does not
formalize the inherited concentration/rate theorem, Taylor bounds,
compactness, Lagrange argument or actual-family existence.

## Statement and the precise new conclusion

All nine original roots of the complex degree-nine polynomial lie in the
CLOSED unit disk. Normalize the polynomial to be monic and rotate its
marked root to $a=1-\eta>0$. Count ALL eight critical points $\zeta_l$ with
multiplicity and put $F_p(a)=\sum_{l=1}^8|a-\zeta_l|^{-1}$, with an infinite
term at a zero denominator. Define

\[
\begin{gathered}
c=\cos(\pi/9),\quad y=\frac1{3(1+c)},\quad x=\frac23-y,\quad
H=14y,\quad U_0=-8x,\quad C=\frac83+y,\quad k=-\frac{7(1+2c)}{18},\\
\omega_j=e^{2\pi ij/9},\quad
B_j(\eta)=\omega_j+\eta(-\omega_j/3-x-y/\omega_j),\\
W_j=\frac i{18}\left[(3+4c)\omega_j-(1+2c)(1+\omega_j^{-1})
                                      -\omega_j^{-2}\right],\\
\mathsf A=\sqrt{\frac{H^3(8+25c+20c^2)}{252}},\qquad
K_E=\frac{6653}{324}+\frac{23915}{486}c-\frac{15839}{243}c^2,
\quad 9<K_E<10 .
\end{gathered}                                                     \tag{1}
\]

**Universal motion theorem.** For EVERY fixed finite real $D$ there are
$\eta_D>0$ and $M_D<\infty$ such that, for EVERY actual polynomial above
and EVERY $0<\eta<\eta_D$ satisfying
\[
F_p(1-\eta)\le8+C\eta+D\eta^2,                                  \tag{2}
\]
its nine originals are simple and have the unique labels $Z_j$ near the
nine distinct $\omega_j$. With the ACTUAL, permutation-invariant moment
\[
J_3(p,\eta)=\sum_{l=1}^8\left(\frac{\Im\zeta_l}{\sqrt\eta}\right)^3,
\]
one has, simultaneously for ALL nine labels,
\[
\max_{0\le j\le8}|Z_j-B_j(\eta)-\eta^{3/2}J_3(p,\eta)W_j|
                                      \le M_D\eta^2,            \tag{3}
\]
and, increasing the SAME $M_D$ if necessary,
\[
\max_j|Z_j-B_j(\eta)|\le\mathsf A\eta^{3/2}+M_D\eta^2.          \tag{4}
\]
Critical collisions, nonconjugate tuples and arbitrary variation with
$\eta$ are included; analytic critical labels are not assumed.

**Sharpness on each larger budget arm.** For EVERY fixed $D>K_E$ the class
in (2) is nonempty for every sufficiently small positive $\eta$, and
\[
\lim_{\eta\downarrow0}\ \sup_{p\text{ satisfying (2)}}
\frac{\max_j|Z_j-B_j(\eta)|}{\eta^{3/2}}=\mathsf A.              \tag{5}
\]
The maximum cubic coefficient occurs exactly at labels $j=2,7$, NOT at
the cube labels $3,6$ used by the earlier necessity example. Its full
finite table is

| $j$ | $|W_j|^2$ |
| --- | --- |
| $0$ | $0$ |
| $1,8$ | $(13+26c+16c^2)/324$ |
| $2,7$ | $(16+50c+40c^2)/324$ |
| $3,6$ | $(9+36c+36c^2)/324$ |
| $4,5$ | $(16+32c+16c^2)/324$ |

**Equality rigidity.** Let $\eta_n\downarrow0$ and actual polynomials
satisfy (2) with one fixed finite $D$. If their normalized maximum motion
tends to $\mathsf A$, then the distance of their imaginary profile to
\[
\mathcal E=\left\{\text{permutations and overall signs of }
       \sqrt{H/56}(7,-1,-1,-1,-1,-1,-1,-1)\right\}              \tag{6}
\]
tends to zero, and
\[
\liminf_n\frac{F_{p_n}(1-\eta_n)-8-C\eta_n}{\eta_n^2}\ge K_E.  \tag{7}
\]
Thus $D<K_E$ cannot admit equality in this universal bound. Neither
attainment under the EXACT cut $D=K_E$ nor the optimal constant on each
smaller budget arm is asserted.

The new result is the universal all-nine cubic law, its exact sharp
maximum and this motion equality classification. The canonical first
motion, necessary cubic moment constraints and least-profile cost are
prior results from8530 and8619, independently assessed by8608 and8684.
The1+7 actual construction and cube obstruction were already10006,
independently confirmed and refined to an OPEN repair region by10028.
The whole sphere is now actually attained by10036, but that new chart
is only complementary context here: (5) uses the independently assessed
OPEN repair region10028. This is not a new skewness inequality, actual
family, global first-power proof, effective numerical annulus or review
verdict on a parent. The effective9954/9988 motion bounds have a different
explicit-window scope; no numerical constant from them is adopted.

## Uniform rates and an arbitrary-competitor polynomial jet

Adopt precisely the arbitrary-competitor rate reduction in
[8619, section2](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/quartic-boundary/PROOF.md),
independently confirmed with its stated concentration/entry inputs by
[8684](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/quartic-boundary-audit/REVIEW.md).
For (2), write $t=\sqrt\eta$, $S=\sum\zeta_l$, $P_m=\sum\zeta_l^m$,
$Q=\sum|\zeta_l|^2$ and $X=\sum(\Re\zeta_l)^2$. The reviewed proof gives

\[
\begin{gathered}
Q=O_D(\eta),\quad S=O_D(\eta),\quad X=O_D(\eta^2),\\
\Re S=U_0\eta+O_D(\eta^2),\quad
\Re P_2=-H\eta+O_D(\eta^2),\quad
\Im S,\Im P_2=O_D(\eta^{3/2}).
\end{gathered}                                                    \tag{8}
\]
Here and below $O_D$ is uniform over the ENTIRE arm (2) in one sufficiently
small collar depending only on $D$. This uniformity follows from the
reviewed proof, not from assumed analytic families: concentration applies
to EVERY sequence with the bounded linear margin, so it is uniform as
$\eta\to0$ by sequential contradiction. In the resulting one fixed small
neighborhood, its local positive-$Q$ bound and Taylor/coefficient estimates
have fixed constants. In the two active rows the positive dual weights
give $X/4\le D\eta^2+K\eta^2$, followed by fixed nonsingular linear systems.
Consequently the constants and a sufficiently small collar in (8) depend
only on $D$. If an arm is empty, the assertions on it are vacuous.

Let $h_l=\Im\zeta_l/t$, $u_l=\Re\zeta_l/t^2$, $J_3=\sum h_l^3$,
$V=\Im S/t^3$ and $B=\Im P_2/t^3$. These real quantities are uniformly
bounded; the reviewed unaveraged active-pair constraints, not merely their
averages, give
\[
V=\frac47B+O_D(t)=\frac{8k}{7}J_3+O_D(t),\qquad
B=2kJ_3+O_D(t).                                                \tag{9}
\]
Also $\sum h_l=O_D(\eta)$, $\sum h_l^2=H+O_D(\eta)$ and
$P_3=-it^3J_3+O_D(t^4)$. For the last estimate, each real coordinate is
$O_D(t^2)$ and each imaginary coordinate is $O_D(t)$; the real cubic
part is $O_D(t^4)$ and the correction to its imaginary part is $O_D(t^5)$.

Newton identities with ALL eight elementary symmetric coefficients and
integration anchored at $a$ yield, in the full degree-nine coefficient norm,
\[
p=z^9-1+t^2g_2(z)+t^3g_3(z)+O_D(t^4),                         \tag{10}
\]
where
\[
\begin{split}
g_2(z)&=9+9x(z^8-1)+9y(z^7-1),\\
g_3(z)&=i[-9V(z^8-1)/8-9B(z^7-1)/14+J_3(z^6-1)/2].
\end{split}                                                     \tag{11}
\]
This is the cubic part of the earlier generic polynomial jet, not a new
identity claim. Its error is uniform: products $S^2,SP_2$ are $O_D(t^4)$;
for $m\ge4$, $e_m=O_D(T^{m-2}Q)=O_D(t^m)$ with
$T=\max|\zeta_l|=O_D(t)$; and replacing the anchor by1 in perturbations
and expanding $a^9$ costs $O_D(t^4)$. No factor is lost through a collision.
Substitute (9) into (11). The $O_D(t)$ closure error becomes $O_D(t^4)$
in the full polynomial, so
\[
g_3=iJ_3[-9(k/7)(z^8-1)-(9k/7)(z^7-1)+(z^6-1)/2]
                                                       +O_D(t). \tag{12}
\]

The fixed limiting polynomial $z^9-1$ has nine simple, separated roots.
Uniform coefficient perturbation, for instance Rouche in nine fixed
disjoint disks followed by the root equation, gives one simple original
in each disk and counts ALL nine. Taylor expansion there gives
\[
Z_j=\omega_j-\frac{t^2g_2(\omega_j)+t^3g_3(\omega_j)}
                         {9\omega_j^8}+O_D(t^4).               \tag{13}
\]
The perturbation and original displacement are $O_D(t^2)$, so their
quadratic Taylor terms and the product of a perturbed derivative with
the displacement are $O_D(t^4)$, uniformly in the nine fixed disks.
There is no division by a critical-point separation. Algebra in (13)
gives the canonical $B_j$ and exactly the $W_j$ in (1), proving (3).
At $j=0$, $B_0=a$, $W_0=0$, and the original is exactly the marked root.

## All harmonics, the classical skewness extremizers and (4)

In the exact field $\mathbb Q[w]/(w^6+w^3+1)$, with
$w=e^{2\pi i/9}$, $c=-(w^4+w^5)/2$. Multiplication by conjugates computes
all nine $|W_j|^2$ and gives the complete table in the statement. The gaps
from label2 to labels1,3,4 are respectively
\[
\frac{3+24c+24c^2}{324},\qquad
\frac{7+14c+4c^2}{324},\qquad
\frac{18c+24c^2}{324},                                       \tag{14}
\]
which are strictly positive since $c>0$. The zero label is also strictly
smaller. Conjugate labels have equal norms. This proves
$\max_j|W_j|^2=(8+25c+20c^2)/162$, only at2 and7.

For EVERY real balanced vector $v\in\mathbb R^8$ with
$\|v\|^2=H$, the classical finite-population skewness inequality is
\[
\left|\sum v_l^3\right|^2\le\frac9{14}H^3.                    \tag{15}
\]
For completeness, this compact sphere is smooth: the constraint gradients
$\mathbf1$ and $v$ are independent since $H>0$ and $\sum v_l=0$.
At any extremum of $\sum v_l^3$, the Lagrange equations say that EVERY
coordinate solves one quadratic equation. One value alone is impossible;
thus there are two values, with multiplicities $r,8-r$, $1\le r\le7$.
Balance forces their ratio to be $-r/(8-r)$; normalization gives
\[
\frac{(\sum v_l^3)^2}{H^3}
 =\frac{(8-2r)^2}{8r(8-r)}.
\]
The seven values are $9/14,1/6,1/30,0,1/30,1/6,9/14$.
The absolute maximum occurs only at $r=1,7$, exactly the orbit (6).
This classical argument and inequality were already used in10036.

The actual $h$ is only approximately balanced and normalized. Center it
by $\bar h\mathbf1$ and normalize the centered vector to squared norm
$H$. By (8)--(9) this gives $v\in\mathcal S$ with
$\|h-v\|=O_D(\eta)$. Its cubic moment differs by $O_D(\eta)$, since all
coordinates are uniformly bounded. Hence
\[
|J_3(p,\eta)|\le\sqrt{9H^3/14}+O_D(\eta).
\]
Together with (3), the ALL-nine harmonic maximum and (15), this gives
(4), with $\mathsf A^2=H^3(8+25c+20c^2)/252$ exactly.

## Actual sharpness without a zero-slack assumption

Use the full actual OPEN repair-plane construction proved in
[review10028](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/asymmetric-motion-audit/PROOF.md),
which independently confirms10006 and adds this refinement. Its exact
definitions are included to identify what is adopted. Write
$\lambda=12(1+c)$, $g=48k$, and fix real $M,\beta$. For real $s$ put
\[
\begin{split}
m&=-x\lambda s^2+igs^3+Ms^4,\quad a=1-\lambda s^2,\\
\zeta_L&=m+7is+42ks^2+7i\beta s^3,\\
\zeta_S&=m-is-6ks^2-i\beta s^3,\\
H_s(z)&=(z-\zeta_S)^9-\tfrac98(\zeta_L-\zeta_S)(z-\zeta_S)^8,\\
p_s(z)&=H_s(z)-H_s(a).
\end{split}                                                      \tag{16}
\]
Its exact derivative is $9(z-\zeta_L)(z-\zeta_S)^7$. The nine simple
originals and their physical containment are proved in the adopted
review: the five inactive second half-normals are strictly negative;
the four active cubic half-normals vanish individually. The fourth
half-normals at3,4 are
\[
\begin{split}
n_3&=-(431+320c+320c^2)/3-(3/2)M+12\beta,\\
n_4&=-(1636+2842c+1980c^2)/9-(1+c)M+8(1-d)\beta,
\quad d=2c^2-1.
\end{split}
\]
Their partners6,5 have the SAME respective coefficients. Let
$q_3=-n_3$, $q_4=-n_4$. The determinant $12(c+d)>0$ makes these affine
coordinates of the entire repair plane. With the prior positive dual
weights $w_4=1/(c+d)$ and
$w_3=(2/3)[7-(1-d)/(c+d)]$, the exact objective is
\[
F_{p_s}(a)=8+C\eta+K(M,\beta)\eta^2+O(\eta^3),\quad
\eta=\lambda s^2,\quad
K(M,\beta)=K_E+(w_3q_3+w_4q_4)/\lambda^2.                       \tag{17}
\]
For EACH fixed $q_3,q_4>0$ with $K(M,\beta)<10$, review10028 proves an
actual common positive collar for ALL nine simple STRICT disk originals
and BOTH of its original cuts. The width is existential, not numerical.

Given ANY fixed $D>K_E$, choose
$\delta=\tfrac12\min(D-K_E,10-K_E)>0$ and
$q_3=q_4=\lambda^2\delta/(w_3+w_4)>0$. Then
$K=K_E+\delta<\min(D,10)$. Shrink that fixed actual collar so the remainder
in (17) is smaller than $(D-K)\eta^2$. This gives (2) for EVERY sufficiently
small positive $\eta$. Its leading imaginary profile is
$(7,-1,\ldots,-1)/\sqrt\lambda$, with $H\lambda=56$, so
$J_3\to336/\lambda^{3/2}=\sqrt{9H^3/14}$. Applying (3) proves that its
maximum normalized motion tends to $\mathsf A$, at2 and7. The uniform
upper bound (4) then gives exactly (5).

Every construction parameter here is in the STRICT open repair region.
No fourth-order zero-slack boundary is declared feasible. The limiting
infimum $K_E$ is approached by repairs; no exact-arm $D=K_E$ conclusion
is needed or obtained.

## Equality rigidity and the necessary budget

By (3), the normalized maximum motion differs from
$|J_3|\max_j|W_j|$ by $O_D(\sqrt\eta)$. If it tends to $\mathsf A$,
then $|J_3|\to\sqrt{9H^3/14}$. Centering/normalization changes the profile
by $O_D(\eta)$. Compactness and the equality classification in (15)
force its distance to $\mathcal E$ to zero; otherwise a convergent
subsequence separated from $\mathcal E$ would attain the same skewness
maximum outside its equality orbit.

For completeness identify the adopted cost formula from8619/8684. Put
\[
\rho=(c-5)/3,\quad\alpha=-527/360+(41/90)c+(13/90)c^2,\quad
\tau=(k+\rho)^2/2,\quad
B_*=2311/108+(4934/27)c-(1976/9)c^2,\quad
K_1=B_*-\alpha H^2/2.
\]
Their necessary finite optimization says that any limiting imaginary
profile $v\in\mathcal S$ in a fixed bounded-surplus arm has limiting
lower cost
$K(v)=K_1+\alpha\sum v_l^4+\tau(\sum v_l^3)^2/H$.
At EVERY $v\in\mathcal E$, $\sum v_l^4=43H^2/56$ and
$(\sum v_l^3)^2=9H^3/14$, and full exact field algebra gives
\[
K(v)=K_1+(43\alpha/56+9\tau/14)H^2=K_E.                        \tag{18}
\]
To prove (7), take a subsequence approaching the liminf surplus; the
reviewed rate and objective expansions make this surplus bounded, and
its bounded critical profiles have a further convergent subsequence.
The preceding rigidity places its limit in $\mathcal E$. Apply the
reviewed lower-cost statement and (18). This proves (7) independently
of the particular sharpness construction.

## Reproduction and trust boundary

`jets.py` computes all EIGHT Newton identities, every one of the TEN
anchored polynomial columns, and the entire root substitutions for ALL
NINE labels, in a three-variable moment ring over rational Gaussian
ninth-cyclotomic arithmetic. It compares all twelve field coordinates,
the complete table/gaps, all SEVEN skewness multiplicity cases, the
sharp constant, the physical embedding and the whole equality (18).
Its higher moments vanish only in the finite third jet; the ordinary
error estimate above justifies that truncation for actual competitors.

The optional source-pinned baseline comparison reproduces ALL nine cubic
maps of10036; it checks neither that entire older record nor the new
analytic theorem. The unchanged kernel is same-author reuse, not
independent review. No peer/reviewer executable or floating-point
value is imported. `verify.py` and `validate.py` check every typed field
of the regenerated finite record and reject ten deliberate mathematical
damages; analytic premises and universal bridges remain ordinary proof.
