# Degree-nine first power with a radial sixfold critical point

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
This is an ordinary author proof with complete exact rational sign
evidence. It is unformalized and awaits independent review. The
unrestricted degree-nine first-power endpoint and the general complex
critical6+1+1 origin minimum remain open here. Literature, prior equality
families and arithmetic reuse are credited in [LITERATURE.md](LITERATURE.md).

## 1. Polynomial theorem and a separate general polar lemma

Let p have degree nine and all its zeros in the closed unit disk.
Write its critical multiset as
\(\{\zeta_H^6,\zeta_1,\zeta_2\}\), allowing coincidences. Let a be a
marked nonzero zero. Suppose \(\zeta_H/a\in\mathbb R\), so the heavy
critical point lies on the line through the origin and a. Then
\[
 S_1(a)=\frac6{|a-\zeta_H|}+\frac1{|a-\zeta_1|}
                         +\frac1{|a-\zeta_2|}\ge8.                 \tag{1}
\]
The inequality is strict for \(|a|<1\). Equality holds exactly when
\(|a|=1\) and, for some nonzero complex C,
\[
 p(z)=C(z^9-a^9)\quad\hbox{or}\quad p(z)=C(z-a)(z+a)^8.       \tag{2}
\]
The usual convention assigns an infinite reciprocal to a zero
denominator. The zero marked root also satisfies the strict inequality,
without a radial hypothesis. Equivalently, the new nonzero-root sector
requires one critical point of multiplicity at least six on that line.
It places no reality or conjugacy restriction on the two light points
or on the polynomial's coefficients. Section 6 gives a nonreal example.
The boundary families (2) retain earlier credit.

We also prove an independent lemma for the full complex critical6+1+1
class. Let \(0<a<1\), \(D=1-a^2\), and let arbitrary complex U,V,W
have radii r,s,t satisfying
\[
 r,s,t\ge\frac1{1+a},\qquad6r+s+t\le8,
 \qquad\xi=\frac{6\Re U+\Re V+\Re W}{8}.
\]
For
\[
 C_a=\int_0^1(a+D\tau U)^6(a+D\tau V)(a+D\tau W)\,d\tau,
\]
we have
\[
 \xi\le a\ \Longrightarrow\ |C_a|\le1-\frac89(1-a)^2<1,       \tag{3}
\]
and the quantitative implication
\[
 |C_a|\ge1\ \Longrightarrow\
 \xi-a\ge\frac{1-a}{128a(1+a)}.                              \tag{4}
\]
The polar lemma does not assume a real heavy reciprocal or equal light
radii. It supplies a necessary mean condition for a hypothetical
first-power failure in the general class; it does not close that class.
The radial proof of (1) does not use (3) or (4).

## 2. A radial-heavy origin minimum with one light disk retained

Take \(0<b\le1\), positive r,s,t with
\[
 r,s,t\ge(1+b)^{-1},\qquad s\le t,\qquad6r+s+t=8.             \tag{5}
\]
Let v,w be unit complex numbers and write \(q=\Re v\). Retain only
the disk constraint for the smaller light reciprocal:
\[
 q\ge d_b(s):=\frac{1-(1-b^2)s^2}{2bs}.                     \tag{6}
\]
The heavy reciprocal is positive real r and the other light phase w
is arbitrary. Define
\[
 I=9\int_0^1(1-br\tau)^6(1-bs\tau v)(1-bt\tau w)\,d\tau,
 \qquad R=r^{12}s^2t^2,\quad N=|I|^2/R.                     \tag{7}
\]
Then \(N\ge1\), strictly for \(b<1\). Its equality cases are exactly
\[
 b=1,\quad v=w=1,\quad
 (r,s,t)=(1,1,1)\ \hbox{or}\ (1/2,1/2,9/2).                \tag{8}
\]
No mean constraint and no disk constraint on w are used in this
abstract minimum. The sorting in (5) is light-label symmetry, not a
restriction on hypothetical polynomial failures.

