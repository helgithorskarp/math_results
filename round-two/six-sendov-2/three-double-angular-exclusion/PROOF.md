# Classification and sharp angular bound for the entire three-double family

Actual author **six-sendov-2**, role **researcher**, 2026-10-04.
Complete ordinary author proof with exact polynomial certificates;
**unformalized and independently unreviewed**. Historical priority is not
claimed. The result concerns actual real original slopes adjacent to the
degree-nine complex first-power problem.

## 1. Statement and full-mass definition

Let \(x=(x_1,\ldots,x_8)\) be real, with four strictly positive and four
strictly negative coordinates, exactly three distinct levels of multiplicity
two and two levels of multiplicity one. Count every original multiplicity.
Assume

\[
 \mu_k=\sum_i x_i^k,\qquad
 \mu_1=\mu_3=\mu_5=0,\quad \mu_2=1.
\]

Use the full-mass angular definition7432: set
\(e=(1,\ldots,1)/\sqrt8\), \(P=I-ee^T\),
\(H=(P\operatorname{diag}(x)P)|_{e^\perp}\), and
\(w=\operatorname{diag}(x)e\). For each distinct eigenvalue let
\(\rho_\lambda=8\|\Pi_\lambda w\|^2\), retaining the entire orthogonal
eigenspace. Put

\[
 \eta=\sum_\lambda\rho_\lambda^2,\quad
 D=\mu_4-1/8,\quad C=(1-\eta)/D.                       \tag{1}
\]

Here \(D>0\). **Every such profile has \(C<16\), and the supremum
on this entire stratum is16.** It is attained only as a limit toward a
four-plus/four-minus equal-magnitude profile, where \(D=0\) and (1) is
undefined. All profiles in the stated stratum are classified in Section2.
The classification does not assume that \(C\) is large or that a general
positive-quartet fiber has a positive direction.

**Application.** Combining this bound with the previously published
quartet/triple reduction10200, every real normalized profile with
\(\mu_1=\mu_3=\mu_5=0,D>0,C\ge47/2\) has at most two original doubles
and at least six distinct original levels. At a constrained local maximum,
the all-distinct exclusion10105 leaves only \(2+1^6\) or \(2+2+1^4\).
This application uses those precise prior scopes. It does not prove
existence of either pattern, a global angular bound, path monotonicity,
unit-disk stability, or the unrestricted complex first-power inequality.

## 2. Direct classification from a squared quartet

The three doubles are distributed across two signs, so one sign contains
two doubles. Reflect to make it the positive quartet \((a,a,b,b)\),
\(0<a<b\). Positive rescaling preserves the homogeneous angular ratio.
Scale \(ab=1\) and set \(p=a+b>2\). The positive quartic is

\[
 g_U(z)=(z^2-pz+1)^2.                                  \tag{2}
\]

The magnitudes of the negative quartet have the same odd powers
\(P_1=S,P_3=K,P_5=L\). For any quartet with elementary coefficients
\((S,A,e_3,e_4)\), Newton identities give

\[
 T=(K-S^3)/3,\quad U=(S^5+5S^2T-L)/(5S),\quad
 e_3=SA+T,\quad e_4=U-TA/S.
\]

Thus any companion quartic differs from (2) by a scalar multiple of
\(q(z)=z^2-Sz-T/S\). In the present case \(S=2p\),
\(K=2(p^3-3p)\), \(T=-2p(p^2+1)\), and

\[
 q(z)=(z-p)^2+1>0\quad(z\in\mathbb R),\qquad
 g_{\text{other}}=g_U-\tau q.                         \tag{3}
\]

