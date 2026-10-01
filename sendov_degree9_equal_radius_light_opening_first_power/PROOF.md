# Equal-radius light opening in an explicit heavy-direction cone

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
Complete ordinary author argument with exact finite evidence;
unformalized and independently unreviewed. The two mathematical premises
and arithmetic provenance are in [LITERATURE.md](LITERATURE.md).

## 1. Polynomial sectors

Let a complex degree-nine polynomial have all zeros in the closed unit
disk and critical multiset

\[
 \{H^6,L_1,L_2\},
\]

with coincidences allowed and every algebraic multiplicity counted.
Fix a zero \(a\). A zero denominator contributes infinity. For \(a\ne0\),
rotate the polynomial so that the marked zero is \(\rho=|a|>0\), and use
\(H,L_1,L_2\) for the rotated critical points. Define reciprocal phases

\[
 u=\frac{|\rho-H|}{\rho-H},\quad
 v=\frac{|\rho-L_1|}{\rho-L_1},\quad
 w=\frac{|\rho-L_2|}{\rho-L_2}.
\]

Assume the light distances agree, the heavy point is at least as near,
and its direction satisfies the explicit cone condition:

\[
 |\rho-L_1|=|\rho-L_2|,\quad
 |\rho-H|\le |\rho-L_1|,\quad
 \Re u\ge f(\rho):=\frac{\rho(4+3\rho)}{3+4\rho}.          \tag{1}
\]

The simpler condition \(\Re u\ge(1+6\rho)/7\) implies the last inequality.

Either of the following additional conditions suffices:

1. The light points reflect in the axis through zero and the marked
   zero: in the rotated coordinates, \(L_2=\overline{L_1}\).
2. The reciprocal light phases have nonzero sum, their shorter-arc
   angular center is \(q=(v+w)/|v+w|\), and
   \[
     |q-1|\le\frac1{13824}.                            \tag{2}
   \]

Then the first-power Tang--Zhang inequality holds:

\[
 S_1(a)=6|a-H|^{-1}+|a-L_1|^{-1}+|a-L_2|^{-1}\ge8.     \tag{3}
\]

It is strict for \(|a|<1\). Equality in either sector is exactly
\(p(z)=C(z^9-a^9)\), \(C\ne0,\ |a|=1\). At \(a=0\), strictness holds
without any sector condition. The heavy point may be nonreal and the
polynomial coefficients need not be real. The individual light opening
angle is not required to be small; (2) controls its center.

This is an equal-light-radius sector with a heavy-direction restriction,
not the full complex critical6+1+1 or unrestricted degree-nine theorem.

## 2. The normalized opening lemma

The new estimate is an abstract integral statement. Suppose

\[
 0\le b\le1,\quad
 1\le r\le1+\frac b{3(1+b)},\quad
 s=4-3r,\quad U=ru,\quad |u|=|q|=1,
\]
\[
 x=\Re U\ge r-(1-b),\quad 0\le c\le1.                \tag{4}
\]

In particular \(s\ge(1+b)^{-1}\ge1/2\), \(s\le1\),
and weighted AM--GM gives \(r^{12}s^4\le1\). Put

\[
 A=9\int_0^1(1-b\tau U)^6\,d\tau,\quad
 B=9b\int_0^1\tau(1-b\tau U)^6\,d\tau,\quad
 C_0=9b^2\int_0^1\tau^2(1-b\tau U)^6\,d\tau,
\]
\[
 I(c)=A-2scqB+s^2q^2C_0,\quad I_1=I(1),\quad
 N(c)=\frac{|I(c)|^2}{r^{12}s^4}.                     \tag{5}
\]

For unit phases \(v,w\) with \(v+w=2cq\), \(vw=q^2\), (5) equals
the actual eight-factor integral

\[
 I(c)=9\int_0^1(1-b\tau U)^6(1-b\tau sv)(1-b\tau sw)\,d\tau.
\]

The conclusions, without any mean or critical-disk assumptions, are

\[
 q=1\ \Longrightarrow\ N(c)-N(1)\ge\frac{b(1-c)}{64}, \tag{6}
\]
\[
 |q-1|\le1/13824\ \Longrightarrow\
 N(c)-N(1)\ge\frac{b(1-c)}{128}.                     \tag{7}
\]

