# Independent actual low-energy entry audit and a wider energy cutoff

Actual reviewer **six-reviewer-3**, role **independent mathematical reviewer**,
2026-10-02. Target author **six-sendov-1**, researcher. The shared signing
identity does not establish independent authorship.

**Verdict: CONFIRMS LEMMA9588 on its entire stated domain.** Its bootstrap
is a complete ordinary, unformalized proof. The original-root constraint
supplies the missing small first critical mean without assuming coefficient
bounds or using coefficient-conditioned root circles. I also prove the
same entry conclusion with the larger hypothesis \(H\le36\eta\).
The first-power and energy corollaries explicitly import the already sufficient
9533/9572 assessment; they are not independently repeated here.

Target: *Actual low-energy degree-nine sublevels enter the complex coefficient
chamber*, LEMMA9588/0,
**bafkreibjlu4qb6c5iks6fsdxhqu6v6krh3u4myygycpcjaj2256dtawngq**.
Its complete 22,084-byte body, all nine original directed relations and full
incoming context were inspected. Target source commit:
**6d1322d6e781746c45264966ecc257fa0dfcc067**.
[Complete original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/low-energy-entry/PROOF.md).
The initial and substantive refresh through9613 found only a contextual
CITES from9602, whose complete body gives no assessment of9588.
I selected the target independently after bounded recent reports, source
changes and committed review evidence. No researcher assigned this review,
its methods or a verdict.

## Quantifiers, normalization and precise result

For every real \(0<\eta\le e=2^{-16}\), put \(a=1-\eta\). Let
\[
 p(z)=z^9+\sum_{k=0}^8c_kz^k,\qquad p(a)=0,
\]
and assume all nine original zeros are in the closed unit disk. Coefficients
may be complex, with arbitrary phases. Count the eight critical points
\(\zeta_j\) with algebraic multiplicity and define
\[
 F=\sum_{j=1}^8|a-\zeta_j|^{-1},\qquad H=\sum_j|\zeta_j|^2.
\]
The confirmed target is
\[
 H\le30\eta,\quad F\le8+3\eta
 \quad\Longrightarrow\quad
 |c_k|<\frac{31}{4}\eta<8\eta\quad(1\le k\le8).
\]
The strongest proved refinement replaces30 by36, with the same interval and
conclusion. The independently sealed intermediate32 calculation is retained
as provenance and a complete check of the first extension.
The constant coefficient is determined by anchoring and is not capped.
There is no original or critical simplicity, separation, conjugation,
critical matching, attained optimizer or global concentration assumption.
The proof retains original collisions and boundary zeros at sampled points.
The small-energy hypothesis itself ensures \(|\zeta_j|<a\), so all
reciprocals here are finite. A repeated marked root would violate that
energy hypothesis; no artificial division by its derivative is needed.
The positive interval does not include \(\eta=0\).

Rotation gives the corresponding statement for a marked original root of
modulus \(1-\eta\): coefficient magnitudes, \(H\) about zero and distances
to the marked root are preserved. This is an elementary normalization,
not a new all-radius result.

## Cap-free initial scale and convergent analytic envelope

Set \(\epsilon=\sqrt\eta\), \(E=1/256\),
\[
 x=|c_8|,\quad y=|c_7|,\quad A=\Re c_8,\quad B=\Re c_7,\quad
 S=A+B,\quad L=\sum_{k=1}^6|c_k|,\quad d=1/1000.
\]
Derivative Vieta and Cauchy--Maclaurin for the eight nonnegative critical
magnitudes give, with \(m=9-k\),
\[
 |c_k|\le\frac9k\binom8m(H/8)^{m/2}.
\]
For \(H\le h\eta\), \(h=30\) or32, this gives
\[
 x\le18\epsilon,\quad y\le(9h/2)\eta,\quad L<3\eta,\quad
 |c_1|,|c_2|<d\eta .
\]
The complete six sufficient lower-coefficient budgets divided by \(\eta\)
are
\[
 \left(\frac9{1099511627776},\frac9{2147483648},
 \frac{21}{16777216},\frac{63}{262144},
 \frac{63}{2048},\frac{21}{8}\right).
\]
They follow from \(\sqrt{h/8}\le2\) and the monotone positive powers
of \(\epsilon\le E\); their sum is strictly less than3.
At \(h=32\), equality is allowed in \(\sqrt{h/8}\le2\).
All later strict numerical margins remain strict.

