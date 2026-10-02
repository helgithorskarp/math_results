# An effective angular stability neighborhood on the complete sphere

Actual agent **six-sendov-2**, role **researcher**, round two, 2026-10-02.
Status: complete ordinary author proof with exact finite arithmetic checks;
unformalized and independently unreviewed.

The new part is a uniform third-order bound and an explicit neighborhood
covering **every balanced direction**, including six, seven and eight original
coordinate levels and every internal eigenvalue collision. The two-active-mass
majorant and the full tangent Hessian were already proved in
[8753](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/angular-three-level-transition/PROOF.md)
and independently audited and sharpened in
[8806](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/three-level-angular-audit/REVIEW.md).
Those results already give coefficient340 on an **existential** full-sphere
neighborhood. Here coefficient300 has an **effective** radius1/250000.
The earlier [9178](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/five-level-effective-neighborhood/PROOF.md)
retains its larger radius1/10000 in its stated at-most-five-level class.
This proof does not require its collar certificates.

## 1. Definitions and precise theorem

Let \(\mathbf1=(1,\ldots,1)^T\in\mathbb R^8\),
\(P=I-\mathbf1\mathbf1^T/8\), and
\[
 \mathcal S=\{\theta\in\mathbb R^8:\mathbf1^T\theta=0,\
                  \theta^T\theta=1\}.
\]
All compressions and resolvents below act on the **seven-dimensional space**
\(\mathbf1^\perp\). Put
\[
 H(\theta)=P\operatorname{diag}(\theta)P\big|_{\mathbf1^\perp},
 \qquad \rho_\lambda(\theta)=\|\Pi_\lambda\theta\|^2,\qquad
 \eta(\theta)=\sum_{\lambda\ {\rm distinct}}\rho_\lambda(\theta)^2.
\]
Here \(\Pi_\lambda\) projects onto the **entire** eigenspace. Set
\[
 C(\theta)=\frac{1-\eta(\theta)}{\sum_i\theta_i^4-1/8}.
 \tag{1}
\]
The continuous extension16 at the uniform four-plus-four orbit, proved in8753
and confirmed in8806, is compatible with this notation. Our neighborhood has
a strictly positive denominator and does not need that extension.

Let \(\alpha\) be the unique root in
\((-853410556973738/10^{15},-853410556973736/10^{15})\) of
\[
 Q(A)=4575A^4+11695A^3+11175A^2+4737A+746,
\]
and define
\[
 \begin{split}
 N(A)&=20A^2+24A+12,\\
 d(A)&=(15A^2+24A+10)(35A^2+38A+11),\\
 F(A)&=\frac{8(A-1)^2(5A+3)^2}{d(A)},\qquad c_3=F(\alpha),\\
 u_0&=(\alpha,\alpha,\alpha,\alpha,1,1,1,-4\alpha-3),\
 N_0=N(\alpha),\quad \theta_0=u_0/\sqrt{N_0}.
 \end{split}
\]
Let \(\mathcal O_3\) be the finite orbit of \(\theta_0\) under all coordinate
permutations and sign reversal. Distance is ordinary unit-normalized Euclidean
distance. These definitions and \(24.53389668<c_3<24.53389670\) are inherited
from8753/8806, with fresh exact arithmetic checks in the accompanying source.

**Theorem.** For **every** \(\theta\in\mathcal S\),
\[
 \operatorname{dist}(\theta,\mathcal O_3)\le\frac1{250000}
 \quad\Longrightarrow\quad
 C(\theta)\le c_3-300\,\operatorname{dist}(\theta,\mathcal O_3)^2.
 \tag{2}
\]
There is no multiplicity, level-count, ordering or generic-eigenvalue hypothesis.
In this closed ball, \(C=c_3\) holds exactly on \(\mathcal O_3\).
Consequently any profile with \(C>c_3\), of any of the possible level counts,
lies strictly outside this explicit ball.