Let the following positive real moments be denoted A,B,C:
\[
 A=9\int_0^1(1-br\tau)^6d\tau,\quad
 B=9b\int_0^1\tau(1-br\tau)^6d\tau,\quad
 C=9b^2\int_0^1\tau^2(1-br\tau)^6d\tau.
\]
Their positivity follows from the even power and a nonzero integrand
on an interval. With \(h=1-br\), independent endpoint sums are
\[
 A=\frac97\sum_{k=0}^6h^k,\quad
 B=\frac{9b}{56}\sum_{k=0}^6(k+1)h^k,\quad
 C=\frac{b^2}{56}\sum_{k=0}^6(k+1)(k+2)h^k.                 \tag{9}
\]
Expanding (7) gives \(I=K-twJ\), where \(K=A-svB\) and
\(J=B-svC\). Thus
\[
 P_A=|K|^2=A^2+s^2B^2-2sABq,\qquad
 P_J=|J|^2=B^2+s^2C^2-2sBCq,
\]
\[
 L=P_A+t^2P_J-R,\qquad F=L^2-4t^2P_AP_J.                   \tag{10}
\]
The next section proves
\[
 L\ge\frac18R>0,\qquad F\ge0.                             \tag{11}
\]
Both signs are used: they imply \(L\ge2t\sqrt{P_AP_J}\), so
\[
 |I|^2-R\ge L-2t\sqrt{P_AP_J}\ge0.                         \tag{12}
\]
If F is positive, the first inequality's lower bound is strictly
positive. The coefficient of q in L is
\(-2sB(A+t^2C)<0\); therefore \(L(q)\ge L(1)\) for every physical
\(q\le1\). It suffices to certify
\(H=L(1)-R/8\) and F with the disk phase map.

## 3. Two complete boxes, all signs and exact equality supports

The entire radial domain (5) is the image of \(b,\alpha,\beta\in[0,1]\),
with the physical restriction \(b>0\), under
\[
 r=\frac{1+(4/3)b\alpha}{1+b},\qquad
 s=\frac{1+4b(1-\alpha)\beta}{1+b},\qquad
 t=\frac{1+8b(1-\alpha)-4b(1-\alpha)\beta}{1+b}.             \tag{13}
\]
Indeed, (5) gives
\(r\in[(1+b)^{-1},(1+(4/3)b)/(1+b)]\), determining \(\alpha\).
At fixed r, sorted s ranges from \((1+b)^{-1}\) to
\((s+t)/2\), determining \(\beta\). At \(\alpha=1\) this interval
collapses and any \(\beta\) represents the same light radii.

Since \(s\ge(1+b)^{-1}\), the identity
\[
 2bs(d_b(s)-1)=(1-(1+b)s)(1+(1-b)s)\le0
\]
shows \(d_b(s)\le1\). Every actual q satisfying (6) and \(q\le1\)
therefore has a disk coordinate \(z\in[0,1]\):
\[
 q=d_b(s)+(1-d_b(s))z.                                    \tag{14}
\]
If the floor equals one, q is one and any z can be used. Some parts
of this enlarged phase box may have q below minus one; the sign
certificate proves F nonnegative on the larger box, and the norm
deduction in (12) is used only at actual unit phases.

For \(D_b=1+b\), after (13) and (14) define
\[
 \mathcal H=D_b^{16}H,\qquad\mathcal F=D_b^{32}F.             \tag{15}
\]
These are polynomials over the rationals. For clarity, the numerator
in (14) is
\[
 T=1-(1-b^2)s^2+[2bs-1+(1-b^2)s^2]z,\qquad q=T/(2bs).
\]
Every apparent b or s denominator cancels exactly before the radial
substitution. Thus the polynomial extension b=0 is safe in the
certificate; physical divisions only occur at b,s positive.

The tensor degrees in \((b,\alpha,\beta,z)\) are respectively
\((32,16,4,0)\) and \((64,32,8,2)\). The following two closed boxes
cover the whole radial cube with disjoint interiors; b, beta and z
each run over \([0,1]\):

| Cell | Alpha interval | Certified targets | Number of signs |
| --- | --- | --- | --- |
| 0 | \([0,3/4]\) | \(\mathcal H,\mathcal F\) | 2805 + 57915 |
| 1 | \([3/4,1]\) | \(\mathcal H,\mathcal F\) | 2805 + 57915 |

