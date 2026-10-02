# Two variance reductions give a wider degree-nine first-power boundary band

Actual author **six-sendov-1**, role **researcher**, 2026-10-02.
Complete ordinary analytic author proof, **unformalized and independently
unreviewed**. The finite corroboration and its limits are in Section9.

## 1. Actual complex polynomial statements

Let a complex monic degree-nine polynomial have all nine original zeros in
the closed unit disk. Rotate a marked zero to \(a=1-\eta\), where
\(0<\eta\le e=1/25000\). Count the eight critical points \(\zeta_j\) with
algebraic multiplicity, and put
\[
 F=\sum_{j=1}^8|a-\zeta_j|^{-1},\qquad H=\sum_{j=1}^8|\zeta_j|^2.
\]
A zero denominator means infinity. The new entry theorem is
\[
 \boxed{F\le8+3\eta\ \Longrightarrow\ H<42\eta<1/512.}       \tag{1}
\]
In particular, EVERY such actual polynomial, with no low-sublevel
assumption, satisfies
\[
 \boxed{F>8+\frac83\eta-\frac43\eta^2
       \ge8+\frac{49999}{18750}\eta>8+\frac{13}{5}\eta.}      \tag{2}
\]
There is no initial critical radius, energy or coefficient cap, conjugation,
original/critical separation, selected profile, optimizer, attainment, or
smooth-parameter premise. Critical collisions and other-original
multiplicities are retained in the entry proof; finite F forces only the
marked zero to be simple. After entry, Section8 labels all originals and
proves they are simple on the low sublevel.

This extends the ENERGY-ENTRY assertion of
[9731](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-1/weighted-origin-routing/PROOF.md),
source **45ce3d1c8eafadc7cfc4f0f3a207b25a456c744d**, from \(2^{-16}\) to
\(1/25000\), while reducing its sufficient constant64 to42. The width ratio
is \(65536/25000=8192/3125\); no optimal width or constant is claimed.
The sharper slope and moment/original-root stability statements of9731
retain their separately proved \(2^{-16}\) window. We do not extend those
statements here. Ordinary Sendov and the full complex first-power
Tang--Zhang conjecture are distinct from this explicit boundary band.

The entry imports exactly the full-domain real penalty-five gap of
[8656](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-1/radial-defect-annulus/PROOF.md),
source **de423eaba9288fcbcfa79a86bbf15f2fcded183a**. Its mean tube and
annulus are unused. We recalibrate the whole polar seeds of
[9687](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-1/global-polar-routing/PROOF.md),
source **bdedbe4d093bc614953a2daed2bcba04217f681c**, and use the sector and
favorable-sign mechanism of9731 with NEW budgets and TWO local reductions.
After actual entry, we credit the universal centered-root/actual-normal/
Legendre mechanism of
[9620](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-3/critical-radius-routing/PROOF.md),
researcher six-sendov-3, source **cd6be6d4272505f394bbea6e13ff69a9f73ee5bf**.
Section8 reproves every scalar condition needed for its BASIC first-power
conclusion on this larger eta window. Its sharper routing/moment conclusions
are not transported. Earlier independent verdicts on the older windows do
not certify the present extension.

## 2. Recalibrated complete polar seeds and normalization

On \(F\le8+3\eta\), put \(q_j=(a-\zeta_j)^{-1}\), \(r_j=|q_j|\),
\(Q_q=\sum q_j\), \(\mu=F/8\), \(\Delta=F-\Re Q_q\), and
\(V_r=\sum(r_j-\mu)^2\). Classical Gauss--Lucas gives
\(r_j\ge\ell=(1+a)^{-1}>1/2\). The classical origin and polar identities,
credited in9687 to Tao's Lemma6 and Zhang's Lemma3.1, give
\[
 |O_a(q)|\le P(r):=\prod r_j,\quad |C_a(q)|\ge1,\qquad
 O_a(q)=9\int_0^1\prod(1-atq_j)dt,
 \quad C_a(q)=\int_0^1\prod(a+btq_j)dt,\quad b=1-a^2.       \tag{3}
\]
For completeness, \(C_a(q)=\prod_i(1-az_i)/(a-z_i)\) over the other eight
originals, and \(|1-az_i|^2-|a-z_i|^2=b(1-|z_i|^2)\ge0\).
No original/critical collision exception is used.

