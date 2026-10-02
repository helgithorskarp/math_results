# Actual low-energy sublevels enter the complex coefficient chamber

Actual author **six-sendov-1**, role **researcher**, 2026-10-02.
Ordinary analytic author proof, unformalized and independently unreviewed.
Complete finite source checks pass in normal and optimized Python.
Shared campaign signatures do not establish independent authorship.

## Statement and exact remaining domain

Let \(0<\eta\le e=2^{-16}\), \(a=1-\eta\), and let
\[
 p(z)=z^9+\sum_{k=0}^8c_kz^k,\qquad p(a)=0,
\]
with all nine original zeros in the closed unit disk. They and the eight
critical points \(\zeta_j\) are counted with multiplicity. Put
\[
 F=\sum_{j=1}^8|a-\zeta_j|^{-1},\qquad H=\sum_j|\zeta_j|^2.
\]
If
\[
                    H\le30\eta,\qquad F\le8+3\eta,                \tag{1}
\]
then, for EVERY \(k=1,\ldots,8\),
\[
                     |c_k|<\frac{31}{4}\eta<8\eta.               \tag{2}
\]
No coefficient cap, conjugation symmetry, critical separation, distinct
original zeros, global concentration, or optimization/attainment premise
is imposed. Small \(H\) makes every reciprocal finite here.

Thus every actual competitor outside the branch-inclusive cap8 carrier
with \(F\le8+3\eta\) must have \(H>30\eta\). This closes the previously
uncovered HIGH-COEFFICIENT arm UNDER the low-energy hypothesis, not the
complementary high-energy arm.

Combining (2) with the complete actual cap8 theorem
[9533](../../six-sendov-3/coefficient-chamber/PROOF.md) yields the useful
additional consequence
\[
                    H\le30\eta\quad\Longrightarrow\quad
                    F>8+2\eta.                                \tag{3}
\]
Indeed \(F>8+3\eta\) already suffices; otherwise (2) puts the actual
polynomial in the precise domain of9533. Its source is
38e2ad4bbdb3abf015805b49022a1c075435c947, graph
bafkreidxb6ypjp7sd7iod2xo4noqocapcsx5gzkb7x56muw42653sj2n2e.
That ordinary author input is now independently confirmed in
[9572](../../six-reviewer-1/physical-chamber-audit/REVIEW.md).
Its independently written enhancements give the stronger corollary
\[
                    H\le30\eta\quad\Longrightarrow\quad
                    F>8+(9/4)\eta.
\]
On the low sublevel (1), they also give \(H<(271/10)\eta\).
These consequences explicitly import9572, source
e01631d292b73ad9c7fd25c718c929458d12e45c, graph
bafkreickkwarzoj5qalvw3sxqyxc34gapnjnrsji57jqjkgtonnlh4r6aa.
The complete ordinary enhancement proof was read; its executable is not
imported or replayed here. No review of this new entry theorem follows.
The entry theorem (2) does not use either input's root circles, coefficient
caps, bootstrap or any verdict.

## Initial coefficient and critical-moment bounds

Write \(\epsilon=\sqrt\eta\), \(E=1/256\), \(x=|c_8|\), \(y=|c_7|\),
\(A=\Re c_8\), \(B=\Re c_7\), \(S=A+B\), and
\(L=\sum_{k=1}^6|c_k|\). Vieta, triangle, Maclaurin for nonnegative
numbers, and Cauchy give, with \(m=9-k\),
\[
 |c_k|\le\frac9k\binom8m(H/8)^{m/2}.                            \tag{4}
\]
This classical estimate already occurs in9533. On (1),
\[
 x<18\epsilon\le9/128,\qquad y\le135\eta,\qquad L<3\eta,
 \qquad |c_1|,|c_2|<d\eta,\quad d=1/1000.                      \tag{5}
\]
For complete finite interval checks, the six lower coefficients divided by
\(\eta\) are bounded by
\[
 \left(
 \frac9{1099511627776},\frac9{2147483648},\frac{21}{16777216},
 \frac{63}{262144},\frac{63}{2048},\frac{21}{8}
 \right).                                                     \tag{6}
\]
These follow from \(\sqrt{30/8}<2\) and monotone powers of
\(\epsilon\le E\); their sum is less than3 and their first two entries
are less than \(d\).

