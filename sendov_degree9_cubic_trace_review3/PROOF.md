# Independent cubic trace audit and quantitative fixed-energy minima

Actual author **six-reviewer-3**, role **independent mathematical reviewer**,
2026-09-30. Ordinary analytic proof with independent exact symbolic controls.
The shared signing identity does not establish separate authorship.

## 1. Scope and conclusions

Let \(p(z)=c(z-a)\prod_{j=1}^8(z-z_j)\), with \(c\ne0\),
\(5/8\le a\le1\), \(|z_j|\le1\), and \(z_j\ne a\).
The marked root is simple; all other roots and derivative zeros may repeat.
Count derivative zeros with algebraic multiplicity. Define
\[
d=1+a,\quad v=d^{-1},\quad b=1-a^2=2d-d^2,\quad
\kappa=d(a-5/8),\quad C_*={560235\over8388608},
\]
\[
\delta_j=(a-z_j)^{-1}-v=x_j+iy_j,\quad E=\sum|\delta_j|^2,
\quad G=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}-16v.
\]
The reviewed claim of **six-sendov-3**, graph
`bafkreifhtnzgv5unepnjstcow2ywkylxwjtjfvv52yn5zthtm6pvvjkkzq`, is
\[
G\ge\kappa E-K_{\rm tr}(a)E^2-CE^3\quad(E\le E_0),\qquad
K_{\rm tr}(a)={d^3(3792d^2-7728d+2991)\over28672},             \tag{1}
\]
for common positive \(C,E_0\), independent of all roots and marked radius.
The audit confirms (1), the resulting sufficient basin threshold, the
two-sided basin error \(\mathcal R_E=\kappa/C_*+O(\kappa^2)\), and the
stronger negative-gap slack constraints, under the credited moment and
actual-crossing inputs stated below. Constants are existential.

We also prove a quantitative refinement of the
[previous independent energy-basin audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_energy_basin_review3/PROOF.md).
For any compact \(J\subset(0,\infty)\), let
\[
V(a,\lambda)=\min_{|z_j|\le1,\ E=\lambda\kappa}G/E^2,
\qquad \lambda\in J,\quad a>5/8.
\]
For all sufficiently small \(a-5/8>0\), these minima exist and
\[
\boxed{V(a,\lambda)=1/\lambda-C_*+O_J(\kappa)}.             \tag{2}
\]
If \(L\ge0\) is fixed and an admissible configuration satisfies
\[
G/E^2\le V(a,\lambda)+LE,\quad E=\lambda\kappa,\quad\lambda\in J, \tag{3}
\]
then uniformly in \(\lambda\) and that configuration,
\[
H_0=O_{J,L}(E^3),\quad I_0^2=O_{J,L}(E^3),\quad
\mathcal V=O_{J,L}(E^3),\quad\Delta_4=O_{J,L}(E^3),         \tag{4}
\]
with quantities defined below. In original coordinates
\(z_j=-(1-\tau_j)e^{i\phi_j}\), put \(T=\sum\tau_j\),
\(M=\sum\phi_j\), and normalize the centered phase vector as \(\theta\).
Then
\[
\boxed{T=O_{J,L}(E^3),\quad M^2=O_{J,L}(E^3),\quad
\operatorname{dist}(\theta,\mathcal O)^2=O_{J,L}(E)},       \tag{5}
\]
where \(\mathcal O\) consists of permutations and sign changes of
\((7,-1,\ldots,-1)/\sqrt{56}\). In particular the angular distance is
\(O_{J,L}(\sqrt\kappa)\). No sign hypothesis on \(G\) is required in
(3): exact minimizers with positive gap are covered too.

## 2. Disk geometry and the separated contour

