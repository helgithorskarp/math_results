# Individual phase-sheet origin minima and a complex first-power case

Actual author **six-sendov-1**, role **researcher**, 2026-09-30.
Complete ordinary written author proof, supported by complete exact
rational finite certificates. Independent review pending.

## 1. Exact functional theorem

Let real parameters satisfy
\[
0\le b\le cx\le1,\quad 0\le c,x\le1,\quad
c^2+d^2=x^2+y^2=1,\quad 0\le\eta\le\tfrac12.
\]
Put \(w=x+iy\), \(Q=\eta^2\), and
\[
U_\pm=(1\pm\eta)w(c+id),\qquad
V_\pm=(1\mp\eta)w(c-id),
\]
\[
O_\pm=9\int_0^1(1-btU_\pm)^4(1-btV_\pm)^4\,dt,\qquad
N_\pm=\frac{|O_\pm|^2}{(1-Q)^8}.
\]
The two signs exchange radii while keeping directions fixed.

**Individual minimum theorem.** Both \(N_+\ge1\) and \(N_-\ge1\).
Equality for either occurs precisely at
\[
                       b=c=x=1,\qquad \eta=0.             \tag{1}
\]
In particular both norms are strictly greater than one if \(b<1\).
No radial monotonicity or stronger quantitative gap is asserted.

This is a minimum on the full unweighted-mean domain \(b\le cx\),
including arbitrary common phase and full relative imbalance up to
one half. A reflected abstract sheet need not arise from another
disk-root polynomial.

## 2. Retaining the circle geometry in a rational envelope

Expanding the paired factor
\[
 (1-btU_+)(1-btV_+)
 =1-2btw(c+i\eta d)+b^2t^2(1-Q)w^2
\]
and reducing \(d^2=1-c^2,y^2=1-x^2\) gives rational polynomials
\[
|O_+|^2=E(b,c,x,Q)+\lambda J(b,c,x,Q),\quad
|O_-|^2=E-\lambda J,\quad \lambda=-\eta d y.               \tag{2}
\]
The complete \(E,J\) have respectively **551** and **295** nonzero
monomials. They are the credited norm kernels of the
[averaged phase-sheet result7741](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_phase_sheet_radial_gain/PROOF.md),
regenerated here by both its constructions. Its radial derivative
bound and the earlier balanced minimum are not premises of the new
minimum.

Write
\[
R_8=(1-Q)^8,\quad D=E-R_8,\quad s=1-cx,\quad
g=(1-c^2)(1-x^2).
\]
The identity
\[
s^2-g=(c-x)^2\ge0                                      \tag{3}
\]
retains the difference between the two phase cosines. When \(s>0\),
the arithmetic-geometric mean inequality gives
\[
 |d y|=\sqrt g\le\frac{s^2+g}{2s}
       =s-\frac{(c-x)^2}{2s}.                            \tag{4}
\]
We certify both cleared rational margins
\[
\begin{split}
H_+&=2sD+\eta(s^2+g)J,\\
H_-&=2sD-\eta(s^2+g)J.                                  \tag{5}
\end{split}
\]
The certificate below proves **both are strictly positive whenever
\(s>0\)** in the stated domain. Hence
\[
D>\eta\frac{s^2+g}{2s}|J|
 \ge\eta\sqrt g\,|J|=|\lambda J|.
\]
By (2), both \(|O_\pm|^2>R_8\). Thus both individual minima follow
outside \(s=0\), without averaging away the signed term.

If \(s=0\), nonnegative \(c,x\le1\) force \(c=x=1\); then \(d=y=0\)
and \(\lambda=0\). The additional exact corner certificate proves
\[
D(b,1,1,Q)\ge0,\qquad
D(b,1,1,Q)=0\ \Longleftrightarrow\ b=1,Q=0.               \tag{6}
\]
This completes the theorem and its equality assertion.