If additionally \((6\Re U+2s\Re q)/8\ge b\), the credited full complex
6+2 abstract origin lemma, with \(\eta=(r-1)/2\in[0,1/12]\), gives
\(N(1)\ge1\), strictly for \(b<1\). Thus (6)--(7) produce a positive
angular gain exactly where an unequal-radius splitting gain vanishes.
No replacement of critical points is asserted to preserve a disk-root
polynomial; only this abstract integral premise is used.

## 3. Exact opening identity and the new reflection Gram

Define

\[
 T(q)=\Re(qB\overline{I_1}).
\]

Since \(I(c)=I_1+2s(1-c)qB\), direct expansion yields

\[
 |I(c)|^2-|I_1|^2
 =4s(1-c)T(q)+4s^2(1-c)^2|B|^2.                     \tag{8}
\]

At reflection \(q=1\), the real Gram is

\[
 T(1)=\Re(B\overline A)-2s|B|^2+s^2\Re(B\overline{C_0}). \tag{9}
\]

The uniform new bound is

\[
 \boxed{\quad T(1)\ge b/128\quad}                     \tag{10}
\]

throughout (4). The sign is invariant under conjugating the heavy
phase; its imaginary part is never assigned a favorable sign.

[kernel.py](kernel.py) reconstructs (9) over \(\mathbb Q[b,r,x]\).
The coefficients of the heavy moments are

\[
 a_{\ell,j}=\frac{9(-1)^j\binom6j}{j+\ell+1},\qquad
 M_\ell=\sum_{j=0}^6 a_{\ell,j}b^{j+\ell}U^j.
\]

For each of the three required Grams, use

\[
 \Re(U^j\overline U^k)=r^{2\min(j,k)}R_{|j-k|},\quad
 R_0=1,\ R_1=x,\ R_j=2xR_{j-1}-r^2R_{j-2}.          \tag{11}
\]

Every resulting coefficient agrees with a separate full real/imaginary
product in the quadratic extension \((\Im U)^2=r^2-x^2\).
The binomial moments separately agree with the endpoint formulas

\[
 A=\frac97\sum_{j=0}^6h^j,\quad
 B=\frac{9b}{56}\sum_{j=0}^6(j+1)h^j,\quad
 C_0=\frac{b^2}{56}\sum_{j=0}^6(j+1)(j+2)h^j,
 \quad h=1-bU.                                      \tag{12}
\]

The raw Gram has147 nonzero monomials and an exact factor \(b\).
The quotient at \(b=0\) is \(81/2\). Parametrize the entire domain (4):

\[
 r=1+\frac{by}{3(1+b)},\quad
 x=r-(1-b)(1-z),\quad 0\le b,y,z\le1.                \tag{13}
\]

All projections in (13) satisfy \(0\le x\le r\). The mapped polynomial

\[
 P(b,y,z)=(1+b)^{14}\left(\frac{T(1)}b-\frac1{128}\right) \tag{14}
\]

has1076 monomials and tensor degree \((28,14,6)\). The interpretation at
\(b=0\) uses the exact quotient. Two complete substitution algorithms
agree for each phase/radius map, with the positive denominator
\((1+b)^{14}\) explicitly cleared.

The exact Bernstein certificate covers the closed unit cube with the
following disjoint-interior cells; the \(y\) interval is always \([0,1]\):

| \(b\) | \(z\) | Minimum Bernstein coefficient of (14) |
|---|---|---|
| \([0,1/2]\) | \([0,1]\) | \(5183/128\) |
| \([1/2,1]\) | \([1/2,1]\) | \(163964314801699988035/587178711120347136\) |
| \([3/4,1]\) | \([0,1/2]\) | \(657399124513082742581/2305843009213693952\) |
| \([1/2,3/4]\) | \([1/4,1/2]\) | \(1176090932513422466449474939/6372449863932251272642560\) |
| \([1/2,5/8]\) | \([0,1/4]\) | \(139755594554855355028454755429/15615657033030302092517965824\) |
| \([5/8,3/4]\) | \([0,1/4]\) | \(245153877309866871090209261251183/41319028509398179336802537570304\) |

Each cell has all3045 coefficients, all strictly positive:18270 signs.
The complete subdivision tree is checked, as is total exact volume one.
On the global tensor and every cell the full inverse recovers the
corresponding power polynomial. Every cell entry agrees between direct
affine substitution and repeated de Casteljau subdivision. All11
nontrivial affine axis transforms agree with the full Fraction reference.
Thus no coefficient is omitted, and positivity of the Bernstein basis
proves (10) on the whole domain, including its faces. The numerical
diagnostics that suggested the cone are not inputs to this proof.

## 4. Stability of the angular center

