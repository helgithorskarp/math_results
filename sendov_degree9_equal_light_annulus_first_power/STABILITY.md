# A quadratic origin margin and an explicit unequal-light tube

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
This is a further ordinary analytic consequence of the complete
certificate in [PROOF.md](PROOF.md). It is unformalized and independently
unreviewed. The coefficient support, constants and additional complete
one-variable identity are checked by [stability.py](stability.py).
The support still requires regeneration of both entire G6 tensors.

## 1. Quantitative normalized margin

Under the equal-light abstract hypotheses (2)--(3) of PROOF.md, write
$\varepsilon=1-b$. The stronger conclusion is

$$
 |I|^2-r^{12}s^4\ge10^{-32}\varepsilon^2.
 \tag{18}
$$

The constant is very conservative. The relevant tensor G6 is the
**reduced sixth angular Bernstein control**, not the leading power
coefficient $G_6$ of the Gram polynomial.
Let $Q_6=P_6/t^4$ in equation(13).
Both complete G6 tensors have $u$ degree72, radius clearing power40,
and no zero coefficient at any $u$-index0 through70.
Their normalized minimum positive coefficients (after the positive
constant scale) are

$$
 B_+=\frac{11132555231232}{2239055},\qquad
 B_-=\frac{17179869184}{639}.
$$

For every $u\in[0,1]$,

$$
 T(u)=\sum_{i=0}^{70}\binom{72}i u^i(1-u)^{72-i}
       \ge(1-u)^2.
 \tag{19}
$$

One proof is that two specified Bernoulli failures imply at least two
failures among72 trials. Equivalently, degree72 Bernstein coefficients
of $T-(1-u)^2$ are

$$
 {\bf1}_{i\le70}-\frac{\binom{72-i}2}{\binom{72}2}\ge0.
$$

The source checks all73 coefficients and their entire power identity
$T-(1-u)^2=2u-u^2-72u^{71}+71u^{72}$.
This is a uniform identity and sign proof, not point sampling.

Use partition of unity on the other tensor coordinates and equation(16).
On either complete radius chart,

$$
 Q_6\ge\frac{B_\pm(1-u)^2}{(1+b)^{40}}
       \ge B_\pm2^{6-40}\varepsilon^2.
$$

The sixth angular coefficient of $G(Kh)$, without the $t^{12}$ clearing,
is $Q_6/t^8$. The floors and budget give $s\le5/2$ and $t\le s$.
Hence this coefficient is at least
$B_\pm2^{14-40}\varepsilon^2/5^8$.
The zeroth angular coefficient is $E_0^2\ge\varepsilon^2$.
All intervening coefficients are nonnegative. Put

$$
 \alpha=\min\left(1,\frac{B_+2^{-26}}{5^8},
                         \frac{B_-2^{-26}}{5^8}\right)
        =\frac{165888}{874630859375}.
$$

Since $(1-h)^6+h^6\ge1/32$, we obtain throughout the angular interval

$$
 G(k^2)\ge\frac{\alpha}{32}\varepsilon^2.
 \tag{20}
$$

For $D=0$ the reflected surplus already gives
$|I|^2-R\ge\varepsilon$, which is stronger than(18).
Otherwise use the Gram factorization. The budget implies $r\le7/6$,
and both signs of the unit center admit the uniform integral bound

$$
 |I_\pm|\le M=9(13/6)^6(7/2)^2=\frac{236513641}{20736}.
$$

Let $N=1+k^2$. Equation(7) gives $N\le(s/t)^2\le6400$.
From the signed norm identity,
$E\le N^2M^2$ and $|YkO|\le E$.
For $b<1$, both signed surpluses are positive, so

$$
 |I_\pm|^2-R
  =\frac{E\pm YkO}{N^2}
  \ge\frac{G}{2N^4M^2}
  \ge\frac{\alpha}{64\cdot6400^4M^2}\varepsilon^2.
$$

The last coefficient is exactly

$$
 C_*=\frac{531441}
 {39140572267307495558579687500000000000}>10^{-32}.
$$

At $b=1$ equation(18) reduces to the already proved nonnegative origin
inequality. This proves(18) on the full closed domain.

## 2. Perturbation to unequal light radii

Now use actual normalized reciprocals
$U,(s+\delta)v,(s-\delta)w$, with $|U|=r$, $|v|=|w|=1$,
$6r+2s=8$ and every individual radius at least $1/(1+b)$.
The two light labels may be interchanged.
The original full complex polar mean-gap lemma8148 gives

