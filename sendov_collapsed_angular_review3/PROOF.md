# Independent angular quartic audit and sharper degree-nine geometry

Actual author: **six-reviewer-3**, role **independent mathematical reviewer**.
2026-09-30. Ordinary written proof with independent exact arithmetic;
the analytic bridges are not proof-assistant formalized.

## Statement and scope

For each fixed integer \(m\ge3\), put
\[
 n=m+1,\qquad a=\frac{m+2}{2m},\qquad v=\frac{2m}{3m+2},
 \qquad p_m=\frac{(m+2)(3m+2)^3}{256m^7}.
\]
For a real balanced nonzero vector \(\theta\), let
\[
 p_{t,\theta}(z)=(z-a)\prod_{j=1}^m(z+e^{i\theta_jt}),\quad
 u_j=(a+e^{i\theta_jt})^{-1},\quad
 E=\sum_j|u_j-v|^2,\quad F=\sum_{p'_{t,\theta}(\zeta)=0}|a-\zeta|^{-1}.
\]
Derivative zeros are counted with multiplicity. Set
\(\mu_k=\sum\theta_j^k\), \(e=m^{-1/2}(1,\ldots,1)^T\),
\(Q=ee^*\), \(P=I-Q\), \(\Theta=\operatorname{diag}\theta\),
\(A=P\Theta P|_{e^\perp}\), and \(w=\Theta e\).
For each distinct eigenvalue of the Hermitian matrix \(A\), use its full
orthogonal projection \(\Pi_\lambda\), and define
\[
 \Psi=\sum_\lambda\|\Pi_\lambda w\|^4,\quad
 X=\mu_4/\mu_2^2,\quad \eta=m^2\Psi/\mu_2^2 .
\]
Then
\[
 F=2mv-K_m(\theta)E^2+o(E^2),\qquad
 K_m=p_m\{m(m^2-4m-4)X+(13m+18)-9(m+2)\eta\}.                 \tag{1}
\]
For fixed \(m\), the normalized remainder is uniform on
\(\mathcal S_m=\{\theta:\sum\theta_j=0,\ \mu_2=1\}\).
The coefficient is continuous, including spectral collisions, and invariant
under permutations and nonzero real rescaling.

For \(m\ge4\), every such vector satisfies
\[
 X\le X_*=\frac{m^2-3m+3}{m(m-1)},\qquad
 \eta\ge\frac{m(m-1)X-(2m-3)}{(m-2)(m-3)}.                 \tag{2}
\]
For \(m\ge8\),
\[
 \max_{\mathcal S_m} K_m
 =p_m\left\{\frac{m^2(m^2-4m-4)}{m-1}-(m-6)(3m+2)\right\}. \tag{3}
\]
Equality consists exactly of the permutations and sign changes of
\((m-1,-1,\ldots,-1)/\sqrt{m(m-1)}\).

For \(m=8\), \(p=p_8=10985/33554432\), the complete range is
\[
 \left[\frac{164775}{8388608},\frac{560235}{8388608}\right]
 =[60p,204p].                                             \tag{4}
\]
Its minimum is attained exactly at the balanced four-positive/four-negative
equal-magnitude vectors. Let
\[
 \delta=204p-K_8(\theta),\quad
 \mathcal O=\left\{\pm\text{ permutations of }(7,-1,\ldots,-1)/\sqrt{56}\right\}.
\]
The proved improvement over the reviewed source is
\[
 \boxed{\delta\le14p/25\quad\Longrightarrow\quad
       \min_{\psi\in\mathcal O}\|\theta-\psi\|^2\le\delta/(64p).} \tag{5}
\]
Here \(\theta\in\mathcal S_8\). The coefficient \(1/64\) is \(7/48\)
of the source coefficient \(3/28\); no optimality of (5) is claimed.

These are angular statements with the marked root fixed at \(a\).
They do not optimize the maximum original-root displacement, reduce inward
motions or nonlinear mean phase, or prove a global first-power reciprocal
endpoint.

## Scalar characteristic calculation

Write \(R(q)=\prod(q-u_j)\). Direct differentiation of the translated
polynomial, using \(q=(a-z)^{-1}\), gives the monic characteristic polynomial
for the critical reciprocals:
\[
 G(q)=nR(q)-qR'(q).                                       \tag{6}
\]
The marked root is simple and \(a+e^{i\theta_jt}\ne0\), so no critical
reciprocal is lost. Alternatively, the rank-one determinant formula gives
\(G=\det(qI-(I+J)\operatorname{diag}u)\), with \(J\) the all-ones matrix.
This matrix is similar to
\[
 B=S\operatorname{diag}u\,S,\qquad S=P+\sqrt n\,Q.
\]
At \(t=0\), its near eigenvalue is \(v\) with multiplicity \(m-1\), and
its far eigenvalue is \(nv\), with gap \(g_0=mv>0\).

The scalar reciprocal Taylor coefficients are
\[
 u_j=v-iv^2\theta_jt+c_2\theta_j^2t^2+
       ic_3\theta_j^3t^3+c_4\theta_j^4t^4+O(t^5),
\]
\[
 c_2=v^2/2-v^3,\quad c_3=v^2/6-v^3+v^4,\quad
 c_4=-v^2/24+7v^3/12-3v^4/2+v^5.                         \tag{7}
\]
Let \(s_k=\sum(u_j-v)^k\), and let \(e_\ell\) be the corresponding
elementary symmetric polynomials. Through order four,
\[
\begin{aligned}
s_1&=c_2\mu_2t^2+ic_3\mu_3t^3+c_4\mu_4t^4,\\
s_2&=-v^4\mu_2t^2-2iv^2c_2\mu_3t^3+(c_2^2+2v^2c_3)\mu_4t^4,\\
s_3&=iv^6\mu_3t^3-3v^4c_2\mu_4t^4,\qquad
s_4=v^8\mu_4t^4 .
\end{aligned}                                            \tag{8}
\]
Use \(\ell e_\ell=\sum_{k=1}^\ell(-1)^{k-1}e_{\ell-k}s_k\).
With \(q=v+\xi\), (6) gives
\[
 G/G_0=1+W,\quad G_0=\xi^{m-1}(\xi-mv),\quad
 W=\sum_{\ell=1}^4(-1)^\ell e_\ell\xi^{-\ell}
       \frac{(\ell+1)\xi-(m-\ell)v}{\xi-mv}+O(t^5).          \tag{9}
\]
For \(m=3\), \(e_4=0\) for the actual three slopes; the Newton expression
automatically enforces this, so (9) is still valid. The Laurent series
is taken on a fixed near contour, inside \(|\xi|<mv\), enclosing all near
roots for small \(t\), not at a zero of \(G\). Since \(W=O(t^2)\),
\(\log(1+W)=W-W^2/2+O(t^6)\). If
\(M_\ell=\sum_{\rm near}(q-v)^\ell\), contour integration by parts gives
\[
 M_\ell=-\ell[\xi^{-\ell}]\log(G/G_0).                     \tag{10}
\]
The independent checker implements (8)--(10), rather than the author's
ordered noncommutative contour-word enumeration. Terms with \(e_\ell\),
\(\ell>4\), cannot affect order four. Expanding the pole in (9) through
\(\xi^4\) suffices: in \(W^2\) at this order the smallest possible power
is \(\xi^{-4}\).

For clarity, write
\[
 T_4=\operatorname{tr}A^4=(1-4/m)\mu_4+2\mu_2^2/m^2,\quad
 U=w^*A^2w=\mu_4/m-\mu_2^2/m^2,\quad R_0=w^*w=\mu_2/m.
\]
The exact scalar calculation yields
\[
\begin{aligned}
[t^4]\Re M_2={}&c_2^2(T_4+2U+R_0^2)+2v^2c_3(T_4+2U)\\
 &+\frac{2nc_2v^4}{g_0}(3U+R_0^2)
   -\frac{2nv^8}{g_0^2}U+\frac{n^2v^8}{g_0^2}R_0^2,\\
[t^4]\Re M_3={}&-3c_2v^4(T_4+U)-\frac{3nv^8}{g_0}U,\\
[t^4]\Re M_4={}&v^8T_4,\qquad [t^2]M_2=-v^4\operatorname{tr}A^2 .
\end{aligned}                                            \tag{11}
\]
The trace and coupling formulas follow by expanding \(P=I-ee^*\).
A separate direct rational-matrix implementation checks them for 85
profiles at \(m=3,\ldots,12\). These profiles are controls, not a proof by
interpolation.

## Spectral collisions and the uniform analytic bridge

A near invariant subspace exists analytically and uniformly in \(\theta\)
on \(\mathcal S_m\), by the fixed gap \(g_0\). Its graph over \(e^\perp\)
gives an effective matrix
\[
 T=vI-iv^2At+Ct^2+O(t^3),\qquad
 C=c_2A^2+c_Rww^*,\quad c_R=c_2+nv^3/m.                   \tag{12}
\]
Indeed, if \(B=B_0+tV_1+t^2V_2+\cdots\), its first graph coefficient is
\(-QV_1P/g_0\). Thus its second coefficient is
\(PV_2P-PV_1QV_1P/g_0\), which gives (12).
Both \(A\) and \(C\) are Hermitian.

Every repeated eigenspace of \(A\) has zero \(w\)-weight. To see this,
\(Ay=\lambda y\), \(y\perp e\), implies
\((\Theta-\lambda I)y=\sigma e\).
If \(\lambda\) is a diagonal value of \(\Theta\), then \(\sigma=0\)
and \(y\) is supported in that equal-value block, so
\(w^*y=\lambda e^*y=0\).
If \(\lambda\) is not a diagonal value, the possible eigenvectors lie
in the one-dimensional span of \((\Theta-\lambda I)^{-1}e\).
Consequently every repeated eigenspace has zero weight, and its
compressed second coefficient is precisely \(c_2\lambda^2I\).
Within a simple eigenspace it is the scalar
\(c_2\lambda^2+c_R\|\Pi_\lambda w\|^2\). For fixed \(\theta\), perturbing
the semisimple first coefficient in (12) therefore gives
\[
 \lim_{t\to0}t^{-4}\sum_{\rm near}[\Re(q-v)]^2
 =c_2^2T_4+2c_2c_RU+c_R^2\Psi.                           \tag{13}
\]

Here is the additional uniformity check; a pointwise expansion would
not suffice. Suppose \(\theta_k\to\theta_0\) and \(t_k\to0\).
Group the eigenvalues of \(A(\theta_k)\) by the distinct limiting
eigenvalues of \(A(\theta_0)\). Their group projections converge, and
different groups have fixed positive gaps. Use orthonormal bases for
these Hermitian groups and remove intergroup coupling in the divided
matrix \((T-vI)/t\), whose off-diagonal second term is \(O(t)\).
The resulting group matrix is
\[
 -iv^2A_{k,\rm group}+t_k C_{k,\rm group}+O(t_k^2).
\]
The remainder is bounded using only gaps between limiting groups; no
bound on gaps within a group is needed. In a repeated limiting group,
\(C_{k,\rm group}\to c_2\lambda_0^2I\). For a normalized right eigenvector
\(h\), taking the real part of its eigenvalue equation eliminates
\(-iv^2h^*A_{k,\rm group}h\). Hence
\(\Re(q-v)/t_k^2\to c_2\lambda_0^2\), uniformly within the group.
A simple limiting group is one-dimensional and gives the ordinary
scalar limit. This proves the sequential, and thus compact-uniform,
version of (13), including splittings on the same scale as \(t_k\).

Also \(\Psi\) is continuous: a repeated limiting group has total
coupling weight tending to zero; the sum of squares of its split
weights is bounded by the square of that total. Simple-group projections
converge normally. This explains why grouping full eigenspaces causes
no discontinuity in this particular compression problem.

Uniformly, \(x=\Re(q-v)=O(t^2)\) and \(y=\Im q=O(t)\) for near roots.
For example, normality of \(B_0\) gives an \(O(t)\) spectral displacement,
and the projected eigenvalue equation gives the \(Q\)-component of a
unit right eigenvector as \(O(t)\). In
\(\Re(q-v)=g_0\|Qh\|^2+\Re h^*(B-B_0)h\), the Hermitian part of
\(B-B_0\) is \(O(t^2)\), proving the bound on \(x\).

For such \(x,y\), scalar modulus expansion and summation give
\[
 \sum_{\rm near}(|q|-\Re q)=
 -\frac{\Re M_2}{2v}+\frac{\sum x^2}{2v}
 +\frac{\Re M_3}{6v^2}-\frac{\Re M_4}{8v^3}+O(t^6).        \tag{14}
\]
The real contour traces are analytic and even in real \(t\), uniformly
on the compact sphere. The simple far branch has zero first derivative
by balance; conjugation symmetry makes its imaginary part \(O(t^3)\).
Its modulus-minus-real contribution is therefore \(O(t^6)\).
Since \(\operatorname{tr}B=2\sum u_j\), (11)--(14) yield
\[
 [t^4]F=
 \frac{m(m+2)}{(3m+2)^5}
 \{-m(m^2-4m-4)\mu_4-(13m+18)\mu_2^2
       +9m^2(m+2)\Psi\}.                                \tag{15}
\]
The balanced quadratic term cancels exactly at this \(a\).
Finally \(E=v^4\mu_2t^2+O(t^4)\) uniformly, giving (1).
The code checks (15) symbolically in \(m\) and the moment indeterminates;
(12)--(14) and compactness remain ordinary mathematical proof.

## Classical scalar moment bound, with its degenerate case

Normalize \(\mu_2=1\); put \(s=\mu_3\), \(z=s^2\).
The scalar inequality
\[
 X\le\tfrac12+\frac{m-3}{2(m-2)}z                         \tag{16}
\]
is credited to Sharma--Bhandari, Theorem 1 and Lemma 1 of
[arXiv:1309.2896v1](https://arxiv.org/pdf/1309.2896v1).
We reconstruct the needed argument, rather than relying on the paper's
status as a certificate. In \(\prod(x-\theta_j)\), the first relevant
coefficients are \(c_2'=-1/2\), \(c_3'=-s/3\),
\(c_4'=1/8-X/4\). Differentiating \(m-4\) times leaves a real-rooted
quartic with coefficients of \(x^2,x,1\) equal to
\(12(m-2)(m-3)c_2'\), \(24(m-3)c_3'\), \(24c_4'\).
When \(c_4'\ne0\), reverse this quartic and differentiate. Its derivative
is \(24y\) times
\[
 4c_4'y^2+3(m-3)c_3'y+(m-2)(m-3)c_2'.
\]
Rolle's theorem, including repeated roots, forces the quadratic
discriminant nonnegative. Dividing by \(m-3>0\) gives
\(9(m-3)(c_3')^2-16(m-2)c_2'c_4'\ge0\), precisely (16).
For \(c_4'=0\), pass to balanced unit vectors with \(c_4'\ne0\).
Such vectors are dense: \(c_4'\) is a nonzero polynomial restriction
on this connected sphere (the singleton profile has \(X_*>1/2\)).
Both sides are continuous, so no missing reciprocal-root case remains.

Pearson's square identity gives
\[
 k=\sum_j(\theta_j^2-s\theta_j-1/m)^2=X-z-1/m\ge0.          \tag{17}
\]
Combining (16) and (17) proves \(X\le X_*\).
At equality both scalar inequalities are equalities, so every slope
is one of the two roots of \(x^2-sx-1/m\). They have opposite signs.
Balance and normalization, with multiplicities \(r,t=m-r\), give
\(X=(m^2-3rt)/(mrt)\); attaining \(X_*\) forces \(rt=m-1\),
hence \(r=1\) or \(t=1\). This also proves the endpoint equality classification.

## Independent spectral Gram certificate, including zero denominators

Choose an orthonormal eigenbasis of \(A\) and set
\(\rho_i=m|\langle w,h_i\rangle|^2\), \(i=1,\ldots,m-1\).
Repeated groups have zero weight, so the grouped invariant is
\(\eta=\sum_i\rho_i^2\). Direct contraction gives
\[
 \sum\rho_i=1,\quad\sum\lambda_i\rho_i=s,\quad
 \sum\lambda_i^2\rho_i=X-1/m,
\]
\[
 T_2=(m-2)/m,\quad T_3=(m-3)s/m,\quad
 T_4=(m-4)X/m+2/m^2,\quad \sum\lambda_i=0.
\]
Define the vector
\(q_i=\lambda_i^2-T_2/(m-1)-(T_3/T_2)\lambda_i\).
It is orthogonal to \(1\) and \(\lambda\). Its squared norm and pairing
with \(\rho\) are
\[
 D=T_4-T_2^2/(m-1)-T_3^2/T_2,\qquad
 N=X-\frac{2m-3}{m(m-1)}-\frac{m-3}{m-2}z .
\]
Bessel's inequality yields
\[
 \eta\ge B+N^2/D,\qquad B=1/(m-1)+mz/(m-2),              \tag{18}
\]
when \(D>0\). Let
\[
 \Delta=X_*-X,\quad z_0=\frac{2(m-2)}{m-3}(X-1/2),\quad
 h=z-z_0\ge0,\quad c=(m-2)/m,\quad\beta=(m-3)/(m-2).
\]
Then \(D=c\Delta-c\beta^2h\), \(N=\Delta-\beta h\).
If \(D=0\) and \(\Delta>0\), these imply
\(N=-\Delta/(m-3)\ne0\), contradicting \(q=0\).
Thus \(D>0\) off the moment endpoint. With
\(L=[m(m-1)X-(2m-3)]/[(m-2)(m-3)]\), the exact positive certificate is
\[
 (B-L)D+N^2=\frac{\Delta h}{(m-2)^2}\ge0.                 \tag{19}
\]
Equations (18)--(19) give \(\eta\ge L\).
At \(\Delta=0\), the classified singleton has one active spectral
weight, so \(\eta=1=L\); no division by zero is used.
The checker constructs and checks (19) after clearing all denominators,
as a universal polynomial identity, not at sampled degrees.

## Angular optimization, range and essential domain

Substitute \(\eta\ge L\) into (1). Its affine slope in \(X\) is
\[
 b_m=\frac{mP_m}{(m-2)(m-3)},\qquad
 P_m=m^4-9m^3+13m^2-13m-6 .
\]
Since
\(P_{8+u}=u^4+23u^3+181u^2+515u+210>0\) for \(u\ge0\),
\[
 K_m\le p_m T_m-p_m b_m\Delta,\qquad
 T_m=\frac{m^2(m^2-4m-4)}{m-1}-(m-6)(3m+2).              \tag{20}
\]
The singleton attains this with \(\eta=1\).
Strict positivity of \(b_m\) proves (3) and its complete equality set.

At \(m=8\), \(b_8=56\) and \(T_8=204\).
For the minimum, \(X\ge1/8\) by the square mean inequality and
\(\eta\le1\); hence \(K_8\ge p(224/8+122-90)=60p\).
Equality in \(X\ge1/8\), combined with balance, forces exactly four
slopes of each sign and common magnitude \(1/\sqrt8\).
This two-block direction has one active spectral weight and attains
the lower value. Continuity on the connected sphere \(\mathcal S_8\cong
S^6\) shows that the image is the full interval (4).

The bound \(m\ge8\) in the optimizer is essential to this theorem.
For \(m=7\), a moving pair has \(X=\eta=1/2\), while the singleton has
\(X=31/42,\eta=1\). The former coefficient is
\(109503/1647086\), the latter \(25368195/421654016\); their difference
is \(2664573/421654016>0\).
The moving-pair weight assertion follows exactly from
\(w^*Aw=0\) and \(A^2w=(1-2/m)w\); the two active eigenvalues are
opposite and their weights equal. A two-block vector
\((t^r,-r^t)\) satisfies \(Aw=(t-r)w\) and has \(\eta=1\).
These operator controls are independently checked with rational matrices.

## Proof of the improved near-maximizer geometry

By (20), \(\delta\ge56p\Delta\). Under the hypothesis of (5),
\(0\le\Delta\le1/100\). Change the sign of \(\theta\) so \(s\ge0\).
Equations (16)--(17) imply
\[
 9/14-12\Delta/5\le z\le9/14,\qquad k\le7\Delta/5.
\]
Let \(r_\pm=(s\pm g)/2\), \(g=\sqrt{z+1/2}\), and round every slope
to its closest root, giving \(y\). The more distant root is at least
\(g/2\) away, so
\[
 \|\theta-y\|^2\le4k/g^2\le56\Delta/11,\qquad
 |\sum y_j|^2\le448\Delta/11<4/9.                         \tag{21}
\]
Indeed \(z\ge1083/1750>3/5\), \(s>31/40\), \(g<15/14\),
and \(g^2>11/10\).
If no slope rounds to \(r_+\), then
\(\sum y_j=-2/(g+s)<-14/15\).
If at least two do, then \(\sum y_j\ge4s-2g>67/70\).
Both contradict (21). Exactly one slope rounds to \(r_+\).
For its corresponding singleton \(\psi\),
\[
 Py=\alpha\psi,\qquad \alpha=\sqrt{7/8}\,g>7/8.
\]
Since \(P\) is an orthogonal projection and both \(\theta,\psi\) are unit,
\[
 \alpha\|\theta-\psi\|^2
 =\|\theta-\alpha\psi\|^2-(1-\alpha)^2
 \le\|\theta-y\|^2.
\]
Thus \(d^2=\|\theta-\psi\|^2\le64\Delta/11<6\Delta\)
when \(\Delta>0\); at \(\Delta=0\) the distance is zero by classification.

Now write \(\theta=c\psi+u\), \(u\perp\psi,e\).
The coarse estimate gives \(c=1-d^2/2\ge97/100\) and
\(\tau=\|u\|^2=1-c^2\le3/50\). At the distinguished coordinate \(u_j=0\);
the other seven \(u\)-coordinates sum to zero.
With \(B_0=-1/\sqrt{56}\), exact expansion gives
\[
 X=c^4X_*+6c^2B_0^2\tau+4cB_0\sum u_j^3+\sum u_j^4 .
\]
Use \(|\sum u_j^3|\le\tau^{3/2}\), \(\sum u_j^4\le\tau^2\),
\(c\le1\), and \(c^2=1-\tau\), to obtain
\[
 \Delta\ge\tau\left\{\frac{10}{7}
         -4|B_0|\sqrt\tau-\frac{93}{56}\tau\right\}.
\]
Since \(\sqrt\tau\le1/4\) and \(|B_0|<1/7\), the bracket is at least
\[
 \frac{10}{7}-\frac17-\frac{93}{56}\frac3{50}
 =\frac{3321}{2800}>\frac76.
\]
Therefore
\[
 d^2=\frac{2\tau}{1+c}
 \le\frac{1200}{1379}\Delta<\frac78\Delta
 \le\frac{\delta}{64p},
\]
with the zero case already handled. This proves (5), with all radical
comparisons certified by rational squares in the independent checker.

## Trust and reproducibility

The primary checker uses Python 3.11 standard-library exact fractions
and independently implemented sparse Laurent/Gaussian polynomial
arithmetic. It imports no author source, uses no numerical root solver,
and leaves \(m\) symbolic. Its manifest records 70 checks (including
22 rational geometry comparisons), 85 finite direct-matrix profiles,
and six rejected universal Gram-certificate mutations.
The finite profiles do not establish the universal inequalities;
the written reductions and symbolic identities do.

An optional SHA-pinned comparator separately replays the two author
manifests and compares 14 generic entries: three quartic functional
coefficients, six contour-moment coefficients, and five Gram quantities.
Author replay is supplemental reproducibility, not the independence
argument. The scalar characteristic and Laurent method differ from the
author's noncommutative contour-word method. The analytic spectral
subspace, collision, modulus and compactness arguments above are ordinary
proof, not verified by Python or a proof-assistant kernel.

The scalar kurtosis input is classical. The independent uniform audit
and the improved constant (5) add evidence and a refinement to these
campaign claims. Bounded candidate-specific primary searches do not
establish historical priority.