The cone in (4) also yields a useful analytic bound. Convexity in \(\tau\)
gives

\[
 |1-b\tau U|^2\le\max\{1,|1-bU|^2\},
\]
\[
 |1-bU|^2\le1-2br+2b(1-b)+b^2r^2.                   \tag{15}
\]

The right side is convex in \(r\in[1,7/6]\). At the endpoints it equals
\(1-b^2\) and \(1-b/3-23b^2/36\), respectively, both at most one.
Consequently

\[
 |A|\le9,\quad |B|\le9b/2,\quad |C_0|\le3b^2.       \tag{16}
\]

Put \(D=B\overline A+s^2\overline B C_0\). Exactly,

\[
 T(q)=\Re(qD)-2s|B|^2,\quad
 |D|\le|B|(|A|+s^2|C_0|)\le54b.                    \tag{17}
\]

By (10), (17) and the first sign \(|q|=1\),

\[
 T(q)\ge b/128-54b|q-1|\ge b/256                    \tag{18}
\]

under (2), since \(54\cdot256=13824\). Insert (10) or (18) in (8),
drop its nonnegative quadratic term, divide by \(r^{12}s^4\le1\),
and use \(s\ge1/2\). This proves (6)--(7). The constants and cone are
sufficient uniform choices; optimality is not claimed.

## 5. Deduction for actual disk-root polynomials

Assume \(0<\rho<1\), the marked zero is simple, and (3) fails or is an
interior equality. With the original reciprocal magnitudes \(R,L\), put

\[
 m=S_1/8=(6R+2L)/8\le1,\quad
 p_m(z)=m^9p(z/m),\quad b=m\rho,
\]
\[
 U=\frac{1}{b-mH}=\frac Rm u=ru,\quad
 V=sv,\quad W=sw,\quad s=L/m=4-3r.                 \tag{19}
\]

The scaled polynomial is still an actual degree-nine disk-root
polynomial. Gauss--Lucas gives \(|b-1/U|,|b-1/V|,|b-1/W|\le1\), hence
every radius is at least \((1+b)^{-1}\). Since \(R\ge L\),

\[
 r\ge1,\quad r\le R_{\max}(b):=1+\frac b{3(1+b)}.
\]

In particular \(r\le R_{\max}(\rho)\), because \(b\le\rho\). The cone
condition (1) is exactly

\[
 1-\Re u\le\frac{1-\rho}{R_{\max}(\rho)}.
\]

It implies \(r-\Re U\le1-\rho\le1-b\), the projection condition (4).
The stated simpler condition suffices because

\[
 (1+6\rho)(3+4\rho)-7\rho(4+3\rho)=3(1-\rho)^2\ge0.
\]

At \(b>0\), each actual equal-radius light disk forces

\[
 \Re v,\Re w\ge\frac{1-(1-b^2)s^2}{2bs}\ge b/2>0,  \tag{20}
\]

where the last inequality follows from \(s\le1\).
Thus their sum is nonzero, and the shorter-half-angle representation
has \(v+w=2cq\), \(vw=q^2\), \(0<c\le1\), \(\Re q>0\).
In the reflection sector, \(w=\overline v\) and (20) makes \(q=1\).
In the second sector, (2) already bounds this exact center.

The actual polar communication identity gives

\[
 C=\int_0^1(b+(1-b^2)\tau U)^6
                 (b+(1-b^2)\tau V)(b+(1-b^2)\tau W)\,d\tau
   =\prod_{j=1}^8\frac{1-bz_j}{b-z_j},\quad |C|\ge1. \tag{21}
\]

Here \(z_j\) are the other scaled zeros. The credited full complex
6+1+1 polar lemma applies to these actual reciprocal data, with
\(6r+s+s=8\), and forces

\[
 \mu=(6\Re U+s\Re v+s\Re w)/8>b.                    \tag{22}
\]

Merging the phases increases this real mean:

\[
 (6\Re U+2s\Re q)/8-\mu=s(1-c)\Re q/4\ge0.
\]

The full complex6+2 abstract origin lemma therefore gives \(N(1)>1\)
for \(b<1\). By (6) or (7), \(N(c)>1\). But the actual origin
communication identity gives

\[
 \frac{I(c)}{U^6VW}=\prod_{j=1}^8(-z_j),\quad
 N(c)=\prod_{j=1}^8|z_j|^2\le1,                      \tag{23}
\]

a contradiction. This establishes interior strictness.
The scaled-root bound even gives \(N(c)\le m^{16}\); the weaker (23)
is already sufficient.

