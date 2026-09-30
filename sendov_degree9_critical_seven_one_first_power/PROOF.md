# First-power Tang--Zhang for the full complex degree-nine critical7+1 class

Author **six-sendov-1**, role **researcher**, 2026-09-30.
This is an ordinary author proof with regenerated exact finite sign
evidence. It is unformalized and awaits independent review.
The unrestricted degree-nine first-power inequality is not proved here.
Primary literature and earlier results are credited in
[LITERATURE.md](LITERATURE.md).

## 1. Polynomial theorem and the two equality families

Let \(p\) have degree nine, with all zeros in the closed unit disk. Let
\(a\) be any marked zero, and suppose the critical multiset is
\(\{\zeta_H^7,\zeta_L\}\), allowing the two points to coincide. Then
\[
 S_1(a):=\frac7{|a-\zeta_H|}+\frac1{|a-\zeta_L|}\ge8.       \tag{1}
\]
The inequality is strict when \(|a|<1\). Equality holds exactly when
\(|a|=1\) and, for some \(C\ne0\),
\[
 p(z)=C(z^9-a^9)\quad\hbox{or}\quad
 p(z)=C(z-a)(z+a)^8.                                      \tag{2}
\]
A zero denominator is interpreted as \(S_1=\infty\).
No ordering of the two critical distances is assumed. The new step is
the opposite ordering left open by the author's
[positive-sector proof](../sendov_degree9_critical_seven_one_positive_sector/PROOF.md),
source2831f4c23f848429d95b23310e57fb109705409d.
The collapsed family in (2) is an already known boundary family, not
a new unrestricted boundary classification.

Combining (1) with the author's previously proved complex
[4+4](../sendov_degree9_full_critical_four_four_first_power/PROOF.md),
[5+3](../sendov_degree9_critical_five_three_first_power/PROOF.md), and
[6+2](../sendov_degree9_critical_six_two_first_power/PROOF.md) cases gives:

**Corollary.** Every degree-nine disk-root polynomial with at most two
distinct critical points satisfies \(S_1(a)\ge8\) at every marked zero,
strictly at interior zeros. Its equality families are exactly (2).
Indeed, two critical multiplicities summing to eight are, up to order,
7+1, 6+2, 5+3 or 4+4. A single critical point is included by coincidence.
This corollary uses those three earlier theorems as logical premises;
their checkers are separate artifacts, not rerun by this source.

## 2. A free-light-phase origin minimum in the opposite ordering

Let \(0<b\le1\), \(1/(1+b)\le r\le1\), and \(s=8-7r\). Let \(u,v\)
be unit complex numbers and write \(\chi=\Re u\). Define the two floors
\[
 d(b,r)=\frac{1-(1-b^2)r^2}{2br},\qquad
 e(b,r)=1-\frac{8(1-b)}{7r}.                              \tag{3}
\]
Suppose \(\chi\ge\max\{d,e\}\). The light phase \(v\) is arbitrary.
Set
\[
 I=9\int_0^1(1-br\tau u)^7(1-bs\tau v)\,d\tau,
 \quad R=r^{14}s^2,\quad N=|I|^2/R.                     \tag{4}
\]
Then \(N\ge1\), with equality exactly when
\[
 b=1,\quad r\in\{1/2,1\},\quad u=v=1.                    \tag{5}
\]
In particular the inequality is strict if \(b<1\).
Neither the light critical-disk constraint nor its actual contribution
to the weighted real mean is needed for this abstract statement.
Both heavy floors in (3) are used.

