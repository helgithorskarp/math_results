# Exact coalesced minimum of a degree-nine origin functional

Author **six-sendov-1**, role **researcher**, 2026-09-30.
Status: ordinary analytic proof with complete exact rational polynomial
verification of its constants. Independent review is pending.

## 1. The relaxed functional and its exact minimum

Let \(\varepsilon=1/16384\). Fix
\[
 1-\varepsilon\le a<1,\qquad r,s\ge1/2,\quad r+s\le2,
 \qquad |u|=|v|=1,\qquad \xi=\Re(ru+sv)/2\ge a.
\]
Set
\[
 m=(r+s)/2,\quad h=(r-s)/2,\quad q=h^2,\quad R=rs=m^2-q,
 \quad e=1-m,\quad c=|u+v|/2,\quad\gamma=1-c,
\]
\[
 O_a=9\int_0^1(1-atru)^4(1-atsv)^4dt,\qquad
 N_a=|O_a|^2/R^8.
\]
For \(w_a=a+i\sqrt{1-a^2}\), define
\[
 \mathcal M(a)=\left|{1-(1-aw_a)^9\over aw_a}\right|^2.
                                                               \tag{1}
\]
Conjugating \(w_a\) gives the same value. It is a rational polynomial
expression in the real parameter \(a\): with \(D=1-a^2\),
\[
 \mathcal M(a)={1-2\sum_{j=0}^4(-1)^j{9\choose2j}
                       a^{2j}D^{9-j}+D^9\over a^2}.             \tag{2}
\]

**Theorem.** On the entire displayed domain,
\[
 \boxed{N_a\ge\mathcal M(a)
             +{(3/2)q+16e+2\gamma\over a^2R^8}.}              \tag{3}
\]
The exact minimum of \(N_a\) is \(\mathcal M(a)\), and its only
minimizers are
\[
                  r=s=1,\qquad u=v=a\pm i\sqrt{1-a^2}.       \tag{4}
\]
Moreover
\[
 \mathcal M(a)\ge 3-2a+2(1-a)^2,                            \tag{5}
\]
and, writing \(\delta=1-a\), its sharp expansion is
\[
 \mathcal M(1-\delta)=1+2\delta+3\delta^2+4\delta^3
                         +5\delta^4-570\delta^5+O(\delta^6).  \tag{6}
\]
Thus common phase first changes the inverse-square reference at fifth
order. The fixed width of the collar is retained; changing that width
is not the new conclusion.

This is a minimum on an **abstract actual-mean domain**. No polar or
individual reciprocal-disk premise is imposed. In particular, (4) is
not claimed to be a feasible disk-root polynomial or a first-power
endpoint equality family. Since \(\mathcal M(a)>1\), it violates the
origin product constraint of such a polynomial. The preceding
[full-imbalance collar](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_imbalance_collar/PROOF.md)
already established the corresponding critical-multiplicity \(4+4\)
polynomial case. The new information is the exact functional minimum,
its quantitative radial/phase penalty, and the sharp fifth-order loss.
The unrestricted complex first-power conjecture is outside this theorem.

## 2. Mean-forced geometry and the retained skew

We restate the structural reduction credited to that preceding source.
The mean gives \(a\le m\le1\), \(0\le e\le\delta\),
\(|h|\le m-1/2\le1/2\), \(0\le q\le1/4\), and
\(1/2<R\le1\). The mean excludes \(u+v=0\), because then
\(\xi\le|h|<a\). Write
\[
 u=w(c+id),\quad v=w(c-id),\quad w=x+iy,\quad
 c>0,\quad c^2+d^2=x^2+y^2=1.
\]
Put \(\beta=hd\), \(B=\beta^2=q(1-c^2)\),
\(\lambda=-\beta y\), and \(\chi=1-x\). Then
\[
 \xi=mcx+\lambda,\qquad
 \lambda^2=q(1-c^2)(1-x^2).                                \tag{7}
\]
If \(x\le0\), \(\xi\le|h|<a\); hence \(x>0\).
Cauchy--Schwarz in the two unit pairs gives
\(\xi^2\le q+Rc^2\) and \(\xi^2\le q+Rx^2\). Therefore
\[
       0\le\gamma,\chi\le4\delta.                         \tag{8}
\]
The refined skew bound needed here is
\[
 |\lambda|\le2\sqrt{q\gamma\chi}
              \le\sqrt\chi(q+\gamma)
              \le2\sqrt\delta(q+\gamma).                  \tag{9}
\]
In addition, \(mc\le1\), \(x>0\), and (7) imply
\[
                  \chi\le\delta+\lambda
                       \le\delta+2\sqrt\delta(q+\gamma).  \tag{10}
\]
These estimates use the actual mean, not a substituted balanced mean.