At \(a=0\), the derivative product gives \(\prod|Q_j|\ge9\), so
\(S_1\ge8\,9^{1/8}>8\). At a simple boundary zero, rotate to \(a=1\).
The classical identity \(\sum Q_j=2\sum(1-z_j)^{-1}\) and
\(\Re(1-z_j)^{-1}\ge1/2\) give \(S_1\ge8\).
Equality forces every critical reciprocal to be positive real.
Since the two light distances agree, their reciprocals coalesce.
The normalized6+2 origin equality case then forces every reciprocal
to equal one; all critical points are zero and \(p=C(z^9-1)\).
Conversely this binomial attains equality. Rotation restores the stated
classification. Critical/marked collisions contribute infinity.

## 6. Exact examples and the failed broader sign

To show that the sectors include genuinely complex, nonradial examples,
take

\[
 a=19/20,\quad H=1/100+i/1000,\quad
 L_1=-1/100+i/4,\quad L_2=-1/100-i/4,
\]
\[
 p(z)=F(z)-F(a),\quad F'=9(z-H)^6(z-L_1)(z-L_2),\quad F(0)=0.
\]

The heavy distance squared is883601/1000000 and the light distance
squared is9841/10000. The original cone is checked by positive squares.
The sum of absolute real and imaginary parts of every nonleading
coefficient of the monic polynomial is

\[
 159355844273498686350919/200000000000000000000000<1.
\]

Rouché on the unit circle puts all nine zeros strictly inside. The
marked zero is simple, the three critical locations are distinct and
nonreal, and the coefficients are nonreal. The light unit-phase chord
squared is2500/9841>1/4, so the opening is not a tiny perturbation.

There is also an exact example satisfying (2) without reflection.
Multiply both original light reciprocals by
\(\alpha=(1-k^2+2ik)/(1+k^2)\), \(k=1/100000\), and integrate the
resulting critical derivative anchored at the same \(a\).
The light distances and opening are preserved, while the center is
\(q=\alpha\) with \(|q-1|^2=4/10000000001\le1/13824^2\).
The new coefficient sum is

\[
 \frac{111559007452929694226663406365368102443429553}
 {140000000028000000001400000000000000000000000}<1.
\]

Both examples' complete derivatives, marked roots, origin/polar
identities and six full polynomial scaling controls are checked exactly.

The unrestricted equal-radius opening sign is false even under the
known necessary disks and stronger polar mean. This exact tuple is a
barrier to that proof mechanism:

\[
 b=1/2,\ r=501/500,\ s=497/500,\quad
 u=(33+56i)/65,\ q=(4-3i)/5,\ c=4/5,
\]
\[
 v=1,\quad w=(7-24i)/25.
\]

It obeys \(6r+2s=8\), \(1<r<R_{\max}(b)\), \(s>(1+b)^{-1}\), and
the three critical-disk squares are

\[
 9649813/13052052,\quad253009/988036,\quad968689/988036,
\]

all less than one. Its actual mean is351371/650000>139/270,
where139/270=\(b+(1-b)/(45b(1+b))\) is the credited stronger necessary
polar mean. Nevertheless both \(T(q)<0\) and
\(T(q)+s(1-c)|B|^2<0\), so (8) is strictly negative.
All exact rational signs and direct integrals are in
[expected.json](expected.json) and regenerated by [verify.py](verify.py).

The actual squared origin ratio of this tuple exceeds one. It is not
an actual hypothetical disk-root failure, nor a first-power counterexample.
It refutes only deriving either proposed opening sign from these necessary
constraints alone. It does not contradict the cone/center restrictions
of the positive lemma or any preceding published sector.

## 7. Evidence boundary

The new checker regenerates all18270 signs, complete moment/Gram and
substitution identities, every global/cell inverse and entry comparison,
1035 original rational Gaussian controls, the analytic endpoint/cone
identities, two exact disk-root examples and the exact opening barrier.
Eleven altered compact fixtures must be rejected in normal and optimized
Python. No floating value, solver verdict or sampled sign is a proof input.

The Bernstein interpretation, convexity/modulus bounds, normalization,
the two prior abstract lemmas, Rouché and classical communication/equality
deductions are ordinary written mathematics. This is not a formalization
or independent review. Read [README.md](README.md) for commands, resources
and complete compact expected results. Wider heavy directions, unequal
light radii at substantial opening, and the unrestricted endpoint remain
unresolved here.
