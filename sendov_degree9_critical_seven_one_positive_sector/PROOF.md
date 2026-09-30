# A complex critical7+1 sector, stability, and exact light-phase elimination

Author **six-sendov-1**, role **researcher**, 2026-09-30.
This is an ordinary mathematical proof with regenerated exact finite
sign evidence. It is unformalized; independent review is pending.
The full complex7+1 case and the unrestricted degree-nine first-power
Tang--Zhang inequality remain open here.

## 1. The polynomial result and its precise sector

Let \(p\) have degree nine and all zeros in the closed unit disk. Let \(a\)
be a marked zero. Suppose its critical multiset is
\(\{\zeta_H^7,\zeta_L\}\), allowing \(\zeta_H=\zeta_L\), and suppose
\[
 |a-\zeta_H|\le |a-\zeta_L|.                         \tag{1}
\]
Then
\[
 S_1(a):=\frac7{|a-\zeta_H|}+\frac1{|a-\zeta_L|}\ge8. \tag{2}
\]
The inequality is strict if \(|a|<1\). Equality in this sector occurs
exactly when \(|a|=1\) and \(p(z)=C(z^9-a^9)\), \(C\ne0\).
If a denominator vanishes, \(S_1=\infty\), so these assertions are immediate.

The multiplicity labels in (1) are fixed. Exchanging the critical points
does not preserve the7+1 pattern. In particular, (2) does not cover the
opposite ordering. The already known boundary family
\(C(z-a)(z+a)^8\), \(|a|=1\), has its sevenfold critical point at \(-a\)
and its single critical point at \(7a/9\); it violates (1).
It remains an essential equality corner of the full7+1 problem.

## 2. Abstract origin minimum and quantitative stability

Let \(0\le b\le1\), \(0\le\eta\le1/14\), and \(u,v\) be unit complex numbers.
Set
\[
 r=1+\eta,\quad s=1-7\eta,\quad U=ru,\quad V=sv,\quad
 M=(7U+V)/8=\rho w,\quad w=x+iy.
\]
Assume \(\mu=\Re M\ge b\). Define
\[
 I=9\int_0^1(1-b\tau U)^7(1-b\tau V)\,d\tau,\qquad
 R=r^{14}s^2,\qquad N=|I|^2/R.                      \tag{3}
\]
Then \(N\ge1\), with equality exactly at
\[
 b=1,\quad \eta=0,\quad u=v=1.                      \tag{4}
\]
The following conservative, explicit stability bounds also hold.
With the coordinates below,
\[
 N-1\ge\frac34\max\{(1-c)^9,(1-x)^{19}\}.            \tag{5}
\]
On the aligned phase corner \(c=x=1\),
\[
 N-1\ge\frac14\{(1-b)+(14\eta)^2\}.                 \tag{6}
\]
No optimality or original-root metric bound is asserted.
The phase coordinates have the geometric interpretations
\(|u-v|^2=4(1-c)\) and \(|w-1|^2=2(1-x)\).

Put
\[
 K=(3+7\eta)/4\in[3/4,7/8],\quad
 r=\frac47(1+K),\quad s=4(1-K).
\]
The two weighted unit vectors forming \(M\) have weights
\((1+K)/2,(1-K)/2\). Thus \(K\le\rho\le1\); in particular \(M\ne0\).
Since \(\mu\ge0\), \(0\le x\le1\). Write
\[
 q=\rho^2=K^2+(1-K^2)c,\quad 0\le c\le1,\quad
 \delta^2=c(1-c).
\]
The triangle identity for the two vectors gives, with the sign of
\(\delta\) retained,
\[
 U=\frac{4w}{7\rho}\{q+K+i(1-K^2)\delta\},\qquad
 V=\frac{4w}{\rho}\{q-K-i(1-K^2)\delta\}.            \tag{7}
\]
Indeed, the two sides \((1+K)\bar w u,(1-K)\bar w v\) sum to \(2\rho\).
The first real part is \((q+K)/\rho\), and its squared imaginary part is
\((1-q)(q-K^2)/q=(1-K^2)^2c(1-c)/q\).
The norm identity for \(M\) also gives
\(c=(1+\Re(u\bar v))/2\), proving the interpretation after (6).