To prove it, write
\[
 A_0=9\int_0^1(1-br\tau u)^7\,d\tau,\qquad
 B_0=9b\int_0^1\tau(1-br\tau u)^7\,d\tau.
\]
Thus \(I=A_0-svB_0\). If \(T=1-br u\), endpoint integration gives
\[
 A_0=\frac98\sum_{k=0}^7T^k,\qquad
 B_0=\frac b8\sum_{k=0}^7(k+1)T^k.                       \tag{6}
\]
These formulas also hold at \(br u=0\) by polynomial identity, although
the present physical domain has \(b,r>0\).
Put
\[
 P_A=|A_0|^2,\quad P_B=|B_0|^2,\quad
 L=P_A+s^2P_B-R,\quad F=L^2-4s^2P_AP_B.                  \tag{7}
\]
The exact coefficient certificates in section3 prove
\[
 L\ge\frac9{32}R>0,\qquad F\ge0                         \tag{8}
\]
under (3). Consequently \(L\ge2s\sqrt{P_AP_B}\), and for every \(v\),
\[
 |I|^2-R
 \ge P_A+s^2P_B-2s\sqrt{P_AP_B}-R\ge0.                  \tag{9}
\]
When \(F>0\), (9) is strict. The signs in (8) are both necessary for
this deduction; the squared condition alone is not used.

Conjugating the whole configuration allows the imaginary part of \(u\)
to be nonnegative. In the formal expansion write
\(u=\chi+i h\), \(h^2=1-\chi^2\). The real polynomial expressions for
\(P_A,P_B,L,F\) are unchanged by conjugation. No real-phase restriction
on the polynomial or its other roots is imposed.

## 3. Three radial boxes and two independent phase parametrizations

Since \(r\ge1/(1+b)\) and \(b\le1\), the full radial domain is
parametrized by
\[
 \frac12\le r\le1,\quad0\le y\le1,\qquad
 b=\frac{1-r+(2r-1)y}{r}.                               \tag{10}
\]
For \(r>1/2\), the inverse is
\(y=(br-1+r)/(2r-1)\); at \(r=1/2\), necessarily \(b=1\) and any
\(y\) gives that same point. The polynomial extension of (10) contains
\(b=0,r=1,y=0\); no division by \(b\) at this extension point occurs
in the physical deduction.

An actual \(\chi\) satisfying both floors belongs to both phase boxes:
\[
 \chi=1-\frac{8(1-b)}{7r}z_m,\quad0\le z_m\le1,            \tag{11}
\]
\[
 \chi=d+(1-d)z_d,\quad0\le z_d\le1.                      \tag{12}
\]
When a floor equals one, its box is the singleton \(\chi=1\) and any
phase coordinate can be used. The coordinates \(z_m,z_d\) generally
differ. We do not impose equality between them.
The radial condition ensures \(d\le1\), and \(e\le1\) is immediate.

Let \(H=L-(9/32)R\). Substitute (11) into \(H\) and \(F\), and (12)
into \(F\), then substitute (10). Exact monomial cancellation gives
polynomials
\[
 \mathcal H=r^{16}H,\qquad
 \mathcal F_m=r^{32}F,\qquad
 \mathcal F_d=r^4F,                                      \tag{13}
\]
where each right side uses its indicated phase map. All clearing
powers are positive on the physical domain. Their respective tensor
degrees in \((y,r,z)\) are
\[
 (16,32,7),\qquad(32,64,14),\qquad(32,36,14).              \tag{14}
\]
The rational numerators of \(\chi\) are
\[
 T_m=r-\frac87z+\frac87bz,\qquad \chi=T_m/r,
\]
\[
 T_d=1-(1-b^2)r^2+\big((1-b^2)r^2+2br-1\big)z,
 \qquad\chi=T_d/(2br).
\]
These definitions fix the substitutions completely. The disk map in
(13) is a polynomial after exact cancellation; its apparent \(b\)
denominators are not evaluated at the polynomial extension point.

The following three closed radial boxes cover the full rectangle in
(10), with disjoint interiors. The phase interval is \([0,1]\) for each
map independently.

| Cell | \(y\) interval | \(r\) interval | Targets |
| --- | --- | --- | --- |
| 0 | \([0,1/2]\) | \([1/2,1]\) | \(\mathcal H,\mathcal F_d\) |
| 1 | \([1/2,1]\) | \([1/2,3/4]\) | \(\mathcal H,\mathcal F_d\) |
| 2 | \([1/2,1]\) | \([3/4,1]\) | \(\mathcal H,\mathcal F_m\) |

