# Complete two-same-sign-double angular bound

Actual author **six-sendov-2**, role **researcher**, 2026-10-04.
Complete ordinary author proof with exact certificates, **unformalized
and independently unreviewed**. All code routes have the same author.

## 1. Actual domain and statement

Let eight actual real original slopes, counted with multiplicity, satisfy
\[
\sum x_j=\sum x_j^3=\sum x_j^5=0,\qquad \sum x_j^2=1.
\]
There are four strict originals of each sign, exactly two distinct
doubles on the same sign side, and four simple originals on the other.
No zero, triple, complex original or formal critical tuple substitutes
for these assumptions.

Use the actual angular convention of
[7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md).
For \(w=(1,\ldots,1)/\sqrt8\), \(P=I-ww^*\), \(A=\operatorname{diag}(x_j)\),
let \(H=PAP|_{w^\perp}\), \(v=PAw\), and
\(m_l=8|\langle v,e_l\rangle|^2\) for all seven orthonormal critical
eigenvectors, including zero masses. Their eigenvalues are simple here,
as proved below. Put
\[
\eta=\sum_lm_l^2,\quad D=\sum_jx_j^4-\tfrac18,\quad C=(1-\eta)/D.
\]
**Lemma. Every stated profile has \(D>0\) and \(C<16\). The supremum
is exactly16, approached towards the equal-magnitude \(D=0\) profile.
No value of \(C\) is assigned at that undefined endpoint.**

This is a real angular stability lemma adjacent to the degree-nine
complex first-power target \(\sum_{l=1}^8|a-\zeta_l|^{-1}\ge8\).
It is not that unrestricted endpoint or a theorem about a complex-disk path.

## 2. Entire square/quadratic pencil reduction

Reflection places both doubles in the positive quartet \((a,a,b,b)\),
\(0<a<b\). Scale \(ab=1\) and put \(p=a+b>2\). Reflection, permutation
and positive scaling preserve \(C\): raw masses scale quadratically,
their squares and the raw denominator quartically. Let
\[
d_2=z^2-pz+1,\qquad g_U=d_2^2.
\]
The negative magnitudes share the first/third/fifth quartet powers
\(S,K,L\) with the positives. Write a quartet's elementary coefficients
as \(e_1=S,e_2=E,e_3=F,e_4=G\). Newton gives
\[
F=SE+(K-S^3)/3,\qquad
L=(5S^2K-2S^5)/3+5(S^3-K)E/3-5SG.
\]
Thus \(G=dE+e\), where \(d=(S^3-K)/(3S)\) and
\(e=(5S^2K-2S^5-3L)/(15S)\). Quartics with these common odd powers
differ by a multiple of \(z^2-Sz+d\). For the doubled quartet,
\(S=2p,\ K=2(p^3-3p)\); consequently its actual companion is
\[
g_A=g_U-\tau q,\qquad q=(z-p)^2+1>0\quad(z\in\mathbb R).
\tag{2.1}
\]
If \(\tau<0\), \(g_A>0\) on the entire real line, impossible for an
actual real quartet. If \(\tau=0\), both quartets are \((a,a,b,b)\),
giving four original doubles. Hence \(\tau>0\).
This direct reduction needs neither high \(C\) nor the general fiber theorem.
The preceding [10218](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/three-double-angular-exclusion/PROOF.md)
uses the same square/quadratic mechanism at the three-double endpoint.

## 3. Necessary and sufficient physical region

For \(R=g_U/q\),
\[
R'=\frac{2d_2[(z-p)^3+(z-p)+p]}{q^2}.
\]
The bracketed cubic is strictly increasing. Its unique zero is
\(\beta=p-r=r^3\), where \(p=r+r^3\) has a unique \(r>1\).
Since \(d_2(\beta)=1-r^4<0\), \(a<\beta<b\).
The minima of \(R\) are zero at \(a,b\), and its interior maximum is
\[
T=R(\beta)=(r^2-1)^2(r^2+1).
\]
On \((0,a),(a,\beta),(\beta,b),(b,\infty)\), its derivative signs are
negative/positive/negative/positive. On the negative half-line it
decreases from infinity to \(R(0)=1/(p^2+1)\). Therefore the companion
has **four simple positive roots if and only if**
\[
0<\tau<T,\qquad \tau<\tau_0=1/(p^2+1).
\tag{3.1}
\]
This proves actuality, including exclusion of negative and zero roots.
At \(\tau=T<\tau_0\) the interior crossing is a double; at \(\tau=\tau_0\)
an original is zero and excluded. The boundary \(\tau=0\) is a four-double
control, not part of the exact two-double theorem.

## 4. Every critical slot, raw moments and masses

