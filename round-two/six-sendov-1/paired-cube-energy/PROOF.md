# Actual paired-cube weights contract the degree-nine critical energy

Actual author **six-sendov-1**, role **researcher**, 2026-10-02.
Complete ordinary analytic author proof, **unformalized and independently
unreviewed**. Finite exact checks corroborate the stated algebra and constants;
they do not formalize the analytic or norm arguments. Shared signing identity
does not establish distinct authorship or independent review.

## Statement and remaining frontier

Let \(0<\eta\le e=2^{-16}\), \(a=1-\eta\), and
\[
 p(z)=z^9+\sum_{k=0}^8c_kz^k,\qquad p(a)=0,
\]
with all nine original zeros in the closed unit disk. All original zeros
and all eight critical points \(\zeta_j\) are counted with multiplicity.
Assume the explicit critical collar
\[
                  \max_j|\zeta_j|\le R=1/25.                    \tag{1}
\]
Define \(F=\sum_j|a-\zeta_j|^{-1}\) and \(H=\sum_j|\zeta_j|^2\).
Then
\[
                  F\le8+3\eta\quad\Longrightarrow\quad
                  H<25\eta.                                 \tag{2}
\]
No coefficient caps, conjugation, separated roots, critical branch matching,
optimizer, attainment, or all-competitor concentration premise is assumed.
Boundary and colliding original roots, and arbitrary critical collisions,
are included. Here \(a>R\), so all reciprocal denominators are nonzero.

Combining (2) with [9588](../low-energy-entry/PROOF.md) gives, on this
low sublevel, every \(|c_1|,\ldots,|c_8|<31\eta/4<8\eta\).
The expressly imported same-cap8 enhancement
[9572](../../six-reviewer-1/physical-chamber-audit/REVIEW.md) then gives
\[
             \max_j|\zeta_j|\le1/25\quad\Longrightarrow\quad
             F>8+(9/4)\eta.                                  \tag{3}
\]
If \(F>8+3\eta\), (3) is immediate; otherwise entry has just been proved.
The cap8 theorem [9533](../../six-sendov-3/coefficient-chamber/PROOF.md)
and its review retain their own hypotheses and credit. They are used only
AFTER entry and give no review verdict on this new result.

Thus every remaining actual outside-cap8 competitor with \(F\le8+3\eta\)
has both \(H>30\eta\) by9588 and \(\max_j|\zeta_j|>1/25\) by (2).
The unrestricted complex first-power endpoint and global concentration remain
open. The explicit collar (1) is a hypothesis, not a universal conclusion.

## Cap-free reciprocal and coefficient estimates

Write \(x=|c_8|\), \(y=|c_7|\), \(A=\Re c_8\), \(B=\Re c_7\),
\(S=A+B\), \(L=\sum_{k=1}^6|c_k|\), and \(U=\sum_j\zeta_j=-8c_8/9\).
Vieta, Cauchy and Maclaurin for nonnegative numbers give
\[
 |c_k|\le\frac9k\binom8{9-k}(H/8)^{(9-k)/2}\quad(1\le k\le8).
                                                                  \tag{4}
\]
Consequently \(H\le h=8R^2=8/625\), \(x\le9R\), and
\[
 |c_k|\le b_kH\quad(1\le k\le7),\qquad
 b_k=\frac9{8k}\binom8{9-k}R^{7-k},\quad
 \ell=\sum_{k=1}^6b_k.                                        \tag{5}
\]
In particular \(y\le(9/2)H\) and \(L\le\ell H\).
Newton gives \(T_2:=\sum\zeta_j^2=U^2-14c_7/9\) and hence
\[
                  y\le\frac9{14}H+\frac{32}{63}x^2.             \tag{6}
\]

Since \(a>24/25\), every \(|\zeta_j/a|<1/24\). The GENERAL cap-free
square-tail envelope of [9492](../coefficient-chamber-sharp/PROOF.md)
therefore gives, with \(\kappa=1/4-5/(4\cdot24)=19/96\),
\[
 a^3F\ge8a^2-\frac{8a}{9}A-\frac76B+\frac34\Re U^2+\kappa H.
                                                                  \tag{7}
\]
This imports only its analytic envelope, not any cap2 root circle,
coefficient bootstrap, sharp family, or optimizer claim. For clarity its
ordinary proof uses \(G(t)=(1-t)^{-1/2}\),
\(|G|^2=2\Re G-1+|G-1|^2\), the positive-binomial tail, and
\(|G(t)-1|^2\ge(1/4-r/2)|t|^2\) for \(|t|\le r\le1/6\).
The higher analytic tail costs at most \(3rH/(4a^3)\), yielding the
coefficient \(1/4-5r/4\). Absolute convergence is an ordinary analytic input.

