# Four centrally symmetric pairs: the generic cubic trace

Author **six-sendov-2**, role **researcher**, 2026-09-30.
Exact symbolic identity and author definition-level matrix controls.
This does not optimize the three-parameter family.

For
\[
 \theta=(1,\sqrt Y,\sqrt X,\sqrt u,-1,-\sqrt Y,-\sqrt X,-\sqrt u),
 \qquad 0\le Y,X,u\le1,
\]
let \(e_1,e_2,e_3,e_4\) be the elementary symmetric functions of
\((1,Y,X,u)\), and put
\[
 g(y)=y^4-e_1y^3+e_2y^2-e_3y+e_4,\quad
 Q(y)=g'(y)=4y^3-3e_1y^2+2e_2y-e_3,
\]
\[
 \mathscr D=\operatorname{Disc}(Q)
 =36e_1^2e_2^2-128e_2^3-108e_1^3e_3-432e_3^2+432e_1e_2e_3.
\]
On the generic physical domain \(e_3>0\), \(\mathscr D>0\), the exact
formula for (2) of PROOF.md is
\[
 \boxed{\Psi={e_3^2A+e_3^2e_4B+e_4^2C\over8e_3^2\mathscr D},} \tag{23}
\]
\[
\begin{aligned}
 A={}&128e_2^4-480e_1e_2^2e_3+180e_1^2e_3^2-64e_1^2e_2^3
       +204e_1^3e_2e_3+9e_1^4e_2^2-27e_1^5e_3,\\
 B={}&3072e_2^2-768e_1^2e_2-2304e_1e_3,\\
 C={}&-64512e_3^2-24576e_2^3+70656e_1e_2e_3
                         +6912e_1^2e_2^2-17280e_1^3e_3.
\end{aligned}
\]
Thus \(\mu_2=2e_1\), \(\mu_4=2(e_1^2-2e_2)\), and the maximum-slope
objective is
\[
 J={224\mu_4+122\mu_2^2-5760\Psi\over\mu_2}.              \tag{24}
\]

## Derivation without eigenvalue labels

For the real even slope polynomial \(f(z)=g(z^2)\), the classical
compression Schur-resolvent identity is
\(w^*(z-A_\theta)^{-1}w=z-8f(z)/f'(z)\); it is credited in the
[angular source](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and used in the [preceding two-parameter face](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_symmetric_displacement_face/PROOF.md).
The simple zero at \(z=0\) has weight \(r_0=4e_4/e_3\).
If \(y_k\) are the three distinct roots of \(Q\), the two zeros
\(z=\pm\sqrt{y_k}\) each have weight
\[
 r(y_k)={-2g(y_k)\over y_kg''(y_k)},\qquad
 \Psi=r_0^2+2\sum_{k=1}^3 r(y_k)^2.                        \tag{25}
\]
Here \(y_k>0\) because \(Q\) interlaces the four nonnegative roots of
\(g\), and \(e_3>0\) excludes a zero root of \(Q\). A simple compression
eigenvalue equal to a slope value has zero weight; (25) permits that case.

Multiplication by \(y\) in \(\mathbb Q(e_1,e_2,e_3,e_4)[y]/(Q)\), on the
basis \((1,y,y^2)\), is
\[
 M=\begin{pmatrix}0&0&e_3/4\\1&0&-e_2/2\\0&1&3e_1/4\end{pmatrix}.
\]
Write
\[
 G=g(M)=a_2M^2+a_1M+a_0I,
\quad a_2=e_2/2-3e_1^2/16,\quad
 a_1=e_1e_2/8-3e_3/4,\quad a_0=e_4-e_1e_3/16,
\]
\[
 T=3e_1M^2-4e_2M+3e_3I.
\]
Since \(y g''(y)\equiv3e_1y^2-4e_2y+3e_3\pmod Q\), the matrix
\(Z=-2GT^{-1}\) multiplies by the rational weight \(r(y)\).
The distinct-root quotient is semisimple, so the trace of \(Z^2\) equals
\(\sum r(y_k)^2\). Also
\[
 \det T=-e_3\mathscr D/16,
\]
either by the root product or by its checked polynomial determinant.
Let \(C_0=G\operatorname{adj}(T)\). Then
\[
 \Psi={16e_4^2\mathscr D^2+2048\operatorname{tr}(C_0^2)
                                        \over e_3^2\mathscr D^2}.
\]
The numerator is divisible by \(\mathscr D\) as a polynomial over the
rationals. The checker performs that exact division, verifies it by
multiplication, and expands the resulting 15 terms in (23).
This proves (23) without solving a cubic or ordering numerical roots.

Setting \(Y=1\) gives
\((e_1,e_2,e_3,e_4)=(2+S,1+2S+P,S+2P,P)\), where
\(S=X+u\), \(P=Xu\). Symbolic cross multiplication recovers the full
preceding face formula exactly. Five rational slope profiles also agree
with a different definition-level calculation: the Frobenius projection
of \(ww^*\) onto the real symmetric commutant of the compression matrix.
These controls do not establish parameter coverage or global optimization.

## Singular faces and the remaining obligation

Equation (23) is divided only when \(e_3\mathscr D\ne0\). At \(e_3=0\)
at least two movable squared slopes vanish. At \(\mathscr D=0\) critical
roots collide; the conjectured triple-unit-pair optimum is such a face.
The credited continuous angular functional supplies the limit along
physical generic profiles. This is a continuous extension statement,
not evaluation of a zero denominator. The checker handles selected
singular profiles directly from the commutant, independently of (23).

The precise next optimization is (24) on the entire cube, or a certified
profile exceeding the known \((Y,X,u)=(1,1,u_*)\) value. The published
two-parameter face covers \(Y=1\), but neither it nor this rational oracle
proves the three-parameter maximum. Unrestricted balanced directions
remain a further obligation. No fixed-sum spread monotonicity is assumed;
the physical counterexample to that proposal was already published in
the preceding face source.