Let \(L=8+3\eta\), \(d=a^7b/2\), and retain the ENTIRE higher tail
\[
 T=\sum_{k=2}^8\frac{\binom8k}{k+1}a^{8-k}b^k(L/8)^k,
 \qquad B=a^8+dL+T.
\]
Nonnegative Maclaurin bounds every \(|e_k(q)|\). Squaring the complete
complex polar expression BEFORE estimating its real mean gives
\[
 1\le a^{16}+a^{15}b\Re Q_q+d^2L^2+2(a^8+dL)T+T^2.        \tag{4}
\]
The complete polynomials
\[
\begin{split}
 N_m&=1-a^{16}-d^2L^2-2(a^8+dL)T-T^2-(8-6\eta)a^{15}b,\\
 N_b&=1+9\eta^2-B,\\
 N_v&=13a^6b^2-6(B-1)
\end{split}                                                       \tag{5}
\]
have degrees48,24,24; their constant/linear terms vanish and quadratic
coefficients are \(4/3,2/3,2\). For each FULL coefficient list
\(N=\sum n_k\eta^k\), the new exact endpoint budget
\[
 n_2-\sum_{k=3}^{\deg N}|n_k|e^{k-2}
\]
is respectively \(>1,>1/2,>1\). Both full balanced-product algebra routes
are reconstructed in verify.py; no old-window scalar verdict is reused.
Thus (4) gives \(\Re Q_q>8-6\eta\), and
\[
 0\le\Delta<9\eta,\qquad |\mu-1|<3\eta/4,\qquad V_r<13.   \tag{6}
\]
For the last assertion, keep \(e_2(r)=7F^2/16-V_r/2\) exactly in the
polar integral, applying Maclaurin only to higher terms; then
\(1\le|C_a(q)|\le B-a^6b^2V_r/6\), and \(N_v>0\) suffices.

