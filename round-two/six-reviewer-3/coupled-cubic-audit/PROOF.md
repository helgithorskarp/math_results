# Independent coupled cubic proof and refinements

Actual author **six-reviewer-3**, role **independent mathematical reviewer**,
2026-10-03. This is a complete ordinary **unformalized** proof of the new
LEMMA9894 deductions **relative to the explicit actual local inputs below**.
The universal moment lemma is standalone. The written target formulas and our
published REVIEW9845 were exposed; target executable/fixtures were unopened
while this independent proof and core were written. This is not a blind audit.

## 1. Exact scope and local input boundary

Let a complex monic polynomial of degree nine have all nine original zeros in
the closed unit disk. Rotate its marked zero to \(a=1-\eta\), where
\(0<\eta\le e=1/16000\). Count all eight critical points with multiplicity.
Write \(F=\sum_j|a-\zeta_j|^{-1}\), interpreting a zero denominator as infinity.
For the low arm \(F\le8+3\eta\), the input is LEMMA9857, source
`7b1b1f0b36c3a729d190f61b85d587eb4699d187`, Sections 6 and its relevant earlier
identities. We adopt its actual bootstrap, full paired/individual normal
estimates and counted all-original motion, rather than review their proof again.
The following list is the complete numerical/local input used here:

\[
 m=M+iD=\tfrac18\sum\zeta_j,\quad \nu_j=\zeta_j-m,\quad
 u=a-m,\ r=|u|,\quad \xi_j=\nu_j\bar u/r=X_j+iY_j,
\]
\[
 V=\sum|\nu_j|^2<5\eta,\quad |M|<4\eta/5,\quad |D|<\eta/3,
 \quad |m|<13\eta/15,\quad 1-\eta<r<1+\eta.
\]
Set \(T=\sum\nu_j^2\), \(Q+iJ=T\bar u/u=\sum\xi_j^2\),
\(E=\sum X_j^2=(V+Q)/2\), and \(H=\sum|\zeta_j|^2=V+8|m|^2\).
There are nine counted labels \(Z_k\), with \(Z_0=a\) and
\(\omega_k=\exp(2\pi ik/9)\), having full nonlinear estimate
\[
 \left|Z_k-m-u\omega_k-\frac{T}{14u}(\omega_k^{-1}-\omega_k)\right|
 \le\frac{\mu_3}{9a_*^2}+V^2,\qquad
 \mu_3=\sum|\nu_j|^3,\ a_*=15999/16000.                 \tag{I1}
\]
The estimate is strict when \(V>0\), zero at \(V=0\). Define actual
nonnegative paired disk slacks
\(s_k=-[(|Z_k|^2-1)+(|Z_{9-k}|^2-1)]/4\), \(k=3,4\).
Put \(A_k=1-\cos(2\pi k/9)\), \(B_k=1-\cos(4\pi k/9)\),
\(L_k=-A_kM-B_kQ/14\), and \(U=\Re\sum\xi_j^3\). The full inputs are
\[
 -s_3=-\eta+L_3+R_3,\quad |R_3|<29\eta^2,
\]
\[
 -s_4=-\eta+L_4-U/(12r)+\widetilde R_4,
 \quad |\widetilde R_4|<33\eta^2,                       \tag{I2}
\]
\[
 |aD-J/14|\le(2/\sqrt3)(s_3+E_3),\qquad
 E_3\le|m|V/6+V^2<26\eta^2.                           \tag{I3}
\]
These are full actual equations, including all lower coefficients and nonlinear
errors. Formal jets and arbitrary critical tuples do not establish these inputs.
The marked original is simple on this finite-F arm; no other root simplicity,
conjugacy, branch matching, limiting path, feasibility of arbitrary tuples or
initial radius/energy restriction is imposed. The separate reviewer-1 audit
of9857 owns its input proof; this review does not certify that bootstrap.

## 2. Standalone all-n moment inequality, including signed parameters

For every integer \(n\ge2\), any zero-sum complex tuple
\(\xi_j=X_j+iY_j\), and any real \(A,\beta\) with
\(\boxed{|A|\le|\beta|}\), set
\(E=\sum X_j^2\), \(V=\sum(X_j^2+Y_j^2)\),
\(f_j=AX_j^2-\beta Y_j^2\), \(R=\sum X_jf_j\).
Then
\[
 \boxed{R^2\le E\left[\frac{n-2}{n}\beta^2V^2+
              \frac{2\beta(A+\beta)}n E(V-E)\right].}   \tag{1}
\]
Thus9894's eight-point lemma follows; its assumptions \(A\ge0\), \(\beta\ge0\)
and fixed count eight can be removed in this stated way. This uses classical
centering and variance; no historical novelty for sample-moment inequalities
is asserted.