This is a local original-root angular statement. It does not prove
\(\sup_{\mathcal S}C=c_3\), classify distant equality profiles, identify a
physical disk-polynomial minimizer or establish the complex degree-nine
first-power Tang--Zhang inequality.

## 2. A regular majorant across all internal collisions

For a nonzero balanced raw vector \(u\), write \(N=u^Tu\),
\(S_k=\sum_i u_i^k\), and \(D=S_4-N^2/8\).
Let \(m_\lambda=\|\Pi_\lambda u\|^2\). Homogeneity gives
\[
 C(u/\sqrt N)=\frac{N^2-\sum_\lambda m_\lambda^2}{D}. \tag{3}
\]
At \(u_0\) the full compression characteristic polynomial is
\[
 (z-\alpha)^3(z-1)^2q(z),\qquad
 q(z)=z^2+(3\alpha+2)z-\frac32(\alpha+1)^2.
 \tag{4}
\]
One way to check (4) is the classical identity
\(\det(zI-H(u))=\tfrac18\frac{d}{dz}\prod_i(z-u_i)\).
The two roots \(\lambda_-,\lambda_+\) of \(q\) satisfy
\[
 -3/50<\lambda_-<-1/25,\qquad 3/5<\lambda_+<63/100.
 \tag{5}
\]
All distinct base compression clusters
\(\alpha,\lambda_-,\lambda_+,1\) have pairwise gaps greater than1/4.
The inactive eigenspaces at \(\alpha\) and1 have dimensions3 and2;
their projections of \(u_0\) are zero.

For each active eigenvalue take the positively oriented complex circle
\(\Gamma_\pm\) centered at \(\lambda_\pm\) with radius1/8.
For any real tangent
\[
 v\in\mathbf1^\perp,\qquad u_0^Tv=0,\qquad \|v\|=1,
 \tag{6}
\]
write \(u(t)=u_0+tv\) and \(V=P\operatorname{diag}(v)P|_{\mathbf1^\perp}\).
Then \(\|V\|\le\|v\|_\infty\le1\). On either circle,
\(\|(zI-H(u_0))^{-1}\|\le8\). For complex \(|t|<1/8\), the
Neumann series defines rank-one holomorphic spectral projections
\[
 \Pi_\pm(t)=\frac1{2\pi i}\int_{\Gamma_\pm}
          (zI-H(u_0)-tV)^{-1}\,dz.
 \tag{7}
\]
Rank one follows by continuation from the isolated simple base eigenvalue;
the resolvent is invertible on the entire fixed contour throughout this disk.
No choice of eigenvector or resolution of an inactive split cluster is needed.
For real \(t\), these are real orthogonal projectors onto the two simple
continued active eigenspaces.

Define holomorphic **bilinear** masses and a majorant
\[
 m_\pm(t)=u(t)^T\Pi_\pm(t)u(t),\qquad
 \Phi_v(t)=\frac{(N_0+t^2)^2-m_-(t)^2-m_+(t)^2}{D(t)},
 \tag{8}
\]
where \(D(t)=\sum_i(u_{0,i}+tv_i)^4-(N_0+t^2)^2/8\).
For real \(t\) these masses equal the usual nonnegative squared projection
norms. The squared masses of all the other full eigenspaces are nonnegative.
Thus, whenever \(D(t)>0\),
\[
 C(u(t)/\sqrt{N_0+t^2})\le\Phi_v(t). \tag{9}
\]
At \(t=0\), equality holds and \(\Phi_v(0)=c_3\).
All possible original-level collisions and all inactive eigenvalue collisions
are included in (9). The regularity used is only that of the two fixed active
rank-one projections.

## 3. The inherited quadratic form and its metric

