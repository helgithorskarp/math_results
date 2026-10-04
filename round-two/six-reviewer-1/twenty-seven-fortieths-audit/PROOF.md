# Independent finite reduction and a stronger actual annular gap

Actual six-reviewer-1 / independent mathematical reviewer, 2026-10-04.
Ordinary proof plus complete exact rational computation; unformalized.

## 1. The actual polynomial and its necessary channels

Let \(p\) have degree nine and all nine original zeros in the closed unit
disk. Mark a zero \(a\) with \(2/3\le |a|\le27/40\), and count all eight
critical points with multiplicity. A critical point equal to \(a\) gives
an infinite reciprocal sum and settles the claim. Otherwise rotate to
positive real \(a\), and set
\[
q_j=(a-\zeta_j)^{-1},\quad r_j=|q_j|,\quad F=\sum r_j,\quad
T=\sum(r_j-1)^2,\quad \mu=u+iv={1\over8}\sum q_j,\quad w=v^2,
\]
\[
E=\sum|q_j-1|^2,\quad \Pi=F-8u,\quad S=\sum|q_j-\mu|^2.
\]
Gauss--Lucas gives \(r_j\ge m(a)=1/(1+a)\). The exact elementary identities are
\[
E=T+2\Pi,\qquad S=E-8[(1-u)^2+w]
 =T+2F-8-8(u^2+w).
\]
Write \(p(z)=(z-a)\prod_{k=1}^8(z-z_k)\). Integrating its derivative, with
\(p'(a)=9/\prod q_j=\prod(a-z_k)\), gives
\[
O=9\int_0^1\prod_j(1-atq_j)\,dt=\prod_k z_k\prod_j q_j,\qquad
J=\int_0^1\prod_j[a+(1-a^2)tq_j]\,dt
 =\prod_k{1-az_k\over a-z_k}.
\]
The second integration normalizes as
\(J=a^9(\prod q_j)p(1/a)/(9(1-a^2))\).
Since
\(|1-az_k|^2-|a-z_k|^2=(1-a^2)(1-|z_k|^2)\ge0\),
\[
|J|\ge1,\qquad |O|\le\prod_jr_j.
\tag{1}
\]
There are eight factors in both identities. Other repeated original roots,
repeated critical points and arbitrary complex directions remain allowed.
These are necessary conditions; there is no tuple-to-polynomial converse.

## 2. Independent scalar entry and polar payments for \(F\le8\)

On a marked interval \([l,h]\subset[1/2,1)\), put
\(c=l+1-l^2-h\). For \(0\le x\le1\),
\[
h+cx-[a+(1-a^2)x]=(1-x)(h-a)+x(a-l)(a+l-1)\ge0.
\]
Triangle inequality and AM--GM, applied to all eight factors, show that
\(F\le37/5\) implies
\[
|J|\le\int_0^1[27/40+(197/360)(37/40)t]^8dt
={16240863702347095495808588445055801\over
16639583300553277440000000000000000}<49/50.
\]
The two independent representations of this complete integral are checked.

Here is the analytic basis of the polar estimates. Put
\(d=\sqrt{T/56}\), \(e_j=r_j-1\), and \(B=a+(1-a^2)t\).
When \(\sum e_j\le0\), every positive \(e_j\le7d\): Cauchy--Schwarz
on the other seven gives \(T\ge8e_j^2/7\).
For \(f(x)=\log(B+yx)\), its quadratic Hermite interpolant \(Q\)
at \(-d,-d,7d\) majorizes \(f\) throughout the positive-factor domain,
because its remainder has the sign of
\(f'''(\xi)(x+d)^2(x-7d)\). Its quadratic coefficient is nonpositive,
and its linear coefficient is at least \(3y/[4(B-yd)]\).
Summing \(Q(e_j)\), then exponentiating, yields
\[
\prod_j(B+ye_j)\le(B+7yd)(B-yd)^7
\exp\!\left[-{3y(8-F)\over4(B-yd)}\right].
\]
At \(T=0\) or \(y=0\) the conclusion is direct. Using
\[
|a+btq_j|^2=(a+btr_j)^2-2abt(r_j-\Re q_j),\qquad b=1-a^2,
\]
and \(\frac12\log(1-x)\le-x/2\), gives the additional phase loss
\(\exp[-abt\Pi/(B+btD)^2]\) for any upper bound \(D\) on \(e_j\).
Vanishing complex factors satisfy the estimate directly.

The uniform floor \(40/67\), fixed sum \(F\le8\) and nonnegative
increments above that floor give \(T\le56(27/67)^2=40824/4489\).
For a box \(a\in[A,H]\), \(T\in[L,U]\), \(F\le F_+\), \(\Pi\ge P\), set
\[
b_-=1-H^2,\ b_+=1-A^2,\ c=A+1-A^2-H,\quad
a_*=\min(A(1-A^2),H(1-H^2)),
\]
\[
\delta={\lfloor1024\sqrt{L/56}\rfloor\over1024},\quad
D=\min\!\left({\lceil256\sqrt{7U/8}\rceil\over256},
F_+-{7\over1+H}-1\right).
\]
Write \(\widehat B=H+ct\), \(\widehat C=H+b_+(1+D)t\),
\(M_B=H+c\), \(M_C=H+b_+(1+D)\),
\(\alpha=c/M_B\), \(\nu=b_+(1+D)/M_C\).
The positive reciprocal lower kernels are
\[
G_1={1\over M_B}\sum_{n=0}^4\alpha^n(1-t)^n,\qquad
G_2={1\over M_C^2}\sum_{n=0}^4(n+1)\nu^n(1-t)^n.
\]
Their ratios lie in \([0,1)\). All radial/denominator signs are paid.
The logarithmic derivative of
\((1+7x)(1-x)^7\) is nonpositive on \([0,1)\).
The envelope and this monotonicity therefore give
\[
|J|\le\int_0^1R(t)[1-K(t)+K(t)^2/2]\,dt,
\]
\[
R=[H+(c+7b_-\delta)t][H+(c-b_-\delta)t]^7,\qquad
K=a_*PtG_2+\tfrac34b_-(8-F_+)tG_1\ge0.
\tag{2}
\]
The exponential is bounded before its upper quadratic is introduced;
monotonicity of that quadratic is never assumed.

All 73 consecutive closed cells
\([k/8,\min((k+1)/8,40824/4489)]\), \(0\le k\le72\),
with \(P=\max(0,(23/5-U)/2)\), give (2) strictly below \(49/50\).
Thus \(|J|\ge49/50\), \(F\le8\) imply \(F>37/5\), \(E<23/5\),
\(u>51/80\), \(|\mu|\le1\), \(w<23/40\).
Every shared endpoint is covered.

For a joint \(E/T\) polar leaf, retain \(d\) itself in the closed rational
square-root enclosure of \([T_-/56,T_+/56]\). Use
\(\Pi\ge E_-/2-28d^2\ge0\) in (2), with the two radial factors retaining \(d\).
The complete product has degree at most 12 in \(d\), 18 in \(t\).
Its two independently reconstructed representations are literal eight-factor
monomial multiplication and separated \(d\) powers carrying Bernstein
\(t\) coefficients. All \(13\times19\) entries and all 13 integrals agree.
Translation to the \(d\)-interval and reconstruction in the Bernstein
basis give 13 controls whose maximum bounds the whole closed interval.

## 3. Complete complex origin and mean payments

For \(z_j=q_j-\mu\), centering gives \(\max|z_j|^2\le7S/8\).
Concentration of the remaining squared radii bounds their fourth, sixth
and eighth sums by \(25S^2/32,43S^3/64,1201S^4/2048\).
Cauchy--Schwarz gives the odd sums. Newton's identities, combined with
the subset Cauchy/Maclaurin estimate
\(|e_k(z)|\le\binom8k(S/8)^{k/2}\), yield the pre-quartic constants in
[check.py](check.py). No coefficient after order four is reoptimized.

For the quartic, on the real zero-sum Hilbert subspace,
\(e_4=S^2/8-p_4/4\) lies between \(-9S^2/128\) and \(3S^2/32\).
The real diagonal norm is exactly \(3/32\), attained at four equal
positive and four equal negative coordinates. The **real Hilbert Banach
symmetric norm identity**, an external ordinary theorem, bounds the
associated multilinear form \(L(x,x,y,y)\) by
\((3/32)\|x\|^2\|y\|^2\). After a unit rotation makes \(e_4(x+iy)\) real,
its real part is \(P(x)-6L(x,x,y,y)+P(y)\).
Writing \(X=\|x\|^2,Y=\|y\|^2\), its bound is
\((3/32)(X^2+6XY+Y^2)\le(3/16)(X+Y)^2\).
No real/complex norm equality is asserted for the complexification.
The seven paid final constants are
\[
(c_2,\ldots,c_8)=(1/2,151/512,3/16,1497/5120,7/128,363/65536,1/4096).
\]
The complete origin expansion is
\[
\prod_j(1-atq_j)=\sum_{k=0}^8e_k(z)(-at)^k(1-at\mu)^{8-k}.
\tag{3}
\]
Only \(e_1=0\) vanishes; all seven remainder orders remain.

For a box \((a,E,F,u,w)\in[A,H]\times[E_-,E_+]\times[F_-,F_+]
\times[L,U]\times[W_-,W_+]\), define
\[
s_m=\min(1,U^2+W_+,(F_+/8)^2),\quad s_\beta=\min(s_m,L^2+W_+),
\]
\[
S_+=\min(E_+-8[(1-U)^2+W_-],
T_++2F_+-8-8(L^2+W_-)).
\]
The first bounds the **actual** mean norm; \(s_\beta\) is only an envelope.
The difference
\((1-atL)^2-(1-atu)^2=at(u-L)[2-at(u+L)]\ge0\)
and the actual norm bound give
\(|1-at\mu|^2\le1-2aLt+a^2s_\beta t^2\).
Set \(A_0=\min(A,2L/s_\beta-H)\) and
\(\beta=1-2A_0Lt+A_0^2s_\beta t^2\).
Convexity in \(a\) and \(2L\ge(A_0+H)s_\beta\) give a bound on the
entire marked interval, including both endpoints. Every anchor, sign and
square-root rounding is checked. In particular,
\[
\sqrt\beta\le Q(t)=1-A_0Lt+
{A_0^2(s_\beta-L^2)t^2\over2(1-A_0L)}.
\]
Use \(H_k=\beta^{(8-k)/2}\) for even \(k\), and
\(H_k=\beta^{(7-k)/2}Q\) for odd \(k\).
With upward \(1/4096\)-root bounds \(d_m,d_\beta,d_S\),
integration of the diagonal and all seven terms of (3) gives
\[
|O|\ge{1-d_\beta\beta(1)^4\over H d_m}
-9\sum_{k=2}^8H^kc_kS_+^{\lfloor k/2\rfloor}d_S^{k\bmod2}
\int_0^1t^kH_k(t)\,dt.
\tag{4}
\]
The denominator uses \(s_m\), not \(s_\beta\).
Every whole coefficient vector and integral is compared in monomial and
Bernstein representations before taking a score.

For a retained-mean leaf, choose
\[
A_0=\min(A,2L/(L^2+W_+)-H,2U/(U^2+W_+)-H).
\]
Concavity in \(u\) pays both anchor endpoints and then the whole interval.
Use \(\beta(u,t)=1-2A_0ut+A_0^2(u^2+W_+)t^2\), and the corresponding
positive-square upper root with denominator \(2(1-A_0U)\).
Separately pay **both** polynomial energy channels
\[
\overline S_E(u)=E_+-8[(1-u)^2+W_-],\qquad
\overline S_J(u)=T_++2F_+-8-8(u^2+W_-).
\]
Their domains, endpoint maxima and nonnegativity are checked independently.
For each channel the complete seven \(9\times10\) matrices and all
integrated coefficients reconstruct (4) as a degree-eight polynomial.
All nine Bernstein controls bound it below.
Alternatively bound the actual norm by
\(|\mu|\le u+W_+/(2L)\), set \(d(u)=H[u+W_+/(2L)]>0\),
and clear this denominator in
\(P(u)=N(u)-d(u)[1+R(u)]\).
All ten degree-nine controls are paid. For \(p_{\min}\ge0\) use
\(1+p_{\min}/d(U)\); for \(p_{\min}<0\) use
\(1+p_{\min}/d(L)\). Both whole-\(u\) bounds are valid; their maximum is
valid. All \(10\times10\) cleared remainder entries are compared.

## 4. New actual product payment and the exhaustive closed tree

For \(0<x\le R\), \(R\ge1\), the derivative of
\(f=x-1-(x-1)^2/(2R)-\log x\) obeys
\[
Rx f'(x)=(x-1)(R-x).
\]
Since \(f(1)=0\), its sign on both sides of 1 proves \(f\ge0\).
Thus \(\prod r_j\le\exp[-(8-F)-T/(2R)]\) for \(F\le8\).
On a tightened box put \(m=1/(1+H)\). The two independent upper caps are
\[
r_j\le F_+-7m,\qquad
r_j\le F_+/8+
\sqrt{\tfrac78[T_+-(8-F_+)^2/8]}.
\]
The latter follows from zero-sum radial variance and monotonicity in
\(F\le8\). Use the rational upward root in the second cap and set
\(R=\max(1,\min(\text{caps}))\), \(z=8-F_++T_-/(2R)\ge0\).
All five positive terms of the lower exponential expansion give
\[
|O|\le\prod r_j\le C_{\rm box}
={1\over1+z+z^2/2+z^3/6+z^4/24}.
\tag{5}
\]
The full formal derivative, both caps, square bracket and complete
polynomial/Horner exponential sum and reciprocal direction are checked
on **every** one of the 240 leaves.

The root enclosure is
\([2/3,27/40]\times[0,23/5]\times[37/5,8]\times[51/80,1]\times[0,23/40]\).
Four ordered necessary intersections and the exact \(T\)-bounds in
[check.py](check.py) follow from the identities in section 1, triangle
inequality and the radius floor. Every endpoint only tightens.
The radius upper variance is increasing in \(F\) on every used box.

[COVER.json](COVER.json) is exposed author data, not a verdict or a search
oracle. It is a full 479-node tree with 239 strict rational midpoint cuts,
240 closed leaves and maximum depth 17. Each cut is a midpoint of a
tightened axis **inside the original raw parent**; the two closed raw
children exhaust that parent and retain every other raw axis.
All listed/reachable paths agree and all shared faces remain.
There are no missing branches or discarded tightened complements.

| Cases | Leaves | Independently paid inequality |
|---|---:|---|
| Scalar/retained origin |95/14|lower \(>10001/10000\)|
| Standard/joint polar |8/95|upper \(<99999/100000\)|
| Scalar/retained actual-product origin |27/1|lower \(>C_{\rm box}+1/100000\)|

Equations (1)--(5) make each leaf contradictory. Legacy origin leaves
also use AM--GM \(\prod r_j\le1\). Every whole polynomial comparison and
strict inequality precedes a fingerprint. Therefore \(F\le8\) is excluded
on the complete new closed annulus.

## 5. Freshly proved stronger annular gap \(2^{-17}\)

Suppose an actual tuple has \(F=8+\Delta\), \(0<\Delta\le\epsilon=2^{-17}\).
The preceding argument excludes \(F\le8\). Put \(m=m(a)\) and
\[
h_j={\Delta(r_j-m)\over F-8m},\qquad
q'_j=(1-h_j/r_j)q_j.
\]
Then \(0\le h_j\le r_j-m\), \(\sum h_j=\Delta\),
\(r'_j\ge m\), \(F'=8\), \(\|q-q'\|_1=\Delta\).
Every point on this radial segment retains the same floor and mass at most
\(8+\epsilon\). The clipped tuple need not be actual.

In the derivative with respect to a slot \(q_j\), its **seven remaining
radii** have sum at most \(8+\epsilon-m_0\), \(m_0=40/67\).
Set \(M=(8+\epsilon-m_0)/7\), \(h=27/40\), \(b_+=5/9\).
Triangle inequality and AM--GM on exactly those seven factors give
\[
L_J\le b_+\int_0^1t(h+b_+Mt)^7dt<3/5,\qquad
L_O\le9h\int_0^1t(1+hMt)^7dt<59.
\tag{6}
\]
[refine.py](refine.py) reconstructs all eight coefficients of each seventh
power by literal multiplication and separate binomial coefficients, and
integrates each complete weighted polynomial in two ways.
Thus \(|J(q')|\ge1-(3/5)\epsilon>49/50\). Entry section 2 puts \(q'\)
in the same complete root enclosure.

Let \(P=\prod r_j,P'=\prod r'_j\). Full eight-factor AM--GM gives
\[
P/P'\le A=(1+\epsilon/(8m_0))^8,\qquad P'\le1.
\]
The actual identity (1) and (6), retaining the whole product ratio, imply
\[
|O(q')|\le P'+\ell,\qquad \ell=A-1+59\epsilon<1/2000.
\tag{7}
\]
The complete rational eighth power is checked, not a first-order
approximation. Every defining leaf surplus is freshly recomputed:
\[
\min(\text{109 ordinary origin lower bounds}-1)>1/2000,
\]
\[
\min(\text{28 product origin lower bounds}-C_{\rm box})>1/400,
\qquad
\min(1-\text{103 polar upper bounds})>1/40000.
\tag{8}
\]
Also \((3/5)\epsilon<1/40000\).
On a product leaf (5) applies to the clipped radii, so \(P'\le C_{\rm box}\).
Equations (6)--(8) contradict every whole defining leaf, including each
retained-mean leaf. No clipped-feasibility converse is needed.
Consequently, for **every** actual polynomial under section 1,
\[
\boxed{\sum_{j=1}^8|a-\zeta_j|^{-1}>8+2^{-17}
\quad\text{when }2/3\le|a|\le27/40.}
\]
This improves the target's numeric gap by 256. It says nothing about the
optimal gap or a wider marked interval. A failed \(2^{-16}\) payment with
these ceilings is only a limitation of these estimates.

## 6. Precisely retained lower-disk dependency and trust

Only combining the lower \(|a|\le2/3\) conclusion of LEMMA10240 gives
\(F>8\) throughout \(|a|\le27/40\). No whole-lower-disk numeric gap is
inferred. Prior REVIEW10250 confirms that lower leaf relative to its
stated lower10216 dependency; this review does not re-audit that ancestry.

The scalar, Hermite, complex-moment, Hilbert, Bernstein, original-root
communication and clipping arguments above are ordinary analytic proofs.
The general real Hilbert Banach identity and Gauss--Lucas remain ordinary
external inputs, not finite-code theorems. All finite work uses exact
integers/Fractions; no float, root solver or optimizer is a premise.
Programs are openly adapted from this reviewer's earlier10250 engine.
Current author programs, native EXPECTED and private records were never
inspected/imported/run. Written original/proof and exposed raw tree were
read, so this is an open audit rather than a blind replication.
Generated complete records are outputs and remain private, never inputs.
