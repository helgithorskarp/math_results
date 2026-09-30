# Degree-nine first power with opposite critical-reciprocal phases

Actual author **six-sendov-1**, role **researcher**, 2026-09-30.
Status: complete ordinary written author proof with exact rational
certificates and a second coefficient reconstruction; independent review
pending. The exponent-one endpoint for arbitrary complex critical points
remains outside this result.

After rotating a marked zero to \(a=|a|\), consider degree-nine
polynomials with all zeros in the closed unit disk whose critical
multiset consists of \(\zeta_+\) four times and \(\zeta_-\) four times.
The points may coincide. If the marked zero is also critical, every
reciprocal-distance sum below is infinite. Otherwise put
\[
 U=(a-\zeta_+)^{-1},\qquad V=(a-\zeta_-)^{-1}.
\]
The phase hypothesis is
\[
                        UV\in(0,\infty).                 \tag{1}
\]
Equivalently, the two reciprocal arguments are opposite. Their moduli
may differ; no real-coefficient or conjugate-critical-point hypothesis
is made. For an unrotated nonzero marked zero \(a_{\rm old}\), (1) means
\((a_{\rm old}-\zeta_+)(a_{\rm old}-\zeta_-)/a_{\rm old}^2\)
is positive real.

**Polynomial theorem.** Under (1),
\[
 S_1(p,a):=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}\ge8,          \tag{2}
\]
with multiplicity. It is strict for every interior marked zero.
Equality holds precisely for \(|a_{\rm old}|=1\) and
\(p(z)=C(z^9-a_{\rm old}^9)\), \(C\ne0\).
The zero marked radius is already covered by the classical derivative
product and does not require a phase hypothesis.

The new finite ingredient is a global monotonicity estimate for the
origin norm on this face. We first prove it as an abstract inequality;
the disk-root deduction is in Section 4.

## 1. Exact abstract minimum and radial penalty

Let \(0<a\le1\), \(0<m\le1\), \(|h|\le m/2\), \(r=m+h\),
\(s=m-h\). Let \(c,d\) be real, \(c^2+d^2=1\), with
\[
                         am\le c\le1.
\]
Put \(u=c+id\), \(v=c-id\), \(b=am\), \(Q=h^2/m^2\), and
\[
 O=9\int_0^1(1-atru)^4(1-atsv)^4\,dt,\qquad
 N={|O|^2\over(rs)^8},\qquad
 B(b)=\sum_{j=0}^8(1-b)^j.
\]
Thus \(B(b)=[1-(1-b)^9]/b\) for \(b>0\).

**Abstract theorem.**
\[
 \boxed{\quad
 N\ge m^{-16}\left\{B(am)^2+
            {7\over8}\big[(1-Q)^{-8}-1\big]\right\}.
 \quad}                                                   \tag{3}
\]
In particular,
\[
 N\ge B(a)^2\ge(2-a)^2=3-2a+(1-a)^2.                    \tag{4}
\]
The exact minimum \(B(a)^2\) is attained only by
\(m=1,h=0,c=1\), hence \(r=s=1,u=v=1\).
The penalty in (3) is at least \(7m^{-16}Q=7h^2/m^{18}\).
The numerical constant 7 is sufficient; no optimal derivative constant
is asserted.

