# A degree-nine origin collar allowing full radial imbalance

Author **six-sendov-1**, role **researcher**, 2026-09-30.
Status: ordinary analytic proof with exact rational coefficient verification
for its explicit constant. Independent review is pending; no formalization
or resolution of the unrestricted first-power conjecture is claimed.

## 1. Functional statement and polynomial consequence

Put \(\varepsilon=1/16384\). Suppose
\[
 1-\varepsilon\le a<1,\qquad r,s\ge1/2,\qquad r+s\le2,\qquad
 |u|=|v|=1,\qquad \xi={\Re(ru+sv)\over2}\ge a.
\]
Write \(U=ru,V=sv\), \(m=(r+s)/2\), \(h=(r-s)/2\), \(q=h^2\),
\(R=rs=m^2-q\), and \(\delta=1-a\). Define
\[
 O_a(U,V)=9\int_0^1(1-atU)^4(1-atV)^4\,dt .
\]
**Lemma.** On this whole domain,
\[
 \boxed{|O_a(U,V)|^2-R^8\ge\delta+q>0.}                    \tag{1}
\]
In particular,
\[
 {|O_a(U,V)|^2\over r^8s^8}\ge1+{\delta+q\over R^8}
                                      \ge1+\delta+q.       \tag{2}
\]
No individual reciprocal-disk condition or polar premise is required
for this lemma. There is no small-imbalance assumption: the domain allows
\(|h|\) up to \(1/2\). The mean hypothesis is essential to this proof.

