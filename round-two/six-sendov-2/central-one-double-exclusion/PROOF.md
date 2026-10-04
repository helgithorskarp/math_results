# Central original-one-double angular exclusion

Actual author **six-sendov-2**, role **researcher**, 2026-10-04.
Ordinary computer-assisted author lemma, **unformalized and independently
unreviewed**. The new ingredients are the coupled cubic-decay feasibility
cap and complete central-chart positivity. Newton identities, Rolle,
compression/resolvents, Bezout determinants, Cauchy--Schwarz and Bernstein
positivity are classical. Historical priority is not claimed.

## 1. Statement and scope

Let \(x=(x_1,\ldots,x_8)\) be real, counting original multiplicities, with

\[
 \sum x_i=\sum x_i^3=\sum x_i^5=0,\qquad \sum x_i^2=1,
 \qquad D=\sum x_i^4-1/8>0.
\]

Suppose exactly one original level has multiplicity two and the six
remaining originals are simple and different from that level. Denote
the repeated level by \(a\), and set \(A=a^2\). Assume

\[
 0<D<1/24,\qquad 24(A-1/8)^2<D.                         \tag{1}
\]

Let \(P_0=I-ee^T\), \(e=(1,\ldots,1)/\sqrt8\), and let
\(T=P_0\operatorname{diag}(x)P_0\) act on \(e^\perp\).
For every distinct eigenvalue retain its **full eigenspace mass**
\(m_\lambda=\|\Pi_\lambda x\|^2\), including zero-mass eigenspaces.
Put \(\eta=\sum_\lambda m_\lambda^2\) and \(C=(1-\eta)/D\).
These are the credited [7432 angular definitions](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md).

**Theorem.** Every such actual original profile satisfies \(C<47/2\).

Condition (1) is a sufficient central chart. This theorem does not prove
that every high-value one-double profile satisfies (1). Other collision
patterns and the nonlinear complex degree-nine first-power problem retain
their separate obligations. The generic original-collision chart is prior
[10136](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/collision-moment-reduction/PROOF.md);
the result here resolves the sign on the stated entire central chart,
rather than on fixed fibres or at sampled roots.

## 2. Entire original polynomial and exact feasible fibre

Reflect all originals if necessary so \(a>0\); (1) excludes \(a=0\).
Reflection preserves all assumptions and the full-mass angular value.
Set

\[
 E=3/64-D/8,\quad s=A-1/8,\quad d=D/4-6s^2,
\]
\[
 q_0(t)=t^2+(2A-1/2)t+3A^2-A+2E,
 \quad k_0(t)=t^2+(A-3/8)t+A^2-3A/8+E.
\]

The original monic octic, after imposing its double at \(a\), is

\[
\begin{split}
 Q_u(z)&=(z+a)^2q_0(z^2)+4u,\\
 H_u(z)&=z(z+a)k_0(z^2)+u,\\
 f_u(z)&=(z-a)^2Q_u(z)
       =(z^2-A)^2q_0(z^2)+4u(z-a)^2,\\
 f_u'(z)&=8(z-a)H_u(z).                              \tag{2}
\end{split}
\]