Every one of the **121440 coefficients** is nonnegative. Both H
tensors have exact minimum \(639/8\), so (11)'s first sign is strict.
All and only zero indices \((i,j,k,\ell)\) in the F tensors are

| Cell | Complete zero-index set |
| --- | --- |
| 0 | \(\{(64,0,0,\ell):0\le\ell\le2\}\cup\{(64,j,k,2):j\in\{31,32\},k\in\{7,8\}\}\) |
| 1 | \(\{(64,j,k,2):j\in\{0,1\},k\in\{7,8\}\}\) |

The tensor Bernstein basis is nonnegative and sums to one. Hence
these complete signs prove (11). Since every zero has b-index64,
F is positive whenever b is less than one, including all other
coordinate faces. At b=1, an interior local alpha coordinate has an
active positive coefficient; at the alpha endpoints the displayed
supports allow only the global corner \((\alpha,\beta)=(0,0)\), or
\((\alpha,\beta,z)=(3/4,1,1)\). For beta strictly between zero and
one, an active beta index outside \{7,8\} eliminates the binomial
zero. Thus these are the entire F zero set, not sampled candidates.

At the collapsed corner, s=1/2 and the disk floor forces v=1
regardless of z. At the binomial corner, z=1 forces v=1. At either
corner K and J are positive real and
\[
 K-tJ=\sqrt R=1\quad\hbox{or}\quad9/256.
\]
For example the collapsed moments are
\((A,B,C)=(1143/448,2223/3584,233/896)\); the binomial moments are
\((9/7,9/56,1/28)\). Equality in (12) for the remaining arbitrary
unit phase forces w=1. This proves exactly (8).

## 4. Passage to disk-root polynomials

Rotate a to real \(a\in[0,1]\) and make p monic. A multiple marked
zero is immediate. Suppose \(a>0\) and its heavy critical point is real.
If \(\zeta_H\ge a\), Gauss--Lucas gives, for \(0<a<1\),
\[
 S_1(a)\ge\frac6{1-a}+\frac2{1+a}
          =\frac{8+4a}{1-a^2}>8.                           \tag{16}
\]
At a=1 the ahead case is a critical collision. It remains to treat
\(\zeta_H<a\), so its reciprocal is positive real.

Assume \(S_1(a)\le8\), and put
\[
 U_*=(a-\zeta_H)^{-1}>0,\quad V_*=(a-\zeta_1)^{-1},\quad
 W_*=(a-\zeta_2)^{-1},\qquad m=S_1(a)/8\in(0,1].
\]
Normalize \(U=U_*/m=r\), \(V=V_*/m=sv\), \(W=W_*/m=tw\),
and \(b=am\). Interchange the light labels to have \(s\le t\).
All normalized reciprocals satisfy
\[
 |b-1/U|=m|\zeta_H|\le1,\quad
 |b-1/V|=m|\zeta_1|\le1,\quad |b-1/W|\le1.                 \tag{17}
\]
Their radii therefore are at least \((1+b)^{-1}\), and their budget
is exactly \(6r+s+t=8\). The light inequality for V in (17), squared,
is precisely (6). Consequently the abstract minimum applies.

Let \(z_1,\ldots,z_8\) be the other original zeros. The classical
origin communication identity, obtained by integrating p' from a
to zero, gives
\[
 I=-\frac{p(0)}a U_*^6V_*W_*,\qquad
 N=m^{16}\frac{|p(0)|^2}{a^2}
   =m^{16}\prod_{j=1}^8|z_j|^2\le m^{16}\le1.               \tag{18}
\]
For \(a<1\), b=am is less than one; strictness in (7) contradicts
(18). Thus S1 is strictly greater than eight in the interior.
For a=1, strictness first forces m=b=1, then (8) forces the two
critical configurations: all points zero, or
\(\{(-1)^7,7/9\}\). Integrating p' with p(1)=0 gives respectively
\(z^9-1\) and \((z-1)(z+1)^8\). Undoing rotation and scaling gives
(2); both families attain S1=8 at their stated marked boundary root.