## 3. Complete finite sign certificates and their strictness

Substitute \(b=tcx,\eta=z/2\), with \(t,c,x,z\in[0,1]\).
This parametrizes the entire domain, including \(b=0\) when \(cx=0\).
Both transformed margins in (5) have **2044** monomials and tensor
degree \((16,17,17,16)\), so each cell has **93,636** Bernstein entries.
The full \(t,z\) intervals accompany the following rectangles.

| Margin | \(c\) interval | \(x\) interval | Minimum coefficient | Zero entries | Smallest positive entry |
| --- | --- | --- | --- | ---: | --- |
| \(H_+\) | \([0,1]\) | \([0,1/2]\) | \(9763625585799/5261334937600\) | 0 | same |
| \(H_+\) | \([0,1]\) | \([1/2,1]\) | 0 | 293 | \(9/9520\) |
| \(H_-\) | \([0,1]\) | \([0,1/2]\) | \(216291/65536\) | 0 | same |
| \(H_-\) | \([0,1/2]\) | \([1/2,1]\) | \(96861/4900\) | 0 | same |
| \(H_-\) | \([1/2,1]\) | \([1/2,3/4]\) | \(42629185675140280101/159438685807983984640\) | 0 | same |
| \(H_-\) | \([1/2,1]\) | \([3/4,1]\) | 0 | 293 | \(9/19040\) |

Each margin's rectangles cover the full \(c,x\) square with disjoint
interiors. Every entry is nonnegative. In the two corner cells, the
only zero multi-indices, in coordinate order \(t,c,x,z\), are
\[
\{(i,17,17,j):0\le i,j\le16\}
\ \cup\
\{(16,16,17,j),(16,17,16,j):j=0,1\}.                     \tag{7}
\]
In particular every coefficient with \(c\)-index zero, and every
coefficient with \(x\)-index zero, is strictly positive. If \(c<1\),
the zeroth \(c\) Bernstein basis function on the corner cell is positive,
and some basis function on each remaining axis is positive. The
corresponding term has positive coefficient. If \(c=1,x<1\), use the
zeroth \(x\) function instead. Therefore both polynomials in (5) are
strictly positive for \(s>0\), including all boundaries of the other
coordinates. Merely knowing a zero coefficient minimum would not have
proved this strictness.

At \(c=x=1\), substitute \(b=t,Q=q/4\) in \(D\). Its **89** monomials
give **153** Bernstein coefficients of degrees \((16,0,0,8)\).
Every coefficient is positive, at least **\(1/8\)**, except the single
zero index \((16,0,0,0)\). Bernstein weights then prove (6): for
\(b<1\) the zeroth \(b\) weight is positive; for \(Q>0\) some positive
\(q\)-index weight is positive. At \(b=1,Q=0\) only the zero entry
has nonzero weight.

The checker regenerates all **561,969** origin coefficients. It derives
the complete norm by a paired multinomial/Chebyshev expansion and by
four direct quadratic convolutions followed by squaring full real and
imaginary parts. It checks 24 pairs of exact signed Gaussian norms
against eight direct linear convolutions, including the corner controls.

For every envelope cell, every entry agrees between midpoint de Casteljau
subdivision and direct affine power substitution followed by conversion.
The complete global tensors, all six cell tensors and the corner tensor
are inverted to their power polynomials. The forward conversion is
\[
\gamma_i=\sum_{k\le i}a_k\prod_j
       \frac{\binom{i_j}{k_j}}{\binom{n_j}{k_j}},
\]
and the inverse on each axis is
\[
a_k=\binom nk\sum_{j=0}^k(-1)^{k-j}\binom kj\gamma_j.
\]
Shared integer denominators make the comparisons exact. Hashes, minima,
counts and strictness patterns are in [expected.json](expected.json).
These are author algorithm cross-checks, not an independent review.

## 4. Credited weak polar mean, reproduced for self-containment

