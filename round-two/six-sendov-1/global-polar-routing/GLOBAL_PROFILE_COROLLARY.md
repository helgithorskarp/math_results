# Global explicit sharp-slope remainder and pointwise stability

Actual author **six-sendov-1**, role **researcher**, 2026-10-02.
Complete ordinary analytic composition, **unformalized and independently
unreviewed**. This appendix was written after the core source publication
bdedbe4d093bc614953a2daed2bcba04217f681c and the fresh discovery of the
committed inputs9671 and9669. The quantitative local estimates below retain
their authors' credit. No verdict on those inputs reviews our global carrier.

Let a complex monic polynomial of degree nine have all its original zeros
in the closed unit disk. Rotate a marked original zero to
\(a=1-\eta\), where \(0<\eta\le2^{-37}\). Count the eight critical
points \(\zeta_j\) with algebraic multiplicity and put
\[
F=\sum_j|a-\zeta_j|^{-1},\qquad H=\sum_j|\zeta_j|^2.
\]
A zero denominator means \(F=+\infty\). There is no initial critical
radius, energy, coefficient cap, conjugation, separation, smooth family,
selected profile, optimizer or attainment hypothesis.

With the **prior** sharp asymptotic coefficient
\[
c=\cos(\pi/9),\quad y=\frac1{3(1+c)},\quad
x=\frac23-y,\quad h_0=14y,\quad C=\frac83+y,
\]
the global estimate is
\[
\boxed{F>8+C\eta-16\eta^{3/2}>8+\frac{14}{5}\eta.}       \tag{A}
\]
The effective local remainder and all subsequent stability estimates are
**CREDITED9671**, researcher **six-sendov-3**, artifact
bafkreidttzvgg7zziwmcraph7wbu275afeczah6ok5pewhjk7lehm77hma,
final source48241d95ef16ffb51e183c89101762a321152dc0:
[complete ordinary proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/effective-profile-stability/PROOF.md).
The new ingredient here is its entry for every actual polynomial in the
specified annulus, supplied by [our global carrier](PROOF.md).
The sharp C and limiting profiles are prior8530/8608;9671 supplies the
finite remainder, rather than a new leading coefficient.

## Complete entry and case argument

On \(F\le8+3\eta\), the global carrier, proved for all
\(0<\eta\le2^{-16}\), gives
\[
H<2^{28}\eta\le2^{28}2^{-37}=\frac1{512}.
\]
Only after this global conclusion do we apply the **core fixed-energy**
theorem9671. Its core uses9620, independently confirmed by9667 and9669;
its optional max-critical-radius enlargement using9629 is not needed here.
There is consequently no dependency on9671 in the proof of the carrier,
and no circular use of an annulus or concentration theorem.
Its conclusion is the first inequality in(A).

If \(F>8+3\eta\), including infinity, the same inequality follows
because \(C<3\). Indeed \(0<c<1\) implies
\(1/6<y<1/3\), hence \(17/6<C<3\).
Finally \(\eta\le2^{-37}<2^{-36}\) gives
\(16\sqrt\eta<1/16384\), and the exact rational margin is
\[
\frac{17}{6}-\frac{14}{5}-\frac1{16384}
=\frac1{30}-\frac1{16384}=\frac{8177}{245760}>0.
\]
This proves both strict inequalities in(A), including the endpoint, with
every high/low/infinite case covered. Rotation preserves all distances,
so(A) holds at every marked original of modulus \(1-\eta\).

## Transported actual slack and moment stability

For these conclusions retain the additional **explicit low-sublevel**
hypothesis \(F\le8+3\eta\). In the rotated coordinates set
\[
m=\frac18\sum_j\zeta_j=M+iD,\quad \nu_j=\zeta_j-m,\quad
V_{\rm crit}=\sum_j|\nu_j|^2,\quad T=\sum_j\nu_j^2,
\quad u=a-m,\quad Q_{\rm rot}+iJ=T\bar u/u.
\]
Here \(Q_{\rm rot}\) is a rotated second centered critical moment,
not the reciprocal mean Q or radial reciprocal variance in our core proof.
The imported counted-circle argument provides all nine actual original
labels \(Z_k\) near \(m+u\omega_k\),
\(\omega_k=e^{2\pi ik/9}\), with \(Z_0=a\).
Simplicity of the originals is a conclusion on this sublevel;
critical multiplicities are still unrestricted. Opposite labels need
not be conjugates.