If \(\mu>0\), put \(t=b/\mu\in[0,1]\). If \(\mu=0\), then \(b=x=0\);
take \(t=0\). In either case \(b=t\rho x\). Substitute (7) into (3).
The factor \(\rho\) cancels from \(bU,bV\). The exact sparse algebra in
[algebra.py](algebra.py) gives
\[
 |I|^2=E+\lambda J,\quad
 \lambda=-\delta y,\quad \lambda^2=h:=c(1-c)(1-x^2),
\]
\[
 R=\left(\frac47\right)^{14}16(1+K)^{14}(1-K)^2,
 \qquad D=E-R.                                    \tag{8}
\]
These identities reuse, with attribution, the author's
[critical7+1 polar reduction](../sendov_degree9_critical_seven_one_polar_reduction/PROOF.md).
All coefficients are regenerated, not imported from a6+2 certificate.
Two complete integral constructions and two complete norm constructions
agree coefficient by coefficient. The nonzero monomial counts of
\(E,J,D\) are5115,3642,5129, respectively.

## 3. Four exact cells and the stability deduction

Let \(\sigma=1-cx^2\). On the cube \(\sigma\ge0\), and
\[
 \sigma^2-4h=(1-2c+cx^2)^2\ge0.                    \tag{9}
\]
If \(\sigma>0\), the first Newton bound is
\[
 \sqrt h\le f_1:=\frac{\sigma^2+4h}{4\sigma}.
\]
This follows directly from
\(f_1-\sqrt h=(\sigma-2\sqrt h)^2/(4\sigma)\ge0\).
Define the two cleared polynomials
\[
 H_\pm=4\sigma D\pm(\sigma^2+4h)J.                 \tag{10}
\]
Then
\[
 D+\lambda J\ge D-|J|\sqrt h
 \ge \frac{\min(H_-,H_+)}{4\sigma}.                \tag{11}
\]

Each polynomial in (10) has15610 nonzero monomials and degrees
\((16,9,19,32)\) in \((t,c,x,K)\). For each sign, the complete domain
\[
 [0,1]_t\times[0,1]_c\times[0,1]_x\times[3/4,7/8]_K
\]
is split into exactly two cells, \(x\in[0,1/2]\) and \(x\in[1/2,1]\).
There are112200 tensor Bernstein coefficients in each cell.
Every coefficient is nonnegative. More precisely:

- Every coefficient with \(c\)-index zero is at least3 in every cell.
- Every coefficient with local \(x\)-index zero is at least3.
- In the cell \(x\in[0,1/2]\), every coefficient is at least3.

The full coefficients are generated and checked by
[verify.py](verify.py), using [certificate.py](certificate.py).
For both signs the checker inverts the complete global tensor and every
cell tensor, and compares every cell entry with an independent direct
affine expansion. A complete Fraction-based affine expansion checks one
full margin cell. The two intervals cover the whole \(x\)-range; no
sampled positivity or unexamined tensor entries are used.

The Bernstein basis is nonnegative and sums to one. Its zeroth
\(c\)-basis element is \((1-c)^9\), so the first support property gives
\[
 H_\pm\ge3(1-c)^9.
\]
In the low-\(x\) cell \(H_\pm\ge3\ge3(1-x)^{19}\). In the high-\(x\) cell,
the local coordinate is \(2x-1\), so the second support property gives
\[
 H_\pm\ge3\{2(1-x)\}^{19}\ge3(1-x)^{19}.
\]
Hence \(\min(H_-,H_+)\ge3\max\{(1-c)^9,(1-x)^{19}\}\).
Since \(0<\sigma\le1\), (11) yields
\[
 D+\lambda J\ge\frac34\max\{(1-c)^9,(1-x)^{19}\}.
\]
Weighted AM-GM and \(7r+s=8\) give \(r^7s\le1\), so \(0<R\le1\).
Division by \(R\) proves (5), and gives strict positivity unless
\(c=x=1\).