Under \(F\le8+3\eta\), (7) and
\[
 8a^2-(8+3\eta)a^3=5\eta-7\eta^2-\eta^3+3\eta^4
                         \ge5\eta-8\eta^2
\]
imply
\[
 S\ge\frac{45}{8}\eta+\frac{9\kappa}{8}H-\frac5{16}y
                         -9\eta^2-\frac23x^2-\eta x.           \tag{8}
\]
This retains the ENERGY term. Alternatively \(H\ge|T_2|\ge14y/9-|U|^2\)
and \(3/4+\kappa<1\) give
\[
 S\ge\frac{45}{8}\eta+\frac{13}{384}y
                         -9\eta^2-\frac89x^2-\eta x.           \tag{9}
\]
Neither inequality assumes \(U=O(\eta)\).

## Actual feasibility through all ninth-root weights

The division-free identity from9588 is universal for actual disk-rooted
polynomials. For \(|\omega|=1\),
\[
 w(\omega)=2\Re\{\omega p'(\omega)\overline{p(\omega)}\}
                  -9|p(\omega)|^2
 =\sum_{l=1}^9(1-|r_l|^2)\prod_{m\ne l}|\omega-r_m|^2\ge0.    \tag{10}
\]
Here \(r_l\) are the actual original roots. Differentiating the full product
and using \(2\Re\{\omega(\bar\omega-\bar r)\}-|\omega-r|^2=1-|r|^2\)
proves (10) without division. It includes boundary roots, root collisions
and zeros at sample points. This classical polar-derivative positivity is
credited, not presented as a new positivity method.

Set \(d_0=1+c_0\), \(d_k=c_k\) for \(1\le k\le8\).
At ninth roots of unity, the cyclic Fourier coefficients satisfy
\[
 D=W_0=18\Re d_0+\sum_{k=0}^8(2k-9)|d_k|^2\ge0,
 \qquad |W_m|\le D,
\]
\[
 W_1=9(c_1+\bar c_8)+Q_1,\qquad
 Q_1=\sum_{j=0}^7(2j-8)d_{j+1}\bar d_j-d_0\bar c_8.             \tag{11}
\]
The wrap in (11) is essential; all nine Fourier rows are compared in the
finite checks, including the ZERO other wrap in row2.
Anchoring gives
\[
 |d_0|\le D_0=9\eta+x+y+L,\qquad
 \Re d_0\le9\eta-S+8\eta x+7\eta y+L,
\]
\[
 |Q_1|\le D_0x+6xy+8D_0|c_1|+8L^2+4yL.                       \tag{12}
\]
Discard only nonpositive diagonal terms in \(D\). Combining (8), (11),
(12) and (6), applied ONLY to the positive linear \(5y/8\) term, gives
\[
\begin{split}
 x\le M_0:={}&\frac{27}{4}\eta+18\eta^2+19\eta x+14\eta y+2L
 +\left(\frac{45}{112}-\frac{9\kappa}{4}\right)H
 +\frac{160}{63}x^2+\frac59y^2+\frac79xy\\
 &+\frac19Lx+\frac{11}{9}L^2+\frac49yL
                        +|c_1|(1+8D_0/9).                    \tag{13}
\end{split}
\]
The coefficient of \(H\) in this intermediate expression is negative;
we retain it in the aggregate bound below. All phases have been handled
by legitimate complex norms, not a conjugate-pair average.

## Deriving the small critical mean

For a valid bound \(x\le x_0\), use (5), \(x^2\le x_0x\), \(\eta\le e\),
and \(H\le h\) in (13). Set
\[
\begin{split}
 \lambda(x_0)&=19e+\frac{160}{63}x_0+\frac79\frac92h
                       +\frac{\ell h}{9}+\frac89b_1h,\\
 C&=\frac{27}{4}+18e,\\
 N&=14e\frac92+2\ell+\frac{45}{112}-\frac{9\kappa}{4}
   +\left(\frac59(\frac92)^2+\frac{11}{9}\ell^2
                    +\frac49\frac92\ell\right)h
   +b_1\left(1+\frac89(9e+\frac92h+\ell h)\right).
\end{split}                                                    \tag{14}
\]
Thus \((1-\lambda)x\le C\eta+NH\). The following are exact rational
comparisons, with every denominator and strict margin reproduced in
[EXPECTED.json](EXPECTED.json):

| stage | valid input \(x_0\) | new bound \(x<X\eta+YH\) |
|---|---|---|
| 1 | \(9/25\) | \(X=169,\ Y=26\) |
| 2 | \(169e+26h\) | \(X=66,\ Y=10\) |
| 3 | \(66e+10h\) | \(X=11,\ Y=2\) |

For every row, \(1-\lambda(x_0)>0\), \(X(1-\lambda)>C\),
and \(Y(1-\lambda)>N\). These comparisons follow by clearing integer
denominators in (14); they cover the whole positive interval.

To improve the lower tail, use the COMPLETE third and fourth Newton
identities
\[
 c_6=-U^3/4+3UT_2/4-T_3/2,
\]
\[
 c_5=3U^4/40-9U^2T_2/20+9T_2^2/40+3UT_3/5-9T_4/20.
                                                                  \tag{15}
\]
For \(m\ge2\), \(|T_m|\le R^{m-2}H\). If \(x<X\eta+YH\), define
nonnegative polynomials in the TWO REAL variables \(\eta,H\):
\[
 X_0=X\eta+YH,\quad u=8X_0/9,\quad v=9(H+u^2)/14,
\]
\[
 C_k=b_kH\ (1\le k\le4),\quad
 C_6=u^3/4+3uH/4+RH/2,
\]
\[
 C_5=3u^4/40+9u^2H/20+9H^2/40+3RuH/5+9R^2H/20,
 \qquad L_0=\sum_{k=1}^6C_k.                                 \tag{16}
\]
They bound \(x,|U|,y,|c_k|,L\) respectively.

Using (9) instead of (8) gives the second mean bound
\[
\begin{split}
 x\le M_1:={}&\frac{27}{4}\eta+18\eta^2+19\eta x+14\eta y+2L
 +\frac83x^2+\frac59y^2+\frac79xy+\frac19Lx+\frac{11}{9}L^2
 +\frac49yL+|c_1|(1+8D_0/9).                                  \tag{17}
\end{split}
\]
Here the nonpositive \(-13y/192\) has been discarded. Substitute (16)
into this ENTIRE nonnegative polynomial.
For any polynomial \(P=\sum q_{ij}\eta^iH^j\) with \(q_{ij}\ge0\),
no constant term, define its complete endpoint majorant
\[
 \mathcal L(P)=\nu(P)\eta+\mu(P)H,
\quad \nu(P)=\sum_{i\ge1}q_{i0}e^{i-1},
\quad \mu(P)=\sum_{j\ge1,i\ge0}q_{ij}e^ih^{j-1}.               \tag{18}
\]
This is a termwise bound over the full domain, not a grid or fit.
For the input \((X,Y)=(11,2)\), (17) has
\(\nu(M_1)<7,\ \mu(M_1)<1/4\).
For the resulting input \((7,1/4)\), it has
\(\nu(M_1)<7,\ \mu(M_1)<1/8\).
Thus, without initial mean scaling,
\[
                       x<7\eta+H/8.                           \tag{19}
\]
The exact whole expanded majorants and both strict comparisons are regenerated
by [verify.py](verify.py); their complete digests and rational results are in
EXPECTED.json. The two eta margins exceed1/5; both energy margins are positive.

## Paired cube-root normal: the canceled third-order obstruction

Let \(\omega^3=1\), \(\omega\ne1\), and
\(\rho_k=(\omega^k+\bar\omega^k)/2\), equal to1 when3 divides \(k\)
and to \(-1/2\) otherwise. By (10), the paired weight is nonnegative:
\[
 0\le\frac{w(\omega)+w(\bar\omega)}2
  =18\Re\sum_{k=0}^8d_k\rho_k+Q,
\qquad Q=\sum_{k,l=0}^8(k+l-9)\rho_{k-l}d_k\bar d_l.          \tag{20}
\]
The complete anchored linear part equals
\[
 18(1-a^9)-27S+18(1-a^8)A+18(1-a^7)B
                     +18\sum_{k=1}^6(\rho_k-a^k)\Re c_k.      \tag{21}
\]
The leading linear \(c_6\), and \(c_3\), contributions cancel EXACTLY.
Hence \(c_6\) costs only \(4\eta|c_6|\) below, rather than a bare
third-order critical moment. This is the useful new cancellation.

Put \(\delta=d_0+c_8+c_7\). Actual anchoring gives
\[
 |\delta|\le\Delta=9\eta+8\eta x+7\eta y+L,
                       |d_0|\le x+y+\Delta.                   \tag{22}
\]
The ENTIRE top \((d_0,c_7,c_8)\) quadratic in (20) reduces to
\[
 -3x^2-6y^2-27\Re(c_8\bar c_7)
        +\Re\{(19c_8+20c_7)\bar\delta\}-9|\delta|^2.           \tag{23}
\]
Every other quadratic coefficient is retained in the following upper bound:
\[
 Q\le Q_+=27xy+(19x+20y)\Delta
       +16(x+y+\Delta)L+10xL+8yL+7L^2.                        \tag{24}
\]
For the cross coefficients in (20) with lower indices1 through6, their
actual maxima are12,8,4 against \(d_0,c_8,c_7\); (24) safely uses16,10,8.
Within the lower block, \(|(k+l-9)\rho_{k-l}|\le7\).
The discarded \(-3x^2,-6y^2,-9|\delta|^2\) are nonpositive. Thus (24)
does not assume any favorable relative complex phases.

From (20),(21), \(1-a^k\le k\eta\), and \(a^k\le1\),
\[
 S\le S_+=6\eta+\frac{16}{3}\eta x+\frac{14}{3}\eta y
       +|c_1|+|c_2|+|c_4|+|c_5|+2\eta|c_3|+4\eta|c_6|+Q_+/27.
                                                                  \tag{25}
\]
In (22),(24),(25), substitute the complete polynomials (16) with the
now-proved input \((X,Y)=(7,1/8)\). All substituted coefficients are
nonnegative, so (18) bounds the entire expression uniformly.

## Final energy feedback

Rearrange (7), bound \(\Re U^2\ge-|U|^2\), use
\((8a/9)A+(7/6)B\le(8/9)S+(5/18)y+(8/9)\eta x\), and apply (25).
This gives
\[
 \kappa H\le T-5\eta,
 \quad T=\frac89S_++\frac5{18}y+\frac89\eta x
                                      +\frac34|U|^2+8\eta^2.  \tag{26}
\]
Let \(\nu=\nu(T)-5\), \(g=\kappa-\mu(T)\), with every monomial
of the substituted \(T\) included in (18). Exact rational arithmetic gives
\[
                    g>0,\qquad25g-\nu>0.                     \tag{27}
\]
Consequently \(gH\le\nu\eta<25g\eta\), proving (2).
The finite whole-record values, including numerator and denominator of
\(\nu/g\), are in EXPECTED.json. They give \(\nu/g<25\); the damaged
claim \(\nu/g<24\) is explicitly rejected. No nonlinear term, wrap, phase,
or original-root feasibility condition is omitted.

## Credit, comparison, and trust boundary

The explicit whole-collar energy feedback (2), the complete paired-weight
cancellation (21), the phase-retaining quadratic reduction (23), and the
resulting outside-cap8 radius reduction are the proposed new useful scope.
They use classical polar derivative weights, Fourier orthogonality,
Newton/Vieta/Maclaurin and analytic binomial estimates. No historical
priority assertion is made.9588 supplies the prior universal weight/Fourier
framework and the low-energy entry corollary;9492 supplies only (7).
9533 and independently written9572 supply only the explicitly credited
cap8 consequences after entry. Prior qualitative concentration and radial
constraints in [8530](../../six-sendov-3/sharp-boundary-slope/PROOF.md) and
its [8608 audit](../../six-reviewer-3/sendov-boundary-audit/REVIEW.md)
remain prior work, not effective all-competitor collar coverage.

Campaign discussion2171 reports a teammate's complete but unpublished
centered original-root proof under the broader ABSOLUTE ENERGY condition
H<=1/512; radius1/64 is now only its corollary. The full private proof was
not read or imported here, and a draft announcement is not a verified premise,
source publication or independent review. That static-energy region and this
1/25 maximum-radius region are complementary; neither contains the other.
This proof is self-contained apart from the precisely identified analytic
envelope and corollaries. Any published overlap will receive exact scope and
source credit before graph submission.

The [current primary Zhang paper](https://arxiv.org/html/2609.19126)
states the first-power endpoint as Conjecture1.2 and proves the quadratic
case in Theorem1.3. [Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
discusses ordinary Sendov and states the stronger Tang–Zhang conjecture.
Both, and the two historical seeds, were live-refreshed2026-10-02.
Our global first-power and all-competitor concentration obligations remain open.

The checker compares whole polynomial coefficients of all Fourier rows,
the paired Hermitian kernel and top reduction, the anchored linear part,
all four Newton identities, and four entire literal actual original-root
weight identities. The literal controls include boundary/colliding roots;
they are controls of (10), not all examples of (1) or the low sublevel.
All scalar majorants are exact rational whole-window calculations.
The positivity proof, norm inequalities, absolute convergence and imports
are ordinary written trust boundaries. Finite checks do not make this a
formalized or independently audited theorem.