All coefficients of the complete tensor Bernstein representations on
these cells are nonnegative. There are three times4488 coefficients
for \(\mathcal H\), twice18315 for \(\mathcal F_d\), and32175 for
\(\mathcal F_m\): **82269 new sign coefficients**.
For local tensor indices \((i,j,k)\), the exact zero supports are:

| Target and cell | All and only zero indices |
| --- | --- |
| \(\mathcal H\), cells0 and1 | none |
| \(\mathcal H\), cell2 | \((16,32,k)\), \(0\le k\le7\) |
| \(\mathcal F_d\), cells0 and1 | \((i,0,k)\), \(0\le i\le32,0\le k\le14\) |
| \(\mathcal F_m\), cell2 | \((32,j,k)\), \(j\in\{63,64\},0\le k\le14\) |

The Bernstein basis is nonnegative and sums to one. Thus these signs
prove (8): for an actual point use its mean coordinate for \(H\), and
the cell's selected phase coordinate for \(F\). A separate phase
coordinate is legitimate because the same actual \(\chi\) satisfies
both floors.

The zero supports give strictness without relying on samples. In
cells0 and1, any local \(r>0\) has a positive active coefficient for
\(\mathcal F_d\), including at other coordinates' endpoints. Thus
\(F>0\) unless the global \(r=1/2\). In cell2, the only zero set is
the global corner \(y=r=1\): if either local radial coordinate is
less than one, a coefficient outside the displayed zero support has
positive basis weight. Therefore equality in (9) forces
\(r=1/2,b=1\), or \(r=1,b=1\). The mean floor then forces \(u=1\).
At either corner \(A_0,B_0\) are positive real and
\((A_0-sB_0)^2=R\). Equality for the arbitrary light phase in (9)
then forces \(v=1\). Explicitly, at \(r=1\),
\((A_0,B_0)=(9/8,1/8)\); at \(r=1/2\),
\((A_0,B_0)=(2295/1024,251/512)\) and \(A_0-sB_0=9/256\).
This proves exactly (5).

## 4. Exact evidence and its trust boundary

[negative.py](negative.py) constructs the new targets over the rational
polynomial ring, and [verify.py](verify.py) regenerates all signs.
The four real/imaginary factors in (6) agree coefficient by coefficient
with the binomial-integral and sequential linear-product constructions
in the credited [arc.py](arc.py). Each of the three phase substitutions
and three radial substitutions also agrees as a complete polynomial
with an independent coefficient-group homogenized Horner expansion.
These are six full substitution identities, not sampled checks.

The checker inverts all three complete global tensors and all six
used cell tensors. It compares every used cell entry from de Casteljau
subdivision with an independent direct affine construction, including
two complete Fraction-based affine references. It checks all zero
indices against the displayed sets. Coverage and nonoverlap of the
three boxes are exact. The unused fourth polynomial variable has
degree zero and does not add physical dimensions.

There are144 exact signed Gaussian controls for the original integral,
and108 original-to-box identity controls. They complement the complete
coefficient identities and signs; they do not establish them. The new
kernel hash is
ae0b2f9e4341d69268c9d374e39f5508b13465bfbf5bad9380321025bac3bc02.
The compact [expected.json](expected.json) stores full tensor hashes,
counts, exact minima and zero-support hashes. Every tensor is generated
from source; a hash is never used as a substitute for sign checking.

The credited positive-sector and polar checks are replayed completely
by [positive_verify.py](positive_verify.py), with their original canonical
manifest digest
40ef9f2414ffbcffdcc027f2c9a72b5c38414a43268138444c931710f80585e2.
They contribute449764 already credited sign entries. The full replay
therefore checks **532033** sign entries. Twelve deliberately corrupted
compact manifests are rejected by explicit exceptions, including under
optimized Python. This is exact author evidence and an ordinary written
proof; no proof-assistant formalization or independent review is implied.

## 5. Credited positive-sector and polar premises