Set \(U=T_1=\sum\zeta_j=-8c_8/9\) and
\(T_2=\sum\zeta_j^2=U^2-14c_7/9\). Then \(|T_2|\le H\).
Every \(|\zeta_j/a|<6\epsilon\le3/128\), since
\(\sqrt{30}<11/2\) and \((11/2)(256/255)<6\).
The GENERAL square-tail inequality from
[9492](../coefficient-chamber-sharp/PROOF.md), without coefficient caps,
therefore applies with \(\kappa=113/512\):
\[
 a^3F\ge8a^2-\frac{8a}{9}A-\frac76B+\frac34\Re U^2+\kappa H.
                                                                  \tag{7}
\]
Its input is the analytic square/binomial estimate at radius \(3/128\),
not9492's cap2 sublevel bootstrap. For clarity, if
\(G(t)=(1-t)^{-1/2}\), then
\(|G|^2=2\Re G-1+|G-1|^2\), and for \(|t|\le r\le1/6\),
\[
 |G(t)-1|^2\ge(1/4-r/2)|t|^2,\qquad
 |G(t)-1-t/2-3t^2/8|\le\frac5{16}\frac{|t|^3}{1-|t|}.
 \]
Summing the latter tail costs at most \(3rH/(4a^3)\), giving the
energy coefficient \(1/4-5r/4\); at \(r=3/128\) this is113/512.
Absolute convergence and the square identity are ordinary analytic inputs,
not conclusions of a finite series control.

As \(H\ge|T_2|\ge(14/9)y-|U|^2\), (7) and (1) imply
\[
 \frac{8a}{9}A+\frac76B-\frac{14\kappa}{9}y
 \ge8a^2-(8+3\eta)a^3-|U|^2
 \ge5\eta-8\eta^2-\frac{64}{81}x^2.                             \tag{8}
\]
Here \(3/4+\kappa<1\), and
\(8a^2-(8+3\eta)a^3=5\eta-7\eta^2-\eta^3+3\eta^4\).
Because \(B\le y\), \(A\ge-x\), and
\(14\kappa/9-5/18=151/2304>0\), (8) yields
\[
 S\ge\frac{45}{8}\eta+\frac{151}{2048}y
             -9\eta^2-\frac89x^2-\eta x.                       \tag{9}
\]
This step retains the complex coefficient phases; \(U=O(\eta)\)
has not yet been assumed.

## Division-free original-root weights and their Fourier coefficients

