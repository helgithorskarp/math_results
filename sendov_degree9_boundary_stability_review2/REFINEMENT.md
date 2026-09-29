# A sharp unit-circle refinement in degree nine

Author of this independent derivation: **six-reviewer-2**, role **reviewer**.
This is a proved restricted refinement of the reviewed lemma, not a priority
claim. All roots and critical points are counted with multiplicity.

Suppose a degree-nine polynomial has all nine roots on the unit circle and
a distinguished root \(a\). Let
\[
\delta=\frac18\sum_{j=1}^8|a-\zeta_j|^{-2}-1
\]
be finite, with \(0\le\delta\le2\cdot10^{-5}\). There is a bijective
labeling, with \(z_0=a\), such that
\[
|z_k-ae^{2\pi i k/9}|\le2500\delta^{5/2},\qquad 0\le k\le8. \tag{R1}
\]
The exponent \(5/2\) cannot be increased on this restricted class. Moreover
the leading critical-energy constant \(8\) in
\(\sum_j|\zeta_j|^2\le(8+o(1))\delta\) is optimal, even on this class.

## Coefficient proof

The zero-deficit case is handled exactly below. Until then assume
\(\delta>0\).

Rotate and normalize to a monic polynomial
\(p(z)=z^9+\sum_{k=0}^8c_kz^k\) with \(p(1)=0\). The distinguished
root is simple, since otherwise the reciprocal sum is infinite.
Set \(q_j=(1-\zeta_j)^{-1}\), \(Q=\sum_j|\zeta_j|^2\), and
\(T=\max_j|\zeta_j|\). The boundary identity gives
\[
\sum_j|q_j-1|^2+2D=8\delta,\qquad
D=\sum_{k=1}^8\frac{1-|z_k|^2}{|1-z_k|^2}.
\]
Here \(D=0\). In fact the following energy estimate only needs \(D\ge0\):
\[
Q\le\frac{8\delta}{(1-\sqrt{8\delta})^2}\le9\delta,
\qquad T\le3\sqrt\delta\le\frac1{32}. \tag{R2}
\]
Indeed \(|q_j|\ge1-\sqrt{8\delta}\) and
\(\zeta_j=(q_j-1)/q_j\). The numerical comparisons hold on the larger
interval \(\delta\le10^{-4}\), as in the target's proof.

Unit-circle roots imply \(|c_0|=1\) and
\(c_k=c_0\overline{c_{9-k}}\); thus paired coefficients have equal modulus.
Integration of the factored derivative gives
\[
c_k=\frac9k(-1)^{9-k}e_{9-k}(\zeta_1,\ldots,\zeta_8),\quad 1\le k\le8.
\]
For \(h\ge2\), pair averaging and Cauchy--Schwarz give
\[
|e_h(\zeta)|\le\binom8h\frac Q8T^{h-2}.
\]
For each coefficient pair use its member involving the larger symmetric
index \(h=\max(k,9-k)\), which is at least five. Consequently
\[
A:=\sum_{k=1}^8|c_k|
\le\frac Q4(126T^3+84T^4+36T^5+9T^6)
<\frac{129}{4}QT^3
\le\frac{31347}{4}\delta^{5/2}. \tag{R3}
\]
The strict numerical comparison follows from
\(126+84/32+36/32^2+9/32^3<129\).

For \(\delta>0\) put \(\rho=2500\delta^{5/2}\), which is less than
\(1/100\). On a circle of radius \(\rho\) about a ninth root of unity
\(\omega\), the binomial expansion gives
\[
|z^9-1|\ge8\rho=20000\delta^{5/2}.
\]
Since \(p(1)=0\),
\[
p(z)-(z^9-1)=\sum_{k=1}^8c_k(z^k-1),
\quad
|p(z)-(z^9-1)|<\frac{21}{10}A
<20000\delta^{5/2}.
\]
The factor \(21/10\) bounds \((101/100)^8+1\), and
\((21/10)(31347/4)<20000\). Rouché gives one root in each disk. The disks
are disjoint, since their diameter is at most \(1/50\), whereas neighboring
ninth roots of unity are separated by at least \(4/9\). The root in the disk
at \(1\) is \(1\) itself. This proves (R1), strictly when \(\delta>0\).
For \(\delta=0\), the reciprocal identity forces all critical points to be
zero, and the normalized polynomial is exactly \(z^9-1\).

## Sharpness and optimal leading energy constant

For real \(t>0\) take
\[
G_t(z)=z^9-1+t(z^5-z^4),\qquad
G'_t(z)=z^3(9z^5+5tz-4t). \tag{R4}
\]
All nine roots lie on the unit circle for \(0<t\le1/1000\). To see this
without numerical root finding, divide by \(z-1\) and use \(x=z+z^{-1}\):
\[
z^{-4}\frac{G_t(z)}{z-1}
=x^4+x^3-3x^2-2x+1+t=:H_t(x).
\]
For every \(0\le t\le1/1000\), this real quartic changes sign on each of
\[
(-19/10,-18/10),\quad(-11/10,-9/10),\quad(3/10,4/10),\quad(15/10,16/10).
\]
The exact endpoint values are in `expected.json`. These four disjoint
intervals lie in \((-2,2)\), so they exhaust the four simple real roots.
Each yields two distinct unit-circle roots of \(z^2-xz+1\). Along with
\(1\), which is not a root of the quotient since its value there is \(9+t\),
they exhaust the nine roots of \(G_t\).

Let \(b=(4/9)^{1/5}\) and write \(z=t^{1/5}v\) in the nonzero critical
factor. The resulting equation is
\(9v^5+5t^{1/5}v-4=0\). Its five simple limiting roots have modulus \(b\),
so ordinary root continuity or the implicit-function theorem gives
\[
Q_t=5b^2t^{2/5}(1+o(1)).
\]
Since all original roots are on the circle, \(D=0\). Also all critical
points tend to zero, and
\(|q_j-1|^2=|\zeta_j|^2/|1-\zeta_j|^2\). Therefore
\[
\delta_t=\frac58b^2t^{2/5}(1+o(1)),\qquad Q_t/\delta_t\longrightarrow8. \tag{R5}
\]
At any nontrivial ninth root of unity \(\omega\), implicit differentiation
of the original polynomial yields
\[
w_\omega(t)=\omega-
\frac{\omega^5-\omega^4}{9\omega^8}t+O(t^2).
\]
Its nonzero velocity has modulus \(|\omega-1|/9\). Hence a matched root
has displacement comparable to \(t\), and thus to \(\delta_t^{5/2}\).
For sufficiently small \(t\), distinct limiting roots force every matching
with error tending to zero to use these local branches. No uniformly valid
bound with exponent greater than \(5/2\) can hold. Equation (R5) also shows
that the leading energy constant \(8\) is optimal.

## Verification boundary

The proof is ordinary complex analysis and polynomial algebra, not a formal
proof. The independent checker verifies the quartic reduction, all interval
signs for the stated parameter range, derivative identities, and exact
rational Rouché constants. The limiting asymptotics and Rouché/implicit-function
bridges are checked in the written proof, not by Python. No floating point,
solver, external input, or omitted large certificate is required.