We state the two earlier premises precisely; their proofs and attribution
remain in the linked sources. Both complete exact certificates are
reproduced locally, with no external source or data download.

**Positive-sector origin premise.** For \(0\le b\le1\),
\(0\le\eta\le1/14\), \(U=(1+\eta)u,V=(1-7\eta)v\), unit \(u,v\),
and \(\Re((7U+V)/8)\ge b\), the ratio defined as in (4) is at least
one. Equality is exactly \(b=1,\eta=0,u=v=1\).
This is proved in
[the preceding positive-sector source](../sendov_degree9_critical_seven_one_positive_sector/PROOF.md),
commit2831f4c23f848429d95b23310e57fb109705409d, graph
bafkreiaka2bskthnbp3nxm4o5lloxjkukt3wgrzi2ubspjdnyfn6j4qhky at8052.

Its weighted-mean triangle parametrization writes
\(|I|^2-R=D+\lambda J\), \(\lambda^2=h=c(1-c)(1-x^2)\),
and uses \(\sigma=1-cx^2\) with
\(\sigma^2-4h=(1-2c+cx^2)^2\ge0\).
Both first-Newton margins
\(4\sigma D\pm(\sigma^2+4h)J\) have nonnegative full tensor
representations on two \(x\)-cells each, with112200 entries per cell.
Their positive support gives
\(N-1\ge(3/4)\max\{(1-c)^9,(1-x)^{19}\}\).
The aligned corner uses a separate289-entry certificate for
\(D-((1-b)+(14\eta)^2)/4\). It treats \(\sigma=0\) without dividing
by zero and gives binomial-only equality. These bounds are credited,
not strengthened or reinterpreted as original-root metric stability here.

**Polar mean premise.** For \(0<a<1\), arbitrary \(U_*,V_*\) with
\(|U_*|,|V_*|\ge(1+a)^{-1}\) and \(7|U_*|+|V_*|\le8\), put
\(\xi=(7\Re U_*+\Re V_*)/8\). If \(\xi\le a\), then
\[
 \left|\int_0^1(a+(1-a^2)\tau U_*)^7
                       (a+(1-a^2)\tau V_*)\,d\tau\right|
 \le1-\frac89(1-a)^2<1.                                 \tag{15}
\]
This is the author's
[critical7+1 polar reduction](../sendov_degree9_critical_seven_one_polar_reduction/PROOF.md),
commit0bebc1748ea52c1c770c660fcb9eb04b76fb888f, graph
bafkreigbdgbmjvmsggbdwgs5xekg43bdtifapki5ox5zl2nlxjr3iux3pm at7998.

For squared factor moduli \(X,Y\), its envelope is
\(X^{7/2}Y^{1/2}\le(X^4+X^3Y)/2\).
Increase radii and real projections coordinatewise to saturate the
radius budget and mean \(a\); the envelope increases. The saturated
radius and projection pairs have cube coordinates
\(r_*=(1+(8/7)av)/(1+a)\),
\(s_*=(1+8a(1-v))/(1+a)\),
\(\Re U_*=r_*-(8/7)(1-a)\theta\),
\(\Re V_*=s_*-8(1-a)(1-\theta)\).
The polynomial quotient of the integrated envelope deficit by
\((1-a)^2\) has zero division remainder and a full675-entry Bernstein
representation, each entry at least8/9. [polar.py](polar.py) rechecks
two complete integral constructions, the full inverse and these signs.
The premise proves (15) for both critical orderings. Its quantitative
mean-gap constants are also replayed and retain their earlier credit.

## 6. Passage from the origin minima to disk-root polynomials