Write \(d=2c^2-1\),
\[
s_k=-\frac12\left(\frac{|Z_k|^2-1}{2}
                       +\frac{|Z_{9-k}|^2-1}{2}\right)\ge0,
\quad k=3,4,
\]
\[
w_4=\frac1{c+d}>0,\quad
w_3=\frac23\left(7-\frac{1-d}{c+d}\right)>0,\qquad
\Phi=w_3s_3+w_4s_4+\frac{V_{\rm crit}+Q_{\rm rot}}4\ge0.
\]
After the same entry,9671 gives, pointwise for every actual polynomial,
\[
F-8>C\eta+\Phi-16\eta^{3/2}.                           \tag{B}
\]
For **every** \(\epsilon\ge0\), if the polynomial also satisfies
\(F\le8+C\eta+\epsilon\eta\), put
\(E=\epsilon\eta+16\eta^{3/2}>0\). The credited estimates become
\[
\begin{gathered}
0\le\Phi<E,\qquad |M+x\eta|<\frac43E,\qquad
|Q_{\rm rot}+h_0\eta|<21E,\\
|V_{\rm crit}-h_0\eta|<25E,\qquad |H-h_0\eta|<26E,\\
\sum_j(\Re\zeta_j)^2<7E,\qquad
|D|<\sqrt{\eta E}+E+44\eta^2.                         \tag{C}
\end{gathered}
\]
Every one of the nine actual original labels satisfies
\[
\left|Z_k-\left[\omega_k+
 \eta\left(-\omega_k/3-x-y\omega_k^{-1}\right)\right]\right|
 <8E+3\sqrt{\eta E}.                                 \tag{D}
\]
Equations(B)--(D) are unchanged local inequalities from9671 on the domain
proved globally above. They do not assert a selected critical template,
unique optimizer or smooth motion through a collision. For arbitrary
large \(\epsilon\), the near-slope upper bound alone does not imply
\(F\le8+3\eta\); both hypotheses have deliberately been retained.

## Complementary credited upper and lower bounds

On the same global low sublevel, the independent9620 review
**9669**, reviewer **six-reviewer-1**, artifact
bafkreia2uvl7342llp2ongdcri54awvhoozglnijcptont3dzqprzcgaqq,
source785f5208b1bf59c1abe5a9f91e2a9cebad0a7368, proves the separately
credited refinements
\[
-3\eta/4<M<0,\quad |D|<5\eta/18,\quad |m|<4\eta/5,
\quad V_{\rm crit}<28\eta/5,\quad H<45\eta/8.
\]
For the rotated monic coefficients it also gives
\[
|c_8|<36\eta/5,\quad |c_7|<29\eta/8,
\quad \sum_{k=1}^6|c_k|<\eta/5.
\]
See the [complete review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/critical-energy-audit/REVIEW.md).
The separately credited **9667** proof gives
\(V_{\rm crit}>135\eta/413\), as already transported in our core
source's Section7. The quantities in these bounds are centered critical
moments, rather than radial reciprocal moments.

The complete ordinary input proofs and signed original bodies were read
and aligned with their whole pinned/main public source bytes. No9671 or
9669 executable, fixture, source seal or review verdict was imported or
replayed.9671 remains independently unreviewed at this intake. Reviews
9667/9669 confirm9620 in its original numerical domain; they do not
review the new global carrier or this composition.

The core checker and its recorded normal/optimized/source-damage validation
continue to cover precisely the original global-carrier finite algebra.
This appendix is an ordinary written two-case deduction with the exact
scalar margin displayed above. It is not covered by a formal kernel or
claimed as an independently checked proof.
Global entry for \(2^{-37}<\eta\le2^{-16}\), optimal annulus constants,
and the unrestricted first-power endpoint remain open here.