If \(\sigma=0\), necessarily \(c=x=1\) and \(\lambda=0\); we do not
divide by \(\sigma\) there. The same corner must also be treated for
equality. Set \(z=8(K-3/4)=14\eta\in[0,1]\). The corner polynomial
\[
 D(t,1,1,K)-\frac14\{(1-t)+z^2\}                  \tag{12}
\]
has a full nonnegative Bernstein representation of degrees
\((16,0,0,16)\) with289 entries. The checker verifies the complete inverse
and a complete Fraction/integer affine comparison. Its only zero
indices are \((16,0,0,0)\) and \((16,0,0,1)\). Consequently
\(D(t,1,1,K)\ge((1-t)+z^2)/4\). Here \(\rho=x=1\), so \(b=t\);
division by \(R\le1\) proves (6). Equality \(N=1\) forces \(t=1,z=0\).
Conversely at that point \(U=V=1\),
\(I=9\int_0^1(1-\tau)^8d\tau=1\), and \(R=1\).
This proves (4) and the whole abstract lemma.

## 4. Passage back to disk-root polynomials

Rotate and scale the polynomial so that the marked zero is real
\(a\in[0,1]\) and the polynomial is monic. Suppose the marked zero is
simple; otherwise \(S_1=\infty\). For \(a>0\), put
\[
 U_*=(a-\zeta_H)^{-1},\quad V_*=(a-\zeta_L)^{-1},\quad
 m=(7|U_*|+|V_*|)/8.
\]
Assume \(S_1\le8\), so \(0<m\le1\). Set \(U=U_*/m,V=V_*/m,b=am\).
Condition (1) gives \(|U|\ge|V|\). Therefore the normalized radii have
the form \(r=1+\eta,s=1-7\eta\) with \(\eta\ge0\).
Gauss--Lucas gives \(|V_*|\ge1/(1+a)\). Since \(m(1+a)=m+b\le1+b\),
\[
 s\ge\frac1{1+b},\qquad
 0\le\eta\le\frac{b}{7(1+b)}\le\frac1{14}.         \tag{13}
\]

For \(0<a<1\), the **logical premise** is the proved polar lemma in the
author's prior [critical7+1 source](../sendov_degree9_critical_seven_one_polar_reduction/PROOF.md),
commit0bebc1748ea52c1c770c660fcb9eb04b76fb888f, graph
bafkreigbdgbmjvmsggbdwgs5xekg43bdtifapki5ox5zl2nlxjr3iux3pm.
Under \(7|U_*|+|V_*|\le8\) and the critical radius lower bounds, it says
that weighted real mean \(\xi\le a\) forces the polar integral modulus
to be at most \(1-(8/9)(1-a)^2<1\).
The classical polar communication identity for a disk-root polynomial
has modulus at least one. Thus \(\xi=(7\Re U_*+\Re V_*)/8>a\), and
\(\mu=\xi/m>a/m\ge am=b\).
[polar.py](polar.py) reproduces this credited premise, including all675
positive coefficients, two full integral constructions and its full
inverse identity. Its previously proved quantitative mean constants are
reproduced for verification, not claimed as a new result.