At a=0, a critical point at zero gives an infinite term. Otherwise
\(|p'(0)|=\prod_j|z_j|\le1\) and
\(|p'(0)|=9\prod_j|\zeta_j|\). AM--GM gives
\(S_1(0)\ge8\,9^{1/8}>8\). This classical endpoint completes (1).

## 5. Full complex critical6+1+1 polar estimate and mean gap

For (3), write squared factor moduli as X,Y,Z. Triangle inequality
and \(\sqrt{YZ}\le(Y+Z)/2\) give
\[
 |C_a|\le\int_0^1 X^3(Y+Z)/2\,d\tau.                      \tag{19}
\]
This envelope is nonnegative and increases as any radius or real
projection increases, while the projections remain in their radius
intervals. If \(\xi\le a\), increase radii to saturate their weighted
budget eight, holding projections fixed. Then increase projections
to weighted real mean a. This is possible because the initial
weighted projection is at most 8a and the saturated upper projection
is eight. Each squared modulus stays nonnegative throughout.

Let \(\varepsilon=1-a\). The saturated heavy radius and total light
radius have cube coordinates \(v\in[0,1]\):
\[
 R_0=1+(4/3)av,\quad S_0=1+8a(1-v),\quad
 r=R_0/(1+a),\quad s+t=(1+S_0)/(1+a).
\]
Nonnegative projection defects have weighted sum \(8\varepsilon\),
so for \(\theta\in[0,1]\),
\[
 \Re U=r-(4/3)\varepsilon\theta,\qquad
 \Re V+\Re W=s+t-8\varepsilon(1-\theta).
\]
At fixed light sum and with each light radius at least \((1+a)^{-1}\),
convexity gives
\(s^2+t^2\le(1+S_0^2)/(1+a)^2\). Therefore (19) is at most
\(\int X^3Y_{\rm sum}/2\), with
\[
 X=a^2+[2a\varepsilon R_0-(8/3)a\varepsilon^2(1+a)\theta]\tau
             +\varepsilon^2R_0^2\tau^2,
\]
\[
 Y_{\rm sum}=2a^2+[2a\varepsilon(1+S_0)
            -16a\varepsilon^2(1+a)(1-\theta)]\tau
             +\varepsilon^2(1+S_0^2)\tau^2.                 \tag{20}
\]
For the selected physical saturated point, X is a squared modulus
and \(Y_{\rm sum}\ge Y+Z\ge0\); the replacements are legitimate.
They do not assume equal light radii.

[polar.py](polar.py) constructs the complete rational polynomial
\[
 Q_{611}=\frac{1-\int_0^1X^3Y_{\rm sum}/2\,d\tau}{(1-a)^2}.
\]
Exact division has zero remainder. Its complete tensor degrees in
\((a,v,\theta)\) are \((14,8,4)\), with **675 entries**, all at least
8/9. These signs prove (3), including every physical projection and
light-radius configuration. The quotient power SHA256 is
69f3e35f35aaaf15c2a7c1db0d0d10bbbe37f6c53fd624f1252b136bc13610f7.

For (4), (3) first forces \(\xi>a\). Saturate radii while holding
projections fixed, then decrease projections coordinatewise to mean a.
Such a path lies in their radius intervals. Its total weighted
projection decrease is \(8(\xi-a)\). Throughout it,
\[
 X\le Q(a)=[1+(4/3)a(1-a)]^2\le16/9,\quad
 Y,Z\le P(a)=[1+8a(1-a)]^2\le9,\quad Q(a)\le P(a).
\]
The derivatives of \(X^3(Y+Z)/2\) in the heavy and each light real
projection are respectively
\(3aD\tau X^2(Y+Z)\) and \(aD\tau X^3\). Dividing the first by
the heavy weight six bounds all derivatives per weighted unit by
\(aD\tau Q(a)^2P(a)\). Integration of tau gives
\[
 |C_a|\le1-\frac89(1-a)^2+4aD Q(a)^2P(a)(\xi-a)
       \le1-\frac89(1-a)^2+\frac{1024}{9}aD(\xi-a).
\]
Using \(|C_a|\ge1\) and cancelling positive factors yields (4).
The constant 1/128 is conservative, not asserted optimal.

For an actual disk-root polynomial of critical multiplicity6+1+1,
Gauss--Lucas supplies the radius floors for its unnormalized
reciprocals. Under a hypothetical S1<=8 the budget holds, and classical
polar communication gives
\[
 C_a=\prod_{j=1}^8\frac{1-az_j}{a-z_j},\qquad |C_a|\ge1,
\]
because \(|1-az_j|^2-|a-z_j|^2=(1-a^2)(1-|z_j|^2)\ge0\).
Thus (4) is a quantitative necessary condition on the actual reciprocal
mean. This implication is valid at arbitrary complex critical phases;
the origin step with a nonreal heavy phase remains unresolved.

## 6. Nonreal sector example and an exact failed relaxation

Let \(a=19/20\), \(d=i/40\), \(e=(1+2i)/50\), and
\[
 f(z)=z^9-\frac98(d+e)z^8+\frac97de\,z^7,\qquad p(z)=f(z)-f(a).
\]
Then \(p'(z)=9z^6(z-d)(z-e)\), a is a simple marked root, and the
two light points are distinct, nonreal and not conjugate. The imaginary
coefficient of z8 is nonzero, so the monic polynomial is not real.
The sum of coefficient bounds \(|\Re c|+|\Im c|\) for its z8, z7
and constant terms is exactly
\[
 \frac{217919198409239}{286720000000000}<1.
\]
On the unit circle Rouché therefore places all nine original roots
strictly inside. Its sixfold critical point is zero and hence radial.
The elementary bound \(6/a+2/(1+a)\) is less than eight at this a;
the theorem covers a substantive complex sector.

The smaller light disk in (6) cannot simply be deleted. Take
\[
 b=1,\quad r=s=1/2,\quad t=9/2,\quad
 v=\frac{99+20i}{101},\quad
 w=\frac{999831+26000i}{1000169}.
\]
Both phases are exactly unit. Direct rational integration in (7) gives
\[
 N=\frac{3059391541}{4949836381}<1.
\]
Here \(d_b(s)=1>\Re v\), so the necessary smaller-light disk is
violated. This is an obstruction to freeing both light phases, not a
disk-root polynomial counterexample. It explains why the earlier7+1
free-light proof cannot be transferred by deleting both constraints.

## 7. Reproduction and mathematical trust boundary

[verify.py](verify.py) is self-contained and uses Python3.10+ standard
library rational/integer arithmetic. It checks complete endpoint versus
binomial moments, both full Gaussian norm expansions, an alternate
discriminant identity, three full homogeneous Horner substitution
identities, all two global and four cell tensor inverses, and every used
affine/de Casteljau entry. Two complete Fraction affine references
complement the integer transforms. Coverage and every equality zero
index are checked exactly. The grouped integer radial construction
changes execution only and is compared through the full Horner identities.

The polar checker verifies two complete integrals, exact defect division
and multiplication, the full inverse and all675 positive signs. There
are415 exact original complex origin integral controls,166 map controls,
27 rational polar defect controls and54 physical Gaussian polar controls.
The physical controls include both mean directions, radius variance,
mean saturation, modulus identities, derivative bounds and the original
integral envelope. They supplement the complete identities and signs.
The nonreal Rouché example and disk-free obstruction are checked exactly.

The total is **122115 regenerated sign coefficients**. Kernel SHA256:
bfd2bfc1c1003211bf212efdfce4b37ee5039210e2116d211677a3479f32a938.
[expected.json](expected.json) records compact exact counts, minima,
zero supports and canonical hashes; hashes never replace sign checking.
Both normal and optimized Python replay the same evidence, with twelve
damaged compact fixtures rejected by explicit exceptions in each mode.
No floating-point sign, external solver, private input, large coefficient
corpus or imported earlier theorem is a proof premise. The communication
identities, monotonicity, projection path and theorem deductions above
are ordinary written mathematics outside a formal proof kernel. Author
checks and graph commitment are not independent mathematical acceptance.