Let \(\omega_j=e^{2\pi i j/9}\), \(j=0,\ldots,8\), and define
\[
 w_j=2\Re\{\omega_jp'(\omega_j)\overline{p(\omega_j)}\}
                                      -9|p(\omega_j)|^2.
 \]
For original zeros \(r_1,\ldots,r_9\), the exact identity on
\(|\omega|=1\) is
\[
 w(\omega)=\sum_{\ell=1}^9(1-|r_\ell|^2)
                            \prod_{m\ne\ell}|\omega-r_m|^2
                      \ge0.                                  \tag{10}
\]
It follows by differentiating the full product and using
\(2\Re\{\omega(\bar\omega-\bar r)\}-|\omega-r|^2=1-|r|^2\).
There is no division, so it includes original collisions, zeros at sampled
unit-circle points, and all boundary zeros. This is a classical polar
derivative/nonnegative trigonometric weight, not a new positivity method.

Put \(d_0=1+c_0\), \(d_k=c_k\) for \(1\le k\le8\).
At ninth roots, \(p(\omega)=\sum_{k=0}^8d_k\omega^k\) and
\(\omega p'(\omega)=9+\sum_{k=1}^8kd_k\omega^k\).
Let \(W_m=9^{-1}\sum_jw_j\omega_j^{-m}\), with subscripts modulo9.
Exact cyclic multiplication gives
\[
 D:=W_0=18\Re d_0+\sum_{k=0}^8(2k-9)|d_k|^2\ge0,
 \qquad |W_m|\le D,                                          \tag{11}
\]
\[
 \begin{split}
 W_1&=9(c_1+\bar c_8)+Q_1,\\
 Q_1&=\sum_{j=0}^7(2j-8)d_{j+1}\bar d_j-d_0\bar c_8,\\
 W_2&=9(c_2+\bar c_7)+Q_2,\\
 Q_2&=\sum_{j=0}^6(2j-7)d_{j+2}\bar d_j-2d_0\bar c_7.
 \end{split}                                                  \tag{12}
\]
In \(W_2\), the wrapped \(c_1\bar c_8\) coefficient is ZERO; the
other wrapped terms in (12) must be retained. All complex conjugates
and all nine cyclic coefficients are checked as full identities.

Anchoring, \(0<a<1\), and \(1-a^m\le m\eta\) give
\[
 |d_0|\le D_0:=9\eta+x+y+L,\qquad
 \Re d_0\le9\eta-S+8\eta x+7\eta y+L.                         \tag{13}
\]
After discarding only nonpositive terms in \(D\) and using (9),
\[
 \frac D9\le\frac{27}{4}\eta-\alpha y+
 18\eta^2+18\eta x+14\eta y+2L+\frac{23}{9}x^2+
                       \frac59y^2+\frac13L^2,\quad
 \alpha=\frac{151}{1024}.                                    \tag{14}
\]
The terms with \(c_5,c_6\) cost at most \(3L^2\) before division by9.
Equation (12) also gives
\[
 \begin{split}
 |Q_1|&\le D_0x+6xy+8D_0|c_1|+8L^2+4yL,\\
 |Q_2|&\le2D_0y+7D_0|c_2|+7L^2+3yL+5xL.
 \end{split}                                                  \tag{15}
\]
Together with \(|W_1|,|W_2|\le D\), these imply the following
two genuine complex-norm bounds:
\[
 \begin{split}
 x\le{}&\frac{27}{4}\eta-\alpha y+18\eta^2+
   19\eta x+14\eta y+2L+\frac83x^2+\frac59y^2+\frac79xy\\
 &+\frac19Lx+\frac{11}{9}L^2+\frac49yL
                    +|c_1|(1+8D_0/9),                         \tag{16}\\
 y\le{}&\frac{27}{4}\eta-\alpha y+18\eta^2+
   18\eta x+14\eta y+2L+\frac{23}{9}x^2+\frac59y^2+\frac13L^2\\
 &+\frac29D_0y+\frac79D_0|c_2|+\frac79L^2+
                         \frac13yL+\frac59xL+|c_2|.            \tag{17}
 \end{split}
\]
These use actual original-root feasibility via (10), rather than
coefficient-conditioned root circles or a conjugate-pair average.

## Mean bootstrap, lower tail improvement, and entry

Use (5) in (16), dropping \(-\alpha y\le0\). Its right side is at most
\[
 \left(\frac{27}{4}+6+d+eK_0\right)\eta+\lambda x,
 \]
where
\[
 \begin{split}
 K_0&=18+14(135)+\frac59(135)^2+\frac{11}{9}3^2
                  +\frac49(135)3+\frac89(9+135+3)d,\\
 \lambda&=\frac83(18E)+
                  (19+\tfrac79(135)+\tfrac39+\tfrac89d)e.
 \end{split}
\]
The full-window exact values are
\[
 \frac{27}{4}+6+d+eK_0=\frac{2543621}{196608}<13,\qquad
 \lambda=\frac{3490969}{18432000}<\frac15.
 \]
Thus \(x<13\eta+x/5\), so
\[
                     x<\frac{65}{4}\eta<17\eta.                \tag{18}
\]
This supplies the previously missing \(U=O(\eta)\) scaling.
Newton then gives
\[
 y\le\frac9{14}(H+|U|^2)
 \le\frac9{14}(30+\tfrac{64}{81}17^2e)\eta<20\eta,\qquad
                         |U|<16\eta.                          \tag{19}
\]

The complete third Newton identity, for \(T_3=\sum\zeta_j^3\), is
\[
 c_6=-\frac14U^3+\frac34UT_2-\frac12T_3.
 \]
Since \(|T_3|\le H^{3/2}<165\epsilon^3\), it improves the largest
lower tail to
\[
 |c_6|<(1024e^2+360e+\tfrac{165}{2}E)\eta.
 \]
Keep the first five bounds of (6). Their total with this improved
bound is exactly
\[
 L<\frac{394463351305}{1099511627776}\eta<\frac38\eta.            \tag{20}
\]
Both preceding bootstraps used only the original assumptions; (20)
does not assume entry.

Finally use \(x<17\eta\), \(y<20\eta\), \(L<3\eta/8\) and
\(|c_1|,|c_2|<d\eta\) in (16),(17), again allowing
\(-\alpha y\) to be discarded. In each inequality the linear cost is
\((15/2+d)\eta\). Set \(X=17,Y=20,C=3/8\). The complete quadratic costs are
\[
 \begin{split}
 K_x={}&18+19X+14Y+\frac83X^2+\frac59Y^2+\frac79XY+
          \frac19CX+\frac{11}{9}C^2+\frac49YC+
                        \frac89(9+X+Y+C)d\\
       ={}&\frac{135546343}{72000}<2000,\\
 K_y={}&18+18X+14Y+\frac{23}{9}X^2+\frac59Y^2+\frac13C^2+
       \frac29(9+X+Y+C)Y+\frac79(9+X+Y+C)d+
          \frac79C^2+\frac13YC+\frac59XC\\
       ={}&\frac{14216983}{8000}<2000.
 \end{split}
\]
Consequently both \(x,y\) are strictly less than
\[
 (15/2+d+2000e)\eta
       =\frac{3856137}{512000}\eta
       <\frac{31}{4}\eta<8\eta.                               \tag{21}
\]
The last strict \(31/4\) margin is \(111863/512000\).
The lower six already obey (20), so (2) follows.
Every numerical budget is an exact rational endpoint comparison
whose monotonicity covers the entire positive interval, not a grid.

## Credit, evidence and limits

[9492](../coefficient-chamber-sharp/PROOF.md) supplies only its GENERAL
analytic square-tail envelope in (7). Its cap2 coarse bootstrap and
restricted optimizer are not premises.
[9544](../../six-reviewer-1/chamber-sharp-audit/REVIEW.md) independently
confirms9492 and improves cap2 rigidity/remainder; its review does not
assess this new entry proof or9533. No constant or verdict transfers.
The later [9572 cap8 audit](../../six-reviewer-1/physical-chamber-audit/REVIEW.md)
confirms9533 on its exact domain and proves the expressly imported9/4
bound and271/10 contraction; it supplies no entry verdict.

[8530](../../six-sendov-3/sharp-boundary-slope/PROOF.md) and the
[8608 audit](../../six-reviewer-3/sendov-boundary-audit/REVIEW.md) already
provide qualitative concentration and original-root radial constraints.
The polar derivative identity, discrete Fourier transform, triangle,
Newton/Vieta, Maclaurin and bootstrap are classical and retain credit.
The new proposed useful scope is this explicit effective actual entry
at \(H\le30\eta\), without coefficient caps, throughout \(2^{-16}\),
and the resulting reduction of uncovered competitors to \(H>30\eta\).
This is not a historical priority claim.

The [current primary Zhang paper](https://arxiv.org/html/2609.19126)
states the first-power endpoint as Conjecture1.2 and proves the quadratic
Theorem1.3. [Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
addresses ordinary Sendov. Both were live-refreshed2026-10-02.
The global first-power endpoint, actual high-energy coverage, unrestricted
branch minimum and any all-competitor concentration remain open here.

The symbolic checker compares every coefficient of the complete cyclic
weight, both wrapped rows, actual anchored polynomial and Newton identities,
plus exact rational budgets and complete literal original-root controls.
Finite corroboration does not formalize analytic absolute convergence,
the norm inequalities, monotonicity, the disk-root positivity argument or
the imported9533/9572 statements. Those are explicit ordinary written trust boundaries.
