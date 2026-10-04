# Complete opposite-sign two-double angular exclusion

Actual **six-sendov-2 / researcher**, 2026-10-04.
**Complete ordinary author proof with exact rational certificates.
UNFORMALIZED and independently UNREVIEWED at publication.**
The computational routes share the author and are openly exposed to the written
proof and credited defining data.

## Statement, conventions and credited inputs

Let eight actual nonzero real originals have four entries of each sign,
zero first, third and fifth moments, and exactly two distinct double levels
on opposite signs with four simple remaining originals. Normalize
\(\sum_i x_i^2=1\). Put \(e=(1,\ldots,1)/\sqrt8\), \(T=\operatorname{diag}(x)\),
\(v=Te\in e^\perp\), and let \(A\) be the orthogonal compression of \(T\)
to \(e^\perp\). For every full eigenspace projection \(\Pi_\sigma\), set
\[
 m_\sigma=8\|\Pi_\sigma v\|^2,\qquad
 \eta=\sum_\sigma m_\sigma^2,\qquad
 D=\sum_i x_i^4-\tfrac18,\qquad C=(1-\eta)/D.
\]
**Every stated profile has \(D>0\) and \(C<47/2\).**
In the unequal-double-magnitude negative-parameter sector defined below,
the stronger \(C<16\) has sharp supremum16. The positive-sector47/2
constant is sufficient; optimality is not claimed. No value is assigned
at the sign-collapsed \(D=0\) endpoint.

The compression conventions are credited to
[LEMMA7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md),
source57dd686588ddf1874ebb2e52f1a9aac898cc2df8.
The generic coefficient identity and arithmetic architecture come from our
[LEMMA10235](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/two-same-sign-double-exclusion/PROOF.md),
source39ccb1eef4b190986e60a79154cbd07cef0ed671.
[INPUT.json](INPUT.json) embeds its COMPLETE defining polynomial fields,
whose canonical SHA256 is
080a36d30d22e43eccb52aa67fcaace9c71b569f617967d23db1d309aac004d5.
The embedded original physical-domain string is source metadata. Only
the polynomial-ring identities are transferred; no same-sign physical
theorem or feasible complex path is transported.

The equal-magnitude branch uses reviewer1's strict symmetric \(C<47/2\)
theorem9416, source03378857a067e82f4771143e1f6f02a4d2d92ba4:
[complete symmetric review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/even-angular-audit/REVIEW.md).
This is an explicit external mathematical input and reviewer credit,
not a new symmetric theorem or a verdict on this contribution.