At \(a=1\), write the other zeros as \(z_1,\ldots,z_8\). Logarithmic
differentiation gives
\[
 7U_*+V_*=\frac{p''(1)}{p'(1)}
      =2\sum_{j=1}^8\frac1{1-z_j}.
\]
Because \(|z_j|\le1\) and \(z_j\ne1\),
\(\Re(1/(1-z_j))\ge1/2\). Hence \(\xi\ge1\),
and again \(\mu=\xi/m\ge1/m\ge m=b\).
This is the classical boundary argument, not a new endpoint theorem.

The classical origin identity reads
\[
 9\int_0^1(1-a\tau U_*)^7(1-a\tau V_*)\,d\tau
       =-\frac{p(0)}a\,U_*^7V_*.
\]
Consequently its normalized ratio (3) satisfies
\[
 N=m^{16}\frac{|p(0)|^2}{a^2}
   =m^{16}\prod_{j=1}^8|z_j|^2\le m^{16}\le1.     \tag{14}
\]
The abstract lemma contradicts (14) when \(a<1\), because \(b=am<1\)
cannot be its equality point. Thus \(S_1>8\) in that case. At \(a=1\),
equality requires \(m=1,b=1,\eta=0,U=V=1\). Both critical points are
then zero, so \(p(z)=z^9-1\) in these normalized coordinates.
Undoing rotation and scalar normalization gives the equality stated
in section1; its direct verification is immediate.

At \(a=0\), if a critical point is zero the result is immediate.
Otherwise \(|p'(0)|=\prod_{j=1}^8|z_j|\le1\) and
\(|p'(0)|=9\prod_{j=1}^8|\zeta_j|\). AM-GM therefore gives
\(S_1\ge8\,9^{1/8}>8\). This familiar argument completes section1.

## 5. Exact scalar reduction for the remaining opposite ordering

The unrestricted normalized7+1 closure proposed in the prior source
retains both disk constraints
\[
 |b-1/U|\le1,\quad |b-1/V|\le1,\quad
 7|U|+|V|=8,\quad \Re((7U+V)/8)\ge b,\quad0<b\le1.
\]
It includes \(r=|U|<1\), the ordering still open here.
The following reduction eliminates the phase of \(V\) exactly without
dropping either disk or mean constraint. It does not prove the resulting
scalar lower bound.

Put \(s=8-7r\), \(U=ru\), \(V=sv\), and conjugate the pair if necessary
so that \(u=\chi+i\sqrt{1-\chi^2}\). Define
\[
 d_b(r)=\frac{1-(1-b^2)r^2}{2br}.
\]
The exact feasible domain for \(b,r,\chi\) is
\[
 0<b\le1,\quad \frac1{1+b}\le r\le
                  \frac{8-(1+b)^{-1}}7,
\]
\[
 \max\left\{-1,d_b(r),\frac{8b-s}{7r}\right\}\le\chi\le1. \tag{15}
\]
For such a point, the remaining phase is precisely the nonempty arc
\[
 |v|=1,\quad \Re v\ge\ell,\qquad
 \ell=\max\left\{-1,d_b(s),\frac{8b-7r\chi}{s}\right\}\le1. \tag{16}
\]
To see this, each disk constraint is equivalent to
\((1-b^2)|U|^2+2b\Re U-1\ge0\), and similarly for \(V\).
The lower radius bounds in (15) are necessary by the triangle inequality
and ensure \(d_b(r),d_b(s)\le1\). The mean inequality then gives precisely
the additional lower bounds in (15) and (16). Conversely all these
conditions imply the two disks and the mean, so no phase information is
lost. Every interval and denominator in (15)--(16) is well defined.

Define the two complex polynomials
\[
 A_0=9\int_0^1(1-br\tau u)^7\,d\tau
    =9\sum_{j=0}^7\binom7j\frac{(-br)^ju^j}{j+1},
\]
\[
 B_0=9b\int_0^1\tau(1-br\tau u)^7\,d\tau
    =9b\sum_{j=0}^7\binom7j\frac{(-br)^ju^j}{j+2}.
\]
Then \(I=A_0-svB_0\). Write \(Z=\bar A_0B_0=P+iQ\).
For \(\ell\in[-1,1]\), let
\[
 {\cal M}(Z,\ell)=
 \begin{cases}
 0,&Z=0,\\
 |Z|,&Z\ne0,\ P/|Z|\ge\ell,\\
 P\ell+|Q|\sqrt{1-\ell^2},&Z\ne0,\ P/|Z|<\ell.
 \end{cases}                                       \tag{17}
\]
This is exactly \(\max_{|v|=1,\Re v\ge\ell}\Re(Zv)\).
Indeed the unconstrained maximizer is \(\bar Z/|Z|\). If it lies outside
the arc, writing \(v=h+ik\) and optimizing the sign of \(k\) gives
\(Ph+|Q|\sqrt{1-h^2}\), \(h\in[\ell,1]\); its maximum is at \(h=\ell\).
This also covers \(Q=0\), \(\ell=\pm1\), and the zero case separately.
Thus the exact minimum over feasible light phases is
\[
 \min_v N=
 \frac{|A_0|^2+s^2|B_0|^2-2s\,{\cal M}(Z,\ell)}
      {r^{14}s^2}.                                \tag{18}
\]

[arc.py](arc.py) constructs \(A_0=A_r+i\sqrt{1-\chi^2}A_i\) and
\(B_0=B_r+i\sqrt{1-\chi^2}B_i\) over \(\mathbb Q[b,r,\chi]\) by two
independent coefficient constructions. It checks the complete Gram
identity
\[
 (A_r^2+(1-\chi^2)A_i^2)(B_r^2+(1-\chi^2)B_i^2)
 =P^2+(1-\chi^2)(A_rB_i-A_iB_r)^2.
\]
There are384 exact Gaussian integral/objective controls and nine
rational optimizer controls covering both branches, their switch,
degeneracies and arc endpoints. The full arc optimization is the ordinary
geometric argument above, not an inference from these finite controls.
Here \(\chi\) is the heavy phase projection; it differs from the weighted
mean projection \(x\) in sections2--3.

For a concrete remaining sign problem, set
\[
 L=|A_0|^2+s^2|B_0|^2-r^{14}s^2,\qquad
 Q=\sqrt{1-\chi^2}\,Q_0,\quad Q_0=A_rB_i-A_iB_r.
\]
In the free branch of (17), inequality (18)\(\ge1\) is equivalent to
\[
 L\ge0,\qquad L^2-4s^2|A_0|^2|B_0|^2\ge0.          \tag{19}
\]
In the constrained branch put \(W=L-2sP\ell\). The same target is
equivalent to
\[
 W\ge0,\qquad
 W^2-4s^2(1-\chi^2)Q_0^2(1-\ell^2)\ge0.           \tag{20}
\]
The nonnegative first inequalities are essential before squaring.
Splitting according to the maximum in (16), and clearing only positive
denominators \(b,r,s\), makes (19)--(20) explicit rational polynomial
sign targets on the corresponding domains. These reductions do not
assert their signs.

Proving (18) is at least one on the part \(r<1\) of (15), with equality
only at \(b=1,r=1/2,\chi=1,v=1\), would close the remaining7+1 case,
alongside the positive sector already proved. That scalar inequality is
**unproved here**. Floating probes motivated this reduction but provide
no sign evidence and are not part of the certificate.

## 6. Evidence boundary

The new origin proof checks449089 complete sign entries:
four112200-entry phase cells and one289-entry radial corner. Replaying
the credited675-entry polar premise gives449764 total sign entries.
All calculations are exact rational arithmetic, with explicit exception
guards that persist under optimized Python. The manifest is mandatory;
ten corruptions are rejected in both replay modes.

The checker also reproduces288 signed Gaussian sector controls,
eight independent Fraction evaluations, the original-coordinate bridge,
both Gauss--Lucas identities, and an actual nonreal polynomial with
\(p'=9(z-(1+i)/40)^7(z-i/20)\), marked zero \(3/4\).
Its derivative, marked root, exact Rouché coefficient bound below one,
marked positive ordering, and both communication identities are checked.
The polynomial is an identity/control example, not a near-extremizer.

The geometric, AM-GM, Bernstein interpretation, classical communication
identities, dependency application and equality deductions remain
ordinary written proofs. Author cross-checks and publication are not
independent review. No solver, floating sign, private input or large
external corpus is required. Reproduction and measured costs are in
[README.md](README.md); attribution and complementary context are in
[LITERATURE.md](LITERATURE.md).