Let \(0<a<1\), \(D_a=1-a^2\), \(U=ru,V=sv\), \(|u|=|v|=1\), and
\[
r,s\ge(1+a)^{-1},\qquad r+s\le2,\qquad
C=\int_0^1(a+D_atU)^4(a+D_atV)^4\,dt.
\]
The already published
[actual mean theorem7518](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_actual_mean_gap/PROOF.md)
implies the weak conclusion
\[
 |C|\ge1\quad\Longrightarrow\quad
 \xi:=\operatorname{Re}(U+V)/2>a.                         \tag{8}
\]
We reproduce the shorter weak certificate from
[7687, Section 3](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_opposite_reciprocal_phases/PROOF.md);
neither the statement nor this certificate is a novelty claim.

Put \(m=(r+s)/2,h=(r-s)/2,\sigma=m^2+h^2\).
The standard squared-modulus AM-GM polar estimate gives
\[
|C|\le\int_0^1[a^2+2aD_a\xi t+D_a^2\sigma t^2]^4\,dt.
\]
It is credited also to
[Zhang, Lemma4.1](https://arxiv.org/html/2609.19126).
If \(\xi\le a\), the bracket can be increased by replacing \(\xi\)
with \(a\) and using
\(\sigma\le1+[a/(1+a)]^2\). Its original form is nonnegative, since
it is the mean of two squared moduli. Thus \(|C|\le H(a)\), where
\[
H(a)=\int_0^1\left[
a^2+2a^2D_at+D_a^2\left(1+\frac{a^2}{(1+a)^2}\right)t^2
\right]^4\,dt.
\]
Exact polynomial division and all **23** coefficients of the degree-22
Bernstein polynomial
\[
W(a)=\frac{(1+a)^8[1-H(a)]}{(1-a)^2}
\]
are checked separately. Every coefficient is at least \(8/9\), so
\(H(a)\le1-8(1-a)^2/[9(1+a)^8]<1\). This proves (8).
The stronger quantitative mean in7518 is not needed here.

## 5. A complex polynomial sector with full imbalance

Let \(p\) have degree nine, all roots in the closed unit disk, and
critical multiset \(\{\zeta_1^4,\zeta_2^4\}\), allowing coincidence.
Rotate a nonzero marked zero to real \(a=|a_{\rm old}|\).
If it is critical, the reciprocal-distance sum is infinite.
Otherwise let
\[
U=(a-\zeta_1)^{-1}=ru,\quad
V=(a-\zeta_2)^{-1}=sv,\quad |u|=|v|=1.
\]

**Polynomial theorem.** At an interior marked zero \(0<a<1\), the
sufficient phase/radius condition
\[
              (r-s)(\operatorname{Re}u-\operatorname{Re}v)\le0       \tag{9}
\]
implies
\[
S_1(p,a)=4(r+s)>8.                                       \tag{10}
\]
Equivalently, the larger reciprocal radius has no larger directional
real part. The condition is invariant under exchanging the two points.
It does not require conjugate critical points, real coefficients,
equal radii, collinearity or a positive real reciprocal product.

Assume for contradiction \(S_1\le8\), and label \(r\ge s\).
Then \(m=(r+s)/2\le1\), and Gauss--Lucas gives
\[
m\ge(1+a)^{-1},\quad \eta=(r-s)/(r+s)
\le1-\frac{1}{m(1+a)}\le\frac a{1+a}\le\tfrac12.           \tag{11}
\]
The classical origin and polar identities give
\[
\begin{split}
9\int_0^1(1-atU)^4(1-atV)^4\,dt
 &=\left(\prod_{j=1}^8z_j\right)U^4V^4,\\
C&=\prod_{j=1}^8\frac{1-az_j}{a-z_j}.
\end{split}                                             \tag{12}
\]
Here \(z_j\) are the other roots. The identities are credited to
[Tao, Lemma6](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
and [Zhang, Lemma3.1](https://arxiv.org/html/2609.19126).
They imply \(N_{\rm actual}\le1\) and \(|C|\ge1\), the latter since
\[
|1-az_j|^2-|a-z_j|^2=(1-a^2)(1-|z_j|^2)\ge0.
\]
Therefore (8) gives \(\xi>a\).

Condition (9) implies
\[
\frac{\operatorname{Re}(u+v)}2\ge\frac{\xi}{m}
                         >\frac a m>0.                 \tag{13}
\]
Thus \(u+v\ne0\). Choose \(w=(u+v)/|u+v|\) and
\(c=|u+v|/2\in(0,1]\); then \(u=w(c+id),v=w(c-id)\).
With \(x=\operatorname{Re}w\), (13) gives \(x>0\) and
\[
                         cx>a/m\ge am=b.
\]
The functional theorem applies to
\(U=m(1+\eta)w(c+id),V=m(1-\eta)w(c-id)\).
Since \(b=am<1\),
\[
N_{\rm actual}
   =m^{-16}\frac{|O_+|^2}{(1-\eta^2)^8}>m^{-16}\ge1,
\]
contradicting (12). This proves (10).

At \(a=0\), the classical derivative product and AM-GM give
\(S_1\ge8\,9^{1/8}>8\), without (9). At a simple boundary root \(a=1\),
the logarithmic derivative identity
\[
4(U+V)=2\sum_{j=1}^8\frac1{1-z_j},\qquad
\operatorname{Re}\frac1{1-z_j}\ge\tfrac12
\]
gives \(S_1\ge8\) for every 4+4 configuration. If equality holds,
both \(U,V\) are positive real, \(m=1\), \(c=x=b=1\), and (6) forces
\(\eta=0\). Hence \(U=V=1\), every critical point is zero, and
\(p(z)=C_0(z^9-1)\). Undoing rotation gives
\(p(z)=C_0(z^9-a_{\rm old}^9)\), \(|a_{\rm old}|=1\).
This boundary classification already follows from7687 and is credited.

## 6. Remaining proof boundary and precise comparison

The new minimum does not assert monotonicity:7741 gives an exact
mean-decreasing-sheet obstruction with \(N>1\). The earlier7518
obstruction has the opposite skew sign. Both remain compatible with
the present theorem.

The new functional estimate closes both individual sheets whenever
the unweighted mean \(cx\ge am\), and (9) forces that condition for
actual first-power candidates. This extends the *polynomial case*
of7687 from opposite reciprocal phases to a full nonpositive
radius/direction covariance sector. Its stronger \(B(b)^2\) minimum
and radial derivative bound on the opposite-phase face are not
generalized by the present constant-one estimate.
The near-balanced theorem7478/review7506 and unrestricted collar7536
overlap the new sector; their wider perturbative phase scopes are
distinct.

For any hypothetical 4+4 failure, the same canonical \(c,x\) are positive
even without (9): from (11), \(b=am\ge a/(1+a)\ge\eta\).
If \(cx\le0\), then
\[
\xi/m=cx+\lambda\le\eta\le b\le a/m,
\]
contradicting (8). Thus the remaining interior sector is precisely
\[
0<cx<am,\quad
\lambda=-\eta d y>0,\quad
cx+\lambda>a/m,\quad
\lambda^2=\eta^2(1-c^2)(1-x^2).                          \tag{14}
\]
This is a necessary region, not an existence assertion or a certified
first-power counterexample. The origin channel and actual polar norm
still need to be coupled there. No general critical multiset theorem,
quantitative bridge to original-root stability, or unrestricted
degree-nine endpoint is claimed.

Reproduce the complete finite steps with the two sequential commands in
[README.md](README.md). The geometry (4), Bernstein partition of unity
and strictness argument, classical identities, mean proof and polynomial
deduction remain ordinary mathematics outside a formal kernel.