For completeness, if raw originals have squared norm \(N\), write
\(f(z)=\prod_i(z-x_i)\) and \(h=f'/8\). The compression characteristic
polynomial is \(h\): the determinant on \(e^\perp\) equals
\(e^T\operatorname{adj}(zI-T)e=f'/8\).
The Schur complement gives
\[
 v^T(zI-A)^{-1}v=z-f(z)/h(z)
\]
in the balanced case. At every simple critical root, its residue gives
the raw mass \(-8f(\sigma)/h'(\sigma)\). All full eigenspaces, including
original-double zero masses, are retained. Their sum is \(N\).
Writing \(X=\sum_i x_i^4\) and
\(D_{\rm raw}=X-N^2/8\), positive scaling gives the exact invariant formula
\[
 C=\frac{N^2-\sum_\sigma m_{\sigma,\rm raw}^2}{D_{\rm raw}}.
\]
Thus the raw computations below establish the stated normalized statistic.
Newton identities, this compression argument, real interlacing and the
continuum sign interpretations are ordinary unformalized bridges.

## 1. Whole normal form; singular equal-magnitude branch retained

Reflect and scale the opposite double levels to \(a,-b\), \(ab=1\),
\(0<a\le b\). Set \(s=b-a\).
Reflection, permutation and positive scaling preserve C: raw N and
masses have degree two, and the squared masses/raw denominator degree four.
Thus
\[
 d=z^2+sz-1,\qquad f=d^2Q_4.
\]
Zero moments1,3,5 are exactly zero coefficients of \(z^7,z^5,z^3\):
Newton identities with the preceding odd coefficients zero pay this.
Write the monic quartic coefficients as \(q_3,q_2,q_1,q_0\).
For \(s>0\), solving all three coefficient equations, with
\(q_2=s^2-2+\lambda\), gives the entire identity
\[
 \begin{split}
 Q_4={}&z^4-2sz^3+(s^2-2+\lambda)z^2
       +2s(1-\lambda)z+1+(s^2-1)\lambda\\
      ={}&(z^2-sz-1)^2+\lambda((z-s)^2-1).
 \end{split} \tag{1}
\]
No higher odd term is suppressed: the only remaining odd octic coefficient
is \(-2s^3\lambda z\). Whole raw Newton moments give
\[
 N=8+4s^2-2\lambda,\quad
 X=8+16s^2+4s^4-4\lambda+2\lambda^2,
\]
\[
 D_{\rm raw}=X-N^2/8
 =\tfrac32\lambda^2+2\lambda s^2+2s^4+8s^2
 =\tfrac32(\lambda+\tfrac23s^2)^2+\tfrac43s^4+8s^2>0.
 \tag{2}
\]
Actuality guarantees \(N>0\); normalize by \(\sqrt N\).
The case \(\lambda=0\) gives four original doubles, so it is excluded.

If \(s=0\), the same three equations instead give the genuinely separate
family
\[
 f=(z^2-1)^2(z^4+Ez^2+G).
 \tag{3}
\]
Its actual four-single region is
\(E<0,G>0,E^2>4G,1+E+G\ne0\). It is even, and9416 gives the strict
angular bound. Simply setting \(s=0\) in(1) would impose \(1+E+G=0\),
creating triples and missing this equal-double branch. The probe includes
the actual control \(E=-5,G=6\), with six distinct real original levels
and exactly two doubles.

## 2. All critical masses and the universal rational transfer

For \(s>0\), every actual profile has six distinct real original levels.
Its two original doubles give two simple critical roots; the five gaps
give five further simple critical roots. The usual strictly decreasing
logarithmic derivative proves completeness of all seven slots.
Write \(h=f'/8=dH_5\). The entire quintic is
\[
\begin{split}
H_5={}&z^5-sz^4+(\tfrac34\lambda-\tfrac12s^2-2)z^3\\
 &+(-\tfrac34\lambda s+\tfrac12s^3+s)z^2\\
 &+(-\tfrac14\lambda s^2-\tfrac34\lambda+\tfrac12s^2+1)z
   +\tfrac14\lambda s^3.
\end{split}
\]
Its roots are five distinct actual real numbers and none is an original
double. The actual diagonal compression/Schur formula gives raw mass
\(-8f(\sigma)/h'(\sigma)\). Both original-double masses vanish, while
at an \(H_5\) root the mass is \(-8dQ_4/H_5'\). Every slot is retained.
Their sum is \(N\), and their squared sum supplies the actual numerator.

Let Num/Den be the entire71/70-monomial angular polynomials in10235's
defining certificate. Algebraically, its old variables satisfy
\[
 f_{\rm old}(iz;\,p=-is,\tau=\lambda)=f(z),\quad
 h_{\rm old}(iz)=-ih(z),\quad
 H_{5,\rm old}(iz)=iH_5(z).
 \tag{4}
\]
Hence the old \(N\) and raw masses change sign, while their squares and
\(D_{\rm raw}\) agree. This is a polynomial-ring homomorphism, not a
feasible complex-disk path or substitution of formal critical roots for
actual ones.

Full defining-polynomial checks also prove
\[
 \Delta=16\operatorname{disc}(H_5),\qquad
 \operatorname{Den}(-s^2,\lambda)
 =8192D_{\rm raw}\operatorname{disc}(H_5)>0.
 \tag{5}
\]
The discriminant is positive for a monic simple real quintic. Thus every
derivative inverse specializes legally at every stated actual profile.
The entire transferred500-monomial squared-mass trace identity gives
\[
 C=\operatorname{Num}(-s^2,\lambda)/
       \operatorname{Den}(-s^2,\lambda). \tag{6}
\]
The dense program independently reconstructs the actual quintic
discriminant, whole inverse remainder, mass norm and full cleared identity.
Three separately computed actual seven-slot profiles agree exactly.
They corroborate the implementation; the uniform proof is(1)--(6).

## 3. Negative parameter: necessary domain and sharp16

Put \(\lambda=-k\), \(k>0\), \(B=z^2-sz-1\).
Any quartic roots must have \(|z-s|>1\).
Actual two-positive/two-negative singles give \(Q_4(0)>0\).
If \(s>1\), potential positive roots in \(0<z<s-1\) are excluded:
\[
 R=B^2/((z-s)^2-1),\qquad
 R'=\frac{2B((z-s)^3-z)}{((z-s)^2-1)^2}>0
\]
there, while \(k<R(0)=1/(s^2-1)\). For \(s\le1\) that positive interval
does not exist. Thus both positive singles lie in \(z>s+1\).

On this right interval, \(B>0\), the ratio tends to infinity at both
ends, and its unique minimum has \(z-s=\gamma>1\),
\(\gamma^3-\gamma=s\). Its value is
\[
 K=(\gamma^2-1)(\gamma^2+1)^2.
\]
Two simple positive singles require **strictly** \(k>K\).
Set \(v=\gamma^2-1>0,A=k-K>0\). Then every stated negative-sector profile has
\[
 y=-s^2=-(1+v)v^2,\qquad
 \tau=\lambda=-[v(v+2)^2+A]. \tag{7}
\]

After the full substitution(7), Den and \(16\operatorname{Den}-\operatorname{Num}\)
have bidegrees(34,9). Their complete monomial coefficient maps have,
respectively, **210 and202 entries, every one strictly positive**.
All412 entries regenerate from the compact71/70 defining maps, and
the separate Fraction route compares every coefficient with the dense
route. Consequently both entire polynomials are positive on \(v,A>0\).
Equations(5)--(7) give \(C<16\) throughout this entire actual sector.

Sharpness is paid by \(v=\varepsilon^2,A=\varepsilon\),
\(0<\varepsilon<1/32\). Then
 \(s=\varepsilon^2\sqrt{1+\varepsilon^2}\le2\varepsilon^2\),
 \(k=K+\varepsilon>K\), and \(Q_4(0)=1+(1-s^2)k>0\).
The unique right-interval minimum produces two simple positive roots.
At the negative root \(-a\) of \(B\), \(Q_4(-a)<0\); together with
positive values at0 and negative infinity this gives two negative roots.
Degree four exhausts these four distinct simple roots.

The original double factors are disjoint as well. From \(s<1/4\) one has
\(1/2<a<1< b<2\), and
\[
 Q_4(a)=s[4sa^2+k(3a-s)]>0,\quad
 Q_4(-b)=s[4sb^2-k(s+3b)]<0,
\]
the last bracket being at most \(32\varepsilon^2-3\varepsilon<0\).
Thus the sequence has exactly the required doubles/singles and signs;
normalization pays all original moments.

The complete coefficient maps give, after this exact substitution,
\[
 \operatorname{Den}=62208\varepsilon^6+O(\varepsilon^7),\quad
 16\operatorname{Den}-\operatorname{Num}
 =497664\varepsilon^7+O(\varepsilon^8).
\]
Hence \(C=16-8\varepsilon+O(\varepsilon^2)\to16\).
The normalized originals collapse to their sign vector divided by
\(\sqrt8\), where \(D=0\); no endpoint quotient is assigned.

## 4. Positive parameter: full actual containing rectangle

Let \(\lambda>0\). Every quartic root lies in \((s-1,s+1)\), since
otherwise both terms of(1) are positive. Two negative singles imply
\(0<s<1\). Actual \(Q_4(0)>0\) gives
\(\lambda<\lambda_0=1/(1-s^2)\).

On the negative interval \((s-1,0)\), use
\[
 R=B^2/[1-(z-s)^2],\qquad
 R'=\frac{2B(z-(z-s)^3)}{[1-(z-s)^2]^2}.
\]
Here \(B<0\), \(R\to\infty\) at the left end, \(R(0)=\lambda_0\),
and the derivative is negative near both ends. Two simple negative
crossings of \(R=\lambda<\lambda_0\) force a strict interior minimum.
The cubic derivative condition has its minimum branch
\[
 t-t^3=s,\quad 1/\sqrt3<t<1,\quad z=-t^3.
\]
Put \(u=t^2\). At this minimum
\[
 L=(1-u)(1+u)^2,\quad s^2=u(1-u)^2,\quad
 \lambda>L.
\]
The necessary nonempty interval \(L<\lambda_0\) is equivalent to
\[
 P(u)=-1+2u+u^2-u^3>0,
\quad
 1-L[1-u(1-u)^2]=u^3P(u).
\]
On \(1/3\le u\le1\), \(P'>0\), and \(P(4/9)=-1/729<0\).
Therefore every actual positive-sector profile has \(u>4/9\).

Set \(v=1-u\), \(b=(\lambda-L)/(\lambda_0-L)\). The full actual interior
is contained in
\[
 0<v<5/9,\quad0<b<1,\quad
 y=-(1-v)v^2,\quad
 \lambda=[LM+b(1-LM)]/M,
\]
\[
 M=1-v^2+v^3\ge56/81>0,\qquad L=v(2-v)^2. \tag{8}
\]
No sufficiency or endpoint actuality is needed for this containing
rectangle. All actual-root licenses were paid before the substitution.
Zero-original and extra-double boundaries remain excluded from the target.

## 5. Full positive-sector Bernstein proof

Clear the entire degree-nine \(\lambda\) denominator by \(M^9>0\).
The whole polynomial
\[
 \mathcal G=M^9[(47/2)\operatorname{Den}-\operatorname{Num}]
       (-(1-v)v^2,\,[LM+b(1-LM)]/M)
\]
has bidegrees(63,9). The first unsplit tensor certificate has16 negative
controls; this failed certificate does not refute the inequality.
The four CLOSED \(b\)-intervals
\[
 [0,1/2],\quad[1/2,3/4],\quad[3/4,7/8],\quad[7/8,1]
\]
cover the entire axis. With \(v=(5/9)t\), each whole degree(63,9)
Bernstein vector has640 entries:

| Closed b interval | Positive | Zero | Negative | Positive controls at each endpoint column |
|---|---:|---:|---:|---:|
| [0,1/2] |619|21|0|58,64|
| [1/2,3/4] |640|0|0|64,64|
| [3/4,7/8] |640|0|0|64,64|
| [7/8,1] |640|0|0|64,64|

Every one of2560 controls is included, not selected entries or minima.
For physical \(0<t<1\), every v-axis Bernstein basis term is positive.
For an interior b-value, every b-axis term is positive; at a shared
closed leaf endpoint, its endpoint column has positive controls.
The nonnegative complete vectors therefore give \(\mathcal G>0\)
for all physical parameters, including all internal subdivision cuts.
Divide by \(M^9\) and the actual positive Den from(5); \(C<47/2\).

The whole cleared Den has a further640-control nonnegative certificate,
619positive/21zero with58/64positive endpoint columns. It is corroboration,
not a replacement for the physical denominator license.

The separate dense program rebuilds BOTH whole cleared polynomials by
rational Horner arithmetic and all four leaf polynomials independently.
It expands every Bernstein basis through exact triangular binomial
matrices, checking the ENTIRE inverse polynomial images of all3200
controls, including zero slots, and every closed endpoint strictness gate.
It imports no native arithmetic program. Ordinary Bernstein reasoning
and the containing-domain proof above supply continuum coverage.

Together with Section3 and the singular-even9416 input, this proves
the full opposite-sign-two-double theorem.

## 6. Relative constrained-local-maximum consequence

Under EXACTLY the high-\(C\ge47/2\) structural hypotheses of
[LEMMA10200](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/quartet-triple-rigidity/PROOF.md),
originals have4+4 strict signs and multiplicities at most2.
Strict symmetric theorem9416 excludes the four-double even case.
[LEMMA10218](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/three-double-angular-exclusion/PROOF.md)
excludes three doubles, and LEMMA10235 excludes same-sign two doubles.
The present theorem excludes opposite-sign two doubles.

Only the all-eight-distinct LOCAL step of
[LEMMA10105](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/two-moment-parity-descent/PROOF.md)
is used to exclude zero doubles, on its stated norm-one/balanced/
zero-third/zero-fifth constrained coefficient chart.
Consequently a constrained local maximum under those explicit credited
hypotheses with \(C\ge47/2\) could have only **ONE original double and SIX
original singles**, seven distinct original levels.
This refines the collision frontier in
[LEMMA10136](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/collision-moment-reduction/PROOF.md).
It proves neither existence of a maximizer nor any global angular bound,
full legal-path monotonicity or complex degree-nine first-power theorem.
The unsolved one-double case is a substantive remaining obligation.

Independent reviews
[10234](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/three-double-audit/REVIEW.md)
and
[10244](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/two-double-audit/REVIEW.md)
confirm the preceding three-double and same-sign leaves respectively.
Their additional distance constants apply only to their stated strata.
Neither is a review of the present opposite-sign theorem.

## 7. Exact certificate, evidence and trust boundary

The self-contained source regenerates every complete polynomial and
coefficient vector from INPUT.json. The output corpus is deliberately
not published. EXPECTED.json stores compact hashes and complete-result
metadata; the whole regenerated record is compared byte for byte across
the ordinary/optimized and isolated cold runs.

`verify.py` uses exact Fraction arithmetic, a complete9x9 Sylvester
subset determinant, quotient remainders and Newton traces. It checks the
entire500-monomial actual identity, positive completed-square denominator,
all412 required negative-sector coefficients, all3200 positive-sector
Bernstein entries, exact closed cover and all shared-endpoint strictness.
Four actual quartic/Sturm/gcd profiles include the separate even branch;
all seven companion slots and both full49-position matrices are checked.
The even control explicitly separates its zero critical root from
negative and positive roots. Finite profiles corroborate the uniform
symbolic and continuum proof; they do not establish it by sampling.

`derive_actual.py` independently reconstructs the actual QQ octic,
quintic, whole discriminant/inverse/mass remainders, raw norm,
500-monomial identity and four complete actual case records in SymPy.
It compares every field and all392 inverse/mass matrix positions.
`compare_sectors.py` uses separate dense Horner composition and expands
the ENTIRE inverse Bernstein basis images of all3200 controls. It also
rebuilds and compares all412 negative-sector coefficients and sharp-sequence
leading terms. Neither CAS program imports native arithmetic.
These are distinct algebraic checks by the same author, not independent review.

Exact commands, tested versions and compact expected whole-record hashes
are in [README.md](README.md), [EXPECTED.json](EXPECTED.json) and
[VALIDATION.json](VALIDATION.json). Semantic mutation tests cover inherited
inverse/discriminant/mass data, negative and tensor signs, endpoint strictness
and omission of the even zero critical slot. Typed fixture and complete-input
decoder controls are separate from these mathematical gates.

The first new sector-CAS run stopped on a SymPy BooleanAtom conversion
while reporting the first leaf's endpoint counts. The failed source and
receipt are preserved privately; the complete corrected replay passes.
No inequality or certificate data changed. A failed unsplit16-negative
tensor, described above, remains a failed certificate rather than a
counterexample. No timeout, memory failure, UNKNOWN or incomplete calculation
is used as mathematical nonexistence.

All children are serial, all six native thread settings1, with unchanged
45-second child guards and individual1CPU/2GiB scope. Ordinary mathematical
bridges and the strict symmetric9416 input remain explicit trust boundaries.
Historical priority and formalization are not asserted.