Indeed, \(\sum X_j=0\) gives \(R=\sum X_j(f_j-\bar f)\),
where \(\bar f=\sum f_j/n\). The full Lagrange identity is
\[
 E\sum(f_j-\bar f)^2-R^2
 =\sum_{j<k}[X_j(f_k-\bar f)-X_k(f_j-\bar f)]^2\ge0.     \tag{2}
\]
Let \(S_4=\sum|\xi_j|^4\), \(H_4=\sum X_j^4\),
\(K=\sum X_j^2Y_j^2\). The zero-sum pair identity gives
\[
 (n-1)V^2-nS_4
 =\sum_j|\xi_j|^2\sum_{k<l,\ k,l\ne j}|\xi_k-\xi_l|^2\ge0. \tag{3}
\]
The inner sum is \((n-1)V-n|\xi_j|^2\), since the other \(n-1\)
values sum to \(-\xi_j\). Also
\(nH_4-E^2=\sum_{j<k}(X_j^2-X_k^2)^2\ge0\).
Exactly, \(\sum f_j=(A+\beta)E-\beta V\) and
\(\sum f_j^2=\beta^2S_4-(\beta^2-A^2)H_4-2\beta(A+\beta)K\).
Subtracting the centered variance from the bracket in(1) yields
\[
 \beta^2[(n-1)V^2/n-S_4]+(\beta^2-A^2)(H_4-E^2/n)
                         +2\beta(A+\beta)K\ge0.        \tag{4}
\]
All coefficients are nonnegative under \(|A|\le|\beta|\).
Combining(2)-(4) proves(1). No division by \(E,V,A,\beta\) or any coordinate
occurs. It includes \(E=0,V=0,\beta=0\), repeated coordinates and \(n=2\).
Identity(3) is the explicit all-n version of our credited REVIEW9845 universal
eight-point quartic SOS; its older numerical stability verdict is not used.
The core checks entire free-variable eight-point maps, retaining the mean
correction before imposing zero sum, and the all-n aggregate identity.

## 3. Re-derive the signed normal, dual and entire reciprocal tail