If \(\tau<0\), then \(g_{\text{other}}>0\) on the entire real line,
contrary to its actual four real roots. If \(\tau=0\), the two quartets
agree and the octic has four doubles, contrary to the stated multiplicities.
Hence \(\tau>0\). The other quartet has one double \(\beta>0\) and
two positive simple roots. At its double,
\(g_U(\beta)/q(\beta)=\tau\) and \((g_U/q)'(\beta)=0\).
It cannot be \(a\) or \(b\), where the ratio is zero.

Direct differentiation gives the complete identity

\[
 (g_U/q)'=
 \frac{2(z^2-pz+1)((z-p)^3+(z-p)+p)}{q(z)^2}.           \tag{4}
\]

The cubic factor is strictly increasing, since its derivative is
\(3(z-p)^2+1>0\). Write its unique zero as \(\beta=p-r\).
Then \(p=r+r^3\), so \(p>2\) implies \(r>1\), and \(\beta=r^3\).
Substituting in (3) yields

\[
 \tau=(r^2-1)^2(r^2+1),\quad B=1+2r^2-r^4-r^6,\quad
 g_{\text{other}}=(z-r^3)^2(z^2-2rz+B).                \tag{5}
\]

Its simple roots are

\[
 c=r-(r^2+1)\sqrt{r^2-1},\qquad
 e_0=r+(r^2+1)\sqrt{r^2-1}.                            \tag{6}
\]

Both are positive exactly when \(B>0\): their sum is \(2r>0\),
product \(B\), and discriminant \(4(r^2+1)^2(r^2-1)>0\).
Also \(r^6-2r^4+B=1+2r^2-3r^4<0\), so \(r^3\) lies strictly
between them. Consequently, up to permutation, reflection and positive
scaling, the ENTIRE stated stratum is

\[
 (a,a,b,b,-c,-r^3,-r^3,-e_0),\quad
 a,b=(p\mp\sqrt{p^2-4})/2,\quad p=r+r^3,\quad r>1,B>0. \tag{7}
\]

Conversely (5) gives matching odd powers by the same Newton pencil.
All four positive originals and all four negative originals are actual,
and the strict checks above give exactly the specified multiplicities.
The entire generic octic also has zero coefficients of \(z^7,z^5,z^3\);
its full first-five Newton powers are retained in the exact record.
Normalize (7) by \(\sqrt N\), where

\[
 N=6r^6+6r^4+2r^2-6>0.                                 \tag{8}
\]

It follows that (7), with this normalization, is a necessary and sufficient
classification, not a formal critical-node tuple or a finite sample.

## 3. Actual critical roots, zero masses and homogeneous normalization

For the unnormalized originals in (7), put

\[
 D_3(z)=(z^2-pz+1)(z+r^3),\quad Q_2(z)=z^2+2rz+B,
\quad f=D_3^2Q_2,\quad h=f'/8=D_3H_4.                 \tag{9}
\]

There are five distinct real originals. The derivative has one simple
root at each of the three original doubles. In each of the four
distinct-original gaps, \(f'/f=\sum_i1/(z-x_i)\) decreases strictly
from positive infinity to negative infinity. It has exactly one zero,
and \((f'/f)'=-\sum_i1/(z-x_i)^2<0\) makes this critical point simple.
These are all seven derivative roots. Therefore the canceled monic
quartic \(H_4\) has four distinct real roots and its discriminant never
vanishes at a physical parameter.

The standard compression identity identifies these derivative roots
with the spectrum of \(H\). At a gap critical root \(\lambda\), an
eigenvector is proportional to \((1/(\lambda-x_i))_i\). Its scalar
product with \(w\) is \(-\sqrt8\) divided by the norm of that vector,
because \(\sum_i1/(\lambda-x_i)=0\). Hence its raw mass is

\[
 m_\lambda=\frac{64}{\sum_i1/(\lambda-x_i)^2}
           =-\frac{8f(\lambda)}{h'(\lambda)}
           =-\frac{8D_3(\lambda)Q_2(\lambda)}{H_4'(\lambda)}. \tag{10}
\]

At an original double the eigenspace is its coordinate-difference line,
orthogonal to \(w\), so its mass is zero. No original or critical
multiplicity is discarded. The full mass sum is
\(8\|w\|^2=N\); after normalization by \(\sqrt N\), masses divide
by \(N\). Let \(X=\sum_i x_i^4\) before normalization. Then (1) equals

\[
 C=\frac{N^2-\sum_{H_4(\lambda)=0}m_\lambda^2}{X-N^2/8}. \tag{11}
\]

The denominator is strictly positive by strict Cauchy--Schwarz: equality
would make all eight original squared magnitudes equal, impossible for
the two distinct positive levels \(a,b\). Formula (11) retains actual
original feasibility and all three zero collision masses.

## 4. Whole exact angular identity

The canceled quartic is

\[
\begin{aligned}
H_4(z)={}&z^4+rz^3+\tfrac{-5r^6-5r^4+r^2+5}{4}z^2\\
 &+\tfrac{-r^7-r^5-3r^3+r}{4}z
 +\tfrac{r^{12}+2r^{10}-r^8-4r^6-r^4+2r^2+1}{4}.
\end{aligned}                                         \tag{12}
\]

Here and in the finite certificate, every rational coefficient is exact.
[CERTIFICATE.json](CERTIFICATE.json) gives a monic common denominator
\(\Delta(r)\) and a degree-at-most-three numerator \(I(z,r)\) such that

\[
 H_4'I\equiv\Delta\pmod{H_4},\qquad
 \operatorname{disc}H_4=\Delta W(r).                    \tag{13}
\]

Both are whole polynomial identities in \(\mathbb Q[r][z]\), and the
discriminant is independently reconstructed from the entire Sylvester
determinant. Since the physical discriminant is nonzero, \(\Delta\ne0\)
at EVERY physical parameter. This closes specialization of the rational
inverse; generic inversion alone would not suffice.

Reduce \(-8D_3Q_2I\) modulo \(H_4\), square it and reduce again.
Newton's four trace powers \(4,-a,a^2-2b,-a^3+3ab-3c\), for
\(H_4=z^4+az^3+bz^2+cz+d\), give the exact sum and squared sum of
all four remaining raw masses. The first trace is exactly \(N\Delta\).
The second, divided by \(\Delta^2\), gives the squared-mass term in
(11). Full denominator clearing gives an ENTIRE degree120 polynomial
identity, yielding

\[
 C=\operatorname{Num}(u)/\operatorname{Den}(u),\qquad u=r^2. \tag{14}
\]

All19 coefficients of each polynomial, including interior zeros when
present, and all complete positivity vectors are displayed at the end.
The full intermediate remainders, inverse coefficients, discriminant,
normalization and degree120 coefficient map are in [EXPECTED.json](EXPECTED.json).
This exact algebra is a finite certificate supporting the ordinary proof.
It is not an inference from interpolation samples.

## 5. Entire physical interval and the sharp bound

Writing \(u=r^2\), the physical condition is
\(u>1\) and \(B(u)=1+2u-u^2-u^3>0\).
For \(v\ge0\), \(B'(1+v)=-3-8v-3v^2<0\);
\(B(1)=1\), \(B(5/4)=-1/64\). Thus every physical parameter satisfies
\(1<u<5/4\). This interval slightly enlarges the actual physical interval.

The COMPLETE Bernstein coefficient vectors of
\(\operatorname{Den}(u)\) and
\((16\operatorname{Den}(u)-\operatorname{Num}(u))/(u-1)\)
after \(u=1+v/4\) have19 and18 strictly positive entries, respectively.
For degree \(n\), the Bernstein basis
\(\binom nk v^k(1-v)^{n-k}\) is nonnegative and sums to one on
\([0,1]\). Therefore both polynomials are strictly positive on the entire
closed interval \([1,5/4]\), and (14) gives \(C<16\) at every physical
\(u>1\).

Finally \(\operatorname{Num}(1)=16\operatorname{Den}(1)\), with
\(\operatorname{Den}(1)=262144>0\). Physical parameters exist arbitrarily
close to1 from above because \(B(1)=1\). Thus \(C\to16\), proving
the sharp supremum. At \(r=1\) the originals collapse to four \(+1\)
and four \(-1\) before normalization, and \(D=0\). This limiting value
is not assigned to (1) at the collapsed point.

## 6. Application and the remaining frontier

The exact prior reduction10200 already proves that a profile with
\(C\ge47/2\) has four originals of each strict sign, no zero, all
original multiplicities at most two, and at least five distinct original
levels. Its inputs are the sign-sector bound10164 and the actual
symmetric strict47/2 bound from REVIEW9416; its original-triple rigidity
is new in that prior contribution. If five levels remained, eight
originals with multiplicities at most two would have exactly three doubles
and two singles. The present whole-family bound \(C<16<47/2\) excludes
this possibility. Hence at least six distinct originals remain.

Only for a constrained local maximum,10105 further excludes the
eight-distinct stratum. The possible multiplicities are consequently
exactly one or two original doubles. Its fixed-even-coefficient parity
variation is not automatically the feasible quartic midpoint path of10200.
The latter changes even coefficients. This leaf supplies no angular
descent along that path.

The two same-sign-double frontier has
\(g_U=(z^2-pz+1)^2\), \(g_{\text{other}}=g_U-\tau((z-p)^2+1)\),
with \(p>2\) and four actual positive companion roots. The present
three-double theorem only covers its collision endpoint. It gives no
bound for the entire interior in \(\tau\). The other two-double type
has one double in each sign quartet. Both remain open here, as does the
one-double stationarity problem and unrestricted first-power target.

## 7. Reproduction and trust boundary

[verify.py](verify.py) uses only standard-library exact Fractions. It
rebuilds the entire generic stationary identity, both actual quartets,
all first-five original powers, the derivative factorization, a whole
degree36 Sylvester discriminant, its inverse-denominator divisibility,
all mass and squared-mass remainders, the whole degree120 angular identity
and both complete positivity vectors. Three physical rational parameters
are also computed in the FULL seven-dimensional derivative companion
algebra, with literal Gaussian inversion, all original multiplicities,
mass normalization and angular values. These checks do not substitute
for the uniform classification.

The entire typed canonical27941-byte record is checked, rather than only
counts or a displayed subset. Explicit exceptions survive Python
optimization. Eight altered mathematical certificates are rejected by
the optional self-test. Local and cold-source normal/optimized runs,
external typed-fixture rejections and the optional CAS comparison are
recorded in README. No private module or generated scratch input is needed.

[compare_cas.py](compare_cas.py), using SymPy1.14.0, independently rebuilds
the WHOLE4688-byte certificate and all three seven-slot records from dense
expressions. Its complete Bernstein vectors use exact interpolation in
the Bernstein basis. It imports no native checker arithmetic. Both routes
have the same author; this is not independent peer review.

The compression/eigenvector correspondence, logarithmic-derivative root
count, actual classification and the mathematical meaning of the exact
identities remain ordinary unformalized written arguments. No floating
arithmetic, solver soundness, exhaustive search, resource-limited result
or incomplete enumeration is a premise. No verdict for a reviewed
ancestor is transferred to this new leaf.

## 8. Complete coefficient vectors

Power vectors use ascending powers of \(u\). Bernstein vectors use
\(v\in[0,1]\) after \(u=1+v/4\), in the ordinary binomial basis.

Num:

```json
["11664", "-140292", "390636", "2706508", "4127676", "-4018836", "-10848244", "-4236516", "17047308", "12783956", "-6621324", "-9943644", "-1928908", "1914084", "1688580", "864756", "315252", "69984", "11664"]
```

Den:

```json
["972", "-12555", "49377", "-112415", "-740283", "-494007", "1712969", "1974573", "-484767", "-1842073", "-739929", "173139", "269519", "231123", "166179", "76383", "27135", "5832", "972"]
```

Den Bernstein, degree18:

```json
["262144", "300032", "5862592/17", "20319421/51", "78706111/170", "6184473523/11424", "108131201761/169728", "2049029831609/2715648", "1119056943843/1244672", "858225257304489/796590080", "1240338576870629/955908096", "1454876569118937/926941184", "49455153749254699/25954353152", "15880742863297877/6845104128", "64594900375345607/22817013760", "3031495367922676751/876173328384", "927151715074318541/219043332096", "66751464514386811/12884901888", "108936502669091023/17179869184"]
```

Divided-gap Bernstein, degree17:

```json
["12582912", "244432896/17", "282219264/17", "1644037368/85", "13510319868/595", "5927358513/221", "1575744588489/49504", "23591170764507/622336", "70402011104163/1555840", "1346492526920061/24893440", "937025068329879/14483456", "251040154013867199/3244294144", "85739999553721899/926941184", "1102732958680389921/9982443520", "6012968282797586223/45634027520", "5729466846583234311/36507222016", "425823653945684817/2281701376", "237881151583434063/1073741824"]
```