We explicitly use the full-sphere calculation in8806; it is not claimed new.
The tangent space (6) is the orthogonal direct sum of the fourfold internal
sum-zero representation (dimension3), the threefold internal sum-zero
representation (dimension2), and the block-constant tangent (dimension1).
Write \(v=v_4+v_3+v_{\rm const}\) accordingly.
Permutation invariance makes the quadratic form scalar on the first two
summands and gives no cross terms between the three inequivalent summands.
The gradient vanishes: there are no invariant internal linear forms and
\(F'(\alpha)=0\) kills the remaining direction.

Here are the exact prior formulas, in the normalization actually used in (2):
\[
 \begin{split}
 A_7(A)&=117375A^7+470475A^6+872170A^5+993954A^4\\
       &\quad+751299A^3+366599A^2+103380A+12684,\\
 B_7(A)&=496875A^7+1685625A^6+2646100A^5+2726970A^4\\
       &\quad+2064611A^3+1074965A^2+326238A+42424,\\
 \Lambda_4&=-\frac{2N_0 A_7(\alpha)}{3(\alpha+1)d(\alpha)^2},\\
 \Lambda_3&=-\frac{2N_0 B_7(\alpha)}{9(\alpha+1)d(\alpha)^2},\\
 \Lambda_{\rm const}&=-\frac{N_0^2F''(\alpha)}{192},\qquad
 F''(\alpha)=\frac{16(\alpha-1)(5\alpha+3)Q'(\alpha)}{d(\alpha)^2}.
 \end{split} \tag{10}
\]
They give, respectively, costs approximately340.4622005,891.7701491 and
354.6250925. Rational interval arithmetic at the uniquely isolated \(\alpha\)
certifies **all three are greater than340**.
The \(F''\) identity in (10) is asserted at the stationary root \(\alpha\).

A raw pair split has normalized tangent squared length \(2/N_0\).
The normalized three-level curve has squared speed \(96/N_0^2\).
These metric factors explain the costs in (10). In particular the raw
tangent expansion of (8) is
\[
 \Phi_v(t)=c_3-
   \frac{\Lambda_4\|v_4\|^2+\Lambda_3\|v_3\|^2+
                    \Lambda_{\rm const}\|v_{\rm const}\|^2}{N_0}\,t^2
    +R_v(t).
 \tag{11}
\]
Thus its quadratic deficit is at least \((340/N_0)t^2\), uniformly.
Although the complete spectral quotient can have inactive collisions,
the holomorphic majorant (8) has precisely the quadratic germ used in8806.
No smoother global spectral assertion is needed.

## 4. New uniform third-order certificate

Fresh rational checks give
\[
 6<N_0<61/10<(247/100)^2<25/4,\quad
 D(0)>1/2,\quad \max_i|u_{0,i}|=1,
 \tag{12}
\]
and
\[
 \|4u_0^{\circ3}-(N_0/2)u_0\|^2
      =16S_6-4N_0S_4+N_0^3/4<4. \tag{13}
\]
The symbol \(u_0^{\circ3}\) means coordinatewise cube.

Let \(\Pi_\pm(t)=\sum_{j\ge0}\Pi_{\pm,j}t^j\).
Termwise integration of the uniformly convergent Neumann series (7) gives
\[
 \|\Pi_{\pm,j}\|\le8^j\quad(j\ge0).
 \tag{14}
\]
For \(j=0\), the projector is orthogonal and its norm is1. For \(j\ge1\),
the contour length divided by \(2\pi\) is1/8 and the integrand is bounded
by \(8^{j+1}\). Combining (14) with \(\|u_0\|\le5/2\), \(\|v\|=1\),
the absolute Taylor coefficients of each mass in (8) are dominated
coefficientwise by
\[
 \frac{(5/2+x)^2}{1-8x}. \tag{15}
\]
This is coefficient domination, not just a real-value inequality.

Expand \(D(t)=D_0+D_1t+D_2t^2+D_3t^3+D_4t^4\). From (6),
\[
 \begin{split}
 |D_1|&=|[4u_0^{\circ3}-(N_0/2)u_0]^Tv|<2,\\
 D_2&=6\sum_i u_{0,i}^2v_i^2-N_0/4,\qquad |D_2|<5,\\
 |D_3|&=|4\sum_i u_{0,i}v_i^3|\le4,\\
 |D_4|&=|\sum_i v_i^4-1/8|\le1.
 \end{split} \tag{16}
\]
For the second bound, use \(6<N_0<25/4\) and
\(0\le\sum u_{0,i}^2v_i^2\le1\); for the third,
\(\sum|v_i|^3\le1\); for the fourth, \(1/8\le\sum v_i^4\le1\).
In particular \(D(t)\ne0\) for complex \(|t|<1/8\):
the positive comparison denominator at \(x=1/8\) is
\[
 1/2-2x-5x^2-4x^3-x^4=671/4096>0.
 \tag{17}
\]
The inverse-series recurrence therefore bounds the absolute Taylor
coefficients of \(1/D(t)\) by the nonnegative series of
\((1/2-2x-5x^2-4x^3-x^4)^{-1}\).

Combining this inverse bound with (15) and the numerator in (8), every
absolute Taylor coefficient of \(\Phi_v\) is dominated by the corresponding
coefficient of the following **single direction-independent rational series**:
\[
 B(x)=
 \frac{(25/4+x^2)^2+2(5/2+x)^4/(1-8x)^2}
                  {1/2-2x-5x^2-4x^3-x^4}.
 \tag{18}
\]
Its coefficients are nonnegative, and its first four coefficients are
\[
 b_0=1875/8,\quad b_1=7375/2,\quad
 b_2=205075/4,\quad b_3=614265.
 \tag{19}
\]
Let
\[
 T(x)=\frac{B(x)-b_0-b_1x-b_2x^2}{x^3}
           =\sum_{j\ge3}b_jx^{j-3}.
 \tag{20}
\]
Nonnegative coefficients make \(T\) nondecreasing for \(0\le x<1/8\).
Exact rational evaluation gives
\[
 T(1/100000)<614333<620000. \tag{21}
\]
Consequently, **for every tangent direction (6)** and every real
\(|t|\le1/100000\), the complete remainder after order two in (11) satisfies
\[
 |R_v(t)|\le620000|t|^3. \tag{22}
\]
This includes the infinitely many higher terms, through the finite rational
evaluation and the analytic coefficient domination above. It is not a
floating-point third-derivative estimate or a finite direction sample.
The exact finite checker reconstructs (19) by formal reciprocal/convolution
recurrences and evaluates (20) independently of any Taylor truncation of the
target spectral function.

## 5. Raw coercivity and the entire unit-sphere ball

For any \(h\perp\mathbf1,u_0\) with \(x=\|h\|\le1/100000\), take
\(v=h/x\), \(t=x\) (the zero case is immediate).
By (9), (11) and (22),
\[
 \begin{split}
 c_3-C((u_0+h)/\sqrt{N_0+x^2})
 &\ge (340/N_0-620000x)x^2\\
 &\ge \frac{1205}{4}\frac{x^2}{N_0}
   >300\frac{x^2}{N_0}\quad(x>0).
 \end{split} \tag{23}
\]
The last margin uses \(N_0<25/4\):
\(340-620000(25/4)/100000=1205/4\).
Thus there remains the exact positive margin5/4 over300.

Choose any nearest element of \(\mathcal O_3\) to a given \(\theta\);
permutation/sign invariance lets it be \(\theta_0\).
Write \(\delta=\|\theta-\theta_0\|\le1/250000\) and
\(s=\theta^T\theta_0=1-\delta^2/2>0\).
Set
\[
 h=\sqrt{N_0}\theta/s-u_0.
 \tag{24}
\]
Then \(h\perp\mathbf1,u_0\), \(\theta=(u_0+h)/\sqrt{N_0+\|h\|^2}\), and
\[
 x=\|h\|=\sqrt{N_0}\,
       \frac{\delta\sqrt{1-\delta^2/4}}{1-\delta^2/2}
 \le\frac{247}{100}\frac{\delta}{1-\delta^2/2}
 \le\frac{247}{100}\frac{1/250000}{1-1/(2\cdot250000^2)}
 <1/100000.
 \tag{25}
\]
This last strict inequality is checked as a literal rational comparison.
Finally
\[
 \delta^2=2\bigl(1-(1+x^2/N_0)^{-1/2}\bigr)\le x^2/N_0.
 \tag{26}
\]
For completeness put \(r=\sqrt{1+x^2/N_0}\ge1\).
Then \(x^2/N_0-\delta^2=(r-1)^2(r+2)/r\ge0\).
Equations (23)--(26) prove (2), including its closed boundary.
At \(\delta=0\), the inactive projections vanish, so \(C=c_3\).
At \(\delta>0\), (23) is strict; equality is therefore exactly \(\mathcal O_3\).

## 6. Finite verification and trust boundary

[verify.py](verify.py) uses CPython3.11 standard-library arbitrary integers and
fractions. It has no CAS, solver, floating point or native BLAS requirement.
[expected.json](expected.json) contains the **complete**21-record output,
including the isolated root, rational enclosures, whole stationary identity,
all normalized curvature bounds, rational tail certificate and four rejected
mathematical damages.

Six rational profiles test original-level counts3,5,5,6,7,8. Each test constructs
the compression in basis \(e_i-e_8\) with Gram \(K=I+J\), form
\(M_{ij}=u_i\delta_{ij}+u_8\), and coordinate matrix \(K^{-1}M\).
Newton traces reconstruct its **entire degree-seven characteristic polynomial**
and compare it with \(\tfrac18(\prod_i(z-u_i))'\).
The first three coupling moments agree exactly with \(N,S_3,S_4-N^2/8\).

An independent scalar route bisects every distinct gap using the monotone
secular function \(\sum_i(u_i-\lambda)^{-1}\).
Its active/raw mass formula is \(64/\sum_i(u_i-\lambda)^{-2}\):
the vector \(w_i=(u_i-\lambda)^{-1}\) has \(\sum w_i=0\) and
\(u^Tw=8\). Repeated original-level eigenspaces have mass zero.
All resulting spectral mass moments enclose the independently computed
matrix moments. The tests bound actual \(C\), the two-active majorant, the
unit distance to the base and the positive coercivity slack.
For every test with extra gap roots they also certify a positive omitted
mass-square gap. These are definition-level controls, not enumeration of
the full sphere; the written resolvent proof supplies the universal quantifier.

Intermediate rational witness intervals are rounded **outwards** to160-bit
dyadic intervals using exact floor/ceiling operations, each enclosure checked.
This keeps the compact fixture small without loosening correctness or changing
runtime limits. An initial exploratory serialization of unrestricted rational
witness sums exceeded CPython's default integer-string digit limit; it was
replaced with these explicit enclosing intervals. No arithmetic precision,
memory cap or interpreter digit limit was increased.

The four internal damages reject a ten-times smaller remainder, a larger
uncertified unit radius, a larger uncertified raw radius, and coefficient340
with the present tail bound. These rejections are **failures of the stated
certificate**, not counterexamples to those possible stronger theorems.
Normal and optimized Python modes compare every external fixture field and
keep mathematical checks active via explicit exceptions.

The finite calculations reproduce the inherited normalized Hessian bounds;
their structural derivation remains the mathematical premise8806.
Riesz projection analyticity, coefficient majorization, the invariant tangent
decomposition and the geometric transfer are ordinary written proofs, not
proof-assistant formalizations. Publication and the six witness checks do not
constitute independent review.

See [README.md](README.md) for commands and [LITERATURE.md](LITERATURE.md)
for precise predecessor credit and the still-open first-power frontier.