Rotate the marked zero to real \(a\in[0,1]\) and make \(p\) monic. A
multiple marked zero is already immediate, so suppose it is simple.
For \(a>0\), put
\[
 U_*=(a-\zeta_H)^{-1},\quad V_*=(a-\zeta_L)^{-1},\quad
 m=\frac{7|U_*|+|V_*|}{8}.
\]
Assume \(S_1(a)\le8\), so \(0<m\le1\). Normalize
\[
 U=U_*/m=ru,\quad V=V_*/m=sv,\quad b=am,
 \quad 7r+s=8.                                         \tag{16}
\]
Gauss--Lucas gives \(|U_*|,|V_*|\ge1/(1+a)\). It also gives the
normalized critical disk inequalities
\[
 |b-1/U|=m|\zeta_H|\le1,\qquad |b-1/V|\le1.              \tag{17}
\]

For \(a<1\), the classical polar communication identity says that
the integral in (15) equals
\(\prod_{j=1}^8(1-az_j)/(a-z_j)\), where \(z_j\) are the other zeros.
Every factor has modulus at least one, because
\[
 |1-az_j|^2-|a-z_j|^2=(1-a^2)(1-|z_j|^2)\ge0.
\]
Thus (15) forces \(\xi>a\), and the normalized real mean satisfies
\[
 \mu:=\Re((7U+V)/8)=\xi/m>a/m\ge am=b.                   \tag{18}
\]
At \(a=1\), logarithmic differentiation gives
\[
 7U_*+V_*=p''(1)/p'(1)=2\sum_{j=1}^8(1-z_j)^{-1}.
\]
Each real part in the sum is at least1/2, so \(\xi\ge1\) and
\(\mu\ge1/m\ge m=b\). This boundary estimate is classical.

If \(r\ge1\), write \(r=1+\eta,s=1-7\eta\). The light radius bound
gives \(s\ge1/(m+b)\ge1/(1+b)\), and therefore
\(0\le\eta\le b/(7(1+b))\le1/14\).
The positive-sector premise applies, proving \(N\ge1\), with its
specified equality.

If \(r\le1\), the heavy disk constraint in (17) gives
\(r\ge1/(1+b)\) and \(\chi\ge d(b,r)\) exactly.
The weighted mean bound and \(\Re v\le1\) give
\[
 7r\chi+s\ge7r\chi+s\Re v\ge8b,
 \qquad\chi\ge1-\frac{8(1-b)}{7r}=e(b,r).                \tag{19}
\]
Thus the new free-light-phase minimum applies. Notice that (19) is a
necessary relaxation of the actual mean condition; it cannot impose
a stronger restriction on a hypothetical polynomial failure.

In either ordering, the classical origin communication identity is
\[
 9\int_0^1(1-a\tau U_*)^7(1-a\tau V_*)\,d\tau
       =-\frac{p(0)}a U_*^7V_*.
\]
Its normalized ratio in (4) is consequently
\[
 N=m^{16}\frac{|p(0)|^2}{a^2}
   =m^{16}\prod_{j=1}^8|z_j|^2\le m^{16}\le1.             \tag{20}
\]
For \(0<a<1\), \(b=am<1\), so both origin minima are strict and
contradict (20). Hence \(S_1(a)>8\).
At \(a=1\), (20) and the origin equality descriptions force \(m=b=1\).
The common corner \(r=s=1,u=v=1\) means both critical points are zero,
and integration gives \(p(z)=z^9-1\).
At the other corner \(r=1/2,s=9/2,u=v=1\), the critical points are
\(-1\) and \(7/9\). Integrating
\(p'(z)=9(z+1)^7(z-7/9)\) with \(p(1)=0\) gives
\(p(z)=(z-1)(z+1)^8\). Undoing normalization gives (2).
Both families have all roots in the unit disk and \(S_1=8\) at the
specified marked boundary root, so they really attain equality.

At \(a=0\), a critical point at zero makes the claim immediate.
Otherwise \(|p'(0)|=\prod_{j=1}^8|z_j|\le1\) and
\(|p'(0)|=9\prod_{j=1}^8|\zeta_j|\). AM-GM gives
\(S_1(0)\ge8\,9^{1/8}>8\). This classical endpoint completes (1).

The argument closes the two-critical-point classes by the stated
logical combination. It makes no claim for three or more distinct
critical points or the unrestricted degree-nine endpoint.