For completeness, the exact affine-skew norm is as follows. Define
\(P_k,Q_k\in\mathbb Q[a,m,c,q]\) from even and odd powers of \(\beta\):
\[
 P_k+i\beta Q_k={9a^k\over k+1}
 \sum_{\substack{n_1+2n_2=k\\n_0+n_1+n_2=4}}
 {4!\over n_0!n_1!n_2!}(-2)^{n_1}(mc+i\beta)^{n_1}R^{n_2}.
                                                               \tag{11}
\]
Odd coefficients define \(Q_k\) without division by \(\beta\).
Using Chebyshev polynomials \(T_j,U_j\), the integral has the norm
\[
 |O_a|^2=E+\lambda J,
\]
\[
\begin{aligned}
 E&=\sum_k(P_k^2+BQ_k^2)
       +2\sum_{j>k}(P_jP_k+BQ_jQ_k)T_{j-k}(x),\\
 J&=2\sum_{j>k}(Q_jP_k-P_jQ_k)U_{j-k-1}(x).                 \tag{12}
\end{aligned}
\]
No sign is assigned to \(J\). Directly squaring the real and imaginary
integral components gives a second complete identity: if
\(A=\sum P_kT_k\), \(G=\sum Q_kT_k\),
\(L=\sum_{k\ge1}Q_kU_{k-1}\), \(H=\sum_{k\ge1}P_kU_{k-1}\), then
\[
 E=A^2+BG^2+(1-x^2)(H^2+BL^2),\qquad J=2AL-2GH.            \tag{13}
\]
The checker verifies (11) by direct fourfold convolution and compares
the whole polynomials in (12) and (13).

## 3. Separate the exact coalesced reference before estimating

Let \(\mathcal P=a^2E-R^8\), \(\mathcal J=a^2J\), and substitute
\(a=1-\delta,m=1-e,c=1-\gamma,x=1-\chi\), retaining \(q\).
At \(\delta=e=\gamma=\chi=0\), the positive radial polynomial is
\[
 \mathcal B(q)=I(q)^2-(1-q)^8,\qquad
 I(q)=1-q/7+3q^2/35-q^3/7+q^4.                             \tag{14}
\]
For \(0\le q\le1/4\),
\[
 I(q)-(1-q)^4=q[27/7-(207/35)q+(27/7)q^2]
                      \ge(333/140)q,
 \qquad I(q)\ge431/448>7/8.
\]
Thus \(\mathcal B(q)\ge2q\). This is a comparison at the exact
boundary corner, not radial monotonicity at arbitrary phases.

The part of \(\mathcal P\) having \(e=\gamma=q=0\) is the exact
coalesced tail \(F(\delta,\chi)\). If \(a=1-\delta\),
\(x=1-\chi\), and \(|w|=1,\Re w=x\), then
\[
 F(\delta,\chi)=a^2\left|{1-(1-aw)^9\over aw}\right|^2-1
      =-2\Re(1-aw)^9+|1-aw|^{18}.                         \tag{15}
\]
Equivalently, an independent complete polynomial expression is
\[
 F=-2\sum_{k=0}^9{9\choose k}(-a)^kT_k(x)
                                  +(1-2ax+a^2)^9.        \tag{16}
\]
All its monomials in \(\delta,\chi\) have total degree at least five;
its degree-five part is
\[
                         -288\delta\chi^4-288\chi^5.     \tag{17}
\]
The other linear terms of \(\mathcal P\) at \(q=0\) are
\(18e+(18/7)\gamma\); the \(\delta\) and \(\chi\) terms vanish.

Here is the complete coefficient grouping, including its precise
finite verification. For a shifted monomial \(z^\nu q^k\), set
\(z=(\delta,e,\gamma,\chi)\), \(d=|\nu|\),
\(W_\nu=4^{\nu_\gamma+\nu_\chi}\),
\(t_0=1/100\), and \(q_0=1/4\). Every monomial is assigned once:

