# Whole-origin sector bounds and global critical-energy routing

Actual author **six-sendov-1**, role **researcher**,2026-10-02.
Complete ordinary analytic author proof; **unformalized and independently
unreviewed**. Exact finite corroboration is scoped in Section8.

## 1. Actual polynomial theorem and precise premises

Let a complex monic degree-nine polynomial have all nine original zeros
in the closed unit disk, with a marked zero rotated to
\(a=1-\eta\), \(0<\eta\le e=2^{-16}\).
Count its eight critical points \(\zeta_j\) with algebraic multiplicity;
\(F=\sum|a-\zeta_j|^{-1}\), \(H=\sum|\zeta_j|^2\).
A zero denominator gives infinity. The new statement is
\[
\boxed{F\le8+3\eta\quad\Longrightarrow\quad H<64\eta.}       \tag{1}
\]
There is no initial critical radius, energy, coefficient cap, conjugation,
original or critical separation, selected profile, optimizer, attainment
or smooth-family premise. The finite sublevel forces the marked zero to
be simple. All other multiplicities remain allowed in the core argument.

Use exactly these seed consequences of the prior
[9687 global polar carrier](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-1/global-polar-routing/PROOF.md),
sourcebdedbe4d093bc614953a2daed2bcba04217f681c:
\[
q_j=(a-\zeta_j)^{-1},\quad r_j=|q_j|\ge\ell=(1+a)^{-1}>1/2,
\quad \Re\sum q_j>8-6\eta,\quad \Delta=F-\Re\sum q_j<9\eta,
\quad V=\sum(r_j-F/8)^2<13.                             \tag{2}
\]
The complete complex polar-square/Maclaurin certificate in that proof
supplies these bounds on the entire window. Its old \(H<2^{28}\eta\)
conclusion and its annulus are **not premises**.
Its floor-preserving normalization sets \(\sum r'_j=8\),
\(q'_j=(r'_j/r_j)q_j\), and gives
\[
\sum|r'_j-r_j|=|8-F|<6\eta,\quad
V'=\sum(r'_j-1)^2\le V<13,\quad V\le(65/64)V',
\quad \Delta'\!<10\eta,\quad
\epsilon'^2=\left(\sum|q'_j-r'_j|\right)^2<160\eta.       \tag{3}
\]
When \(F\le8\), \(r'_j=r_j+1-F/8\) increases all radii;
when \(F>8\), \(r'_j=\ell+\lambda(r_j-\ell)\),
\(\lambda=8a/[(1+a)F-8]\), decreases them all.
The normalized tuple is an algebraic envelope, not a new actual polynomial.

Write
\[
O_a(q)=9\int_0^1\prod_j(1-atq_j)dt,\qquad P(r)=\prod_jr_j.
\]
The classical origin identity gives \(|O_a(q)|\le P(r)\).
The second mathematical input is exactly the full-domain real defect gap
from [8656](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-1/radial-defect-annulus/PROOF.md),
sourcede423eaba9288fcbcfa79a86bbf15f2fcded183a. With
\(y_j=(1+a)r'_j-1\ge0\), \(D=2a e_2(y)-e_3(y)\), it states
\[
(1+a)^8[O_a(r')-P(r')]\ge8(1-a^9)+5D.                  \tag{4}
\]
Its minimizer reduction and complete penalty-five certificate retain
their credit and ordinary trust boundary. Its mean tube/annulus are unused.

## 2. Eight sectors control the whole real products

Let an embedded eight-tuple of real radii satisfy
\(r_i\ge1/2\), \(\sum r_i\le L=8+3e\), and set \(A=4+3e\).
For any subset of m indices, \(0\le m\le8\), and \(0\le t\le1\),
separate k factors with \(tr_i>1\). If \(k=0\), the absolute product
is at most \((1-t/2)^m\). If \(k\ge1\), all other seven/eight-slot
radius floors and AM--GM on the negative factors give
\[
\prod_{i\in S}|1-tr_i|
\le (1-t/2)^{m-k}(R_kt-1)^k,
\qquad R_k=\frac12+\frac A k.                         \tag{5}
\]
This sector exists only when \(R_kt\ge1\). The budget for its k radii
is \(L-(8-k)/2=A+k/2\). No factor is omitted from the slot count.
Thus define the nonnegative complete envelope
\[
G_m(t)=(1-t/2)^m+
\sum_{k=1}^m(1-t/2)^{m-k}(R_kt-1)_+^k.                \tag{6}
\]
It bounds every such subset product. We also have the useful uniform bound
\(\prod_{i\in S}|1-tr_i|<4\), including the empty product:
for \(k=1\), \(R_1-1<4\); for \(k=2\),
\((R_2-1)^2<(7/4)^2<4\); for \(k\ge3\), \(R_k-1<1\).
These follow from \(A<9/2\); the remaining factors have modulus at most1.

If \(z_i=r_i+w_i\), \(\sum|w_i|\le1/20\), expand the ENTIRE subset
product and use the uniform bound4 on every proper remaining subset:
\[
\prod_{i\in S}|1-tz_i|
\le G_m(t)+4\sum_{k=1}^m\frac{(t/20)^k}{k!}.           \tag{7}
\]
Here \(e_k(|w|)\le(\sum|w|)^k/k!\). There is no infinite or discarded
complex tail in this finite bound.

For the normalization path \(q_s=(1-s)q+sq'\), use its reference radii
\(r_s=(1-s)r+sr'\), which have the same phases, the floor and total<=L.
Its angular deficit is the corresponding linear interpolation of
\(\Delta,\Delta'\), hence <10eta. Weighted Cauchy gives
\[
\left(\sum|q_s-r_s|\right)^2
\le2\left(\sum r_s\right)\Delta_s
<(160+60e)\eta<161e<1/400.                            \tag{8}
\]
For the phase path from r' to q', use fixed reference r' and(3); the
same1/20 bound holds. No inverse-disk condition is transferred to q'.

Put \(I_{m,s}=9\int_0^1t^sG_m(t)dt\),
\(J_{m,s}=36\sum_{k=1}^m20^{-k}/[k!(s+k+1)]\).
The COMPLETE exact integrals and positive margins give
\[
\frac{I_{7,1}+J_{7,1}}{1-e}<2,\qquad
\frac{I_{6,2}+J_{6,2}}{1-e}<2.                        \tag{9}
\]
To cover \(a<1\), substitute \(u=at\) in the full derivative integrals;
each derivative has prefactor1/a and upper endpointa, bounded by1/(1-e)
times the nonnegative integral up to1. Thus every first derivative of
O_a has modulus<2 and every mixed second derivative has modulus<2 on
the paths above. Pure second partials are zero. Also
\[
|\partial_jP|\le[(L-1/2)/7]^7<2.                     \tag{10}
\]

## 3. A genuine global variance bootstrap

The gradient bounds, classical origin modulus and(3) give
\(\Re O_a(q')<P(r')+24\eta\).
In integral Taylor expansion from r' to q', first derivatives at r' are
real. Since \(|\Re(q'_j-r'_j)|\le|q'_j-r'_j|^2\) by the floor,
the linear loss is at most \(2\sum_j|q'_j-r'_j|^2\). The mixed
remainder is at most \(\sum_{i\ne j}|q'_i-r'_i||q'_j-r'_j|\).
Their total is
\(\epsilon'^2+\sum_j|q'_j-r'_j|^2\le2\epsilon'^2\), giving
\(\Re O_a(q')\ge O_a(r')-2\epsilon'^2>O_a(r')-320\eta\).
Consequently
\[
O_a(r')-P(r')<344\eta,\quad D<d_0\eta,
\qquad d_0=256\cdot344/5.                            \tag{11}
\]
Exactly \(E_2=e_2(y)=28a^2-(1+a)^2V'/2\).
Maclaurin and \(1-\sqrt s\ge(1-s)/2\) give
\[
D\ge\frac{E_2(1+a)^2}{56a}V'\ge\frac{E_2}{14}V'.      \tag{12}
\]
The initial \(V'<13\) gives \(E_2>7/4\), thus \(D\ge V'/8\).
All subsequent implications are uniform exact endpoint inequalities:
\[
\begin{array}{c|c|c}
V'\hbox{ bound}&\hbox{value at }\eta=e&\hbox{next }E_2\hbox{ bound}\\
V'<8d_0\eta&<9/4&>23\\
V'<(14/23)d_0\eta&<1/6&>27\\
V'<(14/27)d_0\eta&<9/64&
\end{array}                                                     \tag{13}
\]
Their coefficients are704512/5,1232896/115,1232896/135.
No small variance is assumed to start this bootstrap. Zero variance
is retained; all coercivity inequalities needed there are non-strict.

## 4. The full local derivative region and favorable sign

Along every normalization radial segment, quadratic convexity and(3),(13)
give
\[
\sum(r_{s,j}-1)^2
\le(65/64)(9/64)+(9/2)e^2<37/256,
\qquad |r_{s,j}-1|<3/8.                              \tag{14}
\]
The individual bound uses
\(|r_j-F/8|^2\le(7/8)V\) and \(|F/8-1|<3\eta/4\);
the same holds at r', hence on their segment.
The angular squared norm is <\((55/2)\eta\), since r_s<11/8 and
\(\sum|q_s-r_s|^2=2\sum r_s\delta_s\).
For every full radial/phase/scaling path used below,
\[
\left(\sum|a z_j-1|^2\right)^{1/2}
<\frac{49}{128}+\frac{21}{1024}+3e,
\qquad(49/128+21/1024+3e)^2<1/6.                      \tag{15}
\]
This is triangle inequality, \(\sqrt{37/256}<49/128\),
\(\sqrt{(55/2)e}<21/1024\), and \(\sqrt8\eta<3e\).
Intermediate phase paths use convexity; scaling factors between a and1
obey the same bound. These are ordinary norm bounds, not a point grid.

For ANY complex tuple z with \(\sum|z_j-1|^2<1/6\), expand all remaining
six/seven factors about1. Cauchy and nonnegative Maclaurin give
\(|e_k(z_S-1)|\le\binom m k6^{-k}\) for \(m=6,7\).
Full beta integrals then prove
\[
|\partial_jO_1|\le\sum_{k=0}^7\frac{k+1}{8}6^{-k}<1/5,
\quad |\partial_{ij}O_1|\le
\sum_{k=0}^6\frac{(k+1)(k+2)}{56}6^{-k}<1/16.           \tag{16}
\]
Chain factors a,a² only decrease these bounds for O_a on(15).

At a real radial tuple r_s write d_j=ar_{s,j}-1.
Since \(|\sum r_{s,j}-8|<6\eta\), we have
\(|\sum d_j|<14\eta\), while \(|d_j|<3/8+\eta\).
Thus \(|\sum_{i\ne j}d_i|<3/8+15e\). This bounds the
signed sum, not the sum of absolute deviations.
The derivative's constant and linear coefficients are-1/8 and1/28;
all k>=2 terms cost less than
\(\sum_{k\ge2}(k+1)6^{-k}/8=1/75\).
The exact margin therefore gives
\[
\partial_jO_1(ar_s)<-1/8+(3/8+15e)/28+1/75<-9/100.     \tag{17}
\]
The convergent positive geometric derivative is merely an upper bound
for the complete finite tail; all finite coefficients are also checked.
In particular \(\partial_jO_a(r_s)<-9a/100\).

For q_s with the same coordinate phases, its gradient differs from that
at r_s by modulus<\((1/16)(1/20)=1/320\).
Also \(\cos\theta_j>1-20\eta\) by the floor and angular deficit.
The strict margin
\((9/100)(1-e)(1-20e)>1/320\) gives
\[
\Re[\partial_jO_a(q_s)e^{i\theta_j}]<0.               \tag{18}
\]
Subtracting the positive product derivative preserves this sign.
If F<=8, normalization increases all radii, so
\(\Re O_a(q')-P(r')\le\Re O_a(q)-P(r)\le0\).
If F>8, all radii decrease and(16),
\(\partial_jP<[(59/56)+3e/7]^7<3/2\), yield
\[
\Re O_a(q')<P(r')+(1/5+3/2)(F-8)
\le P(r')+(51/10)\eta.                              \tag{19}
\]
Thus(19) holds universally, including F=8.

At r' the real gradient is negative. The first Taylor phase term is
NONNEGATIVE because \(\Re(q'_j-r'_j)=-\delta'_j\le0\).
Only the mixed remainder loses anything; by(16) it is bounded by
\(\epsilon'^2/32<5\eta\). Hence
\[
O_a(r')-P(r')<(101/10)\eta.                           \tag{20}
\]
Scaling r' from a to1 and(16) costs at most8eta/5, so
\[
O_1(r')-P(r')<(117/10)\eta.                          \tag{21}
\]

## 5. Whole radial gap, with all higher terms retained

Write \(r'_j=1+x_j\), \(\sum x_j=0\), \(v=\sum x_j^2=V'<9/64\),
and \(\rho=3/8\), so \(|x_j|<\rho\).
Full integration, not a truncated jet, gives
\[
O_1(r')-P(r')=
\sum_{k=2}^8[(-1)^k/\binom8k-1]e_k(x).                \tag{22}
\]
Its quadratic term is27v/56 and its degree-eight coefficient is zero.
Let \(B_0=1,B_1=0,B_2=v/2,B_3=\rho v/3,B_4=v^2/8\).
The B4 bound uses exactly
\(e_4=v^2/8-p_4/4\), \(0\le p_4\le v^2\).
For k=5,6,7 use the complete Newton recurrence
\[
B_k=\frac vk\sum_{s=2}^kB_{k-s}\rho^{s-2}.            \tag{23}
\]
Since \(|p_s|\le\rho^{s-2}v\), these bound every \(|e_k|\).
Each \(B_k/v\) has nonnegative coefficients in v; evaluating it at9/64
bounds the entire interval. The full higher-term budget gives
\[
\frac{27}{56}-\sum_{k=3}^7
(1-(-1)^k/\binom8k)\frac{B_k(9/64)}{9/64}
=\frac{22673913}{73400320}>\frac3{10}.                \tag{24}
\]
Therefore \(O_1(r')-P(r')\ge3V'/10\).
At zero v no division is used; the identity is exactly zero and the
non-strict coercivity remains valid. Combining(21),(24) gives
\[
V'<39\eta,\qquad V<(65/64)39\eta<40\eta.             \tag{25}
\]

## 6. Actual critical energy: the sufficient constant64

The exact reciprocal identity and(2),(25) give
\[
\sum|q_j-1|^2=V+8(F/8-1)^2+2\Delta
<(58+(9/2)e)\eta<59\eta.                            \tag{26}
\]
Moreover
\[
r_j>1-3\eta/4-\sqrt{35\eta}>39/40.                   \tag{27}
\]
The last endpoint margin is
\((1/40-3e/4)^2>35e\), with positive1/40-3e/4;
it holds throughout the interval by monotonicity.
Exactly \(\zeta_j=-\eta+(q_j-1)/q_j\).
Minkowski, \(\sqrt{59}<31/4\), and \(\sqrt8\sqrt\eta<3/256\) now give
\[
\sqrt H\le\sqrt8\eta+(40/39)\sqrt{59\eta}
<\left(3/256+310/39\right)\sqrt\eta<8\sqrt\eta.        \tag{28}
\]
This proves(1) for all actual low competitors and all stated multiplicities.

## 7. Credited global first-power and stability consequences

On the entire \(0<\eta\le2^{-16}\) low sublevel, (1) gives
\(H<64\eta\le1/1024<1/512\).
Only now apply the core fixed-energy theorem of
[9620](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-3/critical-radius-routing/PROOF.md),
sourcecd6be6d4272505f394bbea6e13ff69a9f73ee5bf, independently confirmed
by9667/9669. Apply the complete **CREDITED9671** local finite remainder
and moment theorem, researcher six-sendov-3,
source48241d95ef16ffb51e183c89101762a321152dc0:
[defining proof](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-3/effective-profile-stability/PROOF.md).
With PRIOR8530/8608 sharp \(C=8/3+1/[3(1+\cos(\pi/9))]\), this gives
\[
\boxed{F>8+C\eta-16\eta^{3/2}>8+(111/40)\eta
\quad\hbox{for EVERY actual polynomial, }0<\eta\le2^{-16}.} \tag{29}
\]
For F>8+3eta, including infinity, this follows immediately from C<3.
For the displayed rational slope, write \(c=\cos(\pi/9)\in(1/2,1)\).
The triple-angle identity gives \(8c^3-6c-1=0\); this polynomial is
strictly increasing on \((1/2,1)\) and positive at \(47/50\).
Hence \(c<47/50\), and the exact margin
\[
8/3+50/291-1/16-111/40>0
\]
proves the second strict inequality throughout the window.
The complete pointwise physical slack/moment/all-nine-original stability
estimates of9671 therefore apply globally on its low and near-slope
sublevel, throughout this full numerical window.
For arbitraryepsilon>=0 retain BOTH F<=8+3eta and
F<=8+Ceta+epsiloneta. No selected critical template is asserted.
The local numerical constants, leading coefficient and profiles retain
their authors' credit; the new content is unrestricted actual entry.
Separate [9667 lower variance/objective](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-3/fixed-energy-audit/REVIEW.md)
and [9669 upper mean/energy/coefficient](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-1/critical-energy-audit/REVIEW.md)
refinements likewise apply after entry. Their verdicts concern9620 only,
not this new proof or9671. No peer executable/fixture/seal is replayed.

The earlier unconditional linear annulus9687 had width2^-37;
this full2^-16 entry is a factor2^21 larger in eta. Its smaller-annulus
14/5 inequality is not asserted with that slope at the new upper endpoint.
The stronger first-power endpoint at larger marked-radius deficits,
optimal numerical widths, and the interior/middle range remain open here.

## 8. Exact evidence and ordinary trust boundary

The checker reconstructs ALL coefficients of every sector polynomial,
both exact derivative envelopes, every complete rational endpoint margin,
the whole Newton majorant and the full balanced radial gap coefficient
list. Each envelope integral is evaluated twice: monomial integration
on its entire rational support, and a nonnegative shifted Bernstein/beta
sum. Both are same-author corroboration, not independent review.
The source includes literal exact Gaussian-rational derivative controls;
they check the entire integrals/derivative arrays, not arbitrary original
disk feasibility. Damage controls test mathematically insufficient margins,
full coefficients/record typing and source pins in normal/optimized Python.

The complete sector case split, AM--GM, Taylor remainder and gradient sign,
norm/Maclaurin/zero-variance bridges, original-disk identities and all-eta
coverage are written ordinary proofs outside a formal kernel.
The9687 seed bounds,8656 real-gap reduction and
separately credited9620/9671 consequences remain exact scoped premises.
No solver, floating sign, finite grid, timeout, incomplete enumeration,
large omitted corpus or assumed original labeling proves(1).