There is no extra restriction in (2) on the generic double-root chart:
Newton identities first give
\(f=z^8-z^6/2+2Ez^4+4Gz^2+8Jz+c\). The conditions
\(f(a)=f'(a)=0\) determine \(J,c\); division gives (2) with
\(u=G-[-A^3+3A^2/8-EA]\). Both computations regenerate the
complete original moments from (2), not from a root sample.

From (1), \(1/12<A<1/6\) and \(d>0\). The identities

\[
 \operatorname{disc}(q_0)=D-8s^2>0,\quad q_0(A)=-d<0,
 \quad q_0(0)=3(A-1/6)^2+1/96-D/4>0
\]

and the positive root sum \(1/2-2A\) show that \(q_0\) has two
positive simple roots \(t_-<A<t_+\). Write \(r_\pm=\sqrt{t_\pm}\).
The ordered roots of \(Q_0\) are

\[
 -r_+,\quad -a\text{ (double)},\quad -r_-,\quad r_-,\quad r_+.
\]

Rolle supplies four intervening derivative roots and the fifth at
\(-a\). All five are simple by degree count;
\(Q_0''(-a)=2q_0(A)<0\). In increasing order call them
\(\gamma_1,\ldots,\gamma_5\), with \(\gamma_2=-a\).
The first, third and fifth are strict negative minima; the second is
a zero maximum and the fourth a positive maximum. They are fixed as
\(u\) varies. Therefore the **entire sextic** \(Q_u\) has six simple
real roots exactly when

\[
 0<u<u_*:=\tfrac14\min\{-Q_0(\gamma_1),
                         -Q_0(\gamma_3),-Q_0(\gamma_5)\}.       \tag{3}
\]

Necessity is the alternating-extremum sign condition for a real-rooted
monic sextic. For sufficiency, those strict signs give one root in each
of the six intervals, including the unbounded ones. Neither a real
critical spectrum alone nor the later cap alone is an original-feasibility
certificate.

## 3. Coupled root-gap cap with cubic boundary decay

Choose the closer \(q_0\)-root to \(A\): use \(t_+\) when \(s\ge0\),
and \(t_-\) otherwise. With \(h=|s|\), its distance \(b>0\) obeys
\(b^2+4hb=d\). On the corresponding negative-\(z\) interval between
\(-a\) and \(-\sqrt{t_{\rm closer}}\), put \(x=|z^2-A|\in(0,b)\).
Then

\[
 q_0(z^2)=-d+4hx+x^2<0,\quad
 -Q_0(z)=\frac{x^2(d-4hx-x^2)}{(\sqrt{z^2}+a)^2}.          \tag{4}
\]

This interval contains one of \(\gamma_1,\gamma_3\), so its depth
bounds \(4u_*\) from above. The following estimate keeps the two
competing root-gap constraints coupled:

\[
 x^2(d-4hx-x^2)\le \frac{d^3}{4(d+16h^2)}.              \tag{5}
\]

Indeed let \(y=x^2/d\), \(k=4hx/d\), \(g=1-y-k>0\).
Then \(0\le k<1\), \((y+k^2)+g=1-k+k^2\le1\), and
\(4(y+k^2)g\le[(y+k^2)+g]^2\le1\).
Since \(y+k^2=(d+16h^2)x^2/d^2\), this is (5).
The exact gaps are

\[
 (1-k+k^2)^2-4(y+k^2)(1-y-k)=[y+k^2-(1-y-k)]^2,
\]
\[
 1-(1-k+k^2)^2=k(1-k)(2-k+k^2)\ge0.                     \tag{6}
\]

Every central interval in (4) has denominator strictly larger than
\(A\). Thus throughout (1),

\[
 0<u_*<\frac{d^3}{16A(d+16s^2)}\le\frac{d^2}{16A}<Ad.   \tag{7}
\]

The last inequality follows from \(d<1/96<16A^2\).
For \(s\ge0\), the selected interval has \(z^2>A\), so its denominator
is strictly larger than \(4A\). For \(s<0\) and \(D<1/25\),

\[
 t_-=1/8+|s|-\sqrt{D/4-2s^2}
     \ge1/8-\sqrt{D/4}>1/40>A/5.
\]

Thus its denominator exceeds
\(A(1+1/\sqrt5)^2>2A\). The two stronger licensed caps are

\[
 u_*<\frac{d^3}{\kappa A(d+16s^2)},\qquad
 \kappa=\begin{cases}32,&s<0,\ D<1/25,\\64,&s\ge0.\end{cases}       \tag{8}
\]

All strictness comes from the open interval in (4); (5) itself need
not be strict. No optimality of these constants is claimed.
In particular \(Q_u(0)>0\) and \(Q_u(a)=4(u-Ad)<0\) on (3),
so no single original reaches zero or the repeated original. Initially
the double \(-a\) splits into two negative singles; the other four
simple roots retain their signs. Connectedness of (3) then gives four
negative and two positive singles throughout, besides the positive double.
This pays exact one-double reality, separation and all sign counts.

## 4. Full spectral masses and the entire high-value polynomial

By actual Rolle/interlacing, \(H_u\) has six distinct real roots
\(\sigma_i\), one in each gap between the seven distinct original levels.
No \(\sigma_i\) equals an original level. The inactive critical node
\(a\) is retained: its supported zero-sum eigenspace has mass zero.
The Schur resolvent of the original diagonal matrix gives

\[
 x^T(z-T)^{-1}x
 =8\left(z-\frac{f_u(z)}{f_u'(z)/8}\right)
 =8\left(z-\frac{(z-a)Q_u(z)}{H_u(z)}\right).
\]

Put
\(r(z)=8zH_u(z)-8(z-a)Q_u(z)\). It has degree five and leading
coefficient one. All six active **full** masses are positive and satisfy

\[
 m_i=r(\sigma_i)/H_u'(\sigma_i)
    =-8(\sigma_i-a)Q_u(\sigma_i)/H_u'(\sigma_i),
 \qquad \sum_i m_i=1.                                 \tag{9}
\]

The last identity is either the coefficient at infinity of the
resolvent or its norm-one spectral interpretation. No zero-mass dimension
is split into a fictitious positive mass.

For monic degree-six \(H=H_u\), define the Bezout matrix by

\[
 \frac{H(X)g(Y)-H(Y)g(X)}{X-Y}
      =\sum_{i,j=0}^5 B(H,g)_{ij}X^iY^j.
\]

Evaluation at the six distinct \(\sigma_i\) diagonalizes this form:
\(VB(H,g)V^T=\operatorname{diag}[H'(\sigma_i)g(\sigma_i)]\).
Consequently, with \(\Delta=\det B(H,H')=\operatorname{disc}(H)>0\),

\[
 \det B(H,H'+w r)=\Delta\prod_{i=1}^6(1+w m_i).
\]

Let \(N\) be its coefficient of \(w^2\). Retaining the whole first
three determinant coefficients is exact for \(\Delta,N\); no
\(A,D,u\) parameter series is truncated. The coefficient of \(w\)
is exactly \(\Delta\), and

\[
 N=\Delta(1-\eta)/2,\quad C=2N/(D\Delta),\quad
 P:=47D\Delta-4N,\quad C\ge47/2\ \Longleftrightarrow\ P\le0.       \tag{10}
\]

Reflection parity is checked in every coefficient before replacing
\(a^2\) by \(A\). The entire maps \(\Delta,N,P\in\mathbb Q[A,D,u]\)
have \(u\)-degree five and respectively 166, 227 and 228 nonzero terms.
The programs regenerate them directly from (2) and (9).

## 5. Complete rational positivity certificate on the necessary band

It suffices for now to treat

\[
 1/729<D\le5/141.                                     \tag{11}
\]

Write \(q=\sqrt{D/24}>0\), \(t=s/q\in(-1,1)\).
Then

\[
 A=1/8+qt,\quad D=24q^2,\quad d=6q^2(1-t^2),
 \ell=d+16s^2=2q^2(3+5t^2).
\]

By (8), every actual point in (11) has
\(u=v d^3/(\kappa A\ell)\) with \(0<v<1\), choosing \(\kappa\)
according to the sign of \(t\). All cleared denominators are positive.
The exact whole-polynomial identity is

\[
 (\kappa A\ell)^5 P\left(A,D,\frac{vd^3}{\kappa A\ell}\right)
      =q^{20}(1-t^2)^2 S_\kappa(q,t,v).                \tag{12}
\]

The factor on the right is strictly positive on the actual open central
chart. The reduced polynomial \(S_\kappa\) has degrees \((12,28,5)\).
The rational enclosure and its one split are

\[
 q\in[1/133,1/26],\qquad q_{\rm mid}=159/6916,
\]

because \((1/133)^2<1/17496\), \((1/26)^2>5/3384\).
Moreover \(24(1/26)^2=6/169<1/25\), so the negative-side
root-distance license remains valid on this enlarged box.
Use these three closed boxes, each with \(v\in[0,1]\):

| box | \(\kappa\) | \(q\) | \(t\) | full Bernstein entries | minimum coefficient |
|---|---:|---|---|---:|---|
| negative | 32 | \([1/133,1/26]\) | \([-1,0]\) | 2262 | \(7885466452528416/815730721\) |
| positive-left | 64 | \([1/133,159/6916]\) | \([0,1]\) | 2262 | \(330815919331712900214563879677199616/559059441355907035400747527\) |
| positive-right | 64 | \([159/6916,1/26]\) | \([0,1]\) | 2262 | \(240063645295309059778608/815432979286835\) |

On each box make the indicated affine changes in \(q,t\) to unit
coordinates and expand in the tensor Bernstein basis of degrees
\((12,28,5)\). For a univariate monomial polynomial \(\sum p_i X^i\),
the complete conversion and its complete inverse are

\[
 b_k=\sum_{i\le k}p_i\frac{\binom{k}{i}}{\binom ni},\qquad
 p_i=\binom ni\sum_{k\le i}(-1)^{i-k}\binom ik b_k.      \tag{13}
\]

Apply (13) successively in all three coordinates. **Every** one of the
6,786 coefficients is strictly positive; reverse reconstruction reproduces
every coefficient of every whole affine polynomial, not merely its hash
or a selection of sample values. A tensor Bernstein basis is nonnegative
and sums to one, so \(S_\kappa>0\) on all three closed boxes.
Equation (12), with its strictly positive actual factor and denominators,
then gives \(P>0\), hence \(C<47/2\) throughout (11).
Closed-box positivity at \(t=\pm1\) is only a polynomial certificate;
division by \((1-t^2)^2\) in (12) is interpreted solely at actual
\(|t|<1\). No physical profile is inferred from a cap-box point.

## 6. Paying both remaining D ranges

For \(0<D\le1/729\), the already published, complete all-multiplicity
odd-moment-zero collar [LEMMA10290](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/near-balanced-angular-collar/PROOF.md)
gives

\[
 C<\frac{16}{1-8\sqrt D}+390625D^2
 \le\frac{237004387}{10097379}<47/2.
\]

Its hypotheses are exactly the original moment assumptions here; it
needs no central-chart coverage or attainment premise. For \(D>5/141\),
the six positive masses in (9) satisfy
\(\eta\ge1/6\) by Cauchy--Schwarz, whence

\[
 C\le5/(6D)<47/2.
\]

The equality endpoint \(D=5/141\) belongs to the strict tensor certificate,
and \(D=1/729\) belongs to the strict collar. These cases cover the
whole range (1) and prove the theorem. No reviewer verdict on a parent
is transported to this new child.

## 7. Reproducibility and remaining frontier

[verify.py](verify.py) uses standard-library integer/Fraction arithmetic,
original polynomial differentiation and moments, complete Bezout entries,
and an integer-cleared **Berkowitz principal-block characteristic
recurrence**. It expands the cap by independent binomial formulas and
subdivides the positive box with exact de Casteljau. It checks all
original identities, whole factor removal and whole reverse tensors.

[compare_cas.py](compare_cas.py) uses SymPy1.14.0 exact polynomial rings,
symbolic derivative division, a **subset determinant dynamic program**,
exact polynomial composition/division, and direct affine construction of
each of the three boxes. It imports no native mathematical engine,
reviewer code, old expected polynomial map or private coefficient corpus.
The only shared module [record_io.py](record_io.py) serializes exact
coefficients and checks final complete coverage/strictness. Both methods
produce identical **whole** mathematical records, including every
matrix entry, determinant coefficient, cap term, box term and tensor
coefficient. This is different same-author validation, not independent
peer review or formal verification.

The complete transient record is 1,609,517 bytes, SHA256
`d72afbbe7b6a4e89abcde57a8d5d919b864abb0a0456b205dd668f1238de6ec1`.
It is regenerated locally and deliberately omitted from source.
[EXPECTED.json](EXPECTED.json) stores the compact complete-record hash,
three minima and counts. A hash/minimum table alone is not the proof:
the supplied source regenerates and verifies every coefficient.
See [README.md](README.md) for exact commands and [VALIDATION.json](VALIDATION.json)
for resource and replay evidence.

Ordinary bridges outside a proof assistant remain: the normalized
original chart, strict real-root extrema and Rolle/interlacing,
compression/full-mass resolvent interpretation, the cap inequalities,
Bernstein partition of unity, and the cited collar. The finite source
computation supplies all of (12)--(13), not those surrounding bridges.

The original reality interval and positivity/stationarity licenses on the
remaining one-double branch must be established separately. The theorem
does not assert that this complement is empty or solve other collision
strata or arbitrary complex first-power paths. Current primary problem
context is documented in [LITERATURE.md](LITERATURE.md).

## 8. Strict outer-branch reduction for the remaining frontier

There is an additional ordinary structural consequence which does not
use any sampled polynomial values. For **any** actual generic one-double
chart (2), without (1), its six simple real \(Q_u\)-roots imply that
\(Q_u'\) has five distinct simple real roots. One is always \(-a\), and

\[
 Q_u'(-a)=0,\qquad Q_u''(-a)=2q_0(A)=-2d,\qquad Q_u(-a)=4u.       \tag{14}
\]

Therefore \(d\ne0\): otherwise \(-a\) would be a multiple derivative
root, contradicting the five distinct Rolle roots and the degree count.
If \(d>0\), the node \(-a\) is a strict local maximum of a real-rooted
monic sextic with simple roots, so its value is positive and \(u>0\).
If \(d<0\), it is a strict local minimum, so its value is negative and
\(u<0\). These alternating signs follow directly from the ordered six
simple roots. Thus **\(du>0\)** everywhere on the actual one-double
stratum; the equality boundary \(d=0\) is never an actual exact
one-double profile. No assumption on the reality of \(q_0\)'s roots is
needed for this last argument. The identities also hold at \(a=0\).

Combining the six-full-mass bound, the cited10290 collar, the theorem
above and (14) gives the precise necessary alternative:

**Corollary.** An actual normalized odd-moment-zero profile with exactly
one original double and \(C\ge47/2\), if one exists, must satisfy

\[
 1/729<D\le5/141,\qquad 24(A-1/8)^2>D,\qquad d<0,\qquad u<0.       \tag{15}
\]

Indeed the D band implies \(D<1/24\); the central theorem excludes
\(d>0\), and (14) excludes \(d=0\). This pays the outer branch's
perturbation sign and removes its equality boundary, while preserving
the essential remaining licenses: all six original \(Q_u\)-roots
simple and real, separation from \(a\), actual \(\Delta>0\), and
\(P\le0\). Its feasibility interval and eventual exclusion are open.
The sign reduction is an ordinary written bridge, rather than an
additional assertion that the finite Bernstein boxes cover the outer
branch. No universal angular or global FIRST conclusion follows.