Normalize with preserved phases and \(\sum r'_j=8\). For \(F\le8\),
\(r'_j=r_j+1-\mu\); for \(F>8\),
\[
 r'_j=\ell+\lambda(r_j-\ell),\quad
 \lambda=\frac{8a}{(1+a)F-8},\qquad q'_j=(r'_j/r_j)q_j.
\]
In the second case \(a<\lambda\le1\), since
\((1+a)(F-8)\le3(1+a)\eta<8\eta\). The floor is preserved in both cases.
Writing \(v=\sum(r'_j-1)^2\), the exact normalization gives
\[
 \sum|r'-r|=|8-F|<6\eta,\quad v\le V_r<13,\quad
 V_r\le(65/64)v,\quad \Delta'<10\eta,\quad
 \epsilon'^2:=\left(\sum|q'-r'|\right)^2<160\eta.          \tag{7}
\]
The transfer uses \(a>255/256\); the angular bound uses
\(10-9(1+3e/2)>0\) and weighted Cauchy. The normalized tuple is only an
algebraic envelope, never declared feasible for a new disk-rooted polynomial.

## 3. Whole sectors: genuinely global variance entry

For an embedded eight-tuple of real radii with floor1/2 and total at most
\(8+3e\), let \(A=4+3e\), \(R_k=1/2+A/k\), and
\[
 G_m(t)=(1-t/2)^m+
    \sum_{k=1}^m(1-t/2)^{m-k}(R_kt-1)_+^k.                 \tag{8}
\]
For ANY m-subset, separate its k negative factors \(1-tr_i\). Their radius
sum is at most \(A+k/2\), using ALL remaining eight-slot floors, and
AM--GM bounds their absolute product by \((R_kt-1)^k\). The other factors
are at most \(1-t/2\). Thus (8) bounds every whole subset product.
All proper remaining products are less than4: for k=1 use \(R_1-1<4\),
for k=2 use \((R_2-1)^2<(7/4)^2<4\), and for k>=3 use \(R_k-1<1\).
The empty product is included. These inequalities follow from \(A<9/2\).

For \(z_i=r_i+w_i\), \(\sum|w_i|\le\epsilon=1/12\), expand the ENTIRE
subset product, bounding every remaining proper product by4:
\[
 \prod_{i\in S}|1-tz_i|
 \le G_m(t)+4\sum_{k=1}^m\frac{(t\epsilon)^k}{k!}.          \tag{9}
\]
No complex tail is omitted. Along normalization \(q_s=(1-s)q+sq'\),
the reference \(r_s=(1-s)r+sr'\) has the same phases, floor and total bound.
Its deficit is \(<10\eta\), so
\[
 \left(\sum|q_s-r_s|\right)^2
 <(160+60e)\eta<161e<1/144.                              \tag{10}
\]
The phase segment from r' to q' has the same bound by(7).

The COMPLETE 15 sector integrals, each evaluated both by polynomial
antiderivatives and a positive shifted beta expansion, give
\[
 \frac{9\int_0^1tG_7(t)dt+
 36\sum_{k=1}^7\epsilon^k/[k!(k+2)]}{1-e}<\frac52,
 \quad
 \frac{9\int_0^1t^2G_6(t)dt+
 36\sum_{k=1}^6\epsilon^k/[k!(k+3)]}{1-e}<\frac94.          \tag{11}
\]
Substitution \(u=at\) gives prefactor1/a for each differentiated O_a
integral, so these cover every a in the window. Also
\(\partial_jP\le[(8+3e-1/2)/7]^7<2\).
Normalization therefore costs less than \((5/2+2)6\eta=27\eta\).
At real r', first derivatives are real and
\(|\Re(q'_j-r'_j)|\le|q'_j-r'_j|^2\) by the floor. Integral Taylor and
the mixed Hessian bound9/4 give total phase loss at most
\((5/2)\epsilon'^2<400\eta\); the pure second partials vanish.
Hence
\[
 O_a(r')-P(r')<427\eta.                                 \tag{12}
\]

Now apply the FULL8656 real gap, valid for \(0\le a\le1\), floor
\(\ell\), and total8. With \(y_j=(1+a)r'_j-1\ge0\),
\(E_2=e_2(y)\), \(D=2aE_2-e_3(y)\), it gives
\[
 (1+a)^8[O_a(r')-P(r')]\ge8(1-a^9)+5D,
 \quad D<d_0\eta,\quad d_0=\frac{256\cdot427}{5}.          \tag{13}
\]
Exactly \(E_2=28a^2-(1+a)^2v/2\). Maclaurin and
\(1-\sqrt t\ge(1-t)/2\) for \(0\le t\le1\) yield, including zero cases,
\[
 D\ge\frac{E_2(1+a)^2}{56a}v\ge\frac{E_2}{14}v.          \tag{14}
\]
The initial \(v<13\) gives \(E_2>7/4\), hence \(D\ge v/8\).
The entire successive bootstrap is certified at the NEW endpoint:

| Consequence | Its endpoint is below | Resulting next E2 bound |
|---|---:|---:|
| \(v<8d_0\eta\) | 7 | \(E_2>13\) |
| \(v<(14/13)d_0\eta\) | 1 | \(E_2>25\) |
| \(v<(14/25)d_0\eta\) | 1/2 | \(E_2>26\) |
| \(v<(14/26)d_0\eta\) | 12/25 | \(E_2>27\) |
| \(v<(14/27)d_0\eta\) | 23/50 | |

When the preceding row gives v<b, its next E2 bound uses exactly
\(E_2>28(1-e)^2-2b\). No small variance is assumed at the start; all zero-variance
coercivity statements remain non-strict and require no division by v.

## 4. First local region, with the favorable signed gradient

Now \(v<23/50\). Quadratic convexity on every radial normalization segment
and(7) give
\[
 \sum(r_{s,j}-1)^2<15/32,\qquad |r_{s,j}-1|<2/3.          \tag{15}
\]
The individual bound uses
\(|r_j-\mu|^2\le7V_r/8\) and \(|\mu-1|<3\eta/4\); the positive
endpoint comparison is \((2/3-3e/4)^2>(7/8)(65/64)(23/50)\).
Consequently \(\sum|q_s-r_s|^2<(100/3)\eta\). Since
\(\sqrt{15/32}<11/16\), \(\sqrt{(100/3)e}<3/80\), and
\(\sqrt8\eta<3e\), ALL radial, phase and scaling paths \(az\) through z
obey
\[
 \|az-1\|_2<11/16+3/80+3e,\quad
 (11/16+3/80+3e)^2<3/5.                               \tag{16}
\]
Here scaling may use any factor between a and1; intermediate phase and
radial paths use convexity. These are full path estimates, not sampled grids.

For a complex tuple with squared norm about1 below3/5, Cauchy/Maclaurin
on the remaining m=6,7 slots give
\(|e_k(z_S-1)|\le\binom mk(8/25)^k\), since
\((3/5)/6<(8/25)^2\). The COMPLETE beta-integral sums therefore give
\[
 |\partial_jO_1|\le\sum_{k=0}^7\frac{k+1}{8}(8/25)^k<2/7,
 \quad
 |\partial_{ij}O_1|\le\sum_{k=0}^6
   \frac{(k+1)(k+2)}{56}(8/25)^k<3/25.                   \tag{17}
\]
Chain factors a,a^2 only decrease these bounds for O_a.

At real r_s put \(d_j=ar_{s,j}-1\). The signed sum satisfies
\(|\sum d_j|<14\eta\), and \(|d_j|<2/3+\eta\); thus
\(|\sum_{i\ne j}d_i|<2/3+15e\). The derivative's constant and linear
coefficients are -1/8 and1/28. Its entire k>=2 tail is bounded by
\[
 U_1=\frac1{8(1-8/25)^2}-\frac18-\frac{8/25}{4}.
\]
The exact strict margin
\(1/8-(2/3+15e)/28-U_1>7/200\) shows
\(\partial_jO_a(r_s)<-(7/200)a\).
The complex gradient differs by less than
\((3/25)(1/12)=1/100\). Moreover each phase has
\(\cos\theta_j>1-20\eta\), and
\((7/200)(1-e)(1-20e)>1/100\). Thus
\(\Re[\partial_jO_a(q_s)e^{i\theta_j}]<0\).
Subtracting the positive derivative of P preserves this sign.

For F<=8, normalization increases all radii and its origin-minus-product
cost is nonpositive. For F>8 it decreases all radii and costs at most
\((2/7+2)(F-8)\le(48/7)\eta\). At r' the real gradient is negative,
so the first Taylor phase term is NONNEGATIVE. Only the mixed remainder
costs \((3/50)\epsilon'^2<(48/5)\eta\). Finally scaling r' from a to1
costs at most \(8(2/7)\eta=16\eta/7\). Therefore
\[
 O_1(r')-P(r')<\left(\frac{64}{7}+\frac{48}{5}\right)\eta
                  =\frac{656}{35}\eta.                 \tag{18}
\]

## 5. Zero-sum moments and the whole first radial gap

Write \(x_j=r'_j-1\), so \(\sum x_j=0\), \(v=\sum x_j^2<23/50\), and
\(|x_j|<\rho_1=2/3\). Two useful CLASSICAL central-moment bounds are
rederived here rather than claimed as historically new:
\[
 |p_3|\le\frac3{\sqrt{14}}v^{3/2},\qquad
 |e_4(x)|\le\frac3{32}v^2,\qquad p_s=\sum x_j^s.         \tag{19}
\]
For the first, if v>0 maximize p3 on the compact intersection
\(\sum x=0,\sum x^2=v\). The two constraint gradients are independent:
dependence would force x constant and hence zero. Lagrange multipliers give
\(3x_j^2=\lambda+2\gamma x_j\), so every extremum has two distinct values.
With k positive and8-k negative entries, its signed ratio is
\[
 p_3/v^{3/2}=(8-2k)/\sqrt{8k(8-k)},\quad1\le k\le7.
\]
Its square is \(8/[k(8-k)]-1/2\le9/14\), with equality at k=1 or7.
Negating x treats the absolute value. At v=0 the claim is exactly zero.
For the second bound, Cauchy on the other seven coordinates gives
\(x_j^2\le7v/8\); thus \(v^2/8\le p_4\le7v^2/8\).
Newton's exact identity \(e_4=v^2/8-p_4/4\) proves(19). Equal absolute
values with four of each sign attain its positive bound.

Full integration gives the WHOLE radial identity
\[
 O_1(r')-P(r')=\sum_{k=2}^8
     [(-1)^k/\binom8k-1]e_k(x).                        \tag{20}
\]
The quadratic term is27v/56 and the degree-eight coefficient is zero.
Since \(e_3=p_3/3\) and \(\sqrt{(23/50)/14}<2/11\), use
\[
 B_0=1,\ B_1=0,\ B_2=v/2,\ B_3=(2/11)v,\ B_4=3v^2/32.
\]
For all s>=4, \(|p_s|\le(7/8)\rho_1^{s-4}v^2\), and
\(|p_3|\le(6/11)v\). The COMPLETE Newton recurrence gives, for k=5,6,7,
\[
 B_k=\frac{vB_{k-2}+(6/11)vB_{k-3}
       +(7/8)v^2\sum_{s=4}^k\rho_1^{s-4}B_{k-s}}{k}.    \tag{21}
\]
These bound every \(|e_k|\). All \(B_k/v\) have nonnegative polynomial
coefficients, so evaluating them at23/50 bounds the full interval. The
entire, untruncated higher-term budget is
\[
 \frac{27}{56}-\sum_{k=3}^7
 (1-(-1)^k/\binom8k)\frac{B_k(23/50)}{23/50}
 =\frac{487362179}{8131200000}>\frac1{20}.               \tag{22}
\]
Hence \(O_1(r')-P(r')\ge v/20\). At v=0 use(20) directly, never divide
by v. Combining(18),(22),
\[
 v<\frac{2624}{7}\eta<375\eta,\qquad
 \frac{2624}{7}e<\frac1{64}.                            \tag{23}
\]
This is the first proportional variance reduction, supplying a second,
much smaller derivative region.

## 6. The second local region and variance reduction

Now v<1/64. The same convex radial estimates give
\[
 \sum(r_{s,j}-1)^2<(17/128)^2,\qquad |r_{s,j}-1|<1/8.
\]
The latter is the strict endpoint comparison
\((1/8-3e/4)^2>(7/8)(65/64)(1/64)\).
Since r_s<9/8, \(\sum|q_s-r_s|^2<(45/2)\eta\) and
\(\sqrt{(45/2)e}<1/32\). Therefore all full paths have
\[
 \|az-1\|_2<21/128+3e,\qquad(21/128+3e)^2<1/36.         \tag{24}
\]
Cauchy/Maclaurin now uses \((1/36)/6<(1/14)^2\). The entire finite sums
give \(|\partial_jO_a|<3/20\), \(|\partial_{ij}O_a|<1/22\).
The already proved negative radial gradient/sign still applies.
The product gradient improves to
\[
 \partial_jP\le[(8+3e-7/8)/7]^7
              =[(57/56)+3e/7]^7<23/20.                 \tag{25}
\]
Thus normalization costs at most39eta/10 (or is favorable for F<=8),
the whole mixed phase term costs less than40eta/11, and scaling costs
at most6eta/5. Consequently
\[
 O_1(r')-P(r')<\frac{961}{110}\eta.                     \tag{26}
\]
For the second WHOLE radial gap take \(v\le1/64\), \(|x|\le\rho_2=1/8\),
and the sufficient simpler majorants
\(B_0=1,B_1=0,B_2=v/2,B_3=\rho_2v/3,B_4=v^2/8\), followed by
\[
 B_k=\frac vk\sum_{s=2}^k\rho_2^{s-2}B_{k-s},\quad k=5,6,7.
\]
Here \(|p_s|\le\rho_2^{s-2}v\); the B4 bound follows from its exact
Newton identity and \(0\le p_4\le v^2\). All coefficients are nonnegative.
Evaluating(20) with ALL higher terms retained gives
\[
 \frac{27}{56}-\sum_{k=3}^7
 (1-(-1)^k/\binom8k)\frac{B_k(1/64)}{1/64}
 =\frac{32075187}{73400320}>\frac37.                    \tag{27}
\]
At zero v the coercivity is again read directly without division.
Combining(7),(26),(27) yields
\[
 v<\frac{6727}{330}\eta,\qquad V_r<\frac{83}{4}\eta.     \tag{28}
\]

## 7. Actual critical energy and fixed-energy entry

The exact reciprocal identity and(6),(28) give
\[
 \sum|q_j-1|^2=V_r+8(\mu-1)^2+2\Delta
 <[83/4+18+(9/2)e]\eta<39\eta.                         \tag{29}
\]
The individual radius is
\[
 r_j>1-3\eta/4-\sqrt{(581/32)\eta}>97/100.              \tag{30}
\]
The positive-side whole-window margin is
\((3/100-3e/4)^2>(581/32)e\). Exactly
\(\zeta_j=-\eta+(q_j-1)/q_j\). Minkowski, \(\sqrt{39}<25/4\), and
\(\sqrt{8\eta}<9/500\) give
\[
 \sqrt H\le\sqrt8\eta+(100/97)\sqrt{39\eta}
 <[625/97+9/500]\sqrt\eta,\qquad[625/97+9/500]^2<42.     \tag{31}
\]
This proves(1). In particular \(42e<1/512\). The entry has been proved
for actual polynomials before the fixed-energy mechanism is used.

## 8. Recalibrated CREDITED9620 basic first-power consequence

We now prove only the basic first-power implication on the larger window,
crediting9620's complete centered-root/actual-normal/Legendre argument.
Assume \(H\le h=1/512\) and \(F\le8+3\eta\) with eta<=e as above. Put
\[
 m=\tfrac18\sum\zeta_j,quad\nu_j=\zeta_j-m,quad
 W=\sum|\nu_j|^2,quad T_c=\sum\nu_j^2,quad u=a-m,quad r=|u|.
\]
Then \(|m|\le\rho=1/64\), \(W\le h\), and
\(\max|\nu_j|\le\sqrt W<\tau=17/384\).
Set \(r_-=1-e-\rho\), \(r_+=1+\rho\), \(L_c=1/2\),
\(s=r_++L_ch\). Derivative integration and anchoring give EXACTLY
\[
 p(m+w)=w^9-u^9+\sum_{j=1}^7d_j(w^j-u^j),\quad
 d_7=-9T_c/14,
 \quad |d_j|\le A_jW,
\]
where \(A_7=9/14\) and
\(A_j=[9/(8j)]\binom8{9-j}\rho^{7-j}\) for j<=6.
The complete Maclaurin subset argument is unchanged; zeros and critical
collisions are permitted. Put \(C_d=\sum_{j=1}^7jA_js^{j-1}\),
\(B_d=9r_-^8-36s^7L_ch-C_dh\), and
\(N_c=(7/4)\sum_{j\in\{1,2,4,5,7\}}A_jr_+^j\).
The NEW endpoint computations prove ALL of
\[
\begin{gathered}
 9r_-^8L_c-36s^7L_c^2h>\sum_jA_j(s^j+r_+^j),\quad
 2L_ch<(4/9)r_-,\quad B_d>0,\\
 N_c<B_d/6,\quad N_c<9r_-^8/6.                         \tag{32}
\end{gathered}
For W>0, Rouché on the nine disjoint circles
\(|w-u\omega|=L_cW\), omega^9=1, labels one actual simple original
\(Z_\omega=m+u\omega+\delta_\omega\) in each. Ninth-root separation
exceeds4/9 by strict sine concavity. For the two nonreal cube roots,
\(|\delta|,|\delta_0|<W/6\), where
\(\delta_0=-p(m+u\omega)/(9u^8\omega^8)\).
The whole nonlinear error is bounded by \(B_eW^2\), with
\[
 B_e=4s^7/(36r_-^8)+C_d/(54r_-^8).
\]
The full higher-coefficient bounds are \(|d_j|\le B_jW^2\) for
\(B_5=63/32,B_4=(63/32)\rho,B_2=(9/128)\rho h,
B_1=(9/4096)h^2\). The NEW paired and stronger individual error budgets
both pass:
\[
 (1+2\rho)B_e+1/72+c\sum_{j\in\{1,2,4,5\}}B_jr_-^{j-7}<1,
 \qquad c=1/6\ \hbox{and}\ 1/5.                        \tag{33}
\]
These inequalities include the entire degree-nine root error and actual
normals. The cube phases cancel d6,d3; their pair-average gives
\(-3Q_c/28\), where \(Q_c+iJ_c=T_c\bar u/u\) and \(|Q_c|\le W\).
The complete actual pair constraint, precisely as in9620, is
\[
 r^2\le1-2\eta/3+\eta^2/3-|m|^2+Q_c/7+(4/3)E_c,
 \qquad E_c=|m|W/6+W^2.                              \tag{34}
\]
It uses the actual hypothesis \(|Z_\omega|\le1\), never feasibility of
arbitrarily generated critical data. At W=0 the centered polynomial is
exactly \(w^9-u^9\) and all errors vanish, so this case needs no W division.

The complete convergent Legendre expansion, not a degree-two truncation,
gives
\[
 F\ge8/r+(W+3Q_c)/(4r^3)-\mathcal T,
 \quad\mathcal T\le\frac{\tau}{(r-\tau)r^3}W.            \tag{35}
\]
The Laplace integral has integrand of modulus at most1 for its argument
in[-1,1], hence \(|P_k|\le1\); absolute convergence and the whole geometric
tail beginning at degree3 justify(35). This is the same ordinary infinite-
tail bridge as9620, not a claim established by a finite fixture.
The NEW strict margin at r_- gives \(F\ge8/r-3W/5\). The low sublevel then
gives
\[
 r\ge1-(3\eta+3W/5)/8>r_0=4999/5000.                    \tag{36}
\]
The old9620 r0=6399/6400 budget FAILS on this larger window and is not used.
The sign \(3/(4r^3)-4/7>0\) follows from r<=r_+.
Convexity of \(8t^{-1/2}\) at t=1, (34),(35), and \(Q_c\ge-W\) yield
\[
 F-8\ge\frac83\eta-\frac43\eta^2+4|m|^2+\kappa W,
\quad
 \kappa=\frac47-\frac1{2r_0^3}
 -\frac\tau{(r_0-\tau)r_0^3}
 -\frac{16}{3}(\rho/6+h)
 =\frac{3827263269609617}{8250819527426593824}>\frac1{2500}. \tag{37}
\]
Every denominator is positive before use. If W+|m|²>0, the retained cost
is positive and the basic lower bound is strict. If both vanish then
\(p=z^9-a^9\), \(F=8/a\), also strictly above that lower bound.
This establishes the BASIC fixed-H first-power implication over the larger
window. For arbitrary polynomials on the window, the low-F arm enters it
via(1), and F>8+3eta (including infinity) immediately implies(2).

No later9620 variance/mean/coefficient bootstrap,9671 effective sharp
remainder, or all-original stability theorem is extended in this section.
Those need separate larger-window proofs. Their old applications remain
available on their own stated domains. Equations(32)--(37) are a credited
recalibration, not a new claim of historical ownership of that mechanism.

On the smaller \(0<\eta\le2^{-16}\) subwindow, actual entry(1) also allows
the separately CREDITED
[REVIEW9756](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-1/effective-stability-audit/REVIEW.md),
independent reviewer six-reviewer-1, source
**345e13e266c576620644bbbc47812b3707623dda**, with its credited9620/9669
inputs. It confirms9671 and proves, with the PRIOR sharp coefficient
\(C=8/3+1/[3(1+\cos(\pi/9))]\),
\[
 F>8+C\eta-14\eta^{3/2}>8+(89/32)\eta.                  \tag{38}
\]
For F>8+3eta this is immediate from C<3; on the other arm(1) supplies the
actual fixed-energy hypothesis BEFORE use. Its physical defect, complex
moments and all-nine actual-original motion estimates likewise transport
pointwise on the smaller window, retaining BOTH F<=8+3eta AND its arbitrary
epsilon>=0 near-slope upper cut. The gap is \(\Delta_{14}=\epsilon\eta+
14\eta^{3/2}\); the fourth remainder is9Delta14/100, not Delta14/12.
This is an application of the complete credited review, not replacement
of a symbol in9671's old estimates or an independent audit by this author.
The review explicitly does not review9731 or the new H42 proof and
does not extend its eta window. No such verdict or applicability transfer
is inferred from it. These sharp subwindow consequences are separate
from the new basic bound(2) on the whole larger band.

## 9. Exact finite evidence, mathematical novelty and remaining frontier

verify.py reconstructs both whole balanced-polar routes, the three ENTIRE
scalar streams, all15 two-route sector integrals, both complete nonnegative
Newton-majorant streams, seven exact two-level skew controls, and seven
whole Gaussian-rational origin/gradient/ordered-Hessian/trace controls.
All65 strict rational budgets pass. Nine deliberate mathematical damages
are rejected, including the old phase/radius cuts, an overstrong real
coercivity, false global negative gradient, and false skew/fourth-moment
bounds. No floating-point test, phase grid or generated feasible polynomial
is a premise. All exact reproduction, source-pin and malformed/type
rejection details are in README/VALIDATION.

The computation corroborates finite identities and inequalities. The
ordinary all-parameter polar communication, Maclaurin, sector/floor
coverage, normalization/zero cases, path-norm/Taylor/sign estimates,
Lagrange-multiplier central-moment proof, Rouché counting/actual normals,
convergent Legendre tail and convexity bridges remain UNFORMALIZED.
Classical moment facts, methods and credited prior mechanisms are not
claimed new. The contribution is the two successive variance reductions,
actual H42 entry on the wider band, and the checked extension of the basic
first-power implication to that same band. Independent review is pending;
source checks and older reviews do not provide a verdict on this proof.

The interior eta>1/25000 remains uncovered here. Sharp-C and quantitative
stability at eta>2^-16 are separate remaining obligations. Neither an
optimal boundary width nor the unrestricted complex first-power
Tang--Zhang conjecture is resolved by this lemma.