Before normalization the actual octic and derivative are
\[
f=d_2(z)^2g_A(-z),\qquad h=f'/8=d_2H_5,
\]
\[
\begin{split}
H_5={}&z^5+pz^4+(-p^2/2-3\tau/4+2)z^3\\
&+(-p^3/2-3p\tau/4+p)z^2\\
&+(p^2\tau/4-p^2/2-3\tau/4+1)z+p^3\tau/4.
\end{split}
\]
Whole expansion/Newton identities give the zero odd powers and
\[
N=4p^2-8+2\tau,\quad
X=4p^4-16p^2+8-4\tau+2\tau^2,\quad
D_{\rm raw}=X-N^2/8=2p^4-2p^2\tau-8p^2+3\tau^2/2.
\tag{4.1}
\]
These are the raw second/fourth moments; normalize by \(\sqrt N\).
Cauchy gives \(X\ge N^2/8\), with equality only when every squared
magnitude is equal. The distinct positive levels \(a,b\) exclude this,
so \(D_{\rm raw}>0\).

The six distinct real originals yield two simple derivative roots at the
doubles and five simple roots in the intervening gaps. Indeed \(f'/f\)
decreases from \(+\infty\) to \(-\infty\) in each gap, with derivative
\(-\sum_j(z-x_j)^{-2}<0\). They exhaust degree7. Hence \(H_5\) has five
simple real roots and is nonzero at \(a,b\). The same count at the actual
three-/four-double controls still gives seven simple critical roots.

Here is the mass bridge explicitly. For the raw diagonal compression,
\(\|v\|^2=N/8\). The diagonal resolvent gives
\(w^*(z-A)^{-1}w=f'/(8f)\), hence \(\det(z-H)=h\).
The balanced block determinant is
\[
f(z)=h(z)\left[z-\sum_l\frac{|\langle v,e_l\rangle|^2}{z-\sigma_l}\right].
\]
Thus every raw mass is
\[
m_l=-8f(\sigma_l)/h'(\sigma_l)\ge0,\qquad \sum_lm_l=N.
\]
Both original-double critical roots have zero mass; at an \(H_5\) root,
\[
m=-8d_2(z)g_A(-z)/H_5'(z).
\tag{4.2}
\]
There are at most five nonzero masses, also at the control endpoints.
For \(\eta_{\rm raw}=\sum_lm_l^2\), normalization gives
\[
C=(N^2-\eta_{\rm raw})/D_{\rm raw},\qquad
\eta_{\rm raw}\ge N^2/5.
\tag{4.3}
\]
All seven critical slots are accounted for.

## 5. Entire large-parameter estimate

Set \(y=p^2\). Physical positivity gives \(0<\tau<1/(y+1)\).
Exact expansion yields
\[
20D_{\rm raw}-N^2
=24y^2-96y-64-56y\tau+32\tau+26\tau^2
>24y^2-96y-120.
\]
The last expression is increasing on \(y\ge6\) and equals168 at6.
Hence \(D_{\rm raw}/N^2>1/20\), so (4.3) gives \(C<16\).
This ordinary estimate requires no symbolic denominator sign or sampling.

## 6. Complete compact-region polynomial proof

For \(4<y<6\), put \(u=r^2>1\); \(y=u(1+u)^2\) increases strictly.
At \(u=49/40\),
\[
y=388129/64000>6,\qquad B_0=1+2u-u^2-u^3=7111/64000>0.
\]
Since \(B_0'<0\) for \(u\ge1\), the compact physical region has
\(1<u<49/40\) and \(B_0>0\). Moreover \(1-T(y+1)=u^3B_0>0\),
so \(T<\tau_0\). With \(b=\tau/T\), the closed containing rectangle is
\[
y=u(1+u)^2,\quad \tau=(u-1)^2(u+1)b,\quad
1\le u\le49/40,\quad 0\le b\le1.
\tag{6.1}
\]
For \(u>1\), its \(b=0,1\) controls also have actual positive originals.
At \(u=1\), only rational limits are used.

[CERTIFICATE.json](CERTIFICATE.json) supplies the entire quintic,
inverse numerators \(I_i\), common denominator \(\Delta\), discriminant
and quotient, and complete angular polynomials Num/Den of bidegrees
\((11,9)\), with 71/70 nonzero monomials. The native checker reconstructs
the full nine-by-nine Sylvester determinant by512-subset dynamic programming
and verifies the entire polynomial identities
\[
H_5'I\equiv\Delta\pmod{H_5},\qquad \operatorname{disc}(H_5)=\Delta W.
\tag{6.2}
\]
All actual \(H_5\) roots are simple, so the discriminant and \(\Delta\)
are nonzero at **every physical parameter**, licensing specialization.

Let \(M=(-8d_2g_A(-z)I)\bmod H_5\), and
\(E_{\rm num}=\operatorname{Tr}(M^2\bmod H_5)\).
Quintic Newton identities give traces of whole remainders. The checker
verifies \(\operatorname{Tr}M=N\Delta\) and the complete500-monomial identity
\[
(N^2\Delta^2-E_{\rm num})\operatorname{Den}(p^2,\tau)
=D_{\rm raw}\Delta^2\operatorname{Num}(p^2,\tau).
\tag{6.3}
\]
These are actual masses by (4.2)/(6.2), not a formal critical substitute.

After the entire substitution (6.1), Num/Den both have the positive
common factor \((u-1)^4(u+1)^6\) for \(u>1\). The checker divides every
whole \(b\)-coefficient by every linear factor with zero remainders.
The reduced polynomials \(\overline{\rm Num},\overline{\rm Den}\)
have bidegrees \((26,9)\). The entire gap
\(16\overline{\rm Den}-\overline{\rm Num}\) divides exactly by \(u-1\),
with quotient of bidegrees \((25,9)\).

With \(u=1+(9/40)t\), every coefficient in the complete tensor Bernstein
basis on the unit square is strictly positive:

| Whole polynomial | Bidegree | Entries | Exact minimum |
|---|---:|---:|---:|
| Reduced denominator | \((26,9)\) |270|16777216|
| Divided16 gap | \((25,9)\) |260|805306368|

The code regenerates and checks **all530 entries**, not only counts,
minima, hashes or samples. Both binomial bases are nonnegative and each
sums to one on its axis. Thus both whole polynomials are positive
throughout the closed rectangle. Den is nonzero and (6.3) gives
\(C=\overline{\rm Num}/\overline{\rm Den}<16\) for physical \(u>1\).
Together with Section5, this proves the entire lemma.

For sharpness, fix \(0<b<1\) and let \(u\downarrow1\). The members are
actual by Section3 and \(B_0>0\) near1. The reduced denominator stays
positive at1 while the16 gap has the factor \(u-1\), so \(C\to16\).
The normalized endpoint has equal squared magnitudes and \(D=0\).

## 7. Reproduction and exact trust boundary

Python3.10+ standard library (validated3.12.14):

```text
python -B verify.py --self-test
python -B -O verify.py --self-test
```

The entire compact [EXPECTED.json](EXPECTED.json),48481B, has SHA256
`2e77402911968a5866100c8609f52b82ab1a93f409610b8f7d13989839d2452e`.
It is compared in full with strict recursive types. All large internal
maps and sign vectors regenerate from the compact defining certificate.
Hashes describe outputs; the full identities and every sign are the gates.
Decoding rejects duplicate keys, invalid dimensions/order/types/rationals.

Eight semantic damages reject explicitly: quintic, inverse numerator,
whole discriminant, specialization divisor, both angular polynomials,
raw norm and last tensor sign. No assertion is a proof gate.
Publication validation uses normal/optimized and empty relocated source.

Twenty actual rational profiles use \(r=101/100,21/20,11/10,10/9\) and
\(b=0,1/4,1/2,3/4,1\). Complete Sturm chains certify actual positive
roots/multiplicities. Full seven-slot companion matrices/Gaussian inverses
reproduce the moments, masses and generic quotient. These finite checks
corroborate bridges; Sections3--6 supply the uniform proof.

The separate dense program requires **SymPy1.14.0**:

```text
python -B compare_cas.py
```

It rebuilds the entire defining certificate, all inverse/mass/trace/angular
polynomials and all20actual seven-slot cases. It independently interpolates
both degree-bounded polynomials in a tensor Bernstein basis at distinct
rational knots, verifies every interpolation equation, and reconstructs
the **entire symbolic polynomial** before checking every sign. This is
exact interpolation, not sampled inequality evidence. Only after all
these computations does it load the native module for whole-entry comparison.

The bulky187KB sign dump and429KB intermediate dump remain private and
are not inputs. No private proof artifact, ledger, credentials or generated
symbolic output is required. The ordinary spectral/physical/continuum/limit
bridges remain unformalized. All arithmetic routes share the author and
are not independent peer review.

## 8. False shortcut and remaining frontier

The proposed fixed-p comparison \(C(p,\tau)\le C(p,T)\) is false.
At actual \(r=21/20,p=17661/8000\), the interior \(b=3/4\) value exceeds
the endpoint \(b=1\); EXPECTED contains the exact positive difference
and complete actual Sturm records. For orientation only the values are
approximately11.38493 and11.26302; no decimal is a proof input.

This fixes one quartet and changes raw normalization. It is **not**
[10200's fixed-normalization midpoint path](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/quartet-triple-rigidity/PROOF.md),
which changes both quartets. Angular monotonicity there remains unproved.

For the scoped high-\(C\ge47/2\) local-maximizer application, use10200's
structural reduction,10218's three-double exclusion, and only
[10105's all-eight-distinct local step](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/two-moment-parity-descent/PROOF.md).
High \(C\) already has4+4/nozero/multiplicities at most2; four doubles
are symmetric and excluded;10218 excludes three doubles. This lemma
excludes same-sign two doubles. Thus only **one original double** or
**two opposite-sign original doubles** can occur at such a local maximum.
This is not a global angular bound.

The symmetric47/2 bound retains
[reviewer1/9416 credit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/even-angular-audit/REVIEW.md);
the sign barrier retains
[10164 credit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/third-moment-sign-barrier/PROOF.md).
One-/opposite-sign-two-double cases, full path monotonicity and the
unrestricted complex first-power endpoint remain open. Review10214
confirms10200 only; no verdict transfers to this new leaf.
See [LITERATURE.md](LITERATURE.md) for primary and dependency scope.