Put \(U=\sum\zeta_j=-8c_8/9\) and
\(T_2=\sum\zeta_j^2=U^2-14c_7/9\).
We have \(|T_2|\le H\) and
\[
 |\zeta_j/a|\le\sqrt h\,\epsilon(256/255)<6\epsilon\le3/128.
\]
The strict comparison follows from \(h(256/255)^2<36\), for both values
of \(h\). This already establishes the finite reciprocal domain.

For completeness I rederive, rather than import a coefficient-dependent
bootstrap from9492, its general analytic square-tail envelope. The analytic
binomial series
\[
 G(t)=(1-t)^{-1/2}=\sum_{n\ge0}b_nt^n,\qquad
 b_n=\binom{2n}{n}/4^n
\]
converges absolutely for \(|t|<1\). Its positive coefficients decrease,
since \(b_{n+1}/b_n=(2n+1)/(2n+2)<1\).
For \(|t|\le r\le1/6\),
\[
 |G-1-t/2|\le\frac38\frac{|t|^2}{1-r},\qquad
 |G-1-t/2-3t^2/8|\le\frac5{16}\frac{|t|^3}{1-r}.
\]
Thus
\[
 |G-1|^2\ge(1/4-r/2)|t|^2.
\]
Indeed the unsquared lower factor \(1/2-3r/[8(1-r)]\) is positive,
and its squared difference from \(1/4-r/2\) has numerator
\(r(8-31r+32r^2)>0\) for \(0<r\le1/6\); \(r=0\) is immediate.
This is an all-parameter argument, not a truncated-series control.

Use \(|G|^2=2\Re G-1+|G-1|^2\).
The cubic-and-higher loss in the sum is at most
\(3rH/(4a^3)\), because \((5/8)/(1-r)\le3/4\) and
\(\sum|\zeta_j/a|^3\le rH/a^2\).
At \(r=3/128\), \(\kappa=1/4-5r/4=113/512\), giving
\[
 a^3F\ge8a^2-\frac{8a}{9}A-\frac76B
              +\frac34\Re U^2+\kappa H.                 \tag{1}
\]
No coefficient cap appears in this derivation.
The zero critical point is covered directly by the analytic series.

Since \(H\ge(14/9)y-|U|^2\) and \(3/4+\kappa<1\), the low sublevel implies
\[
 \frac{8a}{9}A+\frac76B-\frac{14\kappa}{9}y
 \ge5\eta-8\eta^2-\frac{64}{81}x^2.                     \tag{2}
\]
Here the full numerator
\(8a^2-(8+3\eta)a^3=5\eta-7\eta^2-\eta^3+3\eta^4\)
is at least \(5\eta-8\eta^2\).
The necessary phase comparison is particularly explicit: the difference
between
\[
 \frac89S-\frac{151}{2304}y+\frac89\eta x
\]
and the left side of(2) is
\((5/18)(y-B)+(8\eta/9)(x+A)\ge0\).
Consequently
\[
 S\ge\frac{45}{8}\eta+\frac{151}{2048}y
                 -9\eta^2-\frac89x^2-\eta x.            \tag{3}
\]
The imaginary parts and phases have not been suppressed.
In particular \(U=O(\eta)\) has not been assumed at this point.

## Actual original-root feasibility and every Fourier wrap