To prove this, set \(\beta=(h/m)d\). The pair of factors becomes
\[
 (1-atru)(1-atsv)
       =1-2bt(c+i\beta)+b^2(1-Q)t^2,\qquad
 \beta^2=Q(1-c^2).
\]
Consequently
\[
 E(b,c,Q)=\left|9\int_0^1
       [1-2bt(c+i\beta)+b^2(1-Q)t^2]^4dt\right|^2        \tag{5}
\]
is a polynomial over \(\mathbb Q[b,c,Q]\), independent of the sign of
\(\beta\), and
\[
 N=m^{-16}{E(b,c,Q)\over(1-Q)^8}.
\]
Define
\[
              K=(1-Q)E_Q+8E.                            \tag{6}
\]
The complete rational certificate in Section 2 proves
\[
         K>7\quad(0\le b\le c\le1,\ 0\le Q\le1/4).       \tag{7}
\]
Therefore
\[
 {d\over dQ}{E\over(1-Q)^8}
       ={K\over(1-Q)^9}\ge{7\over(1-Q)^9}.
\]
Integrating from zero to \(Q\) gives the penalty in (3). At \(Q=0\)
the integral in (5) is real and nonnegative:
\[
 E(b,c,0)^{1/2}
   =9\int_0^1(1-2bct+b^2t^2)^4dt
   \ge9\int_0^1(1-bt)^8dt=B(b).
\]
Here \(1-2bct+b^2t^2\ge(1-bt)^2\ge0\). For \(b>0\),
the inequality is strict if \(c<1\). This proves (3).

The function \(B\) decreases strictly on \([0,1]\). Since \(am\le a\),
\(m^{-16}\ge1\), and the radial penalty is nonnegative, (4) follows.
Its equality at the exact minimum requires \(m=1,Q=0,c=1\).
Also \(B(a)\ge1+(1-a)\), giving the last inequality in (4).
At \(a=1\) the same argument and equality conclusion apply.

## 2. Complete exact positivity certificate

No numerical optimization supplies (7). Expand (5) by four polynomial
convolutions in the ring
\[
       \mathbb Q[b,c,Q][i\beta]/(\beta^2-Q(1-c^2)).
\]
For a pair \(P+i\beta T\), multiplication is
\[
 (P+i\beta T)(R+i\beta S)
   =PR-Q(1-c^2)TS+i\beta(PS+TR).
\]
Integrate each coefficient of \(t^k\) with weight \(9/(k+1)\)
and square the resulting norm. This fixes every coefficient of \(E\)
and \(K\); they have respectively **214** and **204** nonzero monomials.
Their coordinatewise degrees are at most \((16,8,8)\) and
\((16,8,7)\).

For each \([\ell,r]=[0,1/2]\) or \([1/2,1]\), substitute
\[
 b=\ell+(r-\ell)x,\quad c=b+(1-b)y,\quad Q=z/4,
                \qquad 0\le x,y,z\le1.                  \tag{8}
\]
These two cells cover the entire domain of (7). In the tensor Bernstein
basis of degrees \((16,8,7)\), write
\[
 K_\ell(x,y,z)=\sum_{i=0}^{16}\sum_{j=0}^{8}\sum_{k=0}^{7}
        \gamma^{(\ell)}_{ijk} B_i^{16}(x)B_j^8(y)B_k^7(z),
\quad B_i^n(t)=\binom ni t^i(1-t)^{n-i}.
\]
If the power coefficients after (8) are \(p_{\alpha\eta\nu}\),
the coefficients are specified exactly by
\[
 \gamma_{ijk}=\sum_{\alpha\le i,\eta\le j,\nu\le k}
 p_{\alpha\eta\nu}
 {\binom i\alpha\over\binom{16}\alpha}
 {\binom j\eta\over\binom8\eta}
 {\binom k\nu\over\binom7\nu}.                           \tag{9}
\]
Every one of the **2448** coefficients is checked.

| Cell for \(b\) | Degrees | Coefficients | Exact minimum |
|---|---|---:|---|
| \([0,1/2]\) | \((16,8,7)\) | 1224 | \(1929755003121/65766686720\) |
| \([1/2,1]\) | \((16,8,7)\) | 1224 | \(2309478237/321126400\) |

Both minima exceed 7. A Bernstein tensor is a nonnegative partition
of unity, so (7) follows. This is a finite certificate for the whole
continuous face, not a sampling assertion.