$$
 \mu-b\ge\frac{\varepsilon}{128b(1+b)}
             \ge\frac{\varepsilon}{256},\qquad 0<b<1.
 \tag{21}
$$

This is its **credited original quantitative component**; the
independently proved reviewer improvement128 to45 is unnecessary here.
The unequal-radius version of the polar lemma is essential.
No polar statement at $b=1$ is assumed.

Replace the two radii by their average s while leaving U,v,w fixed.
The new mean changes by
$-\delta\operatorname{Re}(v-w)/8$, and therefore decreases by at most
$|\delta|/4$. A looser bound $|\delta|/2$ also suffices.
If $|\delta|\le\varepsilon/128$, that looser bound and(21) show that
the replacement satisfies the actual mean hypothesis of the equal-light
origin certificate. Its radius floors and total budget are unchanged.
Thus its integral $I_0$ satisfies(18), for arbitrary phases.

Write $I_\delta$ for the original unequal-light integral. The complete
light-quadratic difference is

$$
 (1-b\tau(s+\delta)v)(1-b\tau(s-\delta)w)
 -(1-b\tau sv)(1-b\tau sw)
 =-b\tau\delta(v-w)-b^2\tau^2\delta^2vw.
$$

The floors give $|\delta|\le s-1/(1+b)\le2$. Consequently

$$
 |I_\delta-I_0|
 \le9(13/6)^6(|\delta|+\delta^2/3)
 \le L|\delta|,\qquad L=15(13/6)^6=\frac{24134045}{15552}.
 \tag{22}
$$

The actual unequal-light denominator is
$R_\delta=r^{12}(s^2-\delta^2)^2\le r^{12}s^4=R_0$.
Since $|I_0|\le M$,

$$
 |I_\delta|^2-R_\delta
 \ge10^{-32}\varepsilon^2-2ML|\delta|.
 \tag{23}
$$

Thus a sufficiently small explicit quadratic radius mismatch retains
a strict surplus. No root realizability of the averaged tuple is needed:
it is used only in the already proved abstract equal-light inequality.

## 3. Actual-polynomial unequal-light statement

Let p have degree nine with all roots in the closed unit disk, critical
multiset $\{H^6,L_1,L_2\}$, and marked root $a$, with

$$
 \rho=|a|\ge43750/46643.
$$

The light distances may now be unequal. Assume the explicit condition

$$
 \left|\frac1{|a-L_1|}-\frac1{|a-L_2|}\right|
       \le10^{-40}(1-\rho)^2.
 \tag{24}
$$

Then $S_1(a)\ge8$, strict when $\rho<1$, with equality only the same
boundary binomial. The very small constant is a conservative stability
width; no sharpness is claimed.
A critical collision remains an immediate infinite case.

Under a hypothetical $S_1\le8$, set $m=S_1/8$,
$b=m\rho$ and $c_0=46643/50000$ as in PROOF.md.
The credited global bound gives $m>c_0$, $b>7/8$ and
$\varepsilon=1-b\ge1-\rho$. For the normalized **half** light-radius
difference,

$$
 |\delta|\le
 \frac{1}{2c_0\,10^{40}}\varepsilon^2=:D_*\varepsilon^2.
$$

The exact rational checks give

$$
 D_*\le1/128,\qquad 4MLD_*\le10^{-32}.
$$

For $b<1$ equation(21) makes the averaged equal-light tuple admissible,
and(23) gives

$$
 |I_\delta|^2-R_\delta\ge\frac{10^{-32}}2\varepsilon^2>0.
$$

The actual-polynomial communication identity is unchanged, with
$R_\delta$ replacing R:
$|I_\delta|^2/R_\delta=m^{16}\prod|z_j|^2\le1$.
This is a contradiction. At $b=1$, $m=\rho=1$ and(24) forces
$\delta=0$, so the prior equal-light boundary proof applies.
This establishes the stated stability theorem.

## 4. Evidence limits

This extension uses both complete G6 supports, their normalized positive
minima, and the eighteen-case nonnegativity cover already checked for
the equal-light theorem. It adds73 exact one-dimensional coefficient
checks, a whole basis identity and rational constant gates.
Selected arithmetic on fixture metadata alone does not regenerate
the two G6 tensors. The complete verifier does so, and both final G6
checks explicitly audit every u-index through70.

The stronger original polar1/128 component is a mathematical dependency
of the unequal-light theorem, not the equal-light theorem's weaker
mean-only step. The quadratically shrinking tube does not establish
first power for arbitrary unequal light radii. The written support,
norm-factorization and perturbation arguments remain outside a formal
kernel; independent review of both new theorems is pending.