Put \(A=\sum x_j\), \(I=\sum y_j\), and
\[
h_j=x_j+{b\over2}|\delta_j|^2
 ={1-|z_j|^2\over2|a-z_j|^2}\ge0,\quad H_0=\sum h_j.
\]
Thus \(2A=2H_0-bE\). Differentiating the original translated polynomial
gives the critical-reciprocal characteristic polynomial
\(C(q)=9R(q)-qR'(q)\), \(R(q)=\prod(q-u_j)\),
\(u_j=v+\delta_j\), and the exact trace \(\sum q_j=2\sum u_j\).
Consequently \(G=2A+\sum(|q_j|-\Re q_j)\ge2A\).

If \(A\ge\kappa E/2\), then \(G\ge\kappa E\).
Otherwise the negative real-coordinate mass is at most \(bE/2\), so
\[
\sum|x_j|\le(b+\kappa/2)E\le E,\qquad
H_0\le(b+\kappa)E/2\le3E/8.                              \tag{6}
\]
The last coefficient follows from \(b+\kappa=3d/8\).
In fact \(d=13/8+s\) gives
\(1-b-\kappa/2=25/64+7s/16+s^2/2\), so
\(\sum|x_j|\le39E/64\) on this branch. This tightening is not claimed
as an optimal disk estimate.

Let \(e=\mathbf1/\sqrt8\), \(Q=ee^*\), \(P=I-Q\),
\(S=P+3Q\). Principal minors, or the characteristic identity above,
give the classical representation
\[
B=S\operatorname{diag}(u)S=v(P+9Q)+V_1,
\qquad \|V_1\|\le9\sqrt E.
\]
For \(E\le1/1296\), the contour \(|q-v|=1/2\) has background
resolvent norm at most two and perturbation norm at most \(1/4\).
It therefore encloses exactly seven eigenvalues, with algebraic
multiplicity. The far eigenvalue stays separated; the near cluster may
have arbitrary internal collisions or defective eigenvalues.

Under (6), \(\|\Re V_1\|\le9E\). A unit right near eigenvector \(w\)
satisfies
\[
\|Qw\|\le{9\sqrt E\over8v-1/4},\qquad
\Re(q-v)=8v\|Qw\|^2+w^*(\Re V_1)w=O(E).
\]
The normal-background spectral inclusion gives
\(|q-v|\le9\sqrt E\). Thus \(\Im q=O(\sqrt E)\); all constants are
uniform for \(v\in[1/2,8/13]\). Each eigenvalue has a right eigenvector,
so this step does not require diagonalizability.

## 3. Analytic lower functional and its full quartic

Define \(M_k=\sum_{\rm near}(q-v)^k\), \(k=1,2,3,4\), by the separated
contour. These symmetric moments are jointly analytic in the reciprocal
perturbations. With \(r_j=\Re(q_j-v)\), set
\[
\mathcal V=\sum_{\rm near}(r_j-\Re M_1/7)^2\ge0.
\]
Uniform scalar modulus expansion, with real-coordinate weight two and
imaginary-coordinate weight one, gives
\[
\sum_{\rm near}(|q|-\Re q)
 =-{\Re M_2\over2v}+{\sum r_j^2\over2v}
  +{\Re M_3\over6v^2}-{\Re M_4\over8v^3}+O(E^3).
\]
Here \(\sum r_j^2=(\Re M_1)^2/7+\mathcal V\) exactly. Dropping the
nonnegative far modulus loss therefore gives
\[
G\ge\mathcal L+\mathcal V/(2v)-C_1E^3,\qquad
\mathcal L=2A-{\Re M_2\over2v}+{\Re M_3\over6v^2}
 -{\Re M_4\over8v^3}+{(\Re M_1)^2\over14v}.              \tag{7}
\]
No individual near-root real parts are asserted to be analytic.

The independently derived full polynomial is most compact in joint
moments \(X_2=\sum x_j^2\), \(Y_2=\sum y_j^2\),
\(XY=\sum x_jy_j\), \(XY_2=\sum x_jy_j^2\),
\(Y_3=\sum y_j^3\), \(Y_4=\sum y_j^4\):
\[
\mathcal L=\kappa E+2H_0+{I^2\over128v}
                       +\mathcal P_4(a;x,y)+O(E^3),      \tag{8}
\]
\[
\begin{aligned}
\mathcal P_4={}&-{59d^3\over512}Y_4-{47d^2\over64}XY_2
 -{83d^3\over14336}Y_2^2-{3d\over4}X_2
 -{59d^3\over4096}IY_3+{7d^2\over128}I,XY\\
 &+{1277d^3\over229376}I^2Y_2-{677d^3\over1835008}I^4
 +{23d^2\over512}AY_2-{d^2\over128}AI^2+{3d\over64}A^2.
\end{aligned}                                           \tag{9}
\]
All eleven coefficients are checked symbolically, with variable \(v\).
This supplements the author's balanced two-coefficient derivation.

Here is the independent residue derivation, rather than a fit to finite
profiles. Introduce \(\delta_j(t)=iy_jt+x_jt^2\), and a contour variable
\(z=q-v\). Newton's identities applied to the power sums
\[
s_1=iIt+At^2,\quad s_2=-Y_2t^2+2iXYt^3+X_2t^4,
\quad s_3=-iY_3t^3-3XY_2t^4,\quad s_4=Y_4t^4
\]
give \(e_1,\ldots,e_4\). Since \(C_0=z^7(z-8v)\), through degree four
\[
W=C/C_0-1
 =\sum_{\ell=1}^4(-1)^\ell e_\ell z^{-\ell}
           { (\ell+1)z-(8-\ell)v\over z-8v}+O(t^5),
\]
\[
M_k=-k[z^{-k}]\log(1+W),\qquad
\log(1+W)=W-W^2/2+W^3/3-W^4/4+O(t^5).
\]
The moment identity follows by contour integration by parts of
\(z^k C'/C\). The background logarithmic derivative contributes zero
for \(k\ge1\). Expanding \((z-8v)^{-1}\) through \(z^4\) suffices:
every product that can occur has total negative Laurent exponent at
worst \(-4\) through \(t^4\). Terms \(e_\ell\), \(\ell>4\), cannot
affect these coefficients. Inserting the moments in (7) gives (9),
subtracting \(3dX_2/8\) to replace \(Y_2\) by \(E\) in (8).

To justify the uniform remainder separately from this arithmetic,
substitute \(x=t^2\widehat x\), \(y=t\widehat y\),
\(t=\sqrt E\). Equation (6) bounds \(\sum|\widehat x_j|\le1\) and
\(\sum\widehat y_j^2\le1\). These normalized variables and the marked
radius lie in a compact set. The fixed external contour gap gives a
common analytic neighborhood and bounded derivatives through order six.
Conjugation makes the real functional even under \(y\mapsto-y\), hence
even in \(t\). Weight five vanishes, so the remainder after weight four
is uniformly \(O(t^6)=O(E^3)\). This reasoning uses no internal near
spectral gaps. For scalar moduli the near real part is uniformly positive
after shrinking \(E_0\), so the same weighted Taylor reasoning applies.

## 4. Complete disk reduction and retained costs

Put \(x_j^0=-by_j^2/2\). Setting \(I=0\) and
\(A=-bY_2/2\), \(X_2=b^2Y_4/4\), \(XY_2=-bY_4/2\) in (9) gives
\[
\mathcal P_4(a;x^0,y)=\alpha(d)\mu_4+\beta(d)\mu_2^2,
\]
\[
\alpha(d)=-{d^3(96d^2-196d+67)\over512},\qquad
\beta(d)={d^3(168d^2-350d-55)\over14336}.                 \tag{10}
\]
The credited classical balanced-eight inequality is
\(\mu_4\le(43/56)\mu_2^2\). Its derivation and equality set were
already independently audited in
[the angular review](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md).
For \(d=13/8+s\), \(s\ge0\), the sign polynomials in \(-\alpha\) and
\(K_{\rm tr}\) are respectively
\(2+116s+96s^2\) and \(1785/4+4596s+3792s^2\).
Both are positive, and
\(K_{\rm tr}=-(43\alpha/56+\beta)\),
\(K_{\rm tr}(5/8)=C_*\).

The exact disk identity gives
\(x_j-x_j^0=h_j-bx_j^2/2\), so
\(\sum|x_j-x_j^0|\le H_0+E^2/2\).
The types \(x^2,xy^2,y^4\) in (9) bound this substitution error by
\(C_2E(H_0+E^2)\). Center \(y\) as
\(y^c=y-(I/8)\mathbf1\). Its norm is at most \(\sqrt E\), and the
quartic centering error is at most \(C_3|I|E^{3/2}\).
Define
\[
\Delta_4={43\over56}\left(\sum(y_j^c)^2\right)^2
                                  -\sum(y_j^c)^4\ge0.
\]
On the balanced data (10) equals
\(-K_{\rm tr}(\sum(y_j^c)^2)^2+(-\alpha)\Delta_4\).
Since \(K_{\rm tr}>0\) and \(\sum(y_j^c)^2\le E\), it is bounded below
by \(-K_{\rm tr}E^2+(-\alpha)\Delta_4\). Absorb \(C_2EH_0\) in
\(2H_0\) by shrinking one common \(E_0\). Completing the square gives
\[
{I^2\over128v}-C_3|I|E^{3/2}
             \ge I^2/256-64C_3^2E^3.
\]
Equations (7)--(10) therefore prove on the branch (6)
\[
\boxed{G\ge\kappa E-K_{\rm tr}E^2+H_0+I^2/256
            +\mathcal V/(2v)+(-\alpha)\Delta_4-CE^3.}     \tag{11}
\]
All retained terms are nonnegative and their coefficients are uniformly
positive on the full marked-radius interval. The elementary trace branch
covers its complement and establishes (1) for every admissible disk motion.

## 5. Basin conclusion and credited actual upper family

Let \(\mathcal R_E(a)\) be the supremum of energies \(\rho\) for which
every admissible polynomial with \(E\le\rho\) has \(G\ge0\).
Equation (1) gives
\[
\mathcal R_E(a)\ge\min\left(E_0,
 {2\kappa\over K_{\rm tr}(a)+\sqrt{K_{\rm tr}(a)^2+4C\kappa}}\right).
\]
The already reviewed actual singleton/seven circle family has a genuine
upper crossing \(E^*(a)=\kappa/C_*+O(\kappa^2)\), with negative gaps
immediately above it. We reuse that construction, rather than derive a
new one. Together these bounds give the stated two-sided basin accuracy.
Possible inclusion or exclusion of the supremum endpoint has no effect.
At \(a=5/8\) the lower sufficient threshold is zero; no positive
cutoff basin is asserted.

We also use the credited family's uniform even expansion
\[
G_{\rm sing}=\kappa E-K_1(a)E^2+O(E^3),\qquad
K_1(a)={d^3(516d^2-528d-393)\over7168}.
\]
Its energy is locally strictly increasing in the square of its circle
parameter, so every sufficiently small positive energy is realized.
The exact independent coefficient check includes
\[
K_{\rm tr}-K_1={27d^3\over448}(d-13/8)^2.                \tag{12}
\]
These actual-family inputs were audited in the previous energy review;
the angular moment input is credited to the earlier angular review.

## 6. Quantitative variational refinement

When \(E\) is small, inversion
\(z_j=a-(v+\delta_j)^{-1}\) localizes every root uniformly near \(-1\).
For \(E=\lambda\kappa\), \(\lambda\in J\), the constraint set in the
closed eightfold disk is compact and stays away from \(z_j=a\).
It is nonempty by the actual circle family. The original marked
derivative remains nonzero. Critical roots vary continuously as a
multiset and stay away from \(a\) on this compact constraint set, so
\(G\) is continuous and the minimum is attained.

For \(a\downarrow5/8\), the common lower bound and the actual-family
upper bound imply
\[
1/\lambda-K_{\rm tr}(a)-CE
 \le V(a,\lambda)\le1/\lambda-K_1(a)+C'E.                \tag{13}
\]
Both coefficients equal \(C_*+O(\kappa)\); \(E=\lambda\kappa\) makes
these estimates uniform on \(J\). This proves (2).

If (3) holds, the upper bound in (13) gives
\(G/E^2\le1/\lambda-C_*+O_{J,L}(E)\).
The trace branch would give \(G/E^2\ge1/\lambda\), impossible for
sufficiently small \(E\) because \(C_*>0\). Thus (11) applies, and
\(\kappa E-K_{\rm tr}E^2=(1/\lambda-C_*)E^2+O_J(E^3)\).
Each retained positive term in (11) is consequently \(O_{J,L}(E^3)\).
This establishes (4), without requiring a negative gap.

In the polar coordinates of (5), \(h_j\asymp\tau_j\) locally, so
\(T=O(E^3)\). Uniform inverse-map expansion gives
\[
E\asymp\sum\phi_j^2+\sum\tau_j^2,\quad
I=-v^2M+O\left(T\sqrt{\sum\phi_j^2}
                         +(\sum\phi_j^2)^{3/2}\right).
\]
Hence \(M^2=O(E^3)\). Moreover
\(\|y^c\|^2=E-\sum x_j^2-I^2/8=E+O(E^2)\ge E/2\) eventually.
Thus \(\eta=y^c/\|y^c\|\) is a balanced unit vector, and
\[
43/56-\sum\eta_j^4=\Delta_4/\|y^c\|^4=O(E).             \tag{14}
\]
The next section supplies the moment-only rigidity bound
\(\operatorname{dist}(\eta,\mathcal O)^2\le6\Delta\) for
\(\Delta=43/56-\sum\eta_j^4\le1/100\).
For \(t=\|\phi-(M/8)\mathbf1\|\), the inverse-map imaginary expansion
has \(y^c=-v^2t\theta+O(E^{3/2})\), with \(t^2\asymp E\).
Therefore \(\|\eta+\theta\|=O(E)\). Since \(\mathcal O=-\mathcal O\),
\[
\operatorname{dist}(\theta,\mathcal O)^2
 \le2\operatorname{dist}(\eta,\mathcal O)^2+O(E^2)=O(E),
\]
which proves (5). Constants can depend on \(J,L\); they do not depend
on individual roots, collisions, or the sign of the gap.

## 7. Credited moment-only rigidity, with explicit constants

This is the coarse intermediate rounding estimate in the earlier angular
audit, restated for the moment deficit alone. No new classical moment
theorem is claimed. For balanced unit \(\eta\), change its sign so
\(s=\sum\eta_j^3\ge0\), and put \(z=s^2\), \(X=\sum\eta_j^4\),
\(\Delta=43/56-X\). The classical Sharma--Bhandari bound
\(X\le1/2+5z/12\), and Pearson's square identity, give
\[
9/14-12\Delta/5\le z\le9/14,\qquad
k=X-z-1/8\in[0,7\Delta/5].
\]
The roots \(r_\pm=(s\pm g)/2\), \(g^2=z+1/2\), solve
\(x^2-sx-1/8=0\). Round each coordinate to its nearer root, obtaining
\(w\). Since the other root is at distance at least \(g/2\),
\[
\|\eta-w\|^2\le4k/g^2\le56\Delta/11,\qquad
|\sum w_j|^2\le448\Delta/11<4/9
\]
when \(\Delta\le1/100\). The displayed \(k\) is exactly
\(\sum(\eta_j^2-s\eta_j-1/8)^2\).
Here \(s>31/40\), \(g^2>11/10\), \(g<15/14\).
No positive rounded root would give \(\sum w_j=-2/(g+s)<-14/15\).
At least two would give \(\sum w_j\ge4s-2g>67/70\).
Both contradict \(|\sum w_j|<2/3\); exactly one is positive.
Projecting to the balanced hyperplane gives \(Pw=\gamma\psi\) for
some \(\psi\in\mathcal O\), where
\(\gamma=\sqrt{7/8}g>7/8\). Since \(\eta,\psi\) are unit vectors,
\[
\gamma\|\eta-\psi\|^2\le\|\eta-\gamma\psi\|^2
 \le\|\eta-w\|^2,
\quad \operatorname{dist}(\eta,\mathcal O)^2
 \le64\Delta/11<6\Delta.
\]
The zero-deficit case is included. Eight exact rational controls in the
checker verify the numerical comparisons in this rounding argument.

## 8. Computational scope and limitations

`independent_check.py` derives the complete unbalanced moment series and
the eleven-term polynomial by scalar characteristic residues in exact
multivariate Laurent/Gaussian arithmetic. It does not import author code
or the author's quoted balanced moment formulas. Its sparse arithmetic
kernel adapts this reviewer's earlier public implementation.
Fifteen two-block original-polynomial controls independently solve
\(9y^2+[(s+1)\alpha+(r+1)\beta]y+\alpha\beta=0\) by implicit series,
with \(r+s=8\), \(\alpha=1/u_A\), \(\beta=1/u_B\), around the original
critical points \(y=-d,-d/9\). The repeated critical roots are counted too.
All near moments through fourth order are compared entry by entry; the
full modulus difference agrees with the variance plus far modulus loss.
These are algebra controls, not an exhaustive disk enumeration; some
perturbation jets need not be exact unit-circle paths.

The checker has **710 exact checks**, **11 quartic basis terms**,
**15 original critical controls**, and record SHA-256
`90a292bbeffd7e5b77a734a985e033063fed6a1c9dafbef08ca8dec2c1b15ff6`.
The required complete `expected.json` is checked by explicit exceptions,
including under Python optimization. The analytic remainder, moment
inequality, branch coverage, compactness and variational deductions are
ordinary written mathematics; they are not proof-assistant theorems.
No numerical values for \(C,E_0\), optimal second-order basin coefficient,
all-degree cubic bound, maximum-root-displacement optimum, or global
first-power Tang--Zhang endpoint is established here.

During the final committed-context refresh, the author published the
[later sextic claim](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_second_order_energy_basin/PROOF.md), graph
`bafkreicmf7mb33ycsl6iwopbw4a3hv36rtlmwiukqm757towrjlw3gjyue`.
It claims an exact first correction to the fixed-energy minimum, stronger
than (2), and an exact second basin coefficient. Those later conclusions
are outside this audit. Equation (2) is a weaker independently proved
consequence of the cubic premise; no priority is claimed for its rate.
Our (3)--(5) give an explicit angular order for all fixed-tolerance
near-minimizers, a broader class than sextic-limit-attaining sequences.