1. \(d=0\) is \(\mathcal B(q)\).
2. \(d=1,k=0\) is \(18e+(18/7)\gamma\).
3. \(d\ge1,k\ge1\) contributes to
   \(M_q=\sum |p_{\nu,k}|W_\nu t_0^{d-1}q_0^{k-1}\).
4. \(d\ge2,k=0,\nu_e\ge1\) contributes to
   \(M_e=\sum |p_{\nu,0}|W_\nu t_0^{d-2}\).
5. \(d\ge2,k=0,\nu_e=0,\nu_\gamma\ge1\) contributes to
   \(M_\gamma=\sum |p_{\nu,0}|(W_\nu/4)t_0^{d-2}\).
6. The remaining terms form the complete \(F\) in (15).

Consequently the triangle inequality gives
\[
 |\mathcal P-\mathcal B-18e-(18/7)\gamma-F|
                  \le\delta(M_qq+M_ee+M_\gamma\gamma).    \tag{18}
\]
For the coefficients of \(\mathcal J\), define
\[
 L_q=\sum_{d=0,k\ge1}|j_{\nu,k}|q_0^{k-1},\qquad
 L_1=\sum_{d\ge1,k\ge0}|j_{\nu,k}|W_\nu t_0^{d-1}q_0^k.
\]
There is no constant skew term. The exact reconstructed sums satisfy
\[
 M_q<700,\quad M_e<150,\quad M_\gamma<30,
 \qquad L_q/4+L_1/16384<3.                                \tag{19}
\]
All sums appear as exact fractions in [expected.json](expected.json).
The full shifted \(\mathcal P,\mathcal J\) inventories have 32,559
and 17,338 nonzero entries. Every entry is regenerated; no sample or
floating bound supplies (18) or (19).

Since \(|\mathcal J|<3\), (9) and \(\sqrt\delta\le1/128\) give
\(|\lambda\mathcal J|\le(3/64)(q+\gamma)\). Using (14), (18), and (19),
\[
 a^2|O_a|^2-R^8-F
 \ge(2-700\delta-3/64)q+(18-150\delta)e
                       +(18/7-30\delta-3/64)\gamma
 \ge(19/10)q+17e+(5/2)\gamma.                             \tag{20}
\]
The signed term has been retained and bounded through its exact
geometric constraint. A generic \(O(\delta^2)\) bound would lose the
coalesced reference information needed below.

## 4. The common-phase minimum

Define the exact polynomial difference quotient
\[
 D_F(\delta,\chi)=
             {F(\delta,\chi)-F(\delta,\delta)\over\chi-\delta}.
                                                               \tag{21}
\]
This is a polynomial, also at \(\chi=\delta\). On a monomial
\(f_{ik}\delta^i\chi^k\), it is constructed by multiplying
\(f_{ik}\delta^i\) by
\(\sum_{j=0}^{k-1}\chi^{k-1-j}\delta^j\). The checker verifies the
entire divisibility identity, not a division at selected parameters.
It has 106 nonzero entries, all of degree at least four.

At \(\chi=\delta t\), its degree-four part is
\[
           -288\delta^4(2+2t+2t^2+2t^3+t^4).              \tag{22}
\]
Writing \(D_F=\sum d_{ik}\delta^i\chi^k\), three exact coefficient
sums provide all the estimates required here:
\[
\begin{aligned}
 S&=\sum_{i+k\ge5}|d_{ik}|t_0^{i+k-5}<85000,\\
 M&=\sum_{i+k\ge4}|d_{ik}|4^kt_0^{i+k-4}<190000,\\
 T&=\sum_{i+k\ge5}|f_{ik}|t_0^{i+k-5}<800.               \tag{23}
\end{aligned}
\]
If \(0\le\chi\le\delta\), put \(t=\chi/\delta\in[0,1]\).
Then (22)--(23) imply
\[
 D_F\le-576\delta^4+S\delta^5<-288\delta^4,
 \qquad F(\delta,\chi)\ge F(\delta,\delta),               \tag{24}
\]
with equality in the latter only when \(\chi=\delta\).
For \(\delta<\chi\le4\delta\), the complete quotient bound is
\(|D_F|\le190000\delta^4\). The mean constraint (10) therefore gives,
in both cases,
\[
 F(\delta,\chi)-F(\delta,\delta)
                   \ge-380000\delta^4\sqrt\delta(q+\gamma).
                                                               \tag{25}
\]
Also \(|F(\delta,\delta)|\le800\delta^5\).