The checker reconstructs the same **2448 individual entries** by a
second route. At the 1224 tensor points of degrees \((16,8,7)\) in the
unsplit box, it directly evaluates the integral and its \(Q\) derivative
using scalar dual arithmetic. It differentiates
\(\beta^2=Q(1-c^2)\) inside each multiplication, with no division by
\(\beta\) and no square root. Exact inversion of the three Bernstein
sampling matrices reconstructs the unsplit tensor. De Casteljau
subdivision supplies the two half-cell tensors. Every entry agrees
with (9), including zero-index and endpoint entries.

The surrounding domain reduction, integration of (7), and polynomial
deduction remain ordinary written mathematics outside a formal kernel.
The two algorithms are author verification, not independent peer review.

## 3. Credited weak polar mean filter, reproduced here

We use only the weak conclusion of the previously published
[actual-reciprocal mean theorem7518](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_actual_mean_gap/PROOF.md).
It is not new in this result. For self-containment, a shorter direct
envelope certificate reproduces that conclusion.

Let \(0<a<1\), \(D=1-a^2\), \(U=ru,V=sv\), \(|u|=|v|=1\),
\[
 r,s\ge(1+a)^{-1},\quad r+s\le2,\quad
 C=\int_0^1(a+DtU)^4(a+DtV)^4dt.
\]
Put \(m=(r+s)/2,h=(r-s)/2\),
\(\xi=\operatorname{Re}(U+V)/2\), \(\sigma=m^2+h^2\).
If \(|C|\ge1\), then
\[
                              \xi>a.                    \tag{10}
\]
Indeed, the squared-factor AM-GM bound, as in
[Zhang, Lemma4.1](https://arxiv.org/html/2609.19126), gives
\[
 |C|\le\int_0^1
       [a^2+2aD\xi t+D^2\sigma t^2]^4dt.
\]
The expression inside brackets is the arithmetic mean of two squared
moduli and is nonnegative. If \(\xi\le a\), increasing \(\xi\) to \(a\)
and using
\(\sigma\le1+[a/(1+a)]^2\) bounds this integral by
\[
 H(a)=\int_0^1
  \left[a^2+2a^2Dt+
       D^2\left(1+{a^2\over(1+a)^2}\right)t^2\right]^4dt.
\]
Here \(|h|\le m-(1+a)^{-1}\le a/(1+a)\).
The univariate polynomial
\[
 W(a)={(1+a)^8[1-H(a)]\over(1-a)^2}                     \tag{11}
\]
has degree 22. Exact coefficient comparison proves the division
identity in (11). All its 23 Bernstein coefficients on \([0,1]\)
are at least \(8/9\), as recorded individually in the compact expected
manifest and regenerated by the checker. Thus
\[
 H(a)\le1-{8(1-a)^2\over9(1+a)^8}<1,
\]
contradicting \(|C|\ge1\). This proves (10) without importing an
unreproduced finite certificate. The stronger quantitative mean gap
in7518 retains its original attribution and is not used here.

## 4. Deduction for actual disk-root polynomials

Suppose first \(0<a<1\), \(p'(a)\ne0\), and assume for contradiction
\(S_1\le8\). Write \(U=ru,V=sv\). Then \(m=(r+s)/2\le1\).
Gauss-Lucas gives \(|\zeta_\pm|\le1\), so
\[
 r,s\ge(1+a)^{-1},\qquad
 {|h|\over m}\le1-{1\over m(1+a)}
                  \le {a\over1+a}\le {1\over2}.          \tag{12}
\]
The classical origin and polar identities are
\[
 \begin{split}
 O&=9\int_0^1(1-atU)^4(1-atV)^4dt
       =\left(\prod_{j=1}^8 z_j\right)U^4V^4,\\
 C&=\int_0^1(a+DtU)^4(a+DtV)^4dt
       =\prod_{j=1}^8{1-az_j\over a-z_j}.
 \end{split}                                             \tag{13}
\]
Here \(z_j\) are the other eight zeros. Hence
\[
                       N\le1,\qquad |C|\ge1.              \tag{14}
\]
The second inequality follows from
\(|1-az_j|^2-|a-z_j|^2=D(1-|z_j|^2)\ge0\).
These identities are classical, credited to
[Tao, Lemma6](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
and [Zhang, Lemma3.1](https://arxiv.org/html/2609.19126).
They follow alternatively by integrating the critical-point
factorization along the segment from \(a\) to the evaluation point.

Since \(UV>0\), \(v=\overline u\); write \(u=c+id,v=c-id\).
Then \(\xi=mc\), so (10) yields \(c>a/m\ge am\).
The abstract theorem applies by (12), and gives
\[
                    N\ge B(a)^2>1,
\]
contradicting (14). Thus \(S_1>8\) at every interior nonzero marked
radius under (1).

If \(a=0\) and \(p'(0)\ne0\), the derivative product gives
\[
 \prod_{j=1}^8|\zeta_j|^{-1}
          ={9\over\prod_{j=1}^8|z_j|}\ge9.
\]
AM-GM therefore gives \(S_1\ge8\,9^{1/8}>8\), without (1).
A repeated marked zero has \(S_1=+\infty\).

For a simple boundary marked zero normalize \(a=1\). The classical
logarithmic-derivative identity gives
\[
 4(U+V)=2\sum_{j=1}^8{1\over1-z_j},\qquad
 \operatorname{Re}{1\over1-z_j}\ge{1\over2}.
\]
Thus \(\xi=\operatorname{Re}(U+V)/2\ge1\) and \(S_1\ge8\).
If \(S_1=8\), \(m=1\), and under (1) \(mc=\xi\ge1\)
forces \(c=1\). Apply (3) at \(a=m=c=1\); (13) still gives \(N\le1\).
The positive radial penalty forces \(h=0\), so \(U=V=1\).
Every critical point is zero, \(p'(z)=9Cz^8\), and the marked zero
forces \(p(z)=C(z^9-1)\). Undoing rotation gives the equality family
stated after (2); it directly attains equality.

## 5. Exact scope and remaining phase boundary

The new restriction is the positive real reciprocal product, not
coalescence or equal reciprocal radii. For \(r\ne s\) and \(d\ne0\),
the two critical points and the marked zero are not collinear, and the
critical points need not be conjugate.

The earlier [collinear theorem7212](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_first_power/PROOF.md)
requires all critical points and the marked zero on one affine line.
The [unit-radius origin theorem7478](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_balanced_radius_origin_gap/PROOF.md)
supplies the balanced face, while the
[unrestricted 4+4 collar7536](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_imbalance_collar/PROOF.md)
and [coalesced minimum7621](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_coalesced_origin_minimum/PROOF.md)
apply near the unit marked radius. The present monotonicity estimate
allows the full relative imbalance on an opposite-phase face throughout
the marked-radius interval. It does not generalize the unrestricted
collar or assert monotonicity for arbitrary common phase.

The earlier [quadratic matching criterion7358](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_conjugate_matching_phase/PROOF.md)
also covers small unequal-radius perturbations here: pairing the four
copies of U with the four copies of V has total mismatch 8|h|, so its
sufficient test applies when h^2<=(1-a)/576000. The stronger
[independent refinement7420](https://github.com/helgithorskarp/math_results/blob/main/sendov_conjugate_matching_review2/REVIEW.md)
enlarges this sufficient interval to h^2<=(1-a)/102400. Those criteria
allow arbitrary critical multiplicities and more general phase motion.
The new estimate uses the exact4+4 structure to cover the full relative
imbalance on this specified face; it does not replace the broader
matching theorem.

That distinction is necessary:7518 already gives a polar-feasible
counterexample to radial monotonicity away from this face. The complete
complex norm has the form \(E_O+\lambda J_O\), with signed
\(\lambda=-hdy\) for a common unit phase \(x+iy\); here \(y=0\)
eliminates that term. Controlling it on a wider phase domain is the
next analytic boundary. No general 4+4 interior theorem or unrestricted
degree-nine endpoint is claimed.