Integrating \(p'(m+w)/9=\prod_j(w-\nu_j)\) gives leading centered terms
\(w^9-(9T/14)w^7-(U_3/2)w^6\), where \(U_3=\sum\nu_j^3\).
The cubic first displacement is
\(U_3(\omega^{-2}-\omega)/(18u^2)\). Multiplying by the conjugate base
and taking the paired half-normal gives coefficient
\((\cos(3\theta)-1)/18\) on \(\Re(U_3\bar u/u^2)\).
It is zero at phase3 and **negative** \(-1/12\) at phase4. Exact quotient
reduction by \(z^6+z^3+1\) checks all nine phases, including phase0.
This reconstructs the coefficient in(I2); the residual bounds remain input.

Let \(c=\cos(\pi/9)\), \(d=2c^2-1\),
\[
 y=1/[3(1+c)],\quad x=2/3-y,\quad h_0=14y,\quad C=8/3+y,
\]
\[
 w_4=1/(c+d),\qquad w_3=(2/3)[7-(1-d)/(c+d)].
\]
The exact identities \(8c^3-6c-1=0\) give
\(w_3A_3+w_4A_4=8\), \(w_3B_3+w_4B_4=7\),
\(8-w_3-w_4=C\), and \(A_kx+B_ky=1\) for \(k=3,4\).
The core checks these after clearing the positive denominators, modulo the
minimal cubic. Its selected root has \(15/16<c<47/50\), by endpoint signs
and \(24c^2-6>0\). Consequently
\(4<w_3<23/5\), \(625/1067<w_4<3/5\).

The all-degree reciprocal coefficient bound follows from the Laplace integral
\[
 P_n(q)=\pi^{-1}\int_0^\pi(q+i\sqrt{1-q^2}\cos\phi)^n\,d\phi,
 \qquad -1\le q\le1.
\]
The integrand has modulus at most one. Its uniformly absolutely convergent
geometric series for \(|z|<1\) integrates to
\((1-2qz+z^2)^{-1/2}\), branch one at zero; substitution
\(t=\tan(\phi/2)\) evaluates the integral near zero and holomorphic continuation
extends it on the disk. Hence the coefficient identification and
\(|P_n(q)|\le1\) hold for every degree. The entire degree-at-least-four tail
for \(|r-\xi|^{-1}\), with \(|\xi|<\tau=1/60<r\), is bounded by
\(|\xi|^4/[(r-\tau)r^4]\). Zero \(\xi\) terms are direct.
Identity(3) at eight yields
\[
 F=8/r+(V+3Q)/(4r^3)+P_3/r^4+\mathcal R_{\ge4},\quad
 P_3=\sum(X_j^3-\tfrac32X_jY_j^2),
\]
\[
 |\mathcal R_{\ge4}|\le(7/8)GV^2,\qquad
 G=1/[(a_*-1/60)a_*^4].                               \tag{5}
\]
The smallness follows from \((7/8)5e<1/3600\), not a new premise.
No finite coefficient sample replaces the all-degree convergence argument.

Convexity of \(8s^{-1/2}\), (I1-I3)'s range, and the same full conversion as9857
now give
\[
 F-8\ge8\eta+8M+(V+3Q)/4+P_3/r^4-36\eta^2-(7/8)GV^2. \tag{6}
\]
Its complete conversion cost is
\(8(4/5)(2-e)/a_*^2+4(169/225)/a_*^3+20<36\).
Insert(I2) in the exact dual **before absolute values**. Since
\(\eta-L_4=s_4-U/(12r)+\widetilde R_4\), this gives
\[
 F-8\ge C\eta+w_3s_3+w_4s_4+E/2-190\eta^2-(7/8)GV^2+R,
\]
\[
 R=P_3/r^4-w_4U/(12r)
   =\sum X_j(AX_j^2-\beta Y_j^2),\quad
 A=r^{-4}-w_4/(12r),\quad \beta=3/(2r^4)-w_4/(4r).       \tag{7}
\]
The whole normal cost is \(36+29w_3+33w_4<190\).
The four rational endpoint bounds in the core prove
\(0<A<1, A<\beta<b=271/200\) on the whole window. From(1),
\[
 R^2\le E[kV^2+qE(V-E)]\le E[kV^2+qEV],
 \qquad k=3b^2/4,\ q=b(1+b)/4.                         \tag{8}
\]

## 4. Both exact certificates and proved rational improvements

Put \(v=5e=1/3200\). For positive \(\delta,\lambda\), write
\(a_0=\delta^2-qv\), \(b_0=\delta\lambda-k/2\). Exactly,
\[
 (\delta E+\lambda V^2)^2-E(kV^2+qEV)
 =a_0(E+(b_0/a_0)V^2)^2
  +(\lambda^2-b_0^2/a_0)V^4+q(v-V)E^2.                 \tag{9}
\]
For9894's physical \((\delta,\lambda)=(1/4,69/50)\) and objective
\((1/2,69/100)\), the core re-derives both stated \(a_0\) and determinants
in full, all strictly positive. It also proves positive determinants for
our slightly smaller choices
\[
 \boxed{(\delta,\lambda)_{\rm physical}=(1/4,1379/1000)},
 \qquad \boxed{(\delta,\lambda)_{\rm objective}=(1/2,551/800)}. \tag{10}
\]
Their exact fractions and full cost margins are in `SUMMARY.json`; no rounded
floating values are certificate inputs. The \(V^4\) term is strictly positive
when \(V>0\); both sides to be unsquared are nonnegative. Thus
\(|R|<\delta E+\lambda V^2\) for \(V>0\). At \(V=0\), \(E=R=0\)
and(7)'s strictly positive eta/error margins provide the final strictness.
The case \(E=0<V\) is included without division.

Using \(V<5\eta\),9894's pairs give the full physical cost
\(190+25[(7/8)G+69/50]<247\) and separate objective cost
\(190+25[(7/8)G+69/100]<230\). This confirms its two conclusions.
Using(10) instead proves
\[
 \boxed{F>8+C\eta-(459/2)\eta^2>8+(141/50)\eta},         \tag{11}
\]
\[
 \boxed{F-8>C\eta+\Psi-(987/4)\eta^2},\qquad
 \Psi=w_3s_3+w_4s_4+E/4,\quad F\le8+3\eta.             \tag{12}
\]
The cost margins are checked exactly against \(459/2\) and \(987/4\).
The objective route spends all \(E/2\); the physical route keeps \(E/4\).
The former error is never used in the latter defect.
For \(F>8+3\eta\), including infinity, (11) is immediate from \(C<3\).
The second inequality uses \(C>826/291\) and
\(826/291-(459/2)e>141/50\). There is no extension of the eta window,
optimality claim, interior endpoint resolution or optimizer classification.

## 5. Full fresh pointwise stability for both defect constants

Retain **both** cuts \(F\le8+3\eta\) and
\(F\le8+C\eta+\epsilon\eta\), for arbitrary \(\epsilon\ge0\).
Use either9894's \(D_*=247\), or our proved \(D_*=987/4\), and set
\(\Delta=\epsilon\eta+D_*\eta^2>0\).
Both physical inequalities give \(\Psi<\Delta\), hence
\(s_3<\Delta/4,s_4<2\Delta,E<4\Delta\).
For both constants, \(D_*>(31/2)^2\).
Pointwise
\(9X^2(X^2+Y^2)^2-(X^3-3XY^2)^2=8X^6+24X^4Y^2\ge0\);
Cauchy implies \(|U|\le3V\sqrt E\). Thus(I2) yields
\[
 |L_3-\eta|<(1/4+29/D_*)\Delta<3\Delta/8,
\]
\[
 |R_4|<(33/D_*+5/(31a_*))\Delta<\Delta/2,
 \qquad |L_4-\eta|<5\Delta/2.                          \tag{13}
\]
The old \(\sqrt{272}>16\) is not available at247 or987/4.

The Cramer determinant is \(-3(c+d)/2\). Its magnitude is
strictly greater than \(651/256\); \(B_4<31/128,A_4<97/50\).
The first two are **equalities at the rational endpoint** \(c=15/16\),
and strictness follows from \(c>15/16\) and monotonicity.
Consequently
\[
 |M+x\eta|<[(62/651)(3/8)+(128/217)(5/2)]\Delta<8\Delta/5,
\]
\[
 |-Q/14-y\eta|<[(24832/32550)(3/8)+(128/217)(5/2)]\Delta<9\Delta/5.
\]
These imply
\[
 |Q+h_0\eta|<26\Delta,\quad |V-h_0\eta|<34\Delta,
 \quad |H-h_0\eta|<35\Delta.                           \tag{14}
\]
Here \(V=2E-Q\), \(H=V+8|m|^2\), and
\(34+8(169/225)/D_*<35\). Also \(J^2\le4EV<80\eta\Delta\).
From(I3), \(2/\sqrt3<7/6\), \(\sqrt{80}<9\) and the exact endpoint margins,
\[
 |D|<\sqrt{\eta\Delta}+\Delta+31\eta^2.                \tag{15}
\]
Since \(\Re u>0\), \(|u/r-1|^2\le2D^2/r^2\). Apply the three-term
squared-norm bound to \(\Re\zeta_j=M+X_j+\Re[\xi_j(u/r-1)]\), retaining
the unconditional local range \(|M|<4\eta/5,|D|<\eta/3\). It gives
\[
 \sum(\Re\zeta_j)^2<12\Delta+(384/25)\eta^2+4\eta^3/a_*^2<13\Delta. \tag{16}
\]

For every counted original, \(T/u=(Q+iJ)/\bar u\),
\(|u-1|<28\eta/15\), \(y<16/93\) and (14)-(15) give
\[
 |T/(14u)+y\eta|<[26\Delta+9\sqrt{\eta\Delta}]/(14a_*)
                                +28y\eta^2/(15a_*),
\]
\[
 |m+x\eta|<13\Delta/5+\sqrt{\eta\Delta}+31\eta^2.
\]
Also \(\mu_3\le\sqrt{7V/8}V<(21/2)\eta^{3/2}\), by zero sum and \(V<5\eta\).
Compare(I1) with \(\omega_k+\eta(-\omega_k/3-x-y\omega_k^{-1})\),
using \(x+y=2/3\) and both phase differences at most two. The entire error is
\[
 <(26/5+26/(7a_*))\Delta+(2+9/(7a_*))\sqrt{\eta\Delta}
                       +88\eta^2+[7/(6a_*^2)]\eta^{3/2}.
\]
The88 follows from \(62+25+896/(1395a_*)<88\).
For both \(D_*\), the two exact final margins are
\[
 26/5+26/(7a_*)+88/D_*<19/2,\qquad
 2+9/(7a_*)+7/(93a_*^2)<7/2.
\]
Use \(\eta^2\le\Delta/D_*\) and
\(\eta^{3/2}<(2/31)\sqrt{\eta\Delta}\). Therefore, for all nine labels,
\[
 \boxed{|Z_k-[\omega_k+\eta(-\omega_k/3-x-y\omega_k^{-1})]|
      <(19/2)\Delta+(7/2)\sqrt{\eta\Delta}.}             \tag{17}
\]
This includes \(V=0\), arbitrary epsilon and all critical multiplicities.
We never infer the imaginary cubic from the real energy. All inequalities
are ordinary analytic deductions, corroborated by full exact identities
and strict rational margins; neither finite controls nor source replay
prove the adopted actual-domain input.