Now \(1-R\le2e+q\), and \(0<R\le1\), so
\(1-R^8\le8(2e+q)\). Put \(F_*=F(\delta,\delta)\).
Equations (20) and (25) yield
\[
\begin{split}
 a^2|O_a|^2-R^8(1+F_*)
 \ge &(19/10)q+17e+(5/2)\gamma\\
 &-380000\delta^4\sqrt\delta(q+\gamma)
                         -6400\delta^5(q+2e).            \tag{26}
\end{split}
\]
The exact rational checks
\[
 380000\varepsilon^4/128<1/8,\qquad
                         12800\varepsilon^5<1/8
\]
show the total loss on the second line is at most
\((q+e+\gamma)/4\). Thus (26) is at least
\((3/2)q+16e+2\gamma\). Since \((1+F_*)/a^2=\mathcal M(a)\),
division by the positive \(a^2R^8\) proves (3).

Any nonzero \(q,e,\gamma\) gives strict inequality above the minimum.
If all are zero, \(r=s=1\) and \(u=v=w\); the mean gives
\(\chi\le\delta\). Equation (24) makes equality equivalent to
\(\chi=\delta\), or \(\Re w=a\). This proves the exact attainment
and uniqueness statement (4).

## 5. Sharp expansion and origin interpretation

Equations (15)--(17) give \(F_*=-576\delta^5+O(\delta^6)\).
Multiplying \(1+F_*\) by \((1-\delta)^{-2}\) proves (6).
Moreover \(a^{-2}\le2\) in the collar and
\(a^{-2}\ge1+2\delta+3\delta^2\); hence
\[
 \mathcal M(a)\ge a^{-2}-1600\delta^5
                       \ge1+2\delta+2\delta^2,
\]
because \(1600\varepsilon^3<1\). This proves (5).

The ordinary first origin identity for a disk-root polynomial with
critical reciprocals four copies each of \(ru,sv\) says
\(N_a=|\prod_{j=1}^8z_j|^2\le1\). The credited actual-mean lemma
obtains \(\xi>a\) from the polar identity under a hypothetical
first-power failure. Thus the same \(4+4\) polynomial collar already
excluded by the preceding source is excluded here with a sharper
functional margin. This is not an additional polynomial subclass, and
the quantitative polar mean lemma is not needed for the functional
minimum itself. The minimizers (4) satisfy \(N_a>1\), explaining their
infeasibility as disk-root polynomials.

## 6. An exact obstruction to extending this minimum to all radii

The mean-saturated coalesced profile does not minimize the functional
for every interior marked radius. At \(a=1/2,r=s=1,u=v=1\),
the actual mean is one and all radial budgets hold, but
\[
 N_a={261121\over65536}<{281827\over65536}=\mathcal M(1/2),
 \qquad \mathcal M(1/2)-N_a={10353\over32768}>0.             \tag{27}
\]
Indeed the real integral equals \(511/256\), whereas in (2) the real
ninth-power term vanishes at \(a=1/2\). Even the classical polar
functional at this real profile is
\[
 C_a(1,1)=\int_0^1(1/2+(3/4)t)^8dt={72319\over65536}>1.
\]
The critical point \(a-1=-1/2\) is in the unit disk. Thus adding the
polar and individual critical-disk premises would not remove this
particular obstruction to the global minimum formula. The origin
functional still exceeds one, and the weaker candidate \(3-2a=2\)
also holds here. This is not a counterexample to the joint polynomial
conditions or the first-power conjecture. It identifies a profile
change that any interior extension of the exact-minimum route must face.

## 7. Verification boundary

The standalone checker reconstructs all coefficient inventories from
the defining integral, checks all 18 real/odd integral component
polynomials by another convolution route, compares both full norm
polynomials, reverses both affine substitutions, and independently
reconstructs the full coalesced tail by (16). It verifies (21), the
reference (2), the complete coefficient grouping, and all readable
rounding and absorption inequalities. Exact Gaussian-rational controls
include both skew signs and attained minima; corrupted compact manifests
are rejected even with Python optimization enabled.

The ordinary arguments establishing the geometry, majorant applicability,
functional coverage, uniqueness, and polynomial interpretation remain
unformalized. Author code and its distinct algebraic routes do not
constitute independent review. No solver, floating mathematical input,
external corpus, or imported campaign module is required. See
[README.md](README.md) for exact commands and [LITERATURE.md](LITERATURE.md)
for the precise earlier/new boundary.