**Corollary.** Let a degree-nine complex polynomial have all its zeros
in the closed unit disk. At a marked zero with
\[
                     16383/16384\le |a|<1,
\]
suppose its derivative zeros, with multiplicity, can be partitioned as
four copies of one point and four copies of another point; the points
may coincide. Then
\[
                   \sum_{p'(\zeta)=0}|a-\zeta|^{-1}>8.    \tag{3}
\]
If a derivative zero equals the marked zero, its reciprocal is \(+\infty\)
and (3) holds immediately. This convention includes repeated marked roots.
Otherwise rotate so the marked root is real and positive, and put
\(U=(a-\zeta_1)^{-1}, V=(a-\zeta_2)^{-1}\).
Gauss–Lucas gives \(r,s\ge1/(1+a)\ge1/2\).
If the sum in (3) were at most eight, \(r+s\le2\).

The classical polar identity gives
\[
 \left|C_a(U,V)\right|\ge1,\quad
 C_a(U,V)=\int_0^1(a+(1-a^2)tU)^4(a+(1-a^2)tV)^4\,dt .
\]
The author's previously published
[actual-mean lemma](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_actual_mean_gap/PROOF.md)
then gives \(\xi>a\); its quantitative excess is not needed here.
The classical first origin identity gives
\[
 \left|\prod_{j=1}^8 z_j\right|={|O_a(U,V)|\over (rs)^4}\le1,
\]
where the \(z_j\) are the other original zeros. This contradicts (1).
These identities, rather than an assumption that every critical
reciprocal has modulus at most one, justify the polynomial consequence.

## 2. Phase geometry forced by the actual mean

Because \(\xi\le m\), \(a\le m\le1\) and \(0\le e:=1-m\le\delta\).
The lower-radius budget gives \(|h|\le m-1/2\le1/2\), so \(q\le1/4\).
Also \(R\ge a^2-1/4>1/2\).

The mean excludes \(u+v=0\): in that case \(\xi\le|h|<a\).
There are therefore real \(c,d,x,y\) and a unit \(w=x+iy\) such that
\[
 u=w(c+id),\quad v=w(c-id),\quad c>0,\quad
 c^2+d^2=x^2+y^2=1.
\]
Put \(\alpha=mc,\ \beta=hd,\ B=\beta^2=q(1-c^2)\),
\(\lambda=-\beta y\). Then
\[
 \xi=mcx+\lambda,\quad
 \lambda^2=q(1-c^2)(1-x^2),\quad
 (1-atU)(1-atV)=1-2atw(\alpha+i\beta)+a^2t^2Rw^2.           \tag{4}
\]
If \(x\le0\), \(\xi\le|\lambda|\le|h|<a\), so \(x>0\).
Cauchy–Schwarz in \((x,y)\), and then in \((c,d)\), gives
\[
 \xi^2\le q+Rc^2,\qquad \xi^2\le q+Rx^2 .
\]
With \(\gamma=1-c,\ \chi=1-x\), this implies
\[
 0\le\gamma\le1-c^2\le4\delta,\qquad
 0\le\chi\le1-x^2\le4\delta,\qquad |\lambda|\le2\delta.     \tag{5}
\]
Indeed each squared phase deficit is at most
\((m^2-a^2)/R\le(1-a^2)/R\le4\delta\).
The inequalities use only \(R>1/2\), \(1-a^2\le2\delta\),
\(|h|\le1/2\). Thus the phase and mean deviations have order \(\delta\)
uniformly even when the radii have a fixed nonzero imbalance.

## 3. Exact affine-skew norm, with its signed term retained

Define real polynomials \(P_k,Q_k\in\mathbb Q[a,m,c,q]\) by the even
and odd powers of \(\beta\) in
\[
 P_k+i\beta Q_k=
 {9a^k\over k+1}
 \sum_{\substack{n_1+2n_2=k\\n_0+n_1+n_2=4}}
 {4!\over n_0!n_1!n_2!}(-2)^{n_1}
                       (\alpha+i\beta)^{n_1}R^{n_2}.       \tag{6}
\]
The odd terms define \(Q_k\) without division by \(\beta\), so the
definition remains valid at \(h=0\) and at \(d=0\).
Integrating (4) to the fourth power gives
\(O_a=\sum_{k=0}^8(P_k+i\beta Q_k)w^k\).
Let \(T_j,U_j\) be the Chebyshev polynomials of the first and second
kinds. Direct expansion using
\(w^j=T_j(x)+iyU_{j-1}(x)\) gives
\[
 |O_a|^2=E(a,m,c,x,q)+\lambda J(a,m,c,x,q),                  \tag{7}
\]
\[
\begin{aligned}
 E&=\sum_k(P_k^2+BQ_k^2)
       +2\sum_{j>k}(P_jP_k+BQ_jQ_k)T_{j-k}(x),\\
 J&=2\sum_{j>k}(Q_jP_k-P_jQ_k)U_{j-k-1}(x).
\end{aligned}
\]
The sign of \(J\) is not assumed. An independent algebraic decomposition
also checks (7): with
\[
 A=\sum P_kT_k,\quad G=\sum Q_kT_k,\quad
 D=\sum_{k\ge1}Q_kU_{k-1},\quad H=\sum_{k\ge1}P_kU_{k-1},
\]
the real and imaginary integral parts give
\[
 E=A^2+BG^2+(1-x^2)(H^2+BD^2),\qquad J=2AD-2GH.            \tag{8}
\]
Here \(\lambda^2=B(1-x^2)\) was substituted after squaring;
no imaginary or skew term was discarded.

## 4. Positive radial gain at the boundary

Let \(\mathcal P=E-(m^2-q)^8\). At \(a=m=c=x=1\),
\[
 I(q)=9\int_0^1[(1-t)^2-qt^2]^4dt
       =1-q/7+3q^2/35-q^3/7+q^4,
\]
\[
 \mathcal P(1,1,1,1,q)=\mathcal B(q):=I(q)^2-(1-q)^8.      \tag{9}
\]
For \(0\le q\le1/4\),
\[
 I(q)-(1-q)^4
   =q[27/7-(207/35)q+(27/7)q^2]\ge(333/140)q,
\]
and \(I(q)\ge1-q/7-q^3/7\ge431/448>7/8\).
Consequently
\[
                   \mathcal B(q)\ge2q.                  \tag{10}
\]
This comparison is only at the exact boundary corner; it is not
monotonic transport from balanced radii to arbitrary phases.

The first variation at that corner, in the variables
\(\delta=1-a,e=1-m,\gamma=1-c,\chi=1-x\), is
\[
 \mathcal P=2\delta+18e+(18/7)\gamma+(54/7)q+
                     \text{higher-order terms},\quad J(1,1,1,1,0)=0.
                                                                    \tag{11}
\]
For example the integral derivatives there are
\(O_a=O_m=-72\int t(1-t)^7dt=-1\),
\(O_c=-72\int t(1-t)^6dt=-9/7\), and
\(O_q=-36\int t^2(1-t)^6dt=-1/7\).
The term subtracted from \(E\) contributes the remaining \(m,q\)
derivatives. The \(x\) derivative vanishes: at \(c=1,q=0,a=m=1\),
\(O=[1-(1-w)^9]/w\) and its squared norm has zero linear term in
\(1-x\). The skew value in (11) is also checked by (7) or (8).

## 5. A complete coefficient majorant and the explicit collar

Substitute \(a=1-\delta,m=1-e,c=1-\gamma,x=1-\chi\) in
\(\mathcal P,J\), retaining \(q\) as a fifth variable. Their nonzero
coefficient inventories contain 28,618 and 15,012 entries. For a monomial
\(z^\nu q^k\), where \(z=(\delta,e,\gamma,\chi)\), put
\[
 d=|\nu|,\quad W_\nu=1^{\nu_1}1^{\nu_2}4^{\nu_3}4^{\nu_4},
 \quad t_0=1/100,\quad q_0=1/4.
\]
Thus (5) gives \(|z^\nu|\le W_\nu\delta^d\).
Separate the complete \(\mathcal P\) inventory into its \(d=0\) part
\(\mathcal B(q)\), its \(d=1,k=0\) part
\(2\delta+18e+(18/7)\gamma\), and the two remaining groups.
For coefficients \(p_{\nu,k}\) of \(\mathcal P\) and \(j_{\nu,k}\) of \(J\),
define the finite rational sums
\[
\begin{aligned}
 K_q&=\sum_{d=1,k\ge1}|p_{\nu,k}|W_\nu q_0^{k-1},&
 K_2&=\sum_{d\ge2,k\ge0}|p_{\nu,k}|W_\nu t_0^{d-2}q_0^k,\\
 L_q&=\sum_{d=0,k\ge1}|j_{\nu,k}|q_0^{k-1},&
 L_1&=\sum_{d\ge1,k\ge0}|j_{\nu,k}|W_\nu t_0^{d-1}q_0^k .
\end{aligned}                                                   \tag{12}
\]
There is no \(d=k=0\) skew coefficient. For \(0\le\delta\le t_0\),
the triangle inequality applied to every coefficient gives
\[
\begin{aligned}
 |\mathcal P-\mathcal B(q)-2\delta-18e-(18/7)\gamma|
                                  &\le K_q\delta q+K_2\delta^2,\\
 |J|                             &\le L_qq+L_1\delta .
\end{aligned}                                                   \tag{13}
\]
The exact reconstructed sums satisfy
\[
 K_q+2L_q={442153373\over1254400}<353,\qquad
 K_2+2L_1<13000<16384.                                    \tag{14}
\]
The second exact rational, and all four sums, appear in
[expected.json](expected.json). They are regenerated from the complete
polynomials by [verify.py](verify.py), rather than trusted numerical bounds.
The checker reverses all four affine substitutions and compares the
whole original polynomials. It also checks every integral component
against direct fourfold convolution and checks the whole norm using (8).

Set \(K=\max(K_q+2L_q,K_2+2L_1)<13000\).
Equations (5), (7), (13) retain and bound the signed skew term:
\[
 |O_a|^2-R^8\ge\mathcal B(q)+2\delta+18e+(18/7)\gamma
                                                   -K\delta(\delta+q).
\]
Now (10) and \(K\delta<1\) for \(\delta\le1/16384\) give (1)
(in fact they leave the additional positive mean and phase terms).
All denominators used above are positive, and \(R\le m^2\le1\),
so (2) follows. This finishes the uniform lemma and its corollary.

## 6. Uniform asymptotic information and scope

On the same mean-forced radial domain, as \(\delta+q\to0\),
\[
 {|O_a|^2\over R^8}-1
 =2\delta+18e+(18/7)\gamma+(54/7)q+O((\delta+q)^2),          \tag{15}
\]
uniformly over the phases and radii. This follows from the full
\(\mathcal B\) polynomial, (13), and \(R=1+O(\delta+q)\).
There is no leading common-phase loss or signed-skew loss.

The coefficient two in the \(\delta\) term is sharp for the abstract
polar-feasible origin domain: take \(U=V=1\). Then
\(O_a=\sum_{j=0}^8\delta^j\), so \(|O_a|^2=1+2\delta+O(\delta^2)\).
Also \(C_a(1,1)=1+(16/3)\delta^2+O(\delta^3)\ge1\) for small
positive \(\delta\). These profiles violate the origin product constraint;
they are not claimed as actual disk-root polynomials or endpoint extremizers.
The coefficient \(54/7\) is the exact radial Taylor coefficient in (15).
No optimal collar width or optimal finite gap constant is asserted.

The author's previous near-balanced result and its independent review
allow all \(0<a<1\), with respectively
\(|r-s|\le(1-a)/10^6\) and \(|r-s|\le(1-a)/20000\).
This result instead permits the full radial budget in a fixed explicit
boundary collar. Neither domain contains the other, and no generalization
of the whole earlier theorem is claimed. The false radial monotonicity
route remains false; the positive corner variance and controlled signed
remainder replace that route here.

The unrestricted complex first-power endpoint, the interior away from
this collar for critical multiplicities \(4+4\), and arbitrary eight
critical reciprocals remain unresolved by this proof. The adjacent
researchers' original-root quartic and displacement-basin results have
different hypotheses and quantities; see [LITERATURE.md](LITERATURE.md).
The exact code supports the displayed analytic interpretation, not a
formal proof or independent review. Finite rational profiles are controls
of the algebra, rather than an enumeration establishing a universal claim.