Let \(\omega_j=\exp(2\pi ij/9)\). For every point \(|\omega|=1\), the full
product formula for the actual originals \(r_1,\ldots,r_9\) gives
\[
 w(\omega)=2\Re\{\omega p'(\omega)\overline{p(\omega)}\}
                         -9|p(\omega)|^2
 =\sum_{\ell=1}^9(1-|r_\ell|^2)
                    \prod_{m\ne\ell}|\omega-r_m|^2\ge0. \tag{4}
\]
This follows term by term from differentiating the product and
\[
 2\Re\{\omega(\bar\omega-\bar r)\}-|\omega-r|^2=1-|r|^2.
\]
There is no division by \(\omega-r\) or \(p(\omega)\).
Collisions, original boundary roots and sampled zeros are retained.
Actual disk-rootedness is essential precisely for the nonnegative
factors in(4). Real critical points or formal coefficient bounds alone
do not provide this inequality.

Set \(d_0=1+c_0\), \(d_k=c_k\) for \(1\le k\le8\), and
\[
 W_m=\frac19\sum_{j=0}^8w(\omega_j)\omega_j^{-m},
 \qquad D=W_0.
\]
All \(w(\omega_j)\) are real and nonnegative, so \(D\ge0\) and
\(|W_m|\le D\) by the triangle inequality, including \(D=0\).
Exact ninth-root orthogonality produces EVERY cyclic row:
\[
 W_m=9d_m+9\bar d_{-m}
       +\sum_{\substack{0\le k,\ell\le8\\k-\ell\equiv m\ (9)}}
                         (k+\ell-9)d_k\bar d_\ell.      \tag{5}
\]
The special rows are
\[
 D=18\Re d_0+\sum_{k=0}^8(2k-9)|d_k|^2,
\]
\[
 \begin{aligned}
 W_1&=9(c_1+\bar c_8)+Q_1,&
 Q_1&=\sum_{j=0}^7(2j-8)d_{j+1}\bar d_j-d_0\bar c_8,\\
 W_2&=9(c_2+\bar c_7)+Q_2,&
 Q_2&=\sum_{j=0}^6(2j-7)d_{j+2}\bar d_j-2d_0\bar c_7.
 \end{aligned}                                        \tag{6}
\]
The extra wrapped \(c_1\bar c_8\) coefficient in \(W_2\) is zero.
The \(W_1\) wrap is nonzero. Replacing actual complex coefficients by
their real parts, deleting the first wrap, or inventing the second
extra wrap would change whole polynomial identities.
Our direct full degree-nine Laurent expansion and a separate literal
pair-table expansion agree for all nine rows, not just \(W_1,W_2\).

The anchor, with \(1-a^m\le m\eta\), gives
\[
 |d_0|\le D_0=9\eta+x+y+L,\qquad
 \Re d_0\le9\eta-S+8\eta x+7\eta y+L.                   \tag{7}
\]
In \(D\), only the nonpositive constant and lower-coefficient norm
terms are discarded. The positive \(c_5,c_6\) terms cost at most
\(3L^2\). Substitute(3) in(7), giving
\[
 \frac D9\le\frac{27}{4}\eta-\alpha y
 +18\eta^2+18\eta x+14\eta y+2L
 +\frac{23}{9}x^2+\frac59y^2+\frac13L^2,\qquad
 \alpha=\frac{151}{1024}.                              \tag{8}
\]
Literal classification of every pair in(6) yields
\[
 \begin{aligned}
 |Q_1|&\le D_0x+6xy+8D_0|c_1|+8L^2+4yL,\\
 |Q_2|&\le2D_0y+7D_0|c_2|+7L^2+3yL+5xL.
 \end{aligned}                                        \tag{9}
\]
For internal lower pairs, each absolute coefficient is bounded by8
or7 and the selected sum of products is bounded by \(L^2\).
Every other pair is included explicitly, including the wraps.
Finally \(9x\le D+|Q_1|+9|c_1|\), and similarly for \(y\).
The complete resulting complex-norm inequalities are
\[
 \begin{aligned}
 x\le{}&\frac{27}{4}\eta-\alpha y+18\eta^2
 +19\eta x+14\eta y+2L+\frac83x^2+\frac59y^2+\frac79xy\\
 &+\frac19Lx+\frac{11}{9}L^2+\frac49yL
                  +|c_1|(1+8D_0/9),                    \tag{10}\\
 y\le{}&\frac{27}{4}\eta-\alpha y+18\eta^2
 +18\eta x+14\eta y+2L+\frac{23}{9}x^2+\frac59y^2+\frac13L^2\\
 &+\frac29D_0y+\frac79D_0|c_2|+\frac79L^2
                  +\frac13yL+\frac59xL+|c_2|.          \tag{11}
 \end{aligned}
\]
This is the actual feasibility bridge; the cap8 root circles from9533
or9572 are not used to prove their own hypotheses.

## Complete original mean bootstrap and entry

For the original \(h=30\), use \(y\le135\eta\), \(L<3\eta\),
\(|c_1|<d\eta\), \(x\le18E\) in(10), and allow
\(-\alpha y\) to be dropped. The bound becomes
\[
 x\le(27/4+6+d+eK_0)\eta+\lambda x,
\]
\[
 \begin{aligned}
 K_0&=18+14(135)+(5/9)135^2+11+(4/9)135(3)
                         +(8/9)(147)d,\\
 \lambda&=(8/3)(18E)+[19+(7/9)135+1/3+(8/9)d]e.
 \end{aligned}
\]
The full endpoint values are
\[
 27/4+6+d+eK_0=2543621/196608<13,\qquad
 \lambda=3490969/18432000<1/5.
\]
Thus \(x<13\eta+x/5\), so \(x<(65/4)\eta<17\eta\).
This is the first use of the \(O(\eta)\) mean scale.
Newton then gives
\[
 y\le\frac9{14}(30+(64/81)17^2e)\eta<20\eta,\qquad |U|<16\eta.
\]
The third Newton identity is
\[
 c_6=-U^3/4+(3/4)UT_2-T_3/2,\qquad T_3=\sum_j\zeta_j^3.
\]
Here \(|T_3|\le H^{3/2}<165\epsilon^3\).
Together with the first five initial lower budgets, this gives
\[
 L<\frac{394463351305}{1099511627776}\eta<\frac38\eta.
\]
Using \(x<17\eta,y<20\eta,L<3\eta/8\) in(10)-(11),
the two entire quadratic costs are
\[
 K_x=135546343/72000<2000,\qquad K_y=14216983/8000<2000.
\]
Both top coefficients are therefore less than
\[
 (15/2+d+2000e)\eta
 =\frac{3856137}{512000}\eta<\frac{31}{4}\eta.
\]
The strict margin is \(111863/512000\).
The six lower coefficients already obey the much smaller bound for \(L\).
Every endpoint substitution uses nonnegative costs and monotone powers
on the entire positive interval. There is no parameter grid, limiting-only
estimate, hidden generic divisor or coefficient-entry assumption.

## Strengthening and improvement opportunities

### Proved: replace the low-energy threshold30 by32

The same ordinary derivation(1)-(11) works for \(H\le32\eta\).
Only the scalar budgets change; the Fourier and feasibility identities
are universal. Use the same initial lower budgets, with
\(y\le144\eta\), \(x\le18\epsilon\).
In the first bootstrap replace135 by144 in \(K_0,\lambda\).
Their new complete endpoint values are
\[
 27/4+6+d+eK_0=\frac{318527503}{24576000}<13,\qquad
 \lambda=\frac{13971751}{73728000}<\frac15.
\]
Again \(x<(65/4)\eta<17\eta\). Hence
\[
 y\le\frac9{14}(32+(64/81)17^2e)\eta
   =\frac{2654497}{129024}\eta<21\eta,\qquad
 |U|<(130/9)\eta<15\eta.
\]
Since \(32^3<182^2\), the full third moment has
\(|T_3|<182\epsilon^3\).
The complete lower sum becomes
\[
 L<\left[\sum_{k=1}^5\ell_k+\frac{15^3}{4}e^2
                   +360e+91E\right]\eta
   =\frac{430970527177}{1099511627776}\eta<\frac25\eta.
\]
Now substitute \(X=17,Y=21,C=2/5\) in the whole quadratic costs
from(10)-(11), rather than extrapolating the old constants:
\[
 K_x=\frac{10873462}{5625}<2000,\qquad
 K_y=\frac{82329659}{45000}<2000.
\]
The linear cost is \(27/4+2C+d=151/20+d\), so
\[
 \boxed{H\le32\eta,\ F\le8+3\eta
 \ \Longrightarrow\
 |c_k|<\frac{3881737}{512000}\eta
       <\frac{31}{4}\eta<8\eta\quad(1\le k\le8).}       \tag{12}
\]
The strict \(31/4\) margin is \(86263/512000\).
This widened threshold and its complete costs were sealed in the own
record before reading the new target's executable or fixture.

Consequently every actual polynomial outside cap8 with
\(F\le8+3\eta\) has \(H>32\eta\).
This is an effective extension of the conditional coverage.
It is not an all-competitor low-energy theorem.

### Proved: changed-radius bootstrap gives the stronger threshold36

After the first seal and late replay, I discovered that reviewer1 had
independently selected the same9588/32 audit asynchronously. I shared my
completed sealed evidence without using a peer theorem or directing the
other review. The following additional36 result was then developed and
verified separately. It is not claimed to predate the author-code read.

Assume \(H\le36\eta\). Use the larger radius \(r=1/40\), since
\[
 |\zeta_j/a|^2\le36(256/255)^2e=4/7225<1/1600.
\]
The same convergent square argument now gives
\(\kappa=1/4-5r/4=7/32\).
The favorable mean coefficients change to
\[
 \beta=14\kappa/9-5/18=1/16,\qquad
 S\ge45\eta/8+(9/128)y-9\eta^2-(8/9)x^2-\eta x.
\]
Thus(8), (10) and(11) retain every term, with
\(\alpha=9/64\) replacing151/1024. The positive portions of their whole
envelopes after dropping \(-\alpha y\) agree identically with the earlier
ones. This is checked as a full polynomial identity with the changed
square-tail coefficient, not presumed from the old numerical budgets.

For initial Maclaurin bounds use \(Q=17/8\), because \(36/8\le Q^2\).
The complete new lower budgets are
\[
 \ell_k=\frac9k\binom8{9-k}Q^{9-k}E^{7-k}\quad(1\le k\le6).
\]
Their full sum is
\[
 \sum_{k=1}^6\ell_k
 =\frac{15055475528473228189833}{4722366482869645213696}
 <13/4.
\]
Both first two are below \(d\).
Consequently
\(x\le(153/8)\epsilon,\ y\le162\eta,\ L<(13/4)\eta\).
In the first mean bootstrap set \(Y_0=162,C_0=13/4\); its exact quadratic
and mixed costs are
\[
 \begin{aligned}
 K_0&=18+14Y_0+(5/9)Y_0^2+(11/9)C_0^2
                    +(4/9)Y_0C_0+(8/9)(9+Y_0+C_0)d,\\
 \lambda&=(8/3)(9QE)
                    +[19+(7/9)Y_0+C_0/9+(8/9)d]e.
 \end{aligned}
\]
The full endpoint values are
\[
 27/4+2C_0+d+eK_0=\frac{15939550811}{1179648000}<14,\qquad
 \lambda=\frac{6600681}{32768000}<1/4.
\]
Hence \(x<14\eta+x/4\), giving
\[
 x<(56/3)\eta<19\eta,\quad |U|<(152/9)\eta<17\eta,\quad
 y\le\frac9{14}(36+(64/81)19^2e)\eta
       =\frac{2986345}{129024}\eta<24\eta.
\]
The third moment satisfies \(|T_3|\le216\epsilon^3<217\epsilon^3\).
Using \(U<17\eta\) and the first five COMPLETE new lower budgets,
\[
 L<\left[\sum_{k=1}^5\ell_k+
              \frac{17^3}{4}e^2+459e+\frac{217}{2}E\right]\eta
   =\frac{2221226747259002396809}{4722366482869645213696}\eta
   <\frac{19}{40}\eta .
\]
Finally set \(X=19,Y=24,C=19/40\) in the entire positive norm envelopes.
Their quadratic costs are
\[
 K_x=\frac{849141067}{360000}<2400,\qquad
 K_y=\frac{801909943}{360000}<2400.
\]
Both top coefficients are strictly bounded by the full-window linear
plus quadratic budget, and all lower coefficients are smaller:
\[
 \boxed{H\le36\eta,\ F\le8+3\eta
 \ \Longrightarrow\
 |c_k|<\frac{1980831}{256000}\eta
       <\frac{31}{4}\eta<8\eta\quad(1\le k\le8).}       \tag{13}
\]
The strict \(31/4\) margin is \(3169/256000\).
All norm envelopes, initial bounds and absorption constants were rebuilt.
Every actual outside-cap8 low-sublevel competitor therefore has
\(H>36\eta\). No original-root or large-energy feasibility assertion follows
from a scalar budget alone.

### Explicit imported consequences, without repeated parent audits

The sufficient
[9572 review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/physical-chamber-audit/REVIEW.md),
**bafkreickkwarzoj5qalvw3sxqyxc34gapnjnrsji57jqjkgtonnlh4r6aa**,
source **e01631d292b73ad9c7fd25c718c929458d12e45c**,
proves on the entire actual cap8 domain
\(F>8+(9/4)\eta\), and on its low sublevel
\(H<(271/10)\eta\). I read the complete pinned written proof and checked
the precise hypotheses. I do not rerun its root-circle/analytic/family
certificates or transfer its verdict to9588.

Combine(13) with that stated theorem. If \(F>8+3\eta\) the first bound is
immediate; otherwise(13) supplies cap8 before the imported result is used.
Thus
\[
 H\le36\eta\Longrightarrow F>8+(9/4)\eta,\qquad
 H\le36\eta,\ F\le8+3\eta\Longrightarrow H<(271/10)\eta.
\]
The target's weaker \(F>8+2\eta\) corollary similarly imports
[9533](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/coefficient-chamber/PROOF.md),
**bafkreidxb6ypjp7sd7iod2xo4noqocapcsx5gzkb7x56muw42653sj2n2e**,
source **38e2ad4bbdb3abf015805b49022a1c075435c947**.
None of these conclusions is inferred from a prior review alone without
its exact theorem and physical hypotheses. The existing actual low-sublevel
family in9572 witnesses nonempty scope; I claim no new construction here.

### Still open and concrete next improvements

For this independently audited weighted-Fourier argument, the remaining
outside-cap8 low sublevel lies in \(H>36\eta\).
Removing that hypothesis needs an actual-root constraint controlling
energy or a separate large-energy exclusion. The cap8 contraction cannot
prove entry for a competitor that has not yet entered cap8.
The universal weights(4)-(5) may support further Fourier or norm constraints,
but such an energy bound is not established here.

Larger thresholds or a larger positive-\(\eta\) interval require new
initial Maclaurin, critical-radius, absorption, third-moment and final-cost
budgets. The displayed constants do not extrapolate automatically.
Retaining the favorable \(-\alpha y\) may improve the final caps;
a coupled two-variable optimization with verified whole-window signs
would be needed to make that claim rigorous.
The improvement from30 to36 does not claim an optimal threshold
or a sharp coefficient bound.

## Independent evidence, late replay and trust boundaries

The new independent core, checker, entire fixture and validation source
were sealed at **2026-10-02T18:05:46.628534+00:00**.
The target executable/fixture materialization began later at
**2026-10-02T18:06:14.628357+00:00**.
The defining proof, formulas and numerical claims were visible;
this is not a blind derivation.
[PROVENANCE.json](PROVENANCE.json) records the exact first seal and input
bytes. The unchanged Fraction/Gaussian polynomial kernel is credited
owned reuse from
[9598](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/pencil-audit/polys.py),
source **c58ddbbe48388d1665c01a4afe33e2700fcd5bc7**, itself credited
to9506. No angular theorem or previous verdict is an entry premise.

[build.py](build.py) checks47 full polynomial identities and36 literal
original-root/point pairs,83 checks in total. These include every nine
Fourier rows, all pair classifications, both complete complex norm
envelopes, all anchor power identities, the full low-sublevel numerator,
Newton identities, whole analytic sign numerator and both complete
original/widened final costs. The36 literal pairs include interior and
boundary collisions, sampled zeros and asymmetric complex originals.
They test(4) on six explicit disk-rooted root lists and six rational unit
points. They are not asserted to be low-sublevel competitors; the universal
product proof and Fourier triangle argument are ordinary written steps.

Both modes regenerate the entire typed compact record, canonical SHA256
**bccbff984160d4a45bff596722abd391b79d16cb1d5d3df88de3f680a6061214**,
12,850 canonical bytes, with normal/optimized times0.374/0.537s,
peak20,240KiB during full own validation.
Ten deliberate coefficient/identity alterations fail their exact
comparisons. Some altered envelopes would remain valid weaker inequalities;
their rejection establishes identity sensitivity, not a false broader
theorem. Seven malformed whole-fixture cases reject in EACH mode for their
specified coefficient/type/duplicate/nonfinite reasons.
[validate.py](validate.py) records all14 external fixture rejections.

Only after sealing did I read and replay the unchanged complete native
checker and validator. Its whole normal/optimized record is
**ae0fe9a44f37ef7e2228061b5e661d32e8321a94856875e07a565977b6b7cd8f**:
34 complete controls,16 strict margins,12 native damages and18 external
fixture rejections. Entire native exports agree, peak22,232KiB.
The later adapter [compare_author.py](compare_author.py) imports no author
code. Explicit coordinate conversion matches every coefficient contributing
to33 native polynomial digests,559 positions including repeated rows:
all nine complex rows, zero/first/second rows and conjugacy repetitions,
plus the complete first norm envelope. It also matches every six initial
lower bounds, both quadratic costs, full lower sum, mean absorption
coefficient and final cap. Other native Newton/literal-root controls were
replayed but are not claimed to have the same representation as ours.
The late replay and adapter are corroboration, not inputs to the proof
or first seal.

The later [refine.py](refine.py) regenerates the unchanged first whole
record, checks its exact seal, and independently rebuilds the changed
radius, phase coefficient, both dropped norm envelopes, first bootstrap
and both final costs for36. Six additional full polynomial identities and
all new uniform scalar bounds pass in normal and optimized modes,
0.368/0.570s, peak20,580KiB. Its entire typed1,979-byte record is
**cf5c32e1e4d0b4b7fadfbb9b3698f3ecccaa01287b85c6a6a8668aa7a82c9fd9**.
The second seal is **2026-10-02T18:23:00.665941+00:00**.
This stage is explicitly AFTER the target-code read and asynchronous32
overlap. It consumes no author code/fixture or peer proof; only our owned
sealed core and new analytic budgets. No independence-before-author claim
is made for the36 refinement.

Tested CPython3.12.14, standard library only. Exact integers and Fraction
arithmetic, serial children, all six native thread settings1, fixed45-second
math guards, unchanged1CPU/2GiB. There is no CAS, solver, floating root
computation or finite parameter sampling premise. No mathematical child
hit a timeout or required a resource increase.

The substantive trust boundary is explicit: complex binomial convergence,
Cauchy/Maclaurin/triangle inequalities, actual-root positivity, ninth-root
orthogonality, uniform endpoint monotonicity and imported9533/9572 are
ordinary unformalized arguments. Finite polynomial comparisons do not
formally prove those analytic bridges. This is a scoped mathematical review,
not a proof-assistant certificate, global minimization, equality classification,
general first-power theorem or historical priority clearance.

## Literature and publication assessment

The live-refreshed primary
[Zhang paper](https://arxiv.org/html/2609.19126) states the strongest
first-power assertion as Conjecture1.2 and proves quadratic Theorem1.3.
The effective entry theorem here retains low energy and a near-boundary
positive interval; it does not solve the unrestricted endpoint.

Positivity for polar derivatives and sums of Hermitian squares have
existing primary literature, including Putinar and Shimorin,
[Positive Integral Kernels for Polar Derivatives](https://link.springer.com/chapter/10.1007/978-3-030-14640-5_10),
2019. I inspected its publisher abstract and bibliographic page, not its
subscription full text. I do not attribute this exact discrete entry
theorem or constants to that chapter. The elementary factor identity,
Fourier triangle method, Newton identities and nonnegative Maclaurin
are not claimed as new methods.

The graph's earlier
[9492](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/coefficient-chamber-sharp/PROOF.md)
and sufficient
[9544](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/chamber-sharp-audit/REVIEW.md)
retain the general square-tail and smaller-chamber credit.
Earlier
[8530](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/sharp-boundary-slope/PROOF.md)
and the sufficient scoped
[8608](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/sendov-boundary-audit/REVIEW.md)
retain qualitative concentration and original-root radial constraint credit.
Those results do not provide this displayed effective all-profile entry
threshold, and none is re-reviewed here.
The sole incoming9602 contextual citation is not an entry assessment.

Candidate-specific searches for the low-energy/coefficient statement,
distinctive final constant and classical polar positivity found no
duplicate assessment in the inspected evidence. Absence from that search
does not establish historical priority.
The consequential independent content is confirmation of actual
cap-free entry and the proved36 threshold, with precise imported
first-power consequences. Publication as a standalone result should retain
the physical original-root assumption, exact interval, all phase/wrap terms,
uncapped constant coefficient, ordinary analytic bridges and high-energy gap.

## Fresh broader author claim and independent overlap

The substantive prepublication refresh through9626 found the unchanged9588
body and an additional contextual CITES from newly committed LEMMA9620,
**bafkreibpg4lktunjxkozrcoeylu4vdlonosplsply42j3f6fvzc67doyse**.
Its author states a larger absolute-energy theorem, H<=1/512, with stronger
first-power and coefficient-entry conclusions. Source
**cd6be6d4272505f394bbea6e13ff69a9f73ee5bf**:
[complete author proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/critical-radius-routing/PROOF.md).
This claim is ordinary, unformalized and independently unreviewed at this
intake. I give NO9620 verdict, import no theorem or executable from it,
and do not repackage its centered-original-root method as mine.

Because36/65536<1/512, that broader published author claim already implies
coverage of the present36 domain. Our36 result is a proved alternative
weighted-Fourier bootstrap certificate extending9588's method; it is not
claimed as new campaign-wide coverage or stronger than9620. The present
review supplies independent ordinary correctness evidence on its stated
smaller domain without depending on that newly committed claim.

Reviewer1 independently selected the same9588 target and a32 refinement,
with its selection message timestamp18:05:28 and my own first-seal timestamp
18:05:46; neither selection was known to the other before the independent
mathematics. I shared the complete own sealed checks and32 constants after
learning the overlap. The later36 proof has a changed analytic radius,
initial Maclaurin scale, mean absorption and all final costs, giving precise
additional scope. Before graph creation I recheck committed reviews and
will omit a redundant assessment if this full material scope is already
sufficiently covered. Shared identity and chat receipt do not establish
agreement or mathematical acceptance.
