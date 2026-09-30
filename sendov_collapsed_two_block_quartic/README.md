# Two-block quartic deficit at the collapsed Sendov cutoff

**six-sendov-2**, role **researcher**.
Complete ordinary proof with symbolic exact checks; this extension awaits
independent review. The all-degree Sendov proof report is prior literature.

For \(n=m+1\ge4\), \(a=(m+2)/(2m)\), \(s=m-r\), and integers
\(1\le r\le m-1\), consider
\[
p_t=(z-a)(z+e^{ist})^r(z+e^{-irt})^s.
\]
Write \(F=\sum|a-\zeta_j|^{-1}\), count critical points with multiplicity,
and let
\[
E=r|(a+e^{ist})^{-1}-(1+a)^{-1}|^2+
  s|(a+e^{-irt})^{-1}-(1+a)^{-1}|^2.
\]
The theorem proves
\[
F=\frac{2m}{1+a}-K_m(r)E^2+O_{m,r}(E^3),\quad
K_m(r)=\frac{(m+2)(3m+2)^3}{256m^7}
\left[\frac{m^2(m^2-4m-4)}{r(m-r)}-(m-6)(3m+2)\right]>0.
\]
For \(m\ge5\), the largest coefficient within these balanced two-block
curves occurs exactly at \(r=1,m-1\). The two smaller degrees are treated
exactly in the proof.

In degree nine,
\[
\max_r K_8(r)=\frac{560235}{8388608},
\]
strictly above the preceding moving-pair coefficient by
\(164775/33554432\). The two-block maximum first improves on that curve
in degree nine, and does so in every higher degree.
This strengthens a lower bound for the extremal quartic energy deficit.
Global angular extremality and the best maximum-root basin constant are
open. The curve violates a radial baseline greater than8; it supplies
no counterexample to the first-power Tang--Zhang endpoint.

The proof factors the derivative into repeated factors and one quadratic,
then uses an exact formula for the sum of its root moduli. Positive scalar
square roots and conjugation supply the analytic remainder, without
assuming analytic labels at a repeated critical point.

- [PROOF.md](PROOF.md): statement, branch-free reduction, exact coefficients,
  multiplicity optimization, degree threshold and proof boundary.
- [verify.py](verify.py): standalone symbolic arithmetic and compact output.
- [LITERATURE.md](LITERATURE.md): primary sources and exact comparison scope.

From the repository root, Python 3.11.2 standard library:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B sendov_collapsed_two_block_quartic/verify.py
~~~

Expected: **PASS**, **60 exact checks**, **five rejected coefficient
mutations**, maximum degree-nine coefficient 560235/8388608,
excess 164775/33554432. The degree and multiplicity remain symbolic;
no interpolation, floating point, solver or external certificate is used.
One small CPU job, all library threads one. The ordinary analytic bridge
is written mathematics and has not been formalized.

The comparison imports only the earlier moving-pair coefficient. Its
independent review at source c153e27a7bd3da634bd652fc804387e94c8ab71b
confirms that predecessor, not this extension. The global finite upper
bound for the extremal coefficient in PROOF.md uses the author's preceding
quartic stability theorem, whose independent review remains pending.
